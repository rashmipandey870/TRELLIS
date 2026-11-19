"""TRELLIS Demo Seed Verification Test Suite (Slice 1.7b).

Tests:
1. verify_demo_environment strictly refuses execution when TRELLIS_ENV is not 'demo'.
2. seed_demo_data successfully populates synthetic database records under TRELLIS_ENV=demo.
3. get_home_data computes expected real-time telemetry from seeded records.
"""

from __future__ import annotations

import os
import sys
from collections.abc import Generator

# Ensure repo root is on sys.path so scripts can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from scripts.seed_demo_data import seed_demo_data, verify_demo_environment
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.models.base import Base
from app.services.home_service import get_home_data


@pytest.fixture
def db_engine() -> Generator[Engine, None, None]:
    """Provide an in-memory SQLite database engine with StaticPool."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    """Provide a database session attached to the shared in-memory engine."""
    session = Session(db_engine)
    try:
        yield session
    finally:
        session.close()


def test_seed_demo_refuses_when_not_demo(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify seed refuses execution if TRELLIS_ENV is prod, dev, or unset."""
    for bad_env in ["production", "prod", "staging", "dev", ""]:
        monkeypatch.setenv("TRELLIS_ENV", bad_env)
        with pytest.raises(RuntimeError) as exc:
            verify_demo_environment()
        assert "REFUSING_SEED" in str(exc.value)


def test_seed_demo_populates_database_under_demo_env(
    db_session: Session, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify seed successfully creates demo records when TRELLIS_ENV=demo."""
    monkeypatch.setenv("TRELLIS_ENV", "demo")

    result = seed_demo_data(db_session)
    assert result["org_id"] is not None
    assert result["learner_id"] is not None

    # Verify get_home_data for the seeded demo learner
    home_data = get_home_data(
        session=db_session,
        user_id=result["learner_id"],
        org_id=result["org_id"],
    )

    # 1. Profile
    assert home_data["profile"]["name"] == "Demo Learner 01"
    assert home_data["profile"]["email"] == "demo.learner01@csmtech.internal"
    assert home_data["profile"]["role"] == "Associate Platform Engineer"

    # 2. Enrolment
    enr = home_data["enrolment"]
    assert enr is not None
    assert enr["pathway_code"] == "PW-PLATFORM-90D"
    assert enr["total_modules"] == 6
    assert enr["completed_modules"] == 2
    assert enr["progress_pct"] == 33
    assert enr["current_module_name"] == "Kubernetes Custom Resource Definitions (CRDs)"

    # 3. Evidence Labels
    gaps = {g["skill_code"]: g for g in home_data["skill_gaps"]}
    assert gaps["SKILL-CONSENSUS"]["sample_size"] == 6
    assert gaps["SKILL-CONSENSUS"]["evidence_label"] == "STRONG_EVIDENCE"

    assert gaps["SKILL-K8S"]["sample_size"] == 3
    assert gaps["SKILL-K8S"]["evidence_label"] == "DEVELOPING_EVIDENCE"

    assert gaps["SKILL-MTLS"]["sample_size"] == 1
    assert gaps["SKILL-MTLS"]["evidence_label"] == "LIMITED_EVIDENCE"

    assert gaps["SKILL-KAFKA"]["sample_size"] == 0
    assert gaps["SKILL-KAFKA"]["evidence_label"] == "NOT_ENOUGH_DATA"

    # 4. Streak
    assert home_data["streak"]["current_streak_days"] == 14
    assert home_data["streak"]["freezes_remaining"] == 2
