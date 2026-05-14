# WSET-AI-System — Knowledge Map Build Report

**Phase:** 1 — Semantic Architecture and Knowledge Mapping  
**Build date:** 2026-05-13  
**Status:** Phase 1 complete — all planned nodes created  
**Report generated:** 2026-05-13

---

## 1. Executive Summary

Phase 1 of the WSET-AI-System knowledge map is complete. The semantic architecture has been designed and fully populated with exemplar content covering 8 core WSET Level 3 concepts drawn from RA1 (viticulture and winemaking) and RA3 (Champagne production). A total of 48 knowledge graph nodes have been created across 5 node types, along with 5 JSON Schema definitions, 4 architecture and governance documents, and a manifest file.

All content is in `"ingestion_status": "draft"` and requires human L3/L4 validation before production deployment.

---

## 2. Nodes Created

### 2.1 JSON Schemas (5)

| Schema file | Node type | Validation |
|-------------|-----------|------------|
| `manifests/schemas/topic.schema.json` | Topics | Draft-07, additionalProperties: false |
| `manifests/schemas/concept.schema.json` | Concepts | Draft-07, additionalProperties: false |
| `manifests/schemas/relationship.schema.json` | Relationships | Draft-07, additionalProperties: false |
| `manifests/schemas/misconception.schema.json` | Misconceptions | Draft-07, additionalProperties: false |
| `manifests/schemas/causal_chain.schema.json` | Causal Chains | Draft-07, additionalProperties: false |

### 2.2 Concept Nodes (8)

| Concept ID | Topic | Misconceptions | Chains |
|------------|-------|---------------|--------|
| `C_ACIDITY` | T_RA1_WINE_COMPONENTS | MC_ACIDITY_01, MC_ACIDITY_02 | CC_COOL_CLIMATE_ACIDITY, CC_MLF_ACIDITY, CC_ACIDITY_AGEABILITY |
| `C_TANNIN` | T_RA1_WINE_COMPONENTS | MC_TANNIN_01, MC_TANNIN_02 | CC_TANNIN_AGEABILITY, CC_WHOLE_BUNCH_TANNIN, CC_OAK_TANNIN |
| `C_COOL_CLIMATE` | T_RA1_CLIMATE_VITICULTURE | MC_COOL_CLIMATE_01, MC_COOL_CLIMATE_02 | CC_COOL_CLIMATE_ACIDITY, CC_COOL_CLIMATE_AROMA, CC_COOL_CLIMATE_ALCOHOL |
| `C_BOTRYTIS_CINEREA` | T_RA1_VITICULTURE_HAZARDS | MC_BOTRYTIS_01 | CC_NOBLE_ROT_SUGAR_CONCENTRATION, CC_BOTRYTIS_ACIDITY_REDUCTION |
| `C_WHOLE_BUNCH_FERMENTATION` | T_RA1_WINEMAKING_RED | MC_WHOLE_BUNCH_01 | CC_WHOLE_BUNCH_TANNIN, CC_WHOLE_BUNCH_PH |
| `C_CHAMPAGNE_LEES_AGEING` | T_RA3_CHAMPAGNE_PRODUCTION | MC_LEES_AGEING_01 | CC_LEES_AGEING_AUTOLYSIS, CC_AUTOLYSIS_AROMA_TEXTURE |
| `C_OAK_INFLUENCE` | T_RA1_WINEMAKING_AGEING | MC_OAK_01, MC_OAK_02 | CC_OAK_TANNIN, CC_OAK_FLAVOUR, CC_OAK_MICROOX |
| `C_MALOLACTIC_CONVERSION` | T_RA1_WINEMAKING_WHITE | MC_MLF_01, MC_MLF_02 | CC_MLF_ACIDITY, CC_MLF_TEXTURE, CC_MLF_DIACETYL |

### 2.3 Misconception Nodes (13)

