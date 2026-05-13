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
- Network calls, audio download, Whisper transcription, transcript cleaning, indexing, and metadata writes are intentionally not implemented yet.

This pipeline is for pedagogical source ingestion only. YouTube transcripts must not override official WSET grading authority.
