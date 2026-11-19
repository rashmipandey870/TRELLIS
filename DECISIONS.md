# Architectural Decisions & Rationales (DECISIONS.md)
**Project**: TRELLIS - L&K Portal for CSM Technology  

## Decision Log

### ADR-01: Exactly Three Roles Architecture (ADMIN, MENTOR, LEARNER)
- **Context**: The existing prototype contained a complex 12-role matrix (`EMPLOYEE`, `TRAINER_MENTOR`, `MANAGER`, `LK_ADMIN`, `SUPER_ADMIN`, etc.), which was over-engineered and did not align with the product requirements.
- **Decision**: Collapse roles into exactly three: `ADMIN`, `MENTOR`, and `LEARNER`.
  - `ADMIN`: Platform administration, batch assignment, user lifecycle, department-wide analytics, read-only on meetings/assessments.
  - `MENTOR`: Learning management, meeting scheduling, assessment authoring, assigned learner grading/reviews, Talent Spotlight triage.
  - `LEARNER`: Self-service portal, taking assigned assessments, attending meetings, coding sandbox, AI practice.
- **Enforcement**: Dependency-based FastAPI guards (`require_role("ADMIN")`, `require_role("MENTOR")`, `require_role("LEARNER")`) and relationship-scoped checks (`require_mentor_of_learner`).

### ADR-02: Multi-Database Support (SQL Server & SQLite for Fast In-Memory Tests)
- **Context**: Production database target is SQL Server, while local testing and rapid unit tests run on SQLite/In-Memory.
- **Decision**: Configure SQLAlchemy engine dynamically via `DATABASE_URL`. Support both SQL Server (via `mssql+aioodbc` or `mssql+pyodbc`) and SQLite (`sqlite+aiosqlite` / `sqlite`) with compatible column types (e.g. JSON as text or native JSON where supported).

### ADR-03: Sandboxed Code Execution Service Interface
- **Context**: User-submitted code (Python, Java, JavaScript, C++, C) must never execute within the API process.
- **Decision**: Implement a decoupled `CodeRunner` service interface with an isolated subprocess-based runner configured with strict resource limits (non-root execution, timeout limits, memory constraints, and process isolation) with compatibility for Judge0 or Docker-based workers.

### ADR-04: LLM Practice Generation & Verification Loop
- **Context**: LLM-generated questions must never be unverified or broken.
- **Decision**: Use Anthropic Claude / OpenAI / Mock provider interface with strict JSON schema outputs. For coding problems, validate by executing the reference solution against all generated test cases inside the `CodeRunner` sandbox before saving or presenting to learners. If verification fails, automatically discard and regenerate.

### ADR-05: CSM Technologies Design Tokens (Tone System)
- **Context**: Visual design must match CSM Technologies brand language (Saffron, Signal Red, Cerulean, Graphite) with a light theme default.
- **Decision**: Implement a single CSS variables system (`tokens.scss` / `tokens.css`) defining the tri-colour spectrum, 14px cut corner cards, skewed slanted bars (-21.7deg), and role tones (`data-tone="learner"` for cerulean, `"mentor"` for saffron, `"admin"` for signal red).
