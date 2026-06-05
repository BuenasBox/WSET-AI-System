# Open Response Human Review Packet

Phase: 4A.3.7.46  
Scope: approved internal diagnostic open-response candidates only  
Candidate IDs: 798-817  
Activation: inactive; no learner-facing or cockpit exposure

This packet is a human review aid. It does not change candidate content, review records, schemas, payloads, Tutor, Retrieval, Self-Eval, governance, or activation state.

## Executive Summary

| Proposed decision | Count | IDs |
|---|---:|---|
| keep | 11 | 800, 801, 802, 806, 808, 811, 812, 813, 814, 815, 816 |
| minor_edit | 5 | 798, 799, 803, 805, 810 |
| major_edit | 4 | 804, 807, 809, 817 |
| reject | 0 | none |

Questions that appear closest to ready: 800, 801, 802, 806, 808, 811, 812, 813, 814, 815, 816.

Questions requiring minor edits mainly need tighter wording, reduced overclaim around "quality" or "commercial perception", or clearer expected answer boundaries.

Questions requiring major edits are not structurally invalid, but are too broad, semantically underconstrained, or overlapping enough that human review should decide whether to narrow, merge, or discard them.

Main gaps:

- Corpus support is term-level chunk support, not a full semantic ruling.
- Optional causal chains are plain-text chains, not mapped knowledge-map causal IDs.
- Feedback rubric is generic across all candidates and not yet question-specific.
- Some stems ask broad "quality", "premium", or "commercial perception" judgments that need careful non-examiner framing.
- Soil and water-stress coverage has redundancy: 804 overlaps 817; 810 overlaps 812.

Priority review order:

1. 804 and 817: overlapping soil questions; 817 has explicit sand/clay/gravel scope, while 804 is very broad.
2. 807: broad climate-extreme compensation stem with many possible hazards and interventions.
3. 809: selected vs indigenous yeasts in premium wine; source support is plausible but term-level and the "premium" framing needs control.
4. 810 and 812: duplicate stress-water concept pair; decide whether both are needed.
5. 798 and 805: commercial perception / quality-perception wording should be checked for overclaim.

## Common Review Constraints

- All included candidates have `review_status = approved` only for internal structural review.
- All included candidates have `activation_status = inactive`.
- The packet does not create official scoring, marks, model answers, pass/fail logic, or examiner authority.
- The feedback rubric remains formative only:
  - `concept_coverage`: expected concept presence
  - `causal_link`: formative causal link presence
  - `formative_feedback`: training guidance only
  - `needs_review`: derived from missing or partial concepts

## Candidate Review Notes

### ID 798

- source_question_id: 798
- stem: Discute cómo el uso de prácticas sostenibles en el viñedo puede influir en el precio del vino y en su percepción comercial.
- RA: RA1
- topic: sostenibilidad
- subtopic: precio
- difficulty: distinction
- expected_concepts: sostenibilidad; sostenible; certificación; orgánico; biodinámico; coste; costo; precio; mano de obra; rendimiento; diferenciación; percepción; consumidor; mercado; valor; RA1; coste de producción; percepción comercial
- optional_causal_chain: sostenibilidad -> coste -> precio
- corpus_support summary: supported. Evidence includes official chunks on Vineyard Management, Factors that Affect the Price of Wine, and Common Elements in Winemaking and Maturation, with support for sustainability, organic/biodynamic practices, costs, labour, yields, price, and perception.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: "percepción comercial" is broader than the strongest evidence terms; certification, sustainability costs, and consumer value may need a tighter expected-answer boundary.
- propuesta de decisión: minor_edit
- comentario breve: Keep the concept, but narrow the stem or review expectation so it asks for cost/price and market differentiation without implying unsupported universal commercial uplift.

### ID 799

- source_question_id: 799
- stem: Justifica el uso de la fermentación maloláctica en la producción de ciertos estilos de vino blanco y cómo contribuye a la calidad final.
- RA: RA1
- topic: fermentación maloláctica
- subtopic: vino blanco
- difficulty: distinction
- expected_concepts: fermentación maloláctica; maloláctica; ácido málico; ácido láctico; acidez; suave; suaviza; textura; cremosa; cremosidad; diacetilo; mantequilla; láctico; cuerpo; complejidad; calidad; estilo; RA1; vino blanco
- optional_causal_chain: maloláctica -> acidez -> textura
- corpus_support summary: supported. Evidence includes SAT, Common Elements in Winemaking and Maturation, and Sparkling Wine Production chunks matching malolactic fermentation, acidity, texture, body, complexity, and style.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: "ciertos estilos" and "calidad final" are open-ended; the answer expectation should avoid treating malolactic fermentation as inherently quality-positive in all white wines.
- propuesta de decisión: minor_edit
- comentario breve: Good training item if narrowed to style effects such as softer acidity, texture, dairy/butter notes, and suitability by style.

