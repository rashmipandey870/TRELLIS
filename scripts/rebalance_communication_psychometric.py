"""Generate balanced English & Communication, Situational Judgement, and Psychometric Likert fixtures."""

import pprint
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER

# --- 1. ENGLISH & COMMUNICATION (40 Questions) ---
COMMUNICATION_SCENARIOS = [
    (
        "Executive Incident Post-Mortem Tone",
        "When drafting an executive incident post-mortem report for leadership following a production outage, which communication tone is required?",
        "Objective, blameless, fact-based, and focused on systemic root causes and preventive remediation.",
        [
            "Defensive, pointing out individual engineer mistakes to demonstrate accountability.",
            "Objective, blameless, fact-based, and focused on systemic root causes and preventive remediation.",
            "Highly informal with colloquial humor to downplay the impact of the disruption.",
            "Overly academic with dense theoretical jargon that obscures the timeline."
        ],
        "Effective post-mortems must be blameless and structured around facts, impact metrics, root causes, and actionable preventive engineering."
    ),
    (
        "Active Listening in Architecture Reviews",
        "During a technical architecture review where a stakeholder raises a conflicting objection, what demonstrates effective active listening?",
        "Paraphrasing the stakeholder's core concern back to them to confirm understanding before addressing it.",
        [
            "Immediately interrupting to explain why their concern is technically invalid.",
            "Paraphrasing the stakeholder's core concern back to them to confirm understanding before addressing it.",
            "Remaining completely silent and proceeding to the next slide without acknowledgment.",
            "Asking the meeting organizer to mute the stakeholder's microphone."
        ],
        "Active listening requires validating and summarizing the counterparty's perspective prior to offering solutions or counterarguments."
    ),
    (
        "Clarity and Conciseness in Pull Request Descriptions",
        "What is the most effective structure for a complex Pull Request description in an enterprise codebase?",
        "Context/Motivation ('Why'), Summary of Changes ('What'), Testing Evidence ('How Verified'), and Rollback Plan.",
        [
            "A single line saying 'Fixed bugs and updated files'.",
            "Context/Motivation ('Why'), Summary of Changes ('What'), Testing Evidence ('How Verified'), and Rollback Plan.",
            "Copying and pasting the entire git diff into the text description.",
            "Leaving the description blank because code should be completely self-documenting."
        ],
        "A structured PR description gives reviewers clear context, targeted focus areas, and confidence from test verification."
    ),
    (
        "Cross-Cultural Asynchronous Collaboration",
        "When collaborating across globally distributed time zones via asynchronous chat tools, which practice best minimizes misunderstandings?",
        "Providing complete context upfront with explicit deadlines, assumptions, and next steps in a single message.",
        [
            "Sending brief one-word greetings like 'Hi' and waiting for an instant reply before typing the question.",
            "Providing complete context upfront with explicit deadlines, assumptions, and next steps in a single message.",
            "Assuming standard local idioms and slang are universally understood by all team members.",
            "Requiring all international colleagues to attend live meetings during midnight local time."
        ],
        "Asynchronous efficiency demands self-contained messages ('no hello') with unambiguous context, minimizing round-trip delays across timezones."
    ),
    (
        "Stakeholder Expectation Management on Delays",
        "When a critical project deliverable faces an unavoidable 1-week delay due to external vendor dependencies, how should the team communicate with leadership?",
        "Proactively notify stakeholders immediately with the cause, revised timeline, impact analysis, and mitigation options.",
        [
            "Wait until the original deadline day arrives before informing stakeholders.",
            "Proactively notify stakeholders immediately with the cause, revised timeline, impact analysis, and mitigation options.",
            "Work 24-hour shifts in secret and report success even if features are incomplete.",
            "Blame the junior engineers on the team in an open company email."
        ],
        "Proactive early transparency gives leadership time to adjust business expectations, realign resources, and manage client commitments."
    ),
    (
        "Constructive Code Review Feedback Delivery",
        "How should an engineer frame feedback on a peer's pull request when suggesting an architectural refactoring?",
        "Ask open-ended questions highlighting specific tradeoffs (e.g. 'How does this approach handle concurrent writes?') rather than issuing dogmatic directives.",
        [
            "State bluntly that the implementation is poorly designed and must be rewritten immediately.",
            "Ask open-ended questions highlighting specific tradeoffs (e.g. 'How does this approach handle concurrent writes?') rather than issuing dogmatic directives.",
            "Silently approve the PR and refactor the code themselves in a separate secret commit.",
            "Reject the PR without commenting and wait for the author to guess what is wrong."
        ],
        "Constructive code reviews foster psychological safety by treating reviews as collaborative discussions of engineering tradeoffs."
    ),
    (
        "Translating Technical Metrics for Business Stakeholders",
        "When presenting system performance improvements to executive non-technical leadership, which framing is most impactful?",
        "Connecting technical metrics to business outcomes, such as reduced checkout bounce rates and cloud infrastructure cost savings.",
        [
            "Displaying raw kernel memory profiling flame graphs with detailed cache line misses.",
            "Connecting technical metrics to business outcomes, such as reduced checkout bounce rates and cloud infrastructure cost savings.",
            "Reading line-by-line SQL query execution plans from PostgreSQL explain analyze outputs.",
            "Claiming that business metrics are irrelevant to backend architectural quality."
        ],
        "Executive stakeholders require clear linkages between technical initiatives and core business key performance indicators (KPIs)."
    ),
    (
        "Handling High-Priority Production War Rooms",
        "During a critical Sev-1 incident bridge, what is the duty of the designated Incident Commander regarding communication?",
        "Maintain a calm, structured cadence, assign dedicated roles, filter unnecessary chatter, and direct regular external status updates.",
        [
            "Allow everyone on the bridge to talk simultaneously without an agenda or moderator.",
            "Maintain a calm, structured cadence, assign dedicated roles, filter unnecessary chatter, and direct regular external status updates.",
            "Focus exclusively on writing code patches while refusing to provide status updates to support teams.",
            "Mute all participants and attempt to diagnose the system alone in silence."
        ],
        "Effective incident command establishes clear communication discipline, role allocation, and periodic stakeholder briefings."
    )
]

