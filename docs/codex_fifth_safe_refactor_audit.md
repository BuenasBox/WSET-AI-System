# Codex Fifth Safe Refactor Audit

Date: 2026-05-17

Scope: audit only. No code, tests, file moves, refactors, retrieval behavior, Orchestrator logic, Tutor synthesis behavior, self-eval comparator behavior, official PDFs, raw source files, embeddings, vector DB, APIs, cloud services, frontend, Examiner scoring, or governance flags were changed.

## Recommended Next Fix

Create a tiny Tutor disclaimer/footer registry in `tools/tutor/answer_builder.py`, preserving the current two disclaimer strings exactly.

The current disclaimer text is already centralized as:

- `DISCLAIMER_ES`
- `DISCLAIMER_EN`

The safest next cleanup is therefore not a broad governance-language refactor. It is a compatibility-preserving registry that groups the existing Spanish and English Tutor disclaimers under one local mapping, while keeping the existing constants available.

Recommended future implementation:

- Add `TUTOR_DISCLAIMERS = {"es": DISCLAIMER_ES, "en": DISCLAIMER_EN}` near the existing constants.
- Replace render-site uses of `DISCLAIMER_ES` / `DISCLAIMER_EN` with `TUTOR_DISCLAIMERS[language]` or explicit `TUTOR_DISCLAIMERS["es"]` / `TUTOR_DISCLAIMERS["en"]`.
- Keep `DISCLAIMER_ES` and `DISCLAIMER_EN` for compatibility and existing tests.
- Do not change text.
- Do not alter source notes, governance exception strings, body paragraphs, headings, or topic patterns.

## Why It Is Safe

This is safe because the disclaimer strings are already isolated module constants and are appended in only four render paths:

- misconception answer, English
- misconception answer, Spanish
- normal answer, English
- normal answer, Spanish

The future change can preserve output byte-for-byte and only changes where the render functions read the disclaimer from. Existing tests already assert the Spanish and English disclaimer fragments.

Expected metric impact: none. These footer strings do not drive retrieval, Orchestrator decisions, misconception routing, or comparator logic, as long as text remains exact.

## Issue Inventory

| Issue | Function/location | Exact string or section | Learner-facing | Risk level | Safe to centralize? | Tests required |
|---|---|---|---:|---|---:|---|
| Spanish Tutor disclaimer | `tools/tutor/answer_builder.py`, `DISCLAIMER_ES`; rendered in `_render_misconception_answer` and `_render_normal_answer` | `Nota: esta es una respuesta del Tutor, no una calificación oficial ni una evaluación del Examiner.` | Yes | Low | Yes, recommended | Exact test that `TUTOR_DISCLAIMERS["es"] == DISCLAIMER_ES`; generated Spanish normal and misconception answers still contain the full string; existing disclaimer test. |
| English Tutor disclaimer | `tools/tutor/answer_builder.py`, `DISCLAIMER_EN`; rendered in `_render_misconception_answer` and `_render_normal_answer` | `Note: this is a Tutor response, not an official grade or an Examiner evaluation.` | Yes | Low | Yes, recommended | Exact test that `TUTOR_DISCLAIMERS["en"] == DISCLAIMER_EN`; generated English normal and misconception answers still contain the full string. |
| Spanish normal answer footer render site | `_render_normal_answer`, Spanish branch | Uses `DISCLAIMER_ES` at the end of `lines` | Yes | Low | Yes | Existing Spanish framing/disclaimer tests; exact footer test. |
| English normal answer footer render site | `_render_normal_answer`, English branch | Uses `DISCLAIMER_EN` at the end of `lines` | Yes | Low | Yes | Existing English answer test; exact footer test. |
| Spanish misconception answer footer render site | `_render_misconception_answer`, Spanish branch | Uses `DISCLAIMER_ES` at the end of `lines` | Yes | Low | Yes | Existing `test_answer_includes_tutor_disclaimer`; generated misconception answer exact string test. |
| English misconception answer footer render site | `_render_misconception_answer`, English branch | Uses `DISCLAIMER_EN` at the end of `lines` | Yes | Low | Yes | Add generated English misconception answer exact string test if missing. |
| Governance validation text, safe-for-examiner | `_validate_governance()` | `Unsafe context package: safe_for_examiner must remain false for Tutor output.` | Developer-facing failure text | Low | Wait | Existing test only checks `ValueError`; exact error text test would be needed before centralizing. |
| Governance validation text, Examiner scoring | `_validate_governance()` | `Unsafe context package: Examiner scoring is not allowed for Tutor output.` | Developer-facing failure text | Low | Wait | Add exact error text test only if centralizing later. |
| Source-note official/pedagogical language | `TUTOR_SOURCE_NOTES`, `_source_note()` | Six `Source note:` / `Nota de fuentes:` strings | Yes | Low to medium | Already completed; do not expand now | Existing exact source-note registry test. |
| Source-distinction body fragments | Tests and `_source_note()` outputs | `apoyo pedagógico`, `no autoridad oficial WSET`, `not official WSET authority` | Yes | Medium | Wait | Already covered through source-note tests; changing fragments risks source-authority semantics. |
| Disclaimer fragment tests | `tests/test_tutor_answer_builder.py` | `no una calificación oficial`, `evaluación del Examiner`, `Note: this is a Tutor response` | Test assertions | Low | Strengthen later | Add exact full-string assertions when implementing registry. |

