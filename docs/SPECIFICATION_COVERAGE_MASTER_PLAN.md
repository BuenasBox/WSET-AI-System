# EpistemicLab Specification Coverage Master Plan

**Closeout date:** 2026-06-15  
**Mode:** Evidence-only corpus analysis. No content, runtime, frontend, production, or governance changes.  
**Authority:** Formative planning only. This is not WSET assessment, scoring, or an outcome prediction.

## 1. Authoritative baseline

| Corpus | Verified current state |
|---|---:|
| Operational SBA | 578 |
| Enriched SBA | 360 |
| Fallback SBA | 218 |
| Micro-drills | 276 |
| Open Response | 106 (`OR_001`-`OR_106`, complete and unique) |
| SAT prompts | 6 |
| Misconception nodes | 20/20 operational end to end |
| Causal-chain files | 199 |

The Open Response source of truth is
`knowledge/question-bank/open_response/open_response_bank.json`. The enrichment
source of truth is
`knowledge/question-bank/enrichment/sba_enrichment_v1.json`.

## 2. Official specification baseline

The official WSET Level 3 theory MCQ allocation is:

| RA | Questions per 50 | Share |
|---|---:|---:|
| RA1 | 8 | 16% |
| RA2 | 28 | 56% |
| RA3 | 5 | 10% |
| RA4 | 5 | 10% |
| RA5 | 4 | 8% |

For short written answers, RA1 knowledge is foundational across the paper; RA2
provides most applied regional content; RA3 and RA4 share a smaller allocation;
and RA5 Block 1 contributes the remaining advice/service allocation. SAT is a
separate unit: two still wines, one white and one red.

Source: WSET Level 3 Award in Wines Specification, Issue 2.0.1, represented in
`knowledge/assessment-framework/learning_outcomes.json` and the official WSET
specification:
https://www.wsetglobal.com/media/11731/wset_l3wines_specification_en_highres_may2022_issue2.pdf

## 3. Current balance

### SBA

| RA | Current | Current share | Official share | Finding |
|---|---:|---:|---:|---|
| RA1 | 225 | 38.9% | 16% | Overrepresented |
| RA2 | 217 | 37.5% | 56% | Underrepresented |
| RA3 | 64 | 11.1% | 10% | Proportionate |
| RA4 | 31 | 5.4% | 10% | Underrepresented |
| RA5 | 39 | 6.7% | 8% | Slightly underrepresented |
| Unmapped | 2 | 0.3% | 0% | Mapping repair required |

### Open Response

Recorded metadata distribution:

| RA | Items | Share |
|---|---:|---:|
| RA1 | 36 | 34.0% |
| RA2 | 26 | 24.5% |
| RA3 | 15 | 14.2% |
| RA4 | 15 | 14.2% |
| RA5 | 14 | 13.2% |

This is not equivalent to validated specification coverage. Only one recorded
RA3 item has a clear sparkling-method topic, one recorded RA4 item clearly
covers fortified wine, and no recorded RA5 item clearly covers the full RA5
service/fault/pairing specification from its topic label. The remaining items
often contain useful cross-domain reasoning, but their RA labels cannot be
credited without remapping review.

### SAT

The six prompts contain three white, two red, and one sweet archetype. They
cover the SAT sections, simple/complex contrasts, and several quality/readiness
conclusions. Missing resilience cases include rose, fault recognition,
too-young calibration, end-of-window calibration, and closer quality-boundary
comparisons.

### Misconceptions

All 20 legacy nodes are now operational through detection, evidence frequency,
recommendation, coaching, Profile, and Full Simulation contracts. This closes
the technical loop. It does not create topic breadth: the nodes remain
concentrated in acidity, tannin, climate, oak, MLF, ageing, botrytis, lees,
stabilisation, residual sugar, and whole-bunch fermentation.

## 4. Completion strategy

1. Apply official RA quotas at session selection time.
2. Retain all overrepresented content; do not delete RA1.
3. Add the minimum targeted corpus needed to repair missing and weak concepts.
4. Require specification-valid RA/topic review before new items enter a pool.
5. Pair each new misconception family with its coaching and evidence mapping.
6. Keep SAT separate from theory-domain balancing.

## 5. Final build targets

| Asset | Current | Recommended addition | Completion target |
|---|---:|---:|---:|
| SBA | 578 | **141** | 719 |
| Enriched SBA actions | 360 | **200** | 560 enriched records |
| Open Response | 106 | **28** | 134 |
| SAT prompts | 6 | **8** | 14 |
| Misconception nodes | 20 | **18** | 38 |
| Paired coaching paths | 20 node paths plus shared assets | **18** | One path per new node |
| Micro-drills | 276 | **48** | 324 |
| Causal chains | 199 | **12** | 211 |

The 141 SBA additions are the current-total deficit floor: RA2 +107, RA4 +27,
RA5 +7. Exact corpus-level proportionality by additions alone would be
inefficient because existing RA1 volume is retained. Session quotas provide
immediate proportional operation; additions provide topic depth and rotation.

## 6. Highest-priority gaps

1. Icewine/Eiswein: no defensible coverage in any audited learning modality.
2. RA4 breadth: Port, Madeira, fortified Muscats/VDN, and fortification
   comparisons lack enough depth and written practice.
3. RA2 depth: Southern France/Rhone, Portugal, USA/Canada, and South Africa
   require more causal and written application.
4. RA3 method discrimination: tank/Asti, transfer, ancestral, carbonation,
   Cava/Crémant, and Prosecco/Sekt.
5. RA5 written application: service, faults, food pairing, health, and advice.
6. RA1 process gaps: crushing/pressing/clarification and rose production.
7. Misconception breadth outside the 20 operational legacy families.
8. SAT edge cases for readiness, faults, rose, and quality boundaries.

## 7. Decision

EpistemicLab can sample an officially proportioned theory session now by using
RA quotas. It cannot yet claim resilient specification coverage at subtopic
level. The targeted additions above are the recommended completion build.
