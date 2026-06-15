import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "tools/frontend/regression_gate/gate.mjs"


class FrontendRegressionGateReleaseScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gate = GATE_PATH.read_text(encoding="utf-8")

    def test_sba_corpus_scope_skips_untouched_open_response_gate(self):
        self.assertIn("RELEASE_SCOPE", self.gate)
        self.assertIn("sba-corpus", self.gate)
        self.assertIn("skip('G2'", self.gate)

    def test_adaptive_gates_bypass_authorization_not_experience_logic(self):
        self.assertIn("startAllowedAdp(mode)", self.gate)
        self.assertNotIn("p.click(`button[onclick=\"startAdp('${m}')\"]`)", self.gate)

    def test_navigation_gate_uses_current_commercial_landing_cards(self):
        self.assertIn("a.exp-card", self.gate)
        self.assertNotIn("a.lab-card", self.gate)

    def test_page_errors_are_cleared_before_the_verified_navigation(self):
        clear = "p._errs.length=0; await p.goto"
        self.assertIn(clear, self.gate)


if __name__ == "__main__":
    unittest.main()
