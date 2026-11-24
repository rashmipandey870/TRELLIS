"""TRELLIS Assessment Module Notes & Study Guides Schemas."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class RecommendedReadingItem(BaseModel):
    title: str = Field(..., min_length=1)
    url: str | None = None
    description: str | None = None


class AssessmentNoteCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    module_name: str = Field("Core Module", min_length=1, max_length=255)
    summary: str | None = Field(None, max_length=1000)
    content: str = Field(..., min_length=10)
    key_takeaways: list[str] = Field(default_factory=list)
    recommended_reading: list[dict[str, Any]] = Field(default_factory=list)
    estimated_read_time_minutes: int = Field(10, ge=1, le=120)
    is_published: bool = True


class AssessmentNoteUpdate(BaseModel):
    title: str | None = Field(None, min_length=2, max_length=255)
    module_name: str | None = Field(None, min_length=1, max_length=255)
    summary: str | None = None
    content: str | None = Field(None, min_length=10)
    key_takeaways: list[str] | None = None
    recommended_reading: list[dict[str, Any]] | None = None
    estimated_read_time_minutes: int | None = Field(None, ge=1, le=120)
    is_published: bool | None = None


class AssessmentNoteResponse(BaseModel):
    id: str
    assessment_id: str
    assessment_title: str | None = None
    assessment_field: str | None = None
    author_id: str
    author_name: str | None = None
    title: str
    module_name: str
    summary: str | None = None
    content: str
    key_takeaways: list[str] = Field(default_factory=list)
    recommended_reading: list[dict[str, Any]] = Field(default_factory=list)
    estimated_read_time_minutes: int = 10
    is_published: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
