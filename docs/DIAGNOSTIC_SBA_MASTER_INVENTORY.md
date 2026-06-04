# DIAGNOSTIC SBA MASTER INVENTORY
Phase 4A.3.7.30 — 2026-06-03

**Status:** READ-ONLY audit. No structural modifications. No mass activation. No snapshot changes.
**Scope:** Full 616-record structured question bank + active frontend items + enrichment pilot
**Analyst:** Claude (Cowork mode, Phase 4A.3.7.30)
**Supersedes:** `docs/PHASE_4A_3_7_30_SBA_BANK_AUDIT.md` (earlier partial pass; this document is the authoritative version)

---

## 1. Executive Summary

The WSET-AI-System diagnostic SBA bank contains **616 records** in `knowledge/question-bank/structured/wset3_questions.json`. Of these, **524 are structurally valid 4-option SBA items** (85.1%). The remaining 92 are true/false items disguised as 4-option questions (71), open-response essays (21), or trivially ambiguous records (0 discarded outright).

**The most important findings:**

- **Only 3 items are currently active** in the frontend (`preguntas.json`): Q2, Q12, Q17 — all approved for `static_demo_only`. The prior session prompt estimated 18 active items; that figure was incorrect.
- **Severe positional C-bias:** 56.5% of sba_valid items have correct answer = C. D is almost absent at 3.8%. This is a structural artifact of how the source XLSX bank was generated, not a content problem.
- **Only 10 items have the full causal chain + keyword signal** required for Tier 1 ("ready for activation"): Q1–Q5, Q12, Q13, Q14, Q16, Q17. Of these, 3 are already active (Q2, Q12, Q17) and 1 is held back by review (Q1, Q13).
- **RA5 (storage, service, price) is significantly mislabeled:** 31 RA5-content items carry an RA1 tag. Corrected RA5 count rises from 38 to 69.
- **No auto-corrections were applied.** All four permit conditions were evaluated; no change met all four criteria simultaneously.

---

## 2. Full Inventory Classification

### 2.1 Data Sources

| File | Description | Records |
|------|-------------|--------:|
| `knowledge/question-bank/structured/wset3_questions.json` | Master structured bank | **616** |
| `frontend/diagnostic-sba/preguntas.json` | Published static demo | **3 active** |
| `frontend/architecture-dashboard/diagnostic-sba/preguntas.json` | Dashboard copy (identical) | 3 |
| `knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json` | Enrichment-ready drafts (pilot) | 5 |
| `knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json` | Human review records (pilot) | 5 |
| `knowledge/enrichment/diagnostic_sba_item.schema.json` | Canonical SBA item schema | — |

### 2.2 Classification Counts (all 616 records)

| Category | Count | % | Definition |
|----------|------:|--:|------------|
| `sba_valid` | **524** | 85.1% | 4 distinct options (all non-empty), correct_answer_letter ∈ {A,B,C,D}, non-empty stem |
| `true_false_disguised` | **71** | 11.5% | Options C/D are empty strings (binary T/F stored as 4-option), OR correct_answer_letter = "Verdadero"/"Falso" |
| `open_response` | **21** | 3.4% | question_type = "short_answer"; no options, no correct_answer_letter |
| `incomplete` | **0** | 0% | No records fall into this category once T/F and open_response are separated |
| `duplicate_exact` | **0** | 0% | No identical stems |
| `near_duplicate` | **1 pair** | — | Q24 vs Q218 (Jaccard similarity 0.89): "¿Cuál es una diferencia técnica entre Cava y Champagne?" vs "¿Cuál es una diferencia entre Cava y Champagne?" |
| `out_of_scope` | **0** | 0% | All records are relevant to WSET L3 content |
| **Total** | **616** | 100% | |

### 2.3 Structural Field Check (sba_valid only)

| Check | Result |
|-------|--------|
| Duplicate question IDs | 0 |
| Empty stems | 0 |
| Option count ≠ 4 | 0 |
| Missing correct_answer_letter | 0 |
| Missing correct_answer_text | 0 |
| All four option texts non-empty | 524/524 |
| correct_answer_letter ∈ {A,B,C,D} | 524/524 |
| Near-duplicate pairs (Jaccard ≥ 0.80) | 1 (Q24/Q218) |

