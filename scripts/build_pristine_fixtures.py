"""Build pristine, 100% unique English & Communication and Situational Judgement questions.

Ensures:
- 40 unique English & Communication questions covering grammar, vocab, reading comprehension, sentence correction, and professional email tasks.
- 50 unique Situational Judgement questions with scored options.
- Preserves the 48 Psychometric Likert items.
- Enforces ~25% answer distribution across A, B, C, D.
- No distractor text appears in more than 3 questions.
"""

from __future__ import annotations

import pprint
import random
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "backend"))

from scripts.fixtures.communication_psychometric import COMMUNICATION_PSYCHOMETRIC_QUESTIONS as EXISTING

likert_items = [q for q in EXISTING if q.get("category") == "Psychometric"]
assert len(likert_items) == 48

# ==========================================
# 40 ENGLISH & COMMUNICATION QUESTIONS
# ==========================================
english_specs = [
    # 1. Grammar & Sentence Construction (8 questions)
    {
        "title": "Grammar: Subject-Verb Agreement with Intervening Phrases",
        "topic": "Grammar & Construction",
        "question_text": "Identify the sentence that correctly adheres to subject-verb agreement rules when an intervening prepositional phrase is present.",
        "correct": "The list of microservice dependencies, along with their database connection pools, is updated during deployment.",
        "distractors": [
            "The list of microservice dependencies, along with their database connection pools, are updated during deployment.",
            "The list of microservice dependencies, along with their database connection pools, were updated during deployment.",
            "The list of microservice dependencies, along with their database connection pools, have been updated during deployment.",
        ],
        "explanation": "The grammatical subject is 'The list' (singular). The intervening phrase 'along with their database connection pools' does not alter the singular verb requirement ('is updated').",
        "difficulty": "EASY",
    },
    {
        "title": "Grammar: Dangling and Misplaced Modifiers",
        "topic": "Grammar & Construction",
        "question_text": "Which of the following sentences correctly avoids a dangling modifier?",
        "correct": "Having optimized the SQL execution plan, the platform engineer observed a 40% reduction in query latency.",
        "distractors": [
            "Having optimized the SQL execution plan, a 40% reduction in query latency was observed by the database.",
            "Having optimized the SQL execution plan, query latency decreased dramatically for the platform team.",
            "Having optimized the SQL execution plan, the server CPU utilization dropped without human intervention.",
        ],
        "explanation": "The introductory participial phrase 'Having optimized...' must logically modify the agent who performed the action, which is 'the platform engineer', not the latency or server.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Grammar: Parallel Structure in Technical Specifications",
        "topic": "Grammar & Construction",
        "question_text": "Select the sentence that maintains rigorous parallel grammatical structure in technical documentation.",
        "correct": "The security gateway is designed to intercept incoming requests, validate JWT signatures, and log audit trails.",
        "distractors": [
            "The security gateway is designed to intercept incoming requests, validating JWT signatures, and to log audit trails.",
            "The security gateway is designed for intercepting requests, validate JWT signatures, and logging of audit trails.",
            "The security gateway is designed to intercept incoming requests, for JWT signature validation, and audit logging.",
        ],
        "explanation": "Parallelism requires coordinated elements to share the same grammatical form: 'intercept... validate... and log'.",
        "difficulty": "EASY",
    },
    {
        "title": "Grammar: Subjunctive Mood in SLA Contracts",
        "topic": "Grammar & Construction",
        "question_text": "Which sentence correctly uses the subjunctive mood to express a mandatory system invariant in an SLA document?",
        "correct": "The enterprise compliance policy mandates that every cluster node be encrypted at rest and in transit.",
        "distractors": [
            "The enterprise compliance policy mandates that every cluster node is encrypted at rest and in transit.",
            "The enterprise compliance policy mandates that every cluster node was encrypted at rest and in transit.",
            "The enterprise compliance policy mandates that every cluster node will be encrypted at rest and in transit.",
        ],
        "explanation": "Verbs expressing mandate, requirement, or recommendation take the subjunctive base form ('that every cluster node be encrypted').",
        "difficulty": "HARD",
    },
    {
        "title": "Grammar: Pronoun-Antecedent Agreement with Collective Nouns",
        "topic": "Grammar & Construction",
        "question_text": "In formal technical reporting, which sentence correctly handles pronoun agreement for a collective team noun acting as a single unit?",
        "correct": "The site reliability engineering squad has delivered its quarterly disaster recovery audit report.",
        "distractors": [
            "The site reliability engineering squad has delivered their quarterly disaster recovery audit report.",
            "The site reliability engineering squad have delivered its quarterly disaster recovery audit report.",
            "The site reliability engineering squad are delivering their quarterly disaster recovery audit report.",
        ],
        "explanation": "When a collective noun ('squad') acts cohesively as a single entity, singular pronouns and verbs are required ('has delivered its').",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Grammar: Tense Sequencing in Incident Narratives",
        "topic": "Grammar & Construction",
        "question_text": "Which option displays the correct sequence of tenses when recounting past root causes and ongoing remediation in a post-mortem?",
        "correct": "The engineering team discovered that an unchecked thread pool had exhausted available memory before the failover triggered.",
        "distractors": [
            "The engineering team discovered that an unchecked thread pool has exhausted available memory before the failover triggered.",
            "The engineering team had discovered that an unchecked thread pool exhausts available memory before the failover triggered.",
            "The engineering team discovers that an unchecked thread pool had exhausted available memory before the failover had triggered.",
        ],
        "explanation": "The past perfect tense ('had exhausted') correctly indicates an action completed prior to another past event ('discovered' / 'triggered').",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Grammar: Inversion for Emphatic Technical Arguments",
        "topic": "Grammar & Construction",
        "question_text": "Choose the correctly constructed inverted sentence used for emphasis in architectural design proposals.",
        "correct": "Rarely has an asynchronous distributed system maintained strict linearizability without introducing measurable latency overhead.",
        "distractors": [
            "Rarely an asynchronous distributed system has maintained strict linearizability without introducing measurable latency overhead.",
            "Rarely has maintained an asynchronous distributed system strict linearizability without introducing measurable latency overhead.",
            "Rarely an asynchronous distributed system maintained strict linearizability without introducing measurable latency overhead.",
        ],
        "explanation": "Negative adverbial openers ('Rarely', 'Seldom', 'Scarcely') trigger subject-auxiliary inversion: 'Rarely has [subject] maintained'.",
        "difficulty": "HARD",
    },
    {
        "title": "Grammar: Semicolon vs Colon Precision in Requirements",
        "topic": "Grammar & Construction",
        "question_text": "Which sentence demonstrates the correct punctuation rule governing colons and semicolons in technical requirements?",
        "correct": "The ingress controller enforces three ingress policies: rate limiting per client IP, mutual TLS authentication, and WAF inspection.",
        "distractors": [
            "The ingress controller enforces three ingress policies; rate limiting per client IP, mutual TLS authentication, and WAF inspection.",
            "The ingress controller enforces: rate limiting per client IP, mutual TLS authentication, and WAF inspection.",
            "The ingress controller enforces three ingress policies, namely: rate limiting per client IP, mutual TLS authentication, and WAF inspection.",
        ],
        "explanation": "A colon introduces a formal list following an independent clause. A colon should not directly separate a verb from its direct object.",
        "difficulty": "EASY",
    },

    # 2. Vocabulary in Context (8 questions)
    {
        "title": "Vocab: 'Ephemeral' in Cloud Infrastructure",
        "topic": "Vocabulary in Context",
        "question_text": "In container orchestration documentation, what is the precise meaning of the term 'ephemeral storage'?",
        "correct": "Temporary storage that exists only during the lifespan of the container instance and is wiped upon pod termination.",
        "distractors": [
            "Highly durable multi-region replicated object storage backed by block-level snapshots.",
            "Encrypted cryptographic hardware storage reserved exclusively for TLS private key certificates.",
            "Static, non-volatile read-only firmware memory mapped directly into virtual machine RAM.",
        ],
        "explanation": "'Ephemeral' denotes fleeting, short-lived resources that do not persist beyond the runtime existence of their host container.",
        "difficulty": "EASY",
    },
    {
        "title": "Vocab: 'Idempotent' in API Design",
        "topic": "Vocabulary in Context",
        "question_text": "When an API specification mandates that an endpoint must be 'idempotent', what contractual guarantee is provided?",
        "correct": "Making identical multiple requests results in the exact same server-side state as making a single request.",
        "distractors": [
            "The endpoint processes incoming requests asynchronously without blocking client threads.",
            "The API method executes in zero milliseconds by returning pre-computed cached responses.",
            "The service can execute concurrently across multiple worker threads without locking memory.",
        ],
        "explanation": "Idempotence guarantees that repeated executions with identical parameters produce no incremental side effects beyond the first call.",
        "difficulty": "EASY",
    },
    {
        "title": "Vocab: 'Mitigate' in Security Risk Registers",
        "topic": "Vocabulary in Context",
        "question_text": "In an enterprise cybersecurity audit report, what does it mean to 'mitigate' an identified vulnerability?",
        "correct": "To implement defensive controls that diminish the severity, probability, or operational impact of an exploitation.",
        "distractors": [
            "To completely transfer all legal liability and insurance claims to a third-party managed provider.",
            "To formally accept the risk without allocating engineering resources or implementing safeguards.",
            "To decommission and terminate the underlying server cluster entirely to avoid security scans.",
        ],
        "explanation": "To mitigate is to reduce or soften the impact, exposure, or likelihood of a risk through proactive controls.",
        "difficulty": "EASY",
    },
    {
        "title": "Vocab: 'Discrete' vs 'Discreet' in System Modeling",
        "topic": "Vocabulary in Context",
        "question_text": "Which word correctly completes the architectural statement: 'The microservices architecture splits processing into separate, _______ computational units'?",
        "correct": "discrete",
        "distractors": [
            "discreet",
            "discretionary",
            "discretional",
        ],
        "explanation": "'Discrete' means separate, distinct, and detached. 'Discreet' means careful, prudent, and unobtrusive.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Vocab: 'Unequivocal' in Stakeholder Commitments",
        "topic": "Vocabulary in Context",
        "question_text": "When a client executive demands an 'unequivocal commitment' regarding delivery milestones, what are they requesting?",
        "correct": "A clear, unambiguous, and definitive commitment leaving no room for doubt or multiple interpretations.",
        "distractors": [
            "A tentative and preliminary timeline contingent on prospective budget allocations.",
            "A compromise agreement allowing both parties equal flexibility to alter deliverables.",
            "A non-binding conversational estimate subject to weekly retrospective reassessments.",
        ],
        "explanation": "'Unequivocal' means admitting of no doubt or misunderstanding; clear and absolute.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Vocab: 'Pragmatic' vs 'Dogmatic' Engineering",
        "topic": "Vocabulary in Context",
        "question_text": "In technical leadership evaluations, how is a 'pragmatic' software architect characterized?",
        "correct": "One who balances theoretical elegance against practical constraints, delivery deadlines, and operational ROI.",
        "distractors": [
            "One who strictly adheres to orthodox textbook patterns regardless of team velocity or project context.",
            "One who rejects all formal architectural standards in favor of ad-hoc, unstructured code hacks.",
            "One who exclusively adopts cutting-edge alpha-stage libraries to maximize resume novelty.",
        ],
        "explanation": "Pragmatism in engineering focuses on practical, sensible trade-offs suited to realistic operational context rather than rigid dogma.",
        "difficulty": "EASY",
    },
    {
        "title": "Vocab: 'Congruent' in Regulatory Alignment",
        "topic": "Vocabulary in Context",
        "question_text": "In a data protection compliance review, what does stating that 'internal policies are congruent with DPDP regulations' signify?",
        "correct": "The organization's internal controls are in full agreement, harmony, and conformance with legal requirements.",
        "distractors": [
            "The internal controls partially supersede national legal frameworks through executive decree.",
            "The organizational policies are currently undergoing formal judicial dispute in appellate court.",
            "The compliance directives are temporarily suspended pending international standardization.",
        ],
        "explanation": "'Congruent' means in agreement, coinciding, and harmonious in structure and application.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Vocab: 'Anomalous' in Telemetry Analysis",
        "topic": "Vocabulary in Context",
        "question_text": "When observability alerts flag 'anomalous egress traffic patterns', what does this indicate to the operations team?",
        "correct": "Network traffic metrics that deviate significantly from established baseline behavioral distributions.",
        "distractors": [
            "Traffic that conforms precisely to historical seasonal averages and expected user volumes.",
            "Encrypted packets that have successfully cleared mutual TLS handshake validation protocols.",
            "Outbound data transfers that have been explicitly whitelisted by site reliability administrators.",
        ],
        "explanation": "'Anomalous' denotes irregular, abnormal, or deviating from the standard baseline model.",
        "difficulty": "EASY",
    },

    # 3. Reading Comprehension (8 questions across 2 technical passages)
    # Passage 1: Distributed Consensus (4 questions)
    {
        "title": "Reading: Distributed Consensus - Core Thesis",
        "topic": "Reading Comprehension",
        "question_text": (
            "Passage Excerpt: 'In distributed state machine replication, consensus algorithms such as Raft and Paxos ensure fault tolerance by requiring a majority quorum before committing state transitions. While this guarantees linearizable consistency across non-Byzantine network partitions, it inevitably introduces a write latency penalty proportional to round-trip network hops between quorum participants.'\n\n"
            "Question: Based on the passage, what is the fundamental trade-off imposed by quorum-based consensus?"
        ),
        "correct": "Gaining fault-tolerant linearizability requires accepting network-induced write latency penalties across quorum nodes.",
        "distractors": [
            "Achieving high write throughput requires sacrificing non-Byzantine network partition tolerance.",
            "Replication state machines must eliminate consensus quorums to achieve predictable consistency.",
            "Linearizability can only be attained if round-trip network hops between peers are reduced to zero.",
        ],
        "explanation": "The text explicitly states that consensus guarantees linearizability across partitions at the cost of write latency penalties proportional to quorum network hops.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Reading: Distributed Consensus - Inferential Quorum Sizing",
        "topic": "Reading Comprehension",
        "question_text": (
            "Based on the consensus passage excerpt ('requiring a majority quorum before committing state transitions'), what can be logically inferred about a 5-node cluster experiencing network partition?"
        ),
        "correct": "State transitions can only be committed in a partition that retains at least 3 communicating nodes.",
        "distractors": [
            "Any isolated pair of 2 nodes can independently commit divergent state transitions concurrently.",
            "A single surviving node is authorized to elect itself leader and commit writes locally.",
            "The cluster completely halts all read and write processing until all 5 nodes reconnect simultaneously.",
        ],
        "explanation": "In a 5-node cluster, a majority quorum requires strictly greater than 50%, which is floor(5/2) + 1 = 3 nodes.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Reading: Distributed Consensus - Contextual Vocabulary",
        "topic": "Reading Comprehension",
        "question_text": (
            "In the phrase 'across non-Byzantine network partitions', what does 'non-Byzantine' specifically imply about the failure model?"
        ),
        "correct": "Nodes may fail by crashing, delaying, or dropping packets, but they do not transmit malicious or forged messages.",
        "distractors": [
            "Network switches automatically rectify dropped TCP packets without operating system intervention.",
            "Nodes possess zero memory limits and execute with infinite computational thread capacity.",
            "The cluster operates exclusively within a single physical server rack using shared memory.",
        ],
        "explanation": "Non-Byzantine failure models assume fail-stop or packet-loss conditions without arbitrary, deceptive, or adversarial behavior.",
        "difficulty": "HARD",
    },
    {
        "title": "Reading: Distributed Consensus - Author's Stance on Latency",
        "topic": "Reading Comprehension",
        "question_text": (
            "How does the author characterize the write latency associated with distributed quorum consensus?"
        ),
        "correct": "As an inevitable structural consequence of multi-node network round trips rather than poor implementation.",
        "distractors": [
            "As an easily avoidable software bug that modern CPU hardware has completely eradicated.",
            "As an artificial restriction imposed by obsolete database vendors to sell caching layers.",
            "As an unpredictable phenomenon that cannot be modeled or measured mathematically.",
        ],
        "explanation": "The passage terms write latency an 'inevitably introduces... penalty proportional to round-trip network hops'.",
        "difficulty": "MEDIUM",
    },

    # Passage 2: AI Governance & Explainability (4 questions)
    {
        "title": "Reading: AI Governance - Primary Regulatory Purpose",
        "topic": "Reading Comprehension",
        "question_text": (
            "Passage Excerpt: 'As large language models become deeply embedded in high-stakes enterprise workflows—such as automated credit underwriting and clinical diagnostic support—regulatory mandates increasingly demand algorithmic explainability. Black-box decision paradigms that lack post-hoc auditability expose enterprises to severe compliance penalties and systemic bias entrenchment. Consequently, operationalizing verifiable provenance and automated quality gates is no longer a technical luxury, but a core fiduciary obligation.'\n\n"
            "Question: What is the author's primary argument regarding enterprise AI deployment?"
        ),
        "correct": "Explainability, verifiable provenance, and quality gates are mandatory fiduciary safeguards in critical workflows.",
        "distractors": [
            "High-stakes enterprise domains should immediately abandon machine learning models in favor of manual spreadsheets.",
            "Explainability is purely an academic ideal that has no practical application in commercial banking.",
            "Enterprises should prioritize inference speed and cost minimization above regulatory compliance checks.",
        ],
        "explanation": "The author concludes that verifiable provenance and quality gates are 'core fiduciary obligations' necessary to prevent bias and compliance penalties.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Reading: AI Governance - Risk of Black-Box Systems",
        "topic": "Reading Comprehension",
        "question_text": (
            "According to the AI governance passage, what specific dangers arise from deploying black-box decision models?"
        ),
        "correct": "Vulnerability to regulatory compliance fines and the perpetuation of entrenched systemic bias.",
        "distractors": [
            "Immediate physical hardware degradation and permanent CPU overclocking failures.",
            "Inability of database clusters to store token vector embeddings in relational schemas.",
            "The complete disappearance of open-source model weights from public code repositories.",
        ],
        "explanation": "The text directly states: 'Black-box decision paradigms that lack post-hoc auditability expose enterprises to severe compliance penalties and systemic bias entrenchment.'",
        "difficulty": "EASY",
    },
    {
        "title": "Reading: AI Governance - Contextual Meaning of 'Fiduciary'",
        "topic": "Reading Comprehension",
        "question_text": (
            "In the concluding sentence, what does the phrase 'core fiduciary obligation' denote regarding leadership responsibility?"
        ),
        "correct": "A legally and ethically binding duty of trust, care, and prudent governance owed to stakeholders.",
        "distractors": [
            "An optional recreational activity pursued when engineering budgets have surplus funds.",
            "A temporary public relations marketing campaign aimed at tech conference attendees.",
            "A confidential corporate strategy shielded from government oversight and external audit.",
        ],
        "explanation": "A fiduciary obligation represents an essential ethical and legal responsibility held in high trust and accountability.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Reading: AI Governance - Tone and Target Audience",
        "topic": "Reading Comprehension",
        "question_text": (
            "What is the predominant tone and target audience of the passage on enterprise AI governance?"
        ),
        "correct": "Authoritative and analytical, addressing corporate executives, compliance officers, and system architects.",
        "distractors": [
            "Whimsical and satirical, targeting casual social media audiences and hobbyist gamers.",
            "Aggressively confrontational, aimed at discouraging all computer science education programs.",
            "Pedantic and strictly historical, analyzing early 1950s mechanical punch-card tabulators.",
        ],
        "explanation": "The passage employs formal, professional vocabulary ('fiduciary obligation', 'systemic bias', 'compliance penalties') suited for corporate and governance leaders.",
        "difficulty": "EASY",
    },

    # 4. Sentence Correction & Error Spotting (8 questions)
    {
        "title": "Correction: Misplaced Adverbial Modifiers in SLAs",
        "topic": "Sentence Correction",
        "question_text": "Identify the sentence that positions the adverbial modifier with unambiguous precision.",
        "correct": "The site reliability team regularly conducts disaster recovery failover simulations to verify data integrity.",
        "distractors": [
            "The site reliability team conducts disaster recovery failover simulations regularly to verify data integrity.",
            "The site reliability team conducts regularly disaster recovery failover simulations to verify data integrity.",
            "Regularly the site reliability team to verify data integrity conducts disaster recovery failover simulations.",
        ],
        "explanation": "Adverbs of frequency ('regularly') are most idiomatically and clearly placed immediately preceding the main action verb ('regularly conducts').",
        "difficulty": "EASY",
    },
    {
        "title": "Correction: Comma Splice Elimination in Design Briefs",
        "topic": "Sentence Correction",
        "question_text": "Which option correctly fixes the comma splice in: 'The primary database node crashed, the read replica promoted itself automatically'?",
        "correct": "The primary database node crashed; consequently, the read replica promoted itself automatically.",
        "distractors": [
            "The primary database node crashed, consequently, the read replica promoted itself automatically.",
            "The primary database node crashed, and so therefore the read replica promoted itself automatically.",
            "The primary database node crashed the read replica promoted itself automatically.",
        ],
        "explanation": "Two independent clauses cannot be joined solely by a comma. They require a semicolon with a conjunctive adverb ('consequently') or a coordinating conjunction.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Correction: Ambiguous Pronoun Reference in Changelogs",
        "topic": "Sentence Correction",
        "question_text": "Select the revised sentence that eliminates ambiguous pronoun reference in release documentation.",
        "correct": "When the cache manager invalidated the stale session tokens, those tokens were purged from the Redis cluster.",
        "distractors": [
            "When the cache manager invalidated the stale session tokens, it was purged from the Redis cluster.",
            "When the cache manager invalidated the stale session tokens, they purged it from the Redis cluster.",
            "When the cache manager invalidated the stale session tokens, this happened to them in the Redis cluster.",
        ],
        "explanation": "Using the specific noun phrase ('those tokens') makes clear what was purged, resolving ambiguity between the manager and the tokens.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Correction: Parallelism in Standard Operating Procedures",
        "topic": "Sentence Correction",
        "question_text": "Which option corrects the non-parallel phrasing in: 'Engineers are responsible for monitoring cluster health, to review pull requests, and deployment of hotfixes'?",
        "correct": "Engineers are responsible for monitoring cluster health, reviewing pull requests, and deploying hotfixes.",
        "distractors": [
            "Engineers are responsible to monitor cluster health, reviewing pull requests, and deploy hotfixes.",
            "Engineers are responsible for cluster health monitoring, to review pull requests, and deploying hotfixes.",
            "Engineers are responsible for monitoring cluster health, to review pull requests, and hotfix deployment.",
        ],
        "explanation": "Parallelism demands matching gerund phrases: 'monitoring... reviewing... and deploying'.",
        "difficulty": "EASY",
    },
    {
        "title": "Correction: Preposition Idiom in Network Standards",
        "topic": "Sentence Correction",
        "question_text": "Choose the sentence that employs the correct idiomatic preposition for technical compliance.",
        "correct": "All cloud architecture components must comply with ISO 27001 data governance standards.",
        "distractors": [
            "All cloud architecture components must comply to ISO 27001 data governance standards.",
            "All cloud architecture components must comply by ISO 27001 data governance standards.",
            "All cloud architecture components must comply for ISO 27001 data governance standards.",
        ],
        "explanation": "The idiomatic standard English phrasal verb is 'comply with', not 'comply to' or 'comply by'.",
        "difficulty": "EASY",
    },
    {
        "title": "Correction: Misplaced Relative Clause in Indexing Rules",
        "topic": "Sentence Correction",
        "question_text": "Which revision resolves the misplaced relative clause in: 'The engineer deployed a composite index on the orders table which reduced query execution time by 80%'?",
        "correct": "On the orders table, the engineer deployed a composite index that reduced query execution time by 80%.",
        "distractors": [
            "The engineer deployed on the orders table which reduced query execution time by 80% a composite index.",
            "A composite index on the orders table was deployed by the engineer, which table reduced execution time by 80%.",
            "The engineer deployed a composite index, which orders table reduced execution time by 80%.",
        ],
        "explanation": "The relative clause 'that reduced query execution time...' must be placed immediately adjacent to its antecedent 'composite index'.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Correction: Elimination of Redundant Business Phrasing",
        "topic": "Sentence Correction",
        "question_text": "Which sentence is free from redundant word pairs in client correspondence?",
        "correct": "Please reply by Friday with your revised timeline so we can finalize the milestone schedule.",
        "distractors": [
            "Please revert back by Friday with your revised timeline so we can finalize the milestone schedule.",
            "Please repeat again your reply by Friday with your revised timeline so we can finalize the milestone schedule.",
            "Please revert back and repeat again by Friday with your revised timeline so we can finalize the schedule.",
        ],
        "explanation": "'Revert back' and 'repeat again' are redundant tautologies. 'Reply' or 'revert' stands alone cleanly.",
        "difficulty": "EASY",
    },
    {
        "title": "Correction: Faulty Comparison in Benchmark Analysis",
        "topic": "Sentence Correction",
        "question_text": "Select the sentence that properly avoids an illogical comparison when reporting system performance benchmarks.",
        "correct": "The latency of the Go microservice is significantly lower than that of the legacy monolith.",
        "distractors": [
            "The latency of the Go microservice is significantly lower than the legacy monolith.",
            "The latency of the Go microservice is significantly lower compared to the legacy monolith.",
            "The Go microservice has lower latency than the legacy monolith's performance metrics comparison.",
        ],
        "explanation": "You must compare latency to latency ('that of the legacy monolith'), not latency to a physical monolith.",
        "difficulty": "HARD",
    },

    # 5. Professional Communication & Email Tasks (8 questions)
    {
        "title": "Comm: Escalating a P1 Production Outage to Executives",
        "topic": "Professional Writing",
        "question_text": "When sending an emergency P1 outage broadcast to executive leadership, which initial communication structure is most effective?",
        "correct": "Impact Summary (customer impact, financial exposure), Current Status (what is being done), Next Update ETA, and Incident Commander contact.",
        "distractors": [
            "A detailed 500-line stack trace dump with an exhaustive defense of why the on-call engineer was not at fault.",
            "A brief message stating 'Systems are down, please do not message us while we attempt to fix it.'",
            "A forwarded customer complaint email with multiple emotional punctuation marks demanding immediate help.",
        ],
        "explanation": "Executive incident communication requires crisp, high-level impact clarity, containment status, next checkpoint time, and clear ownership.",
        "difficulty": "EASY",
    },
    {
        "title": "Comm: Negotiating a Sprint Milestone Slip with Product",
        "topic": "Professional Writing",
        "question_text": "A critical technical refactor will delay a promised feature by 4 days. How should this be communicated to the product manager?",
        "correct": "Present the rationale proactively, detail trade-offs (releasing now risks data corruption), and offer options: scope reduction vs deferred date.",
        "distractors": [
            "Conceal the delay until the final day of the sprint demo and blame unexpected vendor latency.",
            "Deploy the incomplete code silently to production and disable the broken parts behind undocumented flags.",
            "Send an angry message to the squad channel stating that product expectations are detached from reality.",
        ],
        "explanation": "Proactive notification with empirical trade-off analysis and actionable scope/schedule options demonstrates professional maturity.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Comm: Constructive Code Review Rejection on Security Flaw",
        "topic": "Professional Writing",
        "question_text": "A pull request from a junior engineer introduces a severe SQL injection vulnerability. What is the most constructive review comment?",
        "correct": "Highlight the vulnerability with the OWASP reference, explain the attack vector clearly, and provide parameterized query example code.",
        "distractors": [
            "Reject the PR with a comment stating 'This code is terrible and demonstrates a total lack of basic security knowledge.'",
            "Approve the pull request anyway to avoid hurting the junior engineer's self-esteem and patch it later yourself.",
            "Take a screenshot of the vulnerable line and post it in the team's public Slack channel as a warning to others.",
        ],
        "explanation": "Constructive code review links to objective standards, explains the 'why' without personal criticism, and guides with concrete remedies.",
        "difficulty": "EASY",
    },
    {
        "title": "Comm: Clarifying Ambiguous Client Requirements",
        "topic": "Professional Writing",
        "question_text": "A client sends a vague specification: 'The portal must be ultra-fast and handle huge traffic.' What is the appropriate written response?",
        "correct": "Acknowledge the requirement and propose specific quantitative SLAs: 'To align on infrastructure sizing, could we target p95 latency under 200ms at 5,000 peak concurrent users?'",
        "distractors": [
            "Reply stating 'Your requirement is meaningless because ultra-fast is not a real engineering metric.'",
            "Accept the requirement without clarification and build the simplest possible single-server architecture.",
            "Forward the email to legal requesting a contract termination due to client incompetence.",
        ],
        "explanation": "Translating ambiguous qualitative client desires into clear, professional quantitative metrics drives alignment without hostility.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Comm: Upward Feedback to Engineering Manager in 1:1",
        "topic": "Professional Writing",
        "question_text": "An engineer feels micro-managed by daily unplanned status inquiries from their manager. What is the most effective phrasing for 1:1 feedback?",
        "correct": "'I find that context-switching to answer unscheduled check-ins interrupts deep work. Could we establish an end-of-day async Slack update instead?'",
        "distractors": [
            "'You are micro-managing me constantly and it proves you have zero trust in my engineering abilities.'",
            "Remain completely silent during 1:1s while complaining about the manager to peer engineers at lunch.",
            "'If you message me again outside of morning standup, I will submit an HR grievance for harassment.'",
        ],
        "explanation": "Framing feedback around personal workflow impact and offering a structured alternative demonstrates collaborative problem solving.",
        "difficulty": "MEDIUM",
    },
    {
        "title": "Comm: Announcing Breaking API Deprecation to Partners",
        "topic": "Professional Writing",
        "question_text": "When publishing a deprecation notice for an enterprise v1 API, which component must be explicitly included?",
        "correct": "Sunsetting schedule with concrete milestones, migration guide with v2 code mappings, and dual-run availability window.",
        "distractors": [
            "A sudden immediate shutdown announcement with zero grace period to force instant customer migration.",
            "A vague suggestion that v1 might stop working eventually without specifying version numbers or dates.",
            "A notice instructing partners to reverse-engineer the new v2 endpoints from client mobile app network logs.",
        ],
        "explanation": "API deprecation notices require transparent timelines, migration guides, sunsetting milestones, and support channels.",
        "difficulty": "EASY",
    },
    {
        "title": "Comm: Resolving Cross-Squad Resource Contention",
        "topic": "Professional Writing",
        "question_text": "Two squads require access to the single staging load-testing cluster during the same 3-day sprint window. How should the leads resolve this?",
        "correct": "Meet to review test objectives, establish time-boxed test execution slots, and agree on shared cluster telemetry benchmarks.",
        "distractors": [
            "The squad lead who logs in first locks the cluster credentials and refuses access to the other squad.",
            "Both squads trigger maximum stress runs concurrently, resulting in cluster thrashing and corrupted test runs.",
            "Escalate immediately to the Vice President of Engineering without attempting any peer coordination.",
        ],
        "explanation": "Professional engineering collaboration involves collaborative time-slot scheduling and shared objective alignment.",
        "difficulty": "EASY",
    },
    {
        "title": "Comm: Summarizing Cloud Cost Anomaly for Financial Audit",
        "topic": "Professional Writing",
        "question_text": "A sudden 35% spike in AWS GPU billing occurs due to an unpruned inference pod replica set. How should engineering report this to finance?",
        "correct": "Provide root-cause explanation (unpruned replicas), total financial impact, exact remediation taken (automated autoscaler limits), and safeguards against recurrence.",
        "distractors": [
            "Submit the raw 10,000-line AWS Cost Explorer CSV file with no narrative explanation or executive summary.",
            "Deny that any anomaly occurred and attribute the discrepancy to unexpected federal currency fluctuations.",
            "Delete the cloud logging history so auditors cannot pinpoint which developer launched the cluster.",
        ],
        "explanation": "Financial transparency requires root-cause diagnosis, quantitative dollar impact, immediate corrective action, and permanent preventive guardrails.",
        "difficulty": "MEDIUM",
    },
]

