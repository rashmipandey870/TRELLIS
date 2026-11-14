"""TRELLIS Database Initialization & User Privileges Script.

Reads credentials from environment variables and applies explicit per-table immutability grants.
"""

import os
import sys
import pymysql


def get_required_env(var_name: str, default: str | None = None) -> str:
    val = os.getenv(var_name, default)
    if not val:
        print(f"Error: Environment variable '{var_name}' is required.", file=sys.stderr)
        sys.exit(1)
    return val


def main() -> None:
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    root_user = os.getenv("MYSQL_ROOT_USER", "root")
    root_password = get_required_env("MYSQL_ROOT_PASSWORD", "root_ci_test_password")

    db_name = os.getenv("TRELLIS_DB_NAME", "trellis_db")
    migrator_password = get_required_env("TRELLIS_MIGRATOR_PASSWORD", "trellis_migrator_pass_secure")
    app_password = get_required_env("TRELLIS_APP_PASSWORD", "trellis_app_pass_secure")

    print(f"Connecting to MySQL at {host}:{port} as {root_user}...")
    conn = pymysql.connect(
        host=host,
        port=port,
        user=root_user,
        password=root_password,
        autocommit=True,
    )

    with conn.cursor() as cur:
        # Create database
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
        )
        cur.execute(f"USE `{db_name}`;")

        # 1. Create migrator user
        cur.execute(
            "CREATE USER IF NOT EXISTS 'trellis_migrator'@'%' IDENTIFIED BY %s;",
            (migrator_password,),
        )
        cur.execute(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO 'trellis_migrator'@'%';")

        # 2. Create app user
        cur.execute(
            "CREATE USER IF NOT EXISTS 'trellis_app'@'%' IDENTIFIED BY %s;",
            (app_password,),
        )

        # 3. Explicit per-table mutable grants (reconciled with Base.metadata.tables)
        mutable_tables = [
            "organisations",
            "users",
            "roles",
            "grants",
            "employment_records",
            "consents",
            "refresh_tokens",
            "skills",
            "skill_levels",
            "skill_edges",
            "role_requirements",
            "evidence_records",
        ]
        for tbl in mutable_tables:
            cur.execute(
                f"GRANT SELECT, INSERT, UPDATE, DELETE ON `{db_name}`.`{tbl}` TO 'trellis_app'@'%';"
            )

        # 4. Explicit per-table immutable grants (ONLY SELECT and INSERT; NEVER UPDATE/DELETE)
        immutable_tables = [
            "audit_log",
            "access_receipts",
            "evidence_ledger",
            "ledger_checkpoints",
        ]
        for tbl in immutable_tables:
            cur.execute(
                f"GRANT SELECT, INSERT ON `{db_name}`.`{tbl}` TO 'trellis_app'@'%';"
            )

        cur.execute("FLUSH PRIVILEGES;")
        print("Database users and explicit per-table immutability grants successfully configured.")

    conn.close()


if __name__ == "__main__":
    main()
