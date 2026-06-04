# Corpus-Grounded Gold Bank

Phase 4A.3.7.32 - Corpus-Grounded Gold Bank Construction

Status: documentary authority artifact only. This document does not activate questions, publish a frontend payload, modify the structured question bank, change answer keys, edit distractors, or alter the dynamic exporter.

## Methodology

The Gold Bank is constructed from the post-remediation official-only corpus audit, not from learner performance, frontend state, unofficial corpus matches, or examiner scoring.

Input artifacts:

- `docs/CORPUS_REMEDIATION_DATASET.json`
- `docs/CORPUS_REMEDIATION_REPORT.md`
- `docs/CORPUS_REMEDIATION_CHANGELOG.md`
- `docs/FULL_BANK_CORPUS_VERIFICATION.json`
- `docs/FULL_BANK_CORPUS_VERIFICATION_SUMMARY.md`
- `docs/DIAGNOSTIC_SBA_MASTER_INVENTORY.md`
- `docs/DIAGNOSTIC_SBA_PHASE_4A_3_7_35_CANONICAL_BASELINE.md`
- `frontend/diagnostic-sba/preguntas.json` for active/elegible cross-check only
- `knowledge/question-bank/structured/wset3_questions.json` for stems, options, difficulty, and answer-position metadata only

Classification rules:

| Class | Meaning |
|---|---|
| Gold-A | Official corpus support is strong; no relevant after-state conflict; distractors are coherent; diagnostic signal is useful; activation risk is low, subject to future non-documentary activation gates. |
| Gold-B | Official corpus support is strong, but the item needs minor editorial review, source-specificity confirmation, RA/topic normalization, or diagnostic metadata hardening before activation. |
| Gold-C | Official corpus support is strong under the deterministic audit, but significant review is needed before activation due to conflict flags, duplicate options, weak source specificity, or semantic fit concerns. |

Important boundary: `after_grounding: STRONG` is necessary for this first Gold Bank, but it is not sufficient for Gold-A. The remediated audit is a deterministic evidence signal; this document adds a conservative governance classification over that signal.

## Base Data

Post-remediation official-only corpus audit:

| Metric | Count |
|---|---:|
| Structurally valid SBA items processed | 524 |
| STRONG | 41 |
| PARTIAL | 219 |
| WEAK | 9 |
| NOT_FOUND | 255 |
| Total after-state distractor conflicts | 14 |
| Active/elegible private static-demo items | 18 |
| Active payload | `frontend/diagnostic-sba/preguntas.json` |
| Exporter | Dynamic scanner |
| Static demo only | true |

The Phase 4A.3.7.35 canonical baseline states that the current active/elegible source IDs are: `2, 4, 5, 12, 15, 17, 20, 30, 44, 50, 78, 83, 87, 108, 247, 253, 386, 510`.

## Gold-A/B/C Classification

Summary:

| Class | Count |
|---|---:|
| Gold-A | 15 |
| Gold-B | 20 |
| Gold-C | 6 |
| Total STRONG reviewed | 41 |

### Top 12 Gold-A

These are the first activation-readiness candidates, but they remain inactive until a later activation phase.

| Rank | Item | RA | Topic signal | Correct | Rationale |
|---:|---|---|---|---|---|
| 1 | Q2 | RA4 | Port fortification | C | Active/elegible; strong official support; no after-state conflict; clear mechanism question. |
| 2 | Q83 | RA1 | Ageability and structure | B | Active/elegible; strong support; solid diagnostic signal around acidity, tannin, balance, and longevity. |
| 3 | Q105 | RA4 | Sherry oxidative complexity | B | Strong fortified-wine support; clean distractor state; useful style discrimination. |
| 4 | Q228 | RA2 | Chianti Classico | B | Region-specific official support; clean state; coherent regional distractors. |
| 5 | Q258 | RA2 | Uco Valley altitude/coolness | B | Region-specific support; clean state; useful South America coverage. |
| 6 | Q265 | RA2 | Central Otago Pinot Noir | C | Region-specific support; clean state; useful New Zealand coverage. |
| 7 | Q287 | RA2 | Barolo structure | B | Strong style-support signal; distractors separate style features well. |
| 8 | Q309 | RA2 | Tokaj botrytis | C | Strong official botrytis support; useful causal bridge to sweet-wine style. |
| 9 | Q356 | RA2 | Sta. Rita Hills / coastal Pinot Noir | C | Region-specific California support; clean state. |
| 10 | Q424 | RA2 | Barossa Valley Shiraz | B | Region-specific Australia support; clean distractor state. |
| 11 | Q659 | RA3 | Brut Nature / no dosage | B | Clean alternative to Q111; supports sparkling label terminology without duplicate options. |
| 12 | Q834 | RA5 | German Pradikat label hierarchy | D | Only STRONG RA5 item; coherent hierarchy distractors; useful label/quality coverage. |

