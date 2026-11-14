"""TRELLIS CI Test Suite: Route Unit-of-Work & Transactional Audit Enforcement.

Introspects app.routes and asserts that every state-mutating HTTP endpoint (POST, PUT, PATCH, DELETE)
either depends directly on get_uow (UnitOfWork) or is registered in an explicit, reviewed allowlist
(e.g., core authentication endpoints that commit in-transaction audits via auth_service).
"""

from typing import Any

from fastapi.routing import APIRoute

from app.api.deps import get_uow
from app.main import app

# Explicit, reviewed allowlist of mutating routes that perform audited transactions via domain services
REVIEWED_UOW_EXEMPT_ROUTES: dict[str, str] = {
    "/api/v1/auth/login": "Audits authentication flow atomically inside auth_service.login_flow",
    "/api/v1/auth/mfa/challenge": "Audits TOTP verification atomically inside auth_service.verify_mfa_challenge",
    "/api/v1/auth/mfa/setup": "Audits TOTP setup atomically inside auth_service.setup_totp_mfa",
    "/api/v1/auth/refresh": "Audits token rotation & reuse revocation atomically inside auth_service.rotate_refresh_token",
    "/api/v1/auth/logout": "Audits session revocation atomically inside auth_service.logout_session",
}


def _collect_all_api_routes(app_instance: Any) -> list[tuple[str, set[str], list[Any]]]:
    """Recursively collect (full_path, methods, list_of_dependency_callables) across all routes."""
    collected: list[tuple[str, set[str], list[Any]]] = []

    for route in app_instance.routes:
        if isinstance(route, APIRoute):
            methods = set(route.methods) - {"HEAD", "OPTIONS"}
            deps = _extract_dependencies(route.dependant)
            collected.append((route.path, methods, deps))
        elif hasattr(route, "original_router"):
            prefix = getattr(getattr(route, "include_context", None), "prefix", "")
            for sub_route in route.original_router.routes:
                if isinstance(sub_route, APIRoute):
                    methods = set(sub_route.methods) - {"HEAD", "OPTIONS"}
                    full_path = f"{prefix}{sub_route.path}".rstrip("/")
                    deps = _extract_dependencies(sub_route.dependant)
                    collected.append((full_path, methods, deps))

    return collected


def _extract_dependencies(dependant: Any) -> list[Any]:
    """Recursively collect dependency callables from a FastAPI Dependant object."""
    calls: list[Any] = []
    if dependant.call:
        calls.append(dependant.call)
    for sub in dependant.dependencies:
        calls.extend(_extract_dependencies(sub))
    return calls


def test_every_mutating_route_enforces_unit_of_work_or_reviewed_allowlist() -> None:
    """CI Check: Fails if any POST/PUT/PATCH/DELETE route lacks get_uow without reviewed allowlist."""
    all_routes = _collect_all_api_routes(app)
    mutating_methods = {"POST", "PUT", "PATCH", "DELETE"}

    violations: list[str] = []

    for path, methods, deps in all_routes:
        mutating = methods.intersection(mutating_methods)
        if not mutating:
            continue

        has_uow = get_uow in deps
        is_exempt = path in REVIEWED_UOW_EXEMPT_ROUTES

        if not has_uow and not is_exempt:
            violations.append(
                f"Route '{path}' with methods {mutating} lacks 'get_uow' dependency "
                f"and is not listed in REVIEWED_UOW_EXEMPT_ROUTES."
            )

    assert not violations, (
        "TRANSACTIONAL AUDIT ENFORCEMENT VIOLATION:\n"
        + "\n".join(f"  - {v}" for v in violations)
        + "\nEvery mutating endpoint MUST declare 'uow: UnitOfWork = Depends(get_uow)' or be explicitly justified in the allowlist."
    )


def test_unregistered_mutating_route_fails_enforcement() -> None:
    """Negative test proving introspection fails when an unauthorized mutating route is added."""
    from fastapi import APIRouter

    mock_router = APIRouter(prefix="/test-mutation")

    # Mutating route without get_uow and not on allowlist
    @mock_router.post("/unauthorized-action")
    def unauthorized_endpoint() -> dict[str, str]:
        return {"status": "unauthorized"}

    class MockApp:
        routes = [mock_router.routes[0]]

    mock_app = MockApp()
    all_mock_routes = _collect_all_api_routes(mock_app)
    path, methods, deps = all_mock_routes[0]

    assert get_uow not in deps
    assert path not in REVIEWED_UOW_EXEMPT_ROUTES
