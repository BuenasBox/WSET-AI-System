# EpistemicLab Knowledge Coverage Audit

**Audit date:** 2026-06-15  
**Mode:** Read-only corpus audit. No content, production, frontend, runtime, or governance changes.  
**Authority:** Formative coverage analysis only. It is not WSET assessment or examiner evaluation.

## 1. Executive finding

The corpus is broad but not proportionally deep.

- Production SBA bank: **578** items.
- Enrichment source: **360** enriched items and **276** micro-drills.
- Current local production payload: **310** enriched items and **239** micro-drills.
- Deployment synchronization delta: **50 enriched records** and **37 drills** exist in the enrichment source but not in the current local production payload.
- Deployed/committed Open Response baseline: **31** items, all in RA1 or RA2.
- SAT prompt bank: **6** prompts.
- Causal-chain files: **199**, all with unique IDs and no truthy governance violation.
- Misconception nodes: **20**.

The strongest coverage is climate, core viticulture, fermentation, extraction, oak, major European regions, Sherry, storage, and SAT structure. The clearest hard gaps are Icewine/Eiswein, VDN/Rutherglen/Marsala depth, several sparkling-method pathways, regional reasoning for the USA/Canada and South Africa, and Open Response coverage outside RA1/RA2.

## 2. Scope and evidence

| Asset | Audit source | Count |
|---|---|---:|
| SBA | `frontend/diagnostic-sba/preguntas_data.js` | 578 |
| Enriched SBA | `knowledge/question-bank/enrichment/sba_enrichment_v1.json` | 360 |
| Micro-drills | Same enrichment sidecar | 276 |
| Causal chains | `knowledge/knowledge-map/causal-chains/*.json` | 199 |
| Open Response | Committed `HEAD` version of `open_response_bank.json` | 31 |
| SAT prompts | `frontend/adaptive-session/session_bank.js` | 6 |
| Misconceptions | `knowledge/knowledge-map/misconceptions/*.json` | 20 |
| Coaching/readiness | `knowledge/{mentor-framework,command-verbs,distinction-patterns,sat-framework}` | 26 JSON assets |

The uncommitted 25-item OR expansion was excluded because it was being produced separately while this audit ran. The committed OR object hash is `15e8d77252bf265017870f76a6c2f8a5df00dde8`.

Snapshot hashes:

- SBA payload SHA-256: `FFA008F7C6B6187FA7968B76F2B466DA58FCE07D6B5FCCFFE02C5413D772AE18`
- SAT/session payload SHA-256: `6F2913D85679869B4B5E5AB61E6877A754D938E431E59711C226937C407E257D`
- Enrichment sidecar SHA-256: `FB03228B0FBF60822F882C425F7A6A2C2703FB0511F1E66871DC39A16C053561`

## 3. RA interpretation

The mission examples use RA2 for general winemaking and RA5 for sweet-wine methods. That is not the official WSET Issue 2.0.1 result-area model stored in `knowledge/assessment-framework/learning_outcomes.json`.

This audit uses the official model:

- **RA1:** natural and human factors in vineyard and winery, including sweet-wine production methods.
- **RA2:** still wines of the world, including regions, legislation, and trade factors.
- **RA3:** sparkling wines.
- **RA4:** fortified wines.
- **RA5:** customer advice, storage, service, faults, food pairing, and health.
- **SAT:** separate tasting unit.

All mission examples are still represented below. Botrytis, passito, Icewine, Tokaji, and Sauternes are cross-referenced under RA1 production methods and RA2 regional wines as appropriate.

## 4. Counting and classification rules

Counts are deterministic lexical mappings over learner-facing fields, topic tags, keywords, IDs, and titles. Counts are **multi-label**: one item may support more than one subtopic. They must not be summed to recover corpus totals.

Columns:

- `SBA`: production SBA items mapped to the subtopic.
- `E`: enriched SBA source records.
- `D`: micro-drills.
- `CC`: causal-chain nodes.
- `OR`: committed Open Response items.
- `SAT`: SAT prompts.
- `MC`: misconception nodes.
- `Coach`: coaching/readiness assets.

Classification:

- **STRONG:** substantial SBA plus enrichment, drills, causal support, OR, and either misconception or coaching support.
- **ADEQUATE:** usable content and at least four supporting modalities, but one important pathway is absent.
- **WEAK:** some content exists, but coverage is sparse or mainly one-mode.
- **MISSING:** no mapped SBA, OR, SAT, causal-chain, or misconception evidence.
- **UNKNOWN:** reserved for mappings that cannot be established confidently. No matrix row required this label; uncertainties are documented below.

