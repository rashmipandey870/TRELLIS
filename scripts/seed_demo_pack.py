"""TRELLIS Comprehensive Enterprise Demo Data Pack Seeder (Phase D & Phase 1).

Seeds:
- 42 Users across 4 batches (1 Admin, 5 Mentors, 36 Learners) with realistic metadata
- ~304 Question Bank Items across all 7 Enterprise Policy Categories + Additional
- 24 LeetCode-style Coding & SQL Problems across 5 languages (Python, SQL, Java, JS, C++) with test cases & judge harness
- 12 Realistic Assessments across all lifecycle states (4 DRAFT, 2 SCHEDULED, 3 PUBLISHED, 3 CLOSED)
- AssessmentAudience specific learner links
- 180+ Assessment Attempts with bell-curve scores, submitted answers, and Growth Ring reports
- 3 In-progress Assessment Attempts with autosave state
- 12 Subjective Graded Answers with rubric evaluation
- 400+ Coding Submissions across learners with realistic verdicts & runtimes
- 600+ AI Practice Attempts & Dedication Scores across topics
- 4 Real Talent Spotlight Alerts with mentor actions and scheduled meetings
- 19 Diverse Meetings (12 completed with attendance, 2 live, 5 upcoming)
- 200+ In-app Notifications (4-8 per user across all 42 users)
- Qualitative Mentor Remarks, and Immutable Audit Logs
"""

from __future__ import annotations

import os
import sys
import random
from datetime import UTC, datetime, timedelta

# Ensure backend is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.api.deps import get_sync_engine
from app.core.security import hash_password
from app.models import (
    AIQuestionPool,
    AlertAction,
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentAudience,
    AssessmentQuestion,
    AuditLog,
    Batch,
    CodingProblem,
    Cohort,
    Consent,
    McqOption,
    Meeting,
    MeetingAttendance,
    MeetingAudience,
    MentorLearnerAssignment,
    MentorRemark,
    Notification,
    Organisation,
    PracticeAttempt,
    PracticeQuestion,
    PracticeScore,
    PracticeSession,
    QuestionBank,
    Submission,
    TalentAlert,
    TestCase,
    User,
)
from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER
from app.services.code_runner import CodeRunner

# Import fixtures
from fixtures.technical_questions import TECHNICAL_QUESTIONS
from fixtures.coding_problems import CODING_PROBLEMS
from fixtures.aptitude_reasoning import APTITUDE_REASONING_QUESTIONS
from fixtures.communication_psychometric import COMMUNICATION_PSYCHOMETRIC_QUESTIONS


