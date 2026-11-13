# PHASE 1 PLAN: Authentication, Policy Engine, Personalised Home, Pathways & Evidence Foundation

**Phase Objective**: Build the production-grade foundational vertical slices of TRELLIS: user identity and SSO, centralized authorization, immutable audit logging, the append-only evidence ledger foundation, personalized learner Home screen, Pathways with First-90-Days Copilot, and the accessible Global Command Bar.

---

## 1. Scope & Core Capabilities

| Capability | Module / Layer | Key Invariants & Features |
|---|---|---|
| **Identity & SSO** | `identity` | Local Argon2id password hashing, JWT access token (30m) + refresh token rotation (7d), visible session device list, Microsoft Entra ID OIDC adapter interface with deterministic dev mock. |
| **Policy Engine & ABAC** | `access` | Runtime implementation of `can(subject, action, resource, context)` driven by `docs/security/PERMISSION_MATRIX.json` under strict **Default-Deny**; repository-level SQL query filtering. |
| **Audit Log & Access Receipts** | `audit` | Immutable `audit_log` recording `who, what, when, why, before, after, ip, approval_ref`; `access_receipts` tracking cross-user personal data reads. |
| **Evidence Ledger Foundation** | `growth_ring` | Per-employee SHA-256 hash chaining using RFC 8785 canonical serialization; off-chain `evidence_records` store with crypto-shredding hooks for DPDP erasure. |
| **Personalised Home** | Frontend (Angular 22) | "Continue climbing" hero, current skill gaps summary, assigned learning, streak tracker with freeze indicator, badges, Greenhouse featured idea, announcements. |
| **Pathways & Onboarding** | `pathways` | Role onboarding pathways, course/module progression, prerequisite graph validation, First-90-Days Copilot daily action prompt. |
| **Global Command Bar** | Frontend (Angular 22) | `Ctrl/Cmd+K` keyboard dialog, server-side permission-trimmed search across actions, courses, wiki, and experts; focus trap and screen-reader announcements. |
| **CI/CD Pipeline** | `.github/workflows/` | Automated linting (Ruff), strict static typing (Mypy), Pytest testcontainers integration suite, Angular build, and Playwright Axe-core accessibility checks. |

---

## 2. Vertical Slices Breakdown

Delivery strictly adheres to vertical slicing: each slice includes migration, models, policy checks, service logic, API endpoints, Angular components, tests, and documentation before moving to the next.

```
Slice 1.1: Core Migrations (0001 & 0002) & Base ORM Models
   ↓
Slice 1.2: Authentication & Token Rotation (Argon2id + OIDC Adapter)
   ↓
Slice 1.3: Centralized Policy Engine & Immutable Audit Logger
   ↓
Slice 1.4: Tamper-Evident Evidence Ledger Core (RFC 8785 + SHA-256 Chaining)
   ↓
Slice 1.5: Pathways & Curriculum Domain Services
   ↓
Slice 1.6: Angular 22 Foundation, Signals Store & Tailwind 4 Layout
   ↓
Slice 1.7: Personalised Home Page (Hero, Streaks, Skeletons, Empty States)
   ↓
Slice 1.8: Pathways & First-90-Days Copilot UI
   ↓
Slice 1.9: Global Command Bar (Ctrl+K Dialog & Permission-Trimmed Search)
   ↓
Slice 1.10: CI/CD Pipeline (.github/workflows/ci.yml) & E2E Validation
```

### Detailed Slices

#### Slice 1.1: Core Migrations & Base Models
- **Database Tables**: `organisations`, `users`, `employment_records`, `roles`, `grants`, `consents`, `skills`, `skill_levels`, `skill_edges`, `role_requirements`, `evidence_ledger`, `evidence_records`, `ledger_checkpoints`.
- **Alembic Scripts**: Reversible `0001_core_tenancy_and_identity.py` and `0002_skills_and_evidence_ledger.py`.
- **Testing**: Applied and rolled back against ephemeral MySQL 8.4 container.

#### Slice 1.2: Authentication & Session Management
- **Endpoints**: `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`, `GET /api/v1/auth/me`, `GET /api/v1/auth/sessions`.
- **Security**: Argon2id password hashing via `argon2-cffi`; JWT signature verification with HS256/RS256; refresh token rotation preventing replay attacks.
- **SSO**: Microsoft Entra ID OIDC client adapter (`OidcAuthAdapter`) with mock implementation active for local dev/demo.

#### Slice 1.3: Centralized Policy Engine & Audit System
- **Engine**: `can(subject, action, resource, context)` evaluating `PERMISSION_MATRIX.json` under strict Default-Deny.
- **Audit**: FastAPI middleware recording immutable rows in `audit_log` for all state mutations; writes `access_receipts` for personal data reads.
- **Separation of Duties**: Author self-approval forbidden; admin user-grant elevations require approval and expiry.

#### Slice 1.4: Evidence Ledger Foundation (RFC 8785)
- **Engine**: Python service implementing `RFC 8785` JSON Canonicalization Scheme (JCS) and SHA-256 chaining.
- **Chain Invariant**:
  $$\text{Hash}_n = \text{SHA256}(\text{org\_id} \,\|\, \text{pseudonym\_id} \,\|\, \text{seq\_num} \,\|\, \text{Hash}_{n-1} \,\|\, \text{JCS}(\text{payload}))$$
