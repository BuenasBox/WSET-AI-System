# WSET-AI-System — Documentation Index

This index maps every document in `docs/` to its purpose, canonical status, and
relationship to other documents. Use this as the entry point when navigating the
architecture or governance documentation.

**Last updated:** 2026-05-14
**Maintainer:** Update this index whenever a new document is added or deprecated.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ Canonical | Authoritative, up-to-date. Use this document. |
| 📖 Reference | Useful background or decision history. Not the primary authority. |
| ⚠️ Stale | Content no longer reflects the current project state. Do not act on this document without cross-checking the canonical source. |
| 🔲 Placeholder | File exists but content is minimal or pending. |

---

## Architecture Documents

| File | Status | Purpose | Notes |
|------|--------|---------|-------|
| `system-architecture.md` | ✅ Canonical | Original high-level system architecture — three-agent model, folder layout, scope definition | The primary early-phase architecture document. Predates the Phase C semantic retrieval layer. |
| `ARCHITECTURE.md` | 🔲 Placeholder | Intended as a consolidated architecture doc | Currently empty (1 line). Superseded in practice by `system-architecture.md` and `SEMANTIC_RETRIEVAL_ARCHITECTURE.md`. Do not use as a reference. |
| `SYSTEM_ARCHITECTURE.md` | 🔲 Placeholder | Duplicate of `ARCHITECTURE.md` | 4-line placeholder. Superseded. Do not use as a reference. |
| `SEMANTIC_RETRIEVAL_ARCHITECTURE.md` | ✅ Canonical | **Phase C retrieval architecture.** Composite scoring formulas (Tutor and Examiner), hard exclusion rules, retrieval failure modes, graph traversal bonus, minimum composite score thresholds. | The authoritative source for all retrieval weighting decisions. Cross-referenced by both retrieval matrix JSON files. |
| `KNOWLEDGE_GRAPH_ARCHITECTURE.md` | ✅ Canonical | Knowledge graph node types, edge types, 4 traversal strategies, Tutor Agent integration guidelines, forbidden operations | Authoritative for all knowledge-map schema and graph design decisions. |
| `KNOWLEDGE_GRAPH_RETRIEVAL_STRATEGY.md` | ✅ Canonical | GraphRAG strategy — 5-layer retrieval fusion pipeline, 6 traversal strategies, semantic filtering rules, graph integrity requirements | Companion to `SEMANTIC_RETRIEVAL_ARCHITECTURE.md` for graph-specific retrieval. |
| `transcript_cleaning_semantic_prep_architecture.md` | 📖 Reference | Transcript cleaning and chunk preparation architecture for Wine With Jimmy pipeline | Documents the `cleaner.py` design rationale and cleaning stages. |
| `youtube-transcription-ingestion-pipeline.md` | 📖 Reference | End-to-end transcript ingestion pipeline architecture | Documents pipeline stages from discovery to enrichment-ready. |

---

## Governance Documents

| File | Status | Purpose | Notes |
|------|--------|---------|-------|
| `AGENT_BOUNDARIES.md` | ✅ Canonical | **Primary governance authority.** Defines the Tutor/Examiner agent boundary, what each agent may and may not do, and the governance framework for all source access. | All trust-tier and retrieval governance documents derive from this. |
| `EXAMINER_CALIBRATION_RULES.md` | ✅ Canonical | Examiner Agent calibration rules — 11 sections covering calibration isolation, authorised sources, forbidden sources, scoring authority, semantic drift monitoring, forbidden reasoning patterns, mandatory disclaimer | Authoritative for all Examiner Agent corpus and scoring decisions. |
| `DATA_GOVERNANCE.md` | ✅ Canonical | Data governance policies for the project — source classification, IP rules, pipeline rules | |
| `AI_CONTRACT.md` | 🔲 Placeholder | Intended as a formal AI behaviour contract | Currently empty. |
| `DECISIONS.md` | 📖 Reference | Architectural decision log — records key design choices and their rationale | Update when making significant architectural decisions. |

