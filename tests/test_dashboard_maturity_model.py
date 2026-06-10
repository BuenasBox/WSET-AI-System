import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = REPO_ROOT / "frontend" / "architecture-dashboard" / "system_state.json"
HTML_PATH = REPO_ROOT / "frontend" / "architecture-dashboard" / "index.html"


class TestDashboardMaturityModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        cls.html = HTML_PATH.read_text(encoding="utf-8")

    def test_weighted_maturity_is_reproducible(self):
        tracks = self.state["maturity_model"]["tracks"]
        self.assertEqual(sum(track["weight"] for track in tracks), 100)
        weighted = round(
            sum(track["percent"] * track["weight"] for track in tracks) / 100
        )
        self.assertEqual(weighted, self.state["maturity"])
        self.assertEqual(weighted, self.state["maturity_model"]["overall_percent"])

    def test_tracks_have_explicit_evidence_and_next_gate(self):
        tracks = self.state["maturity_model"]["tracks"]
        self.assertEqual(len(tracks), 8)
        self.assertEqual(len({track["id"] for track in tracks}), len(tracks))
        for track in tracks:
            self.assertGreaterEqual(track["percent"], 0)
            self.assertLessEqual(track["percent"], 100)
            self.assertTrue(track["stage"])
            self.assertTrue(track["evidence"])
            self.assertTrue(track["next_gate"])

    def test_verified_repository_counts_are_separate_from_estimates(self):
        self.assertEqual(self.state["tests"], 1464)
        self.assertEqual(self.state["tests_skipped"], 9)
        self.assertEqual(self.state["active_sba_items"], 36)
        self.assertEqual(self.state["export_validation_errors"], 0)
        self.assertEqual(self.state["master_bank_total"], 616)
        self.assertEqual(self.state["master_bank_sba"], 595)
        self.assertEqual(self.state["master_bank_open_response"], 21)

    def test_activation_and_governance_are_not_overstated(self):
        self.assertEqual(self.state["open_response_status"], "active_private_lab")
        self.assertEqual(
            self.state["adaptive_engine_status"],
            "pedagogical_contract_only",
        )
        self.assertEqual(self.state["official_scoring_status"], "not_allowed")
        self.assertEqual(self.state["examiner_authority_status"], "not_allowed")
        self.assertFalse(
            self.state["governance_status"]["official_examiner_authority"]
        )

    def test_dashboard_renders_traceable_maturity(self):
        self.assertIn('id="maturity-grid"', self.html)
        self.assertIn("function syncMaturityTracks()", self.html)
        self.assertIn("Madurez de<br>Ingeniería", self.html)
        self.assertIn("No mide inteligencia", self.html)

    def test_domain_status_is_explicit(self):
        self.assertEqual(
            self.state["production_dashboard_url"],
            "https://epistemiclab.dpdns.org/",
        )
        self.assertEqual(
            self.state["requested_custom_domain"],
            "https://www.epistemiclab.org/",
        )
        self.assertEqual(
            self.state["custom_domain_status"],
            "dns_not_pointing_to_github_pages",
        )


if __name__ == "__main__":
    unittest.main()
