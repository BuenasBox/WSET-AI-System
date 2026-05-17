# Codex Second Safe Refactor Audit

Date: 2026-05-17

Scope: audit only. No code, tests, architecture, retrieval behavior, Orchestrator logic, Tutor synthesis, self-eval behavior, official PDFs, raw source files, embeddings, vector DB, APIs, cloud services, frontend, Examiner scoring, or governance flags were changed.

## Recommended Next Fix

Create a central diagnostic label mapping for self-eval labels, limited to `tools/self_eval/answer_comparator.py` and focused tests.

The current comparator has one ordered tuple, `COGNITIVE_ERROR_LABELS`, which controls canonical label order. The same label strings then appear across comparator logic, reporter aggregation, LES feedback, tests, and benchmark interpretation. A small local registry can make this safer without changing any diagnostic decisions.

Recommended implementation shape for a future prompt:

- Add an immutable local mapping in `tools/self_eval/answer_comparator.py`, for example `COGNITIVE_ERROR_LABEL_REGISTRY`.
- Keep the exact current labels and exact current order.
- Derive `COGNITIVE_ERROR_LABELS = tuple(COGNITIVE_ERROR_LABEL_REGISTRY)` so existing behavior and imports remain valid.
- Do not change label strings.
- Do not change comparator conditions.
- Do not change reporter behavior.
- Add/adjust tests only to prove the labels are unchanged and ordered as before.

This is the next safest cleanup because it is mostly structural, has a clear rollback, and does not touch answer generation or retrieval scoring.

## Candidate Assessment

| Candidate | Risk level | Benefit | Files affected | Likelihood of changing self-eval metrics | Tests needed | Rollback strategy |
|---|---:|---|---|---:|---|---|
| Central diagnostic label mapping | Low | Reduces label-string drift, gives self-eval diagnostics one obvious source of truth, and prepares safer reporter/LES documentation later. | Future implementation should touch only `tools/self_eval/answer_comparator.py` and `tests/test_self_eval_loop.py`. Possibly no reporter change in first pass. | Very low if label strings, order, and conditions are unchanged. | Unit test that `COGNITIVE_ERROR_LABELS` equals the current ordered tuple; existing comparator label tests; full suite; brutal self-eval. | Revert the mapping and restore the literal tuple. No data migration or artifact cleanup required. |
| Governance constants registry | Low to medium | Could reduce repeated governance flag dictionaries and make unsafe flags easier to audit. | Would likely span `answer_builder.py`, retrieval, orchestrator, self-eval reporter/runner, tests. | Low if values are unchanged, but broad import surface increases accidental risk. | Governance tests across orchestrator, Tutor, retrieval, self-eval, LES reconciler; full suite; artifact spot-checks. | Revert registry imports and restore local literals. Because many files are touched, rollback is noisier. |
| Constants/config extraction | Medium | Improves readability around thresholds, strictness levels, retrieval `top_k`, confidence values, score weights, and style options. | `answer_comparator.py`, `misconception_prepass.py`, `tutor_retrieval_sandbox.py`, maybe `answer_builder.py`. | Medium. Even a copied numeric value can affect metrics if moved incorrectly or imported too early. | Exact unit tests for threshold behavior, score breakdown snapshots, misconception confidence tests, full suite, brutal self-eval. | Revert extracted constants and restore inline values. Needs careful diff review. |
| Central localization registry | Medium | Removes duplicated English/Spanish headings and disclaimers; makes phrase acceptance tests cleaner. | Primarily `tools/tutor/answer_builder.py` and `tests/test_tutor_answer_builder.py`. | Medium. Comparator and tests are sensitive to output wording. The recent brittle phrase failure shows this area is visible. | Snapshot-style tests for Spanish/English answers, governance disclaimer tests, comparator self-eval smoke tests. | Restore inline strings. Rollback is straightforward but output diffs may be large. |
| Function decomposition in `answer_builder.py` | Medium to high | Makes large C901 functions easier to reason about, especially direct answers, exam lines, mini practice, and official source notes. | `tools/tutor/answer_builder.py`, many answer-builder tests. | Medium to high. Reordering condition branches or changing fallback paths can alter generated answers and self-eval labels. | Broad answer snapshots across common topics, source distinction tests, misconception tests, full suite, brutal self-eval. | Revert decomposition. Harder if many helper functions are introduced at once. |
| Retrieval pattern registry | High | Could unify `SAT_EXPANSIONS`, `DOMAIN_EXPANSIONS`, topic triggers, and reasoning terms. | `tools/retrieval/tutor_retrieval_sandbox.py`, retrieval tests, possible official corpus tests. | High. Retrieval ranking and context selection are benchmark-sensitive. | Retrieval ranking snapshots, official/pedagogical source-diversity tests, score breakdown tests, brutal self-eval. | Revert registry and restore inline pattern dictionaries. Requires benchmark artifact comparison. |
| Externalizing hardcoded topic patterns from `answer_builder.py` | High | Eventually reduces duplicated topic branches for Oloroso/Amontillado, tirage, Cava/Champagne, Tokaji, Crémant, Madeira, Chile sparkling, soil drainage, frost, planting density, etc. | `tools/tutor/answer_builder.py`, likely new local data file or module, answer-builder tests. | High. These patterns define actual answer text, comparator keyword hits, and self-eval results. | Per-topic answer snapshots, Spanish/English route tests, source-note tests, mini-practice tests, full suite, brutal self-eval. | Restore inline branches. Avoid until answer snapshots are stronger. |

