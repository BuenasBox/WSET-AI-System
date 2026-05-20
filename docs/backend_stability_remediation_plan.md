# Backend Stability Remediation Plan
**Date:** 2026-05-19  
**Based on:** `docs/backend_technical_debt_audit.md` (2026-05-17, updated 2026-05-19)  
**Constraint:** Deterministic neuro-symbolic ITS. No LLM, no embeddings, no vector DB, no cloud, no frontend.  
**Governance invariant:** `safe_for_examiner=False` and `examiner_scoring_allowed=False` must remain false throughout all remediation work.  
**Test baseline:** 231 tests passing. Brutal self-eval: `{}`. Any phase that breaks either condition must be rolled back.

---

## Overview

13 of 21 original before-frontend blockers have been resolved (see audit status update). This plan covers the remaining open items, organized into four sequenced phases. Each phase is self-contained and can be handed to Codex as a discrete implementation task.

**Foundation already in place:**
- `tools/constants.py` — PROJECT_ROOT, path constants, governance sentinels
- `knowledge/config/domain_expansions.json` — expansion config loaded from JSON
- `knowledge/config/sat_observation_aliases.json` — SAT alias table
- `_tokens()` — Unicode-aware tokenizer in `tutor_retrieval_sandbox.py`

---

## Phase R1 — Config Extraction (Hardcoded Data → JSON) ★★★ Highest Priority

**Why first:** These are pure data-extraction tasks with zero logic changes. They reduce the surface area for all subsequent phases. Each item is independently executable by Codex. No snapshot regeneration required if extractions are exact.

**Snapshot stability contract:** For each item, Codex must run brutal self-eval before and after. If any label count changes, the extraction is incorrect and must be reverted.

### R1-A: `answer_builder.py` — SAT detection vocabulary to constants (A-02)

`tools/constants.py` already has `SAFE_FOR_EXAMINER` and `EXAMINER_SCORING_ALLOWED` (A-03 resolved). Remaining work is detection/control vocabulary only — do NOT move user-facing answer strings to constants.

1. Find every **detection or control** usage of BICL/SAT terms (`"balance"`, `"intensity"`, `"complexity"`, `"length"`, `"BICL"`, `"finish"`) in `answer_builder.py` — i.e., terms used in `if`/`in` checks, not terms that appear in output prose.
2. Add `SAT_EVALUATION_TERMS: frozenset[str] = frozenset({...})` to `tools/constants.py`.
3. Replace only the detection-context occurrences with membership checks against `SAT_EVALUATION_TERMS`. Leave all output prose strings unchanged.
4. Run: `pytest tests/ -x -q` → must stay at 231+ passing. Brutal self-eval must stay `{}`.

**Files touched:** `tools/constants.py`, `tools/tutor/answer_builder.py`

---

### R1-B: `tutor_retrieval_sandbox.py` — Score weights to config (A-05, A-07)

`PRIORITY_BOOSTS` magic floats and 19+ inline score weights in `score_chunk_for_query()` must move to config.

1. Extract `PRIORITY_BOOSTS` dict (current values: `{"high": 0.12, "medium": 0.06, "low": 0.02}`) to `knowledge/config/retrieval_config.json`. Add a `"calibration_notes"` field per entry explaining rationale.
2. Extract all inline score weights (`score += 0.15`, `score += 0.30`, etc.) from `score_chunk_for_query()` to a `SCORE_WEIGHTS` section in `retrieval_config.json`. Each key must be a descriptive name (e.g., `"keyword_exact_match"`, `"domain_expansion_hit"`, `"priority_boost_golden"`).
3. Load both sections once at module import via `_load_retrieval_config()`. Use `functools.lru_cache(maxsize=1)`.
4. Replace all inline magic numbers in `score_chunk_for_query()` with `SCORE_WEIGHTS["<key>"]` lookups.
5. Tests: add `tests/test_retrieval_config.py` — verify every score weight key referenced in code exists in JSON. Brutal self-eval `{}` must hold.

**Files touched:** `tools/retrieval/tutor_retrieval_sandbox.py`, `knowledge/config/retrieval_config.json` (new), `tests/test_retrieval_config.py` (new)

---

### R1-C: `question_runner.py` — Sample questions and expectation templates to JSON (A-11, A-12)

