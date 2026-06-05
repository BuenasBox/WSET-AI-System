# Open Response Semantic Review Batch 1

Phase: 4A.3.7.47
Scope: open-response semantic review for priority candidates 804, 817, 807, 809
Activation: inactive; no candidate, review, pipeline, frontend, or publication changes

This document is a human review aid only. It does not modify the source question bank, normalized candidates, review records, schemas, payloads, Tutor, Retrieval, Self-Eval, Golden baselines, snapshots, or frontend.

## Summary

| source_question_id | Current semantic risk | Recommendation |
|---|---|---|
| 804 | Over-broad soil-quality prompt; overlaps with 817; causal expectation narrower than stem. | MAJOR_EDIT |
| 817 | Better scoped than 804 but asks for three soil types with uneven evidence and one narrow chain. | MAJOR_EDIT |
| 807 | Very broad climate-extreme compensation prompt; many valid answer paths; quality-control overclaim risk. | MAJOR_EDIT |
| 809 | Useful compare/contrast idea, but "premium" and indigenous yeast risks need tighter boundaries. | MAJOR_EDIT |

## Shared Risks

- Corpus support is term-level chunk support, not a complete semantic ruling that every nuance in the stem is fully supported.
- Current `feedback_rubric` is generic formative concept coverage, not question-specific.
- The review records are structurally approved for internal review only; all candidates remain inactive.
- Soil questions 804 and 817 overlap strongly and should not both be activated without differentiation.
- Quality/premium language should be treated as conditional and style-dependent, not automatic improvement or official quality judgement.

## ID 804

### Candidate

- source_question_id: 804
- stem: Analice el impacto del tipo de suelo en el estilo y la calidad del vino.
- RA: RA1
- topic: suelo
- subtopic: drenaje
- difficulty: intermediate

### Grounding

- expected_concepts: suelo; drenaje; agua; retención; nutrientes; vigor; rendimiento; concentración; maduración; estilo; calidad; arcilla; grava; arena; RA1
- corpus_support: supported
- source_question_bank: `knowledge/question-bank/structured/wset3_questions.json`
- source_type: `WSET3_RA1_Banco_Preguntas_Bloque8.xlsx | Desarrollo`
- evidence_chunks:
  - `OFFICIAL_WSET_OF_W_5_2_5_THE_GROWING_ENVIRONMENT_001` - `5 The Growing Environment`; matched terms: suelo, drenaje, agua, nutrientes, maduración, estilo, arcilla, arena
  - `OFFICIAL_WSET_WINES_OF_THE_WORLD_8_1_43_SHERRY_001` - `43 Sherry`; matched terms: suelo, drenaje, agua, retención, nutrientes, rendimiento, maduración, estilo
  - `OFFICIAL_WSET_PRICE_OF_W_5_3_6_VINEYARD_MANAGEMENT_001` - `6 Vineyard Management`; matched terms: suelo, agua, nutrientes, rendimiento, concentración, maduración, estilo
- candidate optional_causal_chain: suelo -> drenaje -> vigor
- associated knowledge-map causal chain: `CC_SOIL_DRAINAGE_VINE_VIGOUR` is relevant to soil texture/composition -> drainage -> root depth/vigour -> concentration/quality. It does not cover every soil type or the full "quality" judgement in the stem.

### Semantic Review

1. Correctly formulated: Partially. The question is intelligible, but "tipo de suelo" and "calidad" make the scope too broad for an intermediate open response.
2. Ambiguity: High. It could invite geology, soil chemistry, water availability, nutrient status, heat retention, drainage, root depth, vigour, yield, and style all at once.
3. Multiple valid answers: High. A valid answer could focus on drainage, water retention, nutrient availability, heat retention, or specific soil examples without covering the expected chain.
4. Risk of exceeding WSET evidence: Moderate to high. The evidence supports soil, drainage, water, nutrients, maturation, yield, and style, but a broad claim that soil type directly determines wine quality risks overclaim.
5. expected_concepts sufficiency: Insufficient as a rubric target. It lists many terms but does not define which causal path is required or how to treat soil types differently.
6. Rubric adequacy: Not adequate yet. Generic concept coverage cannot distinguish a strong drainage-vigour answer from a broad but weak soil-quality answer.
7. Measurement fit: Weak in current form. It intends to measure RA1 causal reasoning about soil, but the stem may measure broad recall or speculative reasoning instead.

