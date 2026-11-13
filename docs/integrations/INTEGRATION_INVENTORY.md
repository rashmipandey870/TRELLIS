# TRELLIS Integration Inventory & Honest Status Directory

## 1. Governance & Honest Status Tracking (Master Prompt Section 15)
Every integration in TRELLIS is bounded by an abstract Python adapter interface, accompanied by an in-memory/deterministic mock for continuous integration, and reflects an honest status:
- **CONFIGURED**: Fully implemented, tested, and active against live credentials.
- **MOCKED_FOR_DEV**: Fully implemented interface running against a deterministic mock provider pending live credentials.
- **MISSING_CREDENTIALS**: Integration logic complete, awaiting enterprise client secrets/tenant IDs from CSM.
- **NOT_BUILT**: Scheduled for subsequent delivery phases according to the master roadmap.

---

## 2. Integration Registry

| Integration ID | System / Standard | Protocol / Format | Target Phase | Adapter Interface | Current Honest Status | Fallback / Notes |
|---|---|---|---|---|---|---|
| `INT-001` | **Microsoft Entra ID (SSO)** | OIDC / OAuth 2.0 | Phase 1 | `OidcAuthAdapter` | **MISSING_CREDENTIALS** | Local Argon2id authentication + mock OIDC provider enabled for local dev/demo. |
| `INT-002` | **HR System Employee Sync** | CSV Batch Import / REST | Phase 1 | `HrSystemAdapter` | **MOCKED_FOR_DEV** | Standardized CSV parser specification ready; REST API adapter awaiting CSM HR system details. |
| `INT-003` | **xAPI Learning Record Store** | xAPI (IEEE 9274.1.1) | Phase 2 | `XApiStatementDispatcher`| **NOT_BUILT** | Designed to stream assessment and pathway milestone statements into internal LRS. |
| `INT-004` | **SCORM Package Import** | SCORM 1.2 & 2004 4th Ed. | Phase 3 | `ScormPackageParser` | **NOT_BUILT** | ZIP manifest parser and runtime CMI data-model bridge scheduled for Phase 3. |
| `INT-005` | **cmi5 Course Player** | cmi5 (xAPI Profile) | Phase 3 | `Cmi5CourseAdapter` | **NOT_BUILT** | Replaces legacy SCORM with mobile-friendly, secure AU execution. |
| `INT-006` | **LTI 1.3 External Content** | IMS LTI 1.3 Advantage | Phase 3 | `LtiToolConsumer` | **NOT_BUILT** | Enables embedding third-party courseware with deep linking and grade passback. |
| `INT-007` | **Microsoft Teams Sync** | Microsoft Graph API | Phase 3 | `TeamsMeetingSyncAdapter` | **MISSING_CREDENTIALS** | Calendar booking and meeting join links; mocked with local ICS generator until M365 app registration. |
| `INT-008` | **NVIDIA NIM AI Coach** | OpenAI-compatible REST / NIM | Phase 4 | `NvidiaNimClient` | **MOCKED_FOR_DEV** | Deterministic mock client returning schema-validated JSON with citations; awaiting NIM API key. |
| `INT-009` | **SCIM 2.0 Identity Provisioning**| RFC 7644 REST | Phase 4 | `ScimProvisioningEndpoint`| **NOT_BUILT** | Automated user and group provisioning from Entra ID / Okta. |
| `INT-010` | **Verifiable Credentials Issuer**| W3C VC / Open Badges 3.0 | Phase 5 | `VerifiableCredentialIssuer`| **NOT_BUILT** | Cryptographically signed JSON-LD / JWT credentials for portable Skills Passports. |
| `INT-011` | **External Webhooks Engine** | HMAC-SHA256 Signed HTTP POST | Phase 4 | `WebhookDispatcher` | **NOT_BUILT** | Emits real-time learning milestone events to external enterprise HRIS/LMS. |

---

## 3. Abstract Adapter Pattern
All external communication is isolated behind strict interfaces:
```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class ExternalIntegrationAdapter(ABC):
    """Base interface for all third-party and standard interoperability connectors."""

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Returns connection latency, configuration status, and health indicators."""
        pass
```
This guarantees that unit tests and local development can run 100% offline without external network or credential dependencies.