### Top 24 Gold Candidates

Top 24 = ranks 1-12 above plus the next 12 candidates below.

| Rank | Item | Class | RA | Topic signal | Correct | Review note |
|---:|---|---|---|---|---|---|
| 13 | Q269 | Gold-A | RA2 | Vinho Verde | C | Clean region/style item with official Portugal support. |
| 14 | Q438 | Gold-A | RA2 | Willamette Valley Pinot Noir | D | Clean region-specific support; good D-position balance. |
| 15 | Q498 | Gold-A | RA2 | Canopy management / fungal disease | B | Strong viticulture-practice support; useful causal reasoning seed. |
| 16 | Q107 | Gold-B | RA3 | Prise de mousse | C | Strong fermentation support, but term-specific source confirmation should be tightened. |
| 17 | Q206 | Gold-B | RA4 | Port varieties | A | Strong Touriga support, but RA/topic mapping should be normalized before activation. |
| 18 | Q216 | Gold-B | RA3 | Cremant de Loire / Chenin Blanc | A | Clean options, but source specificity should be reviewed because the matched passage is not tightly Cremant-specific. |
| 19 | Q230 | Gold-B | RA1 | Continental-climate red structure | A | Strong SAT-structure support; needs source-specific climate framing. |
| 20 | Q232 | Gold-B | RA2 | Pinot Noir terroir sensitivity | D | Clean D-position item; support is more grape/SAT generic than region-specific. |
| 21 | Q240 | Gold-B | RA3 | Charmat / Prosecco | B | Good concept item; needs tighter method-specific passage review. |
| 22 | Q268 | Gold-B | RA2 | Nebbiolo young style | B | Good style signal; support is SAT-generic and should be tied to Nebbiolo source text. |
| 23 | Q270 | Gold-B | RA2 | Chinon / Cabernet Franc | C | Correct regional-variety association; matched evidence is grape-generic. |
| 24 | Q277 | Gold-B | RA2 | Oregon Pinot Noir | C | Correct association; support should be made more Oregon-specific. |

### Top 36 Gold Candidates

Top 36 = ranks 1-24 above plus ranks 25-36 below.

| Rank | Item | Class | RA | Topic signal | Correct | Review note |
|---:|---|---|---|---|---|---|
| 25 | Q301 | Gold-B | RA2 | Chile / Cabernet Sauvignon | C | Correct association; support is grape-generic and needs Chile-specific confirmation. |
| 26 | Q308 | Gold-B | RA2 | Marlborough Sauvignon Blanc | C | Correct association; support is grape-generic and needs Marlborough-specific confirmation. |
| 27 | Q325 | Gold-B | RA2 | Loire Sauvignon Blanc | C | Correct association; source specificity should be tightened. |
| 28 | Q395 | Gold-B | RA2 | Maipo Cabernet Sauvignon profile | B | Good style signal; support is SAT-structure heavy. |
| 29 | Q402 | Gold-B | RA2 | Douro / Touriga Nacional | C | Correct variety signal; matched passage should be checked for Douro-specificity. |
| 30 | Q421 | Gold-B | RA2 | Ribera del Duero climate effect | C | Good causal style signal; support is SAT-generic. |
| 31 | Q440 | Gold-B | RA1 | Chablis / avoiding MLF | C | Useful winemaking-style question; source support should be narrowed. |
| 32 | Q441 | Gold-B | RA2 | Medoc red structure | B | Good style signal; support is SAT-generic. |
| 33 | Q464 | Gold-B | RA2 | Destemming and green tannin | A | Useful causal winemaking signal; RA should be normalized toward winemaking/RA1 or RA3 before activation. |
| 34 | Q493 | Gold-B | RA1 | Late harvest frost exposure | B | Good causal viticulture signal; matched file context should be reviewed. |
| 35 | Q515 | Gold-B | RA1 | Open vats / malolactic fermentation | A | Requires editorial check that the vessel-to-fermentation link is not over-inferred. |
| 36 | Q21 | Gold-C | RA3 | Cremant de Loire / Chenin Blanc | C | Strong label exists, but source specificity and distractor strength require significant review. |

