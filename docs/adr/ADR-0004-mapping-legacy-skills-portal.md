# ADR-0004: Mapping Legacy CSM Skills Portal Subsystems

## Status
Accepted

## Context
TRELLIS is the next-generation layer of CSM Technology's existing Employee Skills portal. Pending receipt of legacy database exports and screenshots, the architecture must maintain seamless conceptual and data compatibility with the legacy portal's three confirmed core components:
1. **Skill Assessment**
2. **Onboarding Induction**
3. **Skill Sheet**

## Decision
We map these three legacy subsystems directly into TRELLIS's core bounded contexts, preserving historical continuity while elevating them to modern evidence-based, adaptive workflows:

### 1. Legacy "Skill Assessment" -> TRELLIS "Growth Check"
- **Legacy Role**: Static multiple-choice or technical tests taken at set intervals.
- **TRELLIS Evolution**: 
  - Legacy test definitions migrate to `assessments` and `question_banks`.
  - Upgraded to adaptive testing using Item Response Theory (IRT), randomized question banks, coding execution in isolated sandboxes, CEFR-aligned communication evaluations, and accommodation timers.
  - Generates comprehensive Growth Ring reports rather than raw binary pass/fail numbers.

### 2. Legacy "Onboarding Induction" -> TRELLIS "Pathways & First-90-Days Copilot"
- **Legacy Role**: Checklist of induction milestones, documents, and corporate presentations for new joiners.
- **TRELLIS Evolution**:
  - Legacy induction tasks migrate into structured onboarding `pathways`, `courses`, and `modules`.
  - Enhanced by the **First-90-Days Copilot**: orchestrates HR, IT, and learning milestones, automatically pairs the new joiner with a cohort buddy in Grove, schedules sessions around calendar free time, and rigorously measures *time-to-productivity* (onboarding start to first independent task).

### 3. Legacy "Skill Sheet" -> TRELLIS "Growth Ring & Skills Graph"
- **Legacy Role**: Self-reported or manager-rated employee competency matrix (often stale and subjective).
- **TRELLIS Evolution**:
  - Legacy skill inventories migrate into the authoritative `skills` taxonomy and `skill_levels`.
  - Replaced by the continuously updated **Growth Ring**: backed by the cryptographic `evidence_ledger`.
  - Skills fade over time based on configured half-life decay rates, prompting timely refreshers.
  - Skill inferences are suggested rather than asserted: employees confirm, edit, or reject inferred competencies.

## Consequences
### Positive
- CSM Technology preserves all historical organizational knowledge while eliminating the friction of stale self-assessments and manual spreadsheets.
- Future CSV/JSON data migration scripts can cleanly target these exact mapping tables.
