from __future__ import annotations

import copy
import unittest

from tools.learner_model.misconception_adapter import (
    build_active_insights,
    build_insight,
    detect_text_evidence,
    load_node_index,
    normalize_node,
    record_evidence,
    summarize_evidence,
)


class LegacyNodeCompatibilityTests(unittest.TestCase):
    def test_all_legacy_nodes_load_without_schema_migration(self) -> None:
        index = load_node_index()

        self.assertEqual(len(index), 42)
        for mc_id, node in index.items():
            with self.subTest(mc_id=mc_id):
                self.assertEqual(node["misconception_id"], mc_id)
                self.assertNotIn("weakness_signal", node)
                self.assertNotIn("coaching_content", node)
                self.assertNotIn("remediation_topics", node)

    def test_normalization_does_not_mutate_legacy_node(self) -> None:
        node = load_node_index()["MC_MLF_01"]
        before = copy.deepcopy(node)

        adapted = normalize_node(node)

        self.assertEqual(node, before)
        self.assertEqual(adapted["misconception_id"], "MC_MLF_01")
        self.assertEqual(adapted["source"]["misconception"], node["misconception"])
        self.assertEqual(adapted["weakness_relationships"]["topics"], node["related_topics"])
        self.assertEqual(adapted["weakness_relationships"]["concepts"], node["related_concepts"])


class TextEvidenceDetectionTests(unittest.TestCase):
    def test_each_node_is_detectable_from_its_canonical_statement(self) -> None:
        for mc_id, node in load_node_index().items():
            with self.subTest(mc_id=mc_id):
                result = detect_text_evidence(
                    node["misconception"],
                    candidate_ids=[mc_id],
                )
                self.assertTrue(result["detected"])
                self.assertEqual(result["misconception_id"], mc_id)
                self.assertTrue(result["matched_signals"])

    def test_detection_can_be_constrained_to_relevant_nodes(self) -> None:
        result = detect_text_evidence(
            "MLF always makes a wine taste buttery.",
            candidate_ids=["MC_OAK_01"],
        )

        self.assertFalse(result["detected"])
        self.assertIsNone(result["misconception_id"])

    def test_unknown_explicit_id_is_rejected(self) -> None:
        result = detect_text_evidence("", explicit_id="MC_DOES_NOT_EXIST")

        self.assertFalse(result["detected"])
        self.assertEqual(result["reason"], "unknown_misconception_id")

    def test_known_explicit_id_remains_backward_compatible(self) -> None:
        result = detect_text_evidence(
            "",
            explicit_id="MC_TANNIN_01",
            source_type="sba",
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["misconception_id"], "MC_TANNIN_01")
        self.assertEqual(result["detection_method"], "explicit_id")

    def test_generic_topic_weakness_is_not_direct_evidence(self) -> None:
        result = detect_text_evidence(
            "The learner is weak on winemaking.",
            source_type="weakness_profile",
        )

        self.assertFalse(result["detected"])

    def test_sba_or_sat_and_explicit_weakness_sources_use_same_adapter(self) -> None:
        statement = load_node_index()["MC_OAK_QUALITY_01"]["misconception"]
        for source_type in ("sba", "open_response", "sat"):
            with self.subTest(source_type=source_type):
                result = detect_text_evidence(
                    statement,
                    candidate_ids=["MC_OAK_QUALITY_01"],
                    source_type=source_type,
                )
                self.assertTrue(result["detected"])
                self.assertEqual(result["source_type"], source_type)

        weakness_result = detect_text_evidence(
            "",
            explicit_id="MC_OAK_QUALITY_01",
            source_type="weakness_profile",
        )
        self.assertTrue(weakness_result["detected"])
        self.assertEqual(weakness_result["source_type"], "weakness_profile")


