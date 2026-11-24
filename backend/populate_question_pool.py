"""TRELLIS AI Practice Pool Expander & Curated Question Generator.

Populates AIQuestionPool with rich, authentic technical questions across:
- Python (MCQ & CODING)
- Java (MCQ & CODING)
- SQL (MCQ & CODING)
- DSA (MCQ & CODING)
- Web Dev (MCQ & CODING)
- Cloud (MCQ & CODING)
- Data Analytics (MCQ & CODING)
- Aptitude (MCQ & CODING)
"""

import hashlib
import uuid
from typing import Any
from sqlalchemy import select, delete
from app.api.deps import get_sync_engine
from sqlalchemy.orm import Session
from app.models.practice import AIQuestionPool


def compute_hash(txt: str) -> str:
    clean = " ".join((txt or "").strip().lower().split())
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()[:16]


QUESTIONS_CATALOG: list[dict[str, Any]] = [
    # ==================== PYTHON MCQ ====================
    {
        "field": "Python", "mode": "MCQ", "difficulty": "EASY",
        "title": "Python List Comprehensions & Filtration",
        "question": "What is the evaluated output of `[x * 2 for x in range(6) if x % 2 == 0]` in Python 3?",
        "options": ["[0, 4, 8]", "[0, 2, 4]", "[2, 6, 10]", "[0, 4, 16]"],
        "correct_answer": "[0, 4, 8]",
        "explanation": "`range(6)` produces 0, 1, 2, 3, 4, 5. Even elements are 0, 2, 4. Multiplied by 2 they evaluate to 0, 4, 8.",
    },
    {
        "field": "Python", "mode": "MCQ", "difficulty": "EASY",
        "title": "Dictionary Key Hashability Requirement",
        "question": "Which of the following data types CANNOT be used as a dictionary key in Python?",
        "options": ["list", "tuple", "frozenset", "str"],
        "correct_answer": "list",
        "explanation": "Lists are mutable and do not implement a constant __hash__ method; dictionary keys must be hashable.",
    },
    {
        "field": "Python", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "Default Mutable Argument Pitfall",
        "question": "What happens when executing a Python function defined as `def append_item(x, lst=[]): lst.append(x); return lst` across three consecutive calls: `append_item(1)`, `append_item(2)`?",
        "options": [
            "The second call returns [1, 2] because default argument expressions are evaluated once at definition time",
            "The second call returns [2] because default arguments are re-initialized on every invocation",
            "A TypeError is raised because mutable default parameters are forbidden in Python 3",
            "The second call returns [1] because default arguments create immutable copies"
        ],
        "correct_answer": "The second call returns [1, 2] because default argument expressions are evaluated once at definition time",
        "explanation": "Default arguments are bound at function definition time. Subsequent calls mutate the single shared list instance.",
    },
    {
        "field": "Python", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "Python GIL & Multi-Core Concurrency",
        "question": "Which built-in module in Python provides true multi-core parallel execution by spawning distinct operating system processes?",
        "options": ["multiprocessing", "threading", "asyncio", "concurrent.futures.ThreadPoolExecutor"],
        "correct_answer": "multiprocessing",
        "explanation": "`multiprocessing` spawns distinct OS processes with independent Python interpreters and GIL instances.",
    },
    {
        "field": "Python", "mode": "MCQ", "difficulty": "HARD",
        "title": "Metaclass Instantiation Order",
        "question": "In Python, which dunder method is responsible for allocating the memory and returning a new instance of a class before initialization?",
        "options": ["__new__", "__init__", "__call__", "__prepare__"],
        "correct_answer": "__new__",
        "explanation": "`__new__` is the static method called to create the object instance; `__init__` is subsequently called to customize it.",
    },
    {
        "field": "Python", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "Generator Memory Footprint",
        "question": "Why does a generator expression `(x**2 for x in range(10**7))` consume negligible RAM compared to a list comprehension?",
        "options": [
            "Generators compute values lazily on demand during iteration rather than materializing the full sequence in memory",
            "Generators compress numbers in memory using Huffman encoding",
            "Generators offload array elements to temporary disk swap space",
            "Generators run on a background daemon C thread"
        ],
        "correct_answer": "Generators compute values lazily on demand during iteration rather than materializing the full sequence in memory",
        "explanation": "Generators yield one item at a time using iterator protocol, maintaining O(1) space complexity regardless of sequence length.",
    },

    # ==================== JAVA MCQ ====================
    {
        "field": "Java", "mode": "MCQ", "difficulty": "EASY",
        "title": "Java String Pool & Reference Equality",
        "question": "What is the result of `String s1 = \"hello\"; String s2 = new String(\"hello\"); System.out.println(s1 == s2);` in Java?",
        "options": ["false", "true", "Compilation Error", "NullPointerException"],
        "correct_answer": "false",
        "explanation": "`==` checks reference equality. `s1` references the string constant pool, while `new String(...)` allocates a separate heap object.",
    },
    {
        "field": "Java", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "JVM Young Generation & Eden Space",
        "question": "In HotSpot JVM, where are newly instantiated objects initially allocated during normal execution?",
        "options": [
            "Eden Space within the Young Generation",
            "Old / Tenured Generation",
            "Metaspace",
            "Direct Off-Heap Native Buffer"
        ],
        "correct_answer": "Eden Space within the Young Generation",
        "explanation": "New objects reside in Eden. Survivors of Minor GCs are moved to Survivor spaces (S0/S1) before promotion to Tenured.",
    },
    {
        "field": "Java", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "HashMap Treeification in Java 8+",
        "question": "In Java 8 and later, when the number of bucket collisions in a standard HashMap exceeds TREEIFY_THRESHOLD (8), what data structure replaces the linked list?",
        "options": ["Red-Black Tree", "AVL Tree", "B-Tree", "SkipList"],
        "correct_answer": "Red-Black Tree",
        "explanation": "Java 8 converts linked list buckets into balanced Red-Black trees (TreeNode) to improve worst-case lookup from O(n) to O(log n).",
    },
    {
        "field": "Java", "mode": "MCQ", "difficulty": "HARD",
        "title": "Volatile Visibility vs Atomicity",
        "question": "What guarantee does the `volatile` keyword in Java provide regarding multi-threaded memory access?",
        "options": [
            "Guarantees visibility of writes across threads and prevents instruction reordering, but does not guarantee compound atomicity (e.g. count++)",
            "Provides full mutual exclusion locking identical to synchronized blocks",
            "Converts the variable into an immutable atomic reference",
            "Pins the variable to CPU L1 cache exclusively"
        ],
        "correct_answer": "Guarantees visibility of writes across threads and prevents instruction reordering, but does not guarantee compound atomicity (e.g. count++)",
        "explanation": "`volatile` establishes a happens-before relationship ensuring memory visibility, but read-modify-write operations still require atomic primitives.",
    },

    # ==================== SQL MCQ ====================
    {
        "field": "SQL", "mode": "MCQ", "difficulty": "EASY",
        "title": "SQL Group Filtering Clause",
        "question": "Which SQL clause must be used to filter groups of rows aggregated by a GROUP BY statement?",
        "options": ["HAVING", "WHERE", "QUALIFY", "ORDER BY"],
        "correct_answer": "HAVING",
        "explanation": "WHERE filters rows before aggregation; HAVING filters aggregated groups after GROUP BY.",
    },
    {
        "field": "SQL", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "Window Functions vs Group By",
        "question": "What is the key functional difference between `DENSE_RANK()` and `RANK()` in standard SQL?",
        "options": [
            "DENSE_RANK() does not leave gaps in ranking numbers after tied positions, whereas RANK() leaves gaps",
            "RANK() is faster because it does not support partition clauses",
            "DENSE_RANK() can only be used with numeric primary keys",
            "RANK() ignores NULL values whereas DENSE_RANK() raises a syntax error"
        ],
        "correct_answer": "DENSE_RANK() does not leave gaps in ranking numbers after tied positions, whereas RANK() leaves gaps",
        "explanation": "When ties occur (e.g. 1st, 1st), RANK() assigns 3rd to the next row, whereas DENSE_RANK() assigns 2nd.",
    },
    {
        "field": "SQL", "mode": "MCQ", "difficulty": "HARD",
        "title": "Transaction Isolation Levels & Phantom Reads",
        "question": "Which ANSI SQL transaction isolation level completely prevents Dirty Reads, Non-Repeatable Reads, and Phantom Reads?",
        "options": ["SERIALIZABLE", "REPEATABLE READ", "READ COMMITTED", "READ UNCOMMITTED"],
        "correct_answer": "SERIALIZABLE",
        "explanation": "SERIALIZABLE guarantees transactions behave as if executed serially, eliminating phantom rows and concurrency anomalies.",
    },
    {
        "field": "SQL", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "Index Selection & SARGability",
        "question": "Which WHERE clause predicate prevents an existing B-tree index on `created_at` from being effectively utilized (non-SARGable)?",
        "options": [
            "WHERE YEAR(created_at) = 2026",
            "WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'",
            "WHERE created_at = '2026-11-24'",
            "WHERE created_at BETWEEN '2026-01-01' AND '2026-12-31'"
        ],
        "correct_answer": "WHERE YEAR(created_at) = 2026",
        "explanation": "Wrapping the indexed column in a function prevents index range scans; direct range bounds allow index seeks.",
    },

    # ==================== DSA MCQ ====================
    {
        "field": "DSA", "mode": "MCQ", "difficulty": "EASY",
        "title": "Binary Search Worst-Case Time Complexity",
        "question": "What is the worst-case time complexity of searching an element in a sorted array of size N using iterative Binary Search?",
        "options": ["O(log N)", "O(N)", "O(1)", "O(N log N)"],
        "correct_answer": "O(log N)",
        "explanation": "Binary search halves the search space on each iteration, yielding logarithmic O(log N) time.",
    },
    {
        "field": "DSA", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "Shortest Path in Unweighted Graph",
        "question": "Which traversal algorithm is guaranteed to discover the shortest path (minimum edge count) between two vertices in an unweighted graph?",
        "options": [
            "Breadth-First Search (BFS)",
            "Depth-First Search (DFS)",
            "Bellman-Ford Algorithm",
            "Prim's Algorithm"
        ],
        "correct_answer": "Breadth-First Search (BFS)",
        "explanation": "BFS visits vertices level by level in increasing order of distance from the source, guaranteeing minimal edge paths.",
    },
    {
        "field": "DSA", "mode": "MCQ", "difficulty": "HARD",
        "title": "Red-Black Tree Balancing Properties",
        "question": "In a valid Red-Black Tree, what is the maximum possible height of a tree with black-height h?",
        "options": ["2h", "h + 1", "2^h", "h log h"],
        "correct_answer": "2h",
        "explanation": "Because red nodes cannot have red children, the longest possible path alternates red and black nodes, bounding height to <= 2 * black-height.",
    },

    # ==================== WEB DEV MCQ ====================
    {
        "field": "Web Dev", "mode": "MCQ", "difficulty": "EASY",
        "title": "HTTP Method Idempotency",
        "question": "Under RFC 9110, which HTTP request method is explicitly defined as idempotent?",
        "options": ["PUT", "POST", "CONNECT", "PATCH"],
        "correct_answer": "PUT",
        "explanation": "PUT replaces the resource entirely. Sending identical PUT requests repeatedly produces the exact same server state.",
    },
    {
        "field": "Web Dev", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "Event Loop Microtask Execution Order",
        "question": "In JavaScript (V8), when are pending microtasks (e.g. resolved Promise.then callbacks) processed by the event loop?",
        "options": [
            "Immediately after the current call stack clears and before processing the next macrotask or browser paint",
            "At the beginning of the next tick after all setTimeout timers execute",
            "Only when window.requestAnimationFrame is fired",
            "Alternately in 1:1 round robin with macrotasks"
        ],
        "correct_answer": "Immediately after the current call stack clears and before processing the next macrotask or browser paint",
        "explanation": "The microtask queue is completely drained after each execution turn/macrotask before the event loop advances.",
    },
    {
        "field": "Web Dev", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "CORS Preflight Trigger Conditions",
        "question": "Which HTTP header in a cross-origin fetch request triggers an automated CORS preflight OPTIONS request from the browser?",
        "options": [
            "Authorization: Bearer <token>",
            "Accept: application/json",
            "Content-Type: text/plain",
            "Accept-Language: en-US"
        ],
        "correct_answer": "Authorization: Bearer <token>",
        "explanation": "Custom headers such as `Authorization` or non-standard Content-Types make a request non-simple, requiring a preflight check.",
    },

    # ==================== CLOUD MCQ ====================
    {
        "field": "Cloud", "mode": "MCQ", "difficulty": "EASY",
        "title": "Kubernetes Health Checks & Readiness",
        "question": "Which Kubernetes probe signals whether a container has finished booting and is ready to receive network traffic from a Service?",
        "options": ["Readiness Probe", "Liveness Probe", "Startup Probe", "Controller Probe"],
        "correct_answer": "Readiness Probe",
        "explanation": "Failing a Readiness Probe temporarily removes the Pod's IP from Service endpoints without restarting the container.",
    },
    {
        "field": "Cloud", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "Docker Multi-Stage Build Efficiency",
        "question": "What is the primary operational advantage of implementing Docker multi-stage builds?",
        "options": [
            "Compiling in an intermediate stage and copying only the minimal runtime artifacts into the final lightweight image",
            "Allowing multiple Docker daemons to build concurrently on different hosts",
            "Encrypting the file system layers with AES-256",
            "Enabling hot reload of container source code in production"
        ],
        "correct_answer": "Compiling in an intermediate stage and copying only the minimal runtime artifacts into the final lightweight image",
        "explanation": "Multi-stage builds leave behind compilers, SDKs, and build dependencies, drastically shrinking the shipping image size and attack surface.",
    },

    # ==================== DATA ANALYTICS MCQ ====================
    {
        "field": "Data Analytics", "mode": "MCQ", "difficulty": "EASY",
        "title": "Precision vs Recall in High-Risk Scenarios",
        "question": "In fraud detection and medical diagnosis where missing a true positive case carries catastrophic penalties, which metric should be maximized?",
        "options": ["High Recall (Sensitivity)", "High Precision", "High Specificity", "Low Variance"],
        "correct_answer": "High Recall (Sensitivity)",
        "explanation": "Recall measures TP / (TP + FN). Maximizing recall ensures that false negatives are strictly minimized.",
    },
    {
        "field": "Data Analytics", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "L1 (Lasso) vs L2 (Ridge) Regularization",
        "question": "What distinct mathematical feature characterizes L1 (Lasso) regularization over L2 (Ridge) in linear models?",
        "options": [
            "L1 regularization drives irrelevant feature coefficients strictly to zero, performing automatic feature selection",
            "L1 regularization computes derivatives faster than L2",
            "L1 regularization is only applicable to binary classification",
            "L1 regularization never penalizes large weights"
        ],
        "correct_answer": "L1 regularization drives irrelevant feature coefficients strictly to zero, performing automatic feature selection",
        "explanation": "The diamond geometry of L1 penalty creates sparse models by forcing non-essential weights exactly to 0.",
    },

    # ==================== APTITUDE MCQ ====================
    {
        "field": "Aptitude", "mode": "MCQ", "difficulty": "EASY",
        "title": "Work and Time Rates",
        "question": "Person A completes a project in 12 days. Person B completes the same project in 24 days. Working together, how many days will they take to complete the project?",
        "options": ["8 days", "6 days", "10 days", "9 days"],
        "correct_answer": "8 days",
        "explanation": "Rate A = 1/12, Rate B = 1/24. Combined rate = 1/12 + 1/24 = 3/24 = 1/8 work per day. Hence, 8 days.",
    },
    {
        "field": "Aptitude", "mode": "MCQ", "difficulty": "MEDIUM",
        "title": "Relative Speed & Train Crossing",
        "question": "Two trains 150m and 100m long travel towards each other on parallel tracks at 54 km/h and 36 km/h. How many seconds do they take to completely pass each other from the moment they meet?",
        "options": ["10 seconds", "12 seconds", "15 seconds", "8 seconds"],
        "correct_answer": "10 seconds",
        "explanation": "Relative speed = 54 + 36 = 90 km/h = 90 * (5/18) = 25 m/s. Total distance = 150 + 100 = 250m. Time = 250 / 25 = 10 seconds.",
    },

    # ==================== PYTHON CODING PROBLEMS ====================
    {
        "field": "Python", "mode": "CODING", "difficulty": "EASY",
        "title": "Palindrome String Verification",
        "question": "Given a string read from standard input, determine if it is a palindrome considering only alphanumeric characters and ignoring cases. Output 'true' or 'false'.",
        "language": "python",
        "starter_code": {"python": "import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    # Implement here\n\nif __name__ == '__main__':\n    solve()"},
        "reference_solution": "import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    filtered = [c.lower() for c in s if c.isalnum()]\n    print('true' if filtered == filtered[::-1] else 'false')\n\nif __name__ == '__main__':\n    solve()",
        "test_cases": [
            {"input_data": "A man, a plan, a canal: Panama", "expected_output": "true", "is_hidden": False, "weight": 1.0},
            {"input_data": "race a car", "expected_output": "false", "is_hidden": False, "weight": 1.0},
            {"input_data": "Madam, in Eden, I'm Adam", "expected_output": "true", "is_hidden": True, "weight": 2.0},
        ],
    },
    {
        "field": "Python", "mode": "CODING", "difficulty": "EASY",
        "title": "Array Element Frequency Counter",
        "question": "Given an array of space-separated integers on standard input, print the element that appears most frequently. If there is a tie, print the smallest integer among them.",
        "language": "python",
        "starter_code": {"python": "import sys\n\ndef solve():\n    nums = list(map(int, sys.stdin.read().strip().split()))\n    # Implement here\n\nif __name__ == '__main__':\n    solve()"},
        "reference_solution": "import sys\nfrom collections import Counter\n\ndef solve():\n    raw = sys.stdin.read().strip()\n    if not raw: return\n    nums = list(map(int, raw.split()))\n    counts = Counter(nums)\n    max_freq = max(counts.values())\n    best = min([k for k, v in counts.items() if v == max_freq])\n    print(best)\n\nif __name__ == '__main__':\n    solve()",
        "test_cases": [
            {"input_data": "1 3 2 1 4 1", "expected_output": "1", "is_hidden": False, "weight": 1.0},
            {"input_data": "4 4 2 2 3", "expected_output": "2", "is_hidden": False, "weight": 1.0},
            {"input_data": "9 9 9 8 8 8 1 1 1", "expected_output": "1", "is_hidden": True, "weight": 2.0},
        ],
    },

    # ==================== SQL CODING PROBLEMS ====================
    {
        "field": "SQL", "mode": "CODING", "difficulty": "MEDIUM",
        "title": "Department Salary Threshold Aggregation",
        "question": "Write a SQL query to find the department and total payroll for departments with at least 2 employees and total salary exceeding 100,000. Output columns: department, total_payroll ordered by total_payroll DESC.",
        "language": "sql",
        "starter_code": {"sql": "SELECT department, SUM(salary) AS total_payroll FROM employees GROUP BY department"},
        "reference_solution": "SELECT department, SUM(salary) AS total_payroll FROM employees GROUP BY department HAVING COUNT(*) >= 2 AND SUM(salary) > 100000 ORDER BY total_payroll DESC",
        "test_cases": [
            {
                "input_data": "CREATE TABLE employees (id INT, department TEXT, salary INT); INSERT INTO employees VALUES (1, 'Engineering', 90000), (2, 'Engineering', 85000), (3, 'HR', 45000), (4, 'HR', 40000);",
                "expected_output": "Engineering|175000",
                "is_hidden": False,
                "weight": 1.0
            },
            {
                "input_data": "CREATE TABLE employees (id INT, department TEXT, salary INT); INSERT INTO employees VALUES (1, 'Sales', 60000), (2, 'Sales', 70000), (3, 'Finance', 120000);",
                "expected_output": "Sales|130000",
                "is_hidden": True,
                "weight": 1.0
            }
        ]
    },

    # ==================== JAVA CODING PROBLEMS ====================
    {
        "field": "Java", "mode": "CODING", "difficulty": "EASY",
        "title": "Array Running Sum Prefix",
        "question": "Given an array of integers read from standard input as space-separated integers on a single line, compute the running sum of the array where runningSum[i] = sum(nums[0]...nums[i]). Print the running sum as space-separated integers.",
        "language": "java",
        "starter_code": {"java": "import java.util.Scanner;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextLine()) return;\n        String[] parts = sc.nextLine().trim().split(\"\\\\s+\");\n        // Solution here\n    }\n}"},
        "reference_solution": "import java.util.Scanner;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextLine()) return;\n        String line = sc.nextLine().trim();\n        if (line.isEmpty()) return;\n        String[] parts = line.split(\"\\\\s+\");\n        int sum = 0;\n        StringBuilder sb = new StringBuilder();\n        for (int i = 0; i < parts.length; i++) {\n            sum += Integer.parseInt(parts[i]);\n            sb.append(sum);\n            if (i < parts.length - 1) sb.append(\" \");\n        }\n        System.out.println(sb.toString());\n    }\n}",
        "test_cases": [
            {"input_data": "1 2 3 4", "expected_output": "1 3 6 10", "is_hidden": False, "weight": 1.0},
            {"input_data": "3 1 2 10 1", "expected_output": "3 4 6 16 17", "is_hidden": True, "weight": 2.0},
        ]
    },

    # ==================== JAVASCRIPT CODING PROBLEMS ====================
    {
        "field": "Web Dev", "mode": "CODING", "difficulty": "EASY",
        "title": "Array Chunking Utility",
        "question": "Given an array of integers and a chunk size k from standard input (first line: space-separated integers; second line: chunk size integer k), split the array into sub-arrays of maximum size k. Print each chunk on a new line as comma-separated integers.",
        "language": "javascript",
        "starter_code": {"javascript": "const fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim().split('\\n');\n// Solution here"},
        "reference_solution": "const fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim().split('\\n');\nif (input.length >= 2 && input[0].trim().length > 0) {\n    const nums = input[0].trim().split(/\\s+/).map(Number);\n    const k = parseInt(input[1].trim(), 10);\n    for (let i = 0; i < nums.length; i += k) {\n        console.log(nums.slice(i, i + k).join(','));\n    }\n}",
        "test_cases": [
            {"input_data": "1 2 3 4 5\n2", "expected_output": "1,2\n3,4\n5", "is_hidden": False, "weight": 1.0},
            {"input_data": "10 20 30\n3", "expected_output": "10,20,30", "is_hidden": True, "weight": 1.0},
        ]
    }
]


