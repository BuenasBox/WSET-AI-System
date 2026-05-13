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

This pipeline is for pedagogical source ingestion only. YouTube transcripts must not override official WSET grading authority.
