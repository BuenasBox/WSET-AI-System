# Codex First Safe Refactor Audit

Date: 2026-05-17

Scope: surgical engineering readiness audit only. No behavior changes were made. No embeddings, vector DB, APIs, cloud services, Examiner scoring, frontend work, official PDF edits, raw source edits, or governance flag changes were performed.

## Recommended First Fix

Unicode-safe tokenization in `tools/retrieval/tutor_retrieval_sandbox.py`, limited to the local `_tokens()` helper.

This is the smallest safe first refactor because `_tokens()` is already the single tokenization choke point for retrieval query tokens, chunk tokens, expansion trigger matching, knowledge-node token matching, and section/topic token matching inside the retrieval sandbox. The current implementation uses an ASCII-only pattern:

```python
re.findall(r"\b[a-zA-Z][a-zA-Z0-9'-]*\b", text.lower())
```

That pattern can split or drop accented Spanish words such as `biológica`, `fermentación`, `azúcar`, and `oxidación`. The system partially compensates today through manual Spanish trigger phrases and substring phrase matching, but token-level retrieval and knowledge graph matching remain less reliable for accented input.

## Why This Is Safe

The recommended change is narrow: replace only the retrieval sandbox `_tokens()` regex with a Unicode-aware helper that preserves the current semantics for English tokens, apostrophes, and hyphens.

It is safer than centralizing constants or deduplicating topic patterns because it does not move ownership boundaries, change scoring weights, alter governance rules, or rewrite the Tutor synthesis branches. It improves lexical correctness while keeping all scoring formulas, expansions, filters, and output schemas intact.

Expected behavior impact is bounded but real: accented Spanish query tokens may begin matching accented corpus, dictionary, or knowledge-node text at token level. That can slightly alter retrieval rankings and therefore self-eval metrics, especially for Spanish questions around biological ageing, fermentation, sugar, acidity, sparkling wine, and oxidation. This is desirable, but it must be benchmarked.

## Candidate Findings

| Candidate | File | Function(s) | Current behavior | Risk | Expected benefit | Tests needed | Could alter self-eval metrics? |
|---|---|---|---|---|---|---|---|
| Unicode tokenization | `tools/retrieval/tutor_retrieval_sandbox.py` | `_tokens`; callers include `classify_query`, `detect_knowledge_nodes`, `expand_query_terms`, `score_chunk_for_query`, `_matched_chunk_terms`, `_source_concept_phrase_score`, `_section_topic_match_score` | ASCII-only token regex drops or splits accented letters while preserving English apostrophes/hyphens. Phrase matching still catches some Spanish phrases, and manual Spanish expansions compensate for known cases. | Low to medium. Single helper change, but retrieval ranking can shift because lexical overlap and knowledge-node token hits may improve. | Correct token handling for Spanish WSET terms without adding more manual trigger variants. Reduces pressure to patch behavior with duplicated topic keywords. | Unit tests for token output and retrieval/classification invariants; benchmark self-eval before/after. | Yes, possibly. Retrieval scores/ranks may change for accented Spanish queries. |
| Unicode tokenization in misconception pre-pass | `tools/orchestrator/misconception_prepass.py` | `_tokens`, `_is_explanatory_query` | `_tokens` uses `[a-z0-9]+`; `_is_explanatory_query` uses `[a-z]+`. This can split accented Spanish words, though current misconception logic is mostly English/framing-token driven. | Medium. Misconception routing is sensitive: changing token overlap can affect intervention selection and confidence thresholds. | More robust Spanish misconception detection later. | Dedicated misconception false-positive/false-negative tests, especially explanatory-query guard cases. | Yes. Could change `misconception_unresolved`, intervention routing, and downstream answer shape. |
| Centralized constants | `tools/retrieval/tutor_retrieval_sandbox.py`, `tools/orchestrator/misconception_prepass.py`, `tools/tutor/answer_builder.py`, `tools/self_eval/answer_comparator.py`, `tools/self_eval/question_runner.py` | Module constants such as `STOPWORDS`, `PRIORITY_BOOSTS`, `KEY_TERMS`, thresholds, strictness values, `top_k=5` | Constants are local and duplicated in places. Some values encode deliberate benchmark tuning and governance behavior. | Medium to high. Moving constants can accidentally change imports, ownership, test setup, or module initialization. | Better maintainability after behavior is pinned. | Golden output comparison, governance regression tests, import-cycle checks. | Potentially, if any default or threshold changes by mistake. |
| Localization labels | `tools/tutor/answer_builder.py` | `_render_misconception_answer`, `_render_normal_answer`, `_normal_direct_answer`, `_display_query`, `_cause_effect_line`, `_source_note`, `_wset_framing_line`, `_exam_line`, `_mini_practice` | English and Spanish strings are hardcoded inline. Some Spanish answers intentionally retain WSET English terms such as `quality assessment`, `balance`, and `length`. | Medium. Text edits can change comparator keyword hits and self-eval labels even when pedagogically harmless. | Cleaner localization and easier future copy review. | Snapshot tests for representative Tutor answers and comparator keyword preservation. | Yes. Output wording directly affects comparator labels. |
| Magic numbers | `tools/retrieval/tutor_retrieval_sandbox.py`, `tools/orchestrator/misconception_prepass.py`, `tools/self_eval/answer_comparator.py`, `tools/tutor/answer_builder.py` | Retrieval scoring weights, misconception confidence thresholds, strictness thresholds, support-depth thresholds | Numeric weights are embedded near their logic. Many are benchmark-tuned. | High for first fix. Renaming constants is safe only if purely mechanical, but this area invites accidental retuning. | Readability and safer future calibration. | Exact score breakdown tests and benchmark diff review. | Yes, strongly, if any value changes. |
| Duplicated topic patterns | `tools/retrieval/tutor_retrieval_sandbox.py`, `tools/tutor/answer_builder.py`, `tools/self_eval/question_runner.py`, `tools/self_eval/answer_comparator.py` | `DOMAIN_EXPANSIONS`, direct-answer branches, inferred expectations, comparator keyword checks | Topic strings for `crianza biológica`, `fermentación`, `azúcar`, `espumoso`, `oxidación`, etc. appear across retrieval, synthesis, and self-eval. | High for first fix. These duplicates are serving different stages: retrieval expansion, answer rendering, question expectations, and diagnostic comparison. | Eventually reduces drift and missing Spanish variants. | End-to-end self-eval snapshots and per-topic retrieval/answer tests. | Yes. This is behavior-defining logic. |

