"""TRELLIS Centralized Policy Engine & ABAC/RBAC Decision Point (ADR-0002).

Enforces Default-Deny, Multi-Role Resolution with Explicit-Deny Precedence,
Separation of Duties, and Scope Boundary Checks.

Architectural Note on Anonymization and Blind Grading:
The BLIND_GRADING and ANONYMIZED_AGGREGATE scopes in this policy engine serve
strictly as AUTHORISATION GATES. They verify whether the caller has the privilege
to request blind-graded or anonymized aggregate data. The query and data layer
(app.services.privacy_service) is responsible for strictly projecting away candidate PII
and enforcing k-anonymity (k >= 5) on returned record sets.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_claims, get_db
from app.models.auth import RefreshToken
from app.models.ledger import EvidenceRecord
from app.models.skill import Skill
from app.models.user import Consent, EmploymentRecord, Grant, User

_CANDIDATE_PII_KEYS = {
    "candidate_name",
    "candidate_email",
    "employee_code",
    "user_id",
    "sub",
    "full_name",
    "email",
    "target_user_id",
}


@dataclass(frozen=True)
class UserContext:
    """Subject context derived from validated JWT claims."""

    user_id: str
    org_id: str
    roles: list[str]
    cohort_id: str | None = None


class PolicyMatrixRegistry:
    """Loads and compiles docs/security/PERMISSION_MATRIX.json into fast in-memory lookup indices."""

    def __init__(self, matrix_path: Path | None = None) -> None:
        if matrix_path is None:
            # Locate docs/security/PERMISSION_MATRIX.json relative to repository root
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            matrix_path = base_dir / "docs" / "security" / "PERMISSION_MATRIX.json"

        if not matrix_path.exists():
            raise RuntimeError(
                f"FATAL: Permission matrix file could not be loaded; not found at {matrix_path}. "
                "TRELLIS cannot start without verified authorization matrix."
            )

        with open(matrix_path, encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as exc:
                raise RuntimeError(f"FATAL: Malformed JSON in permission matrix: {exc}") from exc

        self.version: str = data.get("version", "unknown")
        self.rules: dict[str, dict[str, dict[str, Any]]] = {}
        self._compile_matrix(data.get("rules", []))

    def _compile_matrix(self, rules: list[dict[str, Any]]) -> None:
        # Index: self.rules[resource][action][role] = grant_details
        for rule in rules:
            resource = rule["resource"]
            if resource not in self.rules:
                self.rules[resource] = {}
            for action, role_grants in rule.get("actions", {}).items():
                if action not in self.rules[resource]:
                    self.rules[resource][action] = {}
                for role, grant in role_grants.items():
                    self.rules[resource][action][role] = grant


# Singleton policy matrix loaded on startup; fails fast if matrix missing or invalid
policy_registry = PolicyMatrixRegistry()


def can(
    subject: UserContext,
    action: str,
    resource: str,
    context: dict[str, Any] | None = None,
) -> bool:
    """Centralized authorization decision evaluator.

    Evaluates permissions against the policy matrix under strict Default-Deny.
    Invariants:
    1. A user with multiple roles is evaluated against all of them.
    2. Explicit deny (allowed: false) on any matching role grant wins immediately.
    3. Separation of duties: creators/authors cannot approve or publish their own work.
       If author cannot be determined from database for approve/publish, request is DENIED.
    4. Scopes (OWN, TEAM_DIRECT, COHORT, ORGANIZATION, BLIND_GRADING, ANONYMIZED_AGGREGATE)
       are verified against server-side context.
    """
    context = context or {}

    # Check if resource and action are defined in the matrix
    action_rules = policy_registry.rules.get(resource, {}).get(action)
    if not action_rules:
        # Strict Default-Deny: unlisted (resource, action) tuple is forbidden
        return False

    has_explicit_allow = False

    for role in subject.roles:
        grant = action_rules.get(role)
        if not grant:
            continue

        # Invariant 1: Explicit deny wins immediately across all roles
        if grant.get("allowed") is False:
            return False

        # Invariant 2: Separation of Duties Checks
        condition = grant.get("condition", "")
        if "author != subject" in condition or action in {"approve", "publish"}:
            author_id = context.get("author_id")
            # If author cannot be determined from database for approve/publish, deny access
            if not author_id:
                return False
            # If author is attempting to approve/publish their own submission, deny immediately
            if author_id == subject.user_id:
                return False

        # Invariant 3: Scope boundary checks
        scope = grant.get("scope", "NONE")
        role_allowed = False

        if scope == "ORGANIZATION":
            target_org = context.get("target_org_id") or context.get("org_id")
            role_allowed = bool(target_org and target_org == subject.org_id)

        elif scope == "OWN":
            target_user = context.get("target_user_id") or subject.user_id
            role_allowed = bool(target_user == subject.user_id)

        elif scope == "TEAM_DIRECT":
            is_direct_report = context.get("is_direct_report", False)
            target_user = context.get("target_user_id")
            role_allowed = bool(is_direct_report or target_user == subject.user_id)

        elif scope == "COHORT":
            target_cohort = context.get("cohort_id")
            user_in_cohort = context.get("is_in_cohort", False)
            role_allowed = bool(
                (target_cohort and target_cohort == subject.cohort_id) or user_in_cohort
            )

        elif scope == "BLIND_GRADING":
            # Note: Authorisation gate only; data layer enforces PII stripping
            is_blind = context.get("is_blind_grading") is True
            has_pii = any(context.get(k) for k in _CANDIDATE_PII_KEYS if k in context)
            role_allowed = bool(is_blind and not has_pii)

        elif scope == "ANONYMIZED_AGGREGATE":
            # Note: Authorisation gate only; data layer enforces k>=5 and identifier removal
            is_agg = context.get("is_aggregate") is True
            sample_size = context.get("sample_size", 0)
            has_individual_id = any(context.get(k) for k in _CANDIDATE_PII_KEYS if k in context)
            role_allowed = bool(is_agg and sample_size >= 5 and not has_individual_id)

        if role_allowed:
            has_explicit_allow = True

    return has_explicit_allow


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

    if resource in {"evidence_records", "evidence", "evidence_ledger"}:
        rec = db.get(EvidenceRecord, resource_id)
        if rec:
            resolved["author_id"] = rec.user_id
            resolved["target_org_id"] = rec.org_id
            resolved["target_user_id"] = rec.user_id

    elif resource in {"users", "profiles"}:
        target_user = db.get(User, resource_id)
        if target_user:
            resolved["author_id"] = target_user.id
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

    elif resource == "consents":
        consent = db.get(Consent, resource_id)
        if consent:
            resolved["author_id"] = consent.user_id
            resolved["target_org_id"] = consent.org_id
            resolved["target_user_id"] = consent.user_id

    elif resource == "grants":
        grant = db.get(Grant, resource_id)
        if grant:
            resolved["author_id"] = grant.granted_by_id or grant.user_id
            resolved["target_org_id"] = grant.org_id

    elif resource == "employment_records":
        emp_rec = db.get(EmploymentRecord, resource_id)
        if emp_rec:
            resolved["author_id"] = emp_rec.user_id
            resolved["target_org_id"] = emp_rec.org_id
            resolved["target_user_id"] = emp_rec.user_id

    elif resource == "refresh_tokens":
        token = db.get(RefreshToken, resource_id)
        if token:
            resolved["author_id"] = token.user_id
            resolved["target_org_id"] = token.org_id
            resolved["target_user_id"] = token.user_id

    elif resource in {"skills", "skill_edges", "skill_levels", "role_requirements"}:
        skill = db.get(Skill, resource_id)
        if skill:
            resolved["target_org_id"] = skill.org_id

    elif resource == "pathways":
        from app.models.curriculum import Pathway

        pathway = db.get(Pathway, resource_id)
        if pathway:
            resolved["author_id"] = pathway.author_id
            resolved["target_org_id"] = pathway.org_id

    elif resource == "enrolments":
        from app.models.curriculum import Enrolment

        enrolment = db.get(Enrolment, resource_id)
        if enrolment:
            resolved["author_id"] = enrolment.user_id
            resolved["target_org_id"] = enrolment.org_id
            resolved["target_user_id"] = enrolment.user_id

    elif resource == "organisations":
        resolved["target_org_id"] = resource_id

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