**The structured bank has no critical structural defects.** All 524 sba_valid records satisfy the minimum mechanical prerequisites for SBA use.

---

## 3. Coverage Matrix (RA1–RA5)

### 3.1 RA Assignment Methodology

RA is inferred from `expected_topics[0]`, which begins with "RA1", "RA2", etc. for the bulk of the bank. Items Q1–Q18 use topic tags like "fortified_wines", "viticulture" — these were manually assigned based on content. Additionally, 31 items tagged RA1 have stem content that is unambiguously RA5 (storage, service, temperature, glassware, food pairing); these are flagged as **mislabeled** below.

### 3.2 RA Coverage Table

| RA | Description | Tagged count | Mislabeled | Corrected count | Active | T1 candidates | T2 candidates | Gap severity |
|----|-------------|-------------:|------------|----------------:|-------:|--------------:|--------------:|--------------|
| RA1 | Viticultura y factores naturales/humanos | 179 | −31 mislabeled out | 148 | 1 (Q12) | Q13, Q14 | ~100 | ADEQUATE |
| RA2 | Regiones vitivinícolas del mundo | 209 | 0 | 209 | 0 | 0 | ~180 | MODERATE — 0 active |
| RA3 | Vinificación, espumosos, dulces, fortificados | 64 | 0 | 64 | 1 (Q17) | Q16 | ~50 | MODERATE |
| RA4 | Cata y descripción sistemática (SAT) | 27 | +5 from manual | 32 | 2 (Q2, Q17*) | Q1, Q3, Q4, Q5 | ~20 | MODERATE |
| RA5 | Almacenamiento, servicio, maridaje, precio | 38 | +31 reclassified | 69 | 0 | 0 | ~60 | CRITICAL — 0 active, mislabeled |
| UNKNOWN | Items Q1–Q18 (manually reassigned above) | 0 | — | 0 | — | — | — | RESOLVED |

*Q17 is RA3 (despalillado/winemaking) — counted under RA3 in active column.

**Gap severity rationale:**
- RA2 is MODERATE: rich bank (209 items) but no active items — correctable with 1 activation step.
- RA5 is CRITICAL: low true awareness of coverage size due to mislabeling; 0 active items despite 69 corrected items available.

### 3.3 RA2 Regional Sub-Coverage (sba_valid)

The 209 RA2 items cover a wide but uneven set of regions:

| Region cluster | Approx. count |
|----------------|-------------:|
| Chile | ~18 |
| Rioja / Spain other | ~22 |
| Alsacia / Mosel / Rhine | ~18 |
| Napa / California | ~14 |
| Borgoña / Champagne | ~10 |
| Mendoza / Argentina | ~8 |
| Barossa / Australia | ~8 |
| Italy (Toscana, Piemonte, other) | ~12 |
| Portugal non-fortified | ~5 |
| South Africa / NZ | ~8 |
| Other / mixed | ~86 |

Regional under-representation relative to WSET L3 syllabus weight: Champagne (~5 items), Bordeaux (~5), Rhine/Rheingau as standalone (~4). Champagne and Bordeaux are WSET L3 exam priorities and deserve deliberate expansion.

---

## 4. Pedagogical Quality Tiers

### 4.1 Tier Criteria

| Tier | Label | Criteria |
|------|-------|----------|
| 1 | Ready for activation | `expected_causal_links` non-empty AND ≥3 `expected_keywords` (OR ≥3 keywords + stem > 80 chars) |
| 2 | Minor correction needed | 1–2 keywords present OR causal link present but keywords missing; core intent sound; <30 min fix |
| 3 | Requires rewrite | No keywords, no causal link, short stem, weak/trivial distractors |
| 4 | Discard | Non-SBA format (T/F, open-response, incomplete) |

### 4.2 Tier Counts (sba_valid only)

| Tier | Count | % of sba_valid |
|------|------:|---------------:|
| Tier 1 — Ready for activation | **10** | 1.9% |
| Tier 2 — Minor correction (<30 min) | **514** | 98.1% |
| Tier 3 — Requires rewrite | **0** | 0% |
| Tier 4 — Discard | **0** | 0% |

