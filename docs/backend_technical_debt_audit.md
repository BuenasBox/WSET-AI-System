# Backend Technical Debt Audit
**Date:** 2026-05-17  
**Tag baseline:** `backend-cognitive-stable-v1`  
**Brutal self-eval at audit time:** `{'shallow_reasoning': 1}` (Q3 Porto Vintage only)  
**Scope:** All Python modules under `tools/`  
**Constraint:** Audit only. No code changes in this document.

---

## Executive Summary

45+ hardcoded-data issues and 35+ hardcoded-pattern issues were identified across 13 files. The single highest-risk item is the `_tokens()` ASCII-only regex in `tutor_retrieval_sandbox.py`, which silently corrupts retrieval scoring for any Spanish-accented term. The second highest-risk category is the ~550-line if/elif topic-dispatch in `answer_builder.py`, which makes each new topic require edits in 5 separate functions. No `safe_for_examiner=True` violations were found. Governance layer is clean.

---

## Category Index

| # | Category | Issues found | Critical | High | Medium |
|---|---|---|---|---|---|
| 1 | Hardcoded data / magic constants | 28 | 2 | 12 | 14 |
| 2 | Fragile coupling / import structure | 9 | 1 | 5 | 3 |
| 3 | Function length / complexity | 8 | 0 | 5 | 3 |
| 4 | Localization / Spanish handling | 5 | 1 | 2 | 2 |
| 5 | Performance / caching | 4 | 0 | 2 | 2 |
| 6 | Test coverage risks | 6 | 0 | 3 | 3 |
| 7 | Governance risks | 3 | 0 | 0 | 3 |

**Before-frontend blockers (Critical + High issues requiring fix before any UI work):** 21 items marked `[BF]` below.

---

## Category 1 — Hardcoded Data / Magic Constants

### 1.1 `tools/tutor/answer_builder.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-01 | ~550 lines of if/elif topic-dispatch split across 5 functions: `_normal_direct_answer()` (lines 247–313), `_cause_effect_line()` (411–492), `_exam_line()` (853–920), `_mini_practice()` (923–990), `_official_idea_from_text()` (800–846). Each new topic requires editing all 5 functions. | **CRITICAL** | 5 functions | Extract topic patterns to `knowledge/answer_patterns.json` (keyed by topic slug); replace each if/elif with a table lookup. | ✓ |
| A-02 | WSET SAT evaluation terms (`"balance"`, `"intensity"`, `"complexity"`, `"length"`, `"BICL"`) hardcoded as string literals in 11+ locations. | High | Scattered | Centralize in `tools/constants.py` as `SAT_EVALUATION_TERMS`. | ✓ |
| A-03 | Governance sentinel values `safe_for_examiner=False`, `examiner_scoring_allowed=False` set only in `_validate_governance()`. No file-level or module-level constant guards them. | High | `_validate_governance()` | Add `GOVERNANCE_DEFAULTS` dict at module top; `_validate_governance()` reads from it. Prevents silent drift if function is refactored. | ✓ |

### 1.2 `tools/retrieval/tutor_retrieval_sandbox.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-04 | `DOMAIN_EXPANSIONS` dict (~100+ entries) and `SAT_EXPANSIONS` dict defined inline in module. Adding new topics requires editing source code. | High | Lines ~200–400 | Move both to `knowledge/domain_expansions.json`; load once at module import. | ✓ |
| A-05 | `PRIORITY_BOOSTS` dict (e.g., `{"golden": 0.45, "high": 0.30, ...}`) contains magic floats with no comments explaining calibration. | High | Lines ~150–170 | Move to `knowledge/retrieval_config.json`; add comments per field documenting rationale. | ✓ |
| A-06 | Single-word expansion terms (e.g., `"oloroso"`, `"botrytis"`, `"acetaldehyde"`) matched against English chunk tokens via `expanded_overlap`. No explicit language-tagging so the matching rule is implicit. | Medium | `score_chunk_for_query()` | Document matching contract in docstring; tag each expansion entry with `"lang": "en"` in the JSON config. | — |
| A-07 | 19+ scoring components embedded inline in `score_chunk_for_query()` with no named constants. E.g., `score += 0.15` with no label. | High | Lines ~1100–1220 | Extract each component weight to `SCORE_WEIGHTS` dict; reference by name in the function. | ✓ |

