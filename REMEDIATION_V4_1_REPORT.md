# Remediation V4.1 Report — Grounding Corrections
**Phase:** V4.2  
**Date:** 2026-06-09  
**Parent patch:** MASTER_BANK_PATCH_V4.json  
**Output patch:** MASTER_BANK_PATCH_V4_1.json  
**Items modified:** 5 (4 required + 1 optional alignment)

---

## Summary

The V4.1 patch applies corpus-alignment corrections identified in GROUNDING_AUDIT_V4.xlsx. No items were retired. No new questions were created. Only the wording of affected options and answer text was changed to match what the WSET L3 study guide explicitly states.

Governance invariants are unchanged across all 5 items:
- `safe_for_examiner: false` ✓
- `examiner_scoring_allowed: false` ✓
- `uses_llm: false` ✓
- `uses_api: false` ✓

---

## Item-by-Item Changes

### 1. wset3_678 — Cover crops benefit (C→B)

**Field:** `options.B` + `correct_answer_text`

**Before:**
> Reducir la compactación del suelo y mejorar su estructura

**After:**
> Mejorar la salud del suelo y su estructura, reduciendo la erosión y la compactación

**Justification:** The WSET L3 study guide describes cover crops as improving soil health and structure broadly (erosion control, organic matter, drainage). "Reduce compaction" alone over-specifies one secondary benefit and was the direct cause of the C-level grounding score. The corrected wording matches the corpus's holistic framing.

**Grounding change:** C → B

---

### 2. wset3_775 — Vineyard solar exposure (C→A)

**Field:** Stem + all 4 options + correct answer

**Before (stem):**
> ¿Qué orientación de las filas del viñedo maximiza generalmente la exposición solar uniforme en el hemisferio norte?

**Before (correct answer):**
> Norte-Sur, ya que permite mayor exposición solar uniforme a ambos lados de la fila durante el día

**After (stem):**
> ¿Qué factor de emplazamiento permite maximizar la exposición solar de la vid en viñedos de pendiente?

**After (correct answer):**
> La orientación de la ladera hacia el ecuador, que maximiza la intercepción de luz solar directa

**Justification:** N-S vs E-W row orientation is not discussed in the WSET L3 study guide. The corpus explicitly discusses slope aspect (orientation toward the equator) as a site-selection factor that maximises solar interception and promotes ripening. The rewritten question tests the same learning objective (sun exposure → ripening) using a concept the corpus directly supports.

**Grounding change:** C → A

---

### 3. wset3_742 — Barossa Shiraz style (B→A)

**Field:** `options.D` + `correct_answer_text`

**Before:**
> Shiraz (Syrah) de cuerpo pleno, taninos maduros y notas especiadas de pimienta negra

**After:**
> Shiraz (Syrah) de cuerpo pleno, taninos suaves y sabores de fruta negra madura con notas especiadas

**Justification:**
- "Pimienta negra" (black pepper) is the signature descriptor for cool-climate Syrah, most associated with Clare Valley and northern Rhône — not Barossa. The WSET corpus describes Barossa Shiraz as "earthy or spicy" and full-bodied with ripe fruit.
- "Taninos maduros" (mature tannins) is not the corpus term. The WSET study guide uses "soft tannins" for Barossa Shiraz.
- Corrected to: full-bodied, soft tannins, ripe black fruit, spiced — all corpus-grounded.

**Grounding change:** B → A

---

### 4. wset3_716 — Altitude and wine profile (C→A)

**Field:** Stem + all 4 options + correct answer + curriculum keywords

**Before (correct answer):**
> Las temperaturas más frescas y la mayor radiación UV en altitud favorecen la síntesis de compuestos aromáticos, produciendo vinos frescos y complejos

**After (correct answer):**
> Las temperaturas más frescas en altitud ralentizan la maduración, conservando la acidez y los aromas primarios de la fruta

**Justification:** The claim that higher UV radiation at altitude promotes aromatic compound synthesis is scientifically discussed in viticultural literature but is NOT present in the WSET L3 study guide. The corpus grounding for altitude effects is: cooler temperatures → slower ripening → retained acidity → preserved primary aromas. The rewritten answer removes the unsupported UV mechanism and grounds the causal chain entirely in corpus-supported content.

Curriculum keywords updated: removed `UV_radiation`; added `maduración lenta`, `acidez`, `aromas primarios`.

**Grounding change:** C → A

---

### 5. wset3_686 — Selected yeasts benefit (optional, A→A)

**Field:** `options.C` + `correct_answer_text`

**Before:**
> Garantizan una fermentación más rápida, predecible y con menor riesgo de parada

**After:**
> Garantizan una fermentación más fiable, predecible y con menor riesgo de parada

**Justification:** The WSET corpus describes the primary benefit of selected yeasts as producing a "more reliable and predictable fermentation" — not specifically a faster one. Speed is a secondary attribute and is not the core corpus claim. "Más rápida" replaced with "más fiable" for precise corpus alignment. Grounding level was already A and remains A; this is a minor precision improvement.

**Grounding change:** A → A (precision alignment only)

---

## Governance Invariant Confirmation

All 5 patched items retain:

```json
"governance": {
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "official_wset_question": false,
  "training_item_only": true,
  "uses_llm": false,
  "uses_api": false,
  "uses_embeddings": false,
  "uses_vector_db": false,
  "cloud_services_active": false
}
```

No other items were touched. No new questions were created.
