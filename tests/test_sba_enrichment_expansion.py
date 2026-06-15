"""Precision contracts for post-Batch-3 SBA enrichment expansion."""

from __future__ import annotations

import unittest

from tools.question_generation.sba_enrichment_deriver import (
    BATCH_SIZE,
    MIN_KEYWORD_HITS,
    NODE_ES,
    REQUIRE_CORRECT_OPTION_HIT,
    REQUIRE_STEM_HIT,
    REQUIRE_UNIQUE_BEST,
    derive,
    load_chain_nodes,
)


MLF_NODE_IDS = {
    "HC_MLF_ACID_CONVERSION",
    "HC_MLF_BLOCKING_FRESHNESS",
    "HC_MLF_MICROBIAL_STABILITY",
    "HC_MLF_STYLE_CONTROL",
}

LEES_NODE_IDS = {
    "HC_BARREL_LEES_WHITE_BODY",
    "HC_BATONNAGE_TEXTURE_COMPLEXITY",
    "HC_SPARKLING_AUTOLYTIC_AROMAS",
    "HC_SPARKLING_LEES_TEXTURE",
    "HC_WHITE_LEES_TEXTURE_COMPLEXITY",
}

BOTTLE_AGEING_NODE_IDS = {
    "HC_BAROLO_TERTIARY_EVOLUTION",
    "HC_BOTTLE_STORAGE_STABILITY",
    "HC_BOTTLE_TANNIN_SOFTENING",
    "HC_HEAT_PREMATURE_BOTTLE_AGEING",
    "HC_MAGNUM_SLOW_AGEING",
    "HC_OLD_RED_SEDIMENT_SERVICE",
    "HC_RED_WINE_AGEABILITY_STRUCTURE",
}

SPARKLING_NODE_IDS = {
    "HC_ANCESTRAL_SINGLE_FERMENTATION",
    "HC_BASE_WINE_OXIDATION_DAMAGE",
    "HC_BRUT_NATURE_NO_DOSAGE",
    "HC_DISGORGEMENT_SEDIMENT_REMOVAL",
    "HC_LIQUEUR_TIRAGE_SECOND_FERMENTATION",
    "HC_PRESSURE_MOUSSE_INTENSITY",
    "HC_RIDDLING_SEDIMENT_COLLECTION",
    "HC_TANK_METHOD_FRUIT_RETENTION",
    "HC_TRADITIONAL_BOTTLE_SECOND_FERMENTATION",
}

VITICULTURE_HAZARD_NODE_IDS = {
    "HC_CANOPY_AIRFLOW_FUNGAL_RISK",
    "HC_CANOPY_SHADE_HEAT_PROTECTION",
    "HC_COVER_CROPS_EROSION_CONTROL",
    "HC_DRIP_IRRIGATION_PRECISION",
    "HC_EARLY_GROWTH_FROST_EXPOSURE",
    "HC_EXCESS_NITROGEN_DISEASE_RISK",
    "HC_FLOWERING_RAIN_FRUIT_SET",
    "HC_FROST_SHOOT_YIELD_DAMAGE",
    "HC_FROST_SLOPE_AIR_DRAINAGE",
    "HC_LATE_HARVEST_FROST_EXPOSURE",
    "HC_PHYLLOXERA_RESISTANT_ROOTSTOCK",
}

CELLAR_CONTROL_NODE_IDS = {
    "HC_CELLAR_HYGIENE_MICROBIAL_CONTROL",
    "HC_COLD_TARTRATE_STABILIZATION",
    "HC_CONCRETE_THERMAL_INERTIA",
    "HC_COOL_FERMENTATION_AROMA_RETENTION",
    "HC_PREBOTTLING_FILTRATION_CLARITY",
    "HC_RED_FERMENTATION_EXTRACTION",
    "HC_STERILE_FILTRATION_MICROBIAL_STABILITY",
}

HARVEST_SITE_NODE_IDS = {
    "HC_EARLY_HARVEST_FRESHNESS_ALCOHOL",
    "HC_NIGHT_HARVEST_FRESHNESS",
    "HC_SELECTIVE_HAND_HARVEST_QUALITY",
    "HC_SOUTH_FACING_EXPOSURE_RIPENESS",
}

OAK_OXYGEN_NODE_IDS = {
    "HC_BARREL_SIZE_OAK_CONTACT",
    "HC_FREQUENT_RACKING_OXYGEN",
    "HC_NEW_OAK_STRUCTURE_SPICE",
    "HC_OXIDATIVE_AGEING_TERTIARY",
    "HC_USED_OAK_OXYGEN_LOW_FLAVOUR",
}

VINEYARD_MECHANISM_NODE_IDS = {
    "HC_ALTITUDE_SLOW_RIPENING_FRESHNESS",
    "HC_DESTEMMING_GREEN_TANNIN_REDUCTION",
    "HC_HUMID_HARVEST_DILUTION",
    "HC_MODERATE_WATER_STRESS_PHENOLICS",
    "HC_SANDY_SOIL_DRAINAGE",
}

SENSORY_PAIRING_NODE_IDS = {
    "HC_ALCOHOL_CHILI_HEAT",
    "HC_FOOD_SWEETNESS_WINE_CONTRAST",
    "HC_LOW_SERVICE_TEMPERATURE_TANNIN_AROMA",
    "HC_PROTEIN_FAT_TANNIN_SOFTENING",
    "HC_SALT_TANNIN_BALANCE",
    "HC_UMAMI_BITTER_ACID_PERCEPTION",
}

FAULT_STABILITY_NODE_IDS = {
    "HC_BENTONITE_PROTEIN_STABILITY",
    "HC_BRETTANOMYCES_ANIMAL_ODOR",
    "HC_EXCESSIVE_WHITE_OXIDATION",
    "HC_HEAT_TRANSPORT_WINE_DAMAGE",
    "HC_MUST_CHILLING_FERMENTATION_CONTROL",
    "HC_OPEN_BOTTLE_OXYGEN_CONTROL",
    "HC_PERFUMED_DETERGENT_GLASS_CONTAMINATION",
    "HC_PRESSING_OXIDATION_RISK",
    "HC_RACKING_OXYGEN_SEDIMENT",
    "HC_REDUCTION_SULFUR_ODORS",
    "HC_REFERMENTATION_UNEXPECTED_BUBBLES",
    "HC_SO2_OXIDATION_PROTECTION",
    "HC_TCA_MUSTY_CARDBOARD",
    "HC_VOLATILE_ACIDITY_VINEGAR_SOLVENT",
}

STYLE_MECHANISM_NODE_IDS = {
    "HC_ALTITUDE_GRAPE_ACIDITY",
    "HC_CANOPY_VIGOUR_EXPOSURE",
    "HC_CARBONIC_MACERATION_FRUIT_LOW_TANNIN",
    "HC_COOL_SPARKLING_BASE_ACIDITY",
    "HC_FORTIFICATION_STOPS_FERMENTATION",
    "HC_HUMBOLDT_CURRENT_FRESHNESS",
    "HC_LOW_VIGOUR_ROOTSTOCK_CONTROL",
    "HC_SOLAR_EXPOSURE_RED_COLOR",
    "HC_WARM_CLIMATE_ACID_LOSS",
    "HC_WARM_DRY_OVERRIPENING",
}

