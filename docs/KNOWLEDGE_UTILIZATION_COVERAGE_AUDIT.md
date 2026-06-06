# Knowledge Utilization Coverage Audit

Phase: 4A.3.8.2 — Reduced Scope

Status: evidence-only audit. No code modified. No question bank modified. No dashboard modified. No deployment triggered. No promotion, generation, or activation performed.

## Scope

This document covers only the four gaps not addressed by prior documentation:

1. Misconception Coverage — which misconception nodes are referenced by SBA items
2. Causal Chain Coverage — which causal chain nodes are referenced by SBA items
3. Wine With Jimmy Utilization — which WWJ chunks appear as source support
4. Cross-Asset Utilization Rate — Tier 1 and Tier 2 assets vs actual diagnostic consumers

The following are explicitly excluded because they are covered by prior phases:

- Corpus verification → `docs/FULL_BANK_CORPUS_VERIFICATION_SUMMARY.md` (Phase 4A.3.7.31)
- Asset inventory → `docs/KNOWLEDGE_ASSET_INVENTORY_AND_AUDIT.md` (Phase 4A.3.6.5)
- Knowledge map manifest reconciliation → `docs/KNOWLEDGE_MAP_MANIFEST_RECONCILIATION_AUDIT.md` (Phase 4A.3.6.6)
- Generation readiness → `docs/GOLD_BANK_ACTIVATION_READINESS.md` (Phase 4A.3.7.33A)

## Method

All evidence is derived from local read-only inspection of existing repository files. No LLM generation, no embeddings, no external API, no vector DB, no corpus modification.

Sources inspected:

- `knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json` (127 KB, 5 items)
- `knowledge/question-bank/diagnostic_sba/drafts/gold_bank_activation_drafts.json` (187 KB)
- `knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json`
- `knowledge/question-bank/diagnostic_sba/reviews/gold_bank_activation_review_records.json`
- `frontend/diagnostic-sba/preguntas.json` (36 active items, production payload)
- `knowledge/enrichment/diagnostic_outcome.schema.json`
- `knowledge/wine-with-jimmy/enrichment-ready/` (directory listing)
- `knowledge/wine-with-jimmy/reports/` (directory listing)
- `docs/KNOWLEDGE_MAP_MANIFEST_RECONCILIATION_AUDIT.md` (node ID lists, reused)
- `docs/KNOWLEDGE_ASSET_INVENTORY_AND_AUDIT.md` (Tier rankings, reused)
- `docs/GOLD_BANK_ACTIVATION_READINESS.md` (active item list, reused)

## Key Schema Finding

The `diagnostic_outcome_v1` schema defines `misconception_id` and `causal_chain_id` as nullable fields (`nullableSafeString`) under the `source_trace` object. Both fields can be:

- A valid ID string referencing a node in the knowledge graph, or
- `null` — meaning the item has no explicit linkage to a misconception or causal chain node.

The active production payload (`preguntas.json`) uses `diagnostic_sba_item_v1` schema for item display and `diagnostic_outcome_v1` for outcome tracing. The linkage fields are structurally present but their values determine utilization.

## Section 1 — Misconception Coverage

### 1.1 Node Inventory

Total misconception nodes: **20**

| Node ID | Registration | Coverage in Drafts | Coverage in Production |
| --- | --- | --- | --- |
| MC_ACIDITY_01 | Registered | YES | NO |
| MC_ACIDITY_02 | Registered | NO | NO |
| MC_TANNIN_01 | Registered | YES | NO |
| MC_TANNIN_02 | Registered | YES | NO |
| MC_COOL_CLIMATE_01 | Registered | YES | NO |
| MC_COOL_CLIMATE_02 | Registered | YES | NO |
| MC_BOTRYTIS_01 | Registered | YES | NO |
| MC_OAK_01 | Registered | NO | NO |
| MC_OAK_02 | Registered | NO | NO |
| MC_MLF_01 | Registered | NO | NO |
| MC_MLF_02 | Registered | NO | NO |
| MC_WHOLE_BUNCH_01 | Registered | NO | NO |
| MC_LEES_AGEING_01 | Registered | NO | NO |
| MC_RESIDUAL_SUGAR_SWEET_01 | Unregistered | YES | NO |
| MC_AGEING_IMPROVEMENT_01 | Unregistered | YES | NO |
| MC_TANNIN_QUALITY_02 | Unregistered | YES | NO |
| MC_ALCOHOL_QUALITY_01 | Unregistered | NO | NO |
| MC_COLD_STABILISATION_QUALITY_01 | Unregistered | NO | NO |
| MC_COMPLEXITY_LENGTH_01 | Unregistered | NO | NO |
| MC_OAK_QUALITY_01 | Unregistered | NO | NO |

