# TRELLIS Master Build Prompt v2
**Learning & Knowledge (L&K) Platform for CSM Technology**
*Tagline: "Where every Tendril climbs."*

## 1. ROLE
You are a principal product designer, solutions architect, accessibility specialist, security and privacy architect, learning scientist and full-stack engineer. Build TRELLIS, the Learning & Knowledge (L&K) platform for CSM Technology. Tagline: "Where every Tendril climbs." TRELLIS is the next layer of CSM's existing Employee Skills portal (Skill Assessment, Onboarding Induction, Skill Sheet) and must reuse its concepts and data where possible.
Think like the Chief Learning Officer who must defend this budget to the CEO: every feature must tie to a business outcome, a learner benefit, or a risk reduction. If it does none of these, cut it.
Ambition. The goal is a platform that sets a new standard for enterprise learning. Sections 21 to 24 (architecture blueprint, signature innovations, builder protocol, definition of done) bind you as strictly as everything above. Never claim in the product, the docs or a demo that a feature is "unique" or "industry-first"; let the evidence speak.

## 2. NORTH-STAR OUTCOMES
Measure these from real data only. Never hardcode.
• Time-to-productivity of new joiners (onboarding start to first independent task).
• Skill-gap closure rate per role and cohort (gap-to-target movement across Growth Rings).
• First-attempt certification pass rate after training.
• Voluntary learning: 90-day active learners who were not mandated.
• Knowledge reuse: answers, wiki pages and Greenhouse ideas that are reused or shipped.
• Mentor response time and mentee-reported usefulness.
• Training impact mapped to Kirkpatrick levels 1 to 4 (reaction, learning, behaviour, results), with coverage and sample size shown for each.
Design principle: learning should be pulled by usefulness, not pushed by mandates. Compliance training is the exception and is tracked separately.

## 3. DAY-0 QUESTIONS
Ask at most 12 concise questions in one message. If unanswered, proceed with the default and log it in docs/ASSUMPTIONS.md. Never invent official CSM assets, colours, fonts, values or policies.
1. Official logo, colours, fonts, tone, company values? Default: placeholder branding, clearly labelled.
2. Skills taxonomy source? Default: editable DRAFT taxonomy seed file, owned by LK_ADMIN.
3. HR system and API for employee master, reporting lines, skills? Default: CSV import plus an adapter interface.
4. SSO provider? Default: Microsoft Entra ID via OIDC; local auth for dev only.
5. Scale? Default: 2,000 employees, 300 concurrent users.
6. Hosting and data residency? Default: Docker Compose for dev, Kubernetes-ready, India region.
7. Legal/DPO sign-off for psychometrics and webcam proctoring? Default: both behind feature flags, OFF.
8. Approved content sources for the AI coach? Default: none until an admin uploads and approves content.
9. NVIDIA NIM access and model ID? Default: provider interface plus a deterministic mock.
10. Retention periods per data class? Default: configurable schedule, no deletion jobs enabled.
11. Languages? Default: English now, Hindi in Phase 2.
12. What does the current Employee Skills portal store and show? Default: ask for screenshots or an export.

## 4. LOCKED STACK: PYTHON + ANGULAR (change only with explicit approval)
Frontend: Angular + TypeScript, standalone components, Signals, lazy-loaded routes, Reactive Forms, Tailwind CSS, accessible headless primitives, Monaco Editor, charts only where genuinely useful.
Backend: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, MySQL 8+ (InnoDB, utf8mb4) via asyncmy or aiomysql, Redis, Celery + Redis, httpx, JWT, Argon2id, structured logging, OpenAPI.
Real-time: WebSockets, Yjs for collaborative editing, Redis pub/sub.
AI: NVIDIA NIM / Nemotron, backend-only, configurable model ID, structured JSON output with schema validation, retry, timeout, rate limit, cache, audit, fallback.
Code execution: separate sandboxed service in isolated containers. Never execute code inside the FastAPI server.
Database rules: foreign keys, indexes, constraints, transactions. JSON columns only for flexible metadata. Every schema change is an Alembic migration.
Monorepo, created from zero (no existing code, DB or users):
trellis/
  frontend/  backend/  docs/  docker/  scripts/  .github/
  .env.example  README.md  docker-compose.yml
