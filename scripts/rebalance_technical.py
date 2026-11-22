"""Rebalance TECHNICAL_QUESTIONS with balanced A/B/C/D keys and realistic distractors."""

import pprint
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

from scripts.fixtures.technical_questions import TECHNICAL_QUESTIONS
from app.schemas.category import AssessmentCategory

REALISTIC_DISTRACTORS = {
    "Zero Trust Architecture": [
        "Trust all internal network traffic implicitly once authenticated through the perimeter VPN gateway.",
        "Rely exclusively on static subnet IP whitelisting to validate trust between containerized microservices.",
        "Disable mutual TLS between private cluster services to eliminate cryptographic handshake overhead."
    ],
    "Asymmetric Cryptography Key Exchange": [
        "Transmits the server private key across the network encrypted with an ephemeral public certificate.",
        "Employs shared symmetric AES-256 keys hardcoded into client binaries during build time.",
        "Requires a centralized certificate authority to generate and retain both session secret keys."
    ],
    "Database Normalization 3NF": [
        "A table is in 3NF if every column is a foreign key and no multi-valued attributes exist.",
        "A table is in 3NF if non-prime attributes are partially dependent on a composite primary key.",
        "A table is in 3NF if all relations have been pre-joined to eliminate foreign key constraints."
    ],
    "Two-Phase Commit (2PC) Blocking": [
        "2PC is non-blocking: cohorts automatically elect a new coordinator via Raft if the primary fails.",
        "2PC guarantees eventual consistency by executing commits asynchronously in background worker threads.",
        "2PC allows cohort nodes to unilaterally abort or commit if no message is received within 100ms."
    ],
    "Consistent Hashing Ring": [
        "Consistent hashing uses a modulo hash table that remaps all keys whenever the server count changes.",
        "Consistent hashing distributes queries strictly round-robin without mapping keys to node tokens.",
        "Consistent hashing requires a centralized directory service to store the physical server location of every key."
    ],
    "API Rate Limiting Token Bucket": [
        "Token bucket drops all requests once an arbitrary fixed threshold of active TCP sockets is reached.",
        "Token bucket counts total requests over a rolling 24-hour window, resetting the counter at midnight.",
        "Token bucket requires client IP addresses to acquire a distributed mutex before sending any HTTP payload."
    ],
    "Message Broker Dead Letter Queue (DLQ)": [
        "A DLQ automatically redelivers corrupt messages to consumers in an infinite retry loop until acknowledged.",
        "A DLQ drops poisoned messages permanently from memory without recording error payloads or metadata.",
        "A DLQ routes failed messages immediately to end-user browsers via WebSockets for manual user remediation."
    ],
    "Database Isolation Level Phantom Reads": [
        "Phantom reads happen when an uncommitted dirty write is rolled back and overwritten by a concurrent transaction.",
        "Phantom reads occur when two concurrent transactions update the same single row simultaneously.",
        "Phantom reads occur when a database index is rebuilt concurrently during an active sequential table scan."
    ],
    "Zero-Copy I/O with sendfile()": [
        "sendfile() forces all byte buffers to be copied twice through user-space memory for inspection.",
        "sendfile() utilizes CPU software rendering to compress file streams before socket transmission.",
        "sendfile() encrypts memory pages in RAM using asymmetric RSA keys before DMA transfer."
    ],
    "Chaos Engineering GameDay": [
        "Chaos engineering disables all production monitoring and alerting to observe engineer response times under pressure.",
        "Chaos engineering randomly deletes database backups during off-hours to test disaster recovery compliance.",
        "Chaos engineering runs exclusively on staging environments with synthetic mock data rather than realistic systems."
    ],
    "Data Warehouse Star vs Snowflake Schema": [
        "Star schema normalizes all dimension tables into 3NF, whereas snowflake schema denormalizes into a single giant flat table.",
        "Star schema supports only unstructured NoSQL documents, while snowflake schema requires relational column stores.",
        "Star schema prohibits primary key indexing, whereas snowflake schema enforces strict document graph edges."
    ],
    "Serverless Cold Start Latency": [
        "Cold starts occur when an active Lambda function exhausts its maximum allocated execution timeout of 15 minutes.",
        "Cold starts represent the delay caused by DNS caching servers propagating new serverless domain records.",
        "Cold starts happen when a serverless database drops active connection pool sockets due to idle timeouts."
    ],
    "Domain-Driven Design (DDD) Bounded Context": [
        "A Bounded Context is a shared monolithic schema where all database entities are accessible by all application services.",
        "A Bounded Context specifies the physical network subnet boundaries enforced by cloud security groups.",
        "A Bounded Context is a microservice chassis library that handles HTTP serialization across languages."
    ],
    "OAuth2 Authorization Code Grant with PKCE": [
        "PKCE replaces access tokens with long-lived client secret strings embedded in public mobile applications.",
        "PKCE encrypts the user's password using symmetric AES before sending it directly to the authorization server.",
        "PKCE requires public clients to store an unencrypted private RSA key in localStorage for mutual TLS."
    ],
    "Database Sharding Key Selection": [
        "A good shard key routes all write operations to a single leader node while sharding read replicas.",
        "A good shard key uses monotonically increasing timestamps so that all recent records cluster on one physical node.",
        "A good shard key selects low-cardinality boolean columns to maximize parallel thread execution."
    ],
    "gRPC over Protocol Buffers": [
        "gRPC relies on text-based XML schemas transmitted over single-direction HTTP/1.0 connections.",
        "gRPC converts all payloads to JSON strings to maintain human-readable network inspectability.",
        "gRPC requires a Node.js runtime process to serialize and deserialize strongly-typed binary schemas."
    ],
    "Hexagonal (Ports and Adapters) Architecture": [
        "Hexagonal architecture couples business domain models directly to specific database ORMs and UI frameworks.",
        "Hexagonal architecture requires six distinct microservice containers to be deployed for every business domain.",
        "Hexagonal architecture restricts domain logic to running inside browser Web Workers exclusively."
    ],
    "Data Mesh Decentralized Governance": [
        "Data Mesh mandates that all enterprise data pipelines ingest into a single central enterprise data warehouse team.",
        "Data Mesh replaces all relational SQL databases with unmanaged distributed file storage buckets.",
        "Data Mesh eliminates domain ownership by centralizing data quality checks with external compliance auditors."
    ],
    "Feature Flags Dynamic Rollout": [
        "Feature flags require a complete blue-green infrastructure redeployment to toggle functionality for users.",
        "Feature flags compile distinct application binaries for each target audience segment at build time.",
        "Feature flags store toggle states in local client browser cookies that users can arbitrarily modify."
    ],
    "Row-Level Security (RLS) in Postgres": [
        "RLS encrypts entire database tables on disk using the database superuser password.",
        "RLS requires backend application code to append custom WHERE clauses to every raw SQL query manually.",
        "RLS prevents users from modifying table schemas by revoking DDL permissions from the public role."
    ],
    "Distributed Tracing Span vs Trace": [
        "A Span is the entire system log aggregation; a Trace is a single metric counter increment.",
        "A Trace represents CPU profiling statistics; a Span represents the network throughput of a gateway.",
        "A Trace is an individual database query; a Span is the total uptime of the host operating system."
    ],
    "Database Pessimistic vs Optimistic Locking": [
        "Optimistic locking acquires exclusive row locks immediately; pessimistic locking verifies versions at commit.",
        "Optimistic locking guarantees zero transaction conflicts by serializing all database writes through one thread.",
        "Pessimistic locking allows concurrent dirty reads by disabling transaction isolation boundaries."
    ],
    "Micro-Frontends Module Federation": [
        "Module Federation bundles all micro-frontend repositories into a single massive monolithic Webpack chunk.",
        "Module Federation isolates frontend components inside nested iframes communicating via window.postMessage.",
        "Module Federation replaces client-side single page applications with server-side rendered JSP templates."
    ],
    "Garbage Collection Stop-The-World Pauses": [
        "Stop-the-world pauses permanently terminate background daemon worker threads that exceed memory thresholds.",
        "Stop-the-world pauses pause incoming network traffic at the load balancer while application threads continue writing.",
        "Stop-the-world pauses trigger only during application startup when initial JVM classes are loaded."
    ],
    "Database Index Selectivity": [
        "Selectivity measures the total disk space consumed by an index relative to the underlying table file.",
        "High-selectivity columns have very few unique values (e.g. boolean flags) and optimize B-tree lookups.",
        "Index selectivity indicates the frequency with which a table is updated by concurrent write transactions."
    ],
    "CORS Access-Control-Allow-Credentials": [
        "Allows cross-origin requests to bypass HTTPS encryption requirements for local development endpoints.",
        "Permits wildcard Access-Control-Allow-Origin: * to be used in conjunction with credentialed requests.",
        "Instructs the browser to disable same-site cookie validation for all third-party analytics trackers."
    ],
    "GraphQL N+1 Query Problem Solution": [
        "Solves the N+1 problem by disabling nested relational fields in the GraphQL schema definition.",
        "Solves the N+1 problem by converting all GraphQL queries to plain REST endpoints at the API gateway.",
        "Solves the N+1 problem by establishing a separate database connection pool for every requested child field."
    ],
    "TLS Certificate SNI (Server Name Indication)": [
        "SNI transmits the client's private decryption key in plain text during the initial TCP handshake.",
        "SNI encrypts DNS query packets to prevent intermediate internet service providers from logging domains.",
        "SNI requires each virtual host to be assigned a unique dedicated public IPv4 address."
    ],
    "Distributed Cache Eviction LRU vs LFU": [
        "LRU evicts the largest cached object in memory; LFU evicts the smallest cached payload.",
        "LRU retains items with the highest frequency of hits; LFU removes items that have expired by TTL.",
        "LRU and LFU are identical eviction algorithms with different vendor-specific naming conventions."
    ],
    "Infrastructure Drift Detection": [
        "Drift detection automatically deletes cloud resources that were created more than 30 days ago.",
        "Drift detection measures the gradual degradation of server CPU clock frequencies over hardware lifespans.",
        "Drift detection prevents engineers from executing git commits when infrastructure code tests fail."
    ]
}

