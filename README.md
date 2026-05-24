# WSET AI System

## Contributing — Documentation Convention

**No binary documents in the repository.** PDFs, Word files (`.docx`), Excel (`.xlsx`), and PowerPoint (`.pptx`) are blocked by `.gitignore`. Before committing any reference material or documentation, convert it to Markdown first using [markitdown](https://github.com/microsoft/markitdown):

```bash
markitdown source.pdf > knowledge/official-wset/study-guide/wset_markdown/output.md
markitdown source.docx > docs/output.md
```

The `.md` file is what gets committed. The original binary stays local only.

---

## YouTube Transcription Ingestion Pipeline

Initial scaffold location:

```text
tools/youtube_transcription/
```

Configuration:

```text
knowledge/wine-with-jimmy/config/playlists.json
```

Later, after dependencies are installed and implementation is completed, the intended command will be:

```bash
python -m tools.youtube_transcription.main
```

Current status:

- The package structure exists.
- The playlist config exists.
- Logging setup exists.
- Dry-run playlist/video metadata discovery is available.
- Targeted YouTube caption retrieval is available for small, high-value Tutor Agent batches.
- Audio download, video download, Whisper transcription, embeddings, and Examiner Agent integration are intentionally not part of this pipeline.

### Dry-Run Playlist Metadata Extraction

Install dependencies separately, then run:

```bash
python -m tools.youtube_transcription.main dry-run
```

This command uses `yt-dlp` only to discover playlist and video metadata. It does not download videos, audio, captions, or transcripts.

Outputs to inspect:

```text
knowledge/wine-with-jimmy/index/videos_discovered.csv
knowledge/wine-with-jimmy/index/videos_discovered.jsonl
knowledge/wine-with-jimmy/logs/ingestion.log
```

If discovery output files already exist, the previous files are backed up with a UTC timestamp before new files are written.

### Caption Retrieval

After inspecting discovery outputs, test caption retrieval with a small batch:

```bash
python -m tools.youtube_transcription.main fetch-captions --limit 10
```

This command reads:

```text
knowledge/wine-with-jimmy/index/videos_discovered.jsonl
```

It attempts to retrieve existing YouTube captions, preferring English, and writes:

```text
knowledge/wine-with-jimmy/raw/
knowledge/wine-with-jimmy/metadata/
knowledge/wine-with-jimmy/index/transcript_status.csv
knowledge/wine-with-jimmy/logs/ingestion.log
```

It does not download audio, download video, run Whisper, summarize, create embeddings, connect to agents, or build UI. Existing raw transcript JSON files are skipped unless `--force` is used.

Caption retrieval is intentionally paced conservatively because YouTube may throttle repeated transcript requests. The default behavior sleeps a random 2-5 seconds before each request and retries only temporary network/parsing failures with backoff delays of 10, 30, and 90 seconds.

Recommended test batch:

```bash
python -m tools.youtube_transcription.main fetch-captions --limit 10
```

Recommended steady batch:

```bash
python -m tools.youtube_transcription.main fetch-captions --limit 50
```

For longer overnight runs, use wider pacing:

```bash
python -m tools.youtube_transcription.main fetch-captions --sleep-min 5 --sleep-max 12
```

To retry only failed rows from `transcript_status.csv`:

```bash
python -m tools.youtube_transcription.main fetch-captions --retry-failed-only
```

The status index is checkpointed after each processed video, so interrupted runs can be restarted safely. Processing remains sequential only.

### High-Value Tutor Target List

Generate a prioritized target list from local discovery/status metadata:

```bash
python -m tools.youtube_transcription.main generate-targets
```

This reads:

```text
knowledge/wine-with-jimmy/index/videos_discovered.csv
knowledge/wine-with-jimmy/index/transcript_status.csv
```

It writes:

```text
knowledge/wine-with-jimmy/config/high_value_tutor_targets.csv
knowledge/wine-with-jimmy/config/high_value_tutor_targets.jsonl
```

Targets are classified from video titles only. Priority S covers exam strategy, mock exams, tasting exam guidance, answer technique, pass/distinction tips, mistakes, time management, SAT tasting guidance, and answer structure. Priority A covers high-value cause-effect theory such as acidity, tannin, balance, quality assessment, climate, viticulture, winemaking choices, oak, malolactic conversion, lees ageing, botrytis, sparkling methods, and fortified methods. Priority B covers broader theory, important regions/grapes, and regional comparisons. Priority C is lower-value narrow or cultural/promotional content.

The first pass recommends at most 30 WSET Level 3/L3-safe videos and does not recommend private videos, transcript-disabled videos, videos that already have local transcripts, or Diploma/D3/Level 4/MW content. Diploma targets can remain high-priority for later enrichment, but `first_pass_l3_fetch_priority` keeps them out of the initial Tutor-first fetch batch.

### Targeted Tutor Fetch

Run only the recommended high-value target batch:

```bash
python -m tools.youtube_transcription.main fetch-targets --limit 3 --sleep-min 180 --sleep-max 420
```

This command reads:

```text
knowledge/wine-with-jimmy/config/high_value_tutor_targets.csv
```

It processes only rows where `recommended_for_targeted_fetch = true` and `already_has_transcript = false`, in priority order S -> A -> B. It fetches one transcript at a time, uses long randomized pacing, skips existing completed/skipped transcripts, updates `transcript_status.csv`, and stops immediately with `TARGETED_FETCH_STOPPED_DUE_TO_THROTTLING` after two consecutive network errors that look like `IpBlocked`, too many requests, or throttling.

Never run `fetch-targets` in parallel with `fetch-captions` or any playlist fetch. Keep this as a single sequential process.

This pipeline is for pedagogical source ingestion only. YouTube transcripts must not override official WSET grading authority.
