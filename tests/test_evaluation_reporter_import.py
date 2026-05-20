import unittest

import tools.self_eval.evaluation_reporter as evaluation_reporter


class EvaluationReporterImportTests(unittest.TestCase):
    def test_les_reconciler_import_is_explicit_and_available(self) -> None:
        self.assertTrue(callable(evaluation_reporter.reconcile_les_from_feedback))


if __name__ == "__main__":
    unittest.main()
