"""TRELLIS Technical Knowledge & Multi-Disciplinary Question Bank Fixtures (100 Questions).
60 Technical Knowledge questions (Full Stack, Cloud/DevOps, Data/AI, Core Systems) +
40 Multi-Disciplinary Architecture & Engineering questions.
Rebalanced keys: ~25% per position A/B/C/D.
"""

from app.schemas.category import AssessmentCategory

TECHNICAL_QUESTIONS = [   {   'category': 'Technical Knowledge',
        'correct_answer': 'OnPush checks the component only when its @Input references change, an event fires inside '
                          'it, or an async pipe emits.',
        'difficulty': 'MEDIUM',
        'explanation': 'OnPush optimizes rendering performance by skipping checks unless input object identities '
                       'change or internal async events trigger it.',
        'field': 'Web & Full Stack',
        'options': [   'OnPush checks the component only when its @Input references change, an event fires inside it, '
                       'or an async pipe emits.',
                       'OnPush completely disables the change detection cycle for the component and its children '
                       'permanently.',
                       'Default runs change detection only during browser page reload events.',
                       'Default requires manual invocation of ChangeDetectorRef.detectChanges() on every user '
                       'keystroke.'],
        'question_text': 'In Angular, what is the key difference between ChangeDetectionStrategy.Default and '
                         'ChangeDetectionStrategy.OnPush?',
        'question_type': 'MCQ',
        'title': 'Angular Change Detection Strategy',
        'topic': 'Frontend Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'DOM -> CSSOM -> Render Tree -> Layout (Reflow) -> Paint -> Composite',
        'difficulty': 'MEDIUM',
        'explanation': 'The browser builds the DOM and CSSOM concurrently, combines visible elements into the Render '
                       'Tree, calculates geometry in Layout, draws pixels in Paint, and layers them in Composite.',
        'field': 'Web & Full Stack',
        'options': [   'DOM -> Render Tree -> CSSOM -> Paint -> Layout -> Composite',
                       'DOM -> CSSOM -> Render Tree -> Layout (Reflow) -> Paint -> Composite',
                       'CSSOM -> DOM -> Layout -> Render Tree -> Composite -> Paint',
                       'Render Tree -> DOM -> CSSOM -> Composite -> Paint -> Layout'],
        'question_text': 'Which sequence correctly represents the browser Critical Rendering Path from HTML arrival to '
                         'pixels on screen?',
        'question_type': 'MCQ',
        'title': 'Browser Critical Rendering Path',
        'topic': 'Browser Internals'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Tokens in localStorage are accessible by any JavaScript running in the origin, making them '
                          'vulnerable to exfiltration via Cross-Site Scripting (XSS).',
        'difficulty': 'HARD',
        'explanation': 'LocalStorage is readable by third-party scripts injected through XSS. In-memory storage '
                       'combined with HttpOnly refresh cookies protects credentials from direct JavaScript '
                       'exfiltration.',
        'field': 'Web & Full Stack',
        'options': [   'LocalStorage cannot store strings longer than 128 characters.',
                       'In-memory tokens automatically sync across all browser tabs via the DOM without web workers.',
                       'Tokens in localStorage are accessible by any JavaScript running in the origin, making them '
                       'vulnerable to exfiltration via Cross-Site Scripting (XSS).',
                       'HTTP headers cannot transmit tokens stored in persistent client storage.'],
        'question_text': 'Why do security-hardened Single Page Applications store access tokens in memory (e.g., '
                         'framework signals/variables) instead of localStorage?',
        'question_type': 'MCQ',
        'title': 'JWT In-Memory vs LocalStorage Security',
        'topic': 'Web Security'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Head-of-Line (HoL) blocking at the application layer where requests had to wait for prior '
                          'responses on that socket.',
        'difficulty': 'MEDIUM',
        'explanation': 'HTTP/2 frames multiple interleaved bidirectional streams over one TCP connection, removing '
                       'HTTP/1.1 pipelining HoL blocking.',
        'field': 'Web & Full Stack',
        'options': [   'DNS lookup latency for secondary domains.',
                       'TLS handshake certificate expiration verification.',
                       'The 1500-byte Maximum Transmission Unit (MTU) limit on Ethernet networks.',
                       'Head-of-Line (HoL) blocking at the application layer where requests had to wait for prior '
                       'responses on that socket.'],
        'question_text': 'What fundamental TCP bottleneck in HTTP/1.1 is resolved by HTTP/2 multiplexing over a single '
                         'connection?',
        'question_type': 'MCQ',
        'title': 'HTTP/2 Multiplexing Benefits',
        'topic': 'Networking'},
    {   'category': 'Technical Knowledge',
        'correct_answer': "Sending a Content-Type header of 'application/json' or custom authorization headers.",
        'difficulty': 'MEDIUM',
        'explanation': 'Requests with Content-Type application/json or non-simple headers (like Authorization) are not '
                       "'simple requests' and require a preflight check.",
        'field': 'Web & Full Stack',
        'options': [   "Sending a Content-Type header of 'application/json' or custom authorization headers.",
                       'A standard GET request with Accept: text/html and no custom headers.',
                       'A standard POST request sending form-urlencoded data with standard simple headers.',
                       'A HEAD request navigating within the exact same origin.'],
        'question_text': 'Which HTTP request condition triggers a CORS preflight (OPTIONS) request from a web browser?',
        'question_type': 'MCQ',
        'title': 'CORS Preflight Trigger Conditions',
        'topic': 'Web Security'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'opacity: 0.99 (or any value less than 1)',
        'difficulty': 'MEDIUM',
        'explanation': 'Setting opacity < 1, transform, filter, or will-change creates a new stacking context in '
                       'modern browsers.',
        'field': 'Web & Full Stack',
        'options': [   'display: inline-block',
                       'opacity: 0.99 (or any value less than 1)',
                       'margin: auto',
                       'border: 1px solid red'],
        'question_text': 'Which CSS declaration creates a new stacking context without requiring position: relative or '
                         'absolute?',
        'question_type': 'MCQ',
        'title': 'CSS Stacking Context Creation',
        'topic': 'Frontend Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'A union of object types that all share a common literal property used as an exact '
                          'discriminant tag.',
        'difficulty': 'MEDIUM',
        'explanation': 'Discriminated unions enable narrowing in switch/if statements via a shared literal tag like '
                       "'kind' or 'type'.",
        'field': 'Web & Full Stack',
        'options': [   'A union type that only accepts primitive numeric constants.',
                       'A class inheritance tree utilizing private abstract constructors.',
                       'A union of object types that all share a common literal property used as an exact discriminant '
                       'tag.',
                       'A tuple type containing variable generic length arguments.'],
        'question_text': "In TypeScript, what characterizes a 'Discriminated Union' pattern?",
        'question_type': 'MCQ',
        'title': 'TypeScript Discriminated Unions',
        'topic': 'TypeScript'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Updates create a new tuple version with xmin/xmax transaction visibility IDs rather than '
                          'overwriting data in-place.',
        'difficulty': 'HARD',
        'explanation': 'PostgreSQL maintains multiple row versions with xmin/xmax timestamps, enabling readers to see '
                       'consistent snapshots without read locks.',
        'field': 'Web & Full Stack',
        'options': [   'Postgres acquires table-level exclusive locks on every write transaction.',
                       'All writes are queued into a Redis cache until all readers finish executing.',
                       'Write operations spawn separate temporary SQLite databases on disk.',
                       'Updates create a new tuple version with xmin/xmax transaction visibility IDs rather than '
                       'overwriting data in-place.'],
        'question_text': 'How does PostgreSQL Multi-Version Concurrency Control (MVCC) ensure read queries do not '
                         'block write queries?',
        'question_type': 'MCQ',
        'title': 'PostgreSQL MVCC Mechanism',
        'topic': 'Databases'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Per-request: created at request start, shared across dependencies in that request, and '
                          'closed in the yield teardown block.',
        'difficulty': 'MEDIUM',
        'explanation': 'Dependencies using yield execute setup before the route handler and teardown (closing the '
                       'session) immediately after response generation.',
        'field': 'Web & Full Stack',
        'options': [   'Per-request: created at request start, shared across dependencies in that request, and closed '
                       'in the yield teardown block.',
                       'Singleton: created once at server startup and shared globally across all threads and requests.',
                       'Per-query: recreated before every individual SQL statement execution.',
                       'Process-level: cached indefinitely until garbage collected.'],
        'question_text': "When using FastAPI's Depends(get_db) in a route handler, what is the default lifecycle of "
                         'the injected database session?',
        'question_type': 'MCQ',
        'title': 'FastAPI Dependency Injection Scope',
        'topic': 'Backend Frameworks'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'GET, HEAD, PUT, DELETE, OPTIONS, TRACE',
        'difficulty': 'EASY',
        'explanation': 'An idempotent method produces the same intended effect on the server state regardless of '
                       'whether it is executed 1 time or N times.',
        'field': 'Web & Full Stack',
        'options': [   'POST, PUT, PATCH, DELETE',
                       'GET, HEAD, PUT, DELETE, OPTIONS, TRACE',
                       'POST, GET, OPTIONS, CONNECT',
                       'PUT, POST, PATCH, OPTIONS'],
        'question_text': 'Which set of HTTP methods are formally defined as idempotent according to RFC 9110?',
        'question_type': 'MCQ',
        'title': 'Idempotent HTTP Methods',
        'topic': 'API Design'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'B-Trees efficiently support range scans (BETWEEN, <, >), sorting (ORDER BY), and prefix '
                          'matching, while Hash indexes only support exact equality.',
        'difficulty': 'MEDIUM',
        'explanation': 'B-Trees keep data sorted, allowing logarithmic lookup, range queries, and ordered traversals, '
                       'unlike unordered hash buckets.',
        'field': 'Web & Full Stack',
        'options': [   'Hash indexes require 100x more memory than B-Trees.',
                       'Hash indexes cannot be created on varchar columns.',
                       'B-Trees efficiently support range scans (BETWEEN, <, >), sorting (ORDER BY), and prefix '
                       'matching, while Hash indexes only support exact equality.',
                       'B-Trees guarantee zero disk reads for all lookup queries.'],
        'question_text': 'Why are B-Tree indexes preferred over Hash indexes as the default index structure in '
                         'relational databases?',
        'question_type': 'MCQ',
        'title': 'B-Tree vs Hash Index',
        'topic': 'Databases'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'When communication is strictly server-to-client (unidirectional), running over standard '
                          'HTTP with native browser auto-reconnection and HTTP/2 multiplexing.',
        'difficulty': 'MEDIUM',
        'explanation': 'SSE is lightweight, operates over standard HTTP/HTTPS, supports HTTP/2 multiplexing, and '
                       'includes automatic reconnection and event IDs natively.',
        'field': 'Web & Full Stack',
        'options': [   'When high-frequency binary peer-to-peer audio and video transmission is required.',
                       'When the server does not support any HTTP protocols above HTTP/1.0.',
                       'When the client needs to stream raw binary byte arrays back to the server at 60fps.',
                       'When communication is strictly server-to-client (unidirectional), running over standard HTTP '
                       'with native browser auto-reconnection and HTTP/2 multiplexing.'],
        'question_text': 'When should Server-Sent Events (SSE) be chosen over WebSockets for real-time frontend '
                         'streaming?',
        'question_type': 'MCQ',
        'title': 'WebSockets vs Server-Sent Events (SSE)',
        'topic': 'Networking'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'API request latency skyrockets as threads block waiting for connections, eventually '
                          'triggering connection checkout timeouts (503 / 504 errors).',
        'difficulty': 'HARD',
        'explanation': 'When all pool connections are checked out, incoming queries queue until their acquisition '
                       'timeout expires, cascading latency spikes across the API.',
        'field': 'Web & Full Stack',
        'options': [   'API request latency skyrockets as threads block waiting for connections, eventually triggering '
                       'connection checkout timeouts (503 / 504 errors).',
                       'Database disk space immediately reaches 100% capacity.',
                       'The database server CPU immediately drops to 0% idle state.',
                       'Client browsers crash due to memory leaks.'],
        'question_text': 'What is the primary operational symptom of database connection pool exhaustion in a '
                         'high-concurrency microservice?',
        'question_type': 'MCQ',
        'title': 'Database Connection Pool Exhaustion',
        'topic': 'Backend Reliability'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'The database compiles the SQL query structure first; user inputs are bound strictly as data '
                          'values and cannot alter the SQL AST.',
        'difficulty': 'EASY',
        'explanation': 'Prepared statements parse the query plan before binding variables; data parameters are never '
                       'treated as executable SQL tokens.',
        'field': 'Web & Full Stack',
        'options': [   'User input is automatically converted to base64 before saving.',
                       'The database compiles the SQL query structure first; user inputs are bound strictly as data '
                       'values and cannot alter the SQL AST.',
                       'Special characters like quotes and semicolons are deleted by the database driver.',
                       'The query runs inside an isolated Docker container.'],
        'question_text': 'Why do parameterized queries (prepared statements) protect against SQL injection '
                         'vulnerabilities?',
        'question_type': 'MCQ',
        'title': 'SQL Injection in Parameterized Queries',
        'topic': 'Web Security'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Using a distributed lock (or mutex) so only one worker queries the database to recalculate '
                          'the key while others wait or serve stale data.',
        'difficulty': 'HARD',
        'explanation': 'Probabilistic early expiration (XFetch) or mutex locks ensure only one request regenerates the '
                       'cached entity upon expiration.',
        'field': 'Web & Full Stack',
        'options': [   'Setting the cache TTL to 0 seconds so data is never cached.',
                       'Increasing the database connection limit to 10,000 connections.',
                       'Using a distributed lock (or mutex) so only one worker queries the database to recalculate the '
                       'key while others wait or serve stale data.',
                       'Restarting the Redis cluster every hour.'],
        'question_text': "Which strategy effectively prevents a 'Cache Stampede' (Thundering Herd) when a hot cache "
                         'key expires?',
        'question_type': 'MCQ',
        'title': 'Redis Cache Stampede Mitigation',
        'topic': 'Caching'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Failing a readiness probe removes the Pod from Service endpoints (stops traffic); failing a '
                          'liveness probe restarts the container.',
        'difficulty': 'MEDIUM',
        'explanation': 'Liveness probes detect deadlocks and restart stuck containers. Readiness probes determine if a '
                       'healthy container is ready to accept user traffic.',
        'field': 'Cloud & DevOps',
        'options': [   'Failing a readiness probe reboots the underlying worker node; failing a liveness probe deletes '
                       'the deployment.',
                       'Readiness probes only check CPU usage; liveness probes only inspect HTTP status codes.',
                       'They are completely interchangeable aliases in Kubernetes v1.25+.',
                       'Failing a readiness probe removes the Pod from Service endpoints (stops traffic); failing a '
                       'liveness probe restarts the container.'],
        'question_text': 'What is the critical behavioral distinction between a Kubernetes Readiness Probe and a '
                         'Liveness Probe?',
        'question_type': 'MCQ',
        'title': 'Kubernetes Pod Readiness vs Liveness Probes',
        'topic': 'Container Orchestration'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Compilers, build tools, and source code are left in intermediate stages, yielding minimal, '
                          'hardened, lightweight production runtime images.',
        'difficulty': 'EASY',
        'explanation': 'Multi-stage builds copy only the compiled binary or dist files into a minimal base (e.g. '
                       'alpine or distroless), shrinking attack surface and size.',
        'field': 'Cloud & DevOps',
        'options': [   'Compilers, build tools, and source code are left in intermediate stages, yielding minimal, '
                       'hardened, lightweight production runtime images.',
                       'Images compile at least 10x faster due to distributed GPU rendering.',
                       'It allows a single container to run Windows and Linux kernels simultaneously.',
                       'Docker multi-stage builds eliminate the need for container registries.'],
        'question_text': 'What is the primary benefit of utilizing Docker multi-stage builds for compiled languages '
                         'like Go, Rust, or Java?',
        'question_type': 'MCQ',
        'title': 'Docker Multi-Stage Build Advantages',
        'topic': 'Containers'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'It prevents concurrent pipeline runs from acquiring write access to the state file '
                          'simultaneously, preventing state corruption.',
        'difficulty': 'MEDIUM',
        'explanation': 'State locking ensures that only one terraform apply execution can modify remote infrastructure '
                       'and state at any given moment.',
        'field': 'Cloud & DevOps',
        'options': [   'It encrypts passwords with hardware security keys.',
                       'It prevents concurrent pipeline runs from acquiring write access to the state file '
                       'simultaneously, preventing state corruption.',
                       'It automatically converts HCL syntax into Kubernetes YAML manifests.',
                       'It bills cloud resources to different departmental cost centers.'],
        'question_text': 'Why is remote state locking (e.g., using AWS DynamoDB with S3) essential in team-based '
                         'Terraform deployments?',
        'question_type': 'MCQ',
        'title': 'Terraform State Locking Purpose',
        'topic': 'Infrastructure as Code'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'The new release is fully deployed and verified on an idle identical environment (Green), '
                          'after which the router/load balancer instantly cuts over traffic from Blue to Green.',
        'difficulty': 'EASY',
        'explanation': 'Blue-Green maintains two identical environments; traffic switchover occurs at the load '
                       'balancer level once the new environment passes verification.',
        'field': 'Cloud & DevOps',
        'options': [   'All servers are stopped simultaneously for 30 seconds while the database updates.',
                       'Traffic is randomly split 50/50 between versions forever.',
                       'The new release is fully deployed and verified on an idle identical environment (Green), after '
                       'which the router/load balancer instantly cuts over traffic from Blue to Green.',
                       'Old servers are deleted before new servers are created.'],
        'question_text': 'In a Blue-Green deployment strategy, how is traffic transition handled to achieve zero '
                         'downtime?',
        'question_type': 'MCQ',
        'title': 'Zero-Downtime Blue-Green Deployment',
        'topic': 'CI/CD & Deployment'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Closed (normal operation), Open (fast fail without calling target), Half-Open (trial '
                          'requests to test recovery)',
        'difficulty': 'MEDIUM',
        'explanation': 'When errors exceed a threshold, the breaker opens to prevent cascading failures. After a '
                       'cooldown, half-open allows limited canary probes.',
        'field': 'Cloud & DevOps',
        'options': [   'Active, Inactive, Suspended',
                       'Green, Yellow, Red',
                       'Connected, Disconnected, Reconnecting',
                       'Closed (normal operation), Open (fast fail without calling target), Half-Open (trial requests '
                       'to test recovery)'],
        'question_text': 'What are the three canonical states of the Circuit Breaker pattern in distributed systems?',
        'question_type': 'MCQ',
        'title': 'Circuit Breaker Pattern States',
        'topic': 'Resilience Engineering'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'The monitoring server controls scrape frequency and pacing, can detect target downtime '
                          'immediately if an endpoint is unreachable, and avoids targets overwhelming the collector.',
        'difficulty': 'HARD',
        'explanation': 'Pulling allows the server to manage ingestion load and reliably detect target health without '
                       'being swamped by millions of uncoordinated push bursts.',
        'field': 'Cloud & DevOps',
        'options': [   'The monitoring server controls scrape frequency and pacing, can detect target downtime '
                       'immediately if an endpoint is unreachable, and avoids targets overwhelming the collector.',
                       'Pulling metrics requires zero network firewall ports to be open.',
                       'Push models are mathematically incapable of recording timestamps.',
                       'Pulling is required by the Linux kernel systemd service manager.'],
        'question_text': "Why does Prometheus primarily adopt a 'pull' model for gathering time-series metrics from "
                         'target services?',
        'question_type': 'MCQ',
        'title': 'Prometheus Pull vs Push Metric Scraping',
        'topic': 'Observability'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'desiredReplicas = ceil[currentReplicas * (currentMetricValue / targetMetricValue)]',
        'difficulty': 'MEDIUM',
        'explanation': 'The standard HPA scaling formula computes ratio = currentMetric / targetMetric and scales '
                       'current replicas proportionally.',
        'field': 'Cloud & DevOps',
        'options': [   'desiredReplicas = currentReplicas + 10 whenever CPU exceeds 50%',
                       'desiredReplicas = ceil[currentReplicas * (currentMetricValue / targetMetricValue)]',
                       'desiredReplicas = floor[targetMetricValue / currentReplicas]',
                       'desiredReplicas = currentReplicas * 2 on any network drop'],
        'question_text': 'How does Kubernetes Horizontal Pod Autoscaler (HPA) calculate desired replicas given a '
                         'target metric utilization?',
        'question_type': 'MCQ',
        'title': 'Horizontal Pod Autoscaler (HPA) Metric Evaluation',
        'topic': 'Container Orchestration'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Topic partitions are reassigned among active consumers; in eager rebalancing, all consumers '
                          'stop processing until assignment completes.',
        'difficulty': 'HARD',
        'explanation': 'Rebalancing redistributes partitions across available consumer instances. Cooperative Sticky '
                       'rebalancing mitigates stop-the-world pauses.',
        'field': 'Cloud & DevOps',
        'options': [   'Messages in the partitions are deleted and recreated from scratch.',
                       'The Kafka cluster shuts down leader brokers temporarily.',
                       'Topic partitions are reassigned among active consumers; in eager rebalancing, all consumers '
                       'stop processing until assignment completes.',
                       'The consumer group is converted to point-to-point RPC.'],
        'question_text': 'What happens during an Apache Kafka consumer group partition rebalance when a new consumer '
                         'joins?',
        'question_type': 'MCQ',
        'title': 'Kafka Partition Rebalancing Impact',
        'topic': 'Event Streaming'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'A tiny percentage of live user traffic (e.g. 5%) is routed to the new version to monitor '
                          'metrics and error rates before full progressive rollout.',
        'difficulty': 'EASY',
        'explanation': 'Canary deployments limit the blast radius of potential regressions by exposing new versions to '
                       'a small slice of real production traffic first.',
        'field': 'Cloud & DevOps',
        'options': [   'The application is rewritten in a new language and launched on separate hardware.',
                       'Testing is performed exclusively in a local developer sandbox without production traffic.',
                       'Deployments are only performed on weekends.',
                       'A tiny percentage of live user traffic (e.g. 5%) is routed to the new version to monitor '
                       'metrics and error rates before full progressive rollout.'],
        'question_text': 'What defines a Canary deployment strategy compared to standard rolling updates?',
        'question_type': 'MCQ',
        'title': 'Canary Deployment Routing',
        'topic': 'CI/CD & Deployment'},
    {   'category': 'Technical Knowledge',
        'correct_answer': '1 RTT (and 0-RTT for resumed sessions)',
        'difficulty': 'MEDIUM',
        'explanation': 'TLS 1.3 slashed the 2-RTT handshake of TLS 1.2 to 1-RTT by combining key share negotiation '
                       'into the ClientHello message.',
        'field': 'Cloud & DevOps',
        'options': [   '1 RTT (and 0-RTT for resumed sessions)',
                       '3 RTT',
                       '5 RTT',
                       'Zero RTT always on initial connection'],
        'question_text': 'How many round trips (RTT) are required for a full TLS 1.3 cryptographic handshake before '
                         'application data can be transmitted?',
        'question_type': 'MCQ',
        'title': 'TLS 1.3 Handshake Round Trips',
        'topic': 'Networking & Security'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'The Linux kernel Out-Of-Memory (OOM) killer terminates the process (OOMKilled, exit code '
                          '137).',
        'difficulty': 'MEDIUM',
        'explanation': 'Exceeding the hard memory limit triggers the kernel OOM killer, killing the offending process '
                       'with SIGKILL (128 + 9 = 137).',
        'field': 'Cloud & DevOps',
        'options': [   'The kernel automatically compresses RAM using zram without penalty.',
                       'The Linux kernel Out-Of-Memory (OOM) killer terminates the process (OOMKilled, exit code 137).',
                       'The container pauses execution and sleeps until memory frees up.',
                       'The system reboots immediately.'],
        'question_text': 'What occurs when a process inside a Docker container exceeds its configured cgroup '
                         'memory.max limit?',
        'question_type': 'MCQ',
        'title': 'Linux cgroups v2 Memory Limits',
        'topic': 'Containers & Linux'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'In environment variables.',
        'difficulty': 'EASY',
        'explanation': 'Twelve-Factor Factor III mandates strict separation of config from code, injecting '
                       'configuration as environment variables.',
        'field': 'Cloud & DevOps',
        'options': [   'Committed into git repository constants files.',
                       'Hardcoded inside compiled application binaries.',
                       'In environment variables.',
                       'Written into client-side browser cookies.'],
        'question_text': 'According to the Twelve-Factor App methodology, where must application configuration that '
                         'varies across deploys (staging, prod) be stored?',
        'question_type': 'MCQ',
        'title': 'Twelve-Factor App Config Principle',
        'topic': 'Software Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': "Via standardized W3C Trace Context HTTP headers ('traceparent' and 'tracestate').",
        'difficulty': 'HARD',
        'explanation': "W3C Trace Context defines the 'traceparent' header (version, trace-id, parent-id, trace-flags) "
                       'to correlate spans across services.',
        'field': 'Cloud & DevOps',
        'options': [   'Through database shared memory locks.',
                       'By embedding trace IDs into DNS TXT records.',
                       'Using CPU hardware interrupt registers.',
                       "Via standardized W3C Trace Context HTTP headers ('traceparent' and 'tracestate')."],
        'question_text': 'In distributed tracing with OpenTelemetry, how is trace context propagated across HTTP '
                         'network boundaries?',
        'question_type': 'MCQ',
        'title': 'OpenTelemetry Trace Context Propagation',
        'topic': 'Observability'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'When write throughput or dataset volume exceeds the capacity of a single primary database '
                          'node.',
        'difficulty': 'HARD',
        'explanation': 'Read replicas scale read queries horizontally, but all writes must still hit the single '
                       'primary. Sharding partitions writes and data across nodes.',
        'field': 'Cloud & DevOps',
        'options': [   'When write throughput or dataset volume exceeds the capacity of a single primary database '
                       'node.',
                       'When read traffic increases by 10%.',
                       'When SSL certificates need renewal.',
                       'When backups take longer than 5 minutes.'],
        'question_text': 'When should an enterprise architecture adopt database sharding instead of simply adding read '
                         'replicas?',
        'question_type': 'MCQ',
        'title': 'Database Read Replicas vs Sharding',
        'topic': 'Database Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Git is the single source of truth; an automated reconciler continuously synchronizes actual '
                          'cluster state to match the declared Git state.',
        'difficulty': 'MEDIUM',
        'explanation': 'GitOps uses Git as the declarative desired state; reconciliation controllers pull and enforce '
                       'changes, preventing configuration drift.',
        'field': 'Cloud & DevOps',
        'options': [   'All developers must SSH into production servers using Git credentials.',
                       'Git is the single source of truth; an automated reconciler continuously synchronizes actual '
                       'cluster state to match the declared Git state.',
                       'Every commit must be signed by at least 10 engineers.',
                       'Git repositories must be hosted on internal physical tapes.'],
        'question_text': 'What is the foundational principle of GitOps operational frameworks like ArgoCD or Flux?',
        'question_type': 'MCQ',
        'title': 'GitOps Core Invariant',
        'topic': 'GitOps'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Smaller chunks provide high semantic precision for vector retrieval but risk losing '
                          'surrounding context; larger chunks retain context but dilute semantic embeddings.',
        'difficulty': 'MEDIUM',
        'explanation': 'Fine-grained chunks pinpoint exact sentences without embedding noise, but need techniques like '
                       'parent-document retrieval to provide sufficient LLM context.',
        'field': 'Data & AI',
        'options': [   'Smaller chunks make LLM inference 100x slower; larger chunks crash vector databases.',
                       'Smaller chunks only work with English text; larger chunks work with any language.',
                       'Smaller chunks provide high semantic precision for vector retrieval but risk losing '
                       'surrounding context; larger chunks retain context but dilute semantic embeddings.',
                       'Chunk size has zero measurable effect on retrieval quality or context.'],
        'question_text': 'In Retrieval-Augmented Generation (RAG), what is the key trade-off when selecting smaller vs '
                         'larger text chunk sizes?',
        'question_type': 'MCQ',
        'title': 'RAG Chunking Trade-offs',
        'topic': 'RAG Systems'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'It measures the cosine of the angle between vectors, capturing directional semantic '
                          'orientation irrespective of vector magnitude.',
        'difficulty': 'MEDIUM',
        'explanation': 'Cosine similarity focuses on orientation in semantic space; for unit-normalized vectors, '
                       'cosine similarity equals the dot product.',
        'field': 'Data & AI',
        'options': [   'It computes the exact Euclidean distance between raw character strings.',
                       'It is the only mathematical function that can run on GPUs.',
                       'It sorts words in alphabetical dictionary order.',
                       'It measures the cosine of the angle between vectors, capturing directional semantic '
                       'orientation irrespective of vector magnitude.'],
        'question_text': 'Why is Cosine Similarity commonly used to compare normalized dense vector embeddings '
                         'produced by LLM embedding models?',
        'question_type': 'MCQ',
        'title': 'Vector Embedding Cosine Similarity',
        'topic': 'Vector Search'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'O(N^2) quadratic complexity due to computing attention weights between every pair of tokens '
                          'in the sequence.',
        'difficulty': 'HARD',
        'explanation': 'Computing the Q * K^T attention matrix produces an N x N matrix, scaling quadratically with '
                       'sequence length.',
        'field': 'Data & AI',
        'options': [   'O(N^2) quadratic complexity due to computing attention weights between every pair of tokens in '
                       'the sequence.',
                       'O(N) linear complexity',
                       'O(log N) logarithmic complexity',
                       'O(1) constant time complexity'],
        'question_text': 'What is the computational and memory complexity of standard Multi-Head Self-Attention with '
                         'respect to sequence length N?',
        'question_type': 'MCQ',
        'title': 'Transformer Self-Attention Complexity',
        'topic': 'Deep Learning'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'It freezes pre-trained model weights and injects trainable rank-decomposition matrices (A '
                          'and B where d x r and r x k, r << d) into attention layers.',
        'difficulty': 'HARD',
        'explanation': 'By decomposing weight updates delta W into low-rank matrices A and B (rank r << d), LoRA '
                       'reduces trainable parameters by >99% while preserving performance.',
        'field': 'Data & AI',
        'options': [   'It removes 90% of model layers and trains only the output softmax.',
                       'It freezes pre-trained model weights and injects trainable rank-decomposition matrices (A and '
                       'B where d x r and r x k, r << d) into attention layers.',
                       'It converts floating point 32 weights into 1-bit binary booleans.',
                       'It trains a separate external heuristic regex engine.'],
        'question_text': 'How does LoRA achieve parameter-efficient fine-tuning (PEFT) without fine-tuning all model '
                         'weights?',
        'question_type': 'MCQ',
        'title': 'LoRA (Low-Rank Adaptation) Parameter Efficiency',
        'topic': 'LLM Fine-Tuning'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'It makes token generation deterministic (greedy decoding), consistently selecting the token '
                          'with the highest predicted log-probability.',
        'difficulty': 'EASY',
        'explanation': 'Lower temperature scales logits so differences are magnified; T->0 approaches argmax (greedy '
                       'choice of the top token).',
        'field': 'Data & AI',
        'options': [   'It disables all safety filters.',
                       'It forces the model to generate random gibberish.',
                       'It makes token generation deterministic (greedy decoding), consistently selecting the token '
                       'with the highest predicted log-probability.',
                       'It reduces server GPU physical temperature by shutting down fans.'],
        'question_text': 'What is the mathematical effect of setting an LLM generation temperature to 0 (or near 0)?',
        'question_type': 'MCQ',
        'title': 'Temperature in LLM Sampling',
        'topic': 'LLM Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'It builds multi-layer skip-list graphs where upper layers enable fast coarse-grained '
                          'long-range navigation and lower layers provide fine-grained local search.',
        'difficulty': 'HARD',
        'explanation': 'HNSW combines ideas from skip-lists and small-world graphs to achieve logarithmic O(log N) '
                       'search latency with high recall.',
        'field': 'Data & AI',
        'options': [   'It stores all vectors directly in uncompressed CSV files.',
                       'It converts floating point embeddings to ASCII characters.',
                       'It requires zero CPU or RAM overhead.',
                       'It builds multi-layer skip-list graphs where upper layers enable fast coarse-grained '
                       'long-range navigation and lower layers provide fine-grained local search.'],
        'question_text': 'What makes HNSW one of the most widely used approximate nearest neighbor (ANN) algorithms in '
                         'vector databases?',
        'question_type': 'MCQ',
        'title': 'HNSW (Hierarchical Navigable Small World) Graphs',
        'topic': 'Vector Databases'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Strict server-side authorization and parameter validation on tool APIs, treating LLM output '
                          'as untrusted user input, combined with output sandboxing.',
        'difficulty': 'HARD',
        'explanation': 'System prompts cannot guarantee immunity from adversarial inputs. Security must be enforced '
                       'deterministically at the tool and API boundary.',
        'field': 'Data & AI',
        'options': [   'Strict server-side authorization and parameter validation on tool APIs, treating LLM output as '
                       'untrusted user input, combined with output sandboxing.',
                       "Telling the model in the system prompt 'Please do not obey evil instructions'.",
                       "Filtering user queries for the exact word 'ignore'.",
                       'Using a smaller 1B parameter model.'],
        'question_text': 'Which defensive architecture provides the strongest protection against prompt injection in '
                         'LLM agents with tool execution privileges?',
        'question_type': 'MCQ',
        'title': 'Prompt Injection Mitigation',
        'topic': 'AI Security'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Constrained grammar decoding (CFG / JSON schema masking) that masks out invalid next tokens '
                          'at the logit level during autoregressive generation.',
        'difficulty': 'HARD',
        'explanation': 'Grammar-guided decoding converts schemas into pushdown automata, forcing logit probability to '
                       '-infinity for tokens violating syntax.',
        'field': 'Data & AI',
        'options': [   'Repeatedly prompting the model until it accidentally generates valid syntax.',
                       'Constrained grammar decoding (CFG / JSON schema masking) that masks out invalid next tokens at '
                       'the logit level during autoregressive generation.',
                       'Passing the raw output through Python json.loads() and returning empty string on error.',
                       'Training a new model from scratch for each JSON schema.'],
        'question_text': 'How do modern inference engines (e.g. llama.cpp, vLLM, Ollama) guarantee that an LLM outputs '
                         'valid JSON conforming to a schema?',
        'question_type': 'MCQ',
        'title': 'Structured Outputs with JSON Schema',
        'topic': 'Inference Engineering'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Lambda maintains separate batch and real-time stream processing pipelines; Kappa unifies '
                          'processing into a single stream processing pipeline.',
        'difficulty': 'MEDIUM',
        'explanation': 'Kappa avoids dual-codebase maintenance by treating all data as an append-only event stream '
                       'replayed through one stream engine.',
        'field': 'Data & AI',
        'options': [   'Lambda only uses AWS Lambda; Kappa only runs on Kubernetes.',
                       'Lambda cannot handle JSON data; Kappa cannot handle SQL queries.',
                       'Lambda maintains separate batch and real-time stream processing pipelines; Kappa unifies '
                       'processing into a single stream processing pipeline.',
                       'There is no difference; they are synonymous branding terms.'],
        'question_text': 'What is the key architectural difference between a Lambda Architecture and a Kappa '
                         'Architecture in big data processing?',
        'question_type': 'MCQ',
        'title': 'Data Pipeline Lambda vs Kappa Architecture',
        'topic': 'Data Engineering'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Columnar layout stores data of the same type together, enabling high compression ratios and '
                          'allowing queries to read only the specific columns requested.',
        'difficulty': 'MEDIUM',
        'explanation': 'OLAP queries aggregate specific columns; Parquet skips irrelevant columns on disk and '
                       'compresses homogeneous column data via run-length and dictionary encoding.',
        'field': 'Data & AI',
        'options': [   'It loads the entire dataset into browser localStorage.',
                       'It compiles SQL queries directly into C++ machine code.',
                       'It stores records in plain uncompressed text lines like CSV.',
                       'Columnar layout stores data of the same type together, enabling high compression ratios and '
                       'allowing queries to read only the specific columns requested.'],
        'question_text': 'Why does Apache Parquet provide dramatic query performance and compression advantages for '
                         'analytical SQL workloads (OLAP)?',
        'question_type': 'MCQ',
        'title': 'Parquet Columnar Storage Efficiency',
        'topic': 'Data Warehousing'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Overfitting (the model memorized training noise instead of generalizing).',
        'difficulty': 'EASY',
        'explanation': 'Overfitting occurs when a complex model fits noise in training data, resulting in poor '
                       'out-of-sample generalization.',
        'field': 'Data & AI',
        'options': [   'Overfitting (the model memorized training noise instead of generalizing).',
                       'Underfitting (the model is too simple to capture patterns).',
                       'Optimal Bayesian convergence.',
                       'Data leakage from the test set.'],
        'question_text': 'In supervised machine learning, high variance and near-zero training error accompanied by '
                         'high validation error indicates:',
        'question_type': 'MCQ',
        'title': 'Overfitting vs Underfitting Bias-Variance',
        'topic': 'Machine Learning'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Features with larger numerical scales would disproportionately dominate Euclidean distance '
                          'calculations regardless of relative importance.',
        'difficulty': 'EASY',
        'explanation': "Distance calculations assume uniform scales; an unscaled feature like 'Salary' ($100k) would "
                       "completely drown out 'Years of Experience' (5).",
        'field': 'Data & AI',
        'options': [   'K-Means cannot compute distances on floating-point numbers.',
                       'Features with larger numerical scales would disproportionately dominate Euclidean distance '
                       'calculations regardless of relative importance.',
                       'Standardization prevents integer overflow in Python.',
                       'It reduces the dataset row count.'],
        'question_text': 'Why is feature normalization/standardization (e.g. StandardScaler) crucial before running '
                         'K-Means clustering or KNN?',
        'question_type': 'MCQ',
        'title': 'Feature Scaling in Distance-Based Algorithms',
        'topic': 'Machine Learning'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Data drift is a shift in the distribution of input features P(X); concept drift is a change '
                          'in the relationship between input features and target labels P(Y|X).',
        'difficulty': 'HARD',
        'explanation': 'In concept drift, what a given feature means changes over time (e.g. consumer purchasing '
                       'behavior changes post-pandemic).',
        'field': 'Data & AI',
        'options': [   'Data drift affects only image models; concept drift affects only text models.',
                       'Data drift occurs during training; concept drift occurs during testing.',
                       'Data drift is a shift in the distribution of input features P(X); concept drift is a change in '
                       'the relationship between input features and target labels P(Y|X).',
                       'Concept drift is a hardware failure in GPU memory.'],
        'question_text': "In production machine learning systems, what distinguishes 'Concept Drift' from 'Data "
                         "(Covariate) Drift'?",
        'question_type': 'MCQ',
        'title': 'Data Drift vs Concept Drift',
        'topic': 'MLOps'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Memory footprint and bandwidth requirements are reduced by ~75% enabling execution on '
                          'smaller hardware, with minor potential degradation in perplexity.',
        'difficulty': 'MEDIUM',
        'explanation': 'Quantization drastically cuts memory and memory-bus bottlenecks with negligible quality loss '
                       'on modern techniques like AWQ/GGUF.',
        'field': 'Data & AI',
        'options': [   'Inference takes 10x more VRAM but guarantees 100% mathematical accuracy.',
                       'The model can no longer output punctuation or numbers.',
                       'Context window length is reduced to 16 tokens.',
                       'Memory footprint and bandwidth requirements are reduced by ~75% enabling execution on smaller '
                       'hardware, with minor potential degradation in perplexity.'],
        'question_text': 'What is the primary trade-off when quantizing a 16-bit floating point LLM down to 4-bit '
                         'integer representation (INT4)?',
        'question_type': 'MCQ',
        'title': 'Quantization (GGUF / AWQ / bitsandbytes)',
        'topic': 'Model Optimization'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'When joining a large DataFrame with a small dimension table; copying the small table to all '
                          'worker nodes eliminates expensive network shuffle of the large table.',
        'difficulty': 'MEDIUM',
        'explanation': 'Broadcasting the small table avoids a SortMergeJoin shuffle, allowing workers to join local '
                       'partitions directly in memory.',
        'field': 'Data & AI',
        'options': [   'When joining a large DataFrame with a small dimension table; copying the small table to all '
                       'worker nodes eliminates expensive network shuffle of the large table.',
                       'When joining two multi-terabyte tables together.',
                       'When running queries on a single-node laptop without a network.',
                       'When writing output to local text files.'],
        'question_text': 'When is a Broadcast Hash Join (Map-Side Join) utilized in Apache Spark, and why is it highly '
                         'performant?',
        'question_type': 'MCQ',
        'title': 'Spark Broadcast Joins',
        'topic': 'Distributed Computing'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'A program accesses a virtual memory address whose corresponding page is not currently '
                          'mapped to physical RAM (e.g., swapped out or demand-paged).',
        'difficulty': 'MEDIUM',
        'explanation': 'When the MMU encounters a page table entry with valid bit 0, a hardware trap triggers the OS '
                       'page fault handler to load the page into RAM.',
        'field': 'Core Systems',
        'options': [   'The program enters an infinite recursion loop.',
                       'A program accesses a virtual memory address whose corresponding page is not currently mapped '
                       'to physical RAM (e.g., swapped out or demand-paged).',
                       'The hard disk sector containing the kernel binary is physically damaged.',
                       'A web browser fails to load an HTML page over HTTP.'],
        'question_text': "What triggers a Page Fault in an operating system's virtual memory subsystem?",
        'question_type': 'MCQ',
        'title': 'Virtual Memory and Page Faults',
        'topic': 'Operating Systems'},
    {   'category': 'Technical Knowledge',
        'correct_answer': "Via a software interrupt or specialized system call instruction (e.g. 'syscall' on x86-64), "
                          'which switches CPU privilege rings.',
        'difficulty': 'MEDIUM',
        'explanation': 'Syscall instructions transition CPU privilege from Ring 3 (user) to Ring 0 (kernel) via '
                       'well-defined entry point handlers.',
        'field': 'Core Systems',
        'options': [   'By directly modifying the kernel code segment pointer in memory.',
                       'By spawning a background thread in Python.',
                       "Via a software interrupt or specialized system call instruction (e.g. 'syscall' on x86-64), "
                       'which switches CPU privilege rings.',
                       'By writing raw bytes to physical memory address 0x00000000.'],
        'question_text': 'How does an unprivileged user process transition CPU execution into kernel mode to perform '
                         'disk I/O?',
        'question_type': 'MCQ',
        'title': 'User Space vs Kernel Space Transition',
        'topic': 'Operating Systems'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'The execution call stack and CPU register state (including program counter).',
        'difficulty': 'EASY',
        'explanation': 'Threads share heap, code, globals, and file descriptors, but each thread maintains its own '
                       'private call stack and register set.',
        'field': 'Core Systems',
        'options': [   'The global heap memory.',
                       'The initialized data segment (.data).',
                       'The open file descriptor table.',
                       'The execution call stack and CPU register state (including program counter).'],
        'question_text': 'Which memory component is unique to each individual thread within a multi-threaded process?',
        'question_type': 'MCQ',
        'title': 'Thread vs Process Memory Layout',
        'topic': 'Concurrency'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait',
        'difficulty': 'HARD',
        'explanation': 'Breaking any one of the four Coffman conditions mathematically prevents deadlocks from '
                       'forming.',
        'field': 'Core Systems',
        'options': [   'Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait',
                       'Starvation, Thrashing, Livelock, Race Condition',
                       'Read Lock, Write Lock, Shared Lock, Exclusive Lock',
                       'Paging, Segmentation, Swapping, Fragmentation'],
        'question_text': 'Which set represents the four Coffman conditions all required simultaneously for a system '
                         'deadlock to occur?',
        'question_type': 'MCQ',
        'title': 'Deadlock Necessary Conditions',
        'topic': 'Operating Systems'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'epoll maintains a persistent kernel-space interest list (red-black tree) and returns an '
                          'event list containing only active sockets, avoiding linear scans.',
        'difficulty': 'HARD',
        'explanation': 'select/poll copies the entire file descriptor set to kernel on every call and loops over all N '
                       'sockets; epoll returns only triggered descriptors.',
        'field': 'Core Systems',
        'options': [   'epoll uses machine learning to predict which sockets will receive data.',
                       'epoll maintains a persistent kernel-space interest list (red-black tree) and returns an event '
                       'list containing only active sockets, avoiding linear scans.',
                       'select/poll can only handle UDP packets, whereas epoll handles TCP.',
                       'epoll bypasses the network interface card entirely.'],
        'question_text': 'Why is Linux epoll O(1) in scalability compared to the O(N) complexity of traditional '
                         'select/poll when handling 100,000 concurrent sockets?',
        'question_type': 'MCQ',
        'title': 'Epoll vs Select Scalability',
        'topic': 'I/O Multiplexing'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Threads on separate cores update distinct, independent variables that happen to reside on '
                          'the same 64-byte hardware cache line, causing constant cache invalidation.',
        'difficulty': 'HARD',
        'explanation': 'Because cache coherence protocols operate at the cache line granularity (usually 64 bytes), '
                       'updates to adjacent bytes invalidate the entire line across cores.',
        'field': 'Core Systems',
        'options': [   'Two processes sharing the same virtual memory page without synchronization.',
                       'A CPU instruction cache predicting the wrong branch.',
                       'Threads on separate cores update distinct, independent variables that happen to reside on the '
                       'same 64-byte hardware cache line, causing constant cache invalidation.',
                       'A thread reading an uninitialized global pointer.'],
        'question_text': "What is 'False Sharing' in high-performance multi-threaded C/C++ applications?",
        'question_type': 'MCQ',
        'title': 'CPU Cache Line False Sharing',
        'topic': 'Computer Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'It atomically checks if a memory location holds an expected value; if true, it updates it '
                          'to a new value and returns success, all in a single hardware cycle.',
        'difficulty': 'MEDIUM',
        'explanation': 'CAS is the fundamental primitive for lock-free data structures, guaranteeing atomicity without '
                       'OS context switches.',
        'field': 'Core Systems',
        'options': [   'It acquires an operating system mutex lock.',
                       'It swaps two CPU registers without touching memory.',
                       'It deletes a variable from RAM.',
                       'It atomically checks if a memory location holds an expected value; if true, it updates it to a '
                       'new value and returns success, all in a single hardware cycle.'],
        'question_text': 'What does an atomic Compare-And-Swap (CAS) instruction perform in lock-free programming?',
        'question_type': 'MCQ',
        'title': 'Atomic Compare-And-Swap (CAS)',
        'topic': 'Concurrency'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'RAID 5 offers higher usable capacity (N-1) but suffers a write penalty for parity '
                          'recalculation and long rebuild times; RAID 10 offers superior write IOPS and fast rebuilds '
                          'at 50% capacity.',
        'difficulty': 'MEDIUM',
        'explanation': 'RAID 5 requires read-modify-write parity computations. RAID 10 stripes mirrored pairs, '
                       'offering raw speed at the cost of disk space.',
        'field': 'Core Systems',
        'options': [   'RAID 5 offers higher usable capacity (N-1) but suffers a write penalty for parity '
                       'recalculation and long rebuild times; RAID 10 offers superior write IOPS and fast rebuilds at '
                       '50% capacity.',
                       'RAID 5 can survive all disks failing at once; RAID 10 cannot survive any disk failure.',
                       'RAID 10 is only supported on SSDs, not HDDs.',
                       'RAID 5 does not support data redundancy.'],
        'question_text': 'What is the primary operational trade-off between RAID 5 and RAID 10 (1+0)?',
        'question_type': 'MCQ',
        'title': 'RAID 5 vs RAID 10 Fault Tolerance',
        'topic': 'Storage Systems'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'fork() copies only the page tables with pages marked read-only; physical memory pages are '
                          'only duplicated when either process writes to a page.',
        'difficulty': 'MEDIUM',
        'explanation': 'Copy-On-Write defers memory duplication until modification, making process creation '
                       'near-instantaneous.',
        'field': 'Core Systems',
        'options': [   'fork() immediately compresses parent memory using gzip.',
                       'fork() copies only the page tables with pages marked read-only; physical memory pages are only '
                       'duplicated when either process writes to a page.',
                       'fork() runs only on ARM architecture, not x86.',
                       'Child processes never receive access to parent memory.'],
        'question_text': 'Why is the Linux fork() system call extremely fast even when the parent process consumes 32 '
                         'GB of memory?',
        'question_type': 'MCQ',
        'title': 'Copy-On-Write (COW) in Fork()',
        'topic': 'Operating Systems'},
    {   'category': 'Technical Knowledge',
        'correct_answer': '0x78, 0x56, 0x34, 0x12 (least significant byte at the lowest memory address)',
        'difficulty': 'EASY',
        'explanation': 'Little-endian architectures store the least significant byte (LSB) first in ascending memory '
                       'addresses.',
        'field': 'Core Systems',
        'options': [   '0x12, 0x34, 0x56, 0x78 (most significant byte at lowest address)',
                       '0x56, 0x78, 0x12, 0x34',
                       '0x78, 0x56, 0x34, 0x12 (least significant byte at the lowest memory address)',
                       '0x00, 0x12, 0x34, 0x56'],
        'question_text': 'How is the 32-bit hexadecimal value 0x12345678 stored in sequential memory addresses '
                         'starting at 0x00 on a Little-Endian system (x86-64)?',
        'question_type': 'MCQ',
        'title': 'Little-Endian vs Big-Endian Byte Order',
        'topic': 'Computer Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'The server encodes connection state into the initial SYN-ACK sequence number, avoiding '
                          'allocating memory in the SYN queue until a valid client ACK returns.',
        'difficulty': 'HARD',
        'explanation': 'SYN cookies eliminate half-open state allocation on the server by hashing client IP/port/MSS '
                       'into the sequence number.',
        'field': 'Core Systems',
        'options': [   'The server drops all incoming TCP packets permanently.',
                       'The server disconnects from the internet for 10 minutes.',
                       'The client sends its MAC address in the HTTP cookie header.',
                       'The server encodes connection state into the initial SYN-ACK sequence number, avoiding '
                       'allocating memory in the SYN queue until a valid client ACK returns.'],
        'question_text': 'How do SYN Cookies protect web servers against TCP SYN flood denial-of-service attacks?',
        'question_type': 'MCQ',
        'title': 'TCP Three-Way Handshake SYN Flooding',
        'topic': 'Networking & Security'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Unused objects remain reachable from active GC root references (e.g. static collections, '
                          'global registries, uncleared event listeners).',
        'difficulty': 'MEDIUM',
        'explanation': 'GC algorithms only collect objects that are unreachable from GC roots. Lingering references in '
                       'caches or static fields prevent reclamation.',
        'field': 'Core Systems',
        'options': [   'Unused objects remain reachable from active GC root references (e.g. static collections, '
                       'global registries, uncleared event listeners).',
                       'The CPU physical silicon registers degrade over time.',
                       'The language runs out of variable names.',
                       'Garbage collection cannot reclaim memory allocated in functions with more than 5 lines.'],
        'question_text': 'How can a memory leak occur in a language with automated garbage collection like Java, '
                         'Python, or Go?',
        'question_type': 'MCQ',
        'title': 'Memory Leak in Garbage Collected Languages',
        'topic': 'Memory Management'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'They are not async-signal-safe; interrupting a non-reentrant function already holding '
                          'internal mutexes causes deadlocks or heap corruption.',
        'difficulty': 'HARD',
        'explanation': 'Signal handlers can interrupt code at any arbitrary instruction. Calling non-reentrant '
                       'functions risks deadlocks if the interrupted thread was holding the malloc lock.',
        'field': 'Core Systems',
        'options': [   'Signal handlers execute in kernel space where C libraries do not exist.',
                       'They are not async-signal-safe; interrupting a non-reentrant function already holding internal '
                       'mutexes causes deadlocks or heap corruption.',
                       'POSIX signals cannot pass string parameters.',
                       'Signal handlers cannot consume more than 2 bytes of RAM.'],
        'question_text': 'Why is it unsafe to call functions like malloc() or printf() inside a POSIX signal handler?',
        'question_type': 'MCQ',
        'title': 'POSIX Signal Handling Restrictions',
        'topic': 'Systems Programming'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Branch prediction combined with speculative execution (and pipeline flush if the prediction '
                          'was incorrect).',
        'difficulty': 'MEDIUM',
        'explanation': 'CPUs use history tables to predict branch targets and speculatively execute instructions ahead '
                       'of time, discarding work if mispredicted.',
        'field': 'Core Systems',
        'options': [   'Software interpretation of binary code.',
                       'Clock speed throttling.',
                       'Branch prediction combined with speculative execution (and pipeline flush if the prediction '
                       'was incorrect).',
                       'Dynamic RAM refreshing.'],
        'question_text': 'What hardware mechanism allows modern CPUs to keep execution pipelines full before '
                         'conditional branches are resolved?',
        'question_type': 'MCQ',
        'title': 'Branch Predictor Speculative Execution',
        'topic': 'Computer Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'NAND flash must be erased in large blocks before individual pages can be rewritten, '
                          'requiring existing valid pages to be read, copied, and rewritten.',
        'difficulty': 'MEDIUM',
        'explanation': 'NAND flash cannot overwrite pages in place. Erasing an entire block requires garbage '
                       'collection cycles, writing more physical bytes than logically requested.',
        'field': 'Core Systems',
        'options': [   'Operating systems writing duplicate backup copies of every file.',
                       'Electricity voltage fluctuations expanding disk sectors.',
                       'USB cable impedance resistance.',
                       'NAND flash must be erased in large blocks before individual pages can be rewritten, requiring '
                       'existing valid pages to be read, copied, and rewritten.'],
        'question_text': 'What causes Write Amplification on Solid State Drives (SSDs)?',
        'question_type': 'MCQ',
        'title': 'SSD Write Amplification',
        'topic': 'Storage Systems'},
    {   'category': 'Additional',
        'correct_answer': 'Consistency (C) or Availability (A)',
        'difficulty': 'EASY',
        'explanation': 'During a network partition, a system can either return stale data/errors to remain available '
                       '(AP) or block requests to guarantee consistency (CP).',
        'field': 'System Architecture',
        'options': [   'Consistency (C) or Availability (A)',
                       'Performance or Reliability',
                       'Security or Usability',
                       'Throughput or Latency'],
        'question_text': 'In a distributed network experiencing a network partition (P), what does the CAP theorem '
                         'dictate a system must choose between?',
        'question_type': 'MCQ',
        'title': 'CAP Theorem Trade-Offs',
        'topic': 'Distributed Systems'},
    {   'category': 'Additional',
        'correct_answer': 'It receives votes from a strict majority (quorum: N/2 + 1) of the cluster nodes.',
        'difficulty': 'MEDIUM',
        'explanation': 'Raft guarantees safety by requiring a majority quorum for both leader election and log entry '
                       'commit.',
        'field': 'System Architecture',
        'options': [   'It has the lowest IP address in the cluster.',
                       'It receives votes from a strict majority (quorum: N/2 + 1) of the cluster nodes.',
                       'The node with the highest CPU clock speed is chosen.',
                       'It sends a broadcast message claiming leadership without a vote.'],
        'question_text': 'In the Raft consensus algorithm, how does a candidate node become the elected leader of a '
                         'term?',
        'question_type': 'MCQ',
        'title': 'Raft Consensus Leader Election',
        'topic': 'Distributed Consensus'},
    {   'category': 'Additional',
        'correct_answer': 'R + W > N (the read set and write set must overlap on at least one replica)',
        'difficulty': 'HARD',
        'explanation': 'When R + W > N, the Pigeonhole Principle ensures at least one node in the read quorum contains '
                       'the latest write version.',
        'field': 'System Architecture',
        'options': [   'R + W < N',
                       'R * W = N',
                       'R + W > N (the read set and write set must overlap on at least one replica)',
                       'R = W = 1'],
        'question_text': 'In a quorum-based distributed store (like Cassandra), what inequality between replicas N, '
                         'read quorum R, and write quorum W guarantees strong read-after-write consistency?',
        'question_type': 'MCQ',
        'title': 'Eventual Consistency in Dynamo-Style Databases',
        'topic': 'Distributed Storage'},
    {   'category': 'Additional',
        'correct_answer': 'LSM-trees write sequentially to an append-only commit log and in-memory MemTable, deferring '
                          'expensive sorting to background compaction.',
        'difficulty': 'HARD',
        'explanation': 'Sequential writes are orders of magnitude faster than random disk updates; LSM-trees convert '
                       'random writes into sequential appends.',
        'field': 'System Architecture',
        'options': [   'LSM-trees do not write data to disk.',
                       'B-trees can only store 10,000 records.',
                       'LSM-trees use GPU hardware registers.',
                       'LSM-trees write sequentially to an append-only commit log and in-memory MemTable, deferring '
                       'expensive sorting to background compaction.'],
        'question_text': 'Why do Log-Structured Merge-trees (LSM-trees) achieve substantially higher write throughput '
                         'than B-trees?',
        'question_type': 'MCQ',
        'title': 'LSM-Tree vs B-Tree Write Performance',
        'topic': 'Storage Engines'},
    {   'category': 'Additional',
        'correct_answer': 'Zero false negatives (if it says an element is absent, it is definitely absent), but false '
                          'positives are possible.',
        'difficulty': 'MEDIUM',
        'explanation': 'Bloom filters test set membership with zero false negatives, allowing databases to bypass disk '
                       'reads when a key definitely does not exist.',
        'field': 'System Architecture',
        'options': [   'Zero false negatives (if it says an element is absent, it is definitely absent), but false '
                       'positives are possible.',
                       'Zero false positives, but false negatives are possible.',
                       '100% deterministic accuracy for all queries.',
                       'It can store and return the original string data.'],
        'question_text': 'What is the probabilistic guarantee provided by a standard Bloom Filter?',
        'question_type': 'MCQ',
        'title': 'Bloom Filter False Positives',
        'topic': 'Data Structures'},
    {   'category': 'Additional',
        'correct_answer': 'Orchestration uses a centralized coordinator service to instruct participants; Choreography '
                          'relies on services publishing and reacting to domain events independently.',
        'difficulty': 'MEDIUM',
        'explanation': 'Orchestrators explicitly sequence calls and compensations; choreographers maintain decoupling '
                       'via pub/sub events.',
        'field': 'System Architecture',
        'options': [   'Orchestration uses two-phase commit (2PC); Choreography does not.',
                       'Orchestration uses a centralized coordinator service to instruct participants; Choreography '
                       'relies on services publishing and reacting to domain events independently.',
                       'Choreography is only for monolithic architectures.',
                       'Orchestration cannot perform compensating transactions.'],
        'question_text': 'In distributed microservices transactions, what distinguishes Saga Orchestration from Saga '
                         'Choreography?',
        'question_type': 'MCQ',
        'title': 'Saga Pattern Orchestration vs Choreography',
        'topic': 'Microservices Patterns'},
    {   'category': 'Additional',
        'correct_answer': 'The server caches the result of the initial request under the client UUID key; retries with '
                          'the same key return the cached charge result without re-processing.',
        'difficulty': 'MEDIUM',
        'explanation': 'Payment gateways record idempotency keys; duplicate submissions return the original '
                       'transaction receipt rather than executing a new debit.',
        'field': 'System Architecture',
        'options': [   'The client sends an encryption key that reverses bank transactions.',
                       "It cancels the customer's credit card.",
                       'The server caches the result of the initial request under the client UUID key; retries with '
                       'the same key return the cached charge result without re-processing.',
                       'It converts POST requests to GET requests.'],
        'question_text': 'How does an Idempotency-Key HTTP header ensure a customer is not charged twice during a '
                         'network timeout?',
        'question_type': 'MCQ',
        'title': 'Idempotency Keys in Payment APIs',
        'topic': 'API Design'},
    {   'category': 'Additional',
        'correct_answer': 'Modifications are written and flushed to durable log storage on disk before the dirty data '
                          'pages are written to data files.',
        'difficulty': 'MEDIUM',
        'explanation': 'WAL guarantees durability and crash recovery: if the server powers down before dirty pages '
                       'reach disk, the WAL is replayed on startup.',
        'field': 'System Architecture',
        'options': [   'It writes an audit log to a remote syslog server.',
                       'It verifies user login credentials against Active Directory.',
                       'It compresses tables during low-traffic night hours.',
                       'Modifications are written and flushed to durable log storage on disk before the dirty data '
                       'pages are written to data files.'],
        'question_text': 'What is the primary role of Write-Ahead Logging (WAL) in database transaction durability '
                         '(ACID)?',
        'question_type': 'MCQ',
        'title': 'Database WAL (Write-Ahead Logging)',
        'topic': 'Databases'},
    {   'category': 'Additional',
        'correct_answer': 'Each unique build produces a distinct URL, enabling infinite (1-year) immutable caching '
                          'while guaranteeing instant client updates when index.html changes.',
        'difficulty': 'EASY',
        'explanation': 'Cache-busting with content hashes allows static assets to be cached permanently '
                       '(`Cache-Control: immutable, max-age=31536000`), with zero stale asset bugs.',
        'field': 'System Architecture',
        'options': [   'Each unique build produces a distinct URL, enabling infinite (1-year) immutable caching while '
                       'guaranteeing instant client updates when index.html changes.',
                       'Asset hashing encrypts JavaScript so competitors cannot read it.',
                       'CDNs charge 10x more for unhashed filenames.',
                       'Browser engines refuse to run unhashed JavaScript files.'],
        'question_text': 'Why is asset hashing (e.g. main.a1b2c3d4.js) preferred over manual cache purging in frontend '
                         'production deployments?',
        'question_type': 'MCQ',
        'title': 'Content Delivery Network (CDN) Cache Invalidation',
        'topic': 'Web Infrastructure'},
    {   'category': 'Additional',
        'correct_answer': 'A forward proxy acts on behalf of internal clients reaching out to the internet; a reverse '
                          'proxy acts on behalf of backend servers receiving traffic from the internet.',
        'difficulty': 'EASY',
        'explanation': 'Forward proxies protect and filter client outbound requests (e.g. enterprise firewalls). '
                       'Reverse proxies route, balance, and terminate SSL for server backends.',
        'field': 'System Architecture',
        'options': [   'A forward proxy only supports HTTP; a reverse proxy only supports FTP.',
                       'A forward proxy acts on behalf of internal clients reaching out to the internet; a reverse '
                       'proxy acts on behalf of backend servers receiving traffic from the internet.',
                       'Reverse proxies are installed inside client operating systems.',
                       'There is no difference; they are exact synonyms.'],
        'question_text': 'What is the architectural difference between a Forward Proxy and a Reverse Proxy?',
        'question_type': 'MCQ',
        'title': 'Reverse Proxy vs Forward Proxy',
        'topic': 'Networking'},
    {   'category': 'Additional',
        'correct_answer': 'Never trust, always verify: every access request is authenticated, authorized, and '
                          'encrypted regardless of network perimeter location.',
        'difficulty': 'MEDIUM',
        'explanation': 'Never trust, always verify: every access request is authenticated, authorized, and encrypted '
                       'regardless of network perimeter location.',
        'field': 'Engineering Architecture',
        'options': [   'Trust all internal network traffic implicitly once authenticated through the perimeter VPN '
                       'gateway.',
                       'Rely exclusively on static subnet IP whitelisting to validate trust between containerized '
                       'microservices.',
                       'Never trust, always verify: every access request is authenticated, authorized, and encrypted '
                       'regardless of network perimeter location.',
                       'Disable mutual TLS between private cluster services to eliminate cryptographic handshake '
                       'overhead.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Zero Trust Architecture?',
        'question_type': 'MCQ',
        'title': 'Zero Trust Architecture',
        'topic': 'Security'},
    {   'category': 'Additional',
        'correct_answer': 'Diffie-Hellman allows two parties to establish a shared secret over an insecure channel '
                          'without transmitting the secret itself.',
        'difficulty': 'MEDIUM',
        'explanation': 'Diffie-Hellman allows two parties to establish a shared secret over an insecure channel '
                       'without transmitting the secret itself.',
        'field': 'Engineering Architecture',
        'options': [   'Transmits the server private key across the network encrypted with an ephemeral public '
                       'certificate.',
                       'Employs shared symmetric AES-256 keys hardcoded into client binaries during build time.',
                       'Requires a centralized certificate authority to generate and retain both session secret keys.',
                       'Diffie-Hellman allows two parties to establish a shared secret over an insecure channel '
                       'without transmitting the secret itself.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Asymmetric Cryptography Key Exchange?',
        'question_type': 'MCQ',
        'title': 'Asymmetric Cryptography Key Exchange',
        'topic': 'Security'},
    {   'category': 'Additional',
        'correct_answer': 'A table is in Third Normal Form (3NF) if it is in 2NF and has no transitive functional '
                          'dependencies.',
        'difficulty': 'MEDIUM',
        'explanation': 'A table is in Third Normal Form (3NF) if it is in 2NF and has no transitive functional '
                       'dependencies.',
        'field': 'Engineering Architecture',
        'options': [   'A table is in Third Normal Form (3NF) if it is in 2NF and has no transitive functional '
                       'dependencies.',
                       'A table is in 3NF if every column is a foreign key and no multi-valued attributes exist.',
                       'A table is in 3NF if non-prime attributes are partially dependent on a composite primary key.',
                       'A table is in 3NF if all relations have been pre-joined to eliminate foreign key constraints.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Database Normalization 3NF?',
        'question_type': 'MCQ',
        'title': 'Database Normalization 3NF',
        'topic': 'Databases'},
    {   'category': 'Technical Knowledge',
        'correct_answer': '2PC is a blocking protocol: if the coordinator crashes during the prepare phase, cohort '
                          'nodes remain locked indefinitely.',
        'difficulty': 'MEDIUM',
        'explanation': '2PC is a blocking protocol: if the coordinator crashes during the prepare phase, cohort nodes '
                       'remain locked indefinitely.',
        'field': 'Engineering Architecture',
        'options': [   '2PC is non-blocking: cohorts automatically elect a new coordinator via Raft if the primary '
                       'fails.',
                       '2PC is a blocking protocol: if the coordinator crashes during the prepare phase, cohort nodes '
                       'remain locked indefinitely.',
                       '2PC guarantees eventual consistency by executing commits asynchronously in background worker '
                       'threads.',
                       '2PC allows cohort nodes to unilaterally abort or commit if no message is received within '
                       '100ms.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Two-Phase Commit (2PC) Blocking?',
        'question_type': 'MCQ',
        'title': 'Two-Phase Commit (2PC) Blocking',
        'topic': 'Distributed Systems'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Consistent hashing maps nodes and keys to a ring, minimizing key redistribution to K/N keys '
                          'when nodes join or leave.',
        'difficulty': 'MEDIUM',
        'explanation': 'Consistent hashing maps nodes and keys to a ring, minimizing key redistribution to K/N keys '
                       'when nodes join or leave.',
        'field': 'Engineering Architecture',
        'options': [   'Consistent hashing uses a modulo hash table that remaps all keys whenever the server count '
                       'changes.',
                       'Consistent hashing distributes queries strictly round-robin without mapping keys to node '
                       'tokens.',
                       'Consistent hashing maps nodes and keys to a ring, minimizing key redistribution to K/N keys '
                       'when nodes join or leave.',
                       'Consistent hashing requires a centralized directory service to store the physical server '
                       'location of every key.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Consistent Hashing Ring?',
        'question_type': 'MCQ',
        'title': 'Consistent Hashing Ring',
        'topic': 'Distributed Systems'},
    {   'category': 'Additional',
        'correct_answer': 'Token bucket allows controlled bursts up to bucket capacity while enforcing a constant '
                          'steady-state replenishment rate.',
        'difficulty': 'MEDIUM',
        'explanation': 'Token bucket allows controlled bursts up to bucket capacity while enforcing a constant '
                       'steady-state replenishment rate.',
        'field': 'Engineering Architecture',
        'options': [   'Token bucket drops all requests once an arbitrary fixed threshold of active TCP sockets is '
                       'reached.',
                       'Token bucket counts total requests over a rolling 24-hour window, resetting the counter at '
                       'midnight.',
                       'Token bucket requires client IP addresses to acquire a distributed mutex before sending any '
                       'HTTP payload.',
                       'Token bucket allows controlled bursts up to bucket capacity while enforcing a constant '
                       'steady-state replenishment rate.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of API Rate Limiting Token Bucket?',
        'question_type': 'MCQ',
        'title': 'API Rate Limiting Token Bucket',
        'topic': 'API Design'},
    {   'category': 'Additional',
        'correct_answer': 'A DLQ isolates poison messages that fail repeatedly after max retry attempts, preventing '
                          'queue processing head-of-line blocking.',
        'difficulty': 'MEDIUM',
        'explanation': 'A DLQ isolates poison messages that fail repeatedly after max retry attempts, preventing queue '
                       'processing head-of-line blocking.',
        'field': 'Engineering Architecture',
        'options': [   'A DLQ isolates poison messages that fail repeatedly after max retry attempts, preventing queue '
                       'processing head-of-line blocking.',
                       'A DLQ automatically redelivers corrupt messages to consumers in an infinite retry loop until '
                       'acknowledged.',
                       'A DLQ drops poisoned messages permanently from memory without recording error payloads or '
                       'metadata.',
                       'A DLQ routes failed messages immediately to end-user browsers via WebSockets for manual user '
                       'remediation.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Message Broker Dead Letter Queue (DLQ)?',
        'question_type': 'MCQ',
        'title': 'Message Broker Dead Letter Queue (DLQ)',
        'topic': 'Messaging'},
    {   'category': 'Additional',
        'correct_answer': 'Phantom reads occur when a transaction re-executes a range query and discovers newly '
                          'inserted rows committed by another transaction.',
        'difficulty': 'MEDIUM',
        'explanation': 'Phantom reads occur when a transaction re-executes a range query and discovers newly inserted '
                       'rows committed by another transaction.',
        'field': 'Engineering Architecture',
        'options': [   'Phantom reads happen when an uncommitted dirty write is rolled back and overwritten by a '
                       'concurrent transaction.',
                       'Phantom reads occur when a transaction re-executes a range query and discovers newly inserted '
                       'rows committed by another transaction.',
                       'Phantom reads occur when two concurrent transactions update the same single row '
                       'simultaneously.',
                       'Phantom reads occur when a database index is rebuilt concurrently during an active sequential '
                       'table scan.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Database Isolation Level Phantom Reads?',
        'question_type': 'MCQ',
        'title': 'Database Isolation Level Phantom Reads',
        'topic': 'Databases'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'sendfile() transfers data directly between kernel file descriptors, bypassing user-space '
                          'memory buffer copies.',
        'difficulty': 'MEDIUM',
        'explanation': 'sendfile() transfers data directly between kernel file descriptors, bypassing user-space '
                       'memory buffer copies.',
        'field': 'Engineering Architecture',
        'options': [   'sendfile() forces all byte buffers to be copied twice through user-space memory for '
                       'inspection.',
                       'sendfile() utilizes CPU software rendering to compress file streams before socket '
                       'transmission.',
                       'sendfile() transfers data directly between kernel file descriptors, bypassing user-space '
                       'memory buffer copies.',
                       'sendfile() encrypts memory pages in RAM using asymmetric RSA keys before DMA transfer.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Zero-Copy I/O with sendfile()?',
        'question_type': 'MCQ',
        'title': 'Zero-Copy I/O with sendfile()',
        'topic': 'Systems Programming'},
    {   'category': 'Additional',
        'correct_answer': 'Chaos engineering injects deliberate turbulent conditions (killing nodes, latency) to '
                          'uncover system resilience flaws before outages occur.',
        'difficulty': 'MEDIUM',
        'explanation': 'Chaos engineering injects deliberate turbulent conditions (killing nodes, latency) to uncover '
                       'system resilience flaws before outages occur.',
        'field': 'Engineering Architecture',
        'options': [   'Chaos engineering disables all production monitoring and alerting to observe engineer response '
                       'times under pressure.',
                       'Chaos engineering randomly deletes database backups during off-hours to test disaster recovery '
                       'compliance.',
                       'Chaos engineering runs exclusively on staging environments with synthetic mock data rather '
                       'than realistic systems.',
                       'Chaos engineering injects deliberate turbulent conditions (killing nodes, latency) to uncover '
                       'system resilience flaws before outages occur.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Chaos Engineering GameDay?',
        'question_type': 'MCQ',
        'title': 'Chaos Engineering GameDay',
        'topic': 'Reliability'},
    {   'category': 'Additional',
        'correct_answer': 'Star schema denormalizes dimensions into single tables for query speed; snowflake '
                          'normalizes dimensions into multiple related tables.',
        'difficulty': 'MEDIUM',
        'explanation': 'Star schema denormalizes dimensions into single tables for query speed; snowflake normalizes '
                       'dimensions into multiple related tables.',
        'field': 'Engineering Architecture',
        'options': [   'Star schema denormalizes dimensions into single tables for query speed; snowflake normalizes '
                       'dimensions into multiple related tables.',
                       'Star schema normalizes all dimension tables into 3NF, whereas snowflake schema denormalizes '
                       'into a single giant flat table.',
                       'Star schema supports only unstructured NoSQL documents, while snowflake schema requires '
                       'relational column stores.',
                       'Star schema prohibits primary key indexing, whereas snowflake schema enforces strict document '
                       'graph edges.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Data Warehouse Star vs Snowflake Schema?',
        'question_type': 'MCQ',
        'title': 'Data Warehouse Star vs Snowflake Schema',
        'topic': 'Data Warehousing'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Cold starts occur when a cloud provider spins up a new container instance and runtime '
                          'environment for an idle function invocation.',
        'difficulty': 'MEDIUM',
        'explanation': 'Cold starts occur when a cloud provider spins up a new container instance and runtime '
                       'environment for an idle function invocation.',
        'field': 'Engineering Architecture',
        'options': [   'Cold starts occur when an active Lambda function exhausts its maximum allocated execution '
                       'timeout of 15 minutes.',
                       'Cold starts occur when a cloud provider spins up a new container instance and runtime '
                       'environment for an idle function invocation.',
                       'Cold starts represent the delay caused by DNS caching servers propagating new serverless '
                       'domain records.',
                       'Cold starts happen when a serverless database drops active connection pool sockets due to idle '
                       'timeouts.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Serverless Cold Start Latency?',
        'question_type': 'MCQ',
        'title': 'Serverless Cold Start Latency',
        'topic': 'Cloud Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'A Bounded Context defines the explicit boundary within which a specific domain model and '
                          'ubiquitous language applies.',
        'difficulty': 'MEDIUM',
        'explanation': 'A Bounded Context defines the explicit boundary within which a specific domain model and '
                       'ubiquitous language applies.',
        'field': 'Engineering Architecture',
        'options': [   'A Bounded Context is a shared monolithic schema where all database entities are accessible by '
                       'all application services.',
                       'A Bounded Context specifies the physical network subnet boundaries enforced by cloud security '
                       'groups.',
                       'A Bounded Context defines the explicit boundary within which a specific domain model and '
                       'ubiquitous language applies.',
                       'A Bounded Context is a microservice chassis library that handles HTTP serialization across '
                       'languages.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Domain-Driven Design (DDD) Bounded Context?',
        'question_type': 'MCQ',
        'title': 'Domain-Driven Design (DDD) Bounded Context',
        'topic': 'Software Architecture'},
    {   'category': 'Additional',
        'correct_answer': 'Proof Key for Code Exchange (PKCE) prevents authorization code interception attacks on '
                          'public clients without client secrets.',
        'difficulty': 'MEDIUM',
        'explanation': 'Proof Key for Code Exchange (PKCE) prevents authorization code interception attacks on public '
                       'clients without client secrets.',
        'field': 'Engineering Architecture',
        'options': [   'PKCE replaces access tokens with long-lived client secret strings embedded in public mobile '
                       'applications.',
                       "PKCE encrypts the user's password using symmetric AES before sending it directly to the "
                       'authorization server.',
                       'PKCE requires public clients to store an unencrypted private RSA key in localStorage for '
                       'mutual TLS.',
                       'Proof Key for Code Exchange (PKCE) prevents authorization code interception attacks on public '
                       'clients without client secrets.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of OAuth2 Authorization Code Grant with PKCE?',
        'question_type': 'MCQ',
        'title': 'OAuth2 Authorization Code Grant with PKCE',
        'topic': 'Security'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'A good shard key distributes data and query volume uniformly across nodes, avoiding hot '
                          'partitions.',
        'difficulty': 'MEDIUM',
        'explanation': 'A good shard key distributes data and query volume uniformly across nodes, avoiding hot '
                       'partitions.',
        'field': 'Engineering Architecture',
        'options': [   'A good shard key distributes data and query volume uniformly across nodes, avoiding hot '
                       'partitions.',
                       'A good shard key routes all write operations to a single leader node while sharding read '
                       'replicas.',
                       'A good shard key uses monotonically increasing timestamps so that all recent records cluster '
                       'on one physical node.',
                       'A good shard key selects low-cardinality boolean columns to maximize parallel thread '
                       'execution.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Database Sharding Key Selection?',
        'question_type': 'MCQ',
        'title': 'Database Sharding Key Selection',
        'topic': 'Database Architecture'},
    {   'category': 'Additional',
        'correct_answer': 'gRPC provides strongly-typed binary serialization, bidirectional streaming, and low latency '
                          'over HTTP/2 transport.',
        'difficulty': 'MEDIUM',
        'explanation': 'gRPC provides strongly-typed binary serialization, bidirectional streaming, and low latency '
                       'over HTTP/2 transport.',
        'field': 'Engineering Architecture',
        'options': [   'gRPC relies on text-based XML schemas transmitted over single-direction HTTP/1.0 connections.',
                       'gRPC provides strongly-typed binary serialization, bidirectional streaming, and low latency '
                       'over HTTP/2 transport.',
                       'gRPC converts all payloads to JSON strings to maintain human-readable network inspectability.',
                       'gRPC requires a Node.js runtime process to serialize and deserialize strongly-typed binary '
                       'schemas.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of gRPC over Protocol Buffers?',
        'question_type': 'MCQ',
        'title': 'gRPC over Protocol Buffers',
        'topic': 'API Design'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Isolates core business domain logic from external dependencies (databases, web APIs) via '
                          'interfaces (ports) and implementations (adapters).',
        'difficulty': 'MEDIUM',
        'explanation': 'Isolates core business domain logic from external dependencies (databases, web APIs) via '
                       'interfaces (ports) and implementations (adapters).',
        'field': 'Engineering Architecture',
        'options': [   'Hexagonal architecture couples business domain models directly to specific database ORMs and '
                       'UI frameworks.',
                       'Hexagonal architecture requires six distinct microservice containers to be deployed for every '
                       'business domain.',
                       'Isolates core business domain logic from external dependencies (databases, web APIs) via '
                       'interfaces (ports) and implementations (adapters).',
                       'Hexagonal architecture restricts domain logic to running inside browser Web Workers '
                       'exclusively.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Hexagonal (Ports and Adapters) Architecture?',
        'question_type': 'MCQ',
        'title': 'Hexagonal (Ports and Adapters) Architecture',
        'topic': 'Software Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Data Mesh treats data as a product owned by decentralized domain teams rather than a '
                          'central monolithic data lake.',
        'difficulty': 'MEDIUM',
        'explanation': 'Data Mesh treats data as a product owned by decentralized domain teams rather than a central '
                       'monolithic data lake.',
        'field': 'Engineering Architecture',
        'options': [   'Data Mesh mandates that all enterprise data pipelines ingest into a single central enterprise '
                       'data warehouse team.',
                       'Data Mesh replaces all relational SQL databases with unmanaged distributed file storage '
                       'buckets.',
                       'Data Mesh eliminates domain ownership by centralizing data quality checks with external '
                       'compliance auditors.',
                       'Data Mesh treats data as a product owned by decentralized domain teams rather than a central '
                       'monolithic data lake.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Data Mesh Decentralized Governance?',
        'question_type': 'MCQ',
        'title': 'Data Mesh Decentralized Governance',
        'topic': 'Data Architecture'},
    {   'category': 'Additional',
        'correct_answer': 'Feature flags allow decoupling code deployment from feature release, enabling instant '
                          'kill-switches and canary rollouts.',
        'difficulty': 'MEDIUM',
        'explanation': 'Feature flags allow decoupling code deployment from feature release, enabling instant '
                       'kill-switches and canary rollouts.',
        'field': 'Engineering Architecture',
        'options': [   'Feature flags allow decoupling code deployment from feature release, enabling instant '
                       'kill-switches and canary rollouts.',
                       'Feature flags require a complete blue-green infrastructure redeployment to toggle '
                       'functionality for users.',
                       'Feature flags compile distinct application binaries for each target audience segment at build '
                       'time.',
                       'Feature flags store toggle states in local client browser cookies that users can arbitrarily '
                       'modify.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Feature Flags Dynamic Rollout?',
        'question_type': 'MCQ',
        'title': 'Feature Flags Dynamic Rollout',
        'topic': 'DevOps'},
    {   'category': 'Additional',
        'correct_answer': 'RLS enforces authorization policies at the database layer, filtering rows visible to '
                          'queries based on current user context.',
        'difficulty': 'MEDIUM',
        'explanation': 'RLS enforces authorization policies at the database layer, filtering rows visible to queries '
                       'based on current user context.',
        'field': 'Engineering Architecture',
        'options': [   'RLS encrypts entire database tables on disk using the database superuser password.',
                       'RLS enforces authorization policies at the database layer, filtering rows visible to queries '
                       'based on current user context.',
                       'RLS requires backend application code to append custom WHERE clauses to every raw SQL query '
                       'manually.',
                       'RLS prevents users from modifying table schemas by revoking DDL permissions from the public '
                       'role.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Row-Level Security (RLS) in Postgres?',
        'question_type': 'MCQ',
        'title': 'Row-Level Security (RLS) in Postgres',
        'topic': 'Security'},
    {   'category': 'Additional',
        'correct_answer': 'A Trace represents an end-to-end transaction journey; a Span represents an individual timed '
                          'unit of work within that trace.',
        'difficulty': 'MEDIUM',
        'explanation': 'A Trace represents an end-to-end transaction journey; a Span represents an individual timed '
                       'unit of work within that trace.',
        'field': 'Engineering Architecture',
        'options': [   'A Span is the entire system log aggregation; a Trace is a single metric counter increment.',
                       'A Trace represents CPU profiling statistics; a Span represents the network throughput of a '
                       'gateway.',
                       'A Trace represents an end-to-end transaction journey; a Span represents an individual timed '
                       'unit of work within that trace.',
                       'A Trace is an individual database query; a Span is the total uptime of the host operating '
                       'system.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Distributed Tracing Span vs Trace?',
        'question_type': 'MCQ',
        'title': 'Distributed Tracing Span vs Trace',
        'topic': 'Observability'},
    {   'category': 'Additional',
        'correct_answer': 'Optimistic locking checks for version conflicts at commit time; pessimistic locking holds '
                          'database locks for the duration of the transaction.',
        'difficulty': 'MEDIUM',
        'explanation': 'Optimistic locking checks for version conflicts at commit time; pessimistic locking holds '
                       'database locks for the duration of the transaction.',
        'field': 'Engineering Architecture',
        'options': [   'Optimistic locking acquires exclusive row locks immediately; pessimistic locking verifies '
                       'versions at commit.',
                       'Optimistic locking guarantees zero transaction conflicts by serializing all database writes '
                       'through one thread.',
                       'Pessimistic locking allows concurrent dirty reads by disabling transaction isolation '
                       'boundaries.',
                       'Optimistic locking checks for version conflicts at commit time; pessimistic locking holds '
                       'database locks for the duration of the transaction.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Database Pessimistic vs Optimistic Locking?',
        'question_type': 'MCQ',
        'title': 'Database Pessimistic vs Optimistic Locking',
        'topic': 'Databases'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Webpack Module Federation allows separate frontend applications to dynamically load remote '
                          'code at runtime without monolith builds.',
        'difficulty': 'MEDIUM',
        'explanation': 'Webpack Module Federation allows separate frontend applications to dynamically load remote '
                       'code at runtime without monolith builds.',
        'field': 'Engineering Architecture',
        'options': [   'Webpack Module Federation allows separate frontend applications to dynamically load remote '
                       'code at runtime without monolith builds.',
                       'Module Federation bundles all micro-frontend repositories into a single massive monolithic '
                       'Webpack chunk.',
                       'Module Federation isolates frontend components inside nested iframes communicating via '
                       'window.postMessage.',
                       'Module Federation replaces client-side single page applications with server-side rendered JSP '
                       'templates.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Micro-Frontends Module Federation?',
        'question_type': 'MCQ',
        'title': 'Micro-Frontends Module Federation',
        'topic': 'Frontend Architecture'},
    {   'category': 'Technical Knowledge',
        'correct_answer': 'Stop-the-world pauses halt all application threads while the garbage collector traces '
                          'object references and compacts memory.',
        'difficulty': 'MEDIUM',
        'explanation': 'Stop-the-world pauses halt all application threads while the garbage collector traces object '
                       'references and compacts memory.',
        'field': 'Engineering Architecture',
        'options': [   'Stop-the-world pauses permanently terminate background daemon worker threads that exceed '
                       'memory thresholds.',
                       'Stop-the-world pauses halt all application threads while the garbage collector traces object '
                       'references and compacts memory.',
                       'Stop-the-world pauses pause incoming network traffic at the load balancer while application '
                       'threads continue writing.',
                       'Stop-the-world pauses trigger only during application startup when initial JVM classes are '
                       'loaded.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Garbage Collection Stop-The-World Pauses?',
        'question_type': 'MCQ',
        'title': 'Garbage Collection Stop-The-World Pauses',
        'topic': 'Runtime Systems'},
    {   'category': 'Additional',
        'correct_answer': 'Index selectivity is the ratio of distinct values to total rows; high-selectivity columns '
                          'benefit significantly more from indexing.',
        'difficulty': 'MEDIUM',
        'explanation': 'Index selectivity is the ratio of distinct values to total rows; high-selectivity columns '
                       'benefit significantly more from indexing.',
        'field': 'Engineering Architecture',
        'options': [   'Selectivity measures the total disk space consumed by an index relative to the underlying '
                       'table file.',
                       'High-selectivity columns have very few unique values (e.g. boolean flags) and optimize B-tree '
                       'lookups.',
                       'Index selectivity is the ratio of distinct values to total rows; high-selectivity columns '
                       'benefit significantly more from indexing.',
                       'Index selectivity indicates the frequency with which a table is updated by concurrent write '
                       'transactions.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Database Index Selectivity?',
        'question_type': 'MCQ',
        'title': 'Database Index Selectivity',
        'topic': 'Databases'},
    {   'category': 'Additional',
        'correct_answer': 'Allows browsers to expose response data to JavaScript when requests include credentials '
                          'like cookies or Authorization headers.',
        'difficulty': 'MEDIUM',
        'explanation': 'Allows browsers to expose response data to JavaScript when requests include credentials like '
                       'cookies or Authorization headers.',
        'field': 'Engineering Architecture',
        'options': [   'Allows cross-origin requests to bypass HTTPS encryption requirements for local development '
                       'endpoints.',
                       'Permits wildcard Access-Control-Allow-Origin: * to be used in conjunction with credentialed '
                       'requests.',
                       'Instructs the browser to disable same-site cookie validation for all third-party analytics '
                       'trackers.',
                       'Allows browsers to expose response data to JavaScript when requests include credentials like '
                       'cookies or Authorization headers.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of CORS Access-Control-Allow-Credentials?',
        'question_type': 'MCQ',
        'title': 'CORS Access-Control-Allow-Credentials',
        'topic': 'Web Security'},
    {   'category': 'Additional',
        'correct_answer': 'DataLoader batches and caches individual database lookups into a single batched query '
                          'across graph resolvers.',
        'difficulty': 'MEDIUM',
        'explanation': 'DataLoader batches and caches individual database lookups into a single batched query across '
                       'graph resolvers.',
        'field': 'Engineering Architecture',
        'options': [   'DataLoader batches and caches individual database lookups into a single batched query across '
                       'graph resolvers.',
                       'Solves the N+1 problem by disabling nested relational fields in the GraphQL schema definition.',
                       'Solves the N+1 problem by converting all GraphQL queries to plain REST endpoints at the API '
                       'gateway.',
                       'Solves the N+1 problem by establishing a separate database connection pool for every requested '
                       'child field.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of GraphQL N+1 Query Problem Solution?',
        'question_type': 'MCQ',
        'title': 'GraphQL N+1 Query Problem Solution',
        'topic': 'API Design'},
    {   'category': 'Additional',
        'correct_answer': 'SNI includes the requested hostname in the TLS ClientHello, allowing servers to host '
                          'multiple SSL certificates on a single IP.',
        'difficulty': 'MEDIUM',
        'explanation': 'SNI includes the requested hostname in the TLS ClientHello, allowing servers to host multiple '
                       'SSL certificates on a single IP.',
        'field': 'Engineering Architecture',
        'options': [   "SNI transmits the client's private decryption key in plain text during the initial TCP "
                       'handshake.',
                       'SNI includes the requested hostname in the TLS ClientHello, allowing servers to host multiple '
                       'SSL certificates on a single IP.',
                       'SNI encrypts DNS query packets to prevent intermediate internet service providers from logging '
                       'domains.',
                       'SNI requires each virtual host to be assigned a unique dedicated public IPv4 address.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of TLS Certificate SNI (Server Name Indication)?',
        'question_type': 'MCQ',
        'title': 'TLS Certificate SNI (Server Name Indication)',
        'topic': 'Networking'},
    {   'category': 'Additional',
        'correct_answer': 'Least Recently Used (LRU) evicts the item accessed longest ago; Least Frequently Used (LFU) '
                          'evicts the item with lowest total access count.',
        'difficulty': 'MEDIUM',
        'explanation': 'Least Recently Used (LRU) evicts the item accessed longest ago; Least Frequently Used (LFU) '
                       'evicts the item with lowest total access count.',
        'field': 'Engineering Architecture',
        'options': [   'LRU evicts the largest cached object in memory; LFU evicts the smallest cached payload.',
                       'LRU retains items with the highest frequency of hits; LFU removes items that have expired by '
                       'TTL.',
                       'Least Recently Used (LRU) evicts the item accessed longest ago; Least Frequently Used (LFU) '
                       'evicts the item with lowest total access count.',
                       'LRU and LFU are identical eviction algorithms with different vendor-specific naming '
                       'conventions.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Distributed Cache Eviction LRU vs LFU?',
        'question_type': 'MCQ',
        'title': 'Distributed Cache Eviction LRU vs LFU',
        'topic': 'Caching'},
    {   'category': 'Additional',
        'correct_answer': 'Drift detection identifies discrepancies between the intended state defined in IaC and the '
                          'actual live cloud resource configuration.',
        'difficulty': 'MEDIUM',
        'explanation': 'Drift detection identifies discrepancies between the intended state defined in IaC and the '
                       'actual live cloud resource configuration.',
        'field': 'Engineering Architecture',
        'options': [   'Drift detection automatically deletes cloud resources that were created more than 30 days ago.',
                       'Drift detection measures the gradual degradation of server CPU clock frequencies over hardware '
                       'lifespans.',
                       'Drift detection prevents engineers from executing git commits when infrastructure code tests '
                       'fail.',
                       'Drift detection identifies discrepancies between the intended state defined in IaC and the '
                       'actual live cloud resource configuration.'],
        'question_text': 'In enterprise architecture and engineering practice, what is the core mechanism or '
                         'definition of Infrastructure Drift Detection?',
        'question_type': 'MCQ',
        'title': 'Infrastructure Drift Detection',
        'topic': 'DevOps'}]
