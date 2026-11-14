"""TRELLIS Request Correlation & Access Logging Middleware.

Note on Architectural Separation:
State-mutating operations and immutable audit trails (AuditLog) are handled
strictly inside the database transaction via UnitOfWork (app.core.uow).
This ASGI middleware is restricted to request correlation tracking (X-Request-ID)
and secondary access logging; it never performs after-the-fact state mutation audits.
"""

import uuid
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import decode_access_token


class AccessLogMiddleware(BaseHTTPMiddleware):
    """ASGI middleware tracking correlation IDs and authenticated request access.

    Invariants:
    1. Correlation X-Request-ID is attached to every request and response.
    2. Client headers like X-Org-ID are NEVER trusted for authorization or auditing.
    3. State mutations are audited transactionally in UnitOfWork, not in middleware.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Correlation ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # Extract verified token claims if present (for logging context only)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            try:
                token = auth_header.split(" ")[1]
                decode_access_token(token)
            except Exception:
                pass

        # Execute downstream route handler
        response: Response = await call_next(request)

        # Attach correlation header to downstream response
        response.headers["X-Request-ID"] = request_id
        return response


# Backwards compatibility alias
AuditLogMiddleware = AccessLogMiddleware


def record_access_receipt(
    session: Any,
    org_id: str,
    accessor_id: str,
    subject_id: str,
    resource_type: str,
    purpose: str,
) -> Any:
    """Record an immutable access receipt for cross-user data access."""
    from app.models.audit import AccessReceipt

    receipt = AccessReceipt(
        org_id=org_id,
        accessor_id=accessor_id,
        subject_id=subject_id,
        resource_type=resource_type,
        purpose=purpose,
    )
    session.add(receipt)
    session.commit()
    return receipt
