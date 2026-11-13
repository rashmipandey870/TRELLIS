# TRELLIS Role-by-Role Permission Review (Plain-English Human Audit)

This document provides a human-readable review of all **118 explicit permission rules** defined in [PERMISSION_MATRIX.json](PERMISSION_MATRIX.json). 

**Security Model Invariant**: Any `(resource, action, role)` tuple not listed below is strictly **DENIED** under the Default-Deny rule.

---

## 1. Active Role: `EMPLOYEE`
The individual learner, test candidate, and knowledge creator.

| Resource | Action | Scope | Approval Req? | Audit Logged? | Plain-English Meaning & Conditions |
|---|---|---|---|---|---|
| `users` | `read` | `OWN` | No | No | Can view own profile, employment details, and preferences. |
| `users` | `update` | `OWN` | No | No | Can update own preferences (dyslexia font, theme, notifications). |
| `users` | `delete` | `OWN` | **Yes** | **Yes** | Can request statutory DPDP Right to Erasure (triggers crypto-shredding). |
| `roles_grants` | `read` | `OWN` | No | No | Can view current active role assignments. |
| `consents` | `read` | `OWN` | No | No | Can view all active and revoked consents in Consent Passport. |
| `consents` | `create` | `OWN` | No | **Yes** | Can grant consent for optional purposes. |
| `consents` | `update` | `OWN` | No | **Yes** | Can revoke consent in 1-click at any time. |
| `skills` | `read` | `ORGANIZATION` | No | No | Can explore the organization skills taxonomy and level descriptors. |
| `pathways` | `read` | `ORGANIZATION` | No | No | Can browse public role pathways and curriculum. |
| `enrolments` | `read` | `OWN` | No | No | Can view own course and pathway progress. |
| `enrolments` | `enrol` | `OWN` | No | **Yes** | Can self-enrol in available voluntary pathways. |
| `assessments`| `read` | `COHORT` | No | No | Can view assessments assigned to their cohort (`is_active == true`). |
| `attempts` | `create` | `OWN` | No | **Yes** | Can start an assessment attempt session. |
| `attempts` | `read` | `OWN` | No | No | Can view own completed attempt reports. |
| `attempts` | `update` | `OWN` | No | No | Can save progress during an active attempt (`in_progress == true`). |
| `growth_ring`| `read` | `OWN` | No | No | Full unrestricted view of own Growth Ring development profile. |
| `growth_ring`| `download` | `OWN` | No | **Yes** | Can download verified Growth Ring PDF report. |
| `growth_ring`| `share` | `OWN` | No | **Yes** | Can choose which sections to share with manager via Consent Passport. |
| `evidence_ledger`| `read`| `OWN` | No | No | Can view own append-only hash chain and verify block integrity. |
| `evidence_ledger`| `create`| `OWN` | **Yes** | **Yes** | Can submit self-reflection evidence (requires trainer review). |
| `sessions` | `read` | `COHORT` | No | No | Can view scheduled batch sessions and calendar join links. |
| `greenhouse_ideas`| `create`| `ORGANIZATION`| No | **Yes** | Can submit an idea or process proposal in Greenhouse. |
| `greenhouse_ideas`| `read` | `ORGANIZATION`| No | No | Can view public/team ideas matching their confidentiality clearance. |
| `grove_spaces`| `read` | `COHORT` | No | No | Can browse cohort discussions, doubts, and announcements. |
| `grove_spaces`| `create` | `COHORT` | No | No | Can open a doubt thread or question for peers/trainers. |
| `kb_articles`| `read` | `ORGANIZATION`| No | No | Can search and read approved knowledge wiki articles. |
| `ai_runs` | `create` | `OWN` | No | **Yes** | Can query the Gardener AI coach (rate limited, logged in audit). |
| `access_receipts`| `read`| `OWN` | No | No | Can see every cross-user read of their personal data (Consent Passport). |
| `credentials`| `read` | `OWN` | No | No | Can view earned badges and certificates. |
| `credentials`| `export` | `OWN` | No | **Yes** | Can export Skills Passport as a W3C Verifiable Credential. |
| `credentials`| `download`| `OWN`| No | **Yes** | Can download certificate files and badge JSON-LD. |

---

## 2. Active Role: `TRAINER_MENTOR`
Facilitates cohort learning, blind grading, mentoring, and session delivery.

