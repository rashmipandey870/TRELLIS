"""TRELLIS English & Communication, Situational Judgement, and Psychometric Likert Fixtures (138 Questions).
40 English & Communication MCQs (100% unique, balanced ~25% A/B/C/D)
50 Situational Judgement MCQs (100% unique scenarios, scored options)
48 Psychometric Likert-scale items across 8 dimensions (with rubrics & disclaimers)
"""

from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER

COMMUNICATION_PSYCHOMETRIC_QUESTIONS = [   {   'category': 'English & Communication',
        'correct_answer': 'The list of microservice dependencies, along with their database connection pools, is '
                          'updated during deployment.',
        'difficulty': 'EASY',
        'explanation': "The grammatical subject is 'The list' (singular). The intervening phrase 'along with their "
                       "database connection pools' does not alter the singular verb requirement ('is updated').",
        'field': 'English & Communication',
        'options': [   'The list of microservice dependencies, along with their database connection pools, is updated '
                       'during deployment.',
                       'The list of microservice dependencies, along with their database connection pools, are updated '
                       'during deployment.',
                       'The list of microservice dependencies, along with their database connection pools, were '
                       'updated during deployment.',
                       'The list of microservice dependencies, along with their database connection pools, have been '
                       'updated during deployment.'],
        'question_text': 'Identify the sentence that correctly adheres to subject-verb agreement rules when an '
                         'intervening prepositional phrase is present.',
        'question_type': 'MCQ',
        'title': 'Grammar: Subject-Verb Agreement with Intervening Phrases',
        'topic': 'Grammar & Construction'},
    {   'category': 'English & Communication',
        'correct_answer': 'Having optimized the SQL execution plan, the platform engineer observed a 40% reduction in '
                          'query latency.',
        'difficulty': 'MEDIUM',
        'explanation': "The introductory participial phrase 'Having optimized...' must logically modify the agent who "
                       "performed the action, which is 'the platform engineer', not the latency or server.",
        'field': 'English & Communication',
        'options': [   'Having optimized the SQL execution plan, a 40% reduction in query latency was observed by the '
                       'database.',
                       'Having optimized the SQL execution plan, the platform engineer observed a 40% reduction in '
                       'query latency.',
                       'Having optimized the SQL execution plan, query latency decreased dramatically for the platform '
                       'team.',
                       'Having optimized the SQL execution plan, the server CPU utilization dropped without human '
                       'intervention.'],
        'question_text': 'Which of the following sentences correctly avoids a dangling modifier?',
        'question_type': 'MCQ',
        'title': 'Grammar: Dangling and Misplaced Modifiers',
        'topic': 'Grammar & Construction'},
    {   'category': 'English & Communication',
        'correct_answer': 'The security gateway is designed to intercept incoming requests, validate JWT signatures, '
                          'and log audit trails.',
        'difficulty': 'EASY',
        'explanation': "Parallelism requires coordinated elements to share the same grammatical form: 'intercept... "
                       "validate... and log'.",
        'field': 'English & Communication',
        'options': [   'The security gateway is designed to intercept incoming requests, validating JWT signatures, '
                       'and to log audit trails.',
                       'The security gateway is designed for intercepting requests, validate JWT signatures, and '
                       'logging of audit trails.',
                       'The security gateway is designed to intercept incoming requests, validate JWT signatures, and '
                       'log audit trails.',
                       'The security gateway is designed to intercept incoming requests, for JWT signature validation, '
                       'and audit logging.'],
        'question_text': 'Select the sentence that maintains rigorous parallel grammatical structure in technical '
                         'documentation.',
        'question_type': 'MCQ',
        'title': 'Grammar: Parallel Structure in Technical Specifications',
        'topic': 'Grammar & Construction'},
    {   'category': 'English & Communication',
        'correct_answer': 'The enterprise compliance policy mandates that every cluster node be encrypted at rest and '
                          'in transit.',
        'difficulty': 'HARD',
        'explanation': "Verbs expressing mandate, requirement, or recommendation take the subjunctive base form ('that "
                       "every cluster node be encrypted').",
        'field': 'English & Communication',
        'options': [   'The enterprise compliance policy mandates that every cluster node is encrypted at rest and in '
                       'transit.',
                       'The enterprise compliance policy mandates that every cluster node was encrypted at rest and in '
                       'transit.',
                       'The enterprise compliance policy mandates that every cluster node will be encrypted at rest '
                       'and in transit.',
                       'The enterprise compliance policy mandates that every cluster node be encrypted at rest and in '
                       'transit.'],
        'question_text': 'Which sentence correctly uses the subjunctive mood to express a mandatory system invariant '
                         'in an SLA document?',
        'question_type': 'MCQ',
        'title': 'Grammar: Subjunctive Mood in SLA Contracts',
        'topic': 'Grammar & Construction'},
    {   'category': 'English & Communication',
        'correct_answer': 'The site reliability engineering squad has delivered its quarterly disaster recovery audit '
                          'report.',
        'difficulty': 'MEDIUM',
        'explanation': "When a collective noun ('squad') acts cohesively as a single entity, singular pronouns and "
                       "verbs are required ('has delivered its').",
        'field': 'English & Communication',
        'options': [   'The site reliability engineering squad has delivered its quarterly disaster recovery audit '
                       'report.',
                       'The site reliability engineering squad has delivered their quarterly disaster recovery audit '
                       'report.',
                       'The site reliability engineering squad have delivered its quarterly disaster recovery audit '
                       'report.',
                       'The site reliability engineering squad are delivering their quarterly disaster recovery audit '
                       'report.'],
        'question_text': 'In formal technical reporting, which sentence correctly handles pronoun agreement for a '
                         'collective team noun acting as a single unit?',
        'question_type': 'MCQ',
        'title': 'Grammar: Pronoun-Antecedent Agreement with Collective Nouns',
        'topic': 'Grammar & Construction'},
    {   'category': 'English & Communication',
        'correct_answer': 'The engineering team discovered that an unchecked thread pool had exhausted available '
                          'memory before the failover triggered.',
        'difficulty': 'MEDIUM',
        'explanation': "The past perfect tense ('had exhausted') correctly indicates an action completed prior to "
                       "another past event ('discovered' / 'triggered').",
        'field': 'English & Communication',
        'options': [   'The engineering team discovered that an unchecked thread pool has exhausted available memory '
                       'before the failover triggered.',
                       'The engineering team discovered that an unchecked thread pool had exhausted available memory '
                       'before the failover triggered.',
                       'The engineering team had discovered that an unchecked thread pool exhausts available memory '
                       'before the failover triggered.',
                       'The engineering team discovers that an unchecked thread pool had exhausted available memory '
                       'before the failover had triggered.'],
        'question_text': 'Which option displays the correct sequence of tenses when recounting past root causes and '
                         'ongoing remediation in a post-mortem?',
        'question_type': 'MCQ',
        'title': 'Grammar: Tense Sequencing in Incident Narratives',
        'topic': 'Grammar & Construction'},
    {   'category': 'English & Communication',
        'correct_answer': 'Rarely has an asynchronous distributed system maintained strict linearizability without '
                          'introducing measurable latency overhead.',
        'difficulty': 'HARD',
        'explanation': "Negative adverbial openers ('Rarely', 'Seldom', 'Scarcely') trigger subject-auxiliary "
                       "inversion: 'Rarely has [subject] maintained'.",
        'field': 'English & Communication',
        'options': [   'Rarely an asynchronous distributed system has maintained strict linearizability without '
                       'introducing measurable latency overhead.',
                       'Rarely has maintained an asynchronous distributed system strict linearizability without '
                       'introducing measurable latency overhead.',
                       'Rarely has an asynchronous distributed system maintained strict linearizability without '
                       'introducing measurable latency overhead.',
                       'Rarely an asynchronous distributed system maintained strict linearizability without '
                       'introducing measurable latency overhead.'],
        'question_text': 'Choose the correctly constructed inverted sentence used for emphasis in architectural design '
                         'proposals.',
        'question_type': 'MCQ',
        'title': 'Grammar: Inversion for Emphatic Technical Arguments',
        'topic': 'Grammar & Construction'},
    {   'category': 'English & Communication',
        'correct_answer': 'The ingress controller enforces three ingress policies: rate limiting per client IP, mutual '
                          'TLS authentication, and WAF inspection.',
        'difficulty': 'EASY',
        'explanation': 'A colon introduces a formal list following an independent clause. A colon should not directly '
                       'separate a verb from its direct object.',
        'field': 'English & Communication',
        'options': [   'The ingress controller enforces three ingress policies; rate limiting per client IP, mutual '
                       'TLS authentication, and WAF inspection.',
                       'The ingress controller enforces: rate limiting per client IP, mutual TLS authentication, and '
                       'WAF inspection.',
                       'The ingress controller enforces three ingress policies, namely: rate limiting per client IP, '
                       'mutual TLS authentication, and WAF inspection.',
                       'The ingress controller enforces three ingress policies: rate limiting per client IP, mutual '
                       'TLS authentication, and WAF inspection.'],
        'question_text': 'Which sentence demonstrates the correct punctuation rule governing colons and semicolons in '
                         'technical requirements?',
        'question_type': 'MCQ',
        'title': 'Grammar: Semicolon vs Colon Precision in Requirements',
        'topic': 'Grammar & Construction'},
    {   'category': 'English & Communication',
        'correct_answer': 'Temporary storage that exists only during the lifespan of the container instance and is '
                          'wiped upon pod termination.',
        'difficulty': 'EASY',
        'explanation': "'Ephemeral' denotes fleeting, short-lived resources that do not persist beyond the runtime "
                       'existence of their host container.',
        'field': 'English & Communication',
        'options': [   'Temporary storage that exists only during the lifespan of the container instance and is wiped '
                       'upon pod termination.',
                       'Highly durable multi-region replicated object storage backed by block-level snapshots.',
                       'Encrypted cryptographic hardware storage reserved exclusively for TLS private key '
                       'certificates.',
                       'Static, non-volatile read-only firmware memory mapped directly into virtual machine RAM.'],
        'question_text': "In container orchestration documentation, what is the precise meaning of the term 'ephemeral "
                         "storage'?",
        'question_type': 'MCQ',
        'title': "Vocab: 'Ephemeral' in Cloud Infrastructure",
        'topic': 'Vocabulary in Context'},
    {   'category': 'English & Communication',
        'correct_answer': 'Making identical multiple requests results in the exact same server-side state as making a '
                          'single request.',
        'difficulty': 'EASY',
        'explanation': 'Idempotence guarantees that repeated executions with identical parameters produce no '
                       'incremental side effects beyond the first call.',
        'field': 'English & Communication',
        'options': [   'The endpoint processes incoming requests asynchronously without blocking client threads.',
                       'Making identical multiple requests results in the exact same server-side state as making a '
                       'single request.',
                       'The API method executes in zero milliseconds by returning pre-computed cached responses.',
                       'The service can execute concurrently across multiple worker threads without locking memory.'],
        'question_text': "When an API specification mandates that an endpoint must be 'idempotent', what contractual "
                         'guarantee is provided?',
        'question_type': 'MCQ',
        'title': "Vocab: 'Idempotent' in API Design",
        'topic': 'Vocabulary in Context'},
    {   'category': 'English & Communication',
        'correct_answer': 'To implement defensive controls that diminish the severity, probability, or operational '
                          'impact of an exploitation.',
        'difficulty': 'EASY',
        'explanation': 'To mitigate is to reduce or soften the impact, exposure, or likelihood of a risk through '
                       'proactive controls.',
        'field': 'English & Communication',
        'options': [   'To completely transfer all legal liability and insurance claims to a third-party managed '
                       'provider.',
                       'To formally accept the risk without allocating engineering resources or implementing '
                       'safeguards.',
                       'To implement defensive controls that diminish the severity, probability, or operational impact '
                       'of an exploitation.',
                       'To decommission and terminate the underlying server cluster entirely to avoid security scans.'],
        'question_text': "In an enterprise cybersecurity audit report, what does it mean to 'mitigate' an identified "
                         'vulnerability?',
        'question_type': 'MCQ',
        'title': "Vocab: 'Mitigate' in Security Risk Registers",
        'topic': 'Vocabulary in Context'},
    {   'category': 'English & Communication',
        'correct_answer': 'discrete',
        'difficulty': 'MEDIUM',
        'explanation': "'Discrete' means separate, distinct, and detached. 'Discreet' means careful, prudent, and "
                       'unobtrusive.',
        'field': 'English & Communication',
        'options': ['discreet', 'discretionary', 'discretional', 'discrete'],
        'question_text': "Which word correctly completes the architectural statement: 'The microservices architecture "
                         "splits processing into separate, _______ computational units'?",
        'question_type': 'MCQ',
        'title': "Vocab: 'Discrete' vs 'Discreet' in System Modeling",
        'topic': 'Vocabulary in Context'},
    {   'category': 'English & Communication',
        'correct_answer': 'A clear, unambiguous, and definitive commitment leaving no room for doubt or multiple '
                          'interpretations.',
        'difficulty': 'MEDIUM',
        'explanation': "'Unequivocal' means admitting of no doubt or misunderstanding; clear and absolute.",
        'field': 'English & Communication',
        'options': [   'A clear, unambiguous, and definitive commitment leaving no room for doubt or multiple '
                       'interpretations.',
                       'A tentative and preliminary timeline contingent on prospective budget allocations.',
                       'A compromise agreement allowing both parties equal flexibility to alter deliverables.',
                       'A non-binding conversational estimate subject to weekly retrospective reassessments.'],
        'question_text': "When a client executive demands an 'unequivocal commitment' regarding delivery milestones, "
                         'what are they requesting?',
        'question_type': 'MCQ',
        'title': "Vocab: 'Unequivocal' in Stakeholder Commitments",
        'topic': 'Vocabulary in Context'},
    {   'category': 'English & Communication',
        'correct_answer': 'One who balances theoretical elegance against practical constraints, delivery deadlines, '
                          'and operational ROI.',
        'difficulty': 'EASY',
        'explanation': 'Pragmatism in engineering focuses on practical, sensible trade-offs suited to realistic '
                       'operational context rather than rigid dogma.',
        'field': 'English & Communication',
        'options': [   'One who strictly adheres to orthodox textbook patterns regardless of team velocity or project '
                       'context.',
                       'One who balances theoretical elegance against practical constraints, delivery deadlines, and '
                       'operational ROI.',
                       'One who rejects all formal architectural standards in favor of ad-hoc, unstructured code '
                       'hacks.',
                       'One who exclusively adopts cutting-edge alpha-stage libraries to maximize resume novelty.'],
        'question_text': "In technical leadership evaluations, how is a 'pragmatic' software architect characterized?",
        'question_type': 'MCQ',
        'title': "Vocab: 'Pragmatic' vs 'Dogmatic' Engineering",
        'topic': 'Vocabulary in Context'},
    {   'category': 'English & Communication',
        'correct_answer': "The organization's internal controls are in full agreement, harmony, and conformance with "
                          'legal requirements.',
        'difficulty': 'MEDIUM',
        'explanation': "'Congruent' means in agreement, coinciding, and harmonious in structure and application.",
        'field': 'English & Communication',
        'options': [   'The internal controls partially supersede national legal frameworks through executive decree.',
                       'The organizational policies are currently undergoing formal judicial dispute in appellate '
                       'court.',
                       "The organization's internal controls are in full agreement, harmony, and conformance with "
                       'legal requirements.',
                       'The compliance directives are temporarily suspended pending international standardization.'],
        'question_text': "In a data protection compliance review, what does stating that 'internal policies are "
                         "congruent with DPDP regulations' signify?",
        'question_type': 'MCQ',
        'title': "Vocab: 'Congruent' in Regulatory Alignment",
        'topic': 'Vocabulary in Context'},
    {   'category': 'English & Communication',
        'correct_answer': 'Network traffic metrics that deviate significantly from established baseline behavioral '
                          'distributions.',
        'difficulty': 'EASY',
        'explanation': "'Anomalous' denotes irregular, abnormal, or deviating from the standard baseline model.",
        'field': 'English & Communication',
        'options': [   'Traffic that conforms precisely to historical seasonal averages and expected user volumes.',
                       'Encrypted packets that have successfully cleared mutual TLS handshake validation protocols.',
                       'Outbound data transfers that have been explicitly whitelisted by site reliability '
                       'administrators.',
                       'Network traffic metrics that deviate significantly from established baseline behavioral '
                       'distributions.'],
        'question_text': "When observability alerts flag 'anomalous egress traffic patterns', what does this indicate "
                         'to the operations team?',
        'question_type': 'MCQ',
        'title': "Vocab: 'Anomalous' in Telemetry Analysis",
        'topic': 'Vocabulary in Context'},
    {   'category': 'English & Communication',
        'correct_answer': 'Gaining fault-tolerant linearizability requires accepting network-induced write latency '
                          'penalties across quorum nodes.',
        'difficulty': 'MEDIUM',
        'explanation': 'The text explicitly states that consensus guarantees linearizability across partitions at the '
                       'cost of write latency penalties proportional to quorum network hops.',
        'field': 'English & Communication',
        'options': [   'Gaining fault-tolerant linearizability requires accepting network-induced write latency '
                       'penalties across quorum nodes.',
                       'Achieving high write throughput requires sacrificing non-Byzantine network partition '
                       'tolerance.',
                       'Replication state machines must eliminate consensus quorums to achieve predictable '
                       'consistency.',
                       'Linearizability can only be attained if round-trip network hops between peers are reduced to '
                       'zero.'],
        'question_text': "Passage Excerpt: 'In distributed state machine replication, consensus algorithms such as "
                         'Raft and Paxos ensure fault tolerance by requiring a majority quorum before committing state '
                         'transitions. While this guarantees linearizable consistency across non-Byzantine network '
                         'partitions, it inevitably introduces a write latency penalty proportional to round-trip '
                         "network hops between quorum participants.'\n"
                         '\n'
                         'Question: Based on the passage, what is the fundamental trade-off imposed by quorum-based '
                         'consensus?',
        'question_type': 'MCQ',
        'title': 'Reading: Distributed Consensus - Core Thesis',
        'topic': 'Reading Comprehension'},
    {   'category': 'English & Communication',
        'correct_answer': 'State transitions can only be committed in a partition that retains at least 3 '
                          'communicating nodes.',
        'difficulty': 'MEDIUM',
        'explanation': 'In a 5-node cluster, a majority quorum requires strictly greater than 50%, which is floor(5/2) '
                       '+ 1 = 3 nodes.',
        'field': 'English & Communication',
        'options': [   'Any isolated pair of 2 nodes can independently commit divergent state transitions '
                       'concurrently.',
                       'State transitions can only be committed in a partition that retains at least 3 communicating '
                       'nodes.',
                       'A single surviving node is authorized to elect itself leader and commit writes locally.',
                       'The cluster completely halts all read and write processing until all 5 nodes reconnect '
                       'simultaneously.'],
        'question_text': "Based on the consensus passage excerpt ('requiring a majority quorum before committing state "
                         "transitions'), what can be logically inferred about a 5-node cluster experiencing network "
                         'partition?',
        'question_type': 'MCQ',
        'title': 'Reading: Distributed Consensus - Inferential Quorum Sizing',
        'topic': 'Reading Comprehension'},
    {   'category': 'English & Communication',
        'correct_answer': 'Nodes may fail by crashing, delaying, or dropping packets, but they do not transmit '
                          'malicious or forged messages.',
        'difficulty': 'HARD',
        'explanation': 'Non-Byzantine failure models assume fail-stop or packet-loss conditions without arbitrary, '
                       'deceptive, or adversarial behavior.',
        'field': 'English & Communication',
        'options': [   'Network switches automatically rectify dropped TCP packets without operating system '
                       'intervention.',
                       'Nodes possess zero memory limits and execute with infinite computational thread capacity.',
                       'Nodes may fail by crashing, delaying, or dropping packets, but they do not transmit malicious '
                       'or forged messages.',
                       'The cluster operates exclusively within a single physical server rack using shared memory.'],
        'question_text': "In the phrase 'across non-Byzantine network partitions', what does 'non-Byzantine' "
                         'specifically imply about the failure model?',
        'question_type': 'MCQ',
        'title': 'Reading: Distributed Consensus - Contextual Vocabulary',
        'topic': 'Reading Comprehension'},
    {   'category': 'English & Communication',
        'correct_answer': 'As an inevitable structural consequence of multi-node network round trips rather than poor '
                          'implementation.',
        'difficulty': 'MEDIUM',
        'explanation': "The passage terms write latency an 'inevitably introduces... penalty proportional to "
                       "round-trip network hops'.",
        'field': 'English & Communication',
        'options': [   'As an easily avoidable software bug that modern CPU hardware has completely eradicated.',
                       'As an artificial restriction imposed by obsolete database vendors to sell caching layers.',
                       'As an unpredictable phenomenon that cannot be modeled or measured mathematically.',
                       'As an inevitable structural consequence of multi-node network round trips rather than poor '
                       'implementation.'],
        'question_text': 'How does the author characterize the write latency associated with distributed quorum '
                         'consensus?',
        'question_type': 'MCQ',
        'title': "Reading: Distributed Consensus - Author's Stance on Latency",
        'topic': 'Reading Comprehension'},
    {   'category': 'English & Communication',
        'correct_answer': 'Explainability, verifiable provenance, and quality gates are mandatory fiduciary safeguards '
                          'in critical workflows.',
        'difficulty': 'MEDIUM',
        'explanation': "The author concludes that verifiable provenance and quality gates are 'core fiduciary "
                       "obligations' necessary to prevent bias and compliance penalties.",
        'field': 'English & Communication',
        'options': [   'Explainability, verifiable provenance, and quality gates are mandatory fiduciary safeguards in '
                       'critical workflows.',
                       'High-stakes enterprise domains should immediately abandon machine learning models in favor of '
                       'manual spreadsheets.',
                       'Explainability is purely an academic ideal that has no practical application in commercial '
                       'banking.',
                       'Enterprises should prioritize inference speed and cost minimization above regulatory '
                       'compliance checks.'],
        'question_text': "Passage Excerpt: 'As large language models become deeply embedded in high-stakes enterprise "
                         'workflows—such as automated credit underwriting and clinical diagnostic support—regulatory '
                         'mandates increasingly demand algorithmic explainability. Black-box decision paradigms that '
                         'lack post-hoc auditability expose enterprises to severe compliance penalties and systemic '
                         'bias entrenchment. Consequently, operationalizing verifiable provenance and automated '
                         "quality gates is no longer a technical luxury, but a core fiduciary obligation.'\n"
                         '\n'
                         "Question: What is the author's primary argument regarding enterprise AI deployment?",
        'question_type': 'MCQ',
        'title': 'Reading: AI Governance - Primary Regulatory Purpose',
        'topic': 'Reading Comprehension'},
    {   'category': 'English & Communication',
        'correct_answer': 'Vulnerability to regulatory compliance fines and the perpetuation of entrenched systemic '
                          'bias.',
        'difficulty': 'EASY',
        'explanation': "The text directly states: 'Black-box decision paradigms that lack post-hoc auditability expose "
                       "enterprises to severe compliance penalties and systemic bias entrenchment.'",
        'field': 'English & Communication',
        'options': [   'Immediate physical hardware degradation and permanent CPU overclocking failures.',
                       'Vulnerability to regulatory compliance fines and the perpetuation of entrenched systemic bias.',
                       'Inability of database clusters to store token vector embeddings in relational schemas.',
                       'The complete disappearance of open-source model weights from public code repositories.'],
        'question_text': 'According to the AI governance passage, what specific dangers arise from deploying black-box '
                         'decision models?',
        'question_type': 'MCQ',
        'title': 'Reading: AI Governance - Risk of Black-Box Systems',
        'topic': 'Reading Comprehension'},
    {   'category': 'English & Communication',
        'correct_answer': 'A legally and ethically binding duty of trust, care, and prudent governance owed to '
                          'stakeholders.',
        'difficulty': 'MEDIUM',
        'explanation': 'A fiduciary obligation represents an essential ethical and legal responsibility held in high '
                       'trust and accountability.',
        'field': 'English & Communication',
        'options': [   'An optional recreational activity pursued when engineering budgets have surplus funds.',
                       'A temporary public relations marketing campaign aimed at tech conference attendees.',
                       'A legally and ethically binding duty of trust, care, and prudent governance owed to '
                       'stakeholders.',
                       'A confidential corporate strategy shielded from government oversight and external audit.'],
        'question_text': "In the concluding sentence, what does the phrase 'core fiduciary obligation' denote "
                         'regarding leadership responsibility?',
        'question_type': 'MCQ',
        'title': "Reading: AI Governance - Contextual Meaning of 'Fiduciary'",
        'topic': 'Reading Comprehension'},
    {   'category': 'English & Communication',
        'correct_answer': 'Authoritative and analytical, addressing corporate executives, compliance officers, and '
                          'system architects.',
        'difficulty': 'EASY',
        'explanation': "The passage employs formal, professional vocabulary ('fiduciary obligation', 'systemic bias', "
                       "'compliance penalties') suited for corporate and governance leaders.",
        'field': 'English & Communication',
        'options': [   'Whimsical and satirical, targeting casual social media audiences and hobbyist gamers.',
                       'Aggressively confrontational, aimed at discouraging all computer science education programs.',
                       'Pedantic and strictly historical, analyzing early 1950s mechanical punch-card tabulators.',
                       'Authoritative and analytical, addressing corporate executives, compliance officers, and system '
                       'architects.'],
        'question_text': 'What is the predominant tone and target audience of the passage on enterprise AI governance?',
        'question_type': 'MCQ',
        'title': 'Reading: AI Governance - Tone and Target Audience',
        'topic': 'Reading Comprehension'},
    {   'category': 'English & Communication',
        'correct_answer': 'The site reliability team regularly conducts disaster recovery failover simulations to '
                          'verify data integrity.',
        'difficulty': 'EASY',
        'explanation': "Adverbs of frequency ('regularly') are most idiomatically and clearly placed immediately "
                       "preceding the main action verb ('regularly conducts').",
        'field': 'English & Communication',
        'options': [   'The site reliability team regularly conducts disaster recovery failover simulations to verify '
                       'data integrity.',
                       'The site reliability team conducts disaster recovery failover simulations regularly to verify '
                       'data integrity.',
                       'The site reliability team conducts regularly disaster recovery failover simulations to verify '
                       'data integrity.',
                       'Regularly the site reliability team to verify data integrity conducts disaster recovery '
                       'failover simulations.'],
        'question_text': 'Identify the sentence that positions the adverbial modifier with unambiguous precision.',
        'question_type': 'MCQ',
        'title': 'Correction: Misplaced Adverbial Modifiers in SLAs',
        'topic': 'Sentence Correction'},
    {   'category': 'English & Communication',
        'correct_answer': 'The primary database node crashed; consequently, the read replica promoted itself '
                          'automatically.',
        'difficulty': 'MEDIUM',
        'explanation': 'Two independent clauses cannot be joined solely by a comma. They require a semicolon with a '
                       "conjunctive adverb ('consequently') or a coordinating conjunction.",
        'field': 'English & Communication',
        'options': [   'The primary database node crashed, consequently, the read replica promoted itself '
                       'automatically.',
                       'The primary database node crashed; consequently, the read replica promoted itself '
                       'automatically.',
                       'The primary database node crashed, and so therefore the read replica promoted itself '
                       'automatically.',
                       'The primary database node crashed the read replica promoted itself automatically.'],
        'question_text': "Which option correctly fixes the comma splice in: 'The primary database node crashed, the "
                         "read replica promoted itself automatically'?",
        'question_type': 'MCQ',
        'title': 'Correction: Comma Splice Elimination in Design Briefs',
        'topic': 'Sentence Correction'},
    {   'category': 'English & Communication',
        'correct_answer': 'When the cache manager invalidated the stale session tokens, those tokens were purged from '
                          'the Redis cluster.',
        'difficulty': 'MEDIUM',
        'explanation': "Using the specific noun phrase ('those tokens') makes clear what was purged, resolving "
                       'ambiguity between the manager and the tokens.',
        'field': 'English & Communication',
        'options': [   'When the cache manager invalidated the stale session tokens, it was purged from the Redis '
                       'cluster.',
                       'When the cache manager invalidated the stale session tokens, they purged it from the Redis '
                       'cluster.',
                       'When the cache manager invalidated the stale session tokens, those tokens were purged from the '
                       'Redis cluster.',
                       'When the cache manager invalidated the stale session tokens, this happened to them in the '
                       'Redis cluster.'],
        'question_text': 'Select the revised sentence that eliminates ambiguous pronoun reference in release '
                         'documentation.',
        'question_type': 'MCQ',
        'title': 'Correction: Ambiguous Pronoun Reference in Changelogs',
        'topic': 'Sentence Correction'},
    {   'category': 'English & Communication',
        'correct_answer': 'Engineers are responsible for monitoring cluster health, reviewing pull requests, and '
                          'deploying hotfixes.',
        'difficulty': 'EASY',
        'explanation': "Parallelism demands matching gerund phrases: 'monitoring... reviewing... and deploying'.",
        'field': 'English & Communication',
        'options': [   'Engineers are responsible to monitor cluster health, reviewing pull requests, and deploy '
                       'hotfixes.',
                       'Engineers are responsible for cluster health monitoring, to review pull requests, and '
                       'deploying hotfixes.',
                       'Engineers are responsible for monitoring cluster health, to review pull requests, and hotfix '
                       'deployment.',
                       'Engineers are responsible for monitoring cluster health, reviewing pull requests, and '
                       'deploying hotfixes.'],
        'question_text': "Which option corrects the non-parallel phrasing in: 'Engineers are responsible for "
                         "monitoring cluster health, to review pull requests, and deployment of hotfixes'?",
        'question_type': 'MCQ',
        'title': 'Correction: Parallelism in Standard Operating Procedures',
        'topic': 'Sentence Correction'},
    {   'category': 'English & Communication',
        'correct_answer': 'All cloud architecture components must comply with ISO 27001 data governance standards.',
        'difficulty': 'EASY',
        'explanation': "The idiomatic standard English phrasal verb is 'comply with', not 'comply to' or 'comply by'.",
        'field': 'English & Communication',
        'options': [   'All cloud architecture components must comply with ISO 27001 data governance standards.',
                       'All cloud architecture components must comply to ISO 27001 data governance standards.',
                       'All cloud architecture components must comply by ISO 27001 data governance standards.',
                       'All cloud architecture components must comply for ISO 27001 data governance standards.'],
        'question_text': 'Choose the sentence that employs the correct idiomatic preposition for technical compliance.',
        'question_type': 'MCQ',
        'title': 'Correction: Preposition Idiom in Network Standards',
        'topic': 'Sentence Correction'},
    {   'category': 'English & Communication',
        'correct_answer': 'On the orders table, the engineer deployed a composite index that reduced query execution '
                          'time by 80%.',
        'difficulty': 'MEDIUM',
        'explanation': "The relative clause 'that reduced query execution time...' must be placed immediately adjacent "
                       "to its antecedent 'composite index'.",
        'field': 'English & Communication',
        'options': [   'The engineer deployed on the orders table which reduced query execution time by 80% a '
                       'composite index.',
                       'On the orders table, the engineer deployed a composite index that reduced query execution time '
                       'by 80%.',
                       'A composite index on the orders table was deployed by the engineer, which table reduced '
                       'execution time by 80%.',
                       'The engineer deployed a composite index, which orders table reduced execution time by 80%.'],
        'question_text': "Which revision resolves the misplaced relative clause in: 'The engineer deployed a composite "
                         "index on the orders table which reduced query execution time by 80%'?",
        'question_type': 'MCQ',
        'title': 'Correction: Misplaced Relative Clause in Indexing Rules',
        'topic': 'Sentence Correction'},
    {   'category': 'English & Communication',
        'correct_answer': 'Please reply by Friday with your revised timeline so we can finalize the milestone '
                          'schedule.',
        'difficulty': 'EASY',
        'explanation': "'Revert back' and 'repeat again' are redundant tautologies. 'Reply' or 'revert' stands alone "
                       'cleanly.',
        'field': 'English & Communication',
        'options': [   'Please revert back by Friday with your revised timeline so we can finalize the milestone '
                       'schedule.',
                       'Please repeat again your reply by Friday with your revised timeline so we can finalize the '
                       'milestone schedule.',
                       'Please reply by Friday with your revised timeline so we can finalize the milestone schedule.',
                       'Please revert back and repeat again by Friday with your revised timeline so we can finalize '
                       'the schedule.'],
        'question_text': 'Which sentence is free from redundant word pairs in client correspondence?',
        'question_type': 'MCQ',
        'title': 'Correction: Elimination of Redundant Business Phrasing',
        'topic': 'Sentence Correction'},
    {   'category': 'English & Communication',
        'correct_answer': 'The latency of the Go microservice is significantly lower than that of the legacy monolith.',
        'difficulty': 'HARD',
        'explanation': "You must compare latency to latency ('that of the legacy monolith'), not latency to a physical "
                       'monolith.',
        'field': 'English & Communication',
        'options': [   'The latency of the Go microservice is significantly lower than the legacy monolith.',
                       'The latency of the Go microservice is significantly lower compared to the legacy monolith.',
                       "The Go microservice has lower latency than the legacy monolith's performance metrics "
                       'comparison.',
                       'The latency of the Go microservice is significantly lower than that of the legacy monolith.'],
        'question_text': 'Select the sentence that properly avoids an illogical comparison when reporting system '
                         'performance benchmarks.',
        'question_type': 'MCQ',
        'title': 'Correction: Faulty Comparison in Benchmark Analysis',
        'topic': 'Sentence Correction'},
    {   'category': 'English & Communication',
        'correct_answer': 'Impact Summary (customer impact, financial exposure), Current Status (what is being done), '
                          'Next Update ETA, and Incident Commander contact.',
        'difficulty': 'EASY',
        'explanation': 'Executive incident communication requires crisp, high-level impact clarity, containment '
                       'status, next checkpoint time, and clear ownership.',
        'field': 'English & Communication',
        'options': [   'Impact Summary (customer impact, financial exposure), Current Status (what is being done), '
                       'Next Update ETA, and Incident Commander contact.',
                       'A detailed 500-line stack trace dump with an exhaustive defense of why the on-call engineer '
                       'was not at fault.',
                       "A brief message stating 'Systems are down, please do not message us while we attempt to fix "
                       "it.'",
                       'A forwarded customer complaint email with multiple emotional punctuation marks demanding '
                       'immediate help.'],
        'question_text': 'When sending an emergency P1 outage broadcast to executive leadership, which initial '
                         'communication structure is most effective?',
        'question_type': 'MCQ',
        'title': 'Comm: Escalating a P1 Production Outage to Executives',
        'topic': 'Professional Writing'},
    {   'category': 'English & Communication',
        'correct_answer': 'Present the rationale proactively, detail trade-offs (releasing now risks data corruption), '
                          'and offer options: scope reduction vs deferred date.',
        'difficulty': 'MEDIUM',
        'explanation': 'Proactive notification with empirical trade-off analysis and actionable scope/schedule options '
                       'demonstrates professional maturity.',
        'field': 'English & Communication',
        'options': [   'Conceal the delay until the final day of the sprint demo and blame unexpected vendor latency.',
                       'Present the rationale proactively, detail trade-offs (releasing now risks data corruption), '
                       'and offer options: scope reduction vs deferred date.',
                       'Deploy the incomplete code silently to production and disable the broken parts behind '
                       'undocumented flags.',
                       'Send an angry message to the squad channel stating that product expectations are detached from '
                       'reality.'],
        'question_text': 'A critical technical refactor will delay a promised feature by 4 days. How should this be '
                         'communicated to the product manager?',
        'question_type': 'MCQ',
        'title': 'Comm: Negotiating a Sprint Milestone Slip with Product',
        'topic': 'Professional Writing'},
    {   'category': 'English & Communication',
        'correct_answer': 'Highlight the vulnerability with the OWASP reference, explain the attack vector clearly, '
                          'and provide parameterized query example code.',
        'difficulty': 'EASY',
        'explanation': "Constructive code review links to objective standards, explains the 'why' without personal "
                       'criticism, and guides with concrete remedies.',
        'field': 'English & Communication',
        'options': [   "Reject the PR with a comment stating 'This code is terrible and demonstrates a total lack of "
                       "basic security knowledge.'",
                       "Approve the pull request anyway to avoid hurting the junior engineer's self-esteem and patch "
                       'it later yourself.',
                       'Highlight the vulnerability with the OWASP reference, explain the attack vector clearly, and '
                       'provide parameterized query example code.',
                       "Take a screenshot of the vulnerable line and post it in the team's public Slack channel as a "
                       'warning to others.'],
        'question_text': 'A pull request from a junior engineer introduces a severe SQL injection vulnerability. What '
                         'is the most constructive review comment?',
        'question_type': 'MCQ',
        'title': 'Comm: Constructive Code Review Rejection on Security Flaw',
        'topic': 'Professional Writing'},
    {   'category': 'English & Communication',
        'correct_answer': "Acknowledge the requirement and propose specific quantitative SLAs: 'To align on "
                          'infrastructure sizing, could we target p95 latency under 200ms at 5,000 peak concurrent '
                          "users?'",
        'difficulty': 'MEDIUM',
        'explanation': 'Translating ambiguous qualitative client desires into clear, professional quantitative metrics '
                       'drives alignment without hostility.',
        'field': 'English & Communication',
        'options': [   "Reply stating 'Your requirement is meaningless because ultra-fast is not a real engineering "
                       "metric.'",
                       'Accept the requirement without clarification and build the simplest possible single-server '
                       'architecture.',
                       'Forward the email to legal requesting a contract termination due to client incompetence.',
                       "Acknowledge the requirement and propose specific quantitative SLAs: 'To align on "
                       'infrastructure sizing, could we target p95 latency under 200ms at 5,000 peak concurrent '
                       "users?'"],
        'question_text': "A client sends a vague specification: 'The portal must be ultra-fast and handle huge "
                         "traffic.' What is the appropriate written response?",
        'question_type': 'MCQ',
        'title': 'Comm: Clarifying Ambiguous Client Requirements',
        'topic': 'Professional Writing'},
    {   'category': 'English & Communication',
        'correct_answer': "'I find that context-switching to answer unscheduled check-ins interrupts deep work. Could "
                          "we establish an end-of-day async Slack update instead?'",
        'difficulty': 'MEDIUM',
        'explanation': 'Framing feedback around personal workflow impact and offering a structured alternative '
                       'demonstrates collaborative problem solving.',
        'field': 'English & Communication',
        'options': [   "'I find that context-switching to answer unscheduled check-ins interrupts deep work. Could we "
                       "establish an end-of-day async Slack update instead?'",
                       "'You are micro-managing me constantly and it proves you have zero trust in my engineering "
                       "abilities.'",
                       'Remain completely silent during 1:1s while complaining about the manager to peer engineers at '
                       'lunch.',
                       "'If you message me again outside of morning standup, I will submit an HR grievance for "
                       "harassment.'"],
        'question_text': 'An engineer feels micro-managed by daily unplanned status inquiries from their manager. What '
                         'is the most effective phrasing for 1:1 feedback?',
        'question_type': 'MCQ',
        'title': 'Comm: Upward Feedback to Engineering Manager in 1:1',
        'topic': 'Professional Writing'},
    {   'category': 'English & Communication',
        'correct_answer': 'Sunsetting schedule with concrete milestones, migration guide with v2 code mappings, and '
                          'dual-run availability window.',
        'difficulty': 'EASY',
        'explanation': 'API deprecation notices require transparent timelines, migration guides, sunsetting '
                       'milestones, and support channels.',
        'field': 'English & Communication',
        'options': [   'A sudden immediate shutdown announcement with zero grace period to force instant customer '
                       'migration.',
                       'Sunsetting schedule with concrete milestones, migration guide with v2 code mappings, and '
                       'dual-run availability window.',
                       'A vague suggestion that v1 might stop working eventually without specifying version numbers or '
                       'dates.',
                       'A notice instructing partners to reverse-engineer the new v2 endpoints from client mobile app '
                       'network logs.'],
        'question_text': 'When publishing a deprecation notice for an enterprise v1 API, which component must be '
                         'explicitly included?',
        'question_type': 'MCQ',
        'title': 'Comm: Announcing Breaking API Deprecation to Partners',
        'topic': 'Professional Writing'},
    {   'category': 'English & Communication',
        'correct_answer': 'Meet to review test objectives, establish time-boxed test execution slots, and agree on '
                          'shared cluster telemetry benchmarks.',
        'difficulty': 'EASY',
        'explanation': 'Professional engineering collaboration involves collaborative time-slot scheduling and shared '
                       'objective alignment.',
        'field': 'English & Communication',
        'options': [   'The squad lead who logs in first locks the cluster credentials and refuses access to the other '
                       'squad.',
                       'Both squads trigger maximum stress runs concurrently, resulting in cluster thrashing and '
                       'corrupted test runs.',
                       'Meet to review test objectives, establish time-boxed test execution slots, and agree on shared '
                       'cluster telemetry benchmarks.',
                       'Escalate immediately to the Vice President of Engineering without attempting any peer '
                       'coordination.'],
        'question_text': 'Two squads require access to the single staging load-testing cluster during the same 3-day '
                         'sprint window. How should the leads resolve this?',
        'question_type': 'MCQ',
        'title': 'Comm: Resolving Cross-Squad Resource Contention',
        'topic': 'Professional Writing'},
    {   'category': 'English & Communication',
        'correct_answer': 'Provide root-cause explanation (unpruned replicas), total financial impact, exact '
                          'remediation taken (automated autoscaler limits), and safeguards against recurrence.',
        'difficulty': 'MEDIUM',
        'explanation': 'Financial transparency requires root-cause diagnosis, quantitative dollar impact, immediate '
                       'corrective action, and permanent preventive guardrails.',
        'field': 'English & Communication',
        'options': [   'Submit the raw 10,000-line AWS Cost Explorer CSV file with no narrative explanation or '
                       'executive summary.',
                       'Deny that any anomaly occurred and attribute the discrepancy to unexpected federal currency '
                       'fluctuations.',
                       'Delete the cloud logging history so auditors cannot pinpoint which developer launched the '
                       'cluster.',
                       'Provide root-cause explanation (unpruned replicas), total financial impact, exact remediation '
                       'taken (automated autoscaler limits), and safeguards against recurrence.'],
        'question_text': 'A sudden 35% spike in AWS GPU billing occurs due to an unpruned inference pod replica set. '
                         'How should engineering report this to finance?',
        'question_type': 'MCQ',
        'title': 'Comm: Summarizing Cloud Cost Anomaly for Financial Audit',
        'topic': 'Professional Writing'},
    {   'category': 'Additional',
        'correct_answer': 'Run the flaky test in isolation with verbose logging to confirm it is unrelated to the '
                          'security patch, document the test flake in a tracking ticket, and seek tech lead approval '
                          'for a scoped override.',
        'difficulty': 'MEDIUM',
        'explanation': 'Balancing urgent security remediation with deployment safety requires isolating and verifying '
                       'the non-relevance of the flake while documenting it transparently.',
        'field': 'Engineering Architecture',
        'options': [   'Run the flaky test in isolation with verbose logging to confirm it is unrelated to the '
                       'security patch, document the test flake in a tracking ticket, and seek tech lead approval for '
                       'a scoped override.',
                       'Disable the entire integration test suite permanently so that future hotfixes merge instantly '
                       'without checks.',
                       'Rerun the entire CI pipeline 15 times repeatedly until a random pass occurs, without '
                       'inspecting failure logs.',
                       'Deploy the code directly to production via SSH, bypassing git version control and CI '
                       'entirely.'],
        'question_text': 'A flaky end-to-end integration test is failing intermittently on an urgent production '
                         'security hotfix PR that has been peer-reviewed.',
        'question_type': 'MCQ',
        'title': 'Situational: Flaky CI Test on Hotfix',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Congratulate the peer on the demo publicly, and during your next 1:1, have a private, '
                          'constructive conversation clarifying future demo collaboration and attribution.',
        'difficulty': 'HARD',
        'explanation': 'Professional composure requires separating public team success from private interpersonal '
                       'conflict resolution.',
        'field': 'Engineering Architecture',
        'options': [   'Interrupt the live presentation in front of executive leadership to angrily accuse your peer '
                       'of intellectual dishonesty.',
                       'Congratulate the peer on the demo publicly, and during your next 1:1, have a private, '
                       'constructive conversation clarifying future demo collaboration and attribution.',
                       "Say nothing, but secretly introduce a subtle defect into your peer's upcoming branch as "
                       'retaliation.',
                       'Broadcast an all-company email denouncing the peer and demanding an immediate public apology.'],
        'question_text': 'During a high-visibility company demo, a peer presents an architecture feature you primarily '
                         'designed and implemented, taking sole personal credit.',
        'question_type': 'MCQ',
        'title': 'Situational: Credit Claiming in Demos',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Explain the regulatory, reputational, and financial risks of shipping unverified code, and '
                          'propose a launch with limited beta access under strict monitoring while testing finishes.',
        'difficulty': 'MEDIUM',
        'explanation': 'Adhering to security governance requires firm, evidence-based boundary setting coupled with '
                       'constructive risk-mitigation options.',
        'field': 'Engineering Architecture',
        'options': [   "Silently comply with the request without documenting the PM's directive or alerting security "
                       'officers.',
                       'Publicly mock the product manager on social media for not caring about user privacy.',
                       'Explain the regulatory, reputational, and financial risks of shipping unverified code, and '
                       'propose a launch with limited beta access under strict monitoring while testing finishes.',
                       'Delete all security scanner config files so the automated build status appears green.'],
        'question_text': 'A product manager asks the team to bypass mandatory penetration testing and vulnerability '
                         'scans to meet a marketing launch deadline.',
        'question_type': 'MCQ',
        'title': 'Situational: Skipping Security Testing for Launch',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Immediately revoke and rotate the compromised credential in the secret manager, notify the '
                          'security team, and purge the secret from git history using git-filter-repo.',
        'difficulty': 'HARD',
        'explanation': 'Immediate credential rotation and history purging are mandatory first responses to public '
                       'secret leakage.',
        'field': 'Engineering Architecture',
        'options': [   'Leave a sarcastic comment on the pull request pointing out the mistake and wait for the '
                       'developer to wake up tomorrow.',
                       'Copy the token to your personal laptop and test whether you can extract confidential user '
                       'tables.',
                       'Simply push a new commit that deletes the line from the file, leaving the secret visible in '
                       'git commit history.',
                       'Immediately revoke and rotate the compromised credential in the secret manager, notify the '
                       'security team, and purge the secret from git history using git-filter-repo.'],
        'question_text': 'You notice that a colleague accidentally committed an active production database API token '
                         'into a publicly accessible GitHub branch.',
        'question_type': 'MCQ',
        'title': 'Situational: Exposed Token in Public PR',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Schedule an informal, supportive 1:1 coffee chat, offer to pair program for an hour, and '
                          'break down the task into smaller, manageable sub-problems.',
        'difficulty': 'MEDIUM',
        'explanation': 'Empathetic mentorship and collaborative pair programming unlock developer productivity without '
                       'intimidation.',
        'field': 'Engineering Architecture',
        'options': [   'Schedule an informal, supportive 1:1 coffee chat, offer to pair program for an hour, and break '
                       'down the task into smaller, manageable sub-problems.',
                       'Publicly reprimand the junior developer in front of the entire team for falling behind sprint '
                       'velocity.',
                       'Reassign the task to yourself without telling the junior developer and complete it late at '
                       'night.',
                       "Advise the engineering manager to terminate the junior engineer's employment immediately."],
        'question_text': 'A junior teammate has made zero git commits in 4 days on a sprint task and appears hesitant '
                         'to speak during daily standup.',
        'question_type': 'MCQ',
        'title': 'Situational: Struggling Junior Engineer',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Facilitate a structured Architecture Decision Record (ADR) session with weighted scoring '
                          'criteria, time-box the discussion, and escalate to the Principal Architect for a final '
                          'tie-breaking decision.',
        'difficulty': 'HARD',
        'explanation': 'Time-boxed ADR sessions with explicit decision criteria prevent analysis paralysis while '
                       'maintaining team buy-in.',
        'field': 'Engineering Architecture',
        'options': [   'Let the debate continue indefinitely until one engineer transfers to another company or gives '
                       'up out of exhaustion.',
                       'Facilitate a structured Architecture Decision Record (ADR) session with weighted scoring '
                       'criteria, time-box the discussion, and escalate to the Principal Architect for a final '
                       'tie-breaking decision.',
                       'Flip a coin in secret and announce that management has mandated your favorite architecture.',
                       'Split the project into two competing parallel prototypes and have the engineers race against '
                       'each other for a month.'],
        'question_text': 'Two senior engineers have been debating microservices vs modular monolith for 3 weeks, '
                         'stalling the start of a critical multi-month initiative.',
        'question_type': 'MCQ',
        'title': 'Situational: Intractable Architecture Debate',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': "Politely acknowledge the feature's value and route the request through the Project Manager "
                          'and formal change request process for schedule and cost estimation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Contractual boundaries protect project health; scope adjustments must be formally estimated '
                       'and scheduled.',
        'field': 'Engineering Architecture',
        'options': [   'Immediately agree to build the feature for free, working through the night without notifying '
                       'your team.',
                       "Ignore the client's message completely and block their account on Slack.",
                       "Politely acknowledge the feature's value and route the request through the Project Manager and "
                       'formal change request process for schedule and cost estimation.',
                       'Agree to build the feature only if the client promises to give you a positive personal '
                       'performance review.'],
        'question_text': 'A client representative asks you via a direct Slack message to add a complex export feature '
                         'before Friday that is outside the agreed scope.',
        'question_type': 'MCQ',
        'title': 'Situational: Scope Creep Without Change Request',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Identify the rogue query via pg_stat_activity, terminate the specific blocking query '
                          'session, and apply a temporary query timeout while alerting the on-call engineer.',
        'difficulty': 'HARD',
        'explanation': 'Surgical query termination restores operational stability with minimal collateral customer '
                       'impact.',
        'field': 'Engineering Architecture',
        'options': [   'Restart the entire production database cluster immediately, terminating all ongoing user '
                       'connections.',
                       'Ignore the spike and assume the cloud provider will automatically scale CPU before the demo '
                       'crashes.',
                       'Blame the sales team for scheduling customer demos during regular operational hours.',
                       'Identify the rogue query via pg_stat_activity, terminate the specific blocking query session, '
                       'and apply a temporary query timeout while alerting the on-call engineer.'],
        'question_text': 'A production database CPU spikes to 99% due to an unindexed analytics query just as the '
                         'sales team begins a major enterprise prospect demo.',
        'question_type': 'MCQ',
        'title': 'Situational: Production DB Spike During Sales Demo',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Document the discrepancy, create a backward-compatible transition plan that accepts both '
                          'formats temporarily, and update the OpenAPI contract and client SDKs.',
        'difficulty': 'MEDIUM',
        'explanation': 'Backward compatibility and gradual contract convergence prevent breaking external downstream '
                       'integrations.',
        'field': 'Engineering Architecture',
        'options': [   'Document the discrepancy, create a backward-compatible transition plan that accepts both '
                       'formats temporarily, and update the OpenAPI contract and client SDKs.',
                       'Immediately rename all production JSON fields without notifying external consumers or client '
                       'teams.',
                       'Delete the OpenAPI documentation entirely so that no one can prove a discrepancy exists.',
                       'Inform customers that the documentation is correct and their client integration code is '
                       'wrong.'],
        'question_text': 'You discover that the live production API returns camelCase fields while the published '
                         'OpenAPI specification documents snake_case.',
        'question_type': 'MCQ',
        'title': 'Situational: Schema Payload Discrepancy',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Bring both leaders together in a brief alignment chat, articulate the conflicting '
                          'priorities and time constraints, and ask them to agree on the primary sprint focus.',
        'difficulty': 'HARD',
        'explanation': 'Transparent stakeholder alignment resolves priority conflicts without putting the engineer in '
                       'an impossible position.',
        'field': 'Engineering Architecture',
        'options': [   'Secretly work on both tasks simultaneously, delivering both in poor, untested quality.',
                       'Bring both leaders together in a brief alignment chat, articulate the conflicting priorities '
                       'and time constraints, and ask them to agree on the primary sprint focus.',
                       "Follow the tech lead's advice and completely ignore the engineering manager's request.",
                       'Complain to human resources that leadership lacks organizational competence.'],
        'question_text': 'Your tech lead instructs you to refactor legacy database models, but your engineering '
                         'manager asks you to deliver a marketing banner by end of day.',
        'question_type': 'MCQ',
        'title': 'Situational: Conflicting Lead Priorities',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': "Reach out privately with empathetic inquiry: 'Hey, noticed you missed standup, is "
                          "everything okay and is there anything I can help unblock on your tasks?'",
        'difficulty': 'MEDIUM',
        'explanation': 'Empathetic, non-judgmental private outreach identifies personal or technical blockers '
                       'constructively.',
        'field': 'Engineering Architecture',
        'options': [   'Announce in the team channel that this person is slacking off and should have their salary '
                       'docked.',
                       'Silently remove them from all shared calendar invites and project documentation.',
                       "Reach out privately with empathetic inquiry: 'Hey, noticed you missed standup, is everything "
                       "okay and is there anything I can help unblock on your tasks?'",
                       'Do their work for them and complain about their absence to other teammates behind their back.'],
        'question_text': 'A teammate has missed three consecutive daily standups and takes several hours to respond to '
                         'direct mentions on urgent blocker tickets.',
        'question_type': 'MCQ',
        'title': 'Situational: Standup Disengagement',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Review distributed tracing spans, structured error logs, and telemetry around the '
                          "customer's tenant ID, and add targeted diagnostic logging in the next deployment.",
        'difficulty': 'HARD',
        'explanation': 'Instrumented observability and targeted telemetry isolate elusive intermittent production '
                       'defects.',
        'field': 'Engineering Architecture',
        'options': [   "Close the customer ticket with 'Cannot Reproduce' and advise the customer to stop complaining.",
                       'Guess the problem blindly and push unverified database schema alterations directly to '
                       'production.',
                       "Blame the customer's internal corporate firewall without checking system logs.",
                       "Review distributed tracing spans, structured error logs, and telemetry around the customer's "
                       'tenant ID, and add targeted diagnostic logging in the next deployment.'],
        'question_text': 'A tier-1 customer reports an intermittent transaction drop that cannot be reproduced in '
                         'local development or staging environments.',
        'question_type': 'MCQ',
        'title': 'Situational: Unreproducible Production Bug',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Clarify that a 2-hour estimate can only be a high-variance T-shirt size (e.g. Large/XL), '
                          'and request a 3-day discovery spike to produce an accurate estimation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Managing expectations with estimation cones of uncertainty avoids premature binding '
                       'commitments.',
        'field': 'Engineering Architecture',
        'options': [   'Clarify that a 2-hour estimate can only be a high-variance T-shirt size (e.g. Large/XL), and '
                       'request a 3-day discovery spike to produce an accurate estimation.',
                       "Invent an overly optimistic date (e.g. '2 weeks') to make management happy, knowing it will "
                       'fail.',
                       'Refuse to speak with management and walk out of the planning meeting.',
                       'Commit your entire squad to working 80 hours a week for the next six months.'],
        'question_text': 'Management asks you to provide a firm delivery commitment for a complex microservices '
                         'migration within 2 hours.',
        'question_type': 'MCQ',
        'title': 'Situational: 2-Hour Project Estimation Pressure',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Analyze exploitability in your architecture, upgrade to the patched version in a staging '
                          'branch, run integration regression tests, and expedite emergency deployment.',
        'difficulty': 'HARD',
        'explanation': 'Immediate exploitability triage, rapid staging validation, and expedited emergency patching '
                       'mitigate zero-day risks.',
        'field': 'Engineering Architecture',
        'options': [   'Wait for the next scheduled quarterly release in three months before considering an upgrade.',
                       'Analyze exploitability in your architecture, upgrade to the patched version in a staging '
                       'branch, run integration regression tests, and expedite emergency deployment.',
                       'Ignore the vulnerability because the library has worked fine for two years without issue.',
                       'Remove the payment gateway entirely from the application to avoid updating the dependency.'],
        'question_text': 'An open-source serialization package used across your payment gateway releases an urgent '
                         'security advisory for a critical remote code execution vulnerability.',
        'question_type': 'MCQ',
        'title': 'Situational: Zero-Day CVE in Core Library',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Respectfully point to the specific section of the published engineering standard in your '
                          'review reply, and ask for their guidance on whether the team should update the standard.',
        'difficulty': 'MEDIUM',
        'explanation': 'Grounding discussions in documented standards invites objective dialogue without personal '
                       'confrontation.',
        'field': 'Engineering Architecture',
        'options': [   'Blindly accept the feedback and knowingly violate company standards across your entire '
                       'codebase.',
                       'Harshly insult the mentor in public for not knowing the company guidelines.',
                       'Respectfully point to the specific section of the published engineering standard in your '
                       'review reply, and ask for their guidance on whether the team should update the standard.',
                       'Escalate immediately to the CEO demanding the mentor be demoted.'],
        'question_text': 'A respected senior mentor submits code review feedback insisting that you use anti-patterns '
                         "that explicitly violate the company's published engineering standards.",
        'question_type': 'MCQ',
        'title': 'Situational: Mentor Violates Style Guide',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Evaluate whether a verified weekend rollback plan and on-call coverage exist; if not, '
                          'arrange an early Monday morning deployment with full team support.',
        'difficulty': 'HARD',
        'explanation': 'Preventing unmonitored Friday deployments protects production reliability while scheduling '
                       'prompt follow-ups.',
        'field': 'Engineering Architecture',
        'options': [   'Deploy the unverified change immediately at 5:00 PM and shut down your laptop for the weekend.',
                       'Agree to do it, but secretly forget about it until Monday afternoon.',
                       'Berate the account manager in an all-hands channel for asking for weekend deployments.',
                       'Evaluate whether a verified weekend rollback plan and on-call coverage exist; if not, arrange '
                       'an early Monday morning deployment with full team support.'],
        'question_text': 'At 4:45 PM on a Friday, an account manager requests an urgent configuration change to enable '
                         'a pilot for a high-value prospect over the weekend.',
        'question_type': 'MCQ',
        'title': 'Situational: Friday Afternoon Urgent Feature',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Document the race condition scenario with a reproducible sequence diagram, and present the '
                          'evidence to the Lead Architect requesting an addendum review.',
        'difficulty': 'MEDIUM',
        'explanation': 'Evidence-backed architectural feedback with clear failure scenarios welcomes constructive '
                       'course corrections.',
        'field': 'Engineering Architecture',
        'options': [   'Document the race condition scenario with a reproducible sequence diagram, and present the '
                       'evidence to the Lead Architect requesting an addendum review.',
                       'Sabotage the project during implementation so that the architecture fails in front of '
                       'everyone.',
                       "Keep silent because the board has already stamped the design and you don't want to cause "
                       'trouble.',
                       'Publicly declare that the Architecture Review Board is incompetent on social media.'],
        'question_text': 'After the Architecture Review Board has officially approved an event-driven design, you '
                         'discover a race condition flaw in the data model.',
        'question_type': 'MCQ',
        'title': 'Situational: Post-Approval Architecture Disagreement',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': "Immediately log an urgent architectural tech debt item, spike the vendor's v2 API and one "
                          'alternative provider, and schedule migration into the next sprint.',
        'difficulty': 'HARD',
        'explanation': 'Proactive vendor transition spikes and sprint scheduling prevent sudden service blackouts.',
        'field': 'Engineering Architecture',
        'options': [   'Wait until day 29 before investigating the migration steps.',
                       "Immediately log an urgent architectural tech debt item, spike the vendor's v2 API and one "
                       'alternative provider, and schedule migration into the next sprint.',
                       "Assume the vendor won't actually shut down the API on the announced deadline.",
                       'Disable user phone verification entirely and allow unverified accounts to register.'],
        'question_text': 'A third-party SMS verification vendor announces it is discontinuing its legacy API in 30 '
                         'days, which your onboarding flow relies upon.',
        'question_type': 'MCQ',
        'title': 'Situational: Vendor 30-Day Deprecation Notice',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Establish structured daily 30-minute check-ins, prepare well-scoped starter issues with '
                          'clear acceptance criteria, and pair them with co-mentors across the team.',
        'difficulty': 'MEDIUM',
        'explanation': 'Structured scoping and distributed team mentorship allow meaningful intern growth without '
                       'overburdening a single lead.',
        'field': 'Engineering Architecture',
        'options': [   'Tell the interns to sit quietly in the corner and not bother you until the migration ends next '
                       'month.',
                       'Give the interns production database administrative credentials and tell them to figure it '
                       'out.',
                       'Establish structured daily 30-minute check-ins, prepare well-scoped starter issues with clear '
                       'acceptance criteria, and pair them with co-mentors across the team.',
                       'Complain to the interns that they are ruining your sprint velocity.'],
        'question_text': 'You are assigned to mentor two summer interns during the highest-intensity sprint of a '
                         'company-wide cloud migration.',
        'question_type': 'MCQ',
        'title': 'Situational: Intern Onboarding During Crunch',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Raise the velocity drop and cognitive fatigue openly during the retrospective, and advocate '
                          'with management to restore sustainable cadence before technical debt multiplies.',
        'difficulty': 'HARD',
        'explanation': 'Advocating for sustainable engineering cadence preserves long-term code quality and human '
                       'retention.',
        'field': 'Engineering Architecture',
        'options': [   'Continue working 14-hour days while consuming excessive energy drinks until someone makes a '
                       'catastrophic error.',
                       'Abruptly stop showing up to work without notifying anyone on the team.',
                       'Secretly disable production alerts so the team can sleep through the night regardless of '
                       'outages.',
                       'Raise the velocity drop and cognitive fatigue openly during the retrospective, and advocate '
                       'with management to restore sustainable cadence before technical debt multiplies.'],
        'question_text': 'After three consecutive weeks of overtime to meet an artificial deadline, you and your squad '
                         'members show clear signs of exhaustion and rising error rates.',
        'question_type': 'MCQ',
        'title': 'Situational: Sprint Fatigue & Crunch Burnout',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Write characterization tests that capture existing baseline behavior before altering any '
                          'business logic, then refactor incrementally in small, testable commits.',
        'difficulty': 'MEDIUM',
        'explanation': 'Characterization testing creates an empirical safety net before refactoring legacy code.',
        'field': 'Engineering Architecture',
        'options': [   'Write characterization tests that capture existing baseline behavior before altering any '
                       'business logic, then refactor incrementally in small, testable commits.',
                       'Rewrite the entire 5,000 lines from memory over a weekend without writing any tests.',
                       'Refuse to work on the module and demand that the original author who left 3 years ago be '
                       'rehired.',
                       'Delete the module and replace it with a third-party billing framework in a single unreviewed '
                       'commit.'],
        'question_text': 'You are tasked with refactoring a critical 5,000-line billing module that currently has zero '
                         'automated unit or integration tests.',
        'question_type': 'MCQ',
        'title': 'Situational: Zero-Test Legacy Refactor',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Deny direct production access, explain security and performance risks (unindexed queries '
                          'locking tables), and provide read-only access to a sanitized analytics replica.',
        'difficulty': 'HARD',
        'explanation': 'Read replicas and sanitized data warehouses protect transactional production performance and '
                       'privacy.',
        'field': 'Engineering Architecture',
        'options': [   'Grant full superuser administrative credentials to the production database immediately.',
                       'Deny direct production access, explain security and performance risks (unindexed queries '
                       'locking tables), and provide read-only access to a sanitized analytics replica.',
                       "Ignore the analyst's request for several weeks without explaining why.",
                       'Export the entire unredacted customer database to a public Google Sheets file and send the '
                       'link.'],
        'question_text': 'A business analyst requests direct write and read credentials to the primary production '
                         'database to build a dashboard in Tableau.',
        'question_type': 'MCQ',
        'title': 'Situational: Direct DB Access for BI User',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Acknowledge the validity of their frustration, propose formal team PR review SLAs (e.g. '
                          'initial review within 4 business hours), and review pull request distribution metrics.',
        'difficulty': 'MEDIUM',
        'explanation': 'Channeling retrospective friction into concrete operational SLAs resolves systemic unfairness.',
        'field': 'Engineering Architecture',
        'options': [   'Tell the teammate to stop whining and that their code is simply too difficult to read.',
                       'Argue that PR reviews are optional and engineers should just merge without review.',
                       'Acknowledge the validity of their frustration, propose formal team PR review SLAs (e.g. '
                       'initial review within 4 business hours), and review pull request distribution metrics.',
                       'Vote to cancel all future retrospectives because they cause emotional discomfort.'],
        'question_text': 'A teammate vents intense frustration during a retrospective, claiming that their pull '
                         'requests sit unreviewed for days while others are approved instantly.',
        'question_type': 'MCQ',
        'title': 'Situational: Retrospective Frustration',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Create a realistic mock server matching the agreed contract specification so your frontend '
                          'and business logic can continue development and testing uninterrupted.',
        'difficulty': 'HARD',
        'explanation': 'Contract mocking decouples team dependencies and maintains engineering velocity during '
                       'upstream delays.',
        'field': 'Engineering Architecture',
        'options': [   'Halt all sprint progress and sit idle for four weeks waiting for the upstream team.',
                       'Build your own duplicate version of the upstream service from scratch in secret.',
                       "Send aggressive messages to the upstream team's leadership demanding they work over the "
                       'weekend.',
                       'Create a realistic mock server matching the agreed contract specification so your frontend and '
                       'business logic can continue development and testing uninterrupted.'],
        'question_text': 'An upstream services team informs you two days before sprint close that their API contract '
                         'delivery is delayed by four weeks.',
        'question_type': 'MCQ',
        'title': 'Situational: Dependency API Delay',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Trigger incident response, roll back or toggle the feature flag, quantify financial '
                          'discrepancy, patch the bug with automated test coverage, and publish a post-mortem.',
        'difficulty': 'MEDIUM',
        'explanation': 'Transparent incident response, rapid rollback, and financial reconciliation protect integrity.',
        'field': 'Engineering Architecture',
        'options': [   'Trigger incident response, roll back or toggle the feature flag, quantify financial '
                       'discrepancy, patch the bug with automated test coverage, and publish a post-mortem.',
                       'Delete the error log entries so management never discovers that 0.5% of users were affected.',
                       "Quietly fix the bug in next month's release without informing finance or customer support.",
                       'Blame the junior engineer who merged the PR on social media.'],
        'question_text': 'An algorithmic edge case bug causes incorrect pricing calculations for 0.5% of checkouts '
                         'before being flagged by monitoring.',
        'question_type': 'MCQ',
        'title': 'Situational: Bug Escaped to 0.5% Users',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Politely decline citing data protection regulations (DPDP/GDPR), explain the risk of data '
                          'leakage, and guide them through the sanctioned CRM data-sharing workflow.',
        'difficulty': 'HARD',
        'explanation': 'Enforcing DPDP compliance and guiding users to sanctioned tools prevents severe privacy '
                       'breaches.',
        'field': 'Engineering Architecture',
        'options': [   'Immediately export the unencrypted CSV and hand over the USB drive without logging the '
                       'transfer.',
                       'Politely decline citing data protection regulations (DPDP/GDPR), explain the risk of data '
                       'leakage, and guide them through the sanctioned CRM data-sharing workflow.',
                       'Sell the customer list to external marketing agencies for personal profit.',
                       'Report the marketing manager to the police without explaining company policy to them.'],
        'question_text': 'A marketing manager asks you to export all customer email addresses, phone numbers, and '
                         'physical addresses to a CSV on their personal USB drive.',
        'question_type': 'MCQ',
        'title': 'Situational: PII Export to Unencrypted CSV',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Focus on the underlying technical substance, respond objectively with architectural '
                          'trade-offs, and suggest a brief call to align constructively on the design.',
        'difficulty': 'MEDIUM',
        'explanation': 'Depersonalizing critical feedback and shifting to synchronous technical alignment de-escalates '
                       'tension.',
        'field': 'Engineering Architecture',
        'options': [   "Reply with personal insults attacking your peer's coding competence and intelligence.",
                       'Close the pull request and refuse to write any more code for the company.',
                       'Focus on the underlying technical substance, respond objectively with architectural '
                       'trade-offs, and suggest a brief call to align constructively on the design.',
                       'Merge the pull request anyway using administrator override permissions.'],
        'question_text': "A peer leaves sharp, abrasive comments on your pull request: 'Did you even think before "
                         "writing this? Completely wrong approach.'",
        'question_type': 'MCQ',
        'title': 'Situational: Harsh PR Critique',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Gather data on meeting hours vs coding hours, and propose consolidating ceremonies, '
                          "implementing async status updates, and designating dedicated 'No-Meeting' focus blocks.",
        'difficulty': 'HARD',
        'explanation': 'Data-backed proposals for async standups and focus blocks reclaim engineering productivity.',
        'field': 'Engineering Architecture',
        'options': [   'Decline every meeting on your calendar without explanation and refuse to speak to anyone.',
                       'Attend every meeting with camera and microphone off while playing video games.',
                       'Resign from the company without giving feedback on meeting culture.',
                       'Gather data on meeting hours vs coding hours, and propose consolidating ceremonies, '
                       "implementing async status updates, and designating dedicated 'No-Meeting' focus blocks."],
        'question_text': 'Your team calendar is overloaded with 4 hours of recurring daily agile ceremonies, leaving '
                         'insufficient uninterrupted time for deep engineering work.',
        'question_type': 'MCQ',
        'title': 'Situational: Agile Ceremony Overload',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Formulate a migration proposal outlining security exposure, evaluate modern supported '
                          'framework alternatives, and prioritize migration in the quarterly engineering roadmap.',
        'difficulty': 'MEDIUM',
        'explanation': 'Roadmap prioritization and security risk quantification drive disciplined framework '
                       'modernization.',
        'field': 'Engineering Architecture',
        'options': [   'Formulate a migration proposal outlining security exposure, evaluate modern supported '
                       'framework alternatives, and prioritize migration in the quarterly engineering roadmap.',
                       "Ignore the end-of-life status because the service hasn't crashed recently.",
                       'Attempt to rewrite the entire framework from scratch by yourself over the weekend.',
                       'Shut down the microservice immediately, taking down customer routing without warning.'],
        'question_text': 'A core routing microservice is running on a web framework version that reached official '
                         'end-of-life and will receive no further security patches.',
        'question_type': 'MCQ',
        'title': 'Situational: End-of-Life Microservice Framework',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Reach out to their squad lead collegially, compare architecture and feature sets, and '
                          'collaborate on a unified roadmap that consolidates efforts rather than creating duplicate '
                          'debt.',
        'difficulty': 'HARD',
        'explanation': 'Cross-team synergy and convergence reduce duplicate architectural maintenance across the '
                       'enterprise.',
        'field': 'Engineering Architecture',
        'options': [   'Publicly accuse their team of stealing your architecture during the company all-hands.',
                       'Reach out to their squad lead collegially, compare architecture and feature sets, and '
                       'collaborate on a unified roadmap that consolidates efforts rather than creating duplicate '
                       'debt.',
                       'Race to release your notification engine first so their work becomes completely worthless.',
                       "Delete your squad's codebase and pretend you never built a notification engine."],
        'question_text': "While reviewing another squad's demo, you notice they have spent two months building a "
                         'notification engine nearly identical to the one your squad maintains.',
        'question_type': 'MCQ',
        'title': 'Situational: Duplicate Feature Development',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Reach out to the support engineer with a standardized triage template: request specific '
                          'timestamp, tenant ID, expected vs actual behavior, and network request IDs.',
        'difficulty': 'MEDIUM',
        'explanation': 'Providing structured triage templates enables support teams to gather actionable diagnostic '
                       'data.',
        'field': 'Engineering Architecture',
        'options': [   'Close the ticket immediately as invalid without offering guidance on how to provide '
                       'reproduction details.',
                       'Deploy random code changes to production hoping one of them fixes whatever is broken.',
                       'Reach out to the support engineer with a standardized triage template: request specific '
                       'timestamp, tenant ID, expected vs actual behavior, and network request IDs.',
                       'Reprimand the customer directly for submitting an unhelpful ticket.'],
        'question_text': "A critical customer support escalation ticket arrives with the title 'System Broken' and no "
                         'logs, account IDs, or reproduction steps attached.',
        'question_type': 'MCQ',
        'title': 'Situational: Missing Bug Reproduction Steps',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Prioritize paired knowledge-transfer sessions, record architecture walkthroughs, document '
                          'edge cases and operational runbooks, and cross-train team members on key workflows.',
        'difficulty': 'HARD',
        'explanation': 'Intensive paired knowledge transfer and runbook documentation mitigate key-person operational '
                       'risk.',
        'field': 'Engineering Architecture',
        'options': [   'Beg the engineer not to leave and offer to pay them out of your own personal savings.',
                       'Demand that the engineer surrender all passwords immediately and escort them out of the '
                       'building on day one.',
                       'Do nothing and assume the team will figure out the billing engine when it breaks next quarter.',
                       'Prioritize paired knowledge-transfer sessions, record architecture walkthroughs, document edge '
                       'cases and operational runbooks, and cross-train team members on key workflows.'],
        'question_text': 'A senior engineer who solely understands the proprietary billing engine announces they are '
                         'leaving the company in two weeks.',
        'question_type': 'MCQ',
        'title': 'Situational: Key-Person Dependency Risk',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Remain calm, transparently explain that the presentation view is reflecting a cached state, '
                          'refresh the session or trigger a live recalculation, and proceed with composure.',
        'difficulty': 'MEDIUM',
        'explanation': 'Graceful composure, clear explanation of caching mechanics, and quick live recovery maintain '
                       'executive credibility.',
        'field': 'Engineering Architecture',
        'options': [   'Remain calm, transparently explain that the presentation view is reflecting a cached state, '
                       'refresh the session or trigger a live recalculation, and proceed with composure.',
                       'Panic, blame your junior teammates publicly in front of the client, and abruptly terminate the '
                       'call.',
                       'Pretend the screen is showing correct data and contradict the client when they point out the '
                       'error.',
                       'Unplug your computer monitor and claim that an internet blackout struck your entire city.'],
        'question_text': 'During a live client demonstration with company executives, the application shows stale '
                         'cached data, confusing the prospective client.',
        'question_type': 'MCQ',
        'title': 'Situational: Stale Cache Demo Failure',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Ask the teammate to draft an evaluation document assessing concrete business drivers: '
                          'scalability bottlenecks, operational overhead, network latency, and deployment complexity.',
        'difficulty': 'HARD',
        'explanation': 'Grounded architectural evaluation of operational trade-offs prevents trend-chasing technical '
                       'debt.',
        'field': 'Engineering Architecture',
        'options': [   "Insult the teammate and declare that anyone who likes microservices doesn't understand "
                       'software.',
                       'Ask the teammate to draft an evaluation document assessing concrete business drivers: '
                       'scalability bottlenecks, operational overhead, network latency, and deployment complexity.',
                       'Agree to the rewrite immediately without evaluating infrastructure costs or operational '
                       'readiness.',
                       'Secretly sabotage the monolith so that management is forced to authorize a rewrite.'],
        'question_text': 'A teammate advocates rewriting a rock-solid, well-tested monolithic service into 15 '
                         "microservices solely because 'microservices are more modern.'",
        'question_type': 'MCQ',
        'title': 'Situational: Unjustified Monolith Rewrite Proposal',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Raise the privacy and legal concerns with the compliance and legal counsel, pointing to '
                          'platform store guidelines (Apple/Google) and privacy statutes (DPDP/GDPR).',
        'difficulty': 'MEDIUM',
        'explanation': 'Constructive escalation to legal and compliance ensures product features conform to regulatory '
                       'statutes.',
        'field': 'Engineering Architecture',
        'options': [   'Implement the tracking silently and disguise the permissions prompt to trick users into '
                       'accepting.',
                       'Leak confidential corporate design documents to anonymous internet forums.',
                       'Raise the privacy and legal concerns with the compliance and legal counsel, pointing to '
                       'platform store guidelines (Apple/Google) and privacy statutes (DPDP/GDPR).',
                       'Resign immediately without discussing legal frameworks or alternative user-centric '
                       'approaches.'],
        'question_text': 'A product requirement asks for background geolocation tracking of users even when the mobile '
                         'application is explicitly closed and not in use.',
        'question_type': 'MCQ',
        'title': 'Situational: Privacy-Violating Tracking Feature',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': "Intervene diplomatically during the meeting: 'I'd really like to hear Priya finish her "
                          "thought on the partitioning strategy before we move to the next point.'",
        'difficulty': 'HARD',
        'explanation': "Inclusive meeting facilitation ensures every engineer's technical perspectives can be "
                       'evaluated on merit.',
        'field': 'Engineering Architecture',
        'options': [   'Start screaming at the senior engineer in the middle of the meeting to assert dominance.',
                       'Privately tell the junior teammates that their ideas are pointless and they should remain '
                       'silent.',
                       'Ignore the behavior completely because senior engineers should always dominate conversations.',
                       "Intervene diplomatically during the meeting: 'I'd really like to hear Priya finish her thought "
                       "on the partitioning strategy before we move to the next point.'"],
        'question_text': 'During architecture brainstorming sessions, a dominant senior engineer repeatedly cuts off '
                         'and dismisses ideas proposed by junior teammates.',
        'question_type': 'MCQ',
        'title': 'Situational: Speaking Over Junior Teammates',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Check search cluster health and error rates, and ask the reporter for the exact query '
                          'string, expected search result, and user permissions used.',
        'difficulty': 'MEDIUM',
        'explanation': 'Proactive cluster telemetry verification combined with specific triage inquiry pinpoints root '
                       'causes.',
        'field': 'Engineering Architecture',
        'options': [   'Check search cluster health and error rates, and ask the reporter for the exact query string, '
                       'expected search result, and user permissions used.',
                       'Restart the Elasticsearch cluster immediately in production without verifying cluster status.',
                       "Mark the bug 'Works For Me' and refuse to communicate further with the reporter.",
                       'Delete the search feature entirely and replace it with a static dropdown menu.'],
        'question_text': "A high-priority bug report states 'Search is broken' without specifying query terms, user "
                         'roles, or environment details.',
        'question_type': 'MCQ',
        'title': "Situational: Vague 'Search Broken' Bug Report",
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Insist on running baseline fairness and demographic parity evaluations before deployment, '
                          'highlighting ethical and legal exposure under labor and discrimination laws.',
        'difficulty': 'HARD',
        'explanation': 'Rigorous fairness audits and demographic parity evaluations are mandatory before '
                       'operationalizing ML models.',
        'field': 'Engineering Architecture',
        'options': [   'Deploy the model immediately to production because 94% accuracy is the only metric that '
                       'matters.',
                       'Insist on running baseline fairness and demographic parity evaluations before deployment, '
                       'highlighting ethical and legal exposure under labor and discrimination laws.',
                       'Alter the training data manually to produce whatever bias distribution management wants to '
                       'see.',
                       'Refuse to work on any artificial intelligence projects ever again.'],
        'question_text': 'A machine learning predictive hiring model shows 94% accuracy, but the data science team has '
                         'not conducted disparate impact or fairness audits.',
        'question_type': 'MCQ',
        'title': 'Situational: Deploying Model Without Bias Audit',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Profile the test pipeline, parallelize test execution across worker nodes, split into fast '
                          'unit and slower nightly suites, and mock slow external HTTP calls.',
        'difficulty': 'MEDIUM',
        'explanation': 'Profiling and parallelizing test suites preserves developer velocity while maintaining test '
                       'coverage.',
        'field': 'Engineering Architecture',
        'options': [   'Permanently delete all integration tests so that commits take 5 seconds to merge.',
                       'Threaten to terminate any engineer who complains about the 45-minute wait time.',
                       'Profile the test pipeline, parallelize test execution across worker nodes, split into fast '
                       'unit and slower nightly suites, and mock slow external HTTP calls.',
                       'Instruct engineers to stop testing their code locally and in CI altogether.'],
        'question_text': 'The automated test suite takes 45 minutes to execute on every commit, leading engineers to '
                         'bypass testing and merge directly to trunk.',
        'question_type': 'MCQ',
        'title': 'Situational: 45-Minute Integration Test Suite',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Collaborate with architecture and product leads to evaluate the operational maintenance '
                          'overhead of an on-prem appliance vs multi-tenant isolation, and present a realistic cost '
                          'model.',
        'difficulty': 'HARD',
        'explanation': 'Thorough operational and economic evaluation determines whether customer-managed deployments '
                       'are sustainable.',
        'field': 'Engineering Architecture',
        'options': [   'Promise the customer an on-premise version in two weeks without consulting engineering or '
                       'architecture.',
                       'Refuse to speak with the sales representative and reject the customer outright without '
                       'analysis.',
                       "Copy the cloud production database to a USB drive and mail it to the customer's office.",
                       'Collaborate with architecture and product leads to evaluate the operational maintenance '
                       'overhead of an on-prem appliance vs multi-tenant isolation, and present a realistic cost '
                       'model.'],
        'question_text': 'A major enterprise customer promises a lucrative contract if your team provides an '
                         'on-premise Kubernetes installation of your multi-tenant SaaS application.',
        'question_type': 'MCQ',
        'title': 'Situational: On-Premise Demand for SaaS Product',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Advise against disabling security controls; instead, generate and install a valid local CA '
                          'certificate in the staging environment trust store to maintain production parity.',
        'difficulty': 'MEDIUM',
        'explanation': 'Maintaining production parity in staging trust stores prevents security vulnerabilities from '
                       'escaping.',
        'field': 'Engineering Architecture',
        'options': [   'Advise against disabling security controls; instead, generate and install a valid local CA '
                       'certificate in the staging environment trust store to maintain production parity.',
                       'Disable certificate verification across all environments, including production, to prevent '
                       'future errors.',
                       'Publicly mock the teammate for not understanding TLS handshakes.',
                       'Ignore the issue and allow staging communication to occur over unencrypted plaintext.'],
        'question_text': 'A teammate proposes disabling SSL/TLS certificate verification in the staging environment to '
                         'resolve a self-signed certificate error quickly.',
        'question_type': 'MCQ',
        'title': 'Situational: Disabling SSL in Staging',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Establish a 2-hour daily overlapping window for synchronous reviews, set clear async review '
                          'handoff guidelines, and distribute reviewer assignments across both regions.',
        'difficulty': 'HARD',
        'explanation': 'Structured overlap windows and distributed review responsibilities streamline cross-timezone '
                       'collaboration.',
        'field': 'Engineering Architecture',
        'options': [   'Require the offshore team to work overnight shifts indefinitely with no schedule adjustments.',
                       'Establish a 2-hour daily overlapping window for synchronous reviews, set clear async review '
                       'handoff guidelines, and distribute reviewer assignments across both regions.',
                       'Require the onshore team to work overnight shifts indefinitely with no schedule adjustments.',
                       'Eliminate code reviews entirely for both teams so that everyone merges without waiting.'],
        'question_text': 'Code reviews between an onshore team and an offshore team take 48-72 hours due to an '
                         'uncoordinated 9.5-hour time difference.',
        'question_type': 'MCQ',
        'title': 'Situational: Offshore 9.5-Hour Time Zone Gap',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Isolate the race condition with an automated concurrency test, introduce database row-level '
                          'locking or optimistic concurrency tokens, and verify idempotency.',
        'difficulty': 'MEDIUM',
        'explanation': 'Optimistic concurrency control and row-level locking guarantee transactional integrity under '
                       'high load.',
        'field': 'Engineering Architecture',
        'options': [   'Ignore the issue because 10,000 TPS only happens during annual flash sales.',
                       'Catch the exception silently and log a generic message without refunding the customer.',
                       'Isolate the race condition with an automated concurrency test, introduce database row-level '
                       'locking or optimistic concurrency tokens, and verify idempotency.',
                       'Disable multi-threading in the payment gateway so it only processes one payment at a time.'],
        'question_text': 'Under peak concurrency tests of 10,000 transactions per second, a subtle race condition '
                         'occasionally double-charges a customer wallet.',
        'question_type': 'MCQ',
        'title': 'Situational: Race Condition in Billing Under Load',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Present an infrastructure audit detailing current redundancy, calculate the multi-million '
                          'dollar multi-region active-active cost of 99.999%, and align on realistic SLA tiers.',
        'difficulty': 'HARD',
        'explanation': 'Evidence-based infrastructure cost modeling brings contractual SLAs into alignment with '
                       'engineering reality.',
        'field': 'Engineering Architecture',
        'options': [   'Tell the sales team that 99.999% is impossible and refuse to support the customer.',
                       'Silently agree to the contract and hope the application never experiences an outage.',
                       'Forge monthly uptime reports to make it look like the system achieved five nines.',
                       'Present an infrastructure audit detailing current redundancy, calculate the multi-million '
                       'dollar multi-region active-active cost of 99.999%, and align on realistic SLA tiers.'],
        'question_text': "The sales team closes an enterprise deal by promising 'five nines' (99.999% uptime, <5 "
                         'minutes downtime/year) without consulting infrastructure leads.',
        'question_type': 'MCQ',
        'title': 'Situational: Sales SLA Promise of 99.999%',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Inform the on-call manager immediately, request a secondary shadow pairing shift alongside '
                          'an experienced engineer, and review critical incident runbooks before primary duty.',
        'difficulty': 'MEDIUM',
        'explanation': 'Shadow pairing and runbook onboarding ensure on-call engineers can resolve production '
                       'incidents safely.',
        'field': 'Engineering Architecture',
        'options': [   'Inform the on-call manager immediately, request a secondary shadow pairing shift alongside an '
                       'experienced engineer, and review critical incident runbooks before primary duty.',
                       "Accept primary on-call duty silently and mute your phone so alerts don't wake you up.",
                       'Panicking and quitting your job the day before your on-call rotation begins.',
                       "Route all incoming pager alerts directly to the CEO's personal phone number."],
        'question_text': 'You are placed on the Tier-1 production on-call rotation next week without having received '
                         'any system runbooks, shadow shifts, or alert training.',
        'question_type': 'MCQ',
        'title': 'Situational: On-Call Rotation Without Training',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Immediately notify the team lead, audit the migration for schema corruption or lock '
                          'contention, verify automated backup restore points, and reinforce CI/CD deployment gates.',
        'difficulty': 'HARD',
        'explanation': 'Auditing rogue changes and enforcing automated deployment gates protect production stability.',
        'field': 'Engineering Architecture',
        'options': [   'Congratulate the teammate on their bravery and encourage everyone to test directly in '
                       'production.',
                       'Immediately notify the team lead, audit the migration for schema corruption or lock '
                       'contention, verify automated backup restore points, and reinforce CI/CD deployment gates.',
                       'Silently drop the database tables that the teammate created to teach them a lesson.',
                       "Ignore the bypass completely because the production database didn't crash this time."],
        'question_text': "A teammate pushes a database migration script directly to the production database to 'save "
                         "time', bypassing staging testing.",
        'question_type': 'MCQ',
        'title': 'Situational: Bypassing Staging to Test in Prod',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Implement cryptographic HMAC signature verification using the shared secret, reject '
                          'unverified payloads with 401 Unauthorized, and add replay-prevention timestamp checks.',
        'difficulty': 'MEDIUM',
        'explanation': 'Cryptographic signature verification and replay prevention secure external webhook '
                       'integrations.',
        'field': 'Engineering Architecture',
        'options': [   "Leave the endpoint open because external providers usually don't send malicious payloads.",
                       'Disable the webhook endpoint entirely so that customers never receive payment confirmations.',
                       'Implement cryptographic HMAC signature verification using the shared secret, reject unverified '
                       'payloads with 401 Unauthorized, and add replay-prevention timestamp checks.',
                       'Store incoming payloads directly into the database without any validation or sanitization.'],
        'question_text': 'You discover that an external third-party payment webhook endpoint accepts incoming HTTP '
                         'POST requests without verifying HMAC signatures.',
        'question_type': 'MCQ',
        'title': 'Situational: Unauthenticated Webhook Payloads',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Adopt an automated zero-config code formatter (such as Prettier/Black) enforced in CI '
                          'pre-commit hooks, removing subjective human debates from pull requests.',
        'difficulty': 'HARD',
        'explanation': 'Automating formatting with opinionated CI tooling eliminates subjective bikeshedding.',
        'field': 'Engineering Architecture',
        'options': [   'Let the teams continue arguing on every pull request for the next six months.',
                       'Mandate that whichever team has more senior engineers wins every formatting debate.',
                       "Ban all code formatters and linters from the company's repositories.",
                       'Adopt an automated zero-config code formatter (such as Prettier/Black) enforced in CI '
                       'pre-commit hooks, removing subjective human debates from pull requests.'],
        'question_text': 'Following an organizational merger of two engineering teams, heated PR arguments erupt over '
                         'linting rules and code formatting conventions.',
        'question_type': 'MCQ',
        'title': 'Situational: Squad Code Style Disagreements',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Implement an immediate targeted patch to resolve the active memory leak in production, and '
                          'schedule the clean architectural abstraction for the next architectural sprint.',
        'difficulty': 'MEDIUM',
        'explanation': 'Pragmatic engineering prioritizes immediate operational stability before executing '
                       'architectural redesigns.',
        'field': 'Engineering Architecture',
        'options': [   'Implement an immediate targeted patch to resolve the active memory leak in production, and '
                       'schedule the clean architectural abstraction for the next architectural sprint.',
                       'Spend three months redesigning the abstraction while allowing production servers to crash '
                       'daily.',
                       'Patch the leak with an infinite while-loop that consumes all available server CPU.',
                       'Ignore both the leak and the abstraction, hoping cloud autoscaling masks the issue.'],
        'question_text': 'A legacy caching layer is causing periodic memory leaks; you must choose between patching '
                         'the leak or redesigning the abstraction layer.',
        'question_type': 'MCQ',
        'title': 'Situational: Tech Debt vs Abstraction Patch',
        'topic': 'Situational Judgement'},
    {   'category': 'Additional',
        'correct_answer': 'Follow the sanctioned identity verification security protocol (e.g. video verification with '
                          'IT security) to reset MFA tokens securely rather than bypassing security checks.',
        'difficulty': 'HARD',
        'explanation': 'Adhering to verified identity protocols prevents social engineering while resolving executive '
                       'lockouts.',
        'field': 'Engineering Architecture',
        'options': [   'Disable multi-factor authentication for the entire company so the executive can log in without '
                       'codes.',
                       'Follow the sanctioned identity verification security protocol (e.g. video verification with IT '
                       'security) to reset MFA tokens securely rather than bypassing security checks.',
                       'Hand over the root database master credentials to the executive via email.',
                       'Refuse to help the executive and hang up the phone during their board meeting.'],
        'question_text': 'An executive user is locked out of their enterprise account after multiple failed '
                         'multi-factor authentication attempts during an urgent board meeting.',
        'question_type': 'MCQ',
        'title': 'Situational: MFA Lockout Escalation',
        'topic': 'Situational Judgement'},
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
