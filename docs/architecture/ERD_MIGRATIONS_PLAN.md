# TRELLIS Entity-Relationship Model & Alembic Migrations Plan

## 1. Schema Overview & Invariants
- **Multi-Tenancy Readiness**: Every entity carries `org_id` (VARCHAR(36), Indexed, FK to `organisations.id`), enabling logical isolation for CSM Technology today and external tenants in the future.
- **Relational Integrity**: Strict foreign keys, unique constraints, and composite indexes. Flexible metadata is confined to explicit JSON columns with validation.
- **Audit & Timestamps**: Every table contains `created_at` (DATETIME(6) UTC) and `updated_at` (DATETIME(6) UTC).
- **Append-Only Evidence Chain**: `evidence_ledger` is strictly append-only, indexed by `(org_id, employee_pseudonym, sequence_number)`, chained via SHA-256 hashes of RFC 8785 canonical JSON, and backed by off-chain erasable `evidence_records` (crypto-shredding for DPDP compliance).

---

## 2. Entity Reconciliation (51 Entities Total)

### Reconciled Master List (Section 21 Baseline + Extended Entities)

| Category | # | Table Name | Description & Key Columns |
|---|---|---|---|
| **Multi-Tenancy & Config** | 1 | `organisations` | Tenant root (`id`, `name`, `code`, `domain`, `status`, `created_at`). |
| | 2 | `feature_flags` | Dynamic system flags (`id`, `org_id`, `flag_key`, `is_enabled`, `rules_json`). |
| | 3 | `retention_policies`| DPDP retention rules per data class (`id`, `org_id`, `data_class`, `retention_days`, `action`). |
| **Identity & Access** | 4 | `users` | Core user identity (`id`, `org_id`, `email`, `password_hash`, `is_active`, `full_name`). |
| | 5 | `employment_records` | HR employment history (`id`, `user_id`, `employee_code`, `department`, `reporting_line_id`). |
| | 6 | `roles` | Role registry (`id`, `name`, `code`, `description`, `is_system_role`). |
| | 7 | `grants` | Active role assignments (`id`, `user_id`, `role_id`, `granted_by`, `expires_at`). |
| | 8 | `consents` | DPDP consent passport (`id`, `user_id`, `purpose_code`, `status`, `granted_at`, `revoked_at`). |
| | 9 | `cohorts` | Learner cohorts (`id`, `org_id`, `name`, `start_date`, `target_completion_date`). |
| | 10 | `batches` | Training batches within cohorts (`id`, `cohort_id`, `name`, `trainer_id`, `max_capacity`). |
| **Skills & Growth Ring** | 11 | `skills` | Skills taxonomy node (`id`, `org_id`, `code`, `name`, `category`, `decay_half_life_days`). |
| | 12 | `skill_levels` | Descriptors per skill level (`id`, `skill_id`, `level_number`, `title`, `rubric_text`). |
| | 13 | `skill_edges` | Graph relations (`id`, `source_skill_id`, `target_skill_id`, `relationship_type`). |
| | 14 | `role_requirements` | Skill benchmarks per job role (`id`, `org_id`, `role_code`, `skill_id`, `target_level`). |
| | 15 | `evidence_ledger` | Append-only hash chain (`id`, `org_id`, `employee_pseudonym`, `seq_num`, `prev_hash`, `data_hash`, `record_id`). |
| | 16 | `evidence_records` | Erasable detail payload (`id`, `user_id`, `skill_id`, `evidence_type`, `weight`, `raw_payload`, `key_id`). |
| | 17 | `ledger_checkpoints` | Signed periodic root checkpoints (`id`, `org_id`, `checkpoint_hash`, `signature`, `created_at`). |
| | 18 | `growth_rings` | Materialized developmental profile (`id`, `user_id`, `ring_version`, `status_json`, `calculated_at`). |
| | 19 | `learning_plans` | Active personal learning plan (`id`, `user_id`, `growth_ring_id`, `target_date`, `status`). |
| **Curriculum & Pathways** | 20 | `courses` | Learning courses (`id`, `org_id`, `title`, `code`, `description`, `published_at`). |
| | 21 | `modules` | Course chapters/units (`id`, `course_id`, `sequence_order`, `title`, `duration_minutes`). |
| | 22 | `pathways` | Role onboarding & learning paths (`id`, `org_id`, `title`, `code`, `is_mandatory`). |
| | 23 | `enrolments` | Pathway & course enrolments (`id`, `user_id`, `pathway_id`, `progress_percent`, `completed_at`). |
| **Assessments (Growth Check)**| 24 | `question_banks` | Competency-tagged banks (`id`, `org_id`, `name`, `skill_id`, `difficulty_tier`). |
| | 25 | `assessments` | Assessment configurations (`id`, `org_id`, `title`, `assessment_type`, `time_limit_mins`). |
| | 26 | `items` | Individual test questions (`id`, `bank_id`, `item_type`, `content_json`, `model_answer_json`). |
| | 27 | `item_stats` | IRT difficulty/discrimination (`id`, `item_id`, `difficulty_b`, `discrimination_a`, `exposure_count`). |
| | 28 | `rubrics` | Multi-criteria scoring rubrics (`id`, `assessment_id`, `criteria_json`, `min_passing_score`). |
| | 29 | `attempts` | Candidate test sessions (`id`, `assessment_id`, `user_id`, `started_at`, `submitted_at`, `status`). |
| | 30 | `responses` | Answers per item (`id`, `attempt_id`, `item_id`, `candidate_response_json`, `score`, `feedback`). |
| | 31 | `integrity_flags` | Proctoring/integrity signals (`id`, `attempt_id`, `flag_type`, `severity`, `details_json`, `reviewed_by`). |
| **Sessions & Mentoring** | 32 | `sessions` | Virtual/in-person classes (`id`, `org_id`, `batch_id`, `title`, `teams_meeting_id`, `start_time`). |
| | 33 | `attendance` | Session attendance records (`id`, `session_id`, `user_id`, `attended_minutes`, `status`). |
| | 34 | `mentoring_slots` | 1:1 mentorship bookings (`id`, `mentor_id`, `mentee_id`, `scheduled_at`, `notes`, `rating`). |
| **Collaboration & Community** | 35 | `greenhouse_ideas` | Innovation ideas pipeline (`id`, `org_id`, `author_id`, `title`, `stage`, `confidentiality`). |
| | 36 | `grafts` | GitHub-style idea forks (`id`, `idea_id`, `forked_by_id`, `diff_patch_json`, `merged_at`). |
| | 37 | `reviews` | Peer & trainer idea reviews (`id`, `idea_id`, `reviewer_id`, `decision`, `comments`). |
| | 38 | `spaces` | Grove cohort social spaces (`id`, `org_id`, `cohort_id`, `name`, `description`). |
| | 39 | `threads` | Discussions & doubts (`id`, `space_id`, `author_id`, `title`, `content`, `is_resolved`). |
| | 40 | `comments` | Thread & idea replies (`id`, `thread_id`, `idea_id`, `author_id`, `body`). |
| | 41 | `votes` | Upvotes on ideas/threads (`id`, `user_id`, `idea_id`, `thread_id`, `direction`). |
| **Knowledge Base** | 42 | `kb_articles` | Approved wiki articles (`id`, `org_id`, `author_id`, `title`, `content_md`, `status`, `approved_by`). |
| **AI Governance (Gardener)** | 43 | `ai_runs` | Auditable AI inferences (`id`, `org_id`, `model_id`, `prompt_version`, `input_hash`, `output_json`). |
| **Audit & Security** | 44 | `audit_log` | Immutable security log (`id`, `org_id`, `actor_id`, `action`, `resource`, `before_json`, `after_json`). |
| | 45 | `access_receipts` | Cross-user data read log (`id`, `org_id`, `accessor_id`, `subject_id`, `resource_type`, `read_at`). |
| | 46 | `notifications` | System & in-app alerts (`id`, `user_id`, `title`, `message`, `is_read`, `created_at`). |
| | 47 | `credentials` | Verifiable credentials & badges (`id`, `user_id`, `credential_type`, `raw_jwt_vc`, `is_revoked`). |
| **Gamification & Engagement**| 48 | `badges` | Earnable developmental badges (`id`, `org_id`, `title`, `icon_url`, `csm_value_code`). |
| | 49 | `user_xp` | XP transaction history (`id`, `user_id`, `amount`, `reason_code`, `awarded_at`). |
| | 50 | `user_streaks` | Learning activity streaks (`id`, `user_id`, `current_streak`, `longest_streak`, `freeze_count`). |
| | 51 | `announcements` | Org & cohort broadcasts (`id`, `org_id`, `cohort_id`, `title`, `body`, `priority`, `posted_at`). |

