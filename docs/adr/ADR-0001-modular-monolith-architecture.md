# ADR-0001: Modular Monolith Architecture (Python 3.11+ FastAPI + Angular 22)

## Status
Accepted

## Context
TRELLIS is the unified enterprise Learning & Knowledge (L&K) platform for CSM Technology, encompassing 10 core functional modules, high-security assessments, real-time collaboration, and AI coaching. As mandated by Section 4 and Section 21 of the Master Prompt, the stack is strictly locked: Python 3.11+ FastAPI on the backend and Angular 22 (Signals, standalone components) on the frontend. We needed to choose between a microservices architecture and a modular monolith.

## Decision
We adopt a **Modular Monolith** architecture:
- **Single Deployable FastAPI Service**: Structured into strict, isolated bounded contexts (`identity`, `access`, `skills`, `pathways`, `assessments`, `growth_ring`, `sessions`, `greenhouse`, `grove`, `gardener`, `knowledge`, `analytics`, `audit`).
- **No Cross-Context Table Access**: Bounded contexts interact strictly through service layer interfaces and domain events.
- **Worker & Sandbox Separation**: Heavy background jobs (PDF rendering, AI evaluations) run in Celery workers; untrusted candidate code runs in a separate, isolated Python sandbox daemon with zero network access.
- **Frontend Architecture**: Angular 22 with standalone components, native Signals for fine-grained reactivity, lazy-loaded routes, Tailwind CSS 4, and Monaco Editor.

## Consequences
### Positive
- High developer velocity and simplified deployment without the operational overhead, network latency, and distributed transaction complexity of microservices.
- Enforces modular boundaries that allow clean future extraction into microservices if scaling demands require it.
- Strict type safety with Python `mypy --strict`, Pydantic v2 schemas, and TypeScript 7.

### Negative / Trade-offs
- Monolith requires strict code review discipline to prevent developers from bypassing service interfaces to make direct cross-context database joins.
- Single deployment artifact requires comprehensive CI test runs before releases.