### Full STRONG Ranking

| Rank | Item | Class | RA | Correct | Active/elegible | Main reason |
|---:|---|---|---|---|---|---|
| 1 | Q2 | Gold-A | RA4 | C | Yes | Strong mechanism support; clean; already private eligible. |
| 2 | Q83 | Gold-A | RA1 | B | Yes | Strong ageability/structure support; clean; already private eligible. |
| 3 | Q105 | Gold-A | RA4 | B | No | Strong fortified style support; clean. |
| 4 | Q228 | Gold-A | RA2 | B | No | Region-specific support; clean. |
| 5 | Q258 | Gold-A | RA2 | B | No | Region-specific support; clean. |
| 6 | Q265 | Gold-A | RA2 | C | No | Region-specific support; clean. |
| 7 | Q287 | Gold-A | RA2 | B | No | Strong style profile; clean. |
| 8 | Q309 | Gold-A | RA2 | C | No | Botrytis causal signal; clean. |
| 9 | Q356 | Gold-A | RA2 | C | No | California regional support; clean. |
| 10 | Q424 | Gold-A | RA2 | B | No | Australia regional support; clean. |
| 11 | Q659 | Gold-A | RA3 | B | No | Sparkling label terminology; clean. |
| 12 | Q834 | Gold-A | RA5 | D | No | RA5 label hierarchy support; clean. |
| 13 | Q269 | Gold-A | RA2 | C | No | Portugal regional style support; clean. |
| 14 | Q438 | Gold-A | RA2 | D | No | Oregon regional support; clean. |
| 15 | Q498 | Gold-A | RA2 | B | No | Canopy management causal support; clean. |
| 16 | Q107 | Gold-B | RA3 | C | No | Needs term-specific source review. |
| 17 | Q206 | Gold-B | RA4 | A | No | Needs RA/topic normalization. |
| 18 | Q216 | Gold-B | RA3 | A | No | Needs Cremant-specific source review. |
| 19 | Q230 | Gold-B | RA1 | A | No | Good style reasoning; generic support. |
| 20 | Q232 | Gold-B | RA2 | D | No | Good D-position item; generic support. |
| 21 | Q240 | Gold-B | RA3 | B | No | Needs Charmat-specific passage check. |
| 22 | Q268 | Gold-B | RA2 | B | No | Good style item; generic support. |
| 23 | Q270 | Gold-B | RA2 | C | No | Correct association; generic grape evidence. |
| 24 | Q277 | Gold-B | RA2 | C | No | Correct association; source specificity needed. |
| 25 | Q301 | Gold-B | RA2 | C | No | Correct association; Chile-specific support needed. |
| 26 | Q308 | Gold-B | RA2 | C | No | Correct association; Marlborough-specific support needed. |
| 27 | Q325 | Gold-B | RA2 | C | No | Correct association; Loire-specific support needed. |
| 28 | Q395 | Gold-B | RA2 | B | No | Good profile signal; SAT-generic support. |
| 29 | Q402 | Gold-B | RA2 | C | No | Correct association; Douro-specific support needed. |
| 30 | Q421 | Gold-B | RA2 | C | No | Good causal style signal; generic support. |
| 31 | Q440 | Gold-B | RA1 | C | No | Useful style/winemaking signal; source narrowing needed. |
| 32 | Q441 | Gold-B | RA2 | B | No | Good style signal; generic support. |
| 33 | Q464 | Gold-B | RA2 | A | No | Useful causal signal; RA normalization needed. |
| 34 | Q493 | Gold-B | RA1 | B | No | Useful risk signal; source context check needed. |
| 35 | Q515 | Gold-B | RA1 | A | No | Possible over-inference; editorial check needed. |
| 36 | Q21 | Gold-C | RA3 | C | No | Source specificity too weak for activation. |
| 37 | Q111 | Gold-C | RA3 | C | No | Duplicate option text appears in A and C; must not activate unchanged. |
| 38 | Q229 | Gold-C | RA2 | C | No | Hawke's Bay claim matched to generic red-winemaking evidence. |
| 39 | Q353 | Gold-C | RA2 | C | No | Etna Rosso claim matched to generic SAT structure evidence. |
| 40 | Q361 | Gold-C | RA2 | C | No | After-state distractor conflict and HUMAN_REVIEW status. |
| 41 | Q367 | Gold-C | RA3 | C | No | Champagne frost claim matched to Bordeaux-context file; needs significant review. |

