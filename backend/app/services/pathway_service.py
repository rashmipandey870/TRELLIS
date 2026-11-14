"""TRELLIS Curriculum & Pathways Domain Service (Slice 1.6).

Implements:
- Prerequisite DAG acyclicity validation (topological sort / cycle detection).
- Pathway creation, publishing with separation-of-duties enforcement, and retrieval.
- Learner enrolment tracking, progress calculation, and time-to-productivity telemetry.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import select

from app.core.uow import UnitOfWork
from app.models.curriculum import Course, Enrolment, Module, Pathway


def validate_course_prerequisites_dag(courses: list[dict[str, Any]]) -> bool:
    """Validate that course prerequisites form a Directed Acyclic Graph (DAG) without circular loops.

    Raises:
        ValueError: If a circular dependency / cycle is detected.
    """
    # Build adjacency list: course_id -> list of dependent course_ids
    # and in-degree map for Kahn's topological sort algorithm
    nodes: set[str] = set()
    graph: dict[str, list[str]] = {}
    in_degree: dict[str, int] = {}

    for c in courses:
        cid = str(c.get("id") or c.get("code"))
        nodes.add(cid)
        if cid not in graph:
            graph[cid] = []
        if cid not in in_degree:
            in_degree[cid] = 0

    for c in courses:
        cid = str(c.get("id") or c.get("code"))
        prereq_id = c.get("prerequisite_id") or c.get("prerequisite_course_id")
        if prereq_id:
            prereq_str = str(prereq_id)
            nodes.add(prereq_str)
            if prereq_str not in graph:
                graph[prereq_str] = []
            graph[prereq_str].append(cid)
            in_degree[cid] = in_degree.get(cid, 0) + 1

    # Kahn's Algorithm
    queue = [n for n in nodes if in_degree.get(n, 0) == 0]
    visited_count = 0

    while queue:
        curr = queue.pop(0)
        visited_count += 1
        for neighbor in graph.get(curr, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if visited_count != len(nodes):
        raise ValueError(
            f"Cycle detected in course prerequisites: Only {visited_count} of {len(nodes)} "
            f"courses could be resolved in topological dependency order."
        )

    return True


def calculate_enrolment_progress(total_modules: int, completed_modules: int) -> float:
    """Calculate progress percentage towards pathway completion."""
    if total_modules <= 0:
        return 0.0
    progress = (completed_modules / total_modules) * 100.0
    return round(min(100.0, max(0.0, progress)), 1)


def estimate_time_to_productivity(
    estimated_hours: float, hours_per_week: float = 10.0
) -> dict[str, Any]:
    """Calculate time-to-productivity telemetry metrics for learning load planning."""
    weeks = estimated_hours / max(1.0, hours_per_week)
    return {
        "estimated_total_hours": estimated_hours,
        "weekly_commitment_hours": hours_per_week,
        "estimated_weeks_to_completion": round(weeks, 1),
        "estimated_days_to_productivity": round(weeks * 7, 0),
    }


def create_pathway_service(
    uow: UnitOfWork,
    org_id: str,
    author_id: str,
    code: str,
    title: str,
    description: str | None = None,
    target_role_code: str | None = None,
    estimated_hours: float = 0.0,
    is_first_90_days: bool = False,
    courses_data: list[dict[str, Any]] | None = None,
    request_id: str | None = None,
) -> Pathway:
    """Create a new pathway with courses, validate prerequisite DAG, and write audit log."""
    courses_data = courses_data or []

    # 1. Validate Prerequisite DAG
    if courses_data:
        validate_course_prerequisites_dag(courses_data)

    # 2. Instantiate Pathway
    pathway = Pathway(
        org_id=org_id,
        code=code,
        title=title,
        description=description,
        author_id=author_id,
        is_published=False,
        target_role_code=target_role_code,
        estimated_hours=estimated_hours,
        is_first_90_days=is_first_90_days,
    )
    uow.session.add(pathway)
    uow.session.flush()

    # 3. Add Courses and Modules
    course_code_to_id: dict[str, str] = {}
    for c_idx, c_dict in enumerate(courses_data):
        course = Course(
            org_id=org_id,
            pathway_id=pathway.id,
            code=c_dict["code"],
            title=c_dict["title"],
            description=c_dict.get("description"),
            sequence_order=c_dict.get("sequence_order", c_idx + 1),
        )
        uow.session.add(course)
        uow.session.flush()
        course_code_to_id[course.code] = course.id

        # Modules
        for m_idx, m_dict in enumerate(c_dict.get("modules", [])):
            mod = Module(
                org_id=org_id,
                course_id=course.id,
                title=m_dict["title"],
                module_type=m_dict.get("module_type", "LESSON"),
                sequence_order=m_dict.get("sequence_order", m_idx + 1),
                estimated_minutes=m_dict.get("estimated_minutes", 30),
                content_json=m_dict.get("content_json"),
            )
            uow.session.add(mod)

    # Resolve prerequisite IDs if referencing codes
    for c_dict in courses_data:
        prereq_code = c_dict.get("prerequisite_code")
        if prereq_code and prereq_code in course_code_to_id:
            cid = course_code_to_id[c_dict["code"]]
            c_obj = uow.session.get(Course, cid)
            if c_obj:
                c_obj.prerequisite_course_id = course_code_to_id[prereq_code]

    # 4. In-transaction transactional audit log via Unit of Work
    uow.record_audit(
        action="create",
        resource="pathways",
        resource_id=pathway.id,
        reason="Created learning pathway specification",
        after_state={"code": code, "title": title, "courses_count": len(courses_data)},
        org_id=org_id,
    )
    uow.commit()
    return pathway


def publish_pathway_service(
    uow: UnitOfWork,
    pathway_id: str,
    publisher_id: str,
    org_id: str,
    request_id: str | None = None,
) -> Pathway:
    """Publish a draft pathway, enforcing separation of duties (author cannot publish own pathway)."""
    pathway = uow.session.get(Pathway, pathway_id)
    if not pathway or pathway.org_id != org_id:
        raise ValueError("Pathway not found.")

    # Separation of duties invariant
    if pathway.author_id == publisher_id:
        raise PermissionError(
            "SEPARATION_OF_DUTIES_VIOLATION: Pathway author cannot self-publish their own pathway. "
            "Independent trainer or administrator review is required."
        )

    before_state = {"is_published": pathway.is_published}
    pathway.is_published = True

    uow.record_audit(
        action="publish",
        resource="pathways",
        resource_id=pathway.id,
        reason="Published learning pathway following peer review",
        before_state=before_state,
        after_state={"is_published": True},
        org_id=org_id,
    )
    uow.commit()
    return pathway


def enrol_user_in_pathway_service(
    uow: UnitOfWork,
    pathway_id: str,
    user_id: str,
    org_id: str,
    cohort_id: str | None = None,
    batch_id: str | None = None,
    request_id: str | None = None,
) -> Enrolment:
    """Enrol an employee in a pathway and record in-transaction audit log."""
    pathway = uow.session.get(Pathway, pathway_id)
    if not pathway or pathway.org_id != org_id:
        raise ValueError("Pathway not found.")

    if not pathway.is_published:
        raise PermissionError("Cannot enrol in an unpublished draft pathway.")

    # Check for existing enrolment
    existing = (
        uow.session.execute(
            select(Enrolment).where(
                Enrolment.user_id == user_id,
                Enrolment.pathway_id == pathway_id,
            )
        )
        .scalars()
        .first()
    )

    if existing:
        return existing

    enrolment = Enrolment(
        org_id=org_id,
        user_id=user_id,
        pathway_id=pathway_id,
        cohort_id=cohort_id,
        batch_id=batch_id,
        status="ENROLLED",
        progress_percent=0.0,
    )
    uow.session.add(enrolment)
    uow.session.flush()

    uow.record_audit(
        action="enrol",
        resource="enrolments",
        resource_id=enrolment.id,
        reason="Enrolled in learning pathway",
        after_state={"pathway_id": pathway_id, "status": "ENROLLED"},
        org_id=org_id,
    )
    uow.commit()
    return enrolment
