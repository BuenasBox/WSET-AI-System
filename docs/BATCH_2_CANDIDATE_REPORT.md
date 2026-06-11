# BATCH 2 — Candidate report (no deploy, no payload merge)

**Date:** 2026-06-11 · **Phase:** P.2 (knowledge-layer expansion)
**Rule honored:** coverage increased **only** by adding causal knowledge. The matcher (v2) is byte-for-byte unchanged in its thresholds and logic; the one code change is a *new exclusion guard* (negative-polarity stems), which tightens precision, not loosens it.

---

## 1. Headline numbers

| Metric | Value |
|---|---|
| Batch-1 enriched items (already in production) | 8 — unchanged, node assignments stable |
| **Batch-2 new candidate items** | **3** (`wset3_380`, `wset3_497`, `wset3_706`) |
| Total in candidate sidecar | 11 |
| New causal nodes authored | 3 (`HC_CONTINENTALITY_STYLE`, `HC_MARITIME_MODERATION`, `HC_WATER_STRESS_CONCENTRATION`) |
| Existing nodes given Spanish layer | 5 (`HC_ALTITUDE_TEMPERATURE`, `HC_COOL_CLIMATE_STYLE`, `HC_DIURNAL_RANGE_FRESHNESS`, `HC_YIELD_CONCENTRATION`, `CC_COOL_CLIMATE_ACIDITY`) |
| `NODE_ES` coverage | 10 → 18 nodes |
| Matcher thresholds | **unchanged** (≥2 specific hits, stem hit, correct-option hit, unique best, word-boundary) |

Coverage gained this batch is deliberately small. The strict matcher rejected far more than it accepted, exactly as intended. **Precision first.**

---

## 2. New causal nodes

All three follow the `HC_` heuristic schema (`source: heuristic`, `classification: inferred`, `official: false`, `formative_only: true`, `safe_for_examiner: false`, `requires_human_review: true`). Triggers are specific multi-word phrases only — no single generic words.

