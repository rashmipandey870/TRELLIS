# TRELLIS Platform Walkthrough & Manager Demo Script (15 Minutes)

Welcome to **TRELLIS**, the enterprise Learning & Knowledge governance portal built for **CSM Technologies**.
This guide provides a step-by-step walkthrough script for executive stakeholders, managers, and mentors demonstrating the end-to-end capabilities across all three enterprise roles.

---

## 🔑 Pre-Seeded Demo Accounts (One-Click Loaded)

All demo accounts are protected by Argon2id hashing and share the standard enterprise demo password:
`CSMTrellis2026!`

| Role | Name | Email | Focus Area |
| :--- | :--- | :--- | :--- |
| **Admin** | Rajesh Mohanty | `admin@csmtech.internal` | L&K Governance, User Provisioning, Batches, Audit Logs |
| **Mentor** | Soumya Ranjan Patnaik | `soumya.p@csmtech.internal` | Full-Stack & Cloud Architecture, Assessments, Spotlight |
| **Mentor** | Ananya Mishra | `ananya.m@csmtech.internal` | Data Engineering & AI Specialist, Rubric Evaluation |
| **Mentor** | Debashis Jena | `debashis.j@csmtech.internal` | Core Systems & Embedded Architecture |
| **Learner** | Priya Sharma | `learner1@csmtech.internal` | Batch Alpha, 14-Day Streak, Talent Spotlight Nominee |
| **Learner** | Vikram Malhotra | `learner11@csmtech.internal` | Batch Beta (DevOps), 18-Day Streak |
| **Learner** | Sandeep Panda | `learner21@csmtech.internal` | Batch Gamma (Data/AI), 28-Day Streak |

---

## ⏱ 15-Minute Step-by-Step Walkthrough

### Part 1: The Learner Experience (Priya Sharma - 5 Minutes)
1. **Sign In**: Navigate to `http://localhost:4200/login`.
   - Click the quick-fill button: **Learner: Priya Sharma** (`learner1@csmtech.internal`).
   - Click **Sign In**. You are immediately routed to `/learner/dashboard`.
2. **Dashboard Overview**:
   - Note the **14-day climbing streak badge** with 2 streak freezes remaining.
   - Review the **Current Pathway Progress** card and upcoming scheduled assessments.
3. **AI Practice Arena & Provenance**:
   - Click **Practice** in the navigation bar.
   - Select a topic (e.g. *Python* or *Cloud Architecture*).
   - Click **Start Drill**. Notice the **Truthful Provenance Badge** showing real model generation parameters (`ollama` / `cloud` / `curated`).
   - Answer an MCQ question to observe instant scoring, explanation rendering, and streak incrementing.
4. **Assessment & Coding Environment**:
   - Navigate to **Assessments**. Select the active *Core Python & Data Structures Assessment*.
   - View the Monaco code editor with syntax highlighting, language selector (Python, SQL, Java, JS, C++), and test case runner.
5. **Growth Ring Report & PDF Export**:
   - Navigate to **Results**. Click on Priya's completed *Foundational Technical Knowledge Baseline*.
   - View the interactive SVG spider/radar Growth Ring visualization displaying 5 competencies (Technical Knowledge, Problem Solving, Code Quality, Systems Architecture, Professional Execution).
   - Click **Download Growth Ring Report (PDF)** to generate the ReportLab vector PDF with signature verification blocks.
6. **The Gardener AI Copilot**:
   - Open the chatbot drawer at the bottom right.
   - Ask: *"What are my active course enrollments and upcoming deadlines?"*
   - Observe real-time Server-Sent Events (SSE) streaming answers sourced directly from Priya's database records.

---

### Part 2: The Mentor Experience (Soumya Patnaik - 5 Minutes)
1. **Switch Persona**: Sign out, return to `/login`, and click **Mentor: Soumya Patnaik** (`soumya.p@csmtech.internal`).
2. **Mentor Dashboard**:
   - Note the **Assigned Batches**: *Batch Alpha (Full Stack)* and *Batch Beta (Cloud & DevOps)*.
   - Inspect the **Learners Needing Attention Queue**: learners falling behind on velocity or with overdue attempts.
3. **Assessment Builder & Question Bank**:
   - Navigate to **Assessments**.
   - Browse the **Question Bank**: over 300 vetted questions categorized into the 7 CSM Enterprise Policy Categories (Technical Knowledge, Coding, English & Communication, Quantitative Aptitude, Logical Reasoning, Psychometric & Situational, and Additional).
   - Filter by category: choose *Psychometric & Situational* and note the mandatory non-clinical disclaimer.
4. **Subjective AI Rubric Evaluation**:
   - Open an assessment submission requiring manual evaluation.
   - Click **AI Rubric Evaluate**. Watch TRELLIS AI analyze the learner's response against structured criteria, returning suggested marks and constructive feedback.
5. **Talent Spotlight & Action Execution**:
   - Navigate to **Spotlight**.
   - Review Priya Sharma's alert: Dedication score **94.5**, 14-day streak, 92.5% accuracy.
   - Observe the audit-logged action: `SCHEDULE_INTERVIEW`, which automatically created a verified Teams meeting and notified Priya.
6. **Live Meeting Management**:
   - Navigate to **Meetings**. Review upcoming 1:1s and batch architectural workshops with validated links.

---

### Part 3: The Administrator & Governance Experience (Rajesh Mohanty - 5 Minutes)
1. **Switch Persona**: Sign out and click **Admin: Rajesh Mohanty** (`admin@csmtech.internal`).
2. **Governance Dashboard**:
   - View enterprise-wide metrics: 42 users, 4 active batches, 12 assessments, 160+ attempts, 570+ practice drills.
3. **Strict Role Isolation**:
   - Notice that Admin navigation does NOT offer assessment creation or meeting scheduling buttons (strictly reserved for Mentors).
4. **User Provisioning & One-Time Passwords (OTP)**:
   - Navigate to **Users**. Click **Add New User**.
   - Observe that no shared default password is ever used: TRELLIS generates a secure, randomized one-time password or invite link.
   - The newly provisioned account has `must_change_password=True`, forcing a password reset on first login.
5. **Immutable Audit Trail**:
   - Navigate to **Audit Logs**.
   - Review the tamper-evident log capturing logins, password changes, report approvals, and role updates with actor IDs, IP addresses, and before/after states.

---

## 🛡 Security Invariants Verified
- **No Shared Passwords**: Production users are forced to change temporary passwords upon first sign-in.
- **Argon2id Hashing**: Robust password hashing with modern salt parameters.
- **In-Memory JWT Access Tokens**: Eliminates XSS vulnerability in client storage.
- **Zero Leaked Secrets**: Filter-repo purge applied to entire repository history; environment variables strictly enforced.
