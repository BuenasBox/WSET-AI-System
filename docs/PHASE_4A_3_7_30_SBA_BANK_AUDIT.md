# PHASE 4A.3.7.30 — Full Diagnostic SBA Bank Audit & Remediation Plan

**Date:** 2026-06-03  
**Status:** READ-ONLY audit. No modifications. No commits. No activation.  
**Scope:** Full 616-record structured question bank + 3 active frontend items  
**Analyst:** Claude (Cowork mode, automated audit)

---

## Data Sources Identified

| File | Description | Records |
|------|-------------|---------|
| `knowledge/question-bank/structured/wset3_questions.json` | Master structured bank | **616** |
| `frontend/diagnostic-sba/preguntas.json` | Published static demo | **3 active** |
| `frontend/architecture-dashboard/diagnostic-sba/preguntas.json` | Dashboard copy (identical to above) | 3 |
| `knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json` | Enrichment-ready drafts (pilot) | 5 |
| `knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json` | Human review records (pilot) | 5 |
| `knowledge/enrichment/diagnostic_sba_item.schema.json` | Canonical SBA item schema | — |

**Note:** The published frontend shows `export_version: static_demo_export_v0` and `static_demo_only: True`. Only **3 items** are currently live (source Q2, Q12, Q17), not 18 as the task prompt assumed. There is no separate "18-item" active set — the prompt estimate was incorrect based on prior session context.

---

## 1. Inventario Completo

### 1.1 Structural Classification (all 616 records)

| Category | Count | Description |
|----------|------:|-------------|
| `complete_sba` — usable 4-option SBA | **524** | All 4 options filled, valid correct_answer A–D |
| `true_false_as_sba` | **71** | Stored as 4-option but C/D empty; binary T/F items, or "Verdadero/Falso" options |
| `open_response` | **20** | `short_answer` type with empty options and no correct_answer_letter — essay questions |
| `incomplete_sba` | **11** | Multiple options missing (including 6 "matching" items with only option A filled) |
| `discardable` | **0** | No records meet the discard threshold |
| **Total** | **616** | |

**Key finding:** The "616 records" headline is misleading. Only **524** records have the structural prerequisites for SBA use. The remaining 92 are either true/false, open-response essays, or partially built matching questions.

### 1.2 Pedagogical Classification (of the 524 complete SBA records)

| Category | Count | Description |
|----------|------:|-------------|
| `eligible` — HIGH diagnostic value | **9** | Causal chain linkage, 3+ keywords, rich distractors |
| `eligible` — MEDIUM diagnostic value | **2** | Good structure, moderate diagnostic signal |
| `correctable` — MEDIUM | **369** | Complete structure; missing causal link or single weak keyword; fixable in <30 min |
| `ambiguous` | **145** | No causal signal, single keyword, short stem — workable but require editorial review |
| **Total usable SBA** | **525** | (524 + 1 mislabeled `short_answer` with full options — Q18) |

**Currently active:** 3 items (Q2, Q12, Q17). All 3 fall in the `eligible / HIGH` tier.

---

## 2. Structural Quality Checks

### 2.1 Field-Level Issues

| Check | Count | Detail |
|-------|------:|--------|
| Duplicate IDs | **0** | All 616 IDs are unique |
| Missing `correct_answer_letter` | **20** | All are `short_answer` / open-response (Q798–Q817 range) |
| Invalid `correct_answer_letter` (not A/B/C/D) | **25** | Same 20 above + 5 matching items |
| Records with empty option text | **91** | 71 T/F (C/D empty) + 11 partial + ~9 other |
| Empty stems | **0** | All records have question text |
| Wrong option count (≠4) | **0** | All records have exactly 4 option keys |
| Mislabeled `question_type` | **1** | Q18 is tagged `short_answer` but has full 4-option SBA structure |
| Matching-format items stored as SBA | **6** | Q742–Q747: "Emparejar:" stems with only option A filled |

### 2.2 Summary by Severity

- **Critical (blocks SBA use):** 92 records (71 T/F + 20 open-response + 1 matching)
- **Moderate (requires edit before use):** 11 records (partial + mislabel)
- **No structural issues:** 524 records

---

## 3. Pedagogical Quality Assessment

