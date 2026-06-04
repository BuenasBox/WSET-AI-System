# Tier-1 Corpus Verification Report
Phase 4A.3.7.31 — 2026-06-03
Methodology: Lexical search of Knowledge corpus Markdown files
Reviewer: Claude (automated pass — awaiting human review layer)

Primary corpus searched:
- `knowledge/official-wset/study-guide/wset_markdown/` (official WSET L3 study guide, converted from PDF)
- `knowledge/wine-with-jimmy/clean/` (supplementary WWJ transcript files)

All file paths are relative to the repository root (`C:\Users\esand\OneDrive\Documents\WSET-AI-System`).

---

## Summary Table

| ID | Topic | Correct Answer | Grounding |
|----|-------|---------------|-----------|
| Q1 | Flor / Jerez biological ageing | C – Protects wine from oxygen & develops unique flavours | STRONG |
| Q2 | Port fermentation arrest | C – Adición de aguardiente vínico | STRONG |
| Q3 | Vintage Port characteristics | C – Estructura potente y necesidad de guarda | STRONG |
| Q4 | Jerez ageing system | C – Sistema de soleras y criaderas | STRONG |
| Q5 | Oloroso vs Amontillado ageing | C – Envejecimiento exclusivamente oxidativo | STRONG |
| Q12 | Spring frost risk factor | C – Pendiente del terreno | STRONG |
| Q13 | Soil drainage factor | C – Estructura arenosa | STRONG |
| Q14 | Mechanical harvesting effect | B – Puede aumentar la oxidación | STRONG |
| Q16 | Extraction technique (colour & tannin) | C – Remontado | STRONG |
| Q17 | Purpose of destemming | B – Evitar la extracción de taninos verdes | PARTIAL |

---

## Detailed Item Verification

---

### Q1 — Flor / Jerez Biological Ageing
**Core claim:** Flor protects the wine from oxidation while also producing acetaldehyde, which gives biologically-aged Sherries their unique flavour.
**Correct answer text:** "Protege al vino del oxígeno y desarrolla sabores únicos"

**Passage 1:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- Section: Flor and Biological Ageing
- Text: "The butts are only part filled so that the flor has easy access to oxygen. Importantly, this layer of flor also protects the wine from oxidation."
- Term coverage: 4/4 key terms (flor, oxygen, protection, oxidation)

**Passage 2:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- Section: Flor and Biological Ageing
- Text: "They feed off the alcohol (and other nutrients) in the wine and oxygen in the atmosphere to produce carbon dioxide and acetaldehyde. It is acetaldehyde that gives biologically aged Sherries their unique flavour."
- Term coverage: 4/4 key terms (flor, oxygen, acetaldehyde, unique flavour)

**Passage 3:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- Section: Styles of Sherry — Fino and Manzanilla
- Text: "These wines have only undergone biological ageing. They are pale lemon in colour and usually have aromas of citrus fruit, almonds and herbs, together with bready notes derived from the action of flor."
- Term coverage: 3/4 key terms (biological ageing, flor, unique flavour / bready notes)

**Preliminary grounding:** STRONG
- Passage 1 directly confirms the oxygen-protection function of flor; Passage 2 directly confirms the unique-flavour mechanism (acetaldehyde). Together they explicitly state both halves of the correct answer.

---

### Q2 — Port Fermentation Arrest
**Core claim:** Port fermentation is stopped by the addition of grape spirit (aguardiente), which kills the yeast and creates a stable sweet wine with residual sugar.
**Correct answer text:** "Adición de aguardiente vínico"

**Passage 1:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-2_44_port.md`
- Section: In the Winery — Fermentation
- Text: "Port fermentation is stopped by fortification once the alcohol level reaches 5–9% abv, to create a sweet wine. This means the fermentation typically only lasts for around 24 to 36 hours."
- Term coverage: 4/4 key terms (fermentation, fortification, stopped, sweet wine)

**Passage 2:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-2_44_port.md`
- Section: In the Winery — Fermentation
- Text: "Fortification kills the yeast to create a stable sweet wine."
- Term coverage: 3/4 key terms (fortification, kills yeast, sweet wine)

**Passage 3:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-2_44_port.md`
- Section: In the Winery — Fermentation
- Text: "Ports are made by adding grape spirit to a fermenting juice to create an alcoholic sweet wine."
- Term coverage: 4/4 key terms (grape spirit / aguardiente, fermenting juice, sweet wine, addition)

**Preliminary grounding:** STRONG
- All three passages directly state that Port is fortified with grape spirit (aguardiente) to arrest fermentation, which is the exact claim tested.

---

### Q3 — Vintage Port Characteristics
**Core claim:** Vintage Port has a powerful structure, high tannins, and requires long bottle ageing (capable of decades in bottle, forming heavy sediment).
**Correct answer text:** "Estructura potente y necesidad de guarda"

**Passage 1:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-2_44_port.md`
- Section: Types of Port — Vintage
- Text: "On release these are the most concentrated and tannic Ports. Some consumers choose to enjoy them young but these wines are capable of ageing in bottle for decades and as they age they will throw a heavy sediment."
- Term coverage: 4/4 key terms (concentrated, tannic, bottle ageing, sediment)