## Coverage Validation

### RA Coverage

| Set | RA1 | RA2 | RA3 | RA4 | RA5 |
|---|---:|---:|---:|---:|---:|
| Top 12 Gold-A | 1 | 8 | 1 | 2 | 1 |
| Top 24 | 2 | 14 | 4 | 3 | 1 |
| Top 36 | 5 | 22 | 5 | 3 | 1 |
| Full STRONG 41 | 5 | 25 | 7 | 3 | 1 |

Note: Q2 is tagged `UNKNOWN` in the remediated dataset but is RA4 in the active payload and review lineage. It is counted as RA4 here for pedagogical coverage.

### Topic Coverage

| Topic group | Items | Coverage assessment |
|---|---|---|
| Fortified wines / Port / Sherry | Q2, Q105, Q206 | Good small cluster; Q2 and Q105 are strongest. |
| Sparkling wines | Q21, Q107, Q111, Q216, Q240, Q367, Q659 | Present but uneven; only Q659 is Gold-A. |
| Regional still wines | Q228, Q258, Q265, Q269, Q270, Q277, Q301, Q308, Q325, Q356, Q402, Q424, Q438 | Strongest overall area, mostly RA2. |
| Style and quality profile | Q83, Q230, Q268, Q287, Q353, Q395, Q421, Q441 | Useful diagnostic area, but many matches are SAT-generic. |
| Viticulture / climate / disease | Q309, Q493, Q498 | Underrepresented but important for causal reasoning. |
| Winemaking and maturation | Q440, Q464, Q515 | Present, but all require review before activation. |
| Label law / category hierarchy | Q834 | One strong RA5 candidate only. |
| Service / storage / commercial price | None in STRONG | Major Gold-A gap. |

### Subtopic Coverage

| Subtopic signal | Items | Status |
|---|---|---|
| Port fortification stops fermentation | Q2 | Gold-A |
| Sherry oxidative complexity | Q105 | Gold-A |
| Ageability: acidity, tannin, balance | Q83 | Gold-A |
| Italy: Chianti, Barolo, Etna | Q228, Q287, Q353 | Mixed: two strong candidates, one Gold-C. |
| New Zealand / Australia / Oregon / California regions | Q265, Q356, Q424, Q438 | Strong regional spread. |
| Germany Pradikat hierarchy | Q834 | Only RA5 Gold-A. |
| Sparkling dosage / terminology | Q659, Q111 | Q659 usable; Q111 blocked by duplicate option text. |
| Charmat / prise de mousse / Cremant | Q107, Q216, Q240, Q21 | Needs source-specific review. |
| Viticulture causal signals | Q309, Q493, Q498 | Good candidates for future causal-chain enrichment. |
| Storage/service | None | No STRONG Gold candidate. |
| Price/commercial route-to-market | None | No STRONG Gold candidate. |

### Difficulty Coverage

All 41 STRONG items are `intermediate` in the structured bank except Q2, which appears as `foundational` in the active payload. The Gold Bank therefore does not yet provide a reliable Pass/Merit/Distinction spread. A future enrichment phase should assign difficulty based on cognitive demand rather than inherited source-bank uniformity.

### Correct Option Coverage

| Set | A | B | C | D | Assessment |
|---|---:|---:|---:|---:|---|
| Top 12 Gold-A | 0 | 6 | 5 | 1 | Better than full bank, but still lacks A. |
| Top 24 | 3 | 10 | 8 | 3 | Acceptable for a documentary candidate set; still B/C heavy. |
| Top 36 | 5 | 13 | 15 | 3 | C-bias reappears. |
| Full STRONG 41 | 5 | 13 | 20 | 3 | Positional bias remains material. |

No option shuffling is authorized in this phase.

## Relation To The 18 Active/Elegible Items

Current active/elegible private items remain `static_demo_only: true`; this document does not change that status.

