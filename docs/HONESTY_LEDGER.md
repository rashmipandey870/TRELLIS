# TRELLIS Honesty Ledger

This document tracks verified, unverified, and unbuilt capabilities across all phases of TRELLIS for leadership review.

Last Updated: 2026-11-14 (Checkpoint 1 Hardening: Immutability, Policy Negatives, Key Rotation, Axe Playwright, Transactional Audit, and MFA Bypass Removal)

---

## 1. Documented Specifications & Foundations

| Spec ID | Capability / Artifact | Documentation Path | Status | Verification & Notes |
|---|---|---|---|---|
| DOC-001 | Master Product Brief (24 Sections) | `docs/PRODUCT_BRIEF.md` & `CLAUDE.md` | Documented | Full 24 sections verbatim; locked Python + Angular stack invariant. |
| DOC-002 | Technology Stack & Registry Pins | `docs/STACK.md` | Documented & Verified | Live-verified on 2026-11-13; TypeScript 6.0.3 (compiler requirement `>=6.0 <6.1`), Angular 22.2.6, single MySQL driver (`asyncmy` 0.2.18), single password hasher (`argon2-cffi` 25.1.0). Live install proven via `npm install` (440 pkgs) and `pip install` + `pip check`. |
| DOC-003 | Day-0 Assumptions & Defaults Log | `docs/ASSUMPTIONS.md` | Documented | Records confirmed answers (Q1 placeholder, Q12 3-part mapping); Q4 (Entra ID) and Q5 (2k/300 scale) marked assumed. |
| DOC-004 | Phase 0 Delivery Plan | `docs/phases/PHASE_0_PLAN.md` | Documented | Scope, boundaries, and vertical deliverable sequence. |
| DOC-005 | Role-Permission Matrix (D0.2) | `docs/security/PERMISSION_MATRIX.json` | Documented & Verified | Complete matrix covering 20 resources x 15 actions x 12 roles (3,600 tuples) with Default-Deny. `coverage_report.py` asserts 100% default-deny coverage (118 explicit grants, 3,482 default-denied). |
| DOC-006 | ERD & Migrations Plan (D0.3) | `docs/architecture/ERD_MIGRATIONS_PLAN.md` | Documented | 51 reconciled entities with full relational constraints; feature-to-table matrix for Sec 8–14 & 22; Alembic 8-step sequence. |
| DOC-007 | Threat Model & Security (D0.7) | `docs/security/THREAT_MODEL.md` | Documented | STRIDE analysis, India DPDP compliance model, blind grading anonymity, and prompt injection defense. |
| DOC-008 | Architecture Decision Records (D0.8)| `docs/adr/` | Documented | ADR-0001 (Monolith), ADR-0002 (Policy Engine), ADR-0003 (Ledger + RFC 8785 + Crypto-Shredding), ADR-0004 (Legacy Portal 3-part map). |
| DOC-009 | Information Architecture (D0.1) | `docs/architecture/INFORMATION_ARCHITECTURE.md` | Documented | 10 module topologies, role-specific navigation, command bar registry, and legacy 3-part transformation. |
| DOC-010 | Design Tokens & System (D0.4) | `docs/design/DESIGN_TOKENS.md` | Documented | WCAG 2.2 AA compliant tokens, labelled placeholder palette (`#0B0D12`, `#1294C4`, `#8B3A3A`, `#FFFFFF`), 8px grid, dyslexia font. |
| DOC-011 | Accessibility Test Plan (D0.5) | `docs/accessibility/ACCESSIBILITY_PLAN.md` | Documented | `@axe-core/playwright` CI gates, keyboard walkthrough, NVDA/JAWS protocol, cognitive suite. |
| DOC-012 | ASCII Wireframes (D0.6) | `docs/design/WIREFRAMES.md` | Documented | Structural ASCII layouts for Home, Command Bar, Growth Ring, Consent Passport, and Evidence View. |
| DOC-013 | AI Governance Spec (Point 4a) | `docs/ai/AI_GOVERNANCE.md` | Documented | AI registry, CI evaluation harness (groundedness $\ge 0.98$), prompt versioning, PII scrubbing; Nemotron placeholder model (`nvidia/llama-3.1-nemotron-70b-instruct`). |
| DOC-014 | Privacy & Consent Catalogue (4b)| `docs/privacy/PRIVACY_CATALOGUE.md` | Documented | 5 data classification tiers, purpose codes, configurable retention policies, right to erasure via crypto-shredding. |
| DOC-015 | API Conventions & Errors (4c) | `docs/architecture/API_CONVENTIONS.md` | Documented | RFC 9457 Problem Details, snake_case to camelCase conversion, cursor pagination, and idempotency headers. |
| DOC-016 | Test Strategy & Budgets (4d) | `docs/quality/TEST_STRATEGY.md` | Documented | Testing pyramid, matrix test generation, p95 $\le 300\text{ ms}$ API budget, FCP $\le 2.0\text{ s}$, 600 concurrent load target. |
| DOC-017 | Integration Inventory (4e) | `docs/integrations/INTEGRATION_INVENTORY.md` | Documented | 11 interoperability connectors (xAPI, SCORM, cmi5, LTI 1.3, Entra ID, Teams, NIM) with honest status. |
| DOC-018 | 14 Innovations Map (4f) | `docs/architecture/SIGNATURE_INNOVATIONS_MAP.md` | Documented | Complete roadmap and acceptance tests for all 14 signature innovations. |
| DOC-019 | Interactive HTML Prototype (4g) | `docs/prototype/index.html` | Documented & Verified | Fully interactive single-page HTML prototype of all 5 key screens with keyboard shortcuts and WCAG AA contrast. |
| DOC-020 | Dependency Vulnerability Audit | `docs/quality/DEPENDENCY_AUDIT_2026-11-13.md` | Documented & Audited | Raw audit output from `pip-audit` and `npm audit`. DOMPurify override (`3.4.17`) verified; 0 critical vulnerabilities in frontend, 0 product CVEs in Python backend. Container pip upgraded to $\ge 26.2.0$. |
| DOC-021 | Permission Human Review (Point 2)| `docs/security/PERMISSION_REVIEW.md` | Documented & Verified | Plain-English human review tables covering all 118 explicit grants across active roles, with strict default-deny boundary. |
| DOC-022 | Local Dev Setup Guide (Point 3) | `docs/DEV_SETUP.md` | Documented | Exact installation instructions for Node 24.15 LTS (via NVM), Docker Desktop with WSL2 or native MySQL 8.4 + Redis, and asymmetric key generation. |
| DOC-023 | Phase 1 Delivery Plan (Reordered)| `docs/phases/PHASE_1_PLAN.md` | Documented | Reordered to place CI pipeline first (Slice 1.1); detailed TOTP MFA, asymmetric key rotation, token family reuse detection, DB-level immutability, and 2 mandatory review checkpoints (after 1.4 and 1.7). |

