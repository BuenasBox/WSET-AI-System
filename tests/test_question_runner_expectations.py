import unittest

from tools.self_eval.question_runner import _infer_expectations, _sample_questions


class QuestionRunnerExpectationsTests(unittest.TestCase):
    def test_sample_questions_produce_non_empty_expectations(self) -> None:
        questions = _sample_questions()

        self.assertEqual(len(questions), 5)
        for question in questions:
            with self.subTest(question_id=question["question_id"]):
                expectations = _infer_expectations(question["question_text"])
                self.assertTrue(expectations["expected_topics"])
                self.assertTrue(expectations["expected_keywords"])
                self.assertTrue(expectations["expected_causal_links"])


if __name__ == "__main__":
    unittest.main()
