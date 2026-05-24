# CLAUDE.md — WSET-AI-System Project Memory

This file is loaded automatically by Claude at the start of every session.
It is the authoritative project context for Claude + Codex collaboration.

---

## PROJECT IDENTITY

WSET-AI-System is a deterministic, local, governance-constrained WSET Level 3 tutoring architecture. It is currently best described as a rule-based neuro-symbolic ITS/RAG substrate, not a generative-first tutor.

Core philosophy: retrieval and structured cognition first; generation only after source, governance, learner-state, misconception, and causal-chain constraints are explicit.

It intentionally avoids: autonomous examiner authority, official scoring, hidden LLM calls, embeddings, vector databases, cloud services, frontend exposure, and untraceable answer drift.

Deterministic retrieval-first was chosen because the system is exam-adjacent and source-governed. The main risk is not lack of fluency — it is unsupported authority, grading overclaim, calibration drift, and untestable changes in cognitive behavior. Retrieval-first makes answer construction inspectable, snapshot-testable, and governance-enforceable.

---

## GOVERNANCE INVARIANTS (IMMUTABLE)

```
safe_for_examiner = False          # never set to True
examiner_scoring_allowed = False   # never set to True
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

Enforcement: `tools/constants.py`. Checked in retrieval filters, Tutor validation, self-eval, LES write-back, SAT reasoner tests, and snapshot tests. Any truthy violation must fail safe.

Do NOT import `tools.orchestrator` from leaf modules.
Do NOT call any external services, LLMs, APIs, embeddings, or vector DB.
Do NOT write to files outside `knowledge/` and `tools/`.
This system is deterministic. All outputs must be reproducible.

---

## CURRENT ARCHITECTURE

### Retrieval layer
`tools/retrieval/tutor_retrieval_sandbox.py` — active deterministic retrieval engine. Loads Wine With Jimmy chunks, official WSET extracted chunks, golden tutor chunks, consolidated dictionary terms, and knowledge-map nodes. Performs query classification, domain expansion, SAT observation expansion, scoring, source diversity selection, governance filtering, and matched causal-chain extraction. Config: `knowledge/config/domain_expansions.json`, `knowledge/config/retrieval_config.json`. Official chunk creation: `tools/retrieval/official_wset_chunks.py`.

### Tutor layer
`tools/tutor/answer_builder.py` — renders deterministic Tutor markdown from context packages. Handles normal answers, misconception interventions, source notes, heading/disclaimer registries, causal-chain rendering, SAT quality section injection, mini-practice prompts, and governance validation. SAT support: `tools/tutor/sat_reasoner.py`. Explanation depth/scaffolding: `tools/tutor/explanation_priority.py`, `tools/tutor/scaffolding_policy.py`, `knowledge/config/explanation_priority_config.json`.

### Orchestrator
`tools/orchestrator/orchestrator.py` — local cognitive loop: ensure learner files → load LES → run misconception pre-pass → route to `misconception_prepass` or `normal_tutor` → run retrieval → build retrieved context → thread matched causal chains into `forced_causal_chains` → write context packages → stage session. Currently a router, not a full strategic planner. Protocol typing: `tools/orchestrator/protocols.py`.

### Learner / epistemic state
`tools/orchestrator/learner_state.py` — LES defaults and session staging.
`tools/orchestrator/les_reconciler.py` — reconciles self-eval feedback into LES.
`tools/learner_model/knowledge_tracing.py` — mastery, retention risk, learning velocity, recurring misconceptions.
Active files: `knowledge/nazareth/epistemic_state.json`, `session_staging.json`, `pedagogical_memory.json`.

### Misconception handling
`tools/orchestrator/misconception_prepass.py` — loads 20 misconception nodes from `knowledge/knowledge-map/misconceptions/`, scores detection signals and `detection_keywords`, applies explanatory-query guards, returns deterministic intervention directives. Misconceptions are cognitive objects, not retrieval snippets.

### SAT reasoning layer
`tools/tutor/sat_reasoner.py` — deterministic SAT query detection, observation extraction, quality hypothesis scoring, exclusion rules, WSET-register quality formulation. Alias data: `knowledge/config/sat_observation_aliases.json`. SAT causal nodes: `CC_SAT_QUALITY_HIGH.json`, `CC_SAT_QUALITY_MEDIUM.json`.

### Causal-chain system
32 JSON nodes in `knowledge/knowledge-map/causal-chains/`. Retrieval detects via trigger keywords and step text → passes full safe nodes into `forced_causal_chains`. Tutor renders CAUSA/MECANISMO/EFECTO/FORMULACIÓN DE EXAMEN blocks via `_render_causal_chain()` and `_select_best_causal_chain()`. Causal chains are typed reasoning structures, not retrieved prose.

### Self-eval harness
`tools/self_eval/question_runner.py` — runs questions through orchestrator → retrieval → Tutor → comparator → reporter.
`tools/self_eval/answer_comparator.py` — deterministic diagnostic labels and SAT strength labels.
`tools/self_eval/evaluation_reporter.py` — writes summaries, feedback, pedagogical memory, and LES reconciliation.

### Snapshot regression harness
`tests/test_tutor_snapshot_regression.py` — 25 frozen Tutor outputs under `tests/fixtures/tutor_snapshots/`. Asserts exact answer snapshots, fixture integrity, idempotency, governance flags, disclaimers, headings, absence of `safe_for_examiner=True`.

### Structured question bank
Questions loaded from `knowledge/question-bank/structured/` → raw XLSX if available → `knowledge/self-eval/sample_questions.json`. Expectation templates: `knowledge/self-eval/question_expectations.json`. Current structured file: `knowledge/question-bank/structured/wset3_questions.json`. Binary files (XLSX, PDF, etc.) are blocked by `.gitignore`; use markitdown to convert docs before committing.

---

## CURRENT TESTING STATUS

- Test count: **262** via `python -m unittest discover -s tests -v` (255 regular + 7 slow, skipped by default)
- All 262 pass locally. (`pytest` not installed in active venv — use `python -m unittest`)
- Slow golden baseline: `RUN_SLOW_TESTS=1 python -m unittest tests.test_golden_self_eval -v` → 7/7 OK
- Brutal self-eval: 25 questions, no failure labels, no retrieval gaps, no SAT weaknesses.
- Known retrieval weakness: `missing_keyword_support` count = 5 (frozen in golden baseline).
- Snapshots: green for all 25 fixtures.

---

## ACTIVE REMEDIATION PLAN — WHERE WE ARE

Plan document: `docs/backend_stability_remediation_plan.md`
Workflow: Claude plans/reviews/writes prompts → Codex implements → Claude verifies → commit only when green.

### ALL BATCHES COMPLETE ✅

**Batch A — R1-C** (question runner config extraction) ✅
- `knowledge/self-eval/sample_questions.json`, `question_expectations.json` extracted
- `tests/test_question_runner_expectations.py` added
- Result: 236 → 238 tests

**Batch B — R1-A, R1-B, R1-D + R2-A, R2-B, R2-C** ✅
- `SAT_EVALUATION_TERMS` in `tools/constants.py`; `tokenize_term()` added
- `knowledge/config/retrieval_config.json`, `explanation_priority_config.json` created
- `tools/orchestrator/protocols.py` — typed protocol interfaces
- `evaluation_reporter.py` — explicit `ImportError` for `les_reconciler`
- `tests/test_retrieval_config.py`, `test_constants.py` added
- Result: 238 tests

**Batch C — R3-A (data-driven topic dispatch) + R3-B (score helpers)** ✅
- `knowledge/answer_patterns.json` (41 entries, bilingual, sentinel `__no_cross_language_pattern__`)
- `answer_builder.py`: all 5 dispatch functions data-driven (`_normal_direct_answer`, `_cause_effect_line`, `_exam_line`, `_mini_practice`, `_official_idea_from_text`)
- `score_chunk_for_query()` decomposed into 5 named helpers: `_score_lexical_overlap`, `_score_term_and_concept_matches`, `_score_boost_signals`, `_aggregate_chunk_score`, `_build_score_breakdown`. Orchestrator body ≤20 lines of logic.
- `tests/test_answer_patterns_schema.py` added (8 schema tests)
- Result: 238 → 246 tests

**Batch D — R4-A, R4-B, R4-C** ✅
- `tests/test_regression_r4a.py` — 9 regression tests (Tokaji + forced_causal_chains)
- `knowledge/self-eval/golden_brutal_output.json` — frozen CI baseline
- `tests/test_golden_self_eval.py` — 7 slow golden tests (guard: `RUN_SLOW_TESTS=1`)
- Result: 246 → 262 tests (255 regular + 7 slow)

### Pending tasks

1. **`tests/test_score_components.py`** — unit tests for each of the 5 `score_chunk_for_query` helpers in isolation (from original R3-B plan). Verification: 262+ tests, brutal self-eval `{}`.

All other items in `docs/backend_stability_remediation_plan.md` are either complete or explicitly deferred to post-frontend stabilization (see "Items Explicitly Out of Scope" section).

---

## VERIFICATION GATE PROTOCOL

After every code change:
```
python -m unittest discover -s tests -v   → must stay at 262+ passing
brutal self-eval                          → must stay {}
```
Slow golden suite (only when touching self-eval pipeline):
```
$env:RUN_SLOW_TESTS=1; python -m unittest tests.test_golden_self_eval -v
```
Any regression = rollback that sub-step before proceeding.

---

## DOCUMENTATION CONVENTION

**No binary documents in the repository.** Convert to Markdown first:
```bash
markitdown source.pdf > output.md
markitdown source.docx > docs/output.md
```
Blocked by `.gitignore`: `*.pdf`, `*.doc`, `*.docx`, `*.xls`, `*.xlsx`, `*.ppt`, `*.pptx`, `*.odt`, `*.ods`, `*.odp`.

---

## COGNITIVE ARTIFACT PROTECTION

The following are **machine-local cognitive objects** and must NEVER be committed or deployed to Vercel/GitHub public. Risks: cognitive leakage, operational drift, false authority, learner-data exposure.

| Path | What it is | Risk |
|------|-----------|------|
| `knowledge/nazareth/` | Live LES, session staging, pedagogical memory | Learner state exposure |
| `knowledge/self-eval/reports/` | Dynamic self-eval run outputs | Drift / false authority |
| `knowledge/self-eval/attempts/` | Per-question attempt artifacts | Operational noise |
| `knowledge/retrieval-sandbox/` | Derived retrieval outputs | Contamination |
| `*.jsonl` | Pipeline stream outputs | Machine-local traces |
| `.claude/` | Agent tooling state | Tooling leakage |
| `.vercel/` | Vercel deployment cache | CI contamination |

**What IS intentionally versioned in `knowledge/self-eval/`:**
- `sample_questions.json` — config, not runtime output
- `question_expectations.json` — config, not runtime output
- `golden_brutal_output.json` — intentional CI baseline (future R4-C)

**Regression harness is protected:** `tests/fixtures/tutor_snapshots/` has explicit `!`-negations in `.gitignore` as a safety net. This must never be excluded.

---

## WHAT NOT TO TOUCH

- Do not refactor `answer_builder.py` behavior-dense code without snapshots
- Do not set any governance flag to True
- Do not add LLM, API, embeddings, vector DB, or cloud paths
- Do not expose anything to a frontend yet
- Do not add official grading authority to any module
- Do not alter snapshot outputs without explicit regression intent
- Do not run R3-B before R1-B is confirmed complete (it is — `retrieval_config.json` exists)

---

## REPO STATUS (as of last session)

Latest commits (session 2026-05-24):
- `feat(batch-c): R3-A data-driven topic dispatch in answer_builder; add schema tests`
- `refactor(batch-c): decompose score_chunk_for_query into named helpers (R3-B)`
- `feat(batch-d): R4-A regression tests (Tokaji + causal chains); R4-C golden CI baseline`

Dirty worktree (not committed — runtime / local only):
- `knowledge/nazareth/epistemic_state.json`, `session_staging.json` — modified locally (machine-local cognitive objects, never commit)
- `knowledge/self-eval/attempts/` — runtime self-eval outputs (gitignored)

Pending commit (next session):
```
git add CLAUDE.md tests/test_score_components.py
git commit -m "docs: update CLAUDE.md to completed plan state; add R3-B score component tests"
git push
```

---

*This file is a development planning document. It does not represent WSET assessment or examiner evaluation.*