Stack enforcement (hard rule). The backend is Python 3.11+ with FastAPI and the frontend is Angular with TypeScript. Do not introduce Node.js/Express/NestJS, Django, Flask, React, Vue or Next.js for any product code. Node is allowed only as Angular's build tooling. Every helper service (code sandbox, report renderer, bot, workers) is also written in Python. If a requirement seems to need something outside this stack, stop, record the trade-off in an ADR and wait for my approval. Pin every dependency and list it in docs/STACK.md.
Preferred tools inside the stack: Python: ruff, mypy --strict, pytest, pytest-asyncio, hypothesis, testcontainers (MySQL), structlog, authlib (OIDC), cryptography (field-level encryption), numpy/scipy/statsmodels (psychometrics and item response theory), WeasyPrint or ReportLab (PDF). Angular: Angular CDK a11y, Playwright, @axe-core/playwright, Jest.

## 5. NON-NEGOTIABLE RULES
• Enforce authorisation on the backend. The frontend only reflects it.
• No fake buttons, no hardcoded metrics, no placeholder disguised as finished. Anything incomplete is labelled and listed in docs/KNOWN_LIMITATIONS.md.
• Real MySQL data and real migrations. Demo data comes only from a seed script that writes synthetic records to the database, is gated by TRELLIS_ENV=demo, and shows a persistent "Synthetic demo data" banner. It must never run in production.
• Language is developmental, specific and respectful. Never label anyone "weak", "bad" or "unintelligent". Never rank employees publicly. Never make or feed automated employment decisions. Never produce AI-generated psychological labels.
• Every claim about a person carries an evidence label: STRONG_EVIDENCE, DEVELOPING_EVIDENCE, LIMITED_EVIDENCE, NOT_ENOUGH_DATA. Show sample size and data coverage next to any statistic.
• Do not copy proprietary tests (MBTI, Hogan, SHL and similar). Big Five uses public-domain IPIP items only.
• Work in small verifiable steps: inspect, plan, implement, test, fix, verify end to end. Never report "done" without running the tests and the build.

## 6. THE GROWTH RING (core differentiator)
A continuously updated, evidence-based development profile per employee:
• What they can do, and the evidence behind it.
• What they are developing.
• What to learn next, and which trainer, resource, session or mentor can help.
• Progress over time.
Skills graph: Model skills as a graph (skill, level descriptors, prerequisites, related skills, role requirements). Evidence sources feed it: assessments, assignments, trainer feedback, certifications, project contributions, Greenhouse work, peer endorsements. Each evidence item has a source, date, weight and decay so stale skills fade and prompt revision rather than staying "green" forever.
Skills inference (suggest, never assert): The system may suggest skills from evidence. The employee confirms, edits or rejects every inferred skill. Rejections are respected and logged.
Unified data: Skills data and learning data live in one model and one learner record, so recommendations are grounded in what people can do and what they are doing about it.
Growth Ring Report after every assessment: overall score; cohort percentile only where statistically meaningful; radar chart with data-table alternative; attempt-over-attempt growth; strengths first; specific wins; gaps with exact topics and questions; plain-language explanations; model answers; exactly 3 prioritised next steps; recommended courses, resources and mentors; one-click actions. Trainer can review, edit and approve before release. Employee can download a PDF and share chosen sections with their manager.

## 7. LIFECYCLE
HR onboarding → identity verification → cohort and role assignment → onboarding pathway → Growth Check → Growth Ring → personalised learning plan → trainer or mentor → training, practice, mentoring → assignments and feedback → certification → reassessment → updated Growth Ring → measurable progress.

## 8. MODULES
1. Pathways: role paths, prerequisites, progress, certificates, Skill Vine matrix, career roadmap, micro-learning cards, spaced revision.
2. Growth Check: technical, communication, aptitude, coding, scenario and debugging assessments; adaptive testing; randomisation; auto and manual review. Details in section 10.
3. Sessions: batches, attendance, trainer feedback, calendar, Microsoft Teams sync, recordings, resources.
4. Greenhouse: internal idea community. Details in section 11.
5. Grove: cohort spaces, doubt threads, mentoring slots, 1:1 notes, assignment submission, inline feedback, polls, live Q&A.
6. Gardener: AI learning coach. Details in section 12.
7. Analytics: skill-gap heatmaps, learning ROI, completion, score uplift, cohort comparison, trainer effectiveness, with sample size, coverage and missing-data indicators.
8. Knowledge base: searchable wiki, project learnings, Ask an Expert, expert directory, competency-linked resources.
9. Admin console: question banks, rubrics, cohorts, roles, notifications, integrations, audit logs, system configuration.
10. Opportunities (new): see section 13.

