from __future__ import annotations

import unittest
from pathlib import Path


CONTRACT_PATH = Path("docs/DASHBOARD_LAB_LINK_CONTRACT.md")


def contract_text() -> str:
    return CONTRACT_PATH.read_text(encoding="utf-8")


class DashboardLabLinkContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = contract_text()
        cls.lower = cls.text.lower()

    def test_contract_file_exists(self) -> None:
        self.assertTrue(CONTRACT_PATH.exists())

    def test_documents_diagnostic_sba_path(self) -> None:
        self.assertIn("/diagnostic-sba/", self.text)
        self.assertIn("diagnostic-sba/index.html", self.text)
        self.assertIn("diagnostic-sba/preguntas.json", self.text)

    def test_documents_allowed_link_labels(self) -> None:
        self.assertIn("Diagnostic SBA Lab", self.text)
        self.assertIn("Laboratorio Diagnóstico SBA", self.text)

    def test_documents_noindex_and_robots_requirements(self) -> None:
        self.assertIn("noindex/nofollow", self.lower)
        self.assertIn("robots.txt", self.lower)
        self.assertIn("Disallow: /", self.text)
        self.assertIn("no sitemap", self.lower)

    def test_documents_training_only_governance(self) -> None:
        self.assertIn("training-only", self.lower)
        self.assertIn("entrenamiento", self.lower)
        self.assertIn("no official WSET evaluation", self.text)
        self.assertIn("no evaluacion oficial wset", self.lower)

    def test_forbids_production_official_examiner_claims(self) -> None:
        required_forbidden_terms = (
            "official exam",
            "official WSET score",
            "pass/fail",
            "certification readiness",
            "examiner simulation",
            "examiner scoring",
            "production app",
        )

        for term in required_forbidden_terms:
            self.assertIn(term.lower(), self.lower)

    def test_documents_required_deployment_structure(self) -> None:
        self.assertIn("Recommended static deployment structure", self.text)
        self.assertIn("system_state.json", self.text)
        self.assertIn("CNAME", self.text)
        self.assertIn("Required deployment files", self.text)

    def test_documents_explicit_gate_before_dashboard_modification(self) -> None:
        self.assertIn("Deployment Gate", self.text)
        self.assertIn("Explicit authorization to modify the architecture dashboard", self.text)
        self.assertIn("no dashboard HTML should be modified", self.text)

    def test_contract_keeps_phase_docs_and_tests_only(self) -> None:
        self.assertIn("contract only", self.lower)
        self.assertIn("modify `frontend/architecture-dashboard/index.html`", self.text)
        self.assertIn("modify `frontend/diagnostic-sba/index.html`", self.text)
        self.assertIn("modify `frontend/diagnostic-sba/preguntas.json`", self.text)


if __name__ == "__main__":
    unittest.main()
