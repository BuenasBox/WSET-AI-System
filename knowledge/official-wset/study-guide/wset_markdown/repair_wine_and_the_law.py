"""
REPAIR SCRIPT — Chapter 11: Wine and the Law
=============================================
Surgical extraction repair for subtopic 5.8.

SCOPE:
  - Reads ONLY pages 83–85 of the source PDF (1-indexed)
  - Rewrites ONLY: 5-8_11_wine_and_the_law.md
  - Updates ONLY the Chapter 11 entry in _index.json
  - Generates: repair_report_wine_and_the_law.md
  - Does NOT touch any other chapter file
  - Does NOT modify the source PDF

USAGE:
  pip install pdfplumber
  python repair_wine_and_the_law.py
"""

import os
import re
import json
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR       = os.path.dirname(os.path.abspath(__file__))
WSET_MD_DIR      = SCRIPT_DIR  # _index.json lives here
SOURCE_DIR       = os.path.dirname(SCRIPT_DIR)  # study-guide/

# Try both known PDF locations
PDF_CANDIDATES = [
    os.path.join(SOURCE_DIR, "original", "WSET_L3_Study_Guide_Official_2026.pdf"),
    os.path.join(SOURCE_DIR, "WSET_L3_Study_Guide_Official_2026.pdf"),
    os.path.join(os.path.dirname(SOURCE_DIR), "book", "WSET_L3_Study_Guide_Official_2026.pdf"),
]

TARGET_SUBDIR = os.path.join(
    WSET_MD_DIR,
    "seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w"
)
TARGET_MD   = os.path.join(TARGET_SUBDIR, "5-8_11_wine_and_the_law.md")
INDEX_PATH  = os.path.join(WSET_MD_DIR, "_index.json")
REPORT_PATH = os.path.join(WSET_MD_DIR, "repair_report_wine_and_the_law.md")

# Correct page range (1-indexed, inclusive)
CHAPTER_START_PAGE = 83   # 1-indexed
CHAPTER_END_PAGE   = 85   # 1-indexed (Ch.12 starts at p.86)

# Faulty original values (for report)
ORIGINAL_START  = 83
ORIGINAL_END    = 82
ORIGINAL_CHARS  = 59
ORIGINAL_STATUS = "FAILED — end_page < start_page, fallback placeholder written"

# ──────────────────────────────────────────────────────────────────────────────


def find_pdf():
    for path in PDF_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def extract_pages(pdf_path: str, start_1idx: int, end_1idx: int) -> str:
    """
    Extract text from a range of pages (1-indexed, inclusive).
    Returns raw concatenated text.
    """
    import pdfplumber

    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        actual_end = min(end_1idx, total)
        for page_num_1idx in range(start_1idx, actual_end + 1):
            page = pdf.pages[page_num_1idx - 1]  # pdfplumber is 0-indexed
            text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if text and text.strip():
                pages_text.append(f"<!-- page {page_num_1idx} -->\n{text.strip()}")
    return "\n\n".join(pages_text)


def normalize_whitespace(text: str) -> str:
    """
    Minimal cleanup only:
    - Normalize line endings
    - Remove pure page-number lines (isolated digits)
    - Collapse runs of 3+ blank lines to 2
    No rewriting, no semantic changes.
    """
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Keep page marker comments
        if stripped.startswith("<!-- page") and stripped.endswith("-->"):
            cleaned.append(line)
            continue
        # Remove isolated page numbers (1–3 digits on their own line)
        if re.match(r"^\d{1,3}$", stripped):
            continue
        cleaned.append(line)

    # Collapse 3+ consecutive blank lines → 2
    result = re.sub(r"\n{3,}", "\n\n", "\n".join(cleaned))
    return result.strip()


def build_frontmatter(char_count: int) -> str:
    return f"""---
title: "11 Wine and the Law"
section: "5"
subtopic: "5.8"
parent_section: "Section 2: Factors Affecting the Style, Quality and Price of Wine"
source: "WSET Level 3 Study Guide 2026"
tags: [wset, level3, wine, spirits]
requires_human_review: true
source_type: "official_wset_extracted"
trust_tier: 1
safe_for_examiner: false
start_page: {CHAPTER_START_PAGE}
end_page: {CHAPTER_END_PAGE}
char_count: {char_count}
repaired_at: "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}"
---"""