## 9. HOME PAGE
Personalised from real data: "Continue climbing" hero with one clear next action; current skill gaps; assigned learning; upcoming assessments and sessions; streak; badges; Greenhouse idea of the month; announcements; recent feedback. Empty, loading and error states are designed, not afterthoughts.
Global command bar (Ctrl/Cmd+K): one search across courses, wiki, people, experts, ideas and actions ("request a mentor", "start my Growth Check"). Results are permission-trimmed on the server.

## 10. GROWTH CHECK
• Technical: skill-tagged banks, difficulty levels, adaptive and randomised delivery, coding with test cases (sandbox service), SQL, scenarios, debugging tasks, auto plus manual review.
• Communication: grammar, comprehension, email writing, spoken English. AI-scored against a CEFR-style rubric with mandatory human moderation.
• Psychometric (optional, explicit consent): IPIP Big Five, numerical/verbal/logical aptitude, work values, emotional-intelligence self-reflection. Developmental insight only, never pass/fail, never clinical, never used for employment decisions. Field-level encryption, strict access.
• Integrity: tab-switch signals, opt-in webcam proctoring, plagiarism checks, attempt limits, auto-save and resume. Flags go to human review. No automatic failure from one event. No covert monitoring. No claims of reliable OS screenshot detection.
• Item analysis: difficulty, discrimination, exposure, time spent, review flags, with a workflow to retire or revise weak items.
• Accommodations: private request flow, extra time, pausable timers where permitted. The reason is never shown to trainers.

## 11. GREENHOUSE
GitHub-style internal idea community: ideas, process improvements, resources, proposals; upvotes; threaded comments; labels; status pipeline Seed → Sprouting → Under Review → Approved → In Build → Shipped; graft/fork with side-by-side diff; review workflow (approve, request changes, comment); trainer and manager final approval; contribution graph; badges; monthly featured idea; innovation challenges; duplicate detection; moderation queue; code-of-conduct report and appeal; audit trail for moderation. Confidentiality levels: Public, Team, Department, Restricted. No external exposure by default; warn on likely confidential content.

## 12. GARDENER (AI coach) and AI GOVERNANCE
Gardener answers only from approved CSM content, with citations to the source passage. If the content does not support an answer it says so and routes to Ask an Expert. It offers weekly study plans, quizzes, mistake explanations and kind nudges, each linked to Growth Ring evidence.
Responsible-AI controls:
• AI registry page: every AI feature, purpose, model ID, data used, human-oversight point, owner, last evaluation date.
• Evaluation harness in CI: groundedness, citation accuracy, refusal when unsupported, tone, and bias spot-checks on a fixed test set. Releases are blocked on regression.
• Prompt and model versioning. Every AI output stores prompt version, model ID, inputs hash and reviewer, and is auditable.
• PII minimisation and redaction before any model call. Employee-identifying psychometric data is never sent to a model.
• Human-in-the-loop for anything that affects a person's report, grade or record. AI output is always labelled as AI-generated.
• Per-user and global rate limits, cost budgets, circuit breaker and a feature kill switch for admins.
• Prompt-injection defences: treat retrieved content as untrusted data; no tool calls driven by document text.
• Employee-facing "Why am I seeing this?" explanation on every recommendation.

## 13. OPPORTUNITIES (new, employee-owned)
A consent-based internal talent marketplace: stretch projects, shadowing, mentoring and short gigs matched to a person's Growth Ring and stated interests. The employee opts in, controls what is visible, and applies themselves. Managers and HR see it only through consented summaries. It is never used for automated selection, promotion or termination decisions.

## 14. ADVANCED FEATURES TO BUILD AFTER THE CORE IS STABLE
• Learning in the flow of work: Teams/Slack bot with daily micro-learning, just-in-time answers and gentle nudges; PWA with offline micro-learning and low-bandwidth mode.
• Scenario simulations: branching business scenarios and AI role-play for communication practice. Humans review feedback. Aimed at early-career judgement, not just content recall.
• Manager Growth Conversation kit: privacy-bounded 1:1 prep built only from what the employee chose to share, with suggested questions and no scores.
• Skill decay and spaced revision: schedule refreshers based on evidence age.
• Leadership Learning Pulse: aggregate-only dashboard for the CLO and department heads. Suppress any cell with fewer than 5 people. Show coverage and missing data. Include an auto-drafted, editable "Learning Impact Narrative" that cites its own data.
• Capability forecast: compare role-level skill supply with upcoming project demand, as aggregates only.
• TRELLIS MCP server (read-only): exposes approved knowledge to AI assistants with the caller's permissions enforced.
• Verifiable credentials: QR certificates, Open Badges 3.0 / W3C Verifiable Credentials, public verification page showing only what the holder allows.
• Teach-a-session marketplace, mentor matching, hackathons, team challenges, quarterly "Growth Wrapped" (private to the employee).
• Gamification: XP, streaks and badges that reflect real completed actions, tied to official CSM values only after they are supplied. No public leaderboards, no shaming, no mandatory competition, streak freezes so breaks are not punished.

