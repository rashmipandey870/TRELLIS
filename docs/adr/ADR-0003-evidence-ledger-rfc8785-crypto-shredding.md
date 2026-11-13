# ADR-0003: Tamper-Evident Evidence Ledger, RFC 8785 Canonical Serialization, and DPDP Erasure via Crypto-Shredding

## Status
Accepted

## Context
A core differentiator of TRELLIS is the **Evidence Ledger** backing the continuous **Growth Ring**: an append-only, tamper-evident log of all skill evidence (assessments, assignments, trainer endorsements, project contributions). 

Two critical challenges arose:
1. **Serialization Non-Determinism**: Key order, whitespace, and floating-point representations in standard JSON vary across platforms, which would cause identical evidence payloads to yield divergent cryptographic hashes.
2. **The Immutable Ledger vs. DPDP Erasure Conflict**: The India Digital Personal Data Protection (DPDP) Act grants data principals the statutory right to erasure of personal data. However, modifying or deleting rows in an append-only hash chain breaks the cryptographic chain for all subsequent entries, rendering historical validation impossible.

## Decision

### 1. Cryptographic Hash Chaining & RFC 8785 Canonicalization
- **Algorithm**: Standard SHA-256.
- **Canonical Serialization**: All evidence payloads are serialized strictly using the **JSON Canonicalization Scheme (JCS, RFC 8785)** before hashing. This guarantees bit-for-bit deterministic serialization regardless of language or operating system.
- **Per-Employee Partitioning**: Instead of one monolithic chain that would cause database write contention, each employee maintains an independent sequential chain:
  $$\text{Hash}_n = \text{SHA256}(\text{org\_id} \,\|\, \text{pseudonym\_id} \,\|\, \text{seq\_num} \,\|\, \text{Hash}_{n-1} \,\|\, \text{RFC8785}(\text{payload}))$$
- **Periodic Signed Checkpoints**: Celery workers compute root Merkle checkpoints daily, which are digitally signed using an asymmetric private key held in an external key management system (KMS / HSM outside the database) and stored in `ledger_checkpoints`.

### 2. Resolving the Erasure Conflict via Off-Chain Crypto-Shredding
To reconcile the append-only ledger with statutory erasure rights, we decouple the cryptographic ledger from the personal evidence records:
1. **The Ledger (`evidence_ledger`)**: Contains strictly pseudonymous and cryptographic data:
   - `employee_pseudonym`: $\text{HMAC-SHA256}(\text{user\_id}, \text{Salt}_{\text{user}})$
   - `sequence_number`: Monotonically increasing integer per employee
   - `prev_hash`: SHA-256 hash of previous block
   - `data_hash`: SHA-256 hash of canonicalized evidence payload
   - `record_id`: UUID reference to `evidence_records`
   - *Zero plain-text personally identifiable information (PII) is stored in this table.*
2. **The Erasable Record Store (`evidence_records`)**: Contains the actual descriptive evidence details, trainer remarks, and assessment responses:
   - Field-level encrypted with an individual per-employee Data Encryption Key (DEK).
3. **The Erasure Workflow**: When an employee exercises their DPDP Right to Erasure:
   - All rows belonging to `user_id` in `evidence_records` are hard-deleted.
   - The employee's individual DEK and pseudonymous salt are permanently destroyed from KMS (Crypto-Shredding).
   - In `evidence_ledger`, the hashes and sequence remain intact. The hashes can still be mathematically verified against any historical offline receipt the employee holds, but the underlying data is rendered cryptographically unrecoverable and unlinked from any natural person.

## Consequences
### Positive
- Strict DPDP Act compliance without corrupting cryptographic hash chain integrity.
- Linear scalability: per-employee chains eliminate org-wide database row-locking contention during high-volume assessment submissions.
- Tamper detection is provable: any unauthorized alteration of a historical ledger row breaks the SHA-256 chain and fails the daily checkpoint verification.

### Negative / Trade-offs
- Verification requires resolving both the ledger row and the off-chain record (prior to erasure).
- External KMS dependency for root checkpoint signing keys and employee DEK management.
