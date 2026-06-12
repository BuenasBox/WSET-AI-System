# Batch 3 Domain Analysis

**Date:** 2026-06-12  
**Scope:** Read-only planning analysis; no Batch 3 implementation  
**Bank assessed:** 578 production SBA items

## 1. Decision criterion

The recommended domain must maximize credible new enrichment while preserving
matcher v2:

- at least two distinct, specific trigger hits;
- at least one stem hit;
- at least one correct-answer hit;
- a unique best causal node;
- word-boundary matching and the generic-term stoplist;
- identification-stem and negative-polarity exclusion;
- a Spanish learner-facing layer before promotion.

The estimates below are intentionally conservative. A topical mention is not
counted as enrichable unless an existing node can plausibly explain why the
correct option is correct.

## 2. Comparative result

| Domain | Existing direct nodes | Spanish coverage | Approx. incremental SBA coverage | False-positive risk | Expected match quality |
|---|---:|---|---:|---|---|
| Botrytis concentration | 2 | None | **3 high-confidence; 1 additional plausible** | Medium | High |
| Lees ageing | 2 direct, 1 adjacent | None | **3 high-confidence** | Medium | High for sparkling tirage; low outside that scope |
| MLF | 4 | None | **1 high-confidence** | Medium | Very high |
| Viticulture hazard mitigation | 1 direct, 2 adjacent | Partial | **1 high-confidence** | High if hazards are grouped | High for frost topology only |
| Bottle ageing | 3 | One direct node localized | **0-1 new**; 1 already enriched | Medium-high | High only for sediment/polymerisation |
| Sparkling production mechanisms | No broad production node; 2 overlapping lees/autolysis nodes | None | **0 independent; up to 3 via lees overlap** | High | Low as a broad domain |

**Finding:** Botrytis concentration offers the highest likely incremental
coverage from existing causal knowledge without weakening matcher v2.

## 3. Domain evaluations

### 3.1 MLF

**Existing causal nodes**

- `CC_MLF_ACIDITY`
- `CC_MLF_DIACETYL`
- `CC_MLF_TEXTURE`
- `HC_MLF_ACIDITY_TEXTURE`

`CC_MLF_TEXTURE` and `HC_MLF_ACIDITY_TEXTURE` already satisfy the enrichment
deriver's structural node contract. The other two use the richer causal schema
and are not currently consumable by this matcher path.

**Existing Spanish coverage**

None of the four nodes has a `NODE_ES` learner-facing layer. The compatible
nodes also lack an exact trigger for the bank's Spanish phrase
`fermentación maloláctica`, so the current read-only matcher yields no item.

**Potentially enrichable SBA items**

- Approximate high-confidence coverage: **1**
- Primary candidate: `wset3_704`

The stem names malolactic fermentation and the correct answer explicitly states
malic-to-lactic conversion and reduced acidity. This is an unusually clean
cause-mechanism-effect fit.

**False-positive risk**

Medium. Terms such as creamy, buttery, texture, and secondary fermentation can
also refer to lees, oak, or sparkling production. Matching should be anchored
to explicit malolactic, malic, or lactic evidence.

**Match quality expectation**

Very high for `wset3_704`; low for generic creamy-texture items that do not name
MLF in both the question context and correct-answer mechanism.

**Pedagogical value**

High. MLF connects a winemaking decision to acidity, texture, and aroma and is
well suited to causal explanation. Coverage volume is small, but the single
match would be precise and instructionally strong.

### 3.2 Lees ageing

**Existing causal nodes**

- `CC_LEES_AGEING_AUTOLYSIS`
- `CC_AUTOLYSIS_AROMA_TEXTURE`
- Adjacent: `CC_BARREL_AGEING_OAK_CHARACTER`

The two direct nodes describe tirage lees contact and autolysis in traditional-
method sparkling wine. They do not currently provide a dedicated causal model
for still-white lees ageing or batonnage.

**Existing Spanish coverage**

None. The two direct nodes also use the richer causal schema and do not expose
the `trigger_keywords` plus labeled `steps` contract required by the enrichment
deriver.