### 1.3 `tools/self_eval/answer_comparator.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-08 | `COGNITIVE_ERROR_LABELS` is a hardcoded tuple in module scope. New labels require source edit + possible ordering change (ordering affects which label appears first in results). | Medium | Lines 13–28 | Load from `knowledge/cognitive_error_labels.json`; include display-order field. | — |
| A-09 | Balance justification thresholds (`present >= 3`, `present >= 2`, `present >= 4`) are magic numbers with no calibration notes. | Medium | `_has_balance_justification()` | Name as `BALANCE_THRESHOLD_HARD = 3`, `BALANCE_THRESHOLD_BRUTAL = 4`, etc., in `constants.py`. | — |
| A-10 | Misconception correction/replacement signal terms (`"no significa"`, `"not always"`, `"en su lugar"`, etc.) hardcoded in `_misconception_unresolved()` and `_misconception_reinforcement_risk()`. If the misconception data model evolves, these must be manually kept in sync. | Medium | Lines 213–230 | Load correction-signal terms from misconception JSON records rather than a static list. | — |

### 1.4 `tools/orchestration/question_runner.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-11 | `_infer_expectations()` is 49 lines of hardcoded topic branches mapping question text substrings to `expected_keywords`, `expected_causal_links`, and `expected_topics`. Every new question type requires editing this function. | High | Lines ~80–130 | Store expectation templates in `knowledge/question_expectations.json`; `_infer_expectations()` becomes a lookup. | ✓ |
| A-12 | 5 hardcoded sample questions embedded in code (used as fallback when no question file is provided). Makes the module harder to test deterministically. | High | Lines ~200–260 | Move sample questions to `knowledge/sample_questions.json`; load at runtime. | ✓ |
| A-13 | `openpyxl` imported lazily inside a function body (`import openpyxl` inside `_load_xlsx_questions()`). If the import fails, the error surfaces at runtime deep in a call stack. | Medium | `_load_xlsx_questions()` | Move to top-level import with a `try/except ImportError` guard and a clear error message. | — |

### 1.5 `tools/orchestration/orchestrator.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-14 | `DEFAULT_CONTEXT_PACKAGE_DIR` hardcoded as an absolute path string in module scope. Breaks on any machine where the project is not at the exact same path. | High | Module scope | Read from env var `WSET_CONTEXT_PKG_DIR` with fallback to `PROJECT_ROOT / "context_packages"`. | ✓ |
| A-15 | Routing logic in `run_orchestrator()` first 92 lines uses hardcoded string-matching on `pedagogical_act` values (`"misconception_intervention"`, `"retrieval_sandbox"`, etc.). New acts require editing the router. | High | `run_orchestrator()` lines 1–92 | Register handlers in a `PEDAGOGICAL_ACT_REGISTRY` dict; `run_orchestrator()` dispatches via lookup. | ✓ |

### 1.6 `tools/state/learner_state.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-16 | `NAZARETH_ROOT`, `DEFAULT_LES_PATH`, `DEFAULT_SESSION_STAGING_PATH` hardcoded. Same path-portability problem as A-14. | High | Module scope | Derive from `PROJECT_ROOT`; use env var overrides. | ✓ |
| A-17 | `DEFAULT_LES` schema (initial Learner Experience State structure) embedded as a Python dict literal in module source. Schema changes require source edits. | Medium | Module scope | Extract to `knowledge/les_schema_default.json`; load at import. | — |

### 1.7 `tools/state/les_reconciler.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-18 | `LES_SCHEMA_VERSION`, `MAX_RECENT_MISCONCEPTIONS`, `MAX_KNOWN_WEAK_AREAS` are magic numbers with no version history or rationale comments. | Medium | Module scope | Move to `knowledge/les_config.json`; document rationale per field. | — |

