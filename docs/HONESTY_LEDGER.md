# TRELLIS Honesty Ledger

This document tracks verified, unverified, and unbuilt capabilities across all phases of TRELLIS for leadership review.

Last Updated: 2026-11-13 (Phase 0 Deliverables Complete)

---

## 1. Documented Specifications (Phase 0 Complete)
All architectural models, security matrices, design tokens, and compliance specifications authored and committed in Phase 0. (Application code is not yet written, as Phase 0 is design and documentation only).

| Spec ID | Capability / Artifact | Documentation Path | Status | Verification & Notes |
|---|---|---|---|---|
| DOC-001 | Master Product Brief (24 Sections) | `docs/PRODUCT_BRIEF.md` & `CLAUDE.md` | Documented | Full 24 sections verbatim; locked stack invariant. |
| DOC-002 | Technology Stack & Registry Pins | `docs/STACK.md` | Documented | Live-verified on 2026-11-13 from PyPI & npm registries; single MySQL driver (`asyncmy`) and single password hasher (`argon2-cffi`). |
| DOC-003 | Day-0 Assumptions & Defaults Log | `docs/ASSUMPTIONS.md` | Documented | Records confirmed answers (Q1 placeholder, Q12 3-part mapping); Q4 (Entra ID) and Q5 (2k/300 scale) marked assumed. |
| DOC-004 | Phase 0 Delivery Plan | `docs/phases/PHASE_0_PLAN.md` | Documented | Scope, boundaries, and vertical deliverable sequence. |
| DOC-005 | Role-Permission Matrix (D0.2) | `docs/security/PERMISSION_MATRIX.json` & `.md` | Documented | JSON matrix covering 5 active and 7 modeled future roles across 15 actions; policy engine `can()`. |
| DOC-006 | ERD & Migrations Plan (D0.3) | `docs/architecture/ERD_MIGRATIONS_PLAN.md` | Documented | 51 reconciled entities with full relational constraints; feature-to-table matrix for Sec 8–14 & 22; Alembic 8-step sequence. |
| DOC-007 | Threat Model & Security (D0.7) | `docs/security/THREAT_MODEL.md` | Documented | STRIDE analysis, India DPDP compliance model, blind grading anonymity, and prompt injection defense. |
| DOC-008 | Architecture Decision Records (D0.8)| `docs/adr/ADR-0001` through `ADR-0004` | Documented | ADR-0001 (Monolith), ADR-0002 (Policy Engine), ADR-0003 (Ledger + RFC 8785 + Crypto-Shredding), ADR-0004 (Legacy Portal 3-part map). |
| DOC-009 | Information Architecture (D0.1) | `docs/architecture/INFORMATION_ARCHITECTURE.md` | Documented | 10 module topologies, role-specific navigation, command bar registry, and legacy 3-part transformation. |
| DOC-010 | Design Tokens & System (D0.4) | `docs/design/DESIGN_TOKENS.md` | Documented | WCAG 2.2 AA compliant tokens, labelled placeholder palette (`#0B0D12`, `#1294C4`, `#8B3A3A`, `#FFFFFF`), 8px grid, dyslexia font. |
| DOC-011 | Accessibility Test Plan (D0.5) | `docs/accessibility/ACCESSIBILITY_PLAN.md` | Documented | `@axe-core/playwright` CI gates, keyboard walkthrough, NVDA/JAWS protocol, cognitive suite. |
| DOC-012 | ASCII Wireframes (D0.6) | `docs/design/WIREFRAMES.md` | Documented | Structural ASCII layouts for Home, Command Bar, Growth Ring, Consent Passport, and Evidence View. |
| DOC-013 | AI Governance Spec (Point 4a) | `docs/ai/AI_GOVERNANCE.md` | Documented | AI registry, CI evaluation harness (groundedness $\ge 0.98$), prompt versioning, PII scrubbing. |
| DOC-014 | Privacy & Consent Catalogue (4b)| `docs/privacy/PRIVACY_CATALOGUE.md` | Documented | 5 data classification tiers, purpose codes, configurable retention policies, right to erasure via crypto-shredding. |
| DOC-015 | API Conventions & Errors (4c) | `docs/architecture/API_CONVENTIONS.md` | Documented | RFC 9457 Problem Details, snake_case to camelCase conversion, cursor pagination, and idempotency headers. |
| DOC-016 | Test Strategy & Budgets (4d) | `docs/quality/TEST_STRATEGY.md` | Documented | Testing pyramid, matrix test generation, p95 $\le 300$ms API budget, FCP $\le 2.0$s, 600 concurrent load target. |
| DOC-017 | Integration Inventory (4e) | `docs/integrations/INTEGRATION_INVENTORY.md` | Documented | 11 interoperability connectors (xAPI, SCORM, cmi5, LTI 1.3, Entra ID, Teams, NIM) with honest status. |
| DOC-018 | 14 Innovations Map (4f) | `docs/architecture/SIGNATURE_INNOVATIONS_MAP.md` | Documented | Complete roadmap and acceptance tests for all 14 signature innovations. |
| DOC-019 | Interactive HTML Prototype (4g) | `docs/prototype/index.html` | Documented & Verified | Fully interactive single-page HTML prototype of all 5 key screens with keyboard shortcuts and WCAG AA contrast. |

---

## 2. Unverified or Environment-Limited Items
Items configured or designed but unverified in live environments due to environment constraints.

| Item ID | Component | Reason Unverified / Limited | Mitigation / Action Taken |
|---|---|---|---|
| ENV-001 | `docker compose config` execution | Docker CLI and daemon are not installed on the local Windows host. | Compose YAML syntax and networking manually verified: MySQL 8.4 deprecated authentication flag removed, ports 3306 & 6379 removed from host exposure, all passwords sourced from `.env` without fallbacks. |
| ENV-002 | Microsoft Entra SSO (Q4) | Assumed, not yet confirmed by CSM. | Architecture specifies OIDC client adapter; local Argon2id auth configured for dev/demo. |
| ENV-003 | Scale Specifications (Q5) | Assumed (2,000 employees, 300 concurrent users), not yet confirmed by CSM. | Connection pool sizing and Redis caching configured for this assumed baseline. |

---

## 3. Not Built or Blocked
Features deferred to future phases, blocked on external credentials, or awaiting legal/asset sign-off.

| Feature ID | Capability | Target Phase | Blocker / Dependency | Mitigation / Fallback |
|---|---|---|---|---|
| BLK-001 | Official CSM branding & assets (Q1) | Phase 0/1 | Official brand guidelines pending user supply | Labelled placeholder branding (`#0B0D12`, `#1294C4`, `#8B3A3A`, `#FFFFFF`) |
| BLK-002 | Microsoft Entra ID production tenant | Phase 1 | Live M365 tenant credentials | Mock OIDC adapter + local Argon2id auth |
| BLK-003 | Live NVIDIA NIM endpoint & API keys (Q9) | Phase 4 | Model endpoint credentials | Deterministic mock provider implementing the NIM schema |
| BLK-004 | Psychometrics & webcam proctoring (Q7) | Phase 2 | Legal & DPO DPDP sign-off | Feature flags default to `OFF` (`FEATURE_PSYCHOMETRICS=false`, `FEATURE_WEBCAM_PROCTORING=false`) |
| BLK-005 | HR System production API connection (Q3) | Phase 1 | HR integration API details | CSV import interface + `HrSystemAdapter` |
| BLK-006 | Current Employee Skills Portal export (Q12) | Phase 0/1 | Screenshots/exports to be sent later | Mapped to 3 known legacy core parts: Skill Assessment, Onboarding Induction, Skill Sheet |