**Potentially enrichable SBA items**

- Approximate high-confidence coverage: **3**
- Strong candidates: `wset3_30`, `wset3_127`, `wset3_128`

These items connect prolonged lees contact or autolysis to bread/yeast aromas,
complexity, and creamy texture in sparkling wine. Several additional still-
wine lees and batonnage items occur in the bank, but the existing direct nodes
do not explain those mechanisms narrowly enough for precision-standard
promotion.

**False-positive risk**

Medium. Lees, yeast, creamy texture, complexity, and brioche overlap with flor,
MLF, oak, and general sparkling terminology. Still-wine lees work must not be
silently mapped to a Champagne tirage node.

**Match quality expectation**

High for the three sparkling autolysis items. Low to medium for still-white
items unless a genuinely applicable existing mechanism is identified.

**Pedagogical value**

Very high. The domain explains how time on lees changes aroma, texture, bubble
quality, and stability. It also supports useful discrimination between primary
fruit, MLF character, oak character, and autolytic development.

### 3.3 Bottle ageing

**Existing causal nodes**

- `CC_BOTTLE_AGEING_SEDIMENT`
- `CC_TANNIN_AGEABILITY`
- `CC_ACIDITY_AGEABILITY`

Only `CC_BOTTLE_AGEING_SEDIMENT` currently satisfies the enrichment deriver's
node contract.

**Existing Spanish coverage**

`CC_BOTTLE_AGEING_SEDIMENT` is localized and active. It already enriches
`wset3_99`. The two ageability nodes have no enrichment Spanish layer and use
the richer causal schema.

**Potentially enrichable SBA items**

- Existing enriched coverage: **1**
- Approximate additional coverage: **0-1**

`wset3_31` is a possible additional item because its correct answer links
bottle ageing to softer texture, but its stem does not explicitly establish
the bottle-ageing mechanism. Items about cork porosity, magnum format, bottle
service, or sparkling disgorgement are not valid matches for the existing
sediment/polymerisation node.

**False-positive risk**

Medium-high. `Botella` appears frequently in service, preservation, sparkling,
closure, and format questions. It cannot act as sufficient causal evidence.

**Match quality expectation**

High for sediment, tertiary aroma, tannin polymerisation, and structured-red
development. Low for generic bottle references.

**Pedagogical value**

High, but incremental value is limited because the clearest existing match is
already enriched.

### 3.4 Botrytis concentration

**Existing causal nodes**

- `CC_NOBLE_ROT_SUGAR_CONCENTRATION`
- `CC_BOTRYTIS_ACIDITY_REDUCTION`

Together they distinguish the main concentration mechanism from the more
advanced acid-metabolism effect.

**Existing Spanish coverage**

None. Both nodes use the richer causal schema and are not currently consumable
by the enrichment deriver.

**Potentially enrichable SBA items**

- Approximate high-confidence coverage: **3**
- Additional plausible coverage: **1**
- Strong candidates: `wset3_426`, `wset3_510`, `wset3_372`
- Plausible candidate requiring careful review: `wset3_8`

The first three connect botrytis or noble-rot conditions to concentration,
morning mist/humidity, or sugar/acid effects. `wset3_8` concerns adding
botrytised Aszu berry paste; the existing concentration node is relevant, but
the question tests a Tokaji production practice rather than the concentration
mechanism directly.

**False-positive risk**

Medium. Botrytis can mean beneficial noble rot or harmful grey rot, and the
negative-polarity item `wset3_783` must remain excluded. Region-identification
items and disease-mitigation questions must not be absorbed into this domain.

**Match quality expectation**

High when the stem names botrytis or noble rot and the correct answer names
concentration or the climatic sequence. Medium for regional practices or
statements about acidity that oversimplify botrytis chemistry.

**Pedagogical value**

Very high. The domain supports a clear chain from climatic conditions through
skin perforation and water loss to sugar, flavour, glycerol, and aroma
concentration, while allowing the acid-reduction node to correct simplistic
"everything concentrates equally" reasoning.

