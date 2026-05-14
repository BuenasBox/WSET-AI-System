import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.youtube_transcription.manual_srt import (
    classify_academic_level,
    infer_video_id,
    import_manual_srt_batch,
    parse_srt_file,
    parse_srt_text,
)


class ManualSrtImportTests(unittest.TestCase):
    def test_parse_valid_srt_preserves_timing(self):
        segments, malformed = parse_srt_text(
            "1\n"
            "00:00:01,000 --> 00:00:03,500\n"
            "WSET Level 3 acidity and tannin\n\n"
            "2\n"
            "00:00:04,000 --> 00:00:05,000\n"
            "Quality assessment\n"
        )

        self.assertFalse(malformed)
        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[0].index, 1)
        self.assertEqual(segments[0].start_time, "00:00:01.000")
        self.assertEqual(segments[0].end_time, "00:00:03.500")
        self.assertEqual(segments[0].text, "WSET Level 3 acidity and tannin")

    def test_tolerates_imperfect_srt(self):
        segments, malformed = parse_srt_text(
            "00:00:01,000 --> 00:00:03,000\n"
            "No numeric index here\n\n"
            "This orphan text should not crash\n"
        )

        self.assertTrue(malformed)
        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[0].text, "No numeric index here")
        self.assertEqual(segments[1].text, "This orphan text should not crash")

    def test_duplicate_caption_line_removal(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "fixture.srt"
            path.write_text(
                "1\n00:00:01,000 --> 00:00:02,000\nSame caption\n\n"
                "2\n00:00:02,000 --> 00:00:03,000\nSame caption\n\n"
                "3\n00:00:03,000 --> 00:00:04,000\nNext caption\n",
                encoding="utf-8-sig",
            )

            parsed = parse_srt_file(path)

            self.assertEqual(len(parsed["segments"]), 2)
            self.assertEqual(parsed["duplicate_caption_lines_removed"], 1)

    def test_title_classification_levels(self):
        self.assertEqual(classify_academic_level("WSET Level 3 Climate"), "WSET_L3")
        self.assertEqual(classify_academic_level("Diploma D3 with MW"), "WSET_DIPLOMA")
        self.assertEqual(
            classify_academic_level("WSET Level 3 and WSET Level 4 Diploma Terroir"),
            "MIXED",
        )

    def test_video_id_inference_does_not_use_ordinary_words(self):
        self.assertEqual(
            infer_video_id("Explaining Wine Terminology for WSET Level 3.srt"),
            "",
        )
        self.assertEqual(
            infer_video_id("Fixture Title [abc123DEF45].srt"),
            "abc123DEF45",
        )

    def test_import_outputs_are_tutor_only_and_manual_source(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "wine-with-jimmy"
            srt_dir = root / "manual-import" / "srt"
            srt_dir.mkdir(parents=True)
            source = srt_dir / "WSET Level 3 SAT Tasting Quality [English (auto-generated)].srt"
            source.write_text(
                "\n\n".join(
                    [
                        f"{index}\n00:00:{index:02d},000 --> 00:00:{index + 1:02d},000\n"
                        f"WSET Level 3 tasting acidity quality Cabernet Sauvignon sentence {index}."
                        for index in range(1, 24)
                    ]
                ),
                encoding="utf-8",
            )

            results = import_manual_srt_batch(root, limit=1)

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["import_status"], "completed")
            self.assertFalse(results[0]["safe_for_examiner"])
            chunk_path = next((root / "chunk-ready").glob("*.chunks.jsonl"))
            chunks = [
                json.loads(line)
                for line in chunk_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertGreaterEqual(len(chunks), 1)
            self.assertTrue(all(chunk["source_type"] == "manual_curated_srt" for chunk in chunks))
            self.assertTrue(all(chunk["safe_for_examiner"] is False for chunk in chunks))
            self.assertTrue(all(chunk["agent_corpus"] == "tutor" for chunk in chunks))
            self.assertIn("source_filename", chunks[0])
            self.assertIn("start_time", chunks[0])
            self.assertIn("end_time", chunks[0])

    def test_manual_import_does_not_call_youtube_caption_fetch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "wine-with-jimmy"
            srt_dir = root / "manual-import" / "srt"
            srt_dir.mkdir(parents=True)
            (srt_dir / "WSET Level 3 Climate.srt").write_text(
                "1\n00:00:01,000 --> 00:00:02,000\nClimate and sunlight.\n",
                encoding="utf-8",
            )

            with patch("tools.youtube_transcription.captions.fetch_captions") as fetch:
                import_manual_srt_batch(root, limit=1)

            fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
