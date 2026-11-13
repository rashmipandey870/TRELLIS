# TRELLIS Locked Technology Stack

## 1. Stack Invariants & Hard Rules (Master Brief Section 4)
- **Backend**: Python 3.11+ with FastAPI.
- **Frontend**: Angular 19 (TypeScript, standalone components, Signals).
- **Hard Rule**: Do not introduce Node.js/Express/NestJS, Django, Flask, React, Vue, or Next.js for any product code. Node is allowed only as Angular's build tooling. Every helper service (code sandbox, report renderer, bot, workers) is also written in Python.
- **Dependency Pinning**: Every dependency is pinned to an exact version (no ranges, no `^`, no `>=`).

---

## 2. Frontend: Angular 19 Stack (Exact Pinned Versions)

| Package | Pinned Version | Purpose |
|---|---|---|
| `@angular/core` | `19.0.0` | Core framework with Signals reactivity |
| `@angular/common` | `19.0.0` | Common directives, pipes, HTTP client |
| `@angular/router` | `19.0.0` | Lazy-loaded standalone routing |
| `@angular/forms` | `19.0.0` | Reactive forms & typed validation |
| `@angular/cdk` | `19.0.0` | Accessible headless UI primitives & A11y live announcer |
| `@angular/compiler` | `19.0.0` | Angular compiler |
| `@angular/platform-browser` | `19.0.0` | Browser platform & DOM abstraction |
| `@angular/platform-browser-dynamic` | `19.0.0` | Dynamic compilation |
| `@angular/cli` | `19.0.0` | Build orchestration (dev dependency) |
| `@angular-devkit/build-angular` | `19.0.0` | Esbuild-based application builder |
| `typescript` | `5.6.3` | TypeScript compiler |
| `rxjs` | `7.8.1` | Reactive extensions |
| `zone.js` | `0.15.0` | Zone execution context |
| `tailwindcss` | `3.4.14` | Utility-first design tokens & layout |
| `postcss` | `8.4.47` | CSS post-processing |
| `autoprefixer` | `10.4.20` | Vendor prefixing |
| `monaco-editor` | `0.52.0` | In-browser coding & debugging assessments |
| `yjs` | `13.6.20` | CRDT collaborative editing engine |
| `y-websocket` | `2.0.4` | Real-time WebSocket provider for Yjs |
| `@playwright/test` | `1.48.2` | End-to-end integration & automated test runner |
| `@axe-core/playwright` | `4.10.0` | WCAG 2.2 AA automated accessibility testing |
| `jest` | `29.7.0` | Frontend unit testing harness |

---

## 3. Backend: Python 3.11+ Stack (Exact Pinned Versions)

| Package | Pinned Version | Purpose |
|---|---|---|
| `fastapi` | `0.115.5` | High-performance async web framework |
| `uvicorn` | `0.32.0` | ASGI server implementation |
| `pydantic` | `2.9.2` | Data validation & schema serialization |
| `pydantic-settings` | `2.6.1` | Type-safe environment configuration |
| `sqlalchemy` | `2.0.36` | Async SQL ORM & query builder |
| `alembic` | `1.14.0` | Schema migrations management |
| `asyncmy` | `0.2.9` | High-speed async MySQL driver (InnoDB, utf8mb4) |
| `aiomysql` | `0.2.0` | Secondary async MySQL connection driver |
| `cryptography` | `43.0.3` | AES-256 field-level encryption for psychometrics |
| `argon2-cffi` | `23.1.0` | Argon2id secure password hashing |
| `pwdlib` | `0.2.1` | Modern password hashing adapter |
| `pyjwt` | `2.9.0` | JWT token issuing, verification & rotation |
| `authlib` | `1.3.2` | Microsoft Entra ID OIDC integration client |
| `httpx` | `0.27.2` | Async HTTP client for NIM & integrations |
| `redis` | `5.2.0` | Caching, rate limiting, and pub/sub |
| `celery` | `5.4.0` | Distributed asynchronous task queue |
| `structlog` | `24.4.0` | JSON structured logging with correlation IDs |
| `numpy` | `2.1.3` | Numerical computing for item response theory |
| `scipy` | `1.14.1` | Psychometrics & statistical distributions |
| `statsmodels` | `0.14.4` | Differential item functioning (DIF) checks |
| `reportlab` | `4.2.5` | Growth Ring PDF generation engine |
| `pytest` | `8.3.3` | Backend test framework |
| `pytest-asyncio` | `0.24.0` | Asyncio test runner |
| `pytest-cov` | `6.0.0` | Test coverage reporting |
| `hypothesis` | `6.119.2` | Property-based testing |
| `testcontainers` | `4.8.2` | Ephemeral MySQL test containers |
| `ruff` | `0.7.3` | High-speed linting & formatting |
| `mypy` | `1.13.0` | Strict static type checking (`--strict`) |

---

## 4. Helper Services Architecture (Python Only)
All auxiliary services are strictly authored in Python:
- **Code Execution Sandbox**: Python daemon controlling unprivileged, network-isolated containers via Linux cgroups/namespaces with CPU (max 1 core) and memory limits (max 256MB).
- **Report Generation Worker**: Python worker using `reportlab` to render downloadable PDF Growth Ring reports with radar visualizations and data-table alternatives.
- **AI Gateway Worker**: Python service managing NVIDIA NIM client connections, retries, circuit breakers, rate limits, and audit trails.
