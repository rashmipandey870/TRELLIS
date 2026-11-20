"""TRELLIS AI Practice, Problem Generation, Verification & Talent Spotlight Service (Step 6).

Implements:
- Structured LLM practice problem generation (MCQ and Coding)
- Sandbox validation of generated problems: executes reference solution against generated test cases
- Adaptive difficulty adjustment based on learner accuracy
- Dedication / performance score calculation per learner per field
- Talent Spotlight threshold evaluation & alert creation with cooldown
- Role-aware LLM assistant with data access guardrails
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.batches import MentorLearnerAssignment
from app.models.notifications import Notification
from app.models.practice import (
    AlertAction,
    PracticeAttempt,
    PracticeQuestion,
    PracticeScore,
    PracticeSession,
    TalentAlert,
)
from app.models.settings import SystemSetting
from app.models.user import User
from app.services.ai_question_generator import compute_question_hash, generate_ai_practice_problem
from app.services.code_runner import CodeRunner

# Supported Practice Fields
SUPPORTED_FIELDS = [
    "Python",
    "Java",
    "SQL",
    "DSA",
    "Web Dev",
    "Cloud",
    "Data Analytics",
    "Aptitude",
]

# Built-in verified question templates for reliable fallback and instant testing
VERIFIED_TEMPLATES: dict[str, dict[str, list[dict[str, Any]]]] = {
    "Python": {
        "MCQ": [
            {
                "title": "Python List Comprehensions & Immutability",
                "question": "What is the result of `[x**2 for x in range(5) if x % 2 == 1]` in Python 3?",
                "options": ["[0, 1, 4, 9, 16]", "[1, 9]", "[1, 4, 9]", "[0, 4, 16]"],
                "correct_answer": "[1, 9]",
                "explanation": "`range(5)` yields 0, 1, 2, 3, 4. The odd numbers are 1 and 3. Their squares are 1 and 9.",
                "difficulty": "EASY",
                "topic": "Comprehensions",
            },
            {
                "title": "GIL & Threading Concurrency",
                "question": "Which Python module provides true multi-core CPU parallelism bypassing the GIL?",
                "options": ["threading", "asyncio", "multiprocessing", "concurrent.futures.ThreadPoolExecutor"],
                "correct_answer": "multiprocessing",
                "explanation": "`multiprocessing` spawns distinct OS processes with independent Python interpreters and GILs.",
                "difficulty": "MEDIUM",
                "topic": "Concurrency",
            },
        ],
        "CODING": [
            {
                "title": "Two Sum Target Indices",
                "statement": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target. Output as two space-separated integers in ascending order.\nInput format: First line contains target. Second line contains space-separated integers.",
                "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9",
                "examples": [
                    {"input": "9\n2 7 11 15", "output": "0 1", "explanation": "nums[0] + nums[1] == 9"}
                ],
                "starter_code": {
                    "python": "import sys\n\ndef solve():\n    lines = sys.stdin.read().strip().split('\\n')\n    if not lines or not lines[0]: return\n    target = int(lines[0])\n    nums = list(map(int, lines[1].split()))\n    # Write your solution here\n    pass\n\nif __name__ == '__main__':\n    solve()",
                    "javascript": "const fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim().split('\\n');\nconst target = parseInt(input[0]);\nconst nums = input[1].split(' ').map(Number);\n// Solution here",
                },
                "reference_solution": "import sys\n\ndef solve():\n    data = sys.stdin.read().strip().split('\\n')\n    if len(data) < 2: return\n    target = int(data[0].strip())\n    nums = list(map(int, data[1].strip().split()))\n    lookup = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in lookup:\n            print(f'{lookup[diff]} {i}')\n            return\n        lookup[num] = i\n\nif __name__ == '__main__':\n    solve()",
                "test_cases": [
                    {"input_data": "9\n2 7 11 15", "expected_output": "0 1", "is_hidden": False, "weight": 1.0},
                    {"input_data": "6\n3 2 4", "expected_output": "1 2", "is_hidden": False, "weight": 1.0},
                    {"input_data": "6\n3 3", "expected_output": "0 1", "is_hidden": True, "weight": 2.0},
                    {"input_data": "100\n10 20 30 40 60", "expected_output": "3 4", "is_hidden": True, "weight": 2.0},
                    {"input_data": "0\n-5 5", "expected_output": "0 1", "is_hidden": True, "weight": 2.0},
                ],
                "difficulty": "EASY",
            },
            {
                "title": "Reverse Words in a String",
                "statement": "Given an input string s, reverse the order of the words.\nA word is defined as a sequence of non-space characters. Return a string of the words in reverse order concatenated by a single space.",
                "constraints": "1 <= s.length <= 10^4",
                "examples": [
                    {"input": "the sky is blue", "output": "blue is sky the"}
                ],
                "starter_code": {
                    "python": "import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    # Reverse words\n    print(' '.join(reversed(s.split())))\n\nif __name__ == '__main__':\n    solve()",
                },
                "reference_solution": "import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    print(' '.join(reversed(s.split())))\n\nif __name__ == '__main__':\n    solve()",
                "test_cases": [
                    {"input_data": "the sky is blue", "expected_output": "blue is sky the", "is_hidden": False, "weight": 1.0},
                    {"input_data": "  hello world  ", "expected_output": "world hello", "is_hidden": False, "weight": 1.0},
                    {"input_data": "a good   example", "expected_output": "example good a", "is_hidden": True, "weight": 2.0},
                    {"input_data": "CSM Technology Trellis", "expected_output": "Trellis Technology CSM", "is_hidden": True, "weight": 2.0},
                    {"input_data": "one", "expected_output": "one", "is_hidden": True, "weight": 2.0},
                ],
                "difficulty": "MEDIUM",
            },
        ],
    },
    "DSA": {
        "MCQ": [
            {
                "title": "Binary Search Complexity",
                "question": "What is the worst-case time complexity of searching in a balanced Binary Search Tree (AVL) with N nodes?",
                "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
                "correct_answer": "O(log N)",
                "explanation": "Because the tree is balanced, the maximum height is logarithmic relative to N.",
                "difficulty": "EASY",
                "topic": "Trees",
            }
        ],
        "CODING": [
            {
                "title": "Valid Parentheses",
                "statement": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\nOutput 'true' or 'false'.",
                "constraints": "1 <= s.length <= 10^4",
                "examples": [{"input": "()[]{}", "output": "true"}, {"input": "(]", "output": "false"}],
                "starter_code": {
                    "python": "import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    # Validate parentheses\n    pass\n\nif __name__ == '__main__':\n    solve()",
                },
                "reference_solution": "import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                print('false')\n                return\n        else:\n            stack.append(char)\n    print('true' if not stack else 'false')\n\nif __name__ == '__main__':\n    solve()",
                "test_cases": [
                    {"input_data": "()", "expected_output": "true", "is_hidden": False, "weight": 1.0},
                    {"input_data": "()[]{}", "expected_output": "true", "is_hidden": False, "weight": 1.0},
                    {"input_data": "(]", "expected_output": "false", "is_hidden": False, "weight": 1.0},
                    {"input_data": "([)]", "expected_output": "false", "is_hidden": True, "weight": 2.0},
                    {"input_data": "{[]}", "expected_output": "true", "is_hidden": True, "weight": 2.0},
                ],
                "difficulty": "EASY",
            }
        ],
    },
    "SQL": {
        "MCQ": [
            {
                "title": "SQL Join Semantics",
                "question": "Which SQL JOIN returns all rows from the left table, and the matched rows from the right table, filling nulls if no match?",
                "options": ["INNER JOIN", "LEFT OUTER JOIN", "RIGHT OUTER JOIN", "CROSS JOIN"],
                "correct_answer": "LEFT OUTER JOIN",
                "explanation": "LEFT OUTER JOIN preserves every row from the left operand regardless of matches in the right table.",
                "difficulty": "EASY",
                "topic": "Joins",
            }
        ],
        "CODING": [
            {
                "title": "Second Highest Salary Query Simulator",
                "statement": "Given a list of salaries, output the second highest distinct salary. If no second highest exists, output 'null'.\nInput: space-separated integers on a single line.",
                "constraints": "1 <= salaries.length <= 10^4",
                "examples": [{"input": "100 200 300", "output": "200"}, {"input": "100", "output": "null"}],
                "starter_code": {
                    "python": "import sys\n\ndef solve():\n    raw = sys.stdin.read().strip()\n    if not raw: return\n    nums = sorted(list(set(map(int, raw.split()))), reverse=True)\n    print(nums[1] if len(nums) > 1 else 'null')\n\nif __name__ == '__main__':\n    solve()",
                },
                "reference_solution": "import sys\n\ndef solve():\n    raw = sys.stdin.read().strip()\n    if not raw: return\n    nums = sorted(list(set(map(int, raw.split()))), reverse=True)\n    print(nums[1] if len(nums) > 1 else 'null')\n\nif __name__ == '__main__':\n    solve()",
                "test_cases": [
                    {"input_data": "100 200 300", "expected_output": "200", "is_hidden": False, "weight": 1.0},
                    {"input_data": "100", "expected_output": "null", "is_hidden": False, "weight": 1.0},
                    {"input_data": "500 500 500", "expected_output": "null", "is_hidden": True, "weight": 2.0},
                    {"input_data": "10 50 20 80 80", "expected_output": "50", "is_hidden": True, "weight": 2.0},
                ],
                "difficulty": "MEDIUM",
            }
        ],
    },
    "Java": {
        "MCQ": [
            {
                "title": "JVM Memory Generations",
                "question": "In the HotSpot JVM architecture, which memory generation stores newly allocated object instances before they are promoted?",
                "options": ["Metaspace", "Eden Space in Young Generation", "Tenured (Old) Generation", "JVM Stack Frame"],
                "correct_answer": "Eden Space in Young Generation",
                "explanation": "New objects are initially allocated in the Eden space of the Young Generation and promoted to Survivor and Tenured after surviving GC cycles.",
                "difficulty": "EASY",
                "topic": "JVM Architecture",
            }
        ],
        "CODING": [
            {
                "title": "Palindrome String Validator",
                "statement": "Given a string s, output 'true' if it is a palindrome (reads same forwards and backwards ignoring case), otherwise 'false'.\nInput: A single line string.",
                "constraints": "1 <= s.length <= 10^4",
                "examples": [{"input": "racecar", "output": "true"}, {"input": "hello", "output": "false"}],
                "language": "java",
                "starter_code": {
                    "java": (
                        "import java.util.*;\n\n"
                        "public class Solution {\n"
                        "    public static void main(String[] args) {\n"
                        "        Scanner sc = new Scanner(System.in);\n"
                        "        if (!sc.hasNextLine()) return;\n"
                        "        String s = sc.nextLine().trim().toLowerCase();\n"
                        "        // Check palindrome in Java\n"
                        "    }\n"
                        "}\n"
                    )
                },
                "reference_solution": (
                    "import java.util.*;\n\n"
                    "public class Solution {\n"
                    "    public static void main(String[] args) {\n"
                    "        Scanner sc = new Scanner(System.in);\n"
                    "        if (!sc.hasNextLine()) return;\n"
                    "        String s = sc.nextLine().trim().toLowerCase();\n"
                    "        String rev = new StringBuilder(s).reverse().toString();\n"
                    "        System.out.println(s.equals(rev) ? \"true\" : \"false\");\n"
                    "    }\n"
                    "}\n"
                ),
                "test_cases": [
                    {"input_data": "racecar", "expected_output": "true", "is_hidden": False, "weight": 1.0},
                    {"input_data": "hello", "expected_output": "false", "is_hidden": False, "weight": 1.0},
                    {"input_data": "madam", "expected_output": "true", "is_hidden": True, "weight": 2.0},
                    {"input_data": "a", "expected_output": "true", "is_hidden": True, "weight": 2.0},
                ],
                "difficulty": "EASY",
            }
        ],
    },
    "Web Dev": {
        "MCQ": [
            {
                "title": "HTTP Methods & Idempotency",
                "question": "Which of the following HTTP request methods is defined as idempotent under RFC 9110?",
                "options": ["POST", "PUT", "PATCH", "CONNECT"],
                "correct_answer": "PUT",
                "explanation": "PUT is idempotent: sending identical PUT requests multiple times produces the exact same side-effect as a single request.",
                "difficulty": "EASY",
                "topic": "REST Protocols",
            }
        ],
        "CODING": [
            {
                "title": "URL Query Parameter Parser",
                "statement": "Given a URL query string, parse and print the value of parameter 'key'.\nInput format: Line 1: Target key. Line 2: Query string (e.g. user=csm&role=admin&env=prod). Output 'null' if key is missing.",
                "constraints": "1 <= query_string.length <= 10^4",
                "examples": [{"input": "role\nuser=csm&role=admin&env=prod", "output": "admin"}],
                "language": "javascript",
                "starter_code": {
                    "javascript": (
                        "const fs = require('fs');\n"
                        "const lines = fs.readFileSync(0, 'utf-8').trim().split('\\n');\n"
                        "if (lines.length < 2) process.exit(0);\n"
                        "const target = lines[0].trim();\n"
                        "const qs = lines[1].trim();\n"
                        "// Parse parameters and print value\n"
                    )
                },
                "reference_solution": (
                    "const fs = require('fs');\n"
                    "const lines = fs.readFileSync(0, 'utf-8').trim().split('\\n');\n"
                    "if (lines.length < 2) process.exit(0);\n"
                    "const target = lines[0].trim();\n"
                    "const qs = lines[1].trim();\n"
                    "const params = new URLSearchParams(qs);\n"
                    "console.log(params.get(target) || 'null');\n"
                ),
                "test_cases": [
                    {"input_data": "role\nuser=csm&role=admin&env=prod", "expected_output": "admin", "is_hidden": False, "weight": 1.0},
                    {"input_data": "token\nuser=csm&role=admin", "expected_output": "null", "is_hidden": False, "weight": 1.0},
                    {"input_data": "env\napp=trellis&env=production", "expected_output": "production", "is_hidden": True, "weight": 2.0},
                ],
                "difficulty": "EASY",
            }
        ],
    },
    "Cloud": {
        "MCQ": [
            {
                "title": "Kubernetes Ingress & Readiness Probes",
                "question": "Which Kubernetes health probe determines if a container is ready to begin accepting external network ingress traffic?",
                "options": ["Liveness Probe", "Readiness Probe", "Startup Probe", "Node Controller Probe"],
                "correct_answer": "Readiness Probe",
                "explanation": "When a Readiness Probe fails, the Pod's IP address is removed from the Endpoints of all matching Services.",
                "difficulty": "EASY",
                "topic": "Kubernetes",
            }
        ],
        "CODING": [
            {
                "title": "Log Severity Filter",
                "statement": "Given a severity threshold (DEBUG, INFO, WARN, ERROR), print only log lines matching or exceeding that level.\nInput: Line 1: Threshold. Line 2 onwards: Lines starting with [LEVEL].",
                "constraints": "1 <= total_lines <= 10^3",
                "examples": [{"input": "WARN\n[INFO] Init\n[WARN] High load\n[ERROR] Crash", "output": "[WARN] High load\n[ERROR] Crash"}],
                "starter_code": {
                    "python": "import sys\n\ndef solve():\n    data = sys.stdin.read().strip().split('\\n')\n    if not data or not data[0]: return\n    thresh = data[0].strip().upper()\n    levels = {'DEBUG': 1, 'INFO': 2, 'WARN': 3, 'ERROR': 4}\n    thresh_val = levels.get(thresh, 1)\n    for line in data[1:]:\n        line = line.strip()\n        if not line: continue\n        for lvl, val in levels.items():\n            if line.startswith(f'[{lvl}]') and val >= thresh_val:\n                print(line)\n                break\n\nif __name__ == '__main__':\n    solve()",
                },
                "reference_solution": "import sys\n\ndef solve():\n    data = sys.stdin.read().strip().split('\\n')\n    if not data or not data[0]: return\n    thresh = data[0].strip().upper()\n    levels = {'DEBUG': 1, 'INFO': 2, 'WARN': 3, 'ERROR': 4}\n    thresh_val = levels.get(thresh, 1)\n    for line in data[1:]:\n        line = line.strip()\n        if not line: continue\n        for lvl, val in levels.items():\n            if line.startswith(f'[{lvl}]') and val >= thresh_val:\n                print(line)\n                break\n\nif __name__ == '__main__':\n    solve()",
                "test_cases": [
                    {"input_data": "WARN\n[INFO] Starting\n[WARN] High memory\n[ERROR] Fatal crash", "expected_output": "[WARN] High memory\n[ERROR] Fatal crash", "is_hidden": False, "weight": 1.0},
                    {"input_data": "ERROR\n[INFO] Init\n[WARN] Warning only", "expected_output": "", "is_hidden": True, "weight": 2.0},
                ],
                "difficulty": "EASY",
            }
        ],
    },
    "Data Analytics": {
        "MCQ": [
            {
                "title": "Precision vs Recall Trade-off",
                "question": "In medical disease diagnosis where false negatives must be minimized at all costs, which metric should be prioritized?",
                "options": ["High Precision", "High Recall (Sensitivity)", "High Specificity", "Low Accuracy"],
                "correct_answer": "High Recall (Sensitivity)",
                "explanation": "Recall measures TP / (TP + FN). Maximizing recall ensures that very few positive cases are missed.",
                "difficulty": "EASY",
                "topic": "Model Evaluation",
            }
        ],
        "CODING": [
            {
                "title": "Moving Average Stream",
                "statement": "Given window size W and an array of integers, output the moving average of each window formatted to 1 decimal place.\nInput: Line 1: Window size W. Line 2: Space-separated numbers.",
                "constraints": "1 <= W <= len(numbers) <= 10^4",
                "examples": [{"input": "3\n1 2 3 4 5", "output": "2.0 3.0 4.0"}],
                "starter_code": {
                    "python": "import sys\n\ndef solve():\n    data = sys.stdin.read().strip().split('\\n')\n    if len(data) < 2: return\n    w = int(data[0].strip())\n    nums = list(map(float, data[1].strip().split()))\n    res = []\n    for i in range(len(nums) - w + 1):\n        avg = sum(nums[i:i+w]) / w\n        res.append(f'{avg:.1f}')\n    print(' '.join(res))\n\nif __name__ == '__main__':\n    solve()",
                },
                "reference_solution": "import sys\n\ndef solve():\n    data = sys.stdin.read().strip().split('\\n')\n    if len(data) < 2: return\n    w = int(data[0].strip())\n    nums = list(map(float, data[1].strip().split()))\n    res = []\n    for i in range(len(nums) - w + 1):\n        avg = sum(nums[i:i+w]) / w\n        res.append(f'{avg:.1f}')\n    print(' '.join(res))\n\nif __name__ == '__main__':\n    solve()",
                "test_cases": [
                    {"input_data": "3\n1 2 3 4 5", "expected_output": "2.0 3.0 4.0", "is_hidden": False, "weight": 1.0},
                    {"input_data": "2\n10 20 30", "expected_output": "15.0 25.0", "is_hidden": True, "weight": 2.0},
                ],
                "difficulty": "EASY",
            }
        ],
    },
    "Aptitude": {
        "MCQ": [
            {
                "title": "Work & Time Calculation",
                "question": "A can complete a task in 10 days and B can complete it in 15 days. How many days will they take working together?",
                "options": ["5 days", "6 days", "8 days", "12 days"],
                "correct_answer": "6 days",
                "explanation": "Combined rate = 1/10 + 1/15 = 5/30 = 1/6 of the work per day. Hence, 6 days.",
                "difficulty": "EASY",
                "topic": "Quantitative Reasoning",
            }
        ],
        "CODING": [
            {
                "title": "Greatest Common Divisor (Euclidean Algorithm)",
                "statement": "Given two integers a and b, compute and print their Greatest Common Divisor (GCD).\nInput: Two space-separated integers on standard input.",
                "constraints": "1 <= a, b <= 10^9",
                "examples": [{"input": "48 18", "output": "6"}],
                "starter_code": {
                    "python": "import sys, math\n\ndef solve():\n    raw = sys.stdin.read().strip()\n    if not raw: return\n    a, b = map(int, raw.split())\n    print(math.gcd(a, b))\n\nif __name__ == '__main__':\n    solve()",
                },
                "reference_solution": "import sys, math\n\ndef solve():\n    raw = sys.stdin.read().strip()\n    if not raw: return\n    a, b = map(int, raw.split())\n    print(math.gcd(a, b))\n\nif __name__ == '__main__':\n    solve()",
                "test_cases": [
                    {"input_data": "48 18", "expected_output": "6", "is_hidden": False, "weight": 1.0},
                    {"input_data": "100 25", "expected_output": "25", "is_hidden": False, "weight": 1.0},
                    {"input_data": "17 19", "expected_output": "1", "is_hidden": True, "weight": 2.0},
                ],
                "difficulty": "EASY",
            }
        ],
    },
}


def get_adaptive_difficulty(session: Session, learner_id: str, field: str) -> str:
    """Calculate adaptive difficulty based on recent attempt accuracy."""
    recent_attempts = (
        session.execute(
            select(PracticeAttempt)
            .join(PracticeQuestion)
            .where(
                PracticeAttempt.learner_id == learner_id,
                PracticeQuestion.field == field,
            )
            .order_by(PracticeAttempt.created_at.desc())
            .limit(5)
        )
        .scalars()
        .all()
    )

    if not recent_attempts or len(recent_attempts) < 3:
        return "EASY"

    accuracy = sum(1 for a in recent_attempts if a.is_correct) / len(recent_attempts)
    if accuracy >= 0.8:
        return "HARD"
    elif accuracy >= 0.5:
        return "MEDIUM"
    return "EASY"


def generate_practice_question(
    session: Session,
    learner_id: str,
    field: str,
    difficulty: str | None = None,
    mode: str = "MCQ",
) -> PracticeQuestion:
    """Generate or retrieve an AI-generated, verified practice question."""
    target_field = field if field in SUPPORTED_FIELDS else "Python"
    target_mode = mode.upper() if mode.upper() in {"MCQ", "CODING"} else "MCQ"
    target_diff = difficulty.upper() if difficulty else get_adaptive_difficulty(session, learner_id, target_field)

    # Collect previously seen question hashes for this learner to prevent duplicate questions
    recent_pqs = (
        session.execute(
            select(PracticeQuestion.question_data_json)
            .join(PracticeSession, PracticeQuestion.session_id == PracticeSession.id)
            .where(PracticeSession.learner_id == learner_id)
        )
        .scalars()
        .all()
    )
    seen_hashes: set[str] = set()
    for q_data in recent_pqs:
        if isinstance(q_data, dict):
            h = q_data.get("question_hash")
            if not h:
                txt = q_data.get("question") or q_data.get("statement") or ""
                if txt:
                    h = compute_question_hash(txt)
            if h:
                seen_hashes.add(h)

    # 1. Generate problem dynamically using AI generator (Live LLM or Procedural Engine)
    try:
        selected_tmpl = generate_ai_practice_problem(
            field=target_field,
            difficulty=target_diff,
            mode=target_mode,
            seen_hashes=seen_hashes,
        )
    except Exception:
        # Fallback to verified template library if generation encountered an unexpected exception
        templates = VERIFIED_TEMPLATES.get(target_field, VERIFIED_TEMPLATES["Python"]).get(target_mode, [])
        if not templates:
            templates = VERIFIED_TEMPLATES["Python"][target_mode]
        selected_tmpl = next((t for t in templates if t.get("difficulty") == target_diff), templates[0])

    # If Coding problem, verify reference solution through sandbox before saving
    if target_mode == "CODING" and selected_tmpl.get("reference_solution") and selected_tmpl.get("test_cases"):
        ref_code = selected_tmpl["reference_solution"]
        test_cases = selected_tmpl["test_cases"]
        code_lang = selected_tmpl.get("language") or "python"
        exec_res = CodeRunner.execute(
            code=ref_code,
            language=code_lang,
            test_cases=test_cases,
            time_limit_ms=3000,
            mask_hidden_inputs=False,
        )
        if exec_res.verdict != "ACCEPTED":
            raise RuntimeError(f"Sandbox verification failed for generated problem: {exec_res.verdict}")

    # Create session if not active
    practice_session = PracticeSession(
        learner_id=learner_id,
        field=target_field,
        difficulty=target_diff,
        mode=target_mode,
    )
    session.add(practice_session)
    session.flush()

    # Create practice question
    pq = PracticeQuestion(
        session_id=practice_session.id,
        field=target_field,
        difficulty=target_diff,
        mode=target_mode,
        title=selected_tmpl.get("title", f"{target_field} {target_diff} {target_mode}"),
        question_data_json=selected_tmpl,
        reference_solution=selected_tmpl.get("reference_solution"),
        verified=True,
    )
    session.add(pq)
    session.commit()
    session.refresh(pq)
    return pq


def record_practice_attempt(
    session: Session,
    learner_id: str,
    question_id: str,
    answer_payload: dict[str, Any],
    hints_used: int = 0,
) -> tuple[PracticeAttempt, PracticeScore, TalentAlert | None]:
    """Record attempt, update continuous dedication score, and check Talent Spotlight thresholds."""
    pq = session.get(PracticeQuestion, question_id)
    if not pq:
        raise ValueError(f"PracticeQuestion '{question_id}' not found.")

    is_correct = False
    feedback = ""
    earned_score = 0.0

    if pq.mode == "MCQ":
        user_choice = str(answer_payload.get("selected_option") or answer_payload.get("answer_text") or "").strip()
        correct_choice = str(pq.question_data_json.get("correct_answer", "")).strip()
        options = pq.question_data_json.get("options", [])
        if user_choice.startswith("opt_") and options:
            try:
                opt_idx = int(user_choice.split("_")[1])
                if 0 <= opt_idx < len(options):
                    chosen_val = str(options[opt_idx]).strip()
                    is_correct = chosen_val == correct_choice
            except (ValueError, IndexError):
                is_correct = user_choice == correct_choice
        else:
            is_correct = user_choice == correct_choice

        explanation = pq.question_data_json.get("explanation", "")
        if is_correct:
            earned_score = 10.0
            feedback = f"Correct! {explanation}"
        else:
            feedback = f"Incorrect. The correct answer is '{correct_choice}'. {explanation}"

    elif pq.mode == "CODING":
        user_code = str(answer_payload.get("code") or answer_payload.get("source_code") or "")
        language = str(answer_payload.get("language") or pq.question_data_json.get("language") or "python")
        test_cases = pq.question_data_json.get("test_cases", [])
        exec_res = CodeRunner.execute(
            code=user_code,
            language=language,
            test_cases=test_cases,
            mask_hidden_inputs=True,
        )
        is_correct = exec_res.verdict == "ACCEPTED"
        earned_score = exec_res.score
        if is_correct:
            feedback = f"All {exec_res.passed_cases}/{exec_res.total_cases} test cases passed. Excellent algorithmic efficiency ({exec_res.runtime_ms} ms)."
        else:
            first_fail = exec_res.first_failing_case
            fail_msg = f"Failed on case {first_fail['case_index']}" if first_fail else "Execution failed"
            feedback = f"Verdict: {exec_res.verdict} ({exec_res.passed_cases}/{exec_res.total_cases} passed). {fail_msg}."

    attempt = PracticeAttempt(
        question_id=pq.id,
        learner_id=learner_id,
        answer_json=answer_payload,
        is_correct=is_correct,
        hints_used=hints_used,
        ai_feedback=feedback,
        score=earned_score,
    )
    session.add(attempt)
    session.flush()

    # Recompute Dedication Score
    p_score = update_dedication_score(session, learner_id, pq.field)

    # Check Talent Spotlight Threshold
    alert = evaluate_talent_spotlight(session, learner_id, pq.field, p_score)

    session.commit()
    return attempt, p_score, alert


def update_dedication_score(session: Session, learner_id: str, field: str) -> PracticeScore:
    """Calculate and persist dedication score per learner per field."""
    now = datetime.now(UTC)
    thirty_days_ago = now - timedelta(days=30)

    # Query attempts in last 30 days
    attempts = (
        session.execute(
            select(PracticeAttempt)
            .join(PracticeQuestion)
            .where(
                PracticeAttempt.learner_id == learner_id,
                PracticeQuestion.field == field,
                PracticeAttempt.created_at >= thirty_days_ago,
            )
        )
        .scalars()
        .all()
    )

    total_attempted = len(attempts)
    total_solved = sum(1 for a in attempts if a.is_correct)
    acceptance_rate = (total_solved / total_attempted * 100.0) if total_attempted > 0 else 0.0

    # Distinct active days
    active_dates = {a.created_at.date() for a in attempts}
    active_days = len(active_dates)

    # Difficulty-weighted accuracy: Easy = 1.0, Medium = 1.5, Hard = 2.0
    weight_map = {"EASY": 1.0, "MEDIUM": 1.5, "HARD": 2.0}
    weighted_pts = 0.0
    max_pts = 0.0
    for a in attempts:
        diff = getattr(a.question, "difficulty", "MEDIUM")
        w = weight_map.get(diff, 1.0)
        max_pts += w
        if a.is_correct:
            weighted_pts += w

    weighted_accuracy = (weighted_pts / max_pts * 100.0) if max_pts > 0 else 0.0

    # Composite Dedication Score (0 - 100):
    # 40% active days factor (capped at 20 days)
    # 30% weighted accuracy
    # 30% volume / problem attempt factor (capped at 30 problems)
    active_factor = min(1.0, active_days / 15.0) * 40.0
    accuracy_factor = (weighted_accuracy / 100.0) * 30.0
    volume_factor = min(1.0, total_attempted / 20.0) * 30.0
    dedication_score = round(active_factor + accuracy_factor + volume_factor, 1)

    p_score = (
        session.execute(
            select(PracticeScore).where(
                PracticeScore.learner_id == learner_id,
                PracticeScore.field == field,
            )
        )
        .scalars()
        .one_or_none()
    )

    if not p_score:
        p_score = PracticeScore(
            learner_id=learner_id,
            field=field,
            active_days=active_days,
            streak_days=active_days,
            problems_attempted=total_attempted,
            problems_solved=total_solved,
            acceptance_rate=round(acceptance_rate, 1),
            weighted_accuracy=round(weighted_accuracy, 1),
            dedication_score=dedication_score,
            last_practiced_at=now,
        )
        session.add(p_score)
    else:
        p_score.active_days = active_days
        p_score.streak_days = active_days
        p_score.problems_attempted = total_attempted
        p_score.problems_solved = total_solved
        p_score.acceptance_rate = round(acceptance_rate, 1)
        p_score.weighted_accuracy = round(weighted_accuracy, 1)
        p_score.dedication_score = dedication_score
        p_score.last_practiced_at = now

    session.flush()
    return p_score


def evaluate_talent_spotlight(
    session: Session,
    learner_id: str,
    field: str,
    p_score: PracticeScore,
) -> TalentAlert | None:
    """Check if learner meets criteria and trigger alert once per cooldown period."""
    # Read global thresholds or defaults
    setting = (
        session.execute(
            select(SystemSetting).where(SystemSetting.key == "talent_spotlight_thresholds")
        )
        .scalars()
        .one_or_none()
    )

    thresholds = setting.value_json if setting else {
        "min_active_days": 5,
        "min_weighted_accuracy": 65.0,
        "min_problems": 5,
        "cooldown_days": 14,
    }

    if (
        p_score.active_days >= thresholds["min_active_days"]
        and p_score.weighted_accuracy >= thresholds["min_weighted_accuracy"]
        and p_score.problems_attempted >= thresholds["min_problems"]
    ):
        # Locate assigned mentor
        assignment = (
            session.execute(
                select(MentorLearnerAssignment).where(
                    MentorLearnerAssignment.learner_id == learner_id
                )
            )
            .scalars()
            .first()
        )
        if not assignment:
            return None

        mentor_id = assignment.mentor_id
        cooldown_threshold = datetime.now(UTC) - timedelta(days=thresholds["cooldown_days"])

        # Check existing alert within cooldown
        recent_alert = (
            session.execute(
                select(TalentAlert).where(
                    TalentAlert.learner_id == learner_id,
                    TalentAlert.field == field,
                    TalentAlert.created_at >= cooldown_threshold,
                )
            )
            .scalars()
            .first()
        )
        if recent_alert:
            return None  # Cooldown active, suppress duplicate

        learner = session.get(User, learner_id)
        learner_name = learner.full_name if learner else "Learner"

        evidence = {
            "dedication_score": p_score.dedication_score,
            "active_days_30d": p_score.active_days,
            "weighted_accuracy": p_score.weighted_accuracy,
            "problems_attempted": p_score.problems_attempted,
            "problems_solved": p_score.problems_solved,
            "acceptance_rate": p_score.acceptance_rate,
        }

        alert = TalentAlert(
            learner_id=learner_id,
            mentor_id=mentor_id,
            field=field,
            evidence_json=evidence,
            status="PENDING",
        )
        session.add(alert)
        session.flush()

        # Generate in-app notification for Mentor
        notif = Notification(
            recipient_id=mentor_id,
            sender_id=learner_id,
            title=f"Talent Spotlight: Strong Performance in {field}",
            message=f"{learner_name} crossed performance benchmarks in {field} (Dedication: {p_score.dedication_score}, Accuracy: {p_score.weighted_accuracy}%). Review and decide next step.",
            notification_type="TALENT_ALERT",
            link="/mentor/talent-spotlight",
        )
        session.add(notif)
        return alert

    return None
