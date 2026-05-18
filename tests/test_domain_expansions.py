import importlib
import json
import unittest

from tools.constants import KNOWLEDGE_DIR


class DomainExpansionsConfigTests(unittest.TestCase):
    def test_domain_expansions_load_from_required_json_config(self) -> None:
        config_path = KNOWLEDGE_DIR / "config" / "domain_expansions.json"
        self.assertTrue(config_path.exists())

        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertTrue(config)
        self.assertEqual(
            config["SAT_EXPANSIONS"]["sat"],
            [
                "balance",
                "intensity",
                "complexity",
                "length",
                "readiness",
                "quality assessment",
                "bicL",
                "appearance",
                "nose",
                "palate",
            ],
        )
        self.assertEqual(
            config["DOMAIN_EXPANSIONS"]["tokaji"],
            [
                "tokaji",
                "tokay",
                "aszú",
                "aszu",
                "botrytis",
                "noble rot",
                "putonyos",
                "sweet wine",
                "hungary",
                "concentrated",
                "furmint",
            ],
        )

        import tools.retrieval.tutor_retrieval_sandbox as sandbox

        self.assertEqual(sandbox.DOMAIN_EXPANSIONS, config["DOMAIN_EXPANSIONS"])

        temporary_path = config_path.with_suffix(".json.tmp")
        config_path.rename(temporary_path)
        try:
            with self.assertRaises(FileNotFoundError):
                importlib.reload(sandbox)
        finally:
            temporary_path.rename(config_path)
            importlib.reload(sandbox)


if __name__ == "__main__":
    unittest.main()
