# TRELLIS - Learning & Knowledge (L&K) Platform
*Enterprise Learning & Knowledge Portal for CSM Technology*

TRELLIS is an enterprise-grade learning, assessment, and talent development platform built for **CSM Technology**. It features role-governed portals, proctored assessments, a LeetCode-style sandboxed coding environment, and an AI practice lab with continuous dedication scoring and Talent Spotlight alerts.

---

## 🏛️ Stack & Monorepo Architecture

- **Backend**: FastAPI + SQLAlchemy 2.0 + Pydantic v2 + JWT (Short expiry + refresh) + Argon2 password hashing.
- **Frontend**: Angular 22 standalone components with Signals, Tailwind CSS, CSM Technologies Design System (Saffron `#FAA634`, Signal Red `#D7182A`, Cerulean `#008FBB`, Graphite `#333132`, Montserrat font, 14px cut-corner cards, -21.7° skewed bars).
- **Database**: Multi-database ready (SQL Server enterprise standard / MySQL 8.4+ / SQLite test harness).
- **Execution Engine**: Subprocess and container-isolated `CodeRunner` sandbox supporting Python 3, JavaScript (Node), Java 21, C++ 20, and C 17 with strict CPU, memory, and timeout constraints.
- **AI Innovations**: LLM-backed practice question generation pre-verified by sandbox execution, progressive hints, mistake & complexity feedback, and role-guarded enterprise assistant.

```
trellis/
  frontend/          # Angular standalone components with Signals, Tailwind CSS
    src/app/
      core/          # AuthService, guards (authGuard, roleGuard), typed domain services
      features/
        auth/        # Role-aware login with one-click persona autofill
        admin/       # Dashboard, User Management, Batches, Learner Directory, Settings
        mentor/      # Dashboard, Conflict-checked Meeting Scheduler, Assessments, Spotlight
        learner/     # Dashboard, Meetings & .ics, Timed Tests, Coding Lab, AI Practice
      shared/        # CSM Header with Role Tone Rail, Role-Guarded AI Assistant
  backend/           # FastAPI backend with strict role dependencies and UoW enforcement
    app/
      api/v1/        # Routers: auth, admin, mentor, learner, coding, practice, notifications
      core/          # Argon2 hashing, JWT rotation, database sessions, permissions
      models/        # 44 SQLAlchemy 2.0 domain entities
      services/      # CodeRunner sandbox, PracticeService, AuthService
  scripts/           # Master seed script (seed_trellis_data.py), DB user initialization
  docker/            # Production Dockerfiles for backend and frontend
  docker-compose.yml # Containerized stack (MSSQL, MySQL, Redis, FastAPI, Celery, Frontend)
  AUDIT.md           # Comprehensive codebase audit and remediation ledger
  DECISIONS.md       # Architectural Decision Records (ADR-01 through ADR-05)
```

---

## 🔐 Strict Role & Permission Matrix (Exactly 3 Roles)

| Capability / Resource | ADMIN (Governance & Oversight) | MENTOR (Curriculum & Learning) | LEARNER (Self-Paced Excellence) |
|---|:---:|:---:|:---:|
| **User & Cohort Management** | **Full** (Create, edit, deactivate, CSV import, assign) | Denied | Denied |
| **Learner Visibility** | **All Learners** (read-only performance dossier) | **Assigned Batches Only** | **Own Data Only** |
| **Meeting Scheduling** | Read-Only | **Create, reschedule, cancel, attendance** | View, join, download `.ics` |
| **Assessment Authoring** | Read-Only | **Create, version, publish, question bank** | Take timed proctored tests |
| **Coding Environment** | Read-Only Submissions | Author problems & test cases | Run, submit, view verdicts |
| **Talent Spotlight** | Department-wide oversight & threshold config | **Triage & 1-click action on alerts** | Practice & build streak |

---

## 🚀 Quick Start & Running Locally

### 1. Backend Setup (Python 3.11 - 3.14)
```powershell
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run deterministic master seed script (Seeds Admin, 2 Mentors, 6 Learners, Batches, Tests)
python ../scripts/seed_trellis_data.py

# Launch FastAPI development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Setup (Angular 22)
```powershell
# Navigate to frontend directory
cd frontend

# Install packages
npm install

# Build production bundle
npm run build

# Start development server
npm start
```
The application will be live at `http://localhost:4200` with the proxy forwarding `/api` calls to `http://localhost:8000`.

### 3. Docker Compose Stack
```bash
# Run with MySQL default
docker-compose up --build

# Or run with SQL Server profile
docker-compose --profile mssql up --build
```

---

## 🔑 Pre-Seeded Demonstration Personas

All personas are seeded with the password: `CSMTrellis2026!`

| Role | Email | Name & Designation | Default Landing |
|---|---|---|---|
| **ADMIN** | `admin@csmtech.internal` | Rajesh Mohanty (L&K Admin) | `/admin` |
| **MENTOR** | `mentor1@csmtech.internal` | Ananya Rao (Lead Cloud Architect) | `/mentor` |
| **MENTOR** | `mentor2@csmtech.internal` | Vikram Patel (Principal Systems Engineer) | `/mentor` |
| **LEARNER** | `learner1@csmtech.internal` | Priya Sharma (Batch Alpha, 14d Streak) | `/learner` |
| **LEARNER** | `learner3@csmtech.internal` | Sneha Mukherjee (Batch Alpha, 19d Streak) | `/learner` |

*(One-click persona buttons are also available on the Login screen and header for rapid inspection).*

---

## 🧪 Verification & Test Suite

Run the full test suite verifying route Unit-of-Work declarations, database grants, Argon2 password verification, role boundaries, and sandboxed code execution:
```powershell
pytest -v
```
All **88 tests** pass cleanly with 0 failures.
