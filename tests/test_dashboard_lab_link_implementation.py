"""
tests/test_dashboard_lab_link_implementation.py

Phase 4A.3.7.21 — Verify the Diagnostic SBA Lab is correctly integrated
into the architecture dashboard. All assertions are deterministic file reads.
"""

import os
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_HTML = os.path.join(REPO, "frontend", "architecture-dashboard", "index.html")
LAB_HTML       = os.path.join(REPO, "frontend", "architecture-dashboard", "diagnostic-sba", "index.html")
LAB_JSON       = os.path.join(REPO, "frontend", "architecture-dashboard", "diagnostic-sba", "preguntas.json")
ROBOTS_TXT     = os.path.join(REPO, "frontend", "architecture-dashboard", "robots.txt")

FORBIDDEN_GOVERNANCE = [
    "official score",
    "pass/fail",
    "certification readiness",
    "examiner scoring",
]

# Only flag actual remote-API / third-party-service identifiers.
# Local static fetches (e.g. fetch('./system_state.json')) are intentional
# and are NOT flagged.
FORBIDDEN_BACKEND = [
    "supabase",
    "Supabase",
    "api.openai",
    "api.anthropic",
    "openai.com",
    "anthropic.com/v1",
    "amazonaws.com",
    "firebase",
    "firestore",
]

FORBIDDEN_ANALYTICS = [
    "google-analytics",
    "gtag(",
    "analytics.js",
    "_gaq",
    "mixpanel",
    "segment.io",
    "hotjar",
    "plausible",
]


class TestDashboardLabLinkImplementation(unittest.TestCase):

    def _read(self, path):
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()

    # ------------------------------------------------------------------
    # 1. Dashboard links to the SBA lab
    # ------------------------------------------------------------------
    def test_dashboard_links_to_sba_lab(self):
        content = self._read(DASHBOARD_HTML)
        self.assertTrue(
            "./diagnostic-sba/" in content or "diagnostic-sba/" in content,
            "Dashboard must contain a link href pointing to ./diagnostic-sba/",
        )

    # ------------------------------------------------------------------
    # 2. Link text identifies the lab correctly
    # ------------------------------------------------------------------
    def test_dashboard_link_text(self):
        content = self._read(DASHBOARD_HTML)
        self.assertTrue(
            "Diagnóstico SBA" in content or "Diagnostic SBA Lab" in content,
            "Dashboard must contain link text 'Diagnóstico SBA' or 'Diagnostic SBA Lab'",
        )

    # ------------------------------------------------------------------
    # 3. Lab index.html exists
    # ------------------------------------------------------------------
    def test_lab_index_exists(self):
        self.assertTrue(
            os.path.isfile(LAB_HTML),
            f"Lab index not found: {LAB_HTML}",
        )

    # ------------------------------------------------------------------
    # 4. preguntas.json exists alongside the lab
    # ------------------------------------------------------------------
    def test_preguntas_json_exists(self):
        self.assertTrue(
            os.path.isfile(LAB_JSON),
            f"preguntas.json not found: {LAB_JSON}",
        )

    # ------------------------------------------------------------------
    # 5. Dashboard has noindex meta
    # ------------------------------------------------------------------
    def test_dashboard_has_noindex(self):
        content = self._read(DASHBOARD_HTML)
        self.assertIn(
            "noindex",
            content,
            "Dashboard index.html must contain 'noindex' meta tag",
        )

    # ------------------------------------------------------------------
    # 6. Lab has noindex meta
    # ------------------------------------------------------------------
    def test_lab_has_noindex(self):
        content = self._read(LAB_HTML)
        self.assertIn(
            "noindex",
            content,
            "Lab index.html must contain 'noindex' meta tag",
        )

    # ------------------------------------------------------------------
    # 7. robots.txt disallows all crawlers
    # ------------------------------------------------------------------
    def test_robots_txt_disallows_all(self):
        self.assertTrue(os.path.isfile(ROBOTS_TXT), f"robots.txt not found: {ROBOTS_TXT}")
        content = self._read(ROBOTS_TXT)
        self.assertIn(
            "Disallow: /",
            content,
            "robots.txt must contain 'Disallow: /'",
        )

    # ------------------------------------------------------------------
    # 8. No forbidden governance words in either file
    # ------------------------------------------------------------------
    def test_no_forbidden_governance_words(self):
        for path in (DASHBOARD_HTML, LAB_HTML):
            content = self._read(path).lower()
            for word in FORBIDDEN_GOVERNANCE:
                self.assertNotIn(
                    word.lower(),
                    content,
                    f"Forbidden governance term '{word}' found in {os.path.basename(path)}",
                )

    # ------------------------------------------------------------------
    # 9. No backend / remote API references
    # ------------------------------------------------------------------
    def test_no_backend_references(self):
        for path in (DASHBOARD_HTML, LAB_HTML):
            content = self._read(path)
            for ref in FORBIDDEN_BACKEND:
                self.assertNotIn(
                    ref,
                    content,
                    f"Forbidden backend reference '{ref}' found in {os.path.basename(path)}",
                )

    # ------------------------------------------------------------------
    # 10. No analytics / tracking scripts
    # ------------------------------------------------------------------
    def test_no_analytics(self):
        for path in (DASHBOARD_HTML, LAB_HTML):
            content = self._read(path)
            for tracker in FORBIDDEN_ANALYTICS:
                self.assertNotIn(
                    tracker,
                    content,
                    f"Forbidden analytics reference '{tracker}' found in {os.path.basename(path)}",
                )


if __name__ == "__main__":
    unittest.main()
