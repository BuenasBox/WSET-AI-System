"""
Snapshot regression tests for the Tutor answer builder.

These tests assert that build_tutor_answer() produces byte-for-byte identical
output when given the same frozen context package as the golden baseline.

HOW IT WORKS
------------
Each snapshot fixture contains two files:
  tests/fixtures/tutor_snapshots/{question_id}/context_package.json
      Frozen input — the exact context package used to generate the golden answer.
  tests/fixtures/tutor_snapshots/{question_id}/expected_answer.txt
      Golden output — the Tutor answer text at the time the fixture was captured.

The test loads each frozen context package, calls build_tutor_answer(), and
compares the result character-by-character against the stored golden answer.

WHAT IS DETECTED
----------------
Any change to any of the following causes at least one test to fail:
  • Heading text or heading count
  • Disclaimer presence or wording
  • Source-note text
  • Causal chain rendering (causa/mecanismo/efecto labels or text)
  • Exam phrasing (Formulación de examen section)
  • Answer section structure (section order, blank lines, section count)
  • Any answer text change caused by code edits in answer_builder.py

GENERATING THE BASELINE (required before first run)
----------------------------------------------------
Snapshots are NEVER created automatically during test discovery.
Before running the test suite for the first time, generate the fixtures
explicitly from the current stable self-eval state:

    python tests/generate_tutor_snapshots.py

This reads knowledge/self-eval/attempts/{1..25}/ and writes:
  tests/fixtures/tutor_snapshots/{id}/context_package.json
  tests/fixtures/tutor_snapshots/{id}/expected_answer.txt
  tests/fixtures/tutor_snapshots/{id}/question.json
  tests/fixtures/tutor_snapshots/manifest.json

Commit those files before running the test suite.
If snapshots are missing, tests FAIL — they do not skip and do not self-generate.

DELIBERATE BASELINE UPDATE
---------------------------
If a behavior change is intentional (e.g., Q3 Porto Vintage keyword pattern added),
regenerate the baseline by running:
    python tests/generate_tutor_snapshots.py
Then commit the updated fixture files.

GOVERNANCE
----------
build_tutor_answer() is always called with the frozen context package.
No retrieval, no orchestrator, no LLM, no API, no embeddings, no vector DB.
Governance flags (safe_for_examiner, examiner_scoring_allowed) are asserted False
for every snapshot test run.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.tutor.answer_builder import (
    DISCLAIMER_EN,
    DISCLAIMER_ES,
    build_tutor_answer,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SNAPSHOTS_ROOT = Path(__file__).parent / "fixtures" / "tutor_snapshots"
MANIFEST_PATH = SNAPSHOTS_ROOT / "manifest.json"
ATTEMPTS_ROOT = Path(__file__).parent.parent / "knowledge" / "self-eval" / "attempts"


def _load_manifest() -> list[dict]:
    if not MANIFEST_PATH.exists():
        return []
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Snapshot comparison helper
# ---------------------------------------------------------------------------

def _run_snapshot(question_id: str) -> tuple[str, str, dict]:
    """
    Load a frozen context package, run build_tutor_answer(), and return
    (actual_answer, expected_answer, governance_result).

    Raises FileNotFoundError if fixture files are missing.
    """
    fixture_dir = SNAPSHOTS_ROOT / str(question_id)
    context_src = fixture_dir / "context_package.json"
    expected_src = fixture_dir / "expected_answer.txt"

    if not context_src.exists():
        raise FileNotFoundError(f"Missing context_package.json for Q{question_id}")
    if not expected_src.exists():
        raise FileNotFoundError(f"Missing expected_answer.txt for Q{question_id}")

    expected_answer = expected_src.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        tmp_context = tmp_root / "context_package.json"
        # Write via bytes to preserve encoding exactly
        tmp_context.write_bytes(context_src.read_bytes())

        result = build_tutor_answer(
            context_package_path=tmp_context,
            output_path=tmp_root / "answer.md",
            style="standard",
        )

        actual_answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

    return actual_answer, expected_answer, result["governance"]


# ---------------------------------------------------------------------------
# Main snapshot regression test class
# (one dynamically-generated test method per snapshot)
# ---------------------------------------------------------------------------

class TutorSnapshotRegressionTests(unittest.TestCase):
    """
    Golden snapshot regression tests.

    Each test method is generated dynamically — one per snapshot fixture.
    Test names follow the pattern test_snapshot_q{question_id}.

    On the first run, if no fixtures exist, they are auto-bootstrapped from
    the current stable state in knowledge/self-eval/attempts/.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Load manifest metadata. Fixture absence is caught at test-method level."""
        cls.manifest = _load_manifest()

    def _snapshot_test(self, question_id: str, question_text: str) -> None:
        """Core snapshot assertion: exact text match + structure invariants."""
        actual, expected, governance = _run_snapshot(question_id)

        # Primary: byte-for-byte identity
        self.assertEqual(
            actual,
            expected,
            msg=(
                f"\nTutor output changed for Q{question_id}: {question_text[:60]!r}\n\n"
                "If this change is INTENTIONAL, regenerate the golden baseline:\n"
                "  python tests/generate_tutor_snapshots.py\n"
                "then commit the updated fixture files.\n\n"
                "If this change is UNINTENTIONAL, revert the code change."
            ),
        )

        # Belt-and-suspenders: structure invariants that must always hold
        label = f"Q{question_id}"

        # Governance flags
        self.assertFalse(
            governance["safe_for_examiner"],
            f"{label}: safe_for_examiner must remain False",
        )
        self.assertFalse(
            governance["examiner_scoring_allowed"],
            f"{label}: examiner_scoring_allowed must remain False",
        )
        self.assertFalse(governance["uses_llm"], f"{label}: uses_llm must be False")
        self.assertFalse(governance["uses_api"], f"{label}: uses_api must be False")
        self.assertFalse(governance["uses_embeddings"], f"{label}: uses_embeddings must be False")
        self.assertFalse(governance["uses_vector_db"], f"{label}: uses_vector_db must be False")

        # Disclaimer at end
        self.assertTrue(
            actual.endswith(DISCLAIMER_ES) or actual.endswith(DISCLAIMER_EN),
            f"{label}: answer must end with the Tutor disclaimer",
        )

        # At least one heading
        headings = [line for line in actual.splitlines() if line.startswith("#")]
        self.assertGreater(len(headings), 0, f"{label}: answer must contain headings")

        # No placeholder text
        self.assertNotIn(
            "usa el contexto recuperado", actual,
            f"{label}: placeholder text must not appear in output",
        )
        self.assertNotIn(
            "Use the retrieved pedagogical context", actual,
            f"{label}: placeholder text must not appear in output",
        )


def _make_snapshot_test(question_id: str, question_text: str):
    """Factory: returns a test method for one snapshot."""
    def test_method(self: TutorSnapshotRegressionTests) -> None:
        self._snapshot_test(question_id, question_text)
    test_method.__name__ = f"test_snapshot_q{question_id}"
    test_method.__doc__ = (
        f"Q{question_id} snapshot: {question_text[:70]}"
        if len(question_text) <= 70
        else f"Q{question_id} snapshot: {question_text[:67]}..."
    )
    return test_method


# ---------------------------------------------------------------------------
# Module-level dynamic test registration.
# NO file I/O is performed here.  If the manifest is present, one test method
# per snapshot is attached.  If the manifest is absent, a single sentinel test
# is attached that fails with a clear actionable message — no silent skip,
# no auto-generation.
# ---------------------------------------------------------------------------
_MISSING_MSG = (
    "Tutor snapshots missing. Run:\n"
    "  python tests/generate_tutor_snapshots.py\n"
    "then commit the generated files before running the test suite."
)

if MANIFEST_PATH.exists():
    for _snap in _load_manifest():
        _qid = str(_snap["question_id"])
        _qtext = _snap.get("question_text", "")
        _method = _make_snapshot_test(_qid, _qtext)
        setattr(TutorSnapshotRegressionTests, _method.__name__, _method)
else:
    def _test_snapshots_missing(self: TutorSnapshotRegressionTests) -> None:
        raise AssertionError(_MISSING_MSG)

    _test_snapshots_missing.__name__ = "test_snapshots_missing"
    _test_snapshots_missing.__doc__ = "Fails clearly when snapshot fixtures have not been generated yet."
    setattr(TutorSnapshotRegressionTests, "test_snapshots_missing", _test_snapshots_missing)


# ---------------------------------------------------------------------------
# Harness integrity tests (always run, do not depend on snapshot content)
# ---------------------------------------------------------------------------

class TutorSnapshotHarnessTests(unittest.TestCase):
    """
    Tests of the snapshot harness itself.

    These run regardless of whether fixtures exist and verify:
    - Governance constant text is unchanged
    - Fixture structure is internally consistent (if fixtures exist)
    - Fixture count matches expected (25)
    """

    def test_disclaimer_es_constant_unchanged(self) -> None:
        """DISCLAIMER_ES must match the exact governance-approved text."""
        self.assertEqual(
            DISCLAIMER_ES,
            "Nota: esta es una respuesta del Tutor, no una calificación oficial "
            "ni una evaluación del Examiner.",
        )

    def test_disclaimer_en_constant_unchanged(self) -> None:
        """DISCLAIMER_EN must match the exact governance-approved text."""
        self.assertEqual(
            DISCLAIMER_EN,
            "Note: this is a Tutor response, not an official grade or an Examiner evaluation.",
        )

    def test_snapshots_root_dir_exists(self) -> None:
        """The fixture directory must exist (at minimum as a .gitkeep placeholder)."""
        self.assertTrue(
            SNAPSHOTS_ROOT.exists(),
            f"Fixture directory missing: {SNAPSHOTS_ROOT}",
        )

    def test_manifest_is_valid_json_when_present(self) -> None:
        """If the manifest exists, it must be valid JSON with required keys."""
        if not MANIFEST_PATH.exists():
            self.skipTest("No manifest yet — fixtures not bootstrapped.")
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertIsInstance(manifest, list, "Manifest must be a JSON array")
        for entry in manifest:
            self.assertIn("question_id", entry, "Each entry must have question_id")
            self.assertIn("question_text", entry, "Each entry must have question_text")
            self.assertFalse(
                entry.get("safe_for_examiner", False),
                f"Manifest entry {entry.get('question_id')} must not set safe_for_examiner=True",
            )

    def test_fixture_dirs_match_manifest(self) -> None:
        """Every manifest entry must have a fixture directory with required files."""
        if not MANIFEST_PATH.exists():
            self.skipTest("No manifest yet — fixtures not bootstrapped.")
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for entry in manifest:
            qid = str(entry["question_id"])
            fixture = SNAPSHOTS_ROOT / qid
            self.assertTrue(fixture.exists(), f"Missing fixture dir for Q{qid}")
            self.assertTrue(
                (fixture / "context_package.json").exists(),
                f"Missing context_package.json for Q{qid}",
            )
            self.assertTrue(
                (fixture / "expected_answer.txt").exists(),
                f"Missing expected_answer.txt for Q{qid}",
            )
            self.assertTrue(
                (fixture / "question.json").exists(),
                f"Missing question.json for Q{qid}",
            )

    def test_snapshot_count_is_25(self) -> None:
        """The full 25-question self-eval suite must produce exactly 25 snapshots."""
        if not MANIFEST_PATH.exists():
            self.skipTest("No manifest yet — fixtures not bootstrapped.")
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            len(manifest),
            25,
            f"Expected exactly 25 snapshots, found {len(manifest)}.\n"
            "If new questions were added to the bank, regenerate:\n"
            "  python tests/generate_tutor_snapshots.py",
        )

    def test_no_safe_for_examiner_in_fixture_context_packages(self) -> None:
        """No frozen context package may contain safe_for_examiner=True."""
        if not MANIFEST_PATH.exists():
            self.skipTest("No manifest yet — fixtures not bootstrapped.")
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        violations: list[str] = []
        for entry in manifest:
            qid = str(entry["question_id"])
            ctx_path = SNAPSHOTS_ROOT / qid / "context_package.json"
            if not ctx_path.exists():
                continue
            ctx = json.loads(ctx_path.read_text(encoding="utf-8"))
            gov = ctx.get("governance") or {}
            if gov.get("safe_for_examiner") is True:
                violations.append(f"Q{qid}")
        self.assertEqual(
            violations,
            [],
            f"Context packages with safe_for_examiner=True: {violations}",
        )

    def test_all_expected_answers_end_with_disclaimer(self) -> None:
        """Every stored golden answer must end with the ES or EN disclaimer."""
        if not MANIFEST_PATH.exists():
            self.skipTest("No manifest yet — fixtures not bootstrapped.")
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        violations: list[str] = []
        for entry in manifest:
            qid = str(entry["question_id"])
            ans_path = SNAPSHOTS_ROOT / qid / "expected_answer.txt"
            if not ans_path.exists():
                continue
            text = ans_path.read_text(encoding="utf-8")
            if not (text.endswith(DISCLAIMER_ES) or text.endswith(DISCLAIMER_EN)):
                violations.append(f"Q{qid}")
        self.assertEqual(
            violations,
            [],
            f"Golden answers missing disclaimer at end: {violations}",
        )

    def test_all_expected_answers_have_headings(self) -> None:
        """Every stored golden answer must contain at least one Markdown heading."""
        if not MANIFEST_PATH.exists():
            self.skipTest("No manifest yet — fixtures not bootstrapped.")
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        violations: list[str] = []
        for entry in manifest:
            qid = str(entry["question_id"])
            ans_path = SNAPSHOTS_ROOT / qid / "expected_answer.txt"
            if not ans_path.exists():
                continue
            text = ans_path.read_text(encoding="utf-8")
            headings = [ln for ln in text.splitlines() if ln.startswith("#")]
            if not headings:
                violations.append(f"Q{qid}")
        self.assertEqual(
            violations,
            [],
            f"Golden answers with no headings: {violations}",
        )

    def test_idempotency_one_question(self) -> None:
        """
        Running build_tutor_answer() twice against the same context package
        must produce identical output (determinism check, independent of fixtures).

        Uses Q1 (flor / crianza biológica) from the attempt directory as a
        lightweight determinism probe. Skips if the attempt directory is absent.
        """
        context_path = ATTEMPTS_ROOT / "1" / "tutor_context_package.json"
        if not context_path.exists():
            self.skipTest("Attempt dir for Q1 not found; skip idempotency probe.")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)

            ctx_copy = tmp_root / "context_package.json"
            ctx_copy.write_bytes(context_path.read_bytes())

            run1 = build_tutor_answer(
                context_package_path=ctx_copy,
                output_path=tmp_root / "run1.md",
                style="standard",
            )
            run2 = build_tutor_answer(
                context_package_path=ctx_copy,
                output_path=tmp_root / "run2.md",
                style="standard",
            )

            answer1 = Path(run1["output_paths"]["latest"]).read_text(encoding="utf-8")
            answer2 = Path(run2["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertEqual(
            answer1,
            answer2,
            "build_tutor_answer() is not deterministic: two runs produced different output.",
        )
        self.assertFalse(run1["governance"]["safe_for_examiner"])
        self.assertFalse(run2["governance"]["safe_for_examiner"])


if __name__ == "__main__":
    unittest.main()