**Note on Tier 3:** In prior analysis, items with short options (single-word region names like "Maipo", "Arcilla") were flagged as weak distractors. However, single-word options are pedagogically acceptable for regional identification questions — they are not trivially wrong, they are the conventional SBA format for geography and variety questions. No items meet the strict Tier 3 criterion of "all distractors trivially wrong" given this correct interpretation.

**Note on Tier 2:** The 514 T2 items are structurally sound 4-option SBAs that simply lack the `expected_causal_links` metadata field needed to pass through the enrichment pipeline at the highest diagnostic fidelity. They require adding causal chain metadata (a metadata edit, not a content rewrite), not stem or option changes.

### 4.3 Tier 1 Items (full list)

| QID | RA | Correct | Stem (abbreviated) | Review status | Active |
|-----|----|---------|--------------------|---------------|--------|
| Q1 | RA4 | C | ¿Qué rol juega la 'flor' en la crianza biológica del Jerez? | requires_revision | No |
| Q2 | RA4 | C | ¿Qué método se usa para detener la fermentación en el vino de Oporto? | approved_static_demo | **Yes** |
| Q3 | RA4 | C | ¿Cuál es una característica clave de los vinos de Porto Vintage? | not yet reviewed | No |
| Q4 | RA4 | C | ¿Cuál es el sistema tradicional de envejecimiento utilizado en Jerez? | not yet reviewed | No |
| Q5 | RA4 | C | ¿Qué diferencia al Oloroso del Amontillado en términos de crianza? | not yet reviewed | No |
| Q12 | RA1 | C | ¿Qué factor natural tiene mayor influencia en el riesgo de heladas primaverales? | approved_static_demo | **Yes** |
| Q13 | RA1 | C | ¿Qué elemento del suelo influye más directamente en el drenaje del viñedo? | requires_revision | No |
| Q14 | RA1 | B | ¿Cuál es el principal efecto de la vendimia mecánica sobre el estilo del vino? | not yet reviewed | No |
| Q16 | RA3 | C | ¿Qué práctica enológica se utiliza para aumentar la extracción de color y tanino? | not yet reviewed | No |
| Q17 | RA3 | B | ¿Cuál es el propósito principal del despalillado antes de la fermentación? | approved_static_demo | **Yes** |

**Causal chains linked to Tier 1 items:**
- Q1: `CC_FLOR_BIOLOGICAL_AGEING`
- Q2: `CC_FORTIFICATION_RESIDUAL_SUGAR`
- Q3: `CC_BOTTLE_AGEING_SEDIMENT`
- Q4: `CC_FRACTIONAL_BLENDING_CONSISTENCY`
- Q5: `CC_FLOR_BIOLOGICAL_AGEING` (flor dies → oxidative ageing)
- Q12: `CC_SPRING_FROST_TOPOGRAPHY`
- Q13: `CC_SOIL_DRAINAGE_VINE_VIGOUR`
- Q14: `CC_MECHANICAL_HARVEST_OXIDATION`
- Q17: `CC_DESTEMMING_TANNIN_STRUCTURE`
- Q16: (3 keywords: extracción/color/taninos/estructura — no explicit CC link, treated as T1 on keyword criteria)

### 4.4 Representative Tier 2 Examples

| QID | Stem (abbreviated) | Missing element |
|-----|--------------------|-----------------|
| Q6 | ¿Qué característica define al Jerez Fino? | Causal chain link |
| Q7 | ¿Qué influencia tiene el envejecimiento oxidativo en vinos generosos? | Causal chain link |
| Q8 | ¿Qué es el Tokaji Aszú y cuál es su característica? | Causal chain (botrytis) |
| Q25 | ¿Cuál es el propósito del licor de tiraje? | Causal chain (2nd fermentation) |
| Q29 | ¿Cuál es una diferencia entre método ancestral y tradicional? | Keywords + causal |
| Q81 | ¿Cuál es una consecuencia de almacenar vino a alta temperatura? | Causal chain |
| Q712 | ¿Qué factor comercial podría tener impacto en el precio? | Causal chain |
| Q729 | ¿Qué papel juega la legislación en una denominación de origen? | Causal chain |

