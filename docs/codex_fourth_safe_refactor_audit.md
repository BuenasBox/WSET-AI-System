# Codex Fourth Safe Refactor Audit

Date: 2026-05-17

Scope: audit only. No code, tests, file moves, refactors, retrieval behavior, Orchestrator logic, Tutor synthesis behavior, self-eval comparator behavior, official PDFs, raw source files, embeddings, vector DB, APIs, cloud services, frontend, Examiner scoring, or governance flags were changed.

## Recommended Next Fix

Centralize only the Tutor source-note strings used by `_source_note()` in `tools/tutor/answer_builder.py`.

This is the safest next cleanup after the heading registry because the source-note logic is already isolated in one function. The future implementation should move the six current return strings into a small local mapping, then keep `_source_note()` behavior and output text exactly the same.

Recommended first slice:

- Keep `DISCLAIMER_ES` and `DISCLAIMER_EN` unchanged; they are already centralized.
- Add a local `TUTOR_SOURCE_NOTES` mapping near existing Tutor text constants.
- Replace only `_source_note()` return literals with mapping lookups.
- Do not change `_source_types()` logic.
- Do not change body paragraphs, exam framing, WSET framing, topic branches, or context summary prefixes.

## Why It Is Safe

`_source_note()` is a small, deterministic function with only three source cases in two languages:

- official reference present
- cognitive correction object present
- default pedagogical/manual transcript support

The future change can preserve every string byte-for-byte and avoid touching answer structure or scoring logic. Existing tests already assert important fragments such as `apoyo pedagógico`, `no autoridad oficial WSET`, `no una calificación oficial`, and `evaluación del Examiner`.

Expected metric impact: none if strings remain exact. The only risk is accidental wording drift in learner-facing source authority language, which can be caught by exact source-note tests plus full self-eval.

## Issue Inventory

| Issue | Function/location | Exact string or section | Learner-facing | Risk level | Safe to centralize? | Tests required |
|---|---|---|---:|---|---:|---|
| Spanish disclaimer constant | `tools/tutor/answer_builder.py`, module constant `DISCLAIMER_ES` | `Nota: esta es una respuesta del Tutor, no una calificación oficial ni una evaluación del Examiner.` | Yes | Low | Already centralized; do not move next | Existing `test_answer_includes_tutor_disclaimer`; full suite. |
| English disclaimer constant | `tools/tutor/answer_builder.py`, module constant `DISCLAIMER_EN` | `Note: this is a Tutor response, not an official grade or an Examiner evaluation.` | Yes | Low | Already centralized; do not move next | Existing English answer test; full suite. |
| Official-source note, English | `_source_note()` | `Source note: from the WSET framework, treat official context as the reference point; use transcript material only as pedagogical support.` | Yes | Low to medium | Yes, recommended | Exact unit test for official context source note in English; official corpus test coverage; full suite. |
| Misconception-source note, English | `_source_note()` | `Source note: the misconception node is a cognitive correction object, and Wine With Jimmy/manual transcript material is pedagogical support, not official WSET authority.` | Yes | Medium | Yes, recommended | Exact unit test for misconception context source note in English; existing misconception answer tests; full suite. |
| Default pedagogical-source note, English | `_source_note()` | `Source note: Wine With Jimmy/manual transcript material is pedagogical support, not official WSET authority.` | Yes | Medium | Yes, recommended | Exact unit test for normal English source note; existing English answer test; full suite. |
| Official-source note, Spanish | `_source_note()` | `Nota de fuentes: desde el marco WSET, el material oficial es la referencia; el material de transcripción sirve solo como apoyo pedagógico.` | Yes | Low to medium | Yes, recommended | Exact unit test for official context source note in Spanish; official corpus tests; full suite. |
| Misconception-source note, Spanish | `_source_note()` | `Nota de fuentes: el misconception_node es un objeto de corrección cognitiva; el material de Wine With Jimmy o transcripciones manuales es apoyo pedagógico, no autoridad oficial WSET.` | Yes | Medium | Yes, recommended | Exact unit test for misconception context source note in Spanish; existing `test_source_distinction_appears`; full suite. |
| Default pedagogical-source note, Spanish | `_source_note()` | `Nota de fuentes: el material de Wine With Jimmy o transcripciones manuales es apoyo pedagógico, no autoridad oficial WSET.` | Yes | Medium | Yes, recommended | Exact unit test for normal Spanish source note; existing retrieved-context/source distinction tests; full suite. |
| Context support prefix, Spanish | `_support_summary()` | `Ideas usadas del contexto: ` | Yes | Low to medium | Safe later, not next | Exact prefix tests; answer-builder tests. |
| Context support prefix, English | `_support_summary()` | `Ideas used from context: ` | Yes | Low to medium | Safe later, not next | Exact prefix tests; answer-builder tests. |
| Empty-context summary, Spanish | `_support_summary()` | `Contexto usado: misconception_node y paquete local del Tutor.` | Yes | Medium | Wait | Needs empty-context answer test; may affect fallback explanations. |
| Empty-context summary, English | `_support_summary()` | `Context used: misconception node and local Tutor package.` | Yes | Medium | Wait | Needs empty-context answer test; may affect fallback explanations. |
| Governance validation error, safe-for-examiner | `_validate_governance()` | `Unsafe context package: safe_for_examiner must remain false for Tutor output.` | Developer-facing failure text | Low | Wait | Existing exception test checks raise, not text. Centralizing failure text is less valuable now. |
| Governance validation error, Examiner scoring | `_validate_governance()` | `Unsafe context package: Examiner scoring is not allowed for Tutor output.` | Developer-facing failure text | Low | Wait | Add exact error tests only if centralizing later. |
| Source labels from context extraction | `_context_label()` | `official_wset`, `misconception_node`, `apoyo pedagógico` | Partly learner-facing through support summary | Medium | Wait | Source-label exact tests and official-context tests. These are data labels and source semantics, not just notes. |