### Risks

- Strong overlap with ID 817.
- "Calidad" can be read as deterministic soil-quality causation.
- Gravel appears in expected concepts but is not strongly matched in the evidence chunks for this item.
- The formal causal chain only supports a narrower drainage/vigour path.

### Recommendation

MAJOR_EDIT

The item should be narrowed before any activation decision. It is not a reject because there is a valid RA1 training construct underneath it, but the current wording is too broad.

### Proposed Edit Only

Option A:

> Explique cómo el drenaje del suelo puede influir en el vigor de la vid y en el estilo del vino.

Option B, if keeping a quality angle:

> Explique cómo un suelo bien drenado puede limitar el vigor de la vid y contribuir potencialmente a uvas más concentradas.

Do not require all soil types in this item if ID 817 remains in the bank.

## ID 817

### Candidate

- source_question_id: 817
- stem: Explica el impacto de diferentes tipos de suelos (arena, arcilla, grava) en el vigor de la vid y cómo esto puede influir en el estilo del vino.
- RA: RA1
- topic: suelo
- subtopic: arena
- difficulty: intermediate

### Grounding

- expected_concepts: suelo; arena; arcilla; grava; drenaje; retención de agua; agua; calor; retención de calor; vigor; maduración; rendimiento; concentración; estilo; RA1
- corpus_support: supported
- source_question_bank: `knowledge/question-bank/structured/wset3_questions.json`
- source_type: `WSET3_RA1_Banco_Preguntas_TOTAL.xlsx | Abiertas`
- evidence_chunks:
  - `OFFICIAL_WSET_OF_W_5_2_5_THE_GROWING_ENVIRONMENT_001` - `5 The Growing Environment`; matched terms: suelo, arena, arcilla, drenaje, agua, calor, maduración, estilo
  - `OFFICIAL_WSET_PRICE_OF_W_5_3_6_VINEYARD_MANAGEMENT_001` - `6 Vineyard Management`; matched terms: suelo, agua, calor, maduración, rendimiento, concentración, estilo
  - `OFFICIAL_WSET_WINES_OF_THE_WORLD_8_1_43_SHERRY_001` - `43 Sherry`; matched terms: suelo, drenaje, agua, calor, maduración, rendimiento, estilo
- candidate optional_causal_chain: arena -> drenaje -> vigor
- associated knowledge-map causal chain: `CC_SOIL_DRAINAGE_VINE_VIGOUR` is relevant, especially for drainage/vigour. It includes gravel/grava and sandy soil trigger terms, but the current candidate chain starts only from sand and does not fully represent clay, gravel, heat retention, or water retention.

### Semantic Review

1. Correctly formulated: Partially. It is more bounded than 804 because it names arena, arcilla, and grava, but it still asks for several soil mechanisms in one intermediate item.
2. Ambiguity: Moderate. "Impacto" could mean drainage, water retention, heat retention, nutrient availability, vigour, yield, ripening, or concentration.
3. Multiple valid answers: High. Learners may answer one soil type deeply or compare all three superficially; both could be reasonable unless the rubric is explicit.
4. Risk of exceeding WSET evidence: Moderate. Sand and clay have direct matched support; gravel support is weaker in the recorded evidence for the candidate, though the knowledge-map chain contains gravel/grava triggers.
5. expected_concepts sufficiency: Partially sufficient as a concept list, insufficient as a reviewable rubric. It does not specify the minimum acceptable comparison among the three soils.
6. Rubric adequacy: Not adequate yet. A generic concept-presence rubric may unfairly penalize valid concise answers or reward term listing without causal linkage.
7. Measurement fit: Moderate. The question does measure soil-vigour-style reasoning, but only if the answer expectation distinguishes drainage and water/heat retention clearly.

### Risks

- Duplicates the conceptual territory of ID 804.
- Three named soils may be too much for one short open response unless the expected answer is explicitly comparative.
- The optional causal chain is only sand -> drainage -> vigour.
- Gravel evidence should be manually verified before being required.

### Recommendation

MAJOR_EDIT

Prefer keeping either a narrowed version of 817 or a narrowed version of 804, not both in overlapping form.

### Proposed Edit Only

Option A:

> Compare cómo suelos arenosos y arcillosos pueden afectar la disponibilidad de agua, el vigor de la vid y el estilo del vino.