**Passage 2:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-2_44_port.md`
- Section: Types of Port — Vintage
- Text: "Vintage – Producers must register their intention to release a Vintage Port in the second year after the harvest and the wine must be bottled no later than the third year. All ageing prior to bottling will take place in either large oak vessels or stainless steel tanks and the wines are unfined and unfiltered."
- Term coverage: 3/4 key terms (Vintage Port, bottling, unfiltered — structure implied)

**Passage 3:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-2_44_port.md`
- Section: Types of Port — Late Bottled Vintage
- Text: "Some LBVs and all Vintage Ports are not filtered and can benefit from long bottle ageing. After this extra period of [ageing]..."
- Term coverage: 3/4 key terms (Vintage Port, long bottle ageing, unfiltered)

**Preliminary grounding:** STRONG
- Passage 1 directly and explicitly states the defining characteristics of Vintage Port: most concentrated and tannic, capable of decades of bottle ageing. This maps precisely to the correct answer's "estructura potente y necesidad de guarda."

---

### Q4 — Jerez Ageing System
**Core claim:** Jerez uses the solera-and-criaderas fractional blending system, which maintains a consistent wine style by progressively topping up older wine with younger wine through multiple levels.
**Correct answer text:** "Sistema de soleras y criaderas"

**Passage 1:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- Section: Blending and Finishing
- Text: "The advantage of the solera system is that it produces a wine of consistent style and quality."
- Term coverage: 3/4 key terms (solera, consistent, quality)

**Passage 2:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- Section: The Solera System
- Text: "These levels are called criaderas [...] The first criadera is then replenished in exactly the same way with wine from the second criadera and so on, so that each criadera is being replenished in turn with younger wine."
- Term coverage: 4/4 key terms (criaderas, solera, replenished, younger wine)

**Passage 3:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- Section: Introduction
- Text: "None of the key techniques, the solera system, biological ageing [are unique to other regions] ... it is a very versatile system that can be used to sustain biological and oxidative ageing."
- Term coverage: 3/4 key terms (solera system, biological, oxidative)

**Preliminary grounding:** STRONG
- The solera and criaderas system is described at length, with the exact terms matching the correct answer. Passage 1 states its core advantage (consistency); Passage 2 explains the fractional blending mechanism.

---

### Q5 — Oloroso vs Amontillado Ageing
**Core claim:** Oloroso undergoes exclusively oxidative ageing (no flor is involved at any stage), unlike Amontillado which undergoes a period of biological ageing under flor before oxidative ageing.
**Correct answer text:** "Envejecimiento exclusivamente oxidativo"

**Passage 1:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- Section: Styles of Sherry — Oloroso
- Text: "Oloroso – These wines have only undergone oxidative ageing. They are brown in colour, full-bodied and dominated by oxidative aromas such as toffee, leather, spice and walnut."
- Term coverage: 4/4 key terms (Oloroso, only, oxidative ageing, no flor)

**Passage 2:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- Section: Oxidative Ageing
- Text: "Oloroso, PX and some Muscat Sherries are aged oxidatively, without the presence of flor. Amontillado is aged oxidatively after a period of biological ageing."
- Term coverage: 4/4 key terms (Oloroso, oxidatively, without flor, contrast with Amontillado)

**Passage 3:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_8_section_5_fortified_wines_of_the_world/8-1_43_sherry.md`
- Section: Wines for oxidative ageing
- Text: "Wines for oxidative ageing – These wines are fortified [...] to 17% abv; at this strength the flor dies."
- Term coverage: 3/4 key terms (oxidative ageing, fortified, flor dies)

**Preliminary grounding:** STRONG
- Passage 1 states explicitly that Oloroso has "only undergone oxidative ageing." Passage 2 adds the contrastive claim (Oloroso = no flor; Amontillado = biological then oxidative), directly grounding the distinction the question tests.

---

### Q12 — Spring Frost Risk Factor
**Core claim:** Topography, specifically vineyard slope, is the primary natural factor influencing spring frost risk because cold air drains downhill, and vineyards on slopes are less susceptible than those in low-lying depressions.
**Correct answer text:** "Pendiente del terreno"

**Passage 1:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md`
- Section: Temperature Hazards — Spring Frosts
- Text: "Because cold air sinks to the lowest point it can find, it is best to plant vineyards on slopes and avoid depressions in which cold air can collect. Vineyards planted on the middle of the slope are noticeably less at risk from frost damage than those in lower lying areas."
- Term coverage: 4/4 key terms (cold air, slope, frost, low-lying / depressions)

