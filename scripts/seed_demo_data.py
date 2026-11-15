"""TRELLIS Demo Synthetic Seed Data Script (Slice 1.7b).

SECURITY & ENVIRONMENT INVARIANT:
Refuses execution unless os.environ.get("TRELLIS_ENV") == "demo".
Produces strictly synthetic persona and curriculum data:
- "Demo Learner 01" (demo.learner01@csmtech.internal)
- "Demo Trainer 01" (demo.trainer01@csmtech.internal)
- "Demo Admin 01" (demo.admin01@csmtech.internal)
- Cohort Nova 2026
- First 90 Days: Platform Engineering Pathway (6 modules across 3 courses)
- 4 Role Benchmarks with Cryptographic Evidence Ledger proofs
  (STRONG_EVIDENCE, DEVELOPING_EVIDENCE, LIMITED_EVIDENCE, NOT_ENOUGH_DATA)
"""

from __future__ import annotations

import os
import sys
from typing import Any

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.core.config import settings
from app.core.security import hash_password
from app.models import (
    EmploymentRecord,
    Grant,
    Organisation,
    Role,
    RoleRequirement,
    Skill,
    User,
)
from app.models.base import Base
from app.models.curriculum import Cohort, Course, Enrolment, Module, Pathway
from app.services.ledger_service import append_evidence


def verify_demo_environment() -> None:
    """Refuse to run when TRELLIS_ENV is not demo."""
    env = os.environ.get("TRELLIS_ENV", "")
    if env != "demo":
        raise RuntimeError(
            f"REFUSING_SEED: Demo seed script refused execution in environment '{env}'. "
            "TRELLIS_ENV must be set strictly to 'demo'."
        )