### ID 800

- source_question_id: 800
- stem: Explica cómo la altitud puede influir en el estilo de un vino tinto.
- RA: RA1
- topic: altitud
- subtopic: clima
- difficulty: intermediate
- expected_concepts: altitud; altura; temperatura; frío; fresco; rango diurno; oscilación térmica; maduración; madura; lenta; despacio; acidez; azúcar; alcohol; estilo; frescura; RA1; clima; estilo de vino tinto
- optional_causal_chain: altitud -> temperatura -> maduración
- corpus_support summary: supported. Evidence includes Growing Environment plus regional chunks for Northern Italy and Spain, matching altitude, temperature, ripening, acidity, sugar, alcohol, and style.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: low risk; human review should confirm that "vino tinto" does not require variety-specific examples.
- propuesta de decisión: keep
- comentario breve: The causal chain is clear and the stem is appropriately bounded for formative open response.

### ID 801

- source_question_id: 801
- stem: Explique cómo la orientación y la pendiente del viñedo pueden afectar la maduración de la uva.
- RA: RA1
- topic: orientación
- subtopic: pendiente
- difficulty: intermediate
- expected_concepts: orientación; pendiente; ladera; exposición; sol; solar; insolación; drenaje; agua; maduración; madura; azúcar; acidez; sombra; temperatura; RA1; exposición solar
- optional_causal_chain: orientación -> exposición -> maduración
- corpus_support summary: supported. Evidence includes Growing Environment, Germany, and California chunks matching orientation, slope, exposure, sun, drainage, water, ripening, sugar, acidity, and temperature.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: low risk; drainage and water effects should remain secondary to orientation/slope and exposure.
- propuesta de decisión: keep
- comentario breve: Strong causal fit and suitable intermediate scope.

### ID 802

- source_question_id: 802
- stem: Describa cómo las prácticas de manejo en la bodega pueden reducir el riesgo de oxidación en vinos blancos.
- RA: RA1
- topic: oxidación
- subtopic: vino blanco
- difficulty: intermediate
- expected_concepts: oxidación; oxígeno; proteger; protección; sulfuroso; SO2; inerte; gas inerte; temperatura; frío; prensado; depósito; aromas; fruta; frescura; color; pardeamiento; RA1; vino blanco; bodega; manejo del oxígeno
- optional_causal_chain: oxígeno -> oxidación -> aromas
- corpus_support summary: supported. Evidence includes Common Elements in Winemaking and Maturation, SAT, and Sherry chunks matching oxidation, oxygen, sulfur dioxide, inert handling, temperature, aromas, and colour.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: some evidence is broad and includes Sherry; the reviewed answer boundary should focus on white-wine oxygen protection practices.
- propuesta de decisión: keep
- comentario breve: Formatively useful and adequately bounded if the rubric keeps examples practical and non-exhaustive.

### ID 803

- source_question_id: 803
- stem: Explique la influencia de la elección de levaduras en el perfil sensorial del vino.
- RA: RA1
- topic: levaduras
- subtopic: fermentación
- difficulty: intermediate
- expected_concepts: levadura; levaduras; fermentación; aromas; ésteres; perfil sensorial; sensorial; levadura seleccionada; seleccionada; control; predecible; estilo; fruta; compuestos aromáticos; RA1
- optional_causal_chain: levadura -> fermentación -> aromas
- corpus_support summary: supported. Evidence includes Common Elements in Winemaking and Maturation plus Germany and Sherry regional chunks matching yeast, fermentation, aromas, selected yeast, control, and style.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: "elección de levaduras" can include selected, ambient, neutral, aromatic, and spoilage dimensions; the stem may invite broader answers than the current concepts cover.
- propuesta de decisión: minor_edit
- comentario breve: Keep after clarifying whether the expected focus is selected yeast predictability/aroma production or a broader selected-versus-ambient comparison.

### ID 804

- source_question_id: 804
- stem: Analice el impacto del tipo de suelo en el estilo y la calidad del vino.
- RA: RA1
- topic: suelo
- subtopic: drenaje
- difficulty: intermediate
- expected_concepts: suelo; drenaje; agua; retención; nutrientes; vigor; rendimiento; concentración; maduración; estilo; calidad; arcilla; grava; arena; RA1
- optional_causal_chain: suelo -> drenaje -> vigor
- corpus_support summary: supported. Evidence includes Growing Environment, Sherry, and Vineyard Management chunks matching soil, drainage, water, nutrients, maturation, yield, concentration, and style.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: stem is very broad; "calidad" invites overclaim; overlaps strongly with ID 817; expected concepts include several soil types but the causal chain is only drainage/vigor.
- propuesta de decisión: major_edit
- comentario breve: Best handled by narrowing to one soil property, such as drainage or water retention, or merging intent with ID 817.