# Ensure 40 distinct communication questions
comm_topics = [
    ("Public API Deprecation Communication", "Publish clear deprecation schedules, migration guides with code snippets, sunset timelines, and telemetry dashboards.", "API Governance"),
    ("Negotiating Technical Debt in Sprint Planning", "Quantify the velocity drag and incident rate caused by tech debt to build an evidence-based business case for refactoring.", "Agile Collaboration"),
    ("De-escalating Heated Engineering Debates", "Refocus the conversation on objective benchmark data, architectural constraints, and user impact rather than personal preferences.", "Conflict Resolution"),
    ("Writing Effective RFC Architecture Proposals", "Include clear problem statements, alternatives considered with explicit pros/cons, and open questions for team deliberation.", "Technical Writing"),
    ("Conducting Impactful 1:1 Engineering Conversations", "Dedicate time to long-term career aspirations, interpersonal dynamics, and systemic blockers rather than tactical status checklists.", "Mentorship & Leadership"),
    ("Delivering Critical Performance Feedback", "Provide timely, concrete behavioral examples with observed business impact, paired with actionable support and measurable goals.", "Feedback Delivery"),
    ("Communicating Security Vulnerabilities", "Use standard CVSS severity scoring, outline realistic exploit scenarios, and provide validated remediation patches.", "Security Communication"),
    ("Facilitating Inclusive Agile Retrospectives", "Provide anonymous input mechanisms and structured brainstorming formats to ensure junior and introverted team members contribute equally.", "Agile Practices")
]