| Active source ID | Current grounding | Gold classification | Recommendation |
|---|---|---|---|
| Q2 | STRONG | Gold-A | Keep as private demo/elegible; also include in Gold Bank candidate record. |
| Q4 | PARTIAL | Not Gold | Keep private demo only; promote only after official-source strengthening. |
| Q5 | PARTIAL + conflict | Not Gold | Keep private demo only at most; conflict/HUMAN_REVIEW makes it unsuitable for Gold. |
| Q12 | PARTIAL | Not Gold | Keep private demo only; good topic, but no longer STRONG after remediation. |
| Q15 | NOT_FOUND | Not Gold | Keep private demo only; do not promote. |
| Q17 | PARTIAL + conflict | Not Gold | Keep private demo only at most; conflict/HUMAN_REVIEW makes it unsuitable for Gold. |
| Q20 | NOT_FOUND | Not Gold | Keep private demo only; do not promote. |
| Q30 | PARTIAL | Not Gold | Keep private demo only; good future promotion candidate. |
| Q44 | PARTIAL | Not Gold | Keep private demo only; service/food-pairing candidate for future promotion. |
| Q50 | NOT_FOUND | Not Gold | Keep private demo only; storage support gap. |
| Q78 | NOT_FOUND | Not Gold | Keep private demo only; storage support gap. |
| Q83 | STRONG | Gold-A | Keep as private demo/elegible; also include in Gold Bank candidate record. |
| Q87 | NOT_FOUND | Not Gold | Keep private demo only; storage support gap. |
| Q108 | NOT_FOUND | Not Gold | Keep private demo only; Charmat support gap. |
| Q247 | PARTIAL | Not Gold | Keep private demo only; high-priority PARTIAL promotion candidate. |
| Q253 | PARTIAL | Not Gold | Keep private demo only; high-priority PARTIAL promotion candidate. |
| Q386 | PARTIAL | Not Gold | Keep private demo only; high-priority PARTIAL promotion candidate. |
| Q510 | NOT_FOUND | Not Gold | Keep private demo only; noble-rot support gap. |

Only 2 of the 18 active/elegible private items are in this first Gold Bank: Q2 and Q83, both Gold-A. The other 16 should not be represented as Gold until their official-corpus grounding improves and any conflict signals are resolved.

## Gaps

Areas without Gold-A:

- RA3 beyond the narrow Brut Nature / dosage item Q659.
- RA1 viticulture and winemaking, except the ageability-style item Q83.
- RA5 storage, service, commercial channels, and price factors.
- Explicit food-pairing/service questions.
- Price and route-to-market reasoning.
- Multi-step causal reasoning with causal-chain metadata.
- Balanced answer-position distribution, especially A and D in the Top 12.

Areas with only PARTIAL support:

- Active RA2 regional questions Q247, Q253, Q386.
- Active service/food/storage questions Q44, Q50, Q78, Q87.
- Active sparkling method/autolysis question Q30.
- RA5 legal/category items Q820, Q822, Q824, Q827, Q836, Q837, Q852.
- Many high-value RA2 region/style items in Mosel, Barolo, Chablis, Sauternes, Priorat, Bordeaux, Rioja, and Napa.

Areas where NOT_FOUND dominates:

| RA | NOT_FOUND / total | Risk |
|---|---:|---|
| RA1 | 115 / 176 | Many viticulture/service-adjacent items lack official-only support under the current audit. |
| RA5 | 28 / 38 | Critical gap for storage, service, label/commercial, and price coverage. |
| RA3 | 26 / 64 | Sparkling and method terminology still needs corpus alignment. |
| RA4 | 11 / 27 | SAT and fortified style support remains thin outside a few items. |
| RA2 | 75 / 209 | Better than other RAs, but many region items still need official-corpus anchoring. |

Pending conflict/discard queue:

| Item | Status | Reason |
|---|---|---|
| Q5 | HUMAN_REVIEW | Oloroso/Amontillado distractor ambiguity remains. |
| Q17 | HUMAN_REVIEW | Despalillado vs malolactic distractor signal remains. |
| Q252 | HUMAN_REVIEW | Syrah distractor signal remains. |
| Q263 | HUMAN_REVIEW | Syrah distractor signal remains. |
| Q328 | HUMAN_REVIEW | Malolactic fermentation distractor signal remains. |
| Q361 | HUMAN_REVIEW | Santa Barbara distractor signal remains; included only as Gold-C. |
| Q405 | HUMAN_REVIEW | Gran Reserva distractor signal remains. |
| Q409 | HUMAN_REVIEW | Barossa Valley distractor signal remains. |
| Q414 | HUMAN_REVIEW | Walker Bay distractor signal remains. |
| Q416 | HUMAN_REVIEW | Syrah distractor signal remains. |
| Q218 | DISCARD | Champagne/Charmat conflict. |
| Q370 | DISCARD | Barossa Valley conflict. |
| Q661 | DISCARD | Chardonnay conflict. |
| Q823 | DISCARD | AOP/DOP category conflict. |