1. Move 5 hardcoded sample questions in `question_runner.py` to `knowledge/self-eval/sample_questions.json`. Load at runtime.
2. Move `_infer_expectations()` topic branches to `knowledge/self-eval/question_expectations.json`. Schema: array of objects with `topic_pattern` (regex string), `expected_keywords` (list), `expected_causal_links` (list), `expected_topics` (list).
3. `_infer_expectations()` becomes a regex-lookup over the JSON array. First matching `topic_pattern` wins.
4. Tests: add `tests/test_question_runner_expectations.py` — verify all 5 sample questions produce non-empty expectations. Brutal self-eval `{}` must hold.

**Files touched:** `tools/self_eval/question_runner.py`, `knowledge/self-eval/sample_questions.json` (new), `knowledge/self-eval/question_expectations.json` (new), `tests/test_question_runner_expectations.py` (new)

---

### R1-D: `explanation_priority.py` — SEVERITY_WEIGHT and DEPTH_TO_STYLE to config (A-22)

⚠️ **Correct file path:** `tools/tutor/explanation_priority.py` (not `tools/pedagogy/`).  
⚠️ **Dependency:** `DEPTH_TO_STYLE` is imported by `tools/tutor/answer_builder.py` (line 22). Must preserve the public export from `explanation_priority.py` after extraction, or update the import in `answer_builder.py` to load from config directly.

1. Move `SEVERITY_WEIGHT` and `DEPTH_TO_STYLE` dicts to `knowledge/config/explanation_priority_config.json`. Add `"rationale"` field per entry.
2. Load at import with `lru_cache`. Keep module-level `SEVERITY_WEIGHT` and `DEPTH_TO_STYLE` names as public symbols so existing imports continue to work.
3. Tests: verify loaded config matches expected keys. Verify `answer_builder.py` still imports `DEPTH_TO_STYLE` without error. Brutal self-eval `{}`.

**Files touched:** `tools/tutor/explanation_priority.py`, `knowledge/config/explanation_priority_config.json` (new)

---

## Phase R2 — Path Portability and Import Structure (B-01, B-02, remaining B-03–05 edge cases)

**Why second:** B-09 is resolved (constants.py). This phase finishes the import cleanup and fixes the one silent-failure risk (B-01).

**Snapshot stability contract:** Same as R1. No logic changes — only import reorganization.

### R2-A: Fix silent `les_reconciler` import in `evaluation_reporter.py` (B-01)

This is the only **Critical** fragile-coupling item still open. The `try/except` around the import silently swallows import errors.

1. Move `from tools.orchestrator.les_reconciler import reconcile_les_from_feedback` to module top in `evaluation_reporter.py`.
2. Wrap with: `try: ... except ImportError as e: raise ImportError(f"les_reconciler unavailable: {e}") from e` — explicit, not silent.
3. Test: `tests/test_evaluation_reporter.py` — add a test that verifies `les_reconciler` is importable and the import does not silently fail.

**Files touched:** `tools/self_eval/evaluation_reporter.py`, `tests/test_evaluation_reporter.py` (new test)

---

### R2-B: Define protocol interfaces for orchestrator dependencies (B-02)

`orchestrator.py` directly imports 5 concrete modules. Introduce thin typed `Protocol` interfaces.

1. Create `tools/orchestration/protocols.py` defining `AnswerBuilderProtocol`, `RetrievalProtocol`, `LearnerStateProtocol`, `ScaffoldingProtocol`.
2. Each protocol defines only the methods `orchestrator.py` actually calls — minimal surface.
3. Update `orchestrator.py` to accept these protocol types in function signatures (type hints only — no runtime change).
4. This is a type-safety change only; no behavior changes. All existing tests must pass unchanged.

**Files touched:** `tools/orchestration/protocols.py` (new), `tools/orchestration/orchestrator.py` (type hints only)

---

### R2-C: Unify tokenizer into shared utility (L-02)

`_tokens()` in `tutor_retrieval_sandbox.py` and the tokenizer in `explanation_priority.py` are separate implementations. L-01 is fixed, but they should be unified.