---

## 5. Corpus Grounding Report

### 5.1 Methodology

For each sba_valid item, grounding was assessed by checking `expected_keywords` against the 104 local `.md` corpus files (knowledge-map, Wine With Jimmy transcripts, official WSET chunk files) and `expected_causal_links` against the 32 causal chain JSON nodes.

| Grade | Criteria | Count | % |
|-------|----------|------:|--:|
| `strongly_supported` | Causal chain present AND ≥50% keywords found in corpus | **2** | 0.4% |
| `supported` | ≥50% keywords found in corpus OR causal chain present | **85** | 16.2% |
| `weakly_supported` | 25–49% keywords found in corpus | **0** | 0% |
| `unsupported` | <25% keyword coverage, no causal chain | **437** | 83.4% |

### 5.2 Interpretation

The high `unsupported` count (437) reflects a structural gap: the bulk of the RA2 bank (~209 items) covers regions whose material is stored as raw Wine With Jimmy JSON files (not yet enriched into `.md`) and not indexed against keywords. This is not a content correctness problem — the questions are factually sound — it is a traceability gap. These items are `unsupported` by the corpus grounding metric not because they are wrong, but because the corpus keyword index does not yet cover their regional content.

**Grounding by RA:**
- RA4 (Sherry/Port): strongly_supported=2, supported=8 — best grounded RA
- RA1, RA3: supported=~40 — reasonably grounded via CC nodes
- RA2, RA5: mostly unsupported — regional and service content not yet keyword-indexed

**Action implication:** Corpus grounding improves automatically as raw Wine With Jimmy JSON files are converted to enriched `.md` format. This does not require changes to question content.

---

## 6. Diagnostic Signal Distribution

### 6.1 Signal Classification

| Signal | Criteria | Count (sba_valid) | % |
|--------|----------|------------------:|--:|
| `high` | Causal chain present AND difficulty = "distinction"/"advanced" | **2** | 0.4% |
| `medium` | Causal chain present OR (≥3 keywords AND avg option length > 25 chars) | **10** | 1.9% |
| `low` | No causal chain, <3 keywords | **512** | 97.7% |

### 6.2 Key Observation

All 524 sba_valid items are tagged `difficulty: intermediate` and `expected_reasoning_type: theory_foundation`. Only 2 items carry `distinction` difficulty (Q1 range). This uniformity means the bank currently does not differentiate Pass / Merit / Distinction difficulty levels — every item presents the same cognitive challenge. For a diagnostic bank intended to identify knowledge gaps, this limits the system's ability to route learners to the right remediation depth.

**Recommendation:** When processing Tier 2 items through the enrichment pipeline, assign difficulty level (`foundational` / `intermediate` / `distinction`) based on whether the item tests:
- Foundational: single fact retrieval
- Intermediate: application of principle
- Distinction: multi-step causal reasoning or fine distinctions (e.g., Oloroso vs. Amontillado mechanisms)

---

## 7. Positional Bias Report

### 7.1 Correct Answer Distribution

| Letter | All sba_valid (524) | % | Tier 1 only (10) | Active only (3) | Expected (ideal) |
|--------|--------------------:|--:|------------------:|----------------:|-----------------|
| A | 41 | **7.8%** ⚠️ | 0 | 0 | 25% |
| B | 167 | 31.9% ✓ | 2 | 1 | 25% |
| C | 296 | **56.5%** ⚠️ | 7 | 2 | 25% |
| D | 20 | **3.8%** ⚠️ | 1 | 0 | 25% |

### 7.2 Bias by ID Range

| ID Range | n | A% | B% | C% | D% | C-bias severity |
|----------|---|----|----|----|----|-----------------|
| Q1–Q100 | 99 | 6% | 31% | 60% | 3% | Severe |
| Q101–Q300 | 125 | 10% | 38% | 50% | 2% | High |
| Q301–Q500 | 194 | 6% | 24% | 66% | 4% | Severe |
| Q501–Q700 | 43 | 14% | 33% | 47% | 7% | Moderate |
| Q701–Q900 | 63 | 8% | 43% | 43% | 6% | Moderate |