### 3.5 Sparkling production mechanisms

**Existing causal nodes**

There is no existing node set covering the broad production sequence. The
closest nodes are:

- `CC_LEES_AGEING_AUTOLYSIS`
- `CC_AUTOLYSIS_AROMA_TEXTURE`

These explain only lees contact and autolysis. There are no direct existing
causal nodes for Charmat, secondary fermentation initiation, riddling,
disgorgement, dosage, pressure formation, or transfer method.

**Existing Spanish coverage**

None for the two overlapping nodes.

**Potentially enrichable SBA items**

- Broad sparkling topic surface: approximately **65** items
- Precision-standard independent coverage from current nodes: **0**
- Possible coverage through the lees/autolysis subset: **up to 3**

The large surface count is misleading. Most items concern geography,
varieties, labels, service, sweetness, or mechanisms for which no current
causal node exists.

**False-positive risk**

High. `Espumoso`, Champagne, Cava, and Prosecco are broad category terms, not
causal evidence. A broad sparkling matcher would produce topical rather than
explanatory matches.

**Match quality expectation**

Low as one domain. High only when restricted to the existing lees/autolysis
mechanism, in which case the work belongs under Lees ageing.

**Pedagogical value**

Very high in principle, but current causal knowledge is too narrow for a
precision-first Batch 3. This domain should wait until distinct production
mechanisms exist rather than using one generic sparkling chain.

### 3.6 Viticulture hazard mitigation

**Existing causal nodes**

- Direct: `CC_SPRING_FROST_TOPOGRAPHY`
- Adjacent: `HC_WATER_STRESS_CONCENTRATION`
- Adjacent: `HC_MARITIME_MODERATION`

Only the frost node directly models hazard exposure and site mitigation.
There are no direct existing nodes for hail, fungal-disease mitigation,
drought mitigation, excessive rain, or wind protection.

**Existing Spanish coverage**

All three listed nodes have Spanish layers. The frost node is structurally
compatible with the deriver, but the current trigger set does not produce a
full stem-plus-correct-answer match in the bank.

**Potentially enrichable SBA items**

- Approximate high-confidence coverage: **1**
- Primary candidate: `wset3_12`

The item links spring-frost risk to terrain slope, which is directly explained
by cold-air drainage and topography. Other hazard items concern damage,
disease, canopy management, or regional climate and are not supported by the
existing frost-topography node.

**False-positive risk**

High if hazards are grouped. Frost, hail, drought, rain, wind, and fungal
disease require different mechanisms and controls. Generic terms such as risk,
climate, disease, and canopy are unsafe matching signals.

**Match quality expectation**

High for explicit spring-frost plus slope/topography evidence. Low for a broad
hazard category.

**Pedagogical value**

High for viticulture decision-making because it links site conditions to crop
risk and mitigation. Current knowledge breadth, however, supports only a
narrow frost-topography slice.

## 4. Recommended Batch 3 priority order

1. **Botrytis concentration** - highest expected new coverage: 3 strong items,
   with a fourth plausible candidate; two complementary existing nodes and
   strong causal teaching value.
2. **Lees ageing** - approximately 3 strong sparkling-autolysis matches; high
   pedagogical value if kept strictly within the existing node scope.
3. **MLF** - only 1 clear item, but exceptionally high match quality and strong
   explanatory value.
4. **Viticulture hazard mitigation** - 1 strong frost-topography candidate;
   do not generalize the node to unrelated hazards.
5. **Bottle ageing** - 0-1 credible new item because the best-supported item is
   already enriched.
6. **Sparkling production mechanisms** - defer as a broad domain. Its apparent
   bank coverage is large, but current nodes support only the lees/autolysis
   subset already counted above.

**Recommendation:** Select **Botrytis concentration** for Batch 3 planning. It
offers the best combination of incremental coverage, existing causal knowledge,
expected match quality, and pedagogical value without loosening matcher
thresholds or reducing precision standards.

---

`safe_for_examiner = false`  
`examiner_scoring_allowed = false`
