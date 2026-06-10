# MASTER BANK V4 REMEDIATION REPORT

**Date:** 2026-06-09
**Remediation version:** v4
**Audit source:** MASTER_BANK_FORENSIC_AUDIT_V4.xlsx

---

## 1. Scope

This remediation targets only the 34 items identified in the V4 forensic audit as requiring intervention:

| Action | Count | Criterion |
|--------|-------|-----------|
| REWRITE | 31 | T/F or Matching format — incompatible with 4-option SBA schema |
| REPLACE | 3 | Out-of-scope health/alcohol topic — retire and replace with corpus-grounded RA1 items |
| **Total** | **34** | |

Items classified VERIFIED (42), VERIFIED_BY_INFERENCE (187), or MINOR_REVISION (353) are **not modified**.

---

## 2. REWRITE Items (31 total)

All 31 items were in True/False or Matching format. These formats are incompatible with the master bank's 4-option Single Best Answer (SBA) schema and cannot be meaningfully used for diagnostic assessment.

### Conversion methodology

1. Preserve original concept, learning objective, RA, topic, expected_keywords, expected_causal_links
2. Re-frame the stem as a positive discriminating question
3. Construct 4 options: 1 correct + 3 plausible distractors grounded in common misconceptions or adjacent correct facts
4. Set `review_state: needs_human_review` — formative drafts awaiting expert validation

### True/False items converted: 20

