# TRELLIS Honesty Ledger

This document tracks verified, unverified, and unbuilt capabilities across all phases of TRELLIS for leadership review.

Last Updated: 2026-11-13 (Initialization & Phase 0 Setup)

---

## 1. Built and Verified
Features that are end-to-end implemented, have automated test coverage passing against real data, and meet the Definition of Done.

| Feature ID | Capability | Phase | Verification Method | Date Verified | Notes |
|---|---|---|---|---|---|
| *None yet* | Monorepo scaffold & Phase 0 planning | 0 | Repo structure & git init verified | 2026-11-13 | Foundation setup |

---

## 2. Built but Unverified
Features implemented in code but lacking complete live-environment test passes, end-to-end validation, or dependencies.

| Feature ID | Capability | Phase | Reason Unverified | Action Required |
|---|---|---|---|---|
| *None yet* | - | - | - | - |

---

## 3. Not Built or Blocked
Features deferred to future phases, blocked on external credentials, or awaiting legal/asset sign-off.

| Feature ID | Capability | Target Phase | Blocker / Dependency | Mitigation / Fallback |
|---|---|---|---|---|
| BLK-001 | Official CSM branding & assets | Phase 0/1 | Official brand guidelines not yet supplied | Placeholder branding (#0B0D12, #1294C4, #8B3A3A) clearly labelled |
| BLK-002 | Microsoft Entra ID production tenant | Phase 1 | SSO credentials and client secret | Local auth with Argon2id + mock OIDC adapter for dev/demo |
| BLK-003 | Live NVIDIA NIM endpoint & API keys | Phase 4 | Model endpoint credentials | Deterministic mock provider implementing the NIM schema |
| BLK-004 | Psychometrics & webcam proctoring | Phase 2 | Legal & DPO DPDP sign-off | Feature flags default to OFF |
| BLK-005 | HR System production API connection | Phase 1 | HR integration details | CSV import interface + adapter pattern |
| BLK-006 | Current Employee Skills Portal export | Phase 1 | Legacy schema export / screenshots | Draft skills taxonomy seed file editable by LK_ADMIN |
