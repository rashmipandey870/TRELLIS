# TRELLIS Known Limitations

As required by Section 5 of the Master Prompt, any incomplete, mocked, or placeholder feature is explicitly documented here.

| Item ID | Component | Current State / Limitation | Planned Resolution Phase |
|---|---|---|---|
| LIM-001 | Branding | Using fallback placeholder palette and generic TRELLIS marks | Phase 1 upon CSM brand guidelines delivery |
| LIM-002 | Microsoft Entra SSO | Local authentication active; OIDC Entra ID configured with mock adapter | Phase 1 integration verification with live tenant |
| LIM-003 | AI Coach (Gardener) | Deterministic mock responses conforming to NVIDIA NIM schema | Phase 4 when live endpoint & approved documents are provided |
| LIM-004 | Psychometrics & Proctoring | Features default to OFF (`FEATURE_PSYCHOMETRICS=false`, `FEATURE_WEBCAM_PROCTORING=false`) | Phase 2 pending CSM legal / DPO sign-off under DPDP Rules |
| LIM-005 | Hindi Localization | UI language strings English-only initially | Phase 2 localization pass |
