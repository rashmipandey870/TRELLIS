# TRELLIS Locked Technology Stack

## 1. Stack Invariants
As specified in Section 4 of the Master Brief, the stack is strictly locked:
- **Backend**: Python 3.11+ with FastAPI.
- **Frontend**: Angular 18+ with TypeScript (standalone components, Signals).
- **Hard Rule**: No Node.js/Express/NestJS, Django, Flask, React, Vue, or Next.js for product code. Node is permitted solely as Angular build tooling. All auxiliary services (code sandbox, report generator, bots, workers) must be written in Python.

## 2. Pinned Backend Stack (Python 3.11+)
- **API Framework**: FastAPI (`fastapi>=0.115.0`)
- **Validation**: Pydantic v2 (`pydantic>=2.9.0`, `pydantic-settings>=2.5.0`)
- **ASGI Server**: Uvicorn (`uvicorn[standard]>=0.31.0`)
- **ORM**: SQLAlchemy 2.0 (`sqlalchemy>=2.0.35`)
- **Database Driver**: `asyncmy>=0.2.9` / `aiomysql>=0.2.0` (MySQL 8+ InnoDB utf8mb4)
- **Migrations**: Alembic (`alembic>=1.13.3`)
- **Task Queue**: Celery (`celery>=5.4.0`) with Redis
- **Cache & Pub/Sub**: Redis (`redis>=5.1.0`)
- **HTTP Client**: HTTPX (`httpx>=0.27.2`)
- **Security & Cryptography**:
  - Argon2id password hashing: `pwdlib[argon2]>=0.2.0` / `argon2-cffi>=23.1.0`
  - JWT Tokens: `python-jose[cryptography]>=3.3.0` / `pyjwt>=2.9.0`
  - Field-level encryption: `cryptography>=43.0.1`
  - OIDC Auth: `authlib>=1.3.2`
- **Observability**: `structlog>=24.4.0`
- **Data Science & Psychometrics**: `numpy>=2.1.0`, `scipy>=1.14.0`, `statsmodels>=0.14.0`
- **Report Generation**: `reportlab>=4.2.5` / `weasyprint>=62.0`
- **Testing & Quality**:
  - `pytest>=8.3.0`, `pytest-asyncio>=0.24.0`, `pytest-cov>=5.0.0`
  - Property testing: `hypothesis>=6.112.0`
  - Integration DB: `testcontainers[mysql]>=4.8.0`
  - Linter & Formatter: `ruff>=0.6.9`
  - Strict type checking: `mypy>=1.11.2`

## 3. Pinned Frontend Stack (Angular)
- **Framework**: Angular 18+ / 19 (`@angular/core`, `@angular/common`, `@angular/router`, `@angular/forms`)
- **Architecture**: Standalone components, Signals (`signal`, `computed`, `effect`), lazy-loaded routes
- **Styling**: Tailwind CSS (`tailwindcss>=3.4.0`)
- **Accessibility**: Angular CDK A11y (`@angular/cdk/a11y`)
- **Code Editor**: Monaco Editor (`@monaco-editor` / `ngx-monaco-editor-v2`)
- **Collaborative Editing**: Yjs (`yjs`, `y-websocket`)
- **Testing**:
  - Unit tests: Jest / Vitest
  - E2E & Accessibility: Playwright (`@playwright/test`), `@axe-core/playwright`

## 4. Code Execution Sandbox Service
- Standalone Python service communicating over isolated gRPC / internal HTTP, executing untrusted candidate code in ephemeral, unprivileged Linux containers with seccomp/apparmor profiles, CPU/memory quotas, and zero network access.