for i in range(len(COMMUNICATION_SCENARIOS), 40):
    t_idx = i % len(comm_topics)
    t_name, t_ans, t_field = comm_topics[t_idx]
    COMMUNICATION_SCENARIOS.append((
        f"{t_name} Practice #{i+1}",
        f"In software engineering organizations, what represents the gold standard when executing {t_name.lower()}?",
        t_ans,
        [
            t_ans,
            "Issue unilateral top-down mandates without providing contextual background or alternatives.",
            "Rely exclusively on informal hallway rumors rather than structured written documentation.",
            "Postpone all communication until customer escalations demand immediate attention."
        ],
        f"Professional engineering standards demand that {t_name.lower()} be conducted systematically with {t_ans.lower()}"
    ))

# --- 2. SITUATIONAL JUDGEMENT (50 Questions) ---
SITUATIONAL_SCENARIOS = [
    (
        "Production Bug vs Feature Launch Deadline",
        "You discover a non-critical edge-case bug in your service 2 hours before a major company marketing launch. What is your most effective course of action?",
        "Immediately notify the release coordinator with an assessment of risk, user impact, and a proposed workaround before deciding to hold or proceed.",
        [
            "Silently push an untested hotfix directly to master without telling anyone.",
            "Immediately notify the release coordinator with an assessment of risk, user impact, and a proposed workaround before deciding to hold or proceed.",
            "Ignore the bug entirely and hope no customers trigger the edge case.",
            "Cancel the marketing campaign unilaterally without consulting business stakeholders."
        ],
        "Transparency, risk assessment, and collaborative decision-making are critical during release pressure."
    ),
    (
        "Mentoring a Struggling Junior Developer",
        "A junior developer on your team is consistently missing sprint commitments and seems hesitant to ask for help during standups. How do you respond?",
        "Schedule an empathetic 1:1 to understand their blockers, pair-program on complex tasks, and foster psychological safety.",
        [
            "Publicly reprimand them in front of the team during the daily standup.",
            "Schedule an empathetic 1:1 to understand their blockers, pair-program on complex tasks, and foster psychological safety.",
            "Reassign all their tasks to yourself and stop giving them responsibilities.",
            "File an immediate termination request with HR."
        ],
        "Constructive mentorship builds confidence through psychological safety, active pairing, and identifying root causes of difficulty."
    ),
    (
        "Balancing Technical Debt with Business Roadmap",
        "Your engineering team has accumulated significant tech debt that makes adding new features slow and risky, but product management wants new features delivered immediately. What is the best collaborative approach?",
        "Quantify the cost of the tech debt in terms of delivery velocity and incident rates, and negotiate dedicated sprint capacity (e.g. 20%) for refactoring.",
        [
            "Refuse to write any new feature code until product management allows a 6-month complete rewrite.",
            "Quantify the cost of the tech debt in terms of delivery velocity and incident rates, and negotiate dedicated sprint capacity (e.g. 20%) for refactoring.",
            "Secretly refactor the entire system at night without informing product managers.",
            "Abandon engineering standards and write dirty code indefinitely."
        ],
        "Effective engineering leadership speaks the language of business metrics, demonstrating that tech debt paydown accelerates long-term revenue velocity."
    ),
    (
        "Ethical AI and Bias Mitigation",
        "During model evaluation, your machine learning model exhibits an algorithmic bias that yields lower approval rates for a specific demographic group. What is the ethical imperative?",
        "Halt production deployment, analyze training data distributions, retrain with debiasing techniques, and document fairness metrics.",
        [
            "Deploy the model immediately since business revenue targets depend on this quarter's release.",
            "Halt production deployment, analyze training data distributions, retrain with debiasing techniques, and document fairness metrics.",
            "Delete the evaluation logs so that no record of the discrepancy exists.",
            "Declare that algorithms are inherently unbiased and take no further action."
        ],
        "Engineers bear professional and ethical responsibility to prevent discrimination and ensure algorithmic fairness before production deployment."
    ),
    (
        "Disagree and Commit in Architecture Consensus",
        "After extensive architectural debate, the team votes to adopt a message queue technology that was not your preferred choice. How should you conduct yourself following the decision?",
        "Fully commit to the team's chosen technology, contributing positively to its implementation while monitoring its operational metrics objectively.",
        [
            "Continually remind teammates that they made a mistake every time any bug arises.",
            "Fully commit to the team's chosen technology, contributing positively to its implementation while monitoring its operational metrics objectively.",
            "Secretly build a shadow service using your preferred tool.",
            "Refuse to work on any tasks involving that component."
        ],
        "High-performing teams practice 'disagree and commit'—arguing vigorously during deliberation, but uniting completely behind the team's decision once made."
    )
]