### 3.1 Scoring Methodology

Each complete SBA record was scored on:
- **Causal chain linkage** (3 pts): `expected_causal_links` present and non-empty
- **Keyword depth** (1–2 pts): ≥2 or ≥3 `expected_keywords`
- **Stem specificity** (1 pt): stem > 80 characters
- **Difficulty** (2 pts): `distinction` level
- **Option richness** (1 pt): average option length > 20 characters

**Diagnostic value tiers:**

| Tier | Score | Count |
|------|------:|------:|
| HIGH (score ≥ 5) | Full causal + keyword + options | 9 |
| MEDIUM (score 3–4) | Good structure, missing one signal | 371 |
| LOW (score 0–2) | Single keyword, short stem, weak distractors | 145 |

### 3.2 Distractor Quality Observations (sample review)

**Strong distractors (Q1–Q18 range, HIGH tier):**
- Q1 (Jerez/flor): Distractors cover plausible wrong mechanisms (acidez, alcohol, oxidación)
- Q12 (heladas): Distractors are all real viticulture factors (exposición, altitud, latitud) — only slope is correct
- Q5 (Oloroso vs. Amontillado): Distractors test genuine misconceptions about both styles

**Weak distractors (MEDIUM/LOW, general bank):**
- Q9 (Madeira variety): Distractors (Tempranillo, Sangiovese, Cab Sauv) are trivially wrong — no trap for someone who studied
- Q22 (Chile espumosos): Single-word region options (Maipo, Curicó, Limarí, Rapel) — low trap value
- Q32 (poda): Short single-term options (Guyot, Royat, Poda en vaso, Poda mínima) — factual recall, not reasoning

---

## 4. Coverage Matrix

### 4.1 By Learning Area (RA)

| RA | Topic Area | Active | Eligible | Correctable | Total (SBA) |
|----|-----------|-------:|---------:|------------:|------------:|
| RA1 | Viticultura / Entorno de cultivo | 0 | 0 | 124 | 176 |
| RA2 | Regiones vitivinícolas del mundo | 1 | 4 | 147 | 209 |
| RA3 | Vinificación | 0 | 0 | 42 | 64 |
| RA4 | Vinos espumosos / Fortificados / Dulces | 1 | 1 | 19 | 27 |
| RA5 | Almacenamiento / Servicio / Precio / Calidad | 0 | 0 | 37 | 43 |
| UNKNOWN | Specific topic tags (Q1–Q18 range) | 2 | 7 | 0 | 7 |

**Coverage gaps:**
- **RA1** (Viticultura): 0 active, 0 eligible — 176 correctable records exist but none have causal links in the SBA-ready records
- **RA3** (Vinificación): 0 active, 0 eligible — 64 correctable records
- **RA5** (Almacenamiento/Servicio): 0 active, 0 eligible — 43 correctable records

### 4.2 RA2 Regional Sub-Coverage

| Region | SBA Items |
|--------|----------:|
| Otras regiones RA2 (mixed) | 142 |
| Rioja | 12 |
| Regiones Riesling (Alsacia/Mosel/Rheingau) | 11 |
| Chile | 8 |
| Priorat | 5 |
| Italia | 5 |
| Alsacia | 5 |
| California / Napa Valley | 5 + 5 |
| Ribera del Duero | 5 |
| Mendoza | 4 |
| Barossa Valley | 4 |
| Burdeos | 4 |
| Nueva Zelanda / Australia | 3 + 3 |
| Borgoña / Champagne | 3 each |
| Argentina / Toscana | 3 / 1 |

**Regional gaps:** Champagne (~3 items, low), Borgoña (~3), Oporto (covered in RA4), Alemania/Rheingau under-represented in RA2 specifically.

---

## 5. Answer Distribution Analysis

### 5.1 Active Items (3 items)

| Option | Count | % |
|--------|------:|--:|
| A | 0 | 0% |
| B | 2 | 67% |
| C | 1 | 33% |
| D | 0 | 0% |

⚠️ **Severe bias** at only 3 items — not statistically meaningful, but A and D are absent.

### 5.2 Full Structured Bank (616 records)