1. Add `tokenize_term(text: str) -> list[str]` to `tools/constants.py` using the `r"(?u)\b[^\W\d_](?:[^\W_]|['-])*\b"` regex.
2. Update `tutor_retrieval_sandbox.py` to call `tokenize_term` (or keep internal `_tokens` as a thin wrapper — either is acceptable).
3. Update `explanation_priority.py` to use the same function.
4. Tests: `tests/test_constants.py` — add tokenizer unit tests including Spanish accent cases. All existing tests must pass.

**Files touched:** `tools/constants.py`, `tools/retrieval/tutor_retrieval_sandbox.py`, `tools/pedagogy/explanation_priority.py`, `tests/test_constants.py` (new tests)

---

## Phase R3 — Architecture Refactor (A-01, C-01, C-02–05, L-05)

**Why third:** These are the largest structural changes. They build on the data extraction done in R1 (JSON configs must exist before dispatch tables can reference them). A-01 is the highest-risk item in the entire audit. Requires the most careful snapshot testing.

**Snapshot stability contract:** Before starting R3, regenerate `knowledge/self-eval/snapshots/` with current baseline. Run brutal self-eval immediately before and immediately after each sub-item. Any snapshot drift must be diagnosed before proceeding.

### R3-A: Data-driven topic dispatch in `answer_builder.py` (A-01, C-02–05, L-05) — **Highest risk item**

This is the ~550-line if/elif dispatch split across 5 functions. This is the single most complex remediation task.

**Pre-condition:** R1-A must be complete (constants.py has SAT terms).

1. Create `knowledge/answer_patterns.json`. Schema:
   ```json
   [
     {
       "topic_slug": "tannin_structure",
       "patterns_es": ["tanino", "estructura tánica"],
       "patterns_en": ["tannin", "tannin structure"],
       "cause_effect": "...",
       "exam_formulation": "...",
       "mini_practice_prompt": "...",
       "official_idea_hint": "..."
     }
   ]
   ```
2. Populate by extracting existing if/elif branches from all 5 functions into this schema. Must preserve bilingual coverage exactly. After extraction, add validation: every topic slug must have at least one ES and one EN pattern variant (resolves L-05).
3. Replace `_normal_direct_answer()`, `_cause_effect_line()`, `_exam_line()`, `_mini_practice()`, `_official_idea_from_text()` with table-lookup functions.
4. Implement in incremental sub-steps. After each function is refactored, run the full test suite + brutal self-eval before touching the next function.
5. Add `tests/test_answer_patterns_schema.py` — asserts every topic slug has ES+EN patterns and all 5 response section fields populated.

**Files touched:** `knowledge/answer_patterns.json` (new), `tools/tutor/answer_builder.py`, `tests/test_answer_patterns_schema.py` (new)

---

### R3-B: Decompose `score_chunk_for_query()` (C-01)

**Pre-condition:** R1-B must be complete (score weights in JSON config).

Extract 19+ scoring components into named helper functions:

- `_score_keyword_exact_match(chunk_tokens, query_tokens) -> float`
- `_score_domain_expansion_overlap(chunk_tokens, expanded_terms) -> float`
- `_score_priority_boost(chunk_metadata, boosts) -> float`
- `_score_causal_chain_relevance(chunk, causal_chains) -> float`
- `_score_sat_observation_overlap(chunk_tokens, sat_observations) -> float`
- Any remaining components each get a named function

`score_chunk_for_query()` becomes an orchestrator calling each helper and summing results. Total function body should be ≤30 lines.

Tests: all existing retrieval tests must pass. Add `tests/test_score_components.py` — unit tests for each helper function in isolation.

**Files touched:** `tools/retrieval/tutor_retrieval_sandbox.py`, `tests/test_score_components.py` (new)

---

## Phase R4 — Test Coverage and CI Hardening (T-01, T-02, T-04, T-06, B-01 test)

**Why last:** Tests validate the previous phases. Some tests (T-04, T-06) require R3 to be complete before they are meaningful.

### R4-A: Regression tests for known fixed bugs (T-01, T-02)

1. **T-01** — Add test: answer containing `"tokaji"` does NOT produce `weak_exam_register` label. (`tests/test_answer_comparator.py`)
2. **T-02** — Add test: context package with `forced_causal_chains` does NOT produce `shallow_retrieval=True`. (`tests/test_answer_comparator.py`)

