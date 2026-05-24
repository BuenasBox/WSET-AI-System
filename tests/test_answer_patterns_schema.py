"""Schema validation tests for knowledge/answer_patterns.json.

Every entry must have:
- topic_slug: unique, non-empty string
- patterns_es: non-empty list of strings
- patterns_en: non-empty list of strings
- All 5 response fields present (null is allowed, but the key must exist
  and the value must be str or None — never an unexpected type).
"""

import json
import unittest

from tools.constants import KNOWLEDGE_DIR

RESPONSE_FIELDS = (
    "normal_answer",
    "cause_effect",
    "exam_formulation",
    "mini_practice_prompt",
    "official_idea_hint",
)


def _load_patterns() -> list[dict]:
    path = KNOWLEDGE_DIR / "answer_patterns.json"
    return json.loads(path.read_text(encoding="utf-8"))


class AnswerPatternsSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.entries = _load_patterns()

    # ------------------------------------------------------------------
    # File-level checks
    # ------------------------------------------------------------------

    def test_file_loads_as_list(self) -> None:
        self.assertIsInstance(self.entries, list)
        self.assertGreater(len(self.entries), 0)

    def test_topic_slugs_are_unique(self) -> None:
        slugs = [e.get("topic_slug") for e in self.entries]
        self.assertEqual(len(slugs), len(set(slugs)), "Duplicate topic_slug values found")

    # ------------------------------------------------------------------
    # Per-entry checks (use subTest for granular failure messages)
    # ------------------------------------------------------------------

    def test_each_entry_has_nonempty_topic_slug(self) -> None:
        for i, entry in enumerate(self.entries):
            with self.subTest(index=i, entry=entry.get("topic_slug")):
                slug = entry.get("topic_slug")
                self.assertIsInstance(slug, str)
                self.assertTrue(slug, "topic_slug must not be empty")

    def test_each_entry_has_patterns_es_nonempty_list_of_strings(self) -> None:
        for entry in self.entries:
            with self.subTest(slug=entry.get("topic_slug")):
                patterns = entry.get("patterns_es")
                self.assertIsInstance(patterns, list, "patterns_es must be a list")
                self.assertGreater(len(patterns), 0, "patterns_es must not be empty")
                for p in patterns:
                    self.assertIsInstance(p, str, f"patterns_es item must be str, got {type(p)}")

    def test_each_entry_has_patterns_en_nonempty_list_of_strings(self) -> None:
        for entry in self.entries:
            with self.subTest(slug=entry.get("topic_slug")):
                patterns = entry.get("patterns_en")
                self.assertIsInstance(patterns, list, "patterns_en must be a list")
                self.assertGreater(len(patterns), 0, "patterns_en must not be empty")
                for p in patterns:
                    self.assertIsInstance(p, str, f"patterns_en item must be str, got {type(p)}")

    def test_each_entry_has_all_five_response_fields(self) -> None:
        for entry in self.entries:
            with self.subTest(slug=entry.get("topic_slug")):
                for field in RESPONSE_FIELDS:
                    self.assertIn(
                        field,
                        entry,
                        f"Missing required field '{field}'",
                    )

    def test_each_response_field_is_str_or_none(self) -> None:
        for entry in self.entries:
            with self.subTest(slug=entry.get("topic_slug")):
                for field in RESPONSE_FIELDS:
                    value = entry.get(field)
                    self.assertIsInstance(
                        value,
                        (str, type(None)),
                        f"Field '{field}' must be str or None, got {type(value)}",
                    )

    def test_nonempty_string_fields_are_not_blank(self) -> None:
        """Non-null response fields must not be empty/whitespace-only strings."""
        for entry in self.entries:
            with self.subTest(slug=entry.get("topic_slug")):
                for field in RESPONSE_FIELDS:
                    value = entry.get(field)
                    if value is not None:
                        self.assertTrue(
                            value.strip(),
                            f"Field '{field}' is an empty/whitespace string",
                        )


if __name__ == "__main__":
    unittest.main()