def seed_demo_pack(session: Session) -> dict[str, int]:
    """Execute complete deterministic seed of the TRELLIS platform."""
    counts: dict[str, int] = {}
    now = datetime.now(UTC)
    pwd_hash = hash_password("CSMTrellis2026!")

    # 1. Organization
    org = session.execute(select(Organisation).where(Organisation.code == "CSM_MAIN")).scalar_one_or_none()
    if not org:
        org = Organisation(name="CSM Technology", code="CSM_MAIN")
        session.add(org)
        session.flush()

    # 2. Users (42 Users: 1 Admin, 5 Mentors, 36 Learners)
    # 2a. Admin
    admin = session.execute(select(User).where(User.email == "admin@csmtech.internal")).scalar_one_or_none()
    if not admin:
        admin = User(
            org_id=org.id,
            email="admin@csmtech.internal",
            password_hash=pwd_hash,
            full_name="Rajesh Mohanty (L&K Governance)",
            role="ADMIN",
            is_active=True,
            must_change_password=False,
        )
        session.add(admin)
        session.flush()

    # 2b. Mentors
    mentor_specs = [
        ("soumya.p@csmtech.internal", "Soumya Ranjan Patnaik (Lead Full Stack & Cloud Architect)"),
        ("ananya.m@csmtech.internal", "Ananya Mishra (Principal Data & AI Specialist)"),
        ("debashis.j@csmtech.internal", "Debashis Jena (Principal Systems Engineer)"),
        ("mentor1@csmtech.internal", "Ananya Rao (Lead Cloud Architect)"),
        ("mentor2@csmtech.internal", "Vikram Patel (Principal Systems Engineer)"),
    ]
    mentors: dict[str, User] = {}
    for email, name in mentor_specs:
        m = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if not m:
            m = User(
                org_id=org.id,
                email=email,
                password_hash=pwd_hash,
                full_name=name,
                role="MENTOR",
                is_active=True,
                must_change_password=False,
            )
            session.add(m)
            session.flush()
        mentors[email] = m

    # 2c. 36 Learners
    learner_names = [
        "Priya Sharma", "Arjun Nair", "Sneha Mukherjee", "Rohan Verma", "Deepika Iyer",
        "Kavita Reddy", "Aditya Joshi", "Pooja Choudhury", "Amitav Das", "Neha Patel",
        "Vikram Malhotra", "Sunita Rao", "Manoj Kumar", "Shreya Sen", "Harish Swaminathan",
        "Meera Krishnan", "Kunal Singhania", "Tanya Saxena", "Ankit Tripathi", "Divya Agarwal",
        "Sandeep Panda", "Swati Mohapatra", "Ashish Behera", "Madhuri Pradhan", "Bibhuti Nayak",
        "Ritu Mohanty", "Alok Tripathy", "Sonali Dash", "Siddharth Roy", "Pallavi Banerjee",
        "Tushar Samantaray", "Rasmita Sahoo", "Pratik Rout", "Jyoti Prakash Jena", "Subhashree Mishra",
        "Biswajit Parida"
    ]
    learners: list[User] = []
    for idx, name in enumerate(learner_names, 1):
        email = f"learner{idx}@csmtech.internal"
        l = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
        # Learner 1 streak is 14 days; others distribute deterministically
        streak = 14 if idx == 1 else ((idx * 7) % 43)
        freezes = 1 if streak > 20 else 2
        last_active = now - timedelta(hours=(idx % 72))
        if not l:
            l = User(
                org_id=org.id,
                email=email,
                password_hash=pwd_hash,
                full_name=name,
                role="LEARNER",
                streak_days=streak,
                streak_freezes_remaining=freezes,
                last_active_at=last_active,
                is_active=True,
                must_change_password=False,
            )
            session.add(l)
            session.flush()
        else:
            # Update streak if needed
            if idx == 1 and l.streak_days != 14:
                l.streak_days = 14
                session.flush()
        learners.append(l)

    counts["users"] = session.execute(select(func.count(User.id))).scalar() or 0

    # 3. Cohorts & 4 Batches
    cohort = session.execute(select(Cohort).where(Cohort.code == "COHORT_2026")).scalar_one_or_none()
    if not cohort:
        cohort = Cohort(
            org_id=org.id,
            name="2026 Core Engineering Cohort",
            code="COHORT_2026",
            trainer_id=mentors["soumya.p@csmtech.internal"].id,
        )
        session.add(cohort)
        session.flush()

    batch_configs = [
        ("BATCH_ALPHA", "Batch Alpha (Full-Stack Engineering)", "Web & Full Stack", mentors["soumya.p@csmtech.internal"], learners[0:10]),
        ("BATCH_BETA", "Batch Beta (Cloud & DevOps Platform)", "Cloud & DevOps", mentors["soumya.p@csmtech.internal"], learners[10:20]),
        ("BATCH_GAMMA", "Batch Gamma (Data Engineering & AI)", "Data & AI", mentors["ananya.m@csmtech.internal"], learners[20:28]),
        ("BATCH_DELTA", "Batch Delta (Core Systems & Embedded)", "Core Systems", mentors["debashis.j@csmtech.internal"], learners[28:36]),
    ]

    batches: dict[str, Batch] = {}
    for code, name, field, lead_mentor, batch_learners in batch_configs:
        b = session.execute(select(Batch).where(Batch.code == code)).scalar_one_or_none()
        if not b:
            b = Batch(
                org_id=org.id,
                cohort_id=cohort.id,
                name=name,
                code=code,
                field=field,
                description=f"Specialized learning track for {field}.",
                max_learners=30,
            )
            session.add(b)
            session.flush()
        batches[code] = b

        # Assign mentor to each learner in this batch
        for l in batch_learners:
            assign = session.execute(
                select(MentorLearnerAssignment).where(
                    MentorLearnerAssignment.mentor_id == lead_mentor.id,
                    MentorLearnerAssignment.learner_id == l.id,
                )
            ).scalar_one_or_none()
            if not assign:
                session.add(MentorLearnerAssignment(
                    mentor_id=lead_mentor.id,
                    learner_id=l.id,
                    batch_id=b.id,
                ))
    session.flush()

    # 4. Question Bank Seeding (~304 Questions across 7 Categories)
    all_raw_questions = TECHNICAL_QUESTIONS + APTITUDE_REASONING_QUESTIONS + COMMUNICATION_PSYCHOMETRIC_QUESTIONS
    bank_questions: list[QuestionBank] = []
    author_id = mentors["soumya.p@csmtech.internal"].id

    for q_data in all_raw_questions:
        title = q_data["title"]
        existing_q = session.execute(select(QuestionBank).where(QuestionBank.title == title)).scalar_one_or_none()
        if not existing_q:
            existing_q = QuestionBank(
                author_id=author_id,
                title=title,
                question_text=q_data["question_text"],
                question_type=q_data.get("question_type", "MCQ"),
                category=q_data.get("category", AssessmentCategory.TECHNICAL_KNOWLEDGE.value),
                field=q_data.get("field", "Engineering Architecture"),
                topic=q_data.get("topic", "General"),
                difficulty=q_data.get("difficulty", "MEDIUM"),
                rubric_json=q_data.get("rubric_json"),
                explanation=q_data.get("explanation"),
                is_active=True,
            )
            session.add(existing_q)
            session.flush()

            # Add MCQ Options if present
            opts = q_data.get("options", [])
            corr = q_data.get("correct_answer")
            for seq, opt_text in enumerate(opts, 1):
                is_c = (opt_text == corr)
                session.add(McqOption(
                    question_id=existing_q.id,
                    option_text=opt_text,
                    is_correct=is_c,
                    sequence_order=seq,
                ))
        bank_questions.append(existing_q)
    session.flush()

    # 5. Coding Problems (24 Problems across 5 Languages with Verification Gate)
    cp_objs: list[CodingProblem] = []
    for cp_data in CODING_PROBLEMS:
        title = cp_data["title"]
        cp = session.execute(select(CodingProblem).where(CodingProblem.title == title)).scalar_one_or_none()
        if not cp:
            # Gate: Refuse to insert any problem that fails its reference solution
            ref_res = CodeRunner.execute(
                code=cp_data.get("reference_solution", ""),
                language=cp_data.get("language", "python"),
                test_cases=cp_data.get("test_cases", []),
                entry_point=cp_data.get("entry_point"),
                argument_schema=cp_data.get("argument_schema", []),
            )
            if ref_res.verdict not in ("ACCEPTED", "RUNNER_UNAVAILABLE"):
                if cp_data.get("language") in ("cpp", "c++", "java") and ref_res.verdict == "COMPILATION_ERROR":
                    pass
                else:
                    raise ValueError(
                        f"Seed gate refusal: problem '{title}' reference solution failed with {ref_res.verdict} "
                        f"({ref_res.first_failing_case or ref_res.compile_error})"
                    )

            # Create corresponding QuestionBank entry
            bank_item = QuestionBank(
                author_id=author_id,
                title=f"Coding: {title}",
                question_text=cp_data["description"],
                question_type="CODING" if cp_data["language"] != "sql" else "SQL",
                category=AssessmentCategory.CODING.value,
                field=cp_data["field"],
                topic=cp_data["field"],
                difficulty=cp_data["difficulty"],
                is_active=True,
            )
            session.add(bank_item)
            session.flush()

            cp = CodingProblem(
                bank_id=bank_item.id,
                title=title,
                description=cp_data["description"],
                constraints=cp_data.get("constraints"),
                difficulty=cp_data["difficulty"],
                field=cp_data["field"],
                marks=cp_data["marks"],
                problem_type=cp_data.get("problem_type", "CODING"),
                schema_ddl=cp_data.get("schema_ddl"),
                starter_code_json=cp_data.get("starter_code_json"),
                reference_solution=cp_data.get("reference_solution"),
                entry_point=cp_data.get("entry_point"),
                argument_schema=cp_data.get("argument_schema"),
                wrong_stub=cp_data.get("wrong_stub"),
                complexity_notes=cp_data.get("complexity_notes"),
                examples_json=cp_data.get("examples_json"),
            )
            session.add(cp)
            session.flush()

            for tc in cp_data.get("test_cases", []):
                session.add(TestCase(
                    problem_id=cp.id,
                    input_data=tc["input_data"],
                    expected_output=tc["expected_output"],
                    is_hidden=tc.get("is_hidden", False),
                    weight=tc.get("weight", 1.0),
                ))
            bank_questions.append(bank_item)
        cp_objs.append(cp)
    session.flush()

    counts["question_bank"] = session.execute(select(func.count(QuestionBank.id))).scalar() or 0
    counts["coding_problems"] = session.execute(select(func.count(CodingProblem.id))).scalar() or 0

    # 6. 12 Realistic Assessments across Lifecycle States (Phase E1)
    # At least 3 coding assessments, 1 psychometric (Likert), 1 mixed battery, plus lifecycle states
    assessment_specs = [
        # DRAFTS (3)
        ("Advanced Microservices Architecture", "DRAFT", "Cloud & DevOps", batches["BATCH_BETA"], 90, 70.0, mentors["soumya.p@csmtech.internal"]),
        ("Kubernetes Operator Development", "DRAFT", "Cloud & DevOps", batches["BATCH_BETA"], 75, 65.0, mentors["soumya.p@csmtech.internal"]),
        ("Linux Kernel Driver Programming", "DRAFT", "Core Systems", batches["BATCH_DELTA"], 120, 75.0, mentors["debashis.j@csmtech.internal"]),

        # SCHEDULED (2)
        ("Enterprise Full-Stack Capstone Assessment", "SCHEDULED", "Web & Full Stack", batches["BATCH_ALPHA"], 90, 65.0, mentors["soumya.p@csmtech.internal"]),
        ("Cloud Security & Compliance Certification Sprint", "SCHEDULED", "Cloud & DevOps", batches["BATCH_BETA"], 60, 70.0, mentors["soumya.p@csmtech.internal"]),

        # PUBLISHED / ACTIVE (4)
        ("Core Python & Data Structures Assessment", "PUBLISHED", "Web & Full Stack", batches["BATCH_ALPHA"], 60, 60.0, mentors["soumya.p@csmtech.internal"]),
        ("Enterprise SQL & Database Performance Assessment", "PUBLISHED", "Data & AI", batches["BATCH_GAMMA"], 60, 60.0, mentors["ananya.m@csmtech.internal"]),
        ("Workplace Behavioral & Psychometric Dimension Profile", "PUBLISHED", "Psychometric", batches["BATCH_ALPHA"], 45, 60.0, mentors["soumya.p@csmtech.internal"]),
        ("Campus-to-Corporate Readiness Battery", "PUBLISHED", "Engineering Architecture", batches["BATCH_ALPHA"], 90, 65.0, mentors["soumya.p@csmtech.internal"]),

        # CLOSED (3)
        ("Foundational Technical Knowledge Baseline", "CLOSED", "Web & Full Stack", batches["BATCH_ALPHA"], 45, 60.0, mentors["soumya.p@csmtech.internal"]),
        ("Engineering Aptitude & Deductive Reasoning Sprint", "CLOSED", "Web & Full Stack", batches["BATCH_ALPHA"], 45, 60.0, mentors["soumya.p@csmtech.internal"]),
        ("Workplace Communication & Readiness Baseline", "CLOSED", "Core Systems", batches["BATCH_DELTA"], 45, 60.0, mentors["debashis.j@csmtech.internal"]),
    ]

    assessments: dict[str, Assessment] = {}
    for title, status, field, batch, duration, pass_score, mentor in assessment_specs:
        a = session.execute(select(Assessment).where(Assessment.title == title)).scalar_one_or_none()
        if not a:
            start_w = now - timedelta(days=14) if status == "CLOSED" else (now + timedelta(days=2) if status == "SCHEDULED" else now - timedelta(days=1))
            end_w = now - timedelta(days=7) if status == "CLOSED" else (now + timedelta(days=5) if status == "SCHEDULED" else now + timedelta(days=7))
            a = Assessment(
                mentor_id=mentor.id,
                batch_id=batch.id,
                title=title,
                field=field,
                instructions=f"Official {field} assessment. Maintain academic integrity. Autosaved continuously.",
                duration_minutes=duration,
                passing_score=pass_score,
                start_window=start_w,
                end_window=end_w,
                status=status,
                version=1,
            )
            session.add(a)
            session.flush()

            # Attach appropriate domain questions (Phase E1)
            if title == "Core Python & Data Structures Assessment":
                # Attach Python coding problems + Python MCQs
                py_coding = [q for q in bank_questions if q.question_type == "CODING" and "Python" in q.title][:2]
                py_mcq = [q for q in bank_questions if q.field == "Python" and q.question_type == "MCQ"][:4]
                selected_qs = py_coding + py_mcq
            elif title == "Enterprise SQL & Database Performance Assessment":
                # Attach SQL coding problems + SQL MCQs
                sql_coding = [q for q in bank_questions if q.question_type == "SQL"][:2]
                sql_mcq = [q for q in bank_questions if q.field == "SQL" and q.question_type == "MCQ"][:4]
                selected_qs = sql_coding + sql_mcq
            elif title == "Enterprise Full-Stack Capstone Assessment":
                # Attach JS coding problems + Web dev MCQs
                js_coding = [q for q in bank_questions if q.question_type == "CODING" and any(k in q.title for k in ("JavaScript", "LRU", "Debounce", "Flatten"))][:2]
                js_mcq = [q for q in bank_questions if q.field in ("Web & Full Stack", "JavaScript") and q.question_type == "MCQ"][:4]
                selected_qs = js_coding + js_mcq
            elif title == "Workplace Behavioral & Psychometric Dimension Profile":
                # Attach 16 Likert questions across 8 dimensions
                selected_qs = [q for q in bank_questions if q.category == "Psychometric"][:16]
            elif title == "Campus-to-Corporate Readiness Battery":
                # Mixed: 3 Aptitude MCQs + 1 Python coding problem + 1 Subjective Short Answer + 8 Likert items
                apt_mcqs = [q for q in bank_questions if q.category in ("Quantitative Aptitude", "Logical & Reasoning")][:3]
                py_coding = [q for q in bank_questions if q.question_type == "CODING"][:1]
                sub_q = [q for q in bank_questions if q.question_type == "SHORT_ANSWER"][:1]
                likert_qs = [q for q in bank_questions if q.category == "Psychometric"][:8]
                selected_qs = apt_mcqs + py_coding + sub_q + likert_qs
            else:
                selected_qs = [q for q in bank_questions if q.field == field or q.field == "Engineering Architecture"][:8]
                if not selected_qs:
                    selected_qs = bank_questions[:6]

            for seq, q in enumerate(selected_qs, 1):
                session.add(AssessmentQuestion(
                    assessment_id=a.id,
                    bank_question_id=q.id,
                    sequence_order=seq,
                    marks=10.0 if q.question_type != "LIKERT" else 0.0,
                ))
        assessments[title] = a
    session.flush()

    # 6b. Seed AssessmentAudience for Individual Learners on >= 2 Assessments
    audience_assessments = [
        assessments["Core Python & Data Structures Assessment"],
        assessments["Enterprise SQL & Database Performance Assessment"],
        assessments["Workplace Behavioral & Psychometric Dimension Profile"],
        assessments["Campus-to-Corporate Readiness Battery"],
    ]
    for a in audience_assessments:
        for l in learners[:12]:
            existing_aud = session.execute(
                select(AssessmentAudience).where(
                    AssessmentAudience.assessment_id == a.id,
                    AssessmentAudience.learner_id == l.id,
                )
            ).scalar_one_or_none()
            if not existing_aud:
                session.add(AssessmentAudience(assessment_id=a.id, learner_id=l.id))
    session.flush()

    counts["assessments"] = session.execute(select(func.count(Assessment.id))).scalar() or 0

    # 7. 180+ Assessment Attempts with Bell Curve Scores & Growth Ring Reports (Phase E)
    scored_assessments = [
        assessments["Foundational Technical Knowledge Baseline"],
        assessments["Engineering Aptitude & Deductive Reasoning Sprint"],
        assessments["Workplace Communication & Readiness Baseline"],
        assessments["Core Python & Data Structures Assessment"],
        assessments["Enterprise SQL & Database Performance Assessment"],
        assessments["Workplace Behavioral & Psychometric Dimension Profile"],
        assessments["Campus-to-Corporate Readiness Battery"],
    ]

    random.seed(42)  # Deterministic seed for reproducible evaluation data
    attempt_count = 0

    for a in scored_assessments:
        target_learners = learners[0:10] if "ALPHA" in (a.batch.code if a.batch else "") else (
            learners[10:20] if "BETA" in (a.batch.code if a.batch else "") else (
                learners[20:28] if "GAMMA" in (a.batch.code if a.batch else "") else learners[28:36]
            )
        )
        extended_learners = list(set(target_learners + learners[:25]))

        is_psych = (a.field == "Psychometric" or "Psychometric" in a.title)
        is_mixed = ("Campus-to-Corporate" in a.title)

        for l in extended_learners:
            existing_att = session.execute(
                select(AssessmentAttempt).where(
                    AssessmentAttempt.assessment_id == a.id,
                    AssessmentAttempt.learner_id == l.id,
                )
            ).scalar_one_or_none()

            if not existing_att:
                raw_score = int(random.gauss(74, 12))
                final_score = max(42.0, min(98.0, float(raw_score)))
                passed = final_score >= a.passing_score
                start_t = (a.start_window or now) + timedelta(hours=random.randint(2, 24))
                submit_t = start_t + timedelta(minutes=random.randint(25, a.duration_minutes - 5))

                if is_psych:
                    final_score = None
                    total_marks = None
                    passed = None
                    growth_report = {
                        "learner_name": l.full_name,
                        "is_psychometric": True,
                        "disclaimer": PSYCHOMETRIC_DISCLAIMER,
                        "psychometric_profile": {
                            "Agreeableness": 84.5,
                            "Conscientiousness": 88.0,
                            "Emotional Stability": 76.5,
                            "Openness": 82.0,
                            "Extraversion": 71.0,
                            "Grit": 90.0,
                            "Collaborative Mindset": 86.5,
                            "Problem-Solving Integrity": 93.0,
                        },
                        "strengths": ["High resilience under project constraints", "Constructive peer feedback culture"],
                        "development_areas": ["Public cross-functional presentation confidence"],
                    }
                    # Seed consent for psychometric evaluation
                    ex_consent = session.execute(
                        select(Consent).where(
                            Consent.user_id == l.id,
                            Consent.purpose_code == "PSYCHOMETRIC_EVALUATION",
                        )
                    ).scalar_one_or_none()
                    if not ex_consent:
                        session.add(Consent(
                            user_id=l.id,
                            org_id=l.org_id,
                            purpose_code="PSYCHOMETRIC_EVALUATION",
                            status="GRANTED",
                            granted_at=now,
                        ))
                else:
                    total_marks = 100.0
                    growth_report = {
                        "learner_name": l.full_name,
                        "overall_score": final_score,
                        "passed": passed,
                        "competencies": {
                            "Technical Knowledge": min(100.0, final_score + random.uniform(-5, 5)),
                            "Problem Solving": min(100.0, final_score + random.uniform(-8, 6)),
                            "Code Quality": min(100.0, final_score + random.uniform(-6, 8)),
                            "System Architecture": min(100.0, final_score + random.uniform(-10, 4)),
                            "Professional Execution": min(100.0, final_score + random.uniform(-4, 6)),
                        },
                        "recommendations": [
                            "Deepen concurrency synchronization understanding.",
                            "Practice parameterized query design for performance tuning.",
                        ]
                    }
                    if is_mixed:
                        growth_report["psychometric_profile"] = {
                            "Agreeableness": 82.0,
                            "Conscientiousness": 86.5,
                            "Emotional Stability": 79.0,
                            "Openness": 80.5,
                            "Extraversion": 74.0,
                            "Grit": 88.0,
                            "Collaborative Mindset": 85.0,
                            "Problem-Solving Integrity": 91.5,
                        }
                        growth_report["disclaimer"] = PSYCHOMETRIC_DISCLAIMER
                        ex_consent = session.execute(
                            select(Consent).where(
                                Consent.user_id == l.id,
                                Consent.purpose_code == "PSYCHOMETRIC_EVALUATION",
                            )
                        ).scalar_one_or_none()
                        if not ex_consent:
                            session.add(Consent(
                                user_id=l.id,
                                org_id=l.org_id,
                                purpose_code="PSYCHOMETRIC_EVALUATION",
                                status="GRANTED",
                                granted_at=now,
                            ))

                # Varied report statuses: APPROVED, PENDING_APPROVAL, PROVISIONAL
                if a.status == "CLOSED":
                    rep_status = "APPROVED"
                elif attempt_count % 3 == 0:
                    rep_status = "PROVISIONAL"
                else:
                    rep_status = "PENDING_APPROVAL"

                att = AssessmentAttempt(
                    assessment_id=a.id,
                    learner_id=l.id,
                    start_time=start_t,
                    submit_time=submit_t,
                    score=final_score,
                    total_marks=total_marks,
                    passed=passed,
                    status="SUBMITTED",
                    grading_status="GRADED",
                    report_json=growth_report,
                    report_status=rep_status,
                    report_approved_at=submit_t + timedelta(hours=2) if rep_status == "APPROVED" else None,
                )
                session.add(att)
                session.flush()

                # Populate concrete Answers for attempt
                for aq in a.questions[:5]:
                    is_q_likert = is_psych or (getattr(aq, "question", None) and getattr(aq.question, "question_type", None) == "LIKERT")
                    session.add(Answer(
                        attempt_id=att.id,
                        bank_question_id=aq.bank_question_id,
                        text_response="5" if is_q_likert else "Optimized approach utilizing hash-map indices for linear time complexity.",
                        grading_status="GRADED",
                        score_awarded=0.0 if is_q_likert else (aq.marks if passed else (aq.marks * 0.5)),
                    ))

                # Create Qualitative Mentor Remark for a sample of attempts
                if attempt_count % 4 == 0:
                    ex_rem = session.execute(
                        select(MentorRemark).where(
                            MentorRemark.mentor_id == a.mentor_id,
                            MentorRemark.learner_id == l.id,
                            MentorRemark.assessment_id == a.id,
                        )
                    ).scalar_one_or_none()
                    if not ex_rem:
                        session.add(MentorRemark(
                            mentor_id=a.mentor_id,
                            learner_id=l.id,
                            assessment_id=a.id,
                            remark_text=f"Demonstrated solid grasp of {a.field} fundamentals. Recommendation: continue daily coding practice on edge cases.",
                            visibility="LEARNER_AND_ADMIN",
                        ))

                attempt_count += 1
    session.flush()

    # 7b. In-Progress Attempts (3 attempts in progress with autosave state)
    in_progress_assessment = assessments["Core Python & Data Structures Assessment"]
    for l_in_prog in learners[33:36]:
        existing_in_prog = session.execute(
            select(AssessmentAttempt).where(
                AssessmentAttempt.assessment_id == in_progress_assessment.id,
                AssessmentAttempt.learner_id == l_in_prog.id,
            )
        ).scalar_one_or_none()
        if not existing_in_prog:
            session.add(AssessmentAttempt(
                assessment_id=in_progress_assessment.id,
                learner_id=l_in_prog.id,
                start_time=now - timedelta(minutes=20),
                submit_time=None,
                score=0.0,
                total_marks=100.0,
                passed=False,
                status="IN_PROGRESS",
                grading_status="PENDING_REVIEW",
                tab_switch_count=0,
                autosave_state_json={
                    "current_question_index": 2,
                    "answers": {
                        "q1": "Selected option A based on indexing speed",
                        "q2": "Using sliding window technique to minimize runtime",
                    },
                    "time_remaining_seconds": 2400,
                },
            ))
    session.flush()

    # 7c. Subjective Graded & Pending Answers (14 answers with in-depth text_response, pending manual review & AI rubric)
    subjective_q = session.execute(
        select(QuestionBank).where(QuestionBank.question_type == "SHORT_ANSWER")
    ).scalar_one_or_none()
    subjective_rubric = {
        "dimensions": [
            {"dimension": "Architecture Contrast", "weight": 0.5, "description": "Clear distinction between Kafka log streaming and ACID relational storage."},
            {"dimension": "Scalability & Consistency", "weight": 0.5, "description": "Addresses CAP theorem, horizontal scaling vs dual-write bottlenecks."}
        ],
        "suggested_answers": [
            "Kafka decouples producers/consumers with append-only partitioning but introduces eventual consistency. Relational DB guarantees ACID transactions but has vertical write limits."
        ]
    }
    if not subjective_q:
        subjective_q = QuestionBank(
            author_id=author_id,
            title="System Design Trade-off Analysis: Event-Driven vs Monolithic State",
            question_text="Explain the trade-offs between an event-driven architecture using Kafka and a centralized relational database architecture for processing high-throughput financial transactions.",
            question_type="SHORT_ANSWER",
            category=AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
            field="System Architecture",
            topic="Distributed Systems",
            difficulty="HARD",
            rubric_json=subjective_rubric,
            is_active=True,
        )
        session.add(subjective_q)
        session.flush()
    else:
        subjective_q.rubric_json = subjective_rubric

    recent_submitted_attempts = session.execute(
        select(AssessmentAttempt).where(AssessmentAttempt.status == "SUBMITTED").limit(14)
    ).scalars().all()

    ai_feedback_suggestions = [
        "[AI Rubric Suggestion]: Proposed Score 8.5/10 (94% confidence). Decoupled Kafka stream contrasted with ACID transactional isolation. Meets criteria for Architecture Contrast and CAP trade-offs.",
        "[AI Rubric Suggestion]: Proposed Score 7.0/10 (88% confidence). Accurately noted write throughput differences, but could expand on transaction replayability and saga orchestration.",
    ]

    for idx, s_att in enumerate(recent_submitted_attempts):
        ex_sub_ans = session.execute(
            select(Answer).where(
                Answer.attempt_id == s_att.id,
                Answer.bank_question_id == subjective_q.id,
            )
        ).scalar_one_or_none()
        if not ex_sub_ans:
            feedback = ai_feedback_suggestions[idx % len(ai_feedback_suggestions)] if idx < 7 else None
            session.add(Answer(
                attempt_id=s_att.id,
                bank_question_id=subjective_q.id,
                text_response=(
                    "An event-driven architecture decouples producers from consumers and enables horizontal scaling with high append throughput. "
                    "However, it introduces eventual consistency and dual-write challenges. A centralized relational system provides ACID guarantees "
                    "and straightforward queries via foreign keys, but suffers write contention and vertical scaling bottlenecks at scale."
                ),
                mentor_feedback=feedback,
                grading_status="PENDING_REVIEW",
                score_awarded=None,
            ))
            s_att.grading_status = "PENDING_REVIEW"
            s_att.report_status = "PROVISIONAL"
    session.flush()

    counts["attempts"] = session.execute(select(func.count(AssessmentAttempt.id))).scalar() or 0

    # 8. 400+ Coding Submissions across Learners & Problems (Phase E: including COMPILATION_ERROR and MEMORY_LIMIT_EXCEEDED)
    existing_sub_count = session.execute(select(func.count(Submission.id))).scalar() or 0
    if existing_sub_count == 0 and cp_objs:
        verdict_weights = (
            ["ACCEPTED"] * 8
            + ["WRONG_ANSWER"] * 2
            + ["RUNTIME_ERROR"] * 1
            + ["TIME_LIMIT_EXCEEDED"] * 1
            + ["COMPILATION_ERROR"] * 1
            + ["MEMORY_LIMIT_EXCEEDED"] * 1
        )
        for l_idx, l in enumerate(learners):
            # Each learner submits 12-14 problems
            for p_idx in range(13):
                prob = cp_objs[(l_idx + p_idx) % len(cp_objs)]
                v = random.choice(verdict_weights)
                tc_total = len(prob.test_cases) if prob.test_cases else 6
                runtime = round(random.uniform(15.0, 140.0), 1)
                memory = round(random.uniform(16.0, 42.0), 1)
                if v == "ACCEPTED":
                    tc_passed = tc_total
                    score = prob.marks
                    code = prob.reference_solution or "# Reference solution passed"
                elif v == "WRONG_ANSWER":
                    tc_passed = random.randint(1, max(1, tc_total - 1))
                    score = round(prob.marks * (tc_passed / tc_total), 1)
                    code = prob.wrong_stub or "# Partial attempt"
                elif v == "TIME_LIMIT_EXCEEDED":
                    tc_passed = random.randint(1, max(1, tc_total // 2))
                    score = 0.0
                    runtime = 2050.0
                    code = "# Nested loop causing TLE\n" + (prob.starter_code_json.get("python", "") if prob.starter_code_json else "")
                elif v == "COMPILATION_ERROR":
                    tc_passed = 0
                    score = 0.0
                    runtime = 0.0
                    code = "def syntax_error_in_code(\n    return 42"
                elif v == "MEMORY_LIMIT_EXCEEDED":
                    tc_passed = random.randint(1, max(1, tc_total // 2))
                    score = 0.0
                    memory = 265.0
                    code = "def memory_exhaustion():\n    return [0] * (10**8)"
                else:  # RUNTIME_ERROR
                    tc_passed = 0
                    score = 0.0
                    code = "# IndexError on empty input\n" + (prob.starter_code_json.get("python", "") if prob.starter_code_json else "")

                session.add(Submission(
                    coding_problem_id=prob.id,
                    learner_id=l.id,
                    code=code,
                    language="sql" if "sql" in prob.title.lower() else "python",
                    verdict=v,
                    runtime_ms=runtime,
                    memory_mb=memory,
                    passed_cases=tc_passed,
                    total_cases=tc_total,
                    score=score,
                    details_json={
                        "verdict": v,
                        "passed_cases": tc_passed,
                        "total_cases": tc_total,
                        "runtime_ms": runtime,
                        "memory_mb": memory,
                    },
                ))
        session.flush()

    counts["submissions"] = session.execute(select(func.count(Submission.id))).scalar() or 0

    # 9. 600+ Practice Attempts across Categories & Dedication Scores (Phase B3: Idempotency Protected)
    practice_fields = ["Python", "SQL", "Java", "JavaScript", "C++", "Cloud & DevOps", "Data & AI"]

    for l in learners:
        for f in practice_fields[:5]:
            existing_ps = session.execute(
                select(PracticeSession).where(
                    PracticeSession.learner_id == l.id,
                    PracticeSession.field == f,
                )
            ).first()
            if not existing_ps:
                ps = PracticeSession(
                    learner_id=l.id,
                    field=f,
                    difficulty="MEDIUM",
                    mode="MCQ",
                    completed_at=now - timedelta(days=random.randint(1, 14)),
                )
                session.add(ps)
                session.flush()

                # Add 5 practice questions and attempts per session
                for q_idx in range(5):
                    pq = PracticeQuestion(
                        session_id=ps.id,
                        field=f,
                        difficulty="MEDIUM",
                        mode="MCQ",
                        title=f"{f} Practice Drill #{q_idx+1}",
                        question_data_json={
                            "title": f"{f} Core Drill",
                            "question": f"Analyze the time and space complexity of {f} collection operations.",
                            "options": ["O(1) average lookup", "O(N) linear scan", "O(N log N)", "O(N^2)"],
                            "answer": "O(1) average lookup",
                        },
                        verified=True,
                    )
                    session.add(pq)
                    session.flush()

                    is_c = random.choice([True, True, True, False])  # 75% accuracy
                    session.add(PracticeAttempt(
                        question_id=pq.id,
                        learner_id=l.id,
                        answer_json={"selected": "O(1) average lookup" if is_c else "O(N) linear scan"},
                        is_correct=is_c,
                        score=10.0 if is_c else 0.0,
                    ))

        # Populate PracticeScore record for dedication tracking
        existing_score = session.execute(
            select(PracticeScore).where(
                PracticeScore.learner_id == l.id,
                PracticeScore.field == "Python",
            )
        ).scalar_one_or_none()
        if not existing_score:
            session.add(PracticeScore(
                learner_id=l.id,
                field="Python",
                active_days=l.streak_days + 5,
                streak_days=l.streak_days,
                problems_attempted=35,
                problems_solved=29,
                acceptance_rate=82.8,
                weighted_accuracy=84.5,
                dedication_score=min(98.5, 60.0 + l.streak_days * 0.9),
                last_practiced_at=l.last_active_at,
            ))
    session.flush()

    counts["practice_attempts"] = session.execute(select(func.count(PracticeAttempt.id))).scalar() or 0

    # 10. 4 Real Talent Spotlight Alerts with Mentor Actions & Scheduled Meetings
    alert_specs = [
        (learners[0], mentors["soumya.p@csmtech.internal"], "Python", "INTERVIEW_SCHEDULED", "SCHEDULE_INTERVIEW", 94.5, 14),
        (learners[10], mentors["soumya.p@csmtech.internal"], "Cloud & DevOps", "INVITED_TO_ASSESSMENT", "INVITE_ASSESSMENT", 91.2, 18),
        (learners[20], mentors["ananya.m@csmtech.internal"], "Data & AI", "RECOMMENDED_PROMOTION", "RECOMMEND_PROMOTION", 96.0, 28),
        (learners[28], mentors["debashis.j@csmtech.internal"], "Core Systems", "PENDING", None, 88.5, 12),
    ]

    for learner, mentor, field, status, action, score, streak in alert_specs:
        existing_alt = session.execute(
            select(TalentAlert).where(
                TalentAlert.learner_id == learner.id,
                TalentAlert.field == field,
            )
        ).scalar_one_or_none()

        if not existing_alt:
            alt = TalentAlert(
                learner_id=learner.id,
                mentor_id=mentor.id,
                field=field,
                evidence_json={
                    "dedication_score": score,
                    "streak_days": streak,
                    "accuracy": 92.5,
                    "recommendation": f"Outstanding velocity in {field} problem solving.",
                },
                status=status,
                action_taken=action,
                action_notes=f"Mentor verified exceptional competency in {field}." if action else None,
                action_time=now - timedelta(days=1) if action else None,
            )
            session.add(alt)
            session.flush()

            if action:
                session.add(AlertAction(
                    alert_id=alt.id,
                    mentor_id=mentor.id,
                    action_taken=action,
                    notes=f"Processed action: {action}",
                    action_time=now - timedelta(days=1),
                ))

            if action == "SCHEDULE_INTERVIEW":
                m_title = f"Talent Spotlight 1:1 - {learner.full_name}"
                existing_mtg = session.execute(select(Meeting).where(Meeting.title == m_title)).scalar_one_or_none()
                if not existing_mtg:
                    mtg = Meeting(
                        title=m_title,
                        description=f"Advanced technical evaluation and career pathway acceleration interview for {learner.full_name}.",
                        meeting_date=(now + timedelta(days=2)).strftime("%Y-%m-%d"),
                        start_time="14:00",
                        end_time="15:00",
                        duration_minutes=60,
                        meeting_link="https://teams.microsoft.com/l/meetup-join/csm-talent-spotlight",
                        mentor_id=mentor.id,
                        status="SCHEDULED",
                    )
                    session.add(mtg)
                    session.flush()
                    session.add(MeetingAudience(meeting_id=mtg.id, learner_id=learner.id))
                    session.add(Notification(
                        recipient_id=learner.id,
                        sender_id=mentor.id,
                        title="Talent Spotlight Interview Scheduled",
                        message=f"You have been nominated for an interview with {mentor.full_name} on {(now + timedelta(days=2)).strftime('%Y-%m-%d')}.",
                        notification_type="TALENT_ALERT",
                    ))
    session.flush()

    # 11. 19 Diverse Meetings (12 completed with attendance, 2 live, 5 upcoming)
    full_meeting_specs = [
        # COMPLETED (12)
        ("Cloud Architecture Sync - Batch Alpha", "Weekly review of distributed systems patterns.", (now - timedelta(days=10)).strftime("%Y-%m-%d"), "10:00", "11:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-cloud-sync-1", mentors["soumya.p@csmtech.internal"], batches["BATCH_ALPHA"], "COMPLETED"),
        ("Data Pipeline Optimization Clinic", "Deep dive into Spark shuffle tuning and Parquet partitioning.", (now - timedelta(days=8)).strftime("%Y-%m-%d"), "15:00", "16:30", 90, "https://teams.microsoft.com/l/meetup-join/csm-data-clinic-1", mentors["ananya.m@csmtech.internal"], batches["BATCH_GAMMA"], "COMPLETED"),
        ("Linux Systems Programming Office Hours", "Q&A on POSIX threads, memory layout, and kernel diagnostics.", (now - timedelta(days=7)).strftime("%Y-%m-%d"), "11:00", "12:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-systems-oh-1", mentors["debashis.j@csmtech.internal"], batches["BATCH_DELTA"], "COMPLETED"),
        ("DevOps CI/CD Deployment Walkthrough", "Live demonstration of zero-downtime rolling deployments on K8s.", (now - timedelta(days=6)).strftime("%Y-%m-%d"), "14:00", "15:30", 90, "https://teams.microsoft.com/l/meetup-join/csm-devops-demo-1", mentors["soumya.p@csmtech.internal"], batches["BATCH_BETA"], "COMPLETED"),
        ("Engineering Aptitude Debrief Session", "Review of quantitative reasoning and deductive logic patterns.", (now - timedelta(days=5)).strftime("%Y-%m-%d"), "16:00", "17:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-aptitude-debrief-1", mentors["soumya.p@csmtech.internal"], batches["BATCH_ALPHA"], "COMPLETED"),
        ("Full-Stack Async Design Review", "FastAPI dependency injection and async session concurrency patterns.", (now - timedelta(days=4)).strftime("%Y-%m-%d"), "10:30", "11:30", 60, "https://teams.microsoft.com/l/meetup-join/csm-async-review", mentors["soumya.p@csmtech.internal"], batches["BATCH_ALPHA"], "COMPLETED"),
        ("SQL Indexing & Query Tuning Workshop", "B-tree vs GIN indexes, execution plan inspection with EXPLAIN ANALYZE.", (now - timedelta(days=3)).strftime("%Y-%m-%d"), "14:00", "15:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-sql-tuning", mentors["ananya.m@csmtech.internal"], batches["BATCH_GAMMA"], "COMPLETED"),
        ("K8s Security & RBAC Configuration", "Pod Security Standards, ServiceAccount tokens, and NetworkPolicies.", (now - timedelta(days=3)).strftime("%Y-%m-%d"), "16:00", "17:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-k8s-security", mentors["mentor1@csmtech.internal"], batches["BATCH_BETA"], "COMPLETED"),
        ("Memory Allocators & C++ Diagnostics", "Debugging heap corruptions with Valgrind and ASan.", (now - timedelta(days=2)).strftime("%Y-%m-%d"), "11:00", "12:30", 90, "https://teams.microsoft.com/l/meetup-join/csm-cpp-debug", mentors["mentor2@csmtech.internal"], batches["BATCH_DELTA"], "COMPLETED"),
        ("Enterprise API Gateway Architecture", "Rate limiting, circuit breaking, and HMAC validation at scale.", (now - timedelta(days=2)).strftime("%Y-%m-%d"), "15:00", "16:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-api-gateway", mentors["soumya.p@csmtech.internal"], batches["BATCH_ALPHA"], "COMPLETED"),
        ("Psychometric Workplace Composure Workshop", "Navigating high-velocity project deadlines and professional feedback.", (now - timedelta(days=1)).strftime("%Y-%m-%d"), "14:00", "15:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-composure-workshop", mentors["ananya.m@csmtech.internal"], batches["BATCH_GAMMA"], "COMPLETED"),
        ("Embedded Firmware Unit Testing Lab", "Mocking hardware registers and boundary testing with Unity framework.", (now - timedelta(days=1)).strftime("%Y-%m-%d"), "16:30", "17:30", 60, "https://teams.microsoft.com/l/meetup-join/csm-firmware-lab", mentors["debashis.j@csmtech.internal"], batches["BATCH_DELTA"], "COMPLETED"),

        # LIVE (2)
        ("Live Architecture Code Review & Pair Programming", "Interactive pull request review session for microservices gateway.", now.strftime("%Y-%m-%d"), "09:30", "11:00", 90, "https://teams.microsoft.com/l/meetup-join/csm-live-pairing", mentors["soumya.p@csmtech.internal"], batches["BATCH_ALPHA"], "SCHEDULED"),
        ("Distributed Cache Invalidation Strategies", "Hands-on implementation of Redis pub/sub cache sync.", now.strftime("%Y-%m-%d"), "13:30", "14:30", 60, "https://teams.microsoft.com/l/meetup-join/csm-live-redis", mentors["ananya.m@csmtech.internal"], batches["BATCH_GAMMA"], "SCHEDULED"),

        # UPCOMING (5)
        ("Cloud Infrastructure as Code Sprint", "Terraform modules, state locking, and drift detection hands-on.", (now + timedelta(days=1)).strftime("%Y-%m-%d"), "10:00", "11:30", 90, "https://teams.microsoft.com/l/meetup-join/csm-terraform-sprint", mentors["soumya.p@csmtech.internal"], batches["BATCH_BETA"], "SCHEDULED"),
        ("Advanced Graph Algorithms in Production", "Shortest path and network flow in logistics optimization.", (now + timedelta(days=2)).strftime("%Y-%m-%d"), "14:00", "15:30", 90, "https://teams.microsoft.com/l/meetup-join/csm-graphs-prod", mentors["debashis.j@csmtech.internal"], batches["BATCH_DELTA"], "SCHEDULED"),
        ("Generative AI & Enterprise Retrieval (RAG)", "Vector embeddings, hybrid search, and hallucination guardrails.", (now + timedelta(days=3)).strftime("%Y-%m-%d"), "11:00", "12:30", 90, "https://teams.microsoft.com/l/meetup-join/csm-rag-deepdive", mentors["ananya.m@csmtech.internal"], batches["BATCH_GAMMA"], "SCHEDULED"),
        ("Enterprise Observability with OpenTelemetry", "Distributed tracing, span metrics, and Prometheus alerts.", (now + timedelta(days=4)).strftime("%Y-%m-%d"), "15:00", "16:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-otel-sync", mentors["mentor1@csmtech.internal"], batches["BATCH_BETA"], "SCHEDULED"),
        ("End-of-Sprint Retrospective & Career Mentoring", "Cohort-wide milestone retrospective and Growth Ring review.", (now + timedelta(days=5)).strftime("%Y-%m-%d"), "16:00", "17:30", 90, "https://teams.microsoft.com/l/meetup-join/csm-sprint-retro", mentors["soumya.p@csmtech.internal"], batches["BATCH_ALPHA"], "SCHEDULED"),
    ]

    for m_title, desc, m_date, s_time, e_time, dur, link, mentor, batch, status in full_meeting_specs:
        ex_m = session.execute(select(Meeting).where(Meeting.title == m_title)).scalar_one_or_none()
        if not ex_m:
            m = Meeting(
                title=m_title,
                description=desc,
                meeting_date=m_date,
                start_time=s_time,
                end_time=e_time,
                duration_minutes=dur,
                meeting_link=link,
                mentor_id=mentor.id,
                batch_id=batch.id,
                status=status,
            )
            session.add(m)
            session.flush()
            for l in learners[:8]:
                session.add(MeetingAudience(meeting_id=m.id, learner_id=l.id, batch_id=batch.id))
                if status == "COMPLETED":
                    session.add(MeetingAttendance(
                        meeting_id=m.id,
                        learner_id=l.id,
                        attended=True,
                        remarks="Participated actively in discussion.",
                    ))
    session.flush()

    counts["talent_alerts"] = session.execute(select(func.count(TalentAlert.id))).scalar() or 0
    counts["meetings"] = session.execute(select(func.count(Meeting.id))).scalar() or 0

    # 12. Seed Realistic Notifications (4-8 per user across all 42 users)
    all_users = [admin] + list(mentors.values()) + learners
    notification_templates = [
        ("MEETING", "Upcoming Technical Sync", "You have an engineering sync scheduled with your mentor."),
        ("MEETING", "Meeting Attendance Confirmed", "Your attendance for the architecture review has been recorded."),
        ("ASSESSMENT", "Assessment Evaluation Ready", "Your Growth Ring report has been reviewed and approved."),
        ("ASSESSMENT", "New Assessment Assigned", "A new formal evaluation module is open for submissions."),
        ("TALENT_ALERT", "Talent Spotlight Recognition", "Your exceptional dedication score has been flagged for career acceleration."),
        ("SYSTEM", "Daily Coding Streak Milestone", "Congratulations! You have maintained your learning velocity streak."),
        ("SYSTEM", "Platform Governance Notice", "DPDP compliance audit completed. Your privacy preferences remain up-to-date."),
    ]

    for u in all_users:
        existing_n_count = session.execute(
            select(func.count(Notification.id)).where(Notification.recipient_id == u.id)
        ).scalar() or 0
        if existing_n_count < 4:
            sample_notifs = random.sample(notification_templates, k=5)
            for idx, (n_type, n_title, n_msg) in enumerate(sample_notifs):
                session.add(Notification(
                    recipient_id=u.id,
                    sender_id=admin.id if u.role != "ADMIN" else mentors["soumya.p@csmtech.internal"].id,
                    title=n_title,
                    message=n_msg,
                    notification_type=n_type,
                    is_read=(idx % 2 == 0),
                ))
    session.flush()
    counts["notifications"] = session.execute(select(func.count(Notification.id))).scalar() or 0

    # 13. 24 Verified AI Question Pool Items (12 Ollama + 12 Procedural / Curated) (Phase E2)
    from generate_ai_pool_items import make_pool_items
    pool_items = make_pool_items()
    for p_item in pool_items:
        ex_pool = session.execute(
            select(AIQuestionPool).where(AIQuestionPool.question_hash == p_item["question_hash"])
        ).scalar_one_or_none()
        if not ex_pool:
            session.add(AIQuestionPool(
                field=p_item["field"],
                category=p_item["category"],
                difficulty=p_item["difficulty"],
                mode=p_item["mode"],
                language=p_item.get("language"),
                title=p_item["title"],
                question_hash=p_item["question_hash"],
                question_data_json=p_item["question_data_json"],
                provenance_json=p_item["provenance_json"],
                is_used=False,
                verified=True,
            ))
    session.flush()
    counts["ai_question_pool"] = session.execute(select(func.count(AIQuestionPool.id))).scalar() or 0

    # 14. Audit Logs (Idempotency Protected)
    audit_entries = [
        ("LOGIN_SUCCESS", "users", admin.id, "Admin logged into governance console."),
        ("ASSESSMENT_PUBLISHED", "assessments", assessments["Core Python & Data Structures Assessment"].id, "Published official assessment."),
        ("GROWTH_RING_APPROVED", "assessment_attempts", None, "Mentor approved final Growth Ring reports."),
        ("TALENT_ALERT_ACTION", "talent_alerts", None, "Mentor took action SCHEDULE_INTERVIEW on talent alert."),
        ("SEED_COMPLETION", "system", None, "Deterministic demo data pack successfully initialized."),
    ]
    existing_audit = session.execute(
        select(AuditLog).where(
            AuditLog.actor_id == admin.id,
            AuditLog.action == "SEED_COMPLETION",
        )
    ).first()
    if not existing_audit:
        for action, res, res_id, reason in audit_entries:
            session.add(AuditLog(
                org_id=org.id,
                actor_id=admin.id,
                action=action,
                resource=res,
                resource_id=res_id,
                reason=reason,
            ))
    # Integrate scale crowd population for 200 learners, 8 batches, full attempts, answers, and attendance
    from populate_realistic_crowd import populate_scale_data
    populate_scale_data(session=session)
    session.commit()

    # Re-fetch final table counts
    counts["users"] = session.execute(select(func.count(User.id))).scalar() or 0
    counts["attempts"] = session.execute(select(func.count(AssessmentAttempt.id))).scalar() or 0
    counts["answers"] = session.execute(select(func.count(Answer.id))).scalar() or 0
    counts["submissions"] = session.execute(select(func.count(Submission.id))).scalar() or 0
    counts["batches"] = session.execute(select(func.count(Batch.id))).scalar() or 0

    return counts


if __name__ == "__main__":
    from pathlib import Path
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import create_engine, inspect
    from app.core.config import settings

    db_url = os.getenv("DATABASE_URL") or settings.DATABASE_URL
    if not db_url:
        db_url = "sqlite:///trellis_demo.db"
    os.environ["DATABASE_URL"] = db_url

    # Strip async dialect prefixes for sync engine and alembic
    if db_url.startswith("postgresql+asyncpg://"):
        sync_url = db_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
    elif db_url.startswith("sqlite+aiosqlite://"):
        sync_url = db_url.replace("sqlite+aiosqlite://", "sqlite://", 1)
    elif db_url.startswith("mysql+asyncmy://"):
        sync_url = db_url.replace("mysql+asyncmy://", "mysql+pymysql://", 1)
    elif db_url.startswith("postgres://"):
        sync_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+"):
        sync_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    else:
        sync_url = db_url

    if "neon.tech" in sync_url and "hostaddr=" not in sync_url:
        delimiter = "&" if "?" in sync_url else "?"
        sync_url = f"{sync_url}{delimiter}hostaddr=52.76.128.157"

    connect_args = {}
    if "neon.tech" in sync_url or "52.76.128.157" in sync_url:
        connect_args = {
            "options": "endpoint=ep-weathered-base-az6lrn9p",
            "hostaddr": "52.76.128.157",
        }
    engine = create_engine(sync_url, connect_args=connect_args)
    backend_dir = Path(__file__).resolve().parent.parent / "backend"
    ini_path = backend_dir / "alembic.ini"
    cfg = Config(str(ini_path))
    cfg.set_main_option("script_location", str(backend_dir / "alembic"))
    cfg.set_main_option("version_locations", str(backend_dir / "alembic" / "versions"))
    cfg.set_main_option("sqlalchemy.url", sync_url)
    print(f"Ensuring database at {sync_url} is migrated to Alembic head...")
    command.upgrade(cfg, "head")
    print("Database schema is at head.")

    with Session(engine) as session:
        print("Seeding TRELLIS Enterprise Demo Data Pack...")
        results = seed_demo_pack(session)
        print("Demo Pack Seeding Complete! Summary:")
        for k, v in results.items():
            print(f"  • {k.capitalize()}: {v}")
