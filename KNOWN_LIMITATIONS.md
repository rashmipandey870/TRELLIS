# TRELLIS - Known Limitations & Implementation Status

**Repository**: `rashmipandey870/TRELLIS`  
**Stack**: FastAPI + SQLAlchemy (Backend), Angular 22 (Frontend), Docker Compose  
**Roles Supported**: Strictly 3 canonical enterprise roles (`ADMIN`, `MENTOR`, `LEARNER`)

---

## 1. Code Execution & Sandboxing
- **Production Mode (`TRELLIS_ENV != dev`)**: The backend strictly refuses to start if no isolated code runner is configured. Supported isolated runners are `Judge0Runner` (via self-hosted Judge0 instance) and `DockerRunner` (`docker run --network none --memory 256m --cpus 1.0 --read-only --pids-limit 64`).
- **Runner Startup Self-Test & Queue Concurrency**: All runners implement `startup_self_test()`. An in-process concurrency limiter (`BoundedSemaphore(10)`) rejects excess runs with `QUEUE_LIMIT_EXCEEDED` to ensure background workers and API threads are never starved.
- **Development Mode (`TRELLIS_ENV = dev`)**: `LocalSubprocessRunner` runs locally in isolated temporary directories with an empty environment (`env={}`) and CPU/memory/process limits via `resource.setrlimit`.
- **Supported Languages**: Python 3, Node.js (JavaScript), Java 21, and GCC/G++ (C/C++).
- **Simulated Execution**: Simulated or fake passes have been completely removed. Missing compilers or runtime errors return real internal/runner unavailable errors, never an ACCEPTED verdict.

## 2. Platform Security & Integrity Controls (WS0)
- **Credential Hygiene & Secret Zero-Default**: Default database credentials (`DATABASE_URL`, `DATABASE_MIGRATION_URL`) have been completely purged from source configuration. The server fails fast on startup if `DATABASE_URL` is omitted. CI secret scanning (Gitleaks) and pre-commit hooks protect against accidental leaks.
- **Manual Grading Bounds & Override Audit**: Manual grade submissions (`POST /mentor/assessments/attempts/{id}/grade`) strictly enforce `0 <= score_awarded <= question marks` (HTTP 422 on out-of-bounds). Any modification or override of an auto-graded or previously recorded score requires a non-empty `override_reason` (HTTP 400 if missing) and logs an immutable `GRADE_OVERRIDE` record in the `AuditLog`.
- **Forced Password Change Lifecycle**: User creation and bulk user import generate unique cryptographically random one-time passwords (`secrets.token_urlsafe(12)`) and flag `must_change_password=True`. Users cannot access protected APIs until completing `POST /api/v1/auth/change-password` (enforced via 403 `MUST_CHANGE_PASSWORD` dependency guards). No shared default passwords exist anywhere in the application.

## 2. Assessment Engine & 7 Question Categories
- **Audience Enforcement**: Only learners belonging to an assessment's assigned batch or explicit audience table (`AssessmentAudience`) can access, start, autosave, or submit assessments.
- **Server-Side Timer**: Server-side start timestamps and durations are strictly enforced. Submissions after expiration are rejected with 400 and flagged as `EXPIRED`.
- **7 Question Types Supported**: Full schema, validation, runner, and UI support for:
  1. `MCQ` (Auto-graded single/multi-choice)
  2. `CODING` (Sandboxed runner with test cases, execution time, and memory metrics)
  3. `SQL` (In-memory SQLite isolated sandbox with custom DDL schemas, fixture seeding, and output row diffing)
  4. `SHORT_ANSWER` (Subjective written answers evaluated against mentor rubrics)
  5. `SCENARIO` (Case-study analysis with rubric-guided criteria)
  6. `COMMUNICATION` (Technical writing and architectural proposals)
  7. `FILE_UPLOAD` (Deliverable artifacts and documents verified via URL assets)
- **Hybrid Auto + Manual Grading**: MCQs and Code/SQL are evaluated instantly upon submission. Subjective categories are flagged as `PENDING_REVIEW` with scores updated dynamically through the Mentor Review & Grading Studio (`POST /mentor/assessments/attempts/{id}/grade`).
- **Zero Mock Data**: Endpoints return `[]` when no assessments or results exist; hardcoded fallback records (`a1`, `att_demo`, `res1`, `qb_1`, `ses-live-401`, `idea-featured-01`) have been completely eradicated. Empty states render with clean UI prompts.

## 3. AI Growth Ring Reports & Gardener Chatbot
- **Growth Ring Report Service**: Automatically synthesized on attempt submission and manual grade finalization via `generate_growth_ring_report()`. Computes proficiency across categories, cohort percentile rank, strengths, gap areas, and a concrete 3-step action roadmap.
- **Dynamic Radar Chart SVG**: Generates a self-contained multi-dimensional SVG radar chart mathematically projected via trigonometric polygon points with grid levels and branded accents (`#008FBB`, `#FAA634`).
- **Report Approval Lifecycle**: Reports transition through `NONE` -> `PENDING_APPROVAL` -> `APPROVED`. Mentors review and release reports using `POST /mentor/assessments/attempts/{id}/approve-report`. Learners can view their interactive dossier upon release.
- **Gardener AI Coach**: Personalized learning companion (`POST /learner/chatbot/chat`) grounded in the learner's enrolled pathway, milestone progress, daily practice streaks, and recent assessment performances with sliding-window rate limiting (30 requests/hour/user).