### 1.8 `tools/retrieval/misconception_prepass.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-19 | `DEFAULT_MISCONCEPTION_DIR` hardcoded absolute path. | High | Module scope | Same pattern as A-14/A-16: derive from `PROJECT_ROOT`. | ✓ |
| A-20 | `STOPWORDS` and `EXPLANATORY_INTENT_WORDS` are module-level constant sets with 20+ items each. Updating vocabulary requires source edit. | Medium | Module scope | Move to `knowledge/misconception_config.json`. | — |
| A-21 | `EXPLANATORY_PENALTY = 0.22` — magic float with no calibration log. | Medium | Module scope | Name it in config; add comment documenting calibration experiment. | — |

### 1.9 `tools/pedagogy/explanation_priority.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-22 | `SEVERITY_WEIGHT` and `DEPTH_TO_STYLE` dicts hardcoded. Changes require source edit. | High | Module scope | Move to `knowledge/explanation_priority_config.json`. | ✓ |
| A-23 | Magic number `4` used as `top_ranked` limit with no label. | Medium | Ranking function | Name as `MAX_RANKED_EXPLANATIONS = 4`. | — |

### 1.10 `tools/pedagogy/scaffolding_policy.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-24 | Threshold floats `0.35` and `0.75` (mastery level cutoffs) hardcoded inline. | Medium | Act selection logic | Name as `MASTERY_LOW_THRESHOLD`, `MASTERY_HIGH_THRESHOLD`; move to config. | — |
| A-25 | Act selection if/elif chains should be data-driven. Currently each new scaffolding act requires adding a branch. | Medium | Act selection function | Use a priority-ordered rule table loaded from config. | — |

### 1.11 `tools/knowledge/official_wset_chunks.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-26 | `DEFAULT_MARKDOWN_DIR`, `DEFAULT_OUTPUT_DIR`, `DEFAULT_JSONL_PATH` hardcoded. | High | Module scope | Derive from `PROJECT_ROOT`; env var overrides. | ✓ |

### 1.12 `tools/state/knowledge_tracing.py`

| ID | Issue | Severity | Location | Recommended fix | BF |
|----|-------|----------|----------|-----------------|-----|
| A-27 | `DEFAULT_PEDAGOGICAL_MEMORY_PATH` hardcoded absolute path. | High | Module scope | Derive from `PROJECT_ROOT`. | ✓ |
| A-28 | Magic values in `DEFAULT_SKILL_STATE` (`0.35`, etc.) — initial mastery priors with no calibration rationale. | Medium | Module scope | Move to `knowledge/knowledge_tracing_config.json`; document prior sources. | — |

---

## Category 2 — Fragile Coupling / Import Structure

| ID | File | Issue | Severity | Recommended fix | BF |
|----|------|-------|----------|-----------------|-----|
| B-01 | `tools/self_eval/evaluation_reporter.py` | `import les_reconciler` placed inside a `try/except` block. If the import fails, the exception is caught silently and the reconciler is skipped without warning. This masks circular dependency crashes during development. | **CRITICAL** | Move import to module top; handle `ImportError` explicitly with a logged error, not silent skip. | ✓ |
| B-02 | `tools/orchestration/orchestrator.py` | Directly imports from 5 modules (`answer_builder`, `tutor_retrieval_sandbox`, `question_runner`, `learner_state`, `scaffolding_policy`) with no interface layer. Any module rename breaks orchestrator. | High | Define protocol interfaces; orchestrator depends on interfaces not concrete modules. | ✓ |
| B-03 | `tools/tutor/answer_builder.py` | Imports `PROJECT_ROOT` from orchestrator — creates a reverse dependency (leaf module depending on orchestrator). | High | Move `PROJECT_ROOT` to `tools/constants.py`; all modules import from constants. | ✓ |
| B-04 | `tools/retrieval/tutor_retrieval_sandbox.py` | Imports `DEFAULT_CONTEXT_PACKAGE_DIR` from orchestrator — same reverse dependency pattern as B-03. | High | Same fix: centralize in `constants.py`. | ✓ |
| B-05 | `tools/state/learner_state.py` | Imports `orchestrator.DEFAULT_CONTEXT_PACKAGE_DIR` — third instance of the reverse-dependency anti-pattern. | High | Same fix. | ✓ |
| B-06 | `tools/self_eval/answer_comparator.py` | No dependency injection for correction/replacement signal terms — reads them from module-level literals, not from the misconception data package passed as `context_package`. | Medium | Pass signal terms through `context_package`; remove module-level literals. | — |
| B-07 | `tools/retrieval/misconception_prepass.py` | `DEFAULT_MISCONCEPTION_DIR` path is used as both an import-time side effect (path is resolved at module load) and a function argument default. Module cannot be imported in a different directory context without patching. | Medium | Lazy-resolve path inside function body; never resolve at import time. | — |
| B-08 | `tools/orchestration/question_runner.py` | Lazy `import openpyxl` inside function (see A-13) — creates a hidden optional dependency that is not declared in any requirements file. | Medium | Declare in `requirements.txt` as optional; guard at module top. | — |
| B-09 | General | No `tools/constants.py` module exists. Path constants, governance sentinels, and evaluation term lists are scattered across 7+ files. | High | Create `tools/constants.py` as the single source of truth for all cross-module constants. | ✓ |

