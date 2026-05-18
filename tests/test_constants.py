import unittest
from pathlib import Path

from tools import constants


class ConstantsTests(unittest.TestCase):
    def test_path_and_governance_constants_are_safe(self) -> None:
        self.assertIsInstance(constants.PROJECT_ROOT, Path)
        self.assertEqual(constants.PROJECT_ROOT, Path(__file__).resolve().parents[1])

        for name in (
            "KNOWLEDGE_DIR",
            "OFFICIAL_WSET_DIR",
            "SELF_EVAL_DIR",
            "RETRIEVAL_SANDBOX_DIR",
            "NAZARETH_DIR",
            "CONTEXT_PACKAGES_DIR",
        ):
            self.assertIsInstance(getattr(constants, name), Path)

        self.assertIs(constants.SAFE_FOR_EXAMINER, False)
        self.assertIs(constants.EXAMINER_SCORING_ALLOWED, False)
        self.assertIs(constants.USES_LLM, False)
        self.assertIs(constants.USES_API, False)
        self.assertIs(constants.USES_EMBEDDINGS, False)
        self.assertIs(constants.USES_VECTOR_DB, False)
        self.assertIs(constants.CLOUD_SERVICES_ACTIVE, False)

        for name in dir(constants):
            if name.isupper():
                self.assertIsNot(getattr(constants, name), True, name)


if __name__ == "__main__":
    unittest.main()
