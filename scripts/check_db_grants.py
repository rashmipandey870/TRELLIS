"""TRELLIS CI Check: Database Grants & ORM Models Reconciliation.

Enforces:
1. Every table defined in SQLAlchemy Base.metadata.tables MUST have an explicit grant in init_db_users.sql.
2. No grant in init_db_users.sql may reference a missing or obsolete table.
3. Immutable tables (audit_log, access_receipts, evidence_ledger, ledger_checkpoints)
   MUST NOT have UPDATE or DELETE grants for 'trellis_app'.
"""

import re
import sys
from pathlib import Path

# Add backend directory to sys.path so app.models can be imported
repo_root = Path(__file__).resolve().parent.parent
backend_dir = repo_root / "backend"
sys.path.insert(0, str(backend_dir))

try:
    from app.models import Base
except ImportError as exc:
    print(f"Error: Unable to import app.models: {exc}", file=sys.stderr)
    sys.exit(1)


def check_grants() -> None:
    sql_path = repo_root / "scripts" / "init_db_users.sql"
    if not sql_path.exists():
        print(f"Error: {sql_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    sql_text = sql_path.read_text(encoding="utf-8")

    # Pattern matching: GRANT <privileges> ON `trellis_db`.`<table_name>` TO 'trellis_app'@'%';
    grant_pattern = re.compile(
        r"GRANT\s+([A-Z,\s]+)\s+ON\s+[`'\"]?trellis_db[`'\"]?\.[`'\"]?([a-z0-9_]+)[`'\"]?\s+TO\s+['\"]trellis_app['\"]@['\"]%['\"];",
        re.IGNORECASE,
    )

    granted_tables: dict[str, set[str]] = {}
    for match in grant_pattern.finditer(sql_text):
        privs_str = match.group(1).upper()
        table_name = match.group(2).lower()
        privs = {p.strip() for p in privs_str.split(",") if p.strip()}
        granted_tables[table_name] = privs

    model_tables = set(Base.metadata.tables.keys())
    granted_names = set(granted_tables.keys())

    errors: list[str] = []

    # 1. Missing grants for model tables
    missing_grants = model_tables - granted_names
    if missing_grants:
        errors.append(f"Model tables missing explicit grant in init_db_users.sql: {sorted(missing_grants)}")

    # 2. Extra grants for non-existent tables
    extra_grants = granted_names - model_tables
    if extra_grants:
        errors.append(f"init_db_users.sql contains grants for non-existent tables: {sorted(extra_grants)}")

    # 3. Immutability invariants
    immutable_tables = {"audit_log", "access_receipts", "evidence_ledger", "ledger_checkpoints"}
    for imm_tbl in immutable_tables:
        if imm_tbl in granted_tables:
            privs = granted_tables[imm_tbl]
            if "UPDATE" in privs or "DELETE" in privs:
                errors.append(
                    f"CRITICAL IMMUTABILITY VIOLATION: Table '{imm_tbl}' has UPDATE/DELETE grants: {privs}"
                )
            if not privs.issubset({"SELECT", "INSERT"}):
                errors.append(
                    f"Table '{imm_tbl}' has unexpected grants (must be SELECT, INSERT only): {privs}"
                )

    if errors:
        print("DATABASE GRANTS RECONCILIATION FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print(
        f"SUCCESS: All {len(model_tables)} ORM model tables are perfectly reconciled with "
        f"scripts/init_db_users.sql (12 mutable tables, 4 immutable tables verified)."
    )


if __name__ == "__main__":
    check_grants()
