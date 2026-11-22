"""Versioned prompts and JSON extraction utilities for TRELLIS AI Gateway."""

from __future__ import annotations

import json
import re
from typing import Any

PROMPT_VERSION = "1.2.0"

PROMPT_MCQ_GENERATION = """You are an expert curriculum developer at CSM Technologies.
Create a high-quality Multiple Choice Question (MCQ) for practice in {field}.
Difficulty: {difficulty}
Category: {category}
Topic context: {topic}

Requirements:
1. Exactly 4 distinct, unambiguous options.
2. Exactly 1 correct answer that precisely matches one of the options.
3. Detailed, educational explanation walking through why the correct answer is right and why distractors are incorrect.
4. 2 practical hints that guide the learner without revealing the answer directly.
5. Return ONLY a valid JSON object matching this schema:
{{
  "title": "<Concise problem title>",
  "question": "<Unambiguous question statement>",
  "options": ["<Option A>", "<Option B>", "<Option C>", "<Option D>"],
  "correct_answer": "<Exact string of the correct option>",
  "explanation": "<Step-by-step educational explanation>",
  "hints": ["<Hint 1>", "<Hint 2>"]
}}
"""

PROMPT_CODING_GENERATION = """You are a senior staff engineer at CSM Technologies.
Create an authentic, practical {language} coding problem for practice.
Field: {field}
Difficulty: {difficulty}
Category: {category}

Requirements:
1. Provide a clear problem statement with input/output format and explicit constraints.
2. Include at least 2 real example walkthroughs.
3. Provide starter code in {language}.
4. Provide a robust, clean reference solution in {language} that passes all test cases.
5. Provide a deliberately flawed wrong_stub in {language} that fails at least one test case.
6. Provide at least 3 comprehensive test cases (with 'input_data', 'expected_output', 'is_hidden' (bool), and 'weight').
7. Return ONLY a valid JSON object matching this schema:
{{
  "title": "<Concise problem title>",
  "question": "<Complete problem statement>",
  "constraints": "<Constraints on input size and runtime>",
  "examples": [
    {{"input": "<Example 1 input>", "output": "<Example 1 output>", "explanation": "<Walkthrough>"}},
    {{"input": "<Example 2 input>", "output": "<Example 2 output>", "explanation": "<Walkthrough>"}}
  ],
  "starter_code": {{"{language}": "<Starter boilerplate code>"}},
  "reference_solution": "<Complete working code that passes all test cases>",
  "wrong_stub": "<Flawed code that fails at least one test case>",
  "test_cases": [
    {{"input_data": "<Test 1 input>", "expected_output": "<Test 1 output>", "is_hidden": false, "weight": 1.0}},
    {{"input_data": "<Test 2 input>", "expected_output": "<Test 2 output>", "is_hidden": false, "weight": 1.0}},
    {{"input_data": "<Test 3 input>", "expected_output": "<Test 3 output>", "is_hidden": true, "weight": 1.0}}
  ],
  "explanation": "<Algorithmic walkthrough and complexity analysis>",
  "hints": ["<Guiding hint 1>", "<Guiding hint 2>"]
}}
"""

PROMPT_SQL_GENERATION = """You are a database architect at CSM Technologies.
Create a real-world SQL problem for {difficulty} level.
Field: SQL
Difficulty: {difficulty}
Category: Coding

Requirements:
1. Define a clean SQLite-compatible table schema with seed INSERT data in test_cases[].input_data.
2. The candidate SQL query will be evaluated directly against this in-memory database.
3. 'expected_output' must be pipe-delimited (|) rows matching the query result.
4. Provide standard SQL starter code: "-- Write your SQL query here\\nSELECT "
5. Return ONLY a valid JSON object matching this schema:
{{
  "title": "<Concise problem title>",
  "question": "<Problem statement detailing tables and required result>",
  "constraints": "Standard ANSI SQL / SQLite dialect",
  "examples": [
    {{"input": "<Schema summary>", "output": "<Expected tabular output>", "explanation": "<Explanation>"}}
  ],
  "starter_code": {{"sql": "-- Write your SQL query here\\nSELECT "}},
  "reference_solution": "<Complete working SQL query>",
  "wrong_stub": "SELECT 'wrong';",
  "test_cases": [
    {{
      "input_data": "CREATE TABLE employees (id INT, name TEXT, salary INT); INSERT INTO employees VALUES (1, 'Alice', 70000), (2, 'Bob', 50000);",
      "expected_output": "Alice|70000",
      "is_hidden": false,
      "weight": 1.0
    }},
    {{
      "input_data": "CREATE TABLE employees (id INT, name TEXT, salary INT); INSERT INTO employees VALUES (1, 'Carol', 85000), (2, 'Dave', 92000);",
      "expected_output": "Dave|92000",
      "is_hidden": true,
      "weight": 1.0
    }}
  ],
  "explanation": "<Query design and indexing rationale>",
  "hints": ["<Hint 1>", "<Hint 2>"]
}}
"""

PROMPT_GARDENER_SOCRATIC = """You are 'The Gardener', the empathetic, expert AI Learning Coach on TRELLIS, the CSM Technologies Learning Platform.
Role Persona & Guidelines:
1. Socratic Mentorship: Guide the learner with reasoning, clues, and analogies rather than giving away assessment answers directly.
2. Active Assessment Detection: If the user appears to be asking for an answer during an active assessment, encourage them to apply core principles on their own.
3. Grounding: All curriculum facts and pathway milestones must be accurate and grounded in the learner's profile.
4. Privacy: Never disclose or compare against other learners by name.
5. Tone: Encouraging, professional, technically precise, and actionable.

Learner Profile:
- Name: {learner_name}
- Pathway: {pathway} (Progress: {progress_percent}%)
- Streak: {streak_days} days
- Recent Performance: {recent_perf}

Conversation History:
{history}

Learner Query: {user_message}

Provide a thoughtful, structured response with clear next steps for the learner.
"""


def extract_json_payload(text: str) -> dict[str, Any]:
    """Robustly extract and parse a JSON object from LLM response text."""
    if not text:
        raise ValueError("Empty LLM response text")

    text_clean = text.strip()
    # Match markdown code block ```json ... ```
    md_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text_clean, re.DOTALL)
    if md_match:
        return json.loads(md_match.group(1))

    # Match outermost curly braces
    brace_match = re.search(r"(\{.*\})", text_clean, re.DOTALL)
    if brace_match:
        return json.loads(brace_match.group(1))

    return json.loads(text_clean)