| ID | Concept | Was | RA | New stem (abbreviated) |
|----|---------|-----|-----|------------------------|
| Q678 | viticulture_vineyard_management | Verdadero | RA1 | ¿Cuál es el principal beneficio agronómico del uso de c... |
| Q679 | viticulture_clonal_selection | Verdadero | RA1 | ¿Cuál es el objetivo principal de la selección clonal e... |
| Q680 | viticulture_harvest | Verdadero | RA1 | ¿Por qué se realiza la cosecha nocturna en regiones de ... |
| Q681 | vinification_white | Verdadero | RA1 | ¿En qué momento del proceso de vinificación en blanco s... |
| Q682 | vinification_sulphur_dioxide | Verdadero | RA1 | ¿Cuál es la función principal del dióxido de azufre (SO... |
| Q683 | vinification_oak_ageing | Verdadero | RA1 | ¿Qué efecto tiene la fermentación o crianza de un vino ... |
| Q684 | vinification_vessels | Verdadero | RA1 | ¿Qué característica diferencia principalmente a los vin... |
| Q685 | viticulture_harvest | Verdadero | RA1 | ¿Cuál es la principal ventaja de la vendimia manual fre... |
| Q686 | vinification_fermentation | Verdadero | RA1 | ¿Cuál es el principal beneficio del uso de levaduras co... |
| Q687 | viticulture_climate_varieties | Verdadero | RA1 | ¿Por qué son preferibles las variedades de ciclo corto ... |
| Q775 | viticulture_site_selection | Falso | RA1 | ¿Qué orientación de las filas del viñedo maximiza gener... |
| Q776 | vinification_white_lees | Falso | RA1 | ¿Para qué se emplea principalmente el battonage (removi... |
| Q777 | viticulture_climate_types | Falso | RA1 | ¿Cuál de las siguientes características describe correc... |
| Q778 | vinification_mlf | Falso | RA1 | ¿Cuál es el efecto de la fermentación maloláctica (FML)... |
| Q779 | viticulture_soils | Falso | RA1 | ¿Cómo afectan los suelos arcillosos al cultivo de la vi... |
| Q780 | vinification_racking | Falso | RA1 | ¿Cuál es el objetivo principal del trasiego en la elabo... |
| Q781 | viticulture_altitude | Falso | RA1 | ¿Cuál de las siguientes afirmaciones describe correctam... |
| Q788 | viticulture_yield | Falso | RA1 | ¿Cuál es la relación más precisa entre el rendimiento p... |
| Q789 | vinification_oak_ageing | Falso | RA1 | ¿Qué determina el uso de barricas nuevas frente a barri... |
| Q790 | viticulture_climate_cool | Falso | RA1 | ¿Cómo influye el clima fresco sobre el nivel de acidez ... |

### Matching items converted: 11

| ID | Original descriptor | RA | New stem type |
|----|--------------------|----|----------------|
| Q742 | Zona vinícola reconocida por Syrah especiado | RA2 | Regional/definitional SBA |
| Q743 | Zona con sistema de clasificación por crus | RA2 | Regional/definitional SBA |
| Q744 | Región con legislación de 'Gran Reserva' | RA2 | Regional/definitional SBA |
| Q745 | Vino tinto con crianza mínima de 3 años | RA2 | Regional/definitional SBA |
| Q746 | Clima mediterráneo con influencia marítima | RA2 | Regional/definitional SBA |
| Q747 | Región productora de Nebbiolo | RA2 | Regional/definitional SBA |
| Q748 | Región famosa por Sauvignon Blanc | RA2 | Regional/definitional SBA |
| Q765 | Despalillado | RA1 | Regional/definitional SBA |
| Q795 | Área con suelos volcánicos ricos en hierro | RA2 | Regional/definitional SBA |
| Q796 | Área argentina de mayor altitud | RA2 | Regional/definitional SBA |
| Q797 | Productor notable de vinos con botrytis | RA2 | Regional/definitional SBA |

### RA breakdown

| RA | Count |
|----|-------|
| RA1 | 21 |
| RA2 | 10 |

---

## 3. REPLACE Items (3 total)

### Q60 → Retired (health consequences) / Replaced with HC_DIURNAL_RANGE_FRESHNESS

**Original:** "¿Cuál es una consecuencia típica del consumo excesivo de alcohol?"
**Retirement reason:** Out-of-scope health topic; not in WSET L3 Study Guide
**Replacement:** Diurnal temperature range effects on acidity and freshness (RA1)
**Grounding:** HC_DIURNAL_RANGE_FRESHNESS causal chain
**New gap filled:** RA1 climate mechanism — diurnal range → freshness previously absent

### Q315 → Retired (health advice) / Replaced with HC_MLF_ACIDITY_TEXTURE

**Original:** "¿Cuál es una recomendación saludable relacionada con el consumo moderado de vino?"
**Retirement reason:** Prescriptive health recommendations outside WSET L3 curriculum
**Replacement:** MLF effect on white wine texture (RA1)
**Grounding:** HC_MLF_ACIDITY_TEXTURE causal chain
**New gap filled:** MLF → texture/creaminess mechanism (distinct from Q778 which covers acidity direction)

### Q716 → Retired (health risk) / Replaced with HC_ALTITUDE_TEMPERATURE

**Original:** "¿Cuál de los siguientes es un riesgo del consumo excesivo de alcohol?"
**Retirement reason:** Health risk topic outside WSET L3 curriculum; governance risk
**Replacement:** Altitude effects on aromatic profile (RA1)
**Grounding:** HC_ALTITUDE_TEMPERATURE causal chain
**New gap filled:** Altitude → aromatic complexity mechanism (distinct from Q781 which covers acidity/maturation)

---

## 4. Bank Status After Remediation

| Metric | Before | After |
|--------|--------|-------|
| Total items | 616 | 616 |
| VERIFIED | 42 | 42 |
| VERIFIED_BY_INFERENCE | 187 | 187 |
| MINOR_REVISION | 353 | 353 |
| REWRITE | 31 | 0 |
| REPLACE | 3 | 0 |
| Valid items | 581 | 616 |

**Success criterion met:** 0 items remain at REWRITE or REPLACE.

---

## 5. Governance

All 34 remediated items:

```
safe_for_examiner = False
examiner_scoring_allowed = False
official_wset_question = False
training_item_only = True
uses_llm = False / uses_api = False / uses_embeddings = False
review_state = needs_human_review
```

---

## 6. Files Produced

| File | Description |
|------|-------------|
| `MASTER_BANK_REMEDIATION_V4.xlsx` | Full remediation table + executive summary + REPLACE detail |
| `MASTER_BANK_PATCH_V4.json` | 34 items in master_bank_patch_v1 schema |
| `REMEDIATION_REPORT_V4.md` | This report |

---

*Development planning artifact. Does not represent WSET assessment or examiner evaluation. All items require human expert review before activation.*
