"""TRELLIS Database Initialization & User Privileges Script.

Reads credentials from environment variables and applies explicit per-table immutability grants.
Supports both PostgreSQL (CI/Production) and MySQL (Legacy/Dev).
"""

import os
import sys

MUTABLE_TABLES = [
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
    "pathways",
    "courses",
    "modules",
    "cohorts",
    "batches",
    "enrolments",
    "mentor_learner_assignments",
    "meetings",
    "meeting_audience",
    "meeting_attendance",
    "question_bank",
    "mcq_options",
    "coding_problems",
    "test_cases",
    "assessments",
    "assessment_audience",
    "assessment_questions",
    "assessment_attempts",
    "answers",
    "submissions",
    "mentor_remarks",
    "practice_sessions",
    "practice_questions",
    "practice_attempts",
    "practice_scores",
    "talent_alerts",
    "alert_actions",
    "notifications",
    "system_settings",
    "ai_question_pool",
    "learner_stats",
    "assessment_stats",
    "batch_stats",
    "topic_mastery",
    "assessment_notes",
]

IMMUTABLE_TABLES = [
    "audit_log",
    "access_receipts",
    "evidence_ledger",
    "ledger_checkpoints",
]


def get_required_env(var_name: str, default: str | None = None) -> str:
    val = os.getenv(var_name, default)
    if not val:
        print(f"Error: Environment variable '{var_name}' is required.", file=sys.stderr)
        sys.exit(1)
    return val


def init_postgres(host: str, port: int, root_user: str, root_password: str, db_name: str, migrator_password: str, app_password: str) -> None:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    print(f"Connecting to PostgreSQL at {host}:{port} as {root_user}...")
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=root_user,
        password=root_password,
        dbname="postgres",
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as cur:
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE "{db_name}";')
            print(f"Created database {db_name}")
    conn.close()

    # Connect to target database
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=root_user,
        password=root_password,
        dbname=db_name,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as cur:
        # 1. Migrator user
        cur.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'trellis_migrator') THEN
                    CREATE ROLE trellis_migrator WITH LOGIN PASSWORD %s;
                ELSE
                    ALTER ROLE trellis_migrator WITH LOGIN PASSWORD %s;
                END IF;
            END $$;
            """,
            (migrator_password, migrator_password),
        )
        cur.execute('GRANT ALL PRIVILEGES ON SCHEMA public TO trellis_migrator;')

        # 2. App user
        cur.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'trellis_app') THEN
                    CREATE ROLE trellis_app WITH LOGIN PASSWORD %s;
                ELSE
                    ALTER ROLE trellis_app WITH LOGIN PASSWORD %s;
                END IF;
            END $$;
            """,
            (app_password, app_password),
        )
        cur.execute('GRANT USAGE ON SCHEMA public TO trellis_app;')
        cur.execute('GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO trellis_app;')
        cur.execute('ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO trellis_app;')

        # 3. Explicit per-table mutable grants
        for tbl in MUTABLE_TABLES:
            try:
                cur.execute(f'GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE "{tbl}" TO trellis_app;')
            except psycopg2.Error:
                # Table may not yet be created if running before alembic
                pass

        # 4. Explicit per-table immutable grants (ONLY SELECT, INSERT)
        for tbl in IMMUTABLE_TABLES:
            try:
                cur.execute(f'GRANT SELECT, INSERT ON TABLE "{tbl}" TO trellis_app;')
            except psycopg2.Error:
                pass

    conn.close()
    print("PostgreSQL users and explicit per-table immutability grants successfully configured.")


def init_mysql(host: str, port: int, root_user: str, root_password: str, db_name: str, migrator_password: str, app_password: str) -> None:
    import pymysql

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

        # 3. Explicit per-table mutable grants
        for tbl in MUTABLE_TABLES:
            cur.execute(
                f"GRANT SELECT, INSERT, UPDATE, DELETE ON `{db_name}`.`{tbl}` TO 'trellis_app'@'%';"
            )

        # 4. Explicit per-table immutable grants (ONLY SELECT and INSERT; NEVER UPDATE/DELETE)
        for tbl in IMMUTABLE_TABLES:
            cur.execute(
                f"GRANT SELECT, INSERT ON `{db_name}`.`{tbl}` TO 'trellis_app'@'%';"
            )

        cur.execute("FLUSH PRIVILEGES;")
        print("MySQL database users and explicit per-table immutability grants successfully configured.")

    conn.close()


def main() -> None:
    is_postgres = (
        bool(os.getenv("PGHOST"))
        or bool(os.getenv("POSTGRES_USER"))
        or "postgres" in os.getenv("DATABASE_MIGRATION_URL", "").lower()
        or "postgres" in os.getenv("DATABASE_URL", "").lower()
    )

    db_name = os.getenv("TRELLIS_DB_NAME", "trellis_db")
    migrator_password = get_required_env("TRELLIS_MIGRATOR_PASSWORD", "trellis_migrator_pass_secure")
    app_password = get_required_env("TRELLIS_APP_PASSWORD", "trellis_app_pass_secure")

    if is_postgres:
        host = os.getenv("PGHOST", os.getenv("POSTGRES_HOST", "127.0.0.1"))
        port = int(os.getenv("PGPORT", os.getenv("POSTGRES_PORT", "5432")))
        root_user = os.getenv("PGUSER", os.getenv("POSTGRES_USER", "postgres"))
        root_password = get_required_env("PGPASSWORD", os.getenv("POSTGRES_PASSWORD", "root_ci_test_password"))
        init_postgres(host, port, root_user, root_password, db_name, migrator_password, app_password)
    else:
        host = os.getenv("MYSQL_HOST", "127.0.0.1")
        port = int(os.getenv("MYSQL_PORT", "3306"))
        root_user = os.getenv("MYSQL_ROOT_USER", "root")
        root_password = get_required_env("MYSQL_ROOT_PASSWORD", "root_ci_test_password")
        init_mysql(host, port, root_user, root_password, db_name, migrator_password, app_password)


if __name__ == "__main__":
    main()