### 1.2 Coverage Summary

| Layer | Count | Percent |
| --- | ---: | ---: |
| Total MC nodes | 20 | 100% |
| Registered | 13 | 65% |
| Unregistered (not in manifest) | 7 | 35% |
| Referenced in enrichment drafts (5 items) | 9 | 45% |
| Referenced in production payload (36 items) | 0 | 0% |
| Referenced in Open Response bank | 0 | 0% (no OR bank exists) |
| Not referenced in any SBA context | 11 | 55% |

### 1.3 Context: What "Referenced in Drafts" Means

The `first_5_enrichment_drafts.json` contains 5 items with full MC/CC linkage. These are the most fully elaborated items in the system. The remaining items in `gold_bank_activation_drafts.json` have `misconception_id: null` — the distractor_role field uses the text value `"misconception"` without pointing to a specific MC node ID.

This means: even within the draft/enrichment pipeline, only 5 items have explicit misconception linkage. The remaining 31 items in the draft pool and all 36 production items have no knowledge-graph MC linkage at all.

### 1.4 Zero-Reference Nodes

The following 11 MC nodes have no reference in any SBA item (draft or production):

- MC_ACIDITY_02 — second acidity misconception, registered
- MC_OAK_01 — oak influence misconception, registered
- MC_OAK_02 — oak influence second variant, registered
- MC_MLF_01 — malolactic conversion misconception, registered
- MC_MLF_02 — MLF second variant, registered
- MC_WHOLE_BUNCH_01 — whole bunch fermentation, registered
- MC_LEES_AGEING_01 — lees ageing misconception, registered
- MC_ALCOHOL_QUALITY_01 — alcohol-quality misconception, unregistered
- MC_COLD_STABILISATION_QUALITY_01 — cold stabilisation, unregistered
- MC_COMPLEXITY_LENGTH_01 — complexity and length confusion, unregistered
- MC_OAK_QUALITY_01 — oak and quality misconception, unregistered

Seven of the eleven zero-reference nodes are registered in the manifest, meaning the system knows they exist but no item has been enriched to link to them.

## Section 2 — Causal Chain Coverage

### 2.1 Node Inventory

Total causal chain nodes: **32** (17 registered, 15 unregistered)

| Node ID | Registration | Referenced in Drafts | Referenced in Production |
| --- | --- | --- | --- |
| CC_COOL_CLIMATE_ACIDITY | Registered | YES | NO |
| CC_NOBLE_ROT_SUGAR_CONCENTRATION | Registered | YES | NO |
| CC_MLF_ACIDITY | Registered | NO | NO |
| CC_MLF_TEXTURE | Registered | NO | NO |
| CC_MLF_DIACETYL | Registered | NO | NO |
| CC_OAK_TANNIN | Registered | NO | NO |
| CC_OAK_FLAVOUR | Registered | NO | NO |
| CC_OAK_MICROOX | Registered | NO | NO |
| CC_TANNIN_AGEABILITY | Registered | YES | NO |
| CC_WHOLE_BUNCH_TANNIN | Registered | NO | NO |
| CC_WHOLE_BUNCH_PH | Registered | NO | NO |
| CC_LEES_AGEING_AUTOLYSIS | Registered | NO | NO |
| CC_AUTOLYSIS_AROMA_TEXTURE | Registered | YES | NO |
| CC_ACIDITY_AGEABILITY | Registered | YES | NO |
| CC_COOL_CLIMATE_AROMA | Registered | NO | NO |
| CC_COOL_CLIMATE_ALCOHOL | Registered | YES | NO |
| CC_BOTRYTIS_ACIDITY_REDUCTION | Registered | NO | NO |
| CC_FLOR_BIOLOGICAL_AGEING | Unregistered | YES | NO |
| CC_FORTIFICATION_RESIDUAL_SUGAR | Unregistered | YES | NO |
| CC_SPRING_FROST_TOPOGRAPHY | Unregistered | YES | NO |
| CC_SOIL_DRAINAGE_VINE_VIGOUR | Unregistered | YES | NO |
| CC_DESTEMMING_TANNIN_STRUCTURE | Unregistered | YES | NO |
| CC_MACERATION_EXTRACTION | Unregistered | YES | NO |
| CC_FRACTIONAL_BLENDING_CONSISTENCY | Unregistered | YES | NO |
| CC_BOTTLE_AGEING_SEDIMENT | Unregistered | YES | NO |
| CC_BARREL_AGEING_OAK_CHARACTER | Unregistered | NO | NO |
| CC_MECHANICAL_HARVEST_OXIDATION | Unregistered | NO | NO |
| CC_SAT_QUALITY_HIGH | Unregistered | NO | NO |
| CC_SAT_QUALITY_MEDIUM | Unregistered | NO | NO |
| CC_SULPHITES_PRESERVATION | Unregistered | NO | NO |
| CC_TANNIN_ASTRINGENCY | Unregistered | NO | NO |
| CC_WARM_CLIMATE_ALCOHOL | Unregistered | NO | NO |

