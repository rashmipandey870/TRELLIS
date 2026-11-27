"""Pytest Global Test Fixtures & In-Memory Isolation Configuration.

Guarantees tests NEVER connect to external or shared cloud databases.
"""

import os

# Enforce in-memory SQLite and dev environment before any application module is imported
os.environ["TRELLIS_ENV"] = "dev"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["DATABASE_MIGRATION_URL"] = "sqlite:///:memory:"

from app.core.config import settings

settings.TRELLIS_ENV = "dev"
settings.DATABASE_URL = "sqlite:///:memory:"
settings.DATABASE_MIGRATION_URL = "sqlite:///:memory:"
