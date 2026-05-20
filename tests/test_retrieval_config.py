import json
import re
import unittest

from tools.constants import KNOWLEDGE_DIR
from tools.retrieval import tutor_retrieval_sandbox as retrieval


class RetrievalConfigTests(unittest.TestCase):
    def test_score_weight_keys_referenced_in_code_exist_in_json(self) -> None:
        path = KNOWLEDGE_DIR / "config" / "retrieval_config.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        source = (
            retrieval.PROJECT_ROOT
            / "tools"
            / "retrieval"
            / "tutor_retrieval_sandbox.py"
        ).read_text(encoding="utf-8")
        referenced = set(re.findall(r'SCORE_WEIGHTS\["([^"]+)"\]', source))

        self.assertTrue(referenced)
        self.assertLessEqual(referenced, set(config["SCORE_WEIGHTS"]))

    def test_priority_boosts_load_with_current_values_and_notes(self) -> None:
        path = KNOWLEDGE_DIR / "config" / "retrieval_config.json"
        config = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(retrieval.PRIORITY_BOOSTS, {"high": 0.12, "medium": 0.06, "low": 0.02})
        for value in config["PRIORITY_BOOSTS"].values():
            self.assertIn("calibration_notes", value)
            self.assertIsInstance(value["calibration_notes"], str)
            self.assertTrue(value["calibration_notes"])


if __name__ == "__main__":
    unittest.main()
