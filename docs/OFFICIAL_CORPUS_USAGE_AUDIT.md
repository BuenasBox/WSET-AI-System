# Official Corpus Usage Audit
**Phase:** V4.3 Part 3  
**Date:** 2026-06-09

---

## Official WSET Asset Inventory

| Family | Files | Format |
|--------|-------|--------|
| Study guide | 1 PDF + markdown conversion + 52 extracted chunks (.jsonl) | Active in retrieval |
| Specification | 1 MD + 1 PDF | Stored only |
| SAT | 1 MD + 1 PDF | Stored only |
| Marking keys | 6 MD + 6 PDF | Stored only |
| Sample papers / model answers | 6 MD + 6 PDF | Stored only |
| Mock exams | (directory present) | Unknown |

---

## Utilization by Document Family

### Study Guide (`knowledge/official-wset/study-guide/`)
**Status: USED**

The study guide is the only official document family actively consumed by the runtime.

- **Chunked** into 52 `.jsonl` entries at `official-chunks/official_wset_chunks.jsonl`
- **Loaded** by `tools/retrieval/tutor_retrieval_sandbox.py` at startup alongside Wine With Jimmy, golden tutor, and dictionary chunks
- **Scored** with `official_source_boost` and `official_exam_register_boost` scoring signals in `score_chunk_for_query()`
- **Filtered** by governance: `official_grading_authority` flag checked before rendering
- **Source type**: `"official_wset_extracted"` — receives retrieval priority boost

### Specification (`knowledge/official-wset/specification/`)
**Status: NOT USED**

- Markdown file exists: `wset_l3wines_specification_es_highres_aug2023_issue201.md`
- No runtime component loads or queries this file
- Content was manually used as a source during Phase X.1 (to populate `knowledge/assessment-framework/`) but those JSON files are also not loaded at runtime

### SAT (`knowledge/official-wset/sat/`)
**Status: NOT USED**

- Markdown file exists: `wset_l3wines_sat_es_may2022_issue2.md`
- No runtime component loads or references this file directly
- SAT structure was extracted into `knowledge/sat-framework/` during Phase X.1 but those files are also not loaded at runtime

### Marking Keys (`knowledge/official-wset/marking-keys/`)
**Status: NOT USED**

- 6 marking key MDs present (one per exam wine)
- No runtime component references these files
- Mark allocation rules were extracted into `knowledge/evaluator-framework/` during Phase X.1 but those files are not loaded at runtime

### Model Answers / Sample Papers (`knowledge/official-wset/sample-papers/`)
**Status: NOT USED**

- 6 model answer MDs present (one per exam wine)
- No runtime component references these files
- Distinction patterns were extracted into `knowledge/distinction-patterns/` during Phase X.1 but those files are not loaded at runtime

---

## Component-Level Utilization Matrix

| Component | Study guide | Spec | SAT | Marking keys | Model answers |
|-----------|-------------|------|-----|--------------|---------------|
| Retrieval (tutor_retrieval_sandbox) | ✅ USED | ✗ | ✗ | ✗ | ✗ |
| Chunking layer (official_wset_chunks) | ✅ USED | ✗ | ✗ | ✗ | ✗ |
| Answer builder (tutor) | Indirect (via chunks) | ✗ | ✗ | ✗ | ✗ |
| SAT reasoner | ✗ | ✗ | ✗ | ✗ | ✗ |
| Open response evaluator | ✗ | ✗ | ✗ | ✗ | ✗ |
| Mentor framework | ✗ | ✗ | ✗ | ✗ | ✗ |
| Evaluator guidance | ✗ | ✗ | ✗ | ✗ | ✗ |
| Dashboard | ✗ | ✗ | ✗ | ✗ | ✗ |
| Phase X.1 JSON assets | ✗ source only | Source only | Source only | Source only | Source only |

**Note:** Phase X.1 extracted knowledge from Spec/SAT/Marking Keys/Model Answers into 18 structured JSON files. Those JSON files are stored in `knowledge/` but are not yet consumed by any runtime module.

---

## Summary

Only the study guide is active in the runtime (52 chunks, boosted in retrieval scoring). The Specification, SAT, Marking Keys, and Model Answers are stored as Markdown but have no runtime consumers. The Phase X.1 intelligence extraction produced 18 JSON files that are also not yet connected to any runtime module.
