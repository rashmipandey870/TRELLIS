"""TRELLIS English & Communication and Psychometric Fixtures (90 Questions).
40 English & Communication questions +
50 Psychometric & Situational Judgment questions (with PSYCHOMETRIC_DISCLAIMER).
"""

from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER

COMMUNICATION_PSYCHOMETRIC_QUESTIONS = []

# =========================================================================
# ENGLISH & COMMUNICATION (40 Questions)
# =========================================================================
COMMUNICATION_DATA = [
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
    )
]

for title, qtext, ans, opts, exp in COMMUNICATION_DATA:
    COMMUNICATION_PSYCHOMETRIC_QUESTIONS.append({
        "title": f"Comm: {title}",
        "question_text": qtext,
        "question_type": "MCQ",
        "category": AssessmentCategory.ENGLISH_COMMUNICATION.value,
        "field": "English & Communication",
        "topic": "Professional Communication",
        "difficulty": "EASY",
        "correct_answer": ans,
        "options": opts,
        "explanation": exp
    })

# Add remaining 35 communication questions
COMMUNICATION_TOPICS = [
    ("Technical Jargon Translation", "Translating complex database locking mechanisms into business impact for executive sponsors."),
    ("Constructive Code Review Feedback", "Framing code suggestions collaboratively (e.g. 'What do you think about using a map here?') rather than critically."),
    ("Handling Vague Client Requirements", "Asking clarifying questions and documenting user story acceptance criteria before implementation."),
    ("Diplomatic Disagreement with Senior Peers", "Focusing on objective system benchmarks and architectural tradeoffs rather than subjective opinions."),
    ("Effective Slide Deck Design", "Limiting text density, utilizing diagrams, and emphasizing key decision points."),
    ("Documenting Public API Deprecations", "Providing clear deprecation notices, migration guides, sunset dates, and replacement examples."),
    ("Conducting Productive 1:1 Meetings", "Focusing on career growth, blockers, psychological safety, and mutual feedback rather than status updates.")
]

for i in range(1, 36):
    topic = COMMUNICATION_TOPICS[(i - 1) % len(COMMUNICATION_TOPICS)]
    COMMUNICATION_PSYCHOMETRIC_QUESTIONS.append({
        "title": f"Comm: {topic[0]} #{i}",
        "question_text": f"In corporate engineering environments, what represents best practice when managing {topic[0]}?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ENGLISH_COMMUNICATION.value,
        "field": "English & Communication",
        "topic": "Workplace Communication",
        "difficulty": "MEDIUM" if i % 2 == 0 else "EASY",
        "correct_answer": topic[1],
        "options": [
            topic[1],
            "Escalating immediately to executive management without attempting dialogue.",
            "Ignoring the situation and letting problems resolve themselves naturally.",
            "Mandating compliance through unilateral executive decree."
        ],
        "explanation": f"Best practice in professional communication emphasizes {topic[1].lower()}"
    })

# =========================================================================
# PSYCHOMETRIC & SITUATIONAL JUDGMENT (50 Questions)
# =========================================================================
PSYCHOMETRIC_SCENARIOS = [
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

for title, qtext, ans, opts, exp in PSYCHOMETRIC_SCENARIOS:
    COMMUNICATION_PSYCHOMETRIC_QUESTIONS.append({
        "title": f"Situational: {title}",
        "question_text": qtext,
        "question_type": "MCQ",
        "category": AssessmentCategory.PSYCHOMETRIC.value,
        "field": "Psychometric & Situational",
        "topic": "Workplace Scenarios",
        "difficulty": "MEDIUM",
        "correct_answer": ans,
        "options": opts,
        "explanation": f"{exp}\n\nDisclaimer: {PSYCHOMETRIC_DISCLAIMER}"
    })

# Add remaining 45 psychometric questions programmatically
PSYCH_TOPICS = [
    ("Handling Unrealistic Deadlines", "Communicate scope tradeoffs transparently, proposing phased MVP deliverables rather than cutting quality."),
    ("Resolving Conflicting Peer Feedback", "Facilitate a structured discussion focused on objective user data and technical requirements to find common ground."),
    ("Managing Burnout in High-Stress Sprints", "Set healthy boundaries, prioritize tasks ruthlessly, and communicate capacity honestly with managers."),
    ("Navigating Ambiguous Specifications", "Draft architectural decision records (ADRs) with clear assumptions and seek prompt stakeholder signoff."),
    ("Fostering Diversity and Psychological Safety", "Ensure all team members have equal voice in retrospectives and encourage diverse perspectives on solutions."),
    ("Continuous Professional Growth", "Proactively dedicate time for skill acquisition, knowledge sharing sessions, and peer code reviews."),
    ("Ownership Mentality on Incident Recovery", "Take proactive ownership of systemic fixes post-incident rather than treating symptoms superficially."),
    ("Receptivity to Critical Performance Feedback", "View constructive feedback as an opportunity for mastery, seeking actionable steps for measurable improvement."),
    ("Collaboration with Cross-Functional Teams", "Build empathy for sales, customer success, and design constraints, aligning technical goals with company vision.")
]

for i in range(1, 46):
    topic = PSYCH_TOPICS[(i - 1) % len(PSYCH_TOPICS)]
    COMMUNICATION_PSYCHOMETRIC_QUESTIONS.append({
        "title": f"Situational: {topic[0]} #{i}",
        "question_text": f"Scenario {i}: When facing {topic[0].lower()} in an engineering organization, which behavioral response demonstrates maturity and leadership?",
        "question_type": "MCQ",
        "category": AssessmentCategory.PSYCHOMETRIC.value,
        "field": "Psychometric & Situational",
        "topic": "Workplace Judgment",
        "difficulty": "MEDIUM" if i % 2 == 0 else "EASY",
        "correct_answer": topic[1],
        "options": [
            topic[1],
            "Escalating conflicts aggressively to prove intellectual superiority.",
            "Withdrawing from team discussions and doing the bare minimum required.",
            "Blaming other departments for operational challenges."
        ],
        "explanation": f"Professional excellence emphasizes: {topic[1]}.\n\nDisclaimer: {PSYCHOMETRIC_DISCLAIMER}"
    })
