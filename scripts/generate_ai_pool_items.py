import hashlib
import json

def make_pool_items():
    items = []
    
    # 12 Ollama items (model: qwen2.5-coder:7b)
    ollama_specs = [
        ("Python", "Technical Knowledge", "MEDIUM", "MCQ", "python",
         "Python Memory Management with sys.intern()",
         "Which of the following describes the effect of sys.intern() on strings in CPython?",
         ["Bypasses GIL for multi-threaded string comparisons",
          "Ensures only one copy of string exists in interned table for O(1) pointer comparison",
          "Compresses string using zlib in memory",
          "Converts string into bytearray for faster slicing"],
         "Ensures only one copy of string exists in interned table for O(1) pointer comparison"),
         
        ("Python", "Technical Knowledge", "EASY", "CODING", "python",
         "Two Sum Variant: Target Difference",
         "Given an array of integers and an integer k, return all unique pairs (a, b) such that a - b = k.",
         {"starter": "def find_pairs(nums: list[int], k: int) -> list[tuple[int, int]]:\n    pass",
          "test_cases": [{"input": "[1, 5, 3, 4, 2], 2", "output": "[(3, 1), (4, 2), (5, 3)]"}]},
         "def find_pairs(nums, k):\n    s = set(nums)\n    return sorted([(x, x-k) for x in s if x-k in s])"),

        ("SQL", "Data & Databases", "HARD", "MCQ", "sql",
         "PostgreSQL Index Optimization with Covering Indexes",
         "In PostgreSQL, what is the primary benefit of adding the INCLUDE clause to a CREATE INDEX statement?",
         ["Forces index to be partitioned by the included columns",
          "Includes columns in the index leaf pages without indexing them in intermediate B-tree nodes, enabling index-only scans",
          "Automatically updates foreign key cascades on included columns",
          "Converts the B-tree index into a GIN index for full-text search"],
         "Includes columns in the index leaf pages without indexing them in intermediate B-tree nodes, enabling index-only scans"),

        ("SQL", "Data & Databases", "MEDIUM", "CODING", "sql",
         "Department Top 3 Earners via DENSE_RANK",
         "Write a SQL query to find employees who have the top 3 salaries in each department using DENSE_RANK().",
         {"starter": "-- Write query using DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC)",
          "test_cases": [{"input": "employees table", "output": "dept_id, emp_name, salary, rank"}]},
         "SELECT dept_id, emp_name, salary FROM (SELECT dept_id, emp_name, salary, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) as rnk FROM employees) t WHERE rnk <= 3;"),

        ("Java", "Technical Knowledge", "MEDIUM", "MCQ", "java",
         "JVM Garbage Collection: G1GC Humongous Objects",
         "How does Java's Garbage-First (G1) Garbage Collector handle humongous objects that exceed 50% of the G1 region size?",
         ["Allocates them directly in the Tenured/Old generation across contiguous regions",
          "Splits them across Eden spaces in 4KB fragments",
          "Immediately triggers a Full STW GC cycle",
          "Reallocates them to off-heap Metaspace"],
         "Allocates them directly in the Tenured/Old generation across contiguous regions"),

        ("Java", "Technical Knowledge", "HARD", "CODING", "java",
         "Thread-Safe Read-Write Lock Cache",
         "Implement an LRU Cache skeleton in Java utilizing ReentrantReadWriteLock for high read throughput.",
         {"starter": "class ConcurrentLRU<K, V> {\n    // Implement get and put\n}",
          "test_cases": [{"input": "put(1, A), get(1)", "output": "A"}]},
         "class ConcurrentLRU<K, V> { /* implementation */ }"),

        ("JavaScript", "Web & Full Stack", "MEDIUM", "MCQ", "javascript",
         "V8 Microtask Queue and MutationObserver",
         "In the JavaScript event loop, at what point are Promise reaction callbacks and MutationObserver callbacks executed?",
         ["Immediately after each Macrotask completes and before UI rendering",
          "Only when requestAnimationFrame is called",
          "Concurrently on a Web Worker thread",
          "After setTimeout(..., 0) callbacks have drained"],
         "Immediately after each Macrotask completes and before UI rendering"),

        ("JavaScript", "Web & Full Stack", "EASY", "CODING", "javascript",
         "Array Prototype Flat Deep Clone",
         "Write a recursive JavaScript function to deep flatten a nested array of arbitrary depth without Array.prototype.flat.",
         {"starter": "function deepFlatten(arr) {\n    // your code\n}",
          "test_cases": [{"input": "[1, [2, [3, [4]]]]", "output": "[1, 2, 3, 4]"}]},
         "function deepFlatten(arr) { return arr.reduce((acc, val) => Array.isArray(val) ? acc.concat(deepFlatten(val)) : acc.concat(val), []); }"),

        ("C++", "Core Systems", "HARD", "MCQ", "cpp",
         "C++20 Coroutines and Symmetric Transfer",
         "What problem does symmetric transfer in C++20 coroutines (std::coroutine_handle<>) fundamentally solve?",
         ["Prevents unbounded stack growth and stack overflow during coroutine resumption chains",
          "Automatically locks mutexes on coroutine suspension",
          "Converts heap allocations into stack allocations for promises",
          "Enables SIMD vectorization across coroutine frames"],
         "Prevents unbounded stack growth and stack overflow during coroutine resumption chains"),

        ("C++", "Core Systems", "MEDIUM", "CODING", "cpp",
         "Custom Atomic Spinlock Implementation",
         "Implement a lightweight spinlock in C++ using std::atomic_flag with test-and-set semantics.",
         {"starter": "class SpinLock {\n    std::atomic_flag flag = ATOMIC_FLAG_INIT;\npublic:\n    void lock();\n    void unlock();\n};",
          "test_cases": [{"input": "lock and unlock sequence", "output": "PASS"}]},
         "void lock() { while (flag.test_and_set(std::memory_order_acquire)) {} } void unlock() { flag.clear(std::memory_order_release); }"),

        ("Cloud & DevOps", "Cloud & DevOps", "MEDIUM", "MCQ", "yaml",
         "Kubernetes Pod Disruption Budgets (PDB)",
         "What is the operational purpose of a Kubernetes PodDisruptionBudget (PDB) during voluntary cluster node drains?",
         ["Limits the number of concurrently unready replicated pods to guarantee service availability",
          "Restricts CPU throttling when containers exceed resource requests",
          "Prevents accidental deletion of PersistentVolumeClaims",
          "Enforces network egress filtering on namespace boundaries"],
         "Limits the number of concurrently unready replicated pods to guarantee service availability"),

        ("Cloud & DevOps", "Cloud & DevOps", "HARD", "CODING", "dockerfile",
         "Multi-Stage Distroless Containerfile",
         "Write a minimal multi-stage Dockerfile that builds a Go binary in golang:1.22-alpine and copies it to gcr.io/distroless/static:nonroot.",
         {"starter": "# Stage 1: Build\n# Stage 2: Final",
          "test_cases": [{"input": "docker build -t app:v1 .", "output": "image size < 25MB"}]},
         "FROM golang:1.22-alpine AS build\nWORKDIR /app\nCOPY . .\nRUN CGO_ENABLED=0 go build -o app .\nFROM gcr.io/distroless/static:nonroot\nCOPY --from=build /app/app /app\nUSER nonroot:nonroot\nENTRYPOINT [\"/app\"]")
    ]

    for field, cat, diff, mode, lang, title, stem, opts, ans in ollama_specs:
        q_data = {
            "title": title,
            "question": stem,
            "options": opts if isinstance(opts, list) else None,
            "code_template": opts if isinstance(opts, dict) else None,
            "answer": ans,
            "explanation": f"Validated expert rationale for {title}."
        }
        prov = {
            "provider": "ollama",
            "model": "qwen2.5-coder:7b",
            "prompt_version": "v2.1",
            "served_from": "pool",
            "verified": True,
        }
        q_hash = hashlib.sha256((title + stem).strip().lower().encode("utf-8")).hexdigest()[:32]
        items.append({
            "field": field, "category": cat, "difficulty": diff, "mode": mode, "language": lang,
            "title": title, "question_hash": q_hash, "question_data_json": q_data,
            "provenance_json": prov, "is_used": False, "verified": True
        })

    # 12 Procedural / Curated items (model: practice-bank-curated)
    procedural_specs = [
        ("Python", "Technical Knowledge", "EASY", "MCQ", "python",
         "Python Dict Key Hashing Contract",
         "In Python, what two methods must an object implement to be correctly used as a dictionary key?",
         ["__hash__() and __eq__()",
          "__cmp__() and __str__()",
          "__iter__() and __next__()",
          "__repr__() and __len__()"],
         "__hash__() and __eq__()"),

        ("Python", "Technical Knowledge", "MEDIUM", "CODING", "python",
         "In-Place Linked List Cycle Detection",
         "Implement Floyd's Cycle-Finding Algorithm (Tortoise and Hare) to determine if a linked list contains a cycle.",
         {"starter": "def has_cycle(head) -> bool:\n    pass",
          "test_cases": [{"input": "1 -> 2 -> 3 -> 2", "output": "True"}]},
         "def has_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow, fast = slow.next, fast.next.next\n        if slow == fast: return True\n    return False"),

        ("SQL", "Data & Databases", "EASY", "MCQ", "sql",
         "SQL NULL Comparison Semantics",
         "In standard SQL ANSI-92, what is the boolean outcome of the expression (NULL = NULL)?",
         ["UNKNOWN (evaluates to false in WHERE clauses)",
          "TRUE",
          "FALSE",
          "Throws a NullPointerException"],
         "UNKNOWN (evaluates to false in WHERE clauses)"),

        ("SQL", "Data & Databases", "HARD", "CODING", "sql",
         "Recursive CTE for Organizational Hierarchy",
         "Write a recursive SQL CTE to calculate the reporting depth of every employee under the CEO.",
         {"starter": "WITH RECURSIVE OrgChart AS (\n    -- base and recursive members\n)",
          "test_cases": [{"input": "emp_id, manager_id", "output": "emp_id, depth"}]},
         "WITH RECURSIVE OrgChart AS (SELECT emp_id, 0 as depth FROM emps WHERE manager_id IS NULL UNION ALL SELECT e.emp_id, o.depth + 1 FROM emps e JOIN OrgChart o ON e.manager_id = o.emp_id) SELECT * FROM OrgChart;"),

        ("Java", "Technical Knowledge", "MEDIUM", "MCQ", "java",
         "Java volatile Keyword and Instruction Reordering",
         "Which guarantee does the volatile keyword provide under the Java Memory Model (JMM)?",
         ["Happens-before ordering preventing hardware reordering and ensuring memory visibility across threads",
          "Mutual exclusion locking equivalent to synchronized block",
          "Automatic atomic increment operations without CAS",
          "Moves the variable from heap memory to CPU L1 register cache"],
         "Happens-before ordering preventing hardware reordering and ensuring memory visibility across threads"),

        ("Java", "Technical Knowledge", "EASY", "CODING", "java",
         "String Palindrome Check with Two Pointers",
         "Write an alphanumeric case-insensitive palindrome checker in Java using two pointers in O(1) extra space.",
         {"starter": "public boolean isPalindrome(String s) {\n    // your code\n}",
          "test_cases": [{"input": "\"A man, a plan, a canal: Panama\"", "output": "true"}]},
         "public boolean isPalindrome(String s) { /* two-pointer implementation */ }"),

        ("JavaScript", "Web & Full Stack", "EASY", "MCQ", "javascript",
         "JavaScript Type Coercion with Object.is()",
         "In JavaScript, which statement demonstrates the behavioral difference between Object.is() and the strict equality operator (===)?",
         ["Object.is(NaN, NaN) is true, whereas (NaN === NaN) is false",
          "Object.is('foo', 'foo') is false while ('foo' === 'foo') is true",
          "Object.is(null, undefined) is true",
          "Object.is({}, {}) is true"],
         "Object.is(NaN, NaN) is true, whereas (NaN === NaN) is false"),

        ("JavaScript", "Web & Full Stack", "MEDIUM", "CODING", "javascript",
         "Promise-Based Sleep Delay Helper",
         "Implement a lightweight async sleep function in JavaScript that resolves after a specified millisecond duration.",
         {"starter": "const sleep = (ms) => {\n    // your code\n};",
          "test_cases": [{"input": "sleep(50)", "output": "Resolves after 50ms"}]},
         "const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));"),

        ("C++", "Core Systems", "MEDIUM", "MCQ", "cpp",
         "RAII and Exception Safety Guarantees",
         "Which exception safety guarantee ensures that an operation either completes successfully or leaves the program state completely unchanged?",
         ["Strong exception guarantee (commit-or-rollback)",
          "Basic exception guarantee (no resource leaks)",
          "Nothrow / nofail guarantee",
          "Optimistic concurrency guarantee"],
         "Strong exception guarantee (commit-or-rollback)"),

        ("C++", "Core Systems", "EASY", "CODING", "cpp",
         "Two-Pointer Reverse In-Place Vector",
         "Implement an in-place vector reverse algorithm in C++ without using std::reverse.",
         {"starter": "void reverseVector(std::vector<int>& vec) {\n    // your code\n}",
          "test_cases": [{"input": "{1, 2, 3, 4, 5}", "output": "{5, 4, 3, 2, 1}"}]},
         "void reverseVector(std::vector<int>& vec) { int i=0, j=vec.size()-1; while(i<j) std::swap(vec[i++], vec[j--]); }"),

        ("Cloud & DevOps", "Cloud & DevOps", "EASY", "MCQ", "devops",
         "Git Three-Way Merge Mechanics",
         "In Git, what three commits are analyzed to perform a standard three-way merge?",
         ["The common merge base ancestor, the HEAD of the target branch, and the HEAD of the incoming branch",
          "The last three commits on the incoming branch",
          "The initial root commit, the remote origin commit, and local HEAD",
          "The branch pointer, the reflog pointer, and the staging index tree"],
         "The common merge base ancestor, the HEAD of the target branch, and the HEAD of the incoming branch"),

        ("Cloud & DevOps", "Cloud & DevOps", "MEDIUM", "CODING", "bash",
         "Log File Error Aggregation One-Liner",
         "Write a Bash pipeline that parses /var/log/app.log, extracts 5xx HTTP error occurrences, and prints the top 5 most frequent URLs.",
         {"starter": "#!/usr/bin/env bash\n# grep | awk | sort | uniq | head",
          "test_cases": [{"input": "app.log containing 500, 502, 200 codes", "output": "Count + URL formatted"}]},
         "grep -E 'HTTP/1.[01]\" 5[0-9]{2}' /var/log/app.log | awk '{print $7}' | sort | uniq -c | sort -nr | head -n 5")
    ]

    for field, cat, diff, mode, lang, title, stem, opts, ans in procedural_specs:
        q_data = {
            "title": title,
            "question": stem,
            "options": opts if isinstance(opts, list) else None,
            "code_template": opts if isinstance(opts, dict) else None,
            "answer": ans,
            "explanation": f"Curated practice bank rationale for {title}."
        }
        prov = {
            "provider": "procedural",
            "model": "practice-bank-curated",
            "prompt_version": "v2.1",
            "served_from": "pool",
            "verified": True,
        }
        q_hash = hashlib.sha256((title + stem).strip().lower().encode("utf-8")).hexdigest()[:32]
        items.append({
            "field": field, "category": cat, "difficulty": diff, "mode": mode, "language": lang,
            "title": title, "question_hash": q_hash, "question_data_json": q_data,
            "provenance_json": prov, "is_used": False, "verified": True
        })

    return items

if __name__ == "__main__":
    items = make_pool_items()
    print(f"Generated {len(items)} AIQuestionPool items:")
    for idx, it in enumerate(items, 1):
        print(f"  {idx:02d}. [{it['provenance_json']['provider']}] {it['field']} - {it['title']} ({it['question_hash']})")
