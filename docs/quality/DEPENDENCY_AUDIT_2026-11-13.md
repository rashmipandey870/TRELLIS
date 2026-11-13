# TRELLIS Dependency Vulnerability Audit (2026-11-13)

This report captures the raw automated audit results from `npm audit` and `pip-audit` executed on 2026-11-13 against the live-installed pinned dependency set.

---

## 1. Summary of Findings

- **Python Backend Set**:
  - **Product Libraries**: **0 vulnerabilities** across all 26 pinned product libraries (`fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `alembic`, `asyncmy`, `cryptography`, `argon2-cffi`, `celery`, `redis`, etc.).
  - **Tooling Warning**: `pip` version `25.2` (bundled inside the Python 3.14 virtual environment) has 12 known advisories resolved in `pip >= 26.2.0`.
  - **Integrity**: `pip check` reported: `No broken requirements found.`
- **Frontend Angular 22 Set**:
  - `npm install` completed with 440 packages installed.
  - `npm audit` reported: **21 vulnerabilities** (4 low, 16 moderate, 1 critical).
  - Primary sources:
    - `monaco-editor` (0.57.0) transitively pulls `dompurify <= 3.4.16` (critical XSS advisories GHSA-p98j-92pf-mc4p).
    - `jest` (30.5.2) transitively pulls `deepmerge` and older `glob`/`minimatch` packages.
  - **Status Update**: The previous claim *"Dependency Audit Status: Clean"* is **removed**. Status is updated to: *"Vulnerabilities Identified in Frontend Tooling & Transitive Dependencies (Documented in DEPENDENCY_AUDIT_2026-11-13.md)"*.

---

## 2. Python `pip-audit` Output

```text
Scanning virtual environment at C:\Users\Rashm\.gemini\antigravity\scratch\test_pip_venv...
Found 12 known vulnerabilities in 1 package
Name Version ID              Fix Versions
---- ------- --------------- ------------
pip  25.2    PYSEC-2026-1795 25.3
pip  25.2    PYSEC-2026-1796 26.0
pip  25.2    PYSEC-2026-2875 26.1
pip  25.2    PYSEC-2026-2876 26.1
pip  25.2    PYSEC-2026-196  26.1.2
pip  25.2    PYSEC-2026-3721 26.2.0
```

*All 26 product dependencies (`fastapi 0.162.5`, `sqlalchemy 2.1.8`, `asyncmy 0.2.18`, `cryptography 50.0.2`, `argon2-cffi 25.1.0`, etc.) clean.*

---

## 3. Frontend `npm audit` Output

```text
21 vulnerabilities (4 low, 16 moderate, 1 critical)

dompurify  <=3.4.16
Severity: critical
DOMPurify: IN_PLACE: node-removing afterSanitize hook leaves detached subtree event handlers armed, causing DOM XSS - https://github.com/advisories/GHSA-p98j-92pf-mc4p
node_modules/dompurify
  monaco-editor  0.57.0-rc.2 - 0.57.0
  Depends on vulnerable versions of dompurify
  node_modules/monaco-editor

deepmerge  >=4.2.0
deepmerge mergeObject() allows prototype poisoning of returned objects - https://github.com/advisories/GHSA-gcqx-w48m-w2h4
node_modules/deepmerge
  jest-config  >=25.2.0-alpha.86
  node_modules/jest-config
    @jest/core  >=25.2.0-alpha.86
    node_modules/@jest/core
      jest  >=25.2.0-alpha.86
      node_modules/jest

glob  9.0.0 - 14.0.1
Severity: moderate
Glob: AbortSignal cancellation bypass allows post-timeout filesystem traversal - https://github.com/advisories/GHSA-3g3m-2fjr-6pw4
node_modules/glob
  @jest/reporters, jest-runtime, test-exclude
```

---

## 4. Remediation Strategy for Phase 1
1. **Frontend Monaco Editor Isolation**: Because Monaco Editor is only loaded in the candidate's Growth Check code editor, restrict DOMPurify usage and investigate pinning `@monaco-editor` with an overrides block or updating to the next patched release once published.
2. **Pip Upgrade**: In container builds (`Dockerfile.backend`), run `pip install --upgrade pip>=26.2.0` before installing requirements.
3. **Vitest / Jest Assessment**: Evaluate replacing Jest with modern `@angular/build` native testing or Vitest in Phase 1 to eliminate the legacy `deepmerge` / `glob` transitive dependency chain.
