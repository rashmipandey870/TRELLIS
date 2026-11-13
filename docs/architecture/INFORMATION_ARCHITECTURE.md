# TRELLIS Information Architecture & Navigation Taxonomy

## 1. System Navigation Hierarchy & Module Topology

```
TRELLIS Platform
├── 1. Personalised Home (`/home`)
│   ├── "Continue Climbing" Hero (Next Priority Action)
│   ├── Skill Gaps & Growth Ring Quick-View
│   ├── Assigned Learning & Upcoming Deadlines
│   ├── Sessions & Calendar Integrations
│   ├── Streak, XP, & Developmental Badges
│   └── Greenhouse Featured Idea & Cohort Announcements
│
├── 2. Pathways (`/pathways`) [Legacy: Onboarding Induction + Career Path]
│   ├── Role Onboarding Pathways (First-90-Days Copilot)
│   ├── Skill Vine Matrix (Visual Prerequisites Graph)
│   ├── Career Roadmap & Competency Progression
│   ├── Micro-Learning Cards & Spaced Revision Refreshers
│   └── Verifiable Certificates & Accreditations
│
├── 3. Growth Check (`/growth-check`) [Legacy: Skill Assessment]
│   ├── Adaptive Technical Assessments (MCQ, SQL, Scenarios)
│   ├── Coding Sandbox Assessments (Live Test Runner)
│   ├── Communication Diagnostics (CEFR Rubrics & Moderation)
│   ├── Optional Developmental Psychometrics (Consent-Gated)
│   └── Post-Assessment Growth Ring Report (Radar + Data Table)
│
├── 4. Growth Ring & Skills (`/growth-ring`) [Legacy: Skill Sheet]
│   ├── Evidence-Based Development Profile (What I can do / evidence)
│   ├── Active Skills Graph & Decay Status (Fade vs Fresh)
│   ├── Inferred Skills Review (Confirm / Edit / Reject)
│   ├── Tamper-Evident Evidence Ledger & Verification View
│   └── Downloadable Growth Ring PDF Report
│
├── 5. Sessions (`/sessions`)
│   ├── Scheduled Batches & Interactive Calendar
│   ├── Microsoft Teams Live Sync & Join Links
│   ├── Attendance Tracking & Verification
│   └── Class Recordings & Curated Session Resources
│
├── 6. Greenhouse (`/greenhouse`)
│   ├── GitHub-Style Idea Explorer (Seed → Sprouting → Shipped)
│   ├── Idea Grafting / Forking with Visual Side-by-Side Diff
│   ├── Peer Reviews & Trainer/Manager Approval Pipeline
│   ├── Monthly Innovation Challenges & Duplicate Detection
│   └── Contribution Heatmap & Idea Badges
│
├── 7. Grove (`/grove`)
│   ├── Cohort Social Spaces & Announcements
│   ├── Peer & Trainer Doubt Threads with Resolution Flags
│   ├── 1:1 Mentoring Slot Booking & Confidential Notes
│   ├── Assignment Submissions & In-line Trainer Feedback
│   └── Live Q&A and Interactive Pulse Polls
│
├── 8. Gardener AI Coach (`/gardener`)
│   ├── Curated Context Q&A (Approved CSM Knowledge Only)
│   ├── Grounded Citations & "Why this recommendation?" Panels
│   ├── Weekly Adaptive Study Plans & Mistake Explanations
│   └── Responsible AI Transparency & Fallback to "Ask an Expert"
│
├── 9. Opportunities (`/opportunities`)
│   ├── Consent-Based Internal Talent & Gig Marketplace
│   ├── Stretch Projects, Job Shadowing, & Mentorship Gigs
│   ├── Growth Ring Match Indicator (% Skills Fit)
│   └── Private Application Tracker (No Automated Decisions)
│
├── 10. Knowledge Base (`/knowledge`)
│   ├── Full-Text Searchable Knowledge Wiki
│   ├── Project Post-Mortems & Reusable Solution Patterns
│   ├── Expert Directory & "Ask an Expert" Interview Capture
│   └── Competency-Tagged Learning Assets
│
├── 11. Analytics & Insights (`/analytics`)
│   ├── Role & Cohort Skill-Gap Heatmaps
│   ├── Kirkpatrick Levels 1–4 Impact Narrative
│   ├── Time-to-Productivity & Certification Pass Rates
│   └── Small-Group Privacy Suppression (`n < 5` Masking)
│
├── 12. Privacy & Consent Passport (`/privacy`)
│   ├── Active Consent Grants & One-Click Revocation
│   ├── Access Receipts Log (Who viewed my data & when)
│   ├── Personal Data Export (Skills Passport VC)
│   └── Statutory DPDP Right to Erasure Workflow
│
└── 13. Admin Console (`/admin`) [LK_ADMIN & SUPER_ADMIN]
    ├── Skills Taxonomy Seed Editor & Edge Linker
    ├── Question Banks & Adaptive Item Parameter Review
    ├── Role Grants, Time-Bounded Elevations & Dual Custody
    ├── AI Registry & Evaluation Benchmark Reports
    └── Immutable Audit Log Explorer
```

---

## 2. Legacy Subsystem Transformation

| Legacy Portal Subsystem | Target TRELLIS Route | Key Transformative Capabilities |
|---|---|---|
| **Skill Assessment** | `/growth-check` | Static testing replaced by adaptive IRT item selection, sandbox coding execution, blind grading for subjective rubrics, and the comprehensive Growth Ring Report. |
| **Onboarding Induction** | `/pathways/onboarding` | Static induction checklists replaced by First-90-Days Copilot, buddy matching in Grove, calendar-aware session booking, and empirical time-to-productivity measurement. |
| **Skill Sheet** | `/growth-ring` | Stale subjective rating sheets replaced by dynamic skills graph, evidence decay half-lives, tamper-evident hash ledger, and employee-confirmed skill inference. |

---

## 3. Role-Based Navigation Scopes

- **EMPLOYEE**: Sees `/home`, `/pathways`, `/growth-check`, `/growth-ring`, `/sessions`, `/greenhouse`, `/grove`, `/gardener`, `/opportunities`, `/knowledge`, and `/privacy`.
- **TRAINER_MENTOR**: Learner routes + Cohort Management, Blind Grading Queue, Session Facilitation, Idea Moderation, and Cohort Analytics.
- **MANAGER**: Learner routes + Team Consented Summaries, 1:1 Growth Conversation Kits, Stretch Opportunity Sponsor tools, and Aggregated Team Skill Gap Heatmaps (`n >= 5`).
- **LK_ADMIN**: Full system catalog management, question banks, taxonomy editor, AI governance registry, and anonymized enterprise analytics.
- **SUPER_ADMIN**: Infrastructure settings, tenant configuration, role grants, and security audit log review.

---

## 4. Global Command Bar (`Ctrl/Cmd+K`) Search Specification
The global command bar provides zero-latency indexed search across the entire platform, with **server-side permission trimming**:
- **Searchable Entities**:
  - `Action`: "Start my Growth Check", "Request a Mentor", "Submit an Idea", "Export my Skills Passport".
  - `Courses & Pathways`: Search by title, code, competency tag.
  - `Wiki & Learnings`: Full-text search across approved knowledge articles.
  - `People & Experts`: Directory of subject-matter experts and mentors.
  - `Greenhouse Ideas`: Public and team-scoped ideas and proposals.
- **Privacy Enforcement**: Items with confidentiality levels (`Department`, `Restricted`) or unconsented profiles are stripped by the API before results reach the client.
