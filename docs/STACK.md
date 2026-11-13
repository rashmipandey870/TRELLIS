# TRELLIS Locked Technology Stack

## 1. Stack Invariants & Hard Rules (Master Brief Section 4)
- **Backend**: Python 3.11+ with FastAPI.
- **Frontend**: Angular 22 (Current Stable Release: 22.2.6, TypeScript, standalone components, Signals).
- **Node Engine Compatibility**: Angular CLI 22.2.7 requires Node `^22.22.3 || ^24.15.0 || >=26.0.0`. (Local build machine runs Node `v25.2.1`, which triggers engine warnings during install).
- **Driver & Security Selections**:
  - **Single MySQL Driver**: `asyncmy` (high-performance asyncio driver for MySQL 8+ InnoDB utf8mb4).
  - **Single Password Hashing Library**: `argon2-cffi` (Argon2id cryptographic password hashing).
- **Verification & Dependency Audit Status**:
  - **Live Verification Date**: `2026-11-13`
  - **Live Installation Proof**: Verified via real `npm install` (440 packages) and real `pip install` + `pip check` (reported: *No broken requirements found*).
  - **Vulnerability Audit Status**: **21 vulnerabilities identified in frontend tooling & transitive packages** (DOMPurify in Monaco Editor, deepmerge/glob in Jest); **0 vulnerabilities in Python product libraries**. See full report in [docs/quality/DEPENDENCY_AUDIT_2026-11-13.md](quality/DEPENDENCY_AUDIT_2026-11-13.md).
- **Hard Rule**: Do not introduce Node.js/Express/NestJS, Django, Flask, React, Vue, or Next.js for any product code. Node is allowed only as Angular's build tooling. Every helper service (code sandbox, report renderer, bot, workers) is also written in Python.
- **Dependency Pinning**: Every dependency is pinned to an exact verified version.

---

## 2. Frontend: Angular 22 Stack (Verified 2026-11-13 via npm Registry & Live Install)

| Package | Pinned Version | Purpose / Compatibility Notes |
|---|---|---|
| `@angular/core` | `22.2.6` | Core framework with Signals reactivity |
| `@angular/common` | `22.2.6` | Common directives, pipes, HTTP client |
| `@angular/router` | `22.2.6` | Lazy-loaded standalone routing |
| `@angular/forms` | `22.2.6` | Reactive forms & typed validation |
| `@angular/cdk` | `22.2.7` | Accessible headless UI primitives & A11y live announcer |
| `@angular/compiler` | `22.2.6` | Angular compiler |
| `@angular/platform-browser` | `22.2.6` | Browser platform & DOM abstraction |
| `@angular/cli` | `22.2.7` | Build orchestration (requires Node `^22.22.3 || ^24.15.0 || >=26.0.0`) |
| `@angular/compiler-cli` | `22.2.6` | Angular Ahead-of-Time compiler (requires TypeScript `>=6.0 <6.1`) |
| `typescript` | `6.0.3` | Pinned to satisfy compiler requirement (`>=6.0 <6.1`) |
| `rxjs` | `7.8.2` | Reactive extensions |
| `zone.js` | `0.16.3` | Zone execution context |
| `tailwindcss` | `4.3.5` | Utility-first design tokens & layout |
| `postcss` | `8.5.32` | CSS post-processing |
| `autoprefixer` | `10.6.2` | Vendor prefixing |
| `monaco-editor` | `0.57.0` | In-browser coding & debugging assessments |
| `yjs` | `13.6.33` | CRDT collaborative editing engine |
| `y-websocket` | `3.1.0` | Real-time WebSocket provider for Yjs |
| `@playwright/test` | `1.65.0` | End-to-end integration & automated test runner |
| `@axe-core/playwright` | `4.14.0` | WCAG 2.2 AA automated accessibility testing |
| `jest` | `30.5.2` | Frontend unit testing harness |

---

## 3. Backend: Python 3.11+ Stack (Verified 2026-11-13 via PyPI & pip check)

| Package | Pinned Version | Purpose / Audit Status |
|---|---|---|
| `fastapi` | `0.162.5` | High-performance async web framework |
| `uvicorn` | `0.54.0` | ASGI server implementation |
| `pydantic` | `2.14.3` | Data validation & schema serialization |
| `pydantic-settings` | `2.16.2` | Type-safe environment configuration |
| `sqlalchemy` | `2.1.8` | Async SQL ORM & query builder |
| `alembic` | `1.20.1` | Schema migrations management |
| `asyncmy` | `0.2.18` | Single chosen async MySQL driver (InnoDB, utf8mb4) |
| `cryptography` | `50.0.2` | AES-256 field-level encryption for psychometrics |
| `argon2-cffi` | `25.1.0` | Single chosen Argon2id secure password hashing library |
| `pyjwt` | `2.15.1` | JWT token issuing, verification & rotation |
| `authlib` | `1.9.5` | Microsoft Entra ID OIDC integration client |
| `httpx` | `0.28.1` | Async HTTP client for NIM & integrations |
| `redis` | `8.1.0` | Caching, rate limiting, and pub/sub |
| `celery` | `5.7.0` | Distributed asynchronous task queue |
| `structlog` | `26.1.0` | JSON structured logging with correlation IDs |
| `numpy` | `2.5.4` | Numerical computing for item response theory |
| `scipy` | `1.18.1` | Psychometrics & statistical distributions |
| `statsmodels` | `0.15.0` | Differential item functioning (DIF) checks |
| `reportlab` | `5.1.0` | Growth Ring PDF generation engine |
| `pytest` | `9.2.0` | Backend test framework |
| `pytest-asyncio` | `1.5.0` | Asyncio test runner |
| `pytest-cov` | `7.1.0` | Test coverage reporting |
| `hypothesis` | `6.170.15` | Property-based testing |
| `testcontainers` | `4.15.0` | Ephemeral MySQL test containers |
| `ruff` | `0.17.5` | High-speed linting & formatting |
| `mypy` | `2.4.1` | Strict static type checking (`--strict`) |

---

## 4. Helper Services Architecture (Python Only)
All auxiliary services are strictly authored in Python:
- **Code Execution Sandbox**: Python daemon controlling unprivileged, network-isolated containers via Linux cgroups/namespaces with CPU (max 1 core) and memory limits (max 256MB).
- **Report Generation Worker**: Python worker using `reportlab` to render downloadable PDF Growth Ring reports with radar visualizations and data-table alternatives.
- **AI Gateway Worker**: Python service managing NVIDIA NIM client connections, retries, circuit breakers, rate limits, and audit trails.
