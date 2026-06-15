# EpistemicLab Misconception Coverage Audit

**Audit date:** 2026-06-15  
**Mode:** Audit only. No misconception nodes, links, analytics, coaching, or runtime behavior changed.

## 1. Executive finding

EpistemicLab has **20 explicit misconception objects**, but **zero are fully detectable end to end in the deployed SBA pathway**.

- 20 misconception nodes exist.
- 13 are registered in the knowledge-map manifest; 7 are unregistered.
- 10 have explicit `detection_keywords`; 10 do not.
- 20 can be detected by the free-text pre-pass when the learner closely expresses the stored claim.
- 0 have deployed SBA distractor linkage in `misconception_signals.json`.
- 19 have a Wine With Jimmy remediation lookup; `MC_WHOLE_BUNCH_01` does not.
- Analytics can track triggered, persistent, and resolved states only after an MC ID reaches the runtime.

Therefore:

- **FULLY DETECTABLE:** 0
- **PARTIALLY DETECTABLE:** 20
- **NOT DETECTABLE as explicit misconception objects:** numerous missing domain families listed in Section 5

## 2. Detectability definition

- **FULLY DETECTABLE:** can be triggered from learner free text and/or a selected SBA distractor, recorded in learner state, routed to remediation, and re-observed.
- **PARTIALLY DETECTABLE:** one or more stages work, but the full path is broken.
- **NOT DETECTABLE:** no explicit misconception object and no reliable route from learner behavior to a misconception ID.

The current break is structural, not merely editorial: production SBA distractors do not carry MC IDs, so wrong answers become generic incorrect outcomes rather than named misconceptions.

## 3. Existing misconception inventory

| Misconception | Keyword routing | Manifest | SBA linked | Remediation | Classification | Reason |
|---|---:|---|---:|---:|---|---|
| High acidity means low quality | Yes | Registered | No | Yes | PARTIALLY DETECTABLE | Robust free-text route; no SBA route |
| MLF removes acidity | No | Registered | No | Yes | PARTIALLY DETECTABLE | Close-phrase detection only; no SBA route |
| All wines improve with age | Yes | Unregistered | No | Yes | PARTIALLY DETECTABLE | Free-text route works; graph registration and SBA route absent |
| Higher alcohol means higher quality | Yes | Unregistered | No | Yes | PARTIALLY DETECTABLE | Same limitation |
| All botrytis is noble rot | No | Registered | No | Yes | PARTIALLY DETECTABLE | Stored claim can match, but detection is brittle |
| Tartrate crystals mean poor quality | Yes | Unregistered | No | Yes | PARTIALLY DETECTABLE | Good free-text signal; no item linkage |
| Complexity and length are identical | Yes | Unregistered | No | Yes | PARTIALLY DETECTABLE | SAT misconception exists but is not tied to SAT responses |
| Cool climate always means low alcohol | No | Registered | No | Yes | PARTIALLY DETECTABLE | Exact/near claim only |
| Cool climate always means green flavours | Yes | Registered | No | Yes | PARTIALLY DETECTABLE | Strongest climate free-text route; no SBA route |
| Champagne lees ageing only adds flavour | No | Registered | No | Yes | PARTIALLY DETECTABLE | No broader sparkling misconception family |
| MLF always tastes buttery | No | Registered | No | Yes | PARTIALLY DETECTABLE | Exact/near claim only |
| MLF removes all acidity | No | Registered | No | Yes | PARTIALLY DETECTABLE | Exact/near claim only |
| Oaky wines are low quality | No | Registered | No | Yes | PARTIALLY DETECTABLE | Exact/near claim only |
| New and old oak have the same effect | No | Registered | No | Yes | PARTIALLY DETECTABLE | Exact/near claim only |
| More oak means higher quality | Yes | Unregistered | No | Yes | PARTIALLY DETECTABLE | Free-text route works; no SBA route |
| Residual sugar always tastes sweet | Yes | Unregistered | No | Yes | PARTIALLY DETECTABLE | Free-text route works; no SBA route |
| Tannin is bitterness | Yes | Registered | No | Yes | PARTIALLY DETECTABLE | Robust free-text route; no SBA route |
| Tannin and acidity are the same sharpness | No | Registered | No | Yes | PARTIALLY DETECTABLE | Exact/near claim only |
| More tannin means better quality/ageability | Yes | Unregistered | No | Yes | PARTIALLY DETECTABLE | Free-text route works; no SBA route |
| Whole bunch always gives green stalkiness | No | Registered | No | No | PARTIALLY DETECTABLE | Detection possible; remediation lookup missing |

## 4. Engine-by-engine audit

### Misconception pre-pass

`tools/orchestrator/misconception_prepass.py` loads all 20 files directly, including unregistered nodes. It uses stored misconception text, detection signals, optional keyword rules, and an explanatory-query guard.

Strength:

- Directly asserted misconceptions can be intercepted deterministically.

Limit:

- Ten nodes have no explicit keyword rules.
- The system detects a learner statement, not a latent misconception inferred from repeated choices.
- Closely related misconceptions compete for one highest-scoring result.

### SBA misconception runtime

`tools/learner_model/misconception_runtime.py` can record:

- `misconception_triggered`
- `misconception_persistent`
- `misconception_resolved`

It requires an incoming known `mc_id`. Current signal inventory reports `sba_distractors_linked = false` for all 20 nodes. The runtime exists, but the deployed question pathway does not supply its required identifier.

### Weakness profiles and learning analytics

Knowledge tracing records mastery, recent failures, misconception hits, recurrence, and retention risk. It can distinguish a named misconception only when an MC ID or a comparator label already exists. Otherwise, repeated wrong answers remain topic weakness, not misconception evidence.

### Recommendation and adaptive engines

The adaptive composer can prioritize persistent unresolved MC IDs and request WWJ remediation. This is a downstream consumer, not a detector. With no SBA linkage, its misconception pathway is mostly dormant.

### Coaching engine

The coaching assets explain SAT, command verbs, response structure, and some common errors. They do not form a comprehensive content-domain misconception library. Nineteen MC nodes have lookup availability, but contextual delivery depends on detection upstream.

## 5. Misconceptions that are not detectable today

The following families have no explicit misconception object or reliable mapping:

| Domain | Missing misconception examples | Classification |
|---|---|---|
| Yield | Low yield always means high quality; high yield always means dilution | NOT DETECTABLE |
| Canopy | More exposure is always better; dense canopy only affects ripeness | NOT DETECTABLE |
| Irrigation | Irrigation always lowers quality; water stress is always beneficial | NOT DETECTABLE |
| Soils | Soil minerals directly transfer flavour; limestone automatically creates acidity | NOT DETECTABLE |
| Harvest | Later harvest always improves quality; mechanical harvest is always inferior | NOT DETECTABLE |
| Pressing/extraction | More pressing or extraction always means more quality | NOT DETECTABLE |
| Stabilisation/filtration | Filtration always strips quality; unfiltered always means superior | NOT DETECTABLE |
| Rose | Rose is made by mixing red and white in all contexts | NOT DETECTABLE |
| Sparkling methods | Traditional method is always higher quality; tank method is inherently low quality | NOT DETECTABLE |
| Dosage | Brut means no sugar; dosage creates all sparkling sweetness/style | NOT DETECTABLE |
| Fortification | Fortification always occurs after fermentation; all fortified wines are sweet | NOT DETECTABLE |
| Port | Tawny is simply old Ruby; Vintage Port is ready on release | NOT DETECTABLE |
| Sherry | All Sherry is sweet; flor is oxidation | NOT DETECTABLE |
| Madeira/VDN/Marsala | Heat damage and deliberate Madeira maturation are the same | NOT DETECTABLE |
| Sweet wine methods | Icewine uses botrytis; passito and late harvest are identical | NOT DETECTABLE |
| Regional reasoning | Region name alone determines quality; appellation tier guarantees quality | NOT DETECTABLE |
| Service/faults | Sediment means fault; decanting always improves wine | NOT DETECTABLE |
| Food pairing | Red with meat and white with fish are universal rules | NOT DETECTABLE |
| Health | Sulphites are the main cause of all wine headaches | NOT DETECTABLE |
| SAT readiness | Tertiary aromas always mean the wine is past its best | NOT DETECTABLE |

## 6. Coverage by requested misconception family

| Family | Classification | Evidence |
|---|---|---|
| Climate misunderstandings | PARTIALLY DETECTABLE | 2 cool-climate nodes plus alcohol-quality node; no maritime/continental/topography misconception coverage |
| Yield misunderstandings | NOT DETECTABLE | No yield MC node |
| Canopy misunderstandings | NOT DETECTABLE | No canopy MC node |
| MLF misunderstandings | PARTIALLY DETECTABLE | 3 acidity/MLF nodes; no SBA linkage |
| Oak misunderstandings | PARTIALLY DETECTABLE | 3 oak nodes; no SBA linkage |
| Sparkling misunderstandings | PARTIALLY DETECTABLE | Only lees-ageing misconception; methods and dosage absent |
| Fortification misunderstandings | NOT DETECTABLE | No fortification MC node |
| Sweet-wine misunderstandings | PARTIALLY DETECTABLE | Botrytis and residual-sugar nodes only |
| Botrytis misunderstandings | PARTIALLY DETECTABLE | One node, brittle keyword routing, no SBA link |
| SAT structure/quality | PARTIALLY DETECTABLE | Complexity/length, acidity, tannin, alcohol, oak; no response-to-MC mapping |

## 7. Required next content

Before adding new nodes, the existing 20 need item and response linkage. That is implementation work, not new content, and is outside this audit.

For new misconception content, the evidence supports a minimum of **18 additional misconception objects**, one for each missing high-value family:

1. Yield
2. Canopy exposure
3. Irrigation/water stress
4. Soil-to-flavour causality
5. Harvest timing
6. Mechanical harvest
7. Pressing/extraction
8. Filtration/stabilisation
9. Rose production
10. Sparkling method hierarchy
11. Dosage/sweetness
12. Fortification timing
13. Port styles
14. Sherry sweetness/flor
15. Madeira heat ageing
16. Icewine/passito method confusion
17. Service/fault/sediment
18. Food-pairing absolutes

This is a minimum family count, not permission to author content.

