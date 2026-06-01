# Knowledge Map Manifest Reconciliation Audit

Phase: 4A.3.6.6

Status: docs-only reconciliation audit. No manifest, knowledge-map node, schema, parser, validator, test, retrieval, planner, SBA, or generator files were modified.

## Scope

Audited:

- `knowledge/knowledge-map/`
- `knowledge/knowledge-map/manifests/knowledge_map_manifest.json`
- `knowledge/knowledge-map/manifests/schemas/*.json`

The goal is to determine what a future reconciliation phase must do before any Diagnostic SBA, learner model, remediation routing, or open-response evaluator consumes the knowledge-map as authoritative.

## 1. Manifest Claims

Manifest path:

- `knowledge/knowledge-map/manifests/knowledge_map_manifest.json`

Top-level fields:

- `manifest_id`
- `manifest_name`
- `description`
- `build_date`
- `schema_version`
- `ingestion_status`
- `summary`
- `concepts`
- `misconceptions`
- `causal_chains`
- `relationships`
- `schemas`
- `pending_nodes`
- `_meta`

Manifest metadata:

- `manifest_id`: `WSET_AI_KNOWLEDGE_MAP_V1`
- `manifest_name`: `WSET-AI-System Knowledge Map — Phase 1 Manifest`
- `build_date`: `2026-05-13`
- `schema_version`: `1.0`
- `ingestion_status`: `draft`

Manifest summary claims:

| Type | Manifest summary | Manifest entries |
| --- | ---: | ---: |
| Topics | 0 | not populated |
| Concepts | 8 | 8 |
| Misconceptions | 13 | 13 |
| Causal chains | 17 | 17 |
| Relationships | 10 | 10 |
| Total nodes | 48 | 48 substantive registered nodes |
| Schemas | not in total | 5 |

Manifest-listed concept IDs:

- `C_ACIDITY`
- `C_TANNIN`
- `C_COOL_CLIMATE`
- `C_BOTRYTIS_CINEREA`
- `C_WHOLE_BUNCH_FERMENTATION`
- `C_CHAMPAGNE_LEES_AGEING`
- `C_OAK_INFLUENCE`
- `C_MALOLACTIC_CONVERSION`

Manifest-listed misconception IDs:

- `MC_ACIDITY_01`
- `MC_ACIDITY_02`
- `MC_TANNIN_01`
- `MC_TANNIN_02`
- `MC_COOL_CLIMATE_01`
- `MC_COOL_CLIMATE_02`
- `MC_BOTRYTIS_01`
- `MC_OAK_01`
- `MC_OAK_02`
- `MC_MLF_01`
- `MC_MLF_02`
- `MC_WHOLE_BUNCH_01`
- `MC_LEES_AGEING_01`

Manifest-listed causal-chain IDs:

- `CC_COOL_CLIMATE_ACIDITY`
- `CC_NOBLE_ROT_SUGAR_CONCENTRATION`
- `CC_MLF_ACIDITY`
- `CC_MLF_TEXTURE`
- `CC_MLF_DIACETYL`
- `CC_OAK_TANNIN`
- `CC_OAK_FLAVOUR`
- `CC_OAK_MICROOX`
- `CC_TANNIN_AGEABILITY`
- `CC_WHOLE_BUNCH_TANNIN`
- `CC_WHOLE_BUNCH_PH`
- `CC_LEES_AGEING_AUTOLYSIS`
- `CC_AUTOLYSIS_AROMA_TEXTURE`
- `CC_ACIDITY_AGEABILITY`
- `CC_COOL_CLIMATE_AROMA`
- `CC_COOL_CLIMATE_ALCOHOL`
- `CC_BOTRYTIS_ACIDITY_REDUCTION`

Manifest-listed relationship IDs:

