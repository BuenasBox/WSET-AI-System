# Repair Report — Chapter 11: Wine and the Law

**Generated:** 2026-05-15T19:11:09Z
**Script:** `repair_wine_and_the_law.py`
**Scope:** Surgical repair of subtopic 5.8 extraction failure only

---

## 1. Original Faulty Values

| Field | Value |
|---|---|
| `start_page` | 83 |
| `end_page` | 82 ← **impossible: end < start** |
| `char_count` | 59 (placeholder only) |
| Extraction status | FAILED — end_page < start_page, fallback placeholder written |

**Root cause:** The page-boundary algorithm computed `end_page = next_item.page - 1`. The bookmark for "11 Wine and the Law" was recorded at PDF page 83 (1-indexed), but the next bookmark in the outline ("12 Introduction to France") was indexed at page 84 by the reader, producing `end = 84 - 1 - 1 = 82` — less than start. This caused `extract_text_range()` to iterate zero pages and return empty string, triggering the fallback placeholder.

---

## 2. Corrected Values

| Field | Original | Corrected |
|---|---|---|
| `start_page` | 83 | **83** |
| `end_page` | 82 | **85** |
| `char_count` | 59 | **11398** |
| Extraction status | FAILED | **SUCCESS** |

**Basis for corrected range:**
- Previous chapter (5.7 — Ch.10 Price of Wine): ends page 82
- Next chapter (6.1 — Ch.12 Introduction to France): starts page 86
- Therefore Ch.11 spans pages **83–85** (3 pages)

---

## 3. Source PDF

| Field | Value |
|---|---|
| Path | `C:\Users\esand\OneDrive\Documents\WSET-AI-System\knowledge\official-wset\study-guide\WSET_L3_Study_Guide_Official_2026.pdf` |
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

- ✅ YAML frontmatter present and well-formed
- ✅ Markdown body length: 11,421 characters
- ✅ No placeholder text detected
- ✅ Chapter heading present
- ✅ Page range coherent in frontmatter (83–85)

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
