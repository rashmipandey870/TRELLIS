# TRELLIS Policy Engine & Role-Permission Matrix

## 1. Architectural Overview
The TRELLIS authorization engine operates on a single pure policy evaluation function:
```python
def can(subject: UserContext, action: Action, resource: Resource, context: RequestContext) -> PolicyDecision:
    """
    Evaluates fine-grained RBAC + ABAC permissions.
    Returns: PolicyDecision(allowed: bool, reason: str, requires_approval: bool, audit_required: bool, access_receipt: bool)
    """
```
As required by Section 16 and Section 21 of the Master Prompt:
- **No Route May Bypass It**: The policy engine executes in FastAPI dependency injection prior to any service or database access.
- **Repository-Level Row Filtering**: Queries automatically apply tenant (`org_id`), cohort, team, and consent boundaries at the SQL level so a missed route check cannot leak unauthorized rows.
- **Data Matrix Source**: The authoritative rules are stored as machine-readable data in [docs/security/PERMISSION_MATRIX.json](file:///C:/Users/Rashm/.gemini/antigravity/scratch/trellis/docs/security/PERMISSION_MATRIX.json). In Phase 1, automated backend pytest suites will be synthesized directly from this JSON.

---

## 2. Active Roles & Modeled Future Roles

### Active Roles (Phase 0 - 1)
1. `EMPLOYEE`: The individual learner and knowledge contributor. Full self-ownership of their own Growth Ring, learning history, consent passport, and ideas.
2. `TRAINER_MENTOR`: Coaches cohorts, grades assessments blindly, facilitates Grove spaces and Sessions, creates evidence.
3. `MANAGER`: Direct line leader. Views consented summaries of team members only (`k >= 5` or explicit consent grant). Never sees individual psychometric raw data or unconsented assessments.
4. `LK_ADMIN`: Learning & Knowledge administrator. Manages question banks, taxonomy seed files, pathways, and anonymized org-wide learning analytics.
5. `SUPER_ADMIN`: System-level operator. Manages platform infrastructure, tenant configuration, and time-bounded emergency grants. Cannot override audit immutability or ledger append-only rules.

### Modeled Future Roles (Phase 2 - 5)
6. `LK_HEAD_CLO`: Executive learning officer. Views high-level aggregate Learning Pulse dashboards, budget what-if simulators, and leadership briefings with small-cell suppression.
7. `DEPARTMENT_HEAD`: Departmental director. Views departmental skill gap distributions and cohort benchmarks.
8. `CONTENT_AUTHOR`: Curriculum creator. Authors learning pathways, lessons, and assessment questions. Bound by separation of duties (cannot self-approve content).
9. `ASSESSMENT_REVIEWER`: Subject-matter evaluator for blind grading and manual rubric moderation.
10. `HR_PARTNER`: Human Resources collaborator. Tracks compliance completion, onboarding induction milestones, and consented high-level psychometric summaries.
11. `GUEST_CANDIDATE`: Prospective candidate taking a pre-hire Growth Check with strictly sandboxed temporary access.
12. `AUDITOR`: Independent compliance/DPO reviewer. Reads immutable audit trails, access receipts, and cryptographic ledger checkpoints. Has zero access to personal assessment answers.

---

## 3. ABAC Contextual Attributes
Beyond coarse role strings, `can()` enforces attribute-based controls (ABAC):
- `subject.department == resource.department`
- `subject.cohort_id == resource.cohort_id`
- `subject.reporting_line.includes(resource.owner_id)` (Manager direct line)
- `resource.consent_status[subject.role] == GRANTED` (Consent Passport check)
- `resource.anonymity_cell_count >= 5` (Small-group suppression gate)
- `resource.is_blind_grading == True` -> Candidate identity redacted to `candidate_hash`

---

## 4. Separation of Duties Invariants
1. **Content Approval**: An author cannot approve or publish their own pathway, question, or article (`subject.id != resource.author_id`).
2. **Blind Grading**: Candidate identities are stripped and replaced with deterministic pseudonyms during grading. Graders cannot see employee name, employee ID, or department.
3. **Audit Log Immutability**: No role—including `SUPER_ADMIN`—possesses `update` or `delete` grants on `audit_log` or `access_receipts`.
4. **Evidence Ledger Immutability**: `evidence_ledger` possesses strictly `create` and `read` actions. Any `update` or `delete` attempt is refused and triggers a high-severity security audit event.
5. **Score Overrides**: Any manual adjustment to an assessment score requires two-person approval (or `LK_ADMIN` with logged justification) and creates an immutable audit receipt.
6. **Time-Bounded Grants**: Any role elevation (e.g. temporary admin access) requires an expiry timestamp and dual-authorization.
