"""TRELLIS Centralized Policy Engine & ABAC Evaluator.

Implements can(subject, action, resource, context) driven by docs/security/PERMISSION_MATRIX.json
under strict Default-Deny.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from fastapi import Depends, HTTPException, Request, status

from app.api.deps import get_current_user_claims


def _resolve_matrix_path() -> Path:
    """Locate docs/security/PERMISSION_MATRIX.json dynamically."""
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        candidate = parent / "docs" / "security" / "PERMISSION_MATRIX.json"
        if candidate.exists():
            return candidate
    # Fallback to standard scratch path
    return Path("/docs/security/PERMISSION_MATRIX.json")


class PolicyMatrixRegistry:
    """Singleton cache loading and indexing PERMISSION_MATRIX.json."""

    def __init__(self) -> None:
        self.matrix_path = _resolve_matrix_path()
        self.rules: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
        self.load()

    def load(self) -> None:
        if not self.matrix_path.exists():
            return

        with open(self.matrix_path, encoding="utf-8") as f:
            data = json.load(f)

        # Index: self.rules[resource][action][role] = grant_details
        for res_rule in data.get("rules", []):
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
        if "author != subject" in condition and context.get("author_id") == subject.user_id:
            return False

        # Scope boundary checks
        scope = grant.get("scope", "NONE")

        if scope == "ORGANIZATION":
            target_org = context.get("org_id", subject.org_id)
            if target_org == subject.org_id:
                return True

        elif scope == "OWN":
            target_user = context.get("target_user_id", subject.user_id)
            if target_user == subject.user_id:
                return True

        elif scope == "TEAM_DIRECT":
            # Manager viewing direct report
            is_direct_report = context.get("is_direct_report", False)
            if is_direct_report or context.get("target_user_id") == subject.user_id:
                return True

        elif scope == "COHORT":
            # Trainer or peer within assigned cohort
            target_cohort = context.get("cohort_id", subject.cohort_id)
            if target_cohort and target_cohort == subject.cohort_id:
                return True

        elif scope in {"BLIND_GRADING", "ANONYMIZED_AGGREGATE"}:
            return True

    # Default-Deny fallback
    return False


def require_permission(action: str, resource: str) -> Any:
    """FastAPI route dependency enforcing permission check against current user context."""

    def dependency(
        request: Request,
        claims: dict[str, Any] = Depends(get_current_user_claims),
    ) -> UserContext:
        user_ctx = UserContext(
            user_id=claims.get("sub", ""),
            org_id=claims.get("org_id", ""),
            roles=claims.get("roles", ["EMPLOYEE"]),
        )

        # Context extracted from request query or path params if present
        context = {
            "org_id": user_ctx.org_id,
            "target_user_id": request.path_params.get("user_id", user_ctx.user_id),
            "author_id": request.query_params.get("author_id"),
            "cohort_id": request.query_params.get("cohort_id"),
        }

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
