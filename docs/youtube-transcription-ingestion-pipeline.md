# YouTube Transcription Ingestion Pipeline

## Scope

This document defines the architecture and implementation plan for a YouTube playlist transcription ingestion pipeline for the WSET Level 3 AI Tutor Agent project.

This phase must only prepare transcript data for future RAG and AI training. It must not build UI, connect to agents, create embeddings, create a vector database, summarize videos, evaluate educational quality, or alter official WSET grading authority.

The transcripts are pedagogical support only. Official WSET materials remain the only grading authority.

## Default Playlists

The pipeline should use these playlist URLs as default input:

```text
https://youtube.com/playlist?list=PLHvqIB13xXh16S0NK1AtPda47MTQeLO23&si=QBbCj4ykYauLHVBc
https://youtube.com/playlist?list=PLHvqIB13xXh2LYc0V3PME6RSYirmhZ0j3&si=ijlTv4liJ4NvchKb
https://youtube.com/playlist?list=PLHvqIB13xXh2p_cuTnddrE9TJyBRDECXr&si=NDgTSYsBiFL7WNyK
https://youtube.com/playlist?list=PLHvqIB13xXh0gTZUlK524pUqXApwTKXyn&si=Ke6rDLHZ_u3UZPtp
https://youtube.com/playlist?list=PLHvqIB13xXh2cUC1I-M-gckve9b44UpVS&si=-YZS9EPWhYSspcXd
```

Additional playlists should be added later through `knowledge/wine-with-jimmy/config/playlists.json`.

## Recommended Folder Structure

```text
knowledge/
  wine-with-jimmy/
    raw/
      video_id__safe_video_title.raw.txt
      video_id__safe_video_title.raw.json
    clean/
      video_id__safe_video_title.clean.md
    audio/
      video_id.m4a
    metadata/
      video_id.metadata.json
    logs/
      ingestion.log
      failures.jsonl
      run_YYYYMMDD_HHMMSS.json
    config/
      playlists.json
      pipeline-settings.json
    index/
      videos_index.csv
```

The pipeline should create these folders automatically if they do not exist.

## Recommended Python Architecture

```text
backend/
  ingestion/
    youtube_pipeline/
      __init__.py
      cli.py
      config.py
      models.py
      playlists.py
      captions.py
      audio.py
      whisper.py
      cleaning.py
      topic_detection.py
      metadata.py
      index.py
      logging_setup.py
      retry.py
      state.py
```

### Module Responsibilities

`cli.py`

- Entry point for batch runs.
- Supports default config path.
- Supports dry run, retry failed, force reprocess, and playlist subset options.

`config.py`

- Loads playlist config.
- Validates playlist objects.
- Creates missing folders.
- Loads pipeline settings such as preferred caption language, retry count, and Whisper model.

`models.py`

- Defines dataclasses or Pydantic models for playlist metadata, video metadata, transcript segments, and processing status.

`playlists.py`

- Uses `yt-dlp` to extract playlist and video metadata.
- Captures video ID, title, URL, duration, upload date, channel name, channel URL, playlist ID, and playlist name.

`captions.py`

- Uses `youtube-transcript-api` first.
- Prefers English captions.
- Stores timestamped raw transcript when available.
- Records caption language and whether captions were manual or generated if available.

`audio.py`

- Uses `yt-dlp` to download audio only when captions are unavailable.
- Saves audio under `knowledge/wine-with-jimmy/audio`.
- Avoids redownloading existing audio unless forced.

`whisper.py`

- Uses Whisper or faster-whisper for local transcription fallback.
- Produces timestamped segments.
- Marks transcript source as `whisper`.

`cleaning.py`

- Normalizes spacing and obvious transcript noise.
- Removes repeated filler fragments only when safe.
- Preserves wine terminology, SAT vocabulary, causal explanations, examples, and exam tips.
- Does not summarize, paraphrase heavily, or rewrite style.

`topic_detection.py`

