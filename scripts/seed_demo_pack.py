"""TRELLIS Comprehensive Enterprise Demo Data Pack Seeder (Phase D).

Seeds:
- 40 Users across 4 batches (1 Admin, 3 Mentors, 36 Learners) with realistic metadata
- ~304 Question Bank Items across all 7 Enterprise Policy Categories + Additional
- 24 LeetCode-style Coding & SQL Problems across 5 languages (Python, SQL, Java, JS, C++) with test cases
- 12 Realistic Assessments across all lifecycle states (4 DRAFT, 2 SCHEDULED, 3 PUBLISHED, 3 CLOSED)
- 180+ Assessment Attempts with bell-curve scores, submitted answers, and Growth Ring reports
- 600+ AI Practice Attempts & Dedication Scores across topics
- 4 Real Talent Spotlight Alerts with mentor actions and scheduled meetings
- In-app Notifications, Qualitative Mentor Remarks, and Immutable Audit Logs
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
from app.schemas.category import AssessmentCategory

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

    # 2. Users (40 Users: 1 Admin, 3 Mentors (+2 legacy compat), 36 Learners)
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
        if not l:
            # Deterministic streak: 0 to 42 days
            streak = (idx * 7) % 43
            freezes = 1 if streak > 20 else 2
            last_active = now - timedelta(hours=(idx % 72))
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

    # 5. Coding Problems (24 Problems across 5 Languages)
    for cp_data in CODING_PROBLEMS:
        title = cp_data["title"]
        cp = session.execute(select(CodingProblem).where(CodingProblem.title == title)).scalar_one_or_none()
        if not cp:
            # Create a corresponding QuestionBank entry for the coding problem
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
    session.flush()

    counts["question_bank"] = session.execute(select(func.count(QuestionBank.id))).scalar() or 0
    counts["coding_problems"] = session.execute(select(func.count(CodingProblem.id))).scalar() or 0

    # 6. 12 Realistic Assessments across Lifecycle States
    # 4 DRAFT, 2 SCHEDULED, 3 PUBLISHED, 3 CLOSED
    assessment_specs = [
        # DRAFTS (4)
        ("Advanced Microservices Architecture", "DRAFT", "Cloud & DevOps", batches["BATCH_BETA"], 90, 70.0, mentors["soumya.p@csmtech.internal"]),
        ("Kubernetes Operator Development", "DRAFT", "Cloud & DevOps", batches["BATCH_BETA"], 75, 65.0, mentors["soumya.p@csmtech.internal"]),
        ("LLM Fine-Tuning & Evaluation Systems", "DRAFT", "Data & AI", batches["BATCH_GAMMA"], 60, 60.0, mentors["ananya.m@csmtech.internal"]),
        ("Linux Kernel Driver Programming", "DRAFT", "Core Systems", batches["BATCH_DELTA"], 120, 75.0, mentors["debashis.j@csmtech.internal"]),

        # SCHEDULED (2)
        ("Enterprise Full-Stack Capstone Assessment", "SCHEDULED", "Web & Full Stack", batches["BATCH_ALPHA"], 90, 65.0, mentors["soumya.p@csmtech.internal"]),
        ("Cloud Security & Compliance Certification Sprint", "SCHEDULED", "Cloud & DevOps", batches["BATCH_BETA"], 60, 70.0, mentors["soumya.p@csmtech.internal"]),

        # PUBLISHED / ACTIVE (3)
        ("Core Python & Data Structures Assessment", "PUBLISHED", "Web & Full Stack", batches["BATCH_ALPHA"], 60, 60.0, mentors["soumya.p@csmtech.internal"]),
        ("Enterprise SQL & Database Performance Assessment", "PUBLISHED", "Data & AI", batches["BATCH_GAMMA"], 60, 60.0, mentors["ananya.m@csmtech.internal"]),
        ("Cloud Native DevOps & CI/CD Assessment", "PUBLISHED", "Cloud & DevOps", batches["BATCH_BETA"], 75, 65.0, mentors["soumya.p@csmtech.internal"]),

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

            # Attach 5-8 questions to the assessment
            selected_qs = [q for q in bank_questions if q.field == field or q.field == "Engineering Architecture"][:8]
            if not selected_qs:
                selected_qs = bank_questions[:6]
            for seq, q in enumerate(selected_qs, 1):
                session.add(AssessmentQuestion(
                    assessment_id=a.id,
                    bank_question_id=q.id,
                    sequence_order=seq,
                    marks=10.0,
                ))
        assessments[title] = a
    session.flush()

    counts["assessments"] = session.execute(select(func.count(Assessment.id))).scalar() or 0

    # 7. 180+ Assessment Attempts with Bell Curve Scores & Growth Ring Reports
    # Focus attempts on CLOSED and PUBLISHED assessments
    scored_assessments = [
        assessments["Foundational Technical Knowledge Baseline"],
        assessments["Engineering Aptitude & Deductive Reasoning Sprint"],
        assessments["Workplace Communication & Readiness Baseline"],
        assessments["Core Python & Data Structures Assessment"],
        assessments["Enterprise SQL & Database Performance Assessment"],
        assessments["Cloud Native DevOps & CI/CD Assessment"],
    ]

    random.seed(42)  # Deterministic seed for reproducible evaluation data
    attempt_count = 0

    for a in scored_assessments:
        # Get target learners from batch
        target_learners = learners[0:10] if "ALPHA" in (a.batch.code if a.batch else "") else (
            learners[10:20] if "BETA" in (a.batch.code if a.batch else "") else (
                learners[20:28] if "GAMMA" in (a.batch.code if a.batch else "") else learners[28:36]
            )
        )
        # Also include cross-batch participants for realistic volume
        extended_learners = list(set(target_learners + learners[:25]))

        for l in extended_learners:
            existing_att = session.execute(
                select(AssessmentAttempt).where(
                    AssessmentAttempt.assessment_id == a.id,
                    AssessmentAttempt.learner_id == l.id,
                )
            ).scalar_one_or_none()

            if not existing_att:
                # Bell curve score around mean 74, stdev 12, clamped between 42 and 98
                raw_score = int(random.gauss(74, 12))
                final_score = max(42.0, min(98.0, float(raw_score)))
                passed = final_score >= a.passing_score
                start_t = (a.start_window or now) + timedelta(hours=random.randint(2, 24))
                submit_t = start_t + timedelta(minutes=random.randint(25, a.duration_minutes - 5))

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

                att = AssessmentAttempt(
                    assessment_id=a.id,
                    learner_id=l.id,
                    start_time=start_t,
                    submit_time=submit_t,
                    score=final_score,
                    total_marks=100.0,
                    passed=passed,
                    status="SUBMITTED",
                    grading_status="GRADED",
                    report_json=growth_report,
                    report_status="APPROVED" if a.status == "CLOSED" else "PENDING_APPROVAL",
                    report_approved_at=submit_t + timedelta(hours=2) if a.status == "CLOSED" else None,
                )
                session.add(att)
                session.flush()

                # Populate concrete Answers for attempt
                for aq in a.questions[:5]:
                    session.add(Answer(
                        attempt_id=att.id,
                        bank_question_id=aq.bank_question_id,
                        text_response="Optimized approach utilizing hash-map indices for linear time complexity.",
                        grading_status="GRADED",
                        score_awarded=aq.marks if passed else (aq.marks * 0.5),
                    ))

                # Create Qualitative Mentor Remark for a sample of attempts
                if attempt_count % 4 == 0:
                    session.add(MentorRemark(
                        mentor_id=a.mentor_id,
                        learner_id=l.id,
                        assessment_id=a.id,
                        remark_text=f"Demonstrated solid grasp of {a.field} fundamentals. Recommendation: continue daily coding practice on edge cases.",
                        visibility="LEARNER_AND_ADMIN",
                    ))

                attempt_count += 1
    session.flush()

    counts["attempts"] = session.execute(select(func.count(AssessmentAttempt.id))).scalar() or 0

    # 8. 600+ Practice Attempts across Categories & Dedication Scores
    practice_fields = ["Python", "SQL", "Java", "JavaScript", "C++", "Cloud & DevOps", "Data & AI"]
    practice_count = 0

    for l in learners:
        for f in practice_fields[:4]:
            ps = PracticeSession(
                learner_id=l.id,
                field=f,
                difficulty="MEDIUM",
                mode="MCQ",
                completed_at=now - timedelta(days=random.randint(1, 14)),
            )
            session.add(ps)
            session.flush()

            # Add 4-5 practice questions and attempts per session
            for q_idx in range(4):
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
                practice_count += 1

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

    # 9. 4 Real Talent Spotlight Alerts with Mentor Actions & Scheduled Meetings
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

            # If interview scheduled, create matching meeting
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

    # 9b. Additional Realistic Meetings (Architecture workshops, 1:1s, retros)
    meeting_specs = [
        ("Cloud Architecture Sync - Batch Alpha", "Weekly review of distributed systems patterns.", (now + timedelta(days=1)).strftime("%Y-%m-%d"), "10:00", "11:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-cloud-sync", mentors["soumya.p@csmtech.internal"], batches["BATCH_ALPHA"]),
        ("Data Pipeline Optimization Clinic", "Deep dive into Spark shuffle tuning and Parquet partitioning.", (now + timedelta(days=2)).strftime("%Y-%m-%d"), "15:00", "16:30", 90, "https://teams.microsoft.com/l/meetup-join/csm-data-clinic", mentors["ananya.m@csmtech.internal"], batches["BATCH_GAMMA"]),
        ("Linux Systems Programming Office Hours", "Q&A on POSIX threads, memory layout, and kernel diagnostics.", (now + timedelta(days=3)).strftime("%Y-%m-%d"), "11:00", "12:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-systems-oh", mentors["debashis.j@csmtech.internal"], batches["BATCH_DELTA"]),
        ("DevOps CI/CD Deployment Walkthrough", "Live demonstration of zero-downtime rolling deployments on K8s.", (now - timedelta(days=2)).strftime("%Y-%m-%d"), "14:00", "15:30", 90, "https://teams.microsoft.com/l/meetup-join/csm-devops-demo", mentors["soumya.p@csmtech.internal"], batches["BATCH_BETA"]),
        ("Engineering Aptitude Debrief Session", "Review of quantitative reasoning and deductive logic patterns.", (now - timedelta(days=5)).strftime("%Y-%m-%d"), "16:00", "17:00", 60, "https://teams.microsoft.com/l/meetup-join/csm-aptitude-debrief", mentors["soumya.p@csmtech.internal"], batches["BATCH_ALPHA"]),
    ]
    for m_title, desc, m_date, s_time, e_time, dur, link, mentor, batch in meeting_specs:
        ex_m = session.execute(select(Meeting).where(Meeting.title == m_title)).scalar_one_or_none()
        if not ex_m:
            status = "COMPLETED" if m_date < now.strftime("%Y-%m-%d") else "SCHEDULED"
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
            for l in learners[:6]:
                session.add(MeetingAudience(meeting_id=m.id, learner_id=l.id, batch_id=batch.id))
                if status == "COMPLETED":
                    session.add(MeetingAttendance(
                        meeting_id=m.id,
                        learner_id=l.id,
                        attended=True,
                        remarks="Actively participated in Q&A session.",
                    ))
    session.flush()

    counts["talent_alerts"] = session.execute(select(func.count(TalentAlert.id))).scalar() or 0
    counts["meetings"] = session.execute(select(func.count(Meeting.id))).scalar() or 0

    # 10. Audit Logs
    audit_entries = [
        ("LOGIN_SUCCESS", "users", admin.id, "Admin logged into governance console."),
        ("ASSESSMENT_PUBLISHED", "assessments", assessments["Core Python & Data Structures Assessment"].id, "Published official assessment."),
        ("GROWTH_RING_APPROVED", "assessment_attempts", None, "Mentor approved final Growth Ring reports."),
        ("TALENT_ALERT_ACTION", "talent_alerts", None, "Mentor took action SCHEDULE_INTERVIEW on talent alert."),
    ]
    for action, res, res_id, reason in audit_entries:
        session.add(AuditLog(
            org_id=org.id,
            actor_id=admin.id,
            action=action,
            resource=res,
            resource_id=res_id,
            reason=reason,
        ))
    session.commit()

    return counts


if __name__ == "__main__":
    from pathlib import Path
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import create_engine, inspect

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        db_url = "sqlite:///trellis_demo.db"
        os.environ["DATABASE_URL"] = db_url

    engine = create_engine(db_url)
    insp = inspect(engine)
    if "organisations" not in insp.get_table_names():
        print(f"📦 Database at {db_url} is empty. Running Alembic migrations to head...")
        backend_dir = Path(__file__).resolve().parent.parent / "backend"
        ini_path = backend_dir / "alembic.ini"
        cfg = Config(str(ini_path))
        cfg.set_main_option("script_location", str(backend_dir / "alembic"))
        cfg.set_main_option("version_locations", str(backend_dir / "alembic" / "versions"))
        cfg.set_main_option("sqlalchemy.url", db_url)
        command.upgrade(cfg, "head")
        print("✅ Migrations applied successfully.")

    with Session(engine) as session:
        print("🌱 Seeding TRELLIS Enterprise Demo Data Pack...")
        results = seed_demo_pack(session)
        print("✨ Demo Pack Seeding Complete! Summary:")
        for k, v in results.items():
            print(f"  • {k.capitalize()}: {v}")