## PARTIAL Promotion Priorities

Recommended promotion work should not edit answers or distractors in this phase. The next phase should strengthen official-corpus support, add or confirm source passages, and then re-run the evidence audit.

High-priority PARTIAL candidates:

| Priority | Item | RA | Coverage reason | Current reason to promote later |
|---:|---|---|---|---|
| 1 | Q247 | RA2 | Mosel / cool climate / acidity | Active private item; fills region plus causal climate gap. |
| 2 | Q253 | RA2 | Barolo / Nebbiolo / ageing | Active private item; fills high-value region/style gap. |
| 3 | Q386 | RA2 | Mosel vs Pfalz Riesling | Active private item; fills regional comparison gap. |
| 4 | Q44 | RA1/RA5-adjacent | Food pairing | Active private item; service/consumer gap. |
| 5 | Q30 | RA3 | Traditional method autolysis | Active private item; sparkling method gap. |
| 6 | Q852 | RA5 | Magnum ageing/storage | Strong service/storage causal candidate. |
| 7 | Q837 | RA5 | Bordeaux 1855 classification | Quality/price and label-literacy candidate. |
| 8 | Q824 | RA5 | DOCG hierarchy | Label-law candidate with coherent topic value. |
| 9 | Q820 | RA5 | DOP hierarchy | Label-law candidate; useful RA5 coverage. |
| 10 | Q55 | RA5 | Volatile acidity defect | Service/SAT defect bridge. |
| 11 | Q725 | RA5 | Volatile acidity defect | Redundant with Q55; choose one in future. |
| 12 | Q246 | RA2 | Sancerre style | Region/style gap with common WSET relevance. |
| 13 | Q256 | RA2 | Chablis profile | Region/style gap with high WSET relevance. |
| 14 | Q350 | RA2 | Sauternes / botrytis | Sweet-wine causal gap. |
| 15 | Q388 | RA2 | Bordeaux maritime climate | Region plus causal climate gap. |
| 16 | Q412 | RA2/RA5-adjacent | Napa price factor | Quality/price gap, but needs careful price-causality support. |
| 17 | Q439 | RA2 | Mosel slope/orientation | Causal terroir candidate. |

Promotion themes:

- RA2: prioritize region questions where the correct answer requires climate, grape, or style reasoning rather than pure name recall.
- RA5: prioritize storage/service/price because the current STRONG set has only one RA5 item and it is label hierarchy, not service or commercial reasoning.
- Causal reasoning: prioritize items with climate-to-style, method-to-sensory, or storage-to-ageing chains.
- Quality/price: prioritize items where the corpus explicitly supports production cost, scarcity, reputation, or distribution effects.

## Risks

- The Gold Bank is corpus-grounded, not examiner-authorized.
- Several STRONG items are supported by broad SAT or grape passages rather than tightly matched regional passages.
- Positional answer bias remains, especially C-heavy in the full STRONG set.
- RA and topic labels are inconsistent across the structured bank, remediated dataset, and active payload for some items.
- Active/elegible does not mean Gold; 16 of the 18 active private items are not Gold under this stricter audit.
- Gold-C items must not be activated unchanged.

Governance invariants remain unchanged:

```text
safe_for_examiner = False
examiner_scoring_allowed = False
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

## Recommended Next Phase

Recommended next phase: Phase 4A.3.7.36 - PARTIAL Promotion and Source-Specific Evidence Hardening.

Scope should be documentation/data-audit first:

1. Promote a small, coverage-driven PARTIAL batch, starting with Q247, Q253, Q386, Q852, Q837, Q824, Q820, Q30, and Q44.
2. Require source-specific official passages, not broad SAT or grape-generic matches.
3. Resolve the 14 after-state conflict/discard signals before any activation expansion.
4. Keep the dynamic exporter and current payload untouched until a separate activation phase.
5. Add a future option-position balancing plan, but do not shuffle options without an explicit activation/remediation phase.

Activation recommendation for this phase: none. The Gold Bank should remain a documentary candidate bank only.
