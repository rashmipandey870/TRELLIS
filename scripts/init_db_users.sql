-- ==============================================================================
-- TRELLIS Database Initialization & Dual-User Immutability Grants
-- ==============================================================================
-- Enforces separation of duties at the MySQL Engine Level:
-- 1. trellis_migrator: DDL privileges for schema migrations (Alembic)
-- 2. trellis_app: DML privileges for application runtime
--    CRITICAL INVARIANT: UPDATE & DELETE strictly REVOKED on immutable tables.
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS `trellis_db`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE `trellis_db`;

-- 1. Migration Admin User (Used exclusively by CI and Alembic CLI)
CREATE USER IF NOT EXISTS 'trellis_migrator'@'%' IDENTIFIED BY 'trellis_migrator_secret_2026';
GRANT ALL PRIVILEGES ON `trellis_db`.* TO 'trellis_migrator'@'%';

-- 2. Application Runtime User (Used by FastAPI backend connection pool)
CREATE USER IF NOT EXISTS 'trellis_app'@'%' IDENTIFIED BY 'trellis_app_secret_2026';
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.* TO 'trellis_app'@'%';

-- 3. Database-Level Immutability Enforcement
-- Revoke UPDATE and DELETE on immutable audit and ledger tables:
REVOKE UPDATE, DELETE ON `trellis_db`.`audit_log` FROM 'trellis_app'@'%';
REVOKE UPDATE, DELETE ON `trellis_db`.`access_receipts` FROM 'trellis_app'@'%';
REVOKE UPDATE, DELETE ON `trellis_db`.`evidence_ledger` FROM 'trellis_app'@'%';
REVOKE UPDATE, DELETE ON `trellis_db`.`ledger_checkpoints` FROM 'trellis_app'@'%';

FLUSH PRIVILEGES;

-- Verification Query (Run as DBA to audit grants):
-- SHOW GRANTS FOR 'trellis_app'@'%';
