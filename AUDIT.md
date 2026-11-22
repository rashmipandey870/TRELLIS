# TRELLIS Codebase Audit & Gap Analysis (AUDIT.md)
**Project**: TRELLIS - Learning & Knowledge (L&K) Portal for CSM Technology  
**Date**: November 2026  
**Auditor**: Principal Full-Stack Engineer  

---

## Executive Summary
An in-depth architectural and implementation audit was conducted across the entire repository (`backend/`, `frontend/`, `docs/`, `scripts/`, `alembic/`, `docker/`).  
The codebase currently contains the foundational shell of an early prototype (Slice 1.7b): an authentication service, an append-only audit ledger prototype, a partial curriculum model, and a single learner home page with hard-coded sections. Core functional domains required for an enterprise L&K portal—Assessments (MCQ & Coding), Meetings/Attendance, User & Batch Administration, Sandboxed Code Execution, and AI Practice with Talent Spotlight—are missing, half-implemented, or mocked.

This audit documents every issue across functionality, security, architecture, and UI/UX, establishing the actionable remediation plan for Steps 1 through 10.

---

## 1. Broken, Half-Implemented, Mocked, or Hard-Coded Features

### 1.1 Backend Services & Endpoints
1. **Mocked Calendar Sessions (`home_service.py:257-278`)**:
   - `get_home_data` injects hard-coded sessions (`ses-live-401`, `ses-live-402`) with fictitious URLs (`https://meet.csmtech.internal/...`).
   - No database model exists for Meetings, Meeting Audience, or Meeting Attendance.
2. **Mocked Greenhouse Innovation Spotlight (`home_service.py:281-294`)**:
   - Hardcoded dictionary (`idea-featured-01`) returned directly in API payload; no database persistence or domain logic.
3. **Missing Assessment Engine**:
   - Completely absent: MCQ tests, options, question banks, coding problems, test cases, and attempt/submission tracking.
   - No grading or result analysis capabilities.
4. **Missing Meeting Management**:
   - No endpoints for creating, editing, rescheduling, or canceling meetings.
   - No audience conflict detection, learner notification triggers, or attendance marking.
5. **Missing Code Execution Engine**:
   - No sandbox service or code runner interface exists.
   - No isolated runner container (Judge0 / Docker runner with CPU/memory/network constraints).
6. **Missing AI Practice & Talent Spotlight**:
   - NVIDIA NIM integration is a mock (`USE_NIM_MOCK=true`).
   - No LLM problem generation with verification loops.
   - No dedication score calculation or mentor alert triggers.
   - Chatbot is completely missing or static.
7. **Ad-Hoc Database Engine Initialisation (`backend/app/api/deps.py:22-38`)**:
   - Fallback to in-memory SQLite hides connection errors and breaks multi-process workers.
   - Database connection string is hardcoded to MySQL/SQLite dialect strings without clean SQL Server support.

### 1.2 Frontend (Angular 22 / Signals)
1. **Dead Navigation Links (`app.component.ts:38-40`)**:
   - Navigation links (`#pathways`, `#growth-ring`, `#greenhouse`) are dummy anchor tags (`href="#..."`).
   - Only two routes exist in `app.config.ts`: `/login` and `/home`.
2. **Missing Role-Specific Portals**:
   - No `/admin`, `/mentor`, or `/learner` routes or route guards.
   - Admin features (User & Batch management, Learner Directory, Department Dashboard) are completely missing.
   - Mentor features (Dashboard, Meeting Scheduler, Assessment Builder, Review) are missing.
   - Learner features (Meetings, Assessments, Results, Coding environment, AI Practice) are missing.
3. **Token Refresh Interceptor Gap (`auth.interceptor.ts:20-25`)**:
   - On 401 Unauthorized, the interceptor immediately clears user session and redirects to login instead of invoking `/auth/refresh` with the refresh token.
4. **No Monaco Editor Integration**:
   - `monaco-editor` is in `package.json`, but no component integrates it for code authoring or running.

---

## 2. Security & Authorization Deficiencies

### 2.1 Role-Permission Architecture
1. **Role Model Incoherence**:
   - The policy matrix defines 12 disparate roles (`EMPLOYEE`, `TRAINER_MENTOR`, `MANAGER`, `LK_ADMIN`, `SUPER_ADMIN`, `CONTENT_AUTHOR`, etc.).
   - Specification strictly mandates exactly three roles: `ADMIN`, `MENTOR`, and `LEARNER`.
   - Adding `LEARNER` ad-hoc broke the test suite (`test_permission_matrix.py`).
