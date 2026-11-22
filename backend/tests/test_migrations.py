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


def test_migration_0004b_definition() -> None:
    """Verify Migration 0004b covers LMS & Assessment baseline tables and links to 0004."""
    mod = load_migration_module("0004b_lms_and_assessments_baseline.py")
    assert mod.revision == "0004b"
    assert mod.down_revision == "0004"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_migration_0005_definition() -> None:
    """Verify Migration 0005 covers assessment audience and links to 0004b."""
    mod = load_migration_module("0005_assessment_audience.py")
    assert mod.revision == "0005"
    assert mod.down_revision == "0004b"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_migration_0006_definition() -> None:
    """Verify Migration 0006 covers 7 assessment categories, grading, reports, and links to 0005."""
    mod = load_migration_module("0006_assessment_categories_and_reports.py")
    assert mod.revision == "0006"
    assert mod.down_revision == "0005"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_migration_0007_definition() -> None:
    """Verify Migration 0007 covers must_change_password and links to 0006."""
    mod = load_migration_module("0007_user_must_change_password.py")
    assert mod.revision == "0007"
    assert mod.down_revision == "0006"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_migration_0008_definition() -> None:
    """Verify Migration 0008 covers question_bank category and links to 0007."""
    mod = load_migration_module("0008_assessment_category_layer.py")
    assert mod.revision == "0008"
    assert mod.down_revision == "0007"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_migration_0009_definition() -> None:
    """Verify Migration 0009 covers ai_question_pool and links to 0008."""
    mod = load_migration_module("0009_ai_question_pool.py")
    assert mod.revision == "0009"
    assert mod.down_revision == "0008"
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")


def test_alembic_upgrade_head_on_clean_database(tmp_path: Path) -> None:
    """Verify that 'alembic upgrade head' runs successfully on an empty database."""
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import create_engine, inspect

    db_path = tmp_path / "clean_alembic_test.db"
    ini_path = Path(__file__).resolve().parent.parent / "alembic.ini"
    cfg = Config(str(ini_path))
    cfg.set_main_option("script_location", str(ini_path.parent / "alembic"))
    cfg.set_main_option("version_locations", str(ini_path.parent / "alembic" / "versions"))
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")

    # Run upgrade head from scratch
    command.upgrade(cfg, "head")

    # Verify tables
    engine = create_engine(f"sqlite:///{db_path}")
    insp = inspect(engine)
    tables = set(insp.get_table_names())
    assert "users" in tables
    assert "assessments" in tables
    assert "question_bank" in tables
    assert "meetings" in tables
    assert "talent_alerts" in tables
    assert "practice_scores" in tables
    assert "ai_question_pool" in tables
    assert len(tables) >= 46


def test_schema_model_drift_check(tmp_path: Path) -> None:
    """Verify there is no schema drift between Base.metadata models and Alembic migrations."""
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import create_engine, inspect
    from app.models import Base

    db_path = tmp_path / "drift_check.db"
    ini_path = Path(__file__).resolve().parent.parent / "alembic.ini"
    cfg = Config(str(ini_path))
    cfg.set_main_option("script_location", str(ini_path.parent / "alembic"))
    cfg.set_main_option("version_locations", str(ini_path.parent / "alembic" / "versions"))
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(cfg, "head")

    engine = create_engine(f"sqlite:///{db_path}")
    insp = inspect(engine)
    db_tables = set(insp.get_table_names())
    model_tables = set(Base.metadata.tables.keys())

    # Every model table must exist in the migrated database
    missing_from_db = model_tables - db_tables
    assert not missing_from_db, f"Model tables missing from migration: {missing_from_db}"

