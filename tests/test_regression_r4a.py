"""R4-A regression tests.

Two known fragility points that must never silently regress:

1. Tokaji answer must NOT trigger weak_exam_register.
   The word "tokaji" contains the substring "ok"; the guard uses " ok" (leading
   space) to avoid false-positives on wine names.  This test anchors that fix.

2. forced_causal_chains must NOT produce shallow_retrieval=True.
   When the orchestrator injects causal chain nodes, _audit_retrieval must count
   them as high-priority content so the answer is not mis-labelled as shallow.
"""

import unittest

from tools.self_eval.answer_comparator import _audit_retrieval, _weak_exam_register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _minimal_chunk(retrieval_priority: str = "low") -> dict:
    """A retrieved context item with no golden/high-priority signal."""
    return {
        "context_type": "retrieval_sandbox_chunk",
        "source_type": "manual_curated_srt",
        "why_retrieved": ["matched canonical/query terms: tannin"],
        "retrieval_priority": retrieval_priority,
    }


def _theory_question() -> dict:
    return {"question_type": "theory"}


# ---------------------------------------------------------------------------
# Tokaji regression
# ---------------------------------------------------------------------------

class TokajWeakExamRegisterTests(unittest.TestCase):
    """Tokaji answers must not trigger weak_exam_register."""

    def _tokaji_answer(self) -> str:
        return (
            "para efectos del examen, el tokaji aszú concentra azúcar y acidez "
            "porque la botrytis cinerea deshidrata las uvas; el balance resultante "
            "evidencia calidad y wset."
        )

    def test_tokaji_answer_not_weak_exam_register_hard(self) -> None:
        result = _weak_exam_register(self._tokaji_answer(), _theory_question(), "hard")
        self.assertFalse(result, "Tokaji answer must NOT trigger weak_exam_register at hard strictness")

    def test_tokaji_answer_not_weak_exam_register_brutal(self) -> None:
        result = _weak_exam_register(self._tokaji_answer(), _theory_question(), "brutal")
        self.assertFalse(result, "Tokaji answer must NOT trigger weak_exam_register at brutal strictness")

    def test_ok_mid_word_does_not_trigger(self) -> None:
        """'ok' as a mid-word substring (tokaji, sake) must not fire."""
        answer = "para efectos del examen, el tokaji y el sake muestran balance y calidad evidenciada."
        self.assertFalse(_weak_exam_register(answer, _theory_question(), "brutal"))

    def test_bare_ok_with_leading_space_does_trigger(self) -> None:
        """Conversational ' ok' (standalone) must still fire."""
        answer = "bueno, es ok que el vino tenga algo de acidez."
        self.assertTrue(_weak_exam_register(answer, _theory_question(), "brutal"))

    def test_normal_strictness_never_triggers(self) -> None:
        """At 'normal' strictness weak_exam_register always returns False."""
        answer = "basically ok, sort of good."
        self.assertFalse(_weak_exam_register(answer, _theory_question(), "normal"))


# ---------------------------------------------------------------------------
# forced_causal_chains shallow_retrieval regression
# ---------------------------------------------------------------------------

class ForcedCausalChainsShallowRetrievalTests(unittest.TestCase):
    """forced_causal_chains must prevent shallow_retrieval being flagged True."""

    def _package_without_chains(self) -> dict:
        return {
            "retrieved_context": [_minimal_chunk(), _minimal_chunk(), _minimal_chunk()],
            "forced_causal_chains": [],
        }

    def _package_with_chains(self) -> dict:
        return {
            "retrieved_context": [_minimal_chunk(), _minimal_chunk(), _minimal_chunk()],
            "forced_causal_chains": [
                {"id": "CC_COOL_CLIMATE_ACIDITY", "steps": ["step1", "step2"]},
            ],
        }

    def test_without_chains_is_shallow(self) -> None:
        """Baseline: low-priority-only chunks with no chains → shallow_retrieval=True."""
        audit = _audit_retrieval(self._package_without_chains(), "hard")
        self.assertTrue(
            audit["shallow_retrieval"],
            "Package with only low-priority chunks and no causal chains should be shallow",
        )

    def test_with_chains_not_shallow(self) -> None:
        """forced_causal_chains must lift high_priority so shallow_retrieval=False."""
        audit = _audit_retrieval(self._package_with_chains(), "hard")
        self.assertFalse(
            audit["shallow_retrieval"],
            "forced_causal_chains must prevent shallow_retrieval=True",
        )

    def test_multiple_chains_not_shallow(self) -> None:
        """Multiple injected chains must also suppress shallow_retrieval."""
        package = {
            "retrieved_context": [_minimal_chunk()],
            "forced_causal_chains": [
                {"id": "CC_TANNIN_STRUCTURE", "steps": []},
                {"id": "CC_SAT_QUALITY_HIGH", "steps": []},
            ],
        }
        audit = _audit_retrieval(package, "brutal")
        self.assertFalse(audit["shallow_retrieval"])

    def test_chains_none_treated_as_empty(self) -> None:
        """forced_causal_chains=None must not raise and must not add priority signal."""
        package = {
            "retrieved_context": [_minimal_chunk(), _minimal_chunk(), _minimal_chunk()],
            "forced_causal_chains": None,
        }
        audit = _audit_retrieval(package, "hard")
        # No chains → same as no high-priority → shallow
        self.assertTrue(audit["shallow_retrieval"])


if __name__ == "__main__":
    unittest.main()
