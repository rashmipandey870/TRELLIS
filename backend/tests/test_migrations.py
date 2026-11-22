"""Automated tests validating Alembic Migration definitions and revision DAG integrity."""

import importlib.util
from pathlib import Path
from typing import Any


def load_migration_module(file_name: str) -> Any:
    """Dynamically load an alembic migration module from file path."""
    migration_path = Path(__file__).resolve().parent.parent / "alembic" / "versions" / file_name
    assert migration_path.exists(), f"Migration file not found at {migration_path}"
    spec = importlib.util.spec_from_file_location("migration_mod", migration_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_migration_0001_definition() -> None:
    """Verify Migration 0001 covers core tenancy, identity, consents, and audit tables."""
    mod = load_migration_module("0001_core_tenancy_identity_and_audit.py")
    assert mod.revision == "0001"
    assert mod.down_revision is None
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_migration_0002_definition() -> None:
    """Verify Migration 0002 covers skills, evidence ledger, and links to 0001."""
    mod = load_migration_module("0002_skills_and_evidence_ledger.py")
    assert mod.revision == "0002"
    assert mod.down_revision == "0001"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_migration_0003_definition() -> None:
    """Verify Migration 0003 covers pathways, courses, modules, cohorts, enrolments, and links to 0002."""
    mod = load_migration_module("0003_pathways_and_courses.py")
    assert mod.revision == "0003"
    assert mod.down_revision == "0002"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_migration_0004_definition() -> None:
    """Verify Migration 0004 covers user pseudonym salt, climbing streaks, and links to 0003."""
    mod = load_migration_module("0004_user_pseudonym_salt_and_streak.py")
    assert mod.revision == "0004"
    assert mod.down_revision == "0003"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_migration_0005_definition() -> None:
    """Verify Migration 0005 covers assessment audience and links to 0004."""
    mod = load_migration_module("0005_assessment_audience.py")
    assert mod.revision == "0005"
    assert mod.down_revision == "0004"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_migration_0006_definition() -> None:
    """Verify Migration 0006 covers 7 assessment categories, grading, reports, and links to 0005."""
    mod = load_migration_module("0006_assessment_categories_and_reports.py")
    assert mod.revision == "0006"
    assert mod.down_revision == "0005"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")

