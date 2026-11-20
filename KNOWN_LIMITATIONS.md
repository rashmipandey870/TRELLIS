# TRELLIS - Known Limitations & Implementation Status

**Repository**: `rashmipandey870/TRELLIS`  
**Stack**: FastAPI + SQLAlchemy (Backend), Angular 22 (Frontend), Docker Compose  
**Roles Supported**: Strictly 3 canonical enterprise roles (`ADMIN`, `MENTOR`, `LEARNER`)

---

## 1. Code Execution & Sandboxing
- **Production Mode (`TRELLIS_ENV != dev`)**: The backend strictly refuses to start if no isolated code runner is configured. Supported isolated runners are `Judge0Runner` (via self-hosted Judge0 instance) and `DockerRunner` (`docker run --network none --memory 256m --cpus 1.0 --read-only --pids-limit 64`).
- **Development Mode (`TRELLIS_ENV = dev`)**: `LocalSubprocessRunner` runs locally in isolated temporary directories with an empty environment (`env={}`) and CPU/memory/process limits via `resource.setrlimit`.
- **Supported Languages**: Python 3, Node.js (JavaScript), Java 21, and GCC/G++ (C/C++).
- **Simulated Execution**: Simulated or fake passes have been completely removed. Missing compilers or runtime errors return real internal/runner unavailable errors, never an ACCEPTED verdict.

## 2. Assessment Engine & Integrity
- **Audience Enforcement**: Only learners belonging to an assessment's assigned batch or explicit audience table (`AssessmentAudience`) can access, start, autosave, or submit assessments.
- **Server-Side Timer**: Server-side start timestamps and durations are strictly enforced. Submissions after expiration are rejected with 400 and flagged as `EXPIRED`.
- **Coding Question Grading**: Assessments grade coding problems automatically by executing stored submissions against test cases and weighting by marks.
- **Zero Mock Data**: Endpoints return `[]` when no assessments or results exist; hardcoded fallback records (`a1`, `res1`, `qb_1`) have been eliminated.

## 3. Mentor & Meeting Validation
- **Meeting Links**: Link URLs are strictly validated using `urllib.parse` for `https://` schemes and must match allow-listed meeting hosts (`teams.microsoft.com`, `meet.google.com`, `zoom.us`, `*.csm.tech`).
- **Schedule & Conflict Detection**: Start and end times are validated (`end_time > start_time`, not in past), and schedule conflict detection flags overlapping sessions for the mentor or any learner in the audience.
- **Attendance**: Marking attendance is strictly restricted to learners who were assigned to the meeting's audience.

## 4. AI Practice Lab & LLM Assistant
- **Configurable Model**: Configurable Claude model (`claude-3-5-sonnet-20241022`) with strict Pydantic schemas, 45s timeouts, and retry logic.
- **Source Transparency**: Every question is labeled as `source: "llm"` or `source: "template"`, displayed as badges in the UI.
- **Multi-Language Generation**: Coding problems generate language-specific solutions (Java, JavaScript, Python, SQL) and are verified in the sandbox before presentation.
- **Answer Concealment**: Explanations and correct answers are excluded from the `/generate` endpoint and returned only upon `/submit`.
- **Rate Limiting**: In-memory rate limits enforce a maximum of 20 practice generations and 30 assistant queries per user per hour.
- **Role-Guarded Assistant**: Server-side role context ensures Learners can only inspect their own progress, Mentors inspect assigned cohorts, and Admins inspect aggregate platform metrics.

## 5. Frontend & Monaco Integration
- **Monaco Editor**: Integrated into both `learner-coding` and `learner-practice` with custom CSM Light and Dark themes, font size selector, reset to starter code, and syntax highlighting across 5 languages.
- **Auth Interceptor**: 401 responses trigger a single `/auth/refresh` rotation with concurrent request queuing via `BehaviorSubject`. Sessions persist across page reloads via single-use refresh token rotation.
- **RFC 9457 Errors**: Problem details are parsed and surfaced via accessible toast notifications.
- **Empty States**: Friendly empty states render cleanly whenever backend endpoints return empty lists.

## 6. What Is Deferred / Not Implemented
- **Webcam Proctoring & Facial Recognition**: Not implemented; mock flags exist but no video pipeline is active.
- **Complex Psychometric Profiling**: Deferred to future enterprise releases.
- **Judge0 Hardware Clustering**: Judge0 runs as a standalone docker service in docker-compose, not a Kubernetes multi-node cluster.
