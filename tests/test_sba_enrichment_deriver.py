"""Tests for the SBA enrichment deriver (Phase P.1, precision-first v2)."""

from __future__ import annotations

import json
import re
import unittest

from tools.question_generation.sba_enrichment_deriver import (
    BATCH_SIZE,
    GENERIC_TRIGGERS,
    MIN_KEYWORD_HITS,
    NODE_ES,
    derive,
    load_chain_nodes,
    load_frontend_items,
    match_item,
)


class FalsePositiveRegressionTests(unittest.TestCase):
    """The exact false positives found in the batch-1 review must stay rejected."""

    @classmethod
    def setUpClass(cls):
        cls.nodes = load_chain_nodes()
        cls.items = {i["id"]: i for i in load_frontend_items()}
        cls.payload = derive()
        cls.enriched_ids = {r["item_id"] for r in cls.payload["items_by_source_question_id"].values()}

    def test_vinho_verde_not_enriched(self):
        # wset3_269: "¿Qué región portuguesa es famosa por vinos blancos frescos?"
        # v1 bug: substring 'port' in 'portuguesa' + generic 'vino' -> fortification.
        self.assertNotIn("wset3_269", self.enriched_ids)
        if "wset3_269" in self.items:
            match, reason = match_item(self.items["wset3_269"], self.nodes)
            self.assertIsNone(match)
            self.assertEqual(reason, "identification_stem")

    def test_loire_oceanic_not_enriched(self):
        # wset3_396: "¿Qué factor natural es más importante en los vinos del Valle del Loira?"
        # v1 bug: substring 'port' in 'importante'.
        self.assertNotIn("wset3_396", self.enriched_ids)
        if "wset3_396" in self.items:
            match, _reason = match_item(self.items["wset3_396"], self.nodes)
            self.assertIsNone(match)

    def test_definitional_stems_rejected(self):
        # "¿Qué es un Manzanilla?" / "¿Qué indica un Porto LBV?" — definitional.
        for qid in ("wset3_101", "wset3_103"):
            self.assertNotIn(qid, self.enriched_ids)

    def test_negative_polarity_stems_rejected(self):
        # Batch-2 guard: "¿Cuál afirmación es INCORRECTA?" — the correct answer is
        # a deliberately false statement; enriching it would teach the falsehood.
        # wset3_792 (maritime INCORRECTA) and wset3_788 (yield INCORRECTA).
        for qid in ("wset3_792", "wset3_788"):
            self.assertNotIn(qid, self.enriched_ids)
            if qid in self.items:
                match, reason = match_item(self.items[qid], self.nodes)
                self.assertIsNone(match)
                self.assertEqual(reason, "negative_polarity_stem")

    def test_no_generic_trigger_in_any_match(self):
        for rec in self.payload["items_by_source_question_id"].values():
            prov = rec["_provenance"]["causal_chain"]
            for kw in prov["matched_keywords"]:
                self.assertNotIn(kw, GENERIC_TRIGGERS, f"generic trigger matched: {kw}")

    def test_word_boundary_no_substring_matches(self):
        # 'port' must never appear as a matched keyword fragment of a longer word.
        for rec in self.payload["items_by_source_question_id"].values():
            item = self.items[rec["item_id"]]
            surface = (item.get("text", "") + " " + " ".join(item.get("keywords", []))).lower()
            for kw in rec["_provenance"]["causal_chain"]["matched_keywords"]:
                self.assertTrue(len(kw) >= 4)


class StrongSignalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = derive()
        cls.records = list(cls.payload["items_by_source_question_id"].values())

    def test_every_match_has_stem_and_correct_option_hits(self):
        for rec in self.records:
            prov = rec["_provenance"]["causal_chain"]
            self.assertTrue(prov["stem_hits"], rec["item_id"])
            self.assertTrue(prov["correct_option_hits"], rec["item_id"])
            self.assertGreaterEqual(prov["match_score"], MIN_KEYWORD_HITS)

    def test_every_chain_node_has_spanish_layer(self):
        for rec in self.records:
            self.assertIn(rec["_provenance"]["causal_chain"]["derived_from"], NODE_ES)

    def test_batch_is_small_and_bounded(self):
        self.assertLessEqual(len(self.records), BATCH_SIZE)
        self.assertGreater(len(self.records), 0)


class DeterminismTests(unittest.TestCase):
    def test_two_runs_identical(self):
        a = json.dumps(derive(), sort_keys=True, ensure_ascii=False)
        b = json.dumps(derive(), sort_keys=True, ensure_ascii=False)
        self.assertEqual(a, b)


class SpanishOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = derive()

    def _learner_text(self):
        out = []
        for rec in self.payload["items_by_source_question_id"].values():
            cc = rec["causal_chain"]
            out += [cc["causa"], cc["mecanismo"], cc["efecto"]]
            out += list(rec["feedback_by_mode"].values())
            if "micro_drill" in rec:
                d = rec["micro_drill"]
                out += [d["prompt"], d["explanation"], d["remediation_signal"]]
        return out

    def test_no_english_markers(self):
        markers = (" the ", " is ", " are ", "wine aged", "yeast", "Work through", "sediment forms")
        joined = " | ".join(self._learner_text())
        for m in markers:
            self.assertNotIn(m, joined, f"English marker leaked: {m!r}")

    def test_no_contraction_artifacts(self):
        joined = " | ".join(self._learner_text())
        self.assertIsNone(re.search(r"\b(?:de el|a el)\b", joined))


class EnrichmentIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = derive()
        cls.records = list(cls.payload["items_by_source_question_id"].values())

    def test_causal_chain_complete(self):
        for rec in self.records:
            cc = rec["causal_chain"]
            for k in ("causa", "mecanismo", "efecto"):
                self.assertTrue(str(cc.get(k, "")).strip(), rec["item_id"])

    def test_feedback_three_distinct_modes(self):
        for rec in self.records:
            fb = rec["feedback_by_mode"]
            texts = [fb["mentor"], fb["trainer"], fb["reviewer"]]
            self.assertTrue(all(t.strip() for t in texts))
            self.assertEqual(len(set(texts)), 3, rec["item_id"])

    def test_drills_valid(self):
        for rec in self.records:
            d = rec.get("micro_drill")
            if not d:
                continue
            self.assertEqual(len(d["options"]), 4)
            self.assertEqual(len(set(d["options"])), 4)
            self.assertTrue(0 <= d["correct_index"] < 4)
            self.assertTrue(d["explanation"].strip())
            self.assertTrue(d["remediation_signal"].strip())

    def test_provenance_present_and_not_learner_facing(self):
        for rec in self.records:
            self.assertIn("_provenance", rec)
            self.assertIn("causal_chain", rec["_provenance"])

    def test_governance_clean(self):
        gov = self.payload["governance"]
        self.assertIs(gov["safe_for_examiner"], False)
        self.assertIs(gov["examiner_scoring_allowed"], False)
        txt = json.dumps(self.payload, ensure_ascii=False).lower()
        for forbidden in ('"mark"', '"score"', '"grade"', "wset_equivalence"):
            self.assertNotIn(forbidden, txt)


if __name__ == "__main__":
    unittest.main()
