# Causal Chain Impact Report
## WSET-AI-System — Structural Reasoning Substrate Assessment

**Date:** 2026-05-15
**Scope:** Analysis of the 9 causal chain nodes added in Milestone 2, their retrieval coverage, rendering quality, and expected self-eval impact

---

## Chains Added

| Node ID | Topic | Trigger Keywords (count) | Linked Misconceptions |
|---|---|---|---|
| CC_COOL_CLIMATE_ACIDITY | Cool climate → acidity retention | 7 | MC_ACIDITY_01, MC_COOL_CLIMATE_02 |
| CC_WARM_CLIMATE_ALCOHOL | Warm climate → alcohol level | 8 | MC_ALCOHOL_QUALITY_01 |
| CC_FLOR_BIOLOGICAL_AGEING | Flor yeast → biological ageing | 8 | — |
| CC_FORTIFICATION_RESIDUAL_SUGAR | Fortification → residual sugar | 8 | MC_RESIDUAL_SUGAR_SWEET_01 |
| CC_MLF_TEXTURE | MLF → wine texture | 8 | — |
| CC_TANNIN_ASTRINGENCY | Tannin → astringency | 8 | MC_TANNIN_01, MC_TANNIN_QUALITY_02 |
| CC_BARREL_AGEING_OAK_CHARACTER | Barrel ageing → oak character | 8 | MC_OAK_QUALITY_01 |
| CC_BOTTLE_AGEING_SEDIMENT | Bottle ageing → sediment/tertiary | 8 | MC_AGEING_IMPROVEMENT_01 |
| CC_FRACTIONAL_BLENDING_CONSISTENCY | Solera → consistency | 8 | — |

---

## Coverage of Baseline Failing Causal Chains

Cross-referencing the 9 new nodes against the top failing causal chains identified in the baseline self-eval:

| Failing chain (self-eval baseline) | Weighted failures | Covered by node? | Node ID |
|---|---|---|---|
| cause -> mechanism -> effect | 14 | ✓ Structural template in all nodes | All CC_* nodes |
| flor -> oxygen protection -> biological ageing | 1 | ✓ | CC_FLOR_BIOLOGICAL_AGEING |
| fortification -> yeast stops -> residual sugar | 1 | ✓ | CC_FORTIFICATION_RESIDUAL_SUGAR |
| structure -> bottle ageing -> sediment | 1 | ✓ | CC_BOTTLE_AGEING_SEDIMENT |
| fractional blending -> consistency | 1 | ✓ | CC_FRACTIONAL_BLENDING_CONSISTENCY |
| flor dies -> oxidative ageing | 1 | ~ Partial (flor node covers onset; oxidative continuation is separate) | CC_FLOR_BIOLOGICAL_AGEING |
| no flor -> oxidative ageing | 1 | ✗ Not yet covered (requires CC_OXIDATIVE_AGEING node) | — |

**Coverage: 6 of 7 named failing chains fully or partially covered. 1 gap remains (no flor → oxidative ageing).**

The generic `cause -> mechanism -> effect` structural failure (14 weighted failures) is addressed by the rendering layer: all 9 nodes produce explicit CAUSA / MECANISMO / EFECTO / FORMULACIÓN sections, providing the structural connector pattern the self-eval's `_has_cause_mechanism_effect()` checks for.

---

## Rendering Quality Assessment

Each node's `steps` array provides 4 ordered entries:

**Step 1 — cause:** Describes the initiating condition (climate, winemaking decision, ageing method)
**Step 2 — mechanism:** Explains the intermediate process — this is the Distinction-level content WSET L3 examiners look for
**Step 3 — effect:** Describes the observable/measurable outcome on the wine
**Step 4 — exam_formulation:** A complete exam-ready sentence linking cause to effect in WSET register

The mechanism step is the critical one. In the baseline, the dominant failure was not merely missing a causal connector — it was missing the mechanism that justifies the causal claim. Example:

**Baseline output (keyword dispatch):**
> "Cadena: clima fresco → maduración más lenta → mayor retención de ácidos → más acidity y sensación de frescura en el vino."

This is one hardcoded sentence. It contains the right concepts but provides no mechanism (why does slow ripening preserve acids? Which acids? What happens to them as grapes ripen?).

**Post-implementation output (CC_COOL_CLIMATE_ACIDITY):**
> **CAUSA:** Cool growing environment (lower temperatures, high altitude, or high-latitude location)
> **MECANISMO:** Slow ripening delays sugar accumulation and preserves natural grape acids (malic and tartaric), reducing the rate at which malic acid is metabolised before harvest
> **EFECTO:** Wines retain higher acidity, show freshness and crispness, and typically have lower alcohol levels
> **FORMULACIÓN DE EXAMEN:** Cool climates slow ripening, preserving acidity and producing wines with higher acidity, freshness, and lower alcohol levels.
> *Relevancia SAT: Use when justifying high acidity as a positive structural element in SAT quality assessment...*

This output explicitly names malic acid, explains degradation rate, and distinguishes malic from tartaric acid — the Distinction-level content. The self-eval's `_has_cause_mechanism_effect()` should now detect:
- Causal connector: "preserving" or "reducing"
- Mechanism term: "malic acid" / "metabolised" / "ripening"
- Effect term: "freshness" / "acidity" / "lower alcohol"

---

## Retrieval Pathway

The causal chain nodes are loaded by `load_knowledge_nodes()` which recursively scans `knowledge/knowledge-map/`. The directory `causal-chains/` is now populated and will be picked up automatically.

Detection happens in `detect_knowledge_nodes()` via:
1. Node type identification (`_knowledge_node_type()` now recognises `node_type: "causal_chain"`)
2. Token overlap with `_knowledge_node_primary_phrases()` which now includes `trigger_keywords` and step texts
3. Threshold: `len(strong_hits) >= 2` for causal chain matching

When a chain is matched:
1. It appears in `query_analysis["matched_causal_chains"]`
2. `select_matched_causal_chain_nodes()` looks up the full node data
3. Full nodes passed as `matched_causal_chain_nodes` in the retrieval run
4. Orchestrator threads them into `context_package["forced_causal_chains"]`
5. Tutor's `_select_best_causal_chain()` picks the highest-keyword-overlap chain
6. `_render_causal_chain()` renders the structured output

---

## Gaps Identified During Chain Authoring

**Missing chain: CC_OXIDATIVE_AGEING**
The chain `no flor → oxidative ageing` appears in the self-eval failure list (1 weighted failure). It requires a separate node covering the absence of flor and development of oxidative Oloroso character. Not added in this session.

**Missing chain: CC_DIURNAL_VARIATION**
Diurnal temperature variation (warm days + cold nights) is mentioned in the Distinction note for CC_COOL_CLIMATE_ACIDITY. It is a Distinction-level nuance and warrants its own node.

**Missing chain: CC_CARBONIC_MACERATION**
Whole bunch fermentation / carbonic maceration produces a distinctive cherry/banana ester profile. This is an exam question topic that currently has no causal chain support.

These gaps are not blockers — the 9 chains added cover the highest-weighted failures. But they represent the next expansion target for the knowledge graph.

---

## SAT Relevance Integration

Each node includes a `sat_relevance` field. This field is rendered in the Tutor output as a SAT usage note:

> *Relevancia SAT: Use when justifying high acidity as a positive structural element in SAT quality assessment. High acidity in a cool-climate context is a feature, not a fault — link it to freshness, food-pairing versatility, and ageing potential.*

This directly addresses the self-eval's `weak_exam_register` failure — the SAT relevance note provides the exam-framing language the student needs to write a distinction-level quality assessment.

---

*Generated: 2026-05-15 | Causal Chain Impact Report | Phase F*
*Not an official WSET document. Not for learner-facing use.*