### ID 805

- source_question_id: 805
- stem: Expón cómo la elección del tipo de roble (americano vs francés) puede afectar el perfil sensorial y la percepción de calidad en vinos tintos.
- RA: RA1
- topic: roble
- subtopic: roble americano
- difficulty: distinction
- expected_concepts: roble; americano; francés; vainilla; coco; dulce; especias; cedro; tostado; tanino; integración; perfil sensorial; coste; costo; calidad; complejidad; nuevo; RA1; roble americano; roble francés
- optional_causal_chain: roble americano -> vainilla -> perfil
- corpus_support summary: supported. Evidence includes Common Elements in Winemaking and Maturation, Spain, and Red/Rosé Winemaking chunks matching oak type, vanilla, spices, toast, tannin, cost, and complexity.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: "percepción de calidad" may overstate the sensory evidence; American vs French oak effects depend on age, toast, size, and integration.
- propuesta de decisión: minor_edit
- comentario breve: Strong item if reframed around sensory profile, cost, and stylistic intention rather than generic quality perception.

### ID 806

- source_question_id: 806
- stem: Describa dos técnicas de manejo del dosel (canopy management) y sus beneficios.
- RA: RA1
- topic: manejo del dosel
- subtopic: técnicas de viñedo
- difficulty: intermediate
- expected_concepts: manejo del dosel; dosel; canopy; deshojado; hojas; posicionamiento de brotes; brotes; exposición; sol; maduración; aireación; circulación de aire; enfermedad; hongos; sombra; racimos; RA1; técnicas de viñedo; sanidad de la uva
- optional_causal_chain: deshojado -> exposición -> maduración
- corpus_support summary: supported. Evidence includes Vineyard Management, Growing Environment, and New Zealand chunks matching canopy management, shoots, exposure, sun, ripening, air circulation, disease, and fungi.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: low risk; the rubric should accept more than two valid techniques where concept coverage is adequate.
- propuesta de decisión: keep
- comentario breve: Clear scope, practical answer shape, and good formative fit.

### ID 807

- source_question_id: 807
- stem: Describe cómo las decisiones humanas en la viña pueden compensar las condiciones climáticas extremas y así mantener la calidad del vino.
- RA: RA1
- topic: decisiones humanas
- subtopic: clima extremo
- difficulty: distinction
- expected_concepts: decisiones humanas; gestión; viña; viñedo; riego; estrés hídrico; sequía; dosel; exposición; sombra; helada; granizo; vendimia; selección; maduración; equilibrio; calidad; clima extremo; RA1; gestión del viñedo
- optional_causal_chain: riego -> estrés hídrico -> maduración
- corpus_support summary: supported. Evidence includes Growing Environment, Vineyard Management, and Germany chunks matching irrigation, water stress, drought, exposure, frost, hail, harvest, selection, ripening, and balance.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: very broad hazard set; "compensar" and "mantener la calidad" may imply more control than growers actually have; one causal chain cannot cover drought, frost, hail, canopy, and harvest decisions together.
- propuesta de decisión: major_edit
- comentario breve: Narrow to one or two climate risks and matching interventions before any activation decision.

### ID 808

- source_question_id: 808
- stem: Explica por qué la densidad de plantación es un factor clave en la gestión del viñedo y cómo afecta el estilo y costo del vino producido.
- RA: RA1
- topic: densidad de plantación
- subtopic: competencia
- difficulty: distinction
- expected_concepts: densidad de plantación; densidad; plantación; competencia; vigor; rendimiento; producción; cosecha; concentración; uva; estilo; coste; costo; mano de obra; mecanización; precio; RA1
- optional_causal_chain: densidad -> competencia -> vigor
- corpus_support summary: supported. Evidence includes Vineyard Management, Factors that Affect the Price of Wine, and Common Elements in Winemaking and Maturation, matching density, planting, competition, yield, concentration, style, cost, labour, mechanisation, and price.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: moderate complexity, but the concept chain is coherent; human review should ensure both style and cost are expected, not one or the other.
- propuesta de decisión: keep
- comentario breve: Good distinction-level item with clear viticulture and price linkage.

### ID 809