| Node | Topic (priority #) | Specific triggers (sample) |
|---|---|---|
| `HC_CONTINENTALITY_STYLE` | Continentality (#4) | `clima continental`, `continental climate`, `continental fresco`, `amplitud termica continental`, `estaciones marcadas` |
| `HC_MARITIME_MODERATION` | Maritime/oceanic influence (#5) | `clima maritimo`, `influencia maritima`, `influencias oceanicas`, `clima oceanico`, `moderacion maritima` |
| `HC_WATER_STRESS_CONCENTRATION` | Water availability (#7) | `estres hidrico`, `estres hidrico leve`, `deficit hidrico`, `riego por goteo`, `disponibilidad de agua` |

The 5 existing climate/site nodes that received a Spanish layer cover priorities #1 (climate), #2 (altitude), #3 (latitude, via cool-climate), #8 (acidity retention), #9–#10 (tannin/ripeness via yield concentration). Only **mechanism** nodes were translated. Two **attribute** nodes (`CC_TANNIN_ASTRINGENCY`, `CC_WARM_CLIMATE_ALCOHOL`) were deliberately **left untranslated** — they describe a sensation/attribute rather than explaining a regional cause, so they carry the same false-positive profile you flagged in batch 1.

---

## 3. The 3 candidate items (full audit)

Each was checked by hand against the single question: *does the node's mechanism explain why the correct answer is correct?*

### `wset3_497` — RA1 — node `HC_YIELD_CONCENTRATION` — score 2 — **CLEAN**
- **Q:** ¿Cuál de los siguientes factores en la viña influye directamente en la intensidad aromática de los vinos blancos?
- **✓ Correcta:** Rendimiento por hectárea
- **Hits:** stem `intensidad aromatica` · correct `rendimiento`
- **Verdict:** Strongest of the three. The node directly explains yield → fewer clusters → more concentration / aromatic intensity. The answer *is* the cause the node describes.

### `wset3_706` — RA1 — node `HC_WATER_STRESS_CONCENTRATION` — score 3 — **CLEAN**
- **Q:** ¿Cuál de las siguientes afirmaciones sobre el estrés hídrico leve es CORRECTA?
- **✓ Correcta:** Un nivel moderado de estrés hídrico puede contribuir a concentrar los compuestos de la baya.
- **Hits:** stem `estres hidrico`, `estres hidrico leve` · correct `estres hidrico`
- **Verdict:** Positive-polarity (CORRECTA → true statement). The node explains mild water stress → smaller berries → concentration, which is exactly the correct statement. Highest score in the batch.

### `wset3_380` — RA2 — node `HC_DIURNAL_RANGE_FRESHNESS` — score 2 — **CLEAN (with note)**
- **Q:** ¿Qué permite el clima continental en Ribera del Duero?
- **✓ Correcta:** Alta oscilación térmica y concentración
- **Hits:** stem `clima continental` · correct `oscilacion termica`
- **Verdict:** The stem mentions continental climate, but the *answer* is about thermal oscillation → the diurnal-range node (which won the unique-best contest because it alone hit the correct option) genuinely explains it: warm days/cool nights preserve acidity and aid concentration. **Note:** `HC_CONTINENTALITY_STYLE` is also topically relevant; the matcher chose diurnal because that node explains the specific answer. Acceptable, but the clearest example of two valid nodes where the correct-option hit is the tiebreaker.

All 3 micro-drills were inspected: the correct option is the item's true correct answer, distractors are correct answers of items matched to *other* nodes (true statements about other mechanisms), and the ES contraction polish is applied (e.g. drill prompt "…corresponde **al** bajo rendimiento").

---

## 4. False-positive risk assessment

| Risk | Status |
|---|---|
| Substring matches (the batch-1 `port`⊂`portuguesa` class) | Eliminated by word-boundary matching — unchanged from v2. |
| Generic trigger matches (`vino`, `clima`, `acidez`…) | 27-word stoplist — unchanged. New nodes use only multi-word triggers. |
| Regional/definitional identification stems | 112 rejected. |
| **Negative-polarity stems** (NEW risk found this batch) | **24 rejected.** `wset3_788` and `wset3_792` ("¿Cuál es INCORRECTA?") would have fed the micro-drill a *deliberately false* statement as a true option (e.g. "clima marítimo = inviernos secos y calurosos"). New guard `_is_negative_polarity_stem` excludes `incorrecta/falsa/excepto/no es correcto/no influye/…`. This is the most important finding of batch 2. |
| Node explains attribute not cause | Mitigated by excluding `CC_TANNIN_ASTRINGENCY` / `CC_WARM_CLIMATE_ALCOHOL` from translation. |
| Residual risk on the 3 candidates | Low. Two are exact mechanism matches (497, 706); one (380) is a defensible tiebreaker. |

**Rejection breakdown (current sidecar):** `below_threshold: 139`, `identification_stem: 112`, `negative_polarity_stem: 24`, `no_correct_option_hit: 11`, `no_stem_hit: 4`. The bulk of the under-threshold pool remains uncovered by design — those items need *new specific nodes*, not a weaker matcher.

---

## 5. What is and isn't done

**Done:** 3 nodes authored + 5 nodes translated; sidecar regenerated (11 items); negative-polarity guard added; 17 deriver tests pass (incl. new guard regression on 788/792); output deterministic (byte-equal across runs); no English, no contraction artifacts, no drill defects.

**NOT done (per your instruction):** no payload regeneration, no merge into `preguntas_data.js` / `session_bank.js` (frontend banks still show exactly the 8 batch-1 items), no dashboard deploy, no commit pushed for this batch.

**To promote batch 2 to production (on your approval):** regenerate payloads → run gate G1–G9 → verify the 3 new items activate panels and the 24 negative-polarity items stay clean → commit both repos.

---

## 6. Coverage outlook

Batch 2 confirms the scaling model works: 8 new ES layers + 3 nodes yielded 3 legitimate matches without touching the matcher. The honest ceiling is set by the knowledge layer, not the matcher — the 139 below-threshold and 299 no-hit items will only convert as more genuine causal nodes are authored for their specific mechanisms (e.g. botrytis concentration, MLF texture, lees ageing, bottle-age tertiary development already have nodes that could be translated next).

*Formative training document. No examiner authority. safe_for_examiner: false.*
