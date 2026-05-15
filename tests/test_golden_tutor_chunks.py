import csv
import json
import tempfile
import unittest
from pathlib import Path

from tools.youtube_transcription.golden_tutor_chunks import (
    generate_golden_tutor_chunk_reports,
    score_chunk,
)


class GoldenTutorChunkTests(unittest.TestCase):
    def test_score_chunk_detects_high_value_exam_strategy(self):
        row = score_chunk(
            {
                "chunk_id": "fixture-0001",
                "source_filename": "fixture.srt",
                "video_title_guess": "Fixture",
                "text": (
                    "In the exam, students lose marks because they do not justify "
                    "the quality assessment or link balance intensity complexity length."
                ),
                "academic_level": "WSET_L3",
                "pedagogical_role": "exam_strategy",
                "quality_flags": [],
            }
        )

        self.assertTrue(row["golden_tutor_chunk_candidate"])
        self.assertEqual(row["retrieval_priority"], "high")
        self.assertIn(row["reasoning_type"], {"common_mistake", "tasting_calibration"})
        self.assertIn("students lose marks", row["matched_signals"])
        self.assertIn("quality assessment", row["matched_signals"])

    def test_report_filters_to_manual_tutor_examiner_false_chunks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "wine-with-jimmy"
            chunk_dir = root / "chunk-ready"
            chunk_dir.mkdir(parents=True)
            chunk_path = chunk_dir / "fixture.chunks.jsonl"
            rows = [
                {
                    "chunk_id": "manual-0001",
                    "source_filename": "manual.srt",
                    "video_title_guess": "Manual Fixture",
                    "source_type": "manual_curated_srt",
                    "agent_corpus": "tutor",
                    "safe_for_examiner": False,
                    "safe_for_tutor": True,
                    "academic_level": "WSET_L3",
                    "pedagogical_role": "exam_strategy",
                    "text": "In the exam, WSET wants you to explain why because marks require a link.",
                    "quality_flags": [],
                },
                {
                    "chunk_id": "youtube-0001",
                    "source_type": "youtube_transcript",
                    "agent_corpus": "tutor",
                    "safe_for_examiner": False,
                    "text": "In the exam this should not be scanned.",
                },
                {
                    "chunk_id": "unsafe-0001",
                    "source_type": "manual_curated_srt",
                    "agent_corpus": "tutor",
                    "safe_for_examiner": True,
                    "text": "In the exam this should not be scanned.",
                },
            ]
            chunk_path.write_text(
                "".join(json.dumps(row) + "\n" for row in rows),
                encoding="utf-8",
            )

            report = generate_golden_tutor_chunk_reports(root)

            self.assertEqual(report.scanned_chunks, 1)
            self.assertEqual(len(report.candidate_rows), 1)
            self.assertTrue(report.output_csv.exists())
            self.assertTrue(report.output_jsonl.exists())
            self.assertTrue(report.summary_path.exists())
            summary = report.summary_path.read_text(encoding="utf-8")
            self.assertIn("safe_for_examiner remains false: true", summary)

            with report.output_csv.open("r", encoding="utf-8", newline="") as file:
                csv_rows = list(csv.DictReader(file))
            self.assertEqual(csv_rows[0]["chunk_id"], "manual-0001")
            self.assertNotIn("safe_for_examiner", csv_rows[0])


if __name__ == "__main__":
    unittest.main()
