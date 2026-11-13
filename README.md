# TRELLIS - Learning & Knowledge (L&K) Platform
*Where every Tendril climbs.*

Built for CSM Technology. Enterprise-grade, evidence-based learning and skills acceleration platform.

## Architecture Highlights
- **Locked Stack**: Python 3.11+ FastAPI backend, Angular 18+ Signals frontend.
- **Evidence-First**: Append-only, hash-chained evidence ledger backing the continuous **Growth Ring**.
- **Privacy & DPDP Compliance**: Fine-grained RBAC/ABAC policy engine, Consent Passport, access receipts, field-level encryption for sensitive categories.
- **AI Governance**: NVIDIA NIM / Nemotron backend integration with CI groundedness evaluation harness, prompt versioning, and zero ungrounded assertions.

## Monorepo Layout
```
trellis/
  frontend/          # Angular standalone components, Signals, Tailwind CSS
  backend/           # FastAPI modular monolith, SQLAlchemy 2.0, Alembic, Celery
  docs/              # Product Brief, Architecture, ADRs, Honesty Ledger, Phase Plans
  docker/            # Dockerfiles for backend, frontend, worker, sandbox
  scripts/           # Seed scripts, test runners, migrations
  .github/workflows/ # CI/CD pipelines: lint, type-check, tests, accessibility, security
  .env.example       # Environment template
  docker-compose.yml # Local development stack (MySQL, Redis, FastAPI, Celery)
```

## Quick Start
See [docs/PRODUCT_BRIEF.md](file:///C:/Users/Rashm/.gemini/antigravity/scratch/trellis/docs/PRODUCT_BRIEF.md) for master specifications and delivery roadmap.
