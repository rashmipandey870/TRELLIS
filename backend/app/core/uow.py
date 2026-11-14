"""TRELLIS Unit of Work & Transactional Audit Management.

Guarantees atomic transaction boundaries: all mutations and their corresponding
immutable AuditLog entries are committed in the exact same database transaction.
If an audit write fails, the entire transaction is rolled back immediately.
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import Request
from sqlalchemy.orm import Session

from app.models.audit import AuditLog


class UnitOfWork:
    """Manages transactional boundaries and mandatory in-transaction audit logging.

    Invariants:
    1. Every mutating operation must record an AuditLog entry before commit.
    2. Tenant org_id must come strictly from verified JWT claims or verified database entity;
       client headers like X-Org-ID are strictly untrusted and forbidden.
    3. Commits are atomic: if any mutation or audit log write fails, the entire session rolls back.
    """

    def __init__(
        self,
        session: Session,
        request: Request | None = None,
        claims: dict[str, Any] | None = None,
    ) -> None:
        self.session = session
        self.request = request
        self.claims = claims or {}
        self.actor_id: str | None = self.claims.get("sub")
        self.org_id: str | None = self.claims.get("org_id")

        # Extract request correlation headers if available
        self.request_id: str = str(uuid.uuid4())
        self.approval_ref: str | None = None
        self.client_ip: str = "127.0.0.1"
        self.user_agent: str | None = None

        if request is not None:
            self.request_id = request.headers.get("X-Request-ID") or self.request_id
            self.approval_ref = request.headers.get("X-Approval-Ref")
            self.client_ip = request.client.host if request.client else "127.0.0.1"
            self.user_agent = request.headers.get("User-Agent")

        self._pending_audits: list[AuditLog] = []

    def record_audit(
        self,
        action: str,
        resource: str,
        resource_id: str | None = None,
        before_state: dict[str, Any] | None = None,
        after_state: dict[str, Any] | None = None,
        reason: str | None = None,
        org_id: str | None = None,
    ) -> AuditLog:
        """Stage an immutable audit record in the active transaction before commit."""
        effective_org_id = org_id or self.org_id
        if not effective_org_id:
            raise ValueError(
                "AUDIT_REJECTED: org_id cannot be determined from verified token claims or entity context."
            )

        audit_entry = AuditLog(
            org_id=effective_org_id,
            actor_id=self.actor_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=self.client_ip,
            user_agent=self.user_agent,
            request_id=self.request_id,
            approval_ref=self.approval_ref,
            reason=reason or f"Executed {action} on {resource}",
            before_state_json=before_state,
            after_state_json=after_state,
        )
        self.session.add(audit_entry)
        self._pending_audits.append(audit_entry)
        # Flush to catch constraints/errors immediately within the transaction
        self.session.flush()
        return audit_entry

    def commit(self) -> None:
        """Commit all mutations and staged audit records in a single atomic transaction.

        If any error occurs during commit, rollback immediately and re-raise.
        """
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def rollback(self) -> None:
        """Rollback active transaction and clear pending state."""
        self.session.rollback()

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