---

## 2. Unverified or Environment-Limited Items
Items configured or designed but unverified in live environments due to environment constraints.

| Item ID | Component | Reason Unverified / Limited | Mitigation / Action Taken |
|---|---|---|---|
| ENV-001 | `docker compose config` execution | **Execution Unverified**: Docker CLI and Docker Desktop daemon are not installed on this local Windows host (`CommandNotFoundException`). | Compose YAML syntax and networking manually hardened: MySQL 8.4 deprecated authentication flag removed, ports 3306 & 6379 isolated from host exposure, all passwords sourced from `.env` without fallbacks. Documented in `docs/DEV_SETUP.md`. |
| ENV-002 | Microsoft Entra SSO (Q4) | Assumed, not yet confirmed by CSM. | Architecture specifies OIDC client adapter; local Argon2id auth configured for dev/demo. |
| ENV-003 | Scale Specifications (Q5) | Assumed (2,000 employees, 300 concurrent users), not yet confirmed by CSM. | Connection pool sizing and Redis caching configured for this assumed baseline. |
| ENV-004 | Node Version Compatibility | Local host runs Node `v25.2.1`. Angular CLI 22.2.7 requires Node `^22.22.3 \|\| ^24.15.0 \|\| >=26.0.0`. | Node engine warnings observed during `npm install`; packages installed successfully. User instructions provided in `docs/DEV_SETUP.md` to switch to Node `24.15.0 LTS` via `nvm-windows`. |
| ENV-005 | Live MySQL 8.4 & Redis Integration Tests | **Unverified on Local Host**: Neither Docker Desktop nor native MySQL 8.4 is currently running on the local host machine. | Integration tests against live MySQL 8.4 and Redis 7.4 marked **Unverified** until Docker Desktop or native MySQL 8.4 is started. Fast in-memory unit tests, mock repositories, and cryptographic hashing tests run cleanly. |
| ENV-006 | Database-Level Immutability | **Unverified until CI passes**: Explicit per-table grants (`scripts/init_db_users.sql` and `scripts/init_db_users.py`) and integration tests (`tests/test_mysql_immutability.py`) asserting MySQL error 1142 on UPDATE/DELETE are written. Live engine verification requires the GitHub Actions CI job with `mysql:8.4` service container. | Tests authored and wired into `.github/workflows/ci.yml`. Marked unverified until live CI execution. |
| ENV-007 | Automated Axe-Core / WCAG 2.2 AA Audit | **Unverified until CI passes**: Real `@axe-core/playwright` browser test authored (`frontend/tests/a11y.spec.ts`, `frontend/playwright.config.ts`). Dummy scripts removed. Scans rules and reports exact pass/incomplete/violation counts. Requires CI headless Chromium execution against built frontend. | Pinned in `package.json`, configured in CI job `accessibility-audit`. Marked unverified until live CI execution. |
| ENV-008 | Asymmetric Key Rotation | **Unverified until CI passes**: Multi-key JWKS registry, active key rotation, backwards-compatible token verification, and non-dev startup refusal authored in `app/core/security.py` and `tests/test_key_rotation.py`. | Tested locally with unit tests; marked unverified until live CI run confirms key rotation pipeline. |
| ENV-009 | All Mutations Audited & Transactional Rollback | **Unverified until CI passes**: Transactional audit logging inside mutations, removal of `default_org`, removal of `except Exception: pass`, and rollback on audit write failure authored in `auth_service.py`, `AuditLogMiddleware`, and `tests/test_audit_transaction.py`. | Unit and transaction tests pass locally; marked unverified until end-to-end CI pipeline passes. |