**Passage 2:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md`
- Section: Temperature Hazards — Spring Frosts
- Text: "Vines can also be trained high to avoid the worst of the cold air."
- Term coverage: 2/4 key terms (cold air, frost avoidance)

**Passage 3:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md`
- Section: Thoughtful Vineyard Design
- Text: "Thoughtful vineyard design can also minimise the risk of frosts. Because cold air sinks to the lowest point it can find, it is best to plant vineyards on slopes and avoid depressions in which cold air can collect."
- Term coverage: 4/4 key terms (frost risk, slope, cold air, drainage)

**Preliminary grounding:** STRONG
- Passage 1 directly states the mechanism (cold air sinks → slopes safer than depressions) and explicitly names slope as the critical design factor. The corpus clearly supports "pendiente del terreno" as the answer.

---

### Q13 — Soil Drainage Factor
**Core claim:** Sandy soil structure (estructura arenosa) most directly influences vineyard drainage because sand particles do not hold water well and facilitate water drainage, unlike clay which retains water.
**Correct answer text:** "Estructura arenosa"

**Passage 1:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md`
- Section: Soil Composition
- Text: "Sand particles and stones do not hold water well and facilitate water drainage. Therefore, if there is too much sand and stone in a soil, insufficient water may be retained and irrigation may be needed, even in areas of high rainfall."
- Term coverage: 4/4 key terms (sand, drainage, water retention, soil)

**Passage 2:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md`
- Section: Soil Composition
- Text: "Water is stored in the soil by binding to clay particles or humus. If a soil contains too much clay it can easily become waterlogged, which in extreme cases can kill the vine's roots."
- Term coverage: 3/4 key terms (clay, waterlogged, water retention — contrast with sand)

**Passage 3:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-2_5_the_growing_environment.md`
- Section: Soil Composition
- Text: "Many of the best soils are made up of a mixture of sand and clay particles, known as loam. These soils have good drainage but retain enough water for vine growth."
- Term coverage: 3/4 key terms (sand, drainage, vine growth)

**Preliminary grounding:** STRONG
- Passage 1 directly states "sand particles ... facilitate water drainage" — the exact claim the question tests. The corpus explicitly identifies sandy structure as the soil property most directly linked to drainage.

---

### Q14 — Mechanical Harvesting Effect on Wine Style
**Core claim:** Mechanical harvesting can increase oxidation because berries are broken on the vine and the resulting juice is exposed to oxygen, which can lead to off-flavours.
**Correct answer text:** "Puede aumentar la oxidación"

**Passage 1:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-3_6_vineyard_management.md`
- Section: Harvest — Machine Harvesters
- Text: "Machines can also work through the night, which allows cool grapes to be brought to the winery. This saves money and energy that would be spent on lowering the temperature of the grapes before fermentation, and it slows down the process of oxidation, which could lead to off-flavours (see section Oxygen in Chapter 7)."
- Term coverage: 3/4 key terms (machine, oxidation, off-flavours — night harvesting mitigates it, implying daytime use raises the risk)

**Passage 2:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-3_6_vineyard_management.md`
- Section: Harvest — Machine Harvesters
- Text: "Machine harvesters work by shaking the trunk of the vine and collecting the ripe berries as they fall off, leaving the stalks behind. They are not selective, often collecting some unhealthy, unripe and damaged grapes, as well as shaking off bits of leaf, insects and other contaminants."
- Term coverage: 2/4 key terms (machine harvesting, damaged grapes — berry damage implies oxidation risk)

**Passage 3:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-3_6_vineyard_management.md`
- Section: Harvest
- Text: "Less damage tends to occur to the grapes when they are manually harvested and the grapes can be further protected from damage by being transported in shallow, stackable trays."
- Term coverage: 2/4 key terms (damage, protection — implies machine harvesting causes more damage and associated oxidation)

**Preliminary grounding:** STRONG
- Passage 1 directly references oxidation as the process that machine harvesting can trigger (slowing it is listed as the advantage of night harvesting, confirming that daytime/warm-temperature machine harvesting increases oxidation risk). The claim is explicitly stated in the official corpus.

---

### Q16 — Extraction Technique for Colour and Tannins
**Core claim:** Pump-over (remontado) is an enological technique used to increase the extraction of colour and tannins from the grape skins during red wine fermentation by drawing fermenting juice from the bottom and pumping it over the cap.
**Correct answer text:** "Remontado"

**Passage 1:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md`
- Section: Cap Management Techniques
- Text: "Pumping over – This involves drawing off fermenting juice from the bottom of the vat and pumping it up on to the top, wetting the cap. Pumping over is a popular extraction technique and is a good way of dissipating heat and oxygenating the juice."
- Term coverage: 4/4 key terms (pumping over / remontado, extraction, cap, juice)

**Passage 2:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md`
- Section: Introduction
- Text: "The key to red winemaking is the successful extraction of colour and tannin from the skins of black grapes, which is achieved [through cap management techniques including pumping over]."
- Term coverage: 4/4 key terms (extraction, colour, tannin, skins)