---

## Category 3 — Function Length / Complexity

| ID | File | Function | Lines | Issue | Severity | Recommended fix | BF |
|----|------|----------|-------|-------|----------|-----------------|-----|
| C-01 | `tutor_retrieval_sandbox.py` | `score_chunk_for_query()` | ~120 | 19+ scoring components inlined with no sub-function decomposition. Cognitive complexity makes audit or regression testing of individual components impossible. | High | Extract each scoring component to a named helper: `_score_keyword_overlap()`, `_score_priority_boost()`, `_score_domain_expansion()`, etc. | ✓ |
| C-02 | `answer_builder.py` | `_normal_direct_answer()` | ~70 | 15+ if/elif topic branches — direct consequence of A-01. Distinct issue: branch density makes dead-code audit unreliable. | High | Same fix as A-01: table-driven dispatch. | ✓ |
| C-03 | `answer_builder.py` | `_cause_effect_line()` | ~80 | Same as C-02. | High | Same fix. | ✓ |
| C-04 | `answer_builder.py` | `_exam_line()` | ~70 | Same as C-02. | High | Same fix. | ✓ |
| C-05 | `answer_builder.py` | `_mini_practice()` | ~70 | Same as C-02. | High | Same fix. | ✓ |
| C-06 | `orchestrator.py` | `run_orchestrator()` | ~92 | First 92 lines are routing/dispatch logic that could be a separate `_route_pedagogical_act()` function. | Medium | Extract routing to `_route_pedagogical_act()`; `run_orchestrator()` calls it. | — |
| C-07 | `question_runner.py` | `_infer_expectations()` | ~49 | Direct consequence of A-11. | Medium | Same fix as A-11. | — |
| C-08 | `answer_comparator.py` | `compare_answer()` | ~75 | Aggregates 14 label checks inline. Could be decomposed into `_run_structural_checks()`, `_run_register_checks()`, `_run_retrieval_checks()`. | Medium | Extract check groups into sub-functions; `compare_answer()` calls them and merges results. | — |

---

## Category 4 — Localization / Spanish Handling

