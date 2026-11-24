"""TRELLIS Main FastAPI Application Entrypoint."""

import asyncio
import contextlib
import logging
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

logger = logging.getLogger(__name__)

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, Response

from app.api.v1.admin import router as admin_router
from app.api.v1.auth import router as auth_router
from app.api.v1.coding import router as coding_router
from app.api.v1.home import router as home_router
from app.api.v1.learner import router as learner_router
from app.api.v1.mentor import router as mentor_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.pathways import router as pathways_router
from app.api.v1.practice import router as practice_router
from app.api.v1.storage import router as storage_router
from app.core.audit_middleware import AuditLogMiddleware
from app.core.config import settings


async def _neon_keepalive_loop() -> None:
    """Background task that pings Neon PostgreSQL every 30 seconds to keep compute active and connection pool warm."""
    from sqlalchemy import text
    from app.api.deps import get_sync_engine
    while True:
        try:
            await asyncio.sleep(30)
            engine = get_sync_engine()
            def _ping() -> None:
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
            await asyncio.to_thread(_ping)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.debug("Neon heartbeat ping failed: %s", e)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager handling startup and shutdown events."""
    # Startup validation
    if not settings.DATABASE_URL:
        raise RuntimeError(
            "CRITICAL: DATABASE_URL is missing. Specify DATABASE_URL via environment variables or secret store."
        )

    # Warm up database connection with retry backoff for serverless/cold-start databases (e.g. Neon)
    from app.api.deps import get_sync_engine, warmup_database
    try:
        warmup_database(get_sync_engine(), max_retries=3, initial_delay=1.0)
        print("Neon PostgreSQL connection pool initialized and warmed up.")
    except Exception as e:
        print(f"Warning: Database warmup encountered error: {e}")

    # Launch background keepalive task so Neon never enters idle/suspended sleep
    heartbeat_task = asyncio.create_task(_neon_keepalive_loop())

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
    heartbeat_task.cancel()
    with contextlib.suppress(Exception):
        await heartbeat_task
    print(f"Shutting down {settings.PROJECT_NAME}")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="CSM Technology Learning & Knowledge Platform - Where every Tendril climbs",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_STR}/docs" if settings.TRELLIS_ENV in ("dev", "test") else None,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.TRELLIS_ENV in ("dev", "test") else None,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

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
app.include_router(storage_router, prefix=settings.API_V1_STR)


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


@app.get(f"{settings.API_V1_STR}/metrics", tags=["Health"], status_code=status.HTTP_200_OK)
async def metrics() -> dict[str, Any]:
    """Prometheus / telemetry health metrics endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.TRELLIS_ENV,
        "uptime_seconds": time.perf_counter(),
    }


@app.exception_handler(Exception)
async def global_rfc9457_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """RFC 9457 compliant problem details error handler for unhandled exceptions."""
    logger.exception("Unhandled server exception on %s: %s", request.url, exc)
    detail_msg = f"{type(exc).__name__}: {exc}" if settings.ENVIRONMENT == "dev" else "An unexpected error occurred while processing the request."
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "type": "https://errors.trellis.csm.tech/errors/internal-server-error",
            "title": "Internal Server Error",
            "status": 500,
            "detail": detail_msg,
            "instance": str(request.url),
        },
        headers={"Content-Type": "application/problem+json"},
    )
