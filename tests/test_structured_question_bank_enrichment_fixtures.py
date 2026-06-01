from __future__ import annotations

import copy
import unittest

from tests.fixtures.diagnostic_sba.enrichment_fixtures import (
    make_fully_enriched_item,
    make_human_review_item,
    make_partially_enriched_item,
    make_unsafe_governance_item,
)
from tools.question_generation.diagnostic_sba_validator import validate_diagnostic_sba_item
from tools.question_generation.structured_question_bank_enrichment import (
    EnrichmentStatus,
    evaluate_enrichment_readiness,
    is_enrichment_complete,
    requires_human_review,
)


FORBIDDEN_AUTHORITY_PHRASES = (
    "official wset question",
    "official wset score",
    "examiner mark",
    "certified result",
    "guaranteed pass",
    "pass/fail",
)


class StructuredQuestionBankEnrichmentFixtureTests(unittest.TestCase):
    def test_fully_enriched_fixture_passes_diagnostic_sba_validator(self) -> None:
        self.assertEqual(validate_diagnostic_sba_item(make_fully_enriched_item()), [])

    def test_fully_enriched_fixture_returns_enrichment_complete(self) -> None:
        item = make_fully_enriched_item()

        self.assertEqual(evaluate_enrichment_readiness(item), [])
        self.assertTrue(is_enrichment_complete(item))
        self.assertEqual(item["enrichment_status"], EnrichmentStatus.ENRICHMENT_COMPLETE)

    def test_partially_enriched_fixture_fails_validator(self) -> None:
        errors = validate_diagnostic_sba_item(make_partially_enriched_item())

        self.assertIn("source_support.source_ids must be a non-empty list", errors)
        self.assertIn("source_support.source_chunks must be a non-empty list", errors)

    def test_partially_enriched_fixture_reports_missing_status(self) -> None:
        statuses = evaluate_enrichment_readiness(make_partially_enriched_item())

        self.assertIn(EnrichmentStatus.SOURCE_SUPPORT_MISSING, statuses)

    def test_human_review_fixture_requires_human_review(self) -> None:
        item = make_human_review_item()

        self.assertTrue(requires_human_review(item))
        self.assertIn(EnrichmentStatus.OPTION_DIAGNOSTICS_MISSING, evaluate_enrichment_readiness(item))
        self.assertIn(EnrichmentStatus.DEFER_FOR_HUMAN_REVIEW, evaluate_enrichment_readiness(item))

    def test_unsafe_governance_fixture_fails_validator(self) -> None:
        errors = validate_diagnostic_sba_item(make_unsafe_governance_item())

        self.assertIn("governance.safe_for_examiner must be false", errors)
        self.assertIn("governance.examiner_scoring_allowed must be false", errors)

    def test_unsafe_governance_fixture_reports_governance_incomplete(self) -> None:
        statuses = evaluate_enrichment_readiness(make_unsafe_governance_item())

        self.assertIn(EnrichmentStatus.GOVERNANCE_INCOMPLETE, statuses)

    def test_fixtures_do_not_mutate_across_calls(self) -> None:
        first = make_fully_enriched_item()
        first["options"]["A"]["option_text"] = "mutated in test"
        second = make_fully_enriched_item()

        self.assertNotEqual(first["options"]["A"]["option_text"], second["options"]["A"]["option_text"])
        self.assertEqual(second["options"]["A"]["option_text"], "The supported factor increases the observed effect.")

    def test_fixtures_contain_exactly_four_options(self) -> None:
        for item in (
            make_fully_enriched_item(),
            make_partially_enriched_item(),
            make_human_review_item(),
            make_unsafe_governance_item(),
        ):
            self.assertEqual(set(item["options"].keys()), {"A", "B", "C", "D"})

    def test_fixtures_contain_exactly_one_correct_option(self) -> None:
        item = make_fully_enriched_item()
        correct_options = [key for key, option in item["options"].items() if option["is_correct"]]

        self.assertEqual(correct_options, ["A"])

    def test_option_diagnostics_have_correct_option_role_correct(self) -> None:
        item = make_fully_enriched_item()

        self.assertEqual(item["options"]["A"]["diagnostic_role"], "correct")

    def test_incorrect_options_do_not_use_correct_role(self) -> None:
        item = make_fully_enriched_item()

        for key in ("B", "C", "D"):
            self.assertNotEqual(item["options"][key]["diagnostic_role"], "correct")

    def test_source_support_role_is_explicit(self) -> None:
        item = make_fully_enriched_item()

        self.assertEqual(item["source_support"]["source_role"], "knowledge_map_support")

    def test_remediation_recommendation_present_in_complete_fixture(self) -> None:
        item = make_fully_enriched_item()

        self.assertTrue(item["feedback"]["remediation_recommendation"])
        self.assertEqual(item["feedback"]["remediation_target"]["target_type"], "topic")

    def test_no_official_authority_wording_appears(self) -> None:
        fixtures = (
            make_fully_enriched_item(),
            make_partially_enriched_item(),
            make_human_review_item(),
            make_unsafe_governance_item(),
        )

        for item in fixtures:
            text = str(item).lower()
            for phrase in FORBIDDEN_AUTHORITY_PHRASES:
                self.assertNotIn(phrase, text)

    def test_fixture_validation_does_not_mutate_item(self) -> None:
        item = make_fully_enriched_item()
        before = copy.deepcopy(item)

        validate_diagnostic_sba_item(item)
        evaluate_enrichment_readiness(item)
        requires_human_review(item)

        self.assertEqual(item, before)


if __name__ == "__main__":
    unittest.main()