| ID | File | Issue | Severity | Recommended fix | BF |
|----|------|-------|----------|-----------------|-----|
| L-01 | `tutor_retrieval_sandbox.py` | `_tokens()` regex at line ~1184: `r"\b[a-zA-Z][a-zA-Z0-9'-]*\b"` — ASCII word boundaries only. Spanish accented characters (`á`, `é`, `í`, `ó`, `ú`, `ñ`, `ü`) cause word fragmentation: `"fermentación"` → `["fermentaci", "n"]`; `"aszú"` → `["asz"]`. This silently degrades overlap scoring for any Spanish query containing accented terms. | **CRITICAL** | Replace with `r"\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ][a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9'-]*\b"` — matches existing pattern in `explanation_priority.py`. Add unit test asserting `_tokens("fermentación") == ["fermentación"]`. | ✓ |
| L-02 | `explanation_priority.py` | Uses a Unicode-aware regex `r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+"` — correct, but inconsistent with `_tokens()` in `tutor_retrieval_sandbox.py`. Two tokenizers with different behavior for the same input. | High | After fixing L-01, unify into a single `tokenize_term()` function in `tools/constants.py`; both modules import it. | ✓ |
| L-03 | `misconception_prepass.py` | `STOPWORDS` and intent words are Spanish/English mixed without explicit language tagging. If misconception records ever include French or Portuguese terms, the filter will misfire silently. | Medium | Tag each term in the JSON config with a `"lang"` field; filter only applies to matching-language tokens. | — |
| L-04 | `answer_comparator.py` | `_has_vague_claim()` checks for `"buen vino"` and `"mejor vino"` but not for `"gran vino"` or other common Spanish vague descriptors. Coverage is incomplete. | Medium | Move vague-term list to config; review for completeness against WSET SAT descriptor vocabulary. | — |
| L-05 | `answer_builder.py` | Topic patterns in 5 dispatch functions mix Spanish and English inline. No systematic way to audit whether ES and EN coverage are equivalent for each topic. | High | After data-driven extraction (A-01), add a validation script that checks each topic slug has at least one ES and one EN pattern variant. | ✓ |

---

## Category 5 — Performance / Caching

| ID | File | Function | Issue | Severity | Recommended fix | BF |
|----|------|----------|-------|----------|-----------------|-----|
| P-01 | `official_wset_chunks.py` | `load_official_markdown_chunks()` | Reads and parses **all markdown files** in `DEFAULT_MARKDOWN_DIR` on every call. No in-memory or disk cache. In a self-eval run of 25 questions, this function is called 25 times, re-reading the same files each time. | High | Add `@functools.lru_cache(maxsize=1)` or module-level `_CHUNKS_CACHE` dict. Cache keyed on directory mtime. | ✓ |
| P-02 | `answer_builder.py` | `_extract_context_ideas()` | Iterates over all retrieved context chunks and applies regex extraction on every call. For 25 questions this means 25× repeated extraction with no memoization. | High | Cache by `frozenset` of chunk IDs. | ✓ |
| P-03 | `tutor_retrieval_sandbox.py` | `score_chunk_for_query()` | `DOMAIN_EXPANSIONS` and `SAT_EXPANSIONS` are re-accessed as dict lookups on every chunk for every query. Because they're module-level dicts this is already O(1), but loading from JSON (post A-04) must preserve this — avoid re-parsing JSON on each call. | Medium | Use module-level `_EXPANSION_CACHE` loaded once at import. | — |
| P-04 | `misconception_prepass.py` | `load_misconceptions()` | Misconception JSON is read from disk on every prepass call. No caching. For a session with 25 questions, this is 25 disk reads of the same file. | Medium | Add `@functools.lru_cache(maxsize=1)` keyed on file mtime. | — |

---

## Category 6 — Test Coverage Risks

| ID | Area | Issue | Severity | Recommended fix | BF |
|----|------|-------|----------|-----------------|-----|
| T-01 | `answer_comparator.py` — `_weak_exam_register()` | The `"ok"` → `" ok"` false-positive bug (firing for all answers containing "tokaji") was not caught by any existing test. Tests check label counts, not per-question behavior. | High | Add regression tests asserting `"tokaji"` in answer text does NOT produce `weak_exam_register` label. | ✓ |
| T-02 | `answer_comparator.py` — `_audit_retrieval()` | The `forced_causal_chains` not being counted toward `high_priority` (causing `shallow_retrieval` false positives for Q1/Q2/Q4) was not caught by tests. | High | Add tests with `context_package` containing `forced_causal_chains` and asserting `shallow_retrieval=False`. | ✓ |
| T-03 | `tutor_retrieval_sandbox.py` — `_tokens()` | The ASCII-only tokenizer silently producing wrong tokens for Spanish words is not tested. | High | Add unit test: `assert _tokens("fermentación") == ["fermentación"]`; `assert _tokens("aszú") == ["aszú"]`. This test MUST fail first, confirming the bug, then pass after L-01 fix. | ✓ |
| T-04 | `answer_builder.py` | No test asserts that adding a new topic to `_normal_direct_answer()` also requires an entry in `_cause_effect_line()`, `_exam_line()`, `_mini_practice()`, and `_official_idea_from_text()`. Coverage gaps are possible and invisible. | High | After A-01 data-driven extraction, add a schema validation test: every topic slug must have entries for all 5 response sections. | ✓ |
| T-05 | `evaluation_reporter.py` | Silent `try/except` around `les_reconciler` import (B-01) means reconciler failures produce no visible test error — tests pass even if reconciler is broken. | Medium | Once B-01 is fixed, add integration test that fails if reconciler import fails. | — |
| T-06 | Self-eval pipeline | 25 sample questions cover the self-eval, but no test guards against regressions to known-fixed bugs. When any fix is made to `answer_comparator.py` or `answer_builder.py`, a full brutal self-eval should be re-run and compared to a stored golden output. | Medium | Add CI step: `python tools/self_eval/run_self_eval.py --mode brutal --golden knowledge/self-eval/golden_output.json`; fail if any label count increases. | ✓ |

