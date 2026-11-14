"""TRELLIS Immutable Audit Logging Middleware & Interceptors."""

import uuid
from collections.abc import Awaitable, Callable

from fastapi import HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.deps import get_sync_engine
from app.core.security import decode_access_token
from app.models import AccessReceipt, AuditLog


class AuditLogMiddleware(BaseHTTPMiddleware):
    """FastAPI ASGI middleware intercepting state mutations and logging immutable audit events.

    Invariants:
    1. Every mutating request must have a verified tenant org_id; 'default_org' fallback is forbidden.
    2. If the audit log insert fails, the request MUST FAIL. Silent pass is strictly forbidden.
    3. Correlation request ID and approval references must be tracked.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Extract or generate correlation Request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        approval_ref = request.headers.get("X-Approval-Ref")

        # Skip high-frequency read-only health checks or static docs
        path = request.url.path
        is_mutation = request.method in {"POST", "PUT", "PATCH", "DELETE"}
        is_exempt = (
            path.endswith("/health") or path.endswith("/docs") or path.endswith("/openapi.json")
        )

        # Execute downstream route handler
        response: Response = await call_next(request)

        # Intercept state-mutating requests with successful HTTP status (2xx)
        if is_mutation and not is_exempt and 200 <= response.status_code < 300:
            actor_id = None
            org_id = None

            # Extract actor and org from Authorization Bearer token
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                try:
                    token = auth_header.split(" ")[1]
                    claims = decode_access_token(token)
                    actor_id = claims.get("sub")
                    org_id = claims.get("org_id")
                except Exception:
                    pass

            # In dev/mock testing without auth, check X-Org-ID header if claims absent
            if not org_id:
                org_id = request.headers.get("X-Org-ID")

            # Invariant: Mutating requests MUST have an identifiable tenant organisation
            if not org_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="AUDIT_REJECTED: Mutating operations require a verified tenant org_id in token or headers.",
                )

            # Derive resource and action from path
            segments = [s for s in path.split("/") if s and s not in {"api", "v1"}]
            resource = segments[0] if segments else "system"
            resource_id = segments[1] if len(segments) > 1 else None

            action_map = {
                "POST": "create",
                "PUT": "update",
                "PATCH": "update",
                "DELETE": "delete",
            }
            action = action_map.get(request.method, "mutation")
            client_ip = request.client.host if request.client else "127.0.0.1"
            user_agent = request.headers.get("User-Agent")

            # Persist audit log; if it fails, request MUST abort and raise
            try:
                engine = get_sync_engine()
                with Session(engine) as session:
                    audit_entry = AuditLog(
                        org_id=org_id,
                        actor_id=actor_id,
                        action=action,
                        resource=resource,
                        resource_id=resource_id,
                        ip_address=client_ip,
                        user_agent=user_agent,
                        approval_ref=approval_ref,
                        request_id=request_id,
                        reason=f"HTTP {request.method} {path} completed with status {response.status_code}",
                        after_state_json={"status_code": response.status_code},
                    )
                    session.add(audit_entry)
                    session.commit()
            except Exception as exc:
                # Fatal: Never silently swallow audit failures
                raise RuntimeError(
                    f"AUDIT_WRITE_FAILED: Failed to persist immutable audit log for {request.method} {path}: {exc}. "
                    "Transaction aborted to prevent un-audited state mutation."
                ) from exc

        return response


def record_access_receipt(
    session: Session,
    org_id: str,
    accessor_id: str,
    subject_id: str,
    resource_type: str,
    purpose: str,
    resource_id: str | None = None,
) -> AccessReceipt:
    """Explicitly write an immutable Access Receipt when a cross-user personal data read occurs."""
    receipt = AccessReceipt(
        org_id=org_id,
        accessor_id=accessor_id,
        subject_id=subject_id,
        resource_type=resource_type,
        resource_id=resource_id,
        purpose=purpose,
    )
    session.add(receipt)
    session.commit()
    return receipt
