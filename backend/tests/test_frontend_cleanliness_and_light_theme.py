"""Test to strictly enforce Section A: Professional App Shell & Light Theme.

A1: Fails if shared demo password or '@csmtech.internal' login literals appear in frontend/src or frontend/dist.
A4: Fails if 'dark:' or 'html.dark' or '[data-theme=\"dark\"]' appears in frontend/src.
"""

from __future__ import annotations

from pathlib import Path


def test_no_credentials_in_frontend_src_or_dist():
    repo_root = Path(__file__).resolve().parent.parent.parent
    frontend_src = repo_root / "frontend" / "src"
    frontend_dist = repo_root / "frontend" / "dist"

    forbidden_patterns = [
        "CSMTrellis2026!",
        "csmtech.internal",
    ]

    violations = []

    # Check src
    if frontend_src.exists():
        src_files = list(frontend_src.rglob("*.ts")) + list(frontend_src.rglob("*.html"))
        for f in src_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            for pattern in forbidden_patterns:
                if pattern in content:
                    violations.append(f"Found '{pattern}' in frontend source: {f.relative_to(repo_root)}")

    # Check dist if built
    if frontend_dist.exists():
        dist_files = list(frontend_dist.rglob("*.js")) + list(frontend_dist.rglob("*.html"))
        for f in dist_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            for pattern in forbidden_patterns:
                if pattern in content:
                    violations.append(f"Found '{pattern}' in frontend dist bundle: {f.relative_to(repo_root)}")

    assert not violations, "Forbidden credential or internal email found:\n" + "\n".join(violations)


def test_light_theme_only_and_no_dark_classes():
    repo_root = Path(__file__).resolve().parent.parent.parent
    frontend_src = repo_root / "frontend" / "src"

    assert frontend_src.exists(), "frontend/src directory must exist"

    dark_violations = []
    files = (
        list(frontend_src.rglob("*.ts"))
        + list(frontend_src.rglob("*.html"))
        + list(frontend_src.rglob("*.css"))
    )

    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        if "dark:" in content:
            dark_violations.append(f"Found 'dark:' class in: {f.relative_to(repo_root)}")
        if "html.dark" in content:
            dark_violations.append(f"Found 'html.dark' in: {f.relative_to(repo_root)}")
        if '[data-theme="dark"]' in content:
            dark_violations.append(f"Found '[data-theme=\"dark\"]' in: {f.relative_to(repo_root)}")

    assert not dark_violations, (
        "Dark theme classes/tokens found in frontend source (Light theme only enforced):\n"
        + "\n".join(dark_violations)
    )