| Option | Count | % | Flag |
|--------|------:|--:|------|
| A | 83 | 14.0% | ⚠️ Below 15% |
| B | 191 | 32.3% | OK |
| C | 296 | 50.1% | ⚠️ Severe — exceeds 40% |
| D | 21 | 3.6% | ⚠️ Critical — far below 10% |

### 5.3 Complete SBA Records Only (524 records)

| Option | Count | % | Flag |
|--------|------:|--:|------|
| A | 41 | 7.8% | ⚠️ Critical |
| B | 167 | 31.9% | OK |
| C | 296 | 56.5% | ⚠️ Severe |
| D | 20 | 3.8% | ⚠️ Critical |

**Root cause:** The bank appears to have been generated with a systematic bias toward option C as the correct answer. This is not random — it likely reflects generation patterns from the source XLSX files. Option D was rarely assigned as the correct answer throughout the entire bank.

**Important:** Per audit instructions, correct answers must NOT be changed to balance statistics. This bias must be addressed by selecting items for activation that collectively balance the distribution, not by altering answer keys.

---

## 6. Diagnostic Signal Ranking — Top 30 Candidates

Ranked by composite score: eligibility tier (20/8/2) + diagnostic value (10/4/0) + causal chain presence (5) + keyword count (up to 4) + difficulty bonus (5) + stem/option richness (up to 4).

| Rank | QID | Score | Category | Diag | Active | Stem (abbreviated) |
|------|-----|------:|----------|------|--------|---------------------|
| 1 | Q5 | 47 | eligible | HIGH | — | ¿Qué diferencia al Oloroso del Amontillado en términos de crianza? |
| 2 | Q1 | 46 | eligible | HIGH | — | ¿Qué rol juega la 'flor' en la crianza biológica del Jerez? |
| 3 | Q3 | 42 | eligible | HIGH | — | ¿Cuál es una característica clave de los vinos de Porto Vintage? |
| 4 | Q14 | 42 | eligible | HIGH | — | ¿Cuál es el principal efecto de la vendimia mecánica sobre el estilo del vino? |
| 5 | **Q17** | 42 | eligible | HIGH | **✓** | ¿Cuál es el propósito principal del despalillado antes de la fermentación? |
| 6 | **Q2** | 41 | eligible | HIGH | **✓** | ¿Qué método se usa para detener la fermentación en el vino de Oporto? |
| 7 | Q4 | 41 | eligible | HIGH | — | ¿Cuál es el sistema tradicional de envejecimiento utilizado en Jerez? |
| 8 | Q13 | 41 | eligible | HIGH | — | ¿Qué elemento del suelo influye más directamente en el drenaje del viñedo? |
| 9 | **Q12** | 40 | eligible | HIGH | **✓** | ¿Qué factor natural tiene mayor influencia en el riesgo de heladas primaverales? |
| 10 | Q18 | 30 | eligible | MEDIUM | — | ¿Cuál es una consecuencia del uso excesivo de sulfitos? |
| 11 | Q16 | 29 | eligible | MEDIUM | — | ¿Qué práctica enológica se utiliza para aumentar la extracción de color y tanino? |
| 12 | Q29 | 17 | correctable | MEDIUM | — | ¿Cuál es una diferencia clave entre método ancestral y tradicional? |
| 13 | Q81 | 17 | correctable | MEDIUM | — | ¿Cuál es una consecuencia de almacenar vino a temperaturas muy altas? |
| 14 | Q335 | 17 | correctable | MEDIUM | — | ¿Cómo impacta el azúcar en los vinos con alta acidez? |
| 15 | Q712 | 17 | correctable | MEDIUM | — | ¿Qué factor comercial impacta el precio de un vino? |
| 16 | Q728 | 17 | correctable | MEDIUM | — | ¿Qué factores naturales influyen más en la calidad de un vino? |
| 17 | Q729 | 17 | correctable | MEDIUM | — | ¿Qué papel juega la legislación en una denominación de origen? |
| 18 | Q740 | 17 | correctable | MEDIUM | — | ¿Qué factor de viña contribuye al estilo en una región particular? |
| 19 | Q824 | 17 | correctable | MEDIUM | — | ¿Qué categoría está por encima de DOC en Italia? |
| 20 | Q831 | 17 | correctable | MEDIUM | — | ¿Qué implica 'Classico' en denominaciones italianas como Chianti? |
| 21 | Q833 | 17 | correctable | MEDIUM | — | ¿Qué indica la etiqueta 'Côte de Nuits Villages AOC, Pinot Noir'? |
| 22 | Q839 | 17 | correctable | MEDIUM | — | ¿Qué organismo establece normas técnicas para el vino? |
| 23 | Q846 | 17 | correctable | MEDIUM | — | ¿Por qué los productores prefieren trabajar con distribuidor exclusivo? |
| 24 | Q848 | 17 | correctable | MEDIUM | — | ¿Qué factor incrementa el coste de producción de un vino premium? |
| 25 | Q852 | 17 | correctable | MEDIUM | — | ¿Cuál es la ventaja del formato magnum vs. botella estándar? |
| 26 | Q7 | 16 | correctable | MEDIUM | — | ¿Qué influencia tiene el envejecimiento oxidativo en los vinos generosos? |
| 27 | Q15 | 16 | correctable | MEDIUM | — | ¿Qué factor humano tiene impacto directo en el precio del vino? |
| 28 | Q30 | 16 | correctable | MEDIUM | — | ¿Qué característica se asocia al método tradicional vs. Charmat? |
| 29 | Q33 | 16 | correctable | MEDIUM | — | ¿Cuál es el efecto de la irrigación por goteo en climas áridos? |
| 30 | Q44 | 16 | correctable | MEDIUM | — | ¿Cuál de las afirmaciones sobre maridaje es correcta? |

