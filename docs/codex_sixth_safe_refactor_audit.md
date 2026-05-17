# Codex Sixth Safe Refactor Audit

Date: 2026-05-17

Scope: audit only. No code, tests, file moves, refactors, retrieval behavior, Orchestrator logic, Tutor synthesis behavior, self-eval comparator behavior, official PDFs, raw source files, embeddings, vector DB, APIs, cloud services, frontend, Examiner scoring, or governance flags were changed.

## Recommended Next Future Fix

Extract only the duplicated markdown line-joining behavior in `tools/tutor/answer_builder.py`.

Recommended helper:

```python
def _join_markdown_lines(lines: list[str | None]) -> str:
    return "\n".join(line for line in lines if line is not None)
```

Then replace the two existing render-function returns:

- `_render_misconception_answer()`
- `_render_normal_answer()`

with:

```python
return _join_markdown_lines(lines)
```

This is the safest decomposition boundary because it does not move topic routing, language-specific answer text, causal reasoning text, source notes, headings, disclaimers, retrieval handling, governance checks, or scoring-sensitive wording. It only names an existing repeated rendering primitive.

## Candidate Decomposition Inventory

| Candidate | Approx. lines | Responsibility | Coupling risk | Regression risk | Self-eval sensitivity | Extraction priority | Estimated safety |
|---|---:|---|---|---|---|---|---|
| `_join_markdown_lines()` from render returns | Current return sites at `answer_builder.py:216` and `answer_builder.py:289` | Preserve the exact current `"\n".join(line for line in lines if line is not None)` behavior behind one helper | Very low: pure string assembly, no package access | Very low if helper is byte-for-byte equivalent | Very low: no answer text changes intended | First | Safest |
| Shared title rendering helper | `_render_misconception_answer()` `136-217`; `_render_normal_answer()` `218-290` | Centralize `# Tutor Draft...` / `# Borrador del Tutor...` and Spanish `_display_query()` handling | Low to medium: title text is learner-facing and tested exactly | Low if tests assert exact headings | Low to medium: heading text may affect answer surface but not reasoning | Later | Safe but not first |
| Shared section block helper | `_render_misconception_answer()` `136-217`; `_render_normal_answer()` `218-290` | Centralize `## n. heading`, body, blank-line triplets | Medium: ordering and blank lines are answer-structure contract | Medium: easy to shift blank lines or section numbering | Medium: section structure is visible to self-eval and tests | Later | Moderate |
| Shared footer helper | `_render_misconception_answer()` `136-217`; `_render_normal_answer()` `218-290` | Centralize `source_note`, `support`, blank line, disclaimer | Medium: source/disclaimer placement is now directly tested | Low to medium | Medium: source-authority and disclaimer language are governance-facing | Later | Moderate |
| `_render_misconception_answer()` internal section data builder | `136-217` | Separate data collection from markdown assembly | Medium: touches misconception correction structure and depth compression | Medium | Medium to high: misconception answers affect diagnostic labels | Wait | Not next |
| `_render_normal_answer()` internal section data builder | `218-290` | Separate data collection from markdown assembly | Medium: touches normal answer sequencing and depth compression | Medium | Medium: normal answers affect shallow reasoning and weak exam register | Wait | Not next |
| `_normal_direct_answer()` topic router | `291-363` | Route query patterns to direct-answer strings | High: keyword order and phrasing are behavior | High | High: directly affects answer quality and retrieval-use diagnostics | Wait | Unsafe for next |
| `_cause_effect_line()` structured-chain fallback split | `459-542` | Prefer causal chain nodes, then fallback to keyword causal statements | High: causal chain text is central to `missing_causal_link` and `shallow_reasoning` | High | Very high | Wait | Unsafe for next |
| `_exam_line()` topic router | `902-971` | Produce exam-purpose phrasing by topic and language | High: exact exam framing is self-eval-sensitive and test-sensitive | High | High: affects `weak_exam_register` and brittle phrase history | Wait | Unsafe for next |
| `_mini_practice()` topic router | `972-1041` | Produce topic-specific practice prompts | Medium to high: learner-facing and language-specific | Medium | Medium: less central than exam/cause lines but visible in output | Wait | Not next |
| `_official_idea_from_text()` topic classifier | `854-901` | Map official source text to learner-facing official idea summaries | High: source grounding and official/pedagogical distinction | Medium to high | High: affects retrieval-grounding surface | Wait | Unsafe for next |
| `_idea_from_context_item()` extraction split | `749-786` | Convert retrieved context item shapes into idea text | High: context use, official chunks, misconception nodes | High | High: can alter retrieval-use evidence and source grounding | Wait | Unsafe for next |

## Functions Over 80 Lines

Only two functions currently exceed 80 lines by a simple `def`-to-`def` count:

- `_cause_effect_line()` at approximately `459-542`, 84 lines.
- `_render_misconception_answer()` at approximately `136-217`, 82 lines.

Near-threshold functions also deserve caution:

