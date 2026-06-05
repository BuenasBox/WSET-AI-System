# Phase 4A.3.7.50 Open Response Readiness Assessment

Date: 2026-06-04

Scope: readiness assessment for the 20 structurally approved, inactive diagnostic open-response candidates, source IDs 798-817.

This assessment does not activate, publish, edit, expose, score, or route any open-response item. It does not modify candidates, review records, schemas, payloads, Tutor, Retrieval, Self-Eval, Golden baselines, snapshots, or frontend.

## Evidence Base

- Normalized candidates: `knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json`
- Review records: `knowledge/question-bank/open_response/reviews/open_response_review_records.json`
- Prior review/remediation documents:
  - `docs/OPEN_RESPONSE_HUMAN_REVIEW_PACKET.md`
  - `docs/OPEN_RESPONSE_SEMANTIC_REVIEW_BATCH_1.md`
  - `docs/PHASE_4A_3_7_48_OPEN_RESPONSE_REMEDIATION_BATCH_1.md`
  - `docs/PHASE_4A_3_7_49_OPEN_RESPONSE_REMEDIATION_BATCH_2.md`

Current structural state:

- 21 open-response records were detected.
- ID 18 remains rejected and is outside this readiness set.
- 20 candidates are normalized, structurally approved, grounded, and inactive.
- All 20 approved candidates retain training-only governance.
- No candidate is active or learner-facing.

## Individual Classification

| ID | Classification | Readiness rationale |
|---|---|---|
| 798 | READY_WITH_MINOR_GAPS | Good sustainability-cost-price construct, but commercial differentiation remains partly market-facing and unmapped to a causal-chain node. |
| 799 | READY_WITH_MINOR_GAPS | Strong malolactic chain, but "quality final" must stay conditional by style rather than treated as inherent improvement. |
| 800 | READY | Clear altitude-temperature-ripening-style causality with solid grounding and bounded scope. |
| 801 | READY | Clear orientation/slope-exposure-ripening item with good RA1 fit and practical answer boundary. |
| 802 | READY | Useful oxygen-management item for white wines; grounding is adequate if feedback stays focused on reduction of oxidation risk. |
| 803 | READY_WITH_MINOR_GAPS | Useful yeast-sensory item, but the stem still allows broader yeast-choice answers than the concept list can fully evaluate. |
| 804 | READY | Batch 1 narrowed this into a clean soil drainage-vigour-style causal item with relevant causal-chain support. |
| 805 | READY | Batch 2 narrowed oak comparison to aroma, tannin, integration, structure, and complexity; causal-chain support is strong enough for private formative use. |
| 806 | READY | Clear two-technique canopy-management item with strong practical scope and grounding. |
| 807 | NEEDS_REVIEW | Improved after remediation, but still distinction-level, unmapped, and potentially broad across irrigation/canopy/drought/heat effects. |
| 808 | READY_WITH_MINOR_GAPS | Valuable density-competition-vigour-cost item, but it combines style and cost; session design should avoid using it as a simple recall prompt. |
| 809 | NEEDS_REVIEW | Compare/contrast construct is useful, but selected-vs-indigenous yeast remains unmapped and needs a question-specific two-sided feedback rubric. |
| 810 | READY_WITH_MINOR_GAPS | Now bounded to yield, berry concentration, cost and price, but overlaps with 812 and price influence must remain potential. |
| 811 | READY_WITH_MINOR_GAPS | Good latitude/altitude item, but "interactúan" may exceed the current expected answer unless feedback accepts a simpler temperature-ripening explanation. |
| 812 | READY | Clean moderate-water-stress-vigour-berry-concentration item; overlap with 810 is manageable through sequencing. |
| 813 | READY | Clear foundational indigenous-yeast risk item; accepts concise formative answers. |
| 814 | READY | Strong foundational pruning-buds-yield reasoning with stable grounding. |
| 815 | READY | Clear foundational stainless-steel technical-benefit item with bounded answer paths. |
| 816 | READY_WITH_MINOR_GAPS | Strong maceration-extraction-tannin construct, but "quality final" requires conditional feedback around balance and over-extraction. |
| 817 | READY_WITH_MINOR_GAPS | Batch 1 narrowed soil comparison to sand/clay water availability and vigour; still overlaps with 804 and has partial causal-chain mapping. |

