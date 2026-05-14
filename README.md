# WSET AI System

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
- Audio download, transcript retrieval, Whisper transcription, transcript cleaning, embeddings, and agent integration are intentionally not implemented yet.

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

This pipeline is for pedagogical source ingestion only. YouTube transcripts must not override official WSET grading authority.
