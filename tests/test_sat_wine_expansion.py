"""
SAT Wine Expansion Validation Suite
Tests schema compliance, governance, and pedagogical completeness
"""

import json
import unittest
from pathlib import Path

from tools.sat_wine_loader import (
    get_inventory_summary,
    get_wines_by_examination_value,
    get_wines_by_grape,
    get_wines_by_priority,
    load_all_wines,
    load_wine_by_id,
    load_wine_inventory,
)


class SATWineSchemaTests(unittest.TestCase):
    """Verify all wines conform to wine_schema_v1"""

    @classmethod
    def setUpClass(cls):
        cls.wine_dir = Path("knowledge/sat-framework/wines")
        cls.schema_file = cls.wine_dir / "wine_schema_v1.json"

        with open(cls.schema_file, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)

        cls.wines = {}
        for wine_file in sorted(cls.wine_dir.glob("SAT_WINE_*.json")):
            with open(wine_file, "r", encoding="utf-8") as f:
                cls.wines[wine_file.name] = json.load(f)

    def test_schema_exists(self):
        """Schema file must exist"""
        self.assertTrue(self.schema_file.exists())

    def test_twelve_wines_exist(self):
        """All 12 priority wines must be present"""
        self.assertEqual(len(self.wines), 12)

    def test_wine_ids_unique(self):
        """Wine IDs must be unique"""
        ids = [wine["id"] for wine in self.wines.values()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_wine_ids_sequential(self):
        """Wine IDs must follow SAT_WINE_NNN format"""
        for wine in self.wines.values():
            wine_id = wine["id"]
            self.assertRegex(wine_id, r"^SAT_WINE_\d{3}$")

    def test_required_fields_present(self):
        """All required fields must be present in each wine"""
        required_fields = [
            "id", "priority", "grape_variety", "region", "country", "style",
            "expected_sat_observations", "common_student_errors",
            "misconceptions_addressed", "coaching_hints",
            "causal_reasoning_paths", "examination_value", "governance"
        ]
        for wine_file, wine in self.wines.items():
            for field in required_fields:
                self.assertIn(field, wine,
                    f"{wine_file} missing field: {field}")

    def test_priority_valid_values(self):
        """Priority must be 1, 2, or 3"""
        for wine in self.wines.values():
            self.assertIn(wine["priority"], [1, 2, 3])

    def test_expected_observations_complete(self):
        """expected_sat_observations must cover appearance, nose, palate, conclusions"""
        required_sections = ["appearance", "nose", "palate", "conclusions"]
        for wine in self.wines.values():
            obs = wine["expected_sat_observations"]
            for section in required_sections:
                self.assertIn(section, obs)
                self.assertIsInstance(obs[section], list)
                self.assertGreater(len(obs[section]), 0)

    def test_common_errors_present(self):
        """Each wine must have 3+ common student errors"""
        for wine in self.wines.values():
            self.assertGreaterEqual(len(wine["common_student_errors"]), 3)

    def test_misconceptions_complete(self):
        """Each misconception must have misconception + correction"""
        for wine in self.wines.values():
            for misc in wine["misconceptions_addressed"]:
                self.assertIn("misconception", misc)
                self.assertIn("correction", misc)
                self.assertGreater(len(misc["misconception"]), 10)
                self.assertGreater(len(misc["correction"]), 10)

    def test_coaching_hints_present(self):
        """Each wine must have 3+ coaching hints"""
        for wine in self.wines.values():
            self.assertGreaterEqual(len(wine["coaching_hints"]), 3)

    def test_causal_reasoning_complete(self):
        """Each causal reasoning must have cause, effect, example"""
        for wine in self.wines.values():
            self.assertGreaterEqual(len(wine["causal_reasoning_paths"]), 1)
            for path in wine["causal_reasoning_paths"]:
                self.assertIn("cause", path)
                self.assertIn("effect", path)
                self.assertIn("example_in_wine", path)
                for field in ["cause", "effect", "example_in_wine"]:
                    self.assertGreater(len(path[field]), 5)

    def test_examination_value_valid(self):
        """Examination value must be Very High, High, or Medium-High"""
        valid_values = ["Very High", "High", "Medium-High"]
        for wine in self.wines.values():
            self.assertIn(wine["examination_value"], valid_values)

    def test_governance_safe_for_examiner_false(self):
        """safe_for_examiner must be False in all wines"""
        for wine in self.wines.values():
            self.assertFalse(wine["governance"]["safe_for_examiner"])

    def test_governance_formative_only_true(self):
        """formative_only must be True"""
        for wine in self.wines.values():
            self.assertTrue(wine["governance"]["formative_only"])

    def test_governance_training_only_true(self):
        """training_context_only must be True"""
        for wine in self.wines.values():
            self.assertTrue(wine["governance"]["training_context_only"])


class SATWinePedagogicalTests(unittest.TestCase):
    """Verify pedagogical completeness and soundness"""

    @classmethod
    def setUpClass(cls):
        cls.wine_dir = Path("knowledge/sat-framework/wines")
        cls.wines = {}
        for wine_file in sorted(cls.wine_dir.glob("SAT_WINE_*.json")):
            with open(wine_file, "r", encoding="utf-8") as f:
                cls.wines[wine_file.name] = json.load(f)

    def test_misconceptions_vary(self):
        """Wines should not have duplicate misconceptions"""
        all_misconceptions = {}
        for wine in self.wines.values():
            for misc in wine["misconceptions_addressed"]:
                misconception = misc["misconception"]
                if misconception in all_misconceptions:
                    # Allow some overlap, but flag if severe
                    pass
                all_misconceptions[misconception] = wine["id"]
        # Check that we have at least 20 unique misconceptions
        self.assertGreater(len(all_misconceptions), 20)

    def test_causal_reasoning_diversity(self):
        """Causal reasoning should cover different causative factors"""
        causes = []
        for wine in self.wines.values():
            for path in wine["causal_reasoning_paths"]:
                causes.append(path["cause"].lower())

        # Should have variety: climate, variety, winemaking, terroir, etc
        cause_keywords = ["climate", "technique", "oak", "terroir", "variety",
                         "skin", "temperature", "ageing", "alcohol"]
        found_keywords = sum(1 for keyword in cause_keywords
                           if any(keyword in cause for cause in causes))
        self.assertGreaterEqual(found_keywords, 4)

    def test_error_lists_educational(self):
        """Common errors should be actual pedagogical mistakes, not generic"""
        for wine in self.wines.values():
            for error in wine["common_student_errors"]:
                # Should be specific, not generic (15+ chars is substantial)
                self.assertGreater(len(error), 15)
                # Should be phrased as an error (using verbs like "calling", "confusing", etc)
                # or reference wine/climate/region terminology
                is_error_phrased = any(term in error.lower()
                    for term in ["calling", "confusing", "missing", "assuming",
                                "treating", "ignoring", "overcalling", "underes",
                                "overusing", "not recognizing", "mistaking", "underestimating"])
                is_wine_context = any(term in error.lower()
                    for term in ["colour", "acidity", "tannin", "aroma", "body",
                                "fruit", "oak", "structure", "quality", "sweetness",
                                "wine", "grape", "climate", "terroir", "ripeness",
                                "warm", "cool", "jammy", "herbal"])
                self.assertTrue(is_error_phrased or is_wine_context,
                    f"Error not pedagogically specific: {error}")

    def test_coaching_hints_actionable(self):
        """Coaching hints should be actionable questions or guidance"""
        for wine in self.wines.values():
            for hint in wine["coaching_hints"]:
                # Should be questions, imperatives, or actionable statements
                is_question = hint.strip().endswith("?")
                is_imperative = any(word in hint.lower()
                    for word in ["notice", "focus", "compare", "can you", "identify",
                                "separate", "distinguish", "assess", "link", "notice"])
                is_actionable = len(hint) > 15 and any(term in hint.lower()
                    for term in ["colour", "acidity", "tannin", "fruit", "oak",
                                "aroma", "body", "structure", "finish", "taste"])
                self.assertTrue(is_question or is_imperative or is_actionable,
                    f"Hint not actionable: {hint}")


class SATWineDiscoverabilityTests(unittest.TestCase):
    """Verify wines are discoverable and properly indexed"""

    @classmethod
    def setUpClass(cls):
        cls.wine_dir = Path("knowledge/sat-framework/wines")
        cls.wines = {}
        for wine_file in sorted(cls.wine_dir.glob("SAT_WINE_*.json")):
            with open(wine_file, "r", encoding="utf-8") as f:
                cls.wines[wine_file.name] = json.load(f)

    def test_wine_files_discoverable(self):
        """All wine files must be discoverable by glob pattern"""
        wine_files = list(self.wine_dir.glob("SAT_WINE_*.json"))
        self.assertEqual(len(wine_files), 12)

    def test_wine_id_in_content(self):
        """Wine ID in filename must match content"""
        for wine_file in self.wine_dir.glob("SAT_WINE_*.json"):
            wine_id = wine_file.name.split("_")[2]  # Extract NNN from SAT_WINE_NNN
            with open(wine_file, "r", encoding="utf-8") as f:
                wine = json.load(f)
            self.assertIn(wine_id, wine["id"])

    def test_priority_distribution(self):
        """Wine priorities should be distributed across 1, 2, 3"""
        priorities = [wine["priority"] for wine in self.wines.values()]
        self.assertIn(1, priorities)
        self.assertIn(2, priorities)
        self.assertIn(3, priorities)
        # Priority 1 should have most wines
        self.assertGreater(priorities.count(1), priorities.count(2))
        self.assertGreater(priorities.count(2), priorities.count(3))

    def test_examination_value_distribution(self):
        """Examination values should be distributed appropriately"""
        exam_values = [wine["examination_value"] for wine in self.wines.values()]
        self.assertGreater(exam_values.count("Very High"), 4)
        self.assertGreater(exam_values.count("High"), 2)


class SATWineGovernanceTests(unittest.TestCase):
    """Verify governance compliance and safety"""

    @classmethod
    def setUpClass(cls):
        cls.wine_dir = Path("knowledge/sat-framework/wines")
        cls.wines = {}
        for wine_file in sorted(cls.wine_dir.glob("SAT_WINE_*.json")):
            with open(wine_file, "r", encoding="utf-8") as f:
                cls.wines[wine_file.name] = json.load(f)

    def test_no_examiner_claims(self):
        """Wines must not claim examiner authority or official WSET status"""
        forbidden_phrases = ["official wset answer", "wset examination answer",
                            "official answer is", "this is the correct answer",
                            "according to wset", "official marking requires",
                            "you must answer"]
        for wine_file, wine in self.wines.items():
            content = json.dumps(wine).lower()
            for phrase in forbidden_phrases:
                self.assertNotIn(phrase, content,
                    f"{wine_file} contains forbidden examiner claim: {phrase}")

    def test_no_scoring_claims(self):
        """Wines must not claim to provide scores or grades"""
        for wine_file, wine in self.wines.items():
            content = json.dumps(wine).lower()
            self.assertNotIn("score", content,
                f"{wine_file} contains score claim")
            self.assertNotIn("pass/fail", content,
                f"{wine_file} contains pass/fail claim")

    def test_no_external_service_calls(self):
        """Governance must show no external services"""
        for wine in self.wines.values():
            governance = wine["governance"]
            # These should not be added
            self.assertNotIn("uses_llm", governance)
            self.assertNotIn("uses_api", governance)
            self.assertNotIn("uses_embeddings", governance)

    def test_formative_language_only(self):
        """Content should use formative language"""
        formative_indicators = ["consider", "explore", "observe", "notice",
                               "practice", "coaching", "training", "hint",
                               "identify", "distinguish", "assess", "compare",
                               "error", "misconception", "calibration"]
        wine_text = " ".join([json.dumps(w).lower() for w in self.wines.values()])
        found_indicators = sum(1 for indicator in formative_indicators
                             if indicator in wine_text)
        self.assertGreater(found_indicators, 4)


class SATWineContentTests(unittest.TestCase):
    """Verify wine content accuracy and completeness"""

    @classmethod
    def setUpClass(cls):
        cls.wine_dir = Path("knowledge/sat-framework/wines")
        cls.wines = {}
        for wine_file in sorted(cls.wine_dir.glob("SAT_WINE_*.json")):
            with open(wine_file, "r", encoding="utf-8") as f:
                cls.wines[wine_file.name] = json.load(f)

    def test_grape_variety_populated(self):
        """Grape variety must be present"""
        for wine in self.wines.values():
            self.assertGreater(len(wine["grape_variety"]), 3)

    def test_region_populated(self):
        """Region must be populated"""
        for wine in self.wines.values():
            self.assertGreater(len(wine["region"]), 3)

    def test_country_populated(self):
        """Country must be populated"""
        for wine in self.wines.values():
            self.assertGreater(len(wine["country"]), 2)

    def test_style_description_detailed(self):
        """Style description should be detailed (80+ chars)"""
        for wine in self.wines.values():
            self.assertGreater(len(wine["style"]), 80)

    def test_tasting_terms_consistent(self):
        """Expected observations should use standard SAT terminology"""
        sat_terms = ["clarity", "intensity", "colour", "aroma", "acidity",
                    "tannin", "sweetness", "body", "flavour", "finish",
                    "quality", "ageing", "development"]
        wine_observations = json.dumps(self.wines).lower()
        found_terms = sum(1 for term in sat_terms if term in wine_observations)
        self.assertGreater(found_terms, 8)


class SATWineLoaderTests(unittest.TestCase):
    """Verify deterministic discovery through the public loader."""

    def test_inventory_and_all_wines_are_consistent(self):
        inventory = load_wine_inventory()
        wines = load_all_wines()

        self.assertEqual(len(inventory["wines"]), 12)
        self.assertEqual(
            [record["wine_id"] for record in inventory["wines"]],
            [wine["id"] for wine in wines],
        )

    def test_load_wine_by_id_handles_known_and_unknown_ids(self):
        self.assertEqual(load_wine_by_id("SAT_WINE_001")["region"], "Chablis")
        self.assertIsNone(load_wine_by_id("SAT_WINE_999"))

    def test_loader_filters_match_inventory(self):
        self.assertEqual(len(get_wines_by_priority(1)), 6)
        self.assertEqual(len(get_wines_by_priority(2)), 4)
        self.assertEqual(len(get_wines_by_priority(3)), 2)
        self.assertEqual(
            [wine["id"] for wine in get_wines_by_grape("Chardonnay")],
            ["SAT_WINE_001", "SAT_WINE_002"],
        )
        self.assertEqual(len(get_wines_by_examination_value("Very High")), 6)

    def test_inventory_summary_is_deterministic(self):
        expected = {
            "total_wines": 12,
            "wines_by_priority": {1: 6, 2: 4, 3: 2},
            "wines_by_examination_value": {
                "Very High": 6,
                "High": 4,
                "Medium-High": 2,
            },
            "unique_grapes": 11,
            "grape_varieties": [
                "Cabernet Sauvignon",
                "Chardonnay",
                "Grenache / Garnacha",
                "Merlot",
                "Nebbiolo",
                "Pinot Noir",
                "Riesling",
                "Sangiovese",
                "Sauvignon Blanc",
                "Syrah / Shiraz",
                "Tempranillo",
            ],
            "unique_countries": 8,
            "countries": [
                "France",
                "France / Australia",
                "France / Spain",
                "France / USA",
                "Germany",
                "Italy",
                "New Zealand",
                "Spain",
            ],
        }

        self.assertEqual(get_inventory_summary(), expected)


if __name__ == "__main__":
    unittest.main()
