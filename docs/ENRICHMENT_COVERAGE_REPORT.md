# Enrichment Coverage Report

**Status date:** 2026-06-12  
**Scope:** Coverage after Batch 2; Batch 3 recommendations only  
**Authority:** Formative training analysis only. No examiner scoring or assessment authority.

## 1. Current enrichment status

| Metric | Count |
|---|---:|
| Total SBA bank | 578 |
| Total enriched SBA items | 11 |
| Batch 1 enriched items | 8 |
| Batch 2 enriched items | 3 |
| Enriched share of SBA bank | 1.9% |
| Distinct causal nodes represented | 10 |

Batch 2 increased coverage from 8 to 11 items by adding causal knowledge while
preserving the matcher v2 precision contract. All 11 promoted items contain the
complete enrichment bundle: mentor-mode feedback, a causal chain, and a
node-anchored micro-drill. These fields activate the TRAIN phase for the item.

## 2. Coverage inventory

| Batch | Item ID | Causal node | Enrichment type |
|---:|---|---|---|
| 1 | `wset3_2` | `CC_FORTIFICATION_RESIDUAL_SUGAR` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |
| 1 | `wset3_4` | `CC_FRACTIONAL_BLENDING_CONSISTENCY` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |
| 1 | `wset3_17` | `CC_DESTEMMING_TANNIN_STRUCTURE` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |
| 1 | `wset3_99` | `CC_BOTTLE_AGEING_SEDIMENT` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |
| 1 | `wset3_102` | `CC_FLOR_BIOLOGICAL_AGEING` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |
| 1 | `wset3_209` | `CC_FRACTIONAL_BLENDING_CONSISTENCY` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |
| 1 | `wset3_373` | `CC_MACERATION_EXTRACTION` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |
| 1 | `wset3_705` | `HC_OAK_AGEING_COMPLEXITY` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |
| 2 | `wset3_380` | `HC_DIURNAL_RANGE_FRESHNESS` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |
| 2 | `wset3_497` | `HC_YIELD_CONCENTRATION` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |
| 2 | `wset3_706` | `HC_WATER_STRESS_CONCENTRATION` | Full: `feedback_by_mode` + `causal_chain` + `micro_drill` |

## 3. Coverage by causal node

Percentages use the 11 enriched items as the denominator.

| Causal node | Item count | Coverage |
|---|---:|---:|
| `CC_FRACTIONAL_BLENDING_CONSISTENCY` | 2 | 18.2% |
| `CC_BOTTLE_AGEING_SEDIMENT` | 1 | 9.1% |
| `CC_DESTEMMING_TANNIN_STRUCTURE` | 1 | 9.1% |
| `CC_FLOR_BIOLOGICAL_AGEING` | 1 | 9.1% |
| `CC_FORTIFICATION_RESIDUAL_SUGAR` | 1 | 9.1% |
| `CC_MACERATION_EXTRACTION` | 1 | 9.1% |
| `HC_DIURNAL_RANGE_FRESHNESS` | 1 | 9.1% |
| `HC_OAK_AGEING_COMPLEXITY` | 1 | 9.1% |
| `HC_WATER_STRESS_CONCENTRATION` | 1 | 9.1% |
| `HC_YIELD_CONCENTRATION` | 1 | 9.1% |

Coverage is broad but intentionally sparse. Nine nodes have one item each, and
one node has two. This is preferable to inflating coverage with weak or
ambiguous matches.

## 4. Features activated by enrichment

- **Mentor selector:** `feedback_by_mode` supplies differentiated Spanish
  guidance for Mentor Guia, Entrenador Tecnico, and Revisor Estricto. The
  selector is data-backed for enriched items rather than acting as a placebo.
- **`feedback_by_mode`:** Each mode explains or challenges the learner from a
  distinct pedagogical stance while remaining anchored to the correct answer
  and matched causal mechanism.
- **`causal_chain`:** Exposes the item's cause, mechanism, and effect, turning a
  correct option into an inspectable explanation rather than answer-only
  feedback.