---

## 3. Not Built or Blocked
Features deferred to future phases, blocked on external credentials, or awaiting legal/asset sign-off.

| Feature ID | Capability | Target Phase | Blocker / Dependency | Mitigation / Fallback |
|---|---|---|---|---|
| BLK-001 | Official CSM branding & assets (Q1) | Phase 0/1 | Official brand guidelines pending user supply | Labelled placeholder branding (`#0B0D12`, `#1294C4`, `#8B3A3A`, `#FFFFFF`) |
| BLK-002 | Microsoft Entra ID production tenant | Phase 1 | Live M365 tenant credentials | Mock OIDC adapter + local Argon2id auth |
| BLK-003 | Live NVIDIA NIM endpoint & API keys (Q9) | Phase 4 | Model endpoint credentials | Deterministic mock provider implementing the NIM schema; Nemotron model placeholder configured (`nvidia/llama-3.1-nemotron-70b-instruct`) |
| BLK-004 | Psychometrics & webcam proctoring (Q7) | Phase 2 | Legal & DPO DPDP sign-off | Feature flags default to `OFF` (`FEATURE_PSYCHOMETRICS=false`, `FEATURE_WEBCAM_PROCTORING=false`) |
| BLK-005 | HR System production API connection (Q3) | Phase 1 | HR integration API details | CSV import interface + `HrSystemAdapter` |
| BLK-006 | Current Employee Skills Portal export (Q12) | Phase 0/1 | Screenshots/exports to be sent later | Mapped to 3 known legacy core parts: Skill Assessment, Onboarding Induction, Skill Sheet |
