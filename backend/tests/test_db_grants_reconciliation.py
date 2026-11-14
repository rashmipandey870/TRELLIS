"""TRELLIS Test Suite: Database Grants Reconciliation."""

import subprocess
import sys
from pathlib import Path


def test_db_grants_script_passes_cleanly() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    check_script = repo_root / "scripts" / "check_db_grants.py"
    res = subprocess.run([sys.executable, str(check_script)], capture_output=True, text=True)
    assert res.returncode == 0, (
        f"check_db_grants failed:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}"
    )
    assert "All 16 ORM model tables are perfectly reconciled" in res.stdout


def test_db_grants_invariants() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    sql_path = repo_root / "scripts" / "init_db_users.sql"
    sql_text = sql_path.read_text(encoding="utf-8")

    # Assert obsolete table is gone
    assert "skill_evidence_links" not in sql_text

    # Assert newly reconciled tables are present
    assert "evidence_records" in sql_text
    assert "skill_levels" in sql_text
    assert "role_requirements" in sql_text

    # Assert immutability on sensitive tables
    for imm_table in ["audit_log", "access_receipts", "evidence_ledger", "ledger_checkpoints"]:
        assert f"GRANT SELECT, INSERT ON `trellis_db`.`{imm_table}`" in sql_text
        grant_line = [
            line
            for line in sql_text.splitlines()
            if imm_table in line and not line.strip().startswith("--")
        ][0]
        assert "UPDATE" not in grant_line
        assert "DELETE" not in grant_line