class EvidenceAccumulationTests(unittest.TestCase):
    def _observe(
        self,
        les: dict,
        *,
        session_id: str,
        item_id: str,
        timestamp: str,
        outcome: str = "observed",
    ) -> dict:
        return record_evidence(
            les,
            misconception_id="MC_MLF_01",
            source_type="sba",
            session_id=session_id,
            item_id=item_id,
            timestamp=timestamp,
            outcome=outcome,
            matched_signals=["MLF always makes a wine taste buttery."],
        )

    def test_confidence_labels_follow_evidence_frequency(self) -> None:
        first = self._observe(
            {},
            session_id="s1",
            item_id="q1",
            timestamp="2026-06-15T10:00:00Z",
        )
        self.assertEqual(summarize_evidence(first, "MC_MLF_01")["confidence_label"], "low")

        second = self._observe(
            first,
            session_id="s1",
            item_id="q2",
            timestamp="2026-06-15T10:01:00Z",
        )
        self.assertEqual(summarize_evidence(second, "MC_MLF_01")["confidence_label"], "medium")

        third = self._observe(
            second,
            session_id="s2",
            item_id="q3",
            timestamp="2026-06-15T11:00:00Z",
        )
        summary = summarize_evidence(third, "MC_MLF_01")
        self.assertEqual(summary["confidence_label"], "high")
        self.assertEqual(summary["evidence_count"], 3)
        self.assertEqual(summary["session_count"], 2)

    def test_correction_reduces_active_confidence_without_deleting_history(self) -> None:
        observed = self._observe(
            {},
            session_id="s1",
            item_id="q1",
            timestamp="2026-06-15T10:00:00Z",
        )
        corrected = self._observe(
            observed,
            session_id="s2",
            item_id="q2",
            timestamp="2026-06-15T11:00:00Z",
            outcome="corrected",
        )

        summary = summarize_evidence(corrected, "MC_MLF_01")
        self.assertFalse(summary["active"])
        self.assertEqual(summary["confidence_label"], "none")
        self.assertEqual(summary["lifetime_observation_count"], 1)
        self.assertEqual(summary["correction_count"], 1)

    def test_duplicate_event_is_idempotent(self) -> None:
        first = self._observe(
            {},
            session_id="s1",
            item_id="q1",
            timestamp="2026-06-15T10:00:00Z",
        )
        duplicate = self._observe(
            first,
            session_id="s1",
            item_id="q1",
            timestamp="2026-06-15T10:00:00Z",
        )

        self.assertEqual(first, duplicate)

    def test_evidence_recording_does_not_mutate_input(self) -> None:
        les = {"misconception_evidence": {}}
        before = copy.deepcopy(les)

        self._observe(
            les,
            session_id="s1",
            item_id="q1",
            timestamp="2026-06-15T10:00:00Z",
        )

        self.assertEqual(les, before)


class RecommendationAndCoachingTests(unittest.TestCase):
    def test_each_node_builds_complete_formative_coaching(self) -> None:
        for mc_id in load_node_index():
            with self.subTest(mc_id=mc_id):
                les = record_evidence(
                    {},
                    misconception_id=mc_id,
                    source_type="open_response",
                    session_id="s1",
                    item_id="or1",
                    timestamp="2026-06-15T10:00:00Z",
                    outcome="observed",
                )
                insight = build_insight(les, mc_id)

                self.assertTrue(insight["active"])
                self.assertTrue(insight["student_statement"])
                self.assertTrue(insight["coaching"]["why_it_matters"])
                self.assertTrue(insight["coaching"]["what_is_confused"])
                self.assertTrue(insight["coaching"]["evidence_triggered"])
                self.assertTrue(insight["coaching"]["practice_next"])
                self.assertTrue(insight["coaching"]["improvement_signal"])
                self.assertTrue(insight["recommendation"]["practice_topics"])
                self.assertFalse(insight["governance"]["safe_for_examiner"])
                self.assertFalse(insight["governance"]["examiner_scoring_allowed"])

    def test_active_insights_are_ranked_by_evidence_frequency(self) -> None:
        les: dict = {}
        for index in range(3):
            les = record_evidence(
                les,
                misconception_id="MC_MLF_01",
                source_type="sba",
                session_id=f"s{index // 2}",
                item_id=f"q{index}",
                timestamp=f"2026-06-15T10:0{index}:00Z",
                outcome="observed",
            )
        les = record_evidence(
            les,
            misconception_id="MC_OAK_01",
            source_type="sat",
            session_id="s1",
            item_id="sat1",
            timestamp="2026-06-15T11:00:00Z",
            outcome="observed",
        )

        insights = build_active_insights(les)

        self.assertEqual(insights[0]["misconception_id"], "MC_MLF_01")
        self.assertEqual(insights[0]["confidence_label"], "high")
        self.assertEqual(insights[1]["confidence_label"], "low")

    def test_corrected_insight_is_not_returned_as_active(self) -> None:
        les = record_evidence(
            {},
            misconception_id="MC_MLF_01",
            source_type="sba",
            session_id="s1",
            item_id="q1",
            timestamp="2026-06-15T10:00:00Z",
            outcome="observed",
        )
        les = record_evidence(
            les,
            misconception_id="MC_MLF_01",
            source_type="sba",
            session_id="s2",
            item_id="q2",
            timestamp="2026-06-15T11:00:00Z",
            outcome="corrected",
        )

        self.assertEqual(build_active_insights(les), [])


if __name__ == "__main__":
    unittest.main()
