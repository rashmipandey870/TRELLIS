# TRELLIS Threat Model & Security Architecture Baseline

## 1. System Overview & Trust Boundaries
TRELLIS processes employee identity, performance evaluations, assessment attempts, psychometric reflections, and proprietary knowledge assets.

### Trust Boundaries
1. **Public / Untrusted Zone**: Candidate browsers, mobile web clients, external SSO identity providers (Microsoft Entra ID).
2. **Perimeter / DMZ**: Reverse proxy / TLS termination layer (TLS 1.3 only, HSTS preloaded).
3. **Application Layer**: FastAPI application executing in containerized isolation.
4. **Data Isolation Layer**: Internal bridge network (`trellis-internal`); MySQL 8+ and Redis with authentication, no host port exposure.
5. **Untrusted Code Execution Sandbox**: Isolated, networkless container subsystem with seccomp/apparmor profiles, CPU quotas, memory limits, and non-root users.

---

## 2. STRIDE Threat Analysis & Mitigations

| Threat Category | Potential Attack Vector | Impact | TRELLIS Countermeasure |
|---|---|---|---|
| **S - Spoofing** | Session token hijacking, credential stuffing, forged OIDC tokens. | Unauthorized impersonation of employee or manager. | Microsoft Entra ID OIDC verification + Argon2id password hashing; short-lived JWTs (30m) with cryptographically rotated refresh tokens stored in HTTP-only, SameSite=Strict cookies; MFA for privileged roles (`LK_ADMIN`, `SUPER_ADMIN`). |
| **T - Tampering** | Altering historic skill evidence, modifying submitted assessment answers, tampering with audit records. | Falsified skills profiles, manipulated certification records. | **Tamper-Evident Evidence Ledger**: SHA-256 hash chaining of RFC 8785 canonical JSON; periodic signed checkpoints (`ledger_checkpoints`); database permissions strictly forbid UPDATE and DELETE on audit and ledger tables; DB user lacks DROP/TRUNCATE. |
| **R - Repudiation** | Grader denies scoring an exam; admin denies elevating privileges. | Lack of accountability, regulatory non-compliance. | **Immutable Audit Log**: Records `who, what, when, why, before_json, after_json, ip_address, session_id, approval_ref` for every state-altering action. System enforces dual custody for score overrides and privilege elevation. |
| **I - Information Disclosure** | Manager accessing unconsented raw scores; data leakage of psychometrics; SQL injection leaking employee records. | Privacy breach, DPDP violation, employee stigmatization. | **Consent Passport & Access Receipts**: Field-level encryption (AES-256-GCM) with per-employee envelope keys for sensitive data; repository-level row filtering; small-cell suppression (cells with `n < 5` are masked); zero unconsented manager views; every personal data read creates an access receipt. |
| **D - Denial of Service** | Assessment submission flooding; compute exhaustion via heavy IRT calculations or sandbox infinite loops. | Service disruption, exam timeouts. | Redis token-bucket rate limiting per IP and per user; Celery queue separation (`reports`, `ai`, `integrations`, `maintenance`) with strict worker concurrency and task timeouts; sandbox container CPU/memory limits with 5-second hard execution timeouts. |
| **E - Elevation of Privilege** | Horizontal privilege escalation (accessing another learner's Growth Ring); vertical escalation to `SUPER_ADMIN`. | Complete system compromise, data theft. | Centralized **Policy Engine** (`can(subject, action, resource, context)`) enforced as FastAPI middleware dependencies; no controller-level bypass; time-bounded role grants with explicit expiration. |

---

## 3. India DPDP Act Compliance Framework
TRELLIS is architected to comply with the Digital Personal Data Protection Act:
1. **Notice & Purpose Specification**: Every data collection flow (assessments, peer feedback, mentorship notes) presents a clear, itemized notice in plain language.
2. **Consent Lifecycle (Consent Passport)**: Consents are recorded as structured objects in the `consents` table with purpose code, timestamp, and status. Employees can revoke consent with one click.
3. **Right to Erasure via Crypto-Shredding (ADR-0003)**:
   - When an employee exercises the right to erasure, their personal details in `evidence_records` are wiped, and their salt/encryption key is shredded.
   - The cryptographic sequence in `evidence_ledger` remains structurally sound (`pseudonym_id` + hash chain intact), ensuring historical audit integrity without retaining identifiable personal data.
4. **Data Fiduciary Accountability**: Every cross-user read of personal data (e.g. manager viewing a team member's summary) writes an `access_receipt` visible to the employee.

---

## 4. Blind Grading & Anti-Bias Invariants
- When an assessment submission enters the review queue for manual grading (e.g. communication essays or scenario rubrics), the API strips all PII: `user_id`, employee name, email, avatar, cohort, and department are replaced with a deterministic, salted `candidate_token`.
- Graders evaluate purely against rubric criteria. The unmasked score is joined to the employee profile only after the grading session is finalised and signed off.

---

## 5. AI Governance & Prompt Injection Defenses
1. **Untrusted Data Boundary**: All user-generated text and external documents ingested into the Gardener AI coach are treated strictly as untrusted data strings.
2. **Zero Tool Execution from Document Content**: Models are prohibited from triggering system tool calls or executing SQL based on ingested document context.
3. **Dual Model Evaluation in CI**: Every prompt template is tested against a fixed adversarial test suite in CI to detect jailbreaks, indirect injections, and grounding regressions before deployment.
4. **PII Masking**: Psychometric reflections, private employee notes, and personal identifiers are scrubbed via regex and NER pipelines prior to dispatching prompts to model endpoints.