- **`micro_drill`:** Adds a node-anchored consolidation question. Its correct
  option remains the source item's correct answer; distractors come from other
  mechanisms.
- **TRAIN phase:** The presence of `micro_drill` activates the post-feedback
  practice stage for that item. Unenriched items continue through the guarded
  non-drill path.

## 5. Safety architecture

- **Matcher v2 strict:** Requires at least two specific keyword hits, a stem
  hit, a correct-answer hit, and a unique best node. Matching remains
  deterministic and precision-first.
- **Stoplist:** Generic terms such as wine, climate, acidity, ageing, and style
  cannot independently create a causal match.
- **Word-boundary matching:** Prevents substring collisions and preserves
  whole-term semantics.
- **Stem hit:** At least one node-specific trigger must occur in the question
  stem, establishing that the question actually invokes the mechanism.
- **Correct-answer hit:** At least one node-specific trigger must occur in the
  correct option, establishing that the node explains why that option is
  correct.
- **Negative polarity guard:** Stems using forms such as `INCORRECT`, `FALSE`,
  `EXCEPT`, `no es correcto`, or `no influye` are excluded so a deliberately
  false option cannot be promoted into a positive micro-drill statement.

These controls supplement provenance tracking for node assignment, match score,
matched keywords, stem hits, and correct-option hits. They must remain intact.

## 6. Rejection inventory

| Rejection reason | Count | Interpretation |
|---|---:|---|
| Below threshold | 139 | Available evidence did not meet the strict minimum score. |
| Identification stem | 112 | The item asks for identification or factual recall rather than a causal explanation. |
| Negative polarity | 24 | The correct option is deliberately false or exceptional under the wording of the stem. |
| Missing correct-answer hit | 11 | The node may be topically related, but it does not explain the correct option. |
| Missing stem hit | 4 | The answer may contain related language, but the question does not establish the mechanism. |

Rejections are expected safety outcomes, not enrichment failures. In
particular, Vinho Verde, Loire climate, and negative-polarity false positives
remain intentionally excluded.

## 7. Batch 3 candidate domains

Batch 3 should remain a knowledge-expansion exercise. Candidate domains should
be evaluated against bank demand, mechanism specificity, answer explainability,
and false-positive risk before any item is promoted.

| Candidate domain | Recommendation | Rationale |
|---|---|---|
| MLF | High priority | Strong cause-mechanism-effect structure: malic-to-lactic conversion, softer acidity, texture, and controlled diacetyl expression. Keep acidity, texture, and aroma claims distinct where necessary. |
| Lees ageing | High priority | Clear mechanism through yeast autolysis, mannoprotein release, texture, stability, and autolytic aroma development. Distinguish still-wine lees work from tirage ageing where stems require it. |
| Botrytis concentration | High priority | Strong causal pathway through skin perforation, water loss, sugar/flavour concentration, and botrytis-specific effects. Preserve the distinction between noble rot concentration and acid metabolism. |
| Sparkling production mechanisms | High priority, split by mechanism | Potentially broad coverage, but it should be represented by specific nodes for secondary fermentation, lees contact, riddling/disgorgement, dosage, and carbonation rather than one generic sparkling node. |
| Viticulture hazard mitigation | Medium-high priority | Suitable where a mitigation clearly answers a named hazard. Separate frost, hail, drought, excessive rain, wind, and disease controls to avoid generic hazard matching. |
| Bottle ageing | Lower incremental priority | A bottle-ageing item is already enriched. Add new knowledge only for materially distinct mechanisms or uncovered answer patterns, not to duplicate sediment/polymerisation coverage. |

## 8. Recommendation

Coverage should increase through **new causal knowledge** that explains
currently unsupported correct answers. Do **not** loosen matcher thresholds.
Do **not** reduce precision standards.

Batch 3 should proceed only after candidate causal mechanisms are defined
narrowly enough to preserve stem evidence, correct-answer evidence, unique-best
selection, provenance, and negative-polarity protection. No Batch 3
implementation is authorized by this report.

---

`safe_for_examiner = false`  
`examiner_scoring_allowed = false`