- `R_COOL_CLIMATE__INCREASES__ACIDITY`
- `R_MALOLACTIC_CONVERSION__REDUCES__ACIDITY`
- `R_OAK_INFLUENCE__INCREASES__TANNIN`
- `R_BOTRYTIS_CINEREA__REDUCES__ACIDITY`
- `R_WHOLE_BUNCH_FERMENTATION__INCREASES__TANNIN`
- `R_WHOLE_BUNCH_FERMENTATION__REDUCES__ACIDITY`
- `R_ACIDITY__INFLUENCES__TANNIN`
- `R_CHAMPAGNE_LEES_AGEING__PRODUCES__AUTOLYTIC_AROMA`
- `R_COOL_CLIMATE__OFTEN_CONFUSED_WITH__UNDER_RIPE`
- `R_BOTRYTIS_CINEREA__CONTRASTS_WITH__GREY_ROT`

## 2. Actual Tree Counts

Actual lightweight files under `knowledge/knowledge-map/`:

| Area | JSON files | Markdown notes |
| --- | ---: | ---: |
| `concepts/` | 8 | 1 |
| `misconceptions/` | 20 | 1 |
| `causal-chains/` | 32 | 1 |
| `relationships/` | 10 | 1 |
| `manifests/` | 1 | 1 |
| `manifests/schemas/` | 5 | 0 |
| Other support directories | 0 | 7 |
| Total | 76 | 12 |

Substantive node counts:

| Type | Actual files | Manifest entries | Delta |
| --- | ---: | ---: | ---: |
| Concepts | 8 | 8 | 0 |
| Misconceptions | 20 | 13 | +7 |
| Causal chains | 32 | 17 | +15 |
| Relationships | 10 | 10 | 0 |
| Total substantive nodes | 70 | 48 | +22 |

Verdict: the manifest is stale.

## 3. Manifest vs Tree Diff

### Present In Tree But Missing From Manifest

Unregistered misconception nodes:

- `knowledge/knowledge-map/misconceptions/mc_ageing_improvement_01.json`
- `knowledge/knowledge-map/misconceptions/mc_alcohol_quality_01.json`
- `knowledge/knowledge-map/misconceptions/mc_cold_stabilisation_quality_01.json`
- `knowledge/knowledge-map/misconceptions/mc_complexity_length_01.json`
- `knowledge/knowledge-map/misconceptions/mc_oak_quality_01.json`
- `knowledge/knowledge-map/misconceptions/mc_residual_sugar_sweet_01.json`
- `knowledge/knowledge-map/misconceptions/mc_tannin_quality_02.json`

Unregistered causal-chain nodes:

- `knowledge/knowledge-map/causal-chains/cc_barrel_ageing_oak_character.json`
- `knowledge/knowledge-map/causal-chains/cc_bottle_ageing_sediment.json`
- `knowledge/knowledge-map/causal-chains/CC_DESTEMMING_TANNIN_STRUCTURE.json`
- `knowledge/knowledge-map/causal-chains/cc_flor_biological_ageing.json`
- `knowledge/knowledge-map/causal-chains/cc_fortification_residual_sugar.json`
- `knowledge/knowledge-map/causal-chains/cc_fractional_blending_consistency.json`
- `knowledge/knowledge-map/causal-chains/CC_MACERATION_EXTRACTION.json`
- `knowledge/knowledge-map/causal-chains/CC_MECHANICAL_HARVEST_OXIDATION.json`
- `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_HIGH.json`
- `knowledge/knowledge-map/causal-chains/CC_SAT_QUALITY_MEDIUM.json`
- `knowledge/knowledge-map/causal-chains/CC_SOIL_DRAINAGE_VINE_VIGOUR.json`
- `knowledge/knowledge-map/causal-chains/CC_SPRING_FROST_TOPOGRAPHY.json`
- `knowledge/knowledge-map/causal-chains/CC_SULPHITES_PRESERVATION.json`
- `knowledge/knowledge-map/causal-chains/cc_tannin_astringency.json`
- `knowledge/knowledge-map/causal-chains/cc_warm_climate_alcohol.json`

### Present In Manifest But Missing From Tree

None found.

### Duplicate IDs

