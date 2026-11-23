"""TRELLIS Enterprise Release Gate Verification Script.

Comprehensive cross-platform verification suite:
1. Clean Database Migrations & Enterprise Demo Seed
2. Demo Data Integrity Verification (record thresholds across all key models)
3. Seed Idempotency Verification (test_seed_idempotency.py)
4. Content Quality & Uniqueness Gate (test_content_quality.py)
5. Psychometric Flow & Consent Gate (test_psychometric_flow.py)
6. Frontend Cleanliness & Light Theme Gate (test_frontend_cleanliness_and_light_theme.py)
7. Coding Pack Judge Harness Gate (verify_coding_pack.py)
8. Full Backend Pytest Suite
9. Frontend Production Build (npm run build cross-platform)
10. Generates comprehensive RELEASE_REPORT.html with verifiable audit evidence.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path


def run_step(step_name: str, cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> tuple[bool, str, float]:
    print(f"\n=======================================================")
    print(f"▶ RUNNING: {step_name}")
    print(f"  Command: {' '.join(str(c) for c in cmd)}")
    print(f"=======================================================")
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )
        duration = time.time() - start
        output = proc.stdout + ("\nSTDERR:\n" + proc.stderr if proc.stderr else "")
        success = (proc.returncode == 0)
        status_str = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status_str} in {duration:.2f}s")
        if not success:
            print(f"Error summary: {output[-500:]}")
        return success, output, duration
    except Exception as exc:
        duration = time.time() - start
        print(f"❌ ERROR: {exc}")
        return False, str(exc), duration


def check_data_integrity(db_path: Path) -> tuple[bool, str]:
    import sqlite3
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        tables = [
            ("users", 40),
            ("question_bank", 300),
            ("coding_problems", 20),
            ("assessments", 10),
            ("assessment_attempts", 150),
            ("submissions", 400),
            ("practice_attempts", 600),
            ("meetings", 18),
            ("notifications", 150),
            ("ai_question_pool", 24),
        ]
        
        report = []
        all_ok = True
        for table, min_expected in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            cnt = cursor.fetchone()[0]
            status = "PASS" if cnt >= min_expected else "FAIL"
            if cnt < min_expected:
                all_ok = False
            report.append(f"  • {table:<22}: {cnt:>5} records (min required: {min_expected:>4}) [{status}]")
        
        conn.close()
        summary = "\n".join(report)
        return all_ok, summary
    except Exception as e:
        return False, f"Data integrity query error: {e}"


def main():
    repo_root = Path(__file__).resolve().parent.parent
    backend_dir = repo_root / "backend"
    frontend_dir = repo_root / "frontend"
    python_exe = sys.executable

    print(f"🚀 TRELLIS Enterprise Release Gate Initiated")
    print(f"  Repository Root: {repo_root}")
    print(f"  Python Binary:   {python_exe}")
    print(f"  Platform:        {sys.platform}")
    print(f"  Timestamp:       {datetime.now(UTC).isoformat()}\n")

    report_entries = []
    all_passed = True

    # 1. Clean Database Migrations & Enterprise Demo Seed
    temp_db = repo_root / "release_gate_test.db"
    if temp_db.exists():
        temp_db.unlink()

    env_overrides = os.environ.copy()
    env_overrides["DATABASE_URL"] = f"sqlite:///{temp_db.as_posix()}"

    seed_cmd = [python_exe, "scripts/seed_demo_pack.py"]
    ok, out, dur = run_step("Clean DB Baseline & Enterprise Demo Seed", seed_cmd, cwd=repo_root, env=env_overrides)
    report_entries.append(("Clean DB Baseline & Enterprise Demo Seed", ok, dur, out))
    if not ok: all_passed = False

    # 2. Data Integrity Checks
    ok_int, out_int = check_data_integrity(temp_db)
    report_entries.append(("Demo Data Integrity Verification", ok_int, 0.05, out_int))
    print(f"{'✅ PASSED' if ok_int else '❌ FAILED'} Data Integrity Verification:\n{out_int}")
    if not ok_int: all_passed = False

    # 3. Frontend Cleanliness & Light Theme Gate
    clean_cmd = [python_exe, "-m", "pytest", "tests/test_frontend_cleanliness_and_light_theme.py", "-v"]
    ok, out, dur = run_step("Frontend Cleanliness & Light Theme Gate", clean_cmd, cwd=backend_dir)
    report_entries.append(("Frontend Cleanliness & Light Theme Gate", ok, dur, out))
    if not ok: all_passed = False

    # 4. Content Quality & Policy Coverage Gate
    content_cmd = [python_exe, "-m", "pytest", "tests/test_content_quality.py", "-v"]
    ok, out, dur = run_step("Content Quality & Policy Coverage Gate", content_cmd, cwd=backend_dir)
    report_entries.append(("Content Quality & Policy Coverage Gate", ok, dur, out))
    if not ok: all_passed = False

    # 5. Psychometric Flow Gate
    psych_cmd = [python_exe, "-m", "pytest", "tests/test_psychometric_flow.py", "-v"]
    ok, out, dur = run_step("Psychometric Flow & Consent Gate", psych_cmd, cwd=backend_dir)
    report_entries.append(("Psychometric Flow & Consent Gate", ok, dur, out))
    if not ok: all_passed = False

    # 6. Seed Idempotency Gate
    idemp_cmd = [python_exe, "-m", "pytest", "tests/test_seed_idempotency.py", "-v"]
    ok, out, dur = run_step("Seed Idempotency Gate", idemp_cmd, cwd=backend_dir)
    report_entries.append(("Seed Idempotency Gate", ok, dur, out))
    if not ok: all_passed = False

    # 7. Coding Pack Verification Gate
    verify_pack_cmd = [python_exe, "scripts/verify_coding_pack.py"]
    ok, out, dur = run_step("Coding Pack Judge Harness Gate", verify_pack_cmd, cwd=repo_root)
    report_entries.append(("Coding Pack Verification Gate", ok, dur, out))
    if not ok: all_passed = False

    # 8. Answer-Key Distribution & Psychometric Likert Tests
    dist_cmd = [python_exe, "-m", "pytest", "tests/test_answer_key_distribution.py", "-v"]
    ok, out, dur = run_step("Answer-Key Distribution & Likert Tests", dist_cmd, cwd=backend_dir)
    report_entries.append(("Answer-Key Distribution & Likert Tests", ok, dur, out))
    if not ok: all_passed = False

    # 9. Full Backend Portable Pytest Suite
    full_pytest_cmd = [python_exe, "-m", "pytest", "-v"]
    ok, out, dur = run_step("Full Backend Pytest Suite", full_pytest_cmd, cwd=backend_dir)
    report_entries.append(("Full Backend Pytest Suite", ok, dur, out))
    if not ok: all_passed = False

    # 10. Frontend Production Build (Cross-platform npm execution)
    npm_bin = shutil.which("npm.cmd" if sys.platform == "win32" else "npm") or "npm"
    build_cmd = [npm_bin, "run", "build"]
    ok, out, dur = run_step("Frontend Production Build (Angular 22)", build_cmd, cwd=frontend_dir)
    report_entries.append(("Frontend Production Build (Angular 22)", ok, dur, out))
    if not ok: all_passed = False

    # Clean up test database
    if temp_db.exists():
        try:
            temp_db.unlink()
        except Exception:
            pass

    # 11. Generate RELEASE_REPORT.html
    report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>TRELLIS Enterprise Release Verification Report</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; }}
    .container {{ max-width: 1000px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 2rem; border: 1px solid #334155; }}
    h1 {{ color: #008FBB; margin-top: 0; }}
    .badge-pass {{ background: #065f46; color: #34d399; padding: 4px 8px; border-radius: 6px; font-weight: bold; }}
    .badge-fail {{ background: #881337; color: #fb7185; padding: 4px 8px; border-radius: 6px; font-weight: bold; }}
    .summary-box {{ background: #0f172a; padding: 1rem; border-radius: 8px; margin: 1.5rem 0; border: 1px solid #334155; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
    th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #334155; }}
    th {{ background: #0f172a; color: #94a3b8; }}
    pre {{ background: #0f172a; padding: 12px; border-radius: 6px; overflow-x: auto; font-size: 12px; color: #cbd5e1; max-height: 300px; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>🌱 TRELLIS Enterprise Release Verification Report</h1>
    <p>Official Verification Gate for CSM Technologies Learning &amp; Knowledge Portal</p>
    
    <div class="summary-box">
      <strong>Overall Status:</strong> 
      <span class="{'badge-pass' if all_passed else 'badge-fail'}">{'100% RELEASE READY (ALL GATES PASSED)' if all_passed else 'RELEASE GATES FAILED'}</span><br>
      <strong>Executed At:</strong> {datetime.now(UTC).isoformat()}<br>
      <strong>Target Repository:</strong> rashmipandey870/TRELLIS
    </div>

    <h2>Verification Stages</h2>
    <table>
      <thead>
        <tr>
          <th>Verification Gate</th>
          <th>Status</th>
          <th>Duration</th>
        </tr>
      </thead>
      <tbody>
"""
    for name, ok, dur, out in report_entries:
        badge = '<span class="badge-pass">PASSED</span>' if ok else '<span class="badge-fail">FAILED</span>'
        report_html += f"""
        <tr>
          <td><strong>{name}</strong></td>
          <td>{badge}</td>
          <td>{dur:.2f}s</td>
        </tr>
        <tr>
          <td colspan="3"><details><summary style="cursor:pointer; color:#008FBB;">View Execution Output</summary><pre>{out[-2000:] if len(out) > 2000 else out}</pre></details></td>
        </tr>
"""
    report_html += """
      </tbody>
    </table>
  </div>
</body>
</html>
"""
    report_path = repo_root / "RELEASE_REPORT.html"
    report_path.write_text(report_html, encoding="utf-8")
    print(f"\n📊 Release Gate Report saved to: {report_path}")

    if all_passed:
        print("\n🎉 ALL RELEASE GATES PASSED! TRELLIS is manager-ready for production deployment.")
        sys.exit(0)
    else:
        print("\n❌ SOME RELEASE GATES FAILED. Review output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
