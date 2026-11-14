# TRELLIS Author Resolution & Separation of Duties Specification

## 1. Architectural Invariant
To enforce strict Separation of Duties (SoD), creators/authors are forbidden from self-approving or publishing their own work (`author != subject`).
Furthermore, if an author **cannot be determined from the database** for an `approve` or `publish` operation (e.g., non-existent entity or unmodeled resource type), the policy engine **strictly DENIES** access (`return False` $\to$ 403 Forbidden).

---

## 2. Phase 1 Resource Author Resolution Matrix

| Resource Type | DB Model | Author Resolution Field | Target Org Resolution | Status in Phase 1 |
|---|---|---|---|---|
| `users` | `User` | `User.id` (self) | `User.org_id` | **Active & Resolved** |
| `evidence_records` | `EvidenceRecord` | `EvidenceRecord.user_id` | `EvidenceRecord.org_id` | **Active & Resolved** |
| `pathways` | `Pathway` | `Pathway.author_id` | `Pathway.org_id` | **Active & Resolved** (Slice 1.6) |
| `enrolments` | `Enrolment` | `Enrolment.user_id` | `Enrolment.org_id` | **Active & Resolved** (Slice 1.6) |
| `consents` | `Consent` | `Consent.user_id` | `Consent.org_id` | **Active & Resolved** |
| `grants` | `Grant` | `Grant.granted_by_id` or `user_id` | `Grant.org_id` | **Active & Resolved** |
| `employment_records` | `EmploymentRecord` | `EmploymentRecord.user_id` | `EmploymentRecord.org_id` | **Active & Resolved** |
| `refresh_tokens` | `RefreshToken` | `RefreshToken.user_id` | `RefreshToken.org_id` | **Active & Resolved** |
| `skills` / `skill_levels` / `skill_edges` / `role_requirements` | `Skill` | System-wide taxonomy (`None`) | `Skill.org_id` | **Active & Resolved** |
| `organisations` | `Organisation` | Tenant entity (`None`) | `Organisation.id` | **Active & Resolved** |
| `audit_log` | `AuditLog` | Append-only immutable (`None`) | `AuditLog.org_id` | **Active & Resolved** (Immutable) |
| `access_receipts` | `AccessReceipt` | Append-only immutable (`None`) | `AccessReceipt.org_id` | **Active & Resolved** (Immutable) |
| `evidence_ledger` | `EvidenceLedger` | Hash chain immutable (`None`) | `EvidenceLedger.org_id` | **Active & Resolved** (Immutable) |
| `ledger_checkpoints` | `LedgerCheckpoint` | Signed root immutable (`None`) | `LedgerCheckpoint.org_id` | **Active & Resolved** (Immutable) |

---

## 3. Resource Types Lacking Author Resolution in Phase 1
The following resources are specified in `docs/security/PERMISSION_MATRIX.json` for later phases and have no ORM models in Slices 1.1–1.6:

| Resource Type | Target Phase / Slice | Reason Lacking Author Resolution | Policy Engine Behavior |
|---|---|---|---|
| `assessments` | Phase 2 | Assessment engine scheduled for Phase 2 | **`publish` stays DENIED** (author unresolved) |
| `items` | Phase 2 | Question bank scheduled for Phase 2 | Unresolved author |
| `attempts` | Phase 2 | Assessment attempts scheduled for Phase 2 | Unresolved author |
| `responses` | Phase 2 | Candidate submissions scheduled for Phase 2 | Blind grading scope gate |
| `growth_ring` | Phase 2 | Hexagonal radar aggregation scheduled for Phase 2 | Read-only aggregate gate |
| `greenhouse_ideas`| Phase 3 | Innovation Greenhouse scheduled for Phase 3 | **`approve` stays DENIED** (author unresolved) |
| `grove_spaces` | Phase 3 | Collaborative spaces scheduled for Phase 3 | Unresolved author |
| `kb_articles` | Phase 3 | Knowledge base articles scheduled for Phase 3 | **`publish` stays DENIED** (author unresolved) |
| `ai_runs` | Phase 4 | Model inference telemetry scheduled for Phase 4 | Unresolved author |
| `credentials` | Phase 4 | Verifiable credentials scheduled for Phase 4 | Unresolved author |

---

## 4. Verification Proof
- `tests/test_policy.py::test_separation_of_duties_requires_real_db_author_and_denies_unknown_author`
- `tests/test_policy.py::test_require_permission_with_real_database_row_no_hand_supplied_author`
