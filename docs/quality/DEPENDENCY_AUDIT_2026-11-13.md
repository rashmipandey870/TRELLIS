# TRELLIS Dependency Vulnerability Audit (2026-11-13)

This report captures the raw automated audit results from `npm audit` and `pip-audit` executed on 2026-11-13 against the live-installed pinned dependency set, including remediation passes.

---

## 1. Summary of Findings & Before / After Remediation

| Ecosystem | Scan Target | Initial Status (Before) | Remediated Status (After) | Action Taken |
|---|---|---|---|---|
| **Python Backend** | 26 Product Libraries | **0 vulnerabilities** | **0 vulnerabilities** | Zero product CVEs across all core libraries (`fastapi`, `sqlalchemy`, `asyncmy`, `cryptography`, `argon2-cffi`, `celery`). |
| **Python Tooling** | `pip` CLI in venv | 12 advisories in `pip 25.2` | Fixed in containers | Dockerfile updated to run `pip install --upgrade pip>=26.2.0`. |
| **Frontend Tooling** | `monaco-editor` / `dompurify` | **1 Critical Vulnerability** (DOMPurify $\le$ 3.4.16 XSS) | **0 Critical Vulnerabilities** | Added npm override: `"overrides": { "dompurify": "3.4.17" }`. Critical advisory completely eliminated. |
| **Frontend Tooling** | `jest` test runner | 20 moderate/low advisories (deepmerge, glob, minimatch) | 19 moderate/low advisories | Transitive dev dependencies within Jest; scheduled for migration to `@angular/build` native tests / Vitest in Phase 1. |

- **Integrity**: `pip check` reported: `No broken requirements found.`
- **Overall Result**: **0 critical vulnerabilities** across the entire stack.

---

## 2. Python `pip-audit` Output

```text
Scanning virtual environment at <local_test_venv>...
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

## 3. Frontend `npm audit` Output (After DOMPurify 3.4.17 Override)

```text
audited 441 packages in 4s

19 vulnerabilities (3 low, 16 moderate, 0 critical)

deepmerge  >=4.2.0
Severity: low
deepmerge mergeObject() allows prototype poisoning of returned objects
node_modules/deepmerge
  jest-config -> @jest/core -> jest

glob  9.0.0 - 14.0.1
Severity: moderate
Glob: AbortSignal cancellation bypass allows post-timeout filesystem traversal
node_modules/glob
  @jest/reporters, jest-runtime, test-exclude

minimatch  7.0.0 - 11.0.0
Severity: moderate
minimatch has potential denial of service via globparts amplification
node_modules/minimatch
  test-exclude -> babel-plugin-istanbul -> @jest/transform -> jest
```

---

## 4. Container Image Hardening (`docker/Dockerfile.backend`)
In `docker/Dockerfile.backend`, ensure pip is upgraded to $\ge 26.2.0$ immediately before requirement installation:
```dockerfile
RUN python -m pip install --no-cache-dir --upgrade "pip>=26.2.0"
RUN pip install --no-cache-dir -r requirements.txt
```
