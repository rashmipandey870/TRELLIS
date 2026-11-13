# ADR-0002: Centralized Policy Engine & Unified ABAC/RBAC Data Matrix

## Status
Accepted

## Context
Enterprise learning and skill data carries significant privacy, ethical, and legal sensitivity (particularly under the India DPDP Act). Traditional role-based access control (RBAC) is insufficient because permissions depend on dynamic relationships (e.g., manager reporting lines, cohort membership, candidate anonymization in blind grading, and individual consent). Hardcoding permission checks inside route handlers leads to security bugs, inconsistent audits, and leaky abstractions.

## Decision
We implement a **Centralized Policy Engine** backed by a machine-readable permission data matrix:
1. **Single Evaluation Function**: `can(subject, action, resource, context) -> PolicyDecision`.
2. **Authority Source**: [docs/security/PERMISSION_MATRIX.json](../security/PERMISSION_MATRIX.json) defines all rules across `Resource × Action × Role × Scope × Approval × Audit`.
3. **Repository-Level Row Filtering**: Queries automatically apply tenant (`org_id`), cohort, team, and consent boundaries at the SQL level via SQLAlchemy query hooks.
4. **Mandatory Separation of Duties**:
   - Content authors cannot approve their own materials.
   - Blind graders cannot view candidate PII.
   - Score overrides require dual authorization and logged justification.
   - Audit logs and evidence ledgers are strictly immutable (no update or delete grants).
5. **Automated Test Generation**: In CI, automated backend permission test cases are generated directly from the JSON matrix, guaranteeing 100% matrix coverage.

## Consequences
### Positive
- Zero authorization logic scattered across controllers or business logic.
- Guaranteed test coverage: every role-resource-action tuple is tested against forbidden and permitted scenarios.
- Complete transparency and auditability for compliance reviews.

### Negative / Trade-offs
- Slight overhead for evaluating complex ABAC rules per request; mitigated via Redis caching of subject permission scopes.
- Context gathering (e.g. fetching reporting hierarchy) must be optimized to prevent N+1 queries.
