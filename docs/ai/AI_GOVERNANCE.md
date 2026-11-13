# TRELLIS Responsible AI Governance & Evaluation Framework

## 1. Principles & Mandatory Boundaries (Master Prompt Section 12)
- **Treat AI Governance as a Product Feature**: Not mere documentation, but enforceable runtime constraints and CI release gates.
- **Strict Grounding in Approved CSM Content**: Gardener answers exclusively from approved, verified internal CSM documents (`kb_articles`). If internal documentation lacks support for an answer, the model must explicitly refuse and offer a route to "Ask an Expert".
- **Zero Automated Employment Impact**: AI recommendations, feedback, and scoring suggestions never feed automated promotion, compensation, disciplinary, or termination decisions.
- **Mandatory Human-in-the-Loop**: Any AI-generated score, summary, or report released to an employee's official record must be moderated and signed off by a human trainer or evaluator.
- **Labeling Invariant**: All AI-assisted responses, explanations, and report draft text carry a persistent visual label: `[AI-Generated - Verified by CSM Trainer]`.

---

## 2. Platform AI Registry

| Feature ID | AI Feature Name | Purpose | Target Model ID | Training / Context Data Used | Human Oversight Point | Feature Owner | Evaluation Interval |
|---|---|---|---|---|---|---|---|
| `AI-001` | **Gardener AI Coach** | Grounded Q&A, study plans, mistake breakdowns | `nvidia/llama-3.1-nemotron-70b-instruct` (NVIDIA NIM Nemotron Placeholder) | Approved `kb_articles`, learner's active skill gaps | Self-service learner; unanswerable routes to Human Expert | Head of L&K | Continuous CI + Weekly audit |
| `AI-002` | **Communication CEFR Grader** | Evaluates email writing and communication rubrics | `nvidia/llama-3.1-nemotron-70b-instruct` (NVIDIA NIM Nemotron Placeholder) | Candidate response + CEFR rubric definitions | **Mandatory**: Assessment reviewer must approve/adjust grade before posting | Lead Communication Trainer | Bi-weekly against benchmark cohort |
| `AI-003` | **Teach-Back Verification Assistant** | Evaluates learner concept explanations | `nvidia/llama-3.1-nemotron-70b-instruct` (NVIDIA NIM Nemotron Placeholder) | Concept definition + learner transcript | **Mandatory**: Trainer or designated peer confirms | Senior Technical Trainer | Monthly |
| `AI-004` | **Leadership Briefing Drafter** | Synthesizes monthly learning metrics into impact narrative | `nvidia/llama-3.1-nemotron-70b-instruct` (NVIDIA NIM Nemotron Placeholder) | Aggregated read-model statistics (`n >= 5`) | **Mandatory**: CLO must edit, approve, and sign off before export | Chief Learning Officer | Monthly |
| `AI-005` | **Skills Inference Engine** | Identifies potential skills from project contributions | `nvidia/llama-3.1-nemotron-70b-instruct` (NVIDIA NIM Nemotron Placeholder) | Merged Greenhouse diffs, task completions | **Mandatory**: Employee confirms, edits, or rejects inference | Skills Lead | Monthly |

---

## 3. CI/CD Automated Evaluation Harness

Releases are blocked if the evaluation harness reports regression against the fixed golden benchmark dataset (100 synthetic test cases):

```
+-----------------------------------------------------------------------------------------+
| METRIC               | THRESHOLD | DESCRIPTION                                          |
+----------------------+-----------+------------------------------------------------------+
| Groundedness Score   | >= 0.98   | Percentage of assertions backed by cited passages.   |
| Citation Accuracy    | >= 0.99   | Cited document ID and passage exactly match source.  |
| Refusal on Unknown   | = 1.00    | Zero hallucinations when queried on unapproved data.  |
| Toxic / Harsh Tone   | = 0.00    | Zero disparaging, ranking, or non-developmental tone.|
| PII Leakage Check    | = 0.00    | Zero transmission of employee identifiers or psych.  |
+-----------------------------------------------------------------------------------------+
```

---

## 4. Operational Controls & Runtime Guardrails
1. **Prompt & Model Versioning**: Every inference execution creates an immutable row in `ai_runs`:
   - `model_id`, `prompt_template_version`, `input_sha256`, `context_docs_sha256`, `output_json`, `execution_time_ms`, `token_count`.
2. **PII Scrubbing Pipeline**: Prior to model dispatch, all inputs pass through regex and local spaCy/regex scrubbers to strip employee names, email addresses, employee codes, and psychometric tokens. Employee-identifying psychometric data is strictly barred from ever reaching a model.
3. **Prompt Injection Hardening**:
   - Retrieved document text is treated strictly as untrusted string literals enclosed within rigid delimiter tags (`<context_document_untrusted>`).
   - System prompts instruct the model that document text must never be interpreted as system instructions, tool execution requests, or role overrides.
4. **Circuits & Rate Limits**:
   - Per-user limit: 50 queries / day.
   - Global rate limit: 100 requests / minute across the cluster.
   - Kill Switch: `FEATURE_AI_COACH=false` instantly disables model calls and gracefully falls back to static Knowledge Base search.
5. **Transparency**: Every recommendation displayed to an employee includes an accessible collapsible drawer titled: *"Why am I seeing this?"*, explaining the specific evidence gap and confidence calculation.