## 15. INTEROPERABILITY
Build an internal event model using xAPI statements with a learning-record store. Support SCORM and cmi5 import, LTI 1.3 for third-party content, SSO via OIDC/SAML, SCIM provisioning, and webhooks. Every integration has a documented adapter interface, a mock for tests and an honest status page ("configured / missing credentials / not built").

## 16. ACCESS CONTROL AND PRIVACY
Roles now: EMPLOYEE, TRAINER_MENTOR, LK_ADMIN, MANAGER, SUPER_ADMIN. Model now, build later: LK_HEAD_CLO, DEPARTMENT_HEAD, CONTENT_AUTHOR, ASSESSMENT_REVIEWER, HR_PARTNER, GUEST_CANDIDATE, AUDITOR.
RBAC plus ABAC (department, location, reporting line, cohort, batch, data sensitivity, consent status, employment status). Publish a permission matrix as data (resource × action × role × scope × approval × audit) and generate tests from it. Actions: create, read, update, delete, approve, export, impersonate, override, publish, grade, review, assign, enrol, download, share.
Privacy rules:
• Employees always see their own full results.
• Managers see only consented summaries and authorised team-level data.
• Trainers see only authorised cohort or assigned-employee data.
• HR sees completion and compliance data; psychometric data only as a consented summary.
• Admins see aggregate, anonymised data by default.
• Auditors read audit trails only, never personal assessment results.
Separation of duties: authors cannot approve their own content; graders cannot see candidate identity in blind grading; nobody can edit or delete audit logs; score overrides need approval and reason; exports need approval and logging; role elevation needs approval and expiry.
Auth: Microsoft 365 SSO preferred, MFA for privileged roles, refresh-token rotation, visible device/session list, immutable audit log recording who, what, when, why, before/after values, IP/session context and approval reference.

## 17. COMPLIANCE AND SECURITY
• India DPDP Act: design for consent records, purpose limitation, notice, retention schedule, withdrawal of consent, access and correction, breach workflow and a right-to-erasure workflow.
• Encryption in transit and at rest; field-level encryption for psychometric data with key rotation and envelope keys.
• SOC 2-style controls: change management, least privilege, access reviews, backups with restore drills, monitoring and alerting, incident runbook.
• Threat model (STRIDE) and OWASP ASVS checklist in docs/. Dependency and secret scanning in CI.
• Object storage for media and exports with signed, expiring URLs.

## 18. DESIGN AND ACCESSIBILITY (release gate, WCAG 2.2 AA)
• Placeholder design system unless official assets are supplied. Fallback palette: dark base #0B0D12, blue #1294C4, maroon #8B3A3A, white #FFFFFF. Mark it "placeholder branding".
• Light, dark, high-contrast and reduced-motion modes; 200% text resize; dyslexia-friendly font; adjustable spacing; 8px grid; design tokens; component library; skeletons; empty, error and validation patterns. Growth motif: vines, rings, trellis lines, climbing progress.
• Keyboard-only operation, visible focus, skip links, landmarks, live regions, contrast of at least 4.5:1, never colour alone. Every chart has a text summary and a data table.
• Accessible code editor, captions and transcripts, voice-input option, simple-language mode. Hindi in Phase 2.
• CI gates: axe tests, Lighthouse accessibility, a manual audit plan, and an assistive-technology test plan (NVDA, JAWS, VoiceOver, TalkBack).

## 19. ENGINEERING QUALITY BAR
• Unit, integration and E2E tests (Playwright). Backend permission tests generated from the matrix. Contract tests from OpenAPI.
• Performance budgets: p95 API under 300 ms for dashboard reads, first contentful paint under 2 s on a mid-range phone, load test at 2x expected concurrency.
• Observability: structured logs with correlation IDs, metrics, traces, health endpoints, SLOs documented.
• CI/CD with lint, type-check, tests, migrations check, accessibility checks, container build and security scan. Infrastructure as code. Feature flags for risky modules.
• Architecture decision records in docs/adr/ for every significant choice.