### 2.2 Coverage Summary

| Layer | Count | Percent |
| --- | ---: | ---: |
| Total CC nodes | 32 | 100% |
| Registered in manifest | 17 | 53% |
| Unregistered | 15 | 47% |
| Referenced in enrichment drafts (5 items) | 14 | 44% |
| Referenced in production payload (36 items) | 0 | 0% |
| Referenced in Open Response bank | 0 | 0% (no OR bank exists) |
| Not referenced in any SBA context | 18 | 56% |

### 2.3 Schema Fragmentation and Coverage Interaction

Of the 14 CC nodes referenced in drafts, 8 are unregistered governance-schema nodes. Of the 11 registered legacy-schema nodes not referenced in drafts, all 11 remain unused in item linkage. This creates an inversion: the newer unregistered nodes were selected for item enrichment because they better describe the causal logic of the enriched items, while many older registered nodes remain available but unused.

### 2.4 Ranking by Diagnostic Relevance (Referenced Nodes)

Nodes referenced in enrichment drafts, ordered by estimated SBA diagnostic priority:

| Rank | Node ID | Topic area | Manifest |
| ---: | --- | --- | --- |
| 1 | CC_TANNIN_AGEABILITY | Tannin and wine ageing | Registered |
| 2 | CC_ACIDITY_AGEABILITY | Acidity and wine ageing | Registered |
| 3 | CC_COOL_CLIMATE_ACIDITY | Cool climate and acidity | Registered |
| 4 | CC_AUTOLYSIS_AROMA_TEXTURE | Lees autolysis, sparkling | Registered |
| 5 | CC_COOL_CLIMATE_ALCOHOL | Cool climate and alcohol | Registered |
| 6 | CC_NOBLE_ROT_SUGAR_CONCENTRATION | Botrytis and sweetness | Registered |
| 7 | CC_FLOR_BIOLOGICAL_AGEING | Sherry flor and biological ageing | Unregistered |
| 8 | CC_FORTIFICATION_RESIDUAL_SUGAR | Port fortification and sugar | Unregistered |
| 9 | CC_DESTEMMING_TANNIN_STRUCTURE | Destemming and tannin | Unregistered |
| 10 | CC_MACERATION_EXTRACTION | Maceration and extraction | Unregistered |
| 11 | CC_FRACTIONAL_BLENDING_CONSISTENCY | Solera system | Unregistered |
| 12 | CC_SPRING_FROST_TOPOGRAPHY | Frost risk and site | Unregistered |
| 13 | CC_SOIL_DRAINAGE_VINE_VIGOUR | Soil drainage and vigour | Unregistered |
| 14 | CC_BOTTLE_AGEING_SEDIMENT | Bottle ageing and sediment | Unregistered |

### 2.5 Zero-Reference Nodes

18 CC nodes have no reference in any SBA context:

Registered (11): CC_MLF_ACIDITY, CC_MLF_TEXTURE, CC_MLF_DIACETYL, CC_OAK_TANNIN, CC_OAK_FLAVOUR, CC_OAK_MICROOX, CC_WHOLE_BUNCH_TANNIN, CC_WHOLE_BUNCH_PH, CC_LEES_AGEING_AUTOLYSIS, CC_COOL_CLIMATE_AROMA, CC_BOTRYTIS_ACIDITY_REDUCTION

Unregistered (7): CC_BARREL_AGEING_OAK_CHARACTER, CC_MECHANICAL_HARVEST_OXIDATION, CC_SAT_QUALITY_HIGH, CC_SAT_QUALITY_MEDIUM, CC_SULPHITES_PRESERVATION, CC_TANNIN_ASTRINGENCY, CC_WARM_CLIMATE_ALCOHOL

