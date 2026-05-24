"""R4-C: Golden output CI baseline for the brutal self-eval.

This test runs the full 25-question self-eval and asserts that key outcome
metrics do not regress below the golden baseline captured in
knowledge/self-eval/golden_brutal_output.json.

It is intentionally slow (~7 s on current hardware) and is guarded behind
the environment variable RUN_SLOW_TESTS=1 so it does not run in the default
`python -m unittest discover` suite.

To run explicitly:
    RUN_SLOW_TESTS=1 python -m unittest tests.test_golden_self_eval -v
On Windows PowerShell:
    $env:RUN_SLOW_TESTS=1; python -m unittest tests.test_golden_self_eval -v
"""

from __future__ import annotations

import json
import os
import unittest
from collections import Counter
from pathlib import Path

from tools.constants import KNOWLEDGE_DIR


GOLDEN_PATH = KNOWLEDGE_DIR / "self-eval" / "golden_brutal_output.json"
SLOW_TESTS = os.environ.get("RUN_SLOW_TESTS", "").strip() not in ("", "0", "false", "False")


def _load_golden() -> dict:
    return json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))


@unittest.skipUnless(SLOW_TESTS, "set RUN_SLOW_TESTS=1 to run golden self-eval baseline test")
class GoldenSelfEvalTests(unittest.TestCase):
    """Compare a live self-eval run against the frozen golden baseline."""

    @classmethod
    def setUpClass(cls) -> None:
        from tools.self_eval.question_runner import run_self_eval
        from tools.self_eval.evaluation_reporter import build_les_feedback

        cls.golden = _load_golden()
        result = run_self_eval(limit=25)
        cls.results = result["results"]
        cls.feedback = build_les_feedback(cls.results, strictness="hard")

        # Aggregate per-result metrics for the assertions below
        label_counter: Counter = Counter()
        retrieval_counter: Counter = Counter()
        causal_counter: Counter = Counter()
        misconception_counter: Counter = Counter()
        sat_weakness_ids: list[str] = []
        retrieval_gap_ids: list[str] = []

        for r in cls.results:
            comparison = r.get("comparison", {})
            labels = comparison.get("failure_labels", [])
            label_counter.update(labels)
            retrieval_counter.update(comparison.get("retrieval_weaknesses", []))
            causal_counter.update(comparison.get("missing_causal_links", []))
            misconception_counter.update(comparison.get("likely_misconception_gaps", []))
            if r.get("question_type") == "sat" and labels:
                sat_weakness_ids.append(r.get("question_id", ""))
            if "retrieval_gap" in labels:
                retrieval_gap_ids.append(r.get("question_id", ""))

        cls.label_counter = label_counter
        cls.retrieval_counter = retrieval_counter
        cls.causal_counter = causal_counter
        cls.misconception_counter = misconception_counter
        cls.sat_weakness_ids = sat_weakness_ids
        cls.retrieval_gap_ids = retrieval_gap_ids

    # ------------------------------------------------------------------
    # Hard gates — these must be zero; any non-zero is a regression
    # ------------------------------------------------------------------

    def test_no_failure_labels(self) -> None:
        """No question must produce any failure label."""
        self.assertEqual(
            dict(self.label_counter),
            self.golden["failure_labels"],
            f"Failure labels regressed: {dict(self.label_counter)}",
        )

    def test_no_sat_weaknesses(self) -> None:
        """No SAT question must produce a failure label."""
        self.assertEqual(
            self.sat_weakness_ids,
            self.golden["sat_weakness_question_ids"],
            f"SAT weaknesses appeared: {self.sat_weakness_ids}",
        )

    def test_no_retrieval_gaps(self) -> None:
        """No question must produce a retrieval_gap label."""
        self.assertEqual(
            self.retrieval_gap_ids,
            self.golden["retrieval_gap_question_ids"],
            f"Retrieval gaps appeared: {self.retrieval_gap_ids}",
        )

    def test_no_new_retrieval_weaknesses(self) -> None:
        """No retrieval weakness type may appear that is not in the golden baseline."""
        golden_keys = set(self.golden["retrieval_weaknesses"].keys())
        live_keys = set(self.retrieval_counter.keys())
        new_weaknesses = live_keys - golden_keys
        self.assertFalse(
            new_weaknesses,
            f"New retrieval weakness types appeared (not in golden baseline): {new_weaknesses}",
        )

    def test_known_retrieval_weakness_not_worse(self) -> None:
        """Known weakness missing_keyword_support must not exceed the golden count."""
        golden_count = self.golden["retrieval_weaknesses"].get("missing_keyword_support", 0)
        live_count = self.retrieval_counter.get("missing_keyword_support", 0)
        self.assertLessEqual(
            live_count,
            golden_count,
            f"missing_keyword_support regressed: {live_count} > golden {golden_count}",
        )

    # ------------------------------------------------------------------
    # Informational check — causal chains
    # ------------------------------------------------------------------

    def test_no_new_missing_causal_chains(self) -> None:
        """No missing causal chain may appear that is not in the golden baseline."""
        golden_keys = set(self.golden["causal_chains_missing"].keys())
        live_keys = set(self.causal_counter.keys())
        new_missing = live_keys - golden_keys
        self.assertFalse(
            new_missing,
            f"New missing causal chains appeared: {new_missing}",
        )

    # ------------------------------------------------------------------
    # Governance check
    # ------------------------------------------------------------------

    def test_governance_flags_unchanged(self) -> None:
        """Governance flags must remain false throughout a full self-eval run."""
        from tools.constants import (
            SAFE_FOR_EXAMINER,
            EXAMINER_SCORING_ALLOWED,
            USES_LLM,
            USES_API,
            USES_EMBEDDINGS,
            USES_VECTOR_DB,
            CLOUD_SERVICES_ACTIVE,
        )
        self.assertFalse(SAFE_FOR_EXAMINER)
        self.assertFalse(EXAMINER_SCORING_ALLOWED)
        self.assertFalse(USES_LLM)
        self.assertFalse(USES_API)
        self.assertFalse(USES_EMBEDDINGS)
        self.assertFalse(USES_VECTOR_DB)
        self.assertFalse(CLOUD_SERVICES_ACTIVE)


if __name__ == "__main__":
    unittest.main()
