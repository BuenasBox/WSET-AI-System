# Transcript Cleaning and Semantic Preparation Architecture

## 1. Purpose

This document defines the next pipeline stage for the Wine with Jimmy transcript corpus: cleaning raw YouTube captions and preparing them for later semantic processing.

This stage produces clean, structured, pedagogically useful transcript artifacts for the Tutor Agent only. It does not create embeddings, build a vector database, connect to agents, summarize videos, grade students, or process official WSET calibration material.

Official WSET materials remain the only grading and calibration authority. Wine with Jimmy transcripts are supplemental teaching material and must not be available to the Examiner Agent for scoring.

## 2. Input Files

Primary inputs:

```text
knowledge/wine-with-jimmy/raw/
  <video_id>__<safe_title>.raw.txt
  <video_id>__<safe_title>.raw.json

knowledge/wine-with-jimmy/metadata/
  <video_id>.metadata.json

knowledge/wine-with-jimmy/index/
  videos_index.csv
```

The cleaning pipeline may read transcript status indexes later, but it must not modify `knowledge/wine-with-jimmy/index/transcript_status.csv` during this design phase.

## 3. Output Files

Recommended derived outputs:

```text
knowledge/wine-with-jimmy/clean/
  <video_id>__<safe_title>.clean.json
  <video_id>__<safe_title>.clean.md

knowledge/wine-with-jimmy/chunk-ready/
  <video_id>__<safe_title>.chunk_ready.json

knowledge/wine-with-jimmy/review/
  manual_review_queue.jsonl

knowledge/wine-with-jimmy/logs/
  cleaning_run_<YYYYMMDD_HHMMSS>.json
```

All outputs are derived artifacts. Raw transcripts are immutable source artifacts and must never be edited by the cleaning stage.

## 4. Cleaning Philosophy

Cleaning must be conservative, reversible in spirit, and reproducible.

The pipeline should improve readability and downstream chunk quality without changing meaning. It should remove obvious caption artifacts, normalize safe formatting issues, and flag uncertain terminology instead of silently rewriting ambiguous text.

Every cleaned transcript must retain a pointer to:

- `video_id`
- raw transcript path
- metadata path
- cleaning version
- date processed

No generated summaries are allowed at this stage.

## 5. What To Remove

The cleaner may remove or mark:

- Music markers such as `[Music]`, `(music)`, and `♪`
- Applause or non-speech markers when not pedagogically meaningful
- Repeated caption fragments caused by overlap
- Timestamp-only lines
- Empty lines created by caption export
- Obvious subscribe, like, notification, sponsor, or channel housekeeping boilerplate
- Intro/outro noise when clearly unrelated to wine education
- Mechanical filler repetition such as repeated "um", "uh", and duplicated false starts
- Caption formatting residue such as HTML entities and malformed whitespace

Removal should be rule-based and auditable. Anything uncertain should be retained and flagged.

## 6. What To Preserve

The cleaner must preserve:

- Wine terms, grape names, region names, appellations, producer names, and classifications
- WSET terminology and SAT vocabulary
- Cause-and-effect explanations
- Comparisons between grapes, regions, climates, winemaking choices, and styles
- Speaker nuance that affects teaching meaning
- Tasting structure, examples, and exam-relevant explanations
- Timestamps or segment boundaries when available
- Transcript provenance and source metadata

The pipeline should prefer light normalization over polished prose.

## 7. Wine Terminology Protection Rules

Wine terms are high-value tokens and require special handling.

Protection rules:

- Do not auto-correct a possible wine term unless the correction is deterministic from an approved glossary or local alias map.
- Preserve diacritics when present, but do not require adding them if absent.
- Treat grape varieties, regions, appellations, quality levels, and producer names as protected spans.
- Keep both the original and corrected form when a correction is applied.
- Flag low-confidence corrections with `low_confidence_term`.
- Prefer `possible_asr_error` over aggressive rewriting.
- Maintain a configurable glossary for future implementation.

Examples of protected wine terms include `Sangiovese`, `Tempranillo`, `Nebbiolo`, `Chablis`, `Barolo`, `Rioja`, `Bordeaux`, `Chianti Classico`, `Brunello di Montalcino`, `Alsace`, `Mosel`, `Marlborough`, and `appellation`.

## 8. WSET Terminology Protection Rules

WSET vocabulary must be preserved because it anchors later tutoring behavior.

Protected WSET terms include:

- Systematic Approach to Tasting and `SAT`
- appearance, nose, palate, conclusions
- sweetness, acidity, tannin, alcohol, body, intensity, finish
- primary, secondary, tertiary aromas
- climate, weather, latitude, altitude, aspect, continentality
- viticulture, vinification, maturation, ageing
- PDO, PGI, appellation, geographical indication
- learning outcome, command verbs, identify, describe, explain, compare

The cleaning stage must not reinterpret WSET criteria, infer official learning outcomes, or introduce grading language beyond future metadata placeholders.

## 9. Common ASR and Caption Issues Observed

Expected caption problems include:

- Appellations damaged or split into unrelated English words
- Grape varieties damaged by phonetic transcription
- `appellations` becoming `appalachians`
- `Sangiovese` becoming bad phonetic variants
- Music markers embedded in otherwise useful text
- Intro/outro channel noise around educational sections
- Filler phrases and repeated spoken resets
- Missing punctuation causing long ambiguous sentences
- Duplicate caption lines from overlapping caption segments
- Homophones around wine, region, and chemistry terms

These issues should inform flags and review queues before they inform automated correction.

## 10. Conservative Correction Strategy

The initial implementation should support three correction levels:

```text
level_0_format_only
  Normalize whitespace, line endings, simple punctuation spacing, and caption markers.

level_1_glossary_exact
  Apply approved deterministic replacements from a versioned glossary or alias table.

level_2_review_suggestions
  Generate suggested corrections but do not apply them automatically.
```

Default mode should be `level_0_format_only` plus review flags. Higher levels should require explicit CLI flags.

Applied corrections must be recorded in a correction log with:

- original text
- corrected text
- rule ID
- confidence
- timestamp or segment ID when available

## 11. No Hallucination Rule

The cleaning pipeline must not add facts, examples, explanations, regions, grape names, WSET outcomes, or summaries that are not present in the source transcript or its existing metadata.

If a term is unclear, the cleaner should flag it. It must not invent the intended term.

## 12. Clean Transcript Schema

Recommended `clean.json` shape:

```json
{
  "schema_version": "clean_transcript.v1",
  "video_id": "string",
  "title": "string",
  "source": {
    "raw_transcript_path": "string",
    "metadata_path": "string",
    "raw_format": "txt|json",
    "caption_source": "youtube_manual|youtube_generated|whisper|unknown"
  },
  "processing": {
    "cleaning_version": "string",
    "date_processed": "ISO-8601 datetime",
    "cleaning_level": "level_0_format_only",
    "rules_applied": ["string"]
  },
  "segments": [
    {
      "segment_id": "string",
      "start_seconds": 0.0,
      "end_seconds": 0.0,
      "raw_text": "string",
      "clean_text": "string",
      "corrections": [],
      "quality_flags": []
    }
  ],
  "document_quality_flags": [],
  "access_scope": "tutor_only"
}
```

The Markdown version should be a human-readable rendering of the same content, not an independent source of truth.

## 13. Chunk-Ready Transcript Schema

Recommended `chunk_ready.json` shape:

```json
{
  "schema_version": "chunk_ready_transcript.v1",
  "video_id": "string",
  "clean_transcript_path": "string",
  "source": {
    "raw_transcript_path": "string",
    "metadata_path": "string",
    "cleaning_version": "string",
    "date_processed": "ISO-8601 datetime"
  },
  "chunk_candidates": [
    {
      "chunk_candidate_id": "string",
      "segment_ids": ["string"],
      "start_seconds": 0.0,
      "end_seconds": 0.0,
      "text": "string",
      "token_estimate": 0,
      "boundary_reason": "topic_shift|time_window|length_limit|caption_boundary",
      "quality_flags": [],
      "semantic_placeholders": {
        "topics_detected": [],
        "grape_varieties": [],
        "regions": [],
        "appellations": [],
        "sat_terms": [],
        "wset_learning_outcomes": [],
        "cause_effect_chains": [],
        "common_misconceptions": [],
        "exam_tips": [],
        "distinction_insights": []
      }
    }
  ],
  "access_scope": "tutor_only"
}
```

Chunk-ready output prepares boundaries and metadata fields only. It must not embed, summarize, or semantically enrich content with generated facts.

## 14. Metadata Update Schema

Cleaning metadata should be stored as a derived metadata companion or later merged into a dedicated derived index, not written back into raw metadata without an explicit migration.

Recommended shape:

```json
{
  "schema_version": "cleaning_metadata.v1",
  "video_id": "string",
  "raw_transcript_path": "string",
  "metadata_path": "string",
  "clean_transcript_path": "string",
  "chunk_ready_path": "string",
  "cleaning_version": "string",
  "date_processed": "ISO-8601 datetime",
  "cleaning_level": "level_0_format_only",
  "segment_count": 0,
  "chunk_candidate_count": 0,
  "quality_flags": [],
  "manual_review_required": false,
  "access_scope": "tutor_only"
}
```

