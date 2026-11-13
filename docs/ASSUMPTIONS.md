# TRELLIS Assumptions & Day-0 Defaults Log

This document records all Day-0 architectural and product assumptions for CSM Technology. Official CSM assets, colors, fonts, values, or policies are never invented.

Last Updated: 2026-11-13 (Phase 0 Planning)

| # | Question Area | Status & Value | Resolution Notes |
|---|---|---|---|
| 1 | **Official logo, colours, fonts, tone, company values** | **PLACEHOLDER BRANDING (Confirmed)** | User confirmed: No official brand assets yet; will supply later. Fallback palette applied and clearly labelled: Dark base `#0B0D12`, Blue `#1294C4`, Maroon `#8B3A3A`, White `#FFFFFF`. Typography: Inter / system sans-serif with OpenDyslexic option. |
| 2 | **Skills taxonomy source** | **ACTIVE DEFAULT** | Editable `DRAFT` taxonomy seed file (`taxonomy_seed.json`), owned and managed by `LK_ADMIN`. |
| 3 | **HR system & API for employee master, reporting lines, skills** | **ACTIVE DEFAULT** | CSV import specification plus an extensible `HrSystemAdapter` interface. |
| 4 | **SSO provider** | **ENTRA ID TARGET (Confirmed)** | User confirmed: Microsoft 365 / Entra ID via OIDC is the architectural target. Local Argon2id authentication with JWT rotation provided for dev/demo. |
| 5 | **Scale** | **DEFAULT CONFIRMED** | Target capacity: 2,000 employees, 300 concurrent users. Database connection pools, query caching, and rate limiting configured accordingly. |
| 6 | **Hosting and data residency** | **ACTIVE DEFAULT** | Docker Compose for development, Kubernetes-ready deployment artifacts, targeted to India region data residency (DPDP Act compliance). |
| 7 | **Legal / DPO sign-off for psychometrics & webcam proctoring** | **ACTIVE DEFAULT (OFF)** | Both features architected behind strict feature flags (`FEATURE_PSYCHOMETRICS=false`, `FEATURE_WEBCAM_PROCTORING=false`), default OFF. |
| 8 | **Approved content sources for AI coach (Gardener)** | **ACTIVE DEFAULT** | Knowledge Base empty until an administrator uploads and approves curated documents. Strict zero-shot refusal without verified citations. |
| 9 | **NVIDIA NIM access & model ID** | **ACTIVE DEFAULT** | Provider interface (`NvidiaNimClient`) configured with deterministic mock provider for CI/dev/demo adhering to NIM schema. |
| 10 | **Retention periods per data class** | **ACTIVE DEFAULT** | Configurable retention schedule in compliance with India DPDP guidelines; auto-deletion jobs disabled by default pending legal confirmation. |
| 11 | **Languages** | **ACTIVE DEFAULT** | English (`en-IN` / `en-US`) in Phase 0 & 1; Hindi (`hi-IN`) localization infrastructure prepared for Phase 2. |
| 12 | **Current Employee Skills Portal schema & export** | **3-PART MAP CONFIRMED** | User confirmed: Screenshots/export to be sent later. Until then, design is mapped directly to its 3 known parts: **1. Skill Assessment**, **2. Onboarding Induction**, and **3. Skill Sheet**. |
