# CLAUDE.md - TRELLIS Master Build Instructions

See [docs/PRODUCT_BRIEF.md](file:///C:/Users/Rashm/.gemini/antigravity/scratch/trellis/docs/PRODUCT_BRIEF.md) for full brief and requirements.

## Stack & Hard Invariants
- Backend: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, MySQL 8+ (InnoDB, utf8mb4) via asyncmy/aiomysql, Redis, Celery + Redis.
- Frontend: Angular + TypeScript (standalone components, Signals, Reactive Forms, Tailwind CSS).
- STRICT RULE: Do not introduce Node/Express/NestJS/React/Vue/Next/Django/Flask for product code. Python backend only, Angular frontend only.
- Strict authorization on backend (Policy Engine `can(subject, action, resource, context)`).
- Append-only, hash-chained Evidence Ledger for the Growth Ring.
- Real MySQL data & migrations; Synthetic demo data gated by `TRELLIS_ENV=demo`.
- Maintain `docs/HONESTY_LEDGER.md` and `docs/KNOWN_LIMITATIONS.md`.