## 15. Future Semantic Tagging Fields

The following fields are reserved for future semantic tagging:

- `topics_detected`
- `grape_varieties`
- `regions`
- `appellations`
- `sat_terms`
- `wset_learning_outcomes`
- `cause_effect_chains`
- `common_misconceptions`
- `exam_tips`
- `distinction_insights`

At this stage, these fields should be empty arrays or omitted behind a feature flag. They should not be populated by LLMs or inferred summaries during cleaning.

## 16. Quality Flags

Required quality flags:

- `possible_asr_error`
- `low_confidence_term`
- `noisy_caption`
- `incomplete_transcript`
- `language_mismatch`

Additional useful flags:

- `possible_intro_outro_noise`
- `duplicate_caption_fragment`
- `music_marker_removed`
- `missing_timestamps`
- `possible_wset_term_damage`
- `manual_review_required`

Flags should exist at segment and document level.

## 17. Manual Review Workflow

The manual review workflow should be lightweight:

1. Cleaning run emits segment-level flags.
2. Flagged segments are appended to `knowledge/wine-with-jimmy/review/manual_review_queue.jsonl`.
3. Reviewer checks the raw transcript and video metadata.
4. Reviewer may approve a deterministic glossary correction.
5. Approved corrections are added to a versioned glossary or alias map.
6. Pipeline is rerun to reproduce derived outputs.

Manual edits should not be made directly to clean transcript outputs. Reviewed corrections should flow through versioned rules so outputs remain reproducible.

## 18. Recommended Folder Structure

```text
knowledge/
  wine-with-jimmy/
    raw/
    clean/
    chunk-ready/
    metadata/
    derived-metadata/
    review/
      manual_review_queue.jsonl
    config/
      cleaning-settings.json
      wine-term-glossary.json
      wset-term-glossary.json
      correction-aliases.json
    logs/
      cleaning_run_<YYYYMMDD_HHMMSS>.json
    index/
      videos_index.csv
      cleaning_index.csv

tools/
  youtube_transcription/
    cleaner.py
    cleaning_pipeline_plan.md
    future modules:
      terminology.py
      chunk_prep.py
      review_queue.py
      schemas.py
```

## 19. CLI Commands To Implement Later

Proposed future commands:

```powershell
python -m tools.youtube_transcription.main clean-transcripts --dry-run --limit 5
python -m tools.youtube_transcription.main clean-transcripts --video-id <video_id>
python -m tools.youtube_transcription.main clean-transcripts --cleaning-level level_0_format_only
python -m tools.youtube_transcription.main clean-transcripts --retry-failed-only
python -m tools.youtube_transcription.main prepare-chunks --video-id <video_id>
python -m tools.youtube_transcription.main export-review-queue --limit 50
python -m tools.youtube_transcription.main validate-cleaned --video-id <video_id>
```

These commands must not fetch captions, call YouTube, run Whisper, create embeddings, or connect to agents.

## 20. Risks

Primary risks:

- Over-correction of valid wine terminology
- Loss of pedagogical nuance through aggressive filler removal
- Silent corruption of appellations, grape varieties, or WSET terms
- Accidental use of tutor-only transcripts by the Examiner Agent
- Non-reproducible manual edits to derived artifacts
- Confusing generated semantic fields with source-derived transcript text
- Processing active or partially written raw transcript files

Mitigations:

- Default to format-only cleaning
- Keep raw transcripts immutable
- Store correction logs and rule IDs
- Require tutor-only access scope in every derived artifact
- Use manual review for uncertain terms
- Version cleaning settings, glossaries, and aliases
- Avoid processing files currently being written by ingestion jobs

## 21. Next Implementation Milestone

The next milestone should implement a safe dry-run cleaner for one transcript at a time.

Scope:

- Add schema models or typed dictionaries for clean and chunk-ready outputs
- Read one raw transcript and its metadata by `video_id`
- Normalize whitespace and caption markers only
- Preserve raw text alongside clean text
- Emit quality flags for obvious music markers, noisy captions, and possible terminology damage
- Write derived output only under `knowledge/wine-with-jimmy/clean/` and `knowledge/wine-with-jimmy/chunk-ready/`
- Create a dry-run mode that prints planned output paths without writing files
- Add tests using small fixture transcripts, not the full raw corpus

Out of scope:

- Embeddings
- Vector databases
- LLM calls
- Summaries
- Agent integration
- Bulk transcript processing
- YouTube or Whisper requests