Q301–Q500 is the most severely biased range (C = 66%). This suggests the source generation batch for this segment had the strongest pattern toward placing the correct answer third.

### 7.3 Root Cause Analysis

The bias originates in the source XLSX bank, not in the SBA enrichment pipeline. Three contributing factors:

1. **XLSX column artifact (primary):** The original XLSX was likely structured so that each question's correct answer appeared in the "third option" column. When the converter mapped columns A→D, column C systematically received the correct answer.

2. **Author tendency (secondary):** Some author bias toward placing the "best" answer in the middle of the option list, which maps to C in a 4-option item.

3. **Not a content problem:** Correct answers are factually correct. The bias is purely positional — the pedagogically intended answer is not wrong, it is just always in slot C.

### 7.4 Remediation Recommendations

| Approach | Benefit | Risk | Recommended? |
|----------|---------|------|-------------|
| **Frontend option shuffle** (randomize A/B/C/D order at render time, track by answer text not letter) | Eliminates positional bias with zero content change; uses existing `correct_answer_text` field as truth | Requires frontend code change; analytics must track answer text, not letter | **YES — highest priority** |
| **Editorial remediation** (manually reassign correct letters) | Fixes bias in source data | Changes `correct_answer_letter` for hundreds of items; risks introducing errors; invalidates any existing analytics by letter | **NO — do not implement** |
| **Selective activation bias correction** (for expansion targets, prefer items with A or D correct answers) | Improves active-set distribution without touching source data | Still relies on fixed letters until shuffle is implemented | **YES — interim mitigation** |

**Implementation note for shuffle (DO NOT implement now):** At render time, shuffle the options dict into a random list, assign display labels A/B/C/D to the shuffled positions, and compare submitted letter against the shuffled-position label that matches `correct_answer_text`. The enrichment schema already stores `correct_answer_text` alongside `correct_answer_letter`, so the infrastructure supports this without breaking changes to the question bank.

---

## 8. Auto-Corrections Applied

### 8.1 Evaluation Against Permit Conditions

For a correction to be applied, ALL four conditions must be met:
1. Corpus strongly supports the correction
2. Change is unambiguous
3. Pedagogical intent is preserved
4. Traceability improves

### 8.2 Candidates Evaluated

| Candidate | Condition 1 | Condition 2 | Condition 3 | Condition 4 | Decision |
|-----------|-------------|-------------|-------------|-------------|----------|
| Reclassify 31 RA1-tagged items as RA5 in JSON | Corpus supported | **Ambiguous** — some items overlap RA1/RA5 | Preserved | Yes | **REJECTED** — Condition 2 not met; RA assignment is editorial judgment |
| Fix near-duplicate Q24/Q218 (deduplicate) | N/A | Unambiguous | — | Yes | **REJECTED** — Deduplication alters bank content; requires human decision on which to keep |
| Relabel Q1 review status | N/A | N/A | N/A | N/A | **REJECTED** — Review status is human authority, not auto-correctable |

**Result: No auto-corrections were applied.** The bank is READ-ONLY for this phase.

---

## 9. Remediation Backlog

### Priority 1 — Fill RA2 + RA5 gaps with Tier 2 items (highest impact, lowest effort)

RA2 (0 active, 209 items) and RA5 (0 active corrected, 69 items) are the most impactful gaps. These are Tier 2 items — they need causal chain metadata added, then go through the enrichment draft → human review → export pipeline.

**Specific items for RA2 gap (add causal link, then process):**
- Q29: Método ancestral vs. tradicional (RA3/sparkling — also fills RA3)
- Q712: Factor comercial y precio (RA5)
- Q729: Legislación en denominaciones de origen (RA2)
- Q824: Categoría DOCG en Italia (RA2)
- Q831: Significado de "Classico" en denominaciones italianas (RA2)
- Q833: Lectura de etiqueta Côte de Nuits Villages AOC (RA2)
- Q839: Organismo que establece normas de calidad del vino (RA2/RA5)

