# PHASE 0 PLAN: Architecture Blueprint & System Foundations

**Phase Objective**: Establish complete architectural specifications, data schemas, security threat models, access control matrix, design tokens, and accessibility plans for TRELLIS before any application code is written.

---

## 1. Scope & Boundaries
- **Strict Boundary**: Design and documentation only. **Zero application code** (FastAPI routes, Angular components, or database records) will be written during Phase 0.
- **Legacy Integration Baseline**: Maps the existing CSM Employee Skills portal's three confirmed subsystems:
  1. *Skill Assessment* -> maps into **Growth Check** and question banks.
  2. *Onboarding Induction* -> maps into **Pathways** (First-90-Days Copilot).
  3. *Skill Sheet* -> maps into **Growth Ring** and the evidence-based skills graph.
- **Governance**: Implements strict requirements from Master Prompt Sections 21 (Architecture Blueprint), 22 (Signature Innovations), 23 (Builder Operating Protocol), and 24 (Definition of Done).

---

## 2. Planned Phase 0 Deliverables

| Deliverable | Target Document | Description |
|---|---|---|
| **D0.1: Information Architecture** | `docs/architecture/INFORMATION_ARCHITECTURE.md` | Comprehensive sitemap, module boundaries, routing hierarchy, command bar search space, and legacy portal concept mapping. |
| **D0.2: Role-Permission Matrix** | `docs/security/PERMISSION_MATRIX.json` & `.md` | Machine-readable permission matrix: `Resource × Action × Role × Scope × Approval × Audit` covering 5 active roles and 7 modeled future roles. |
| **D0.3: ERD & Migrations Plan** | `docs/architecture/ERD_MIGRATIONS_PLAN.md` | Complete database schema covering all 33 core entities specified in Section 21, foreign keys, indexes, hash-chaining structure for the Evidence Ledger, multi-tenancy `org_id`, and phased Alembic migration sequence. |
| **D0.4: Design Tokens & System** | `docs/design/DESIGN_TOKENS.md` | WCAG 2.2 AA tokens: placeholder palette (`#0B0D12`, `#1294C4`, `#8B3A3A`, `#FFFFFF`), typography, 8px grid, high-contrast, dark mode, dyslexia font, and growth motif components. |
| **D0.5: Accessibility Test Plan** | `docs/accessibility/ACCESSIBILITY_PLAN.md` | WCAG 2.2 AA testing protocols, automated `@axe-core/playwright` CI gates, keyboard navigation maps, and assistive technology (NVDA, JAWS, VoiceOver) verification scripts. |
| **D0.6: Clickable Wireframes & UI Flows** | `docs/design/WIREFRAMES.md` | Detailed text/ASCII layout wireframes for Home Hero ("Continue climbing"), Command Bar (Ctrl+K), Growth Ring Report (radar + table alternative), and Consent Passport. |
| **D0.7: Threat Model & Security Baseline** | `docs/security/THREAT_MODEL.md` | STRIDE analysis, India DPDP Act compliance model, blind grading separation of duties, and prompt-injection mitigations. |
| **D0.8: Architectural Decision Records** | `docs/adr/ADR-0001` through `ADR-0004` | Formal ADRs capturing context, decisions, consequences, and rejected alternatives for stack, policy engine, evidence ledger, and legacy migration. |

---

## 3. Detailed Deliverables Breakdown

### S-1: Information Architecture & Navigation
- Map the user journeys for all 5 roles: `EMPLOYEE`, `TRAINER_MENTOR`, `MANAGER`, `LK_ADMIN`, `SUPER_ADMIN`.
- Unify learning and skills into single learner record:
  - *Employee Skills Portal Legacy*:
    - Skill Assessment -> Assessment banks, attempts, item difficulty, auto/manual scoring.
    - Onboarding Induction -> Cohort assignment, milestone paths, buddy matching.
    - Skill Sheet -> Skills graph, evidence decay, employee-confirmed inference.
- Global Command Bar (`Ctrl/Cmd+K`) indexable entity registry.

### S-2: Access Control & Privacy Engine Specification
- Pure policy function specification: `can(subject, action, resource, context) -> (Decision, Reason, ApprovalReq)`.
- Enforces Separation of Duties:
  - Authors cannot approve their own content.
  - Blind grading hides candidate identity.
  - Immutable audit logs (no UPDATE or DELETE grants).
  - Score overrides require explicit approval + reason.
- Consent Passport & Access Receipt specification: Every cross-user read of personal data logs a tamper-evident receipt.

### S-3: Core Data Model & Migrations Strategy
- Complete ERD covering all 33 required tables with explicit constraints:
  - `org_id` on every table for multi-tenancy readiness.
  - `evidence_ledger`: `id`, `org_id`, `employee_id`, `skill_id`, `evidence_type`, `weight`, `decay_rate`, `recorded_at`, `payload_hash`, `prev_hash`, `signature`.
  - Field-level encryption specified for psychometric responses (`encrypted_payload`, `key_id`).
  - Read-model denormalized summary schemas with mandatory metadata: `n`, `coverage`, `computed_at`.
- Phased Alembic migration scripts outline.

### S-4: Threat Model (STRIDE) & DPDP Compliance
- **Spoofing**: Microsoft Entra ID OIDC + Argon2id fallback, signed JWT with short TTL and rotation.
- **Tampering**: Append-only hash-chained ledger; cryptographic hash verification.
- **Repudiation**: Append-only immutable audit trail recording `who, what, when, why, before, after, ip, approval_ref`.
- **Information Disclosure**: Repository-level row filtering by default; manager sees consented summary only; small-group suppression (suppress any metric where `n < 5`).
- **Denial of Service**: Redis rate-limiting, job queue separation (reports, ai, integrations, maintenance).
- **Elevation of Privilege**: Time-bounded role grants with mandatory audit trail.
- **DPDP Rules Compliance**: Purpose limitation, consent log, access receipts, and withdrawal of consent workflow.

---

## 4. Phase 0 Verification & Quality Gates
- [ ] Role-Permission matrix has 100% coverage of resources × actions.
- [ ] Every entity in Section 21 is represented with complete primary/foreign keys and indexes in the ERD.
- [ ] Hash-chaining algorithm for the Evidence Ledger is mathematically defined.
- [ ] Color contrast ratios in the design system meet or exceed WCAG 2.2 AA (4.5:1 for normal text, 3:1 for large text).
- [ ] Every known limitation and default assumption is documented in `docs/KNOWN_LIMITATIONS.md` and `docs/ASSUMPTIONS.md`.
- [ ] Honesty Ledger updated to reflect completed Phase 0 design artifacts.

---

## 5. Open Questions & Decision Points for User Approval
1. **Approval of Phase 0 Scope**: Does the above outline cover all required architectural foundations?
2. **Permission Matrix Structure**: We will author `docs/security/PERMISSION_MATRIX.json` so that in Phase 1, automated backend tests can be generated directly from it.
3. **Evidence Ledger Hash Algorithm**: We propose SHA-256 for chaining evidence entries (`prev_hash + row_data_hash`). Any specific cryptographic preference?

*Upon user approval of this plan, Phase 0 documentation and architectural artifacts will be generated.*
