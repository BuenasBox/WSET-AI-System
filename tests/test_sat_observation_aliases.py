import json
import unittest
from pathlib import Path


ALIAS_PATH = Path(__file__).resolve().parents[1] / "knowledge" / "config" / "sat_observation_aliases.json"
EXPECTED_PARAMETERS = {
    "acidity",
    "tannin",
    "sweetness",
    "body",
    "finish",
    "intensity",
    "complexity",
    "balance",
    "condition",
    "development",
}


def _load_aliases() -> dict:
    return json.loads(ALIAS_PATH.read_text(encoding="utf-8"))


def _resolve(alias_table: dict, alias: str, language_key: str) -> set[tuple[str, str]]:
    matches = set()
    needle = alias.casefold()
    for parameter, config in alias_table["parameters"].items():
        for level, aliases in config[language_key].items():
            if needle in {item.casefold() for item in aliases}:
                matches.add((parameter, level))
    return matches


class SatObservationAliasesTests(unittest.TestCase):
    def test_alias_file_exists_and_has_safe_schema(self) -> None:
        self.assertTrue(ALIAS_PATH.exists())
        data = _load_aliases()
        self.assertEqual(data["schema_version"], "sat_aliases_v1")
        self.assertIs(data["safe_for_examiner"], False)
        self.assertIs(data["examiner_scoring_allowed"], False)
        self.assertEqual(set(data["parameters"]), EXPECTED_PARAMETERS)

    def test_each_parameter_has_levels_and_non_empty_alias_lists(self) -> None:
        data = _load_aliases()
        for parameter, config in data["parameters"].items():
            with self.subTest(parameter=parameter):
                self.assertIsInstance(config["levels"], list)
                self.assertTrue(config["levels"])
                self.assertIsInstance(config["aliases_es"], dict)
                self.assertIsInstance(config["aliases_en"], dict)
                self.assertEqual(set(config["aliases_es"]), set(config["levels"]))
                self.assertEqual(set(config["aliases_en"]), set(config["levels"]))
                for aliases in list(config["aliases_es"].values()) + list(config["aliases_en"].values()):
                    self.assertIsInstance(aliases, list)
                    self.assertTrue(aliases)

    def test_common_spanish_aliases_resolve_to_expected_parameter_and_level(self) -> None:
        data = _load_aliases()
        expected = {
            "acidez alta": ("acidity", "high"),
            "tanino alto": ("tannin", "high"),
            "cuerpo medio": ("body", "medium"),
            "final largo": ("finish", "long"),
            "intensidad pronunciada": ("intensity", "pronounced"),
            "complejidad alta": ("complexity", "high"),
            "equilibrado": ("balance", "balanced"),
            "limpio": ("condition", "clean"),
            "defectuoso": ("condition", "faulty"),
            "joven": ("development", "youthful"),
            "desarrollado": ("development", "fully developed"),
        }
        for alias, match in expected.items():
            with self.subTest(alias=alias):
                self.assertIn(match, _resolve(data, alias, "aliases_es"))

    def test_common_english_aliases_resolve_to_expected_parameter_and_level(self) -> None:
        data = _load_aliases()
        expected = {
            "high acidity": ("acidity", "high"),
            "high tannin": ("tannin", "high"),
            "medium body": ("body", "medium"),
            "long finish": ("finish", "long"),
            "pronounced intensity": ("intensity", "pronounced"),
            "high complexity": ("complexity", "high"),
            "balanced": ("balance", "balanced"),
            "clean": ("condition", "clean"),
            "faulty": ("condition", "faulty"),
            "youthful": ("development", "youthful"),
            "developed": ("development", "fully developed"),
        }
        for alias, match in expected.items():
            with self.subTest(alias=alias):
                self.assertIn(match, _resolve(data, alias, "aliases_en"))


if __name__ == "__main__":
    unittest.main()