| Misconception ID | Related concept | Severity | Frequency | Distinction-relevant |
|-----------------|----------------|----------|-----------|---------------------|
| `MC_ACIDITY_01` | C_ACIDITY | medium | common | yes |
| `MC_ACIDITY_02` | C_ACIDITY | high | very_common | yes |
| `MC_TANNIN_01` | C_TANNIN | high | very_common | yes |
| `MC_TANNIN_02` | C_TANNIN | high | very_common | yes |
| `MC_COOL_CLIMATE_01` | C_COOL_CLIMATE | medium | common | no |
| `MC_COOL_CLIMATE_02` | C_COOL_CLIMATE | high | very_common | yes |
| `MC_BOTRYTIS_01` | C_BOTRYTIS_CINEREA | **critical** | common | yes |
| `MC_OAK_01` | C_OAK_INFLUENCE | medium | common | no |
| `MC_OAK_02` | C_OAK_INFLUENCE | high | common | yes |
| `MC_MLF_01` | C_MALOLACTIC_CONVERSION | medium | very_common | no |
| `MC_MLF_02` | C_MALOLACTIC_CONVERSION | high | common | yes |
| `MC_WHOLE_BUNCH_01` | C_WHOLE_BUNCH_FERMENTATION | medium | common | yes |
| `MC_LEES_AGEING_01` | C_CHAMPAGNE_LEES_AGEING | medium | common | yes |

**Critical misconceptions requiring priority tutor intervention:** `MC_BOTRYTIS_01` (botrytis = always noble rot). This is the only critical-severity misconception in Phase 1.

**Highest-frequency errors (very_common):** `MC_ACIDITY_02`, `MC_TANNIN_01`, `MC_TANNIN_02`, `MC_COOL_CLIMATE_02`, `MC_MLF_01`.

### 2.4 Causal Chain Nodes (17)

| Chain ID | Complexity | Exam relevance | Starts at |
|----------|-----------|---------------|-----------|
| `CC_COOL_CLIMATE_ACIDITY` | moderate | **critical** | C_COOL_CLIMATE |
| `CC_COOL_CLIMATE_AROMA` | moderate | **critical** | C_COOL_CLIMATE |
| `CC_COOL_CLIMATE_ALCOHOL` | simple | high | C_COOL_CLIMATE |
| `CC_NOBLE_ROT_SUGAR_CONCENTRATION` | complex | **critical** | C_BOTRYTIS_CINEREA |
| `CC_BOTRYTIS_ACIDITY_REDUCTION` | complex | **critical** | C_BOTRYTIS_CINEREA |
| `CC_MLF_ACIDITY` | moderate | **critical** | C_MALOLACTIC_CONVERSION |
| `CC_MLF_TEXTURE` | moderate | high | C_MALOLACTIC_CONVERSION |
| `CC_MLF_DIACETYL` | complex | high | C_MALOLACTIC_CONVERSION |
| `CC_OAK_TANNIN` | moderate | high | C_OAK_INFLUENCE |
| `CC_OAK_FLAVOUR` | moderate | high | C_OAK_INFLUENCE |
| `CC_OAK_MICROOX` | complex | high | C_OAK_INFLUENCE |
| `CC_TANNIN_AGEABILITY` | complex | **critical** | C_TANNIN |
| `CC_WHOLE_BUNCH_TANNIN` | complex | high | C_WHOLE_BUNCH_FERMENTATION |
| `CC_WHOLE_BUNCH_PH` | complex | high | C_WHOLE_BUNCH_FERMENTATION |
| `CC_LEES_AGEING_AUTOLYSIS` | complex | **critical** | C_CHAMPAGNE_LEES_AGEING |
| `CC_AUTOLYSIS_AROMA_TEXTURE` | complex | **critical** | C_CHAMPAGNE_LEES_AGEING |
| `CC_ACIDITY_AGEABILITY` | complex | **critical** | C_ACIDITY |

