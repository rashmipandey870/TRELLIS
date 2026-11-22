"""TRELLIS Technical Knowledge & Multi-Disciplinary Question Bank Fixtures (100 Questions).
60 Technical Knowledge questions (Full Stack, Cloud/DevOps, Data/AI, Core Systems) +
40 Multi-Disciplinary Architecture & Engineering questions.
"""

from app.schemas.category import AssessmentCategory

TECHNICAL_QUESTIONS = [
    # --- FULL STACK (15) ---
    {
        "title": "Angular Change Detection Strategy",
        "question_text": "In Angular, what is the key difference between ChangeDetectionStrategy.Default and ChangeDetectionStrategy.OnPush?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Frontend Architecture",
        "difficulty": "MEDIUM",
        "correct_answer": "OnPush checks the component only when its @Input references change, an event fires inside it, or an async pipe emits.",
        "options": [
            "OnPush completely disables the change detection cycle for the component and its children permanently.",
            "OnPush checks the component only when its @Input references change, an event fires inside it, or an async pipe emits.",
            "Default runs change detection only during browser page reload events.",
            "Default requires manual invocation of ChangeDetectorRef.detectChanges() on every user keystroke."
        ],
        "explanation": "OnPush optimizes rendering performance by skipping checks unless input object identities change or internal async events trigger it."
    },
    {
        "title": "Browser Critical Rendering Path",
        "question_text": "Which sequence correctly represents the browser Critical Rendering Path from HTML arrival to pixels on screen?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Browser Internals",
        "difficulty": "MEDIUM",
        "correct_answer": "DOM -> CSSOM -> Render Tree -> Layout (Reflow) -> Paint -> Composite",
        "options": [
            "DOM -> Render Tree -> CSSOM -> Paint -> Layout -> Composite",
            "DOM -> CSSOM -> Render Tree -> Layout (Reflow) -> Paint -> Composite",
            "CSSOM -> DOM -> Layout -> Render Tree -> Composite -> Paint",
            "Render Tree -> DOM -> CSSOM -> Composite -> Paint -> Layout"
        ],
        "explanation": "The browser builds the DOM and CSSOM concurrently, combines visible elements into the Render Tree, calculates geometry in Layout, draws pixels in Paint, and layers them in Composite."
    },
    {
        "title": "JWT In-Memory vs LocalStorage Security",
        "question_text": "Why do security-hardened Single Page Applications store access tokens in memory (e.g., framework signals/variables) instead of localStorage?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Web Security",
        "difficulty": "HARD",
        "correct_answer": "Tokens in localStorage are accessible by any JavaScript running in the origin, making them vulnerable to exfiltration via Cross-Site Scripting (XSS).",
        "options": [
            "LocalStorage cannot store strings longer than 128 characters.",
            "Tokens in localStorage are accessible by any JavaScript running in the origin, making them vulnerable to exfiltration via Cross-Site Scripting (XSS).",
            "In-memory tokens automatically sync across all browser tabs via the DOM without web workers.",
            "HTTP headers cannot transmit tokens stored in persistent client storage."
        ],
        "explanation": "LocalStorage is readable by third-party scripts injected through XSS. In-memory storage combined with HttpOnly refresh cookies protects credentials from direct JavaScript exfiltration."
    },
    {
        "title": "HTTP/2 Multiplexing Benefits",
        "question_text": "What fundamental TCP bottleneck in HTTP/1.1 is resolved by HTTP/2 multiplexing over a single connection?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Networking",
        "difficulty": "MEDIUM",
        "correct_answer": "Head-of-Line (HoL) blocking at the application layer where requests had to wait for prior responses on that socket.",
        "options": [
            "DNS lookup latency for secondary domains.",
            "Head-of-Line (HoL) blocking at the application layer where requests had to wait for prior responses on that socket.",
            "TLS handshake certificate expiration verification.",
            "The 1500-byte Maximum Transmission Unit (MTU) limit on Ethernet networks."
        ],
        "explanation": "HTTP/2 frames multiple interleaved bidirectional streams over one TCP connection, removing HTTP/1.1 pipelining HoL blocking."
    },
    {
        "title": "CORS Preflight Trigger Conditions",
        "question_text": "Which HTTP request condition triggers a CORS preflight (OPTIONS) request from a web browser?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Web Security",
        "difficulty": "MEDIUM",
        "correct_answer": "Sending a Content-Type header of 'application/json' or custom authorization headers.",
        "options": [
            "A standard GET request with Accept: text/html and no custom headers.",
            "Sending a Content-Type header of 'application/json' or custom authorization headers.",
            "A standard POST request sending form-urlencoded data with standard simple headers.",
            "A HEAD request navigating within the exact same origin."
        ],
        "explanation": "Requests with Content-Type application/json or non-simple headers (like Authorization) are not 'simple requests' and require a preflight check."
    },
    {
        "title": "CSS Stacking Context Creation",
        "question_text": "Which CSS declaration creates a new stacking context without requiring position: relative or absolute?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Frontend Architecture",
        "difficulty": "MEDIUM",
        "correct_answer": "opacity: 0.99 (or any value less than 1)",
        "options": [
            "display: inline-block",
            "opacity: 0.99 (or any value less than 1)",
            "margin: auto",
            "border: 1px solid red"
        ],
        "explanation": "Setting opacity < 1, transform, filter, or will-change creates a new stacking context in modern browsers."
    },
    {
        "title": "TypeScript Discriminated Unions",
        "question_text": "In TypeScript, what characterizes a 'Discriminated Union' pattern?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "TypeScript",
        "difficulty": "MEDIUM",
        "correct_answer": "A union of object types that all share a common literal property used as an exact discriminant tag.",
        "options": [
            "A union type that only accepts primitive numeric constants.",
            "A union of object types that all share a common literal property used as an exact discriminant tag.",
            "A class inheritance tree utilizing private abstract constructors.",
            "A tuple type containing variable generic length arguments."
        ],
        "explanation": "Discriminated unions enable narrowing in switch/if statements via a shared literal tag like 'kind' or 'type'."
    },
    {
        "title": "PostgreSQL MVCC Mechanism",
        "question_text": "How does PostgreSQL Multi-Version Concurrency Control (MVCC) ensure read queries do not block write queries?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Databases",
        "difficulty": "HARD",
        "correct_answer": "Updates create a new tuple version with xmin/xmax transaction visibility IDs rather than overwriting data in-place.",
        "options": [
            "Postgres acquires table-level exclusive locks on every write transaction.",
            "Updates create a new tuple version with xmin/xmax transaction visibility IDs rather than overwriting data in-place.",
            "All writes are queued into a Redis cache until all readers finish executing.",
            "Write operations spawn separate temporary SQLite databases on disk."
        ],
        "explanation": "PostgreSQL maintains multiple row versions with xmin/xmax timestamps, enabling readers to see consistent snapshots without read locks."
    },
    {
        "title": "FastAPI Dependency Injection Scope",
        "question_text": "When using FastAPI's Depends(get_db) in a route handler, what is the default lifecycle of the injected database session?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Backend Frameworks",
        "difficulty": "MEDIUM",
        "correct_answer": "Per-request: created at request start, shared across dependencies in that request, and closed in the yield teardown block.",
        "options": [
            "Singleton: created once at server startup and shared globally across all threads and requests.",
            "Per-request: created at request start, shared across dependencies in that request, and closed in the yield teardown block.",
            "Per-query: recreated before every individual SQL statement execution.",
            "Process-level: cached indefinitely until garbage collected."
        ],
        "explanation": "Dependencies using yield execute setup before the route handler and teardown (closing the session) immediately after response generation."
    },
    {
        "title": "Idempotent HTTP Methods",
        "question_text": "Which set of HTTP methods are formally defined as idempotent according to RFC 9110?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "API Design",
        "difficulty": "EASY",
        "correct_answer": "GET, HEAD, PUT, DELETE, OPTIONS, TRACE",
        "options": [
            "POST, PUT, PATCH, DELETE",
            "GET, HEAD, PUT, DELETE, OPTIONS, TRACE",
            "POST, GET, OPTIONS, CONNECT",
            "PUT, POST, PATCH, OPTIONS"
        ],
        "explanation": "An idempotent method produces the same intended effect on the server state regardless of whether it is executed 1 time or N times."
    },
    {
        "title": "B-Tree vs Hash Index",
        "question_text": "Why are B-Tree indexes preferred over Hash indexes as the default index structure in relational databases?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Databases",
        "difficulty": "MEDIUM",
        "correct_answer": "B-Trees efficiently support range scans (BETWEEN, <, >), sorting (ORDER BY), and prefix matching, while Hash indexes only support exact equality.",
        "options": [
            "Hash indexes require 100x more memory than B-Trees.",
            "B-Trees efficiently support range scans (BETWEEN, <, >), sorting (ORDER BY), and prefix matching, while Hash indexes only support exact equality.",
            "Hash indexes cannot be created on varchar columns.",
            "B-Trees guarantee zero disk reads for all lookup queries."
        ],
        "explanation": "B-Trees keep data sorted, allowing logarithmic lookup, range queries, and ordered traversals, unlike unordered hash buckets."
    },
    {
        "title": "WebSockets vs Server-Sent Events (SSE)",
        "question_text": "When should Server-Sent Events (SSE) be chosen over WebSockets for real-time frontend streaming?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Networking",
        "difficulty": "MEDIUM",
        "correct_answer": "When communication is strictly server-to-client (unidirectional), running over standard HTTP with native browser auto-reconnection and HTTP/2 multiplexing.",
        "options": [
            "When high-frequency binary peer-to-peer audio and video transmission is required.",
            "When communication is strictly server-to-client (unidirectional), running over standard HTTP with native browser auto-reconnection and HTTP/2 multiplexing.",
            "When the server does not support any HTTP protocols above HTTP/1.0.",
            "When the client needs to stream raw binary byte arrays back to the server at 60fps."
        ],
        "explanation": "SSE is lightweight, operates over standard HTTP/HTTPS, supports HTTP/2 multiplexing, and includes automatic reconnection and event IDs natively."
    },
    {
        "title": "Database Connection Pool Exhaustion",
        "question_text": "What is the primary operational symptom of database connection pool exhaustion in a high-concurrency microservice?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Backend Reliability",
        "difficulty": "HARD",
        "correct_answer": "API request latency skyrockets as threads block waiting for connections, eventually triggering connection checkout timeouts (503 / 504 errors).",
        "options": [
            "Database disk space immediately reaches 100% capacity.",
            "API request latency skyrockets as threads block waiting for connections, eventually triggering connection checkout timeouts (503 / 504 errors).",
            "The database server CPU immediately drops to 0% idle state.",
            "Client browsers crash due to memory leaks."
        ],
        "explanation": "When all pool connections are checked out, incoming queries queue until their acquisition timeout expires, cascading latency spikes across the API."
    },
    {
        "title": "SQL Injection in Parameterized Queries",
        "question_text": "Why do parameterized queries (prepared statements) protect against SQL injection vulnerabilities?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Web Security",
        "difficulty": "EASY",
        "correct_answer": "The database compiles the SQL query structure first; user inputs are bound strictly as data values and cannot alter the SQL AST.",
        "options": [
            "User input is automatically converted to base64 before saving.",
            "The database compiles the SQL query structure first; user inputs are bound strictly as data values and cannot alter the SQL AST.",
            "Special characters like quotes and semicolons are deleted by the database driver.",
            "The query runs inside an isolated Docker container."
        ],
        "explanation": "Prepared statements parse the query plan before binding variables; data parameters are never treated as executable SQL tokens."
    },
    {
        "title": "Redis Cache Stampede Mitigation",
        "question_text": "Which strategy effectively prevents a 'Cache Stampede' (Thundering Herd) when a hot cache key expires?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Web & Full Stack",
        "topic": "Caching",
        "difficulty": "HARD",
        "correct_answer": "Using a distributed lock (or mutex) so only one worker queries the database to recalculate the key while others wait or serve stale data.",
        "options": [
            "Setting the cache TTL to 0 seconds so data is never cached.",
            "Using a distributed lock (or mutex) so only one worker queries the database to recalculate the key while others wait or serve stale data.",
            "Increasing the database connection limit to 10,000 connections.",
            "Restarting the Redis cluster every hour."
        ],
        "explanation": "Probabilistic early expiration (XFetch) or mutex locks ensure only one request regenerates the cached entity upon expiration."
    },

    # --- CLOUD & DEVOPS (15) ---
    {
        "title": "Kubernetes Pod Readiness vs Liveness Probes",
        "question_text": "What is the critical behavioral distinction between a Kubernetes Readiness Probe and a Liveness Probe?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Container Orchestration",
        "difficulty": "MEDIUM",
        "correct_answer": "Failing a readiness probe removes the Pod from Service endpoints (stops traffic); failing a liveness probe restarts the container.",
        "options": [
            "Failing a readiness probe reboots the underlying worker node; failing a liveness probe deletes the deployment.",
            "Failing a readiness probe removes the Pod from Service endpoints (stops traffic); failing a liveness probe restarts the container.",
            "Readiness probes only check CPU usage; liveness probes only inspect HTTP status codes.",
            "They are completely interchangeable aliases in Kubernetes v1.25+."
        ],
        "explanation": "Liveness probes detect deadlocks and restart stuck containers. Readiness probes determine if a healthy container is ready to accept user traffic."
    },
    {
        "title": "Docker Multi-Stage Build Advantages",
        "question_text": "What is the primary benefit of utilizing Docker multi-stage builds for compiled languages like Go, Rust, or Java?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Containers",
        "difficulty": "EASY",
        "correct_answer": "Compilers, build tools, and source code are left in intermediate stages, yielding minimal, hardened, lightweight production runtime images.",
        "options": [
            "Images compile at least 10x faster due to distributed GPU rendering.",
            "Compilers, build tools, and source code are left in intermediate stages, yielding minimal, hardened, lightweight production runtime images.",
            "It allows a single container to run Windows and Linux kernels simultaneously.",
            "Docker multi-stage builds eliminate the need for container registries."
        ],
        "explanation": "Multi-stage builds copy only the compiled binary or dist files into a minimal base (e.g. alpine or distroless), shrinking attack surface and size."
    },
    {
        "title": "Terraform State Locking Purpose",
        "question_text": "Why is remote state locking (e.g., using AWS DynamoDB with S3) essential in team-based Terraform deployments?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Infrastructure as Code",
        "difficulty": "MEDIUM",
        "correct_answer": "It prevents concurrent pipeline runs from acquiring write access to the state file simultaneously, preventing state corruption.",
        "options": [
            "It encrypts passwords with hardware security keys.",
            "It prevents concurrent pipeline runs from acquiring write access to the state file simultaneously, preventing state corruption.",
            "It automatically converts HCL syntax into Kubernetes YAML manifests.",
            "It bills cloud resources to different departmental cost centers."
        ],
        "explanation": "State locking ensures that only one terraform apply execution can modify remote infrastructure and state at any given moment."
    },
    {
        "title": "Zero-Downtime Blue-Green Deployment",
        "question_text": "In a Blue-Green deployment strategy, how is traffic transition handled to achieve zero downtime?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "CI/CD & Deployment",
        "difficulty": "EASY",
        "correct_answer": "The new release is fully deployed and verified on an idle identical environment (Green), after which the router/load balancer instantly cuts over traffic from Blue to Green.",
        "options": [
            "All servers are stopped simultaneously for 30 seconds while the database updates.",
            "The new release is fully deployed and verified on an idle identical environment (Green), after which the router/load balancer instantly cuts over traffic from Blue to Green.",
            "Traffic is randomly split 50/50 between versions forever.",
            "Old servers are deleted before new servers are created."
        ],
        "explanation": "Blue-Green maintains two identical environments; traffic switchover occurs at the load balancer level once the new environment passes verification."
    },
    {
        "title": "Circuit Breaker Pattern States",
        "question_text": "What are the three canonical states of the Circuit Breaker pattern in distributed systems?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Resilience Engineering",
        "difficulty": "MEDIUM",
        "correct_answer": "Closed (normal operation), Open (fast fail without calling target), Half-Open (trial requests to test recovery)",
        "options": [
            "Active, Inactive, Suspended",
            "Closed (normal operation), Open (fast fail without calling target), Half-Open (trial requests to test recovery)",
            "Green, Yellow, Red",
            "Connected, Disconnected, Reconnecting"
        ],
        "explanation": "When errors exceed a threshold, the breaker opens to prevent cascading failures. After a cooldown, half-open allows limited canary probes."
    },
    {
        "title": "Prometheus Pull vs Push Metric Scraping",
        "question_text": "Why does Prometheus primarily adopt a 'pull' model for gathering time-series metrics from target services?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Observability",
        "difficulty": "HARD",
        "correct_answer": "The monitoring server controls scrape frequency and pacing, can detect target downtime immediately if an endpoint is unreachable, and avoids targets overwhelming the collector.",
        "options": [
            "Pulling metrics requires zero network firewall ports to be open.",
            "The monitoring server controls scrape frequency and pacing, can detect target downtime immediately if an endpoint is unreachable, and avoids targets overwhelming the collector.",
            "Push models are mathematically incapable of recording timestamps.",
            "Pulling is required by the Linux kernel systemd service manager."
        ],
        "explanation": "Pulling allows the server to manage ingestion load and reliably detect target health without being swamped by millions of uncoordinated push bursts."
    },
    {
        "title": "Horizontal Pod Autoscaler (HPA) Metric Evaluation",
        "question_text": "How does Kubernetes Horizontal Pod Autoscaler (HPA) calculate desired replicas given a target metric utilization?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Container Orchestration",
        "difficulty": "MEDIUM",
        "correct_answer": "desiredReplicas = ceil[currentReplicas * (currentMetricValue / targetMetricValue)]",
        "options": [
            "desiredReplicas = currentReplicas + 10 whenever CPU exceeds 50%",
            "desiredReplicas = ceil[currentReplicas * (currentMetricValue / targetMetricValue)]",
            "desiredReplicas = floor[targetMetricValue / currentReplicas]",
            "desiredReplicas = currentReplicas * 2 on any network drop"
        ],
        "explanation": "The standard HPA scaling formula computes ratio = currentMetric / targetMetric and scales current replicas proportionally."
    },
    {
        "title": "Kafka Partition Rebalancing Impact",
        "question_text": "What happens during an Apache Kafka consumer group partition rebalance when a new consumer joins?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Event Streaming",
        "difficulty": "HARD",
        "correct_answer": "Topic partitions are reassigned among active consumers; in eager rebalancing, all consumers stop processing until assignment completes.",
        "options": [
            "Messages in the partitions are deleted and recreated from scratch.",
            "Topic partitions are reassigned among active consumers; in eager rebalancing, all consumers stop processing until assignment completes.",
            "The Kafka cluster shuts down leader brokers temporarily.",
            "The consumer group is converted to point-to-point RPC."
        ],
        "explanation": "Rebalancing redistributes partitions across available consumer instances. Cooperative Sticky rebalancing mitigates stop-the-world pauses."
    },
    {
        "title": "Canary Deployment Routing",
        "question_text": "What defines a Canary deployment strategy compared to standard rolling updates?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "CI/CD & Deployment",
        "difficulty": "EASY",
        "correct_answer": "A tiny percentage of live user traffic (e.g. 5%) is routed to the new version to monitor metrics and error rates before full progressive rollout.",
        "options": [
            "The application is rewritten in a new language and launched on separate hardware.",
            "A tiny percentage of live user traffic (e.g. 5%) is routed to the new version to monitor metrics and error rates before full progressive rollout.",
            "Testing is performed exclusively in a local developer sandbox without production traffic.",
            "Deployments are only performed on weekends."
        ],
        "explanation": "Canary deployments limit the blast radius of potential regressions by exposing new versions to a small slice of real production traffic first."
    },
    {
        "title": "TLS 1.3 Handshake Round Trips",
        "question_text": "How many round trips (RTT) are required for a full TLS 1.3 cryptographic handshake before application data can be transmitted?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Networking & Security",
        "difficulty": "MEDIUM",
        "correct_answer": "1 RTT (and 0-RTT for resumed sessions)",
        "options": [
            "3 RTT",
            "1 RTT (and 0-RTT for resumed sessions)",
            "5 RTT",
            "Zero RTT always on initial connection"
        ],
        "explanation": "TLS 1.3 slashed the 2-RTT handshake of TLS 1.2 to 1-RTT by combining key share negotiation into the ClientHello message."
    },
    {
        "title": "Linux cgroups v2 Memory Limits",
        "question_text": "What occurs when a process inside a Docker container exceeds its configured cgroup memory.max limit?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Containers & Linux",
        "difficulty": "MEDIUM",
        "correct_answer": "The Linux kernel Out-Of-Memory (OOM) killer terminates the process (OOMKilled, exit code 137).",
        "options": [
            "The kernel automatically compresses RAM using zram without penalty.",
            "The Linux kernel Out-Of-Memory (OOM) killer terminates the process (OOMKilled, exit code 137).",
            "The container pauses execution and sleeps until memory frees up.",
            "The system reboots immediately."
        ],
        "explanation": "Exceeding the hard memory limit triggers the kernel OOM killer, killing the offending process with SIGKILL (128 + 9 = 137)."
    },
    {
        "title": "Twelve-Factor App Config Principle",
        "question_text": "According to the Twelve-Factor App methodology, where must application configuration that varies across deploys (staging, prod) be stored?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Software Architecture",
        "difficulty": "EASY",
        "correct_answer": "In environment variables.",
        "options": [
            "Committed into git repository constants files.",
            "In environment variables.",
            "Hardcoded inside compiled application binaries.",
            "Written into client-side browser cookies."
        ],
        "explanation": "Twelve-Factor Factor III mandates strict separation of config from code, injecting configuration as environment variables."
    },
    {
        "title": "OpenTelemetry Trace Context Propagation",
        "question_text": "In distributed tracing with OpenTelemetry, how is trace context propagated across HTTP network boundaries?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Observability",
        "difficulty": "HARD",
        "correct_answer": "Via standardized W3C Trace Context HTTP headers ('traceparent' and 'tracestate').",
        "options": [
            "Through database shared memory locks.",
            "Via standardized W3C Trace Context HTTP headers ('traceparent' and 'tracestate').",
            "By embedding trace IDs into DNS TXT records.",
            "Using CPU hardware interrupt registers."
        ],
        "explanation": "W3C Trace Context defines the 'traceparent' header (version, trace-id, parent-id, trace-flags) to correlate spans across services."
    },
    {
        "title": "Database Read Replicas vs Sharding",
        "question_text": "When should an enterprise architecture adopt database sharding instead of simply adding read replicas?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "Database Architecture",
        "difficulty": "HARD",
        "correct_answer": "When write throughput or dataset volume exceeds the capacity of a single primary database node.",
        "options": [
            "When read traffic increases by 10%.",
            "When write throughput or dataset volume exceeds the capacity of a single primary database node.",
            "When SSL certificates need renewal.",
            "When backups take longer than 5 minutes."
        ],
        "explanation": "Read replicas scale read queries horizontally, but all writes must still hit the single primary. Sharding partitions writes and data across nodes."
    },
    {
        "title": "GitOps Core Invariant",
        "question_text": "What is the foundational principle of GitOps operational frameworks like ArgoCD or Flux?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Cloud & DevOps",
        "topic": "GitOps",
        "difficulty": "MEDIUM",
        "correct_answer": "Git is the single source of truth; an automated reconciler continuously synchronizes actual cluster state to match the declared Git state.",
        "options": [
            "All developers must SSH into production servers using Git credentials.",
            "Git is the single source of truth; an automated reconciler continuously synchronizes actual cluster state to match the declared Git state.",
            "Every commit must be signed by at least 10 engineers.",
            "Git repositories must be hosted on internal physical tapes."
        ],
        "explanation": "GitOps uses Git as the declarative desired state; reconciliation controllers pull and enforce changes, preventing configuration drift."
    },

    # --- DATA & AI (15) ---
    {
        "title": "RAG Chunking Trade-offs",
        "question_text": "In Retrieval-Augmented Generation (RAG), what is the key trade-off when selecting smaller vs larger text chunk sizes?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "RAG Systems",
        "difficulty": "MEDIUM",
        "correct_answer": "Smaller chunks provide high semantic precision for vector retrieval but risk losing surrounding context; larger chunks retain context but dilute semantic embeddings.",
        "options": [
            "Smaller chunks make LLM inference 100x slower; larger chunks crash vector databases.",
            "Smaller chunks provide high semantic precision for vector retrieval but risk losing surrounding context; larger chunks retain context but dilute semantic embeddings.",
            "Smaller chunks only work with English text; larger chunks work with any language.",
            "Chunk size has zero measurable effect on retrieval quality or context."
        ],
        "explanation": "Fine-grained chunks pinpoint exact sentences without embedding noise, but need techniques like parent-document retrieval to provide sufficient LLM context."
    },
    {
        "title": "Vector Embedding Cosine Similarity",
        "question_text": "Why is Cosine Similarity commonly used to compare normalized dense vector embeddings produced by LLM embedding models?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "Vector Search",
        "difficulty": "MEDIUM",
        "correct_answer": "It measures the cosine of the angle between vectors, capturing directional semantic orientation irrespective of vector magnitude.",
        "options": [
            "It computes the exact Euclidean distance between raw character strings.",
            "It measures the cosine of the angle between vectors, capturing directional semantic orientation irrespective of vector magnitude.",
            "It is the only mathematical function that can run on GPUs.",
            "It sorts words in alphabetical dictionary order."
        ],
        "explanation": "Cosine similarity focuses on orientation in semantic space; for unit-normalized vectors, cosine similarity equals the dot product."
    },
    {
        "title": "Transformer Self-Attention Complexity",
        "question_text": "What is the computational and memory complexity of standard Multi-Head Self-Attention with respect to sequence length N?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "Deep Learning",
        "difficulty": "HARD",
        "correct_answer": "O(N^2) quadratic complexity due to computing attention weights between every pair of tokens in the sequence.",
        "options": [
            "O(N) linear complexity",
            "O(N^2) quadratic complexity due to computing attention weights between every pair of tokens in the sequence.",
            "O(log N) logarithmic complexity",
            "O(1) constant time complexity"
        ],
        "explanation": "Computing the Q * K^T attention matrix produces an N x N matrix, scaling quadratically with sequence length."
    },
    {
        "title": "LoRA (Low-Rank Adaptation) Parameter Efficiency",
        "question_text": "How does LoRA achieve parameter-efficient fine-tuning (PEFT) without fine-tuning all model weights?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "LLM Fine-Tuning",
        "difficulty": "HARD",
        "correct_answer": "It freezes pre-trained model weights and injects trainable rank-decomposition matrices (A and B where d x r and r x k, r << d) into attention layers.",
        "options": [
            "It removes 90% of model layers and trains only the output softmax.",
            "It freezes pre-trained model weights and injects trainable rank-decomposition matrices (A and B where d x r and r x k, r << d) into attention layers.",
            "It converts floating point 32 weights into 1-bit binary booleans.",
            "It trains a separate external heuristic regex engine."
        ],
        "explanation": "By decomposing weight updates delta W into low-rank matrices A and B (rank r << d), LoRA reduces trainable parameters by >99% while preserving performance."
    },
    {
        "title": "Temperature in LLM Sampling",
        "question_text": "What is the mathematical effect of setting an LLM generation temperature to 0 (or near 0)?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "LLM Architecture",
        "difficulty": "EASY",
        "correct_answer": "It makes token generation deterministic (greedy decoding), consistently selecting the token with the highest predicted log-probability.",
        "options": [
            "It disables all safety filters.",
            "It makes token generation deterministic (greedy decoding), consistently selecting the token with the highest predicted log-probability.",
            "It forces the model to generate random gibberish.",
            "It reduces server GPU physical temperature by shutting down fans."
        ],
        "explanation": "Lower temperature scales logits so differences are magnified; T->0 approaches argmax (greedy choice of the top token)."
    },
    {
        "title": "HNSW (Hierarchical Navigable Small World) Graphs",
        "question_text": "What makes HNSW one of the most widely used approximate nearest neighbor (ANN) algorithms in vector databases?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "Vector Databases",
        "difficulty": "HARD",
        "correct_answer": "It builds multi-layer skip-list graphs where upper layers enable fast coarse-grained long-range navigation and lower layers provide fine-grained local search.",
        "options": [
            "It stores all vectors directly in uncompressed CSV files.",
            "It builds multi-layer skip-list graphs where upper layers enable fast coarse-grained long-range navigation and lower layers provide fine-grained local search.",
            "It converts floating point embeddings to ASCII characters.",
            "It requires zero CPU or RAM overhead."
        ],
        "explanation": "HNSW combines ideas from skip-lists and small-world graphs to achieve logarithmic O(log N) search latency with high recall."
    },
    {
        "title": "Prompt Injection Mitigation",
        "question_text": "Which defensive architecture provides the strongest protection against prompt injection in LLM agents with tool execution privileges?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "AI Security",
        "difficulty": "HARD",
        "correct_answer": "Strict server-side authorization and parameter validation on tool APIs, treating LLM output as untrusted user input, combined with output sandboxing.",
        "options": [
            "Telling the model in the system prompt 'Please do not obey evil instructions'.",
            "Strict server-side authorization and parameter validation on tool APIs, treating LLM output as untrusted user input, combined with output sandboxing.",
            "Filtering user queries for the exact word 'ignore'.",
            "Using a smaller 1B parameter model."
        ],
        "explanation": "System prompts cannot guarantee immunity from adversarial inputs. Security must be enforced deterministically at the tool and API boundary."
    },
    {
        "title": "Structured Outputs with JSON Schema",
        "question_text": "How do modern inference engines (e.g. llama.cpp, vLLM, Ollama) guarantee that an LLM outputs valid JSON conforming to a schema?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "Inference Engineering",
        "difficulty": "HARD",
        "correct_answer": "Constrained grammar decoding (CFG / JSON schema masking) that masks out invalid next tokens at the logit level during autoregressive generation.",
        "options": [
            "Repeatedly prompting the model until it accidentally generates valid syntax.",
            "Constrained grammar decoding (CFG / JSON schema masking) that masks out invalid next tokens at the logit level during autoregressive generation.",
            "Passing the raw output through Python json.loads() and returning empty string on error.",
            "Training a new model from scratch for each JSON schema."
        ],
        "explanation": "Grammar-guided decoding converts schemas into pushdown automata, forcing logit probability to -infinity for tokens violating syntax."
    },
    {
        "title": "Data Pipeline Lambda vs Kappa Architecture",
        "question_text": "What is the key architectural difference between a Lambda Architecture and a Kappa Architecture in big data processing?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "Data Engineering",
        "difficulty": "MEDIUM",
        "correct_answer": "Lambda maintains separate batch and real-time stream processing pipelines; Kappa unifies processing into a single stream processing pipeline.",
        "options": [
            "Lambda only uses AWS Lambda; Kappa only runs on Kubernetes.",
            "Lambda maintains separate batch and real-time stream processing pipelines; Kappa unifies processing into a single stream processing pipeline.",
            "Lambda cannot handle JSON data; Kappa cannot handle SQL queries.",
            "There is no difference; they are synonymous branding terms."
        ],
        "explanation": "Kappa avoids dual-codebase maintenance by treating all data as an append-only event stream replayed through one stream engine."
    },
    {
        "title": "Parquet Columnar Storage Efficiency",
        "question_text": "Why does Apache Parquet provide dramatic query performance and compression advantages for analytical SQL workloads (OLAP)?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "Data Warehousing",
        "difficulty": "MEDIUM",
        "correct_answer": "Columnar layout stores data of the same type together, enabling high compression ratios and allowing queries to read only the specific columns requested.",
        "options": [
            "It loads the entire dataset into browser localStorage.",
            "Columnar layout stores data of the same type together, enabling high compression ratios and allowing queries to read only the specific columns requested.",
            "It compiles SQL queries directly into C++ machine code.",
            "It stores records in plain uncompressed text lines like CSV."
        ],
        "explanation": "OLAP queries aggregate specific columns; Parquet skips irrelevant columns on disk and compresses homogeneous column data via run-length and dictionary encoding."
    },
    {
        "title": "Overfitting vs Underfitting Bias-Variance",
        "question_text": "In supervised machine learning, high variance and near-zero training error accompanied by high validation error indicates:",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "Machine Learning",
        "difficulty": "EASY",
        "correct_answer": "Overfitting (the model memorized training noise instead of generalizing).",
        "options": [
            "Underfitting (the model is too simple to capture patterns).",
            "Overfitting (the model memorized training noise instead of generalizing).",
            "Optimal Bayesian convergence.",
            "Data leakage from the test set."
        ],
        "explanation": "Overfitting occurs when a complex model fits noise in training data, resulting in poor out-of-sample generalization."
    },
    {
        "title": "Feature Scaling in Distance-Based Algorithms",
        "question_text": "Why is feature normalization/standardization (e.g. StandardScaler) crucial before running K-Means clustering or KNN?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "Machine Learning",
        "difficulty": "EASY",
        "correct_answer": "Features with larger numerical scales would disproportionately dominate Euclidean distance calculations regardless of relative importance.",
        "options": [
            "K-Means cannot compute distances on floating-point numbers.",
            "Features with larger numerical scales would disproportionately dominate Euclidean distance calculations regardless of relative importance.",
            "Standardization prevents integer overflow in Python.",
            "It reduces the dataset row count."
        ],
        "explanation": "Distance calculations assume uniform scales; an unscaled feature like 'Salary' ($100k) would completely drown out 'Years of Experience' (5)."
    },
    {
        "title": "Data Drift vs Concept Drift",
        "question_text": "In production machine learning systems, what distinguishes 'Concept Drift' from 'Data (Covariate) Drift'?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "MLOps",
        "difficulty": "HARD",
        "correct_answer": "Data drift is a shift in the distribution of input features P(X); concept drift is a change in the relationship between input features and target labels P(Y|X).",
        "options": [
            "Data drift affects only image models; concept drift affects only text models.",
            "Data drift is a shift in the distribution of input features P(X); concept drift is a change in the relationship between input features and target labels P(Y|X).",
            "Data drift occurs during training; concept drift occurs during testing.",
            "Concept drift is a hardware failure in GPU memory."
        ],
        "explanation": "In concept drift, what a given feature means changes over time (e.g. consumer purchasing behavior changes post-pandemic)."
    },
    {
        "title": "Quantization (GGUF / AWQ / bitsandbytes)",
        "question_text": "What is the primary trade-off when quantizing a 16-bit floating point LLM down to 4-bit integer representation (INT4)?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "Model Optimization",
        "difficulty": "MEDIUM",
        "correct_answer": "Memory footprint and bandwidth requirements are reduced by ~75% enabling execution on smaller hardware, with minor potential degradation in perplexity.",
        "options": [
            "Inference takes 10x more VRAM but guarantees 100% mathematical accuracy.",
            "Memory footprint and bandwidth requirements are reduced by ~75% enabling execution on smaller hardware, with minor potential degradation in perplexity.",
            "The model can no longer output punctuation or numbers.",
            "Context window length is reduced to 16 tokens."
        ],
        "explanation": "Quantization drastically cuts memory and memory-bus bottlenecks with negligible quality loss on modern techniques like AWQ/GGUF."
    },
    {
        "title": "Spark Broadcast Joins",
        "question_text": "When is a Broadcast Hash Join (Map-Side Join) utilized in Apache Spark, and why is it highly performant?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Data & AI",
        "topic": "Distributed Computing",
        "difficulty": "MEDIUM",
        "correct_answer": "When joining a large DataFrame with a small dimension table; copying the small table to all worker nodes eliminates expensive network shuffle of the large table.",
        "options": [
            "When joining two multi-terabyte tables together.",
            "When joining a large DataFrame with a small dimension table; copying the small table to all worker nodes eliminates expensive network shuffle of the large table.",
            "When running queries on a single-node laptop without a network.",
            "When writing output to local text files."
        ],
        "explanation": "Broadcasting the small table avoids a SortMergeJoin shuffle, allowing workers to join local partitions directly in memory."
    },

    # --- CORE SYSTEMS (15) ---
    {
        "title": "Virtual Memory and Page Faults",
        "question_text": "What triggers a Page Fault in an operating system's virtual memory subsystem?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Operating Systems",
        "difficulty": "MEDIUM",
        "correct_answer": "A program accesses a virtual memory address whose corresponding page is not currently mapped to physical RAM (e.g., swapped out or demand-paged).",
        "options": [
            "The program enters an infinite recursion loop.",
            "A program accesses a virtual memory address whose corresponding page is not currently mapped to physical RAM (e.g., swapped out or demand-paged).",
            "The hard disk sector containing the kernel binary is physically damaged.",
            "A web browser fails to load an HTML page over HTTP."
        ],
        "explanation": "When the MMU encounters a page table entry with valid bit 0, a hardware trap triggers the OS page fault handler to load the page into RAM."
    },
    {
        "title": "User Space vs Kernel Space Transition",
        "question_text": "How does an unprivileged user process transition CPU execution into kernel mode to perform disk I/O?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Operating Systems",
        "difficulty": "MEDIUM",
        "correct_answer": "Via a software interrupt or specialized system call instruction (e.g. 'syscall' on x86-64), which switches CPU privilege rings.",
        "options": [
            "By directly modifying the kernel code segment pointer in memory.",
            "Via a software interrupt or specialized system call instruction (e.g. 'syscall' on x86-64), which switches CPU privilege rings.",
            "By spawning a background thread in Python.",
            "By writing raw bytes to physical memory address 0x00000000."
        ],
        "explanation": "Syscall instructions transition CPU privilege from Ring 3 (user) to Ring 0 (kernel) via well-defined entry point handlers."
    },
    {
        "title": "Thread vs Process Memory Layout",
        "question_text": "Which memory component is unique to each individual thread within a multi-threaded process?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Concurrency",
        "difficulty": "EASY",
        "correct_answer": "The execution call stack and CPU register state (including program counter).",
        "options": [
            "The global heap memory.",
            "The execution call stack and CPU register state (including program counter).",
            "The initialized data segment (.data).",
            "The open file descriptor table."
        ],
        "explanation": "Threads share heap, code, globals, and file descriptors, but each thread maintains its own private call stack and register set."
    },
    {
        "title": "Deadlock Necessary Conditions",
        "question_text": "Which set represents the four Coffman conditions all required simultaneously for a system deadlock to occur?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Operating Systems",
        "difficulty": "HARD",
        "correct_answer": "Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait",
        "options": [
            "Starvation, Thrashing, Livelock, Race Condition",
            "Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait",
            "Read Lock, Write Lock, Shared Lock, Exclusive Lock",
            "Paging, Segmentation, Swapping, Fragmentation"
        ],
        "explanation": "Breaking any one of the four Coffman conditions mathematically prevents deadlocks from forming."
    },
    {
        "title": "Epoll vs Select Scalability",
        "question_text": "Why is Linux epoll O(1) in scalability compared to the O(N) complexity of traditional select/poll when handling 100,000 concurrent sockets?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "I/O Multiplexing",
        "difficulty": "HARD",
        "correct_answer": "epoll maintains a persistent kernel-space interest list (red-black tree) and returns an event list containing only active sockets, avoiding linear scans.",
        "options": [
            "epoll uses machine learning to predict which sockets will receive data.",
            "epoll maintains a persistent kernel-space interest list (red-black tree) and returns an event list containing only active sockets, avoiding linear scans.",
            "select/poll can only handle UDP packets, whereas epoll handles TCP.",
            "epoll bypasses the network interface card entirely."
        ],
        "explanation": "select/poll copies the entire file descriptor set to kernel on every call and loops over all N sockets; epoll returns only triggered descriptors."
    },
    {
        "title": "CPU Cache Line False Sharing",
        "question_text": "What is 'False Sharing' in high-performance multi-threaded C/C++ applications?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Computer Architecture",
        "difficulty": "HARD",
        "correct_answer": "Threads on separate cores update distinct, independent variables that happen to reside on the same 64-byte hardware cache line, causing constant cache invalidation.",
        "options": [
            "Two processes sharing the same virtual memory page without synchronization.",
            "Threads on separate cores update distinct, independent variables that happen to reside on the same 64-byte hardware cache line, causing constant cache invalidation.",
            "A CPU instruction cache predicting the wrong branch.",
            "A thread reading an uninitialized global pointer."
        ],
        "explanation": "Because cache coherence protocols operate at the cache line granularity (usually 64 bytes), updates to adjacent bytes invalidate the entire line across cores."
    },
    {
        "title": "Atomic Compare-And-Swap (CAS)",
        "question_text": "What does an atomic Compare-And-Swap (CAS) instruction perform in lock-free programming?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Concurrency",
        "difficulty": "MEDIUM",
        "correct_answer": "It atomically checks if a memory location holds an expected value; if true, it updates it to a new value and returns success, all in a single hardware cycle.",
        "options": [
            "It acquires an operating system mutex lock.",
            "It atomically checks if a memory location holds an expected value; if true, it updates it to a new value and returns success, all in a single hardware cycle.",
            "It swaps two CPU registers without touching memory.",
            "It deletes a variable from RAM."
        ],
        "explanation": "CAS is the fundamental primitive for lock-free data structures, guaranteeing atomicity without OS context switches."
    },
    {
        "title": "RAID 5 vs RAID 10 Fault Tolerance",
        "question_text": "What is the primary operational trade-off between RAID 5 and RAID 10 (1+0)?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Storage Systems",
        "difficulty": "MEDIUM",
        "correct_answer": "RAID 5 offers higher usable capacity (N-1) but suffers a write penalty for parity recalculation and long rebuild times; RAID 10 offers superior write IOPS and fast rebuilds at 50% capacity.",
        "options": [
            "RAID 5 can survive all disks failing at once; RAID 10 cannot survive any disk failure.",
            "RAID 5 offers higher usable capacity (N-1) but suffers a write penalty for parity recalculation and long rebuild times; RAID 10 offers superior write IOPS and fast rebuilds at 50% capacity.",
            "RAID 10 is only supported on SSDs, not HDDs.",
            "RAID 5 does not support data redundancy."
        ],
        "explanation": "RAID 5 requires read-modify-write parity computations. RAID 10 stripes mirrored pairs, offering raw speed at the cost of disk space."
    },
    {
        "title": "Copy-On-Write (COW) in Fork()",
        "question_text": "Why is the Linux fork() system call extremely fast even when the parent process consumes 32 GB of memory?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Operating Systems",
        "difficulty": "MEDIUM",
        "correct_answer": "fork() copies only the page tables with pages marked read-only; physical memory pages are only duplicated when either process writes to a page.",
        "options": [
            "fork() immediately compresses parent memory using gzip.",
            "fork() copies only the page tables with pages marked read-only; physical memory pages are only duplicated when either process writes to a page.",
            "fork() runs only on ARM architecture, not x86.",
            "Child processes never receive access to parent memory."
        ],
        "explanation": "Copy-On-Write defers memory duplication until modification, making process creation near-instantaneous."
    },
    {
        "title": "Little-Endian vs Big-Endian Byte Order",
        "question_text": "How is the 32-bit hexadecimal value 0x12345678 stored in sequential memory addresses starting at 0x00 on a Little-Endian system (x86-64)?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Computer Architecture",
        "difficulty": "EASY",
        "correct_answer": "0x78, 0x56, 0x34, 0x12 (least significant byte at the lowest memory address)",
        "options": [
            "0x12, 0x34, 0x56, 0x78 (most significant byte at lowest address)",
            "0x78, 0x56, 0x34, 0x12 (least significant byte at the lowest memory address)",
            "0x56, 0x78, 0x12, 0x34",
            "0x00, 0x12, 0x34, 0x56"
        ],
        "explanation": "Little-endian architectures store the least significant byte (LSB) first in ascending memory addresses."
    },
    {
        "title": "TCP Three-Way Handshake SYN Flooding",
        "question_text": "How do SYN Cookies protect web servers against TCP SYN flood denial-of-service attacks?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Networking & Security",
        "difficulty": "HARD",
        "correct_answer": "The server encodes connection state into the initial SYN-ACK sequence number, avoiding allocating memory in the SYN queue until a valid client ACK returns.",
        "options": [
            "The server drops all incoming TCP packets permanently.",
            "The server encodes connection state into the initial SYN-ACK sequence number, avoiding allocating memory in the SYN queue until a valid client ACK returns.",
            "The server disconnects from the internet for 10 minutes.",
            "The client sends its MAC address in the HTTP cookie header."
        ],
        "explanation": "SYN cookies eliminate half-open state allocation on the server by hashing client IP/port/MSS into the sequence number."
    },
    {
        "title": "Memory Leak in Garbage Collected Languages",
        "question_text": "How can a memory leak occur in a language with automated garbage collection like Java, Python, or Go?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Memory Management",
        "difficulty": "MEDIUM",
        "correct_answer": "Unused objects remain reachable from active GC root references (e.g. static collections, global registries, uncleared event listeners).",
        "options": [
            "The CPU physical silicon registers degrade over time.",
            "Unused objects remain reachable from active GC root references (e.g. static collections, global registries, uncleared event listeners).",
            "The language runs out of variable names.",
            "Garbage collection cannot reclaim memory allocated in functions with more than 5 lines."
        ],
        "explanation": "GC algorithms only collect objects that are unreachable from GC roots. Lingering references in caches or static fields prevent reclamation."
    },
    {
        "title": "POSIX Signal Handling Restrictions",
        "question_text": "Why is it unsafe to call functions like malloc() or printf() inside a POSIX signal handler?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Systems Programming",
        "difficulty": "HARD",
        "correct_answer": "They are not async-signal-safe; interrupting a non-reentrant function already holding internal mutexes causes deadlocks or heap corruption.",
        "options": [
            "Signal handlers execute in kernel space where C libraries do not exist.",
            "They are not async-signal-safe; interrupting a non-reentrant function already holding internal mutexes causes deadlocks or heap corruption.",
            "POSIX signals cannot pass string parameters.",
            "Signal handlers cannot consume more than 2 bytes of RAM."
        ],
        "explanation": "Signal handlers can interrupt code at any arbitrary instruction. Calling non-reentrant functions risks deadlocks if the interrupted thread was holding the malloc lock."
    },
    {
        "title": "Branch Predictor Speculative Execution",
        "question_text": "What hardware mechanism allows modern CPUs to keep execution pipelines full before conditional branches are resolved?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Computer Architecture",
        "difficulty": "MEDIUM",
        "correct_answer": "Branch prediction combined with speculative execution (and pipeline flush if the prediction was incorrect).",
        "options": [
            "Software interpretation of binary code.",
            "Branch prediction combined with speculative execution (and pipeline flush if the prediction was incorrect).",
            "Clock speed throttling.",
            "Dynamic RAM refreshing."
        ],
        "explanation": "CPUs use history tables to predict branch targets and speculatively execute instructions ahead of time, discarding work if mispredicted."
    },
    {
        "title": "SSD Write Amplification",
        "question_text": "What causes Write Amplification on Solid State Drives (SSDs)?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        "field": "Core Systems",
        "topic": "Storage Systems",
        "difficulty": "MEDIUM",
        "correct_answer": "NAND flash must be erased in large blocks before individual pages can be rewritten, requiring existing valid pages to be read, copied, and rewritten.",
        "options": [
            "Operating systems writing duplicate backup copies of every file.",
            "NAND flash must be erased in large blocks before individual pages can be rewritten, requiring existing valid pages to be read, copied, and rewritten.",
            "Electricity voltage fluctuations expanding disk sectors.",
            "USB cable impedance resistance."
        ],
        "explanation": "NAND flash cannot overwrite pages in place. Erasing an entire block requires garbage collection cycles, writing more physical bytes than logically requested."
    },

    # --- MULTI-DISCIPLINARY ARCHITECTURE & ENGINEERING (40) ---
    {
        "title": "CAP Theorem Trade-Offs",
        "question_text": "In a distributed network experiencing a network partition (P), what does the CAP theorem dictate a system must choose between?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "System Architecture",
        "topic": "Distributed Systems",
        "difficulty": "EASY",
        "correct_answer": "Consistency (C) or Availability (A)",
        "options": [
            "Performance or Reliability",
            "Consistency (C) or Availability (A)",
            "Security or Usability",
            "Throughput or Latency"
        ],
        "explanation": "During a network partition, a system can either return stale data/errors to remain available (AP) or block requests to guarantee consistency (CP)."
    },
    {
        "title": "Raft Consensus Leader Election",
        "question_text": "In the Raft consensus algorithm, how does a candidate node become the elected leader of a term?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "System Architecture",
        "topic": "Distributed Consensus",
        "difficulty": "MEDIUM",
        "correct_answer": "It receives votes from a strict majority (quorum: N/2 + 1) of the cluster nodes.",
        "options": [
            "It has the lowest IP address in the cluster.",
            "It receives votes from a strict majority (quorum: N/2 + 1) of the cluster nodes.",
            "The node with the highest CPU clock speed is chosen.",
            "It sends a broadcast message claiming leadership without a vote."
        ],
        "explanation": "Raft guarantees safety by requiring a majority quorum for both leader election and log entry commit."
    },
    {
        "title": "Eventual Consistency in Dynamo-Style Databases",
        "question_text": "In a quorum-based distributed store (like Cassandra), what inequality between replicas N, read quorum R, and write quorum W guarantees strong read-after-write consistency?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "System Architecture",
        "topic": "Distributed Storage",
        "difficulty": "HARD",
        "correct_answer": "R + W > N (the read set and write set must overlap on at least one replica)",
        "options": [
            "R + W < N",
            "R + W > N (the read set and write set must overlap on at least one replica)",
            "R * W = N",
            "R = W = 1"
        ],
        "explanation": "When R + W > N, the Pigeonhole Principle ensures at least one node in the read quorum contains the latest write version."
    },
    {
        "title": "LSM-Tree vs B-Tree Write Performance",
        "question_text": "Why do Log-Structured Merge-trees (LSM-trees) achieve substantially higher write throughput than B-trees?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "System Architecture",
        "topic": "Storage Engines",
        "difficulty": "HARD",
        "correct_answer": "LSM-trees write sequentially to an append-only commit log and in-memory MemTable, deferring expensive sorting to background compaction.",
        "options": [
            "LSM-trees do not write data to disk.",
            "LSM-trees write sequentially to an append-only commit log and in-memory MemTable, deferring expensive sorting to background compaction.",
            "B-trees can only store 10,000 records.",
            "LSM-trees use GPU hardware registers."
        ],
        "explanation": "Sequential writes are orders of magnitude faster than random disk updates; LSM-trees convert random writes into sequential appends."
    },
    {
        "title": "Bloom Filter False Positives",
        "question_text": "What is the probabilistic guarantee provided by a standard Bloom Filter?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "System Architecture",
        "topic": "Data Structures",
        "difficulty": "MEDIUM",
        "correct_answer": "Zero false negatives (if it says an element is absent, it is definitely absent), but false positives are possible.",
        "options": [
            "Zero false positives, but false negatives are possible.",
            "Zero false negatives (if it says an element is absent, it is definitely absent), but false positives are possible.",
            "100% deterministic accuracy for all queries.",
            "It can store and return the original string data."
        ],
        "explanation": "Bloom filters test set membership with zero false negatives, allowing databases to bypass disk reads when a key definitely does not exist."
    },
    {
        "title": "Saga Pattern Orchestration vs Choreography",
        "question_text": "In distributed microservices transactions, what distinguishes Saga Orchestration from Saga Choreography?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "System Architecture",
        "topic": "Microservices Patterns",
        "difficulty": "MEDIUM",
        "correct_answer": "Orchestration uses a centralized coordinator service to instruct participants; Choreography relies on services publishing and reacting to domain events independently.",
        "options": [
            "Orchestration uses two-phase commit (2PC); Choreography does not.",
            "Orchestration uses a centralized coordinator service to instruct participants; Choreography relies on services publishing and reacting to domain events independently.",
            "Choreography is only for monolithic architectures.",
            "Orchestration cannot perform compensating transactions."
        ],
        "explanation": "Orchestrators explicitly sequence calls and compensations; choreographers maintain decoupling via pub/sub events."
    },
    {
        "title": "Idempotency Keys in Payment APIs",
        "question_text": "How does an Idempotency-Key HTTP header ensure a customer is not charged twice during a network timeout?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "System Architecture",
        "topic": "API Design",
        "difficulty": "MEDIUM",
        "correct_answer": "The server caches the result of the initial request under the client UUID key; retries with the same key return the cached charge result without re-processing.",
        "options": [
            "The client sends an encryption key that reverses bank transactions.",
            "The server caches the result of the initial request under the client UUID key; retries with the same key return the cached charge result without re-processing.",
            "It cancels the customer's credit card.",
            "It converts POST requests to GET requests."
        ],
        "explanation": "Payment gateways record idempotency keys; duplicate submissions return the original transaction receipt rather than executing a new debit."
    },
    {
        "title": "Database WAL (Write-Ahead Logging)",
        "question_text": "What is the primary role of Write-Ahead Logging (WAL) in database transaction durability (ACID)?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "System Architecture",
        "topic": "Databases",
        "difficulty": "MEDIUM",
        "correct_answer": "Modifications are written and flushed to durable log storage on disk before the dirty data pages are written to data files.",
        "options": [
            "It writes an audit log to a remote syslog server.",
            "Modifications are written and flushed to durable log storage on disk before the dirty data pages are written to data files.",
            "It verifies user login credentials against Active Directory.",
            "It compresses tables during low-traffic night hours."
        ],
        "explanation": "WAL guarantees durability and crash recovery: if the server powers down before dirty pages reach disk, the WAL is replayed on startup."
    },
    {
        "title": "Content Delivery Network (CDN) Cache Invalidation",
        "question_text": "Why is asset hashing (e.g. main.a1b2c3d4.js) preferred over manual cache purging in frontend production deployments?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "System Architecture",
        "topic": "Web Infrastructure",
        "difficulty": "EASY",
        "correct_answer": "Each unique build produces a distinct URL, enabling infinite (1-year) immutable caching while guaranteeing instant client updates when index.html changes.",
        "options": [
            "Asset hashing encrypts JavaScript so competitors cannot read it.",
            "Each unique build produces a distinct URL, enabling infinite (1-year) immutable caching while guaranteeing instant client updates when index.html changes.",
            "CDNs charge 10x more for unhashed filenames.",
            "Browser engines refuse to run unhashed JavaScript files."
        ],
        "explanation": "Cache-busting with content hashes allows static assets to be cached permanently (`Cache-Control: immutable, max-age=31536000`), with zero stale asset bugs."
    },
    {
        "title": "Reverse Proxy vs Forward Proxy",
        "question_text": "What is the architectural difference between a Forward Proxy and a Reverse Proxy?",
        "question_type": "MCQ",
        "category": AssessmentCategory.ADDITIONAL.value,
        "field": "System Architecture",
        "topic": "Networking",
        "difficulty": "EASY",
        "correct_answer": "A forward proxy acts on behalf of internal clients reaching out to the internet; a reverse proxy acts on behalf of backend servers receiving traffic from the internet.",
        "options": [
            "A forward proxy only supports HTTP; a reverse proxy only supports FTP.",
            "A forward proxy acts on behalf of internal clients reaching out to the internet; a reverse proxy acts on behalf of backend servers receiving traffic from the internet.",
            "Reverse proxies are installed inside client operating systems.",
            "There is no difference; they are exact synonyms."
        ],
        "explanation": "Forward proxies protect and filter client outbound requests (e.g. enterprise firewalls). Reverse proxies route, balance, and terminate SSL for server backends."
    }
]

