# TRELLIS Honesty Ledger

This document tracks verified, unverified, and unbuilt capabilities across all phases of TRELLIS for leadership review.

Last Updated: 2026-11-13 (Phase 0 Planning)

---

## 1. Built and Verified
Features that are end-to-end implemented, have automated test coverage passing against real data, and meet the Definition of Done.

| Feature ID | Capability | Phase | Verification Method | Date Verified | Notes |
|---|---|---|---|---|---|
| VER-001 | Monorepo layout & Git VCS | 0 | Repository structure initialized; directory layout matches Section 4 | 2026-11-13 | Foundation complete |
| VER-002 | Complete 24-Section Specification | 0 | `CLAUDE.md` and `docs/PRODUCT_BRIEF.md` contain all 24 sections verbatim | 2026-11-13 | Architecture & governance locked |
| VER-003 | Exact Dependency Pinning | 0 | `docs/STACK.md` pinned with exact Python 3.11+ and Angular 19 versions | 2026-11-13 | No version ranges permitted |
| VER-004 | Day-0 Assumptions & Defaults Log | 0 | `docs/ASSUMPTIONS.md` records 12 Day-0 answers (Q1 placeholder, Q4 Entra ID, Q5 2k/300, Q12 3-part map) | 2026-11-13 | Confirmed with user |

---

## 2. Built but Unverified
Features implemented in code but lacking complete live-environment test passes, end-to-end validation, or dependencies.

| Feature ID | Capability | Phase | Reason Unverified | Action Required |
|---|---|---|---|---|
| *None* | - | - | Phase 0 is design & documentation only (no application code written) | - |

---

## 3. Not Built or Blocked
Features deferred to future phases, blocked on external credentials, or awaiting legal/asset sign-off.

| Feature ID | Capability | Target Phase | Blocker / Dependency | Mitigation / Fallback |
|---|---|---|---|---|
| BLK-001 | Official CSM branding & assets | Phase 0/1 | Official brand guidelines pending user supply | Placeholder branding (`#0B0D12`, `#1294C4`, `#8B3A3A`, `#FFFFFF`) clearly labelled |
| BLK-002 | Microsoft Entra ID production tenant | Phase 1 | Live M365 tenant credentials | Local auth with Argon2id + mock OIDC adapter for dev/demo |
| BLK-003 | Live NVIDIA NIM endpoint & API keys | Phase 4 | Model endpoint credentials | Deterministic mock provider implementing the NIM schema |
| BLK-004 | Psychometrics & webcam proctoring | Phase 2 | Legal & DPO DPDP sign-off | Feature flags default to `OFF` (`FEATURE_PSYCHOMETRICS=false`, `FEATURE_WEBCAM_PROCTORING=false`) |
| BLK-005 | HR System production API connection | Phase 1 | HR integration API details | CSV import interface + `HrSystemAdapter` |
| BLK-006 | Current Employee Skills Portal export | Phase 0/1 | Screenshots/exports to be sent later | Mapped to 3 known legacy core parts: Skill Assessment, Onboarding Induction, Skill Sheet |