## 5. Master coverage matrix

### RA1 - Vineyard and winery factors

| Subtopic | SBA | E | D | CC | OR | SAT | MC | Coach | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Climate types | 52 | 38 | 28 | 28 | 4 | 0 | 3 | 10 | STRONG |
| Topography, aspect, altitude | 29 | 22 | 19 | 13 | 4 | 0 | 0 | 1 | STRONG |
| Weather hazards and vintage | 12 | 8 | 7 | 10 | 2 | 0 | 0 | 0 | ADEQUATE |
| Soils and drainage | 30 | 16 | 11 | 10 | 5 | 0 | 0 | 0 | ADEQUATE |
| Vine cycle and ripening | 13 | 9 | 7 | 17 | 3 | 0 | 0 | 3 | STRONG |
| Pests and disease | 8 | 5 | 4 | 3 | 2 | 0 | 0 | 0 | ADEQUATE |
| Training, pruning, canopy | 13 | 11 | 5 | 4 | 3 | 0 | 0 | 0 | ADEQUATE |
| Yield management | 8 | 7 | 5 | 6 | 5 | 0 | 0 | 0 | ADEQUATE |
| Irrigation and water stress | 7 | 4 | 3 | 3 | 6 | 0 | 0 | 0 | ADEQUATE |
| Harvest timing and method | 10 | 9 | 8 | 10 | 0 | 0 | 0 | 1 | ADEQUATE |
| Crushing, pressing, clarification | 2 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | WEAK |
| Fermentation and yeast | 43 | 36 | 26 | 37 | 6 | 1 | 1 | 7 | STRONG |
| Red extraction and cap management | 8 | 8 | 5 | 11 | 2 | 0 | 0 | 1 | STRONG |
| Malolactic conversion | 6 | 4 | 4 | 8 | 1 | 0 | 3 | 12 | ADEQUATE |
| Lees and batonnage | 15 | 12 | 9 | 10 | 0 | 1 | 1 | 2 | ADEQUATE |
| Oak and maturation | 32 | 24 | 18 | 16 | 4 | 2 | 2 | 10 | STRONG |
| Stabilisation, filtration, bottling | 18 | 10 | 9 | 17 | 0 | 0 | 1 | 0 | ADEQUATE |
| Rose production | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 2 | WEAK |
| Botrytis / noble rot | 7 | 4 | 2 | 6 | 1 | 0 | 1 | 0 | ADEQUATE |
| Passito / late harvest | 3 | 1 | 1 | 3 | 0 | 0 | 0 | 0 | WEAK |
| Icewine / Eiswein | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | MISSING |

### RA2 - Still wines of the world

| Subtopic | SBA | E | D | CC | OR | SAT | MC | Coach | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Bordeaux | 11 | 5 | 4 | 3 | 1 | 0 | 0 | 6 | STRONG |
| Burgundy / Beaujolais | 19 | 8 | 7 | 2 | 1 | 0 | 0 | 5 | STRONG |
| Rhone / Southern France | 7 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | WEAK |
| Loire / Alsace | 13 | 4 | 3 | 3 | 1 | 0 | 0 | 0 | ADEQUATE |
| Germany / Austria / Hungary / Greece | 17 | 11 | 11 | 4 | 1 | 0 | 0 | 1 | STRONG |
| Italy | 25 | 7 | 7 | 3 | 2 | 0 | 0 | 0 | ADEQUATE |
| Spain, still wines | 26 | 15 | 15 | 1 | 2 | 0 | 0 | 0 | ADEQUATE |
| Portugal, still wines | 7 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | ADEQUATE |
| USA / Canada | 15 | 9 | 7 | 0 | 0 | 0 | 0 | 0 | WEAK |
| Chile / Argentina | 25 | 9 | 8 | 4 | 1 | 0 | 0 | 1 | STRONG |
| South Africa | 7 | 2 | 1 | 0 | 1 | 0 | 0 | 1 | WEAK |
| Australia | 11 | 5 | 5 | 1 | 1 | 0 | 0 | 0 | ADEQUATE |
| New Zealand | 10 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | ADEQUATE |
| Regional law and classifications | 37 | 14 | 14 | 4 | 1 | 0 | 0 | 2 | STRONG |

### RA3 - Sparkling wines