- source_question_id: 809
- stem: Compara las ventajas y desventajas del uso de levaduras seleccionadas frente a levaduras autóctonas en la producción de vinos premium.
- RA: RA1
- topic: levaduras seleccionadas
- subtopic: levaduras autóctonas
- difficulty: distinction
- expected_concepts: levaduras seleccionadas; seleccionadas; levaduras autóctonas; autóctonas; salvajes; fermentación; control; consistencia; predecible; variabilidad; complejidad; riesgo; parada fermentativa; aromas no deseados; calidad; premium; RA1; vino premium
- optional_causal_chain: levaduras seleccionadas -> control -> consistencia
- corpus_support summary: supported. Evidence includes Vineyard Management, Common Elements in Winemaking and Maturation, and White/Sweet Winemaking chunks matching fermentation, control, complexity, risk, and premium; selected/autochthonous matching is term-level and uneven.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: "premium" framing is broad; support for indigenous yeast risk is plausible but not yet semantically audited; the contrast requires a two-sided rubric, not just one causal chain.
- propuesta de decisión: major_edit
- comentario breve: Rework into a controlled compare/contrast item with explicit accepted advantages, disadvantages, and non-scoring limits.

### ID 810

- source_question_id: 810
- stem: Evalúa las consecuencias del estrés hídrico moderado en viñedos de alta calidad y su impacto en el precio del vino.
- RA: RA1
- topic: estrés hídrico
- subtopic: calidad
- difficulty: distinction
- expected_concepts: estrés hídrico; agua; moderado; baya; bayas pequeñas; concentración; piel; rendimiento; coste; costo; precio; calidad; valor; maduración; azúcar; fenoles; RA1
- optional_causal_chain: estrés hídrico -> baya -> concentración
- corpus_support summary: supported. Evidence includes Vineyard Management, White/Sweet Winemaking, and Common Elements in Winemaking and Maturation, matching water, berry size, concentration, yield, cost, price, ripening, and sugar.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: overlaps with ID 812; price/value impact needs careful framing because lower yield and higher concentration do not automatically guarantee higher price.
- propuesta de decisión: minor_edit
- comentario breve: Keep if differentiated from ID 812 as the advanced price/yield/concentration version.

### ID 811

- source_question_id: 811
- stem: Describe cómo la latitud y la altitud interactúan para influir en el estilo del vino en una región de clima cálido.
- RA: RA1
- topic: latitud
- subtopic: altitud
- difficulty: intermediate
- expected_concepts: latitud; altitud; altura; clima cálido; temperatura; calor; maduración; rápida; acidez; rango diurno; oscilación térmica; frescura; alcohol; estilo; RA1
- optional_causal_chain: latitud -> temperatura -> maduración
- corpus_support summary: supported. Evidence includes Growing Environment, Australia, and Northern Italy chunks matching latitude, altitude, warm climate, temperature, heat, ripening, acidity, alcohol, and style.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: low to moderate risk; "interactúan" may be too ambitious if the expected answer only contrasts warming/cooling effects.
- propuesta de decisión: keep
- comentario breve: Suitable if the formative expectation accepts a clear temperature-ripening-style explanation.

### ID 812

- source_question_id: 812
- stem: Explica cómo el estrés hídrico moderado puede influir en la calidad del vino.
- RA: RA1
- topic: estrés hídrico
- subtopic: calidad
- difficulty: intermediate
- expected_concepts: estrés hídrico; agua; moderado; vigor; crecimiento vegetativo; baya; bayas pequeñas; concentración; maduración; rendimiento; calidad; azúcar; fenoles; RA1
- optional_causal_chain: estrés hídrico -> vigor -> concentración
- corpus_support summary: supported. Evidence includes Growing Environment, Vineyard Management, and California chunks matching water stress, moderate stress, berry, concentration, ripening, yield, and sugar.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: overlaps with ID 810 but is simpler; "calidad" should be framed as potential contribution through concentration and ripening balance, not automatic improvement.
- propuesta de decisión: keep
- comentario breve: Keep as the intermediate concept item if ID 810 remains the price-focused advanced version.

### ID 813

- source_question_id: 813
- stem: Menciona un riesgo enológico del uso de levaduras autóctonas.
- RA: RA1
- topic: levaduras autóctonas
- subtopic: riesgo enológico
- difficulty: foundational
- expected_concepts: levaduras autóctonas; autóctonas; salvajes; fermentación; riesgo; parada fermentativa; lenta; impredecible; aromas no deseados; defectos; control; calidad; RA1; riesgo enológico
- optional_causal_chain: levaduras autóctonas -> riesgo
- corpus_support summary: supported. Evidence includes Vineyard Management, Common Elements in Winemaking and Maturation, and Alsace chunks matching indigenous/wild yeast terms, fermentation, risk, defects, and control.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: low risk; human review should allow any valid single risk and avoid requiring every expected concept.
- propuesta de decisión: keep
- comentario breve: Clear foundational short-answer item.

