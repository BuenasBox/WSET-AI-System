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

- Test count: **238** via `python -m unittest discover -s tests -v`
- All 238 pass locally. (`pytest` not installed in active venv — use `python -m unittest`)
- Brutal self-eval: 25 questions, no failure labels, no retrieval gaps, no SAT weaknesses.
- Known retrieval weakness: `missing_keyword_support` count = 5.
- Snapshots: green for all 25 fixtures.

---

## ACTIVE REMEDIATION PLAN — WHERE WE ARE

Plan document: `docs/backend_stability_remediation_plan.md`
Workflow: Claude plans/reviews/writes prompts → Codex implements → Claude verifies → commit only when green.

### Completed batches

**Batch A — R1-C (question runner config extraction)**
- `knowledge/self-eval/sample_questions.json` — 5 sample questions extracted
- `knowledge/self-eval/question_expectations.json` — expectation templates extracted
- `question_runner.py` updated to load both from JSON via `lru_cache`
- `tests/test_question_runner_expectations.py` added (5 sample questions × non-empty expectations)
- Fixed: `SELF_EVAL_DIR` import was missing; `SELF_SAMPLE_ACIDITY_01` needed bidirectional acidity pattern in expectations
- Result: 236 → 238 tests green, brutal self-eval `{}`

**Batch B — R1-A, R1-B, R1-D + R2-A, R2-B, R2-C**
- `SAT_EVALUATION_TERMS` frozenset added to `tools/constants.py`
- `answer_builder.py` detection-context occurrences replaced with `SAT_EVALUATION_TERMS` membership checks
- `knowledge/config/retrieval_config.json` created with `PRIORITY_BOOSTS` and `SCORE_WEIGHTS`
- `knowledge/config/explanation_priority_config.json` created with `SEVERITY_WEIGHT` and `DEPTH_TO_STYLE`
- `tools/constants.py` — `tokenize_term()` Unicode-aware tokenizer added
- `tools/orchestrator/protocols.py` — `AnswerBuilderProtocol`, `RetrievalProtocol`, `LearnerStateProtocol`, `ScaffoldingProtocol`
- `evaluation_reporter.py` — explicit `ImportError` for `les_reconciler` (B-01 fixed)
- `tutor_retrieval_sandbox.py` — `_tokens()` wraps `tokenize_term()`
- `explanation_priority.py` — reuses `tokenize_term()`
- Tests added: `test_retrieval_config.py`, `test_constants.py`
- Result: 238 tests green, brutal self-eval `{}`

**Batch C (in progress) — R3-A: data-driven topic dispatch in `answer_builder.py`**

`knowledge/answer_patterns.json` created with full topic dispatch table. Schema per entry:
```json
{
  "topic_slug": "...",
  "patterns_es": ["..."],
  "patterns_en": ["__no_cross_language_pattern__"],
  "normal_answer": "...",
  "cause_effect": "...",
  "exam_formulation": "...",
  "mini_practice_prompt": "...",
  "official_idea_hint": "..."
}
```
Null fields are skipped by the corresponding function's lookup loop. Use `"__no_cross_language_pattern__"` sentinel for entries that only apply in one language.

Bidirectional patterns required: Spanish word order varies — always include both directions in `patterns_es`.

`_load_answer_patterns()` + `_match_pattern()` added to `answer_builder.py`.

Sub-steps completed in R3-A:
- R3-A-1: `knowledge/answer_patterns.json` created ✅
- R3-A-2: `_load_answer_patterns()` + `_match_pattern()` added ✅
- R3-A-3: `_normal_direct_answer()` refactored ✅ (fixed bidirectional patterns for Q7 oxidative, Q23 sparkling)
- R3-A-4: `_cause_effect_line()` refactored ✅
- R3-A-5: `_exam_line()` refactored ✅

**R3-A-6: `_mini_practice()` — BLOCKED, reverted, fix identified, NOT YET applied**

Root cause: Q11 (`¿Cuál de los siguientes climas se asocia comúnmente con una alta acidez en los vinos blancos?`) needs mini practice `"Reescribe esta frase: 'high acidity significa baja calidad', usando balance y estilo del vino."` — but adding `"acidez"` to the existing `acidity_quality_es` entry causes `_exam_line()` (already refactored) to also match and return the wrong exam_formulation for Q11.

**Correct fix (ready to send to Codex):**
Add a NEW entry to `knowledge/answer_patterns.json` with `topic_slug: "acidity_mini_es"`, `patterns_es: ["acidez"]`, ALL fields null except `mini_practice_prompt`. This way `_exam_line()` matches but skips (null), `_mini_practice()` matches and returns.

```json
{
  "topic_slug": "acidity_mini_es",
  "patterns_es": ["acidez"],
  "patterns_en": ["__no_cross_language_pattern__"],
  "normal_answer": null,
  "cause_effect": null,
  "exam_formulation": null,
  "mini_practice_prompt": "Reescribe esta frase: 'high acidity significa baja calidad', usando balance y estilo del vino.",
  "official_idea_hint": null
}
```

State after last Codex run: 238 tests green, brutal self-eval `{}`, `_mini_practice()` refactor reverted.

### Pending tasks (in order)

1. **R3-A-6** — Apply `acidity_mini_es` entry + refactor `_mini_practice()`. Verification: 238+ tests, snapshot Q11 passes, brutal self-eval `{}`.
2. **R3-A-7** — Refactor `_official_idea_from_text()` using `"official_idea_hint"` field. Same verification gate.
3. **R3-A-8** — Create `tests/test_answer_patterns_schema.py`: every topic slug has ES+EN patterns, all 5 response fields populated (null is allowed per-field, but structure must be valid).
4. **R3-B** — Decompose `score_chunk_for_query()` into named helpers (requires `retrieval_config.json` from R1-B, already done). Target: ≤30 line orchestrator body.
5. **Commit Batch C** — after all above green.
6. **Batch D: R4-A** — regression tests for Tokaji (must not trigger `weak_exam_register`) and `forced_causal_chains` (must not produce `shallow_retrieval=True`). Tests only — no behavior changes.
7. **Batch D: R4-B** — `tests/test_answer_patterns_schema.py` (may overlap with R3-A-8).
8. **Batch D: R4-C** — golden output CI baseline (`knowledge/self-eval/golden_brutal_output.json` + `tests/test_golden_self_eval.py`, marked `@pytest.mark.slow`).

---

## VERIFICATION GATE PROTOCOL

After every single function refactor in R3-A, before touching the next:
```
python -m unittest discover -s tests -v   → must stay at 238+ passing
brutal self-eval                          → must stay {}
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

Latest commit: `06bf369 chore: block binary doc formats globally; add markitdown convention`

Dirty worktree:
- `.gitignore`, `README.md` — binary doc rules added (uncommitted)
- `knowledge/nazareth/epistemic_state.json`, `session_staging.json` — modified locally
- `knowledge/question-bank/raw/WSET3_Banco_Maestro_V9.xlsx` — deleted from git index (git rm --cached done)
- `.claude/` — untracked

Recommended next commit after R3-A-6 fix is confirmed green:
```
git add .gitignore README.md CLAUDE.md
git commit -m "docs: add CLAUDE.md project memory; finalize binary doc gitignore"
```

---

*This file is a development planning document. It does not represent WSET assessment or examiner evaluation.*
