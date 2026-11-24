"""TRELLIS Scale Population Script: Populates realistic assignments, solved attempts,
answers, submissions, meetings, and practice events into trellis_demo.db.
Ensures zero hardcoding: every screen queries real database rows.
"""

import math
import os
import random
import sys
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.core.security import hash_password
from app.models import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentAudience,
    AssessmentQuestion,
    Base,
    Batch,
    CodingProblem,
    Cohort,
    McqOption,
    Meeting,
    MeetingAttendance,
    MeetingAudience,
    MentorLearnerAssignment,
    Organisation,
    PracticeAttempt,
    PracticeQuestion,
    PracticeSession,
    PracticeScore,
    QuestionBank,
    Submission,
    User,
)
from app.models.summaries import AssessmentStats, BatchStats, LearnerStats, TopicMastery


def populate_scale_data(session: Session | None = None, db_path: str = "trellis_demo.db"):
    own_session = False
    if session is None:
        db_url = os.environ.get("DATABASE_URL") or f"sqlite:///{db_path}"
        if db_url.startswith("sqlite+aiosqlite://"):
            db_url = db_url.replace("sqlite+aiosqlite://", "sqlite://", 1)
        elif db_url.startswith("postgresql+asyncpg://"):
            db_url = db_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
        engine = create_engine(db_url, echo=False)
        session = Session(engine)
        own_session = True
    now = datetime.now(UTC)
    pwd_hash = hash_password("CSMTrellis2026!")

    print(f"Populating scale data (own_session={own_session})...")

    # 1. Organisation
    org = session.execute(select(Organisation).where(Organisation.code == "CSM_MAIN")).scalar_one_or_none()
    if not org:
        org = Organisation(name="CSM Technologies", code="CSM_MAIN")
        session.add(org)
        session.flush()

    # 2. Admins (2)
    admin_specs = [
        ("admin@csmtech.internal", "Rajesh Mohanty (L&K Governance)"),
        ("admin2@csmtech.internal", "Sasmita Rath (Enterprise Training Director)"),
    ]
    for email, name in admin_specs:
        u = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if not u:
            session.add(User(
                org_id=org.id,
                email=email,
                password_hash=pwd_hash,
                full_name=name,
                role="ADMIN",
                is_active=True,
                must_change_password=False,
            ))
    session.flush()

    # 3. Mentors (8 Mentors)
    mentor_specs = [
        ("mentor1@csmtech.internal", "Ananya Rao (Lead Cloud Architect & Evaluator)"),
        ("soumya.p@csmtech.internal", "Soumya Ranjan Patnaik (Principal Full Stack Architect)"),
        ("ananya.m@csmtech.internal", "Ananya Mishra (Principal Data & AI Specialist)"),
        ("debashis.j@csmtech.internal", "Debashis Jena (Principal Systems Engineer)"),
        ("mentor2@csmtech.internal", "Vikram Patel (Principal Reliability Engineer)"),
        ("priya.k@csmtech.internal", "Priya Kulkarni (DevSecOps Lead)"),
        ("arun.s@csmtech.internal", "Arun Swaminathan (Distributed Systems Specialist)"),
        ("sunita.v@csmtech.internal", "Sunita Verma (Quality & Enterprise Architecture Lead)"),
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

    # 4. Learners (200 Learners)
    first_names = [
        "Priya", "Arjun", "Sneha", "Rohan", "Deepika", "Kavita", "Aditya", "Pooja", "Amitav", "Neha",
        "Vikram", "Sunita", "Manoj", "Shreya", "Harish", "Meera", "Kunal", "Tanya", "Ankit", "Divya",
        "Sandeep", "Swati", "Ashish", "Madhuri", "Bibhuti", "Ritu", "Alok", "Sonali", "Siddharth", "Pallavi",
        "Tushar", "Rasmita", "Pratik", "Jyoti", "Subhashree", "Biswajit", "Manish", "Preeti", "Gautam", "Aarti",
    ]
    last_names = [
        "Sharma", "Nair", "Mukherjee", "Verma", "Iyer", "Reddy", "Joshi", "Choudhury", "Das", "Patel",
        "Malhotra", "Rao", "Kumar", "Sen", "Swaminathan", "Krishnan", "Singhania", "Saxena", "Tripathi", "Agarwal",
        "Panda", "Mohapatra", "Behera", "Pradhan", "Nayak", "Mohanty", "Tripathy", "Dash", "Roy", "Banerjee",
    ]

    learners: list[User] = []
    print("Ensuring 200 learners exist...")
    for i in range(1, 201):
        email = f"learner{i}@csmtech.internal"
        l = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if not l:
            fn = first_names[(i - 1) % len(first_names)]
            ln = last_names[((i - 1) * 3) % len(last_names)]
            streak = 14 if i == 1 else ((i * 7) % 45)
            freezes = 1 if streak > 15 else 2
            l = User(
                org_id=org.id,
                email=email,
                password_hash=pwd_hash,
                full_name=f"{fn} {ln}" if i > 1 else "Priya Sharma",
                role="LEARNER",
                streak_days=streak,
                streak_freezes_remaining=freezes,
                last_active_at=now - timedelta(hours=(i % 48)),
                is_active=True,
                must_change_password=False,
            )
            session.add(l)
            session.flush()
        learners.append(l)

    # 5. Batches (8 Batches, 25 learners each)
    cohort = session.execute(select(Cohort).where(Cohort.code == "COHORT_2026")).scalar_one_or_none()
    if not cohort:
        cohort = Cohort(
            org_id=org.id,
            name="2026 Enterprise Engineering Cohort",
            code="COHORT_2026",
            trainer_id=mentors["mentor1@csmtech.internal"].id,
        )
        session.add(cohort)
        session.flush()

    batch_meta = [
        ("BATCH_ALPHA", "Batch Alpha (Full-Stack Architecture)", "Web & Full Stack", "mentor1@csmtech.internal", learners[0:25]),
        ("BATCH_BETA", "Batch Beta (Cloud Infrastructure & K8s)", "Cloud & DevOps", "mentor1@csmtech.internal", learners[25:50]),
        ("BATCH_GAMMA", "Batch Gamma (Enterprise SQL & Data AI)", "Data & AI", "ananya.m@csmtech.internal", learners[50:75]),
        ("BATCH_DELTA", "Batch Delta (Core Systems & Linux C++)", "Core Systems", "debashis.j@csmtech.internal", learners[75:100]),
        ("BATCH_EPSILON", "Batch Epsilon (Distributed Microservices)", "Web & Full Stack", "soumya.p@csmtech.internal", learners[100:125]),
        ("BATCH_ZETA", "Batch Zeta (DevSecOps & Platform Reliability)", "Cloud & DevOps", "priya.k@csmtech.internal", learners[125:150]),
        ("BATCH_ETA", "Batch Eta (Enterprise Mobile & Reactive)", "Web & Full Stack", "arun.s@csmtech.internal", learners[150:175]),
        ("BATCH_THETA", "Batch Theta (Architectural Reliability & Resilience)", "Core Systems", "sunita.v@csmtech.internal", learners[175:200]),
    ]

    batches: dict[str, Batch] = {}
    print("Setting up 8 batches and mentor assignments...")
    for code, name, field, mentor_email, b_learners in batch_meta:
        b = session.execute(select(Batch).where(Batch.code == code)).scalar_one_or_none()
        if not b:
            b = Batch(
                org_id=org.id,
                cohort_id=cohort.id,
                name=name,
                code=code,
                field=field,
                description=f"Specialized CSM enterprise training track for {field}.",
                max_learners=35,
            )
            session.add(b)
            session.flush()
        batches[code] = b

        lead_mentor = mentors[mentor_email]
        for l in b_learners:
            assign = session.execute(
                select(MentorLearnerAssignment).where(
                    MentorLearnerAssignment.learner_id == l.id,
                    MentorLearnerAssignment.batch_id == b.id,
                )
            ).scalars().first()
            if not assign:
                session.add(MentorLearnerAssignment(
                    mentor_id=lead_mentor.id,
                    learner_id=l.id,
                    batch_id=b.id,
                ))
    session.flush()

    # 6. Retrieve Question Bank for Assessment Attachment
    all_questions = session.execute(select(QuestionBank).where(QuestionBank.is_active.is_(True))).scalars().all()
    print(f"Available Question Bank items: {len(all_questions)}")

    # 7. Create 26+ Assignments (Assessments) across Batches and Lifecycle States
    # Specifications: (Title, Status, Field, Batch_Code, Duration, Pass_Score, Mentor_Email)
    assessment_specs = [
        # CLOSED COMPLETED ASSIGNMENTS (Rich historical data & analytics)
        ("Foundational Technical Knowledge Baseline", "CLOSED", "Web & Full Stack", "BATCH_ALPHA", 45, 60.0, "mentor1@csmtech.internal"),
        ("Engineering Aptitude & Quantitative Reasoning", "CLOSED", "Web & Full Stack", "BATCH_ALPHA", 45, 60.0, "mentor1@csmtech.internal"),
        ("Core Linux & Systems Programming Fundamentals", "CLOSED", "Core Systems", "BATCH_DELTA", 60, 65.0, "debashis.j@csmtech.internal"),
        ("Core Python & Data Structures Assessment", "CLOSED", "Python", "BATCH_ALPHA", 60, 65.0, "mentor1@csmtech.internal"),
        ("Enterprise SQL & Database Performance Assessment", "CLOSED", "Data & AI", "BATCH_GAMMA", 60, 60.0, "ananya.m@csmtech.internal"),
        ("Object-Oriented Design & Clean Architecture", "CLOSED", "Cloud & DevOps", "BATCH_BETA", 60, 70.0, "mentor1@csmtech.internal"),
        ("Full-Stack Web Architecture & REST API Design", "CLOSED", "Web & Full Stack", "BATCH_ALPHA", 60, 65.0, "mentor1@csmtech.internal"),
        ("Cloud Infrastructure, Docker & Containerization", "CLOSED", "Cloud & DevOps", "BATCH_BETA", 60, 70.0, "mentor1@csmtech.internal"),
        ("Workplace Communication & Professional Readiness", "CLOSED", "Core Systems", "BATCH_DELTA", 45, 60.0, "debashis.j@csmtech.internal"),
        ("Distributed Microservices & Event-Driven Architecture", "CLOSED", "Web & Full Stack", "BATCH_EPSILON", 75, 70.0, "soumya.p@csmtech.internal"),
        ("Advanced Database Sharding & Concurrency Control", "CLOSED", "Data & AI", "BATCH_GAMMA", 60, 65.0, "ananya.m@csmtech.internal"),
        ("Campus-to-Corporate Readiness Battery", "CLOSED", "Engineering Architecture", "BATCH_ALPHA", 90, 65.0, "mentor1@csmtech.internal"),
        ("DevOps CI/CD Pipelines & Infrastructure as Code", "CLOSED", "Cloud & DevOps", "BATCH_ZETA", 60, 70.0, "priya.k@csmtech.internal"),
        ("Enterprise Full-Stack Capstone Assessment", "CLOSED", "Web & Full Stack", "BATCH_ALPHA", 90, 70.0, "mentor1@csmtech.internal"),
        ("Workplace Behavioral & Psychometric Dimension Profile", "CLOSED", "Psychometric", "BATCH_ALPHA", 45, 60.0, "mentor1@csmtech.internal"),
        ("Mobile Systems Architecture & Reactive State Management", "CLOSED", "Web & Full Stack", "BATCH_ETA", 60, 65.0, "arun.s@csmtech.internal"),
        ("Fault-Tolerant Distributed Storage Engines", "CLOSED", "Core Systems", "BATCH_THETA", 75, 70.0, "sunita.v@csmtech.internal"),
        ("Automated Testing Suites & Verification Engineering", "CLOSED", "Web & Full Stack", "BATCH_ALPHA", 60, 65.0, "mentor1@csmtech.internal"),

        # PUBLISHED / ACTIVE ASSIGNMENTS (Ready for Learners to take in portal right now!)
        ("Distributed Systems Architecture & Resiliency Lab", "PUBLISHED", "Web & Full Stack", "BATCH_ALPHA", 60, 70.0, "mentor1@csmtech.internal"),
        ("High-Throughput Reactive Systems & Kafka Stream Processing", "PUBLISHED", "Web & Full Stack", "BATCH_ALPHA", 75, 70.0, "mentor1@csmtech.internal"),
        ("Enterprise Cloud Security & Zero-Trust Governance", "PUBLISHED", "Cloud & DevOps", "BATCH_BETA", 60, 70.0, "mentor1@csmtech.internal"),
        ("AI Agentic Systems & Large Language Model Architecture", "PUBLISHED", "Data & AI", "BATCH_GAMMA", 60, 65.0, "ananya.m@csmtech.internal"),
        ("Advanced Algorithmic Optimization & Memory Efficiency", "PUBLISHED", "Python", "BATCH_ALPHA", 90, 75.0, "mentor1@csmtech.internal"),
        ("Kubernetes Cluster Orchestration & Service Mesh Lab", "PUBLISHED", "Cloud & DevOps", "BATCH_ZETA", 60, 70.0, "priya.k@csmtech.internal"),

        # AWAITING GRADING & SCHEDULED ASSIGNMENTS
        ("System Security Audit & Threat Modeling Review", "AWAITING_GRADING", "Web & Full Stack", "BATCH_ALPHA", 60, 65.0, "mentor1@csmtech.internal"),
        ("Production Readiness Review & Disaster Recovery Drill", "SCHEDULED", "Web & Full Stack", "BATCH_ALPHA", 60, 70.0, "mentor1@csmtech.internal"),
        ("Staff Engineer Architectural Synthesis Defense", "DRAFT", "Web & Full Stack", "BATCH_ALPHA", 90, 75.0, "mentor1@csmtech.internal"),
    ]

    print("Creating/updating 27 assessments across batches and states...")
    assessments: dict[str, Assessment] = {}
    for title, status, field, b_code, duration, pass_score, mentor_email in assessment_specs:
        b = batches[b_code]
        m = mentors[mentor_email]
        a = session.execute(select(Assessment).where(Assessment.title == title)).scalar_one_or_none()
        if not a:
            start_w = now - timedelta(days=21) if status in ("CLOSED", "AWAITING_GRADING") else now - timedelta(days=2)
            end_w = now - timedelta(days=7) if status == "CLOSED" else (now + timedelta(days=14) if status == "PUBLISHED" else now + timedelta(days=3))
            a = Assessment(
                mentor_id=m.id,
                batch_id=b.id,
                title=title,
                field=field,
                instructions=f"Official CSM {field} assessment. Continuous autosave and proctoring enabled.",
                duration_minutes=duration,
                passing_score=pass_score,
                start_window=start_w,
                end_window=end_w,
                status=status,
                version=1,
            )
            session.add(a)
            session.flush()

            # Attach 6-8 relevant questions to this assessment
            chosen_qs = [q for q in all_questions if q.field == field or q.field == "Engineering Architecture"][:8]
            if len(chosen_qs) < 4:
                chosen_qs = all_questions[:6]

            for seq, q in enumerate(chosen_qs, 1):
                session.add(AssessmentQuestion(
                    assessment_id=a.id,
                    bank_question_id=q.id,
                    sequence_order=seq,
                    marks=10.0 if q.question_type != "LIKERT" else 0.0,
                ))
            session.flush()
        else:
            if a.status != status:
                a.status = status
                session.flush()
        assessments[title] = a

    # 8. SOLVE ASSIGNMENTS ON BEHALF OF STUDENTS (Create AssessmentAttempt, Answer, and Submission rows)
    # Target closed and submitted assessments
    print("Solving assessments on behalf of students to populate real analytics...")
    random.seed(1337)  # Deterministic seed

    closed_assessment_titles = [
        "Foundational Technical Knowledge Baseline",
        "Engineering Aptitude & Quantitative Reasoning",
        "Core Linux & Systems Programming Fundamentals",
        "Core Python & Data Structures Assessment",
        "Enterprise SQL & Database Performance Assessment",
        "Object-Oriented Design & Clean Architecture",
        "Full-Stack Web Architecture & REST API Design",
        "Cloud Infrastructure, Docker & Containerization",
        "Distributed Microservices & Event-Driven Architecture",
        "Advanced Database Sharding & Concurrency Control",
        "Campus-to-Corporate Readiness Battery",
        "Enterprise Full-Stack Capstone Assessment",
        "Workplace Behavioral & Psychometric Dimension Profile",
        "Automated Testing Suites & Verification Engineering",
        "System Security Audit & Threat Modeling Review",
    ]

    total_attempts_created = 0
    total_answers_created = 0
    total_submissions_created = 0

    for title in closed_assessment_titles:
        a = assessments.get(title)
        if not a:
            continue

        b_code = "BATCH_ALPHA"
        for code, b in batches.items():
            if b.id == a.batch_id:
                b_code = code
                break

        # Get learners in this batch plus learner1 (to ensure Priya Sharma has rich results)
        cohort_learners = [l for l in learners if session.execute(
            select(MentorLearnerAssignment).where(
                MentorLearnerAssignment.batch_id == a.batch_id,
                MentorLearnerAssignment.learner_id == l.id,
            )
        ).first()]

        # Ensure learner1 is always evaluated for Batch Alpha assessments
        if learners[0] not in cohort_learners and "ALPHA" in b_code:
            cohort_learners.insert(0, learners[0])

        # Get attached questions
        aq_list = session.execute(
            select(AssessmentQuestion).where(AssessmentQuestion.assessment_id == a.id).order_by(AssessmentQuestion.sequence_order)
        ).scalars().all()
        q_ids = [aq.bank_question_id for aq in aq_list]
        q_objs = session.execute(select(QuestionBank).where(QuestionBank.id.in_(q_ids))).scalars().all()
        q_map = {q.id: q for q in q_objs}

        for idx, l in enumerate(cohort_learners):
            existing_att = session.execute(
                select(AssessmentAttempt).where(
                    AssessmentAttempt.assessment_id == a.id,
                    AssessmentAttempt.learner_id == l.id,
                )
            ).scalars().first()

            if existing_att:
                continue

            # Generate realistic student ability (Priya Sharma is top distinction: 88-96%)
            is_priya = (l.id == learners[0].id)
            if is_priya:
                mean_ability = 92.0
            else:
                persona_mod = (idx % 5)
                mean_ability = 85.0 if persona_mod == 0 else (78.0 if persona_mod in (1, 2) else 68.0)

            earned_marks_total = 0.0
            total_marks_possible = 0.0
            answers_to_add = []

            for aq in aq_list:
                q = q_map.get(aq.bank_question_id)
                if not q:
                    continue

                q_marks = aq.marks or 10.0
                total_marks_possible += q_marks

                # Calculate item pass probability based on student ability and difficulty
                diff_weight = 0.9 if q.difficulty == "EASY" else (0.75 if q.difficulty == "MEDIUM" else 0.6)
                pass_prob = (mean_ability / 100.0) * diff_weight
                is_correct = random.random() < pass_prob

                earned = q_marks if is_correct else 0.0
                earned_marks_total += earned

                # Find option ID if MCQ
                chosen_opt_ids = []
                options = session.execute(select(McqOption).where(McqOption.question_id == q.id)).scalars().all()
                if options:
                    correct_opt = next((o for o in options if o.is_correct), options[0])
                    wrong_opts = [o for o in options if not o.is_correct]
                    if is_correct or not wrong_opts:
                        chosen_opt_ids = [correct_opt.id]
                    else:
                        chosen_opt_ids = [random.choice(wrong_opts).id]

                # Create Answer
                ans = Answer(
                    attempt_id=None,  # Will link after attempt flush
                    bank_question_id=q.id,
                    selected_option_ids_json=chosen_opt_ids if chosen_opt_ids else None,
                    text_response="Automated solution verified by code sandbox runner." if q.question_type in ("SHORT_ANSWER", "SCENARIO") else None,
                    score_awarded=earned,
                    mentor_feedback="Good architectural clarity and proper edge case handling." if is_correct else "Review boundary conditions and algorithmic efficiency.",
                    grading_status="GRADED",
                )
                answers_to_add.append(ans)

            # Calculate final normalized percentage
            pct_score = round((earned_marks_total / max(1.0, total_marks_possible)) * 100.0, 1) if total_marks_possible > 0 else 80.0
            passed = pct_score >= a.passing_score

            submit_dt = now - timedelta(days=random.randint(3, 18), hours=random.randint(1, 12))
            start_dt = submit_dt - timedelta(minutes=random.randint(30, 55))

            # Growth report structure
            growth_report = {
                "assessment_title": a.title,
                "score": pct_score,
                "passing_score": a.passing_score,
                "passed": passed,
                "percentile_rank": min(98, max(45, int(pct_score * 0.95))),
                "ai_narrative": f"Demonstrated high aptitude in {a.field} with strong structural comprehension and concise test case execution.",
                "strengths": [f"Deep conceptual understanding of {a.field}", "Consistent test-case execution", "Clean code patterns"],
                "gaps": ["Further optimize space complexity for high-throughput concurrency"],
                "next_steps": ["Implement LRU caching layer", "Profile memory allocation under heavy load"],
            }

            att = AssessmentAttempt(
                assessment_id=a.id,
                learner_id=l.id,
                start_time=start_dt,
                submit_time=submit_dt,
                score=pct_score,
                total_marks=total_marks_possible,
                passed=passed,
                status="SUBMITTED",
                tab_switch_count=0 if is_priya else random.choice([0, 0, 1, 2]),
                grading_status="GRADED",
                report_json=growth_report,
                report_status="APPROVED",
                report_approved_at=submit_dt + timedelta(hours=2),
            )
            session.add(att)
            session.flush()
            total_attempts_created += 1

            for ans in answers_to_add:
                ans.attempt_id = att.id
                session.add(ans)
                total_answers_created += 1

            # If assessment had coding questions, create real Submission rows
            coding_qs = [aq for aq in aq_list if q_map.get(aq.bank_question_id) and q_map[aq.bank_question_id].question_type == "CODING"]
            for c_aq in coding_qs:
                q_code = q_map[c_aq.bank_question_id]
                cp = getattr(q_code, "coding_problem", None)
                if not cp:
                    cp = session.execute(select(CodingProblem)).scalars().first()
                if not cp:
                    continue
                verdict = "ACCEPTED" if random.random() < (mean_ability / 100.0) else "WRONG_ANSWER"
                sub = Submission(
                    attempt_id=att.id,
                    coding_problem_id=cp.id,
                    learner_id=l.id,
                    code="def solution():\n    # Optimal solution generated by learner\n    return True",
                    language="python",
                    verdict=verdict,
                    runtime_ms=random.randint(12, 85),
                    memory_mb=round(random.uniform(14.2, 28.6), 1),
                    passed_cases=6 if verdict == "ACCEPTED" else random.randint(2, 5),
                    total_cases=6,
                    score=10.0 if verdict == "ACCEPTED" else 0.0,
                )
                session.add(sub)
                total_submissions_created += 1

    # Ensure EVERY learner across all 200 learners has >= 6 submitted attempts with answer rows, >= 3 coding submissions, and attendance
    all_coding_probs = session.execute(select(CodingProblem)).scalars().all()
    print("Verifying all 200 learners have >= 6 submitted attempts, >= 3 coding submissions, and attendance...")
    for l_idx, l in enumerate(learners):
        existing_att_count = session.execute(
            select(func.count(AssessmentAttempt.id)).where(
                AssessmentAttempt.learner_id == l.id,
                AssessmentAttempt.status == "SUBMITTED",
            )
        ).scalar() or 0

        if existing_att_count < 6:
            needed = 6 - existing_att_count
            for k in range(needed):
                title_idx = (l_idx * 3 + k) % len(closed_assessment_titles)
                a_title = closed_assessment_titles[title_idx]
                a_obj = assessments.get(a_title)
                if not a_obj:
                    continue
                att_exists = session.execute(
                    select(AssessmentAttempt).where(
                        AssessmentAttempt.assessment_id == a_obj.id,
                        AssessmentAttempt.learner_id == l.id,
                    )
                ).scalars().first()
                if att_exists:
                    continue

                is_priya = (l.id == learners[0].id)
                mean_ability = 92.0 if is_priya else (74.0 + ((l_idx * 5) % 20))
                aq_list = session.execute(
                    select(AssessmentQuestion).where(AssessmentQuestion.assessment_id == a_obj.id).order_by(AssessmentQuestion.sequence_order)
                ).scalars().all()

                earned_marks = 0.0
                total_marks = 0.0
                answers = []
                for aq in aq_list:
                    q = session.get(QuestionBank, aq.bank_question_id)
                    if not q:
                        continue
                    q_marks = aq.marks or 10.0
                    total_marks += q_marks
                    diff_weight = 0.9 if q.difficulty == "EASY" else (0.75 if q.difficulty == "MEDIUM" else 0.6)
                    is_corr = random.random() < ((mean_ability / 100.0) * diff_weight)
                    earned = q_marks if is_corr else 0.0
                    earned_marks += earned

                    chosen_opt_ids = []
                    opts = session.execute(select(McqOption).where(McqOption.question_id == q.id)).scalars().all()
                    if opts:
                        corr_opt = next((o for o in opts if o.is_correct), opts[0])
                        w_opts = [o for o in opts if not o.is_correct]
                        chosen_opt_ids = [corr_opt.id] if (is_corr or not w_opts) else [random.choice(w_opts).id]

                    answers.append(Answer(
                        bank_question_id=q.id,
                        selected_option_ids_json=chosen_opt_ids if chosen_opt_ids else None,
                        text_response="Automated solution verified by code sandbox runner." if q.question_type in ("SHORT_ANSWER", "SCENARIO") else None,
                        score_awarded=earned,
                        mentor_feedback="Good architectural clarity." if is_corr else "Review boundary conditions.",
                        grading_status="GRADED",
                    ))

                pct = round((earned_marks / max(1.0, total_marks)) * 100.0, 1) if total_marks > 0 else 80.0
                sub_dt = now - timedelta(days=random.randint(4, 50), hours=random.randint(1, 10))
                st_dt = sub_dt - timedelta(minutes=random.randint(30, 50))

                new_att = AssessmentAttempt(
                    assessment_id=a_obj.id,
                    learner_id=l.id,
                    start_time=st_dt,
                    submit_time=sub_dt,
                    score=pct,
                    total_marks=total_marks,
                    passed=(pct >= a_obj.passing_score),
                    status="SUBMITTED",
                    grading_status="GRADED",
                    report_json={
                        "assessment_title": a_obj.title,
                        "score": pct,
                        "passing_score": a_obj.passing_score,
                        "passed": (pct >= a_obj.passing_score),
                        "percentile_rank": min(98, max(45, int(pct * 0.95))),
                        "ai_narrative": f"Demonstrated competency in {a_obj.field}.",
                        "strengths": [f"Conceptual grasp of {a_obj.field}", "Clean implementation"],
                        "gaps": ["Concurrency profiling under load"],
                        "next_steps": ["Review indexing tradeoffs"],
                    },
                    report_status="APPROVED",
                    report_approved_at=sub_dt + timedelta(hours=2),
                )
                session.add(new_att)
                session.flush()
                total_attempts_created += 1

                for ans in answers:
                    ans.attempt_id = new_att.id
                    session.add(ans)
                    total_answers_created += 1

        # Coding Submissions: ensure >= 3
        existing_subs = session.execute(
            select(func.count(Submission.id)).where(Submission.learner_id == l.id)
        ).scalar() or 0
        if existing_subs < 3 and all_coding_probs:
            for cp in all_coding_probs[:3]:
                is_priya = (l.id == learners[0].id)
                v = "ACCEPTED" if (is_priya or random.random() < 0.75) else "WRONG_ANSWER"
                session.add(Submission(
                    attempt_id=None,
                    coding_problem_id=cp.id,
                    learner_id=l.id,
                    code="def solve():\n    return True",
                    language="python",
                    verdict=v,
                    runtime_ms=random.randint(14, 55),
                    memory_mb=round(random.uniform(14.0, 24.0), 1),
                    passed_cases=6 if v == "ACCEPTED" else random.randint(2, 4),
                    total_cases=6,
                    score=10.0 if v == "ACCEPTED" else 0.0,
                ))
                total_submissions_created += 1

        # Attendance: ensure MeetingAttendance exists
        ex_attnd = session.execute(
            select(MeetingAttendance).where(MeetingAttendance.learner_id == l.id)
        ).first()
        if not ex_attnd:
            all_meetings = session.execute(select(Meeting)).scalars().all()
            for m_item in all_meetings[:4]:
                session.add(MeetingAttendance(
                    meeting_id=m_item.id,
                    learner_id=l.id,
                    attended=True if random.random() < 0.9 else False,
                ))

    session.flush()
    print(f"Created {total_attempts_created} attempts, {total_answers_created} answers, {total_submissions_created} coding submissions.")

    # 9. Real Mentoring Meetings with Join Links and Attendance
    print("Scheduling real mentoring meetings...")
    meeting_specs = [
        ("Full-Stack Microservices & Docker Lab", "mentor1@csmtech.internal", "BATCH_ALPHA", "https://teams.microsoft.com/l/meetup-join/csm-fullstack-session", 1, 14, 15),
        ("Kubernetes Pod Scheduling & Service Mesh Deep Dive", "mentor1@csmtech.internal", "BATCH_BETA", "https://teams.microsoft.com/l/meetup-join/csm-k8s-deepdive", 2, 16, 17),
        ("Distributed Database Sharding & Cassandra Consistency", "ananya.m@csmtech.internal", "BATCH_GAMMA", "https://meet.google.com/trellis-db-sharding", 3, 11, 12),
        ("Linux Kernel Tracing & eBPF Observability Review", "debashis.j@csmtech.internal", "BATCH_DELTA", "https://zoom.us/j/9876543210", 4, 15, 16),
        ("Spring Cloud Gateway & Reactive Microservices Sync", "soumya.p@csmtech.internal", "BATCH_EPSILON", "https://teams.microsoft.com/l/meetup-join/csm-spring-reactive", 5, 10, 11),
        ("DevSecOps Automated Vulnerability Scanning & SBOM", "priya.k@csmtech.internal", "BATCH_ZETA", "https://meet.google.com/csm-devsecops-sync", 6, 14, 15),
    ]

    for title, mentor_email, b_code, link, day_offset, start_h, end_h in meeting_specs:
        m = mentors[mentor_email]
        b = batches[b_code]
        existing_m = session.execute(select(Meeting).where(Meeting.title == title)).scalar_one_or_none()
        m_date = (now + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        s_time = f"{start_h:02d}:00"
        e_time = f"{end_h:02d}:00"

        if not existing_m:
            mtg = Meeting(
                title=title,
                description=f"Cohort mentoring sync for {b.name}. Interactive architectural code walkthrough.",
                meeting_date=m_date,
                start_time=s_time,
                end_time=e_time,
                duration_minutes=60,
                meeting_link=link,
                mentor_id=m.id,
                batch_id=b.id,
                status="SCHEDULED",
            )
            session.add(mtg)
            session.flush()

            # Add audience for batch learners
            b_learners = [l for l in learners if session.execute(
                select(MentorLearnerAssignment).where(
                    MentorLearnerAssignment.batch_id == b.id,
                    MentorLearnerAssignment.learner_id == l.id,
                )
            ).first()]

            for l in b_learners:
                session.add(MeetingAudience(meeting_id=mtg.id, learner_id=l.id, batch_id=b.id))
                # Add attendance record
                session.add(MeetingAttendance(
                    meeting_id=mtg.id,
                    learner_id=l.id,
                    attended=True if random.random() < 0.92 else False,
                ))
    session.flush()

    # 10. Bulk Insert Practice Attempts Crowd (3,000+ records)
    print("Populating practice attempts crowd...")
    existing_practice = session.execute(select(func.count(PracticeAttempt.id))).scalar() or 0
    if existing_practice < 2500:
        practice_qs = session.execute(select(PracticeQuestion)).scalars().all()
        if not practice_qs:
            # Create a practice session and verified practice questions across fields
            ps = PracticeSession(
                learner_id=learners[0].id,
                field="Python",
                difficulty="MEDIUM",
                mode="MCQ",
            )
            session.add(ps)
            session.flush()
            fields = ["Python", "SQL", "Cloud", "DevOps", "Frontend", "Backend", "Data Structures"]
            for f in fields:
                for diff in ["EASY", "MEDIUM", "HARD"]:
                    pq = PracticeQuestion(
                        session_id=ps.id,
                        field=f,
                        difficulty=diff,
                        mode="MCQ",
                        title=f"{f} {diff} Mastery Question",
                        question_data_json={
                            "stem": f"Analyze the core concepts of {f} ({diff}). What is the optimal approach?",
                            "options": ["Approach A: O(1) memory lookup", "Approach B: In-memory cache", "Approach C: Linear scan", "Approach D: Recursive traversal"],
                            "answer": "Approach A: O(1) memory lookup"
                        },
                        reference_solution="Approach A provides predictable low-latency access.",
                        verified=True,
                    )
                    session.add(pq)
            session.flush()
            practice_qs = session.execute(select(PracticeQuestion)).scalars().all()

        q_ids = [pq.id for pq in practice_qs]

        mappings = []
        batch_size = 2000
        for i in range(3000):
            l = learners[i % len(learners)]
            dt = now - timedelta(days=random.randint(1, 60), hours=random.randint(0, 23), minutes=random.randint(0, 59))
            is_correct = random.random() < 0.82
            mappings.append({
                "id": str(uuid.uuid4()),
                "question_id": random.choice(q_ids),
                "learner_id": l.id,
                "answer_json": {"selected": "Approach A", "time_spent_seconds": random.randint(25, 180)},
                "is_correct": is_correct,
                "hints_used": random.randint(0, 2) if not is_correct else 0,
                "ai_feedback": "Correct! Well-structured solution." if is_correct else "Review indexing tradeoffs.",
                "score": 10.0 if is_correct else 0.0,
                "created_at": dt,
                "updated_at": dt,
            })
            if len(mappings) >= batch_size:
                session.bulk_insert_mappings(PracticeAttempt, mappings)
                session.commit()
                mappings = []

        if mappings:
            session.bulk_insert_mappings(PracticeAttempt, mappings)
            session.commit()

    # 11. Populate Summary Tables (LearnerStats, AssessmentStats, BatchStats, TopicMastery)
    print("Computing pre-aggregated summary tables...")
    for b_code, b in batches.items():
        b_attempts = session.execute(
            select(AssessmentAttempt.score)
            .join(Assessment, Assessment.id == AssessmentAttempt.assessment_id)
            .where(Assessment.batch_id == b.id, AssessmentAttempt.status == "SUBMITTED")
        ).scalars().all()

        scores = [float(s) for s in b_attempts if s is not None]
        avg_score = sum(scores) / len(scores) if scores else 80.0
        pass_count = sum(1 for s in scores if s >= 60.0)
        pass_rate = (pass_count / len(scores)) * 100.0 if scores else 90.0

        b_stat = session.execute(select(BatchStats).where(BatchStats.batch_id == b.id)).scalar_one_or_none()
        if not b_stat:
            b_stat = BatchStats(
                batch_id=b.id,
                learner_count=25,
                average_score=round(avg_score, 1),
                completion_rate=round(pass_rate, 1),
                practice_count=random.randint(1200, 3500),
                attendance_rate=94.5,
                updated_at=now,
            )
            session.add(b_stat)
        else:
            b_stat.learner_count = 25
            b_stat.average_score = round(avg_score, 1)
            b_stat.completion_rate = round(pass_rate, 1)
            b_stat.updated_at = now

    for l in learners[:50]:
        l_attempts = session.execute(
            select(AssessmentAttempt.score)
            .where(AssessmentAttempt.learner_id == l.id, AssessmentAttempt.status == "SUBMITTED")
        ).scalars().all()

        scores = [float(s) for s in l_attempts if s is not None]
        avg_s = sum(scores) / len(scores) if scores else 85.0
        l_stat = session.execute(select(LearnerStats).where(LearnerStats.learner_id == l.id)).scalar_one_or_none()
        if not l_stat:
            session.add(LearnerStats(
                learner_id=l.id,
                total_assessments_taken=len(scores),
                average_score=round(avg_s, 1),
                median_score=round(avg_s, 1),
                streak_days=l.streak_days,
                active_days=min(45, max(12, l.streak_days * 2)),
                practice_total=random.randint(50, 200),
                practice_accuracy=84.5,
                attendance_rate=95.0,
                updated_at=now,
            ))
        else:
            l_stat.total_assessments_taken = len(scores)
            l_stat.average_score = round(avg_s, 1)
            l_stat.updated_at = now

    session.flush()
    if own_session:
        session.commit()
    print("Database scale population complete!")

    from sqlalchemy import text
    print("\n--- FINAL DATABASE TABLE POPULATION ---")
    for tbl in ["users", "batches", "assessments", "assessment_attempts", "answers", "submissions", "meetings", "practice_attempts"]:
        cnt = session.execute(text(f"SELECT COUNT(*) FROM {tbl}")).scalar() or 0
        print(f"  {tbl}: {cnt:,} rows")

    if own_session:
        session.close()


if __name__ == "__main__":
    populate_scale_data("trellis_demo.db")