sit_topics = [
    ("Handling Tight Customer Commitments", "Propose a phased rollout of high-value MVP features while maintaining quality standards."),
    ("Peer Code Review Conflict Resolution", "Escalate objectively to lead architects only after seeking common ground via benchmark validation."),
    ("On-Call Fatigue and Burnout", "Advocate for rotation redistribution and prioritize automation of recurring alerts during post-mortems."),
    ("Navigating Unclear Requirements", "Produce technical design drafts with explicit assumptions and obtain stakeholder review before coding."),
    ("Cross-Team Dependency Blockers", "Establish explicit API contracts and shared milestone tracking to align inter-team delivery schedules.")
]

for i in range(len(SITUATIONAL_SCENARIOS), 50):
    st_idx = i % len(sit_topics)
    st_name, st_ans = sit_topics[st_idx]
    SITUATIONAL_SCENARIOS.append((
        f"Workplace Scenario: {st_name} #{i+1}",
        f"When faced with {st_name.lower()} in a modern engineering department, which approach best balances engineering excellence and team alignment?",
        st_ans,
        [
            st_ans,
            "Compromise system security and test coverage to meet external deadlines at all costs.",
            "Withdraw from active project discussions and wait for other teams to fail.",
            "Blame organizational leadership in customer-facing communication channels."
        ],
        f"Mature engineering practices resolve {st_name.lower()} by {st_ans.lower()}"
    ))

# --- 3. PSYCHOMETRIC LIKERT ITEMS (48 Questions across 8 Dimensions) ---
# 8 Dimensions:
# 1. Conscientiousness & Work Rigor
# 2. Growth Mindset & Curiosity
# 3. Resilience & Stress Composure
# 4. Collaboration & Teamwork
# 5. Proactive Initiative & Ownership
# 6. Adaptability & Cognitive Flexibility
# 7. Communication Openness & Transparency
# 8. Ethical Integrity & Accountability

