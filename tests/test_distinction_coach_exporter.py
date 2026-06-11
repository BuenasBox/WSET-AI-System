"""Tests for tools.question_generation.distinction_coach_exporter (Phase Y.1)."""

import json
import tempfile
import unittest
from pathlib import Path

from tools.question_generation.distinction_coach_exporter import (
    COACH_GLOBAL,
    COMMAND_VERBS,
    SCHEMA_VERSION,
    build_coach_payload,
    export_coach_payload,
    render_coach_js,
)


class PayloadSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = build_coach_payload()

    def test_schema_version(self):
        self.assertEqual(self.payload["schema_version"], SCHEMA_VERSION)

    def test_required_top_level_keys(self):
        for key in (
            "governance", "sat_sections", "palate_element_detect", "scales",
            "quality_terms", "readiness_terms", "justification_connectors",
            "quality_principle", "common_quality_errors", "simple_wine_note",
            "mentor_hints", "command_verbs",
        ):
            self.assertIn(key, self.payload)

    def test_four_sat_sections_in_official_order(self):
        ids = [s["id"] for s in self.payload["sat_sections"]]
        self.assertEqual(ids, ["aspecto", "nariz", "boca", "conclusiones"])

    def test_sections_have_detection_keywords(self):
        for sec in self.payload["sat_sections"]:
            self.assertTrue(sec["detect"], f"no detect keywords for {sec['id']}")
            self.assertTrue(sec["elements"])

    def test_quality_terms_from_official_scale(self):
        self.assertIn("excelente", self.payload["quality_terms"])
        self.assertEqual(len(self.payload["quality_terms"]), 6)

    def test_readiness_terms_present(self):
        self.assertEqual(len(self.payload["readiness_terms"]), 4)

    def test_all_six_command_verbs(self):
        self.assertEqual(set(self.payload["command_verbs"]), set(COMMAND_VERBS))
        for verb, spec in self.payload["command_verbs"].items():
            self.assertTrue(spec["definition"], verb)
            self.assertTrue(spec["mentor_hint"], verb)

    def test_mentor_hints_cover_sat_areas(self):
        for topic in ("SAT_palate", "SAT_quality", "SAT_readiness", "MCQ_strategy"):
            self.assertIn(topic, self.payload["mentor_hints"])

    def test_scales_flattened_with_palate_acidity(self):
        self.assertIn("palate.acidity", self.payload["scales"])
        self.assertIn("alta", self.payload["scales"]["palate.acidity"])


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.payload = build_coach_payload()

    def test_safe_for_examiner_false(self):
        self.assertIs(self.payload["governance"]["safe_for_examiner"], False)

    def test_examiner_scoring_not_allowed(self):
        self.assertIs(self.payload["governance"]["examiner_scoring_allowed"], False)

    def test_formative_only(self):
        self.assertIs(self.payload["governance"]["formative_only"], True)

    def test_no_llm_no_api(self):
        self.assertIs(self.payload["governance"]["uses_llm"], False)
        self.assertIs(self.payload["governance"]["uses_api"], False)

    def test_no_mark_or_grade_fields(self):
        blob = json.dumps(self.payload, ensure_ascii=False).lower()
        for forbidden in ('"marks_awarded"', '"grade"', '"score":', '"pass_fail"'):
            self.assertNotIn(forbidden, blob)

    def test_no_safe_for_examiner_true_anywhere(self):
        blob = json.dumps(self.payload, ensure_ascii=False)
        self.assertNotIn('"safe_for_examiner": true', blob)


class DeterminismTests(unittest.TestCase):
    def test_payload_is_deterministic(self):
        a = json.dumps(build_coach_payload(), sort_keys=True, ensure_ascii=False)
        b = json.dumps(build_coach_payload(), sort_keys=True, ensure_ascii=False)
        self.assertEqual(a, b)

    def test_rendered_js_is_deterministic(self):
        p = build_coach_payload()
        self.assertEqual(render_coach_js(p), render_coach_js(p))