| Subtopic | SBA | E | D | CC | OR | SAT | MC | Coach | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Traditional method | 14 | 9 | 7 | 5 | 0 | 0 | 0 | 0 | ADEQUATE |
| Tank / Asti method | 3 | 3 | 3 | 2 | 0 | 0 | 0 | 0 | WEAK |
| Transfer / ancestral / carbonation | 3 | 2 | 1 | 2 | 0 | 0 | 0 | 0 | WEAK |
| Champagne | 14 | 6 | 3 | 3 | 0 | 0 | 1 | 0 | ADEQUATE |
| Cava / Cremant | 8 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | WEAK |
| Prosecco / Sekt | 6 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | WEAK |
| Dosage and sweetness levels | 7 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | ADEQUATE |

### RA4 - Fortified wines

| Subtopic | SBA | E | D | CC | OR | SAT | MC | Coach | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Port | 9 | 5 | 5 | 5 | 0 | 0 | 0 | 0 | ADEQUATE |
| Sherry | 15 | 11 | 7 | 6 | 1 | 1 | 0 | 4 | STRONG |
| Madeira | 5 | 2 | 2 | 1 | 0 | 0 | 0 | 0 | ADEQUATE |
| VDN / Rutherglen / Marsala | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | WEAK |
| Fortification timing and ageing | 7 | 7 | 7 | 5 | 0 | 0 | 0 | 1 | ADEQUATE |

### RA5 - Advice, storage, service, faults, pairing, health

| Subtopic | SBA | E | D | CC | OR | SAT | MC | Coach | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Storage | 8 | 8 | 7 | 3 | 3 | 0 | 0 | 1 | STRONG |
| Service, glassware, decanting | 17 | 14 | 8 | 9 | 0 | 0 | 0 | 0 | ADEQUATE |
| Wine faults | 21 | 18 | 13 | 9 | 0 | 0 | 0 | 3 | ADEQUATE |
| Food pairing | 6 | 5 | 4 | 5 | 0 | 0 | 0 | 0 | ADEQUATE |
| Health and responsible consumption | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | WEAK |
| Advice, trade, and price | 20 | 12 | 11 | 7 | 3 | 0 | 0 | 2 | STRONG |

### SAT - Separate tasting unit

| Subtopic | SBA | E | D | CC | OR | SAT | MC | Coach | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Appearance | 9 | 9 | 6 | 11 | 2 | 6 | 0 | 9 | STRONG |
| Nose and aroma categories | 3 | 3 | 3 | 7 | 1 | 6 | 0 | 10 | WEAK |
| Palate structure | 115 | 94 | 83 | UNKNOWN | 14 | 6 | 9 | 14 | STRONG |
| Quality justification | 16 | 14 | 11 | 18 | 4 | 2 | 1 | 12 | STRONG |
| Readiness / drinking window | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 9 | WEAK |

`Palate structure` causal-chain count is marked `UNKNOWN` because generic chain fields such as `final_outcome` make deterministic lexical counting over-inclusive. The presence of substantial causal support is verified, but a defensible exact count requires a curated chain-to-topic registry that does not currently exist.

## 6. Overrepresented areas

- Generic RA1 climate and fermentation content.
- Oak, maturation, tannin, and broad palate-structure language.
- Spain, Italy, and Chile/Argentina relative to weaker regional clusters.
- Sherry relative to Port, Madeira, and other fortified styles.
- Generic SAT palate vocabulary relative to nose discrimination and readiness practice.

## 7. Weak or missing areas

Highest-confidence content gaps:

1. Icewine/Eiswein: no mapped item in any audited modality.
2. VDN/Rutherglen/Marsala: one SBA and no enrichment, drill, chain, OR, misconception, or coaching path.
3. Crushing/pressing/clarification: only two SBA and no micro-drill or OR support.
4. Rose production and passito/late harvest: isolated coverage, no OR or misconception pathway.
5. USA/Canada and South Africa: factual SBA presence without causal or OR depth.
6. Cava/Cremant and Prosecco/Sekt: recognition coverage without causal chains, OR, misconceptions, or coaching.
7. RA3 overall: no deployed OR.
8. RA4 overall: only one deployed OR, for Sherry.
9. RA5: no OR for service, faults, pairing, or health.
10. SAT: six prompts, but readiness is prompt-level only and nose/aroma discrimination remains thin.

## 8. Validation notes

- All 578 SBA IDs were unique in the production payload.
- All 360 enrichment records were keyed by source question ID.
- All 199 causal-chain IDs were unique.
- No causal-chain governance field was truthy for `safe_for_examiner` or `examiner_scoring_allowed`.
- Counts in this matrix are evidence counts, not quality scores.
- A lexical match can establish presence but not pedagogical correctness. Borderline mappings were kept out or marked `UNKNOWN`.