- Applies lightweight keyword and phrase tagging.
- Does not generate educational summaries.
- Tags topics, SAT topics, and likely WSET learning outcome buckets.

`metadata.py`

- Writes one metadata JSON file per video.
- Merges playlist references for duplicate videos.
- Updates status and error fields.

`index.py`

- Maintains `videos_index.csv`.
- Updates rows idempotently by `video_id`.
- Includes clean/raw/metadata paths and topic tags.

`logging_setup.py`

- Configures structured JSONL or structured text logging.
- Writes run-level and video-level logs.

`retry.py`

- Handles retries, backoff, and temporary failure classification.

`state.py`

- Determines whether a video should be skipped, retried, or processed.
- Prevents overwriting completed transcripts unless explicitly forced.

## Config File

Create:

```text
knowledge/wine-with-jimmy/config/playlists.json
```

Recommended structure:

```json
[
  {
    "playlist_name": "",
    "playlist_url": "https://youtube.com/playlist?list=PLHvqIB13xXh16S0NK1AtPda47MTQeLO23&si=QBbCj4ykYauLHVBc",
    "playlist_id": "PLHvqIB13xXh16S0NK1AtPda47MTQeLO23",
    "source_channel": "",
    "status": "pending",
    "last_processed": ""
  },
  {
    "playlist_name": "",
    "playlist_url": "https://youtube.com/playlist?list=PLHvqIB13xXh2LYc0V3PME6RSYirmhZ0j3&si=ijlTv4liJ4NvchKb",
    "playlist_id": "PLHvqIB13xXh2LYc0V3PME6RSYirmhZ0j3",
    "source_channel": "",
    "status": "pending",
    "last_processed": ""
  },
  {
    "playlist_name": "",
    "playlist_url": "https://youtube.com/playlist?list=PLHvqIB13xXh2p_cuTnddrE9TJyBRDECXr&si=NDgTSYsBiFL7WNyK",
    "playlist_id": "PLHvqIB13xXh2p_cuTnddrE9TJyBRDECXr",
    "source_channel": "",
    "status": "pending",
    "last_processed": ""
  },
  {
    "playlist_name": "",
    "playlist_url": "https://youtube.com/playlist?list=PLHvqIB13xXh0gTZUlK524pUqXApwTKXyn&si=Ke6rDLHZ_u3UZPtp",
    "playlist_id": "PLHvqIB13xXh0gTZUlK524pUqXApwTKXyn",
    "source_channel": "",
    "status": "pending",
    "last_processed": ""
  },
  {
    "playlist_name": "",
    "playlist_url": "https://youtube.com/playlist?list=PLHvqIB13xXh2cUC1I-M-gckve9b44UpVS&si=-YZS9EPWhYSspcXd",
    "playlist_id": "PLHvqIB13xXh2cUC1I-M-gckve9b44UpVS",
    "source_channel": "",
    "status": "pending",
    "last_processed": ""
  }
]
```

Playlist names and channel names can be filled automatically after metadata extraction.

## Processing Flow

1. Load playlist config.
2. Create required folders.
3. Extract playlist metadata with `yt-dlp`.
4. Build a deduplicated video work queue keyed by `video_id`.
5. Merge playlist membership for duplicate videos.
6. Check existing metadata and transcript files.
7. Skip videos marked `completed` unless `--force` is used.
8. Attempt YouTube captions through `youtube-transcript-api`.
9. Prefer English captions.
10. If captions exist, save raw TXT and raw JSON.
11. If captions do not exist, download audio with `yt-dlp`.
12. Transcribe audio with Whisper or faster-whisper.
13. Save raw transcript with timestamps if available.
14. Clean transcript conservatively.
15. Run lightweight topic detection.
16. Write per-video metadata JSON.
17. Update master CSV index.
18. Write structured processing logs.
19. Update playlist config status and `last_processed`.

## Error Handling Strategy

Use explicit status values:

```text
pending
completed
failed
skipped
unavailable
private
deleted
caption_unavailable
audio_failed
whisper_failed
metadata_failed
```

