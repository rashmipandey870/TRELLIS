# TRELLIS Assumptions & Day-0 Defaults Log

As mandated in Section 3 of the TRELLIS Master Build Prompt, all unanswered Day-0 questions fall back to stated defaults. Official CSM assets, colors, fonts, values, or policies are never invented.

| # | Question Area | Default Applied | Status / Notes |
|---|---|---|---|
| 1 | **Official logo, colours, fonts, tone, company values** | Placeholder branding clearly labelled with fallback palette: Dark base `#0B0D12`, Blue `#1294C4`, Maroon `#8B3A3A`, White `#FFFFFF`. Typography: Inter / system sans-serif with dyslexia-friendly option. Values placeholder until supplied. | ACTIVE DEFAULT |
| 2 | **Skills taxonomy source** | Editable `DRAFT` taxonomy seed file, owned and manageable by `LK_ADMIN`. | ACTIVE DEFAULT |
| 3 | **HR system & API for employee master, reporting lines, skills** | CSV import specification plus an extensible adapter interface (`HrSystemAdapter`). | ACTIVE DEFAULT |
| 4 | **SSO provider** | Microsoft Entra ID via OIDC architecture; Argon2id local authentication with JWT rotation for dev/demo. | ACTIVE DEFAULT |
| 5 | **Scale** | Target capacity: 2,000 employees, 300 concurrent users. Database connection pools, query caching, and rate limiting configured accordingly. | ACTIVE DEFAULT |
| 6 | **Hosting and data residency** | Docker Compose for development, Kubernetes-ready deployment artifacts, targeted to India region data residency. | ACTIVE DEFAULT |
| 7 | **Legal / DPO sign-off for psychometrics & webcam proctoring** | Both systems architected behind strict feature flags (`FEATURE_PSYCHOMETRICS=false`, `FEATURE_WEBCAM_PROCTORING=false`), default OFF. | ACTIVE DEFAULT |
| 8 | **Approved content sources for AI coach (Gardener)** | Knowledge Base empty until an administrator uploads and approves curated documents. Strict zero-shot refusal without verified citations. | ACTIVE DEFAULT |
| 9 | **NVIDIA NIM access & model ID** | Configurable provider interface (`NvidiaNimClient`) with deterministic mock provider for CI/dev/demo. | ACTIVE DEFAULT |
| 10 | **Retention periods per data class** | Configurable retention schedule in compliance with India DPDP guidelines; auto-deletion jobs disabled by default pending legal confirmation. | ACTIVE DEFAULT |
| 11 | **Languages** | English (en-IN / en-US) in Phase 0 & 1; Hindi (hi-IN) localization infrastructure prepared for Phase 2. | ACTIVE DEFAULT |
| 12 | **Current Employee Skills Portal schema & export** | Standalone extensible schema mimicking standard Skill Assessment, Onboarding Induction, and Skill Sheet entities; import mappings ready for legacy exports/screenshots. | ACTIVE DEFAULT |