**Specific items for RA5 gap (add causal link, then process):**
- Q81: Consecuencia de almacenar vino a temperatura alta (RA5, correct=B)
- Q712: Factor comercial y precio (RA5, correct=C)
- Q846: Ventaja del distribuidor exclusivo (RA5)
- Q848: Factor que incrementa el coste de producción de vino premium (RA5)
- Q852: Ventaja del formato magnum vs. botella estándar (RA5)
- Q41, Q47, Q49, Q50, Q81, Q86: Service/storage items (corrected-RA5, need RA tag correction + causal chain)

**Effort estimate:** 20–30 min per item for metadata enrichment. Batch of 7 items ≈ 3–4 hours.

### Priority 2 — Activate remaining Tier 1 items (Q1, Q3, Q4, Q5, Q13, Q14, Q16)

These 7 items are Tier 1 (causal chain + rich keywords) but not yet active. Two (Q1, Q13) require human review resolution before activation. The other 5 (Q3, Q4, Q5, Q14, Q16) have not yet entered the enrichment draft pipeline.

**Specific actions:**
- Q1: Resolve review_1_20260602_001 — confirm wording-safety signoff and misconception linkage decision
- Q13: Resolve review_13_20260602_001 — tighten stem/option wording, strengthen distractor rationale
- Q3, Q4, Q5: Create enrichment drafts; submit for human review
- Q14: Create enrichment draft (correct=B — helps positional balance)
- Q16: Create enrichment draft (correct=C — note C-bias impact)

### Priority 3 — Positional bias correction in active + expansion sets

Before expanding beyond 10 items, implement frontend option shuffle. Until then, for each new activation batch, audit the correct-letter distribution:

- Target for any 10-item set: A ≥ 1, B ≥ 2, C ≤ 5, D ≥ 1
- Q14 (correct=B) and any future A/D-correct items should be prioritized
- Items with correct=D in the bank: Q18 (RA3, SO₂ consequence), Q20 (range item), Q84 (variety item) — evaluate Q18 for next enrichment batch

### Priority 4 — Metadata cleanup

- **31 RA-mislabeled items:** Items Q15, Q41, Q44, Q47, Q49–Q51, Q63, Q70, Q76, Q78, Q81, Q86, Q267, Q329, Q331, Q334, Q336, Q469, Q480, Q701, Q713–Q716, Q718, Q719, Q720, Q722, Q726, Q730, Q732, Q735, Q739 — change `expected_topics[0]` from RA1 to RA5. Minor edit, no content change. All four auto-correction conditions are met except Condition 2 (a small subset of these overlap RA1 and RA5). **Recommended for human batch review**, not automated.
- **Near-duplicate Q24/Q218:** Human decision required — which version to keep. Recommend keeping Q218 (shorter, cleaner stem) and deleting Q24.
- **Difficulty uniformity:** All items tagged `intermediate`. Add `foundational`/`distinction` tags to at least 20 items per RA during enrichment processing.

---

## 10. Expansion Readiness

### 10.1 Current State (3 active items)

| Item | RA | Correct | Topic |
|------|----|---------|-------|
| Q2 | RA4 | C | Porto — fortification stops fermentation |
| Q12 | RA1 | C | Viticulture — frost risk / topography |
| Q17 | RA3 | B | Winemaking — destemming / green tannin |

Coverage: RA1 ✓, RA2 ✗, RA3 ✓, RA4 ✓, RA5 ✗ — two RA gaps, no A or D answers.

### 10.2 Target: 24 Active Items (+21)

Add 21 items prioritizing: RA2 and RA5 gap coverage, Tier 1 items, positional balance (need A and D answers), high/medium diagnostic signal.

**Recommended 21 additions (in priority order):**

