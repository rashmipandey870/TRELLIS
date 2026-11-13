# PHASE 1 PLAN: CI Quality Pipeline, Identity & MFA, Policy Engine, Personalised Home, Pathways & Evidence Foundation

**Phase Objective**: Build the production-grade foundational vertical slices of TRELLIS, beginning with the automated CI quality gate. Establish user identity with TOTP MFA, centralized authorization, database-enforced immutable audit logging, the append-only evidence ledger foundation, personalized learner Home screen, Pathways with First-90-Days Copilot, and the accessible Global Command Bar.

---

## 1. Scope & Core Capabilities

| Capability | Module / Layer | Key Invariants & Features |
|---|---|---|
| **CI Quality Gate** | `.github/workflows/` | Automated linting (`ruff`), strict static typing (`mypy --strict`), test runner (`pytest`), permission matrix verifier, Angular build, and `@axe-core/playwright` accessibility gate. **Every slice must pass this pipeline.** |
| **Identity & Asymmetric Auth** | `identity` | Local Argon2id password hashing; asymmetric JWT signing (RS256 / Ed25519) with automated key rotation plan and JWKS endpoint; hashed refresh token storage with single-use rotation and token-family reuse revocation; TOTP MFA (RFC 6238) required for `LK_ADMIN` and `SUPER_ADMIN`; Microsoft Entra ID OIDC mock adapter. |
| **Database-Level Immutability** | `database` | Strict DB user privilege separation: `trellis_migrator` (DDL only) vs `trellis_app` (DML only). `trellis_app` has strictly `SELECT, INSERT` on `audit_log`, `access_receipts`, and `evidence_ledger`. `UPDATE` and `DELETE` privileges are explicitly denied at the MySQL engine level. |
| **Policy Engine & ABAC** | `access` | Runtime implementation of `can(subject, action, resource, context)` driven by `docs/security/PERMISSION_MATRIX.json` under strict **Default-Deny**; repository-level SQL query filtering. |
| **Audit Log & Access Receipts** | `audit` | Included in Migration `0001`; immutable `audit_log` recording `who, what, when, why, before, after, ip, approval_ref`; `access_receipts` tracking cross-user personal data reads. |
| **Evidence Ledger Foundation** | `growth_ring` | Per-employee SHA-256 hash chaining using RFC 8785 canonical serialization (JCS); off-chain `evidence_records` store with crypto-shredding hooks for DPDP erasure. |
| **Personalised Home** | Frontend (Angular 22) | "Continue climbing" hero, current skill gaps summary, assigned learning, streak tracker with freeze indicator, badges, Greenhouse featured idea, announcements. |
| **Pathways & Onboarding** | `pathways` | Role onboarding pathways, course/module progression, prerequisite graph validation, First-90-Days Copilot daily action prompt. |
| **Global Command Bar** | Frontend (Angular 22) | `Ctrl/Cmd+K` keyboard dialog, server-side permission-trimmed search across actions, courses, wiki, and experts; focus trap and screen-reader announcements. |

---

## 2. Reordered Vertical Slices Sequence

Every slice is complete, fully tested, and must pass the CI pipeline before the next slice begins. Two mandatory user checkpoints are scheduled after Slice 1.4 and Slice 1.7.

```
Slice 1.1: Automated CI Quality Pipeline & Test Harness (.github/workflows/ci.yml)
   ↓
Slice 1.2: Core Migrations (0001 & 0002) with DB-Level Immutability Enforced
   ↓
Slice 1.3: Asymmetric Auth, Hashed Token Rotation & TOTP MFA (pyotp)
   ↓
Slice 1.4: Centralized Policy Engine & Immutable Audit System
   ↓
★ MANDATORY CHECKPOINT 1: Backend Core Review (Demo script, test results, unverified items)
   ↓
Slice 1.5: Tamper-Evident Evidence Ledger Core (RFC 8785 + SHA-256 Chaining)
   ↓
Slice 1.6: Pathways & Curriculum Domain Services
   ↓
Slice 1.7: Angular 22 Foundation, Signals Store, Tailwind 4 & Personalised Home
   ↓
★ MANDATORY CHECKPOINT 2: First Demoable UI Review (Demo script, test results, unverified items)
   ↓
Slice 1.8: Pathways & First-90-Days Copilot UI
   ↓
Slice 1.9: Global Command Bar (Ctrl+K Dialog & Permission-Trimmed Search)
   ↓
Slice 1.10: Integration E2E Suite, Synthetic Demo Seed Script & Phase 1 Sign-Off
```

---

## 3. Detailed Slice Specifications

### Slice 1.1: Automated CI Pipeline & Test Harness (First Slice)
- **GitHub Workflow** (`.github/workflows/ci.yml`):
  1. *Backend Lint & Formatting*: `ruff check backend/` and `ruff format --check backend/`.
  2. *Strict Static Typing*: `mypy --strict backend/`.
  3. *Permission Matrix Verification*: Automated execution of `docs/security/coverage_report.py` and test generator asserting 100% default-deny coverage.
  4. *Backend Test Suite*: `pytest backend/tests/ -v --cov=backend/app --cov-report=term-missing`.
  5. *Frontend Compilation*: `ng build --configuration=production` under Node 24.15 LTS.
  6. *Accessibility Gate*: Playwright + `@axe-core/playwright` scanning compiled views for zero WCAG 2.2 AA violations.