| Resource | Action | Scope | Approval Req? | Audit Logged? | Plain-English Meaning & Conditions |
|---|---|---|---|---|---|
| `users` | `read` | `COHORT` | No | No | Can view learner profiles within assigned cohort batches. |
| `skills` | `read` | `ORGANIZATION` | No | No | Can view skills taxonomy. |
| `pathways` | `read` | `ORGANIZATION` | No | No | Can browse pathways. |
| `pathways` | `publish` | `ORGANIZATION` | No | **Yes** | Can publish a pathway (`author != subject`, separation of duties). |
| `enrolments` | `read` | `COHORT` | No | No | Can monitor cohort learners' progress through curriculum. |
| `assessments`| `read` | `COHORT` | No | No | Can inspect assessments assigned to their cohorts. |
| `attempts` | `read` | `COHORT` | No | No | Can inspect cohort attempts in blind grading mode. |
| `responses` | `grade` | `BLIND_GRADING`| No | **Yes** | Grades candidate submissions with candidate PII redacted. |
| `growth_ring`| `read` | `COHORT` | No | **Yes** | Views cohort members' Growth Rings (creates access receipt). |
| `evidence_ledger`| `read`| `COHORT` | No | **Yes** | Views cohort evidence history (creates access receipt). |
| `evidence_ledger`| `create`| `COHORT` | No | **Yes** | Appends trainer feedback/endorsement evidence to learner chain. |
| `sessions` | `read` | `COHORT` | No | No | Views assigned cohort calendar sessions. |
| `sessions` | `create` | `COHORT` | No | **Yes** | Schedules new training sessions or batch workshops. |
| `greenhouse_ideas`| `create`| `ORGANIZATION`| No | **Yes** | Can submit idea proposals. |
| `greenhouse_ideas`| `read` | `ORGANIZATION`| No | No | Can review community ideas. |
| `greenhouse_ideas`| `approve`| `COHORT` | No | **Yes** | Approves ideas submitted by cohort learners (`author != subject`). |
| `grove_spaces`| `read` | `COHORT` | No | No | Views cohort social spaces. |
| `grove_spaces`| `create` | `COHORT` | No | No | Posts official cohort notices or replies to doubt threads. |
| `kb_articles`| `read` | `ORGANIZATION`| No | No | Views knowledge wiki. |
| `kb_articles`| `create` | `ORGANIZATION`| No | **Yes** | Drafts knowledge articles from project post-mortems. |
| `kb_articles`| `publish` | `ORGANIZATION`| No | **Yes** | Approves and publishes knowledge articles (`author != subject`). |

---

## 3. Active Role: `MANAGER`
Line manager focused on career development, 1:1 growth conversations, and team capability.

| Resource | Action | Scope | Approval Req? | Audit Logged? | Plain-English Meaning & Conditions |
|---|---|---|---|---|---|
| `users` | `read` | `TEAM_DIRECT` | No | No | Views direct reports' basic employment profiles. |
| `skills` | `read` | `ORGANIZATION` | No | No | Views skills taxonomy to plan team growth. |
| `pathways` | `read` | `ORGANIZATION` | No | No | Browses company pathways. |
| `pathways` | `assign` | `TEAM_DIRECT` | No | **Yes** | Assigns learning pathway to team member (`load_guard_passed`). |
| `enrolments` | `read` | `TEAM_DIRECT` | No | No | Tracks team members' pathway completion progress. |
| `enrolments` | `enrol` | `TEAM_DIRECT` | No | **Yes** | Enrols direct report in a developmental pathway. |
| `growth_ring`| `read` | `TEAM_DIRECT` | No | **Yes** | Views team member's consented Growth Ring (requires consent + writes receipt). |
| `sessions` | `read` | `TEAM_DIRECT` | No | No | Views scheduled training calendar for team. |
| `greenhouse_ideas`| `approve`| `TEAM_DIRECT`| No | **Yes** | Approves team member's Greenhouse idea for build (`author != subject`). |

---

## 4. Active Role: `LK_ADMIN`
Learning & Knowledge administrator managing platforms, banks, pathways, and taxonomies.

