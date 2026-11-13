"""TRELLIS Immutable Audit Logging Middleware & Interceptors."""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.deps import get_sync_engine
from app.core.security import decode_access_token
from app.models import AccessReceipt, AuditLog


class AuditLogMiddleware(BaseHTTPMiddleware):
    """FastAPI ASGI middleware intercepting state mutations and logging immutable audit events."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response: Response = await call_next(request)

        # Intercept state-mutating requests with successful HTTP status (2xx)
        if (
            request.method in {"POST", "PUT", "PATCH", "DELETE"}
            and 200 <= response.status_code < 300
        ):
            path = request.url.path

            # Skip high-frequency health probes or auth login (login logs internally)
            if (
                not path.endswith("/health")
                and not path.endswith("/login")
                and not path.endswith("/refresh")
            ):
                actor_id = None
                org_id = "default_org"

                # Extract actor from Authorization header if present
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    try:
                        token = auth_header.split(" ")[1]
                        claims = decode_access_token(token)
                        actor_id = claims.get("sub")
                        org_id = claims.get("org_id", "default_org")
                    except Exception:
                        pass

                # Derive resource from path segment
                segments = [s for s in path.split("/") if s and s != "api" and s != "v1"]
                resource = segments[0] if segments else "system"
                action_map = {
                    "POST": "create",
                    "PUT": "update",
                    "PATCH": "update",
                    "DELETE": "delete",
                }
                action = action_map.get(request.method, "mutation")

                client_ip = request.client.host if request.client else "127.0.0.1"
                user_agent = request.headers.get("User-Agent")

                try:
                    engine = get_sync_engine()
                    with Session(engine) as session:
                        audit_entry = AuditLog(
                            org_id=org_id,
                            actor_id=actor_id,
                            action=action,
                            resource=resource,
                            resource_id=segments[1] if len(segments) > 1 else None,
                            ip_address=client_ip,
                            user_agent=user_agent,
                            reason=f"HTTP {request.method} {path} completed with {response.status_code}",
                        )
                        session.add(audit_entry)
                        session.commit()
                except Exception:
                    # Never crash the client request if audit logging encounters a transient DB error
                    pass

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
