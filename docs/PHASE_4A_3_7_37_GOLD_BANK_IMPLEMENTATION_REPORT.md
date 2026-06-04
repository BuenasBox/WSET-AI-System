# Phase 4A.3.7.37 Gold Bank Implementation Report

Status: implemented for private Diagnostic SBA static-demo lab only. No publication, Tutor change, Retrieval change, Self-Eval change, snapshot change, causal-chain change, governance change, or option shuffle was introduced.

## Implementation Summary

The active private Diagnostic SBA lab was moved from the historical 18-item active set to a 36-item Gold Bank target set.

Implementation actions:

| Action | Result |
|---|---|
| Historical non-Gold active reviews | Preserved but changed out of `approved_for_static_demo` eligibility. |
| Gold Bank activation drafts | Added `knowledge/question-bank/diagnostic_sba/drafts/gold_bank_activation_drafts.json`. |
| Gold Bank activation reviews | Added `knowledge/question-bank/diagnostic_sba/reviews/gold_bank_activation_review_records.json`. |
| Dynamic exporter | Unchanged. |
| Frontend payload | Regenerated `frontend/diagnostic-sba/preguntas.json`. |
| Option shuffle | Not implemented. |

Final dry-run result:

```text
eligible_item_count: 36
validation_errors: 0
```

## Selection Rule

The final set uses all available Gold-A and Gold-B items from `docs/CORPUS_GROUNDED_GOLD_BANK.md`, plus one explicit Gold-C exception:

| Class | Count | Items |
|---|---:|---|
| Gold-A | 15 | Q2, Q83, Q105, Q228, Q258, Q265, Q287, Q309, Q356, Q424, Q659, Q834, Q269, Q438, Q498 |
| Gold-B | 20 | Q107, Q206, Q216, Q230, Q232, Q240, Q268, Q270, Q277, Q301, Q308, Q325, Q395, Q402, Q421, Q440, Q441, Q464, Q493, Q515 |
| Gold-C exception | 1 | Q21 |

Q21 is included only because the target was explicitly set to 36 questions and there are only 35 Gold-A/Gold-B items. It is the rank-36 Gold candidate, has STRONG corpus grounding in the Gold Bank, and remains bounded to private static-demo training use. Its Gold-C source-specificity/distractor-strength risk remains documented.

## Previous 18

```text
Q2, Q4, Q5, Q12, Q15, Q17, Q20, Q30, Q44, Q50, Q78, Q83, Q87, Q108, Q247, Q253, Q386, Q510
```

Survived:

```text
Q2, Q83
```

Removed from active eligibility:

```text
Q4, Q5, Q12, Q15, Q17, Q20, Q30, Q44, Q50, Q78, Q87, Q108, Q247, Q253, Q386, Q510
```

## Final 36

```text
Q2, Q21, Q83, Q105, Q107, Q206, Q216, Q228, Q230, Q232, Q240, Q258,
Q265, Q268, Q269, Q270, Q277, Q287, Q301, Q308, Q309, Q325, Q356, Q395,
Q402, Q421, Q424, Q438, Q440, Q441, Q464, Q493, Q498, Q515, Q659, Q834
```

Added:

```text
Q21, Q105, Q107, Q206, Q216, Q228, Q230, Q232, Q240, Q258, Q265, Q268,
Q269, Q270, Q277, Q287, Q301, Q308, Q309, Q325, Q356, Q395, Q402, Q421,
Q424, Q438, Q440, Q441, Q464, Q493, Q498, Q515, Q659, Q834
```

## Coverage Before And After

### RA Coverage

| RA | Previous 18 | Final 36 | Change |
|---|---:|---:|---:|
| RA1 | 9 | 5 | -4 |
| RA2 | 3 | 22 | +19 |
| RA3 | 2 | 5 | +3 |
| RA4 | 3 | 3 | 0 |
| RA5 | 1 | 1 | 0 |

RA2 coverage increases substantially because the Gold Bank's strongest official-corpus grounding is concentrated in regional still-wine items. RA1 and RA5 remain coverage risks despite the larger set.

### Topic Coverage

| Topic | Final count |
|---|---:|
| still_wines | 20 |
| sparkling_wines | 5 |
| fortified_wines | 3 |
| winemaking | 3 |
| viticulture | 2 |
| quality_factors | 2 |
| label_law | 1 |

