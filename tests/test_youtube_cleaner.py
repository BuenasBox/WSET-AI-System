import json
import tempfile
import unittest
from pathlib import Path

from tools.youtube_transcription.cleaner import clean_one_video, clean_transcript


class YoutubeCleanerTests(unittest.TestCase):
    def test_clean_transcript_removes_artifacts_and_duplicate_fragments(self):
        raw_text = "\n".join(
            [
                "[00:00:01] [Music]",
                "[00:00:02] WSET Level 3 and Barossa Valley",
                "[00:00:03] WSET Level 3 and Barossa Valley",
                "[00:00:04] preserve Côte-Rôtie terminology",
            ]
        )

        cleaned = clean_transcript(raw_text)

        self.assertNotIn("[Music]", cleaned)
        self.assertEqual(cleaned.count("WSET Level 3 and Barossa Valley"), 1)
        self.assertIn("Côte-Rôtie", cleaned)

    def test_clean_one_video_writes_only_clean_chunk_and_report_outputs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "wine-with-jimmy"
            raw_dir = root / "raw"
            metadata_dir = root / "metadata"
            raw_dir.mkdir(parents=True)
            metadata_dir.mkdir(parents=True)

            video_id = "abc123"
            raw_txt_path = raw_dir / "abc123__Fixture.raw.txt"
            raw_json_path = raw_dir / "abc123__Fixture.raw.json"
            metadata_path = metadata_dir / "abc123.metadata.json"
            raw_txt_path.write_text(
                "[00:00:01] [Music]\n[00:00:02] hello WSET wct Barosa\n",
                encoding="utf-8",
            )
            raw_json_path.write_text(
                json.dumps(
                    {
                        "video_id": video_id,
                        "language": "en",
                        "segments": [
                            {"start": 1.0, "duration": 1.0, "text": "[Music]"},
                            {
                                "start": 2.0,
                                "duration": 2.0,
                                "text": "hello WSET wct Barosa",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            metadata_path.write_text(
                json.dumps(
                    {
                        "video_id": video_id,
                        "raw_txt_path": str(raw_txt_path),
                        "raw_json_path": str(raw_json_path),
                    }
                ),
                encoding="utf-8",
            )

            report = clean_one_video(video_id, root)

            self.assertTrue((root / "clean" / "abc123__Fixture.clean.txt").exists())
            self.assertTrue(
                (root / "chunk-ready" / "abc123__Fixture.chunk-ready.txt").exists()
            )
            self.assertTrue(
                (root / "reports" / "abc123__Fixture.cleaning-report.json").exists()
            )
            self.assertIn("possible_asr_error", report["quality_flags"])
            self.assertIn("possible_appellation_error", report["quality_flags"])
            self.assertTrue(
                raw_txt_path.read_text(encoding="utf-8").startswith("[00:00:01] [Music]")
            )


if __name__ == "__main__":
    unittest.main()
