import csv
import tempfile
import unittest
from pathlib import Path

from tools.youtube_transcription.main import (
    _is_throttling_network_status,
    _select_target_videos_for_fetch,
)
from tools.youtube_transcription.targets import (
    build_high_value_targets,
    generate_high_value_targets,
)


class YoutubeTargetsTests(unittest.TestCase):
    def test_build_targets_prioritizes_exam_and_skips_completed_private_rows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "wine-with-jimmy"
            (root / "raw").mkdir(parents=True)
            videos = [
                {
                    "video_id": "exam1",
                    "video_title": "How to pass your WSET Level 3 Theory Exam!",
                    "video_url": "https://www.youtube.com/watch?v=exam1",
                    "playlist_titles": "Understanding WSET Level 3 Wine Theory",
                },
                {
                    "video_id": "climate1",
                    "video_title": "Understanding Chile for WSET Level 3 Wines Part 1 - Climate",
                    "video_url": "https://www.youtube.com/watch?v=climate1",
                    "playlist_titles": "Understanding WSET Level 3 Wine Theory",
                },
                {
                    "video_id": "diploma1",
                    "video_title": "WSET Diploma D3 Exam Technique with Mark Pygott MW",
                    "video_url": "https://www.youtube.com/watch?v=diploma1",
                    "playlist_titles": "WSET Diploma - Unit 3",
                },
                {
                    "video_id": "private1",
                    "video_title": "[Private video]",
                    "video_url": "https://www.youtube.com/watch?v=private1",
                    "playlist_titles": "WSET Level 3 Mock Exam Questions",
                },
            ]
            status = {
                "climate1": {"transcript_status": "completed"},
                "private1": {"error_type": "private_video"},
            }

            targets = build_high_value_targets(videos, status, root)

            self.assertEqual(targets[0]["video_id"], "exam1")
            self.assertEqual(targets[0]["priority"], "S")
            self.assertEqual(targets[0]["recommended_for_targeted_fetch"], "true")
            self.assertEqual(targets[0]["first_pass_l3_fetch_priority"], "true")
            completed = next(row for row in targets if row["video_id"] == "climate1")
            diploma = next(row for row in targets if row["video_id"] == "diploma1")
            private = next(row for row in targets if row["video_id"] == "private1")
            self.assertEqual(completed["already_has_transcript"], "true")
            self.assertEqual(completed["recommended_for_targeted_fetch"], "false")
            self.assertEqual(completed["exclusion_reason"], "already_has_transcript")
            self.assertEqual(diploma["academic_level_guess"], "WSET_DIPLOMA")
            self.assertEqual(diploma["recommended_for_targeted_fetch"], "false")
            self.assertEqual(diploma["first_pass_l3_fetch_priority"], "false")
            self.assertEqual(diploma["exclusion_reason"], "diploma_level_content")
            self.assertEqual(private["recommended_for_targeted_fetch"], "false")
            self.assertEqual(private["exclusion_reason"], "private_or_disabled")

    def test_generate_targets_writes_csv_and_jsonl(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "wine-with-jimmy"
            (root / "index").mkdir(parents=True)
            with (root / "index" / "videos_discovered.csv").open(
                "w", encoding="utf-8", newline=""
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "video_id",
                        "video_title",
                        "video_url",
                        "playlist_titles",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "video_id": "sat1",
                        "video_title": "How to prepare for the WSET Level 3 Tasting Exam",
                        "video_url": "https://www.youtube.com/watch?v=sat1",
                        "playlist_titles": "WSET Level 3 Mock Exam Questions",
                    }
                )

            csv_path, jsonl_path, targets = generate_high_value_targets(root)

            self.assertTrue(csv_path.exists())
            self.assertTrue(jsonl_path.exists())
            self.assertEqual(len(targets), 1)
            self.assertIn("tasting", targets[0]["target_reason"].lower())

    def test_select_target_videos_orders_s_a_b_and_skips_current_completed(self):
        rows = [
            {
                "video_id": "b1",
                "video_title": "Region Explained",
                "priority": "B",
                "recommended_for_targeted_fetch": "true",
                "already_has_transcript": "false",
            },
            {
                "video_id": "a1",
                "video_title": "Climate and Viticulture",
                "priority": "A",
                "recommended_for_targeted_fetch": "true",
                "already_has_transcript": "false",
            },
            {
                "video_id": "s1",
                "video_title": "Mock Exam",
                "priority": "S",
                "recommended_for_targeted_fetch": "true",
                "already_has_transcript": "false",
            },
        ]
        videos = _select_target_videos_for_fetch(
            rows,
            {"s1": {"transcript_status": "completed"}},
            limit=2,
        )

        self.assertEqual([video["video_id"] for video in videos], ["a1", "b1"])

    def test_throttling_status_detection(self):
        self.assertTrue(
            _is_throttling_network_status(
                {
                    "error_type": "network_error",
                    "error_message": "IpBlocked: too many requests",
                }
            )
        )
        self.assertFalse(
            _is_throttling_network_status(
                {"error_type": "network_error", "error_message": "temporary timeout"}
            )
        )


if __name__ == "__main__":
    unittest.main()
