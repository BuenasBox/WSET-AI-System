from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.question_generation.diagnostic_sba_validator import validate_diagnostic_sba_item
from tools.question_generation.human_review_resolution import (
    ApprovalScope,
    ReviewStatus,
    SAFE_GOVERNANCE,
    can_promote_to_static_demo,
    validate_review_record,
)


CONTRACT_PATH = Path("docs/STATIC_DEMO_EXPORT_CONTRACT.md")
PREGUNTAS_PATH = Path("frontend/diagnostic-sba/preguntas.json")


def valid_draft(source_question_id: str = "2") -> dict:
    return {
        "schema_version": "diagnostic_sba_item_v1",
        "draft_notice": "Human-review draft only. Not official assessment material.",
        "enrichment_status": "defer_for_human_review",
        "identity": {
            "item_id": f"draft_diag_sba_structured_{source_question_id}",
            "item_version": "0.1.0-draft",
            "created_by": "contract_fixture",
            "generation_method": "manual_repo_local_enrichment_draft",
            "training_item_only": True,
            "source_question_id": source_question_id,
        },
        "lineage": {
            "source_question_id": source_question_id,
            "source_bank_path": "knowledge/question-bank/structured/wset3_questions.json",
            "adapter_version": "structured_adapter_v0",
            "enrichment_version": "contract_fixture_v0",
            "transformation_notes": ["Contract fixture only."],
        },
        "curriculum": {
            "ra_id": "RA4",
            "topic": "fortified_wines",
            "subtopic": "port_fortification_fermentation",
            "difficulty": "intermediate",
            "learning_objective": "Identify a training-only diagnostic relationship.",
        },
        "question": {
            "stem": "What stops fermentation in Port production?",
            "question_type": "single_best_answer",
            "expected_reasoning_type": "process",
        },
        "options": {
            "A": {
                "option_id": "A",
                "option_text": "Long maturation",
                "is_correct": False,
                "diagnostic_role": "process_confusion",
                "misconception_id": None,
                "diagnostic_note": "Confuses ageing with fermentation control.",
            },
            "B": {
                "option_id": "B",
                "option_text": "American oak",
                "is_correct": False,
                "diagnostic_role": "process_confusion",
                "misconception_id": None,
                "diagnostic_note": "Confuses vessel choice with fermentation control.",
            },
            "C": {
                "option_id": "C",
                "option_text": "Addition of grape spirit",
                "is_correct": True,
                "diagnostic_role": "correct",
                "misconception_id": None,
                "diagnostic_note": "Matches the fortification process.",
            },
            "D": {
                "option_id": "D",
                "option_text": "Sun drying",
                "is_correct": False,
                "diagnostic_role": "regional_confusion",
                "misconception_id": None,
                "diagnostic_note": "Confuses a grape-concentration technique with Port.",
            },
        },
        "source_support": {
            "source_ids": ["CC_FORTIFICATION_RESIDUAL_SUGAR"],
            "source_chunks": ["knowledge/knowledge-map/causal-chains/cc_fortification_residual_sugar.json"],
            "support_rationale": "Local causal-chain support identifies fortification as the process.",
            "source_role": "knowledge_map_support",
            "status": "draft_requires_human_review",
        },
        "causal_chain_linkage": {
            "causal_chain_id": "CC_FORTIFICATION_RESIDUAL_SUGAR",
            "status": "draft_supported_by_expected_causal_links",
        },
        "misconception_linkage": {
            "status": "none_attached",
            "notes": "No direct misconception node confirmed.",
        },
        "sat_relevance": [],
        "feedback": {
            "correct_rationale": "Adding grape spirit stops fermentation.",
            "why_other_options_are_wrong": {
                "A": "Maturation does not stop fermentation.",
                "B": "Oak choice does not stop fermentation.",
                "C": "This is the correct answer.",
                "D": "Sun drying is not the Port fermentation-control method.",
            },
            "remediation_recommendation": "Review fortification and residual sugar.",
            "remediation_target": {
                "target_type": "causal_chain",
                "target_id": "CC_FORTIFICATION_RESIDUAL_SUGAR",
            },
        },
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
        "attempt_analytics_placeholders": {
            "response_time": None,
            "confidence": None,
            "answer_changed": None,
            "diagnosed_error_type": None,
            "hesitation": None,
            "recommended_next_action": None,
        },
        "human_review": {
            "required": True,
            "reasons": ["Contract fixture."],
            "risk_level": "low",
            "reviewer_notes": "",
        },
    }


