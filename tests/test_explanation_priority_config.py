import json
import unittest

from tools.constants import KNOWLEDGE_DIR
from tools.tutor import answer_builder
from tools.tutor.explanation_priority import DEPTH_TO_STYLE, SEVERITY_WEIGHT


class ExplanationPriorityConfigTests(unittest.TestCase):
    def test_config_has_expected_keys_and_rationales(self) -> None:
        path = KNOWLEDGE_DIR / "config" / "explanation_priority_config.json"
        config = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(set(config["SEVERITY_WEIGHT"]), {"low", "medium", "high", "critical"})
        self.assertEqual(set(config["DEPTH_TO_STYLE"]), {"minimal", "standard", "deep"})
        for section in ("SEVERITY_WEIGHT", "DEPTH_TO_STYLE"):
            for value in config[section].values():
                self.assertIn("rationale", value)
                self.assertTrue(value["rationale"])

    def test_public_exports_remain_available_for_answer_builder(self) -> None:
        self.assertEqual(DEPTH_TO_STYLE["standard"], "standard")
        self.assertEqual(SEVERITY_WEIGHT["medium"], 0.45)
        self.assertIs(answer_builder.DEPTH_TO_STYLE, DEPTH_TO_STYLE)


if __name__ == "__main__":
    unittest.main()