**Notes on Top 30:**
- Items ranked 1–11 are the 8 non-active eligible items — these are the strongest candidates.
- Items ranked 12–30 are `correctable`: structurally complete but need a causal chain added to their metadata before enrichment pipeline processing.
- The correct answer for the top 30 (non-active) is: A=2, B=11, C=14, D=3 — still heavily skewed to C/B. Any activation batch should deliberately select items with A or D answers to rebalance.

---

## 7. Remediation Backlog

### Tier 1 — Ready for Activation (eligible, structurally complete, HIGH/MEDIUM diagnostic)

**8 items** — require only enrichment pipeline processing (draft → review → export).

| QID | Stem | Correct | RA | Correct Ans |
|-----|------|---------|-----|-------------|
| Q1 | Rol de la 'flor' en crianza biológica del Jerez | C | RA4 | C |
| Q3 | Característica clave de Porto Vintage | C | RA4 | C |
| Q4 | Sistema de envejecimiento en Jerez (solera) | C | RA4 | C |
| Q5 | Diferencia Oloroso vs. Amontillado | C | RA4 | C |
| Q13 | Elemento de suelo que influye en drenaje | C | RA1 | C |
| Q14 | Efecto de la vendimia mecánica | B | RA1 | B |
| Q16 | Práctica para aumentar extracción de color/tanino | C | RA3 | C |
| Q18 | Consecuencia del uso excesivo de sulfitos | D | RA3 | D |

**Constraint noted:** Q1, Q3, Q4, Q5 all have correct answer C — activating all 4 would worsen C-bias. Should activate with deliberate selection.

### Tier 2 — Minor Edit Needed (correctable, < 30 min fix)

**~369 items** — structurally sound SBA with 4 complete options and valid answer. The primary gap is missing `expected_causal_links`. Fix: add causal chain metadata entry; no stem or option changes required.

**Representative examples:**
- Q6: Jerez Fino characteristics — good distractors, just missing causal link
- Q7: Envejecimiento oxidativo — sensory outcome item, add oxidation chain
- Q8: Tokaji Aszú — distinctive winemaking item, add botrytis → sugar → paste chain
- Q25: Licor de tiraje purpose — sparkling method, add second-fermentation chain
- Q26: Riddling (remuage) — add sediment-movement → disgorgement chain
- Q29: Método ancestral vs. tradicional — strong conceptual item
- Q81: Storage temperature consequence — straightforward, high practical value

**Priority within Tier 2:** Items Q6–Q50 range cover fortified/sparkling/viticulture topics well; Q700–Q860 range covers RA5 (storage, service, legislation, price) which is currently unrepresented in active items.

### Tier 3 — Requires Rewrite (ambiguous stem, defensible distractors)