The MLF cluster (3 chains: CC_MLF_ACIDITY, CC_MLF_TEXTURE, CC_MLF_DIACETYL) and the Oak cluster (3 chains: CC_OAK_TANNIN, CC_OAK_FLAVOUR, CC_OAK_MICROOX) are the most significant gaps given their centrality to the WSET L3 curriculum. All six are registered in the manifest and have zero linkage to any SBA item.

## Section 3 — Wine With Jimmy Utilization

### 3.1 Corpus State

| Asset | Location | Count | Status |
| --- | --- | ---: | --- |
| Clean transcript Markdown | `knowledge/wine-with-jimmy/clean/` | 30 files | Exists |
| Chunk-ready JSONL files | `knowledge/wine-with-jimmy/chunk-ready/` | 30 files | Exists |
| Chunk-ready rows | across 30 JSONL files | 333 rows | Exists |
| Video-level enrichment metadata | `knowledge/wine-with-jimmy/enrichment-ready/` | ≥5 files | Partial (in progress) |
| Cleaning reports | `knowledge/wine-with-jimmy/reports/` | 28+ files | Exists |
| Golden tutor chunk candidates | prior: `manual-import/reports/golden_tutor_chunk_candidates.jsonl` | 166 rows (prior audit) | Reorganized — prior path not found |
| Index of discovered videos | `knowledge/wine-with-jimmy/index/videos_discovered.jsonl` | 377 entries | Exists |

Note: the `manual-import/reports/` directory no longer exists at its documented path. The repo was reorganized. The `enrichment-ready/` directory now holds per-video enrichment metadata but not the consolidated golden candidate list. Any future phase that references the 166 golden candidates must first locate the canonical current path of this file.

### 3.2 Utilization in SBA Items

| Scope | WWJ chunks as source_support | Official WSET as source_support |
| --- | ---: | ---: |
| Active production items (preguntas.json, 36 items) | 0 | 0 (fields null) |
| Enrichment drafts (5 items) | 0 | all 5 use official-wset only |
| Gold activation drafts (remaining items) | 0 | not extracted (source_support not sampled) |
| Open Response bank | 0 | 0 (bank does not exist) |

Evidence: targeted search for `wine-with-jimmy`, `wwj`, and `chunk_id` patterns in `frontend/diagnostic-sba/` and `knowledge/question-bank/` returned 0 results. Source_support fields in `first_5_enrichment_drafts.json` exclusively reference `official_wset` / `official-wset` source types.

### 3.3 WWJ Utilization Rate

- 333 chunk-ready rows: **0% utilized** in any SBA item
- 166 golden candidates (prior count): **0% utilized** in any SBA item
- 5+ enrichment-ready video metadata files: **0% linked** to any item source_support

The WWJ corpus is available and indexed. The enrichment-ready directory shows active preparation of video-level enrichment metadata. But as of this audit, no SBA item — active or in draft — uses a WWJ chunk as explicit source_support.

### 3.4 Utilization Opportunities (Evidence Only)

The prior asset audit (KNOWLEDGE_ASSET_INVENTORY_AND_AUDIT.md) identified WWJ material as high value for misconception remediation, worked-answer examples, answer-structure coaching, and SAT explanations. The specific gap types where WWJ content could contribute:

| Gap type | Relevant WWJ content type |
| --- | --- |
| Items with distractor_role = misconception but null source_support | Misconception-correction worked examples from exam_strategy and theory_explanation transcripts |
| SAT-adjacent items with no pedagogical grounding | SAT coaching and tasting practice transcripts |
| Items in storage/service domain with weak official corpus grounding | Service and presentation transcripts |
| Future Open Response bank | Worked-answer style and exam strategy transcripts |

These are opportunities, not activations. No changes made here.

## Section 4 — Cross-Asset Utilization Rate

### 4.1 Definition

**Utilized**: at least one active SBA item, enrichment draft, or production-grade test references this asset as a direct input (source_support, misconception_id, causal_chain_id, schema consumer, or retrieval evidence).

**Partially utilized**: referenced in tests, tools, or retrieval infrastructure but not yet in any active item payload.

**Not utilized**: present in repository, correctly catalogued, but with zero references in any item-level or diagnostic-level context.

### 4.2 Tier 1 Assets

