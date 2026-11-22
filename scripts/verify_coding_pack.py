"""TRELLIS Coding Pack Verification Harness.

Runs every reference solution through the runner for every language against every test case.
Requires:
1. Reference solution must achieve ACCEPTED verdict (100% test cases pass).
2. Wrong stub must NOT achieve ACCEPTED verdict (at least one test case fails).
3. Prints raw evidence table with runtime and verdicts.
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

from app.services.code_runner import CodeRunner
from scripts.fixtures.coding_problems import CODING_PROBLEMS


def verify_all_coding_problems():
    print("=" * 80)
    print("TRELLIS CODING PACK VERIFICATION GATE")
    print("=" * 80)
    print(f"{'#':<3} {'Title':<40} {'Lang':<6} {'Cases':<6} {'Ref Verdict':<12} {'Stub Verdict':<12} {'Status'}")
    print("-" * 80)

    total = len(CODING_PROBLEMS)
    passed_count = 0
    skipped_count = 0
    failed_problems = []

    for idx, prob in enumerate(CODING_PROBLEMS, 1):
        title = prob["title"]
        lang = prob["language"]
        cases = prob["test_cases"]
        ref_sol = prob["reference_solution"]
        wrong_stub = prob.get("wrong_stub", "")
        entry_point = prob.get("entry_point")
        arg_schema = prob.get("argument_schema", [])

        # 1. Test reference solution
        t0 = time.perf_counter()
        ref_res = CodeRunner.execute(
            code=ref_sol,
            language=lang,
            test_cases=cases,
            time_limit_ms=prob.get("time_limit_ms", 3000),
            memory_limit_mb=prob.get("memory_limit_mb", 256),
            entry_point=entry_point,
            argument_schema=arg_schema,
        )
        t_ref = (time.perf_counter() - t0) * 1000

        # If compiler is unavailable on this host
        if ref_res.verdict == "RUNNER_UNAVAILABLE":
            print(f"{idx:<3} {title[:38]:<40} {lang:<6} {len(cases):<6} {'UNAVAIL':<12} {'UNAVAIL':<12} [SKIP - No Host Tool]")
            skipped_count += 1
            continue

        # 2. Test wrong stub
        stub_verdict = "N/A"
        if wrong_stub:
            stub_res = CodeRunner.execute(
                code=wrong_stub,
                language=lang,
                test_cases=cases,
                time_limit_ms=prob.get("time_limit_ms", 3000),
                memory_limit_mb=prob.get("memory_limit_mb", 256),
                entry_point=entry_point,
                argument_schema=arg_schema,
            )
            stub_verdict = stub_res.verdict or "NONE"

        # Verification rules
        ref_ok = (ref_res.verdict == "ACCEPTED" and ref_res.passed_cases == len(cases))
        stub_ok = (stub_verdict != "ACCEPTED")

        if ref_ok and stub_ok:
            status = "PASS"
            passed_count += 1
        else:
            status = "FAIL"
            failed_problems.append((title, lang, ref_res.verdict, ref_res.compile_error or ref_res.first_failing_case, stub_verdict))

        print(f"{idx:<3} {title[:38]:<40} {lang:<6} {len(cases):<6} {ref_res.verdict:<12} {stub_verdict:<12} [{status}]")

    print("-" * 80)
    print(f"Results: Total={total}, Passed={passed_count}, Skipped={skipped_count}, Failed={len(failed_problems)}")
    print("=" * 80)

    if failed_problems:
        print("\nFAILURES DETAIL:")
        for title, lang, r_verdict, r_err, s_verdict in failed_problems:
            print(f"- {title} ({lang}): Ref={r_verdict} (Error: {r_err}), Stub={s_verdict}")
        sys.exit(1)

    print("\nALL TESTED PROBLEMS PASSED VERIFICATION GATE.")
    return True


if __name__ == "__main__":
    verify_all_coding_problems()