### Difficulty Distribution

| Difficulty | Final count |
|---|---:|
| intermediate | 36 |

This is not an ideal cognitive spread. It is accepted for this implementation because the instruction prohibited modifying question content and the current Gold Bank is difficulty-uniform. Future metadata hardening should assign cognitive-demand difficulty after source-specific review.

### Correct Answer Distribution

| Option | Previous 18 | Final 36 |
|---|---:|---:|
| A | 3 | 5 |
| B | 4 | 13 |
| C | 8 | 15 |
| D | 3 | 3 |

The final set remains B/C-heavy, but no option shuffle was implemented in this phase.

## Validation

Exporter dry-run:

```text
export_version: static_demo_export_v0
static_demo_only: True
eligible_item_count: 36
source_question_ids: 2, 21, 83, 105, 107, 206, 216, 228, 230, 232, 240, 258, 265, 268, 269, 270, 277, 287, 301, 308, 309, 325, 356, 395, 402, 421, 424, 438, 440, 441, 464, 493, 498, 515, 659, 834
validation_errors: 0
target_path: frontend/diagnostic-sba/preguntas.json
```

Test suite:

```text
python -m unittest discover -s tests -v
Ran 1352 tests
OK (skipped=9)
```

Slow golden self-eval check:

```text
$env:RUN_SLOW_TESTS='1'; python -m unittest tests.test_golden_self_eval -v
FAILED (failures=4)
```

Observed slow-test failures:

| Metric | Live result |
|---|---:|
| `missing_keyword_support` | 17, golden maximum 5 |
| `shallow_retrieval` failure labels | 13 |
| `shallow_reasoning` failure labels | 12 |
| `missing_causal_link` failure labels | 1 |
| New retrieval weakness types | `shallow_retrieval`, `missing_causal_link_support` |
| New missing causal chain | `cause -> mechanism -> effect` |

This failure is recorded as a separate Tutor/Retrieval/Self-Eval baseline issue. Phase 4A.3.7.37 did not modify those modules, and the phase restrictions explicitly prohibited touching them.

Governance validation:

| Check | Result |
|---|---|
| `safe_for_examiner` | All false |
| `examiner_scoring_allowed` | All false |
| `official_wset_question` | All false |
| `training_item_only` | All true |
| `static_demo_only` | All true |
| Pre-submit correctness leakage | None in render payload |
| Outcome payload separation | Preserved |

## Gains Over The Historical 18

| Dimension | Previous 18 | Final 36 | Gain |
|---|---:|---:|---|
| Gold-A | 2 | 15 | +13 |
| Gold-B | 0 | 20 | +20 |
| Gold-C | 0 | 1 | +1 explicit exception |
| Non-Gold active items | 16 | 0 | -16 |
| STRONG-grounded Gold candidates | 2 | 36 | +34 |
| Historical conflict-bearing active items | 2 | 0 | Removed Q5 and Q17 from active eligibility |
| NOT_FOUND active items | 7 | 0 | Removed unsupported historical active items |

## Remaining Risks

| Risk | Assessment |
|---|---|
| Q21 Gold-C exception | Accepted only to meet the explicit 36-item target; should be first candidate for later repair or replacement. |
| RA2 dominance | High; final set is strongest where the Gold Bank is strongest, but not balanced across the full WSET L3 curriculum. |
| RA5 weakness | High; only Q834 is active and it covers label hierarchy, not storage/service/price breadth. |
| Difficulty uniformity | Medium; all final payload items are `intermediate`. |
| Correct option bias | Medium; B/C remain overrepresented and D remains low. |
| Gold-B review notes | Medium; Gold-B items retain source-specificity or metadata-hardening follow-up notes. |

## Recommendations Next

1. Do not publish yet.
2. Keep option shuffle as a separate implementation phase with original/display option identity.
3. Run a source-specific hardening pass for Gold-B items, starting with Q107, Q216, Q240, Q270, Q277, Q301, Q308, Q325, Q402, and Q421.
4. Replace or repair Q21 before any public-facing expansion.
5. Start a PARTIAL promotion cycle for RA5 service/storage/price and RA1 causal viticulture gaps.
