"""YouTube caption retrieval placeholders.

Future implementation will use youtube-transcript-api to fetch official or
auto-generated captions, preferring English captions when available.
"""


def fetch_captions(video_id: str) -> None:
    """Fetch captions for a video.

    TODO: Retrieve timestamped captions without summarizing or rewriting them.
    """
    raise NotImplementedError("Caption retrieval is not implemented yet.")
