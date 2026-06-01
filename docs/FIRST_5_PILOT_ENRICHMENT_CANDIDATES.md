# First 5 Pilot Enrichment Candidates

Phase: 4A.3.7.8

Status: selection and enrichment-feasibility report only. This document does
not create converted items, a pilot bank, generated questions, or migrated
question-bank records.

Source bank:

- `knowledge/question-bank/structured/wset3_questions.json`

Adapter:

- `tools/question_generation/structured_question_bank_adapter.py`

Selected source question IDs:

- `1`
- `2`
- `12`
- `13`
- `17`

## 1. Selection Method

The five candidates were selected from the structured bank using the current
adapter and the Phase 4A.3.7.8 constraints.

All selected records satisfy:

- `classification_status = adapter_ready_clean_pilot`
- `question_type = theory`
- exact A-D options present
- all option texts non-empty
- no duplicate normalized option text
- valid A-D `correct_answer_letter`
- non-empty `correct_answer_text`
- selected option text matches `correct_answer_text`
- `expected_topics` present
- `expected_reasoning_type` present
- `safe_for_examiner = false`

Preference was given to records with explicit `expected_causal_links`,
meaningful keywords, clear topic boundaries, and likely support from
knowledge-map causal-chain nodes plus official Markdown/chunk grounding.

## 2. Important Boundary

These are enrichment candidates, not enriched diagnostic SBA items.

No item in this report has validated `source_support`, option diagnostics,
source-grounded rationales, remediation, or final governance audit. Every item
still requires enrichment and validation before it can become a diagnostic SBA
item.

Official WSET Markdown or official chunks may be used only for grounding. They
must not be used for wording imitation or examiner authority.

## 3. Candidate 1

### Source

- `source_question_id`: `1`
- Original question: `¿Qué rol juega la 'flor' en la crianza biológica del Jerez?`
- Correct answer letter: `C`
- Correct answer text: `Protege al vino del oxígeno y desarrolla sabores únicos`
- `expected_topics`: `flor`, `jerez`, `biological ageing`
- `expected_causal_links`: `flor -> oxygen protection -> biological ageing`
- `expected_keywords`: `flor`, `crianza biológica`, `oxígeno`, `acetaldehído`
- `expected_reasoning_type`: `theory_foundation`

Options summary:

- `A`: Incrementa la acidez volátil
- `B`: Reduce la concentración alcohólica
- `C`: Protege al vino del oxígeno y desarrolla sabores únicos
- `D`: Oxida completamente el vino

### Enrichment Feasibility

