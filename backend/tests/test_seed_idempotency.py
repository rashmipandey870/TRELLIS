import os
import sys
import tempfile
from pathlib import Path
import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session

# Ensure paths
backend_dir = Path(__file__).resolve().parent.parent
repo_root = backend_dir.parent
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "scripts"))

from app.models.base import Base
import app.models  # load all models
from seed_demo_pack import seed_demo_pack


def test_seed_demo_pack_is_strictly_idempotent():
    """
    Phase B3 Gate:
    Run seed_demo_pack twice on the database.
    Assert that a second run adds 0 rows to any table (row counts before == row counts after).
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        tmp_db_path = tmp_file.name

    db_url = f"sqlite:///{tmp_db_path}"
    engine = create_engine(db_url)

    try:
        # Create schema
        Base.metadata.create_all(bind=engine)

        # Run 1: Initial Seed
        with Session(engine) as session:
            counts_run1 = seed_demo_pack(session)

        # Inspect table row counts after Run 1
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        row_counts_run1 = {}

        with Session(engine) as session:
            for table in table_names:
                count = session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                row_counts_run1[table] = count

        assert row_counts_run1.get("users", 0) >= 42
        assert row_counts_run1.get("question_bank", 0) >= 280
        assert row_counts_run1.get("coding_problems", 0) >= 24
        assert row_counts_run1.get("assessments", 0) >= 12
        assert row_counts_run1.get("assessment_attempts", 0) >= 150
        assert row_counts_run1.get("practice_attempts", 0) >= 600
        assert row_counts_run1.get("ai_question_pool", 0) == 24

        # Run 2: Second Seed
        with Session(engine) as session:
            counts_run2 = seed_demo_pack(session)

        # Inspect table row counts after Run 2
        row_counts_run2 = {}
        with Session(engine) as session:
            for table in table_names:
                count = session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                row_counts_run2[table] = count

        # Compare row counts across ALL tables
        mismatches = []
        for table in table_names:
            c1 = row_counts_run1[table]
            c2 = row_counts_run2[table]
            if c1 != c2:
                mismatches.append(f"Table '{table}' row count changed: {c1} -> {c2} (diff: {c2 - c1})")

        assert len(mismatches) == 0, f"Seed is not idempotent! Violations found:\n" + "\n".join(mismatches)

    finally:
        engine.dispose()
        if os.path.exists(tmp_db_path):
            try:
                os.remove(tmp_db_path)
            except OSError:
                pass
