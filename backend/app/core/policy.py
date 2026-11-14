"""TRELLIS Centralized Policy Engine & ABAC Evaluator.

Implements can(subject, action, resource, context) driven by docs/security/PERMISSION_MATRIX.json
under strict Default-Deny with database-derived entity scope resolution.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_claims, get_db
from app.models import EmploymentRecord, Skill, User


def _resolve_matrix_path() -> Path:
    """Locate docs/security/PERMISSION_MATRIX.json dynamically."""
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        candidate = parent / "docs" / "security" / "PERMISSION_MATRIX.json"
        if candidate.exists():
            return candidate
    return Path("docs/security/PERMISSION_MATRIX.json")


class PolicyMatrixRegistry:
    """Singleton cache loading and indexing PERMISSION_MATRIX.json.

    Invariant: Startup MUST fail if the matrix file cannot be loaded or is invalid.
    """

    def __init__(self, matrix_path: Path | None = None) -> None:
        self.matrix_path = matrix_path or _resolve_matrix_path()
        self.rules: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
        self.load()

    def load(self) -> None:
        if not self.matrix_path or not self.matrix_path.exists():
            raise RuntimeError(
                f"FATAL: PERMISSION_MATRIX.json could not be loaded from '{self.matrix_path}'. "
                "TRELLIS Policy Engine cannot initialize under Default-Deny."
            )

        try:
            with open(self.matrix_path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:
            raise RuntimeError(
                f"FATAL: Failed to parse PERMISSION_MATRIX.json from '{self.matrix_path}': {exc}"
            ) from exc

        rules = data.get("rules", [])
        if not rules:
            raise RuntimeError(
                "FATAL: PERMISSION_MATRIX.json contains zero rules. Engine cannot start."
            )

        # Index: self.rules[resource][action][role] = grant_details
        self.rules.clear()
        for res_rule in rules:
            resource = res_rule["resource"]
            self.rules[resource] = {}
            for action, role_map in res_rule.get("actions", {}).items():
                self.rules[resource][action] = role_map


policy_registry = PolicyMatrixRegistry()


@dataclass
class UserContext:
    """Security subject context for authorization decisions."""

    user_id: str
    org_id: str
    roles: list[str]
    department: str | None = None
    reporting_line_id: str | None = None
    cohort_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)


# Direct identifier keys strictly forbidden during blind grading or anonymized aggregate evaluation
_CANDIDATE_PII_KEYS = {
    "candidate_name",
    "candidate_email",
    "candidate_user_id",
    "candidate_id",
    "employee_code",
    "user_id",
    "target_user_id",
}


def can(
    subject: UserContext,
    action: str,
    resource: str,
    context: dict[str, Any] | None = None,
) -> bool:
    """Centralized authorization decision evaluator.

    Evaluates permissions against the policy matrix under strict Default-Deny.
    Returns True if and only if an explicit grant exists matching subject scope and conditions.
    """
    context = context or {}

    # Check if resource and action are defined in the matrix
    action_rules = policy_registry.rules.get(resource, {}).get(action)
    if not action_rules:
        # Strict Default-Deny: unlisted (resource, action) tuple is forbidden
        return False

    for role in subject.roles:
        grant = action_rules.get(role)
        if not grant:
            continue

        # Invariant: Check if grant explicitly disallows action
        if grant.get("allowed") is False:
            return False

        # Invariant: Separation of Duties Checks
        # E.g. author != subject: creators cannot self-approve ideas or pathways
        condition = grant.get("condition", "")
        if "author != subject" in condition:
            author_id = context.get("author_id")
            if author_id and author_id == subject.user_id:
                return False

        # Scope boundary checks
        scope = grant.get("scope", "NONE")

        if scope == "ORGANIZATION":
            target_org = context.get("target_org_id") or context.get("org_id")
            return bool(target_org and target_org == subject.org_id)

        elif scope == "OWN":
            target_user = context.get("target_user_id", subject.user_id)
            if target_user == subject.user_id:
                return True

        elif scope == "TEAM_DIRECT":
            # Manager viewing direct report; derived server-side
            is_direct_report = context.get("is_direct_report", False)
            target_user = context.get("target_user_id")
            if is_direct_report or target_user == subject.user_id:
                return True

        elif scope == "COHORT":
            # Trainer or peer within assigned cohort
            target_cohort = context.get("cohort_id")
            user_in_cohort = context.get("is_in_cohort", False)
            if (target_cohort and target_cohort == subject.cohort_id) or user_in_cohort:
                return True

        elif scope == "BLIND_GRADING":
            # Real check: must be marked blind grading and MUST NOT expose candidate PII
            is_blind = context.get("is_blind_grading") is True
            is_anon = context.get("anonymized") is True
            has_pii = any(context.get(k) for k in _CANDIDATE_PII_KEYS if k in context)
            return bool(is_blind and is_anon and not has_pii)

        elif scope == "ANONYMIZED_AGGREGATE":
            # Real check: must be aggregate, anonymized, and meet k-anonymity (sample_size >= 5)
            is_agg = context.get("is_aggregate") is True
            is_anon = context.get("anonymized") is True
            sample_size = context.get("sample_size", 0)
            has_individual_id = any(context.get(k) for k in _CANDIDATE_PII_KEYS if k in context)
            return bool(is_agg and is_anon and sample_size >= 5 and not has_individual_id)

    # Default-Deny fallback
    return False


def resolve_server_side_context(
    db: Session,
    resource: str,
    resource_id: str | None,
    subject: UserContext,
) -> dict[str, Any]:
    """Derive entity attributes, separation-of-duties author, direct report line and cohort from DB."""
    resolved: dict[str, Any] = {
        "target_org_id": subject.org_id,
        "author_id": None,
        "is_direct_report": False,
        "is_in_cohort": False,
        "target_user_id": resource_id,
    }

    if not resource_id:
        return resolved

    if resource == "users":
        target_user = db.get(User, resource_id)
        if target_user:
            resolved["target_org_id"] = target_user.org_id
            resolved["target_user_id"] = target_user.id
            # Check manager hierarchy in DB
            emp = (
                db.execute(
                    select(EmploymentRecord).where(
                        EmploymentRecord.user_id == target_user.id,
                        EmploymentRecord.reporting_line_id == subject.user_id,
                    )
                )
                .scalars()
                .first()
            )
            if emp:
                resolved["is_direct_report"] = True

    elif resource == "organisations":
        resolved["target_org_id"] = resource_id

    elif resource == "skills":
        skill = db.get(Skill, resource_id)
        if skill:
            resolved["target_org_id"] = skill.org_id

    return resolved


def require_permission(action: str, resource: str) -> Any:
    """FastAPI route dependency enforcing permission check with server-side DB context."""

    def dependency(
        request: Request,
        claims: dict[str, Any] = Depends(get_current_user_claims),
        db: Session = Depends(get_db),
    ) -> UserContext:
        user_ctx = UserContext(
            user_id=claims.get("sub", ""),
            org_id=claims.get("org_id", ""),
            roles=claims.get("roles", ["EMPLOYEE"]),
        )

        resource_id = request.path_params.get("id") or request.path_params.get("user_id")

        # Resolve context strictly from the database, never query parameters
        context = resolve_server_side_context(db, resource, resource_id, user_ctx)

        if not can(user_ctx, action, resource, context):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "type": "https://errors.trellis.csm.tech/errors/forbidden",
                    "title": "Access Denied",
                    "status": 403,
                    "detail": f"Permission denied: Missing required permission '{resource}:{action}' for your role(s).",
                    "instance": str(request.url),
                },
            )
        return user_ctx

    return dependency
