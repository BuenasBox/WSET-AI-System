"""Tests for tools/question_bank/convert_xlsx_to_json.py"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.question_bank.convert_xlsx_to_json import (
    OUTPUT_FILENAME,
    STRUCTURED_DIR,
    XLSX_PATH,
    _KNOWN_ORIGINAL_IDS,
    _build_expected_topics,
    _derive_keywords,
    _has_manual_metadata,
    _is_safe_to_overwrite,
    _map_tipo,
    convert,
)
from tools.self_eval.question_runner import load_questions


class TestTipoMapping(unittest.TestCase):
    def test_opcion_multiple_mixed_case(self):
        self.assertEqual(_map_tipo("Opcion_Multiple"), "theory")

    def test_opcion_multiple_upper(self):
        self.assertEqual(_map_tipo("OPCION_MULTIPLE"), "theory")

    def test_verdadero_falso_mixed(self):
        self.assertEqual(_map_tipo("Verdadero_Falso"), "theory")

    def test_verdadero_falso_upper(self):
        self.assertEqual(_map_tipo("VERDADERO_FALSO"), "theory")

    def test_emparejamiento(self):
        self.assertEqual(_map_tipo("Emparejamiento"), "theory")

    def test_abierta_lower(self):
        self.assertEqual(_map_tipo("Abierta"), "short_answer")

    def test_unrecognized_returns_none(self):
        self.assertIsNone(_map_tipo("Desconocido"))

    def test_empty_returns_none(self):
        self.assertIsNone(_map_tipo(""))


class TestKeywordDerivation(unittest.TestCase):
    def test_uses_respuesta_texto_first(self):
        row = {"Respuesta_Texto": "Clima fresco continental", "Respuesta_Letra": "C"}
        kws, warn = _derive_keywords(row)
        self.assertEqual(kws, ["Clima fresco continental"])
        self.assertFalse(warn)

    def test_derives_from_option_when_no_texto(self):
        row = {
            "Respuesta_Texto": "",
            "Respuesta_Letra": "B",
            "Opcion_B": "Chianti Classico",
        }
        kws, warn = _derive_keywords(row)
        self.assertEqual(kws, ["Chianti Classico"])
        self.assertFalse(warn)

    def test_correct_option_letter_lookup_d(self):
        row = {
            "Respuesta_Texto": "",
            "Respuesta_Letra": "D",
            "Opcion_D": "Opción D content",
        }
        kws, warn = _derive_keywords(row)
        self.assertEqual(kws, ["Opción D content"])
        self.assertFalse(warn)

    def test_respuesta_texto_takes_priority_over_option(self):
        row = {
            "Respuesta_Texto": "Texto directo",
            "Respuesta_Letra": "A",
            "Opcion_A": "Opción A",
        }
        kws, warn = _derive_keywords(row)
        self.assertEqual(kws, ["Texto directo"])
        self.assertFalse(warn)

    def test_warning_when_neither_source(self):
        row = {"Respuesta_Texto": None, "Respuesta_Letra": ""}
        kws, warn = _derive_keywords(row)
        self.assertEqual(kws, [])
        self.assertTrue(warn)


class TestExpectedTopics(unittest.TestCase):
    def test_ra_and_bloque_combined(self):
        row = {"RA": "RA3", "Bloque": "Bloque 9"}
        self.assertEqual(_build_expected_topics(row), ["RA3 / Bloque 9"])

    def test_ra_only(self):
        row = {"RA": "RA1", "Bloque": None}
        self.assertEqual(_build_expected_topics(row), ["RA1"])

    def test_bloque_only(self):
        row = {"RA": None, "Bloque": "Bloque 5"}
        self.assertEqual(_build_expected_topics(row), ["Bloque 5"])

    def test_neither_returns_empty(self):
        row = {"RA": None, "Bloque": None}
        self.assertEqual(_build_expected_topics(row), [])


class TestManualMetadataDetection(unittest.TestCase):
    def test_detects_non_empty_topics(self):
        entry = {
            "expected_topics": ["flor"],
            "expected_causal_links": [],
            "expected_keywords": [],
        }
        self.assertTrue(_has_manual_metadata(entry))

    def test_detects_non_empty_keywords(self):
        entry = {
            "expected_topics": [],
            "expected_causal_links": [],
            "expected_keywords": ["solera"],
        }
        self.assertTrue(_has_manual_metadata(entry))

    def test_false_when_all_empty(self):
        entry = {
            "expected_topics": [],
            "expected_causal_links": [],
            "expected_keywords": [],
        }
        self.assertFalse(_has_manual_metadata(entry))

    def test_false_when_fields_missing(self):
        self.assertFalse(_has_manual_metadata({}))


class TestSafeToOverwrite(unittest.TestCase):
    def _make_entries(self, ids: range | list) -> list[dict]:
        return [{"question_id": str(i)} for i in ids]

    def test_true_for_exactly_known_25(self):
        entries = self._make_entries(range(1, 26))
        self.assertTrue(_is_safe_to_overwrite(entries))

    def test_false_when_extra_id_present(self):
        entries = self._make_entries(list(range(1, 26)) + [99])
        self.assertFalse(_is_safe_to_overwrite(entries))

    def test_false_when_entry_missing(self):
        entries = self._make_entries(range(1, 25))  # only 24
        self.assertFalse(_is_safe_to_overwrite(entries))

    def test_false_when_not_list(self):
        self.assertFalse(_is_safe_to_overwrite({}))  # type: ignore[arg-type]

    def test_false_when_wrong_id_set(self):
        entries = self._make_entries(range(26, 51))  # 25 entries, wrong IDs
        self.assertFalse(_is_safe_to_overwrite(entries))


class TestIntegrationConvert(unittest.TestCase):
    """Integration tests against the real Excel, writing to a temp dir."""

    @classmethod
    def setUpClass(cls):
        cls._tmpdir = tempfile.TemporaryDirectory()
        cls.tmp_root = Path(cls._tmpdir.name)
        cls.tmp_structured = cls.tmp_root / "structured"
        cls.tmp_structured.mkdir(parents=True, exist_ok=True)

        # Seed with exactly the 25 known original entries (filtered from the real file
        # regardless of how many entries it currently has after previous converter runs).
        # This guarantees _is_safe_to_overwrite returns True and the converter writes
        # to the primary path — keeping the temp dir to a single JSON file.
        real_content = json.loads(
            (STRUCTURED_DIR / OUTPUT_FILENAME).read_text(encoding="utf-8")
        )
        cls.seed_entries = [
            q for q in real_content
            if str(q.get("question_id", "")) in _KNOWN_ORIGINAL_IDS
        ]
        (cls.tmp_structured / OUTPUT_FILENAME).write_text(
            json.dumps(cls.seed_entries, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        cls.stats = convert(xlsx_path=XLSX_PATH, structured_dir=cls.tmp_structured)
        cls.output = json.loads(
            Path(cls.stats["output_path"]).read_text(encoding="utf-8")
        )
        cls.output_by_id = {str(q["question_id"]): q for q in cls.output}

    @classmethod
    def tearDownClass(cls):
        cls._tmpdir.cleanup()

    # --- cuadre ---

    def test_cuadre_total_exact(self):
        s = self.stats
        total = s["converted"] + s["preserved"] + s["skipped"]
        self.assertEqual(
            total,
            s["excel_rows"],
            f"Row mismatch: {s['converted']} converted + {s['preserved']} preserved "
            f"+ {s['skipped']} skipped = {total} != {s['excel_rows']} Excel rows",
        )

    def test_each_skipped_has_reason(self):
        self.assertEqual(len(self.stats["skipped_details"]), self.stats["skipped"])
        for detail in self.stats["skipped_details"]:
            self.assertTrue(
                detail.get("reason"), f"Skipped entry missing reason: {detail}"
            )

    # --- load_questions integration ---

    def test_load_questions_reads_output_without_error(self):
        questions = load_questions(limit=1000, question_bank_root=self.tmp_root)
        expected_valid = self.stats["converted"] + self.stats["preserved"]
        self.assertEqual(
            len(questions),
            min(expected_valid, 1000),
            f"load_questions() returned {len(questions)}, expected {expected_valid}",
        )

    # --- encoding ---

    def test_utf8_round_trip_with_accented_chars(self):
        accented = {"¿", "á", "é", "í", "ó", "ú", "ñ", "ü", "Á", "É", "Í", "Ó", "Ú"}
        all_text = " ".join(q.get("question_text", "") for q in self.output)
        found = accented & set(all_text)
        self.assertTrue(
            found,
            "No Spanish accented/special characters found in output — "
            "possible ensure_ascii or openpyxl encoding issue.",
        )

    # --- preservation of manual metadata ---

    def test_enriched_entries_keep_curated_arrays(self):
        # Use the seed (the 25 entries the converter actually received) to identify
        # which entries had manual metadata at conversion time.
        enriched_seed = {
            str(e["question_id"]): e
            for e in self.seed_entries
            if _has_manual_metadata(e)
        }
        self.assertGreater(len(enriched_seed), 0, "No enriched entries found in seed")
        for qid, orig in enriched_seed.items():
            self.assertIn(qid, self.output_by_id, f"Preserved ID {qid} missing from output")
            out = self.output_by_id[qid]
            self.assertEqual(
                out["expected_topics"],
                orig["expected_topics"],
                f"expected_topics changed for preserved ID {qid}",
            )
            self.assertEqual(
                out["expected_causal_links"],
                orig["expected_causal_links"],
                f"expected_causal_links changed for preserved ID {qid}",
            )
            self.assertEqual(
                out["expected_keywords"],
                orig["expected_keywords"],
                f"expected_keywords changed for preserved ID {qid}",
            )

    # --- output integrity ---

    def test_all_ids_unique_in_output(self):
        ids = [str(q["question_id"]) for q in self.output]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate question_ids found in output")

    def test_no_safe_for_examiner_true(self):
        for q in self.output:
            self.assertFalse(
                q.get("safe_for_examiner"),
                f"Question {q.get('question_id')} has safe_for_examiner=True",
            )

    # --- Abierta question protection (IDs 798-817) ---

    _ABIERTA_IDS: frozenset[str] = frozenset(str(i) for i in range(798, 818))

    def test_abierta_questions_all_present_in_output(self):
        missing = self._ABIERTA_IDS - set(self.output_by_id.keys())
        self.assertEqual(missing, set(), f"Missing Abierta IDs from output: {missing}")

    def test_abierta_questions_have_short_answer_type(self):
        for qid in self._ABIERTA_IDS:
            q = self.output_by_id.get(qid)
            self.assertIsNotNone(q, f"Abierta ID {qid} not in output")
            self.assertEqual(
                q["question_type"],
                "short_answer",
                f"Wrong question_type for Abierta ID {qid}",
            )

    def test_abierta_questions_produce_no_keyword_warnings(self):
        warned_ids = {str(d["id"]) for d in self.stats["warning_details"]}
        overlap = self._ABIERTA_IDS & warned_ids
        self.assertEqual(
            overlap,
            set(),
            f"Abierta questions must not produce keyword warnings; got: {overlap}",
        )

    def test_extra_mcq_fields_present(self):
        has_options = any("options" in q for q in self.output)
        self.assertTrue(has_options, "No question has 'options' extra field in output")

    # --- safe overwrite ---

    def test_safe_overwrite_true_when_seeded_with_known_25(self):
        self.assertTrue(
            self.stats["safe_overwrite"],
            "safe_overwrite should be True when seeded with the known 25 entries",
        )

    def test_output_written_to_primary_path(self):
        if self.stats["safe_overwrite"]:
            expected = str(self.tmp_structured / OUTPUT_FILENAME)
            self.assertEqual(self.stats["output_path"], expected)


if __name__ == "__main__":
    unittest.main()
