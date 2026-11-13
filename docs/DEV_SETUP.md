# TRELLIS Local Development & Environment Setup Guide

This guide details the exact prerequisites, toolchains, and environment configuration required to run, develop, and test TRELLIS locally, including live MySQL 8.4 and Redis 7.4 integration tests.

---

## 1. System Prerequisites & Installation

To run the complete TRELLIS test suite and application locally, your machine requires:
1. **Node.js 24.15.0 LTS** (Strictly required for Angular 22 CLI compatibility).
2. **Python 3.11+** (FastAPI backend engine).
3. **Database & Cache Infrastructure** (Either Docker Desktop with WSL2 OR Native Windows Services).

### A. Node.js Toolchain (Node 24.15.0 LTS)
Angular CLI 22.2.7 requires Node engine `^22.22.3 || ^24.15.0 || >=26.0.0`. If your local machine runs Node 25.x (or Node 20.x), npm will emit engine warning notices.

**Recommended Setup using NVM for Windows:**
```powershell
# 1. Install NVM for Windows (if not already installed)
winget install CoreyButler.NVMforWindows

# 2. Install and activate Node 24.15.0 LTS
nvm install 24.15.0
nvm use 24.15.0

# 3. Verify Node and npm versions
node -v   # Expected: v24.15.0
npm -v    # Expected: 10.8.2 or later
```

---

### B. Database & Cache Engine (MySQL 8.4 + Redis 7.4)

You can choose between **Option 1 (Recommended: Docker Desktop)** or **Option 2 (Native Windows Services)**.

#### Option 1: Docker Desktop with WSL2 (Recommended)
This provides isolated, production-identical MySQL 8.4 and Redis 7.4 containers without polluting your host system.

1. **Install Docker Desktop**:
   ```powershell
   winget install Docker.DockerDesktop
   ```
2. **Start Docker Desktop**:
   Launch Docker Desktop from your Start menu and ensure the engine status shows **Running** with WSL2 integration enabled (`Settings > General > Use the WSL 2 based engine`).
3. **Verify CLI**:
   ```powershell
   docker --version
   docker compose version
   ```
4. **Start Background Database Services**:
   ```powershell
   # From the project root
   docker compose up -d mysql redis
   ```
   *Note*: In `docker-compose.yml`, MySQL 8.4 and Redis are isolated to an internal bridge network to prevent unauthorized external network exposure. Ports `3306` and `6379` are bound to `127.0.0.1` only for local testing.

---

#### Option 2: Native Windows Services (Without Docker)
If Docker Desktop cannot be installed on your workstation, install native Windows services:

1. **MySQL 8.4 Community Server**:
   ```powershell
   winget install Oracle.MySQL
   ```
   - Complete the configuration wizard.
   - Set the root password (e.g., `trellis_root_dev_secret_2026`).
   - Ensure the MySQL service is running: `Get-Service MySQL84`
   - Create the development database and user permissions in MySQL:
     ```sql
     CREATE DATABASE trellis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

     -- Migrator User (Full DDL rights for Alembic migrations)
     CREATE USER 'trellis_migrator'@'localhost' IDENTIFIED BY 'trellis_migrator_secret_2026';
     GRANT ALL PRIVILEGES ON trellis_db.* TO 'trellis_migrator'@'localhost';

     -- Application User (Restricted DML - Enforces Immutability at the DB User Level)
     CREATE USER 'trellis_app'@'localhost' IDENTIFIED BY 'trellis_app_secret_2026';
     GRANT SELECT, INSERT, UPDATE, DELETE ON trellis_db.* TO 'trellis_app'@'localhost';
     -- Strictly revoke UPDATE and DELETE on immutable audit and ledger tables:
     REVOKE UPDATE, DELETE ON trellis_db.audit_log FROM 'trellis_app'@'localhost';
     REVOKE UPDATE, DELETE ON trellis_db.access_receipts FROM 'trellis_app'@'localhost';
     REVOKE UPDATE, DELETE ON trellis_db.evidence_ledger FROM 'trellis_app'@'localhost';
     FLUSH PRIVILEGES;
     ```

2. **Redis for Windows (or Memurai Developer Edition)**:
   ```powershell
   winget install Memurai.MemuraiDeveloper
   ```
   - Verify Redis/Memurai service is active on port `6379`:
     ```powershell
     Test-NetConnection -ComputerName 127.0.0.1 -Port 6379
     ```

---

## 2. Environment Configuration (`.env`)

1. Copy the template `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Verify local credentials match your active setup:
   ```ini
   TRELLIS_ENV=dev
   LOG_LEVEL=DEBUG

   # Database Connection Strings
   DATABASE_URL=mysql+asyncmy://trellis_app:trellis_app_secret_2026@127.0.0.1:3306/trellis_db
   DATABASE_MIGRATION_URL=mysql+asyncmy://trellis_migrator:trellis_migrator_secret_2026@127.0.0.1:3306/trellis_db

   # Redis
   REDIS_URL=redis://127.0.0.1:6379/0

   # JWT Asymmetric Keys (RS256 / Ed25519)
   JWT_ALGORITHM=RS256
   JWT_PRIVATE_KEY_PATH=secrets/jwt_private.pem
   JWT_PUBLIC_KEY_PATH=secrets/jwt_public.pem
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

   # Security & Privacy
   ARGON2_TIME_COST=3
   ARGON2_MEMORY_COST=65536
   ARGON2_PARALLELISM=4
   ```

3. Generate Local Asymmetric JWT Signing Keys:
   ```powershell
   mkdir -Force secrets
   openssl genrsa -out secrets/jwt_private.pem 4096
   openssl rsa -in secrets/jwt_private.pem -pubout -out secrets/jwt_public.pem
   ```

---

## 3. Backend Setup & Verification

1. **Create and Activate Python 3.11+ Virtual Environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Harden Tooling & Install Dependencies**:
   ```powershell
   python -m pip install --upgrade "pip>=26.2.0"
   pip install -r backend/requirements.txt -r backend/requirements-dev.txt
   ```

3. **Run Code Quality and Static Typing Checks**:
   ```powershell
   # Linting and formatting
   ruff check backend/
   ruff format --check backend/

   # Strict static typing
   mypy --strict backend/
   ```

4. **Apply Database Migrations (requires live MySQL 8.4)**:
   ```powershell
   alembic upgrade head
   ```

5. **Run Integration Test Suite**:
   ```powershell
   pytest backend/tests/ -v --cov=backend/app --cov-report=term-missing
   ```

---

## 4. Frontend Setup & Verification

1. **Install Pinned Dependencies**:
   ```powershell
   cd frontend
   npm ci
   ```

2. **Verify Clean Dependency Audit (DOMPurify Override)**:
   ```powershell
   npm audit
   # Expected output: 0 critical vulnerabilities (DOMPurify 3.4.17 enforced)
   ```

3. **Compile & Typecheck Angular 22 Application**:
   ```powershell
   npm run build -- --configuration=production
   ```

4. **Run Unit & Automated Axe-Core Accessibility Tests**:
   ```powershell
   npm test
   npm run test:axe
   ```

---

## 5. Status in Honesty Ledger

Until Docker Desktop or native MySQL 8.4 is provisioned and started on your workstation:
- **`ENV-001` (Docker Execution)** and **`ENV-005` (Live MySQL Integration Tests)** remain logged as **`Unverified`** in `docs/HONESTY_LEDGER.md`.
- All mock, unit, policy engine matrix evaluation, cryptographic hash chaining, and static typing tests execute fully in memory.
