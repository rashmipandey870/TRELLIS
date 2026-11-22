"""Unit tests for AssessmentCategory enum validation on question creation (1.4)."""

import pytest
from pydantic import ValidationError

from app.api.v1.mentor import UnifiedQuestionCreateRequest, McqQuestionCreateRequest, CodingProblemCreateRequest
from app.schemas.category import AssessmentCategory


def test_category_validation_rejects_bogus_category():
    """Verify that 'BOGUS-CAT' fails Pydantic schema validation."""
    with pytest.raises(ValidationError) as exc:
        UnifiedQuestionCreateRequest(
            title="Invalid Category Question",
            question_text="What is this?",
            category="BOGUS-CAT",
        )
    assert "category" in str(exc.value)


def test_category_validation_accepts_valid_enum():
    """Verify that all canonical AssessmentCategory values are accepted."""
    for cat in AssessmentCategory:
        req = UnifiedQuestionCreateRequest(
            title="Valid Question",
            question_text="Valid question text",
            category=cat,
        )
        assert req.category == cat