| Resource | Action | Scope | Approval Req? | Audit Logged? | Plain-English Meaning & Conditions |
|---|---|---|---|---|---|
| `users` | `read` | `ORGANIZATION` | No | No | Directory access across organization. |
| `users` | `update` | `ORGANIZATION` | No | **Yes** | Admin updates to user attributes. |
| `users` | `delete` | `ORGANIZATION` | **Yes** | **Yes** | Deactivates or archives user accounts (requires dual-signoff). |
| `roles_grants` | `create` | `ORGANIZATION`| **Yes** | **Yes** | Grants roles to users (`target_role != SUPER_ADMIN`). |
| `roles_grants` | `read` | `ORGANIZATION`| No | **Yes** | Audits active role assignments. |
| `roles_grants` | `delete` | `ORGANIZATION`| **Yes** | **Yes** | Revokes role assignments. |
| `skills` | `read` | `ORGANIZATION` | No | No | Reads full skills taxonomy. |
| `skills` | `create` | `ORGANIZATION` | No | **Yes** | Adds new skills to taxonomy. |
| `skills` | `update` | `ORGANIZATION` | No | **Yes** | Updates skill descriptors, decay half-lives, and edges. |
| `skills` | `delete` | `ORGANIZATION` | **Yes** | **Yes** | Retires deprecated skills. |
| `pathways` | `create` | `ORGANIZATION` | No | **Yes** | Creates new pathways. |
| `pathways` | `publish` | `ORGANIZATION` | No | **Yes** | Publishes pathways (`author != subject`). |
| `pathways` | `assign` | `ORGANIZATION` | No | **Yes** | Assigns mandatory compliance pathways org-wide. |
| `enrolments` | `read` | `ORGANIZATION` | No | No | Views enterprise enrolment metrics. |
| `enrolments` | `enrol` | `ORGANIZATION` | No | **Yes** | Bulk enrols cohorts. |
| `assessments`| `read` | `ORGANIZATION` | No | No | Views all assessment configurations. |
| `assessments`| `create` | `ORGANIZATION` | No | **Yes** | Configures new Growth Check assessments. |
| `assessments`| `publish`| `ORGANIZATION` | **Yes** | **Yes** | Releases assessment to cohorts. |
| `items` | `read` | `ORGANIZATION` | No | No | Accesses question bank items and IRT parameters. |
| `items` | `create` | `ORGANIZATION` | No | **Yes** | Adds new questions to question banks. |
| `items` | `review` | `ORGANIZATION` | No | **Yes** | Reviews flagged DIF/biased questions. |
| `attempts` | `read` | `ORGANIZATION` | No | No | Accesses completed attempt records. |
| `responses` | `override` | `ORGANIZATION`| **Yes**| **Yes** | Overrides assessment score (requires mandatory justification). |
| `growth_ring`| `read` | `ANONYMIZED_AGGREGATE`| No | **Yes** | Views aggregated skill distributions (individual names masked). |
| `sessions` | `create` | `ORGANIZATION` | No | **Yes** | Creates organization-level training tracks. |
| `greenhouse_ideas`| `approve`| `ORGANIZATION`| No | **Yes** | Final approval for company-wide implementation. |
| `kb_articles`| `publish` | `ORGANIZATION`| No | **Yes** | Publishes knowledge articles (`author != subject`). |
| `ai_runs` | `read` | `ORGANIZATION` | No | **Yes** | Reviews AI model performance telemetry and audit logs. |
| `audit_log` | `read` | `ORGANIZATION` | No | **Yes** | Views system audit trail. |

---

## 5. Active Role: `SUPER_ADMIN`
Infrastructure and tenant operator. Bound by strict immutability invariants.

| Resource | Action | Scope | Approval Req? | Audit Logged? | Plain-English Meaning & Conditions |
|---|---|---|---|---|---|
| `users` | `update` | `ORGANIZATION` | No | **Yes** | Updates tenant user configurations. |
| `users` | `delete` | `ORGANIZATION` | **Yes** | **Yes** | Hard account removal under legal order. |
| `roles_grants` | `create` | `ORGANIZATION`| **Yes** | **Yes** | Time-bounded privileged role elevation (with expiry). |
| `roles_grants` | `read` | `ORGANIZATION`| No | **Yes** | Inspects privileged grants. |
| `roles_grants` | `delete` | `ORGANIZATION`| **Yes** | **Yes** | Revokes privileged grants. |
| `audit_log` | `read` | `ORGANIZATION` | No | **Yes** | Reads security event log. |
| *Immutability Invariant* | `update`/`delete` on `audit_log` | `NONE` | **FORBIDDEN** | **ALERT** | **Strictly prohibited**: Super admin CANNOT alter or delete audit rows. |
| *Immutability Invariant* | `update`/`delete` on `evidence_ledger` | `NONE` | **FORBIDDEN** | **ALERT** | **Strictly prohibited**: Super admin CANNOT alter or delete ledger rows. |

---

## 6. Modeled Future Roles (Brief Summary)
- `LK_HEAD_CLO`: `growth_ring:read` (ANONYMIZED_AGGREGATE with $n \ge 5$), `analytics_dashboard:read` (ORGANIZATION).
- `DEPARTMENT_HEAD`: `growth_ring:read` (DEPARTMENT aggregate with $n \ge 5$).
- `CONTENT_AUTHOR`: `items:create`, `pathways:create`, `kb_articles:create` (Cannot self-approve).
- `ASSESSMENT_REVIEWER`: `items:review`, `responses:grade` (BLIND_GRADING with PII stripped).
- `HR_PARTNER`: `users:read` (ORGANIZATION), `consents:read` (ANONYMIZED), `pathways:read` (ORGANIZATION).
- `GUEST_CANDIDATE`: `assessments:read` (Temporary token), `attempts:create`, `responses:create` (Ephemeral sandbox).
- `AUDITOR`: `audit_log:read`, `access_receipts:read`, `evidence_ledger:read` (Hash verification only; zero access to assessment answers or personal data).