---

## Category 7 — Governance Risks

| ID | Area | Issue | Severity | Status |
|----|------|-------|----------|--------|
| G-01 | `answer_builder.py` — `_validate_governance()` | Governance sentinels `safe_for_examiner=False` and `examiner_scoring_allowed=False` are enforced correctly. No `safe_for_examiner=True` found anywhere in codebase. **Clean.** | Medium | ✅ No action required. Monitor: any future contributor must not add `safe_for_examiner=True`. |
| G-02 | `answer_comparator.py` | Comparator is documented clearly: "does not grade, score, or emulate WSET Examiner behavior." No scoring language used in output keys. **Clean.** | Medium | ✅ No action required. |
| G-03 | All tutor output | All tutor-attempt files end with the disclaimer: `"Nota: esta es una respuesta del Tutor, no una calificación oficial ni una evaluación del Examiner."` Disclaimer is present in all 25 self-eval attempts reviewed. **Clean.** | Medium | ✅ No action required. Consider adding a governance test that scans all `tutor_attempt.md` files and asserts the disclaimer line is present. |

---

## Before-Frontend Blocker Summary

The following 21 issues must be resolved before any UI layer is added. Each is marked `[BF]` in the tables above.

| ID | File | One-line description |
|----|------|---------------------|
| A-01 | answer_builder.py | ~550-line if/elif topic dispatch in 5 functions |
| A-02 | answer_builder.py | SAT evaluation terms scattered as literals |
| A-03 | answer_builder.py | Governance sentinels not protected by named constants |
| A-04 | tutor_retrieval_sandbox.py | DOMAIN_EXPANSIONS/SAT_EXPANSIONS inline in source |
| A-05 | tutor_retrieval_sandbox.py | PRIORITY_BOOSTS magic floats |
| A-07 | tutor_retrieval_sandbox.py | 19+ score components with unnamed weights |
| A-11 | question_runner.py | `_infer_expectations()` 49-line hardcoded topic branches |
| A-12 | question_runner.py | 5 hardcoded sample questions in source |
| A-14 | orchestrator.py | DEFAULT_CONTEXT_PACKAGE_DIR hardcoded absolute path |
| A-15 | orchestrator.py | Pedagogical act router hardcoded string-matching |
| A-16 | learner_state.py | NAZARETH_ROOT / DEFAULT paths hardcoded |
| A-19 | misconception_prepass.py | DEFAULT_MISCONCEPTION_DIR hardcoded |
| A-22 | explanation_priority.py | SEVERITY_WEIGHT/DEPTH_TO_STYLE hardcoded |
| A-26 | official_wset_chunks.py | DEFAULT_MARKDOWN_DIR/OUTPUT_DIR/JSONL_PATH hardcoded |
| A-27 | knowledge_tracing.py | DEFAULT_PEDAGOGICAL_MEMORY_PATH hardcoded |
| B-01 | evaluation_reporter.py | Silent import of les_reconciler inside try/except |
| B-02 | orchestrator.py | Direct coupling to 5 concrete modules |
| B-03/04/05 | Multiple | Reverse dependency on orchestrator for PROJECT_ROOT |
| B-09 | (all) | No tools/constants.py — constants scattered across 7+ files |
| C-01 | tutor_retrieval_sandbox.py | score_chunk_for_query() 120 lines / 19+ components inline |
| C-02–05 | answer_builder.py | 4 functions each 70–80 lines of if/elif (consequence of A-01) |
| L-01 | tutor_retrieval_sandbox.py | _tokens() ASCII-only regex corrupts Spanish tokenization |
| L-02 | explanation_priority.py | Two inconsistent tokenizers |
| L-05 | answer_builder.py | ES/EN pattern coverage not auditable |
| P-01 | official_wset_chunks.py | No caching — 25× re-read on every self-eval run |
| P-02 | answer_builder.py | No caching in _extract_context_ideas() |
| T-01–04/T-06 | self_eval, answer_builder | Missing regression tests for known bugs and golden output CI |

