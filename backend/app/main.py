"""TRELLIS Main FastAPI Application Entrypoint."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.auth import router as auth_router
from app.core.audit_middleware import AuditLogMiddleware
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager handling startup and shutdown events."""
    # Startup
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

# Authentication & Identity Router
app.include_router(auth_router, prefix=settings.API_V1_STR)


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