def valid_review(
    source_question_id: str = "2",
    status: str = ReviewStatus.APPROVED_FOR_STATIC_DEMO,
    scope: str = ApprovalScope.STATIC_DEMO_ONLY,
) -> dict:
    return {
        "review_id": f"review_{source_question_id}_20260602_001",
        "source_question_id": source_question_id,
        "draft_id": f"draft_diag_sba_structured_{source_question_id}",
        "reviewer": "contract_reviewer",
        "reviewed_at": "2026-06-02T00:00:00Z",
        "review_status": status,
        "risk_before": "low",
        "risk_after": "low",
        "checklist": {
            "source_support_checked": True,
            "correct_answer_checked": True,
            "distractor_logic_checked": True,
            "diagnostic_roles_checked": True,
            "misconception_links_checked": True,
            "causal_chain_links_checked": True,
            "sat_relevance_checked": True,
            "rationale_quality_checked": True,
            "remediation_quality_checked": True,
            "wording_safety_checked": True,
            "governance_checked": True,
        },
        "issues_found": [],
        "required_changes": [],
        "approval_scope": scope,
        "governance_confirmation": copy.deepcopy(SAFE_GOVERNANCE),
        "notes": "Static demo only.",
    }


def is_export_eligible(draft: dict, review: dict | None) -> bool:
    if not isinstance(review, dict):
        return False
    if validate_diagnostic_sba_item(draft):
        return False
    if draft.get("governance") != SAFE_GOVERNANCE:
        return False
    if validate_review_record(review):
        return False
    if review.get("governance_confirmation") != SAFE_GOVERNANCE:
        return False
    return can_promote_to_static_demo(draft, review)


def build_contract_payload(drafts: list[dict], reviews: list[dict]) -> dict:
    reviews_by_source_id = {record["source_question_id"]: record for record in reviews}
    eligible_drafts = [
        draft
        for draft in drafts
        if is_export_eligible(draft, reviews_by_source_id.get(draft["identity"]["source_question_id"]))
    ]
    eligible_drafts.sort(key=lambda draft: int(draft["identity"]["source_question_id"]))

    items = []
    outcomes_by_item_id = {}
    for draft in eligible_drafts:
        source_id = draft["identity"]["source_question_id"]
        review = reviews_by_source_id[source_id]
        item_id = draft["identity"]["item_id"]
        items.append(
            {
                "item_id": item_id,
                "source_question_id": source_id,
                "draft_id": item_id,
                "review_id": review["review_id"],
                "approval_scope": review["approval_scope"],
                "static_demo_only": True,
                "training_item_only": True,
                "official_wset_question": False,
                "safe_for_examiner": False,
                "examiner_scoring_allowed": False,
                "question": {
                    "stem": draft["question"]["stem"],
                    "question_type": draft["question"]["question_type"],
                },
                "options": [
                    {
                        "option_id": key,
                        "option_text": option["option_text"],
                    }
                    for key, option in sorted(draft["options"].items())
                ],
            }
        )
        outcomes_by_item_id[item_id] = {
            "correct_option_id": next(key for key, option in draft["options"].items() if option["is_correct"]),
            "feedback": copy.deepcopy(draft["feedback"]),
        }

    return {
        "export_version": "static_demo_export_v0",
        "exported_at": "2026-06-02T00:00:00Z",
        "disclaimer": "PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET",
        "items": items,
        "outcomes_by_item_id": outcomes_by_item_id,
    }