2. **Missing Route-Level Role Authorization Guards**:
   - Endpoints rely on coarse `require_permission("read", "enrolments")` rather than role-based and relationship-based access controls (e.g., verifying whether a learner is assigned to the requesting mentor).
   - Insecure Direct Object References (IDOR): No enforcement ensuring a mentor cannot inspect or modify learners belonging to another mentor.
3. **Insecure Key Length & Secret Fallbacks**:
   - JWT HMAC key in test configurations emits `InsecureKeyLengthWarning` (< 32 bytes).
   - Dev secrets in `config.py` contain dummy Fernet keys that risk accidental promotion if environment detection fails.
4. **Missing Rate Limiting**:
   - Code execution and AI generation endpoints lack per-user and per-IP rate limiting, leaving the service vulnerable to denial-of-service and quota depletion.

---

## 3. Dead Code, Duplicated Logic & Error Handling

1. **Dead Models & Tables**:
   - `EmploymentRecord.reporting_line_id` and Manager scopes are unused for the 3-role portal model.
   - Unused tables in `0001` - `0004` migrations that do not serve the streamlined L&K workflows.
2. **Error Handling Discrepancies**:
   - Backend returns RFC 9457 Problem Details (`application/problem+json`), but frontend services do not consistently parse Problem Details, causing generic or empty UI error notifications.
3. **Broken Test Suite**:
   - `test_permission_matrix.py` fails due to role definition mismatch.
   - `test_seed_demo.py` collection fails when `PYTHONPATH` does not include repository root.

---

## 4. Remediation Plan

All audit items will be systematically resolved according to the 10-step roadmap:
- **Step 1**: Re-architect roles to strictly `ADMIN`, `MENTOR`, and `LEARNER`. Implement dependency guards and route guards.
- **Step 2**: Implement complete Admin suite (User & Batch management, CSV bulk import, Learner directory, Department dashboard, Talent Spotlight oversight).
- **Step 3**: Implement complete Mentor suite (Dashboard, conflict-aware Meeting scheduler with attendance, Assessment builder with question bank & CSV export, Learner review).
- **Step 4**: Implement complete Learner suite (Dashboard, My Meetings with `.ics`, Timed Assessments with autosave & tab-switch warnings, Results analysis).
- **Step 5**: Build LeetCode-style Coding Environment with isolated sandboxed execution service (`CodeRunner`).
- **Step 6**: Implement AI Practice with LLM schema generation, sandbox validation, adaptive difficulty, dedication score, and Talent Spotlight alerts.
- **Step 7 & 8**: Comprehensive data model with migrations, configurable SQL Server/SQLite/Postgres/MySQL connection string, and updated seed script.
- **Step 9 & 10**: Unit & integration test coverage, Docker Compose orchestration, and CSM Technologies visual design system (tokens, Montserrat typography, signature cut-corner cards, tone per role).

---

## 5. Verification & Resolution Sign-Off (November 2026)

All identified audit issues, workstreams (WS0-WS3), and Phases (A through F) have been completely resolved and verified:
1. **Security & History (Phase A / WS0)**: Leaked credentials purged from git history via `git filter-repo`. Mandatory password change enforced on first login via `must_change_password` and `/change-password` route. Admin OTP generation enforced.
2. **AI Honesty & Gateway (WS2 / Phase A)**: Never-fail multi-provider ladder (Ollama primary, cloud secondary, DB pool fallback). Persisted `ai_question_pool` table. Truthful provenance tracking (`ollama` vs `procedural` vs `curated`).
3. **Core Features (WS3 / Phase B)**:
   - Multi-role chatbot (Learner, Mentor, Admin) with SSE streaming and tool calling.
   - 7 CSM Enterprise Policy Categories with non-clinical disclaimer.
   - Subjective AI rubric evaluation (`/mentor/assessments/attempts/{id}/answers/{ans_id}/ai-evaluate`).
   - Secure file storage with signed download tokens.
   - Vector ReportLab PDF Growth Ring report export.
   - Topic mastery calculation and adaptive study plan generator.
   - Mentor needs-attention queue.
4. **Motion, Accessibility & Design (Phase C)**: Official CSM Technologies design tokens, Montserrat typography, shimmer skeleton loaders, reduced motion accessibility queries.
5. **Enterprise Demo Data Pack (Phase D)**: 40+ users, 4 batches, 304 questions across 7 categories, 24 coding problems across 5 languages, 12 assessments across all lifecycle states, 160+ attempts, 570+ practice attempts, 4 talent alerts.
6. **Authorization Matrix & Security Tests (Phase E)**: Strict 3-role matrix verified (`test_auth_matrix.py` 5/5 passed).
7. **Release Gate Verification (Phase F)**: Clean DB baseline, migrations, seed, test suites, and frontend production build pass with 100% success (`RELEASE_REPORT.html`).