## Why This Should Come Next

The diagnostic label registry is a cleanup around identifiers, not behavior. The comparator already centralizes label ordering in `COGNITIVE_ERROR_LABELS`; the future change would make that centralization more explicit and harder to drift from by deriving the tuple from a registry.

It also improves the next layer of engineering readiness. Self-eval labels are used as backend signals for benchmark interpretation, LES feedback, reporter summaries, and regression tracking. A small registry gives those labels a maintainable home before any later work tries to add categories, descriptions, or UI-facing names.

Most importantly, it avoids touching the two riskiest active surfaces: retrieval ranking and Tutor answer wording.

## Why Other Fixes Should Wait

Central localization should wait because Tutor output text is behavior in this system. Even harmless wording movement can affect tests, comparator detections, and brutal self-eval labels.

Externalizing topic patterns from `answer_builder.py` should wait because the current branches are not just data; they encode answer selection, causal wording, Spanish/English phrasing, and fallback order.

Constants/config extraction should wait unless it is split into very small local passes. Retrieval weights, misconception thresholds, and strictness thresholds are active calibration, not inert style debt.

Function decomposition in `answer_builder.py` should wait until there are stronger answer snapshots. Large helper extraction is easy to do mechanically, but one branch-order slip would change behavior.

Retrieval pattern registry should wait because the retrieval sandbox is benchmark-sensitive. After Unicode tokenization, the next retrieval cleanup should not immediately touch expansion dictionaries or scoring.

Governance constants registry is valuable, but it spans many modules. It is safe conceptually, yet broader than the diagnostic-label registry and therefore not the best next surgical fix.

## Exact Implementation Plan For A Future Prompt

1. In `tools/self_eval/answer_comparator.py`, replace the literal tuple definition with a local registry whose insertion order exactly matches the current tuple.

   Suggested structure:

   ```python
   COGNITIVE_ERROR_LABEL_REGISTRY = {
       "missing_causal_link": {"category": "reasoning"},
       "vague_claim": {"category": "reasoning"},
       "unsupported_conclusion": {"category": "reasoning"},
       "missing_exam_language": {"category": "exam_register"},
       "incomplete_balance_justification": {"category": "sat"},
       "weak_sat_commitment": {"category": "sat"},
       "misconception_unresolved": {"category": "misconception"},
       "missing_counterexample": {"category": "misconception"},
       "retrieval_gap": {"category": "retrieval"},
       "weak_context_support": {"category": "retrieval"},
       "shallow_retrieval": {"category": "retrieval"},
       "shallow_reasoning": {"category": "reasoning"},
       "misconception_reinforcement_risk": {"category": "misconception"},
       "weak_exam_register": {"category": "exam_register"},
   }

   COGNITIVE_ERROR_LABELS = tuple(COGNITIVE_ERROR_LABEL_REGISTRY)
   ```

2. Do not use the metadata anywhere in behavior in the first pass. The first pass is only to centralize labels while preserving comparator output.

3. Add a focused test in `tests/test_self_eval_loop.py` that asserts `COGNITIVE_ERROR_LABELS` equals the exact current ordered tuple.

4. Keep all existing comparator tests unchanged unless import updates are needed.

5. Do not touch `evaluation_reporter.py` in the first pass. Reporter adoption can be a separate refactor after the registry is stable.

6. Run the full benchmark commands below.

## Tests Needed

Minimum:

- `python -m unittest tests.test_self_eval_loop -v`
- `python -m unittest discover -s tests -v`

Behavior checks:

- Existing tests for `missing_causal_link`, `retrieval_gap`, `shallow_reasoning`, SAT weakness labels, misconception labels, and strictness behavior must pass unchanged.
- New test should prove label order and spelling are identical to the pre-refactor tuple.

Benchmark:

- Brutal self-eval should show no diagnostic changes caused by this registry-only refactor.

## Benchmark Commands

Run after implementation:

```bash
python -m unittest discover -s tests -v
python -m tools.youtube_transcription.main self-eval --limit 25 --question-type all --strictness brutal
```

Expected:

- Full suite remains green.
- Brutal self-eval remains stable.
- No reappearance of `missing_causal_link`, `unsupported_conclusion`, `retrieval_gap`, or `weak_exam_register`.
- Governance remains `safe_for_examiner=false`, `examiner_scoring_allowed=false`, and no embeddings/vector DB/APIs/cloud/frontend become active.
