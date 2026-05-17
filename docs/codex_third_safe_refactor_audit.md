# Codex Third Safe Refactor Audit

Date: 2026-05-17

Scope: audit only. No code, tests, files outside this report, retrieval behavior, Orchestrator logic, Tutor synthesis, self-eval behavior, official PDFs, raw source files, embeddings, vector DB, APIs, cloud services, frontend, Examiner scoring, or governance flags were changed.

## Recommended Next Fix

Create a narrow Tutor structural localization registry for stable Markdown headings in `tools/tutor/answer_builder.py`.

This should be the first localization cleanup, not a broad Spanish/WSET phrase registry. The safest first slice is to centralize only repeated structural labels such as answer titles and section headings:

- `# Tutor Draft: ...`
- `# Borrador del Tutor: ...`
- `## 1. Short Direct Answer`
- `## 1. Respuesta directa`
- `## 2. WSET Framing`
- `## 2. Marco WSET`
- `## 4. Exam Formulation`
- `## 4. Formulación de examen`
- `## 5. Mini Practice`
- `## 5. Mini práctica`

Do not centralize answer body prose, topic-specific exam wording, source notes, Orchestrator instructions, retrieval report labels, or self-eval summary labels in the first implementation.

## Why It Is Safe

The heading strings are structural and already tested as visible output. They do not decide retrieval, misconception routing, self-eval scoring, or Tutor topic selection.

The future implementation can preserve every string byte-for-byte and only replace inline literals with lookups from a local mapping in the same file. This gives a first localization registry without changing the generated Markdown.

Expected metric impact: none if strings are exact. The only residual risk is a typo or missing key that changes output text, which is easy to catch with existing `test_tutor_answer_builder.py` assertions and the full suite.

## Issue Inventory

| Issue | File | Function or section | Current hardcoded text | Risk level | Learner-facing | Safe to centralize? | Tests needed |
|---|---|---|---|---|---:|---:|---|
| Normal answer title labels | `tools/tutor/answer_builder.py` | `_render_normal_answer` | `# Tutor Draft: {query}`, `# Borrador del Tutor: ...` | Low | Yes | Yes, in first pass | Existing answer-builder tests plus exact output smoke test for English/Spanish normal answers. |
| Misconception answer title labels | `tools/tutor/answer_builder.py` | `_render_misconception_answer` | `# Tutor Draft: {query}`, `# Borrador del Tutor: ...` | Low | Yes | Yes, in first pass | Misconception answer tests for title and sections. |
| Normal answer section headings | `tools/tutor/answer_builder.py` | `_render_normal_answer` | `Short Direct Answer`, `Respuesta directa`, `WSET Framing`, `Marco WSET`, `Cause/Effect Explanation`, `Explicación causa → efecto`, `Exam Formulation`, `Formulación de examen`, `Mini Practice`, `Mini práctica` | Low | Yes | Yes, recommended first fix | Existing tests already assert several headings. Add one focused registry integrity test if implemented. |
| Misconception answer section headings | `tools/tutor/answer_builder.py` | `_render_misconception_answer` | `Direct Correction`, `Corrección directa`, `Why The Misconception Is Tempting`, `Por qué esa idea confunde`, `Correct WSET Framing`, `Marco WSET correcto`, `How To Write It For Marks`, `Cómo escribirlo para puntos` | Low to medium | Yes | Yes, but same first pass only if exact and local | Existing misconception answer tests plus exact heading coverage. |
| Tutor disclaimers | `tools/tutor/answer_builder.py` | module constants and render functions | `Nota: esta es una respuesta del Tutor...`, `Note: this is a Tutor response...` | Low | Yes | Already centralized; do not move yet | Existing disclaimer tests. |
| Context support prefixes | `tools/tutor/answer_builder.py` | `_support_summary` | `Ideas usadas del contexto:`, `Ideas used from context:` | Low to medium | Yes | Safe later, but wait until heading registry is stable | Existing retrieved-context tests; add exact prefix test. |
| Source notes | `tools/tutor/answer_builder.py` | `_source_note` | `Source note: ...`, `Nota de fuentes: ...`, `not official WSET authority`, `no autoridad oficial WSET` | Medium | Yes | Wait | Source distinction tests, official corpus tests, brutal self-eval. These phrases encode governance/source handling, not just labels. |
| Exam framing phrases | `tools/tutor/answer_builder.py` | `_exam_line`, tests | `For exam purposes`, `Para efectos del examen`, `Exam Formulation`, `Formulación de examen` | Medium to high | Yes | Wait, except structural headings | Answer-builder tests, comparator sensitivity checks, brutal self-eval. Body phrases can affect `missing_exam_language` and `weak_exam_register`. |
| WSET framing prefixes | `tools/tutor/answer_builder.py` | `_wset_framing_line`, fallbacks | `From the WSET perspective`, `Desde el marco WSET`, `Como apoyo pedagógico`, `Como formulación de Tutor` | Medium | Yes | Wait | Official corpus tests assert `Desde el marco WSET`; self-eval comparator may benefit from these strings. |
| Topic-specific learner prose | `tools/tutor/answer_builder.py` | `_normal_direct_answer`, `_cause_effect_line`, `_official_idea_from_text`, `_exam_line`, `_mini_practice`, `_spanish_paraphrase` | Many topic branches for Sherry ageing, tirage, Cava/Champagne, Tokaji, Crémant, Madeira, Chile sparkling, soil drainage, frost, planting density, tannin/acidity | High | Yes | No, not next | Per-topic answer snapshots, official source tests, brutal self-eval. These are answer behavior. |
| Orchestrator source-handling instructions | `tools/orchestrator/orchestrator.py` | `build_context_package`, `_language_instruction`, `_success_criteria` | `Use official WSET support first...`, `Preserve official WSET terms...`, `Keep Examiner scoring disabled...` | Medium | Indirectly | Wait | Orchestrator tests assert phrases; source-handling semantics are governance-adjacent. |
| Self-eval summary labels | `tools/self_eval/evaluation_reporter.py` | `_render_summary` | `Strictness`, `Questions attempted`, `Most common failure labels`, `Governance...` | Low to medium | Developer-facing | Wait | Reporter tests plus benchmark artifact diff. These are diagnostic output labels, not Tutor localization. |
| Retrieval report labels | `tools/retrieval/tutor_retrieval_sandbox.py` | `_render_markdown`, CLI prints | `Query Analysis`, `Retrieved Chunks`, `Governance filter applied`, `No tutoring answer was generated...` | Low to medium | Developer-facing | Wait | Retrieval report tests and artifact snapshots. Not part of learner-facing Tutor localization. |
| Comparator diagnostic metadata | `tools/self_eval/answer_comparator.py` | `COGNITIVE_ERROR_LABEL_METADATA` | `label_es`, `description_es`, `severity_hint`, `learner_facing` | Low | Potentially learner-facing later | Already completed; do not expand in this pass | Existing metadata integrity tests. |

