# TRELLIS Quality Assurance Strategy, Test Harness & Performance Budgets

## 1. Testing Pyramid & Verification Gates (Master Prompt Section 19)

```
        / \
       /   \        E2E Tests (Playwright + Axe-Core A11y)
      / ----\       [Cross-browser user journeys, WCAG 2.2 AA]
     /       \      Contract & Integration Tests (Testcontainers MySQL)
    / --------\     [OpenAPI schema contracts, Policy Engine generated tests]
   /           \    Unit & Property Tests (Pytest, Hypothesis, Jest)
  /_____________\   [Hash-chaining, IRT models, ABAC logic, Signals state]
```

---

## 2. Test Layer Specifications

### Layer 1: Unit & Property-Based Tests
- **Backend (Pytest + Hypothesis)**:
  - Cryptographic hash-chaining verification (`RFC 8785` serialization stability under arbitrary dictionary key orders).
  - Item Response Theory 2PL mathematical scoring models.
  - Small-group k-anonymity masking algorithms (proves no sequence of filtered queries can isolate an individual when `n < 5`).
- **Frontend (Jest / Signals testing)**:
  - Reactive form validations, state transition effects, and keyboard event handlers.

### Layer 2: Automated Permission Tests (Generated from Matrix)
- A dedicated test generator parses [docs/security/PERMISSION_MATRIX.json](file:///C:/Users/Rashm/.gemini/antigravity/scratch/trellis/docs/security/PERMISSION_MATRIX.json) and programmatically generates test fixtures for every single `(role, resource, action, scope)` tuple.
- Proves that unauthorized roles receive `403 Forbidden` and that allowed actions succeed and emit an audit event.

### Layer 3: Integration & Contract Tests (Testcontainers)
- Spawns real, ephemeral MySQL 8.4 containers via `testcontainers-python` to verify:
  - Alembic forward migrations and clean reverse rollbacks on an empty database.
  - Foreign key cascades, unique constraints, and transaction rollback integrity.
  - OpenAPI specification contract validation against Pydantic response schemas.

### Layer 4: End-to-End & Accessibility Tests (Playwright)
- Automated browser testing across Chromium, Firefox, and WebKit:
  - Complete candidate onboarding flow, assessment submission, and Growth Ring generation.
  - Real-time Yjs collaborative editing in Greenhouse and Grove.
  - Zero violations on `@axe-core/playwright` accessibility audits across all pages.

---

## 3. Strict Performance Budgets

| Metric | Target Budget | Measurement Method | Failure Consequence |
|---|---|---|---|
| **API p95 Response Time** | $\le 300\text{ ms}$ | Dashboard reads & Growth Ring queries under normal load. | CI load-test regression gate fails PR. |
| **API p99 Response Time** | $\le 800\text{ ms}$ | Heavy complex queries (e.g. IRT parameter recalculation). | Alert flagged in Datadog/Prometheus. |
| **First Contentful Paint (FCP)** | $\le 2.0\text{ s}$ | Mobile viewport profile on throttled 4G network. | Lighthouse CI build fails. |
| **Largest Contentful Paint (LCP)**| $\le 2.5\text{ s}$ | Desktop and mobile client render. | Lighthouse CI build fails. |
| **Cumulative Layout Shift (CLS)** | $\le 0.1$ | Page rendering with dynamic skeleton loaders. | Lighthouse CI build fails. |
| **Concurrency Load Target** | $\ge 600\text{ concurrent users}$ | $2\times$ expected peak concurrency (assumed 300 concurrent). | Locust / k6 load script verification. |

---

## 4. Observability & SLO Targets
- **Availability SLO**: 99.9% uptime (excluding scheduled maintenance).
- **Error Budget**: $< 0.1\%$ non-client (5xx) responses over any rolling 30-day window.
- **Traceability**: 100% of API requests, Celery background tasks, and AI inferences carry a unified `X-Correlation-ID` logged in structured JSON format via `structlog`.