class RenderAndExportTests(unittest.TestCase):
    def test_js_assigns_expected_global(self):
        js = render_coach_js(build_coach_payload())
        self.assertIn(f"window.{COACH_GLOBAL} =", js)
        self.assertTrue(js.rstrip().endswith(";"))

    def test_js_payload_round_trips_as_json(self):
        js = render_coach_js(build_coach_payload())
        body = js.split(f"window.{COACH_GLOBAL} =", 1)[1].rstrip().rstrip(";")
        self.assertEqual(
            json.loads(body)["schema_version"], SCHEMA_VERSION
        )

    def test_export_writes_target_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "coach_data.js"
            written = export_coach_payload(target)
            self.assertEqual(written, target)
            content = target.read_text(encoding="utf-8")
            self.assertIn(f"window.{COACH_GLOBAL}", content)
            self.assertIn("safe_for_examiner", content)


class SpanishLocalizationGuardTests(unittest.TestCase):
    """Phase Z.2: coach_data.js learner-facing strings must be Spanish.

    These tests prevent a regeneration from reintroducing English into the
    deployed coach payload (the regression that motivated upstream
    reconciliation on 2026-06-10).
    """

    @classmethod
    def setUpClass(cls):
        cls.payload = build_coach_payload()

    # Distinctive English markers from the original (English) knowledge assets.
    ENGLISH_MARKERS = (
        "Work through",
        "For MCQ",
        "Make an informed judgement",
        "Give reasons for",
        "State the cause",
        "the correct answer",
        "must be justified by specific tasting observations",
        "Count the marks",
        "Overthinking distractors",
    )

    def _learner_strings(self):
        out = []
        for spec in self.payload["command_verbs"].values():
            out.append(spec["definition"])
            out.extend(spec["do"])
            out.extend(spec["do_not"])
            out.append(spec["mentor_hint"])
        for hint in self.payload["mentor_hints"].values():
            out.append(hint["hint"])
            out.extend(hint.get("common_errors", []))
        out.append(self.payload["quality_principle"])
        out.extend(self.payload["common_quality_errors"])
        out.append(self.payload["simple_wine_note"])
        return out

    def test_no_english_markers_in_learner_strings(self):
        joined = " | ".join(self._learner_strings())
        for marker in self.ENGLISH_MARKERS:
            self.assertNotIn(marker, joined, f"English marker leaked: {marker!r}")

    def test_every_command_verb_has_spanish_override(self):
        from tools.question_generation.distinction_coach_exporter import (
            COMMAND_VERBS,
            ES_COMMAND_VERBS,
        )
        for verb in COMMAND_VERBS:
            self.assertIn(verb, ES_COMMAND_VERBS)
            for field in ("definition", "do", "do_not", "mentor_hint"):
                self.assertTrue(ES_COMMAND_VERBS[verb][field], f"{verb}.{field} empty")

    def test_every_mentor_hint_topic_has_spanish_override(self):
        import json
        from tools.question_generation.distinction_coach_exporter import (
            ES_MENTOR_HINTS,
            MENTOR_HINTS_PATH,
        )
        topics = json.loads(MENTOR_HINTS_PATH.read_text(encoding="utf-8"))["hints_by_topic"]
        for topic in topics:
            self.assertIn(topic, ES_MENTOR_HINTS)
            self.assertTrue(ES_MENTOR_HINTS[topic]["hint"], f"{topic}.hint empty")

    def test_export_fails_when_translation_missing(self):
        import tools.question_generation.distinction_coach_exporter as exporter
        removed = exporter.ES_COMMAND_VERBS.pop("explain")
        try:
            with self.assertRaises(ValueError):
                exporter.build_coach_payload()
        finally:
            exporter.ES_COMMAND_VERBS["explain"] = removed

    def test_rendered_js_declares_spanish_contract(self):
        js = render_coach_js(self.payload)
        self.assertIn("Spanish by contract", js)


if __name__ == "__main__":
    unittest.main()
