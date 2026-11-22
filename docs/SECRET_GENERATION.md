# TRELLIS Cryptographic Key & Secret Generation Guide

This guide details how to generate secure, cryptographically random keys and secrets for production deployments of TRELLIS.

---

## 1. Required Production Environment Variables

| Variable | Description | Recommended Generation Command |
| :--- | :--- | :--- |
| `SECRET_KEY` | Master application secret for session signatures and HMAC | `python -c "import secrets; print(secrets.token_hex(32))"` |
| `FIELD_ENCRYPTION_KEY` | AES-256 Fernet base64 key for encrypting sensitive fields at rest | `python -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"` |
| `LEDGER_SALT_KEY` | Hex salt for evidence ledger DPDP pseudonymisation | `python -c "import secrets; print(secrets.token_hex(16))"` |
| `DATABASE_URL` | Neon/Postgres async connection string | Provided by database administrator |
| `DATABASE_MIGRATION_URL` | Neon/Postgres sync connection string for Alembic | Provided by database administrator |

---

## 2. Invariant Enforcement
- In production (`TRELLIS_ENV != dev`), the application **fails fast on startup** if any of `SECRET_KEY`, `FIELD_ENCRYPTION_KEY`, `LEDGER_SALT_KEY`, or `DATABASE_URL` are missing.
- In `docker-compose.yml`, the syntax `${VAR:?Error: VAR required}` causes container startup to abort immediately if secrets are not set in the host environment.
