# Batch 3 Candidate Report: Botrytis Concentration

**Date:** 2026-06-12  
**Phase:** P.3 candidate review  
**Status:** Candidate only; not deployed and not merged into production payloads

## 1. Headline result

| Metric | Result |
|---|---:|
| Production SBA bank | 578 items |
| Existing enriched baseline | 11 items |
| New Batch 3 candidates | **3 items** |
| Candidate sidecar total | 14 items |
| Expected enriched total if approved | 14 items |
| Expected bank coverage if approved | 2.4% |
| Incremental coverage gain | +3 items, approximately +0.5 percentage points |
| New causal nodes | 2 |
| Candidates with micro-drill | 2 |

The Batch 3 candidate sidecar is:
`knowledge/question-bank/enrichment/sba_enrichment_batch3_candidate.json`.
The active `sba_enrichment_v1.json` sidecar remains unchanged.

## 2. New nodes created

### `HC_BOTRYTIS_CONCENTRATION`

Explains beneficial Botrytis infection, skin perforation, water loss, and the
concentration of sugar, remaining acids, flavour compounds, and glycerol
precursors. It preserves the important acidity nuance: Botrytis also
metabolizes grape acids, so net acidity is lower than simple concentration
alone would predict.

Specific matching evidence includes:

- `botrytis`
- `botrytis cinerea`
- `mayor concentración`
- `concentración de azúcar`
- `aumenta la concentración`

### `HC_NOBLE_ROT_DEVELOPMENT_CONDITIONS`

Explains the climatic sequence required for beneficial noble rot: humid or
misty mornings establish Botrytis, while warmer dry afternoons limit
destructive grey rot and promote controlled evaporation.

Specific matching evidence includes:

- `podredumbre noble`
- `clima húmedo`
- `nieblas matinales`
- `morning mist`
- `dry afternoons`

Both nodes are heuristic, formative-only, subject to human review, and retain:

```text
safe_for_examiner = false
examiner_scoring_allowed = false
```

## 3. Spanish layer

Both nodes have complete Spanish learner-facing layers:

- `subject`
- `causa`
- `mecanismo`
- `efecto`

The existing deterministic templates use these fields to generate
`feedback_by_mode`, `causal_chain`, and, where the existing drill rules permit,
`micro_drill`.

No matcher thresholds, matching functions, stoplists, polarity rules, or
identification guards were changed.

## 4. Candidate inventory

| Item ID | Node | Score | Stem hits | Correct-answer hits | Micro-drill |
|---|---|---:|---|---|---|
| `wset3_372` | `HC_BOTRYTIS_CONCENTRATION` | 3 | `botrytis` | `aumenta la concentracion`, `concentracion de azucar` | Yes |
| `wset3_426` | `HC_BOTRYTIS_CONCENTRATION` | 3 | `botrytis`, `botrytis cinerea` | `mayor concentracion` | No |
| `wset3_510` | `HC_NOBLE_ROT_DEVELOPMENT_CONDITIONS` | 3 | `podredumbre noble` | `clima humedo`, `nieblas matinales` | Yes |

`wset3_426` does not receive a micro-drill because its correct answer,
`Mayor concentración`, is shorter than the existing minimum drill-option
length. The pipeline omits the drill rather than weakening that guard or
inventing substitute text.

## 5. Candidate examples

### `wset3_372`

**Question:** ¿Cuál es el efecto de la botrytis en los vinos de Tokaj?  
**Correct answer:** Aumenta la concentración de azúcar y acidez  
**Node:** `HC_BOTRYTIS_CONCENTRATION`

The enrichment explains water loss through perforated skins and concentration
of dissolved components. It also states that Botrytis metabolizes some grape
acids, so net acidity remains lower than concentration alone would predict.
This prevents the source answer from being taught as an unqualified
"all acidity simply rises" rule.

### `wset3_426`

**Question:** ¿Qué efecto tiene la botrytis cinerea deseada?  
**Correct answer:** Mayor concentración  
**Node:** `HC_BOTRYTIS_CONCENTRATION`

This is the cleanest direct mechanism match: Botrytis appears in the stem and
concentration appears in the correct answer. The causal explanation supplies
the missing mechanism between them.

### `wset3_510`

**Question:** ¿Qué tipo de clima es más propenso a desarrollar podredumbre noble?  
**Correct answer:** Clima húmedo con nieblas matinales  
**Node:** `HC_NOBLE_ROT_DEVELOPMENT_CONDITIONS`

The node explains why humidity and morning mist support infection and why dry
afternoons remain necessary to produce beneficial noble rot rather than
destructive grey rot.

## 6. False-positive risk assessment

| Risk | Control and result |
|---|---|
| Beneficial noble rot confused with harmful Botrytis | The nodes require mechanism-specific stem and correct-answer evidence. Generic disease references do not qualify. |
| Negative-polarity stem promoted as truth | `wset3_783` remains excluded by the existing negative-polarity guard. |
| Regional identification treated as causal | `wset3_350` remains excluded by the identification-stem guard. |
| Botrytis mitigation mapped to concentration | `wset3_489` remains excluded because `Canopy abierto` has no correct-answer hit for either new node. |
| Tokaji production practice mapped to concentration | `wset3_8` remains excluded; the new nodes do not use `Tokaji Aszú` or `bayas botritizadas` as a shortcut match. |
| Correct answer mentions Botrytis but stem lacks mechanism | `wset3_309` remains excluded because it does not satisfy the required stem hit. |
| Generic concentration collision | Existing `HC_YIELD_CONCENTRATION` remains distinct; Botrytis candidates win through explicit Botrytis/noble-rot evidence and unique-best scoring. |
| Acidity oversimplification | The concentration node explicitly includes Botrytis acid metabolism and lower-than-simple-concentration net acidity. |

Current candidate-pipeline rejection totals remain conservative:

| Rejection reason | Count |
|---|---:|
| Below threshold | 138 |
| Identification stem | 112 |
| Negative-polarity stem | 24 |
| Missing correct-answer hit | 11 |
| Missing stem hit | 5 |

## 7. Precision and expected coverage

All three candidates have score 3, exceed the unchanged minimum of 2, contain
at least one stem hit, contain at least one correct-answer hit, and have a
unique best node.

If approved for a later production step, enrichment coverage would increase:

```text
11 / 578 = 1.9%
14 / 578 = 2.4%
gain       = 3 items, approximately 0.5 percentage points
```

The gain comes from new causal knowledge and Spanish rendering coverage, not
from looser matching.

## 8. Candidate status

Completed for review:

- two Botrytis causal nodes;
- Spanish learner-facing layers;
- separate candidate sidecar;
- three precision-standard candidate items;
- focused regression tests;
- candidate report.

Not performed:

- no active sidecar replacement;
- no frontend payload regeneration;
- no production-bank modification;
- no deployment;
- no implementation of Lees ageing, MLF, hazards, bottle ageing, or broader
  sparkling mechanisms.

This candidate batch must receive human approval before any production
promotion.

---

*Formative training artifact. No examiner authority.*