Classification counts:

- READY: 10
- READY_WITH_MINOR_GAPS: 8
- NEEDS_REVIEW: 2

## Coverage Assessment

RA coverage is narrow by design: all 20 approved candidates are RA1. The set is therefore not ready as a general WSET L3 open-response lab. It is ready only as a private RA1-focused lab around factors affecting wine style, quality, and price.

Topic coverage is reasonably diverse within RA1. It includes climate/site effects, soil and water availability, canopy and pruning, density, fermentation vessels, oxygen management, malolactic fermentation, oak, yeast choice, maceration, sustainability, and cost/price influences. The largest topic concentrations are soil and water stress, each with two items, plus three yeast-related items if IDs 803, 809, and 813 are considered together.

Subtopic coverage is adequate for a small private lab but not comprehensive. It covers fermentation, white wine, yield, drainage, climate, altitude, slope, vineyard techniques, risk, oak, drought/heat, and price. It does not yet cover the full WSET L3 topic range: regions, grape varieties by region, sparkling, fortified, service/storage, SAT tasting judgement, or broader RA2/RA3 style comparisons.

Difficulty coverage is usable: 3 foundational, 9 intermediate, and 8 distinction. The bank can support mixed sessions, but the distinction items need controlled sequencing because several contain multi-step causal or commercial reasoning.

Causal reasoning coverage is one of the set's strengths. Every approved item has an `optional_causal_chain`, and several map well to existing knowledge-map reasoning, especially soil drainage, oak, maceration, malolactic fermentation, canopy, altitude, pruning, and stainless steel. The weaker causal areas are sustainability-cost-price, water stress-price, selected-vs-indigenous yeast, and drought/heat management, where the current chains are native plain-text expectations rather than reviewed knowledge-map nodes.

Expected-concept coverage is structurally present and generally improved by the two remediation batches. The main limitation is still rubric depth: concept presence can detect omissions, but it cannot reliably distinguish term listing from a valid causal explanation. This is acceptable for formative private practice if feedback is framed as guidance, not scoring.

Grounding is available for all 20 approved candidates, with `corpus_support.status = supported`. However, support is chunk-and-term based, not a full semantic guarantee that every nuance of each stem is supported. This matters most for price, commercial differentiation, quality, and premium-like reasoning.

Redundancies remain but are manageable:

- 804 and 817 both cover soil-vigour-style, now differentiated as drainage vs sand/clay comparison.
- 810 and 812 both cover moderate water stress, now differentiated as cost/price vs vigour/berry/concentration.
- 803, 809, and 813 all cover yeast, but at different levels: sensory influence, compare/contrast tradeoffs, and a single risk.

Important gaps:

- No RA2/RA3 spread.
- No region-specific open-response coverage.
- No SAT open-response quality/readiness item.
- No sparkling or fortified open-response item.
- No question-specific feedback rubrics yet.
- No private-lab UX or session-selection layer exists.
- No activation flag should be changed until a private-lab governance contract exists.

## Pedagogical Value

The set has enough diversity for a useful private RA1 practice lab. It exercises explanation, cause-effect reasoning, comparison, and application of viticulture/winemaking choices to style, concentration, cost, price, and sensory profile.

It does not have enough diversity for a full WSET L3 open-response practice product. The concentration on RA1 is too high, and the absence of regional, sparkling, fortified, and SAT judgement questions would make any broader lab misleading.

Causal depth is adequate for private formative use. The best items ask learners to connect a factor to a mechanism and then to a wine-style consequence. The weaker items need either sequencing constraints or additional rubric specificity so broad distinction answers do not become unreviewable.

## Readiness Decision

Decision: Option B - Activable after minor adjustments.