## 3. Mentor & Meeting Validation
- **Meeting Links**: Link URLs are strictly validated using `urllib.parse` for `https://` schemes and must match allow-listed meeting hosts (`teams.microsoft.com`, `meet.google.com`, `zoom.us`, `*.csm.tech`).
- **Schedule & Conflict Detection**: Start and end times are validated (`end_time > start_time`, not in past), and schedule conflict detection flags overlapping sessions for the mentor or any learner in the audience.
- **Attendance**: Marking attendance is strictly restricted to learners who were assigned to the meeting's audience.

## 4. AI Practice Lab & LLM Assistant (WS2 Complete)
- **TRELLIS AI Gateway Architecture**:
  - Unified multi-provider gateway (`app.ai`) supporting self-hosted Ollama (primary), Cloud API (OpenAI/Anthropic/Gemini compatible fallback), and deterministic procedural fallback engine.
  - Zero-fail ladder: Verified in-memory pool -> live LLM generation with quality gate verification -> procedural engine. Offline environments or LLM connection drops never surface 500 errors or fake static templates to learners.
  - Strict Quality Gates: MCQ 4-distinct-options verification; Coding/SQL sandbox pre-verification (reference solution must score 100% in isolated runner; wrong stub must fail at least one test case).
  - Language Fidelity: SQL problems execute against in-memory SQLite tables with proper SQL starter code; Java problems provide Java starter code; JavaScript problems provide Node-compatible starter code.
  - Socratic Gardener Chatbot: Grounded in real pathway progress, climbing streaks, and recent assessment results with 30 queries/hour/user rate limiting and PII redaction.
  - Admin AI Health Dashboard: Real-time telemetry (`p50`/`p95` latency, success rate, validation rate, pool counts), with manual Circuit Breaker trip/reset and pool refill controls.
- **Configurable Model**: Configurable Ollama/Cloud models (`AI_INSTRUCT_MODEL`, `AI_CODE_MODEL`) with strict Pydantic schemas, timeouts, and retry logic.
- **Source Transparency**: Every question is labeled with authentic provenance metadata (`served_from`: `pool` | `live` | `verified_fallback`), displayed as a "Generated by TRELLIS AI" badge in the UI.
- **Multi-Language Generation**: Coding problems generate language-specific solutions (Java, JavaScript, Python, SQL) and are verified in the sandbox before presentation.
- **Answer Concealment**: Explanations and correct answers are excluded from the `/generate` endpoint and returned only upon `/submit`.
- **Rate Limiting**: In-memory rate limits enforce a maximum of 20 practice generations and 30 assistant queries per user per hour.
- **Role-Guarded Assistant**: Server-side role context ensures Learners can only inspect their own progress, Mentors inspect assigned cohorts, and Admins inspect aggregate platform metrics.

## 5. Frontend & Monaco Integration
- **Monaco Editor**: Integrated into both `learner-coding` and `learner-practice` with custom CSM Light and Dark themes, font size selector, reset to starter code, and syntax highlighting across 5 languages.
- **Auth Interceptor**: 401 responses trigger a single `/auth/refresh` rotation with concurrent request queuing via `BehaviorSubject`. Sessions persist across page reloads via single-use refresh token rotation.

## 6. Database, Migration & Clean Clone Deployment (WS1)
- **Alembic Baseline & Clean Clone Execution**: `alembic upgrade head` executes with zero errors on empty databases across SQLite, PostgreSQL, and MySQL. Migration `0004b` provides the baseline for all 24 LMS, Assessment, Meeting, Practice, and platform entities with complete schema-vs-model drift verification in automated CI (`test_schema_model_drift_check`).
- **Neon Serverless PostgreSQL Support**: Native connection pooling (`pool_size=10`, `max_overflow=20`), `pool_recycle=300`, `pool_pre_ping=True`, SSL mode (`sslmode=require`), and retry warm-up backoff preventing scale-to-zero cold start dropouts.
- **Single-Command Docker Compose**: Complete compose stack orchestrates backend API, Angular frontend (Nginx reverse proxy), PostgreSQL 16, Redis 7.4, Celery worker, Judge0 runner, and Ollama model server with `.env.example`.
- **Deterministic & Idempotent Seeding**: `scripts/seed_trellis_data.py` seeds organizations, personas, cohorts, batches, meetings, assessments, 5 coding problems with test cases, assessment attempts with graded answers, practice sessions & attempts, and real Talent Spotlight alerts on day one without duplicates on repeated runs.
- **Cross-Platform Test Portability**: Full 153-test suite passes on Windows, Linux, and CI without asserting empty OS environments or failing on canonical role authorization.
- **RFC 9457 Errors**: Problem details are parsed and surfaced via accessible toast notifications.
- **Empty States**: Friendly empty states render cleanly whenever backend endpoints return empty lists.

## 6. What Is Deferred / Not Implemented
- **Webcam Proctoring & Facial Recognition**: Not implemented; mock flags exist but no video pipeline is active.
- **Complex Psychometric Profiling**: Deferred to future enterprise releases.
- **Judge0 Hardware Clustering**: Judge0 runs as a standalone docker service in docker-compose, not a Kubernetes multi-node cluster.
