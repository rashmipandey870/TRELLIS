"""TRELLIS English & Communication, Situational Judgement, and Psychometric Likert Fixtures (138 Questions).
40 English & Communication MCQs (rebalanced ~25% A/B/C/D)
50 Situational Judgement MCQs (AssessmentCategory.ADDITIONAL, rebalanced)
48 Psychometric Likert-scale items across 8 dimensions (with rubrics & disclaimers)
"""

from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER

COMMUNICATION_PSYCHOMETRIC_QUESTIONS = [   {   'category': 'English & Communication',
        'correct_answer': 'Objective, blameless, fact-based, and focused on systemic root causes and preventive '
                          'remediation.',
        'difficulty': 'EASY',
        'explanation': 'Effective post-mortems must be blameless and structured around facts, impact metrics, root '
                       'causes, and actionable preventive engineering.',
        'field': 'English & Communication',
        'options': [   'Objective, blameless, fact-based, and focused on systemic root causes and preventive '
                       'remediation.',
                       'Defensive, pointing out individual engineer mistakes to demonstrate accountability.',
                       'Highly informal with colloquial humor to downplay the impact of the disruption.',
                       'Overly academic with dense theoretical jargon that obscures the timeline.'],
        'question_text': 'When drafting an executive incident post-mortem report for leadership following a production '
                         'outage, which communication tone is required?',
        'question_type': 'MCQ',
        'title': 'Comm: Executive Incident Post-Mortem Tone',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': "Paraphrasing the stakeholder's core concern back to them to confirm understanding before "
                          'addressing it.',
        'difficulty': 'MEDIUM',
        'explanation': "Active listening requires validating and summarizing the counterparty's perspective prior to "
                       'offering solutions or counterarguments.',
        'field': 'English & Communication',
        'options': [   'Immediately interrupting to explain why their concern is technically invalid.',
                       "Paraphrasing the stakeholder's core concern back to them to confirm understanding before "
                       'addressing it.',
                       'Remaining completely silent and proceeding to the next slide without acknowledgment.',
                       "Asking the meeting organizer to mute the stakeholder's microphone."],
        'question_text': 'During a technical architecture review where a stakeholder raises a conflicting objection, '
                         'what demonstrates effective active listening?',
        'question_type': 'MCQ',
        'title': 'Comm: Active Listening in Architecture Reviews',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': "Context/Motivation ('Why'), Summary of Changes ('What'), Testing Evidence ('How Verified'), "
                          'and Rollback Plan.',
        'difficulty': 'EASY',
        'explanation': 'A structured PR description gives reviewers clear context, targeted focus areas, and '
                       'confidence from test verification.',
        'field': 'English & Communication',
        'options': [   "A single line saying 'Fixed bugs and updated files'.",
                       'Copying and pasting the entire git diff into the text description.',
                       "Context/Motivation ('Why'), Summary of Changes ('What'), Testing Evidence ('How Verified'), "
                       'and Rollback Plan.',
                       'Leaving the description blank because code should be completely self-documenting.'],
        'question_text': 'What is the most effective structure for a complex Pull Request description in an enterprise '
                         'codebase?',
        'question_type': 'MCQ',
        'title': 'Comm: Clarity and Conciseness in Pull Request Descriptions',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Providing complete context upfront with explicit deadlines, assumptions, and next steps in '
                          'a single message.',
        'difficulty': 'MEDIUM',
        'explanation': "Asynchronous efficiency demands self-contained messages ('no hello') with unambiguous context, "
                       'minimizing round-trip delays across timezones.',
        'field': 'English & Communication',
        'options': [   "Sending brief one-word greetings like 'Hi' and waiting for an instant reply before typing the "
                       'question.',
                       'Assuming standard local idioms and slang are universally understood by all team members.',
                       'Requiring all international colleagues to attend live meetings during midnight local time.',
                       'Providing complete context upfront with explicit deadlines, assumptions, and next steps in a '
                       'single message.'],
        'question_text': 'When collaborating across globally distributed time zones via asynchronous chat tools, which '
                         'practice best minimizes misunderstandings?',
        'question_type': 'MCQ',
        'title': 'Comm: Cross-Cultural Asynchronous Collaboration',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Proactively notify stakeholders immediately with the cause, revised timeline, impact '
                          'analysis, and mitigation options.',
        'difficulty': 'EASY',
        'explanation': 'Proactive early transparency gives leadership time to adjust business expectations, realign '
                       'resources, and manage client commitments.',
        'field': 'English & Communication',
        'options': [   'Proactively notify stakeholders immediately with the cause, revised timeline, impact analysis, '
                       'and mitigation options.',
                       'Wait until the original deadline day arrives before informing stakeholders.',
                       'Work 24-hour shifts in secret and report success even if features are incomplete.',
                       'Blame the junior engineers on the team in an open company email.'],
        'question_text': 'When a critical project deliverable faces an unavoidable 1-week delay due to external vendor '
                         'dependencies, how should the team communicate with leadership?',
        'question_type': 'MCQ',
        'title': 'Comm: Stakeholder Expectation Management on Delays',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': "Ask open-ended questions highlighting specific tradeoffs (e.g. 'How does this approach "
                          "handle concurrent writes?') rather than issuing dogmatic directives.",
        'difficulty': 'MEDIUM',
        'explanation': 'Constructive code reviews foster psychological safety by treating reviews as collaborative '
                       'discussions of engineering tradeoffs.',
        'field': 'English & Communication',
        'options': [   'State bluntly that the implementation is poorly designed and must be rewritten immediately.',
                       "Ask open-ended questions highlighting specific tradeoffs (e.g. 'How does this approach handle "
                       "concurrent writes?') rather than issuing dogmatic directives.",
                       'Silently approve the PR and refactor the code themselves in a separate secret commit.',
                       'Reject the PR without commenting and wait for the author to guess what is wrong.'],
        'question_text': "How should an engineer frame feedback on a peer's pull request when suggesting an "
                         'architectural refactoring?',
        'question_type': 'MCQ',
        'title': 'Comm: Constructive Code Review Feedback Delivery',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Connecting technical metrics to business outcomes, such as reduced checkout bounce rates '
                          'and cloud infrastructure cost savings.',
        'difficulty': 'EASY',
        'explanation': 'Executive stakeholders require clear linkages between technical initiatives and core business '
                       'key performance indicators (KPIs).',
        'field': 'English & Communication',
        'options': [   'Displaying raw kernel memory profiling flame graphs with detailed cache line misses.',
                       'Reading line-by-line SQL query execution plans from PostgreSQL explain analyze outputs.',
                       'Connecting technical metrics to business outcomes, such as reduced checkout bounce rates and '
                       'cloud infrastructure cost savings.',
                       'Claiming that business metrics are irrelevant to backend architectural quality.'],
        'question_text': 'When presenting system performance improvements to executive non-technical leadership, which '
                         'framing is most impactful?',
        'question_type': 'MCQ',
        'title': 'Comm: Translating Technical Metrics for Business Stakeholders',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Maintain a calm, structured cadence, assign dedicated roles, filter unnecessary chatter, '
                          'and direct regular external status updates.',
        'difficulty': 'MEDIUM',
        'explanation': 'Effective incident command establishes clear communication discipline, role allocation, and '
                       'periodic stakeholder briefings.',
        'field': 'English & Communication',
        'options': [   'Allow everyone on the bridge to talk simultaneously without an agenda or moderator.',
                       'Focus exclusively on writing code patches while refusing to provide status updates to support '
                       'teams.',
                       'Mute all participants and attempt to diagnose the system alone in silence.',
                       'Maintain a calm, structured cadence, assign dedicated roles, filter unnecessary chatter, and '
                       'direct regular external status updates.'],
        'question_text': 'During a critical Sev-1 incident bridge, what is the duty of the designated Incident '
                         'Commander regarding communication?',
        'question_type': 'MCQ',
        'title': 'Comm: Handling High-Priority Production War Rooms',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Publish clear deprecation schedules, migration guides with code snippets, sunset timelines, '
                          'and telemetry dashboards.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that public api deprecation communication be '
                       'conducted systematically with publish clear deprecation schedules, migration guides with code '
                       'snippets, sunset timelines, and telemetry dashboards.',
        'field': 'English & Communication',
        'options': [   'Publish clear deprecation schedules, migration guides with code snippets, sunset timelines, '
                       'and telemetry dashboards.',
                       'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'public api deprecation communication?',
        'question_type': 'MCQ',
        'title': 'Comm: Public API Deprecation Communication Practice #9',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Quantify the velocity drag and incident rate caused by tech debt to build an evidence-based '
                          'business case for refactoring.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that negotiating technical debt in sprint planning '
                       'be conducted systematically with quantify the velocity drag and incident rate caused by tech '
                       'debt to build an evidence-based business case for refactoring.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Quantify the velocity drag and incident rate caused by tech debt to build an evidence-based '
                       'business case for refactoring.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'negotiating technical debt in sprint planning?',
        'question_type': 'MCQ',
        'title': 'Comm: Negotiating Technical Debt in Sprint Planning Practice #10',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Refocus the conversation on objective benchmark data, architectural constraints, and user '
                          'impact rather than personal preferences.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that de-escalating heated engineering debates be '
                       'conducted systematically with refocus the conversation on objective benchmark data, '
                       'architectural constraints, and user impact rather than personal preferences.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Refocus the conversation on objective benchmark data, architectural constraints, and user '
                       'impact rather than personal preferences.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'de-escalating heated engineering debates?',
        'question_type': 'MCQ',
        'title': 'Comm: De-escalating Heated Engineering Debates Practice #11',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Include clear problem statements, alternatives considered with explicit pros/cons, and open '
                          'questions for team deliberation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that writing effective rfc architecture proposals be '
                       'conducted systematically with include clear problem statements, alternatives considered with '
                       'explicit pros/cons, and open questions for team deliberation.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.',
                       'Include clear problem statements, alternatives considered with explicit pros/cons, and open '
                       'questions for team deliberation.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'writing effective rfc architecture proposals?',
        'question_type': 'MCQ',
        'title': 'Comm: Writing Effective RFC Architecture Proposals Practice #12',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Dedicate time to long-term career aspirations, interpersonal dynamics, and systemic '
                          'blockers rather than tactical status checklists.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that conducting impactful 1:1 engineering '
                       'conversations be conducted systematically with dedicate time to long-term career aspirations, '
                       'interpersonal dynamics, and systemic blockers rather than tactical status checklists.',
        'field': 'English & Communication',
        'options': [   'Dedicate time to long-term career aspirations, interpersonal dynamics, and systemic blockers '
                       'rather than tactical status checklists.',
                       'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'conducting impactful 1:1 engineering conversations?',
        'question_type': 'MCQ',
        'title': 'Comm: Conducting Impactful 1:1 Engineering Conversations Practice #13',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Provide timely, concrete behavioral examples with observed business impact, paired with '
                          'actionable support and measurable goals.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that delivering critical performance feedback be '
                       'conducted systematically with provide timely, concrete behavioral examples with observed '
                       'business impact, paired with actionable support and measurable goals.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Provide timely, concrete behavioral examples with observed business impact, paired with '
                       'actionable support and measurable goals.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'delivering critical performance feedback?',
        'question_type': 'MCQ',
        'title': 'Comm: Delivering Critical Performance Feedback Practice #14',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Use standard CVSS severity scoring, outline realistic exploit scenarios, and provide '
                          'validated remediation patches.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that communicating security vulnerabilities be '
                       'conducted systematically with use standard cvss severity scoring, outline realistic exploit '
                       'scenarios, and provide validated remediation patches.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Use standard CVSS severity scoring, outline realistic exploit scenarios, and provide validated '
                       'remediation patches.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'communicating security vulnerabilities?',
        'question_type': 'MCQ',
        'title': 'Comm: Communicating Security Vulnerabilities Practice #15',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Provide anonymous input mechanisms and structured brainstorming formats to ensure junior '
                          'and introverted team members contribute equally.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that facilitating inclusive agile retrospectives be '
                       'conducted systematically with provide anonymous input mechanisms and structured brainstorming '
                       'formats to ensure junior and introverted team members contribute equally.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.',
                       'Provide anonymous input mechanisms and structured brainstorming formats to ensure junior and '
                       'introverted team members contribute equally.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'facilitating inclusive agile retrospectives?',
        'question_type': 'MCQ',
        'title': 'Comm: Facilitating Inclusive Agile Retrospectives Practice #16',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Publish clear deprecation schedules, migration guides with code snippets, sunset timelines, '
                          'and telemetry dashboards.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that public api deprecation communication be '
                       'conducted systematically with publish clear deprecation schedules, migration guides with code '
                       'snippets, sunset timelines, and telemetry dashboards.',
        'field': 'English & Communication',
        'options': [   'Publish clear deprecation schedules, migration guides with code snippets, sunset timelines, '
                       'and telemetry dashboards.',
                       'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'public api deprecation communication?',
        'question_type': 'MCQ',
        'title': 'Comm: Public API Deprecation Communication Practice #17',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Quantify the velocity drag and incident rate caused by tech debt to build an evidence-based '
                          'business case for refactoring.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that negotiating technical debt in sprint planning '
                       'be conducted systematically with quantify the velocity drag and incident rate caused by tech '
                       'debt to build an evidence-based business case for refactoring.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Quantify the velocity drag and incident rate caused by tech debt to build an evidence-based '
                       'business case for refactoring.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'negotiating technical debt in sprint planning?',
        'question_type': 'MCQ',
        'title': 'Comm: Negotiating Technical Debt in Sprint Planning Practice #18',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Refocus the conversation on objective benchmark data, architectural constraints, and user '
                          'impact rather than personal preferences.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that de-escalating heated engineering debates be '
                       'conducted systematically with refocus the conversation on objective benchmark data, '
                       'architectural constraints, and user impact rather than personal preferences.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Refocus the conversation on objective benchmark data, architectural constraints, and user '
                       'impact rather than personal preferences.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'de-escalating heated engineering debates?',
        'question_type': 'MCQ',
        'title': 'Comm: De-escalating Heated Engineering Debates Practice #19',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Include clear problem statements, alternatives considered with explicit pros/cons, and open '
                          'questions for team deliberation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that writing effective rfc architecture proposals be '
                       'conducted systematically with include clear problem statements, alternatives considered with '
                       'explicit pros/cons, and open questions for team deliberation.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.',
                       'Include clear problem statements, alternatives considered with explicit pros/cons, and open '
                       'questions for team deliberation.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'writing effective rfc architecture proposals?',
        'question_type': 'MCQ',
        'title': 'Comm: Writing Effective RFC Architecture Proposals Practice #20',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Dedicate time to long-term career aspirations, interpersonal dynamics, and systemic '
                          'blockers rather than tactical status checklists.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that conducting impactful 1:1 engineering '
                       'conversations be conducted systematically with dedicate time to long-term career aspirations, '
                       'interpersonal dynamics, and systemic blockers rather than tactical status checklists.',
        'field': 'English & Communication',
        'options': [   'Dedicate time to long-term career aspirations, interpersonal dynamics, and systemic blockers '
                       'rather than tactical status checklists.',
                       'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'conducting impactful 1:1 engineering conversations?',
        'question_type': 'MCQ',
        'title': 'Comm: Conducting Impactful 1:1 Engineering Conversations Practice #21',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Provide timely, concrete behavioral examples with observed business impact, paired with '
                          'actionable support and measurable goals.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that delivering critical performance feedback be '
                       'conducted systematically with provide timely, concrete behavioral examples with observed '
                       'business impact, paired with actionable support and measurable goals.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Provide timely, concrete behavioral examples with observed business impact, paired with '
                       'actionable support and measurable goals.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'delivering critical performance feedback?',
        'question_type': 'MCQ',
        'title': 'Comm: Delivering Critical Performance Feedback Practice #22',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Use standard CVSS severity scoring, outline realistic exploit scenarios, and provide '
                          'validated remediation patches.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that communicating security vulnerabilities be '
                       'conducted systematically with use standard cvss severity scoring, outline realistic exploit '
                       'scenarios, and provide validated remediation patches.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Use standard CVSS severity scoring, outline realistic exploit scenarios, and provide validated '
                       'remediation patches.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'communicating security vulnerabilities?',
        'question_type': 'MCQ',
        'title': 'Comm: Communicating Security Vulnerabilities Practice #23',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Provide anonymous input mechanisms and structured brainstorming formats to ensure junior '
                          'and introverted team members contribute equally.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that facilitating inclusive agile retrospectives be '
                       'conducted systematically with provide anonymous input mechanisms and structured brainstorming '
                       'formats to ensure junior and introverted team members contribute equally.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.',
                       'Provide anonymous input mechanisms and structured brainstorming formats to ensure junior and '
                       'introverted team members contribute equally.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'facilitating inclusive agile retrospectives?',
        'question_type': 'MCQ',
        'title': 'Comm: Facilitating Inclusive Agile Retrospectives Practice #24',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Publish clear deprecation schedules, migration guides with code snippets, sunset timelines, '
                          'and telemetry dashboards.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that public api deprecation communication be '
                       'conducted systematically with publish clear deprecation schedules, migration guides with code '
                       'snippets, sunset timelines, and telemetry dashboards.',
        'field': 'English & Communication',
        'options': [   'Publish clear deprecation schedules, migration guides with code snippets, sunset timelines, '
                       'and telemetry dashboards.',
                       'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'public api deprecation communication?',
        'question_type': 'MCQ',
        'title': 'Comm: Public API Deprecation Communication Practice #25',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Quantify the velocity drag and incident rate caused by tech debt to build an evidence-based '
                          'business case for refactoring.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that negotiating technical debt in sprint planning '
                       'be conducted systematically with quantify the velocity drag and incident rate caused by tech '
                       'debt to build an evidence-based business case for refactoring.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Quantify the velocity drag and incident rate caused by tech debt to build an evidence-based '
                       'business case for refactoring.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'negotiating technical debt in sprint planning?',
        'question_type': 'MCQ',
        'title': 'Comm: Negotiating Technical Debt in Sprint Planning Practice #26',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Refocus the conversation on objective benchmark data, architectural constraints, and user '
                          'impact rather than personal preferences.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that de-escalating heated engineering debates be '
                       'conducted systematically with refocus the conversation on objective benchmark data, '
                       'architectural constraints, and user impact rather than personal preferences.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Refocus the conversation on objective benchmark data, architectural constraints, and user '
                       'impact rather than personal preferences.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'de-escalating heated engineering debates?',
        'question_type': 'MCQ',
        'title': 'Comm: De-escalating Heated Engineering Debates Practice #27',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Include clear problem statements, alternatives considered with explicit pros/cons, and open '
                          'questions for team deliberation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that writing effective rfc architecture proposals be '
                       'conducted systematically with include clear problem statements, alternatives considered with '
                       'explicit pros/cons, and open questions for team deliberation.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.',
                       'Include clear problem statements, alternatives considered with explicit pros/cons, and open '
                       'questions for team deliberation.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'writing effective rfc architecture proposals?',
        'question_type': 'MCQ',
        'title': 'Comm: Writing Effective RFC Architecture Proposals Practice #28',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Dedicate time to long-term career aspirations, interpersonal dynamics, and systemic '
                          'blockers rather than tactical status checklists.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that conducting impactful 1:1 engineering '
                       'conversations be conducted systematically with dedicate time to long-term career aspirations, '
                       'interpersonal dynamics, and systemic blockers rather than tactical status checklists.',
        'field': 'English & Communication',
        'options': [   'Dedicate time to long-term career aspirations, interpersonal dynamics, and systemic blockers '
                       'rather than tactical status checklists.',
                       'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'conducting impactful 1:1 engineering conversations?',
        'question_type': 'MCQ',
        'title': 'Comm: Conducting Impactful 1:1 Engineering Conversations Practice #29',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Provide timely, concrete behavioral examples with observed business impact, paired with '
                          'actionable support and measurable goals.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that delivering critical performance feedback be '
                       'conducted systematically with provide timely, concrete behavioral examples with observed '
                       'business impact, paired with actionable support and measurable goals.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Provide timely, concrete behavioral examples with observed business impact, paired with '
                       'actionable support and measurable goals.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'delivering critical performance feedback?',
        'question_type': 'MCQ',
        'title': 'Comm: Delivering Critical Performance Feedback Practice #30',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Use standard CVSS severity scoring, outline realistic exploit scenarios, and provide '
                          'validated remediation patches.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that communicating security vulnerabilities be '
                       'conducted systematically with use standard cvss severity scoring, outline realistic exploit '
                       'scenarios, and provide validated remediation patches.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Use standard CVSS severity scoring, outline realistic exploit scenarios, and provide validated '
                       'remediation patches.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'communicating security vulnerabilities?',
        'question_type': 'MCQ',
        'title': 'Comm: Communicating Security Vulnerabilities Practice #31',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Provide anonymous input mechanisms and structured brainstorming formats to ensure junior '
                          'and introverted team members contribute equally.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that facilitating inclusive agile retrospectives be '
                       'conducted systematically with provide anonymous input mechanisms and structured brainstorming '
                       'formats to ensure junior and introverted team members contribute equally.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.',
                       'Provide anonymous input mechanisms and structured brainstorming formats to ensure junior and '
                       'introverted team members contribute equally.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'facilitating inclusive agile retrospectives?',
        'question_type': 'MCQ',
        'title': 'Comm: Facilitating Inclusive Agile Retrospectives Practice #32',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Publish clear deprecation schedules, migration guides with code snippets, sunset timelines, '
                          'and telemetry dashboards.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that public api deprecation communication be '
                       'conducted systematically with publish clear deprecation schedules, migration guides with code '
                       'snippets, sunset timelines, and telemetry dashboards.',
        'field': 'English & Communication',
        'options': [   'Publish clear deprecation schedules, migration guides with code snippets, sunset timelines, '
                       'and telemetry dashboards.',
                       'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'public api deprecation communication?',
        'question_type': 'MCQ',
        'title': 'Comm: Public API Deprecation Communication Practice #33',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Quantify the velocity drag and incident rate caused by tech debt to build an evidence-based '
                          'business case for refactoring.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that negotiating technical debt in sprint planning '
                       'be conducted systematically with quantify the velocity drag and incident rate caused by tech '
                       'debt to build an evidence-based business case for refactoring.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Quantify the velocity drag and incident rate caused by tech debt to build an evidence-based '
                       'business case for refactoring.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'negotiating technical debt in sprint planning?',
        'question_type': 'MCQ',
        'title': 'Comm: Negotiating Technical Debt in Sprint Planning Practice #34',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Refocus the conversation on objective benchmark data, architectural constraints, and user '
                          'impact rather than personal preferences.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that de-escalating heated engineering debates be '
                       'conducted systematically with refocus the conversation on objective benchmark data, '
                       'architectural constraints, and user impact rather than personal preferences.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Refocus the conversation on objective benchmark data, architectural constraints, and user '
                       'impact rather than personal preferences.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'de-escalating heated engineering debates?',
        'question_type': 'MCQ',
        'title': 'Comm: De-escalating Heated Engineering Debates Practice #35',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Include clear problem statements, alternatives considered with explicit pros/cons, and open '
                          'questions for team deliberation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that writing effective rfc architecture proposals be '
                       'conducted systematically with include clear problem statements, alternatives considered with '
                       'explicit pros/cons, and open questions for team deliberation.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.',
                       'Include clear problem statements, alternatives considered with explicit pros/cons, and open '
                       'questions for team deliberation.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'writing effective rfc architecture proposals?',
        'question_type': 'MCQ',
        'title': 'Comm: Writing Effective RFC Architecture Proposals Practice #36',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Dedicate time to long-term career aspirations, interpersonal dynamics, and systemic '
                          'blockers rather than tactical status checklists.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that conducting impactful 1:1 engineering '
                       'conversations be conducted systematically with dedicate time to long-term career aspirations, '
                       'interpersonal dynamics, and systemic blockers rather than tactical status checklists.',
        'field': 'English & Communication',
        'options': [   'Dedicate time to long-term career aspirations, interpersonal dynamics, and systemic blockers '
                       'rather than tactical status checklists.',
                       'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'conducting impactful 1:1 engineering conversations?',
        'question_type': 'MCQ',
        'title': 'Comm: Conducting Impactful 1:1 Engineering Conversations Practice #37',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Provide timely, concrete behavioral examples with observed business impact, paired with '
                          'actionable support and measurable goals.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that delivering critical performance feedback be '
                       'conducted systematically with provide timely, concrete behavioral examples with observed '
                       'business impact, paired with actionable support and measurable goals.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Provide timely, concrete behavioral examples with observed business impact, paired with '
                       'actionable support and measurable goals.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'delivering critical performance feedback?',
        'question_type': 'MCQ',
        'title': 'Comm: Delivering Critical Performance Feedback Practice #38',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Use standard CVSS severity scoring, outline realistic exploit scenarios, and provide '
                          'validated remediation patches.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering standards demand that communicating security vulnerabilities be '
                       'conducted systematically with use standard cvss severity scoring, outline realistic exploit '
                       'scenarios, and provide validated remediation patches.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Use standard CVSS severity scoring, outline realistic exploit scenarios, and provide validated '
                       'remediation patches.',
                       'Postpone all communication until customer escalations demand immediate attention.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'communicating security vulnerabilities?',
        'question_type': 'MCQ',
        'title': 'Comm: Communicating Security Vulnerabilities Practice #39',
        'topic': 'Professional Communication'},
    {   'category': 'English & Communication',
        'correct_answer': 'Provide anonymous input mechanisms and structured brainstorming formats to ensure junior '
                          'and introverted team members contribute equally.',
        'difficulty': 'MEDIUM',
        'explanation': 'Professional engineering standards demand that facilitating inclusive agile retrospectives be '
                       'conducted systematically with provide anonymous input mechanisms and structured brainstorming '
                       'formats to ensure junior and introverted team members contribute equally.',
        'field': 'English & Communication',
        'options': [   'Issue unilateral top-down mandates without providing contextual background or alternatives.',
                       'Rely exclusively on informal hallway rumors rather than structured written documentation.',
                       'Postpone all communication until customer escalations demand immediate attention.',
                       'Provide anonymous input mechanisms and structured brainstorming formats to ensure junior and '
                       'introverted team members contribute equally.'],
        'question_text': 'In software engineering organizations, what represents the gold standard when executing '
                         'facilitating inclusive agile retrospectives?',
        'question_type': 'MCQ',
        'title': 'Comm: Facilitating Inclusive Agile Retrospectives Practice #40',
        'topic': 'Professional Communication'},
    {   'category': 'Additional',
        'correct_answer': 'Immediately notify the release coordinator with an assessment of risk, user impact, and a '
                          'proposed workaround before deciding to hold or proceed.',
        'difficulty': 'MEDIUM',
        'explanation': 'Transparency, risk assessment, and collaborative decision-making are critical during release '
                       'pressure.',
        'field': 'Situational Judgement',
        'options': [   'Immediately notify the release coordinator with an assessment of risk, user impact, and a '
                       'proposed workaround before deciding to hold or proceed.',
                       'Silently push an untested hotfix directly to master without telling anyone.',
                       'Ignore the bug entirely and hope no customers trigger the edge case.',
                       'Cancel the marketing campaign unilaterally without consulting business stakeholders.'],
        'question_text': 'You discover a non-critical edge-case bug in your service 2 hours before a major company '
                         'marketing launch. What is your most effective course of action?',
        'question_type': 'MCQ',
        'title': 'Situational: Production Bug vs Feature Launch Deadline',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Schedule an empathetic 1:1 to understand their blockers, pair-program on complex tasks, and '
                          'foster psychological safety.',
        'difficulty': 'MEDIUM',
        'explanation': 'Constructive mentorship builds confidence through psychological safety, active pairing, and '
                       'identifying root causes of difficulty.',
        'field': 'Situational Judgement',
        'options': [   'Publicly reprimand them in front of the team during the daily standup.',
                       'Schedule an empathetic 1:1 to understand their blockers, pair-program on complex tasks, and '
                       'foster psychological safety.',
                       'Reassign all their tasks to yourself and stop giving them responsibilities.',
                       'File an immediate termination request with HR.'],
        'question_text': 'A junior developer on your team is consistently missing sprint commitments and seems '
                         'hesitant to ask for help during standups. How do you respond?',
        'question_type': 'MCQ',
        'title': 'Situational: Mentoring a Struggling Junior Developer',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Quantify the cost of the tech debt in terms of delivery velocity and incident rates, and '
                          'negotiate dedicated sprint capacity (e.g. 20%) for refactoring.',
        'difficulty': 'MEDIUM',
        'explanation': 'Effective engineering leadership speaks the language of business metrics, demonstrating that '
                       'tech debt paydown accelerates long-term revenue velocity.',
        'field': 'Situational Judgement',
        'options': [   'Refuse to write any new feature code until product management allows a 6-month complete '
                       'rewrite.',
                       'Secretly refactor the entire system at night without informing product managers.',
                       'Quantify the cost of the tech debt in terms of delivery velocity and incident rates, and '
                       'negotiate dedicated sprint capacity (e.g. 20%) for refactoring.',
                       'Abandon engineering standards and write dirty code indefinitely.'],
        'question_text': 'Your engineering team has accumulated significant tech debt that makes adding new features '
                         'slow and risky, but product management wants new features delivered immediately. What is the '
                         'best collaborative approach?',
        'question_type': 'MCQ',
        'title': 'Situational: Balancing Technical Debt with Business Roadmap',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Halt production deployment, analyze training data distributions, retrain with debiasing '
                          'techniques, and document fairness metrics.',
        'difficulty': 'MEDIUM',
        'explanation': 'Engineers bear professional and ethical responsibility to prevent discrimination and ensure '
                       'algorithmic fairness before production deployment.',
        'field': 'Situational Judgement',
        'options': [   "Deploy the model immediately since business revenue targets depend on this quarter's release.",
                       'Delete the evaluation logs so that no record of the discrepancy exists.',
                       'Declare that algorithms are inherently unbiased and take no further action.',
                       'Halt production deployment, analyze training data distributions, retrain with debiasing '
                       'techniques, and document fairness metrics.'],
        'question_text': 'During model evaluation, your machine learning model exhibits an algorithmic bias that '
                         'yields lower approval rates for a specific demographic group. What is the ethical '
                         'imperative?',
        'question_type': 'MCQ',
        'title': 'Situational: Ethical AI and Bias Mitigation',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': "Fully commit to the team's chosen technology, contributing positively to its implementation "
                          'while monitoring its operational metrics objectively.',
        'difficulty': 'MEDIUM',
        'explanation': "High-performing teams practice 'disagree and commit'—arguing vigorously during deliberation, "
                       "but uniting completely behind the team's decision once made.",
        'field': 'Situational Judgement',
        'options': [   "Fully commit to the team's chosen technology, contributing positively to its implementation "
                       'while monitoring its operational metrics objectively.',
                       'Continually remind teammates that they made a mistake every time any bug arises.',
                       'Secretly build a shadow service using your preferred tool.',
                       'Refuse to work on any tasks involving that component.'],
        'question_text': 'After extensive architectural debate, the team votes to adopt a message queue technology '
                         'that was not your preferred choice. How should you conduct yourself following the decision?',
        'question_type': 'MCQ',
        'title': 'Situational: Disagree and Commit in Architecture Consensus',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve handling tight customer commitments by propose a phased '
                       'rollout of high-value mvp features while maintaining quality standards.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with handling tight customer commitments in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Handling Tight Customer Commitments #6',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Escalate objectively to lead architects only after seeking common ground via benchmark '
                          'validation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve peer code review conflict resolution by escalate '
                       'objectively to lead architects only after seeking common ground via benchmark validation.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Escalate objectively to lead architects only after seeking common ground via benchmark '
                       'validation.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with peer code review conflict resolution in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Peer Code Review Conflict Resolution #7',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                          'post-mortems.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve on-call fatigue and burnout by advocate for rotation '
                       'redistribution and prioritize automation of recurring alerts during post-mortems.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                       'post-mortems.'],
        'question_text': 'When faced with on-call fatigue and burnout in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: On-Call Fatigue and Burnout #8',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Produce technical design drafts with explicit assumptions and obtain stakeholder review '
                          'before coding.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve navigating unclear requirements by produce technical '
                       'design drafts with explicit assumptions and obtain stakeholder review before coding.',
        'field': 'Situational Judgement',
        'options': [   'Produce technical design drafts with explicit assumptions and obtain stakeholder review before '
                       'coding.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with navigating unclear requirements in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Navigating Unclear Requirements #9',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                          'schedules.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve cross-team dependency blockers by establish explicit api '
                       'contracts and shared milestone tracking to align inter-team delivery schedules.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                       'schedules.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with cross-team dependency blockers in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Cross-Team Dependency Blockers #10',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve handling tight customer commitments by propose a phased '
                       'rollout of high-value mvp features while maintaining quality standards.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with handling tight customer commitments in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Handling Tight Customer Commitments #11',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Escalate objectively to lead architects only after seeking common ground via benchmark '
                          'validation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve peer code review conflict resolution by escalate '
                       'objectively to lead architects only after seeking common ground via benchmark validation.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Escalate objectively to lead architects only after seeking common ground via benchmark '
                       'validation.'],
        'question_text': 'When faced with peer code review conflict resolution in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Peer Code Review Conflict Resolution #12',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                          'post-mortems.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve on-call fatigue and burnout by advocate for rotation '
                       'redistribution and prioritize automation of recurring alerts during post-mortems.',
        'field': 'Situational Judgement',
        'options': [   'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                       'post-mortems.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with on-call fatigue and burnout in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: On-Call Fatigue and Burnout #13',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Produce technical design drafts with explicit assumptions and obtain stakeholder review '
                          'before coding.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve navigating unclear requirements by produce technical '
                       'design drafts with explicit assumptions and obtain stakeholder review before coding.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Produce technical design drafts with explicit assumptions and obtain stakeholder review before '
                       'coding.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with navigating unclear requirements in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Navigating Unclear Requirements #14',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                          'schedules.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve cross-team dependency blockers by establish explicit api '
                       'contracts and shared milestone tracking to align inter-team delivery schedules.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                       'schedules.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with cross-team dependency blockers in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Cross-Team Dependency Blockers #15',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve handling tight customer commitments by propose a phased '
                       'rollout of high-value mvp features while maintaining quality standards.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Propose a phased rollout of high-value MVP features while maintaining quality standards.'],
        'question_text': 'When faced with handling tight customer commitments in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Handling Tight Customer Commitments #16',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Escalate objectively to lead architects only after seeking common ground via benchmark '
                          'validation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve peer code review conflict resolution by escalate '
                       'objectively to lead architects only after seeking common ground via benchmark validation.',
        'field': 'Situational Judgement',
        'options': [   'Escalate objectively to lead architects only after seeking common ground via benchmark '
                       'validation.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with peer code review conflict resolution in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Peer Code Review Conflict Resolution #17',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                          'post-mortems.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve on-call fatigue and burnout by advocate for rotation '
                       'redistribution and prioritize automation of recurring alerts during post-mortems.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                       'post-mortems.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with on-call fatigue and burnout in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: On-Call Fatigue and Burnout #18',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Produce technical design drafts with explicit assumptions and obtain stakeholder review '
                          'before coding.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve navigating unclear requirements by produce technical '
                       'design drafts with explicit assumptions and obtain stakeholder review before coding.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Produce technical design drafts with explicit assumptions and obtain stakeholder review before '
                       'coding.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with navigating unclear requirements in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Navigating Unclear Requirements #19',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                          'schedules.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve cross-team dependency blockers by establish explicit api '
                       'contracts and shared milestone tracking to align inter-team delivery schedules.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                       'schedules.'],
        'question_text': 'When faced with cross-team dependency blockers in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Cross-Team Dependency Blockers #20',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve handling tight customer commitments by propose a phased '
                       'rollout of high-value mvp features while maintaining quality standards.',
        'field': 'Situational Judgement',
        'options': [   'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with handling tight customer commitments in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Handling Tight Customer Commitments #21',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Escalate objectively to lead architects only after seeking common ground via benchmark '
                          'validation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve peer code review conflict resolution by escalate '
                       'objectively to lead architects only after seeking common ground via benchmark validation.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Escalate objectively to lead architects only after seeking common ground via benchmark '
                       'validation.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with peer code review conflict resolution in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Peer Code Review Conflict Resolution #22',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                          'post-mortems.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve on-call fatigue and burnout by advocate for rotation '
                       'redistribution and prioritize automation of recurring alerts during post-mortems.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                       'post-mortems.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with on-call fatigue and burnout in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: On-Call Fatigue and Burnout #23',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Produce technical design drafts with explicit assumptions and obtain stakeholder review '
                          'before coding.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve navigating unclear requirements by produce technical '
                       'design drafts with explicit assumptions and obtain stakeholder review before coding.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Produce technical design drafts with explicit assumptions and obtain stakeholder review before '
                       'coding.'],
        'question_text': 'When faced with navigating unclear requirements in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Navigating Unclear Requirements #24',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                          'schedules.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve cross-team dependency blockers by establish explicit api '
                       'contracts and shared milestone tracking to align inter-team delivery schedules.',
        'field': 'Situational Judgement',
        'options': [   'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                       'schedules.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with cross-team dependency blockers in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Cross-Team Dependency Blockers #25',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve handling tight customer commitments by propose a phased '
                       'rollout of high-value mvp features while maintaining quality standards.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with handling tight customer commitments in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Handling Tight Customer Commitments #26',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Escalate objectively to lead architects only after seeking common ground via benchmark '
                          'validation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve peer code review conflict resolution by escalate '
                       'objectively to lead architects only after seeking common ground via benchmark validation.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Escalate objectively to lead architects only after seeking common ground via benchmark '
                       'validation.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with peer code review conflict resolution in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Peer Code Review Conflict Resolution #27',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                          'post-mortems.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve on-call fatigue and burnout by advocate for rotation '
                       'redistribution and prioritize automation of recurring alerts during post-mortems.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                       'post-mortems.'],
        'question_text': 'When faced with on-call fatigue and burnout in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: On-Call Fatigue and Burnout #28',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Produce technical design drafts with explicit assumptions and obtain stakeholder review '
                          'before coding.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve navigating unclear requirements by produce technical '
                       'design drafts with explicit assumptions and obtain stakeholder review before coding.',
        'field': 'Situational Judgement',
        'options': [   'Produce technical design drafts with explicit assumptions and obtain stakeholder review before '
                       'coding.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with navigating unclear requirements in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Navigating Unclear Requirements #29',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                          'schedules.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve cross-team dependency blockers by establish explicit api '
                       'contracts and shared milestone tracking to align inter-team delivery schedules.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                       'schedules.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with cross-team dependency blockers in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Cross-Team Dependency Blockers #30',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve handling tight customer commitments by propose a phased '
                       'rollout of high-value mvp features while maintaining quality standards.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with handling tight customer commitments in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Handling Tight Customer Commitments #31',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Escalate objectively to lead architects only after seeking common ground via benchmark '
                          'validation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve peer code review conflict resolution by escalate '
                       'objectively to lead architects only after seeking common ground via benchmark validation.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Escalate objectively to lead architects only after seeking common ground via benchmark '
                       'validation.'],
        'question_text': 'When faced with peer code review conflict resolution in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Peer Code Review Conflict Resolution #32',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                          'post-mortems.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve on-call fatigue and burnout by advocate for rotation '
                       'redistribution and prioritize automation of recurring alerts during post-mortems.',
        'field': 'Situational Judgement',
        'options': [   'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                       'post-mortems.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with on-call fatigue and burnout in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: On-Call Fatigue and Burnout #33',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Produce technical design drafts with explicit assumptions and obtain stakeholder review '
                          'before coding.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve navigating unclear requirements by produce technical '
                       'design drafts with explicit assumptions and obtain stakeholder review before coding.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Produce technical design drafts with explicit assumptions and obtain stakeholder review before '
                       'coding.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with navigating unclear requirements in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Navigating Unclear Requirements #34',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                          'schedules.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve cross-team dependency blockers by establish explicit api '
                       'contracts and shared milestone tracking to align inter-team delivery schedules.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                       'schedules.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with cross-team dependency blockers in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Cross-Team Dependency Blockers #35',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve handling tight customer commitments by propose a phased '
                       'rollout of high-value mvp features while maintaining quality standards.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Propose a phased rollout of high-value MVP features while maintaining quality standards.'],
        'question_text': 'When faced with handling tight customer commitments in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Handling Tight Customer Commitments #36',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Escalate objectively to lead architects only after seeking common ground via benchmark '
                          'validation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve peer code review conflict resolution by escalate '
                       'objectively to lead architects only after seeking common ground via benchmark validation.',
        'field': 'Situational Judgement',
        'options': [   'Escalate objectively to lead architects only after seeking common ground via benchmark '
                       'validation.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with peer code review conflict resolution in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Peer Code Review Conflict Resolution #37',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                          'post-mortems.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve on-call fatigue and burnout by advocate for rotation '
                       'redistribution and prioritize automation of recurring alerts during post-mortems.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                       'post-mortems.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with on-call fatigue and burnout in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: On-Call Fatigue and Burnout #38',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Produce technical design drafts with explicit assumptions and obtain stakeholder review '
                          'before coding.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve navigating unclear requirements by produce technical '
                       'design drafts with explicit assumptions and obtain stakeholder review before coding.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Produce technical design drafts with explicit assumptions and obtain stakeholder review before '
                       'coding.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with navigating unclear requirements in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Navigating Unclear Requirements #39',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                          'schedules.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve cross-team dependency blockers by establish explicit api '
                       'contracts and shared milestone tracking to align inter-team delivery schedules.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                       'schedules.'],
        'question_text': 'When faced with cross-team dependency blockers in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Cross-Team Dependency Blockers #40',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve handling tight customer commitments by propose a phased '
                       'rollout of high-value mvp features while maintaining quality standards.',
        'field': 'Situational Judgement',
        'options': [   'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with handling tight customer commitments in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Handling Tight Customer Commitments #41',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Escalate objectively to lead architects only after seeking common ground via benchmark '
                          'validation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve peer code review conflict resolution by escalate '
                       'objectively to lead architects only after seeking common ground via benchmark validation.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Escalate objectively to lead architects only after seeking common ground via benchmark '
                       'validation.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with peer code review conflict resolution in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Peer Code Review Conflict Resolution #42',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                          'post-mortems.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve on-call fatigue and burnout by advocate for rotation '
                       'redistribution and prioritize automation of recurring alerts during post-mortems.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                       'post-mortems.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with on-call fatigue and burnout in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: On-Call Fatigue and Burnout #43',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Produce technical design drafts with explicit assumptions and obtain stakeholder review '
                          'before coding.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve navigating unclear requirements by produce technical '
                       'design drafts with explicit assumptions and obtain stakeholder review before coding.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Produce technical design drafts with explicit assumptions and obtain stakeholder review before '
                       'coding.'],
        'question_text': 'When faced with navigating unclear requirements in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Navigating Unclear Requirements #44',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                          'schedules.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve cross-team dependency blockers by establish explicit api '
                       'contracts and shared milestone tracking to align inter-team delivery schedules.',
        'field': 'Situational Judgement',
        'options': [   'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                       'schedules.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with cross-team dependency blockers in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Cross-Team Dependency Blockers #45',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve handling tight customer commitments by propose a phased '
                       'rollout of high-value mvp features while maintaining quality standards.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Propose a phased rollout of high-value MVP features while maintaining quality standards.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with handling tight customer commitments in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Handling Tight Customer Commitments #46',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Escalate objectively to lead architects only after seeking common ground via benchmark '
                          'validation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve peer code review conflict resolution by escalate '
                       'objectively to lead architects only after seeking common ground via benchmark validation.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Escalate objectively to lead architects only after seeking common ground via benchmark '
                       'validation.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with peer code review conflict resolution in a modern engineering department, '
                         'which approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Peer Code Review Conflict Resolution #47',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                          'post-mortems.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve on-call fatigue and burnout by advocate for rotation '
                       'redistribution and prioritize automation of recurring alerts during post-mortems.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.',
                       'Advocate for rotation redistribution and prioritize automation of recurring alerts during '
                       'post-mortems.'],
        'question_text': 'When faced with on-call fatigue and burnout in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: On-Call Fatigue and Burnout #48',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Produce technical design drafts with explicit assumptions and obtain stakeholder review '
                          'before coding.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve navigating unclear requirements by produce technical '
                       'design drafts with explicit assumptions and obtain stakeholder review before coding.',
        'field': 'Situational Judgement',
        'options': [   'Produce technical design drafts with explicit assumptions and obtain stakeholder review before '
                       'coding.',
                       'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with navigating unclear requirements in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Navigating Unclear Requirements #49',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Additional',
        'correct_answer': 'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                          'schedules.',
        'difficulty': 'MEDIUM',
        'explanation': 'Mature engineering practices resolve cross-team dependency blockers by establish explicit api '
                       'contracts and shared milestone tracking to align inter-team delivery schedules.',
        'field': 'Situational Judgement',
        'options': [   'Compromise system security and test coverage to meet external deadlines at all costs.',
                       'Establish explicit API contracts and shared milestone tracking to align inter-team delivery '
                       'schedules.',
                       'Withdraw from active project discussions and wait for other teams to fail.',
                       'Blame organizational leadership in customer-facing communication channels.'],
        'question_text': 'When faced with cross-team dependency blockers in a modern engineering department, which '
                         'approach best balances engineering excellence and team alignment?',
        'question_type': 'MCQ',
        'title': 'Situational: Workplace Scenario: Cross-Team Dependency Blockers #50',
        'topic': 'Workplace Scenarios'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Conscientiousness & Work Rigor (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I systematically break complex, ambiguous engineering problems into verifiable '
                         'sub-components before beginning implementation.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Conscientiousness',
                           'dimension_name': 'Conscientiousness & Work Rigor',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Conscientiousness #1',
        'topic': 'Conscientiousness & Work Rigor'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Conscientiousness & Work Rigor (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I verify edge cases, error handlers, and failure recovery paths even when working under '
                         'tight deadline pressure.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Conscientiousness',
                           'dimension_name': 'Conscientiousness & Work Rigor',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Conscientiousness #2',
        'topic': 'Conscientiousness & Work Rigor'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Conscientiousness & Work Rigor (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I maintain structured, up-to-date documentation for systems and APIs I design so peers can '
                         'onboard easily.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Conscientiousness',
                           'dimension_name': 'Conscientiousness & Work Rigor',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Conscientiousness #3',
        'topic': 'Conscientiousness & Work Rigor'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Conscientiousness & Work Rigor (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I prefer deploying quick improvisational fixes without writing automated tests or verifying '
                         'regression risks.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Conscientiousness',
                           'dimension_name': 'Conscientiousness & Work Rigor',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Conscientiousness #4',
        'topic': 'Conscientiousness & Work Rigor'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Conscientiousness & Work Rigor (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I tend to lose focus on ongoing maintenance tasks once the initial prototype is functioning.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Conscientiousness',
                           'dimension_name': 'Conscientiousness & Work Rigor',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Conscientiousness #5',
        'topic': 'Conscientiousness & Work Rigor'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Conscientiousness & Work Rigor (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I leave non-blocking code cleanups and minor warning logs unaddressed unless an external '
                         'audit flags them.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Conscientiousness',
                           'dimension_name': 'Conscientiousness & Work Rigor',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Conscientiousness #6',
        'topic': 'Conscientiousness & Work Rigor'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Growth Mindset & Curiosity (Direct). Disclaimer: Indicative only, not clinical. '
                       'This psychometric assessment is designed for professional development, coaching insight, and '
                       'workplace preference mapping. It does not constitute psychological diagnosis or clinical '
                       'psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I actively seek out code reviews from engineers whose architectural perspectives differ from '
                         'my own.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Growth Mindset',
                           'dimension_name': 'Growth Mindset & Curiosity',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Growth Mindset #1',
        'topic': 'Growth Mindset & Curiosity'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Growth Mindset & Curiosity (Direct). Disclaimer: Indicative only, not clinical. '
                       'This psychometric assessment is designed for professional development, coaching insight, and '
                       'workplace preference mapping. It does not constitute psychological diagnosis or clinical '
                       'psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I view challenging production bugs and incident post-mortems as valuable opportunities to '
                         'deepen systemic mastery.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Growth Mindset',
                           'dimension_name': 'Growth Mindset & Curiosity',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Growth Mindset #2',
        'topic': 'Growth Mindset & Curiosity'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Growth Mindset & Curiosity (Direct). Disclaimer: Indicative only, not clinical. '
                       'This psychometric assessment is designed for professional development, coaching insight, and '
                       'workplace preference mapping. It does not constitute psychological diagnosis or clinical '
                       'psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I regularly experiment with emerging programming languages, frameworks, or tools outside my '
                         'core day-to-day stack.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Growth Mindset',
                           'dimension_name': 'Growth Mindset & Curiosity',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Growth Mindset #3',
        'topic': 'Growth Mindset & Curiosity'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Growth Mindset & Curiosity (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I feel uncomfortable when assigned tasks that require working with unfamiliar tech stacks or '
                         'domain concepts.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Growth Mindset',
                           'dimension_name': 'Growth Mindset & Curiosity',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Growth Mindset #4',
        'topic': 'Growth Mindset & Curiosity'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Growth Mindset & Curiosity (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I interpret critical feedback during architectural reviews as a personal attack on my '
                         'technical competence.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Growth Mindset',
                           'dimension_name': 'Growth Mindset & Curiosity',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Growth Mindset #5',
        'topic': 'Growth Mindset & Curiosity'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Growth Mindset & Curiosity (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I prefer sticking strictly to the tools and patterns I already know well rather than '
                         'adopting newer paradigms.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Growth Mindset',
                           'dimension_name': 'Growth Mindset & Curiosity',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Growth Mindset #6',
        'topic': 'Growth Mindset & Curiosity'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Resilience & Stress Composure (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'During high-severity production outages, I maintain emotional composure and focus '
                         'systematically on triage evidence.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Resilience',
                           'dimension_name': 'Resilience & Stress Composure',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Resilience #1',
        'topic': 'Resilience & Stress Composure'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Resilience & Stress Composure (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'When a multi-week technical design proposal is rejected by leadership, I can quickly regroup '
                         'and iterate positively.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Resilience',
                           'dimension_name': 'Resilience & Stress Composure',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Resilience #2',
        'topic': 'Resilience & Stress Composure'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Resilience & Stress Composure (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I handle urgent priority shifts and unexpected scope changes without becoming visibly '
                         'frustrated or disengaged.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Resilience',
                           'dimension_name': 'Resilience & Stress Composure',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Resilience #3',
        'topic': 'Resilience & Stress Composure'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Resilience & Stress Composure (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I find it difficult to bounce back productively after a deployment failure or critical '
                         'performance regression.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Resilience',
                           'dimension_name': 'Resilience & Stress Composure',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Resilience #4',
        'topic': 'Resilience & Stress Composure'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Resilience & Stress Composure (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'Under sustained on-call pressure, I often feel overwhelmed and struggle to prioritize '
                         'competing tasks effectively.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Resilience',
                           'dimension_name': 'Resilience & Stress Composure',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Resilience #5',
        'topic': 'Resilience & Stress Composure'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Resilience & Stress Composure (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'Unexpected interruptions during deep coding work frequently derail my entire productivity '
                         'for the rest of the day.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Resilience',
                           'dimension_name': 'Resilience & Stress Composure',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Resilience #6',
        'topic': 'Resilience & Stress Composure'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Collaboration & Teamwork (Direct). Disclaimer: Indicative only, not clinical. '
                       'This psychometric assessment is designed for professional development, coaching insight, and '
                       'workplace preference mapping. It does not constitute psychological diagnosis or clinical '
                       'psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': "I prioritize unblocking a teammate's pull request or build failure over advancing my own "
                         'individual sprint tasks.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Collaboration',
                           'dimension_name': 'Collaboration & Teamwork',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Collaboration #1',
        'topic': 'Collaboration & Teamwork'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Collaboration & Teamwork (Direct). Disclaimer: Indicative only, not clinical. '
                       'This psychometric assessment is designed for professional development, coaching insight, and '
                       'workplace preference mapping. It does not constitute psychological diagnosis or clinical '
                       'psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I actively share institutional knowledge and technical context rather than hoarding '
                         'information as personal leverage.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Collaboration',
                           'dimension_name': 'Collaboration & Teamwork',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Collaboration #2',
        'topic': 'Collaboration & Teamwork'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Collaboration & Teamwork (Direct). Disclaimer: Indicative only, not clinical. '
                       'This psychometric assessment is designed for professional development, coaching insight, and '
                       'workplace preference mapping. It does not constitute psychological diagnosis or clinical '
                       'psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I invest time in pair programming and mentoring peers who are learning new areas of our '
                         'codebase.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Collaboration',
                           'dimension_name': 'Collaboration & Teamwork',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Collaboration #3',
        'topic': 'Collaboration & Teamwork'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Collaboration & Teamwork (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I prefer working in total isolation on my components without having to coordinate design '
                         'decisions with others.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Collaboration',
                           'dimension_name': 'Collaboration & Teamwork',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Collaboration #4',
        'topic': 'Collaboration & Teamwork'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Collaboration & Teamwork (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I find cross-functional alignment meetings with product and design to be a distraction from '
                         'real engineering.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Collaboration',
                           'dimension_name': 'Collaboration & Teamwork',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Collaboration #5',
        'topic': 'Collaboration & Teamwork'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Collaboration & Teamwork (Reverse-keyed). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I hesitate to offer assistance to teammates outside my immediate squad unless directed by '
                         'management.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Collaboration',
                           'dimension_name': 'Collaboration & Teamwork',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Collaboration #6',
        'topic': 'Collaboration & Teamwork'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Proactive Initiative & Ownership (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'When I notice recurring flakiness in CI pipelines, I voluntarily investigate and fix the '
                         'root cause without being asked.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Initiative',
                           'dimension_name': 'Proactive Initiative & Ownership',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Initiative #1',
        'topic': 'Proactive Initiative & Ownership'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Proactive Initiative & Ownership (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I take end-to-end accountability for services I build, from initial design through '
                         'production telemetry and monitoring.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Initiative',
                           'dimension_name': 'Proactive Initiative & Ownership',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Initiative #2',
        'topic': 'Proactive Initiative & Ownership'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Proactive Initiative & Ownership (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I proactively propose optimizations that enhance developer velocity or reduce cloud '
                         'infrastructure expenditure.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Initiative',
                           'dimension_name': 'Proactive Initiative & Ownership',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Initiative #3',
        'topic': 'Proactive Initiative & Ownership'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Proactive Initiative & Ownership (Reverse-keyed). Disclaimer: Indicative only, '
                       'not clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I only work on items that are explicitly assigned to me as Jira tickets in the current '
                         'sprint.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Initiative',
                           'dimension_name': 'Proactive Initiative & Ownership',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Initiative #4',
        'topic': 'Proactive Initiative & Ownership'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Proactive Initiative & Ownership (Reverse-keyed). Disclaimer: Indicative only, '
                       'not clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'When an architectural ambiguity arises, I wait for a senior lead to tell me what to do '
                         'rather than formulating options.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Initiative',
                           'dimension_name': 'Proactive Initiative & Ownership',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Initiative #5',
        'topic': 'Proactive Initiative & Ownership'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Proactive Initiative & Ownership (Reverse-keyed). Disclaimer: Indicative only, '
                       'not clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I consider a task complete once my branch is merged, regardless of whether it deploys '
                         'cleanly to production.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Initiative',
                           'dimension_name': 'Proactive Initiative & Ownership',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Initiative #6',
        'topic': 'Proactive Initiative & Ownership'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Adaptability & Cognitive Flexibility (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I quickly adapt my working style when our engineering team pivots organizational goals or '
                         'architectural strategies.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Adaptability',
                           'dimension_name': 'Adaptability & Cognitive Flexibility',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Adaptability #1',
        'topic': 'Adaptability & Cognitive Flexibility'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Adaptability & Cognitive Flexibility (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I comfortably balance strict engineering best practices with pragmatic business delivery '
                         'constraints when warranted.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Adaptability',
                           'dimension_name': 'Adaptability & Cognitive Flexibility',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Adaptability #2',
        'topic': 'Adaptability & Cognitive Flexibility'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Adaptability & Cognitive Flexibility (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I am willing to abandon an architectural approach I championed if new data proves an '
                         'alternative is superior.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Adaptability',
                           'dimension_name': 'Adaptability & Cognitive Flexibility',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Adaptability #3',
        'topic': 'Adaptability & Cognitive Flexibility'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Adaptability & Cognitive Flexibility (Reverse-keyed). Disclaimer: Indicative '
                       'only, not clinical. This psychometric assessment is designed for professional development, '
                       'coaching insight, and workplace preference mapping. It does not constitute psychological '
                       'diagnosis or clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I become frustrated when established team conventions or development processes are altered '
                         'by leadership.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Adaptability',
                           'dimension_name': 'Adaptability & Cognitive Flexibility',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Adaptability #4',
        'topic': 'Adaptability & Cognitive Flexibility'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Adaptability & Cognitive Flexibility (Reverse-keyed). Disclaimer: Indicative '
                       'only, not clinical. This psychometric assessment is designed for professional development, '
                       'coaching insight, and workplace preference mapping. It does not constitute psychological '
                       'diagnosis or clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I insist on using identical tools and workflows regardless of whether a project is an '
                         'exploratory MVP or core service.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Adaptability',
                           'dimension_name': 'Adaptability & Cognitive Flexibility',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Adaptability #5',
        'topic': 'Adaptability & Cognitive Flexibility'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Adaptability & Cognitive Flexibility (Reverse-keyed). Disclaimer: Indicative '
                       'only, not clinical. This psychometric assessment is designed for professional development, '
                       'coaching insight, and workplace preference mapping. It does not constitute psychological '
                       'diagnosis or clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I resist adopting new team methodologies like trunk-based development or pair programming.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Adaptability',
                           'dimension_name': 'Adaptability & Cognitive Flexibility',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Adaptability #6',
        'topic': 'Adaptability & Cognitive Flexibility'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Communication Openness & Transparency (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I communicate potential timeline delays, dependency blockers, and technical risks to '
                         'stakeholders as early as possible.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Communication Openness',
                           'dimension_name': 'Communication Openness & Transparency',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Communication Openness #1',
        'topic': 'Communication Openness & Transparency'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Communication Openness & Transparency (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I openly admit when I do not understand a technical concept and ask clarifying questions in '
                         'public team channels.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Communication Openness',
                           'dimension_name': 'Communication Openness & Transparency',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Communication Openness #2',
        'topic': 'Communication Openness & Transparency'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Communication Openness & Transparency (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I present constructive disagreements candidly and diplomatically during design deliberation '
                         'meetings.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Communication Openness',
                           'dimension_name': 'Communication Openness & Transparency',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Communication Openness #3',
        'topic': 'Communication Openness & Transparency'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Communication Openness & Transparency (Reverse-keyed). Disclaimer: Indicative '
                       'only, not clinical. This psychometric assessment is designed for professional development, '
                       'coaching insight, and workplace preference mapping. It does not constitute psychological '
                       'diagnosis or clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I tend to conceal technical difficulties or bugs until the very last moment before a release '
                         'deadline.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Communication Openness',
                           'dimension_name': 'Communication Openness & Transparency',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Communication Openness #4',
        'topic': 'Communication Openness & Transparency'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Communication Openness & Transparency (Reverse-keyed). Disclaimer: Indicative '
                       'only, not clinical. This psychometric assessment is designed for professional development, '
                       'coaching insight, and workplace preference mapping. It does not constitute psychological '
                       'diagnosis or clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I avoid speaking up in architecture discussions even when I spot critical flaws in proposed '
                         'designs.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Communication Openness',
                           'dimension_name': 'Communication Openness & Transparency',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Communication Openness #5',
        'topic': 'Communication Openness & Transparency'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Communication Openness & Transparency (Reverse-keyed). Disclaimer: Indicative '
                       'only, not clinical. This psychometric assessment is designed for professional development, '
                       'coaching insight, and workplace preference mapping. It does not constitute psychological '
                       'diagnosis or clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I use overly dense technical jargon deliberately to prevent non-technical colleagues from '
                         'questioning my estimates.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Communication Openness',
                           'dimension_name': 'Communication Openness & Transparency',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Communication Openness #6',
        'topic': 'Communication Openness & Transparency'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Ethical Integrity & Accountability (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I adhere strictly to data privacy standards and security policies even when taking shortcuts '
                         'would speed up delivery.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Ethical Integrity',
                           'dimension_name': 'Ethical Integrity & Accountability',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Ethical Integrity #1',
        'topic': 'Ethical Integrity & Accountability'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Ethical Integrity & Accountability (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I give public credit to teammates whose ideas, libraries, or suggestions contributed to my '
                         "project's success.",
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Ethical Integrity',
                           'dimension_name': 'Ethical Integrity & Accountability',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Ethical Integrity #2',
        'topic': 'Ethical Integrity & Accountability'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Ethical Integrity & Accountability (Direct). Disclaimer: Indicative only, not '
                       'clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I promptly flag algorithmic bias, accessibility oversights, or compliance gaps to leadership '
                         'before launch.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Ethical Integrity',
                           'dimension_name': 'Ethical Integrity & Accountability',
                           'reverse_keyed': False,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Ethical Integrity #3',
        'topic': 'Ethical Integrity & Accountability'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Ethical Integrity & Accountability (Reverse-keyed). Disclaimer: Indicative only, '
                       'not clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I would bypass mandatory security review gates if doing so helped meet an aggressive '
                         'quarterly bonus deadline.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Ethical Integrity',
                           'dimension_name': 'Ethical Integrity & Accountability',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Ethical Integrity #4',
        'topic': 'Ethical Integrity & Accountability'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Ethical Integrity & Accountability (Reverse-keyed). Disclaimer: Indicative only, '
                       'not clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I sometimes claim personal credit for open-source community code or peer contributions in '
                         'executive presentations.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Ethical Integrity',
                           'dimension_name': 'Ethical Integrity & Accountability',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Ethical Integrity #5',
        'topic': 'Ethical Integrity & Accountability'},
    {   'category': 'Psychometric',
        'correct_answer': None,
        'difficulty': 'MEDIUM',
        'explanation': 'Assessment of Ethical Integrity & Accountability (Reverse-keyed). Disclaimer: Indicative only, '
                       'not clinical. This psychometric assessment is designed for professional development, coaching '
                       'insight, and workplace preference mapping. It does not constitute psychological diagnosis or '
                       'clinical psychometric profiling.',
        'field': 'Psychometrics & Workplace Profile',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'question_text': 'I believe that software engineers have no responsibility for how business algorithms impact '
                         'end users.',
        'question_type': 'LIKERT',
        'rubric_json': {   'dimension': 'Ethical Integrity',
                           'dimension_name': 'Ethical Integrity & Accountability',
                           'reverse_keyed': True,
                           'scale_labels': {   '1': 'Strongly Disagree',
                                               '2': 'Disagree',
                                               '3': 'Neutral',
                                               '4': 'Agree',
                                               '5': 'Strongly Agree'},
                           'scale_max': 5,
                           'scale_min': 1},
        'title': 'Psychometric: Ethical Integrity #6',
        'topic': 'Ethical Integrity & Accountability'}]