- **Project Tooling Configurations**:
  - `backend/pyproject.toml` (Ruff, Mypy, Pytest configurations).
  - `backend/requirements.txt` & `backend/requirements-dev.txt`.
  - `frontend/package.json` with DOMPurify `3.4.17` override, Angular 22.2.6, and TypeScript 6.0.3 pins.
- **Invariant**: No subsequent slice code can be merged unless Slice 1.1 passes with zero errors.

---

### Slice 1.2: Core Migrations & Database-Level Immutability
- **Database Tables**:
  - *Migration 0001 (`0001_core_tenancy_identity_and_audit.py`)*: `organisations`, `users`, `employment_records`, `roles`, `grants`, `consents`, `audit_log`, `access_receipts`. *(Note: `audit_log` and `access_receipts` are in Migration 0001 as required for Slice 1.3/1.4).*
  - *Migration 0002 (`0002_skills_and_evidence_ledger.py`)*: `skills`, `skill_levels`, `skill_edges`, `role_requirements`, `evidence_ledger`, `evidence_records`, `ledger_checkpoints`.
- **Database-Level Immutability Enforcement**:
  - Migrations run under `trellis_migrator` (DDL privileges).
  - Application queries run under `trellis_app` (DML privileges).
  - `trellis_app` is explicitly denied `UPDATE` and `DELETE` on `audit_log`, `access_receipts`, and `evidence_ledger`.
- **Immutability Invariant Test** (`test_audit_immutability.py`):
  - Proves via automated assertion that executing an `UPDATE` or `DELETE` statement against `audit_log` or `evidence_ledger` under `trellis_app` raises a MySQL permission denied error (`OperationalError: 1142: UPDATE command denied to user 'trellis_app'`).

---

### Slice 1.3: Asymmetric Auth, Token Family Rotation & TOTP MFA
- **Endpoints**:
  - `POST /api/v1/auth/login`: Authenticates password using Argon2id (`argon2-cffi`). If user holds `LK_ADMIN` or `SUPER_ADMIN` role, returns `mfa_required=true` with a temporary MFA exchange ticket.
  - `POST /api/v1/auth/mfa/challenge`: Validates 6-digit TOTP token (`pyotp`, RFC 6238, 30-second window, skew $\pm 1$) or backup recovery code.
  - `POST /api/v1/auth/mfa/setup`: Generates base32 secret and `otpauth://` URI with QR code for authenticator apps.
  - `POST /api/v1/auth/refresh`: Validates refresh token. Stores tokens as cryptographic hashes. On every refresh, rotates token and issues a new one. Detects token reuse: if an invalidated token is re-submitted, immediately revokes the entire token family and logs a high-severity security alert.
  - `POST /api/v1/auth/logout`: Revokes current session and invalidates refresh token.
  - `GET /api/v1/auth/me`: Returns current user identity, roles, and profile.
  - `GET /api/v1/auth/sessions`: Lists active sessions with device details and last activity.
  - `GET /api/v1/auth/.well-known/jwks.json`: Public JSON Web Key Set exposing current and previous public keys with key IDs (`kid`) for seamless asymmetric rotation.
- **Asymmetric Key Rotation Plan**:
  - Tokens signed using RS256 / Ed25519 private key.
  - Private key stored outside application codebase (`secrets/jwt_private.pem`).
  - Active key ID (`kid`) embedded in JWT header.
  - Verification allows an overlapping grace period (7 days) for previous key IDs during key rotation.
- **Mock OIDC Adapter**:
  - `OidcAuthAdapter` interface with deterministic development mock providing seamless local authentication while CSM IT provisions live Entra ID tenant credentials.

---

### Slice 1.4: Centralized Policy Engine & Immutable Audit System
- **Authorization Engine**:
  - Centralized function: `can(subject: UserContext, action: Action, resource: Resource, context: RequestContext) -> bool`.
  - Driven by `docs/security/PERMISSION_MATRIX.json` under strict **Default-Deny** (any unlisted tuple returns `False`).
  - Repository-level SQL filters (`apply_scope_filters`) automatically enforcing `OWN`, `COHORT`, `TEAM_DIRECT`, and `ORGANIZATION` boundaries.
  - Separation of duties enforcement: author self-approval forbidden; admin user-grant elevations require approval and explicit expiry.
- **Audit System**:
  - FastAPI middleware intercepting all state-changing requests (`POST`, `PUT`, `PATCH`, `DELETE`).
  - Writes immutable records to `audit_log` (`who, what, when, why, before, after, ip, approval_ref`).
  - Intercepts cross-user personal data reads (e.g. manager viewing team member Growth Ring) and writes to `access_receipts`.
- **Checkpoint 1 Verification**:
  - All unit, integration, and policy tests pass.