### R4-B: Schema validation for topic slug coverage (T-04)

**Pre-condition:** R3-A must be complete.

After `answer_patterns.json` exists, add `tests/test_answer_patterns_schema.py` (may already exist from R3-A):
- Every topic slug in `answer_patterns.json` must have non-empty entries for all 5 response section fields.
- Every topic slug must have ≥1 ES pattern and ≥1 EN pattern.
- Run as part of standard `pytest` — not a separate CI step.

### R4-C: Golden output CI baseline (T-06)

1. Run brutal self-eval and save output to `knowledge/self-eval/golden_brutal_output.json`. Format: `{"label_counts": {...}, "failure_count": 0, "test_run_date": "2026-05-19"}`.
2. Add `tests/test_golden_self_eval.py` that loads `golden_brutal_output.json` and compares label counts against a fresh brutal self-eval run. Test fails if any failure label count increases.
3. This test is slow (~2 minutes) — mark with `@pytest.mark.slow` and run separately from the main fast suite.

**Files touched:** `knowledge/self-eval/golden_brutal_output.json` (new), `tests/test_golden_self_eval.py` (new)

---

## Sequencing Summary

```
R1-A  →  independent (constants.py already exists)
R1-B  →  independent
R1-C  →  independent
R1-D  →  independent

R2-A  →  independent (fixes B-01)
R2-B  →  independent
R2-C  →  after L-01 confirmed (already fixed)

R3-A  →  after R1-A (needs constants.py SAT terms)
R3-B  →  after R1-B (needs retrieval_config.json)

R4-A  →  independent
R4-B  →  after R3-A
R4-C  →  after R3 complete
```

R1 items can all be run in parallel by Codex (they touch different files). R2 items are also independently executable. R3 items must be sequential (R3-A is high risk, isolate from R3-B). R4 items are mostly independent.

---

## Codex Handoff Notes

Each phase above is designed to be a self-contained Codex prompt. When handing off to Codex:

1. Paste the phase section verbatim.
2. Prepend the standard governance header:
   ```
   GOVERNANCE (immutable):
   - safe_for_examiner must remain False everywhere
   - examiner_scoring_allowed must remain False everywhere
   - Do NOT import tools.orchestrator from leaf modules
   - Do NOT call any external services, LLMs, APIs, embeddings, or vector DB
   - Do NOT write to files outside knowledge/ and tools/
   - This system is deterministic. All outputs must be reproducible.
   ```
3. Append: "Run `pytest tests/ -x -q` after each sub-step. Report test count and any failures. Run brutal self-eval at end of phase and report label counts. Do not proceed if any test breaks."
4. Review the Codex report here before committing.

---

## Items Explicitly Out of Scope

The following audit items are **not** before-frontend blockers and are deferred to post-frontend stabilization:

| ID | Reason for deferral |
|----|---------------------|
| A-06 | Documentation-only change; no behavior impact |
| A-08 | `COGNITIVE_ERROR_LABELS` ordering is stable; low risk |
| A-09 | Balance thresholds are calibrated and working; renaming is cosmetic |
| A-10 | Misconception signal terms work correctly; low risk of drift |
| A-13 | `openpyxl` lazy import is functional; declare in requirements.txt separately |
| A-17 | `DEFAULT_LES` schema is stable |
| A-18 | LES config values are stable and tested |
| A-20/A-21 | Misconception stopwords are stable; calibration log is nice-to-have |
| A-23–A-25 | Scaffolding policy magic numbers work correctly |
| A-28 | Knowledge tracing priors are calibrated and stable |
| B-06 | Comparator signal terms are stable; low coupling risk |
| B-07 | Misconception prepass path resolution works; refactor is cosmetic |
| B-08 | `openpyxl` optional dep; declare in requirements.txt |
| C-06–C-08 | Function length issues that follow naturally from R3 |
| L-03 | No French/Portuguese content in scope |
| L-04 | Vague-term Spanish coverage is functional |
| P-03 | Module-level dict is already O(1); low impact |
| P-04 | Misconception prepass cache; add after R1 with `lru_cache` |
| T-05 | Follows from R2-A fix |
| G-01–G-03 | Governance is clean; monitoring only |

---

*This plan is a development planning document. It does not represent WSET assessment or examiner evaluation.*