| Asset | Path | Utilization | Consumer |
| --- | --- | --- | --- |
| Official WSET chunks (`official_wset_chunks.jsonl`) | `knowledge/official-wset/study-guide/official-chunks/` | PARTIALLY UTILIZED | source_support in 5 enrichment draft items; 0 in production |
| Structured question bank (`wset3_questions.json`, 616 items) | `knowledge/question-bank/structured/` | UTILIZED | 36 items exported to active preguntas.json |
| Knowledge-map graph (concepts, misconceptions, causal chains) | `knowledge/knowledge-map/` | PARTIALLY UTILIZED | MC/CC IDs linked in 5 draft items only; 0 in production |
| WWJ chunk-ready corpus (333 chunks) | `knowledge/wine-with-jimmy/chunk-ready/` | NOT UTILIZED | 0 item references in any SBA context |
| Canonical terms master dictionary | `knowledge/enrichment/wset_master_dictionary/` | PARTIALLY UTILIZED | retrieval sandbox, transcript cleaning, tests — not in item metadata |

| Tier 1 status | Count | Percent |
| --- | ---: | ---: |
| Fully utilized (active items + production) | 1 | 20% |
| Partially utilized (drafts, tools, or tests only) | 3 | 60% |
| Not utilized in any item context | 1 | 20% |

### 4.3 Tier 2 Assets

| Asset | Path | Utilization | Consumer |
| --- | --- | --- | --- |
| Official WSET Markdown (`wset_markdown/`) | `knowledge/official-wset/study-guide/wset_markdown/` | PARTIALLY UTILIZED | source for official chunks; no direct item reference |
| Golden tutor chunk candidates (166 rows) | reorganized from `manual-import/reports/` | NOT UTILIZED | 0 item references; file path changed |
| SAT observation aliases | `knowledge/config/sat_observation_aliases.json` | UTILIZED | SAT reasoner, answer builder, active tests |
| Domain expansions | `knowledge/config/domain_expansions.json` | UTILIZED | retrieval sandbox, integration tests |
| Self-eval artifacts (1,229 files) | `knowledge/self-eval/` | UTILIZED | learner tracing, regression evidence, test calibration |
| Tutor snapshot fixtures (77 files) | `tests/fixtures/tutor_snapshots/` | UTILIZED | regression tests, baseline validation |
| Learning objectives JSONL | `knowledge/official-wset/study-guide/artifacts/study_guide_learning_objectives.jsonl` | NOT UTILIZED | catalogued but no active item or tool consumer found |

| Tier 2 status | Count | Percent |
| --- | ---: | ---: |
| Fully utilized | 4 | 57% |
| Partially utilized | 1 | 14% |
| Not utilized in item context | 2 | 29% |

### 4.4 Aggregate Utilization Summary

| Tier | Total assets | Utilized | Partial | Not utilized |
| --- | ---: | ---: | ---: | ---: |
| Tier 1 | 5 | 1 (20%) | 3 (60%) | 1 (20%) |
| Tier 2 | 7 | 4 (57%) | 1 (14%) | 2 (29%) |
| Combined | 12 | 5 (42%) | 4 (33%) | 3 (25%) |

The three not-utilized assets are: WWJ chunk-ready corpus (Tier 1), golden tutor chunk candidates (Tier 2, path reorganized), and learning objectives JSONL (Tier 2).

## Section 5 — Knowledge Utilization Flow