**Critical-exam-relevance chains (8):** CC_COOL_CLIMATE_ACIDITY, CC_COOL_CLIMATE_AROMA, CC_NOBLE_ROT_SUGAR_CONCENTRATION, CC_BOTRYTIS_ACIDITY_REDUCTION, CC_MLF_ACIDITY, CC_TANNIN_AGEABILITY, CC_LEES_AGEING_AUTOLYSIS, CC_AUTOLYSIS_AROMA_TEXTURE, CC_ACIDITY_AGEABILITY.

### 2.5 Relationship Nodes (10)

| Relationship ID | Type | Source → Target |
|----------------|------|----------------|
| `R_COOL_CLIMATE__INCREASES__ACIDITY` | increases | C_COOL_CLIMATE → C_ACIDITY |
| `R_MALOLACTIC_CONVERSION__REDUCES__ACIDITY` | reduces | C_MALOLACTIC_CONVERSION → C_ACIDITY |
| `R_OAK_INFLUENCE__INCREASES__TANNIN` | increases | C_OAK_INFLUENCE → C_TANNIN |
| `R_BOTRYTIS_CINEREA__REDUCES__ACIDITY` | reduces | C_BOTRYTIS_CINEREA → C_ACIDITY |
| `R_WHOLE_BUNCH_FERMENTATION__INCREASES__TANNIN` | increases | C_WHOLE_BUNCH_FERMENTATION → C_TANNIN |
| `R_WHOLE_BUNCH_FERMENTATION__REDUCES__ACIDITY` | reduces | C_WHOLE_BUNCH_FERMENTATION → C_ACIDITY |
| `R_ACIDITY__INFLUENCES__TANNIN` | influences | C_ACIDITY → C_TANNIN |
| `R_CHAMPAGNE_LEES_AGEING__PRODUCES__AUTOLYTIC_AROMA` | produces | C_CHAMPAGNE_LEES_AGEING → [autolysis] |
| `R_COOL_CLIMATE__OFTEN_CONFUSED_WITH__UNDER_RIPE` | often_confused_with | C_COOL_CLIMATE ↔ [under-ripeness] |
| `R_BOTRYTIS_CINEREA__CONTRASTS_WITH__GREY_ROT` | contrasts_with | C_BOTRYTIS_CINEREA ↔ grey rot |

---

## 3. Documentation Created

| Document | Location | Purpose |
|----------|----------|---------|
| KNOWLEDGE_GRAPH_ARCHITECTURE.md | `docs/` | Full architecture specification, node types, traversal patterns, Tutor Agent integration |
| KNOWLEDGE_MAP_VALIDATION_RULES.md | `docs/` | L1–L4 validation rules, QA checklist, deprecation policy |
| knowledge_map_build_report.md | `docs/` | This document |
| knowledge_map_manifest.json | `knowledge/knowledge-map/manifests/` | Index of all nodes with file paths and metadata |

---

## 4. Cross-Reference Coverage Analysis

### 4.1 Concept → Misconception coverage

All 8 concepts have at least 1 misconception. 5 concepts (C_ACIDITY, C_TANNIN, C_COOL_CLIMATE, C_OAK_INFLUENCE, C_MALOLACTIC_CONVERSION) have 2 misconceptions each.

### 4.2 Concept → Causal chain coverage

All 8 concepts appear in at least 1 causal chain as starting factor or intermediate step. Average chains per concept: 2.1.

### 4.3 Graph connectivity

The relationships graph for Phase 1 shows two primary hubs:
- **C_ACIDITY** is the most connected target concept (receives edges from C_COOL_CLIMATE, C_MALOLACTIC_CONVERSION, C_BOTRYTIS_CINEREA, C_WHOLE_BUNCH_FERMENTATION — 4 incoming relationships)
- **C_TANNIN** is the second most connected target (receives edges from C_OAK_INFLUENCE, C_WHOLE_BUNCH_FERMENTATION, C_ACIDITY — 3 incoming relationships)