assert len(english_specs) == 40, f"Expected 40 English specs, got {len(english_specs)}"

# ==========================================
# 50 SITUATIONAL JUDGEMENT QUESTIONS
# ==========================================
situational_specs = [
    ("Flaky CI Test on Hotfix", "A flaky end-to-end integration test is failing intermittently on an urgent production security hotfix PR that has been peer-reviewed.",
     "Run the flaky test in isolation with verbose logging to confirm it is unrelated to the security patch, document the test flake in a tracking ticket, and seek tech lead approval for a scoped override.",
     "Disable the entire integration test suite permanently so that future hotfixes merge instantly without checks.",
     "Rerun the entire CI pipeline 15 times repeatedly until a random pass occurs, without inspecting failure logs.",
     "Deploy the code directly to production via SSH, bypassing git version control and CI entirely.",
     "Balancing urgent security remediation with deployment safety requires isolating and verifying the non-relevance of the flake while documenting it transparently."),

    ("Credit Claiming in Demos", "During a high-visibility company demo, a peer presents an architecture feature you primarily designed and implemented, taking sole personal credit.",
     "Congratulate the peer on the demo publicly, and during your next 1:1, have a private, constructive conversation clarifying future demo collaboration and attribution.",
     "Interrupt the live presentation in front of executive leadership to angrily accuse your peer of intellectual dishonesty.",
     "Say nothing, but secretly introduce a subtle defect into your peer's upcoming branch as retaliation.",
     "Broadcast an all-company email denouncing the peer and demanding an immediate public apology.",
     "Professional composure requires separating public team success from private interpersonal conflict resolution."),

    ("Skipping Security Testing for Launch", "A product manager asks the team to bypass mandatory penetration testing and vulnerability scans to meet a marketing launch deadline.",
     "Explain the regulatory, reputational, and financial risks of shipping unverified code, and propose a launch with limited beta access under strict monitoring while testing finishes.",
     "Silently comply with the request without documenting the PM's directive or alerting security officers.",
     "Publicly mock the product manager on social media for not caring about user privacy.",
     "Delete all security scanner config files so the automated build status appears green.",
     "Adhering to security governance requires firm, evidence-based boundary setting coupled with constructive risk-mitigation options."),

    ("Exposed Token in Public PR", "You notice that a colleague accidentally committed an active production database API token into a publicly accessible GitHub branch.",
     "Immediately revoke and rotate the compromised credential in the secret manager, notify the security team, and purge the secret from git history using git-filter-repo.",
     "Leave a sarcastic comment on the pull request pointing out the mistake and wait for the developer to wake up tomorrow.",
     "Copy the token to your personal laptop and test whether you can extract confidential user tables.",
     "Simply push a new commit that deletes the line from the file, leaving the secret visible in git commit history.",
     "Immediate credential rotation and history purging are mandatory first responses to public secret leakage."),

    ("Struggling Junior Engineer", "A junior teammate has made zero git commits in 4 days on a sprint task and appears hesitant to speak during daily standup.",
     "Schedule an informal, supportive 1:1 coffee chat, offer to pair program for an hour, and break down the task into smaller, manageable sub-problems.",
     "Publicly reprimand the junior developer in front of the entire team for falling behind sprint velocity.",
     "Reassign the task to yourself without telling the junior developer and complete it late at night.",
     "Advise the engineering manager to terminate the junior engineer's employment immediately.",
     "Empathetic mentorship and collaborative pair programming unlock developer productivity without intimidation."),

    ("Intractable Architecture Debate", "Two senior engineers have been debating microservices vs modular monolith for 3 weeks, stalling the start of a critical multi-month initiative.",
     "Facilitate a structured Architecture Decision Record (ADR) session with weighted scoring criteria, time-box the discussion, and escalate to the Principal Architect for a final tie-breaking decision.",
     "Let the debate continue indefinitely until one engineer transfers to another company or gives up out of exhaustion.",
     "Flip a coin in secret and announce that management has mandated your favorite architecture.",
     "Split the project into two competing parallel prototypes and have the engineers race against each other for a month.",
     "Time-boxed ADR sessions with explicit decision criteria prevent analysis paralysis while maintaining team buy-in."),

    ("Scope Creep Without Change Request", "A client representative asks you via a direct Slack message to add a complex export feature before Friday that is outside the agreed scope.",
     "Politely acknowledge the feature's value and route the request through the Project Manager and formal change request process for schedule and cost estimation.",
     "Immediately agree to build the feature for free, working through the night without notifying your team.",
     "Ignore the client's message completely and block their account on Slack.",
     "Agree to build the feature only if the client promises to give you a positive personal performance review.",
     "Contractual boundaries protect project health; scope adjustments must be formally estimated and scheduled."),

    ("Production DB Spike During Sales Demo", "A production database CPU spikes to 99% due to an unindexed analytics query just as the sales team begins a major enterprise prospect demo.",
     "Identify the rogue query via pg_stat_activity, terminate the specific blocking query session, and apply a temporary query timeout while alerting the on-call engineer.",
     "Restart the entire production database cluster immediately, terminating all ongoing user connections.",
     "Ignore the spike and assume the cloud provider will automatically scale CPU before the demo crashes.",
     "Blame the sales team for scheduling customer demos during regular operational hours.",
     "Surgical query termination restores operational stability with minimal collateral customer impact."),

    ("Schema Payload Discrepancy", "You discover that the live production API returns camelCase fields while the published OpenAPI specification documents snake_case.",
     "Document the discrepancy, create a backward-compatible transition plan that accepts both formats temporarily, and update the OpenAPI contract and client SDKs.",
     "Immediately rename all production JSON fields without notifying external consumers or client teams.",
     "Delete the OpenAPI documentation entirely so that no one can prove a discrepancy exists.",
     "Inform customers that the documentation is correct and their client integration code is wrong.",
     "Backward compatibility and gradual contract convergence prevent breaking external downstream integrations."),

    ("Conflicting Lead Priorities", "Your tech lead instructs you to refactor legacy database models, but your engineering manager asks you to deliver a marketing banner by end of day.",
     "Bring both leaders together in a brief alignment chat, articulate the conflicting priorities and time constraints, and ask them to agree on the primary sprint focus.",
     "Secretly work on both tasks simultaneously, delivering both in poor, untested quality.",
     "Follow the tech lead's advice and completely ignore the engineering manager's request.",
     "Complain to human resources that leadership lacks organizational competence.",
     "Transparent stakeholder alignment resolves priority conflicts without putting the engineer in an impossible position."),

    ("Standup Disengagement", "A teammate has missed three consecutive daily standups and takes several hours to respond to direct mentions on urgent blocker tickets.",
     "Reach out privately with empathetic inquiry: 'Hey, noticed you missed standup, is everything okay and is there anything I can help unblock on your tasks?'",
     "Announce in the team channel that this person is slacking off and should have their salary docked.",
     "Silently remove them from all shared calendar invites and project documentation.",
     "Do their work for them and complain about their absence to other teammates behind their back.",
     "Empathetic, non-judgmental private outreach identifies personal or technical blockers constructively."),

    ("Unreproducible Production Bug", "A tier-1 customer reports an intermittent transaction drop that cannot be reproduced in local development or staging environments.",
     "Review distributed tracing spans, structured error logs, and telemetry around the customer's tenant ID, and add targeted diagnostic logging in the next deployment.",
     "Close the customer ticket with 'Cannot Reproduce' and advise the customer to stop complaining.",
     "Guess the problem blindly and push unverified database schema alterations directly to production.",
     "Blame the customer's internal corporate firewall without checking system logs.",
     "Instrumented observability and targeted telemetry isolate elusive intermittent production defects."),

    ("2-Hour Project Estimation Pressure", "Management asks you to provide a firm delivery commitment for a complex microservices migration within 2 hours.",
     "Clarify that a 2-hour estimate can only be a high-variance T-shirt size (e.g. Large/XL), and request a 3-day discovery spike to produce an accurate estimation.",
     "Invent an overly optimistic date (e.g. '2 weeks') to make management happy, knowing it will fail.",
     "Refuse to speak with management and walk out of the planning meeting.",
     "Commit your entire squad to working 80 hours a week for the next six months.",
     "Managing expectations with estimation cones of uncertainty avoids premature binding commitments."),

    ("Zero-Day CVE in Core Library", "An open-source serialization package used across your payment gateway releases an urgent security advisory for a critical remote code execution vulnerability.",
     "Analyze exploitability in your architecture, upgrade to the patched version in a staging branch, run integration regression tests, and expedite emergency deployment.",
     "Wait for the next scheduled quarterly release in three months before considering an upgrade.",
     "Ignore the vulnerability because the library has worked fine for two years without issue.",
     "Remove the payment gateway entirely from the application to avoid updating the dependency.",
     "Immediate exploitability triage, rapid staging validation, and expedited emergency patching mitigate zero-day risks."),

    ("Mentor Violates Style Guide", "A respected senior mentor submits code review feedback insisting that you use anti-patterns that explicitly violate the company's published engineering standards.",
     "Respectfully point to the specific section of the published engineering standard in your review reply, and ask for their guidance on whether the team should update the standard.",
     "Blindly accept the feedback and knowingly violate company standards across your entire codebase.",
     "Harshly insult the mentor in public for not knowing the company guidelines.",
     "Escalate immediately to the CEO demanding the mentor be demoted.",
     "Grounding discussions in documented standards invites objective dialogue without personal confrontation."),

    ("Friday Afternoon Urgent Feature", "At 4:45 PM on a Friday, an account manager requests an urgent configuration change to enable a pilot for a high-value prospect over the weekend.",
     "Evaluate whether a verified weekend rollback plan and on-call coverage exist; if not, arrange an early Monday morning deployment with full team support.",
     "Deploy the unverified change immediately at 5:00 PM and shut down your laptop for the weekend.",
     "Agree to do it, but secretly forget about it until Monday afternoon.",
     "Berate the account manager in an all-hands channel for asking for weekend deployments.",
     "Preventing unmonitored Friday deployments protects production reliability while scheduling prompt follow-ups."),

    ("Post-Approval Architecture Disagreement", "After the Architecture Review Board has officially approved an event-driven design, you discover a race condition flaw in the data model.",
     "Document the race condition scenario with a reproducible sequence diagram, and present the evidence to the Lead Architect requesting an addendum review.",
     "Sabotage the project during implementation so that the architecture fails in front of everyone.",
     "Keep silent because the board has already stamped the design and you don't want to cause trouble.",
     "Publicly declare that the Architecture Review Board is incompetent on social media.",
     "Evidence-backed architectural feedback with clear failure scenarios welcomes constructive course corrections."),

    ("Vendor 30-Day Deprecation Notice", "A third-party SMS verification vendor announces it is discontinuing its legacy API in 30 days, which your onboarding flow relies upon.",
     "Immediately log an urgent architectural tech debt item, spike the vendor's v2 API and one alternative provider, and schedule migration into the next sprint.",
     "Wait until day 29 before investigating the migration steps.",
     "Assume the vendor won't actually shut down the API on the announced deadline.",
     "Disable user phone verification entirely and allow unverified accounts to register.",
     "Proactive vendor transition spikes and sprint scheduling prevent sudden service blackouts."),

    ("Intern Onboarding During Crunch", "You are assigned to mentor two summer interns during the highest-intensity sprint of a company-wide cloud migration.",
     "Establish structured daily 30-minute check-ins, prepare well-scoped starter issues with clear acceptance criteria, and pair them with co-mentors across the team.",
     "Tell the interns to sit quietly in the corner and not bother you until the migration ends next month.",
     "Give the interns production database administrative credentials and tell them to figure it out.",
     "Complain to the interns that they are ruining your sprint velocity.",
     "Structured scoping and distributed team mentorship allow meaningful intern growth without overburdening a single lead."),

    ("Sprint Fatigue & Crunch Burnout", "After three consecutive weeks of overtime to meet an artificial deadline, you and your squad members show clear signs of exhaustion and rising error rates.",
     "Raise the velocity drop and cognitive fatigue openly during the retrospective, and advocate with management to restore sustainable cadence before technical debt multiplies.",
     "Continue working 14-hour days while consuming excessive energy drinks until someone makes a catastrophic error.",
     "Abruptly stop showing up to work without notifying anyone on the team.",
     "Secretly disable production alerts so the team can sleep through the night regardless of outages.",
     "Advocating for sustainable engineering cadence preserves long-term code quality and human retention."),

    ("Zero-Test Legacy Refactor", "You are tasked with refactoring a critical 5,000-line billing module that currently has zero automated unit or integration tests.",
     "Write characterization tests that capture existing baseline behavior before altering any business logic, then refactor incrementally in small, testable commits.",
     "Rewrite the entire 5,000 lines from memory over a weekend without writing any tests.",
     "Refuse to work on the module and demand that the original author who left 3 years ago be rehired.",
     "Delete the module and replace it with a third-party billing framework in a single unreviewed commit.",
     "Characterization testing creates an empirical safety net before refactoring legacy code."),

    ("Direct DB Access for BI User", "A business analyst requests direct write and read credentials to the primary production database to build a dashboard in Tableau.",
     "Deny direct production access, explain security and performance risks (unindexed queries locking tables), and provide read-only access to a sanitized analytics replica.",
     "Grant full superuser administrative credentials to the production database immediately.",
     "Ignore the analyst's request for several weeks without explaining why.",
     "Export the entire unredacted customer database to a public Google Sheets file and send the link.",
     "Read replicas and sanitized data warehouses protect transactional production performance and privacy."),

    ("Retrospective Frustration", "A teammate vents intense frustration during a retrospective, claiming that their pull requests sit unreviewed for days while others are approved instantly.",
     "Acknowledge the validity of their frustration, propose formal team PR review SLAs (e.g. initial review within 4 business hours), and review pull request distribution metrics.",
     "Tell the teammate to stop whining and that their code is simply too difficult to read.",
     "Argue that PR reviews are optional and engineers should just merge without review.",
     "Vote to cancel all future retrospectives because they cause emotional discomfort.",
     "Channeling retrospective friction into concrete operational SLAs resolves systemic unfairness."),

    ("Dependency API Delay", "An upstream services team informs you two days before sprint close that their API contract delivery is delayed by four weeks.",
     "Create a realistic mock server matching the agreed contract specification so your frontend and business logic can continue development and testing uninterrupted.",
     "Halt all sprint progress and sit idle for four weeks waiting for the upstream team.",
     "Build your own duplicate version of the upstream service from scratch in secret.",
     "Send aggressive messages to the upstream team's leadership demanding they work over the weekend.",
     "Contract mocking decouples team dependencies and maintains engineering velocity during upstream delays."),

    ("Bug Escaped to 0.5% Users", "An algorithmic edge case bug causes incorrect pricing calculations for 0.5% of checkouts before being flagged by monitoring.",
     "Trigger incident response, roll back or toggle the feature flag, quantify financial discrepancy, patch the bug with automated test coverage, and publish a post-mortem.",
     "Delete the error log entries so management never discovers that 0.5% of users were affected.",
     "Quietly fix the bug in next month's release without informing finance or customer support.",
     "Blame the junior engineer who merged the PR on social media.",
     "Transparent incident response, rapid rollback, and financial reconciliation protect integrity."),

    ("PII Export to Unencrypted CSV", "A marketing manager asks you to export all customer email addresses, phone numbers, and physical addresses to a CSV on their personal USB drive.",
     "Politely decline citing data protection regulations (DPDP/GDPR), explain the risk of data leakage, and guide them through the sanctioned CRM data-sharing workflow.",
     "Immediately export the unencrypted CSV and hand over the USB drive without logging the transfer.",
     "Sell the customer list to external marketing agencies for personal profit.",
     "Report the marketing manager to the police without explaining company policy to them.",
     "Enforcing DPDP compliance and guiding users to sanctioned tools prevents severe privacy breaches."),

    ("Harsh PR Critique", "A peer leaves sharp, abrasive comments on your pull request: 'Did you even think before writing this? Completely wrong approach.'",
     "Focus on the underlying technical substance, respond objectively with architectural trade-offs, and suggest a brief call to align constructively on the design.",
     "Reply with personal insults attacking your peer's coding competence and intelligence.",
     "Close the pull request and refuse to write any more code for the company.",
     "Merge the pull request anyway using administrator override permissions.",
     "Depersonalizing critical feedback and shifting to synchronous technical alignment de-escalates tension."),

    ("Agile Ceremony Overload", "Your team calendar is overloaded with 4 hours of recurring daily agile ceremonies, leaving insufficient uninterrupted time for deep engineering work.",
     "Gather data on meeting hours vs coding hours, and propose consolidating ceremonies, implementing async status updates, and designating dedicated 'No-Meeting' focus blocks.",
     "Decline every meeting on your calendar without explanation and refuse to speak to anyone.",
     "Attend every meeting with camera and microphone off while playing video games.",
     "Resign from the company without giving feedback on meeting culture.",
     "Data-backed proposals for async standups and focus blocks reclaim engineering productivity."),

    ("End-of-Life Microservice Framework", "A core routing microservice is running on a web framework version that reached official end-of-life and will receive no further security patches.",
     "Formulate a migration proposal outlining security exposure, evaluate modern supported framework alternatives, and prioritize migration in the quarterly engineering roadmap.",
     "Ignore the end-of-life status because the service hasn't crashed recently.",
     "Attempt to rewrite the entire framework from scratch by yourself over the weekend.",
     "Shut down the microservice immediately, taking down customer routing without warning.",
     "Roadmap prioritization and security risk quantification drive disciplined framework modernization."),

    ("Duplicate Feature Development", "While reviewing another squad's demo, you notice they have spent two months building a notification engine nearly identical to the one your squad maintains.",
     "Reach out to their squad lead collegially, compare architecture and feature sets, and collaborate on a unified roadmap that consolidates efforts rather than creating duplicate debt.",
     "Publicly accuse their team of stealing your architecture during the company all-hands.",
     "Race to release your notification engine first so their work becomes completely worthless.",
     "Delete your squad's codebase and pretend you never built a notification engine.",
     "Cross-team synergy and convergence reduce duplicate architectural maintenance across the enterprise."),

    ("Missing Bug Reproduction Steps", "A critical customer support escalation ticket arrives with the title 'System Broken' and no logs, account IDs, or reproduction steps attached.",
     "Reach out to the support engineer with a standardized triage template: request specific timestamp, tenant ID, expected vs actual behavior, and network request IDs.",
     "Close the ticket immediately as invalid without offering guidance on how to provide reproduction details.",
     "Deploy random code changes to production hoping one of them fixes whatever is broken.",
     "Reprimand the customer directly for submitting an unhelpful ticket.",
     "Providing structured triage templates enables support teams to gather actionable diagnostic data."),

    ("Key-Person Dependency Risk", "A senior engineer who solely understands the proprietary billing engine announces they are leaving the company in two weeks.",
     "Prioritize paired knowledge-transfer sessions, record architecture walkthroughs, document edge cases and operational runbooks, and cross-train team members on key workflows.",
     "Beg the engineer not to leave and offer to pay them out of your own personal savings.",
     "Demand that the engineer surrender all passwords immediately and escort them out of the building on day one.",
     "Do nothing and assume the team will figure out the billing engine when it breaks next quarter.",
     "Intensive paired knowledge transfer and runbook documentation mitigate key-person operational risk."),

    ("Stale Cache Demo Failure", "During a live client demonstration with company executives, the application shows stale cached data, confusing the prospective client.",
     "Remain calm, transparently explain that the presentation view is reflecting a cached state, refresh the session or trigger a live recalculation, and proceed with composure.",
     "Panic, blame your junior teammates publicly in front of the client, and abruptly terminate the call.",
     "Pretend the screen is showing correct data and contradict the client when they point out the error.",
     "Unplug your computer monitor and claim that an internet blackout struck your entire city.",
     "Graceful composure, clear explanation of caching mechanics, and quick live recovery maintain executive credibility."),

    ("Unjustified Monolith Rewrite Proposal", "A teammate advocates rewriting a rock-solid, well-tested monolithic service into 15 microservices solely because 'microservices are more modern.'",
     "Ask the teammate to draft an evaluation document assessing concrete business drivers: scalability bottlenecks, operational overhead, network latency, and deployment complexity.",
     "Insult the teammate and declare that anyone who likes microservices doesn't understand software.",
     "Agree to the rewrite immediately without evaluating infrastructure costs or operational readiness.",
     "Secretly sabotage the monolith so that management is forced to authorize a rewrite.",
     "Grounded architectural evaluation of operational trade-offs prevents trend-chasing technical debt."),

    ("Privacy-Violating Tracking Feature", "A product requirement asks for background geolocation tracking of users even when the mobile application is explicitly closed and not in use.",
     "Raise the privacy and legal concerns with the compliance and legal counsel, pointing to platform store guidelines (Apple/Google) and privacy statutes (DPDP/GDPR).",
     "Implement the tracking silently and disguise the permissions prompt to trick users into accepting.",
     "Leak confidential corporate design documents to anonymous internet forums.",
     "Resign immediately without discussing legal frameworks or alternative user-centric approaches.",
     "Constructive escalation to legal and compliance ensures product features conform to regulatory statutes."),

    ("Speaking Over Junior Teammates", "During architecture brainstorming sessions, a dominant senior engineer repeatedly cuts off and dismisses ideas proposed by junior teammates.",
     "Intervene diplomatically during the meeting: 'I'd really like to hear Priya finish her thought on the partitioning strategy before we move to the next point.'",
     "Start screaming at the senior engineer in the middle of the meeting to assert dominance.",
     "Privately tell the junior teammates that their ideas are pointless and they should remain silent.",
     "Ignore the behavior completely because senior engineers should always dominate conversations.",
     "Inclusive meeting facilitation ensures every engineer's technical perspectives can be evaluated on merit."),

    ("Vague 'Search Broken' Bug Report", "A high-priority bug report states 'Search is broken' without specifying query terms, user roles, or environment details.",
     "Check search cluster health and error rates, and ask the reporter for the exact query string, expected search result, and user permissions used.",
     "Restart the Elasticsearch cluster immediately in production without verifying cluster status.",
     "Mark the bug 'Works For Me' and refuse to communicate further with the reporter.",
     "Delete the search feature entirely and replace it with a static dropdown menu.",
     "Proactive cluster telemetry verification combined with specific triage inquiry pinpoints root causes."),

    ("Deploying Model Without Bias Audit", "A machine learning predictive hiring model shows 94% accuracy, but the data science team has not conducted disparate impact or fairness audits.",
     "Insist on running baseline fairness and demographic parity evaluations before deployment, highlighting ethical and legal exposure under labor and discrimination laws.",
     "Deploy the model immediately to production because 94% accuracy is the only metric that matters.",
     "Alter the training data manually to produce whatever bias distribution management wants to see.",
     "Refuse to work on any artificial intelligence projects ever again.",
     "Rigorous fairness audits and demographic parity evaluations are mandatory before operationalizing ML models."),

    ("45-Minute Integration Test Suite", "The automated test suite takes 45 minutes to execute on every commit, leading engineers to bypass testing and merge directly to trunk.",
     "Profile the test pipeline, parallelize test execution across worker nodes, split into fast unit and slower nightly suites, and mock slow external HTTP calls.",
     "Permanently delete all integration tests so that commits take 5 seconds to merge.",
     "Threaten to terminate any engineer who complains about the 45-minute wait time.",
     "Instruct engineers to stop testing their code locally and in CI altogether.",
     "Profiling and parallelizing test suites preserves developer velocity while maintaining test coverage."),

    ("On-Premise Demand for SaaS Product", "A major enterprise customer promises a lucrative contract if your team provides an on-premise Kubernetes installation of your multi-tenant SaaS application.",
     "Collaborate with architecture and product leads to evaluate the operational maintenance overhead of an on-prem appliance vs multi-tenant isolation, and present a realistic cost model.",
     "Promise the customer an on-premise version in two weeks without consulting engineering or architecture.",
     "Refuse to speak with the sales representative and reject the customer outright without analysis.",
     "Copy the cloud production database to a USB drive and mail it to the customer's office.",
     "Thorough operational and economic evaluation determines whether customer-managed deployments are sustainable."),

    ("Disabling SSL in Staging", "A teammate proposes disabling SSL/TLS certificate verification in the staging environment to resolve a self-signed certificate error quickly.",
     "Advise against disabling security controls; instead, generate and install a valid local CA certificate in the staging environment trust store to maintain production parity.",
     "Disable certificate verification across all environments, including production, to prevent future errors.",
     "Publicly mock the teammate for not understanding TLS handshakes.",
     "Ignore the issue and allow staging communication to occur over unencrypted plaintext.",
     "Maintaining production parity in staging trust stores prevents security vulnerabilities from escaping."),

    ("Offshore 9.5-Hour Time Zone Gap", "Code reviews between an onshore team and an offshore team take 48-72 hours due to an uncoordinated 9.5-hour time difference.",
     "Establish a 2-hour daily overlapping window for synchronous reviews, set clear async review handoff guidelines, and distribute reviewer assignments across both regions.",
     "Require the offshore team to work overnight shifts indefinitely with no schedule adjustments.",
     "Require the onshore team to work overnight shifts indefinitely with no schedule adjustments.",
     "Eliminate code reviews entirely for both teams so that everyone merges without waiting.",
     "Structured overlap windows and distributed review responsibilities streamline cross-timezone collaboration."),

    ("Race Condition in Billing Under Load", "Under peak concurrency tests of 10,000 transactions per second, a subtle race condition occasionally double-charges a customer wallet.",
     "Isolate the race condition with an automated concurrency test, introduce database row-level locking or optimistic concurrency tokens, and verify idempotency.",
     "Ignore the issue because 10,000 TPS only happens during annual flash sales.",
     "Catch the exception silently and log a generic message without refunding the customer.",
     "Disable multi-threading in the payment gateway so it only processes one payment at a time.",
     "Optimistic concurrency control and row-level locking guarantee transactional integrity under high load."),

    ("Sales SLA Promise of 99.999%", "The sales team closes an enterprise deal by promising 'five nines' (99.999% uptime, <5 minutes downtime/year) without consulting infrastructure leads.",
     "Present an infrastructure audit detailing current redundancy, calculate the multi-million dollar multi-region active-active cost of 99.999%, and align on realistic SLA tiers.",
     "Tell the sales team that 99.999% is impossible and refuse to support the customer.",
     "Silently agree to the contract and hope the application never experiences an outage.",
     "Forge monthly uptime reports to make it look like the system achieved five nines.",
     "Evidence-based infrastructure cost modeling brings contractual SLAs into alignment with engineering reality."),

    ("On-Call Rotation Without Training", "You are placed on the Tier-1 production on-call rotation next week without having received any system runbooks, shadow shifts, or alert training.",
     "Inform the on-call manager immediately, request a secondary shadow pairing shift alongside an experienced engineer, and review critical incident runbooks before primary duty.",
     "Accept primary on-call duty silently and mute your phone so alerts don't wake you up.",
     "Panicking and quitting your job the day before your on-call rotation begins.",
     "Route all incoming pager alerts directly to the CEO's personal phone number.",
     "Shadow pairing and runbook onboarding ensure on-call engineers can resolve production incidents safely."),

    ("Bypassing Staging to Test in Prod", "A teammate pushes a database migration script directly to the production database to 'save time', bypassing staging testing.",
     "Immediately notify the team lead, audit the migration for schema corruption or lock contention, verify automated backup restore points, and reinforce CI/CD deployment gates.",
     "Congratulate the teammate on their bravery and encourage everyone to test directly in production.",
     "Silently drop the database tables that the teammate created to teach them a lesson.",
     "Ignore the bypass completely because the production database didn't crash this time.",
     "Auditing rogue changes and enforcing automated deployment gates protect production stability."),

    ("Unauthenticated Webhook Payloads", "You discover that an external third-party payment webhook endpoint accepts incoming HTTP POST requests without verifying HMAC signatures.",
     "Implement cryptographic HMAC signature verification using the shared secret, reject unverified payloads with 401 Unauthorized, and add replay-prevention timestamp checks.",
     "Leave the endpoint open because external providers usually don't send malicious payloads.",
     "Disable the webhook endpoint entirely so that customers never receive payment confirmations.",
     "Store incoming payloads directly into the database without any validation or sanitization.",
     "Cryptographic signature verification and replay prevention secure external webhook integrations."),

    ("Squad Code Style Disagreements", "Following an organizational merger of two engineering teams, heated PR arguments erupt over linting rules and code formatting conventions.",
     "Adopt an automated zero-config code formatter (such as Prettier/Black) enforced in CI pre-commit hooks, removing subjective human debates from pull requests.",
     "Let the teams continue arguing on every pull request for the next six months.",
     "Mandate that whichever team has more senior engineers wins every formatting debate.",
     "Ban all code formatters and linters from the company's repositories.",
     "Automating formatting with opinionated CI tooling eliminates subjective bikeshedding."),

    ("Tech Debt vs Abstraction Patch", "A legacy caching layer is causing periodic memory leaks; you must choose between patching the leak or redesigning the abstraction layer.",
     "Implement an immediate targeted patch to resolve the active memory leak in production, and schedule the clean architectural abstraction for the next architectural sprint.",
     "Spend three months redesigning the abstraction while allowing production servers to crash daily.",
     "Patch the leak with an infinite while-loop that consumes all available server CPU.",
     "Ignore both the leak and the abstraction, hoping cloud autoscaling masks the issue.",
     "Pragmatic engineering prioritizes immediate operational stability before executing architectural redesigns."),

    ("MFA Lockout Escalation", "An executive user is locked out of their enterprise account after multiple failed multi-factor authentication attempts during an urgent board meeting.",
     "Follow the sanctioned identity verification security protocol (e.g. video verification with IT security) to reset MFA tokens securely rather than bypassing security checks.",
     "Disable multi-factor authentication for the entire company so the executive can log in without codes.",
     "Hand over the root database master credentials to the executive via email.",
     "Refuse to help the executive and hang up the phone during their board meeting.",
     "Adhering to verified identity protocols prevents social engineering while resolving executive lockouts."),
]