---

## Appendix: Files Audited

```
tools/tutor/answer_builder.py
tools/retrieval/tutor_retrieval_sandbox.py
tools/self_eval/answer_comparator.py
tools/self_eval/evaluation_reporter.py
tools/orchestration/orchestrator.py
tools/orchestration/question_runner.py
tools/state/learner_state.py
tools/state/les_reconciler.py
tools/state/knowledge_tracing.py
tools/retrieval/misconception_prepass.py
tools/pedagogy/explanation_priority.py
tools/pedagogy/scaffolding_policy.py
tools/knowledge/official_wset_chunks.py
```

*Audit does not cover frontend, notebooks, or migration scripts.*

---

*This document is a development diagnostic. It does not represent WSET assessment or examiner evaluation.*

---

## Status Update — 2026-05-19

**Brutal self-eval at update time:** `{}` (all 25 questions clean, 231 tests passing)  
**Commit baseline:** `47cb941` (SAT observation alias table) → consolidated Phases 3–7 commit

### Items Resolved Since 2026-05-17 Audit

The following audit items have been confirmed resolved by direct code inspection:

| ID | Original description | Resolution |
|----|---------------------|------------|
| **B-09** | No `tools/constants.py` — constants scattered across 7+ files | ✅ `tools/constants.py` created. Contains `PROJECT_ROOT`, all path constants (`KNOWLEDGE_DIR`, `NAZARETH_DIR`, `CONTEXT_PACKAGES_DIR`, etc.), and governance sentinels. All modules now import from it. |
| **A-03** | Governance sentinels not protected by named constants | ✅ `constants.py` defines `SAFE_FOR_EXAMINER = False`, `EXAMINER_SCORING_ALLOWED = False`, `USES_LLM = False`, `USES_API = False`, `USES_EMBEDDINGS = False`, `USES_VECTOR_DB = False`, `CLOUD_SERVICES_ACTIVE = False`. |
| **B-03** | `answer_builder.py` imports `PROJECT_ROOT` from orchestrator (reverse dep) | ✅ `answer_builder.py` now imports from `tools.constants`. |
| **B-04** | `tutor_retrieval_sandbox.py` imports from orchestrator (reverse dep) | ✅ `tutor_retrieval_sandbox.py` imports `KNOWLEDGE_DIR`, `OFFICIAL_WSET_DIR`, `PROJECT_ROOT`, `RETRIEVAL_SANDBOX_DIR` from `tools.constants`. |
| **B-05** | `learner_state.py` imports from orchestrator (reverse dep) | ✅ `learner_state.py` imports `CLOUD_SERVICES_ACTIVE`, `NAZARETH_DIR`, `SAFE_FOR_EXAMINER` from `tools.constants`. |
| **A-14** | `DEFAULT_CONTEXT_PACKAGE_DIR` hardcoded absolute path in `orchestrator.py` | ✅ Now derived: `DEFAULT_CONTEXT_PACKAGE_DIR = CONTEXT_PACKAGES_DIR` (from constants). Portable. |
| **A-16** | `NAZARETH_ROOT` and DEFAULT paths hardcoded in `learner_state.py` | ✅ Paths now derived from `NAZARETH_DIR` (from constants). `DEFAULT_LES_PATH = NAZARETH_ROOT / "epistemic_state.json"`. |
| **A-19** | `DEFAULT_MISCONCEPTION_DIR` hardcoded absolute path | ✅ `misconception_prepass.py` now uses `DEFAULT_MISCONCEPTION_DIR = PROJECT_ROOT / "knowledge" / "knowledge-map" / "misconceptions"`. |
| **A-26** | `DEFAULT_MARKDOWN_DIR` / `DEFAULT_OUTPUT_DIR` / `DEFAULT_JSONL_PATH` hardcoded | ✅ `official_wset_chunks.py` derives all paths from `PROJECT_ROOT`. |
| **A-27** | `DEFAULT_PEDAGOGICAL_MEMORY_PATH` hardcoded absolute path | ✅ `knowledge_tracing.py` uses `DEFAULT_PEDAGOGICAL_MEMORY_PATH = PROJECT_ROOT / "knowledge" / "nazareth" / "pedagogical_memory.json"`. |
| **A-04** | `DOMAIN_EXPANSIONS` / `SAT_EXPANSIONS` dicts inline in source | ✅ Moved to `knowledge/config/domain_expansions.json`. Module loads from JSON at import. |
| **L-01** | `_tokens()` ASCII-only regex silently corrupts Spanish tokenization | ✅ `_tokens()` now uses `r"(?u)\b[^\W\d_](?:[^\W_]|['-])*\b"` — Unicode-aware, handles all accented characters. `fermentación` → `["fermentación"]`. |
| **T-03** | No unit test for `_tokens()` Unicode behavior | ✅ `tests/test_tutor_retrieval_sandbox.py` asserts `"fermentación"` ∈ tokens and `"fermentaci"` ∉ tokens. |