---

## 3. Feature Coverage Matrix (Sections 8–14 & 22)

| Section & Feature | Supporting Database Tables | Architecture Role |
|---|---|---|
| **Sec 8.1 / 14: Pathways & Skill Vine** | `pathways`, `courses`, `modules`, `enrolments`, `skills`, `skill_edges` | Manages role learning curves, prerequisite trees, module progress, and completion states. |
| **Sec 8.2 / 10: Growth Check & Items** | `assessments`, `question_banks`, `items`, `item_stats`, `rubrics`, `attempts`, `responses`, `integrity_flags` | Randomised item selection, IRT difficulty estimation, auto/manual grading, and accommodation timers. |
| **Sec 8.3: Sessions & Teams Sync** | `sessions`, `attendance`, `batches`, `cohorts` | Tracks scheduled live workshops, calendar sync IDs, and attendance percentage. |
| **Sec 8.4 / 11: Greenhouse Community** | `greenhouse_ideas`, `grafts`, `reviews`, `comments`, `votes` | GitHub-style branch-and-merge ideas, diff viewer, moderation queue, and status stages. |
| **Sec 8.5: Grove Cohort Spaces** | `spaces`, `threads`, `comments`, `votes`, `mentoring_slots` | Cohort-bound Q&A boards, peer discussions, and 1:1 mentor booking slots. |
| **Sec 8.6 / 12: Gardener AI Coach** | `ai_runs`, `kb_articles`, `skills`, `evidence_ledger` | RAG context retrieval from approved knowledge articles, prompt audit trails, zero hallucination. |
| **Sec 8.7: Analytics & Dashboards** | `growth_rings`, `item_stats`, `attempts`, `enrolments`, `audit_log` | Refreshes denormalised read models with sample size `n`, coverage, and small-group suppression. |
| **Sec 8.8: Knowledge Base & Wiki** | `kb_articles`, `skills` | Competency-linked internal wiki, peer learnings, and Ask-an-Expert knowledge capture. |
| **Sec 8.9: Admin Console** | `users`, `roles`, `grants`, `organisations`, `retention_policies`, `feature_flags`, `audit_log` | System governance, tenant settings, and DPDP compliance schedules. |
| **Sec 8.10 / 13: Opportunities Marketplace** | `role_requirements`, `skills`, `growth_rings`, `consents` | Internal talent marketplace matching people to gigs via opt-in consented profile views. |
| **Sec 9: Personalised Home & Command Bar** | `growth_rings`, `enrolments`, `sessions`, `user_streaks`, `badges`, `announcements` | Aggregates learner "Continue climbing" hero, assigned tasks, and searchable indices. |
| **Sec 14: Gamification** | `user_xp`, `user_streaks`, `badges` | Meaningful developmental milestones, streak freezes, and values alignment without public ranking. |
| **Sec 22.1: Tamper-Evident Ledger** | `evidence_ledger`, `evidence_records`, `ledger_checkpoints` | Cryptographic SHA-256 hash chaining of evidence events with off-chain crypto-shredding. |
| **Sec 22.3: Consent Passport & Receipts** | `consents`, `access_receipts` | Per-purpose consent toggles and transparent tracking of who accessed employee data. |
| **Sec 22.4: Fair-Assessment Audit** | `items`, `item_stats`, `responses` | 2-parameter IRT models and differential item functioning flags. |
| **Sec 22.6: First-90-Days Copilot** | `cohorts`, `pathways`, `enrolments`, `mentoring_slots` | Onboarding induction orchestrator tracking time to first independent task. |
| **Sec 22.11: Skills Passport** | `credentials`, `growth_rings`, `skills` | Verifiable W3C / Open Badges credential generation for offline portability. |

---

## 4. Alembic Migrations Strategy

Migrations follow an ordered, isolated sequence. Every migration script implements both `upgrade()` and clean `downgrade()` methods verified on an empty MySQL 8+ database.

```
alembic/versions/
  ├── 0001_core_tenancy_and_identity.py    # organisations, users, employment_records, roles, grants, consents
  ├── 0002_skills_and_evidence_ledger.py   # skills, skill_levels, skill_edges, role_requirements, evidence_ledger, evidence_records, checkpoints
  ├── 0003_pathways_and_courses.py         # cohorts, batches, pathways, courses, modules, enrolments
  ├── 0004_assessments_and_integrity.py    # question_banks, assessments, rubrics, items, item_stats, attempts, responses, integrity_flags
  ├── 0005_sessions_and_grove.py           # sessions, attendance, mentoring_slots, spaces, threads, comments, votes
  ├── 0006_greenhouse_and_knowledge.py     # greenhouse_ideas, grafts, reviews, kb_articles
  ├── 0007_ai_governance_and_audit.py      # ai_runs, audit_log, access_receipts, notifications
  └── 0008_gamification_and_credentials.py # badges, user_xp, user_streaks, announcements, credentials, feature_flags, retention_policies
```