## Why Bigger Refactors Should Wait

Disclaimers should not move yet because they are already module-level constants and tested. Moving them into a broader registry would add churn without much benefit.

Context support prefixes should wait because `_support_summary()` combines source labels and extracted ideas. It is close to answer evidence presentation rather than a pure static footer.

Source labels such as `official_wset`, `misconception_node`, and `apoyo pedagógico` should wait because they are mixed with context extraction and source classification. Changing them can alter visible support summaries and tests.

Governance exception text should wait because it is developer-facing and less urgent than learner-facing source notes.

Topic prose, exam framing, WSET framing, and mini-practice prompts should remain untouched. Those strings are answer behavior and can affect self-eval diagnostics.

## Exact Implementation Plan For A Future Prompt

1. Touch only:

   - `tools/tutor/answer_builder.py`
   - `tests/test_tutor_answer_builder.py`

2. Add a local mapping near existing constants:

   ```python
   TUTOR_SOURCE_NOTES = {
       "en": {
           "official_reference": "Source note: from the WSET framework, treat official context as the reference point; use transcript material only as pedagogical support.",
           "cognitive_correction": "Source note: the misconception node is a cognitive correction object, and Wine With Jimmy/manual transcript material is pedagogical support, not official WSET authority.",
           "pedagogical_support": "Source note: Wine With Jimmy/manual transcript material is pedagogical support, not official WSET authority.",
       },
       "es": {
           "official_reference": "Nota de fuentes: desde el marco WSET, el material oficial es la referencia; el material de transcripción sirve solo como apoyo pedagógico.",
           "cognitive_correction": "Nota de fuentes: el misconception_node es un objeto de corrección cognitiva; el material de Wine With Jimmy o transcripciones manuales es apoyo pedagógico, no autoridad oficial WSET.",
           "pedagogical_support": "Nota de fuentes: el material de Wine With Jimmy o transcripciones manuales es apoyo pedagógico, no autoridad oficial WSET.",
       },
   }
   ```

3. Change `_source_note()` only to select from that mapping:

   - `official_reference` when `"official reference" in source_types`
   - `cognitive_correction` when `"cognitive correction object" in source_types`
   - `pedagogical_support` otherwise

4. Preserve branch priority exactly: official reference still wins before cognitive correction, matching current behavior.

5. Add focused tests that render or directly verify all six note outputs exactly. Prefer generated Tutor answers where practical, but a direct `_source_note()` test is acceptable if kept local and exact.

6. Confirm existing disclaimer tests still pass. Do not alter `DISCLAIMER_ES` or `DISCLAIMER_EN`.

7. Do not alter `_source_types()`, `_support_summary()`, `_context_label()`, body paragraphs, headings, exam lines, Orchestrator logic, retrieval, or self-eval comparator.

## Rollback Strategy

Rollback is local:

- Restore the six inline return strings in `_source_note()`.
- Remove `TUTOR_SOURCE_NOTES`.
- Remove any focused source-note registry test.

No data migration is involved. If self-eval changes, treat it as a regression because the intended implementation preserves output text exactly.

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
