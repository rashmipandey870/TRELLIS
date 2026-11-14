-- ==============================================================================
-- TRELLIS Database Initialization & Dual-User Per-Table Immutability Grants
-- ==============================================================================
-- Enforces separation of duties at the MySQL Engine Level:
-- 1. trellis_migrator: DDL privileges for schema migrations (Alembic)
-- 2. trellis_app: Explicit per-table DML privileges for application runtime
--    CRITICAL INVARIANT: ONLY SELECT and INSERT are granted on immutable tables.
--    UPDATE and DELETE are NEVER granted on audit_log, access_receipts,
--    evidence_ledger, or ledger_checkpoints.
--
-- Secrets are parameterized via environment variables:
--   TRELLIS_DB_NAME (default: trellis_db)
--   TRELLIS_MIGRATOR_PASSWORD
--   TRELLIS_APP_PASSWORD
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS `trellis_db`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE `trellis_db`;

-- 1. Migration Admin User (Used exclusively by CI and Alembic CLI)
-- Password populated from TRELLIS_MIGRATOR_PASSWORD environment variable
CREATE USER IF NOT EXISTS 'trellis_migrator'@'%' IDENTIFIED BY '${TRELLIS_MIGRATOR_PASSWORD}';
GRANT ALL PRIVILEGES ON `trellis_db`.* TO 'trellis_migrator'@'%';

-- 2. Application Runtime User (Used by FastAPI backend connection pool)
-- Password populated from TRELLIS_APP_PASSWORD environment variable
CREATE USER IF NOT EXISTS 'trellis_app'@'%' IDENTIFIED BY '${TRELLIS_APP_PASSWORD}';

-- 3. Explicit Per-Table Grants on Mutable Tables (SELECT, INSERT, UPDATE, DELETE)
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.`organisations` TO 'trellis_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.`users` TO 'trellis_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.`roles` TO 'trellis_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.`grants` TO 'trellis_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.`employment_records` TO 'trellis_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.`consents` TO 'trellis_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.`refresh_tokens` TO 'trellis_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.`skills` TO 'trellis_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.`skill_edges` TO 'trellis_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `trellis_db`.`skill_evidence_links` TO 'trellis_app'@'%';

-- 4. Explicit Per-Table Grants on IMMUTABLE Tables (ONLY SELECT and INSERT; NEVER UPDATE/DELETE)
GRANT SELECT, INSERT ON `trellis_db`.`audit_log` TO 'trellis_app'@'%';
GRANT SELECT, INSERT ON `trellis_db`.`access_receipts` TO 'trellis_app'@'%';
GRANT SELECT, INSERT ON `trellis_db`.`evidence_ledger` TO 'trellis_app'@'%';
GRANT SELECT, INSERT ON `trellis_db`.`ledger_checkpoints` TO 'trellis_app'@'%';

FLUSH PRIVILEGES;

-- Verification Query:
-- SHOW GRANTS FOR 'trellis_app'@'%';