def seed_demo_data(session: Session) -> dict[str, Any]:
    """Populate synthetic demo records into the target database session."""
    verify_demo_environment()

    # 1. Organisation
    org = session.execute(
        select(Organisation).where(Organisation.code == "CSM_DEMO")
    ).scalar_one_or_none()
    if org is None:
        org = Organisation(name="CSM Technology (Demo)", code="CSM_DEMO")
        session.add(org)
        session.flush()

    # 2. System Roles
    roles = {
        "LEARNER": "Learner",
        "TRAINER": "Trainer",
        "CONTENT_AUTHOR": "Content Author",
        "CONTENT_REVIEWER": "Content Reviewer",
        "PEOPLE_MANAGER": "People Manager",
        "LK_ADMIN": "L&K Platform Administrator",
        "SUPER_ADMIN": "Super Administrator",
    }
    role_entities: dict[str, Role] = {}
    for code, name in roles.items():
        role = session.execute(select(Role).where(Role.code == code)).scalar_one_or_none()
        if role is None:
            role = Role(code=code, name=name, is_system_role=True)
            session.add(role)
            session.flush()
        role_entities[code] = role

    # 3. Synthetic Users
    # 3a. Demo Learner 01
    learner = session.execute(
        select(User).where(User.email == "demo.learner01@csmtech.internal")
    ).scalar_one_or_none()
    if learner is None:
        learner = User(
            org_id=org.id,
            email="demo.learner01@csmtech.internal",
            password_hash=hash_password("DemoPassword123!"),
            full_name="Demo Learner 01",
            pseudonym_salt="demo-learner-salt-01",
            streak_days=14,
            streak_freezes_remaining=2,
            is_active=True,
        )
        session.add(learner)
        session.flush()

        emp_learner = EmploymentRecord(
            user_id=learner.id,
            org_id=org.id,
            employee_code="CSM-EMP-1001",
            department="Platform Engineering",
            designation="Associate Platform Engineer",
        )
        session.add(emp_learner)

        grant_learner = Grant(
            user_id=learner.id,
            role_id=role_entities["LEARNER"].id,
            org_id=org.id,
        )
        session.add(grant_learner)

    # 3b. Demo Trainer 01
    trainer = session.execute(
        select(User).where(User.email == "demo.trainer01@csmtech.internal")
    ).scalar_one_or_none()
    if trainer is None:
        trainer = User(
            org_id=org.id,
            email="demo.trainer01@csmtech.internal",
            password_hash=hash_password("DemoPassword123!"),
            full_name="Demo Trainer 01",
            pseudonym_salt="demo-trainer-salt-01",
            is_active=True,
        )
        session.add(trainer)
        session.flush()

        emp_trainer = EmploymentRecord(
            user_id=trainer.id,
            org_id=org.id,
            employee_code="CSM-EMP-2001",
            department="Platform Engineering",
            designation="Principal Architect & Trainer",
        )
        session.add(emp_trainer)

        grant_trainer = Grant(
            user_id=trainer.id,
            role_id=role_entities["TRAINER"].id,
            org_id=org.id,
        )
        session.add(grant_trainer)

    # 3c. Demo Admin 01
    admin = session.execute(
        select(User).where(User.email == "demo.admin01@csmtech.internal")
    ).scalar_one_or_none()
    if admin is None:
        admin = User(
            org_id=org.id,
            email="demo.admin01@csmtech.internal",
            password_hash=hash_password("DemoPassword123!"),
            full_name="Demo Admin 01",
            pseudonym_salt="demo-admin-salt-01",
            is_active=True,
        )
        session.add(admin)
        session.flush()

        emp_admin = EmploymentRecord(
            user_id=admin.id,
            org_id=org.id,
            employee_code="CSM-EMP-3001",
            department="Learning & Knowledge",
            designation="L&K Platform Administrator",
        )
        session.add(emp_admin)

        grant_admin = Grant(
            user_id=admin.id,
            role_id=role_entities["LK_ADMIN"].id,
            org_id=org.id,
        )
        session.add(grant_admin)

    # 4. Skills Taxonomy
    skills_def = [
        ("SKILL-CONSENSUS", "Distributed Consensus (Raft/Paxos)", "Distributed Systems"),
        ("SKILL-K8S", "Kubernetes Operator Architecture", "Cloud Infrastructure"),
        ("SKILL-MTLS", "Zero-Trust mTLS & Service Mesh", "Security & Networking"),
        ("SKILL-KAFKA", "Event Streaming with Apache Kafka", "Data Engineering"),
        ("SKILL-CHAOS", "Chaos Engineering & Fault Injection", "Observability & SRE"),
    ]
    skill_entities: dict[str, Skill] = {}
    for code, name, category in skills_def:
        skill = session.execute(
            select(Skill).where(Skill.org_id == org.id, Skill.code == code)
        ).scalar_one_or_none()
        if skill is None:
            skill = Skill(org_id=org.id, code=code, name=name, category=category)
            session.add(skill)
            session.flush()
        skill_entities[code] = skill

    # 5. Role Requirements for PLATFORM_ENG_L2
    role_benchmarks = [
        ("SKILL-CONSENSUS", 4),
        ("SKILL-K8S", 3),
        ("SKILL-MTLS", 3),
        ("SKILL-KAFKA", 3),
        ("SKILL-CHAOS", 2),
    ]
    for skill_code, target_lvl in role_benchmarks:
        sk = skill_entities[skill_code]
        req = session.execute(
            select(RoleRequirement).where(
                RoleRequirement.org_id == org.id,
                RoleRequirement.role_code == "PLATFORM_ENG_L2",
                RoleRequirement.skill_id == sk.id,
            )
        ).scalar_one_or_none()
        if req is None:
            req = RoleRequirement(
                org_id=org.id,
                role_code="PLATFORM_ENG_L2",
                skill_id=sk.id,
                target_level=target_lvl,
            )
            session.add(req)

    # 6. First 90 Days Pathway Hierarchy
    pw = session.execute(
        select(Pathway).where(Pathway.org_id == org.id, Pathway.code == "PW-PLATFORM-90D")
    ).scalar_one_or_none()
    if pw is None:
        pw = Pathway(
            org_id=org.id,
            code="PW-PLATFORM-90D",
            title="First 90 Days: Platform Engineering",
            description="Accelerate your onboarding into CSM Technology's distributed platform infrastructure.",
            author_id=admin.id,
            is_published=True,
            is_first_90_days=True,
            target_role_code="PLATFORM_ENG_L2",
            estimated_hours=60.0,
        )
        session.add(pw)
        session.flush()

        # Courses & Modules
        courses_def = [
            (
                "CRS-ENG-101",
                "Platform Foundations & GitOps",
                1,
                [
                    ("MOD-101", "Repository Architecture & Trunk-Based Development", 30),
                    ("MOD-102", "CI/CD Pipeline Security & Container Attestations", 45),
                ],
            ),
            (
                "CRS-ENG-201",
                "Cloud-Native Infrastructure & Kubernetes",
                2,
                [
                    ("MOD-201", "Kubernetes Custom Resource Definitions (CRDs)", 60),
                    ("MOD-202", "Service Mesh mTLS and Traffic Shaping", 50),
                ],
            ),
            (
                "CRS-ENG-301",
                "Resilient Distributed Systems & SRE",
                3,
                [
                    ("MOD-301", "Raft Consensus Cluster Implementation", 90),
                    ("MOD-302", "Chaos Mesh & Automated Disaster Recovery Drills", 75),
                ],
            ),
        ]

        for crs_code, crs_title, seq, mods in courses_def:
            crs = Course(
                org_id=org.id,
                pathway_id=pw.id,
                code=crs_code,
                title=crs_title,
                sequence_order=seq,
            )
            session.add(crs)
            session.flush()

            for m_idx, (m_code, m_title, m_mins) in enumerate(mods, start=1):
                mod = Module(
                    org_id=org.id,
                    course_id=crs.id,
                    title=m_title,
                    sequence_order=m_idx,
                    estimated_minutes=m_mins,
                )
                session.add(mod)

    # 7. Cohort Nova 2026
    cohort = session.execute(
        select(Cohort).where(Cohort.org_id == org.id, Cohort.code == "COHORT-NOVA-2026")
    ).scalar_one_or_none()
    if cohort is None:
        cohort = Cohort(
            org_id=org.id,
            pathway_id=pw.id,
            name="Cohort Nova 2026",
            code="COHORT-NOVA-2026",
            trainer_id=trainer.id,
        )
        session.add(cohort)
        session.flush()

    # 8. Active Enrolment for Demo Learner 01
    enrolment = session.execute(
        select(Enrolment).where(
            Enrolment.user_id == learner.id,
            Enrolment.pathway_id == pw.id,
        )
    ).scalar_one_or_none()
    if enrolment is None:
        enrolment = Enrolment(
            org_id=org.id,
            user_id=learner.id,
            pathway_id=pw.id,
            cohort_id=cohort.id,
            status="IN_PROGRESS",
            progress_percent=33.3,  # 2 of 6 modules completed
        )
        session.add(enrolment)
        session.flush()

    # 9. Cryptographic Evidence Ledger Entries for Demo Learner 01
    # 6 proofs for SKILL-CONSENSUS -> STRONG_EVIDENCE
    # 3 proofs for SKILL-K8S -> DEVELOPING_EVIDENCE
    # 1 proof for SKILL-MTLS -> LIMITED_EVIDENCE
    # 0 for SKILL-KAFKA and SKILL-CHAOS -> NOT_ENOUGH_DATA
    ledger_plans = [
        ("SKILL-CONSENSUS", 6, "LAB_ASSESSMENT", "Distributed Consensus Raft Implementation Lab"),
        ("SKILL-K8S", 3, "CODE_REVIEW", "Production CRD Controller Architecture Assessment"),
        ("SKILL-MTLS", 1, "QUIZ", "Zero-Trust mTLS Encryption Protocol Examination"),
    ]
    for skill_code, count, ev_type, title in ledger_plans:
        sk = skill_entities[skill_code]
        for i in range(count):
            payload = {
                "assessment_title": f"{title} #{i + 1}",
                "score_percent": 90 + i,
                "verified_by": "Automated Test Harness & Trainer Review",
                "timestamp_utc": "2026-11-14T10:00:00Z",
            }
            append_evidence(
                session=session,
                org_id=org.id,
                user_id=learner.id,
                skill_id=sk.id,
                evidence_type=ev_type,
                payload=payload,
                salt="demo-learner-salt-01",
            )

    session.commit()
    print("SUCCESS: Demo synthetic seed data created successfully.")
    return {
        "org_id": org.id,
        "learner_id": learner.id,
        "trainer_id": trainer.id,
        "admin_id": admin.id,
        "pathway_id": pw.id,
    }


def main() -> None:
    """CLI Entrypoint for demo seeding."""
    verify_demo_environment()
    db_url = settings.DATABASE_URL.replace("mysql+asyncmy://", "mysql+pymysql://")
    if "mysql" not in db_url:
        db_url = "sqlite:///trellis_demo.db"

    print(f"Connecting to database: {db_url}")
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        seed_demo_data(session)


if __name__ == "__main__":
    main()