## Why Other Fixes Should Wait

Source notes should wait because they carry governance and source-authority semantics. Centralizing them is useful, but a wording slip could weaken the official-vs-pedagogical distinction.

Exam framing phrases should wait because body text such as `For exam purposes` and `Para efectos del examen` can affect answer-builder tests and self-eval checks for exam register. The recent brittle assertion fix showed this surface is sensitive.

WSET framing prefixes should wait because `Desde el marco WSET` is asserted in official corpus tests and helps signal official support. It is more behavior-adjacent than headings.

Topic-specific prose should wait because those branches define actual Tutor answers. Externalizing them is closer to answer redesign than safe localization cleanup.

Orchestrator source-handling instructions should wait because they are contract text for the context package and are tested directly.

Self-eval and retrieval report labels should wait because they are developer-facing diagnostics, not the highest-value learner-facing localization cleanup.

## Exact Implementation Plan For A Future Prompt

1. Touch only `tools/tutor/answer_builder.py` and focused tests.

2. Add a local mapping near existing constants:

   ```python
   TUTOR_MARKDOWN_LABELS = {
       "en": {
           "title": "Tutor Draft",
           "normal_direct": "Short Direct Answer",
           "normal_framing": "WSET Framing",
           "cause_effect": "Cause/Effect Explanation",
           "normal_exam": "Exam Formulation",
           "mini_practice": "Mini Practice",
           "misconception_direct": "Direct Correction",
           "misconception_confusion": "Why The Misconception Is Tempting",
           "misconception_framing": "Correct WSET Framing",
           "misconception_exam": "How To Write It For Marks",
       },
       "es": {
           "title": "Borrador del Tutor",
           "normal_direct": "Respuesta directa",
           "normal_framing": "Marco WSET",
           "cause_effect": "Explicación causa → efecto",
           "normal_exam": "Formulación de examen",
           "mini_practice": "Mini práctica",
           "misconception_direct": "Corrección directa",
           "misconception_confusion": "Por qué esa idea confunde",
           "misconception_framing": "Marco WSET correcto",
           "misconception_exam": "Cómo escribirlo para puntos",
       },
   }
   ```

3. Replace only the heading literals in `_render_normal_answer` and `_render_misconception_answer` with lookups from this mapping.

4. Preserve the numeric section prefixes exactly where they are rendered, for example:

   ```python
   f"## 1. {labels['normal_direct']}"
   ```

5. Do not change disclaimers, source notes, body prose, exam lines, WSET framing lines, mini-practice prompts, Orchestrator instructions, retrieval report text, self-eval summary text, or diagnostic metadata.

6. Add a focused test in `tests/test_tutor_answer_builder.py` that checks required keys exist for `en` and `es` and that current expected headings still appear in generated normal and misconception answers.

7. Run the benchmark commands below.

## Rollback Strategy

Rollback is local and simple: restore inline heading strings in `_render_normal_answer` and `_render_misconception_answer`, then remove the heading registry and its focused test.

No data migration is involved. No generated artifacts should be required to roll back.

If self-eval changes unexpectedly, inspect whether any heading string changed. Since the intended implementation only changes lookup mechanics, any metric movement should be treated as a regression and reverted.

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
