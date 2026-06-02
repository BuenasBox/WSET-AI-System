from __future__ import annotations

import unittest
from pathlib import Path


CONTRACT_PATH = Path("docs/STATIC_RELEASE_ASSEMBLY_SCRIPT_CONTRACT.md")


def contract_text() -> str:
    return CONTRACT_PATH.read_text(encoding="utf-8")


class StaticReleaseAssemblyScriptContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = contract_text()
        cls.lower = cls.text.lower()

    def test_contract_file_exists(self) -> None:
        self.assertTrue(CONTRACT_PATH.exists())

    def test_documents_future_script_path(self) -> None:
        self.assertIn("tools/dashboard/assemble_static_release.py", self.text)

    def test_documents_future_output_directory(self) -> None:
        self.assertIn("dist/epistemiclab-static/", self.text)
        self.assertIn("outside `dist/`", self.text)

    def test_documents_required_output_tree(self) -> None:
        for token in (
            "dist/epistemiclab-static/",
            "index.html",
            "system_state.json",
            "robots.txt",
            "CNAME",
            ".nojekyll",
            "diagnostic-sba/",
            "preguntas.json",
        ):
            self.assertIn(token, self.text)

    def test_documents_dashboard_allowlist(self) -> None:
        self.assertIn("Allowed dashboard files", self.text)
        for token in ("index.html", "system_state.json", "robots.txt", "CNAME", ".nojekyll"):
            self.assertIn(token, self.text)

    def test_documents_diagnostic_sba_allowlist(self) -> None:
        self.assertIn("Allowed Diagnostic SBA files", self.text)
        self.assertIn("frontend/diagnostic-sba/", self.text)
        self.assertIn("preguntas.json", self.text)

    def test_documents_denylist(self) -> None:
        for token in ("knowledge/", "docs/", "tests/", "tools/", ".git/"):
            self.assertIn(token, self.text)
        self.assertIn("node_modules/", self.text)
        self.assertIn("__pycache__/", self.text)

    def test_documents_fail_closed_behavior(self) -> None:
        self.assertIn("fail closed", self.lower)
        self.assertIn("required file is missing", self.lower)
        self.assertIn("attempted copy is outside the allowlist", self.lower)

    def test_documents_dry_run_default(self) -> None:
        self.assertIn("--dry-run", self.text)
        self.assertIn("--write", self.text)
        self.assertIn("--clean", self.text)
        self.assertIn("Default mode must be dry-run/no write", self.text)

    def test_documents_no_deploy_responsibility(self) -> None:
        self.assertIn("must not deploy", self.lower)
        self.assertIn("Deployment remains a separate manual/explicit step", self.text)
        self.assertIn("git subtree push", self.text)

    def test_documents_preguntas_json_validation(self) -> None:
        self.assertIn("preguntas.json", self.text)
        self.assertIn("static demo payload validation", self.lower)
        self.assertIn("pre-submit leakage", self.lower)

    def test_documents_noindex_and_robots_checks(self) -> None:
        self.assertIn("noindex", self.lower)
        self.assertIn("nofollow", self.lower)
        self.assertIn("robots.txt", self.lower)
        self.assertIn("disallow-all", self.lower)


if __name__ == "__main__":
    unittest.main()
