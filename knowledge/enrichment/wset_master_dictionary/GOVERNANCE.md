# WSET Master Dictionary — Governance Record

**Status:** Provisional — pending L4 human review
**Provisional Trust Tier:** 1 (Official WSET Specification — extracted vocabulary)
**Examiner Agent:** FORBIDDEN until calibration gate is passed
**Date established:** 2026-05-14
**Review required by:** Before any retrieval system ingests this vocabulary

---

## 1. What Is This Artifact?

The `wset_master_dictionary/` directory contains a controlled-vocabulary extraction
derived from three official WSET Level 3 source documents:

| Source | File |
|--------|------|
| WSET L3 Specification (2026) | `knowledge/official-wset/specification/WSET_L3_Specification_Official_2026.pdf` |
| WSET L3 Official SAT (2016) | `knowledge/official-wset/sat/WSET_L3_SAT_Official_2016.pdf` |
| WSET L3 Study Guide (2026) | `knowledge/official-wset/study-guide/WSET_L3_Study_Guide_Official_2026.pdf` |

The extraction was performed by `tools/extract_wset_master_dictionary.py` and
consolidated by `tools/consolidate_wset_master_dictionary.py`.

### Contents

| File | Description |
|------|-------------|
| `master_terms.csv` | Raw extracted terms with category, source, and confidence level |
| `master_terms.jsonl` | Same as above in JSONL format for pipeline consumption |
| `extraction_quality_flags.csv` | Per-term quality flags (duplicates, OCR issues, ambiguous categories) |
| `extraction_report.md` | Extraction run report — category counts, quality flag summary, method |
| `consolidated/canonical_terms_master.csv` | Deduplicated canonical terms with alias mappings |
| `consolidated/canonical_terms_master.jsonl` | Same in JSONL format |
| `consolidated/consolidation_quality_flags.csv` | Flags from the consolidation pass |
| `consolidated/consolidation_report.md` | Consolidation run report |

### Category Coverage (from extraction_report.md)

- `appellation`: 175 terms
- `grape_variety`: 202 terms
- `wine_law`: 87 terms
- `region`: 72 terms
- `sat_term`: 44 terms
- `vinification`: 44 terms
- `viticulture`: 38 terms
- `climate`: 18 terms

---

## 2. Provisional Trust Tier: 1

The dictionary is classified as **provisional Tier 1** because:

- It was extracted exclusively from official WSET-issued PDFs (Tier 1 sources).
- The extraction method uses only seeded vocabulary found in those PDFs.
- Terms carry the official WSET capitalisation and spelling from the source material.
- SAT terms were extracted exclusively from the official SAT documentation.

However, this Tier 1 designation is **provisional** pending the calibration gate
review described in §4. Until that review is complete, the dictionary must be
treated conservatively.

---

## 3. Current Governance State

| Dimension | Status |
|-----------|--------|
| Trust tier | Provisional Tier 1 (pending calibration gate) |
| Examiner Agent access | **FORBIDDEN** until calibration gate passed |
| Tutor Agent access | Permitted for ASR correction and term detection only (current use in `cleaner.py`) |
| Retrieval corpus | Not yet ingested as retrievable content |
| Calibration gate | **NOT YET PASSED** — no `calibration_manifest.schema.json` instance exists |
| IP clearance | Not formally recorded — must be confirmed before any system deployment |
| Human review | Not yet performed |

---

## 4. Calibration Gate Requirements (Before Examiner Agent Use)

If this dictionary is ever used to support Examiner Agent operations (e.g. term
validation in scoring), it must first pass the calibration gate defined in
`knowledge/calibration/calibration_manifest.schema.json`:

1. A WSET-qualified reviewer (minimum WSET Level 3 Award in Wines) must verify:
   - `source_authenticity_verified: true` — the source PDFs are genuine WSET-issued documents.
   - `currency_confirmed: true` — the sources are from the current WSET Level 3 specification.
   - `no_pedagogical_contamination: true` — the dictionary contains no enrichment or pedagogical content.
   - `sat_version_alignment: true` — SAT terms match the current official WSET SAT version.
   - `legal_ip_compliance: true` — IP/legal clearance has been obtained.
2. A calibration manifest entry must be created with `ingestion_status: "approved"`.
3. The manifest entry must be signed off with the reviewer's credentials.

---

## 5. Current Permitted Uses

The dictionary is currently used by `tools/youtube_transcription/cleaner.py` for:
- **ASR correction** — mapping known mis-transcriptions (e.g. `Rhone` → `Rhône`, `wct` → `WSET`) to canonical WSET terms.
- **Term detection** — identifying which WSET terms appear in a transcript, used to populate `dictionary_terms_matched` and `dictionary_categories_detected` in chunk metadata.

These uses do not constitute retrieval or scoring. The dictionary is used as a
lookup table against official vocabulary — it is not injected into any agent
response or used for mark scheme interpretation.

---

## 6. Forbidden Uses (Until Calibration Gate is Passed)

- Must not be ingested into the Examiner Agent retrieval corpus.
- Must not be used to validate or supplement WSET mark scheme terms.
- Must not be presented to learners as authoritative WSET vocabulary without
  the framing: *"Terms are drawn from official WSET materials and are for
  reference only."*
- Must not be used for scoring authority of any kind.

---

## 7. Relationship to the Retrieval Priority Matrix

This artifact does not currently appear in `knowledge/enrichment/retrieval_priority_matrix.json`
because it is not yet a retrievable content source. It is a **pipeline utility** (term lookup),
not a knowledge source.

If in future the dictionary terms are ingested as concept nodes or tasting vocabulary
into the knowledge graph, they would be classified as:
- Source type: `wset_textbook` (for term definitions) or `wset_sat_official` (for SAT terms)
- Trust tier: 1 or 2 respectively
- And would require a calibration manifest entry.

---

## 8. Action Required Before Next Phase

Before the system moves into active retrieval implementation:

1. Confirm IP clearance for the three source PDFs with the organisation's legal adviser.
2. Commission a WSET-qualified reviewer to perform the calibration gate checks.
3. Create a `calibration_manifest.schema.json` instance in `knowledge/calibration/` with
   at least one approved source entry covering the WSET L3 textbook.
4. Decide whether dictionary terms should be promoted to knowledge-graph concept nodes
   (which would require pedagogical role annotation per `knowledge/enrichment/pedagogical_roles.schema.json`).

---

*Governed by: `docs/AGENT_BOUNDARIES.md` · `docs/EXAMINER_CALIBRATION_RULES.md` · `knowledge/enrichment/trust-tier-matrix.json`*