---

## Pedagogical Documents

| File | Status | Purpose | Notes |
|------|--------|---------|-------|
| `PEDAGOGICAL_CLASSIFICATION_SYSTEM.md` | ✅ Canonical | 9 pedagogical roles, role-retrieval interaction matrix, forbidden role assignments, context override logic | Authoritative for all content annotation and retrieval role decisions. |
| `TUTOR_REASONING_PATTERNS.md` | ✅ Canonical | 8 Tutor Agent reasoning patterns — trigger conditions, numbered structural steps, Distinction mode additions, pattern selection decision tree | Authoritative for Tutor Agent response construction. |

---

## Knowledge Map Documents

| File | Status | Purpose | Notes |
|------|--------|---------|-------|
| `KNOWLEDGE_MAP_VALIDATION_RULES.md` | ✅ Canonical | L1–L4 validation framework for all knowledge-map JSON nodes — schema compliance, cross-reference integrity, pedagogical quality, WSET factual accuracy | Required reading before adding or modifying any knowledge-map node. |
| `knowledge_map_build_report.md` | 📖 Reference | Phase 1 build inventory — node count tables, cross-reference coverage, validation status, quality observations | Snapshot as of Phase 1 completion. Will be superseded by Phase 2 build report. |

---

## Planning and Requirements Documents

| File | Status | Purpose | Notes |
|------|--------|---------|-------|
| `product-requirements.md` | 📖 Reference | Product requirements for the full WSET-AI-System | |
| `roadmap.md` | 📖 Reference | Phase-by-phase project roadmap | |
| `folder_structure_audit.md` | ⚠️ Stale | Audit of folder structure from an early project phase | Does **not** reflect the current directory structure, which has grown substantially across Phases A, B, and C. Do not use as a reference for the current layout. See `knowledge/knowledge-map/manifests/knowledge_map_manifest.json` for the authoritative node inventory. |

---

## Canonical Source for Key Governance Questions

| Question | Authoritative Document |
|----------|----------------------|
| What may the Examiner Agent use? | `AGENT_BOUNDARIES.md` + `EXAMINER_CALIBRATION_RULES.md` + `knowledge/enrichment/trust-tier-matrix.json` |
| What are the retrieval weights? | `knowledge/enrichment/retrieval_priority_matrix.json` |
| What trust tier is a source? | `knowledge/enrichment/trust-tier-matrix.json` |
| How is a knowledge-map node validated? | `KNOWLEDGE_MAP_VALIDATION_RULES.md` |
| How does retrieval scoring work? | `SEMANTIC_RETRIEVAL_ARCHITECTURE.md` |
| What pedagogical roles exist? | `PEDAGOGICAL_CLASSIFICATION_SYSTEM.md` |
| How does graph traversal work? | `KNOWLEDGE_GRAPH_RETRIEVAL_STRATEGY.md` |
| What is the calibration gate? | `EXAMINER_CALIBRATION_RULES.md` §9 |
| What are the Wine With Jimmy rules? | `knowledge/wine-with-jimmy/PIPELINE_GOVERNANCE.md` |
| What is the wset_master_dictionary? | `knowledge/enrichment/wset_master_dictionary/GOVERNANCE.md` |

---

## Document Naming Conventions

The `docs/` directory contains two generations of documents reflecting naming
convention changes during the project:

- **Generation 1 (lowercase-hyphen):** `system-architecture.md`, `product-requirements.md`,
  `roadmap.md`, `youtube-transcription-ingestion-pipeline.md` — written in the early project phase.
- **Generation 2 (UPPERCASE_UNDERSCORE):** `SEMANTIC_RETRIEVAL_ARCHITECTURE.md`,
  `EXAMINER_CALIBRATION_RULES.md`, etc. — written during Phase C (semantic retrieval layer).

New documents should use **UPPERCASE_UNDERSCORE** naming to match Generation 2.

---

*To add a document: create the file, then add a row to this index with status, purpose, and any notes about its relationship to other documents.*