### ID 814

- source_question_id: 814
- stem: Justifica por qué un viticultor utilizaría poda en invierno.
- RA: RA1
- topic: poda de invierno
- subtopic: rendimiento
- difficulty: foundational
- expected_concepts: poda; poda de invierno; invierno; yemas; brotes; rendimiento; vigor; equilibrio; maduración; calidad; uva; vid; RA1; equilibrio de la vid
- optional_causal_chain: poda -> yemas -> rendimiento
- corpus_support summary: supported. Evidence includes Vineyard Management, The Vine, and Growing Environment chunks matching winter pruning, buds, shoots, yield, balance, and ripening.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: low risk; answer expectation should distinguish winter pruning from summer canopy work.
- propuesta de decisión: keep
- comentario breve: Strong foundational causality and concise scope.

### ID 815

- source_question_id: 815
- stem: Describe un beneficio técnico de la fermentación en acero inoxidable.
- RA: RA1
- topic: acero inoxidable
- subtopic: fermentación
- difficulty: foundational
- expected_concepts: acero inoxidable; inoxidable; temperatura; control de temperatura; fermentación; inerte; aromas primarios; fruta; frescura; limpio; oxígeno; sabor; RA1; estilo fresco
- optional_causal_chain: acero inoxidable -> temperatura -> aromas
- corpus_support summary: supported. Evidence includes Red/Rosé Winemaking, Common Elements in Winemaking and Maturation, and White/Sweet Winemaking chunks matching stainless steel, temperature control, fermentation, inert vessels, primary aromas, and oxygen.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: low risk; should accept either temperature control or inertness/freshness as valid benefits.
- propuesta de decisión: keep
- comentario breve: Clear, bounded, and appropriate for foundational diagnostic use.

### ID 816

- source_question_id: 816
- stem: Analiza los efectos de la maceración prolongada en la vinificación de vinos tintos desde el punto de vista del estilo y calidad final.
- RA: RA1
- topic: maceración prolongada
- subtopic: vino tinto
- difficulty: distinction
- expected_concepts: maceración prolongada; maceración; extracción; color; tanino; antocianos; fenoles; estructura; cuerpo; envejecimiento; guarda; astringencia; amargor; equilibrio; calidad; RA1; vino tinto; estilo
- optional_causal_chain: maceración -> extracción -> tanino
- corpus_support summary: supported. Evidence includes SAT, Red/Rosé Winemaking, and Loire Valley chunks matching maceration, extraction, colour, tannin, body, ageing, astringency, bitterness, balance, and style.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: moderate but acceptable; "calidad final" should be conditional on balance and style, not treated as automatic.
- propuesta de decisión: keep
- comentario breve: Keep with human-reviewed expectation that includes both benefits and risks of over-extraction.

### ID 817

- source_question_id: 817
- stem: Explica el impacto de diferentes tipos de suelos (arena, arcilla, grava) en el vigor de la vid y cómo esto puede influir en el estilo del vino.
- RA: RA1
- topic: suelo
- subtopic: arena
- difficulty: intermediate
- expected_concepts: suelo; arena; arcilla; grava; drenaje; retención de agua; agua; calor; retención de calor; vigor; maduración; rendimiento; concentración; estilo; RA1
- optional_causal_chain: arena -> drenaje -> vigor
- corpus_support summary: supported. Evidence includes Growing Environment, Vineyard Management, and Sherry chunks matching soil, sand, clay, drainage, water, heat, maturation, yield, concentration, and style; explicit gravel support is weaker in the matched terms.
- feedback_rubric: generic formative concept coverage plus causal link presence; no scoring or examiner use.
- riesgos detectados: overlaps with ID 804; asks for three soil types but the optional chain covers only sand/drainage/vigor; gravel may need stronger evidence verification.
- propuesta de decisión: major_edit
- comentario breve: Narrow to drainage/water-retention comparison or split into smaller items before activation.

## Governance Check

No activation or publication action is proposed by this packet. The source layer remains governed by:

- `safe_for_examiner = false`
- `examiner_scoring_allowed = false`
- `official_wset_question = false`
- `training_item_only = true`
- `uses_llm = false`
- `uses_api = false`
- `uses_embeddings = false`
- `uses_vector_db = false`
- `cloud_services_active = false`

