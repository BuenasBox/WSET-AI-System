# Wine With Jimmy — Pipeline Governance

**Authority:** `docs/EXAMINER_CALIBRATION_RULES.md` · `knowledge/enrichment/trust-tier-matrix.json`
**Trust Tier:** 4 (Pedagogical Enrichment — not WSET-sanctioned)
**Version:** 1.0
**Date:** 2026-05-14

---

## 1. Corpus Identity

Wine With Jimmy transcripts are informal pedagogical enrichment content produced by
a third-party educator. They are **not** WSET-issued materials. They may only enter
the system corpus under the rules defined in this document.

---

## 2. Absolute Governance Rules (Non-Negotiable)

| Rule | Requirement |
|------|-------------|
| **Examiner Agent** | Wine With Jimmy content is **unconditionally FORBIDDEN** from the Examiner Agent corpus. No exception case exists. |
| **safe_for_examiner** | Always `false` for every record. Hardcoded in `tools/youtube_transcription/metadata.py`. |
| **Framing** | Every Tutor Agent response drawing on this content must include the framing statement: *"This comes from an informal pedagogical source and is for enrichment only — it is not WSET official guidance."* |
| **Exam strategy** | Wine With Jimmy content must never be used for exam strategy guidance, distinction training, or any content claiming to represent WSET marking criteria. |
| **Mark scheme language** | Never paraphrase or reproduce content that resembles WSET mark scheme language from this source. |

---

## 3. Curriculum-Level Classification

Every video metadata record carries a `curriculum_level` field. Valid values and
their governance implications:

| Value | Meaning | Tutor Agent Eligibility |
|-------|---------|------------------------|
| `l3_eligible` | Content confirmed appropriate for WSET Level 3 | Eligible after human review and WSET accuracy check |
| `diploma_only` | WSET Diploma (Level 4) content only | Requires explicit L3-downgrade annotation per trust-tier-matrix.json §diploma_content before any use |
| `mixed` | Video contains both L3 and Diploma content | Requires chunk-level review; Diploma chunks must be L3-downgraded or excluded |
| `unclassified` | Not yet reviewed | **Must not enter Tutor Agent corpus.** Default for all new records. |

**Classification is a human task.** No automated classification pipeline may
promote a record from `unclassified` to `l3_eligible` without explicit human
sign-off. The cleaner's `academic_level` heuristic (`WSET_L3`, `WSET_DIPLOMA`,
`MIXED`, `UNKNOWN`) provides a signal but is not a governance decision.

---

## 4. Ingestion Pipeline Stages

```
videos_discovered.csv / .jsonl   ← discovery-only (index/, not for retrieval)
        ↓
*.metadata.json                  ← per-video metadata (metadata/, machine-local)
        ↓
*.raw.json / *.raw.txt           ← raw captions (raw/, never ingested directly)
        ↓
*.clean.md                       ← cleaned transcript (clean/)
        ↓
*.chunks.jsonl                   ← chunk-ready segments (chunk-ready/)
        ↓
*.enrichment.json                ← enrichment metadata (enrichment-ready/)
        ↓
[HUMAN REVIEW GATE]              ← curriculum_level confirmed, WSET accuracy checked
        ↓
[INGESTION TO TUTOR CORPUS]      ← l3_eligible only, with framing annotation
```

All directories except the final ingest step are local-only pipeline artifacts
and are excluded from version control via `.gitignore`.

---

## 5. .gitignore Coverage

The following directories are intentionally excluded from git tracking.
They are recreated by `tools/youtube_transcription/config.py → ensure_directories()`:

| Directory | Reason |
|-----------|--------|
| `raw/` | Raw captions — large, machine-local |
| `clean/` | Derived output — machine-local |
| `chunk-ready/` | Derived output — machine-local |
| `enrichment-ready/` | Derived output — machine-local |
| `metadata/` | Machine-specific paths embedded in JSON; machine-local state |
| `index/` | Derived discovery CSV/JSONL; machine-local |
| `reports/` | Pipeline reports — machine-local |
| `embeddings/` | Vector store outputs — never committed |
| `audio/` | Audio files — large, machine-local |

---

## 6. Path Portability

All file paths stored in metadata records must be **project-relative POSIX strings**.
Absolute paths (`C:\Users\...` or `/home/...`) are forbidden in committed files.

The `_to_project_relative()` helper in `tools/youtube_transcription/main.py` handles
this conversion at the point where paths enter the status dictionary.

If you discover absolute paths in existing metadata files, they must be corrected
before those records can be used in any pipeline step that reads `raw_json_path`
or `raw_txt_path`.

---

## 7. Review Requirements

Before any Wine With Jimmy content enters the Tutor Agent retrieval corpus:

1. Human reviewer with minimum WSET Level 3 Award must confirm WSET accuracy of the content.
2. `curriculum_level` must be explicitly set to `l3_eligible` (or `diploma_only` with L3-downgrade annotation).
3. The `enrichment_flag: true` annotation must be set in the pedagogical role record.
4. The mandatory framing statement must be configured for the content chunk.
5. The content must carry a `trust_tier: 4` annotation in any retrieval system.

---

*Governed by: `docs/EXAMINER_CALIBRATION_RULES.md` §8 and `knowledge/enrichment/trust-tier-matrix.json` §wine_with_jimmy*