- Adapter skeleton readiness: structurally clean, requires enrichment.
- Likely source-support candidates:
  - `knowledge/knowledge-map/causal-chains/cc_flor_biological_ageing.json`
  - `OFFICIAL_WSET_WINES_OF_THE_WORLD_8_1_43_SHERRY_001`
  - `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- Likely misconception candidates:
  - none confirmed from current misconception nodes; use null unless a future evidence pass finds a defensible node.
- Likely causal-chain candidates:
  - `CC_FLOR_BIOLOGICAL_AGEING`
- Likely SAT relevance:
  - possible structure/aroma-style relevance through biological-ageing character, but not enough to attach SAT metadata automatically.
- Likely diagnostic roles:
  - `A`: `causal_confusion`
  - `B`: `scope_error`
  - `C`: `correct`
  - `D`: `causal_confusion`
- Enrichment gaps remaining:
  - source chunk confirmation
  - source-grounded correct rationale
  - distractor rationales
  - diagnostic role evidence per distractor
  - remediation target
- Human review needed: yes
- Risk level: medium
- Recommendation: `enrich_next`

## 4. Candidate 2

### Source

- `source_question_id`: `2`
- Original question: `¿Qué método se usa para detener la fermentación en el vino de Oporto?`
- Correct answer letter: `C`
- Correct answer text: `Adición de aguardiente vínico`
- `expected_topics`: `port`, `fortification`, `fermentation`
- `expected_causal_links`: `fortification -> yeast stops -> residual sugar`
- `expected_keywords`: `aguardiente`, `fortificación`, `fermentación`, `azúcar residual`
- `expected_reasoning_type`: `theory_foundation`

Options summary:

- `A`: Crianza en roble americano
- `B`: Uso de crianza larga
- `C`: Adición de aguardiente vínico
- `D`: Secado de uvas al sol

### Enrichment Feasibility

- Adapter skeleton readiness: structurally clean, requires enrichment.
- Likely source-support candidates:
  - `knowledge/knowledge-map/causal-chains/cc_fortification_residual_sugar.json`
  - `OFFICIAL_WSET_WINES_OF_THE_WORLD_8_2_44_PORT_001`
  - `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-2_44_port.md`
- Likely misconception candidates:
  - `MC_RESIDUAL_SUGAR_SWEET_01` may be relevant to residual sugar only if a distractor rationale explicitly targets residual-sugar misunderstanding. Do not attach automatically.
- Likely causal-chain candidates:
  - `CC_FORTIFICATION_RESIDUAL_SUGAR`
- Likely SAT relevance:
  - possible sweetness relevance because residual sugar is involved, but this item is primarily production-method reasoning.
- Likely diagnostic roles:
  - `A`: `process_confusion`
  - `B`: `process_confusion`
  - `C`: `correct`
  - `D`: `regional_confusion`
- Enrichment gaps remaining:
  - source chunk confirmation
  - correct rationale grounded in fortification and fermentation halt
  - distractor rationales distinguishing maturation, ageing, drying, and fortification
  - remediation target
- Human review needed: yes
- Risk level: low-medium
- Recommendation: `enrich_next`

## 5. Candidate 12

### Source

- `source_question_id`: `12`
- Original question: `¿Qué factor natural tiene mayor influencia en el riesgo de heladas primaverales?`
- Correct answer letter: `C`
- Correct answer text: `Pendiente del terreno`
- `expected_topics`: `heladas primaverales`, `topografía`, `viticultura`
- `expected_causal_links`: `aire frío -> puntos bajos -> riesgo de heladas primaverales`
- `expected_keywords`: `topografía`, `aire frío`, `heladas primaverales`, `drenaje del aire frío`
- `expected_reasoning_type`: `theory_foundation`

Options summary:

- `A`: Exposición al sol
- `B`: Altitud
- `C`: Pendiente del terreno
- `D`: Latitud

### Enrichment Feasibility

- Adapter skeleton readiness: structurally clean, requires enrichment.
- Likely source-support candidates:
  - `knowledge/knowledge-map/causal-chains/CC_SPRING_FROST_TOPOGRAPHY.json`
  - `OFFICIAL_WSET_OF_W_5_2_5_THE_GROWING_ENVIRONMENT_001`
  - `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md`
  - `knowledge/wine-with-jimmy/chunk-ready/Viticulture_Exam_Prep_WSET_Level_3_Sample_Questions.chunks.jsonl`
- Likely misconception candidates:
  - none confirmed; possible future misconception around cold-air pooling should remain null until a node exists.
- Likely causal-chain candidates:
  - `CC_SPRING_FROST_TOPOGRAPHY`
- Likely SAT relevance:
  - none; this is viticulture risk reasoning, not SAT observation.
- Likely diagnostic roles:
  - `A`: `partial_reasoning`
  - `B`: `partial_reasoning`
  - `C`: `correct`
  - `D`: `scope_error`
- Enrichment gaps remaining:
  - source chunk confirmation
  - rationale that explains why slope/topography is the best answer
  - distractor rationales for sun exposure, altitude, and latitude
  - remediation route to vineyard topography/frost risk
- Human review needed: yes
- Risk level: low-medium
- Recommendation: `enrich_next`

## 6. Candidate 13

### Source

- `source_question_id`: `13`
- Original question: `¿Qué elemento del suelo influye más directamente en el drenaje del viñedo?`
- Correct answer letter: `C`
- Correct answer text: `Estructura arenosa`
- `expected_topics`: `textura del suelo`, `drenaje`, `vigor de la vid`
- `expected_causal_links`: `textura del suelo -> retención de agua -> vigor de la vid`
- `expected_keywords`: `textura del suelo`, `drenaje`, `raíces`, `concentración`
- `expected_reasoning_type`: `theory_foundation`

Options summary:

- `A`: Contenido de arcilla
- `B`: Presencia de piedra caliza
- `C`: Estructura arenosa
- `D`: Materia orgánica

### Enrichment Feasibility

- Adapter skeleton readiness: structurally clean, requires enrichment.
- Likely source-support candidates:
  - `knowledge/knowledge-map/causal-chains/CC_SOIL_DRAINAGE_VINE_VIGOUR.json`
  - `OFFICIAL_WSET_OF_W_5_2_5_THE_GROWING_ENVIRONMENT_001`
  - `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md`
  - `knowledge/wine-with-jimmy/chunk-ready/WSET_Level_3_Wines_-_Understanding_the_Growing_Environment_Soils_Part_1.chunks.jsonl`
- Likely misconception candidates:
  - none confirmed; do not invent a soil-drainage misconception ID.
- Likely causal-chain candidates:
  - `CC_SOIL_DRAINAGE_VINE_VIGOUR`
- Likely SAT relevance:
  - none; this is vineyard/soil reasoning, not SAT observation.
- Likely diagnostic roles:
  - `A`: `near_neighbor_confusion`
  - `B`: `terminology_confusion`
  - `C`: `correct`
  - `D`: `partial_reasoning`
- Enrichment gaps remaining:
  - confirmation that the selected wording is sufficiently supported and not over-specific
  - source-grounded rationale for sandy structure vs clay/limestone/organic matter
  - remediation target to soil texture/drainage
- Human review needed: yes
- Risk level: medium
- Recommendation: `enrich_next`

## 7. Candidate 17

### Source

- `source_question_id`: `17`
- Original question: `¿Cuál es el propósito principal del despalillado antes de la fermentación?`
- Correct answer letter: `B`
- Correct answer text: `Evitar la extracción de taninos verdes`
- `expected_topics`: `despalillado`, `fermentación`, `estructura tánica`
- `expected_causal_links`: `raspones -> taninos verdes -> estructura`
- `expected_keywords`: `despalillado`, `raspones`, `taninos verdes`, `astringencia`
- `expected_reasoning_type`: `theory_foundation`

Options summary:

- `A`: Reducir el nivel de azúcar
- `B`: Evitar la extracción de taninos verdes
- `C`: Estimular la fermentación maloláctica
- `D`: Mejorar la retención aromática

### Enrichment Feasibility

- Adapter skeleton readiness: structurally clean, requires enrichment.
- Likely source-support candidates:
  - `knowledge/knowledge-map/causal-chains/CC_DESTEMMING_TANNIN_STRUCTURE.json`
  - `OFFICIAL_WSET_4_7_COMMON_ELEMENTS_IN_WINEMAKING_AND_MATURATION_001`
  - `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md`
  - `knowledge/wine-with-jimmy/chunk-ready/Understanding_Red_Wine_Making_for_WSET_Level_3.chunks.jsonl`
- Likely misconception candidates:
  - `MC_TANNIN_01` and `MC_TANNIN_02` are adjacent but not direct matches. Do not attach unless a future rationale explicitly concerns tannin/astringency confusion.
- Likely causal-chain candidates:
  - `CC_DESTEMMING_TANNIN_STRUCTURE`
- Likely SAT relevance:
  - possible tannin/astringency relevance through SAT alias `tannin`; this should remain tentative until evidence is attached.
- Likely diagnostic roles:
  - `A`: `process_confusion`
  - `B`: `correct`
  - `C`: `process_confusion`
  - `D`: `partial_reasoning`
- Enrichment gaps remaining:
  - source chunk confirmation
  - rationale distinguishing destemming from sugar, MLF, and aroma-retention claims
  - decision on whether tannin SAT relevance is in scope
  - remediation target to destemming/tannin extraction
- Human review needed: yes
- Risk level: low-medium
- Recommendation: `enrich_next`

## 8. Cross-Candidate Summary

| ID | Topic family | Risk | Human review | Recommendation |
| --- | --- | --- | --- | --- |
| `1` | Sherry flor and biological ageing | Medium | Yes | `enrich_next` |
| `2` | Port fortification and fermentation halt | Low-medium | Yes | `enrich_next` |
| `12` | Spring frost and topography | Low-medium | Yes | `enrich_next` |
| `13` | Soil texture and drainage | Medium | Yes | `enrich_next` |
| `17` | Destemming and green tannins | Low-medium | Yes | `enrich_next` |

All five are suitable for a first enrichment draft attempt, but none should
skip human review. The biggest remaining risk is unsupported rationale: source
support candidates exist, but the exact source chunks and distractor
rationales still need to be attached and validated.

## 9. Likely Enrichment Sources

Knowledge-map causal chains:

- `CC_FLOR_BIOLOGICAL_AGEING`
- `CC_FORTIFICATION_RESIDUAL_SUGAR`
- `CC_SPRING_FROST_TOPOGRAPHY`
- `CC_SOIL_DRAINAGE_VINE_VIGOUR`
- `CC_DESTEMMING_TANNIN_STRUCTURE`

Official grounding candidates:

- `knowledge/official-wset/study-guide/official-chunks/official_wset_chunks.jsonl`
- `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-2_44_port.md`
- `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md`
- `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-4_7_common_elements_in_winemaking_and_maturation.md`

Pedagogical support candidates:

- `knowledge/wine-with-jimmy/chunk-ready/Viticulture_Exam_Prep_WSET_Level_3_Sample_Questions.chunks.jsonl`
- `knowledge/wine-with-jimmy/chunk-ready/WSET_L3_Understanding_Growing_Environment_Problems_Short_Written_Question_Part_1.chunks.jsonl`
- `knowledge/wine-with-jimmy/chunk-ready/WSET_Level_3_Wines_-_Understanding_the_Growing_Environment_Soils_Part_1.chunks.jsonl`
- `knowledge/wine-with-jimmy/chunk-ready/Understanding_Red_Wine_Making_for_WSET_Level_3.chunks.jsonl`

SAT/config candidates:

- `knowledge/config/sat_observation_aliases.json`
- `knowledge/config/domain_expansions.json`

## 10. Readiness Verdict

These five candidates are ready for the next phase: enrichment drafts.

They are not ready for a converted bank, generated bank, practice runtime, or
frontend use.

Next recommended phase:

- Phase 4A.3.7.9 - First 5 Enrichment Drafts