---

### ★ CHECKPOINT 1: Backend Core Review
- **Trigger**: Following Slice 1.4 completion.
- **Deliverables presented to user**:
  1. Detailed execution demo script showcasing login, MFA challenge, token rotation, reuse revocation, policy denial, and audit log generation.
  2. Complete automated test results (coverage, execution timings, immutability assertion).
  3. Honest ledger of unverified items (e.g. live Entra ID credentials, live MySQL if running against SQLite mock).
- **Gate**: Stop and await user approval before proceeding to Slice 1.5.

---

### Slice 1.5: Tamper-Evident Evidence Ledger Core (RFC 8785)
- **Engine**: Python service implementing RFC 8785 JSON Canonicalization Scheme (JCS) and SHA-256 chaining.
- **Chain Invariant**:
  $$\text{Hash}_n = \text{SHA256}(\text{org\_id} \,\|\, \text{pseudonym\_id} \,\|\, \text{seq\_num} \,\|\, \text{Hash}_{n-1} \,\|\, \text{JCS}(\text{payload}))$$
- **Verification Service**: `verify_employee_chain(pseudonym_id)` validates cryptographic integrity from block #1 to present; flags tampering as security incident.
- **Crypto-Shredding Hooks**: Off-chain personal details in `evidence_records` can be deleted with their encryption key upon DPDP Right to Erasure request, while the on-chain hash sequence remains mathematically intact.

---

### Slice 1.6: Pathways & Curriculum Domain Services
- **Migrations**: `0003_pathways_and_courses.py` (`pathways`, `courses`, `modules`, `enrolments`, `cohorts`, `batches`).
- **Endpoints**: `GET /api/v1/pathways`, `GET /api/v1/pathways/{id}`, `POST /api/v1/pathways/{id}/enrol`, `GET /api/v1/pathways/first-90-days`.
- **Domain Logic**: Prerequisite DAG acyclicity validation; calculates progress percentage and time-to-productivity telemetry.

---

### Slice 1.7: Angular 22 Foundation, Signals Store, Tailwind 4 & Personalised Home
- **Frontend Architecture**: Standalone components, native Signals (`signal()`, `computed()`, `effect()`), lazy-loaded routing, Tailwind CSS 4 design tokens with dyslexia font toggle and high-contrast support.
- **Personalised Home View**:
  - `HeroClimbingComponent`: "Continue climbing" hero card with resume button and progress ring.
  - `SkillGapsCardComponent`: Real-time skill gaps from latest Growth Ring projection.
  - `StreakCounterComponent`: 14-day climbing streak with freeze count badge.
  - `AssignedSessionsComponent`: Upcoming cohort calendar sessions.
  - `GreenhouseCardComponent`: Featured idea of the month.
  - `DemoBannerComponent`: Persistent synthetic data banner when `TRELLIS_ENV=demo`.
  - Accessible loading states: skeleton pulse animations (`aria-busy="true"`), empty state cards, retryable error cards.
- **Accessibility & Axe Validation**: Automated axe-core scan with 0 WCAG 2.2 AA violations.

---

### ★ CHECKPOINT 2: First Demoable UI Review
- **Trigger**: Following Slice 1.7 completion.
- **Deliverables presented to user**:
  1. Live demo script with steps to run the Angular application and navigate the Home screen with synthetic demo data.
  2. Visual evidence / layout verification against design tokens.
  3. Axe-core accessibility audit results and keyboard walkthrough verification.
  4. Honest ledger of unverified items.
- **Gate**: Stop and await user approval before proceeding to Slice 1.8.

---

### Slice 1.8: Pathways & First-90-Days Copilot UI
- **Components**:
  - `PathwayListComponent`: Interactive pathway catalog with role-based and difficulty filtering.
  - `First90DaysCopilotComponent`: Daily prioritised onboarding task, buddy contact card, and milestone checklist.
  - `ModulePlayerComponent`: Lesson viewer with reading ruler, dyslexia font toggle, and calm mode.

---

### Slice 1.9: Global Command Bar (`Ctrl/Cmd+K`)
- **Components**: Accessible modal dialog (`role="dialog"`, `aria-modal="true"`).
- **Features**:
  - Global hotkey listener (`Ctrl+K` and `Cmd+K`), `Escape` to dismiss.
  - Server-side permission-trimmed search querying actions, courses, wiki articles, and mentors.
  - Keyboard navigation: arrow key traversal with roving `aria-selected="true"`.

---

### Slice 1.10: Integration E2E Suite, Synthetic Demo Seed Script & Sign-Off
- **E2E Test Suite**: Full Playwright browser walkthrough of login $\to$ home $\to$ pathway navigation $\to$ command bar search.
- **Synthetic Seed Script**: `scripts/seed_demo_data.py` (gated by `TRELLIS_ENV=demo`) populating realistic synthetic joiners ("Priya S."), cohorts, pathways, and ideas.
- **Honesty Ledger Sign-Off**: Verification entries updated with live test timings, code coverage percentage, and test results.
