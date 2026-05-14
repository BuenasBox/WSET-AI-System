import json
import tempfile
import unittest
from pathlib import Path

from tools.youtube_transcription.cleaner import _apply_asr_corrections, _make_chunks
from tools.youtube_transcription.dictionary import (
    load_wset_dictionary,
    low_confidence_terms as dictionary_low_confidence_terms,
)


class WsetDictionaryPipelineTests(unittest.TestCase):
    def write_dictionary(self, path: Path) -> None:
        records = [
            {
                "canonical_term": "Languedoc-Roussillon",
                "category": "region",
                "aliases": ["longodop rusilion"],
                "confidence": "high",
                "quality_flags": [],
            },
            {
                "canonical_term": "Low Confidence Term",
                "category": "region",
                "aliases": ["lowconf alias"],
                "confidence": "low",
                "quality_flags": [],
            },
            {
                "canonical_term": "Needs Review",
                "category": "region",
                "aliases": ["review alias"],
                "confidence": "high",
                "quality_flags": ["needs_human_review"],
            },
        ]
        with path.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record) + "\n")

    def test_dictionary_loads_and_ignores_needs_human_review(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            dictionary_path = Path(temp_dir) / "canonical_terms_master.jsonl"
            self.write_dictionary(dictionary_path)

            dictionary = load_wset_dictionary(dictionary_path)

            self.assertEqual(len(dictionary.terms), 2)
            self.assertEqual(dictionary.terms[0].canonical_term, "Languedoc-Roussillon")
            self.assertNotIn(
                ("review alias", "Needs Review"),
                dictionary.high_confidence_alias_corrections,
            )

    def test_alias_correction_only_uses_high_confidence_aliases(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            dictionary_path = Path(temp_dir) / "canonical_terms_master.jsonl"
            self.write_dictionary(dictionary_path)
            dictionary = load_wset_dictionary(dictionary_path)

            lines, corrections, low_confidence_terms = _apply_asr_corrections(
                ["The longodop rusilion area is not the same as lowconf alias."],
                "The longodop rusilion area is not the same as lowconf alias.",
                dictionary,
            )
            matches = dictionary.find_matches("\n".join(lines))

            self.assertIn("Languedoc-Roussillon", lines[0])
            self.assertIn("lowconf alias", lines[0])
            self.assertTrue(
                any(
                    correction["original"] == "longodop rusilion"
                    and correction["corrected"] == "Languedoc-Roussillon"
                    for correction in corrections
                )
            )
            self.assertFalse(any(correction["original"] == "lowconf alias" for correction in corrections))
            self.assertIn("Low Confidence Term", {match.canonical_term for match in matches})
            self.assertEqual(dictionary_low_confidence_terms(matches), ["Low Confidence Term"])
            self.assertEqual(low_confidence_terms, [])

    def test_chunk_enrichment_keeps_examiner_unsafe_and_adds_dictionary_terms(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            dictionary_path = Path(temp_dir) / "canonical_terms_master.jsonl"
            self.write_dictionary(dictionary_path)
            dictionary = load_wset_dictionary(dictionary_path)

            chunks = _make_chunks(
                clean_body="Languedoc-Roussillon has Mediterranean climate.",
                video_id="fixture",
                video_title="Fixture",
                academic_level="WSET_L3",
                pedagogical_role="theory_explanation",
                document_detected={},
                document_quality_flags=["theory_content"],
                dictionary=dictionary,
            )

            self.assertEqual(chunks[0]["canonical_terms_detected"], ["Languedoc-Roussillon"])
            self.assertEqual(chunks[0]["dictionary_categories_detected"], ["region"])
            self.assertFalse(chunks[0]["safe_for_examiner"])
            self.assertTrue(chunks[0]["official_term_matches"])


if __name__ == "__main__":
    unittest.main()