This connectivity reflects the WSET exam's emphasis on acidity and tannin as the structural pillars around which multiple concepts converge.

---

## 5. Quality Observations

### 5.1 Strength of Phase 1 content

- All 9 critical-exam-relevance chains include `distinction_note` fields specifying the precise mechanistic knowledge required for Distinction
- The botrytis dual-outcome mechanism (noble rot vs. grey rot) is fully documented with appropriate `contrasts_with` relationship and `critical` severity misconception
- MLF diacetyl variability is correctly modelled as a controllable winemaking parameter rather than a fixed outcome
- Oak new-vs-old distinction, toast level effects, and micro-oxygenation are all covered with separate chains

### 5.2 Known gaps in Phase 1

- **No topic nodes created.** All concept nodes reference topic IDs (T_RA1_*, T_RA3_*) that do not yet have corresponding files. This is a planned gap deferred to Phase 2.
- **No SAT integration.** The Systematic Approach to Tasting assessment framework is not yet linked to the knowledge graph. Phase 7 is planned for this.
- **RA2 regional content absent.** No regional wine concept nodes have been created. The knowledge graph currently has no direct representation of wine regions, appellations, or regional styles — all of which are heavily exam-tested.
- **No Examiner Agent corpus.** The knowledge graph is entirely pedagogical (Tiers 2–4). Tier 0–1 official WSET content for the Examiner Agent is outside the scope of this phase and governed separately by AGENT_BOUNDARIES.md.

### 5.3 Cross-reference warnings

The following cross-references in concept files point to causal chains or misconceptions that were created after the concept files (i.e., they were listed as `cause_effect_links` or `common_misconceptions` in the concept files but the chain/misconception files may have been created in a different build pass). These require L2 validation to confirm they resolve correctly:

- `C_ACIDITY` → `CC_MLF_ACIDITY` (created in Phase 1 chain batch)
- `C_TANNIN` → `CC_OAK_TANNIN`, `CC_WHOLE_BUNCH_TANNIN` (created in Phase 1 chain batch)
- All concept files → their respective `MC_*` entries (all created in Phase 1 misconception batch)

No dangling references are expected, but L2 automated validation should confirm this before deployment.

---

## 6. Validation Status

| Node type | Created | Validated (L4) | % validated |
|-----------|---------|----------------|-------------|
| Schemas | 5 | 0 | 0% |
| Concepts | 8 | 0 | 0% |
| Misconceptions | 13 | 0 | 0% |
| Causal Chains | 17 | 0 | 0% |
| Relationships | 10 | 0 | 0% |
| **Total** | **53** | **0** | **0%** |

All content is `"ingestion_status": "draft"`. The following actions are required before any node can be promoted to `"validated"`:

1. Run L1 automated schema validation (requires `validate_knowledge_map.py` — pending Phase 1.5)
2. Run L2 cross-reference integrity check
3. Human L3 pedagogical review by a WSET L3 content editor
4. Human L4 factual accuracy review by a WSET-qualified reviewer

Estimated L4 review effort: approximately 3–5 hours for all Phase 1 content by a qualified reviewer.

---

## 7. Next Steps — Phase 2 Recommendations

Priority order for Phase 2 work:

1. **Create validation script** (`tools/validate_knowledge_map.py`) to automate L1/L2 checks
2. **Create topic nodes** for all RA1 topics referenced in Phase 1 concept files
3. **Extend misconception coverage** for RA2 regional content (common student errors about regions, grape varieties, wine laws)
4. **Build RA2 concept nodes** starting with highest-frequency exam topics (Bordeaux, Burgundy, Champagne, Rioja, Mosel, Barossa Valley)
5. **SAT integration planning** — design schema extensions for sensory → structural inference chains
6. **L3/L4 validation** of all Phase 1 content — prerequisite for any production deployment

---

*This report reflects the state of the knowledge map as of 2026-05-13. It is an internal development document and does not represent official WSET guidance or assessment policy.*
