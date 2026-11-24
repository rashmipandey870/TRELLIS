import asyncio
import socket
from logging.config import fileConfig

try:
    _orig_getaddrinfo = socket.getaddrinfo
    _NEON_FALLBACKS = {
        'ep-weathered-base-az6lrn9p.c-3.ap-southeast-1.aws.neon.tech': '52.76.128.157',
        'ep-weathered-base-az6lrn9p-pooler.c-3.ap-southeast-1.aws.neon.tech': '52.76.128.157',
        'c-3.ap-southeast-1.aws.neon.tech': '52.76.128.157'
    }
    def _neon_safe_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        try:
            return _orig_getaddrinfo(host, port, family, type, proto, flags)
        except socket.gaierror:
            if host in _NEON_FALLBACKS:
                return _orig_getaddrinfo(_NEON_FALLBACKS[host], port, family, type, proto, flags)
            raise
    socket.getaddrinfo = _neon_safe_getaddrinfo
except Exception:
    pass

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.core.config import settings
from app.models import Base

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target model metadata for 'autogenerate' support
target_metadata = Base.metadata

# Override URL with environment settings if available
db_url = config.get_main_option("sqlalchemy.url") or settings.DATABASE_MIGRATION_URL or settings.DATABASE_URL or "sqlite+aiosqlite:///:memory:"
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Execute migrations within an active database connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    configuration = config.get_section(config.config_ini_section, {})
    url = config.get_main_option("sqlalchemy.url") or ""
    configuration["sqlalchemy.url"] = url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = config.get_main_option("sqlalchemy.url") or ""
    if (
        url.startswith("sqlite://")
        or url.startswith("mysql+pymysql://")
        or url.startswith("postgresql+psycopg2://")
        or (url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"))
    ):
        from sqlalchemy import create_engine
        sync_url = url
        if sync_url.startswith("postgresql://") and not sync_url.startswith("postgresql+"):
            sync_url = sync_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        connect_args = {}
        if "neon.tech" in sync_url or "52.76.128.157" in sync_url:
            connect_args = {
                "options": "endpoint=ep-weathered-base-az6lrn9p",
                "hostaddr": "52.76.128.157",
            }
        connectable = create_engine(sync_url, poolclass=pool.NullPool, connect_args=connect_args)
        with connectable.connect() as connection:
            do_run_migrations(connection)
        connectable.dispose()
    else:
        asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