The current bank is not "premature" as a private, non-public RA1 Open Response Lab because 18 of 20 items are either ready or close to ready, all 20 are inactive, all 20 have support, and governance is intact. It is also not activable today because two items still need review and the lab-level activation contract does not yet exist.

Minimum activation should use only READY and selected READY_WITH_MINOR_GAPS items. IDs 807 and 809 should remain excluded until review-specific feedback expectations are added.

## Risks

- Learners may interpret formative feedback as scoring unless the UI and copy explicitly block score/pass/fail/examiner language.
- Generic concept coverage may reward keyword listing instead of reasoning.
- Price, commercial differentiation, and quality language can overclaim if feedback is not conditional.
- RA1 concentration can create a false impression of broad WSET L3 readiness.
- Redundant soil/water-stress questions can make short sessions feel repetitive.
- Unmapped causal chains reduce explainability for some distinction items.

## Minimum Activation Needs

Obligatory:

- Keep `activation_status` inactive until a separate activation phase explicitly changes only the intended private-lab layer.
- Exclude ID 18.
- Exclude NEEDS_REVIEW items 807 and 809 from the first private lab session pool.
- Preserve all governance invariants: no official scoring, no examiner authority, no pass/fail, no certification-readiness claim, no LLM/API/embedding/vector/cloud path.
- Add a private-lab contract defining scope as RA1 formative practice only.
- Add deterministic session selection so redundant pairs are not shown together by default: 804/817 and 810/812.
- Add feedback wording that frames results as concept coverage and reasoning guidance only.

Recommended:

- Add question-specific formative feedback expectations for READY_WITH_MINOR_GAPS items.
- Map additional causal chains or explicitly mark unmapped chains as native formative chains only.
- Add a small private dry-run fixture covering one session with foundational, intermediate, and distinction items.
- Add lab-level documentation that the current set is not a full WSET L3 open-response bank.

Optional:

- Add RA2/RA3 open-response candidates in later phases.
- Add SAT quality/readiness open-response practice after separate governance review.
- Add sequencing metadata for topic rotation and difficulty progression.
- Add human-review notes for commercial/quality/price-sensitive items.

## Minimal Future Open Response Lab Design

Recommended session size: 5 questions. Use one foundational, two intermediate, one distinction, and one adaptive challenge or review item. For a first private lab, draw from READY items first and include at most one READY_WITH_MINOR_GAPS item per session.

Selection rules should avoid redundancy. Do not pair 804 with 817 in the same short session. Do not pair 810 with 812 unless the session is explicitly about water stress. Do not pair 803, 809, and 813 together unless the session is explicitly about yeast.

Feedback should be formative and deterministic. It should report present concepts, missing concepts, weak causal links, and a revision suggestion. It must not assign marks, grades, pass/fail status, examiner judgement, or certification readiness. The feedback should distinguish "mentioned the term" from "explained the causal link" wherever the deterministic rubric can do so.

Causal-chain integration should be used as explanatory scaffolding, not as scoring. Existing mapped chains can provide mechanism reminders for soil drainage, oak, maceration, malolactic fermentation, canopy, pruning, and related concepts. Unmapped chains should remain plain formative expectations until reviewed knowledge-map nodes exist.

SBA integration should be complementary. Open-response should use SBA outcomes only to select practice themes or reinforce weak concepts, not to convert open answers into scores. SBA and open-response payloads should remain separate, with no shared official assessment claim.

Governance restrictions are absolute: private only, inactive until explicit activation, training-only, no official WSET question claim, no examiner scoring, no pass/fail, no hidden model calls, no API, no embeddings, no vector database, no cloud service, and no public frontend exposure.

## Final Decision

The 20 approved open-response candidates are ready enough to justify building a private RA1 Open Response Lab after minor lab-level adjustments, but not ready for broad activation, publication, or a full-course WSET L3 open-response product.

Recommended next step: build the private lab only after defining the private-lab governance contract, deterministic session selection, and formative feedback boundaries. Start with READY items and a small subset of READY_WITH_MINOR_GAPS. Keep NEEDS_REVIEW items out of the first activation pool.
