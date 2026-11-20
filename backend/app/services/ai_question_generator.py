"""TRELLIS AI Practice Question Generation Engine (Phase 4).

Features:
1. Real LLM Generation (Anthropic Messages API / OpenAI) with configurable model ID from settings.
2. Realistic timeout (30-60s), strict JSON requesting, validated via Pydantic models.
3. Retries once on invalid output.
4. Distinguishes source: "llm" | "template".
5. Multi-language CODING support honoring chosen field (Python, Java, JavaScript, SQL, DSA).
6. Sandbox pre-verification for CODING: executes reference solution in isolated CodeRunner (must pass),
   and verifies deliberately wrong stub fails at least one case. Discards and retries up to 3 times.
7. MCQ validation: exactly 4 distinct choices, with correct_answer matching one of them.
8. Normalized question hashing for de-duplication per learner.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import random
import re
import urllib.request
from typing import Any

from pydantic import BaseModel, Field, model_validator

from app.core.config import settings
from app.services.code_runner import CodeRunner

logger = logging.getLogger(__name__)

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


class GeneratedMcqQuestion(BaseModel):
    title: str = Field(..., min_length=2)
    question: str = Field(..., min_length=5)
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=5)
    hints: list[str] = Field(default_factory=list)
    field: str
    difficulty: str

    @model_validator(mode="after")
    def validate_options_and_answer(self) -> "GeneratedMcqQuestion":
        if len(self.options) != 4:
            raise ValueError("MCQ must have exactly 4 options.")
        if len(set(self.options)) != 4:
            raise ValueError("MCQ options must be distinct.")
        if self.correct_answer not in self.options:
            raise ValueError(
                f"correct_answer '{self.correct_answer}' must exactly match one of the 4 options: {self.options}"
            )
        return self


class GeneratedCodingQuestion(BaseModel):
    title: str = Field(..., min_length=2)
    question: str = Field(..., min_length=5)
    field: str
    difficulty: str
    language: str
    constraints: str | None = None
    examples: list[dict[str, Any]] = Field(default_factory=list)
    starter_code: dict[str, str] = Field(default_factory=dict)
    reference_solution: str = Field(..., min_length=5)
    wrong_stub: str | None = None
    test_cases: list[dict[str, Any]] = Field(..., min_length=2)
    explanation: str = Field(..., min_length=5)
    hints: list[str] = Field(default_factory=list)


def get_field_language(field: str) -> str:
    """Map technical discipline to runtime language."""
    f = field.strip().lower()
    if "java" in f:
        return "java"
    elif "web" in f or "javascript" in f:
        return "javascript"
    elif "sql" in f:
        return "python"  # Simulated SQL/SQLite environment
    elif "cpp" in f or "c++" in f:
        return "cpp"
    return "python"


def compute_question_hash(question_text: str) -> str:
    """Compute normalized SHA-256 hash for de-duplication."""
    clean = re.sub(r"\s+", " ", (question_text or "").strip().lower())
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()[:16]


def verify_coding_problem(problem: dict[str, Any], language: str) -> bool:
    """Run reference solution through isolated CodeRunner (must pass 100%),
    and verify that deliberately wrong stub fails at least one test case."""
    ref_code = problem.get("reference_solution")
    test_cases = problem.get("test_cases", [])
    if not ref_code or not test_cases:
        return False

    # 1. Reference solution must pass all test cases
    try:
        ref_res = CodeRunner.execute(
            code=ref_code,
            language=language,
            test_cases=test_cases,
            time_limit_ms=3500,
            mask_hidden_inputs=False,
        )
        if ref_res.verdict != "ACCEPTED" or ref_res.score < 100.0:
            logger.warning(
                "Sandbox verification failed for reference solution: verdict=%s score=%s",
                ref_res.verdict,
                ref_res.score,
            )
            return False
    except Exception as e:
        logger.warning("Sandbox reference execution error: %s", e)
        return False

    # 2. Deliberately wrong stub must FAIL at least one test case
    wrong_stub = problem.get("wrong_stub")
    if not wrong_stub:
        if language == "python":
            wrong_stub = "import sys\nprint('__WRONG_OUTPUT_ASSERTION__')\n"
        elif language == "java":
            wrong_stub = "public class Solution { public static void main(String[] args) { System.out.println('__WRONG__'); } }"
        elif language == "javascript":
            wrong_stub = "console.log('__WRONG__');"
        else:
            wrong_stub = "print('__WRONG__')"

    try:
        stub_res = CodeRunner.execute(
            code=wrong_stub,
            language=language,
            test_cases=test_cases,
            time_limit_ms=3500,
            mask_hidden_inputs=False,
        )
        if stub_res.verdict == "ACCEPTED":
            logger.warning("Sandbox verification failed: wrong stub unexpectedly passed all cases!")
            return False
    except Exception:
        # Failing compilation or runtime is expected and acceptable for wrong stub
        pass

    return True


def _clean_json_text(text: str) -> str:
    """Strip markdown backticks or preamble from LLM response."""
    t = (text or "").strip()
    if t.startswith("```"):
        lines = t.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        t = "\n".join(lines).strip()
    # Find outer JSON object/array if there is extra prose
    start = t.find("{")
    end = t.rfind("}")
    if start != -1 and end != -1 and end > start:
        return t[start : end + 1]
    return t


def _call_ollama_api(prompt: str, timeout: int = 45) -> dict[str, Any] | None:
    """Call local Ollama service (zero API keys required, 100% private & self-hosted)."""
    base_url = (settings.AI_LOCAL_URL or "http://localhost:11434").rstrip("/")
    url = f"{base_url}/api/generate"
    model = settings.AI_MODEL_ID or "qwen2.5-coder:7b"
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": 2048,
            },
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                raw = json.loads(resp.read().decode("utf-8"))
                response_text = raw.get("response", "")
                cleaned = _clean_json_text(response_text)
                return json.loads(cleaned)
    except Exception as exc:
        logger.debug("Local Ollama call unavailable or failed: %s", exc)
    return None


def _call_openai_compat_api(prompt: str, base_url: str, api_key: str, timeout: int = 45) -> dict[str, Any] | None:
    """Call any OpenAI-compatible local or cloud endpoint (vLLM, LM Studio, LocalAI, OpenAI)."""
    url = f"{base_url.rstrip('/')}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    body = json.dumps(
        {
            "model": settings.AI_MODEL_ID,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
            "response_format": {"type": "json_object"},
        }
    ).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                raw = json.loads(resp.read().decode("utf-8"))
                choice = raw.get("choices", [{}])[0]
                msg = choice.get("message", {}).get("content", "")
                cleaned = _clean_json_text(msg)
                return json.loads(cleaned)
    except Exception as exc:
        logger.debug("OpenAI-compatible call failed: %s", exc)
    return None


def _call_anthropic_api(prompt: str, timeout: int) -> dict[str, Any] | None:
    """Call Anthropic API using configurable model and settings."""
    api_key = settings.AI_API_KEY or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    base_url = settings.AI_BASE_URL or os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    url = f"{base_url.rstrip('/')}/v1/messages"
    body = json.dumps(
        {
            "model": settings.AI_MODEL_ID,
            "max_tokens": 2000,
            "temperature": 0.4,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                raw = json.loads(resp.read().decode("utf-8"))
                text = raw.get("content", [{}])[0].get("text", "").strip()
                cleaned = _clean_json_text(text)
                return json.loads(cleaned)
    except Exception as exc:
        logger.debug("Anthropic API call failed: %s", exc)
    return None


def _call_llm_json(prompt: str, timeout: int = 45) -> dict[str, Any] | None:
    """Route LLM JSON request according to AI_PROVIDER configuration."""
    provider = getattr(settings, "AI_PROVIDER", "auto").lower()

    if provider in {"ollama", "local"}:
        return _call_ollama_api(prompt, timeout=timeout)
    elif provider == "openai":
        return _call_openai_compat_api(
            prompt,
            base_url=settings.AI_BASE_URL or "https://api.openai.com",
            api_key=settings.AI_API_KEY,
            timeout=timeout,
        )
    elif provider == "anthropic":
        return _call_anthropic_api(prompt, timeout=timeout)
    elif provider == "smart_template":
        return None  # Directly use procedural template engine

    # Provider == "auto": Probe local Ollama first (zero API key needed); then cloud; then fallback
    res = _call_ollama_api(prompt, timeout=min(timeout, 15))
    if res:
        return res

    if settings.AI_API_KEY:
        if "anthropic" in (settings.AI_BASE_URL or "") or settings.AI_MODEL_ID.startswith("claude"):
            return _call_anthropic_api(prompt, timeout=timeout)
        return _call_openai_compat_api(
            prompt,
            base_url=settings.AI_BASE_URL or "https://api.openai.com",
            api_key=settings.AI_API_KEY,
            timeout=timeout,
        )

    return None


def call_llm_text(prompt: str, timeout: int = 30) -> str | None:
    """Call LLM API to get natural language completion for assistant queries & narrative diagnostics."""
    provider = getattr(settings, "AI_PROVIDER", "auto").lower()

    # 1. Try local Ollama if configured or in auto mode
    if provider in {"ollama", "local", "auto"}:
        base_url = (settings.AI_LOCAL_URL or "http://localhost:11434").rstrip("/")
        req_body = json.dumps(
            {
                "model": settings.AI_MODEL_ID or "qwen2.5-coder:7b",
                "prompt": prompt,
                "stream": False,
            }
        ).encode("utf-8")
        try:
            req = urllib.request.Request(
                f"{base_url}/api/generate",
                data=req_body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=min(timeout, 15)) as resp:
                if resp.status == 200:
                    raw = json.loads(resp.read().decode("utf-8"))
                    text = raw.get("response", "").strip()
                    if text:
                        return text
        except Exception:
            pass

    # 2. Try cloud Anthropic if key exists
    api_key = settings.AI_API_KEY or os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        base_url = settings.AI_BASE_URL or os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
        url = f"{base_url.rstrip('/')}/v1/messages"
        body = json.dumps(
            {
                "model": settings.AI_MODEL_ID,
                "max_tokens": 1000,
                "temperature": 0.5,
                "messages": [{"role": "user", "content": prompt}],
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    raw = json.loads(resp.read().decode("utf-8"))
                    return raw.get("content", [{}])[0].get("text", "").strip()
        except Exception as exc:
            logger.warning("LLM text call failed: %s", exc)

    return None


def _call_llm_generator(
    field: str,
    difficulty: str,
    mode: str,
    seen_hashes: set[str] | None = None,
) -> dict[str, Any] | None:
    """Attempt live LLM generation with strict JSON schema validation and retry."""
    language = get_field_language(field)
    timeout = settings.AI_REQUEST_TIMEOUT_SECONDS or 45

    base_prompt = (
        f"You are the TRELLIS AI Practice Problem Generator.\n"
        f"Generate a rigorous {difficulty} level {mode} practice problem for technical field: '{field}' (Language: '{language}').\n"
        f"Return ONLY valid JSON (no markdown formatting, no code fences) with the exact structure:\n"
    )

    if mode == "MCQ":
        schema_desc = (
            "- title: string (short descriptive title)\n"
            "- question: string (clear problem statement)\n"
            "- options: list of exactly 4 distinct strings\n"
            "- correct_answer: string (exact character match of one option)\n"
            "- explanation: string (detailed technical rationale)\n"
            "- hints: list of 2 progressive hints\n"
            f"- field: '{field}'\n"
            f"- difficulty: '{difficulty}'\n"
        )
    else:
        schema_desc = (
            "- title: string\n"
            "- question: string\n"
            f"- language: '{language}'\n"
            "- constraints: string\n"
            "- examples: list of dicts with 'input' and 'output'\n"
            f"- starter_code: dict with '{language}' key containing boilerplate reading stdin and printing stdout\n"
            f"- reference_solution: fully working {language} code reading stdin and printing stdout\n"
            f"- wrong_stub: intentionally wrong {language} code that fails the test cases\n"
            "- test_cases: list of 4 dicts with 'input_data', 'expected_output', 'is_hidden' (bool), 'weight' (float)\n"
            "- explanation: string\n"
            "- hints: list of 2 progressive hints\n"
            f"- field: '{field}'\n"
            f"- difficulty: '{difficulty}'\n"
        )

    prompt = base_prompt + schema_desc

    for attempt in range(2):
        try:
            parsed = _call_llm_json(prompt, timeout=timeout)
            if not isinstance(parsed, dict):
                continue

            if mode == "MCQ":
                val_mcq = GeneratedMcqQuestion(
                    title=parsed.get("title", ""),
                    question=parsed.get("question", ""),
                    options=parsed.get("options", []),
                    correct_answer=parsed.get("correct_answer", ""),
                    explanation=parsed.get("explanation", ""),
                    hints=parsed.get("hints", []),
                    field=field,
                    difficulty=difficulty,
                )
                res = val_mcq.model_dump()
                res["mode"] = "MCQ"
                res["source"] = "llm"
                res["question_hash"] = compute_question_hash(res["question"])
                if seen_hashes and res["question_hash"] in seen_hashes:
                    prompt += "\nNote: Generate an entirely different topic from the previous one."
                    continue
                return res

            elif mode == "CODING":
                val_code = GeneratedCodingQuestion(
                    title=parsed.get("title", ""),
                    question=parsed.get("question", ""),
                    field=field,
                    difficulty=difficulty,
                    language=language,
                    constraints=parsed.get("constraints"),
                    examples=parsed.get("examples", []),
                    starter_code=parsed.get("starter_code", {}),
                    reference_solution=parsed.get("reference_solution", ""),
                    wrong_stub=parsed.get("wrong_stub"),
                    test_cases=parsed.get("test_cases", []),
                    explanation=parsed.get("explanation", ""),
                    hints=parsed.get("hints", []),
                )
                res = val_code.model_dump()
                res["mode"] = "CODING"
                res["source"] = "llm"
                res["question_hash"] = compute_question_hash(res["question"])

                if seen_hashes and res["question_hash"] in seen_hashes:
                    prompt += "\nNote: Generate a different problem."
                    continue

                # Verify in isolated runner
                if verify_coding_problem(res, language):
                    return res
                else:
                    logger.warning("LLM generated coding problem failed verification. Retrying...")

        except Exception as exc:
            logger.info("LLM generation attempt %d failed: %s", attempt + 1, exc)
            prompt += f"\nPrevious attempt had invalid format: {exc}. Please correct and output strict valid JSON."

    return None


# -----------------------------------------------------------------------------
# MULTI-LANGUAGE PROCEDURAL GENERATIVE TEMPLATES (source: "template")
# -----------------------------------------------------------------------------

def _gen_python_coding(difficulty: str) -> dict[str, Any]:
    offset = random.randint(3, 15)
    problems = [
        lambda: {
            "title": "Frequency-Sorted Character Compactor",
            "statement": (
                "Given a string `s`, sort it in decreasing order based on the frequency of the characters. "
                "If two characters have the same frequency, sort them in alphabetical order.\n\n"
                "Input: Single line containing string `s`.\n"
                "Output: The frequency-sorted string."
            ),
            "field": "Python",
            "difficulty": difficulty,
            "language": "python",
            "constraints": "1 <= len(s) <= 10^5",
            "examples": [
                {"input": "tree", "output": "eert"},
                {"input": "cccaaa", "output": "aaaccc"},
            ],
            "starter_code": {
                "python": (
                    "import sys\nfrom collections import Counter\n\n"
                    "def solve():\n"
                    "    s = sys.stdin.read().strip()\n"
                    "    if not s: return\n"
                    "    # Frequency sort logic\n"
                    "    pass\n\n"
                    "if __name__ == '__main__':\n    solve()\n"
                )
            },
            "reference_solution": (
                "import sys\nfrom collections import Counter\n\n"
                "def solve():\n"
                "    s = sys.stdin.read().strip()\n"
                "    if not s: return\n"
                "    counts = Counter(s)\n"
                "    res = ''.join(ch * counts[ch] for ch in sorted(counts.keys(), key=lambda c: (-counts[c], c)))\n"
                "    print(res)\n\n"
                "if __name__ == '__main__':\n    solve()\n"
            ),
            "wrong_stub": "import sys\nprint('wrong_compaction')\n",
            "test_cases": [
                {"input_data": "tree", "expected_output": "eert", "is_hidden": False, "weight": 1.0},
                {"input_data": "cccaaa", "expected_output": "aaaccc", "is_hidden": False, "weight": 1.0},
                {"input_data": "Aabb", "expected_output": "bbAa", "is_hidden": True, "weight": 2.0},
            ],
            "explanation": "Count character frequencies using Counter and sort by compound key (-count, char).",
            "hints": ["Use collections.Counter for O(N) frequency counts.", "Sort with compound key (-freq, char)."],
        },
        lambda: {
            "title": f"Sliding Subarray Maximum with Window K={min(offset, 4)}",
            "statement": (
                f"Given an array of integers and an integer K={min(offset, 4)}, output the maximum value in each sliding "
                "window of size K from left to right as space-separated integers.\n\n"
                "Input:\nLine 1: K\nLine 2: Space-separated integers."
            ),
            "field": "Python",
            "difficulty": difficulty,
            "language": "python",
            "constraints": "1 <= K <= N <= 10^5",
            "examples": [{"input": "3\n1 3 -1 -3 5 3 6 7", "output": "3 3 5 5 6 7"}],
            "starter_code": {
                "python": (
                    "import sys\nfrom collections import deque\n\n"
                    "def solve():\n"
                    "    data = sys.stdin.read().strip().split('\\n')\n"
                    "    if len(data) < 2: return\n"
                    "    k = int(data[0].strip())\n"
                    "    nums = list(map(int, data[1].split()))\n"
                    "    # Sliding window logic\n"
                    "    pass\n\n"
                    "if __name__ == '__main__':\n    solve()\n"
                )
            },
            "reference_solution": (
                "import sys\nfrom collections import deque\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().strip().split('\\n')\n"
                "    if len(data) < 2: return\n"
                "    k = int(data[0].strip())\n"
                "    nums = list(map(int, data[1].split()))\n"
                "    q = deque()\n"
                "    res = []\n"
                "    for i, n in enumerate(nums):\n"
                "        while q and q[0] <= i - k:\n"
                "            q.popleft()\n"
                "        while q and nums[q[-1]] <= n:\n"
                "            q.pop()\n"
                "        q.append(i)\n"
                "        if i >= k - 1:\n"
                "            res.append(str(nums[q[0]]))\n"
                "    print(' '.join(res))\n\n"
                "if __name__ == '__main__':\n    solve()\n"
            ),
            "wrong_stub": "import sys\nprint('0 0 0')\n",
            "test_cases": [
                {"input_data": "3\n1 3 -1 -3 5 3 6 7", "expected_output": "3 3 5 5 6 7", "is_hidden": False, "weight": 1.0},
                {"input_data": "1\n5", "expected_output": "5", "is_hidden": False, "weight": 1.0},
                {"input_data": "2\n9 11", "expected_output": "11", "is_hidden": True, "weight": 2.0},
            ],
            "explanation": "Monotonic decreasing deque maintains candidate maximum indices in O(N) total time.",
            "hints": ["Store indices in the deque.", "Maintain deque elements in strictly descending order."],
        },
    ]
    return random.choice(problems)()


def _gen_java_coding(difficulty: str) -> dict[str, Any]:
    return {
        "title": "Java Two Sum Index Locator",
        "statement": (
            "Given a target integer and a list of space-separated integers, output the 0-based indices "
            "of the two numbers that add up to target.\n\n"
            "Input:\nLine 1: Target integer\nLine 2: Space-separated integers\n"
            "Output: Space-separated indices (e.g. '0 1')."
        ),
        "field": "Java",
        "difficulty": difficulty,
        "language": "java",
        "constraints": "1 <= N <= 10^5",
        "examples": [{"input": "9\n2 7 11 15", "output": "0 1"}],
        "starter_code": {
            "java": (
                "import java.util.*;\n\n"
                "public class Solution {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if (!sc.hasNextInt()) return;\n"
                "        int target = sc.nextInt();\n"
                "        List<Integer> nums = new ArrayList<>();\n"
                "        while (sc.hasNextInt()) {\n"
                "            nums.add(sc.nextInt());\n"
                "        }\n"
                "        // Implement O(N) HashMap lookup here\n"
                "    }\n"
                "}\n"
            )
        },
        "reference_solution": (
            "import java.util.*;\n\n"
            "public class Solution {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        if (!sc.hasNextInt()) return;\n"
            "        int target = sc.nextInt();\n"
            "        List<Integer> nums = new ArrayList<>();\n"
            "        while (sc.hasNextInt()) {\n"
            "            nums.add(sc.nextInt());\n"
            "        }\n"
            "        Map<Integer, Integer> map = new HashMap<>();\n"
            "        for (int i = 0; i < nums.size(); i++) {\n"
            "            int complement = target - nums.get(i);\n"
            "            if (map.containsKey(complement)) {\n"
            "                System.out.println(map.get(complement) + \" \" + i);\n"
            "                return;\n"
            "            }\n"
            "            map.put(nums.get(i), i);\n"
            "        }\n"
            "    }\n"
            "}\n"
        ),
        "wrong_stub": "public class Solution { public static void main(String[] args) { System.out.println(\"-1 -1\"); } }",
        "test_cases": [
            {"input_data": "9\n2 7 11 15", "expected_output": "0 1", "is_hidden": False, "weight": 1.0},
            {"input_data": "6\n3 2 4", "expected_output": "1 2", "is_hidden": False, "weight": 1.0},
            {"input_data": "10\n5 5", "expected_output": "0 1", "is_hidden": True, "weight": 2.0},
        ],
        "explanation": "Use a HashMap to store seen values and their indices for single-pass O(N) lookup.",
        "hints": ["HashMap provides O(1) average lookup for target - num.", "Store index as the map value."],
    }


def _gen_webdev_coding(difficulty: str) -> dict[str, Any]:
    return {
        "title": "URL Query Parameter Key Sorter",
        "statement": (
            "Given a URL query string, parse the parameters and output each key=value pair sorted alphabetically by key.\n\n"
            "Input: Single line containing query string (e.g. 'b=2&a=1').\n"
            "Output: Space-separated key=value pairs sorted by key."
        ),
        "field": "Web Dev",
        "difficulty": difficulty,
        "language": "javascript",
        "constraints": "1 <= length <= 10^4",
        "examples": [{"input": "b=2&a=1", "output": "a=1 b=2"}],
        "starter_code": {
            "javascript": (
                "const fs = require('fs');\n"
                "const input = fs.readFileSync(0, 'utf-8').trim();\n"
                "if (!input) process.exit(0);\n"
                "// Parse query parameters and output sorted by key\n"
            )
        },
        "reference_solution": (
            "const fs = require('fs');\n"
            "const input = fs.readFileSync(0, 'utf-8').trim();\n"
            "if (!input) process.exit(0);\n"
            "const params = input.split('&').map(p => p.split('='));\n"
            "params.sort((a, b) => a[0].localeCompare(b[0]));\n"
            "console.log(params.map(p => `${p[0]}=${p[1]}`).join(' '));\n"
        ),
        "wrong_stub": "console.log('wrong=output');",
        "test_cases": [
            {"input_data": "b=2&a=1", "expected_output": "a=1 b=2", "is_hidden": False, "weight": 1.0},
            {"input_data": "z=100&m=50&a=1", "expected_output": "a=1 m=50 z=100", "is_hidden": False, "weight": 1.0},
            {"input_data": "token=xyz&auth=true", "expected_output": "auth=true token=xyz", "is_hidden": True, "weight": 2.0},
        ],
        "explanation": "Split on & and = then sort lexicographically by parameter key.",
        "hints": ["Split input using '&' delimiter.", "Sort the pairs by key."],
    }


def _gen_sql_coding(difficulty: str) -> dict[str, Any]:
    return {
        "title": "SQL Dense Rank Simulator",
        "statement": (
            "Given a list of employee salaries, output the distinct salaries sorted in descending order "
            "prefixed with their dense rank (1-indexed).\n\n"
            "Input: Space-separated integer salaries.\n"
            "Output: Space-separated rank:salary pairs (e.g. '1:300 2:200')."
        ),
        "field": "SQL",
        "difficulty": difficulty,
        "language": "python",
        "constraints": "1 <= N <= 10^4",
        "examples": [{"input": "100 200 300", "output": "1:300 2:200 3:100"}],
        "starter_code": {
            "python": (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().strip()\n"
                "    if not data: return\n"
                "    nums = list(map(int, data.split()))\n"
                "    # Dense rank simulation\n"
                "    pass\n\n"
                "if __name__ == '__main__':\n    solve()\n"
            )
        },
        "reference_solution": (
            "import sys\n\n"
            "def solve():\n"
            "    data = sys.stdin.read().strip()\n"
            "    if not data: return\n"
            "    nums = sorted(list(set(map(int, data.split()))), reverse=True)\n"
            "    print(' '.join(f'{i+1}:{s}' for i, s in enumerate(nums)))\n\n"
            "if __name__ == '__main__':\n    solve()\n"
        ),
        "wrong_stub": "import sys\nprint('1:0')\n",
        "test_cases": [
            {"input_data": "100 200 300", "expected_output": "1:300 2:200 3:100", "is_hidden": False, "weight": 1.0},
            {"input_data": "50 50 100", "expected_output": "1:100 2:50", "is_hidden": False, "weight": 1.0},
            {"input_data": "10 40 20 40 10", "expected_output": "1:40 2:20 3:10", "is_hidden": True, "weight": 2.0},
        ],
        "explanation": "Simulate DENSE_RANK() by deduplicating and sorting in descending order.",
        "hints": ["Extract unique salaries using set.", "Sort in descending order and enumerate from 1."],
    }


def _gen_dsa_coding(difficulty: str) -> dict[str, Any]:
    return {
        "title": "Balanced Parentheses Sequence Checker",
        "statement": (
            "Given a string `s` containing only characters '(', ')', '{', '}', '[', ']', determine if the input string is valid.\n"
            "Output 'true' or 'false'."
        ),
        "field": "DSA",
        "difficulty": difficulty,
        "language": "python",
        "constraints": "1 <= len(s) <= 10^5",
        "examples": [{"input": "()[]{}", "output": "true"}, {"input": "(]", "output": "false"}],
        "starter_code": {
            "python": (
                "import sys\n\n"
                "def solve():\n"
                "    s = sys.stdin.read().strip()\n"
                "    # Stack-based bracket validation\n"
                "    pass\n\n"
                "if __name__ == '__main__':\n    solve()\n"
            )
        },
        "reference_solution": (
            "import sys\n\n"
            "def solve():\n"
            "    s = sys.stdin.read().strip()\n"
            "    stack = []\n"
            "    mapping = {')': '(', '}': '{', ']': '['}\n"
            "    for ch in s:\n"
            "        if ch in mapping:\n"
            "            top = stack.pop() if stack else '#'\n"
            "            if mapping[ch] != top:\n"
            "                print('false')\n"
            "                return\n"
            "        else:\n"
            "            stack.append(ch)\n"
            "    print('true' if not stack else 'false')\n\n"
            "if __name__ == '__main__':\n    solve()\n"
        ),
        "wrong_stub": "import sys\nprint('true')\n",
        "test_cases": [
            {"input_data": "()[]{}", "expected_output": "true", "is_hidden": False, "weight": 1.0},
            {"input_data": "(]", "expected_output": "false", "is_hidden": False, "weight": 1.0},
            {"input_data": "([)]", "expected_output": "false", "is_hidden": True, "weight": 2.0},
            {"input_data": "{[]}", "expected_output": "true", "is_hidden": True, "weight": 2.0},
        ],
        "explanation": "Use a stack to match opening brackets with corresponding closing brackets in O(N) time.",
        "hints": ["Push opening brackets to stack; pop on closing bracket.", "Check if stack is empty at end."],
    }


def _gen_python_mcq(difficulty: str) -> dict[str, Any]:
    generators = [
        lambda: {
            "title": "AsyncIO Event Loop Task Lifecycle",
            "question": (
                "In Python 3.11+, when `asyncio.gather(*tasks)` encounters an unhandled exception in one task "
                "with default `return_exceptions=False`, what is the immediate lifecycle state of the remaining concurrent tasks?"
            ),
            "options": [
                "The remaining tasks continue executing in the background unless explicitly cancelled.",
                "All remaining tasks are immediately terminated via SIGKILL at OS level.",
                "The event loop halts permanently and discards all pending callbacks.",
                "Remaining tasks are paused and automatically retried 3 times.",
            ],
            "correct_answer": "The remaining tasks continue executing in the background unless explicitly cancelled.",
            "explanation": (
                "By default, `asyncio.gather` raises the first exception immediately to the caller, "
                "but does NOT automatically cancel the other tasks. `asyncio.TaskGroup` guarantees cancellation."
            ),
            "hints": ["Contrast gather() with the newer Python 3.11 TaskGroup context manager.", "Does raising propagate cancellation down?"],
        },
        lambda: {
            "title": "Python Metaclasses & Class Construction",
            "question": (
                "In Python's object model, which method of a metaclass is responsible for allocating and returning "
                "the new class object before `__init__` is called?"
            ),
            "options": [
                "`__new__(mcs, name, bases, namespace)`",
                "`__prepare__(mcs, name, bases)`",
                "`__init__(cls, name, bases, namespace)`",
                "`__call__(cls, *args, **kwargs)`",
            ],
            "correct_answer": "`__new__(mcs, name, bases, namespace)`",
            "explanation": (
                "`__new__` is the constructor that creates and returns the class instance in memory. "
                "`__init__` merely customizes it."
            ),
            "hints": ["Metaclasses follow the dual new/init pattern as regular class instantiation.", "Which dunder method creates the pointer?"],
        },
    ]
    return random.choice(generators)()


def _gen_dsa_mcq(difficulty: str) -> dict[str, Any]:
    generators = [
        lambda: {
            "title": "Red-Black Tree vs AVL Tree Balancing",
            "question": (
                "Why are Red-Black Trees generally preferred over AVL trees in high-frequency insertion/deletion "
                "scenarios (such as C++ std::map and Java TreeMap)?"
            ),
            "options": [
                "Red-Black trees require at most 2-3 tree rotations per insertion/deletion, whereas AVL trees perform more frequent rotations.",
                "Red-Black trees have strictly lower maximum tree height than AVL trees.",
                "Red-Black trees do not require any memory overhead for node metadata.",
                "Red-Black trees support O(1) worst-case search complexity.",
            ],
            "correct_answer": "Red-Black trees require at most 2-3 tree rotations per insertion/deletion, whereas AVL trees perform more frequent rotations.",
            "explanation": (
                "AVL trees maintain strict balance (height difference <= 1), leading to more frequent restructuring rotations on writes. "
                "Red-Black trees bound rotations to at most 3."
            ),
            "hints": ["Compare the balance factor of AVL (|h_left - h_right| <= 1) with black-height.", "Focus on write rotation cost."],
        },
    ]
    return random.choice(generators)()


def _gen_sql_mcq(difficulty: str) -> dict[str, Any]:
    generators = [
        lambda: {
            "title": "SQL Join Semantics",
            "question": "Which SQL JOIN returns all rows from the left table and matched rows from the right table, filling nulls if no match?",
            "options": ["LEFT OUTER JOIN", "INNER JOIN", "RIGHT OUTER JOIN", "CROSS JOIN"],
            "correct_answer": "LEFT OUTER JOIN",
            "explanation": "LEFT OUTER JOIN preserves every row from the left table regardless of right table matches.",
            "hints": ["Preserves left table operand completely.", "Nulls are populated where no match occurs."],
        },
    ]
    return random.choice(generators)()


def _gen_java_mcq(difficulty: str) -> dict[str, Any]:
    generators = [
        lambda: {
            "title": "ConcurrentHashMap Lock Striping Mechanics",
            "question": (
                "In Java 8+, how does `ConcurrentHashMap` achieve thread-safe writes with high concurrency without locking the entire map?"
            ),
            "options": [
                "It uses CAS (Compare-And-Swap) for empty bucket heads and synchronized blocks only on individual bucket node heads.",
                "It uses a single global ReentrantLock guarding every operation.",
                "It clones the entire underlying table on every write (Copy-On-Write).",
                "It queues all write requests onto a dedicated background dispatcher thread.",
            ],
            "correct_answer": "It uses CAS (Compare-And-Swap) for empty bucket heads and synchronized blocks only on individual bucket node heads.",
            "explanation": (
                "Java 8 replaced segment locking with node-level granularity: CAS is used for unpopulated bins, "
                "and synchronized on the root node of the specific bin is used for hash collisions."
            ),
            "hints": ["Java 8 removed the Segment array.", "What primitive guards the head of a collision chain?"],
        },
    ]
    return random.choice(generators)()


def _gen_webdev_mcq(difficulty: str) -> dict[str, Any]:
    generators = [
        lambda: {
            "title": "CORS Preflight Trigger Conditions",
            "question": "Which of the following HTTP requests will trigger a CORS preflight OPTIONS request before the actual request?",
            "options": [
                "A POST request with Content-Type: application/json and custom header X-Auth-Token.",
                "A GET request with standard Accept and User-Agent headers.",
                "A POST request with Content-Type: application/x-www-form-urlencoded without custom headers.",
                "A HEAD request to a public static asset.",
            ],
            "correct_answer": "A POST request with Content-Type: application/json and custom header X-Auth-Token.",
            "explanation": "A request triggers preflight unless it uses GET/HEAD/POST with CORS-safelisted headers and content types.",
            "hints": ["Is application/json considered a CORS-safelisted content type?", "Custom headers always trigger preflight."],
        },
    ]
    return random.choice(generators)()


def _gen_cloud_mcq(difficulty: str) -> dict[str, Any]:
    generators = [
        lambda: {
            "title": "Kubernetes Pod Eviction & Disruption Budgets",
            "question": (
                "When a Kubernetes node is placed into maintenance drain (`kubectl drain`), what mechanism prevents "
                "a deployment from dropping below a required quorum of available replicas?"
            ),
            "options": [
                "PodDisruptionBudget (PDB)",
                "HorizontalPodAutoscaler (HPA)",
                "ReadinessGates",
                "NodeAffinity rules",
            ],
            "correct_answer": "PodDisruptionBudget (PDB)",
            "explanation": "A PodDisruptionBudget limits the number of pods of a replicated application that are down simultaneously from voluntary disruptions.",
            "hints": ["Protects against voluntary maintenance drains.", "Configured per application deployment."],
        },
    ]
    return random.choice(generators)()


def _gen_data_analytics_mcq(difficulty: str) -> dict[str, Any]:
    generators = [
        lambda: {
            "title": "Evaluation Metrics: Precision vs Recall in Imbalanced Datasets",
            "question": (
                "In credit card fraud detection where fraudulent transactions represent 0.05% of all events, "
                "why is raw Classification Accuracy a misleading evaluation metric?"
            ),
            "options": [
                "A naive model that predicts 'Not Fraud' 100% of the time achieves 99.95% accuracy while identifying zero fraudulent transactions.",
                "Accuracy cannot be calculated when class labels are binary.",
                "Accuracy is strictly mathematically undefined for sample sizes exceeding 10,000.",
                "The ROC curve cannot be computed if accuracy is known.",
            ],
            "correct_answer": "A naive model that predicts 'Not Fraud' 100% of the time achieves 99.95% accuracy while identifying zero fraudulent transactions.",
            "explanation": "In extreme class imbalance, the majority class dominates accuracy. Precision, Recall, and PR-AUC are required.",
            "hints": ["What happens if the model predicts the majority class 100% of the time?", "Consider the base rate."],
        },
    ]
    return random.choice(generators)()


def _gen_aptitude_mcq(difficulty: str) -> dict[str, Any]:
    rate_a = random.choice([6, 8, 10, 12, 15, 20])
    rate_b = random.choice([10, 12, 15, 20, 30])
    total_time = round((rate_a * rate_b) / (rate_a + rate_b), 1)

    generators = [
        lambda: {
            "title": "Combined Work-Rate Mechanics",
            "question": (
                f"Pipe A can fill an enterprise water reservoir in {rate_a} hours, while Pipe B can fill the same "
                f"reservoir in {rate_b} hours. If both pipes are opened simultaneously at full pressure, "
                "how many hours will they take to completely fill the reservoir?"
            ),
            "options": [
                f"{total_time} hours",
                f"{round(total_time + 1.5, 1)} hours",
                f"{round(total_time * 1.4, 1)} hours",
                f"{round((rate_a + rate_b) / 2, 1)} hours",
            ],
            "correct_answer": f"{total_time} hours",
            "explanation": (
                f"Combined rate = (1/{rate_a} + 1/{rate_b}) = ({rate_a + rate_b})/({rate_a * rate_b}). "
                f"Time required = ({rate_a * rate_b})/({rate_a + rate_b}) = {total_time} hours."
            ),
            "hints": ["Compute the fractional work per hour for each pipe.", "Take the reciprocal of the combined rate."],
        },
    ]
    return random.choice(generators)()


def _generate_procedural_problem(field: str, difficulty: str, mode: str) -> dict[str, Any]:
    """Dispatch to high-fidelity procedural generation with language accuracy."""
    norm_field = field if field in SUPPORTED_FIELDS else "Python"
    norm_diff = difficulty.upper() if difficulty in {"EASY", "MEDIUM", "HARD"} else "MEDIUM"
    norm_mode = mode.upper() if mode in {"MCQ", "CODING"} else "MCQ"

    if norm_mode == "CODING":
        if norm_field == "Java":
            problem = _gen_java_coding(norm_diff)
        elif norm_field == "Web Dev":
            problem = _gen_webdev_coding(norm_diff)
        elif norm_field == "SQL":
            problem = _gen_sql_coding(norm_diff)
        elif norm_field == "DSA":
            problem = _gen_dsa_coding(norm_diff)
        else:
            problem = _gen_python_coding(norm_diff)

        problem["field"] = norm_field
        problem["difficulty"] = norm_diff
        problem["mode"] = "CODING"
        problem["source"] = "template"
        problem["question_hash"] = compute_question_hash(problem.get("statement") or problem.get("question", ""))
        return problem

    # MCQ dispatch
    field_dispatch = {
        "Python": _gen_python_mcq,
        "DSA": _gen_dsa_mcq,
        "SQL": _gen_sql_mcq,
        "Java": _gen_java_mcq,
        "Web Dev": _gen_webdev_mcq,
        "Cloud": _gen_cloud_mcq,
        "Data Analytics": _gen_data_analytics_mcq,
        "Aptitude": _gen_aptitude_mcq,
    }

    generator_fn = field_dispatch.get(norm_field, _gen_python_mcq)
    problem = generator_fn(norm_diff)
    problem["field"] = norm_field
    problem["difficulty"] = norm_diff
    problem["mode"] = "MCQ"
    problem["source"] = "template"
    problem["question_hash"] = compute_question_hash(problem.get("question", ""))

    if "options" in problem and "correct_answer" in problem:
        opts = list(problem["options"])
        random.shuffle(opts)
        problem["options"] = opts

    return problem


def generate_ai_practice_problem(
    field: str = "Python",
    difficulty: str = "MEDIUM",
    mode: str = "MCQ",
    seen_hashes: set[str] | None = None,
) -> dict[str, Any]:
    """Main orchestrator for AI Practice Problem Generation.
    
    1. Tries live LLM API if key is present and network reachable.
    2. Validates with Pydantic and isolates execution in CodeRunner sandbox.
    3. Falls back to dynamic parameterized procedural generator (marked source: "template").
    """
    # 1. Attempt live LLM
    problem = _call_llm_generator(field, difficulty, mode, seen_hashes=seen_hashes)

    # 2. Fall back to procedural generative engine if LLM was unavailable or invalid
    if not problem or not problem.get("title"):
        problem = _generate_procedural_problem(field, difficulty, mode)

    # Ensure question_hash is present
    if "question_hash" not in problem:
        problem["question_hash"] = compute_question_hash(
            problem.get("question") or problem.get("statement") or ""
        )

    return problem