Option B:

> Explique cómo el drenaje y la retención de agua del suelo pueden afectar el vigor de la vid y el estilo del vino.

If gravel remains, add a human-verified evidence note and make the rubric explicitly comparative across arena, arcilla, and grava.

## ID 807

### Candidate

- source_question_id: 807
- stem: Describe cómo las decisiones humanas en la viña pueden compensar las condiciones climáticas extremas y así mantener la calidad del vino.
- RA: RA1
- topic: decisiones humanas
- subtopic: clima extremo
- difficulty: distinction

### Grounding

- expected_concepts: decisiones humanas; gestión; viña; viñedo; riego; estrés hídrico; sequía; dosel; exposición; sombra; helada; granizo; vendimia; selección; maduración; equilibrio; calidad; clima extremo; RA1; gestión del viñedo
- corpus_support: supported
- source_question_bank: `knowledge/question-bank/structured/wset3_questions.json`
- source_type: `WSET3_RA1_Banco_Preguntas_TOTAL.xlsx | Abiertas`
- evidence_chunks:
  - `OFFICIAL_WSET_OF_W_5_2_5_THE_GROWING_ENVIRONMENT_001` - `5 The Growing Environment`; matched terms: riego, estrés hídrico, sequía, exposición, helada, granizo, vendimia, maduración
  - `OFFICIAL_WSET_PRICE_OF_W_5_3_6_VINEYARD_MANAGEMENT_001` - `6 Vineyard Management`; matched terms: riego, exposición, helada, granizo, vendimia, selección, maduración, equilibrio
  - `OFFICIAL_WSET_WINES_OF_THE_WORLD_6_11_22_GERMANY_001` - `22 Germany`; matched terms: estrés hídrico, exposición, helada, vendimia, maduración, equilibrio
- candidate optional_causal_chain: riego -> estrés hídrico -> maduración
- associated knowledge-map causal chain: no direct mapped chain found for the full item. `CC_SPRING_FROST_TOPOGRAPHY` is related to frost/topography and air drainage, but it does not represent the candidate's riego/estrés hídrico chain or the full set of extreme climate interventions.

### Semantic Review

1. Correctly formulated: Partially. The concept is valid, but the wording is too broad and implies a high degree of grower control over extreme conditions.
2. Ambiguity: High. "Condiciones climáticas extremas" can include drought, heat, frost, hail, excessive rain, wind, sunburn, and more; each requires different interventions.
3. Multiple valid answers: Very high. Answers could focus on irrigation, canopy shade, frost protection, hail nets, harvest timing, fruit selection, site choice, or yield management.
4. Risk of exceeding WSET evidence: High. The evidence supports many terms, but "compensar" and "mantener la calidad" may imply that human decisions can reliably offset extreme climate damage.
5. expected_concepts sufficiency: Insufficient. The list mixes hazards, interventions, outcomes, and broad quality terms without specifying which hazard-intervention pair is expected.
6. Rubric adequacy: Not adequate. A single generic causal-link check cannot fairly evaluate multiple possible climate hazards.
7. Measurement fit: Weak in current form. It intends to measure applied vineyard-management reasoning, but may instead reward broad lists of possible interventions.

### Risks

- Overclaim: "compensar" suggests complete mitigation rather than risk reduction.
- Quality framing is too absolute.
- One causal chain cannot cover drought, frost, hail, canopy, harvest, and selection.
- Distinction difficulty is plausible, but only with a constrained compare/explain prompt and a specific rubric.

### Recommendation

MAJOR_EDIT

The question should be narrowed to one or two climate risks with matching interventions, or split into separate items.

### Proposed Edit Only

Option A:

> Explique cómo el riego y el manejo del dosel pueden reducir los efectos de la sequía o el calor extremo sobre la maduración de la uva.

Option B:

> Describa dos decisiones de manejo del viñedo que pueden reducir el riesgo de pérdida de calidad ante sequía, helada o granizo.

Use "reducir el riesgo" or "limitar el impacto" rather than "compensar" or "mantener la calidad".

## ID 809

### Candidate

- source_question_id: 809
- stem: Compara las ventajas y desventajas del uso de levaduras seleccionadas frente a levaduras autóctonas en la producción de vinos premium.
- RA: RA1
- topic: levaduras seleccionadas
- subtopic: levaduras autóctonas
- difficulty: distinction

### Grounding

