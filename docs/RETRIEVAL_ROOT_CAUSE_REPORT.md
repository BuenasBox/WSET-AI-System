# Retrieval Root Cause Report

**Date:** 2026-06-15
**Status:** Investigation complete; no fix applied
**Scope:** Q24 `unsupported_conclusion` after SBA Batch 1

## Executive Finding

The Q24 failure is caused by a systemic false-positive path in the deterministic
knowledge-node matcher. The retrieval stopword list is English-only, while the
question bank is predominantly Spanish. `detect_knowledge_nodes()` treats any
two remaining query tokens found anywhere in a causal node's name, identifier,
trigger sentences, or selected step phrases as a valid causal-chain match.

For Q24:

```text
¿Cuál es una diferencia técnica entre Cava y Champagne?
```

the query tokens `es` and `técnica` both occur in this canopy trigger sentence:

```text
técnica en la viña es esencial en Sancerre para controlar el vigor
```

That two-token overlap satisfies the causal-chain threshold and marks
`HC_CANOPY_VIGOUR_EXPOSURE` as the only matched causal chain.

This is not caused by SBA Batch 1 content, enrichment linkage, the planner hint
path, or governance. It is a pre-existing matcher defect exposed and greatly
amplified by the large causal-chain expansion added on 2026-06-12.

## Task 1: Q24 Reproduction

### Question and expected support

- Question ID: `24`
- RA: RA3
- Correct option: `C`
- Correct answer: `Champagne permite mezclas de múltiples añadas`
- Expected retrieval domain: Cava, Champagne, sparkling-wine production,
  traditional method, regional production rules and style comparison.
- Expected causal support: sparkling-specific nodes such as traditional bottle
  fermentation, Champagne ageing, or autolysis where relevant. A canopy,
  vigour, or bunch-exposure chain is not relevant.

### Actual causal candidate ranking

| Rank | Node | Overlap | Result |
|---:|---|---|---|
| 1 | `HC_CANOPY_VIGOUR_EXPOSURE` | `es`, `técnica` | Selected |
| below threshold | `CC_AUTOLYSIS_AROMA_TEXTURE` | `champagne` | Rejected: one token |
| below threshold | `CC_LEES_AGEING_AUTOLYSIS` | `champagne` | Rejected: one token |
| below threshold | `HC_VINTAGE_CHAMPAGNE_EXTENDED_AGEING` | `champagne` | Rejected: one token |

The matcher therefore rewards two generic Spanish words more strongly than one
domain-specific word.

### Actual chunk ranking

| Rank | Retrieved chunk | Score | Causal terms inherited from false match |
|---:|---|---:|---|
| 1 | `OFFICIAL_WSET_4_7_COMMON_ELEMENTS_IN_WINEMAKING_AND_MATURATION_001` | 0.6759 | `balance`, canopy node name |
| 2 | `OFFICIAL_WSET_1_1_THE_SYSTEMATIC_APPROACH_TO_TASTING_WINE_001` | 0.6274 | `balance`, canopy node name |
| 3 | `OFFICIAL_WSET_WINES_OF_THE_WORLD_6_19_30_SPAIN_001` | 0.6253 | `balance`, `growing season`, canopy node name |
| 4 | `OFFICIAL_WSET_WINES_OF_THE_WORLD_8_1_43_SHERRY_001` | 0.6218 | `balance`, `growing season`, canopy node name |
| 5 | `How_to_assess_the_quality_of_a_wine_for_WSET_Level_3-0001` | 0.4368 | `balance`, canopy node name |

The false node also expands the query with generic terms such as `balance` and
`growing season`, which contaminates chunk scoring after the initial false
positive.

The failure reproduced with isolated learner-state paths, so it is independent
of LES or session-ledger state.

## Task 2: Exact Root Cause

### Primary defect

File: `tools/retrieval/tutor_retrieval_sandbox.py`

1. `STOPWORDS` contains English words only.
2. `_tokens()` removes only that English list.
3. `_knowledge_node_primary_phrases()` adds full `trigger_keywords` and selected
   step-derived phrases to each node's searchable text.
4. `detect_knowledge_nodes()` flattens all those fields into one token set.
5. A causal chain is accepted when `len(strong_hits) >= 2`.

Spanish function words including `de`, `el`, `en`, `es`, `la`, `los`, `qué`,
`se`, `una`, and `entre` therefore count as strong semantic evidence.

### Q24-specific activating data