```
KNOWLEDGE EXISTING
  Knowledge-map nodes:   20 misconceptions  |  32 causal chains
  WWJ corpus:            333 chunks         |  ~166 golden candidates
  Official corpus:       52 chunks          |  52 Markdown files
  Structured bank:       616 questions

        ↓

KNOWLEDGE UTILIZED (in any SBA context)
  Misconceptions:        9 of 20  (45%)  — enrichment drafts only, not production
  Causal chains:         14 of 32 (44%)  — enrichment drafts only, not production
  Official WSET chunks:  used in 5 draft items as source_support
  WWJ chunks:            0 of 333 (0%)
  Structured bank:       36 of 616 items exported (6%)

        ↓

KNOWLEDGE IN PRODUCTION (active preguntas.json)
  Misconceptions:        0 of 20  (0%)   — all null in active payload
  Causal chains:         0 of 32  (0%)   — all null in active payload
  WWJ source support:    0 of 333 (0%)
  Official source support: 0 in production (null for all 36 items)
  Question items active: 36 of 616 (6%)

        ↓

KNOWLEDGE DESAPROVECHADO (unused in all SBA contexts)
  Misconceptions:        11 of 20 nodes never linked to any item
  Causal chains:         18 of 32 nodes never linked to any item
  WWJ corpus:            333 chunks / ~166 golden candidates — zero utilization
  Learning objectives:   38 JSONL entries — no item consumer
  Structured bank:       580 of 616 questions not exported to SBA (94%)

        ↓

OPORTUNIDADES (evidence only — no activation here)
  Highest-gap MC nodes:  MLF cluster (MC_MLF_01, MC_MLF_02), Oak cluster
                         (MC_OAK_01, MC_OAK_02), MC_WHOLE_BUNCH_01,
                         MC_LEES_AGEING_01 — 6 registered nodes with 0 linkage
  Highest-gap CC nodes:  MLF cluster (CC_MLF_ACIDITY, CC_MLF_TEXTURE,
                         CC_MLF_DIACETYL), Oak cluster (CC_OAK_TANNIN,
                         CC_OAK_FLAVOUR, CC_OAK_MICROOX) — all registered,
                         none linked, high WSET L3 exam relevance
  WWJ opportunity:       333 chunks ready for source_support enrichment in
                         misconception remediation and SAT-adjacent items
  Production gap:        All 36 active items have null MC/CC/source linkage;
                         5 enrichment drafts exist but not yet promoted to
                         production
```

## Section 6 — Findings Requiring Attention Before Next Phase

Observational findings only. No action taken here.

### 6.1 Production-Draft Divergence

The 5 enrichment drafts in `knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json` contain fully linked MC IDs, CC IDs, and official WSET source_support. The same items in the production `preguntas.json` have null values for all three fields. There is no evidence these enrichments have been promoted to any active payload.

This divergence is not a defect in this phase — enrichment and production promotion are separate pipeline stages — but it is quantitatively documented here for the first time.

### 6.2 Gold Activation Drafts Without Knowledge Graph Linkage

The `gold_bank_activation_drafts.json` contains items with `distractor_role: "misconception"` but `misconception_id: null`. This confirms that the majority of the bank has structural support for graph linkage (the field exists in the schema) but no actual links populated.

### 6.3 WWJ Path Reorganization

The golden_tutor_chunk_candidates.jsonl file was previously documented at `knowledge/wine-with-jimmy/manual-import/reports/golden_tutor_chunk_candidates.jsonl`. That path no longer exists. The `enrichment-ready/` directory contains per-video enrichment metadata but not the consolidated golden candidate list. Any future phase that references the 166 golden candidates must first locate the canonical current path.

### 6.4 Schema Fragmentation Persists

Of the 14 CC nodes referenced in enrichment drafts, 8 are unregistered governance-schema nodes that cannot be validated by the current manifest validator. Before any promotion of these enrichments to production, the schema fragmentation documented in `docs/KNOWLEDGE_MAP_MANIFEST_RECONCILIATION_AUDIT.md` must be resolved.

## Governance Invariants

This document does not modify any runtime behavior. All governance invariants remain unchanged:

```
safe_for_examiner = false
examiner_scoring_allowed = false
official_wset_question = false
training_item_only = true
uses_llm = false
uses_api = false
uses_embeddings = false
uses_vector_db = false
cloud_services_active = false
ENABLE_PEDAGOGICAL_STRATEGY_LAYER = False
```

## Input Documents

| Document | Role |
| --- | --- |
| `docs/KNOWLEDGE_ASSET_INVENTORY_AND_AUDIT.md` | Asset list and Tier rankings (reused, not repeated) |
| `docs/KNOWLEDGE_MAP_MANIFEST_RECONCILIATION_AUDIT.md` | Node ID lists (reused, not repeated) |
| `docs/FULL_BANK_CORPUS_VERIFICATION_SUMMARY.md` | Corpus grounding (reused, not repeated) |
| `docs/GOLD_BANK_ACTIVATION_READINESS.md` | Active item set and Gold rankings (reused, not repeated) |
| `knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json` | Primary evidence for MC/CC linkage in enriched items |
| `knowledge/question-bank/diagnostic_sba/drafts/gold_bank_activation_drafts.json` | Evidence for null linkage in broader Gold draft set |
| `frontend/diagnostic-sba/preguntas.json` | Production payload — confirmed 0 MC/CC linkage |
| `knowledge/enrichment/diagnostic_outcome.schema.json` | Schema confirmation of nullable MC/CC fields |
| `knowledge/wine-with-jimmy/enrichment-ready/` | WWJ enrichment status per video |