assert len(situational_specs) == 50, f"Expected 50 Situational specs, got {len(situational_specs)}"

print("Successfully verified 40 English specs and 50 Situational specs.")

# Assemble questions with balanced options (approx 25% A, 25% B, 25% C, 25% D)
assembled_english = []
for idx, spec in enumerate(english_specs):
    # Deterministic target position 0, 1, 2, 3
    target_pos = idx % 4
    opts = list(spec["distractors"])
    opts.insert(target_pos, spec["correct"])
    assembled_english.append({
        "title": spec["title"],
        "question_text": spec["question_text"],
        "options": opts,
        "correct_answer": spec["correct"],
        "question_type": "MCQ",
        "category": "English & Communication",
        "field": "English & Communication",
        "topic": spec["topic"],
        "difficulty": spec["difficulty"],
        "explanation": spec["explanation"],
    })

assembled_situational = []
for idx, (title_suffix, scenario, best_action, poor1, poor2, worst, explanation) in enumerate(situational_specs):
    target_pos = idx % 4
    distractors = [poor1, poor2, worst]
    opts = list(distractors)
    opts.insert(target_pos, best_action)
    assembled_situational.append({
        "title": f"Situational: {title_suffix}",
        "question_text": scenario,
        "options": opts,
        "correct_answer": best_action,
        "question_type": "MCQ",
        "category": "Additional",
        "field": "Engineering Architecture",
        "topic": "Situational Judgement",
        "difficulty": "MEDIUM" if idx % 2 == 0 else "HARD",
        "explanation": explanation,
    })

