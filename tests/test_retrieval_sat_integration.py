import inspect
import unittest
from unittest.mock import patch

from tools.retrieval import tutor_retrieval_sandbox as retrieval


EMPTY_KNOWLEDGE = {
    "concepts": [],
    "causal_chains": [],
    "relationships": [],
    "misconceptions": [],
}
EXPECTED_CLASSIFY_KEYS = {
    "query_intent",
    "reasoning_intent",
    "matched_terms",
    "matched_concepts",
    "matched_causal_chains",
    "matched_relationships",
    "matched_misconceptions",
    "query_expansion_terms",
    "query_tokens",
    "expanded_query_tokens",
}


class RetrievalSatIntegrationTests(unittest.TestCase):
    def test_spanish_sat_observation_query_adds_parameter_tokens(self) -> None:
        result = retrieval.classify_query(
            "el vino tiene acidez alta, tanino alto y final largo",
            dictionary_terms=[],
            knowledge_nodes=[],
        )
        expanded = set(result["expanded_query_tokens"])
        self.assertIn("acidity", expanded)
        self.assertIn("tannin", expanded)
        self.assertIn("finish", expanded)

    def test_english_sat_observation_query_adds_parameter_tokens(self) -> None:
        result = retrieval.classify_query(
            "the wine shows high acidity, high tannin and long finish",
            dictionary_terms=[],
            knowledge_nodes=[],
        )
        expanded = set(result["expanded_query_tokens"])
        self.assertIn("acidity", expanded)
        self.assertIn("tannin", expanded)
        self.assertIn("finish", expanded)

    def test_non_sat_theory_query_does_not_add_unmentioned_sat_parameters(self) -> None:
        result = retrieval.classify_query(
            "How does cool climate affect acidity?",
            dictionary_terms=[],
            knowledge_nodes=[],
        )
        expanded = set(result["expanded_query_tokens"])
        self.assertNotIn("tannin", expanded)
        self.assertNotIn("finish", expanded)

    def test_sat_observation_expansion_is_deterministic(self) -> None:
        query = "the wine shows high acidity, high tannin and long finish"
        first = retrieval.classify_query(query, dictionary_terms=[], knowledge_nodes=[])
        second = retrieval.classify_query(query, dictionary_terms=[], knowledge_nodes=[])
        self.assertEqual(first["expanded_query_tokens"], second["expanded_query_tokens"])

    def test_classify_query_signature_and_return_shape_are_unchanged(self) -> None:
        signature = inspect.signature(retrieval.classify_query)
        self.assertEqual(list(signature.parameters), ["query", "dictionary_terms", "knowledge_nodes"])
        result = retrieval.classify_query(
            "the wine shows high acidity, high tannin and long finish",
            dictionary_terms=[],
            knowledge_nodes=[],
        )
        self.assertEqual(set(result), EXPECTED_CLASSIFY_KEYS)

    def test_sat_reasoner_unavailable_preserves_baseline_expansion(self) -> None:
        query = "the wine shows high acidity, high tannin and long finish"
        expected_expansion = retrieval.expand_query_terms(query, [], EMPTY_KNOWLEDGE)
        with patch.object(retrieval, "_SAT_REASONER_AVAILABLE", False):
            result = retrieval.classify_query(query, dictionary_terms=[], knowledge_nodes=[])
        self.assertEqual(result["query_expansion_terms"], expected_expansion)

    def test_governance_flags_are_not_set_true_in_retrieval_sandbox_source(self) -> None:
        source = inspect.getsource(retrieval).casefold()
        self.assertNotIn("safe_for_examiner = true", source)
        self.assertNotIn("safe_for_examiner\": true", source)
        self.assertNotIn("examiner_scoring_allowed = true", source)
        self.assertNotIn("examiner_scoring_allowed\": true", source)


if __name__ == "__main__":
    unittest.main()
