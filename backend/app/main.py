"""TRELLIS Main FastAPI Application Entrypoint."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.admin import router as admin_router
from app.api.v1.auth import router as auth_router
from app.api.v1.coding import router as coding_router
from app.api.v1.home import router as home_router
from app.api.v1.learner import router as learner_router
from app.api.v1.mentor import router as mentor_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.pathways import router as pathways_router
from app.api.v1.practice import router as practice_router
from app.core.audit_middleware import AuditLogMiddleware
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager handling startup and shutdown events."""
    # Startup validation
    if not settings.DATABASE_URL:
        raise RuntimeError(
            "CRITICAL: DATABASE_URL is missing. Specify DATABASE_URL via environment variables or secret store."
        )

    # In production environments, verify isolated runner passes startup self-test
    if settings.TRELLIS_ENV != "dev":
        from app.services.code_runner import get_code_runner
        runner = get_code_runner()
        if hasattr(runner, "startup_self_test"):
            runner.startup_self_test()

    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.TRELLIS_ENV}]")
    print(f"Tagline: {settings.TAGLINE}")
    yield
    # Shutdown
    print(f"Shutting down {settings.PROJECT_NAME}")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="CSM Technology Learning & Knowledge Platform - Where every Tendril climbs",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_STR}/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Immutable Audit Logging Middleware
app.add_middleware(AuditLogMiddleware)

# Authentication & Domain Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(mentor_router, prefix=settings.API_V1_STR)
app.include_router(learner_router, prefix=settings.API_V1_STR)
app.include_router(coding_router, prefix=settings.API_V1_STR)
app.include_router(practice_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
app.include_router(home_router, prefix=settings.API_V1_STR)
app.include_router(pathways_router, prefix=settings.API_V1_STR)


@app.get(f"{settings.API_V1_STR}/health", tags=["Health"], status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, Any]:
    """Liveness probe and system health status endpoint."""
    return {
        "status": "ok",
        "app": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "version": settings.VERSION,
        "environment": settings.TRELLIS_ENV,
    }


@app.exception_handler(Exception)
async def global_rfc9457_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """RFC 9457 compliant problem details error handler for unhandled exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "type": "https://errors.trellis.csm.tech/errors/internal-server-error",
            "title": "Internal Server Error",
            "status": 500,
            "detail": "An unexpected error occurred while processing the request.",
            "instance": str(request.url),
        },
        headers={"Content-Type": "application/problem+json"},
    )