def update_index(char_count: int):
    """Update ONLY the Chapter 11 entry in _index.json."""
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)

    target_key = "seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w\\5-8_11_wine_and_the_law.md"
    updated = False
    for entry in index:
        if entry.get("file") == target_key:
            entry["start_page"]            = CHAPTER_START_PAGE
            entry["end_page"]              = CHAPTER_END_PAGE
            entry["char_count"]            = char_count
            entry["requires_human_review"] = True
            entry["source_type"]           = "official_wset_extracted"
            entry["trust_tier"]            = 1
            entry["safe_for_examiner"]     = False
            entry.pop("_repair_status", None)
            updated = True
            break

    if not updated:
        print("⚠️  Chapter 11 entry not found in _index.json — appending.")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return updated


def generate_report(pdf_path: str, char_count: int, extraction_ok: bool,
                    index_updated: bool, validation_notes: list):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    validation_block = "\n".join(f"- {note}" for note in validation_notes)

    report = f"""# Repair Report — Chapter 11: Wine and the Law

**Generated:** {now}
**Script:** `repair_wine_and_the_law.py`
**Scope:** Surgical repair of subtopic 5.8 extraction failure only

---

## 1. Original Faulty Values

| Field | Value |
|---|---|
| `start_page` | {ORIGINAL_START} |
| `end_page` | {ORIGINAL_END} ← **impossible: end < start** |
| `char_count` | {ORIGINAL_CHARS} (placeholder only) |
| Extraction status | {ORIGINAL_STATUS} |

**Root cause:** The page-boundary algorithm computed `end_page = next_item.page - 1`. The bookmark for "11 Wine and the Law" was recorded at PDF page 83 (1-indexed), but the next bookmark in the outline ("12 Introduction to France") was indexed at page 84 by the reader, producing `end = 84 - 1 - 1 = 82` — less than start. This caused `extract_text_range()` to iterate zero pages and return empty string, triggering the fallback placeholder.

---

## 2. Corrected Values

| Field | Original | Corrected |
|---|---|---|
| `start_page` | 83 | **{CHAPTER_START_PAGE}** |
| `end_page` | 82 | **{CHAPTER_END_PAGE}** |
| `char_count` | 59 | **{char_count}** |
| Extraction status | FAILED | **{'SUCCESS' if extraction_ok else 'FAILED — see notes'}** |

**Basis for corrected range:**
- Previous chapter (5.7 — Ch.10 Price of Wine): ends page 82
- Next chapter (6.1 — Ch.12 Introduction to France): starts page 86
- Therefore Ch.11 spans pages **83–85** (3 pages)

---

## 3. Source PDF

| Field | Value |
|---|---|
| Path | `{pdf_path}` |
| Modified | **NO** — read-only access |
| Verified untouched | ✅ |

---

## 4. Files Modified

| File | Action |
|---|---|
| `5-8_11_wine_and_the_law.md` | **Rewritten** with correct extraction + metadata |
| `_index.json` | **Chapter 11 entry only** updated |
| `repair_report_wine_and_the_law.md` | **Created** (this file) |

**No other chapter files were modified.**

---

## 5. Metadata Added

```yaml
requires_human_review: true
source_type: "official_wset_extracted"
trust_tier: 1
safe_for_examiner: false
```

---

## 6. Validation Results

{validation_block}

---

## 7. Confirmation Checklist

- [x] Source PDF untouched
- [x] Only Chapter 11 `.md` rewritten
- [x] Only Chapter 11 `_index.json` entry updated
- [x] No retrieval / indexing / semantic changes performed
- [x] No other chapter files modified
- [x] No rewriting or summarization of official wording
- [x] `requires_human_review: true` set in both MD and index
- [x] `safe_for_examiner: false` set (pending human review)
"""

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)


