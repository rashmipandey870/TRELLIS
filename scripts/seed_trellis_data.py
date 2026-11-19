"""TRELLIS Master Seed Data Script (Step 8).

Seeds required system entities:
- 1 Admin: admin@csmtech.internal
- 2 Mentors: mentor1@csmtech.internal, mentor2@csmtech.internal
- 6 Learners: learner1@csmtech.internal through learner6@csmtech.internal
- 2 Batches: BATCH_ALPHA, BATCH_BETA with assignments
- Sample meetings with validated meeting links
- Sample MCQ Assessment published with questions and options
- 5 LeetCode-style Coding Problems with sample and hidden test cases
"""

from __future__ import annotations

import os
import sys

# Ensure backend is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from datetime import UTC, datetime, timedelta

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.api.deps import get_sync_engine
from app.core.security import hash_password
from app.models import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentQuestion,
    Base,
    Batch,
    CodingProblem,
    McqOption,
    Meeting,
    MeetingAttendance,
    MeetingAudience,
    MentorLearnerAssignment,
    MentorRemark,
    Notification,
    Organisation,
    PracticeScore,
    QuestionBank,
    Role,
    SystemSetting,
    TestCase,
    User,
)


def seed_trellis(session: Session) -> dict[str, int]:
    """Execute complete deterministic seed of TRELLIS platform."""
    # 1. Organization
    org = session.execute(select(Organisation).where(Organisation.code == "CSM_MAIN")).scalar_one_or_none()
    if not org:
        org = Organisation(name="CSM Technology", code="CSM_MAIN")
        session.add(org)
        session.flush()

    pwd_hash = hash_password("CSMTrellis2026!")

    # 2. Users
    # 2a. 1 Admin
    admin = session.execute(select(User).where(User.email == "admin@csmtech.internal")).scalar_one_or_none()
    if not admin:
        admin = User(
            org_id=org.id,
            email="admin@csmtech.internal",
            password_hash=pwd_hash,
            full_name="Rajesh Mohanty (L&K Admin)",
            role="ADMIN",
            is_active=True,
        )
        session.add(admin)
        session.flush()

    # 2b. 2 Mentors
    mentors = []
    mentor_specs = [
        ("mentor1@csmtech.internal", "Ananya Rao (Lead Cloud Architect)"),
        ("mentor2@csmtech.internal", "Vikram Patel (Principal Systems Engineer)"),
    ]
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
            )
            session.add(m)
            session.flush()
        mentors.append(m)

    # 2c. 6 Learners
    learners = []
    learner_specs = [
        ("learner1@csmtech.internal", "Priya Sharma", 14),
        ("learner2@csmtech.internal", "Arjun Nair", 8),
        ("learner3@csmtech.internal", "Sneha Mukherjee", 19),
        ("learner4@csmtech.internal", "Rohan Verma", 5),
        ("learner5@csmtech.internal", "Deepika Iyer", 12),
        ("learner6@csmtech.internal", "Kavita Reddy", 3),
    ]
    for email, name, streak in learner_specs:
        l = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if not l:
            l = User(
                org_id=org.id,
                email=email,
                password_hash=pwd_hash,
                full_name=name,
                role="LEARNER",
                streak_days=streak,
                streak_freezes_remaining=2,
                is_active=True,
            )
            session.add(l)
            session.flush()
        learners.append(l)

    # 3. Batches
    batch_a = session.execute(select(Batch).where(Batch.code == "BATCH_ALPHA")).scalar_one_or_none()
    if not batch_a:
        batch_a = Batch(
            name="Batch Alpha (Cloud Platform Engineering)",
            code="BATCH_ALPHA",
            field="Cloud & DevOps",
            description="Core onboarding cohort for distributed systems and cloud operations.",
            max_learners=30,
        )
        session.add(batch_a)
        session.flush()

    batch_b = session.execute(select(Batch).where(Batch.code == "BATCH_BETA")).scalar_one_or_none()
    if not batch_b:
        batch_b = Batch(
            name="Batch Beta (Full-Stack & Data Systems)",
            code="BATCH_BETA",
            field="Web & Data",
            description="Foundations in modern web architectures and relational data engineering.",
            max_learners=30,
        )
        session.add(batch_b)
        session.flush()

    # 4. Mentor-Learner Assignments
    # Mentor 1 -> Learners 0, 1, 2 (Batch Alpha)
    for l in learners[:3]:
        existing = session.execute(
            select(MentorLearnerAssignment).where(
                MentorLearnerAssignment.mentor_id == mentors[0].id,
                MentorLearnerAssignment.learner_id == l.id,
            )
        ).scalar_one_or_none()
        if not existing:
            session.add(MentorLearnerAssignment(mentor_id=mentors[0].id, learner_id=l.id, batch_id=batch_a.id))

    # Mentor 2 -> Learners 3, 4, 5 (Batch Beta)
    for l in learners[3:]:
        existing = session.execute(
            select(MentorLearnerAssignment).where(
                MentorLearnerAssignment.mentor_id == mentors[1].id,
                MentorLearnerAssignment.learner_id == l.id,
            )
        ).scalar_one_or_none()
        if not existing:
            session.add(MentorLearnerAssignment(mentor_id=mentors[1].id, learner_id=l.id, batch_id=batch_b.id))

    # 5. Sample Meetings
    today_str = datetime.now(UTC).strftime("%Y-%m-%d")
    tomorrow_str = (datetime.now(UTC) + timedelta(days=1)).strftime("%Y-%m-%d")

    m1 = session.execute(select(Meeting).where(Meeting.title == "Distributed Architecture Workshop")).scalar_one_or_none()
    if not m1:
        m1 = Meeting(
            title="Distributed Architecture Workshop",
            description="Deep dive into CAP theorem, event-driven microservices, and message brokers.",
            meeting_date=tomorrow_str,
            start_time="11:00",
            end_time="12:30",
            duration_minutes=90,
            meeting_link="https://teams.microsoft.com/l/meetup-join/csm-cloud-workshop",
            mentor_id=mentors[0].id,
            batch_id=batch_a.id,
            status="SCHEDULED",
        )
        session.add(m1)
        session.flush()
        for l in learners[:3]:
            session.add(MeetingAudience(meeting_id=m1.id, learner_id=l.id, batch_id=batch_a.id))

    # 6. Sample MCQ Assessment with Question Bank
    assessment = session.execute(select(Assessment).where(Assessment.title == "Python & Cloud Core Assessment")).scalar_one_or_none()
    if not assessment:
        assessment = Assessment(
            mentor_id=mentors[0].id,
            batch_id=batch_a.id,
            title="Python & Cloud Core Assessment",
            field="Python",
            instructions="Timed technical assessment consisting of multiple-choice and conceptual questions.",
            duration_minutes=45,
            passing_score=60.0,
            status="PUBLISHED",
            version=1,
        )
        session.add(assessment)
        session.flush()

        # Add 3 MCQ questions to Question Bank and Assessment
        mcq_data = [
            (
                "Python Memory Management",
                "How does Python primarily perform automated garbage collection?",
                "Reference counting with a generational cyclic garbage collector",
                [
                    "Mark and sweep algorithm only",
                    "Reference counting with a generational cyclic garbage collector",
                    "Manual malloc and free pointers",
                    "JVM generational compaction",
                ],
                "Python uses reference counting as its core GC mechanism, augmented by a generational collector for cyclic references.",
            ),
            (
                "Idempotency in REST APIs",
                "Which HTTP method is defined as idempotent per RFC 9110?",
                "PUT",
                ["POST", "PATCH", "PUT", "CONNECT"],
                "PUT is idempotent: multiple identical requests produce the same side-effect on server state.",
            ),
            (
                "AsyncIO Event Loop Mechanics",
                "What keyword transfers execution control back to the Python AsyncIO event loop?",
                "await",
                ["yield from", "await", "async def", "defer"],
                "The `await` expression yields control back to the active event loop until the awaited coroutine completes.",
            ),
        ]

        for seq, (q_title, q_text, correct_ans, options, expl) in enumerate(mcq_data, start=1):
            qb = QuestionBank(
                author_id=mentors[0].id,
                title=q_title,
                question_text=q_text,
                question_type="MCQ",
                field="Python",
                topic="Core Architecture",
                difficulty="MEDIUM",
                explanation=expl,
            )
            session.add(qb)
            session.flush()

            for opt_idx, opt_text in enumerate(options, start=1):
                session.add(
                    McqOption(
                        question_id=qb.id,
                        option_text=opt_text,
                        is_correct=(opt_text == correct_ans),
                        explanation=expl if opt_text == correct_ans else None,
                        sequence_order=opt_idx,
                    )
                )

            session.add(
                AssessmentQuestion(
                    assessment_id=assessment.id,
                    bank_question_id=qb.id,
                    sequence_order=seq,
                    marks=20.0,
                )
            )

    # 7. 5 LeetCode-style Coding Problems with Test Cases
    coding_specs = [
        (
            "Two Sum Target Indices",
            "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target. Output as two space-separated integers in ascending order.\nInput: target on line 1, space-separated integers on line 2.",
            "2 <= nums.length <= 10^4",
            "EASY",
            "Python",
            [("9\n2 7 11 15", "0 1", False), ("6\n3 2 4", "1 2", False), ("6\n3 3", "0 1", True), ("100\n10 20 30 40 60", "3 4", True)],
            "import sys\n\ndef solve():\n    lines = sys.stdin.read().strip().split('\\n')\n    if len(lines) < 2: return\n    target = int(lines[0].strip())\n    nums = list(map(int, lines[1].strip().split()))\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            print(f'{seen[target - n]} {i}')\n            return\n        seen[n] = i\n\nif __name__ == '__main__':\n    solve()",
        ),
        (
            "Valid Parentheses",
            "Given a string s containing '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\nOutput 'true' or 'false'.",
            "1 <= s.length <= 10^4",
            "EASY",
            "DSA",
            [("()", "true", False), ("()[]{}", "true", False), ("(]", "false", False), ("([)]", "false", True), ("{[]}", "true", True)],
            "import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    st = []\n    m = {')':'(', '}':'{', ']':'['}\n    for c in s:\n        if c in m:\n            if not st or st.pop() != m[c]:\n                print('false')\n                return\n        else:\n            st.append(c)\n    print('true' if not st else 'false')\n\nif __name__ == '__main__':\n    solve()",
        ),
        (
            "Reverse Words in a String",
            "Given an input string s, reverse the order of the words. Return words separated by a single space.",
            "1 <= s.length <= 10^4",
            "MEDIUM",
            "Python",
            [("the sky is blue", "blue is sky the", False), ("  hello world  ", "world hello", False), ("a good   example", "example good a", True)],
            "import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    print(' '.join(reversed(s.split())))\n\nif __name__ == '__main__':\n    solve()",
        ),
        (
            "Palindrome Number Checker",
            "Given an integer x, return 'true' if x is a palindrome integer, and 'false' otherwise.",
            "-2^31 <= x <= 2^31 - 1",
            "EASY",
            "Python",
            [("121", "true", False), ("-121", "false", False), ("10", "false", False), ("12321", "true", True)],
            "import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    print('true' if s == s[::-1] else 'false')\n\nif __name__ == '__main__':\n    solve()",
        ),
        (
            "Maximum Subarray Sum",
            "Given an integer array nums, find the subarray with the largest sum, and output its sum.\nInput: space-separated integers on line 1.",
            "1 <= nums.length <= 10^5",
            "MEDIUM",
            "DSA",
            [("-2 1 -3 4 -1 2 1 -5 4", "6", False), ("1", "1", False), ("5 4 -1 7 8", "23", True), ("-1 -2 -3", "-1", True)],
            "import sys\n\ndef solve():\n    nums = list(map(int, sys.stdin.read().strip().split()))\n    if not nums: return\n    max_so_far = max_ending = nums[0]\n    for x in nums[1:]:\n        max_ending = max(x, max_ending + x)\n        max_so_far = max(max_so_far, max_ending)\n    print(max_so_far)\n\nif __name__ == '__main__':\n    solve()",
        ),
    ]

    for title, desc, constr, diff, field, cases, ref in coding_specs:
        existing = session.execute(select(CodingProblem).where(CodingProblem.title == title)).scalar_one_or_none()
        if not existing:
            qb = QuestionBank(
                author_id=mentors[0].id,
                title=title,
                question_text=desc,
                question_type="CODING",
                field=field,
                topic="Algorithms",
                difficulty=diff,
            )
            session.add(qb)
            session.flush()

            prob = CodingProblem(
                bank_id=qb.id,
                title=title,
                description=desc,
                constraints=constr,
                difficulty=diff,
                field=field,
                marks=10.0,
                reference_solution=ref,
                starter_code_json={
                    "python": "import sys\n\ndef solve():\n    # Write your solution here\n    pass\n\nif __name__ == '__main__':\n    solve()",
                    "javascript": "const fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim();\n// Solution here\n",
                },
            )
            session.add(prob)
            session.flush()

            for inp, exp, hidden in cases:
                session.add(
                    TestCase(
                        problem_id=prob.id,
                        input_data=inp,
                        expected_output=exp,
                        is_hidden=hidden,
                        weight=2.0 if hidden else 1.0,
                    )
                )

    # 8. Practice Scores Seed
    for l in learners:
        session.add(
            PracticeScore(
                learner_id=l.id,
                field="Python",
                active_days=l.streak_days,
                streak_days=l.streak_days,
                problems_attempted=18,
                problems_solved=15,
                acceptance_rate=83.3,
                weighted_accuracy=85.0,
                dedication_score=78.5,
                last_practiced_at=datetime.now(UTC),
            )
        )

    # 9. Global System Setting
    session.add(
        SystemSetting(
            key="talent_spotlight_thresholds",
            value_json={
                "min_active_days": 5,
                "min_weighted_accuracy": 65.0,
                "min_problems": 5,
                "cooldown_days": 14,
            },
            updated_by_id=admin.id,
        )
    )

    session.commit()
    return {
        "admin": 1,
        "mentors": len(mentors),
        "learners": len(learners),
        "batches": 2,
        "coding_problems": len(coding_specs),
    }


if __name__ == "__main__":
    engine = get_sync_engine()
    with Session(engine) as sess:
        res = seed_trellis(sess)
        print("TRELLIS Database Seed Successful:", res)