## Why Bigger Refactors Should Wait

Governance exception text should wait because it is developer-facing, not learner-facing, and changing it would require new exact exception-message tests.

Source-note language should wait because it has already been centralized. Expanding or reshaping it now would add churn without improving safety.

Body paragraphs, exam framing, WSET framing, topic patterns, and mini-practice prompts should wait because those strings are answer behavior and can affect self-eval diagnostics.

A broader localization module should wait because importing a new module would increase the blast radius. A local mapping in `answer_builder.py` is enough for this step.

Removing `DISCLAIMER_ES` or `DISCLAIMER_EN` should wait because existing imports/tests may rely on stable constant names in future work. Keep them as compatibility aliases.

## Exact Implementation Plan For A Future Prompt

1. Touch only:

   - `tools/tutor/answer_builder.py`
   - `tests/test_tutor_answer_builder.py`

2. Add a local registry near the existing constants:

   ```python
   TUTOR_DISCLAIMERS = {
       "es": DISCLAIMER_ES,
       "en": DISCLAIMER_EN,
   }
   ```

3. Update render functions only:

   - In English branches, replace `DISCLAIMER_EN` in `lines` with `TUTOR_DISCLAIMERS["en"]`.
   - In Spanish branches, replace `DISCLAIMER_ES` in `lines` with `TUTOR_DISCLAIMERS["es"]`.

4. Keep the existing `DISCLAIMER_ES` and `DISCLAIMER_EN` constants unchanged.

5. Add or update tests in `tests/test_tutor_answer_builder.py`:

   - Assert `TUTOR_DISCLAIMERS["es"] == DISCLAIMER_ES`.
   - Assert `TUTOR_DISCLAIMERS["en"] == DISCLAIMER_EN`.
   - Assert generated normal Spanish answer contains the exact full Spanish disclaimer.
   - Assert generated misconception Spanish answer contains the exact full Spanish disclaimer.
   - Assert generated normal English answer contains the exact full English disclaimer.
   - Assert generated misconception English answer contains the exact full English disclaimer.
   - Assert `safe_for_examiner` remains false in generated Tutor result governance.

6. Do not alter headings, source notes, body paragraphs, `_validate_governance()`, retrieval, Orchestrator, self-eval comparator, official files, or raw files.

## Rollback Strategy

Rollback is local:

- Replace `TUTOR_DISCLAIMERS[...]` render-site lookups with `DISCLAIMER_ES` / `DISCLAIMER_EN`.
- Remove `TUTOR_DISCLAIMERS`.
- Remove the focused registry test additions.

No data migration is involved. If generated answer text changes, revert immediately because the intended implementation is output-preserving.

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