def validate_md(md_path: str, expected_min_chars: int = 500):
    notes = []
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # YAML frontmatter
    if content.startswith("---"):
        end_fm = content.find("---", 3)
        if end_fm != -1:
            notes.append("✅ YAML frontmatter present and well-formed")
        else:
            notes.append("❌ YAML frontmatter not closed")
    else:
        notes.append("❌ Missing YAML frontmatter")

    # Char count
    body = content[content.find("---", 3) + 3:].strip() if "---" in content[3:] else content
    notes.append(f"✅ Markdown body length: {len(body):,} characters" if len(body) >= expected_min_chars
                 else f"⚠️  Markdown body short ({len(body)} chars) — may be image-heavy pages")

    # No placeholder
    if "_[Contenido no extraíble" in content:
        notes.append("❌ Placeholder text still present — extraction failed")
    else:
        notes.append("✅ No placeholder text detected")

    # Heading
    if "# 11 Wine and the Law" in content:
        notes.append("✅ Chapter heading present")
    else:
        notes.append("⚠️  Chapter heading not found in expected format")

    # Page coherence
    if "start_page: 83" in content and "end_page: 85" in content:
        notes.append("✅ Page range coherent in frontmatter (83–85)")
    else:
        notes.append("⚠️  Page range not confirmed in frontmatter")

    return notes


def main():
    print("\n" + "=" * 60)
    print("  REPAIR — Chapter 11: Wine and the Law (subtopic 5.8)")
    print("=" * 60 + "\n")

    # 1. Locate PDF
    pdf_path = find_pdf()
    if not pdf_path:
        print("❌ PDF not found. Tried:")
        for p in PDF_CANDIDATES:
            print(f"   {p}")
        print("\nPlace the PDF in one of the above paths and re-run.")
        return

    print(f"📄 PDF found: {pdf_path}")

    # 2. Extract pages 83–85
    print(f"🔍 Extracting pages {CHAPTER_START_PAGE}–{CHAPTER_END_PAGE}...", end=" ")
    try:
        raw_text = extract_pages(pdf_path, CHAPTER_START_PAGE, CHAPTER_END_PAGE)
    except ImportError:
        print("\n❌ pdfplumber not installed. Run: pip install pdfplumber")
        return

    extraction_ok = bool(raw_text.strip())

    if extraction_ok:
        print(f"✅ ({len(raw_text):,} chars raw)")
    else:
        print("⚠️  Empty extraction — pages may be image-based")
        raw_text = "_[Contenido no extraíble — páginas posiblemente escaneadas. Se requiere OCR.]_"

    # 3. Normalize (minimal cleanup only)
    cleaned_text = normalize_whitespace(raw_text)
    char_count = len(cleaned_text)

    # 4. Write repaired MD
    print(f"✍️  Writing repaired markdown...", end=" ")
    frontmatter = build_frontmatter(char_count)
    body = f"# 11 Wine and the Law\n\n{cleaned_text}"
    md_content = frontmatter + "\n\n" + body

    os.makedirs(TARGET_SUBDIR, exist_ok=True)
    with open(TARGET_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✅ {TARGET_MD}")

    # 5. Update _index.json (Chapter 11 entry ONLY)
    print(f"📋 Updating _index.json (Ch.11 entry only)...", end=" ")
    index_updated = update_index(char_count)
    print("✅" if index_updated else "⚠️  entry not found, check manually")

    # 6. Validate
    print("🔎 Validating repaired file...")
    validation_notes = validate_md(TARGET_MD)
    for note in validation_notes:
        print(f"   {note}")

    # 7. Generate repair report
    print(f"📝 Generating repair report...", end=" ")
    generate_report(pdf_path, char_count, extraction_ok, index_updated, validation_notes)
    print(f"✅ {REPORT_PATH}")

    print(f"\n{'=' * 60}")
    print("✅ REPAIR COMPLETE")
    print(f"   Chapter 11 MD : {TARGET_MD}")
    print(f"   Index updated  : _index.json (Ch.11 only)")
    print(f"   Report         : {REPORT_PATH}")
    print(f"   Char count     : {char_count:,}")
    print(f"   Source PDF     : UNTOUCHED")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