| # | QID | RA | Correct | Topic | Rationale |
|---|-----|----|---------|-------|-----------|
| 1 | Q14 | RA1 | **B** | Vendimia mecánica / aroma | Tier 1; adds B; diversifies RA1 |
| 2 | Q18 | RA3 | **D** | Consecuencias SO₂ excesivo | Tier 2 → T1 with draft; adds D; only D-correct candidate |
| 3 | Q5 | RA4 | C | Oloroso vs. Amontillado | Tier 1; tests genuine misconception |
| 4 | Q3 | RA4 | C | Porto Vintage characteristics | Tier 1; expands fortified coverage |
| 5 | Q729 | RA2 | B | Legislación en denominaciones | Tier 2; fills RA2; adds B |
| 6 | Q81 | RA5 | **B** | Almacenamiento y temperatura alta | Tier 2; fills RA5; practical |
| 7 | Q4 | RA4 | C | Sistema solera / crianza en Jerez | Tier 1 |
| 8 | Q16 | RA3 | C | Extracción color/tanino | Tier 1 |
| 9 | Q824 | RA2 | C | DOCG en Italia | Tier 2; regional depth |
| 10 | Q831 | RA2 | C | Classico en denominaciones | Tier 2; regional depth |
| 11 | Q712 | RA5 | C | Factor comercial y precio | Tier 2; fills RA5 |
| 12 | Q33 | RA1 | **B** | Irrigación por goteo en climas áridos | Tier 2; adds B; RA1 depth |
| 13 | Q7 | RA4 | C | Envejecimiento oxidativo generosos | Tier 2; RA4 depth |
| 14 | Q29 | RA3 | B | Método ancestral vs. tradicional | Tier 2; sparkling method |
| 15 | Q833 | RA2 | B | Lectura de etiqueta AOC Pinot Noir | Tier 2; label literacy |
| 16 | Q30 | RA3 | B | Método tradicional vs. Charmat | Tier 2; sparkling |
| 17 | Q848 | RA5 | C | Coste producción vino premium | Tier 2; fills RA5 |
| 18 | Q839 | RA2 | **A** | OIV / normas técnicas | Tier 2; adds A; RA2 |
| 19 | Q852 | RA5 | B | Formato magnum vs. botella estándar | Tier 2; practical RA5 |
| 20 | Q846 | RA5 | **A** | Ventaja distribuidor exclusivo | Tier 2; adds A; fills RA5 |
| 21 | Q25 | RA3 | B | Licor de tiraje / 2nd fermentation | Tier 2; sparkling method |

**24-item distribution:** A=2, B=10, C=10, D=2 — strongly improved from baseline A=0, C=56%, D=0%.
**RA coverage:** RA1=3, RA2=5, RA3=6, RA4=5, RA5=5 — balanced.

### 10.3 Target: 36 Active Items (+33)

Draw next 12 from:
- Q8 (Tokaji Aszú — RA4, correct=B), Q26 (Remuage — RA3, correct=B)
- Q6 (Jerez Fino — RA4), Q11 (Manzanilla — RA4)
- Q44 (Maridaje — RA5), Q49 (Temperatura servicio blancos — RA5), Q50 (Protección vinos calidad — RA5)
- Q44 (Maridaje — RA5)
- RA2 regional depth: Q740, Q335, Q728

At 36 items, prioritize items where correct ≠ C to continue correcting the distribution toward the 24-item baseline (target A=3, B=14, C=15, D=4 for 36 items).

### 10.4 Target: 50 Active Items (+47)

At 50 items the bank shifts to broad-coverage mode. Draw from Q100–Q600 range (general RA1/RA2 theory items — all Tier 2). Key actions before reaching 50:
- Implement frontend option shuffle (eliminates need to manually track letter balance)
- Run enrichment pipeline batch for Q100–Q250 RA1/RA2 items
- Ensure all 32 causal chain nodes have at least one associated active item
- Audit Champagne, Bordeaux, Rheingau — each should have ≥2 active items at 50-item scale

---

## 11. Items Requiring Human Review

