import csv
import json
import tempfile
import unittest
from pathlib import Path

from tools.consolidate_wset_master_dictionary import run_consolidation


class WsetDictionaryConsolidationTests(unittest.TestCase):
    def write_inputs(self, root: Path, rows: list[dict[str, str]], flags: list[dict[str, str]]) -> None:
        fieldnames = [
            "canonical_term",
            "category",
            "official_source",
            "source_document",
            "ra",
            "aliases",
            "confidence",
            "manually_reviewed",
            "notes",
        ]
        with (root / "master_terms.csv").open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        with (root / "master_terms.jsonl").open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        with (root / "extraction_quality_flags.csv").open(
            "w", newline="", encoding="utf-8-sig"
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "canonical_term",
                    "category",
                    "official_source",
                    "source_document",
                    "duplicate_term",
                    "ambiguous_category",
                    "low_confidence_extraction",
                    "possible_ocr_issue",
                    "details",
                ],
            )
            writer.writeheader()
            writer.writerows(flags)

    def test_consolidates_exact_term_category_without_inventing_aliases(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "consolidated"
            rows = [
                {
                    "canonical_term": "  Alsace Grand Cru ",
                    "category": "appellation",
                    "official_source": "specification",
                    "source_document": "spec.pdf",
                    "ra": "RA2",
                    "aliases": "",
                    "confidence": "high",
                    "manually_reviewed": "false",
                    "notes": "page 12",
                },
                {
                    "canonical_term": "Alsace Grand Cru",
                    "category": "appellation",
                    "official_source": "study-guide",
                    "source_document": "guide.pdf",
                    "ra": "Study Guide p.101",
                    "aliases": "",
                    "confidence": "high",
                    "manually_reviewed": "false",
                    "notes": "page 101",
                },
            ]
            self.write_inputs(root, rows, [])

            consolidated, quality_rows, metrics = run_consolidation(root, output)

            self.assertEqual(metrics["raw_term_count"], 2)
            self.assertEqual(metrics["consolidated_count"], 1)
            self.assertEqual(metrics["duplicates_merged"], 1)
            self.assertEqual(quality_rows, [])
            record = consolidated[0]
            self.assertEqual(record["canonical_term"], "Alsace Grand Cru")
            self.assertEqual(record["source_documents"], ["spec.pdf", "guide.pdf"])
            self.assertEqual(record["official_sources"], ["specification", "study-guide"])
            self.assertEqual(record["aliases"], [])
            self.assertTrue(record["safe_for_tutor"])
            self.assertFalse(record["safe_for_examiner"])

    def test_preserves_same_term_in_multiple_categories_and_flags_ambiguity(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            rows = [
                {
                    "canonical_term": "Bordeaux",
                    "category": "region",
                    "official_source": "specification",
                    "source_document": "spec.pdf",
                    "ra": "RA2",
                    "aliases": "Claret",
                    "confidence": "high",
                    "manually_reviewed": "false",
                    "notes": "",
                },
                {
                    "canonical_term": "Bordeaux",
                    "category": "wine_law",
                    "official_source": "study-guide",
                    "source_document": "guide.pdf",
                    "ra": "Study Guide p.1",
                    "aliases": "",
                    "confidence": "high",
                    "manually_reviewed": "false",
                    "notes": "",
                },
            ]
            self.write_inputs(root, rows, [])

            consolidated, quality_rows, metrics = run_consolidation(root, root / "out")

            self.assertEqual(len(consolidated), 2)
            self.assertIn("Bordeaux", metrics["ambiguous_terms"])
            self.assertTrue(
                all("ambiguous_category" in row["quality_flags"] for row in consolidated)
            )
            self.assertEqual(len(quality_rows), 2)

    def test_low_confidence_and_ocr_flags_flow_to_human_review(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            rows = [
                {
                    "canonical_term": "carbonic maceration",
                    "category": "vinification",
                    "official_source": "study-guide",
                    "source_document": "guide.pdf",
                    "ra": "Study Guide p.10",
                    "aliases": "carbonicm aceration; carbonicm aceration",
                    "confidence": "medium",
                    "manually_reviewed": "false",
                    "notes": "",
                }
            ]
            flags = [
                {
                    "canonical_term": "carbonic maceration",
                    "category": "vinification",
                    "official_source": "study-guide",
                    "source_document": "guide.pdf",
                    "duplicate_term": "false",
                    "ambiguous_category": "false",
                    "low_confidence_extraction": "true",
                    "possible_ocr_issue": "true",
                    "details": "fixture",
                }
            ]
            self.write_inputs(root, rows, flags)

            consolidated, quality_rows, _metrics = run_consolidation(root, root / "out")

            record = consolidated[0]
            self.assertEqual(record["confidence"], "low")
            self.assertEqual(record["aliases"], ["carbonicm aceration"])
            self.assertIn("possible_ocr_issue", record["quality_flags"])
            self.assertIn("duplicate_alias", record["quality_flags"])
            self.assertIn("needs_human_review", record["quality_flags"])
            self.assertEqual(len(quality_rows), 1)


if __name__ == "__main__":
    unittest.main()