- expected_concepts: levaduras seleccionadas; seleccionadas; levaduras autóctonas; autóctonas; salvajes; fermentación; control; consistencia; predecible; variabilidad; complejidad; riesgo; parada fermentativa; aromas no deseados; calidad; premium; RA1; vino premium
- corpus_support: supported
- source_question_bank: `knowledge/question-bank/structured/wset3_questions.json`
- source_type: `WSET3_RA1_Banco_Preguntas_TOTAL.xlsx | Abiertas`
- evidence_chunks:
  - `OFFICIAL_WSET_PRICE_OF_W_5_3_6_VINEYARD_MANAGEMENT_001` - `6 Vineyard Management`; matched terms: autóctonas, salvajes, fermentación, control, riesgo, premium
  - `OFFICIAL_WSET_4_7_COMMON_ELEMENTS_IN_WINEMAKING_AND_MATURATION_001` - `7 Common Elements in Winemaking and Maturation`; matched terms: fermentación, control, complejidad, riesgo, premium
  - `OFFICIAL_WSET_W_5_5_8_WHITE_AND_SWEET_WINEMAKING_001` - `8 White and Sweet Winemaking`; matched terms: fermentación, control, complejidad, riesgo, premium
- candidate optional_causal_chain: levaduras seleccionadas -> control -> consistencia
- associated knowledge-map causal chain: no direct mapped chain found for selected versus indigenous yeast. Existing yeast-related chains are for flor, lees autolysis, and fortification/residual sugar, not this compare/contrast concept.

### Semantic Review

1. Correctly formulated: Partially. Compare/contrast is appropriate, but the "vinos premium" framing needs tighter control.
2. Ambiguity: Moderate to high. "Premium" can imply price, quality, style, brand positioning, artisan production, complexity, or risk tolerance.
3. Multiple valid answers: High. A valid answer could emphasize predictability and consistency for selected yeasts, or complexity and site/style expression for indigenous yeasts, with several possible tradeoffs.
4. Risk of exceeding WSET evidence: Moderate to high. The evidence supports fermentation/control/risk terms, but selected-versus-indigenous nuance is uneven and appears partly term-level.
5. expected_concepts sufficiency: Partially sufficient. It includes the key tradeoff terms, but needs a two-sided structure: selected yeast advantages/disadvantages and indigenous yeast advantages/disadvantages.
6. Rubric adequacy: Not adequate yet. Generic concept coverage cannot ensure balanced comparison or prevent simplistic "selected good / indigenous risky" framing.
7. Measurement fit: Moderate. The question can measure distinction-level winemaking tradeoff reasoning if rewritten with explicit accepted comparison axes.

### Risks

- "Premium" may invite unsupported assumptions that indigenous yeast is inherently more premium or that selected yeast is inherently lower quality.
- Term-level support for indigenous yeast risks needs human semantic confirmation.
- Current optional chain only covers selected yeast benefit, not indigenous yeast benefit or risk.
- Could overlap with ID 803 and ID 813 unless the purpose is explicitly two-sided comparison.

### Recommendation

MAJOR_EDIT

Keep the underlying compare/contrast construct, but rewrite and create a specific formative rubric before activation.

### Proposed Edit Only

Option A:

> Compare el uso de levaduras seleccionadas y levaduras autóctonas en fermentación, considerando control, consistencia, complejidad potencial y riesgos.

Option B:

> Explique una ventaja y una desventaja de las levaduras seleccionadas frente a las levaduras autóctonas en la elaboración de vino.

Avoid requiring "premium" unless the rubric explicitly frames it as style/market positioning rather than official quality.

## Batch-Level Recommendation

Do not activate any of the four candidates as currently written. All four should remain in human semantic review with `activation_status = inactive`.

Recommended handling:

- 804 and 817: decide whether to merge, split, or keep only one narrowed soil item.
- 807: split or narrow by climate hazard and intervention.
- 809: keep as a compare/contrast item only after removing or tightly defining the "premium" framing.

## Governance Check

No activation or publication action is proposed by this review. The source layer remains governed by:

- `safe_for_examiner = false`
- `examiner_scoring_allowed = false`
- `official_wset_question = false`
- `training_item_only = true`
- `uses_llm = false`
- `uses_api = false`
- `uses_embeddings = false`
- `uses_vector_db = false`
- `cloud_services_active = false`
