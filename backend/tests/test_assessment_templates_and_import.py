"""Unit tests for Phase 3.5 Assessment Templates / Presets and CSV Import with Dry-Run."""

import pytest
from app.api.v1.mentor import QuestionImportRequest, get_assessment_templates, import_questions_csv
from app.models.user import User


def test_assessment_templates_presets():
    """Verify predefined assessment templates cover required domains and experience levels."""
    dummy_mentor = User(id="mentor-123", email="mentor@csmtech.internal", role="MENTOR")
    templates = get_assessment_templates(mentor=dummy_mentor)

    assert len(templates) >= 5
    ids = {t["id"] for t in templates}
    assert "FULLSTACK_ENTRY" in ids
    assert "CLOUD_DEVOPS_MID" in ids
    assert "DATA_AI_SPECIALIST" in ids
    assert "SYSTEMS_KERNEL" in ids
    assert "WORKPLACE_READINESS" in ids

    for t in templates:
        assert t["duration_minutes"] > 0
        assert 50.0 <= t["passing_score"] <= 100.0
        assert "proctoring_flags" in t
        assert "category_split" in t


def test_question_csv_import_dry_run_validation():
    """Verify CSV import validates rows, categories, and respects dry_run without saving."""
    dummy_mentor = User(id="mentor-123", email="mentor@csmtech.internal", role="MENTOR")

    csv_data = (
        "title,question_text,category,field,topic,difficulty,correct_answer,options\n"
        "Async Event Loop,How does asyncio schedule tasks?,Technical Knowledge,Python,Async,MEDIUM,Cooperative multitasking,Cooperative multitasking|Kernel preemption|Signal interrupts\n"
        "Broken Category Question,Invalid category test,INVALID-CAT,Python,General,EASY,Ans,A|B\n"
    )

    req = QuestionImportRequest(csv_content=csv_data, dry_run=True)
    res = import_questions_csv(payload=req, db=None, mentor=dummy_mentor, _uow=None)

    assert res["dry_run"] is True
    assert res["valid_count"] == 1
    assert res["error_count"] == 1
    assert any("INVALID-CAT" in err for err in res["errors"])
    assert len(res["preview"]) == 1
