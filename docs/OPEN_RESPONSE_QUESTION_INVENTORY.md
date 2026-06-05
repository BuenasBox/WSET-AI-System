# Open Response Question Inventory

Phase: 4A.3.7.44  
Source: `knowledge/question-bank/structured/wset3_questions.json`  
Inventory mode: deterministic local inspection only

## Summary

- Total structured questions inspected: 616
- Source question type distribution:
  - `theory`: 595
  - `short_answer`: 21
- Open response candidates detected: 21
- Detected open response type values: `short_answer`
- Candidate IDs: 18, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817

## Inventory Table

| ID | Type | RA | Topic | Subtopic | Difficulty | Causal chain | Missing fields / quality notes |
|---|---|---|---|---|---|---|---|
| 18 | short_answer | missing | sulfitos | SO2 / character of wine | intermediate | missing | Legacy SBA residue: options and answer letter remain populated; no RA; no causal link. |
| 798 | short_answer | RA1 | sostenibilidad | precio | distinction | present | Structurally usable; source support is source metadata only. |
| 799 | short_answer | RA1 | fermentacion malolactica | vino blanco | distinction | present | Structurally usable; source support is source metadata only. |
| 800 | short_answer | RA1 | altitud | clima | intermediate | present | Structurally usable; source support is source metadata only. |
| 801 | short_answer | RA1 | orientacion | pendiente | intermediate | present | Structurally usable; source support is source metadata only. |
| 802 | short_answer | RA1 | oxidacion | vino blanco | intermediate | present | Structurally usable; source support is source metadata only. |
| 803 | short_answer | RA1 | levaduras | fermentacion | intermediate | present | Structurally usable; source support is source metadata only. |
| 804 | short_answer | RA1 | suelo | drenaje | intermediate | present | Structurally usable; source support is source metadata only. |
| 805 | short_answer | RA1 | roble | roble americano | distinction | present | Structurally usable; source support is source metadata only. |
| 806 | short_answer | RA1 | manejo del dosel | tecnicas de vinedo | intermediate | present | Structurally usable; source support is source metadata only. |
| 807 | short_answer | RA1 | decisiones humanas | clima extremo | distinction | present | Structurally usable; source support is source metadata only. |
| 808 | short_answer | RA1 | densidad de plantacion | competencia | distinction | present | Structurally usable; source support is source metadata only. |
| 809 | short_answer | RA1 | levaduras seleccionadas | levaduras autoctonas | distinction | present | Structurally usable; source support is source metadata only. |
| 810 | short_answer | RA1 | estres hidrico | calidad | distinction | present | Structurally usable; source support is source metadata only. |
| 811 | short_answer | RA1 | latitud | altitud | intermediate | present | Structurally usable; source support is source metadata only. |
| 812 | short_answer | RA1 | estres hidrico | calidad | intermediate | present | Structurally usable; source support is source metadata only. |
| 813 | short_answer | RA1 | levaduras autoctonas | riesgo enologico | foundational | present | Structurally usable; source support is source metadata only. |
| 814 | short_answer | RA1 | poda de invierno | rendimiento | foundational | present | Structurally usable; source support is source metadata only. |
| 815 | short_answer | RA1 | acero inoxidable | fermentacion | foundational | present | Structurally usable; source support is source metadata only. |
| 816 | short_answer | RA1 | maceracion prolongada | vino tinto | distinction | present | Structurally usable; source support is source metadata only. |
| 817 | short_answer | RA1 | suelo | arena | intermediate | present | Structurally usable; source support is source metadata only. |

## Structural Quality

- RA coverage: 20 of 21 candidates include an RA signal in `expected_topics`.
- Topic/subtopic coverage: all candidates have topic candidates in `expected_topics`; topic/subtopic still require canonical taxonomy normalization.
- Expected concept coverage: all candidates have usable `expected_keywords`; these can seed deterministic formative concept coverage.
- Causal chain coverage: 20 of 21 candidates include at least one expected causal link.
- Corpus support: all candidates currently have source metadata, but none include explicit source chunk IDs in the open response contract.
- Legacy format residue: all detected open response records still include an `options` object from the structured bank format. Candidate 18 also carries a populated answer letter and answer text, so it should be reviewed before activation.

## Governance Status

The inventory did not activate open response items in any cockpit or frontend. The detected candidates remain training-only source records. The new pipeline foundation preserves project governance defaults: no examiner authority, no official evaluation, no LLM/API calls, no embeddings, no vector database, and no cloud services.
