from __future__ import annotations

import unittest
from pathlib import Path


PLAN_PATH = Path("docs/STATIC_LAB_DEPLOYMENT_STAGING_PLAN.md")


def plan_text() -> str:
    return PLAN_PATH.read_text(encoding="utf-8")


class StaticLabDeploymentStagingPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = plan_text()
        cls.lower = cls.text.lower()

    def test_plan_exists(self) -> None:
        self.assertTrue(PLAN_PATH.exists())

    def test_documents_desired_deployed_tree(self) -> None:
        self.assertIn("Desired Deployed Tree", self.text)
        self.assertIn("system_state.json", self.text)
        self.assertIn("robots.txt", self.text)
        self.assertIn("CNAME", self.text)
        self.assertIn(".nojekyll", self.text)
        self.assertIn("diagnostic-sba/", self.text)

    def test_mentions_lab_files(self) -> None:
        self.assertIn("diagnostic-sba/index.html", self.text)
        self.assertIn("diagnostic-sba/preguntas.json", self.text)

    def test_forbids_publishing_knowledge_corpus(self) -> None:
        self.assertIn("knowledge corpus", self.lower)
        self.assertIn("must not include", self.lower)

    def test_forbids_docs_tests_tools_in_deployment(self) -> None:
        self.assertIn("tests", self.lower)
        self.assertIn("docs", self.lower)
        self.assertIn("python tools", self.lower)
        self.assertIn("research docs", self.lower)

    def test_requires_robots_disallow_and_noindex(self) -> None:
        self.assertIn("robots.txt", self.lower)
        self.assertIn("Disallow: /", self.text)
        self.assertIn("noindex,nofollow", self.lower)
        self.assertIn("no sitemap", self.lower)

    def test_documents_subtree_push(self) -> None:
        self.assertIn("git subtree push --prefix frontend/architecture-dashboard origin gh-pages", self.text)
        self.assertIn("git subtree split --prefix frontend/architecture-dashboard main", self.text)

    def test_documents_pre_and_post_deploy_checks(self) -> None:
        self.assertIn("Pre-Deploy Checks", self.text)
        self.assertIn("Post-Deploy Checks", self.text)
        self.assertIn("/diagnostic-sba/` loads", self.text)
        self.assertIn("/diagnostic-sba/preguntas.json` loads", self.text)
        self.assertIn("https://epistemiclab.dpdns.org/diagnostic-sba/", self.text)

    def test_documents_no_deployment_phase_boundary(self) -> None:
        self.assertIn("planning and static validation only", self.lower)
        self.assertIn("must not", self.lower)
        self.assertIn("deploy", self.lower)
        self.assertIn("modify `gh-pages`", self.text)


if __name__ == "__main__":
    unittest.main()
