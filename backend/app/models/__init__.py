"""TRELLIS ORM Models Registry."""

from app.models.assessments import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentAudience,
    AssessmentQuestion,
    CodingProblem,
    McqOption,
    QuestionBank,
    Submission,
    TestCase,
)
from app.models.audit import AccessReceipt, AuditLog
from app.models.auth import RefreshToken
from app.models.base import Base
from app.models.batches import Batch, MentorLearnerAssignment
from app.models.curriculum import Cohort, Course, Enrolment, Module, Pathway
from app.models.ledger import EvidenceLedger, EvidenceRecord, LedgerCheckpoint
from app.models.meetings import Meeting, MeetingAttendance, MeetingAudience
from app.models.notifications import Notification
from app.models.practice import (
    AIQuestionPool,
    AlertAction,
    PracticeAttempt,
    PracticeQuestion,
    PracticeScore,
    PracticeSession,
    TalentAlert,
)
from app.models.reviews import MentorRemark
from app.models.settings import SystemSetting
from app.models.skill import RoleRequirement, Skill, SkillEdge, SkillLevel
from app.models.tenancy import Organisation
from app.models.user import Consent, EmploymentRecord, Grant, Role, User

__all__ = [
    "Base",
    "Organisation",
    "User",
    "RefreshToken",
    "EmploymentRecord",
    "Role",
    "Grant",
    "Consent",
    "AuditLog",
    "AccessReceipt",
    "Skill",
    "SkillLevel",
    "SkillEdge",
    "RoleRequirement",
    "EvidenceLedger",
    "EvidenceRecord",
    "LedgerCheckpoint",
    "Pathway",
    "Course",
    "Module",
    "Cohort",
    "Batch",
    "MentorLearnerAssignment",
    "Enrolment",
    "Meeting",
    "MeetingAudience",
    "MeetingAttendance",
    "QuestionBank",
    "McqOption",
    "CodingProblem",
    "TestCase",
    "Assessment",
    "AssessmentQuestion",
    "AssessmentAttempt",
    "Answer",
    "Submission",
    "MentorRemark",
    "PracticeSession",
    "PracticeQuestion",
    "PracticeAttempt",
    "PracticeScore",
    "TalentAlert",
    "AlertAction",
    "Notification",
    "SystemSetting",
]