def populate_pool() -> None:
    engine = get_sync_engine()
    db = Session(engine)
    try:
        inserted = 0
        for item in QUESTIONS_CATALOG:
            q_text = item.get("question") or item.get("statement") or ""
            q_hash = compute_hash(q_text)

            existing = db.execute(
                select(AIQuestionPool).where(AIQuestionPool.question_hash == q_hash)
            ).scalar_one_or_none()

            q_data = {
                "title": item["title"],
                "question": q_text,
                "statement": q_text,
                "difficulty": item["difficulty"],
                "field": item["field"],
                "options": item.get("options", []),
                "correct_answer": item.get("correct_answer"),
                "explanation": item.get("explanation", ""),
                "hints": [
                    "Review algorithmic edge conditions and constraints.",
                    "Verify behavior on boundary values and empty input collections."
                ],
                "question_hash": q_hash,
            }
            if item["mode"] == "CODING":
                q_data.update({
                    "language": item.get("language", "python"),
                    "starter_code": item.get("starter_code", {}),
                    "reference_solution": item.get("reference_solution", ""),
                    "test_cases": item.get("test_cases", []),
                    "constraints": "Standard execution limits (Time: 2000ms, Memory: 64MB)"
                })

            if not existing:
                pool_entry = AIQuestionPool(
                    id=str(uuid.uuid4()),
                    field=item["field"],
                    category="Technical Knowledge",
                    difficulty=item["difficulty"],
                    mode=item["mode"],
                    language=item.get("language", "python" if item["mode"] == "CODING" else None),
                    title=item["title"],
                    question_hash=q_hash,
                    question_data_json=q_data,
                    provenance_json={"provider": "curated", "served_from": "pool", "verified": True},
                    is_used=False,
                    verified=True
                )
                db.add(pool_entry)
                inserted += 1

        db.commit()
        print(f"Successfully populated AIQuestionPool: added {inserted} new questions. Total catalog size: {len(QUESTIONS_CATALOG)}")
    finally:
        db.close()


if __name__ == "__main__":
    populate_pool()