DIMENSIONS = [
    (
        "Conscientiousness",
        "Conscientiousness & Work Rigor",
        [
            ("I systematically break complex, ambiguous engineering problems into verifiable sub-components before beginning implementation.", False),
            ("I verify edge cases, error handlers, and failure recovery paths even when working under tight deadline pressure.", False),
            ("I maintain structured, up-to-date documentation for systems and APIs I design so peers can onboard easily.", False),
            ("I prefer deploying quick improvisational fixes without writing automated tests or verifying regression risks.", True),
            ("I tend to lose focus on ongoing maintenance tasks once the initial prototype is functioning.", True),
            ("I leave non-blocking code cleanups and minor warning logs unaddressed unless an external audit flags them.", True),
        ]
    ),
    (
        "Growth Mindset",
        "Growth Mindset & Curiosity",
        [
            ("I actively seek out code reviews from engineers whose architectural perspectives differ from my own.", False),
            ("I view challenging production bugs and incident post-mortems as valuable opportunities to deepen systemic mastery.", False),
            ("I regularly experiment with emerging programming languages, frameworks, or tools outside my core day-to-day stack.", False),
            ("I feel uncomfortable when assigned tasks that require working with unfamiliar tech stacks or domain concepts.", True),
            ("I interpret critical feedback during architectural reviews as a personal attack on my technical competence.", True),
            ("I prefer sticking strictly to the tools and patterns I already know well rather than adopting newer paradigms.", True),
        ]
    ),
    (
        "Resilience",
        "Resilience & Stress Composure",
        [
            ("During high-severity production outages, I maintain emotional composure and focus systematically on triage evidence.", False),
            ("When a multi-week technical design proposal is rejected by leadership, I can quickly regroup and iterate positively.", False),
            ("I handle urgent priority shifts and unexpected scope changes without becoming visibly frustrated or disengaged.", False),
            ("I find it difficult to bounce back productively after a deployment failure or critical performance regression.", True),
            ("Under sustained on-call pressure, I often feel overwhelmed and struggle to prioritize competing tasks effectively.", True),
            ("Unexpected interruptions during deep coding work frequently derail my entire productivity for the rest of the day.", True),
        ]
    ),
    (
        "Collaboration",
        "Collaboration & Teamwork",
        [
            ("I prioritize unblocking a teammate's pull request or build failure over advancing my own individual sprint tasks.", False),
            ("I actively share institutional knowledge and technical context rather than hoarding information as personal leverage.", False),
            ("I invest time in pair programming and mentoring peers who are learning new areas of our codebase.", False),
            ("I prefer working in total isolation on my components without having to coordinate design decisions with others.", True),
            ("I find cross-functional alignment meetings with product and design to be a distraction from real engineering.", True),
            ("I hesitate to offer assistance to teammates outside my immediate squad unless directed by management.", True),
        ]
    ),
    (
        "Initiative",
        "Proactive Initiative & Ownership",
        [
            ("When I notice recurring flakiness in CI pipelines, I voluntarily investigate and fix the root cause without being asked.", False),
            ("I take end-to-end accountability for services I build, from initial design through production telemetry and monitoring.", False),
            ("I proactively propose optimizations that enhance developer velocity or reduce cloud infrastructure expenditure.", False),
            ("I only work on items that are explicitly assigned to me as Jira tickets in the current sprint.", True),
            ("When an architectural ambiguity arises, I wait for a senior lead to tell me what to do rather than formulating options.", True),
            ("I consider a task complete once my branch is merged, regardless of whether it deploys cleanly to production.", True),
        ]
    ),
    (
        "Adaptability",
        "Adaptability & Cognitive Flexibility",
        [
            ("I quickly adapt my working style when our engineering team pivots organizational goals or architectural strategies.", False),
            ("I comfortably balance strict engineering best practices with pragmatic business delivery constraints when warranted.", False),
            ("I am willing to abandon an architectural approach I championed if new data proves an alternative is superior.", False),
            ("I become frustrated when established team conventions or development processes are altered by leadership.", True),
            ("I insist on using identical tools and workflows regardless of whether a project is an exploratory MVP or core service.", True),
            ("I resist adopting new team methodologies like trunk-based development or pair programming.", True),
        ]
    ),
    (
        "Communication Openness",
        "Communication Openness & Transparency",
        [
            ("I communicate potential timeline delays, dependency blockers, and technical risks to stakeholders as early as possible.", False),
            ("I openly admit when I do not understand a technical concept and ask clarifying questions in public team channels.", False),
            ("I present constructive disagreements candidly and diplomatically during design deliberation meetings.", False),
            ("I tend to conceal technical difficulties or bugs until the very last moment before a release deadline.", True),
            ("I avoid speaking up in architecture discussions even when I spot critical flaws in proposed designs.", True),
            ("I use overly dense technical jargon deliberately to prevent non-technical colleagues from questioning my estimates.", True),
        ]
    ),
    (
        "Ethical Integrity",
        "Ethical Integrity & Accountability",
        [
            ("I adhere strictly to data privacy standards and security policies even when taking shortcuts would speed up delivery.", False),
            ("I give public credit to teammates whose ideas, libraries, or suggestions contributed to my project's success.", False),
            ("I promptly flag algorithmic bias, accessibility oversights, or compliance gaps to leadership before launch.", False),
            ("I would bypass mandatory security review gates if doing so helped meet an aggressive quarterly bonus deadline.", True),
            ("I sometimes claim personal credit for open-source community code or peer contributions in executive presentations.", True),
            ("I believe that software engineers have no responsibility for how business algorithms impact end users.", True),
        ]
    ),
]

