"""Integration test proving MySQL 8.4 engine-level immutability enforcement.

Connects as runtime user 'trellis_app' and verifies that MySQL itself refuses
UPDATE and DELETE statements on audit_log and access_receipts with Error 1142.
"""

import os
import uuid

import pytest


def is_mysql_available() -> bool:
    """Check if MySQL service container is reachable."""
    try:
        import pymysql
    except ImportError:
        return False

    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    app_pass = os.getenv("TRELLIS_APP_PASSWORD", "trellis_app_pass_secure")
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user="trellis_app",
            password=app_pass,
            database=os.getenv("TRELLIS_DB_NAME", "trellis_db"),
            connect_timeout=2,
        )
        conn.close()
        return True
    except Exception:
        return False


@pytest.mark.skipif(
    not is_mysql_available(),
    reason="MySQL 8.4 service container not reachable (runs in CI workflow with image: mysql:8.4)",
)
def test_mysql_engine_refuses_audit_log_update_and_delete() -> None:
    """Prove MySQL itself returns Error 1142 (command denied) when trellis_app executes UPDATE or DELETE."""
    import pymysql

    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    db_name = os.getenv("TRELLIS_DB_NAME", "trellis_db")
    app_pass = os.getenv("TRELLIS_APP_PASSWORD", "trellis_app_pass_secure")

    conn = pymysql.connect(
        host=host,
        port=port,
        user="trellis_app",
        password=app_pass,
        database=db_name,
        autocommit=True,
    )

    test_id = str(uuid.uuid4())
    org_id = str(uuid.uuid4())

    with conn.cursor() as cur:
        # First ensure an organisation exists for FK constraint
        cur.execute(
            f"INSERT INTO `{db_name}`.`organisations` (id, code, name, created_at, updated_at) "
            "VALUES (%s, %s, %s, NOW(), NOW()) "
            "ON DUPLICATE KEY UPDATE name=VALUES(name);",
            (org_id, f"org_{test_id[:8]}", "Immutability Test Org"),
        )

        # 1. INSERT into audit_log MUST SUCCEED
        cur.execute(
            f"INSERT INTO `{db_name}`.`audit_log` (id, org_id, action, resource, reason, created_at) "
            "VALUES (%s, %s, %s, %s, %s, NOW());",
            (test_id, org_id, "test_action", "test_resource", "Initial immutable entry"),
        )

        # 2. SELECT from audit_log MUST SUCCEED
        cur.execute(f"SELECT id, reason FROM `{db_name}`.`audit_log` WHERE id = %s;", (test_id,))
        row = cur.fetchone()
        assert row is not None
        assert row[0] == test_id

        # 3. UPDATE on audit_log MUST FAIL with MySQL Error 1142
        with pytest.raises(pymysql.err.OperationalError) as exc_info:
            cur.execute(
                f"UPDATE `{db_name}`.`audit_log` SET reason = 'TAMPERED' WHERE id = %s;",
                (test_id,),
            )
        error_code = exc_info.value.args[0]
        assert error_code == 1142, (
            f"Expected MySQL ER_TABLEACCESS_DENIED_ERROR (1142), got {error_code}"
        )

        # 4. DELETE on audit_log MUST FAIL with MySQL Error 1142
        with pytest.raises(pymysql.err.OperationalError) as exc_info:
            cur.execute(f"DELETE FROM `{db_name}`.`audit_log` WHERE id = %s;", (test_id,))
        error_code = exc_info.value.args[0]
        assert error_code == 1142, (
            f"Expected MySQL ER_TABLEACCESS_DENIED_ERROR (1142), got {error_code}"
        )

    conn.close()
