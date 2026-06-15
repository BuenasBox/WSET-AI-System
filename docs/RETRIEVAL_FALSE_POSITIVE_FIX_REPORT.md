# Retrieval False Positive Fix Report

**Date:** 2026-06-15
**Status:** Fix implemented and focused validation complete
**Scope:** Tutor retrieval and causal-chain rendering only

## Root Cause Summary

The retrieval sandbox used an English-only stopword set against predominantly
Spanish questions. Generic tokens such as `es`, `de`, `el`, `en`, `qué`, and
question-framing terms were therefore treated as strong semantic evidence.

`detect_knowledge_nodes()` accepted a causal chain when two query tokens
occurred anywhere in the node's combined identity, trigger sentences, and
selected step phrases. Q24 consequently matched
`HC_CANOPY_VIGOUR_EXPOSURE` through `es` and `técnica`.

The Tutor then rendered the first forced chain when every complete trigger
phrase scored zero, converting the retrieval false positive into unsupported
causal prose.

## Files Changed

- `tools/retrieval/tutor_retrieval_sandbox.py`
  - Added Spanish stopwords and low-signal question terms.
  - Added domain-bearing causal-token filtering.
  - Required the two-token causal threshold to use domain-bearing tokens.
  - Added geographic-scope protection for region-specific causal nodes.
- `tools/tutor/answer_builder.py`
  - Changed causal selection to return `None` when every complete-trigger score
    is zero.
- `tests/test_retrieval_spanish_false_positive.py`
  - Added 10 focused regression tests.
- `tests/fixtures/tutor_snapshots/17/expected_answer.txt`
  - Replaced an unrelated mechanical-harvest chain with the existing
    destemming fallback after the new zero-score guard correctly rejected it.
- `docs/RETRIEVAL_ROOT_CAUSE_REPORT.md`
  - Preserved the investigation evidence.
- `docs/RETRIEVAL_FALSE_POSITIVE_FIX_REPORT.md`
  - Added this implementation and validation record.

No SBA Batch 1 or Batch 2 question content was changed. Matcher-v2 enrichment
behavior was not changed. Governance constants and flags were not changed.

## Tests Added

The new regression suite verifies:

1. Required Spanish and low-signal stopwords are excluded.
2. `es + técnica` cannot activate the canopy node.
3. Q24 does not retrieve the canopy node.
4. Representative sparkling questions do not receive unrelated viticulture
   chains.
5. A Chilean cool-climate sparkling question retains generic cool-climate
   support but does not receive a Mosel-specific chain.
6. Valid canopy/vigour queries still retrieve
   `HC_CANOPY_VIGOUR_EXPOSURE`.
7. Valid soil-drainage/vigour queries still retrieve their causal chain.
8. Returned causal nodes retain safe governance flags.
9. Zero-score forced candidates are not selected.
10. Q24 brutal self-evaluation no longer reports
    `unsupported_conclusion`.

## Before and After

The same matcher-level audit was run against all 663 records currently present
in the structured corpus.

| Measure | Before | After |
|---|---:|---:|
| Questions matching at least one causal chain | 662 | 360 |
| Total causal-chain matches | 32,877 | 716 |
| Questions matching `HC_CANOPY_VIGOUR_EXPOSURE` | 643 | 22 |
| Sparkling questions with viticulture-like chains | 60 of 63 | 1 of 63 |
| Viticulture-like matches across sparkling questions | 599 | 1 |

The one remaining sparkling/viticulture-like match is intentional:
`HC_COOL_CLIMATE_STYLE` supports a question that explicitly asks about
cool-climate Chilean sparkling wine. The incorrect Mosel-specific chain is no
longer matched.

## Q24 Result

### Before

- Matched causal chain: `HC_CANOPY_VIGOUR_EXPOSURE`
- Activating overlap: `es`, `técnica`
- Brutal self-eval: `unsupported_conclusion`
- Chunk ranking was contaminated by canopy expansion terms such as `balance`
  and `growing season`.

### After

- Matched causal chains: none
- Forced causal nodes: none
- Brutal self-eval failure labels: none
- Top retrieval now includes:
  1. common winemaking and maturation
  2. sparkling wines of the world
  3. sparkling-wine production
  4. Spain
- No canopy terms are injected into chunk scoring.

## Sparkling Subset

The brutal Q21-Q30 subset produced no failure labels for Q21-Q25, including
Q24. Q25 retained the valid `HC_LIQUEUR_TIRAGE_SECOND_FERMENTATION` chain.
Q22 retained only relevant climate and sparkling-base-acidity support.

Q26-Q30 still report pre-existing `shallow_reasoning` labels; none retrieved
the canopy node or unrelated viticulture chains. Those labels are outside this
false-positive fix.

## Validation Results

- New false-positive regression suite: 10/10 passed.
- Combined retrieval, planner, score, and snapshot gate: 159 passed, 1 skipped.
- SBA Batch 1 and governance gate: 45/45 passed.
- Existing causal loading/rendering plus retrieval sandbox: 26/26 passed.
- Tutor snapshots: 35/35 passed.
- Q24 isolated brutal self-eval: no failure labels.
- Q21-Q30 brutal subset: no `unsupported_conclusion` labels.
- `git diff --check`: passed for implementation files; the regenerated Q17
  snapshot reports only Git's CRLF normalization warning.

Full `python -m unittest discover -s tests -v` exceeded the five-minute command
limit and was terminated. Separately, the broader
`tests.test_milestone_1_3` module encountered an existing UTF-8 BOM parsing
error in local misconception data. The retrieval, causal-chain, Batch 1,
snapshot, and governance-focused tests listed above all passed.

## Resume Recommendation

SBA Batch 1 remains valid and its focused integration tests pass.

Batch 2 integration may resume. The retrieval defect that paused expansion is
fixed, Q24 is clean, valid viticulture retrieval remains operational, and the
sparkling false-positive surface has been reduced to one explicitly relevant
cool-climate match.

The unrelated misconception BOM parsing issue should be tracked separately; it
does not originate in this retrieval change.

This report is formative project documentation. It does not represent WSET
assessment, examiner evaluation, official scoring, or pass prediction.