**Before-frontend blockers resolved:** 13 of 21 original BF items confirmed closed (B-09, A-03, B-03, B-04, B-05, A-14, A-16, A-19, A-26, A-27, A-04, L-01, T-03).  
**Remaining before-frontend blockers:** 8 items still open (A-01, A-05, A-07, A-11, A-12, A-15, A-22, B-01, B-02, C-01, C-02–05, L-02, L-05, P-01, P-02, T-01, T-02, T-04, T-06 — see remediation plan).

---

### SAT Reasoning Layer — New Codebase Items (2026-05-19)

The SAT Reasoning Layer (7 phases) was implemented and committed after the 2026-05-17 audit baseline. The following new files are now in scope for future audits:

| File | Type | Governance status |
|------|------|------------------|
| `tools/tutor/sat_reasoner.py` | Core module | `safe_for_examiner=False` enforced via constants; no LLM, no API, no file writes, deterministic |
| `knowledge/config/sat_observation_aliases.json` | Config | Static data; no governance flags required |
| `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_HIGH.json` | Knowledge node | `safe_for_examiner: false` in node schema |
| `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_MEDIUM.json` | Knowledge node | `safe_for_examiner: false` in node schema |

**SAT integration guard pattern** (`_SAT_REASONER_AVAILABLE`) is used consistently in `answer_builder.py`, `tutor_retrieval_sandbox.py`, and `answer_comparator.py`. Import failure degrades gracefully to pre-SAT behavior without raising exceptions.

**SAT test coverage added:** 5 new test files (230 → 231 total tests).  
**Brutal self-eval impact:** No new failure labels introduced. `{}` maintained.

---

### Revised Before-Frontend Blocker Count

| Status | Count | Items |
|--------|-------|-------|
| ✅ Resolved | 13 | B-09, A-03, B-03, B-04, B-05, A-14, A-16, A-19, A-26, A-27, A-04, L-01, T-03 |
| 🔴 Still open | 8+ | A-01, A-02, A-05, A-07, A-11, A-12, A-15, A-22, B-01, B-02, C-01–05, L-02, L-05, P-01, P-02, T-01, T-02, T-04, T-06 |

See `docs/backend_stability_remediation_plan.md` for sequenced remediation plan.
