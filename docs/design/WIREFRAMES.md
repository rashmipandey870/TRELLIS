# TRELLIS Wireframes & Key Interface Layouts

This document details the text and ASCII structural wireframes for the five core screens of TRELLIS. These wireframes are paired with the static HTML prototypes in `docs/prototype/`.

---

## 1. Personalised Home (`/home`)

```text
+----------------------------------------------------------------------------------------------------+
|  TRELLIS | CSM Technology   [ Search or jump to... (Ctrl+K) ]      [Notification (2)]  [Profile: Priya] |
+----------------------------------------------------------------------------------------------------+
|  [!] SYNTHETIC DEMO DATA ACTIVE - FOR VALIDATION & REVIEW ONLY                                     |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  +----------------------------------------------------------------------------------------------+  |
|  |  CONTINUE CLIMBING                                                                           |  |
|  |  Welcome back, Priya! Next step in your "Senior Backend Engineer (Python)" pathway:          |  |
|  |  -> Module 4: Asynchronous Task Queues with Celery & Redis (Est: 45 mins)                    |  |
|  |                                                                                              |  |
|  |  [ > Resume Lesson ]      [ View Full Pathway ]           Target Completion: Nov 28, 2026   |  |
|  +----------------------------------------------------------------------------------------------+  |
|                                                                                                    |
|  +-----------------------------------------+  +-------------------------------------------------+  |
|  | YOUR GROWTH RING (CURRENT STATUS)       |  | ASSIGNED LEARNING & UPCOMING SESSIONS           |  |
|  | Core Skills: 12 Active | 2 Gaps Need Att|  |                                                 |  |
|  |                                         |  | [Session] Advanced FastAPI & DB Concurrency     |  |
|  | [*] Python Core: Level 4 [STRONG]       |  |   Tomorrow @ 14:00 IST | Trainer: Rajesh M.      |  |
|  | [*] System Design: Level 3 [DEVELOPING] |  |   [ Sync to Outlook / Teams ]                   |  |
|  | [!] Async Architectures: Level 2 [GAP]  |  |                                                 |  |
|  | [!] Security & DPDP: Level 1 [GAP]      |  | [Assessment] Q4 Growth Check: Backend Systems   |  |
|  |                                         |  |   Due in 6 days | Pausable accommodation active |  |
|  | [ Open Full Growth Ring Profile -> ]    |  |   [ Start Growth Check ]                        |  |
|  +-----------------------------------------+  +-------------------------------------------------+  |
|                                                                                                    |
|  +----------------------------------------------------------------------------------------------+  |
|  |  GREENHOUSE IDEA OF THE MONTH                                                                |  |
|  |  "Zero-Downtime Database Migration Framework using Alembic & Vitess" by Ananya Sharma       |  |
|  |  Stage: In Build | 42 Upvotes | 14 Review Comments | [ Read Proposal & View Diff ]           |  |
|  +----------------------------------------------------------------------------------------------+  |
|                                                                                                    |
|  +----------------------------------------------------------------------------------------------+  |
|  |  MOMENTUM & STREAK                                                                           |  |
|  |  14-Day Climbing Streak! [*][*][*][*][*][*][*][*][*][*][*][*][*][*]     [Freeze Available: 2] |  |
|  |  Total XP: 1,850 XP | Badges Earned: "Clean Architect", "First Greenhouse Graft"             |  |
|  +----------------------------------------------------------------------------------------------+  |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Global Command Bar (`Ctrl/Cmd+K`) Modal

```text
+----------------------------------------------------------------------------------+
|  [Search icon] Type a command, course, wiki article, or person...          [ESC] |
+----------------------------------------------------------------------------------+
|  QUICK ACTIONS                                                                   |
|    > Start my Scheduled Growth Check                                             |
|    > Request a 1:1 Mentoring Session in Grove                                    |
|    > Propose a New Idea in Greenhouse                                            |
|    > Open Consent Passport & View Access Receipts                                |
|    > Export My Skills Passport (Verifiable Credential)                           |
+----------------------------------------------------------------------------------+
|  MATCHING COURSES & PATHWAYS                                                     |
|    [Course] Async Python 3.11+: Concurrency, Tasks & Event Loops                 |
|    [Pathway] New Joiner Onboarding Induction (Tech Cohort 2026-B)                |
+----------------------------------------------------------------------------------+
|  KNOWLEDGE WIKI & BEST PRACTICES                                                 |
|    [Wiki] CSM Tech Coding Standards: Python Formatting, Ruff & Type Hints        |
|    [Wiki] Handling India DPDP Consent Tokens in Microservices                    |
+----------------------------------------------------------------------------------+
|  PEOPLE & EXPERTS                                                                |
|    [Expert] Rajesh Mohan - Principal Solutions Architect (Python / Cloud)       |
|    [Buddy] Sunita Rao - Senior Backend Developer (Assigned Grove Buddy)          |
+----------------------------------------------------------------------------------+
|  * Results are filtered on the server according to your authorized permissions.   |
+----------------------------------------------------------------------------------+
```

---

## 3. Growth Ring Assessment Report (`/growth-check/reports/:id`)

```text
+----------------------------------------------------------------------------------------------------+
|  GROWTH RING REPORT: Backend Engineering Competency Check                       [Download PDF]     |
|  Candidate: Priya S. (Self View) | Date: 2026-11-13 | Reviewer Moderation: Approved by Trainer     |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  OVERALL DEVELOPMENT SCORE: 84 / 100                                                               |
|  Cohort Percentile: 78th Percentile (Statistically Meaningful: Cohort n=48, Coverage 96%)          |
|                                                                                                    |
|  +-----------------------------------------+  +-------------------------------------------------+  |
|  | RADAR VISUALIZATION                     |  | DATA-TABLE ALTERNATIVE (ACCESSIBLE)             |  |
|  |                Python Core              |  | +--------------------+-------+--------+---------+ |  |
|  |                   (4.5)                 |  | | Skill Area         | Score | Target | Status  | |  |
|  |                     ^                   |  | +--------------------+-------+--------+---------+ |  |
|  |                     |                   |  | | Python Core        |  92%  |  85%   | STRONG  | |  |
|  | Async/Celery <------+------> System Des|  | | System Design      |  82%  |  80%   | STRONG  | |  |
|  |     (2.8)           |          (3.6)    |  | | Async & Celery     |  64%  |  75%   | DEVELOP | |  |
|  |                     v                   |  | | Security & DPDP    |  52%  |  70%   | GAP     | |  |
|  |               Security/DPDP             |  | +--------------------+-------+--------+---------+ |  |
|  |                   (2.2)                 |  | Sample Size: 24 items | IRT Standard Error: 0.12|  |
|  +-----------------------------------------+  +-------------------------------------------------+  |
|                                                                                                    |
|  DEVELOPMENTAL FEEDBACK & CELEBRATIONS                                                             |
|  - Key Win: Demonstrated deep mastery in FastAPI dependency injection and typed schema validation. |
|  - Growth Opportunity: Async task error handling and idempotent Celery worker retry semantics.     |
|                                                                                                    |
|  EXACTLY 3 PRIORITISED NEXT STEPS                                                                  |
|  1. Review Lesson 4.2: "Idempotent Consumers and Outbox Pattern in Celery".    [Launch Lesson]     |
|  2. Complete Interactive Debugging Lab: "Troubleshooting Redis Deadlocks".     [Start Lab]         |
|  3. Schedule a 30-min Teach-Back session with Mentor Rajesh Mohan in Grove.     [Book Slot]         |
+----------------------------------------------------------------------------------------------------+
```

---

## 4. Consent Passport & Access Receipts (`/privacy`)

```text
+----------------------------------------------------------------------------------------------------+
|  CONSENT PASSPORT & DATA SOVEREIGNTY (India DPDP Act Compliance)                                  |
|  Manage your active consents, inspect who has viewed your personal data, and control sharing.      |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  ACTIVE CONSENT PURPOSES                                                                           |
|  +----------------------------------------------------------------------------------------------+  |
|  | 1. Manager Aggregated Growth Ring Summary                                [ STATUS: GRANTED ] |  |
|  |    Purpose: Allows your direct manager to view consented skill summaries to support 1:1s.   |  |
|  |    Granted: Oct 12, 2026 | [ Revoke Consent in 1-Click ]                                     |  |
|  +----------------------------------------------------------------------------------------------+  |
|  | 2. Opportunities Internal Talent Marketplace Matching                    [ STATUS: GRANTED ] |  |
|  |    Purpose: Recommends stretch projects and gig shadowing based on your Growth Ring skills.  |  |
|  |    Granted: Oct 15, 2026 | [ Revoke Consent in 1-Click ]                                     |  |
|  +----------------------------------------------------------------------------------------------+  |
|  | 3. Developmental Psychometrics & Work Values Reflection                  [ STATUS: OPTED OUT]|  |
|  |    Purpose: Voluntary self-reflection. Raw data is encrypted; never shared or evaluated.     |  |
|  |    [ Opt In to Voluntary Psychometrics ]                                                     |  |
|  +----------------------------------------------------------------------------------------------+  |
|                                                                                                    |
|  ACCESS RECEIPTS AUDIT LOG (Transparent Proof of Who Read Your Data)                               |
|  +---------------------+-------------------+-------------------------------+---------------------+  |
|  | Timestamp           | Accessor          | Data Category Accessed        | Purpose Reference   |  |
|  +---------------------+-------------------+-------------------------------+---------------------+  |
|  | 2026-11-12 16:42:10 | Vikram Malhotra   | Consented Growth Ring Summary | 1:1 Prep Meeting    |  |
|  | 2026-11-08 10:15:32 | Opportunities Sys | Skills Graph Fit Vector       | Stretch Gig Match   |  |
|  | 2026-11-01 09:30:00 | HR Compliance Hub | Induction Milestone Checklist | Onboarding Audit    |  |
|  +---------------------+-------------------+-------------------------------+---------------------+  |
|                                                                                                    |
|  DATA PORTABILITY & ERASURE                                                                        |
|  [ Download My Skills Passport (JSON-LD / W3C VC) ]       [ Request Right to Erasure / Purge ]    |
+----------------------------------------------------------------------------------------------------+
```

---

## 5. Tamper-Evident Evidence View (`/growth-ring/evidence`)

```text
+----------------------------------------------------------------------------------------------------+
|  TAMPER-EVIDENT EVIDENCE LEDGER: Priya S. [Pseudonym: 7f8a9b2c...]            [Verify Chain Integrity]
|  Status: ALL BLOCKS VERIFIED (Signed Checkpoint: 2026-11-13 00:00 UTC - Signature Valid)          |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  Chain: Sequence #1 -> #2 -> #3 -> #4 (Append-Only SHA-256 Hash Chained with RFC 8785)             |
|                                                                                                    |
|  +----------------------------------------------------------------------------------------------+  |
|  | BLOCK #4 | Sequence: 4 | Recorded: 2026-11-13 09:15:22 UTC | Weight: 0.85 | Decay Half-Life: 180d |
|  | Skill: Python Core -> Async Architecture                                                     |  |
|  | Evidence Source: Assessment #GC-2026-884 (Growth Check)                                      |  |
|  | Verified By: Auto-Scored Sandbox (Test Cases 14/14 Passed)                                    |  |
|  |                                                                                              |  |
|  | Prev Block Hash: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855          |  |
|  | Canonical Data Hash: 8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4     |  |
|  | Current Block Hash:  4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b     |  |
|  | [ View Off-Chain Evidence Detail ]                                 [ Status: Cryptographically OK ] |
|  +----------------------------------------------------------------------------------------------+  |
|                                                                                                    |
|  +----------------------------------------------------------------------------------------------+  |
|  | BLOCK #3 | Sequence: 3 | Recorded: 2026-11-02 14:30:10 UTC | Weight: 0.70 | Decay Half-Life: 180d |
|  | Skill: System Design -> Database Migrations                                                  |  |
|  | Evidence Source: Greenhouse Idea Contribution (#GH-42 Shipped)                               |  |
|  | Verified By: Trainer Rajesh Mohan (Code Review & Merge)                                      |  |
|  | Prev Block Hash: 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b          |  |
|  | Current Block Hash:  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855     |  |
|  | [ View Off-Chain Evidence Detail ]                                 [ Status: Cryptographically OK ] |
|  +----------------------------------------------------------------------------------------------+  |
+----------------------------------------------------------------------------------------------------+
```