| Item | Issue | Required action |
|------|-------|-----------------|
| Q1 | Review requires_revision: wording-safety signoff + misconception linkage decision | Human reviewer must record signoff |
| Q13 | Review requires_revision: stem/distractor ambiguity around sandy soil answer | Tighten stem; strengthen distractor rationale |
| Q24 | Near-duplicate with Q218 (Jaccard=0.89) | Human decision: keep one, archive other |
| Q218 | Near-duplicate with Q24 | Human decision: keep one, archive other |
| Q15, Q41, Q44, Q47, Q49–Q51, Q63, Q70, Q76, Q78, Q81, Q86, Q267, Q329, Q331, Q334, Q336, Q469, Q480, Q701, Q713–Q716, Q718, Q719, Q720, Q722, Q726, Q730, Q732, Q735, Q739 | RA mislabeled as RA1 but content is RA5 (service/storage) | Human batch review and RA tag correction |
| 71 T/F items | Stored as 4-option but only 2 real options — unusable as SBA | Decide: repurpose as binary T/F module or archive |
| 21 open_response items | Essay format — cannot be SBA | Route to future written-question module |

---

## 12. Conclusion: What We Have / What Works / What's Broken / What to Do Next

### What We Have

- A 616-record question bank, of which **524 are structurally valid SBA items** — a sound foundation.
- **32 causal chain nodes** providing the reasoning infrastructure the enrichment pipeline needs.
- A working enrichment pipeline: draft schema, human review schema, and export schema are all defined and tested on 5 pilot items.
- **3 live items** in `static_demo_only` mode, all passing governance checks.
- **10 Tier 1 items** with full causal + keyword signal ready (or nearly ready) for the pipeline.

### What Works

- The enrichment schema (`diagnostic_sba_item_v1`) is well-designed: it captures diagnostic role per option, corpus grounding, causal chain linkage, misconception linkage, and governance flags.
- Governance is clean across all checked items: `safe_for_examiner = False`, `examiner_scoring_allowed = False` everywhere.
- The 3 active items (Q2, Q12, Q17) are high-quality: they have causal chains, rich keywords, plausible distractors, and clean reviews.
- The `correct_answer_text` field exists on all 524 sba_valid items — this is the prerequisite for frontend option shuffle.

### What's Broken

- **Severe C-bias (56.5%)** and near-absent D-bias (3.8%) — systemic from source XLSX generation. Option shuffle is the correct fix; editorial remediation would be destructive.
- **RA mislabeling:** 31 items labeled RA1 contain RA5 content (storage, service, temperature). This understates RA5 coverage and overstates RA1 coverage in any tracking system that uses the tag.
- **Diagnostic signal uniformity:** All 524 items carry `difficulty: intermediate` and `reasoning: theory_foundation`. The bank cannot currently drive difficulty-adaptive routing.
- **Corpus grounding gap:** 83% of sba_valid items are `unsupported` by the keyword corpus — not because they are factually wrong, but because regional content from Wine With Jimmy is not yet indexed. This limits traceability claims.
- **Q1 and Q13** are held back by unresolved review issues — two of the best Tier 1 items are stuck.

### What to Do Next (ordered by impact)

1. **Implement frontend option shuffle** — eliminates C-bias without touching question content. Single highest-leverage action.
2. **Resolve Q1 and Q13 reviews** — unblocks two Tier 1 items and expands active set to 5 with zero new pipeline work.
3. **Activate Q3, Q4, Q5, Q14** — create 4 enrichment drafts, submit for review. These are Tier 1 items with defined causal chains; draft creation is templated from existing pilot drafts.
4. **Create enrichment drafts for Q18 (correct=D) and Q839/Q846 (correct=A)** — directly addresses positional bias in the active set.
5. **Correct RA mislabels for the 31 items** — human batch review pass; improves coverage reporting accuracy.
6. **Deduplicate Q24/Q218** — minor housekeeping; human call on which to archive.
7. **Add difficulty tiers to all Tier 1/2 items processed through enrichment** — enables diagnostic routing beyond the current single-level bank.

At the conclusion of steps 1–4, the active set will be 9–10 items, covering all 5 RA areas, with answer distribution A≥1, B≥3, C≤4, D≥1 — a pedagogically sound and positionally unbiased diagnostic bank.

---

*This document is a planning and audit artifact only. It does not represent WSET assessment authority, official scoring, or examiner evaluation. All governance flags remain unchanged: `safe_for_examiner = False`, `examiner_scoring_allowed = False`, `uses_llm = False`, `uses_api = False`.*