No duplicate IDs found among actual nodes for:

- `concept_id`
- `misconception_id`
- `chain_id`
- `node_id`
- `relationship_id`

### Malformed IDs

No malformed IDs found using these patterns:

- `C_*` for concepts
- `MC_*` for misconceptions
- `CC_*` for causal chains
- `R_*__*__*` for relationships

### Files Without ID Fields

No substantive JSON node files were missing an ID field. Causal-chain IDs may appear as either `chain_id` or `node_id`.

### IDs That Do Not Match Filenames

Mostly acceptable abbreviations, but should be normalized or explicitly allowed in a future validator:

- `cc_noble_rot_concentration.json` has `CC_NOBLE_ROT_SUGAR_CONCENTRATION`
- `botrytis__contrasts_with__grey_rot.json` has `R_BOTRYTIS_CINEREA__CONTRASTS_WITH__GREY_ROT`
- `botrytis__reduces__acidity.json` has `R_BOTRYTIS_CINEREA__REDUCES__ACIDITY`
- `champagne_lees__produces__autolytic_aroma.json` has `R_CHAMPAGNE_LEES_AGEING__PRODUCES__AUTOLYTIC_AROMA`
- `cool_climate__often_confused_with__unripe.json` has `R_COOL_CLIMATE__OFTEN_CONFUSED_WITH__UNDER_RIPE`
- `mlf__reduces__acidity.json` has `R_MALOLACTIC_CONVERSION__REDUCES__ACIDITY`
- `whole_bunch__increases__tannin.json` has `R_WHOLE_BUNCH_FERMENTATION__INCREASES__TANNIN`
- `whole_bunch__reduces__acidity.json` has `R_WHOLE_BUNCH_FERMENTATION__REDUCES__ACIDITY`

These are not necessarily wrong, but future tooling must not assume filename stem equals ID.

## 4. Broken / Unresolved References

### Missing Concept References

The following referenced concepts do not exist as concept nodes:

- `C_AGEING_POTENTIAL`
- `C_ALCOHOL`
- `C_TARTARIC_ACID`
- `C_COMPLEXITY`
- `C_LENGTH`
- `C_OAK_AGEING`
- `C_RESIDUAL_SUGAR`

Affected nodes:

- `mc_ageing_improvement_01.json`
- `mc_alcohol_quality_01.json`
- `mc_cold_stabilisation_quality_01.json`
- `mc_complexity_length_01.json`
- `mc_oak_quality_01.json`
- `mc_residual_sugar_sweet_01.json`

### Unresolved Topic References

Many nodes reference topic IDs, but `knowledge/knowledge-map/topics/` has only `README.md` and no topic JSON nodes. Therefore topic references are unresolved by design or by incompletion.

Examples:

- `T_RA1_WINE_COMPONENTS`
- `T_RA1_CLIMATE_VITICULTURE`
- `T_RA1_SAT`
- `T_RA1_WINEMAKING`
- `T_RA1_WINEMAKING_WHITE`
- `T_RA1_WINEMAKING_RED`
- `T_RA1_WINEMAKING_AGEING`
- `T_RA1_VITICULTURE_HAZARDS`
- `T_RA2_GERMANY`
- `T_RA2_BORDEAUX_SWEET`
- `T_RA2_SPAIN`
- `T_RA3_SHERRY`
- `T_RA3_PORT`
- `T_RA3_CHAMPAGNE_PRODUCTION`

Risk: topic-aware consumers cannot rely on `related_topics` or `linked_topics` until topic nodes or a topic-ID registry exists.

## 5. Causal-Chain Schema Variant Audit

The causal-chain corpus has two schema families plus one hybrid node.

### Legacy / Manifest Schema

Required by `causal_chain.schema.json`:

- `chain_id`
- `starting_factor`
- `intermediate_steps`
- `final_outcome`

Observed common fields:

- `chain_id`
- `chain_name`
- `starting_factor`
- `intermediate_steps`
- `final_outcome`
- `examples`
- `related_exam_questions`
- `distinction_note`
- `complexity`
- `exam_relevance`
- `tutor_use`
- `examiner_use`
- `_meta`

Legacy-style nodes:

- `cc_acidity_ageability.json`
- `cc_autolysis_aroma_texture.json`
- `cc_botrytis_acidity_reduction.json`
- `cc_cool_climate_alcohol.json`
- `cc_cool_climate_aroma.json`
- `cc_lees_ageing_autolysis.json`
- `cc_mlf_acidity.json`
- `cc_mlf_diacetyl.json`
- `cc_noble_rot_concentration.json`
- `cc_oak_flavour.json`
- `cc_oak_microox.json`
- `cc_oak_tannin.json`
- `cc_tannin_ageability.json`
- `cc_whole_bunch_ph.json`
- `cc_whole_bunch_tannin.json`

Strength:

- Good cause/mechanism/effect structure.
- Good exam/SBA relevance via `related_exam_questions` and `exam_relevance`.

Weakness:

- Missing explicit `trigger_keywords`, `steps`, `safe_for_examiner`, `examiner_scoring_allowed`, and `governance`.
- SAT relevance is implicit, not fielded.
- Source references are generally absent.

### Governance / Retrieval Schema

Observed common fields:

- `node_type`
- `node_id`
- `topic`
- `trigger_keywords`
- `steps`
- `sat_relevance`
- `linked_misconceptions`
- `linked_topics`
- `agent_corpus`
- `safe_for_examiner`
- `examiner_scoring_allowed`
- `requires_human_review`
- `governance`
- `_meta`

Governance-style nodes:

- `cc_barrel_ageing_oak_character.json`
- `cc_bottle_ageing_sediment.json`
- `CC_DESTEMMING_TANNIN_STRUCTURE.json`
- `cc_flor_biological_ageing.json`
- `cc_fortification_residual_sugar.json`
- `cc_fractional_blending_consistency.json`
- `CC_MACERATION_EXTRACTION.json`
- `CC_MECHANICAL_HARVEST_OXIDATION.json`
- `cc_mlf_texture.json`
- `CC_SAT_QUALITY_HIGH.json`
- `CC_SAT_QUALITY_MEDIUM.json`
- `CC_SOIL_DRAINAGE_VINE_VIGOUR.json`
- `CC_SPRING_FROST_TOPOGRAPHY.json`
- `CC_SULPHITES_PRESERVATION.json`
- `cc_tannin_astringency.json`
- `cc_warm_climate_alcohol.json`

Strength:

- Good retrieval triggers and governance fields.
- Good SAT relevance field.
- Safer for runtime consumption because `safe_for_examiner` and `examiner_scoring_allowed` are explicit.

Weakness:

- Does not satisfy existing `causal_chain.schema.json`.
- Missing `chain_name`, `starting_factor`, `intermediate_steps`, `final_outcome`, `related_exam_questions`, and `exam_relevance`.
- Source references are generally absent.

### Hybrid Node

- `cc_cool_climate_acidity.json`

This node includes both legacy and governance fields:

- `chain_id`
- `node_id`
- `chain_name`
- `topic`
- `trigger_keywords`
- `steps`
- `starting_factor`
- `intermediate_steps`
- `final_outcome`
- `sat_relevance`
- `linked_misconceptions`
- `linked_topics`
- `examples`
- `related_exam_questions`
- `distinction_note`
- `complexity`
- `exam_relevance`
- `tutor_use`
- `examiner_use`
- `agent_corpus`
- `safe_for_examiner`
- `examiner_scoring_allowed`
- `requires_human_review`
- `governance`
- `_meta`

This is the best model for a future compatibility schema, but it should not be declared canonical until reviewed.

## 6. Misconception Node Readiness

Required by `misconception.schema.json`:

- `misconception_id`
- `misconception`
- `why_incorrect`
- `corrected_understanding`
- `related_topics`
- `severity`

Observed readiness:

- All 20 have an ID.
- All 20 have a misconception title/text.
- All 20 have correction content through `corrected_understanding` and/or `tutor_intervention`.
- All 20 are useful as diagnostic distractor sources because they contain misconception text, why it is wrong, and corrected understanding.
- All 20 have related concepts.
- 10 have explicit `detection_keywords`.
- None have explicit `related_causal_chains`.
- None have explicit top-level governance fields like `safe_for_examiner` or `examiner_scoring_allowed`.

Risk:

- The runtime misconception prepass can use them, but Diagnostic SBA should require additional enrichment before direct distractor use:
  - `distractor_role`
  - `diagnostic_error_type`
  - explicit source support
  - governance metadata
  - linked causal-chain IDs where appropriate

## 7. Concept And Relationship Node Audit

### Concepts

All 8 concepts include:

- `concept_id`
- `concept_name`
- `topic_id`
- `definition`
- `common_misconceptions`
- `distinction_insights`
- `cause_effect_links`
- `related_grapes`
- `related_regions`
- `related_wine_laws`
- `official_reference`
- `tutor_allowed`
- `examiner_allowed`
- `_meta`

Usefulness:

- Strong for SBA diagnosis.
- Strong for learner model concept mastery.
- Strong for remediation and retrieval expansion.

Risk:

- Some `topic_id` values may point to topic nodes that do not exist yet.
- `official_reference` exists, but future source grounding should still map to official chunks/Markdown.

### Relationships

All 10 relationships include:

- `relationship_id`
- `source_concept`
- `target_concept`
- `relationship_type`
- `strength`
- `conditions`
- `direction`
- `explanation`
- `exam_relevance`
- `tutor_use`
- `examiner_use`
- `_meta`

Cross-reference consistency:

- All relationship `source_concept` and `target_concept` references resolve to existing concept IDs.

Usefulness:

- High for diagnostic concept-differentiation.
- High for learner model adjacency and remediation routing.
- Medium for direct SBA generation; relationships are better used to check distractor ambiguity and concept similarity than to generate items by themselves.

## 8. Consumer Risk Analysis

| Consumer | Risk | Reason |
| --- | --- | --- |
| Retrieval sandbox | Medium | It scans actual directories, so it may see unregistered nodes. Mixed causal-chain schema can affect scoring/explanation consistency. |
| Misconception prepass | Medium | Uses actual misconception files, including unregistered nodes. Missing governance fields are tolerable now but risky for Diagnostic SBA. |
| Causal-chain matching | High | Mixed schemas mean a consumer expecting `chain_id` or `intermediate_steps` will miss governance-style nodes; a consumer expecting `node_id`/`steps` will miss legacy nodes. |
| SAT reasoner | Low | SAT reasoner mainly uses `knowledge/config/sat_observation_aliases.json`; knowledge-map SAT chains are supplementary. |
| Self-eval | Medium | Self-eval context/retrieval may indirectly use graph nodes; stale manifest can mislead audits, but runtime mostly reads directories. |
| Snapshots | Medium | Snapshot fixtures include knowledge-map match reasons; reconciliation may change retrieval context if consumers later switch manifest source. |
| Diagnostic SBA | High | Cannot safely consume graph-wide assets until manifest, schema variants, source support, and governance fields are reconciled. |
| Diagnostic outcome model | Medium | Misconception IDs are stable, but unregistered nodes and missing related causal chains weaken analytics. |
| Future learner model | High | Learner state needs stable concept/misconception/causal-chain IDs and registered relationships. Missing concept nodes and topic nodes are a problem. |
| PSL | Low/Medium | PSL is not a factual consumer yet, but future strategy decisions may use misconception/concept state; stale IDs could route poorly. |

## 9. SBA Readiness Classification

### Ready For Direct Diagnostic Use

Use only with current constraints, not as final generated items:

- 8 concept nodes
- 10 relationship nodes
- Registered legacy causal chains with complete cause/mechanism/effect fields

Reason:

- IDs are valid.
- Core fields are present.
- They are useful for reasoning and diagnosis.

Limit:

- Still need item-level source support and diagnostic item schema wrapping.

### Usable With Enrichment

- All 20 misconception nodes
- Governance-style causal-chain nodes
- Hybrid causal-chain node

Needed enrichment:

- manifest registration
- source support
- explicit Diagnostic SBA governance metadata
- related causal-chain links for misconceptions
- normalized causal-chain schema
- topic-node resolution

### Reference-Only For Now

- README files under empty/planned directories:
  - `topics/README.md`
  - `regions/README.md`
  - `grape-varieties/README.md`
  - `tasting/README.md`
  - `service/README.md`
  - `wine-laws/README.md`
  - `distinction-patterns/README.md`

Reason:

- They describe planned structure but are not substantive graph nodes.

### Unsafe / Incomplete For Direct SBA

- Any node with unresolved concept references:
  - `C_AGEING_POTENTIAL`
  - `C_ALCOHOL`
  - `C_TARTARIC_ACID`
  - `C_COMPLEXITY`
  - `C_LENGTH`
  - `C_OAK_AGEING`
  - `C_RESIDUAL_SUGAR`
- Any topic-linked workflow relying on `T_*` references before topic nodes or a topic registry exists.
- Any causal-chain-wide consumer that assumes one schema.

## 10. Reconciliation Plan

Recommended future sequence:

1. Manifest regeneration contract
   - Define whether manifest is authoritative, derived, or manually curated.
   - Define canonical sections for concepts, misconceptions, causal chains, relationships, schemas, and support-only README directories.
   - Define whether unregistered nodes should be registered or quarantined.

2. Manifest schema
   - Create a manifest schema before regenerating.
   - Required fields should include manifest metadata, generated timestamp, source tree root, node counts, registered file paths, ID fields, schema family, governance status, and unresolved-reference summary.

3. Causal-chain compatibility contract
   - Decide whether canonical future causal chains use:
     - legacy `chain_id` cause/mechanism/effect schema,
     - governance `node_id`/`steps` schema,
     - or a hybrid v2 schema.
   - Do not silently coerce; document field mappings.

4. Reference resolution contract
   - Define allowed unresolved references.
   - Either create topic nodes/registry or mark `T_*` references as external taxonomy references.
   - Decide whether missing concepts should become pending nodes or invalid references.

5. Manifest validator
   - Validate file existence.
   - Validate ID uniqueness.
   - Validate ID pattern.
   - Validate filename/ID relationship with explicit alias allowance.
   - Validate schema family.
   - Validate governance fields.
   - Validate broken references.

6. Consistency tests
   - Test manifest count equals actual node count.
   - Test every substantive node is registered.
   - Test no registered file is missing.
   - Test all relationship concept references resolve.
   - Test all misconception concept references resolve or are listed as pending.
   - Test all causal-chain linked misconceptions resolve.

7. Safe regeneration
   - Generate a candidate manifest to a temporary/report path first.
   - Human review the diff.
   - Only then replace `knowledge_map_manifest.json`.

8. Consumer regression tests
   - Run focused retrieval sandbox tests.
   - Run misconception prepass tests.
   - Run causal-chain/SAT tests.
   - Run snapshot regression or snapshot no-op checks if retrieval ranking changes.
   - Run diagnostic schema/validator tests only if Diagnostic SBA consumers are touched.

## 11. Recommended Next Phase

Phase 4A.3.6.7 - Knowledge Map Manifest Regeneration Contract.

This should still be docs-first. It should define the canonical manifest contract, causal-chain schema compatibility policy, unresolved-reference policy, and validator requirements before any manifest or node file is modified.

## Final Verdict

The knowledge-map is valuable and strategically central, but not yet ready to be treated as a clean authoritative graph. The manifest is stale, causal chains are split across schema families, topics are referenced but not represented as nodes, and several new misconception nodes point to concepts that do not yet exist. The next work should formalize the reconciliation contract before touching data.