**~145 items** — complete structure but low diagnostic signal. Issues:
- Stems are simple recall questions (single correct fact, no reasoning required)
- Distractors are often trivially wrong (e.g., Tempranillo as a Madeira variety)
- No causal chain — answer is just a memorized fact

**Representative examples:**
- Q9: Variedad de Madeira (recall only — Tempranillo/Sangiovese distractors are obvious wrong)
- Q22: Región chilena de espumosos (single-word options, no reasoning trap)
- Q35: Clima que favorece sobremaduración (correct but trivially obvious)
- Q37: Técnica que aumenta extracción de taninos (answer defensible but B=Remontado and C=Desfangado could be argued)

**Rewrite effort:** Add causal reasoning requirement to stem (e.g., "¿Por qué...?" instead of "¿Qué...?"), replace trivially-wrong distractors with plausible wrong mechanisms.

### Tier 4 — Discard or Repurpose

**92 items** — not suitable as SBA in current form:

| Sub-type | Count | Disposition |
|----------|------:|-------------|
| True/False disguised as SBA | 71 | Repurpose as binary T/F format if needed; discard from SBA pool |
| Open-response essays | 20 | Keep for future written-question module; not SBA |
| Matching items (stub) | 6 | Incomplete — discard or complete as separate format |
| Mislabeled (Q18) | 1 | Fix label only (already counted in Tier 1) |

---

## 8. Expansion Strategy

### 8.1 Current State

- **Active:** 3 items (Q2=RA4/Porto, Q12=RA1/viticultura, Q17=RA3/vinificación)
- **Coverage:** RA2, RA5 completely absent; RA1/RA3/RA4 each have ≤1 item

### 8.2 Target: 9 Active Items (+6)

**Goal:** Ensure all 5 RA areas have at least 1 item; add 1 distinction-level item.

| # | QID | Topic | RA | Correct Ans | Rationale |
|---|-----|-------|----|-------------|-----------|
| +1 | Q1 | Flor / crianza biológica Jerez | RA4 | C | Eligible HIGH; causal chain present |
| +2 | Q5 | Oloroso vs. Amontillado | RA4 | C | Eligible HIGH; covers misconception |
| +3 | Q13 | Textura de suelo y drenaje | RA1 | C | Eligible HIGH; viticulture causal |
| +4 | Q18 | Consecuencia del SO₂ excesivo | RA3 | **D** | Eligible MEDIUM; adds D-correct item |
| +5 | Q712 | Factor comercial y precio | RA5 | C | Correctable; fills RA5 gap |
| +6 | Q729 | Legislación en denominaciones | RA2 | B | Correctable; fills RA2 gap |

**Resulting distribution:** A=0, B=3, C=5, D=1 — still C-heavy but improved. RA coverage: RA1=2, RA2=2, RA3=2, RA4=3, RA5=1.

### 8.3 Target: 21 Active Items (+18)

Add items prioritizing: RA2 regional depth, RA5 breadth, answer distribution balance, difficulty variety.

**Priority order for next 12 items beyond the 9:**

1. **RA2 regions** — select Q824 (DOCG/Italia), Q831 (Classico), Q833 (AOC etiqueta), Q839 (OIV)
2. **RA1 more depth** — select Q14 (vendimia mecánica, correct=B), Q33 (irrigación goteo, correct=B), Q81 (almacenamiento calor, correct=B)
3. **RA5 service/storage** — select Q846 (distribuidor exclusivo), Q848 (coste producción), Q852 (formato magnum)
4. **RA3 winemaking** — select Q7 (envejecimiento oxidativo), Q16 (extracción color/tanino)

**Note:** 8 of these 12 have correct=B, which helps rebalance the B/C distribution.

### 8.4 Target: 36 Active Items (+33)

Beyond 21, draw from `correctable` Tier 2 items in Q6–Q50 range and Q700–Q860 range:
- Add causal chain metadata to selected records
- Process through enrichment draft pipeline
- Prioritize items with correct=A or correct=D to address distribution bias
- Ensure Champagne, Borgoña, Burdeos, Rheingau receive at least 1 item each

**Estimated effort:** Each correctable item requires ~20–30 min enrichment metadata edit before pipeline processing.

