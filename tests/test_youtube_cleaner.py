import json
import tempfile
import unittest
from pathlib import Path

from tools.youtube_transcription.cleaner import clean_one_video, clean_transcript


class YoutubeCleanerTests(unittest.TestCase):
    def test_cleaner_removes_music_and_preserves_core_wine_terms(self):
        raw_text = "\n".join(
            [
                "[00:00:01] [Music]",
                "[00:00:02] WSET Level 3 and Barossa Valley",
                "[00:00:03] WSET Level 3 and Barossa Valley",
                "[00:00:04] preserve Côte-Rôtie and Cabernet Sauvignon terminology",
            ]
        )

        cleaned = clean_transcript(raw_text)

        self.assertNotIn("[Music]", cleaned)
        self.assertEqual(cleaned.count("WSET Level 3 and Barossa Valley"), 1)
        self.assertIn("Côte-Rôtie", cleaned)
        self.assertIn("Cabernet Sauvignon", cleaned)

    def test_clean_one_video_writes_valid_safe_outputs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "wine-with-jimmy"
            raw_dir = root / "raw"
            metadata_dir = root / "metadata"
            index_dir = root / "index"
            raw_dir.mkdir(parents=True)
            metadata_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)

            video_id = "abc123"
            raw_txt_path = raw_dir / "abc123__Fixture.raw.txt"
            raw_json_path = raw_dir / "abc123__Fixture.raw.json"
            metadata_path = metadata_dir / "abc123.metadata.json"
            raw_txt_path.write_text(
                "[00:00:01] [Music]\n"
                "[00:00:02] Diploma Level 4 Cabernet Sauvignon acidity tannin BICL\n"
                "[00:00:04] Burgundy fermentation theory and exam question\n",
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
                                "text": "Diploma Level 4 Cabernet Sauvignon acidity tannin BICL",
                            },
                            {
                                "start": 4.0,
                                "duration": 2.0,
                                "text": "Burgundy fermentation theory and exam question",
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
                        "video_title": "Fixture WSET Level 4 Diploma",
                        "raw_txt_path": str(raw_txt_path),
                        "raw_json_path": str(raw_json_path),
                    }
                ),
                encoding="utf-8",
            )

            report = clean_one_video(video_id, root)

            clean_path = root / "clean" / "abc123__Fixture.clean.md"
            chunk_path = root / "chunk-ready" / "abc123__Fixture.chunks.jsonl"
            enrichment_path = root / "enrichment-ready" / "abc123.enrichment.json"
            report_path = root / "reports" / "abc123.cleaning_report.json"
            self.assertTrue(clean_path.exists())
            self.assertTrue(chunk_path.exists())
            self.assertTrue(enrichment_path.exists())
            self.assertTrue(report_path.exists())

            chunks = [
                json.loads(line)
                for line in chunk_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertGreaterEqual(len(chunks), 1)
            self.assertTrue(all(chunk["safe_for_examiner"] is False for chunk in chunks))
            self.assertTrue(all(chunk["safe_for_tutor"] is True for chunk in chunks))
            self.assertIn("Cabernet Sauvignon", chunks[0]["grape_varieties"])
            self.assertEqual(report["academic_level"], "WSET_DIPLOMA")
            self.assertFalse(report["safe_for_examiner"])
            self.assertIn("diploma_level_content", report["quality_flags"])
            self.assertTrue(
                raw_txt_path.read_text(encoding="utf-8").startswith("[00:00:01] [Music]")
            )

    def test_intro_asr_corrections_sat_and_chunk_size_controls(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "wine-with-jimmy"
            raw_dir = root / "raw"
            metadata_dir = root / "metadata"
            index_dir = root / "index"
            raw_dir.mkdir(parents=True)
            metadata_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)

            video_id = "southfr"
            raw_txt_path = raw_dir / "southfr__Southern_France.raw.txt"
            raw_json_path = raw_dir / "southfr__Southern_France.raw.json"
            metadata_path = metadata_dir / "southfr.metadata.json"
            educational_lines = [
                "Southern France wsct level three sits beside the roan and the Mediterranean climate gives warm summers.",
                "The longodop rusilion area includes russian where drought can reduce yields.",
                "Victor culture must manage disease pressure, mildew and rot in the vineyard.",
                "IGP day paid dock wines may include Syrah and Pinot Noir in commercial blends.",
            ] * 35
            transcript_lines = [
                "[00:00:01] welcome to the channel and thank you for clicking on the video",
                "[00:00:02] subscribe and contact me through social media or the portal website",
                *[f"[00:00:{index + 3:02d}] {line}" for index, line in enumerate(educational_lines)],
            ]
            raw_txt_path.write_text("\n".join(transcript_lines), encoding="utf-8")
            raw_json_path.write_text(
                json.dumps(
                    {
                        "video_id": video_id,
                        "language": "en",
                        "segments": [
                            {"start": float(index), "duration": 1.0, "text": line.split("] ", 1)[1]}
                            for index, line in enumerate(transcript_lines)
                        ],
                    }
                ),
                encoding="utf-8",
            )
            metadata_path.write_text(
                json.dumps(
                    {
                        "video_id": video_id,
                        "video_title": "Understanding Southern France for WSET Level 3",
                        "raw_txt_path": str(raw_txt_path),
                        "raw_json_path": str(raw_json_path),
                    }
                ),
                encoding="utf-8",
            )

            report = clean_one_video(video_id, root)
            chunk_path = root / "chunk-ready" / "southfr__Southern_France.chunks.jsonl"
            chunks = [
                json.loads(line)
                for line in chunk_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            correction_pairs = {
                (item["original"], item["corrected"])
                for item in report["asr_corrections_applied"]
            }

            self.assertTrue(chunks[0]["exclude_from_retrieval"])
            self.assertEqual(chunks[0]["segment_type"], "intro")
            self.assertIn(("wsct", "WSET"), correction_pairs)
            self.assertIn(("roan", "Rhône"), correction_pairs)
            self.assertIn(("longodop rusilion", "Languedoc-Roussillon"), correction_pairs)
            self.assertIn(("russian", "Roussillon"), correction_pairs)
            self.assertIn(("victor culture", "viticulture"), correction_pairs)
            self.assertIn(("igp day paid dock", "IGP Pays d'Oc"), correction_pairs)
            self.assertTrue(any("Southern France" in chunk["regions"] for chunk in chunks))
            self.assertTrue(any("Languedoc-Roussillon" in chunk["regions"] for chunk in chunks))
            self.assertTrue(any("IGP Pays d'Oc" in chunk["appellations"] for chunk in chunks))
            self.assertFalse(any("sat" in chunk["topics_detected"] for chunk in chunks))
            self.assertGreater(len(chunks), 3)
            self.assertLessEqual(max(len(chunk["text"].split()) for chunk in chunks), 350)
            self.assertTrue(all(chunk["safe_for_examiner"] is False for chunk in chunks))


if __name__ == "__main__":
    unittest.main()