class StaticDemoExportContractTests(unittest.TestCase):
    def test_contract_document_exists(self) -> None:
        self.assertTrue(CONTRACT_PATH.exists())

    def test_approved_for_static_demo_item_eligible(self) -> None:
        draft = valid_draft("2")
        review = valid_review("2")

        self.assertTrue(is_export_eligible(draft, review))

    def test_requires_revision_item_excluded(self) -> None:
        draft = valid_draft("1")
        review = valid_review("1", ReviewStatus.REQUIRES_REVISION, ApprovalScope.INTERNAL_REVIEW_ONLY)

        self.assertFalse(is_export_eligible(draft, review))

    def test_rejected_item_excluded(self) -> None:
        draft = valid_draft("3")
        review = valid_review("3", ReviewStatus.REJECTED, ApprovalScope.INTERNAL_REVIEW_ONLY)

        self.assertFalse(is_export_eligible(draft, review))

    def test_missing_review_excluded(self) -> None:
        self.assertFalse(is_export_eligible(valid_draft("2"), None))

    def test_unsafe_governance_excluded(self) -> None:
        draft = valid_draft("2")
        draft["governance"]["safe_for_examiner"] = True

        self.assertFalse(is_export_eligible(draft, valid_review("2")))

    def test_forbidden_scope_excluded(self) -> None:
        draft = valid_draft("2")
        review = valid_review("2", ReviewStatus.APPROVED_FOR_STATIC_DEMO, "production")

        self.assertFalse(is_export_eligible(draft, review))

    def test_pre_submit_payload_does_not_expose_correctness(self) -> None:
        payload = build_contract_payload([valid_draft("2")], [valid_review("2")])
        render_text = json.dumps(payload["items"], ensure_ascii=False)

        self.assertNotIn("is_correct", render_text)
        self.assertNotIn("correct_option_id", render_text)
        self.assertIn("correct_option_id", json.dumps(payload["outcomes_by_item_id"]))

    def test_pre_submit_payload_does_not_expose_diagnostic_roles(self) -> None:
        payload = build_contract_payload([valid_draft("2")], [valid_review("2")])
        render_text = json.dumps(payload["items"], ensure_ascii=False)

        self.assertNotIn("diagnostic_role", render_text)
        self.assertNotIn("misconception", render_text.lower())
        self.assertNotIn("remediation", render_text.lower())

    def test_outcome_payload_separated(self) -> None:
        payload = build_contract_payload([valid_draft("2")], [valid_review("2")])

        self.assertIn("items", payload)
        self.assertIn("outcomes_by_item_id", payload)
        self.assertNotEqual(payload["items"], payload["outcomes_by_item_id"])

    def test_export_metadata_preserves_review_source_lineage(self) -> None:
        payload = build_contract_payload([valid_draft("2")], [valid_review("2")])
        item = payload["items"][0]

        self.assertEqual(item["source_question_id"], "2")
        self.assertEqual(item["draft_id"], "draft_diag_sba_structured_2")
        self.assertEqual(item["review_id"], "review_2_20260602_001")
        self.assertEqual(item["approval_scope"], "static_demo_only")
        self.assertEqual(payload["export_version"], "static_demo_export_v0")
        self.assertEqual(payload["exported_at"], "2026-06-02T00:00:00Z")

    def test_deterministic_ordering(self) -> None:
        payload = build_contract_payload(
            [valid_draft("17"), valid_draft("2"), valid_draft("12")],
            [valid_review("17"), valid_review("2"), valid_review("12")],
        )

        self.assertEqual([item["source_question_id"] for item in payload["items"]], ["2", "12", "17"])

    def test_contract_builder_does_not_write_preguntas_json(self) -> None:
        before = PREGUNTAS_PATH.read_text(encoding="utf-8") if PREGUNTAS_PATH.exists() else None

        build_contract_payload([valid_draft("2")], [valid_review("2")])

        after = PREGUNTAS_PATH.read_text(encoding="utf-8") if PREGUNTAS_PATH.exists() else None
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