File:
`knowledge/knowledge-map/causal-chains/HC_CANOPY_VIGOUR_EXPOSURE.json`

The trigger sentence containing both `técnica` and `es` provides the exact
two-token collision. The node content is valid for its intended canopy domain;
the defect is that the matcher tokenizes a long trigger sentence and treats its
generic words as independent matching signals.

### Downstream amplifier

File: `tools/tutor/answer_builder.py`

`_select_best_causal_chain()` scores only complete trigger-keyword substrings.
When no complete trigger matches, every candidate scores zero and the function
returns the first chain. For Q24, the false canopy node is the sole candidate,
so it is rendered despite having no full trigger-phrase match.

### Ruled-out causes

- Planner query expansion: disabled by default.
- Planner causal-chain injection: disabled by default.
- Matcher-v2 enrichment derivation: not imported by the retrieval path.
- SBA Batch 1 enrichment linkage: not consulted for Q24 retrieval.
- Knowledge-map alias collision: no Cava/Champagne alias points to the canopy
  node.
- Governance: flags remained compliant and did not influence selection.
- Learner state: failure reproduced with isolated state.

## Task 3: Impact

The scan used the exact current matcher logic against the current structured
corpus:

| Measure | Result |
|---|---:|
| Structured questions scanned | 663 |
| Questions matching at least one causal chain | 662 |
| Total causal-chain matches | 32,877 |
| Questions matching `HC_CANOPY_VIGOUR_EXPOSURE` | 643 |
| Sparkling-related questions identified | 63 |
| Sparkling questions receiving at least one viticulture-like chain | 60 |
| Viticulture-like matches across sparkling questions | 599 |

Within the frozen 25-question self-eval set, 24 questions matched causal chains.
Q24 matched only the canopy node. Other Spanish questions commonly received
dozens of candidates; examples include 53 candidates for Q1, 93 for Q2, and 86
for Q14.

The broad counts include all records currently present in the worktree, not
only the 625-item post-Batch-1 operational count. They nevertheless establish
that the behavior is systemic rather than an isolated Q24 anomaly.

The most frequent viticulture-like leakage into sparkling questions included:

- `HC_CANOPY_VIGOUR_EXPOSURE`: 58 sparkling questions
- `HC_YIELD_CONCENTRATION`: 51
- `HC_COOL_CLIMATE_STYLE`: 45
- `HC_CANOPY_AIRFLOW_FUNGAL_RISK`: 34
- `HC_NIGHT_HARVEST_FRESHNESS`: 33
- `HC_SOUTH_FACING_EXPOSURE_RIPENESS`: 33

The matcher logic predates SBA Batch 1. The canopy node and the large heuristic
causal-chain expansion were added on 2026-06-12, making the latent defect
operationally visible.

## Recommended Fix

No fix was applied in this investigation.

Recommended remediation order:

1. Make token filtering language-aware, including Spanish function words and
   generic question-form words.
2. Stop treating arbitrary tokens from long trigger sentences and step prose as
   equally strong node identity evidence.
3. Require domain-bearing overlap or an atomic trigger-phrase match for causal
   chains; generic tokens must contribute zero match authority.
4. Make `_select_best_causal_chain()` fail closed when every complete-trigger
   score is zero instead of returning the first candidate.
5. Add negative-domain regression tests for Q24, the full sparkling fixture
   group, and representative RA1/RA2/RA4/RA5 Spanish questions.
6. Re-run the 25-question self-eval, snapshots, and a corpus-wide causal-match
   audit before resuming batch integration.

## Risk Assessment

**Severity: High.**

The direct answer can remain correct while an unrelated causal chain is
rendered as supporting reasoning. This creates unsupported conclusions and can
silently contaminate retrieval ranking through query expansion. Additional
causal nodes increase the collision surface.

The issue is systemic across Spanish retrieval, not isolated to Q24 or canopy
management.

## Batch 2 Decision

Batch 2 should not proceed to integration, validation, commit, or push before
this retrieval defect is fixed and the regression suite is green.

Independent offline drafting would not change the defect, but it cannot be
reliably validated as enrichment-ready while causal matching is contaminated.
RA4 expansion would also add more trigger-rich nodes and increase the current
false-positive surface. Therefore SBA expansion cannot safely continue in
parallel under the stated completion and validation requirements.

This report is formative project documentation. It does not represent WSET
assessment, examiner evaluation, official scoring, or pass prediction.