new_questions = []

for i, q in enumerate(TECHNICAL_QUESTIONS):
    title = q["title"]
    qtext = q["question_text"]
    ans = q["correct_answer"]
    opts = list(q["options"])
    exp = q["explanation"]
    cat = q.get("category", AssessmentCategory.TECHNICAL_KNOWLEDGE.value)
    field = q.get("field", "Web & Full Stack")
    topic = q.get("topic", "Architecture")
    diff = q.get("difficulty", "MEDIUM")

    # If this was one of the generated questions with joke distractors, replace them
    if title in REALISTIC_DISTRACTORS:
        other_3 = REALISTIC_DISTRACTORS[title]
    else:
        other_3 = [o for o in opts if o != ans][:3]
        while len(other_3) < 3:
            other_3.append(f"Alternative design approach {len(other_3)+1}")

    # Rotate correct answer evenly across positions 0 (A), 1 (B), 2 (C), 3 (D)
    target_pos = i % 4
    balanced_opts = list(other_3[:3])
    balanced_opts.insert(target_pos, ans)

    new_questions.append({
        "title": title,
        "question_text": qtext,
        "question_type": "MCQ",
        "category": cat,
        "field": field,
        "topic": topic,
        "difficulty": diff,
        "correct_answer": ans,
        "options": balanced_opts,
        "explanation": exp
    })

# Format python file
out_path = ROOT / "scripts" / "fixtures" / "technical_questions.py"
content = '"""TRELLIS Technical Knowledge & Multi-Disciplinary Question Bank Fixtures (100 Questions).\n60 Technical Knowledge questions (Full Stack, Cloud/DevOps, Data/AI, Core Systems) +\n40 Multi-Disciplinary Architecture & Engineering questions.\nRebalanced keys: ~25% per position A/B/C/D.\n"""\n\nfrom app.schemas.category import AssessmentCategory\n\nTECHNICAL_QUESTIONS = ' + pprint.pformat(new_questions, indent=4, width=120) + "\n"

out_path.write_text(content, encoding="utf-8")
print(f"Wrote {len(new_questions)} balanced technical questions to {out_path}")