### 8.5 Target: 50 Active Items (+47)

At 50+ items, the bank shifts to broad coverage mode:
- Begin drawing from Q100–Q600 range (general RA1/RA2 theory items)
- Items in this range are mostly `correctable/ambiguous`; many require distractor rewrites
- Prioritize rewriting items with trivially-wrong distractors (Tier 3 rewrites become necessary)
- At this scale, a randomization strategy (see §9) becomes important

---

## 9. Randomization Recommendation

### Options Considered

| Approach | Benefit | Risk |
|----------|---------|------|
| Fixed question order | Predictable; learner patterns trackable | Memorization of sequence |
| Randomized question order per session | Breaks sequential memorization | Requires stateless item design |
| Randomized option order (A/B/C/D scrambled) | Eliminates positional bias | Requires answer-key remapping in frontend |
| Both question + option order randomized | Maximum anti-memorization | Highest implementation complexity |

### Recommendation: **Randomize option order only (not question order)**

**Rationale:**
1. The bank has a severe C-bias (56.5% correct answers are C). Even without memorization, learners who guess C will score above chance. Option-order randomization eliminates this positional signal entirely.
2. Question-order randomization is less critical at ≤50 items — the cognitive benefit is smaller, and fixed ordering aids diagnostic signal tracking (same item always appears in same session position).
3. Option-order randomization requires remapping: store correct answer as the option *text* (already present in `correct_answer_text` field), not as a letter. The letter assignment is regenerated at render time.
4. The enrichment schema already stores `correct_answer_text` alongside `correct_answer_letter` — the infrastructure supports this without breaking changes.
5. Diagnostic signal tracking survives: signals are tied to `item_id` and `source_question_id`, not to option letters.

**Implementation note (DO NOT implement now):** When rendering, shuffle `options` dict into a random list, assign A/B/C/D to shuffled positions, display that way, and compare submitted answer against the shuffled-position letter that matches `correct_answer_text`.

---

## 10. Estimación Final

### How many of the 616 records truly deserve activation?

| Tier | Count | Activation Path |
|------|------:|----------------|
| Eligible (Tier 1) — activate as-is after enrichment pipeline | **11** | Immediate: enrichment draft + review + export |
| Correctable top candidates (Tier 2, with causal metadata) | **~80–100** | Short-term: add causal chain metadata, process pipeline |
| Correctable — remaining (need distractor review) | **~250–270** | Medium-term: editorial review pass |
| Ambiguous (Tier 3 rewrite candidates) | **~50–80** | Long-term: stem/distractor rewrite |
| True/False (repurpose) | 71 | Different module, not SBA |
| Open-response (different module) | 20 | Essay/written-question module |
| Matching stubs (incomplete) | 6 | Discard or complete |

**Realistic SBA activation potential:** **~150–200 items** from the 616, after tiered editorial work.

The top **30–50 items** (all Tier 1 + top Tier 2) can reach activation-ready status with moderate effort and would cover all 5 RA areas at 3–6 items each — a pedagogically sound diagnostic bank.

---

## Appendix: Key Findings Summary

1. **Only 3 items are currently active** (not 18 as originally assumed).
2. **524 of 616 records** have valid 4-option SBA structure — the other 92 are T/F, essays, or incomplete.
3. **Severe answer bias:** C=56.5% correct answers, D=3.8% — systemic generation artifact from source XLSX files.
4. **Only 11 records are immediately eligible** for activation (full causal chain + keyword + option quality). All others require at least metadata enrichment.
5. **RA5 (storage/service/price) is entirely unrepresented** in active items despite having 43 correctable records.
6. **The enrichment pilot (5 drafts + 5 reviews)** demonstrates the pipeline works. The governance, schema, and review infrastructure is ready to process more items.
7. **Recommended first activation batch:** Q1, Q5, Q13, Q14, Q18 + 1 RA2 item + 1 RA5 item = 7 new items → 10 total active, covering all 5 RA areas with balanced B/C/D distribution.

---

*This document is a planning artifact only. It does not represent WSET assessment, official scoring, or examiner evaluation. All governance flags remain unchanged: `safe_for_examiner = False`, `examiner_scoring_allowed = False`.*