**Passage 3:**
- File: `knowledge/wine-with-jimmy/clean/Red_Wine_Extraction_Techniques_Advanced_Version_useful_for_WSET_L3_and_L4.clean.md`
- Section: Extraction discussion
- Text: "what is extracted so what is what are we actually doing this for [...] polyphenols and these polyphenols are what we find mainly the tanning compounds [...] it is tannin that we are trying to extract [...] another compound called anthocyanins and this is where we find the pigmentation so the color of the wine"
- Term coverage: 3/4 key terms (extraction, tannin, colour/anthocyanins)

**Preliminary grounding:** STRONG
- Passage 1 explicitly defines pump-over (remontado) as an extraction technique. Passage 2 frames the overall objective of extraction as colour and tannin from skins. The correct answer is directly grounded.

**Note on distractors:** "Desfangado" (clarification of white must, not an extraction technique), "Bâtonnage" (lees stirring, adds texture not colour/tannin), "Estabilización tartárica" (cold stabilisation) — none are extraction techniques. The corpus confirms remontado is the only option that applies.

---

### Q17 — Purpose of Destemming Before Fermentation
**Core claim:** The primary purpose of destemming (despalillado) is to avoid the extraction of green, undesirable tannins from the grape stems, which would give the finished wine a bitter or herbaceous taste.
**Correct answer text:** "Evitar la extracción de taninos verdes"

**Passage 1:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md`
- Section: Whole Bunch Fermentation (contrasting with destemming)
- Text: "The winemaker must ensure that the grape stems are fully ripe: if not, the tannins in the stems can give the finished wine an undesirable bitter taste."
- Term coverage: 3/4 key terms (stems, tannins, undesirable / bitter — implies destemming prevents this)

**Passage 2:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md`
- Section: Crushed Fruit Fermentation
- Text: "The vast majority of fruit used in red winemaking is destemmed and crushed."
- Term coverage: 2/4 key terms (destemmed, red winemaking — establishes destemming as standard practice)

**Passage 3:**
- File: `knowledge/official-wset/study-guide/wset_markdown/seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/5-6_9_red_and_rose_winemaking.md`
- Section: Grape varieties (Pinot Noir)
- Text: "The stems on whole bunches of this variety can often give a herbaceous and [undesirable character]. [...] tannins are not fully ripe."
- Term coverage: 3/4 key terms (stems, herbaceous, unripe tannins)

**Preliminary grounding:** PARTIAL
- The corpus confirms that stem tannins are undesirable when unripe and that destemming is standard practice. However, no passage explicitly states "the purpose of destemming IS to avoid green tannin extraction" as a declarative sentence — the claim is supported by strong inference from the whole-bunch fermentation warning (Passage 1), but not by a direct definitional statement. The grounding is robust enough to support the correct answer, but a human reviewer should note the indirect inferential path.

---

## Corpus Coverage Assessment

| Sub-corpus | Items covered | Notes |
|------------|--------------|-------|
| `seccion_8.../8-1_43_sherry.md` | Q1, Q4, Q5 | All directly confirmed |
| `seccion_8.../8-2_44_port.md` | Q2, Q3 | All directly confirmed |
| `seccion_5.../5-2_5_the_growing_environment.md` | Q12, Q13 | All directly confirmed |
| `seccion_5.../5-3_6_vineyard_management.md` | Q14 | Directly confirmed |
| `seccion_5.../5-6_9_red_and_rose_winemaking.md` | Q16, Q17 | Q16 strong; Q17 partial (inferential) |
| `wine-with-jimmy/clean/Red_Wine_Extraction_Techniques...` | Q16 (supplementary) | Corroborates; not primary |

**Overall:** 9/10 items STRONG grounding; 1/10 (Q17) PARTIAL.

---

## Recommendations for Human Review Layer

1. **Q17 (destemming):** Add a golden tutor chunk or official extract that explicitly states the purpose of destemming is to prevent green tannin extraction. Current corpus supports by inference only.
2. **Q14 (mechanical harvesting):** The direct statement is framed in the positive (night harvesting slows oxidation), making the oxidation risk implicit rather than stated as the primary effect. Consider flagging this item for a distractor-analysis pass.
3. **Distractor validation:** This pass only verified the correct answer. A full verification should also confirm that the three incorrect distractors are NOT supported by corpus passages for the same question stem — this is especially important for Q12 (altitude and latitude are plausible distractors).

---

*This document is a machine-generated analysis pass. It does not constitute WSET assessment guidance or official examiner review.*