Recommended handling:

- Temporary network failure: retry with exponential backoff.
- YouTube rate limit: pause and resume later.
- Private/deleted/unavailable video: mark as unavailable and continue.
- Caption unavailable: fallback to audio and Whisper.
- Audio download failure: log failure and continue batch.
- Whisper failure: preserve metadata, mark failed, retry later.
- Interrupted execution: resume from metadata and index state.
- File write failure: fail the video, log exact path and exception.

Do not stop the full playlist run because one video fails.

## Duplicate Handling Strategy

Duplicate videos across playlists should be stored once by `video_id`.

Per-video metadata should preserve all playlist memberships:

```json
"playlist_ids": ["playlist_1", "playlist_2"],
"playlist_names": ["Playlist A", "Playlist B"]
```

File outputs should be single-instance:

```text
raw/video_id__safe_video_title.raw.txt
clean/video_id__safe_video_title.clean.md
metadata/video_id.metadata.json
```

The master index should contain one row per unique `video_id`.

If duplicate videos have conflicting titles from playlist extraction, keep the most recent extracted title in `video_title` and optionally store alternate titles in metadata later.

## Metadata Schema

One JSON file per video:

```json
{
  "video_id": "",
  "video_title": "",
  "video_url": "",
  "playlist_ids": [],
  "playlist_names": [],
  "channel_name": "",
  "channel_url": "",
  "duration": "",
  "upload_date": "",
  "transcript_source": "youtube_caption",
  "caption_language": "en",
  "language_detected": "",
  "topics_detected": [],
  "wset_learning_outcomes": [],
  "sat_topics": [],
  "contains_exam_tips": false,
  "contains_tasting_content": false,
  "contains_theory_content": false,
  "contains_cause_effect_reasoning": false,
  "processing_status": "pending",
  "error_message": "",
  "raw_transcript_path": "",
  "clean_transcript_path": "",
  "metadata_path": "",
  "audio_path": "",
  "last_processed": ""
}
```

Allowed `transcript_source` values:

```text
youtube_caption
whisper
unavailable
```

Allowed `processing_status` values:

```text
pending
completed
failed
skipped
unavailable
```

## Master Index

Create:

```text
knowledge/wine-with-jimmy/index/videos_index.csv
```

Columns:

```text
video_id
video_title
video_url
channel_name
playlist_names
duration
upload_date
transcript_source
processing_status
clean_transcript_path
raw_transcript_path
metadata_path
topics_detected
wset_learning_outcomes
sat_topics
last_processed
```

Use stable CSV serialization:

- UTF-8 encoding
- quoted fields where needed
- list fields serialized as semicolon-separated values or JSON strings
- idempotent row replacement by `video_id`

## Raw Transcript Format

TXT file:

```text
[00:00:01] transcript text
[00:00:05] transcript text
```

JSON file:

```json
{
  "video_id": "",
  "source": "youtube_caption",
  "language": "en",
  "segments": [
    {
      "start": 0.0,
      "duration": 3.5,
      "text": ""
    }
  ]
}
```

Naming:

```text
video_id__safe_video_title.raw.txt
video_id__safe_video_title.raw.json
```

## Clean Transcript Format

Markdown file:

```markdown
# Video Title

- Video ID:
- Source:
- Caption language:
- Playlist names:

## Transcript

[00:00:01] Cleaned transcript text.
```

Cleaning should:

- Normalize spacing.
- Remove obvious caption artifacts.
- Remove repeated filler only when safe.
- Preserve wine terminology.
- Preserve SAT vocabulary.
- Preserve causal explanations.
- Preserve examples and exam tips.
- Preserve speaker style where useful for pedagogy.

Cleaning must not:

- Summarize.
- Rewrite heavily.
- Remove technical terms.
- Convert transcript into teaching notes.
- Evaluate content quality.

Naming:

```text
video_id__safe_video_title.clean.md
```

## Topic Detection

Use lightweight keyword matching and phrase matching.