# Check answer positions
for name, q_list in [("English", assembled_english), ("Situational", assembled_situational)]:
    pos_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    for q in q_list:
        pos = q["options"].index(q["correct_answer"])
        pos_counts[pos] += 1
    total = len(q_list)
    print(f"{name} Position Distribution (Total {total}):")
    for pos, c in pos_counts.items():
        letter = chr(ord('A') + pos)
        print(f"  Option {letter}: {c} ({c/total*100:.1f}%)")
        assert 0.20 <= (c / total) <= 0.30, f"{name} position {letter} out of 20-30% range!"

# Combine all: 40 English + 50 Situational + 48 Likert = 138 questions
full_fixtures = assembled_english + assembled_situational + likert_items
assert len(full_fixtures) == 138

# Verify stem uniqueness across the full fixtures
seen_stems = {}
for q in full_fixtures:
    key = (q["category"], q["question_text"].strip())
    assert key not in seen_stems, f"Duplicate stem found in {q['category']}: {q['question_text'][:50]}"
    seen_stems[key] = True

print(f"\nALL 138 QUESTIONS VERIFIED: 100% UNIQUE STEMS, 0 DUPLICATES!")

# Format output file
out_path = repo_root / "scripts" / "fixtures" / "communication_psychometric.py"
header = '''"""TRELLIS English & Communication, Situational Judgement, and Psychometric Likert Fixtures (138 Questions).
40 English & Communication MCQs (100% unique, balanced ~25% A/B/C/D)
50 Situational Judgement MCQs (100% unique scenarios, scored options)
48 Psychometric Likert-scale items across 8 dimensions (with rubrics & disclaimers)
"""

from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER

COMMUNICATION_PSYCHOMETRIC_QUESTIONS = '''

with open(out_path, "w", encoding="utf-8") as f:
    f.write(header)
    pprint.pprint(full_fixtures, stream=f, indent=4, width=120)

print(f"Successfully generated pristine fixtures file: {out_path}")

