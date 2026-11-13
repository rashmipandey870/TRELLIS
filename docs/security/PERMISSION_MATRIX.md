# TRELLIS Policy Engine & Role-Permission Matrix

## 1. Architectural Overview & Default-Deny Security Model
The TRELLIS authorization engine operates on a single pure policy evaluation function:
```python
def can(subject: UserContext, action: Action, resource: Resource, context: RequestContext) -> PolicyDecision:
    """
    Evaluates fine-grained RBAC + ABAC permissions.
    Returns: PolicyDecision(allowed: bool, reason: str, requires_approval: bool, audit_required: bool, access_receipt: bool)
    """
```
- **Strict Default-Deny**: Any `(resource, action, role)` tuple not explicitly permitted in [PERMISSION_MATRIX.json](PERMISSION_MATRIX.json) is unconditionally **DENIED** (`allowed: false`, `reason: "Default-deny policy enforced"`).
- **Repository-Level Row Filtering**: Queries automatically apply tenant (`org_id`), cohort, team, and consent boundaries at the SQL level via SQLAlchemy query hooks.
- **Coverage Validation**: The test script `coverage_report.py` verifies 100% evaluation of the $20 \times 15 \times 12 = 3,600$ Cartesian tuples across all monitored resources, actions, and roles.

---

## 2. Monitored Resources (20 Resources)

1. `users`: Employee accounts, profile settings, accessibility preferences.
2. `roles_grants`: Role assignments, time-bounded grants, dual-custody elevations.
3. `consents`: DPDP purpose-bound consent passport records.
4. `skills`: Skills taxonomy nodes, levels, and prerequisite graph edges.
5. `pathways`: Role learning curves, onboarding pathways, courses, and modules.
6. `enrolments`: Learner pathway and course progression records.
7. `assessments`: Growth Check assessment definitions, question banks, and rubrics.
8. `items`: Question items, test cases, and difficulty parameters.
9. `attempts`: Candidate test sessions and active attempts.
10. `responses`: Candidate answers, rubric scores, and reviewer feedback.
11. `growth_ring`: Materialized developmental profiles and radar visualizations.
12. `evidence_ledger`: Append-only, hash-chained skill evidence records.
13. `sessions`: Virtual classes, calendar batches, and attendance records.
14. `greenhouse_ideas`: Innovation pipeline proposals, diff grafts, and reviews.
15. `grove_spaces`: Cohort discussion spaces, doubt threads, and mentoring slots.
16. `kb_articles`: Approved wiki articles, project learnings, and expert captures.
17. `ai_runs`: Gardener AI coach prompt runs, inferences, and audit telemetry.
18. `audit_log`: Immutable SOC 2 security event trail.
19. `access_receipts`: Cross-user personal data access records.
20. `credentials`: W3C Verifiable Credentials, Open Badges 3.0, and certificates.

---

## 3. Functional Actions (15 Actions)
`create, read, update, delete, approve, export, impersonate, override, publish, grade, review, assign, enrol, download, share`

---

## 4. Roles Monitored (12 Roles: 5 Active, 7 Modeled Future)
- **Active Roles (Phase 0–1)**: `EMPLOYEE`, `TRAINER_MENTOR`, `MANAGER`, `LK_ADMIN`, `SUPER_ADMIN`.
- **Modeled Future Roles (Phase 2–5)**: `LK_HEAD_CLO`, `DEPARTMENT_HEAD`, `CONTENT_AUTHOR`, `ASSESSMENT_REVIEWER`, `HR_PARTNER`, `GUEST_CANDIDATE`, `AUDITOR`.

---

## 5. Separation of Duties Invariants
1. **Content Approval**: An author cannot approve or publish their own pathway, question, or article (`subject.id != resource.author_id`).
2. **Blind Grading**: Candidate identities are stripped and replaced with deterministic pseudonyms during grading. Graders cannot see employee name, employee ID, or department.
3. **Audit Log Immutability**: No role—including `SUPER_ADMIN`—possesses `update` or `delete` grants on `audit_log` or `access_receipts`.
4. **Evidence Ledger Immutability**: `evidence_ledger` possesses strictly `create` and `read` actions. Any `update` or `delete` attempt is refused and triggers a high-severity security audit event.
5. **Score Overrides**: Any manual adjustment to an assessment score requires two-person approval (or `LK_ADMIN` with logged justification) and creates an immutable audit receipt.
6. **Time-Bounded Grants**: Any role elevation (e.g. temporary admin access) requires an expiry timestamp and dual-authorization.