- **Verification Service**: `verify_employee_chain(user_id)` validates cryptographic integrity from block #1 to present; flags tampering as security incident.
- **Crypto-Shredding Hooks**: Prepares off-chain `evidence_records` deletion without breaking hash sequence.

#### Slice 1.5: Pathways Service & Curriculum API
- **Migrations**: `0003_pathways_and_courses.py` (`pathways`, `courses`, `modules`, `enrolments`, `cohorts`, `batches`).
- **Endpoints**: `GET /api/v1/pathways`, `GET /api/v1/pathways/{id}`, `POST /api/v1/pathways/{id}/enrol`, `GET /api/v1/pathways/first-90-days`.
- **Logic**: Prerequisite graph validation; calculates progress percentage and time-to-productivity telemetry.

#### Slice 1.6: Angular 22 Application Foundation
- **Architecture**: Standalone components, native Signals (`signal()`, `computed()`, `effect()`), lazy-loaded routes, Tailwind CSS 4 design tokens.
- **Auth Store**: Reactive authentication state tracking current user, active role, and token rotation.
- **Accessibility**: Skip link, landmark structure (`header`, `nav`, `main`, `footer`), visible focus indicators (`2px solid cyan/blue`).

#### Slice 1.7: Personalised Home Screen
- **Components**:
  - `HeroClimbingComponent`: Dynamic "Continue climbing" action card with resume button.
  - `SkillGapsCardComponent`: Real-time skill gaps from latest Growth Ring projection.
  - `AssignedSessionsComponent`: Upcoming sessions and calendar sync trigger.
  - `StreakCounterComponent`: 14-day climbing streak with freeze count badge.
  - `GreenhouseCardComponent`: Featured idea of the month.
  - `DemoBannerComponent`: Persistent synthetic data banner when `TRELLIS_ENV=demo`.
- **States**: Loading skeleton pulses (`aria-busy="true"`), empty state cards, and retryable error cards.

#### Slice 1.8: Pathways & First-90-Days Copilot UI
- **Components**:
  - `PathwayListComponent`: Interactive pathway browser with filter by role and difficulty.
  - `First90DaysCopilotComponent`: Daily prioritised onboarding task, buddy contact card, and milestone checklist.
  - `ModulePlayerComponent`: Lesson viewer with reading ruler, dyslexia font toggle, and calm mode.

#### Slice 1.9: Global Command Bar (`Ctrl/Cmd+K`)
- **Component**: Accessible modal dialog (`role="dialog"`, `aria-modal="true"`).
- **Features**:
  - Global hotkey listener (`Ctrl+K` and `Cmd+K`), `Escape` to dismiss.
  - Server-side permission-trimmed search querying actions, courses, wiki articles, and mentors.
  - Keyboard navigation: arrow key traversal with roving `aria-selected="true"`.

#### Slice 1.10: First CI Pipeline & Automated Test Suite
- **GitHub Workflow** (`.github/workflows/ci.yml`):
  1. *Backend Lint & Types*: `ruff check .` and `mypy --strict .`
  2. *Backend Tests*: `pytest --cov=app --cov-report=term-missing`
  3. *Permission Matrix Tests*: Programmatically generated tests verifying all permitted and forbidden tuples.
  4. *Frontend Lint & Build*: `ng build --configuration=production`
  5. *Accessibility Tests*: Playwright + `@axe-core/playwright` scanning Home, Pathways, and Command Bar for zero violations.

---

## 3. Testing & Verification Gates for Phase 1
- [ ] Local auth & JWT refresh token rotation tested with automated expiration tests.
- [ ] Policy engine enforces Default-Deny: unlisted tuples return 403 Forbidden.
- [ ] 100% of mutation endpoints write to `audit_log`; manager reads write to `access_receipts`.
- [ ] Evidence ledger SHA-256 chaining passes property-based tests (arbitrary dictionary key order yields deterministic hash).
- [ ] Simulated tampering test: modifying a historical block hash is detected and refused.
- [ ] All Angular views achieve zero WCAG 2.2 AA violations in `@axe-core/playwright`.
- [ ] Keyboard walkthrough: Tab, Shift+Tab, Ctrl+K, Escape, and Enter fully functional without mouse.
- [ ] Skeletons, empty states, error states, and synthetic demo banner render and tested.
- [ ] Honesty Ledger updated with verified test outputs.

---

## 4. Open Questions & Approvals Needed
1. **Approval of Phase 1 Scope**: Does the sequence of vertical slices match leadership priorities?
2. **Entra ID Tenant Mock**: Confirm that Phase 1 local development proceeds with the deterministic mock OIDC provider until CSM IT provisions live client credentials.
3. **Synthetic Demo Seed**: We will provide `scripts/seed_demo_data.py` (gated by `TRELLIS_ENV=demo`) to populate realistic synthetic joiners (e.g. "Priya S."), cohorts, pathways, and ideas for review.

*Upon approval, Phase 1 execution will commence with Slice 1.1.*