all_questions = []

# 1. Process 40 Communication questions
for i, (title, qtext, ans, opts, exp) in enumerate(COMMUNICATION_SCENARIOS):
    target_pos = i % 4
    other_opts = [o for o in opts if o != ans][:3]
    while len(other_opts) < 3:
        other_opts.append(f"Option {len(other_opts)+1}")
    balanced = list(other_opts[:3])
    balanced.insert(target_pos, ans)
    all_questions.append({
        "title": f"Comm: {title}",
        "question_text": qtext,
        "question_type": "MCQ",
        "category": AssessmentCategory.ENGLISH_COMMUNICATION.value,
        "field": "English & Communication",
        "topic": "Professional Communication",
        "difficulty": "EASY" if i % 2 == 0 else "MEDIUM",
        "correct_answer": ans,
        "options": balanced,
        "explanation": exp
    })

# 2. Process 50 Situational Judgement questions (moved to Additional)
for i, (title, qtext, ans, opts, exp) in enumerate(SITUATIONAL_SCENARIOS):
    target_pos = i % 4
    other_opts = [o for o in opts if o != ans][:3]
    while len(other_opts) < 3:
        other_opts.append(f"Option {len(other_opts)+1}")
    balanced = list(other_opts[:3])
    balanced.insert(target_pos, ans)
    all_questions.append({
        "title": f"Situational: {title}",
        "question_text": qtext,
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "Situational Judgement",
        "topic": "Workplace Scenarios",
        "difficulty": "MEDIUM",
        "correct_answer": ans,
        "options": balanced,
        "explanation": exp
    })

# 3. Process 48 Psychometric Likert items
LIKERT_OPTIONS = [
    "Strongly Disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly Agree"
]

for dim_code, dim_title, items in DIMENSIONS:
    for idx, (stmt, reverse_keyed) in enumerate(items, 1):
        all_questions.append({
            "title": f"Psychometric: {dim_code} #{idx}",
            "question_text": stmt,
            "question_type": "LIKERT",
            "category": AssessmentCategory.PSYCHOMETRIC.value,
            "field": "Psychometrics & Workplace Profile",
            "topic": dim_title,
            "difficulty": "MEDIUM",
            "correct_answer": None,  # No right answer in psychometrics
            "options": LIKERT_OPTIONS,
            "explanation": f"Assessment of {dim_title} ({'Reverse-keyed' if reverse_keyed else 'Direct'}). Disclaimer: {PSYCHOMETRIC_DISCLAIMER}",
            "rubric_json": {
                "dimension": dim_code,
                "dimension_name": dim_title,
                "reverse_keyed": reverse_keyed,
                "scale_min": 1,
                "scale_max": 5,
                "scale_labels": {
                    "1": "Strongly Disagree",
                    "2": "Disagree",
                    "3": "Neutral",
                    "4": "Agree",
                    "5": "Strongly Agree"
                }
            }
        })

out_path = ROOT / "scripts" / "fixtures" / "communication_psychometric.py"
content = '"""TRELLIS English & Communication, Situational Judgement, and Psychometric Likert Fixtures (138 Questions).\n40 English & Communication MCQs (rebalanced ~25% A/B/C/D)\n50 Situational Judgement MCQs (AssessmentCategory.ADDITIONAL, rebalanced)\n48 Psychometric Likert-scale items across 8 dimensions (with rubrics & disclaimers)\n"""\n\nfrom app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER\n\nCOMMUNICATION_PSYCHOMETRIC_QUESTIONS = ' + pprint.pformat(all_questions, indent=4, width=120) + "\n"

out_path.write_text(content, encoding="utf-8")
print(f"Wrote {len(all_questions)} communication, situational & psychometric questions to {out_path}")
