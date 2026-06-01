from __future__ import annotations

import builtins
import copy
import unittest
from unittest.mock import patch

from tests.test_structured_question_bank_adapter import SOURCE_BANK_PATH, clean_source_item
from tests.test_structured_question_bank_enrichment_contract import complete_enriched_item
from tools.question_generation.diagnostic_sba_validator import validate_diagnostic_sba_item
from tools.question_generation.structured_question_bank_adapter import map_structured_question_skeleton
from tools.question_generation.structured_question_bank_enrichment import (
    EnrichmentStatus,
    build_enrichment_placeholders,
    evaluate_enrichment_readiness,
    is_enrichment_complete,
    requires_human_review,
    summarize_enrichment_gaps,
)


def adapter_skeleton() -> dict:
    return map_structured_question_skeleton(clean_source_item(), SOURCE_BANK_PATH)


class StructuredQuestionBankEnrichmentTests(unittest.TestCase):
    def test_readiness_detects_missing_source_support(self) -> None:
        statuses = evaluate_enrichment_readiness(adapter_skeleton())

        self.assertIn(EnrichmentStatus.SOURCE_SUPPORT_MISSING, statuses)

    def test_readiness_detects_missing_option_diagnostics(self) -> None:
        statuses = evaluate_enrichment_readiness(adapter_skeleton())

        self.assertIn(EnrichmentStatus.OPTION_DIAGNOSTICS_MISSING, statuses)

    def test_readiness_detects_missing_rationales(self) -> None:
        statuses = evaluate_enrichment_readiness(adapter_skeleton())

        self.assertIn(EnrichmentStatus.RATIONALE_MISSING, statuses)

    def test_readiness_detects_missing_remediation(self) -> None:
        statuses = evaluate_enrichment_readiness(adapter_skeleton())

        self.assertIn(EnrichmentStatus.REMEDIATION_MISSING, statuses)

    def test_governance_incomplete_detected_if_unsafe_or_missing(self) -> None:
        unsafe = adapter_skeleton()
        unsafe["governance"]["safe_for_examiner"] = True
        missing = adapter_skeleton()
        missing["governance"].pop("uses_api")

        self.assertIn(EnrichmentStatus.GOVERNANCE_INCOMPLETE, evaluate_enrichment_readiness(unsafe))
        self.assertIn(EnrichmentStatus.GOVERNANCE_INCOMPLETE, evaluate_enrichment_readiness(missing))

    def test_placeholders_added_deterministically(self) -> None:
        first = build_enrichment_placeholders(adapter_skeleton())
        second = build_enrichment_placeholders(adapter_skeleton())

        self.assertEqual(first, second)
        for section in (
            "source_support",
            "option_diagnostics",
            "misconception_linkage",
            "causal_chain_linkage",
            "sat_relevance",
            "rationales",
            "remediation",
            "human_review",
        ):
            self.assertIn(section, first)

    def test_placeholders_do_not_invent_source_ids(self) -> None:
        state = build_enrichment_placeholders(adapter_skeleton())

        self.assertEqual(state["source_support"]["source_ids"], [])
        self.assertEqual(state["source_support"]["source_chunks"], [])
        self.assertIsNone(state["source_support"]["support_rationale"])

    def test_placeholders_do_not_invent_misconception_ids(self) -> None:
        state = build_enrichment_placeholders(adapter_skeleton())

        for option_state in state["misconception_linkage"].values():
            self.assertIsNone(option_state["misconception_id"])
            self.assertEqual(option_state["evidence"], [])

    def test_placeholders_do_not_invent_causal_chain_ids(self) -> None:
        state = build_enrichment_placeholders(adapter_skeleton())

        self.assertIsNone(state["causal_chain_linkage"]["causal_chain_id"])
        self.assertEqual(state["causal_chain_linkage"]["evidence"], [])

    def test_placeholders_do_not_invent_sat_relevance(self) -> None:
        state = build_enrichment_placeholders(adapter_skeleton())

        self.assertEqual(state["sat_relevance"]["aliases"], [])
        self.assertEqual(state["sat_relevance"]["evidence"], [])

    def test_requires_human_review_is_true_for_incomplete_enrichment(self) -> None:
        state = build_enrichment_placeholders(adapter_skeleton())

        self.assertTrue(requires_human_review(state))

    def test_complete_mock_enrichment_recognized_only_when_all_fields_present(self) -> None:
        complete = complete_enriched_item()
        incomplete = complete_enriched_item()
        incomplete["source_support"]["source_ids"] = []

        self.assertEqual(evaluate_enrichment_readiness(complete), [])
        self.assertTrue(is_enrichment_complete(complete))
        self.assertIn(EnrichmentStatus.SOURCE_SUPPORT_MISSING, evaluate_enrichment_readiness(incomplete))
        self.assertFalse(is_enrichment_complete(incomplete))

    def test_summarize_gaps_deterministic(self) -> None:
        state = build_enrichment_placeholders(adapter_skeleton())

        first = summarize_enrichment_gaps(state)
        second = summarize_enrichment_gaps(copy.deepcopy(state))

        self.assertEqual(first, second)
        self.assertEqual(
            first,
            [
                "source support is missing or incomplete",
                "option diagnostic metadata is missing or incomplete",
                "correct or distractor rationales are missing",
                "remediation recommendation or target is missing",
                "human review is required before enrichment can complete",
            ],
        )

    def test_input_skeleton_not_mutated(self) -> None:
        skeleton = adapter_skeleton()
        before = copy.deepcopy(skeleton)

        evaluate_enrichment_readiness(skeleton)
        build_enrichment_placeholders(skeleton)
        requires_human_review(skeleton)
        summarize_enrichment_gaps(skeleton)

        self.assertEqual(skeleton, before)

    def test_validator_rejects_placeholder_enriched_skeleton_until_real_enrichment_exists(self) -> None:
        state = build_enrichment_placeholders(adapter_skeleton())

        errors = validate_diagnostic_sba_item(state)

        self.assertTrue(errors)
        self.assertIn("source_support.source_ids must be a non-empty list", errors)
        self.assertIn("feedback.correct_rationale must be present and non-empty", errors)

    def test_no_file_writes(self) -> None:
        skeleton = adapter_skeleton()
        original_open = builtins.open

        def fail_open(*args, **kwargs):
            raise AssertionError("enrichment skeleton must not open files")

        with patch("builtins.open", side_effect=fail_open):
            evaluate_enrichment_readiness(skeleton)
            build_enrichment_placeholders(skeleton)
            requires_human_review(skeleton)
            summarize_enrichment_gaps(skeleton)

        self.assertIs(builtins.open, original_open)


if __name__ == "__main__":
    unittest.main()