Initial topic list:

```text
Bordeaux
Burgundy
Champagne
Rioja
Port
Sherry
Riesling
Sauvignon Blanc
Chardonnay
Pinot Noir
Cabernet Sauvignon
Merlot
Syrah
Grenache
Climate
Viticulture
Canopy management
Harvest
Fermentation
Oak
Maturation
Bottle ageing
Tannins
Acidity
Alcohol
Body
SAT
Appearance
Nose
Palate
Conclusions
BICL
Blind tasting
Sparkling wine
Fortified wine
Exam strategy
Distinction tips
Common mistakes
Cause-effect reasoning
```

Boolean flags should be derived from tags:

- `contains_exam_tips`
- `contains_tasting_content`
- `contains_theory_content`
- `contains_cause_effect_reasoning`

Do not generate educational summaries in this phase.

## Logging Strategy

Use structured logging with one log event per meaningful step.

Recommended fields:

```json
{
  "timestamp": "",
  "run_id": "",
  "level": "INFO",
  "event": "caption_downloaded",
  "playlist_id": "",
  "video_id": "",
  "status": "completed",
  "duration_ms": 0,
  "error": ""
}
```

Log files:

```text
logs/ingestion.log
logs/failures.jsonl
logs/run_YYYYMMDD_HHMMSS.json
```

The run summary should include:

- playlists processed
- total videos discovered
- unique videos discovered
- completed
- skipped
- failed
- unavailable
- caption transcripts
- Whisper transcripts
- start time
- end time

## Suggested Dependencies

Core:

```text
yt-dlp
youtube-transcript-api
pydantic
python-slugify
tenacity
tqdm
```

Transcription fallback:

```text
faster-whisper
```

Optional:

```text
langdetect
orjson
rich
```

System dependency:

```text
ffmpeg
```

Recommended package file:

```text
requirements-ingestion.txt
```

## Scalability Considerations

- Use one metadata file per video to support resume and partial completion.
- Avoid storing state only in memory.
- Use idempotent writes through temp files and atomic rename where possible.
- Process videos sequentially by default to reduce rate-limit risk.
- Add bounded concurrency later for metadata extraction, not necessarily caption/audio retrieval.
- Use retry queues for failed videos.
- Keep audio files optional and removable after successful Whisper transcription if storage becomes an issue.
- Support playlist batches with 200+ videos.
- Store transcript paths rather than transcript text in the master CSV.
- Keep future chunking separate from transcript ingestion.

## Recommended Execution Order

1. Create folder structure and config file.
2. Create schemas or Pydantic models.
3. Implement playlist metadata extraction.
4. Implement deduplicated work queue.
5. Implement skip/resume logic.
6. Implement YouTube caption retrieval.
7. Implement raw transcript writes.
8. Implement conservative transcript cleaning.
9. Implement metadata JSON writes.
10. Implement master CSV index updates.
11. Implement audio fallback.
12. Implement Whisper fallback.
13. Implement topic detection.
14. Implement structured logging.
15. Run dry-run metadata extraction.
16. Run one playlist end-to-end.
17. Run all playlists.
18. Retry failures.
19. Review index and logs.

## Future Integration Notes for RAG and Tutor Agent

Future RAG ingestion should treat these transcripts as pedagogical source material only.

Future retrieval metadata should include:

- source type: `youtube_transcript`
- authority tier: pedagogical support
- allowed agent: Tutor Agent
- prohibited use: official grading authority
- video ID
- playlist names
- topic tags
- SAT tags
- transcript source
- timestamp ranges

Future chunking should preserve:

- timestamp references
- video metadata
- topic tags
- SAT tags
- cause-effect passages
- exam-tip passages

Future Tutor Agent use:

- explanation style
- coaching patterns
- deliberate-practice examples
- study advice
- cause-effect training

Future Examiner Agent restriction:

- These transcripts must not be used to alter grading severity.
- These transcripts must not override official SAT structure.
- These transcripts must not override official mark schemes.