FERMENTATION_CONTROL_NODE_IDS = {
    "HC_COOL_FERMENTATION_AROMA_RETENTION",
    "HC_HARVEST_COOLING_AROMA_PROTECTION",
    "HC_HIGH_FERMENTATION_TEMP_BURNT_AROMAS",
    "HC_NIGHT_HARVEST_FRESHNESS",
    "HC_SELECTED_YEAST_PREDICTABILITY",
    "HC_STAINLESS_PRIMARY_AROMA_PRESERVATION",
    "HC_STAINLESS_TEMPERATURE_CONTROL",
}

SOIL_PHYSICS_NODE_IDS = {
    "HC_CLAY_WATER_RETENTION",
    "HC_COVER_CROP_SOIL_STRUCTURE",
    "HC_SANDY_SOIL_DRAINAGE",
    "HC_WELL_DRAINED_ROOT_DEVELOPMENT",
}

STORAGE_SERVICE_NODE_IDS = {
    "HC_BOTTLE_STORAGE_STABILITY",
    "HC_ICE_WATER_RAPID_CHILLING",
}

SERVICE_MECHANICS_NODE_IDS = {
    "HC_AERATION_YOUNG_STRUCTURED_WINE",
    "HC_GENTLE_CARBONATED_WINE_SERVICE",
    "HC_LARGE_BOWL_AROMA_EXPRESSION",
    "HC_SAFE_SPARKLING_CORK_OPENING",
}

WINEMAKING_MECHANICS_NODE_IDS = {
    "HC_EXTRACTION_BODY_STRUCTURE",
    "HC_MUST_SETTLING_CLARIFICATION",
    "HC_NEW_OAK_TANNIN_WHITE_WINE",
    "HC_SHORT_MACERATION_LOW_COLOR",
}

COOL_CLIMATE_RIPENING_NODE_IDS = {
    "HC_COOL_CLIMATE_STYLE",
}

VINEYARD_MANAGEMENT_NODE_IDS = {
    "HC_CANOPY_VIGOUR_EXPOSURE",
    "HC_EARLY_HARVEST_FRESHNESS_ALCOHOL",
    "HC_SELECTIVE_HAND_HARVEST_QUALITY",
    "HC_YIELD_CONCENTRATION",
}

WINE_FAULT_CAUSATION_NODE_IDS = {
    "HC_REDUCTION_SULFUR_ODORS",
    "HC_TCA_MUSTY_CARDBOARD",
    "HC_VOLATILE_ACIDITY_VINEGAR_SOLVENT",
}

EXTRACTION_OXYGEN_INTERVENTION_NODE_IDS = {
    "CC_MECHANICAL_HARVEST_OXIDATION",
    "HC_MICROOXYGENATION_TANNIN_SOFTENING",
    "HC_RED_FERMENTATION_EXTRACTION",
}

UNDERRIPE_HARVEST_NODE_IDS = {
    "HC_UNDERRIPE_HARVEST_GREEN_AROMAS",
}

ALCOHOL_BITTERNESS_NODE_IDS = {
    "HC_ALCOHOL_BITTERNESS_PERCEPTION",
}

FLOR_BIOLOGICAL_AGEING_NODE_IDS = {
    "CC_FLOR_BIOLOGICAL_AGEING",
}

HUMBOLDT_COASTAL_COOLING_NODE_IDS = {
    "HC_HUMBOLDT_CURRENT_FRESHNESS",
}

AGEABILITY_STRUCTURE_NODE_IDS = {
    "HC_RED_WINE_AGEABILITY_STRUCTURE",
}

PRODUCTION_ECONOMICS_NODE_IDS = {
    "HC_COOPERATIVE_SHARED_RESOURCES",
    "HC_MECHANIZATION_PRODUCTION_COST",
}

WINE_BALANCE_NODE_IDS = {
    "HC_LOW_ACID_STRUCTURE_FLATNESS",
}

MARKET_ECONOMICS_NODE_IDS = {
    "HC_EXCLUSIVE_DISTRIBUTOR_MARKET_ACCESS",
    "HC_SCARCITY_DEMAND_PRICE_PRESSURE",
}

ALSACE_RIPENING_NODE_IDS = {
    "HC_ALSACE_SUN_DRY_RIPENING",
}

SO2_MICROBIAL_CONTROL_NODE_IDS = {
    "HC_SO2_MICROBIAL_INHIBITION",
}

MARITIME_MODERATION_NODE_IDS = {
    "HC_MARITIME_MODERATION",
}

CLONAL_SELECTION_NODE_IDS = {
    "HC_CLONAL_SELECTION_STYLE_INFLUENCE",
}

STEEP_SLOPE_SOLAR_RIPENING_NODE_IDS = {
    "HC_STEEP_SLOPE_SOLAR_RIPENING",
}

SHORT_CYCLE_VARIETY_NODE_IDS = {
    "HC_SHORT_CYCLE_VARIETY_COOL_SEASON_FIT",
}

LATE_HARVEST_RIPENESS_NODE_IDS = {
    "HC_LATE_HARVEST_RIPENESS_BODY",
}

OLOROSO_AMONTILLADO_PATH_NODE_IDS = {
    "HC_OLOROSO_AMONTILLADO_AGEING_PATH",
}

ACID_FOOD_WINE_BALANCE_NODE_IDS = {
    "HC_ACID_FOOD_HIGH_ACID_WINE_BALANCE",
}

SPICY_FOOD_WINE_PAIRING_NODE_IDS = {
    "HC_RESIDUAL_SUGAR_LOW_ALCOHOL_CHILI_PAIRING",
}


class FrozenMatcherContractTests(unittest.TestCase):
    def test_matcher_v2_controls_remain_frozen(self):
        self.assertEqual(MIN_KEYWORD_HITS, 2)
        self.assertIs(REQUIRE_STEM_HIT, True)
        self.assertIs(REQUIRE_CORRECT_OPTION_HIT, True)
        self.assertIs(REQUIRE_UNIQUE_BEST, True)

    def test_expansion_capacity_covers_the_full_sba_bank(self):
        self.assertEqual(BATCH_SIZE, 578)


class MlfExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_mlf_nodes_are_matcher_compatible_and_localized(self):
        for node_id in MLF_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_mlf_enrichment_assignments(self):
        expected = {
            "wset3_440": "HC_MLF_BLOCKING_FRESHNESS",
            "wset3_475": "HC_MLF_STYLE_CONTROL",
            "wset3_481": "HC_MLF_MICROBIAL_STABILITY",
            "wset3_704": "HC_MLF_ACID_CONVERSION",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"] in MLF_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_mlf_matches_have_stem_and_correct_answer_evidence(self):
        for item_id in ("wset3_440", "wset3_475", "wset3_481", "wset3_704"):
            provenance = self.records[item_id]["_provenance"]["causal_chain"]
            self.assertTrue(provenance["stem_hits"])
            self.assertTrue(provenance["correct_option_hits"])
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_weak_and_negative_mlf_items_remain_excluded(self):
        for item_id in ("wset3_515", "wset3_778"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    MLF_NODE_IDS,
                )


class LeesExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_lees_nodes_are_matcher_compatible_and_localized(self):
        for node_id in LEES_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_lees_enrichment_assignments(self):
        expected = {
            "wset3_30": "HC_SPARKLING_AUTOLYTIC_AROMAS",
            "wset3_127": "HC_SPARKLING_AUTOLYTIC_AROMAS",
            "wset3_128": "HC_SPARKLING_LEES_TEXTURE",
            "wset3_362": "HC_WHITE_LEES_TEXTURE_COMPLEXITY",
            "wset3_377": "HC_BATONNAGE_TEXTURE_COMPLEXITY",
            "wset3_432": "HC_BATONNAGE_TEXTURE_COMPLEXITY",
            "wset3_435": "HC_WHITE_LEES_TEXTURE_COMPLEXITY",
            "wset3_482": "HC_BARREL_LEES_WHITE_BODY",
            "wset3_491": "HC_WHITE_LEES_TEXTURE_COMPLEXITY",
            "wset3_500": "HC_WHITE_LEES_TEXTURE_COMPLEXITY",
            "wset3_703": "HC_BATONNAGE_TEXTURE_COMPLEXITY",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"] in LEES_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_lees_matches_have_stem_and_correct_answer_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in LEES_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_unsupported_and_negative_lees_items_remain_excluded(self):
        for item_id in ("wset3_520", "wset3_658", "wset3_776"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    LEES_NODE_IDS,
                )


class BottleAgeingExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_bottle_ageing_nodes_are_matcher_compatible_and_localized(self):
        for node_id in BOTTLE_AGEING_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_bottle_ageing_enrichment_assignments(self):
        expected = {
            "wset3_3": "HC_RED_WINE_AGEABILITY_STRUCTURE",
            "wset3_31": "HC_BOTTLE_TANNIN_SOFTENING",
            "wset3_41": "HC_OLD_RED_SEDIMENT_SERVICE",
            "wset3_59": "HC_OLD_RED_SEDIMENT_SERVICE",
            "wset3_50": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_53": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_78": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_83": "HC_RED_WINE_AGEABILITY_STRUCTURE",
            "wset3_81": "HC_HEAT_PREMATURE_BOTTLE_AGEING",
            "wset3_86": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_87": "HC_OLD_RED_SEDIMENT_SERVICE",
            "wset3_287": "HC_BAROLO_TERTIARY_EVOLUTION",
            "wset3_331": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_385": "HC_RED_WINE_AGEABILITY_STRUCTURE",
            "wset3_720": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_722": "HC_OLD_RED_SEDIMENT_SERVICE",
            "wset3_733": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_852": "HC_MAGNUM_SLOW_AGEING",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in BOTTLE_AGEING_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_bottle_ageing_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in BOTTLE_AGEING_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_oversimplified_or_unrelated_bottle_items_remain_excluded(self):
        for item_id in ("wset3_46", "wset3_58", "wset3_850"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    BOTTLE_AGEING_NODE_IDS,
                )


class SparklingProductionExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_sparkling_nodes_are_matcher_compatible_and_localized(self):
        for node_id in SPARKLING_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_sparkling_enrichment_assignments(self):
        expected = {
            "wset3_23": "HC_PRESSURE_MOUSSE_INTENSITY",
            "wset3_25": "HC_LIQUEUR_TIRAGE_SECOND_FERMENTATION",
            "wset3_27": "HC_BASE_WINE_OXIDATION_DAMAGE",
            "wset3_29": "HC_ANCESTRAL_SINGLE_FERMENTATION",
            "wset3_108": "HC_TANK_METHOD_FRUIT_RETENTION",
            "wset3_110": "HC_TANK_METHOD_FRUIT_RETENTION",
            "wset3_125": "HC_TRADITIONAL_BOTTLE_SECOND_FERMENTATION",
            "wset3_129": "HC_DISGORGEMENT_SEDIMENT_REMOVAL",
            "wset3_201": "HC_RIDDLING_SEDIMENT_COLLECTION",
            "wset3_204": "HC_ANCESTRAL_SINGLE_FERMENTATION",
            "wset3_214": "HC_DISGORGEMENT_SEDIMENT_REMOVAL",
            "wset3_217": "HC_BRUT_NATURE_NO_DOSAGE",
            "wset3_240": "HC_TANK_METHOD_FRUIT_RETENTION",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in SPARKLING_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_sparkling_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in SPARKLING_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_definitional_and_sweetness_risk_items_remain_excluded(self):
        for item_id in ("wset3_26", "wset3_28", "wset3_107", "wset3_124", "wset3_215"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    SPARKLING_NODE_IDS,
                )


class ViticultureHazardExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_hazard_nodes_are_matcher_compatible_and_localized(self):
        for node_id in VITICULTURE_HAZARD_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_hazard_enrichment_assignments(self):
        expected = {
            "wset3_12": "HC_FROST_SLOPE_AIR_DRAINAGE",
            "wset3_316": "HC_EARLY_GROWTH_FROST_EXPOSURE",
            "wset3_318": "HC_CANOPY_AIRFLOW_FUNGAL_RISK",
            "wset3_33": "HC_DRIP_IRRIGATION_PRECISION",
            "wset3_433": "HC_EXCESS_NITROGEN_DISEASE_RISK",
            "wset3_488": "HC_CANOPY_SHADE_HEAT_PROTECTION",
            "wset3_489": "HC_CANOPY_AIRFLOW_FUNGAL_RISK",
            "wset3_493": "HC_LATE_HARVEST_FROST_EXPOSURE",
            "wset3_498": "HC_CANOPY_AIRFLOW_FUNGAL_RISK",
            "wset3_504": "HC_FLOWERING_RAIN_FRUIT_SET",
            "wset3_505": "HC_COVER_CROPS_EROSION_CONTROL",
            "wset3_672": "HC_PHYLLOXERA_RESISTANT_ROOTSTOCK",
            "wset3_676": "HC_EARLY_GROWTH_FROST_EXPOSURE",
            "wset3_677": "HC_CANOPY_AIRFLOW_FUNGAL_RISK",
            "wset3_688": "HC_DRIP_IRRIGATION_PRECISION",
            "wset3_707": "HC_DRIP_IRRIGATION_PRECISION",
            "wset3_708": "HC_FROST_SHOOT_YIELD_DAMAGE",
            "wset3_709": "HC_CANOPY_AIRFLOW_FUNGAL_RISK",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in VITICULTURE_HAZARD_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_hazard_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in VITICULTURE_HAZARD_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_questionable_and_negative_hazard_items_remain_excluded(self):
        for item_id in ("wset3_429", "wset3_454", "wset3_772", "wset3_777", "wset3_791"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    VITICULTURE_HAZARD_NODE_IDS,
                )


class CellarControlExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_cellar_nodes_are_matcher_compatible_and_localized(self):
        for node_id in CELLAR_CONTROL_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_cellar_control_assignments(self):
        expected = {
            "wset3_16": "HC_RED_FERMENTATION_EXTRACTION",
            "wset3_37": "HC_RED_FERMENTATION_EXTRACTION",
            "wset3_64": "HC_CELLAR_HYGIENE_MICROBIAL_CONTROL",
            "wset3_74": "HC_STERILE_FILTRATION_MICROBIAL_STABILITY",
            "wset3_317": "HC_COLD_TARTRATE_STABILIZATION",
            "wset3_459": "HC_COOL_FERMENTATION_AROMA_RETENTION",
            "wset3_469": "HC_COOL_FERMENTATION_AROMA_RETENTION",
            "wset3_470": "HC_CONCRETE_THERMAL_INERTIA",
            "wset3_472": "HC_PREBOTTLING_FILTRATION_CLARITY",
            "wset3_474": "HC_STERILE_FILTRATION_MICROBIAL_STABILITY",
            "wset3_480": "HC_RED_FERMENTATION_EXTRACTION",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in CELLAR_CONTROL_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_cellar_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in CELLAR_CONTROL_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)


class HarvestAndSiteExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_harvest_site_nodes_are_matcher_compatible_and_localized(self):
        for node_id in HARVEST_SITE_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_harvest_site_assignments(self):
        expected = {
            "wset3_40": "HC_SOUTH_FACING_EXPOSURE_RIPENESS",
            "wset3_349": "HC_NIGHT_HARVEST_FRESHNESS",
            "wset3_351": "HC_EARLY_HARVEST_FRESHNESS_ALCOHOL",
            "wset3_407": "HC_NIGHT_HARVEST_FRESHNESS",
            "wset3_451": "HC_SOUTH_FACING_EXPOSURE_RIPENESS",
            "wset3_457": "HC_SELECTIVE_HAND_HARVEST_QUALITY",
            "wset3_496": "HC_EARLY_HARVEST_FRESHNESS_ALCOHOL",
            "wset3_680": "HC_NIGHT_HARVEST_FRESHNESS",
            "wset3_685": "HC_SELECTIVE_HAND_HARVEST_QUALITY",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in HARVEST_SITE_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_harvest_site_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in HARVEST_SITE_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_oversimplified_night_harvest_acidity_item_remains_excluded(self):
        record = self.records.get("wset3_468")
        if record is not None:
            self.assertNotIn(
                record["_provenance"]["causal_chain"]["derived_from"],
                HARVEST_SITE_NODE_IDS,
            )


class OakAndOxygenExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_oak_oxygen_nodes_are_matcher_compatible_and_localized(self):
        for node_id in OAK_OXYGEN_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_oak_oxygen_assignments(self):
        expected = {
            "wset3_7": "HC_OXIDATIVE_AGEING_TERTIARY",
            "wset3_207": "HC_OXIDATIVE_AGEING_TERTIARY",
            "wset3_346": "HC_NEW_OAK_STRUCTURE_SPICE",
            "wset3_461": "HC_NEW_OAK_STRUCTURE_SPICE",
            "wset3_473": "HC_BARREL_SIZE_OAK_CONTACT",
            "wset3_490": "HC_FREQUENT_RACKING_OXYGEN",
            "wset3_492": "HC_OXIDATIVE_AGEING_TERTIARY",
            "wset3_511": "HC_USED_OAK_OXYGEN_LOW_FLAVOUR",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in OAK_OXYGEN_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_oak_oxygen_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in OAK_OXYGEN_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_regional_attribution_and_cork_items_remain_excluded(self):
        for item_id in ("wset3_324", "wset3_389", "wset3_850"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    OAK_OXYGEN_NODE_IDS,
                )


class VineyardMechanismExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_vineyard_nodes_are_matcher_compatible_and_localized(self):
        for node_id in VINEYARD_MECHANISM_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_vineyard_mechanism_assignments(self):
        expected = {
            "wset3_13": "HC_SANDY_SOIL_DRAINAGE",
            "wset3_340": "HC_HUMID_HARVEST_DILUTION",
            "wset3_352": "HC_ALTITUDE_SLOW_RIPENING_FRESHNESS",
            "wset3_365": "HC_ALTITUDE_SLOW_RIPENING_FRESHNESS",
            "wset3_400": "HC_ALTITUDE_SLOW_RIPENING_FRESHNESS",
            "wset3_464": "HC_DESTEMMING_GREEN_TANNIN_REDUCTION",
            "wset3_483": "HC_MODERATE_WATER_STRESS_PHENOLICS",
            "wset3_675": "HC_SANDY_SOIL_DRAINAGE",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in VINEYARD_MECHANISM_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_vineyard_mechanism_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in VINEYARD_MECHANISM_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_context_dependent_vineyard_claims_remain_excluded(self):
        for item_id in ("wset3_509",):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    VINEYARD_MECHANISM_NODE_IDS,
                )


class SensoryPairingExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_sensory_nodes_are_matcher_compatible_and_localized(self):
        for node_id in SENSORY_PAIRING_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_sensory_pairing_assignments(self):
        expected = {
            "wset3_43": "HC_UMAMI_BITTER_ACID_PERCEPTION",
            "wset3_47": "HC_PROTEIN_FAT_TANNIN_SOFTENING",
            "wset3_56": "HC_ALCOHOL_CHILI_HEAT",
            "wset3_62": "HC_FOOD_SWEETNESS_WINE_CONTRAST",
            "wset3_85": "HC_SALT_TANNIN_BALANCE",
            "wset3_335": "HC_FOOD_SWEETNESS_WINE_CONTRAST",
            "wset3_713": "HC_LOW_SERVICE_TEMPERATURE_TANNIN_AROMA",
            "wset3_719": "HC_FOOD_SWEETNESS_WINE_CONTRAST",
            "wset3_724": "HC_FOOD_SWEETNESS_WINE_CONTRAST",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in SENSORY_PAIRING_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_sensory_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in SENSORY_PAIRING_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_health_and_oversimplified_alcohol_items_remain_excluded(self):
        for item_id in ("wset3_60", "wset3_75", "wset3_716", "wset3_731"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    SENSORY_PAIRING_NODE_IDS,
                )


class FaultAndStabilityExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_fault_stability_nodes_are_matcher_compatible_and_localized(self):
        for node_id in FAULT_STABILITY_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_fault_stability_assignments(self):
        expected = {
            "wset3_38": "HC_SO2_OXIDATION_PROTECTION",
            "wset3_45": "HC_BRETTANOMYCES_ANIMAL_ODOR",
            "wset3_48": "HC_TCA_MUSTY_CARDBOARD",
            "wset3_51": "HC_PERFUMED_DETERGENT_GLASS_CONTAMINATION",
            "wset3_58": "HC_OPEN_BOTTLE_OXYGEN_CONTROL",
            "wset3_68": "HC_TCA_MUSTY_CARDBOARD",
            "wset3_71": "HC_OPEN_BOTTLE_OXYGEN_CONTROL",
            "wset3_73": "HC_REDUCTION_SULFUR_ODORS",
            "wset3_80": "HC_EXCESSIVE_WHITE_OXIDATION",
            "wset3_330": "HC_TCA_MUSTY_CARDBOARD",
            "wset3_427": "HC_BENTONITE_PROTEIN_STABILITY",
            "wset3_494": "HC_MUST_CHILLING_FERMENTATION_CONTROL",
            "wset3_501": "HC_RACKING_OXYGEN_SEDIMENT",
            "wset3_502": "HC_REDUCTION_SULFUR_ODORS",
            "wset3_507": "HC_PRESSING_OXIDATION_RISK",
            "wset3_717": "HC_TCA_MUSTY_CARDBOARD",
            "wset3_725": "HC_VOLATILE_ACIDITY_VINEGAR_SOLVENT",
            "wset3_727": "HC_HEAT_TRANSPORT_WINE_DAMAGE",
            "wset3_736": "HC_REFERMENTATION_UNEXPECTED_BUBBLES",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in FAULT_STABILITY_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_fault_stability_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in FAULT_STABILITY_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_closure_specific_oxidation_claim_remains_excluded(self):
        record = self.records.get("wset3_734")
        if record is not None:
            self.assertNotIn(
                record["_provenance"]["causal_chain"]["derived_from"],
                FAULT_STABILITY_NODE_IDS,
            )


class StyleMechanismExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_style_nodes_are_matcher_compatible_and_localized(self):
        for node_id in STYLE_MECHANISM_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_style_mechanism_assignments(self):
        expected = {
            "wset3_35": "HC_WARM_DRY_OVERRIPENING",
            "wset3_92": "HC_FORTIFICATION_STOPS_FERMENTATION",
            "wset3_112": "HC_COOL_SPARKLING_BASE_ACIDITY",
            "wset3_123": "HC_COOL_SPARKLING_BASE_ACIDITY",
            "wset3_205": "HC_FORTIFICATION_STOPS_FERMENTATION",
            "wset3_222": "HC_COOL_SPARKLING_BASE_ACIDITY",
            "wset3_319": "HC_CANOPY_VIGOUR_EXPOSURE",
            "wset3_304": "HC_HUMBOLDT_CURRENT_FRESHNESS",
            "wset3_354": "HC_HUMBOLDT_CURRENT_FRESHNESS",
            "wset3_417": "HC_CANOPY_VIGOUR_EXPOSURE",
            "wset3_436": "HC_CANOPY_VIGOUR_EXPOSURE",
            "wset3_467": "HC_CARBONIC_MACERATION_FRUIT_LOW_TANNIN",
            "wset3_477": "HC_LOW_VIGOUR_ROOTSTOCK_CONTROL",
            "wset3_486": "HC_SOLAR_EXPOSURE_RED_COLOR",
            "wset3_495": "HC_WARM_CLIMATE_ACID_LOSS",
            "wset3_518": "HC_ALTITUDE_GRAPE_ACIDITY",
            "wset3_668": "HC_ALTITUDE_GRAPE_ACIDITY",
            "wset3_710": "HC_CANOPY_VIGOUR_EXPOSURE",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in STYLE_MECHANISM_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_style_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in STYLE_MECHANISM_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_regional_and_categorical_style_claims_remain_excluded(self):
        for item_id in (
            "wset3_91",
            "wset3_106",
            "wset3_210",
            "wset3_247",
            "wset3_322",
            "wset3_341",
            "wset3_374",
            "wset3_421",
            "wset3_442",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    STYLE_MECHANISM_NODE_IDS,
                )


class FermentationControlExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_fermentation_control_nodes_are_matcher_compatible_and_localized(self):
        for node_id in FERMENTATION_CONTROL_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_fermentation_control_assignments(self):
        expected = {
            "wset3_42": "HC_HIGH_FERMENTATION_TEMP_BURNT_AROMAS",
            "wset3_349": "HC_NIGHT_HARVEST_FRESHNESS",
            "wset3_407": "HC_NIGHT_HARVEST_FRESHNESS",
            "wset3_431": "HC_STAINLESS_TEMPERATURE_CONTROL",
            "wset3_459": "HC_COOL_FERMENTATION_AROMA_RETENTION",
            "wset3_469": "HC_COOL_FERMENTATION_AROMA_RETENTION",
            "wset3_674": "HC_STAINLESS_TEMPERATURE_CONTROL",
            "wset3_680": "HC_NIGHT_HARVEST_FRESHNESS",
            "wset3_684": "HC_STAINLESS_PRIMARY_AROMA_PRESERVATION",
            "wset3_686": "HC_SELECTED_YEAST_PREDICTABILITY",
            "wset3_702": "HC_HARVEST_COOLING_AROMA_PROTECTION",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in FERMENTATION_CONTROL_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_fermentation_control_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in FERMENTATION_CONTROL_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_definitions_negative_stems_and_weak_yeast_claims_remain_excluded(self):
        for item_id in ("wset3_107", "wset3_460", "wset3_466", "wset3_787"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    FERMENTATION_CONTROL_NODE_IDS,
                )


class SoilPhysicsExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_soil_physics_nodes_are_matcher_compatible_and_localized(self):
        for node_id in SOIL_PHYSICS_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_soil_physics_assignments(self):
        expected = {
            "wset3_13": "HC_SANDY_SOIL_DRAINAGE",
            "wset3_39": "HC_CLAY_WATER_RETENTION",
            "wset3_476": "HC_CLAY_WATER_RETENTION",
            "wset3_675": "HC_SANDY_SOIL_DRAINAGE",
            "wset3_678": "HC_COVER_CROP_SOIL_STRUCTURE",
            "wset3_711": "HC_WELL_DRAINED_ROOT_DEVELOPMENT",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in SOIL_PHYSICS_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_soil_physics_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in SOIL_PHYSICS_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_negative_and_unsupported_soil_claims_remain_excluded(self):
        for item_id in ("wset3_261", "wset3_456", "wset3_485", "wset3_506", "wset3_779"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    SOIL_PHYSICS_NODE_IDS,
                )


class StorageServiceExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_storage_service_nodes_are_matcher_compatible_and_localized(self):
        for node_id in STORAGE_SERVICE_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_storage_service_assignments(self):
        expected = {
            "wset3_46": "HC_ICE_WATER_RAPID_CHILLING",
            "wset3_50": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_53": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_78": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_86": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_331": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_720": "HC_BOTTLE_STORAGE_STABILITY",
            "wset3_733": "HC_BOTTLE_STORAGE_STABILITY",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in STORAGE_SERVICE_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_storage_service_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in STORAGE_SERVICE_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_closure_claim_and_service_temperature_recall_remain_excluded(self):
        for item_id in ("wset3_49", "wset3_67", "wset3_76", "wset3_329", "wset3_734", "wset3_850"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    STORAGE_SERVICE_NODE_IDS,
                )


class ServiceMechanicsExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_service_mechanics_nodes_are_matcher_compatible_and_localized(self):
        for node_id in SERVICE_MECHANICS_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_service_mechanics_assignments(self):
        expected = {
            "wset3_52": "HC_AERATION_YOUNG_STRUCTURED_WINE",
            "wset3_70": "HC_LARGE_BOWL_AROMA_EXPRESSION",
            "wset3_72": "HC_AERATION_YOUNG_STRUCTURED_WINE",
            "wset3_84": "HC_SAFE_SPARKLING_CORK_OPENING",
            "wset3_336": "HC_LARGE_BOWL_AROMA_EXPRESSION",
            "wset3_732": "HC_GENTLE_CARBONATED_WINE_SERVICE",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in SERVICE_MECHANICS_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_service_mechanics_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in SERVICE_MECHANICS_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_vague_or_unsupported_service_advice_remains_excluded(self):
        for item_id in ("wset3_63", "wset3_334", "wset3_718", "wset3_735"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    SERVICE_MECHANICS_NODE_IDS,
                )


class WinemakingMechanicsExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_winemaking_mechanics_nodes_are_matcher_compatible_and_localized(self):
        for node_id in WINEMAKING_MECHANICS_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_winemaking_mechanics_assignments(self):
        expected = {
            "wset3_20": "HC_EXTRACTION_BODY_STRUCTURE",
            "wset3_478": "HC_SHORT_MACERATION_LOW_COLOR",
            "wset3_681": "HC_MUST_SETTLING_CLARIFICATION",
            "wset3_683": "HC_NEW_OAK_TANNIN_WHITE_WINE",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in WINEMAKING_MECHANICS_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_winemaking_mechanics_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in WINEMAKING_MECHANICS_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_terms_regional_styles_and_negative_stems_remain_excluded(self):
        for item_id in ("wset3_369", "wset3_393", "wset3_520", "wset3_700", "wset3_776", "wset3_780"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    WINEMAKING_MECHANICS_NODE_IDS,
                )


class CoolClimateRipeningExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_cool_climate_node_is_matcher_compatible_and_localized(self):
        for node_id in COOL_CLIMATE_RIPENING_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_cool_climate_ripening_assignments(self):
        expected = {
            "wset3_271": "HC_COOL_CLIMATE_STYLE",
            "wset3_430": "HC_COOL_CLIMATE_STYLE",
            "wset3_442": "HC_COOL_CLIMATE_STYLE",
            "wset3_509": "HC_COOL_CLIMATE_STYLE",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in COOL_CLIMATE_RIPENING_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_cool_climate_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in COOL_CLIMATE_RIPENING_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_regional_attribution_and_negative_stems_remain_excluded(self):
        for item_id in ("wset3_247", "wset3_322", "wset3_374", "wset3_790"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    COOL_CLIMATE_RIPENING_NODE_IDS,
                )


class VineyardManagementExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_vineyard_management_nodes_are_matcher_compatible_and_localized(self):
        for node_id in VINEYARD_MANAGEMENT_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_vineyard_management_assignments(self):
        expected = {
            "wset3_19": "HC_YIELD_CONCENTRATION",
            "wset3_319": "HC_CANOPY_VIGOUR_EXPOSURE",
            "wset3_351": "HC_EARLY_HARVEST_FRESHNESS_ALCOHOL",
            "wset3_417": "HC_CANOPY_VIGOUR_EXPOSURE",
            "wset3_436": "HC_CANOPY_VIGOUR_EXPOSURE",
            "wset3_452": "HC_CANOPY_VIGOUR_EXPOSURE",
            "wset3_457": "HC_SELECTIVE_HAND_HARVEST_QUALITY",
            "wset3_484": "HC_YIELD_CONCENTRATION",
            "wset3_496": "HC_EARLY_HARVEST_FRESHNESS_ALCOHOL",
            "wset3_497": "HC_YIELD_CONCENTRATION",
            "wset3_462": "HC_CANOPY_VIGOUR_EXPOSURE",
            "wset3_516": "HC_CANOPY_VIGOUR_EXPOSURE",
            "wset3_685": "HC_SELECTIVE_HAND_HARVEST_QUALITY",
            "wset3_710": "HC_CANOPY_VIGOUR_EXPOSURE",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in VINEYARD_MANAGEMENT_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_vineyard_management_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in VINEYARD_MANAGEMENT_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_absolute_doubtful_and_negative_claims_remain_excluded(self):
        for item_id in (
            "wset3_32",
            "wset3_458",
            "wset3_471",
            "wset3_519",
            "wset3_788",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    VINEYARD_MANAGEMENT_NODE_IDS,
                )


class WineFaultCausationExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_wine_fault_nodes_are_matcher_compatible_and_localized(self):
        for node_id in WINE_FAULT_CAUSATION_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_wine_fault_causation_assignments(self):
        expected = {
            "wset3_48": "HC_TCA_MUSTY_CARDBOARD",
            "wset3_68": "HC_TCA_MUSTY_CARDBOARD",
            "wset3_73": "HC_REDUCTION_SULFUR_ODORS",
            "wset3_330": "HC_TCA_MUSTY_CARDBOARD",
            "wset3_502": "HC_REDUCTION_SULFUR_ODORS",
            "wset3_717": "HC_TCA_MUSTY_CARDBOARD",
            "wset3_725": "HC_VOLATILE_ACIDITY_VINEGAR_SOLVENT",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in WINE_FAULT_CAUSATION_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_wine_fault_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in WINE_FAULT_CAUSATION_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_weak_or_misattributed_fault_claims_remain_excluded(self):
        for item_id in ("wset3_18", "wset3_54", "wset3_55", "wset3_734"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    WINE_FAULT_CAUSATION_NODE_IDS,
                )


class ExtractionOxygenInterventionExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_intervention_nodes_are_matcher_compatible_and_localized(self):
        for node_id in EXTRACTION_OXYGEN_INTERVENTION_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_extraction_oxygen_intervention_assignments(self):
        expected = {
            "wset3_16": "HC_RED_FERMENTATION_EXTRACTION",
            "wset3_37": "HC_RED_FERMENTATION_EXTRACTION",
            "wset3_444": "HC_MICROOXYGENATION_TANNIN_SOFTENING",
            "wset3_480": "HC_RED_FERMENTATION_EXTRACTION",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in EXTRACTION_OXYGEN_INTERVENTION_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_intervention_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in EXTRACTION_OXYGEN_INTERVENTION_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_related_but_distinct_processes_remain_excluded(self):
        for item_id in ("wset3_14", "wset3_443", "wset3_515", "wset3_816"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    EXTRACTION_OXYGEN_INTERVENTION_NODE_IDS,
                )


class UnderripeHarvestExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_underripe_harvest_node_is_matcher_compatible_and_localized(self):
        for node_id in UNDERRIPE_HARVEST_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_underripe_harvest_assignments(self):
        expected = {
            "wset3_428": "HC_UNDERRIPE_HARVEST_GREEN_AROMAS",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in UNDERRIPE_HARVEST_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_underripe_harvest_matches_have_dual_evidence(self):
        record = self.records["wset3_428"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertTrue(provenance["stem_hits"])
        self.assertTrue(provenance["correct_option_hits"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_deliberate_early_harvest_claims_remain_distinct(self):
        for item_id in ("wset3_351", "wset3_458", "wset3_496"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    UNDERRIPE_HARVEST_NODE_IDS,
                )


class AlcoholBitternessExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_alcohol_bitterness_node_is_matcher_compatible_and_localized(self):
        for node_id in ALCOHOL_BITTERNESS_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_alcohol_bitterness_assignments(self):
        expected = {
            "wset3_731": "HC_ALCOHOL_BITTERNESS_PERCEPTION",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in ALCOHOL_BITTERNESS_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_alcohol_bitterness_match_has_specific_dual_evidence(self):
        record = self.records["wset3_731"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertIn(
            "alcohol en la percepcion de amargor del vino",
            provenance["stem_hits"],
        )
        self.assertEqual(provenance["correct_option_hits"], ["lo intensifica"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_chili_and_health_items_remain_distinct(self):
        for item_id in ("wset3_49", "wset3_60", "wset3_75", "wset3_716"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    ALCOHOL_BITTERNESS_NODE_IDS,
                )


class FlorBiologicalAgeingExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_flor_node_is_matcher_compatible_and_localized(self):
        for node_id in FLOR_BIOLOGICAL_AGEING_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_flor_biological_ageing_assignments(self):
        expected = {
            "wset3_1": "CC_FLOR_BIOLOGICAL_AGEING",
            "wset3_102": "CC_FLOR_BIOLOGICAL_AGEING",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in FLOR_BIOLOGICAL_AGEING_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_flor_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in FLOR_BIOLOGICAL_AGEING_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_direct_salinity_attribution_remains_excluded(self):
        record = self.records.get("wset3_208")
        if record is not None:
            self.assertNotIn(
                record["_provenance"]["causal_chain"]["derived_from"],
                FLOR_BIOLOGICAL_AGEING_NODE_IDS,
            )


class HumboldtCoastalCoolingExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_humboldt_node_is_matcher_compatible_and_localized(self):
        for node_id in HUMBOLDT_COASTAL_COOLING_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_humboldt_assignments(self):
        expected = {
            "wset3_304": "HC_HUMBOLDT_CURRENT_FRESHNESS",
            "wset3_354": "HC_HUMBOLDT_CURRENT_FRESHNESS",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in HUMBOLDT_COASTAL_COOLING_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_humboldt_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in HUMBOLDT_COASTAL_COOLING_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_generic_coastal_region_claims_remain_excluded(self):
        for item_id in ("wset3_251", "wset3_728"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    HUMBOLDT_COASTAL_COOLING_NODE_IDS,
                )


class AgeabilityStructureExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_ageability_node_is_matcher_compatible_and_localized(self):
        for node_id in AGEABILITY_STRUCTURE_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_ageability_structure_assignments(self):
        expected = {
            "wset3_3": "HC_RED_WINE_AGEABILITY_STRUCTURE",
            "wset3_83": "HC_RED_WINE_AGEABILITY_STRUCTURE",
            "wset3_385": "HC_RED_WINE_AGEABILITY_STRUCTURE",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in AGEABILITY_STRUCTURE_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_ageability_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in AGEABILITY_STRUCTURE_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_regional_ageing_shortcuts_remain_excluded(self):
        for item_id in ("wset3_253", "wset3_324"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    AGEABILITY_STRUCTURE_NODE_IDS,
                )


class ProductionEconomicsExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_economics_nodes_are_matcher_compatible_and_localized(self):
        for node_id in PRODUCTION_ECONOMICS_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_production_economics_assignments(self):
        expected = {
            "wset3_15": "HC_MECHANIZATION_PRODUCTION_COST",
            "wset3_841": "HC_COOPERATIVE_SHARED_RESOURCES",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in PRODUCTION_ECONOMICS_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_economics_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in PRODUCTION_ECONOMICS_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_price_placeholders_and_intermediary_definitions_remain_excluded(self):
        for item_id in ("wset3_348", "wset3_412", "wset3_712", "wset3_840", "wset3_844"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    PRODUCTION_ECONOMICS_NODE_IDS,
                )


class WineBalanceExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_wine_balance_node_is_matcher_compatible_and_localized(self):
        for node_id in WINE_BALANCE_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_wine_balance_assignments(self):
        expected = {
            "wset3_54": "HC_LOW_ACID_STRUCTURE_FLATNESS",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in WINE_BALANCE_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_wine_balance_match_has_dual_evidence(self):
        record = self.records["wset3_54"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertEqual(
            provenance["derived_from"],
            "HC_LOW_ACID_STRUCTURE_FLATNESS",
        )
        self.assertTrue(provenance["stem_hits"])
        self.assertTrue(provenance["correct_option_hits"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_fault_and_storage_flatness_items_remain_distinct(self):
        for item_id in ("wset3_48", "wset3_65", "wset3_733"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    WINE_BALANCE_NODE_IDS,
                )


class MarketEconomicsExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_market_economics_nodes_are_matcher_compatible_and_localized(self):
        for node_id in MARKET_ECONOMICS_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_market_economics_assignments(self):
        expected = {
            "wset3_846": "HC_EXCLUSIVE_DISTRIBUTOR_MARKET_ACCESS",
            "wset3_847": "HC_SCARCITY_DEMAND_PRICE_PRESSURE",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in MARKET_ECONOMICS_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_market_economics_matches_have_dual_evidence(self):
        for item_id, record in self.records.items():
            provenance = record["_provenance"]["causal_chain"]
            if provenance["derived_from"] not in MARKET_ECONOMICS_NODE_IDS:
                continue
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertTrue(provenance["correct_option_hits"], item_id)
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_definitions_placeholders_and_vague_price_claims_remain_excluded(self):
        for item_id in (
            "wset3_267",
            "wset3_348",
            "wset3_412",
            "wset3_712",
            "wset3_840",
            "wset3_844",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    MARKET_ECONOMICS_NODE_IDS,
                )


class AlsaceRipeningExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_alsace_node_is_matcher_compatible_and_localized(self):
        for node_id in ALSACE_RIPENING_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_alsace_ripening_assignments(self):
        expected = {
            "wset3_408": "HC_ALSACE_SUN_DRY_RIPENING",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in ALSACE_RIPENING_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_alsace_match_has_dual_evidence(self):
        record = self.records["wset3_408"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertEqual(
            provenance["derived_from"],
            "HC_ALSACE_SUN_DRY_RIPENING",
        )
        self.assertTrue(provenance["stem_hits"])
        self.assertTrue(provenance["correct_option_hits"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_other_regional_and_unsupported_concentration_claims_remain_excluded(self):
        for item_id in (
            "wset3_251",
            "wset3_374",
            "wset3_421",
            "wset3_454",
            "wset3_479",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    ALSACE_RIPENING_NODE_IDS,
                )


class So2MicrobialControlExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_so2_microbial_node_is_matcher_compatible_and_localized(self):
        for node_id in SO2_MICROBIAL_CONTROL_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_so2_microbial_control_assignments(self):
        expected = {
            "wset3_682": "HC_SO2_MICROBIAL_INHIBITION",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in SO2_MICROBIAL_CONTROL_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_so2_microbial_match_has_dual_evidence(self):
        record = self.records["wset3_682"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertEqual(
            provenance["derived_from"],
            "HC_SO2_MICROBIAL_INHIBITION",
        )
        self.assertTrue(provenance["stem_hits"])
        self.assertTrue(provenance["correct_option_hits"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_definition_absolute_identification_and_label_items_remain_excluded(self):
        for item_id in ("wset3_88", "wset3_514", "wset3_517", "wset3_827"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    SO2_MICROBIAL_CONTROL_NODE_IDS,
                )


class MaritimeModerationExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_maritime_node_is_matcher_compatible_and_localized(self):
        for node_id in MARITIME_MODERATION_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_maritime_moderation_assignments(self):
        expected = {
            "wset3_388": "HC_MARITIME_MODERATION",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in MARITIME_MODERATION_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_maritime_match_has_dual_evidence(self):
        record = self.records["wset3_388"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertTrue(provenance["stem_hits"])
        self.assertTrue(provenance["correct_option_hits"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_regional_profiles_and_negative_claim_remain_excluded(self):
        for item_id in (
            "wset3_251",
            "wset3_288",
            "wset3_345",
            "wset3_396",
            "wset3_728",
            "wset3_792",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    MARITIME_MODERATION_NODE_IDS,
                )


class ClonalSelectionExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_clonal_selection_node_is_matcher_compatible_and_localized(self):
        for node_id in CLONAL_SELECTION_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_clonal_selection_assignments(self):
        expected = {
            "wset3_679": "HC_CLONAL_SELECTION_STYLE_INFLUENCE",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in CLONAL_SELECTION_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_clonal_selection_match_has_dual_evidence(self):
        record = self.records["wset3_679"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertTrue(provenance["stem_hits"])
        self.assertTrue(provenance["correct_option_hits"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_rootstock_and_hybrid_items_remain_excluded(self):
        for item_id in ("wset3_437", "wset3_477", "wset3_672"):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    CLONAL_SELECTION_NODE_IDS,
                )


class SteepSlopeSolarRipeningExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_steep_slope_node_is_matcher_compatible_and_localized(self):
        for node_id in STEEP_SLOPE_SOLAR_RIPENING_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_steep_slope_solar_ripening_assignments(self):
        expected = {
            "wset3_671": "HC_STEEP_SLOPE_SOLAR_RIPENING",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in STEEP_SLOPE_SOLAR_RIPENING_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_steep_slope_match_has_dual_evidence(self):
        record = self.records["wset3_671"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertTrue(provenance["stem_hits"])
        self.assertTrue(provenance["correct_option_hits"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_vague_slope_frost_and_identification_items_remain_excluded(self):
        for item_id in (
            "wset3_12",
            "wset3_247",
            "wset3_299",
            "wset3_322",
            "wset3_376",
            "wset3_394",
            "wset3_439",
            "wset3_695",
            "wset3_775",
            "wset3_786",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    STEEP_SLOPE_SOLAR_RIPENING_NODE_IDS,
                )


class ShortCycleVarietyExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_short_cycle_node_is_matcher_compatible_and_localized(self):
        for node_id in SHORT_CYCLE_VARIETY_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_short_cycle_variety_assignments(self):
        expected = {
            "wset3_687": "HC_SHORT_CYCLE_VARIETY_COOL_SEASON_FIT",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in SHORT_CYCLE_VARIETY_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_short_cycle_match_has_dual_evidence(self):
        record = self.records["wset3_687"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertTrue(provenance["stem_hits"])
        self.assertTrue(provenance["correct_option_hits"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_climate_profiles_and_harvest_timing_remain_excluded(self):
        for item_id in (
            "wset3_11",
            "wset3_247",
            "wset3_322",
            "wset3_351",
            "wset3_374",
            "wset3_458",
            "wset3_496",
            "wset3_790",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    SHORT_CYCLE_VARIETY_NODE_IDS,
                )


class LateHarvestRipenessExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_late_harvest_ripeness_node_is_matcher_compatible_and_localized(self):
        for node_id in LATE_HARVEST_RIPENESS_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_late_harvest_ripeness_assignments(self):
        expected = {
            "wset3_513": "HC_LATE_HARVEST_RIPENESS_BODY",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in LATE_HARVEST_RIPENESS_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_late_harvest_ripeness_match_has_dual_evidence(self):
        record = self.records["wset3_513"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertTrue(provenance["stem_hits"])
        self.assertTrue(provenance["correct_option_hits"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_early_dried_overripe_and_frost_items_remain_excluded(self):
        for item_id in (
            "wset3_35",
            "wset3_339",
            "wset3_351",
            "wset3_428",
            "wset3_458",
            "wset3_493",
            "wset3_496",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    LATE_HARVEST_RIPENESS_NODE_IDS,
                )


class OlorosoAmontilladoAgeingPathExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_ageing_path_node_is_matcher_compatible_and_localized(self):
        for node_id in OLOROSO_AMONTILLADO_PATH_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_oloroso_amontillado_path_assignments(self):
        expected = {
            "wset3_5": "HC_OLOROSO_AMONTILLADO_AGEING_PATH",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in OLOROSO_AMONTILLADO_PATH_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_ageing_path_match_has_dual_evidence(self):
        record = self.records["wset3_5"]
        provenance = record["_provenance"]["causal_chain"]
        self.assertTrue(provenance["stem_hits"])
        self.assertTrue(provenance["correct_option_hits"])
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_related_fortified_wine_items_remain_excluded(self):
        for item_id in (
            "wset3_93",
            "wset3_97",
            "wset3_102",
            "wset3_207",
            "wset3_208",
            "wset3_210",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    OLOROSO_AMONTILLADO_PATH_NODE_IDS,
                )


class AcidFoodWineBalanceExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_acid_food_balance_node_is_matcher_compatible_and_localized(self):
        for node_id in ACID_FOOD_WINE_BALANCE_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_acid_food_balance_assignments(self):
        expected = {
            "wset3_57": "HC_ACID_FOOD_HIGH_ACID_WINE_BALANCE",
            "wset3_737": "HC_ACID_FOOD_HIGH_ACID_WINE_BALANCE",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in ACID_FOOD_WINE_BALANCE_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_acid_food_balance_matches_have_dual_evidence(self):
        for item_id in ("wset3_57", "wset3_737"):
            provenance = self.records[item_id]["_provenance"]["causal_chain"]
            self.assertTrue(provenance["stem_hits"], item_id)
            self.assertEqual(
                provenance["correct_option_hits"],
                ["vino blanco joven con alta acidez"],
                item_id,
            )
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_other_food_pairing_mechanisms_remain_excluded(self):
        for item_id in (
            "wset3_43",
            "wset3_44",
            "wset3_47",
            "wset3_56",
            "wset3_69",
            "wset3_79",
            "wset3_90",
            "wset3_332",
            "wset3_333",
            "wset3_721",
            "wset3_738",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    ACID_FOOD_WINE_BALANCE_NODE_IDS,
                )


class SpicyFoodWinePairingExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in payload["items_by_source_question_id"].values()
        }

    def test_spicy_food_pairing_node_is_matcher_compatible_and_localized(self):
        for node_id in SPICY_FOOD_WINE_PAIRING_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_spicy_food_pairing_assignments(self):
        expected = {
            "wset3_333": "HC_RESIDUAL_SUGAR_LOW_ALCOHOL_CHILI_PAIRING",
        }
        actual = {
            item_id: record["_provenance"]["causal_chain"]["derived_from"]
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"]
            in SPICY_FOOD_WINE_PAIRING_NODE_IDS
        }
        self.assertEqual(actual, expected)

    def test_spicy_food_pairing_match_has_dual_evidence(self):
        provenance = self.records["wset3_333"]["_provenance"]["causal_chain"]
        self.assertEqual(
            provenance["stem_hits"],
            ["maridar vinos con platos picantes"],
        )
        self.assertEqual(
            provenance["correct_option_hits"],
            ["vino con dulzor residual y baja graduacion"],
        )
        self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_related_food_and_alcohol_items_remain_excluded(self):
        for item_id in (
            "wset3_43",
            "wset3_44",
            "wset3_47",
            "wset3_56",
            "wset3_57",
            "wset3_69",
            "wset3_75",
            "wset3_79",
            "wset3_90",
            "wset3_332",
            "wset3_716",
            "wset3_721",
            "wset3_737",
            "wset3_738",
        ):
            record = self.records.get(item_id)
            if record is not None:
                self.assertNotIn(
                    record["_provenance"]["causal_chain"]["derived_from"],
                    SPICY_FOOD_WINE_PAIRING_NODE_IDS,
                )


if __name__ == "__main__":
    unittest.main()