- `_render_normal_answer()` at approximately `218-290`, 73 lines.
- `_normal_direct_answer()` at approximately `291-363`, 73 lines.
- `_exam_line()` at approximately `902-971`, 70 lines.
- `_mini_practice()` at approximately `972-1041`, 70 lines.

Line count alone should not drive the next change. `_cause_effect_line()` is larger, but it is also one of the most self-eval-sensitive functions in the file. `_render_misconception_answer()` is large mostly because it spells out markdown structure and language branches, but even there, section order and blank lines are user-visible. A tiny markdown join helper gives the system a first decomposition foothold without disturbing either area.

## Repetition Observed

### Markdown Assembly

`_render_misconception_answer()` and `_render_normal_answer()` both build a `lines` list and finish with:

```python
return "\n".join(line for line in lines if line is not None)
```

This repeated primitive is safe to name because it is mechanical and output-preserving.

### Language Branching

The two render functions branch on `language == "en"` and otherwise use Spanish labels. This is currently coupled to:

- `TUTOR_MARKDOWN_LABELS`
- `_display_query()`
- `TUTOR_DISCLAIMERS`
- answer structure tests

Centralizing the branch further is plausible, but not the first move.

### Topic Routing

The following functions duplicate topic triggers such as acidity, tannin, oxidative ageing, mechanical harvest, destemming, SO2, tirage, pressure, Cava/Champagne, drainage, frost, planting density, Tokaji, Cremant, Madeira, and Chile sparkling:

- `_normal_direct_answer()`
- `_cause_effect_line()`
- `_exam_line()`
- `_mini_practice()`
- `_official_idea_from_text()`

These repeated patterns are real technical debt, but they should wait. Changing them risks altering answer content, topic precedence, and self-eval diagnostics.

## Sections Tightly Coupled To Self-Eval Expectations

The following should not be touched in the next implementation:

- `_cause_effect_line()`: causal wording is directly tied to `missing_causal_link` and `shallow_reasoning`.
- `_exam_line()`: exam framing is tied to `weak_exam_register`; prior brittle tests also depended on exam-purpose phrasing.
- `_normal_direct_answer()`: direct learner answer content influences perceived reasoning depth.
- `_official_idea_from_text()` and `_idea_from_context_item()`: source use influences retrieval and grounding diagnostics.
- `_source_note()`, `TUTOR_SOURCE_NOTES`, `TUTOR_DISCLAIMERS`, and `TUTOR_MARKDOWN_LABELS`: recently stabilized; avoid churn.

## Why The Recommended Candidate Is Safest

The `_join_markdown_lines()` extraction is safest because:

- It has no domain logic.
- It has no language logic.
- It has no retrieval logic.
- It has no governance logic.
- It preserves current `None` filtering exactly.
- It touches only two return sites.
- Existing tests already check rendered headings, normal/misconception structure, disclaimer placement, source notes, and `safe_for_examiner=False`.

Expected self-eval impact: none. The rendered answer should be byte-for-byte identical.

## Why Larger Refactors Should Still Wait

Topic routing should wait because it is the most behavior-rich part of the file. Extracting or centralizing topic patterns could change precedence when multiple keywords are present.

Language-branch decomposition should wait because small differences in Spanish/English title handling, section order, and footer placement are learner-facing and already tested as contract.

Source and official-context helpers should wait because they affect whether the answer visibly uses retrieved context and distinguishes official WSET support from pedagogical transcript support.

The causal-chain fallback should wait because the current brutal self-eval is stable, and this function is one of the easiest places to reintroduce `missing_causal_link` or `shallow_reasoning`.

## Exact Future Implementation Strategy

1. Touch only:

   - `tools/tutor/answer_builder.py`
   - `tests/test_tutor_answer_builder.py`

2. Add a tiny private helper near the render functions or near the small formatting helpers:

   ```python
   def _join_markdown_lines(lines: list[str | None]) -> str:
       return "\n".join(line for line in lines if line is not None)
   ```

3. Replace only:

   ```python
   return "\n".join(line for line in lines if line is not None)
   ```

   in `_render_misconception_answer()` and `_render_normal_answer()` with:

   ```python
   return _join_markdown_lines(lines)
   ```

4. Add focused tests:

   - `_join_markdown_lines(["a", None, "", "b"]) == "a\n\nb"` to preserve current `None` filtering and blank-line behavior.
   - Generated normal Spanish answer is unchanged for the fixture package.
   - Generated normal English answer is unchanged for the fixture package.
   - Generated misconception Spanish answer is unchanged for the fixture package.
   - Generated misconception English answer is unchanged for the fixture package.
   - `safe_for_examiner` remains false.

5. Do not change body text, headings, source notes, disclaimers, section order, topic routing, retrieval, Orchestrator logic, self-eval comparator, official files, raw files, or governance constants.

## Rollback Strategy

Rollback is local and mechanical:

- Replace `_join_markdown_lines(lines)` with the original inline expression in both render functions.
- Remove `_join_markdown_lines()`.
- Remove the focused helper tests.

No data migration is involved. If any generated Tutor answer differs, revert immediately because the intended implementation is output-preserving.

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