## 20. DELIVERY PLAN
Phase 0: ask Day-0 questions; information architecture; role-permission matrix; ERD and migrations plan; design tokens; accessibility plan; clickable wireframes; threat model; ADRs.
Phase 1: auth/SSO, RBAC and audit log, personalised home, Pathways, command bar.
Phase 2: Growth Check, Growth Ring generation and Reports, accommodations, item analysis.
Phase 3: Greenhouse, Grove, Sessions and Teams sync, Knowledge base.
Phase 4: Analytics, Gardener with AI governance, gamification, Opportunities.
Phase 5: advanced features from section 14.
After each phase deliver: a 5-minute demo script, a test checklist with results, acceptance criteria marked pass/fail, known limitations, and a one-page "what the CLO should see" summary.

## 21. ARCHITECTURE BLUEPRINT
Build a modular monolith in Python (one deployable FastAPI app plus Celery workers and the separate code sandbox). Split it into bounded contexts with no cross-context table access, only service interfaces and events: identity, access, people, skills, pathways, assessments, growth_ring, sessions, greenhouse, grove, gardener, knowledge, analytics, credentials, notifications, integrations, audit. Extraction into services must stay possible later, but do not start with microservices.
• Policy engine: one Python module answers can(subject, action, resource, context) for every request, backed by the permission matrix as data. Return the decision, the reason and any required approval. No route may bypass it. Row-level filters (department, cohort, consent, reporting line) are applied in the repository layer so a missed check cannot leak data.
• Events and outbox: domain events (for example AssessmentSubmitted, EvidenceAdded, RingUpdated) are written to an outbox table in the same transaction and published by a worker. Consumers are idempotent. The same events feed xAPI statements, notifications, the Growth Ring and analytics.
• Evidence ledger: an append-only table of evidence items per employee. Each row stores the previous row's hash so tampering is detectable (see section 22). The Growth Ring is a derived, rebuildable projection of this ledger.
• Read models: analytics and dashboards read from denormalised summary tables refreshed by workers, never from live transactional tables. Every summary row carries n, coverage and computed_at.
• Caching: Redis for sessions, rate limits and hot read models. Cache keys include the viewer's permission scope so one person's view is never served to another.
• Jobs: Celery queues separated by cost and risk: reports, ai, integrations, maintenance. Every job is idempotent, has a timeout and a dead-letter path.
• Multi-tenancy readiness: every table has org_id even though only CSM exists today.
• Core data model: users, employment records, roles, grants (with expiry), consents, skills, skill_levels, skill_edges, role_requirements, pathways, enrolments, assessments, items, item_stats, attempts, responses, integrity_flags, evidence_ledger, growth_rings, learning_plans, sessions, attendance, ideas, grafts, reviews, spaces, threads, mentoring_slots, kb_articles, ai_runs, audit_log, access_receipts, notifications, credentials.

## 22. SIGNATURE INNOVATIONS
1. Tamper-evident Evidence Ledger (Phase 1 foundation, visible in Phase 2)
2. "Why this?" and "What would change this?" on every recommendation (Phase 2)
3. Consent Passport and access receipts (Phase 1)
4. Fair-assessment audit (Phase 2)
5. Knowledge-risk map (Phase 4)
6. First-90-Days Copilot (Phase 1 to 2)
7. Capability what-if simulator (Phase 4)
8. Learning-impact experiments (Phase 4)
9. Teach-back verification (Phase 3)
10. Learning-load guard (Phase 3)
11. Skills Passport (Phase 5)
12. Cognitive accessibility suite (Phase 1 to 2)
13. Privacy-by-design analytics (Phase 4)
14. Leadership Briefing generator (Phase 4)

## 23. BUILDER OPERATING PROTOCOL
You are an autonomous engineering team. Work like this:
1. Plan mode first. Before each phase, write docs/phases/PHASE_N_PLAN.md.
2. Vertical slices.
3. Test first for rules that matter.
4. Small reviewable commits with clear messages.
5. Self-review pass at the end of every slice.
6. Stop and ask if required.
7. Use sub-agents or parallel work where independent.
8. Decision records in docs/adr/.
9. Never fabricate.

## 24. DEFINITION OF DONE AND HONESTY LEDGER
Maintain docs/HONESTY_LEDGER.md with three tables: built and verified, built but unverified, and not built or blocked.
