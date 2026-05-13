"""Audio download placeholders.

Future implementation will use yt-dlp to download audio only when captions are
unavailable. This scaffold intentionally performs no downloads.
"""


def download_audio(video_id: str) -> None:
    """Download audio for Whisper fallback.

    TODO: Download audio with yt-dlp only after caption retrieval fails.
    """
    raise NotImplementedError("Audio download is not implemented yet.")
