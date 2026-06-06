import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_RULES = (
    "Production dashboard source = BuenasBox/epistemiclab-dashboard",
    "Operational domain = epistemiclab.dpdns.org",
    "Do not audit origin/gh-pages as production source unless explicitly reactivated.",
)


class TestProductionDashboardSourceContract(unittest.TestCase):
    def test_authoritative_memory_records_production_source(self):
        text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for rule in REQUIRED_RULES:
            self.assertIn(rule, text)

    def test_frontend_reconciliation_records_prevalent_rule(self):
        text = (
            REPO_ROOT / "docs" / "FRONTEND_SOURCE_OF_TRUTH_RECONCILIATION.md"
        ).read_text(encoding="utf-8")
        for rule in REQUIRED_RULES:
            self.assertIn(rule, text)

    def test_current_state_does_not_identify_gh_pages_as_active_source(self):
        text = (
            REPO_ROOT / "docs" / "PROJECT_STATE_RECONCILIATION.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Fuente de producción: `BuenasBox/epistemiclab-dashboard`",
            text,
        )
        self.assertIn(
            "`WSET-AI-System/origin/gh-pages` para determinar el estado publicado",
            text,
        )


if __name__ == "__main__":
    unittest.main()