## Why Other Fixes Should Wait

Centralized constants should wait because constants in this codebase are not only style debt; many are active control surfaces for retrieval ranking, misconception confidence, strictness behavior, answer synthesis, and governance reporting.

Localization labels should wait because the comparator depends on exact output terms. Moving strings could look harmless while changing `missing_exam_language`, `shallow_reasoning`, or keyword detection.

Magic numbers should wait because the latest brutal self-eval is nearly clean. Any cleanup near scoring weights or thresholds could obscure whether a metric change came from refactor mechanics or actual calibration.

Duplicated topic patterns should wait because the duplication currently acts as stage-specific control: retrieval needs expansion phrases, Tutor synthesis needs answer branches, and self-eval needs expected keywords. Consolidating too early risks redesigning behavior.

Misconception tokenization should wait until retrieval tokenization is benchmarked. The misconception pre-pass has confidence thresholds and explanatory-query suppression that are more routing-sensitive than retrieval token cleanup.

## Exact Implementation Plan For Next Prompt

Change only:

- `tools/retrieval/tutor_retrieval_sandbox.py`
- Function: `_tokens(text: str) -> list[str]`

Preferred implementation:

```python
def _tokens(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"(?u)\b[^\W\d_](?:[^\W_]|['-])*\b", text.lower())
        if token not in STOPWORDS and len(token) > 1
    ]
```

Rationale:

- Use Python `re` with explicit Unicode mode `(?u)`. In Python 3 this is the default for `str`, but the inline flag makes the intent visible.
- `[^\W\d_]` means “Unicode letter, not digit, not underscore” for the first character. This preserves the old behavior that tokens must start with a letter.
- `(?:[^\W_]|['-])*` preserves existing apostrophe and hyphen behavior for English and WSET terms, allows Unicode letters and digits after the first character, and avoids newly accepting underscores as word-internal token characters.
- Existing English tokens such as `quality`, `tannin`, `cool`, `climate`, `don't`, and `semi-sparkling` should remain intact.
- Existing stopword filtering and `len(token) > 1` should remain unchanged.

Do not change `_contains_phrase()` in the first implementation. It already uses Unicode-aware `\w` boundaries in Python 3 and is less clearly broken than `_tokens()`.

Do not introduce a shared tokenizer module in the first implementation. That would enlarge the refactor beyond the safest single-function change.

## Proposed Tests Only

Add tests in a later implementation prompt; do not create them during this audit.

Suggested unit tests:

- `_tokens("crianza biológica")` includes `crianza` and `biológica`.
- `_tokens("fermentación y oxidación")` includes `fermentación` and `oxidación`, and excludes Spanish stopwords only if they are explicitly in the local `STOPWORDS`.
- `_tokens("azúcar residual y acidez")` includes `azúcar` and `acidez`.
- `_tokens("tanino espumoso")` includes `tanino` and `espumoso`.
- `_tokens("cool-climate acidity don't tannin")` preserves `cool-climate`, `acidity`, `don't`, and `tannin` or otherwise preserves the current documented apostrophe/hyphen behavior.
- `classify_query("Explica la crianza biológica y la oxidación en Jerez", [], [])["query_tokens"]` includes `biológica` and `oxidación`.
- A retrieval sandbox smoke test for accented and unaccented variants verifies no exception and stable governance flags:
  - `biológica`
  - `fermentación`
  - `acidez`
  - `azúcar`
  - `tanino`
  - `espumoso`
  - `oxidación`

Suggested regression check:

- Compare retrieval output for a small set of Spanish queries before/after and inspect whether changes are limited to improved token matches/rank order, not governance or source filtering.

## Rollback Strategy

Rollback is one-line and local: restore the previous `_tokens()` regex in `tools/retrieval/tutor_retrieval_sandbox.py`.

Before accepting the change, save benchmark artifacts or command output for comparison. If brutal self-eval worsens unexpectedly beyond explainable retrieval-rank changes, revert the tokenizer and defer Unicode work until retrieval snapshots are added.

Governance rollback checks:

- Confirm `safe_for_examiner` remains false in Tutor, self-eval, and reporter artifacts.
- Confirm no new API, cloud, embedding, vector DB, or Examiner scoring path is introduced.
- Confirm official source files and raw source files are untouched.

## Benchmark Commands After Implementation

Run:

```bash
python -m unittest discover -s tests -v
python -m tools.youtube_transcription.main self-eval --limit 25 --question-type all --strictness brutal
```

Acceptance target:

- Unit tests pass.
- Governance remains unchanged.
- No new failure labels appear without an explainable retrieval improvement.
- Current brutal benchmark should remain at or near the latest known state, where only `shallow_reasoning: 1` remains.