# Generate remaining 30 multi-disciplinary questions programmatically to reach 100 total
ADDITIONAL_TOPICS = [
    ("Zero Trust Architecture", "Security", "Never trust, always verify: every access request is authenticated, authorized, and encrypted regardless of network perimeter location."),
    ("Asymmetric Cryptography Key Exchange", "Security", "Diffie-Hellman allows two parties to establish a shared secret over an insecure channel without transmitting the secret itself."),
    ("Database Normalization 3NF", "Databases", "A table is in Third Normal Form (3NF) if it is in 2NF and has no transitive functional dependencies."),
    ("Two-Phase Commit (2PC) Blocking", "Distributed Systems", "2PC is a blocking protocol: if the coordinator crashes during the prepare phase, cohort nodes remain locked indefinitely."),
    ("Consistent Hashing Ring", "Distributed Systems", "Consistent hashing maps nodes and keys to a ring, minimizing key redistribution to K/N keys when nodes join or leave."),
    ("API Rate Limiting Token Bucket", "API Design", "Token bucket allows controlled bursts up to bucket capacity while enforcing a constant steady-state replenishment rate."),
    ("Message Broker Dead Letter Queue (DLQ)", "Messaging", "A DLQ isolates poison messages that fail repeatedly after max retry attempts, preventing queue processing head-of-line blocking."),
    ("Database Isolation Level Phantom Reads", "Databases", "Phantom reads occur when a transaction re-executes a range query and discovers newly inserted rows committed by another transaction."),
    ("Zero-Copy I/O with sendfile()", "Systems Programming", "sendfile() transfers data directly between kernel file descriptors, bypassing user-space memory buffer copies."),
    ("Chaos Engineering GameDay", "Reliability", "Chaos engineering injects deliberate turbulent conditions (killing nodes, latency) to uncover system resilience flaws before outages occur."),
    ("Data Warehouse Star vs Snowflake Schema", "Data Warehousing", "Star schema denormalizes dimensions into single tables for query speed; snowflake normalizes dimensions into multiple related tables."),
    ("Serverless Cold Start Latency", "Cloud Architecture", "Cold starts occur when a cloud provider spins up a new container instance and runtime environment for an idle function invocation."),
    ("Domain-Driven Design (DDD) Bounded Context", "Software Architecture", "A Bounded Context defines the explicit boundary within which a specific domain model and ubiquitous language applies."),
    ("OAuth2 Authorization Code Grant with PKCE", "Security", "Proof Key for Code Exchange (PKCE) prevents authorization code interception attacks on public clients without client secrets."),
    ("Database Sharding Key Selection", "Database Architecture", "A good shard key distributes data and query volume uniformly across nodes, avoiding hot partitions."),
    ("gRPC over Protocol Buffers", "API Design", "gRPC provides strongly-typed binary serialization, bidirectional streaming, and low latency over HTTP/2 transport."),
    ("Hexagonal (Ports and Adapters) Architecture", "Software Architecture", "Isolates core business domain logic from external dependencies (databases, web APIs) via interfaces (ports) and implementations (adapters)."),
    ("Data Mesh Decentralized Governance", "Data Architecture", "Data Mesh treats data as a product owned by decentralized domain teams rather than a central monolithic data lake."),
    ("Feature Flags Dynamic Rollout", "DevOps", "Feature flags allow decoupling code deployment from feature release, enabling instant kill-switches and canary rollouts."),
    ("Row-Level Security (RLS) in Postgres", "Security", "RLS enforces authorization policies at the database layer, filtering rows visible to queries based on current user context."),
    ("Distributed Tracing Span vs Trace", "Observability", "A Trace represents an end-to-end transaction journey; a Span represents an individual timed unit of work within that trace."),
    ("Database Pessimistic vs Optimistic Locking", "Databases", "Optimistic locking checks for version conflicts at commit time; pessimistic locking holds database locks for the duration of the transaction."),
    ("Micro-Frontends Module Federation", "Frontend Architecture", "Webpack Module Federation allows separate frontend applications to dynamically load remote code at runtime without monolith builds."),
    ("Garbage Collection Stop-The-World Pauses", "Runtime Systems", "Stop-the-world pauses halt all application threads while the garbage collector traces object references and compacts memory."),
    ("Database Index Selectivity", "Databases", "Index selectivity is the ratio of distinct values to total rows; high-selectivity columns benefit significantly more from indexing."),
    ("CORS Access-Control-Allow-Credentials", "Web Security", "Allows browsers to expose response data to JavaScript when requests include credentials like cookies or Authorization headers."),
    ("GraphQL N+1 Query Problem Solution", "API Design", "DataLoader batches and caches individual database lookups into a single batched query across graph resolvers."),
    ("TLS Certificate SNI (Server Name Indication)", "Networking", "SNI includes the requested hostname in the TLS ClientHello, allowing servers to host multiple SSL certificates on a single IP."),
    ("Distributed Cache Eviction LRU vs LFU", "Caching", "Least Recently Used (LRU) evicts the item accessed longest ago; Least Frequently Used (LFU) evicts the item with lowest total access count."),
    ("Infrastructure Drift Detection", "DevOps", "Drift detection identifies discrepancies between the intended state defined in IaC and the actual live cloud resource configuration.")
]

for title, topic, explanation in ADDITIONAL_TOPICS:
    TECHNICAL_QUESTIONS.append({
        "title": title,
        "question_text": f"In enterprise architecture and engineering practice, what is the core mechanism or definition of {title}?",
        "question_type": "MCQ",
        "category": AssessmentCategory.TECHNICAL_KNOWLEDGE.value if "Architecture" in topic or "Systems" in topic else AssessmentCategory.ADDITIONAL.value,
        "field": "Engineering Architecture",
        "topic": topic,
        "difficulty": "MEDIUM",
        "correct_answer": explanation,
        "options": [
            explanation,
            f"It is a legacy deprecated technique replaced by manual shell scripts.",
            f"It operates exclusively on physical tape drives without network connectivity.",
            f"It automatically restarts the operating system whenever memory exceeds 10%."
        ],
        "explanation": explanation
    })
