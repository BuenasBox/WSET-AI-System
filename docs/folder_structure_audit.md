# WSET-AI-System — Folder Structure Audit Report

**Generated:** 2026-05-13  
**Project root:** `C:\Users\esand\OneDrive\Documents\WSET-AI-System`  
**Performed by:** Claude (Cowork mode) — read-only scan + safe folder creation only

> ✅ **Safety confirmation:** No files were deleted, moved, or overwritten during this operation.  
> All actions were additive only (new folders and new placeholder files created).

---

## 1. Folders Already Present (left untouched)

| Path | Evidence |
|------|----------|
| `knowledge/question-bank/raw/` | Contains `WSET3_Banco_Maestro_V9.xlsx` |
| `knowledge/wine-with-jimmy/config/` | Contains `playlists.json` |
| `docs/` | Contains 7 existing `.md` files (see §5) |
| `prompts/` | Contains `tutor-agent.md`, `examiner-agent.md`, `orchestrator.md` |
| `tools/youtube_transcription/` | Contains Python source files |
| `.git/` | Git repository — not touched |

---

## 2. Folders Created (missing from target structure)

Each was created by writing a `.gitkeep` placeholder file so the directory is tracked by git.

### knowledge/official-wset/
| Folder | Status |
|--------|--------|
| `knowledge/official-wset/specification/` | ✅ Created |
| `knowledge/official-wset/sat/` | ✅ Created |
| `knowledge/official-wset/study-guide/` | ✅ Created |
| `knowledge/official-wset/sample-papers/` | ✅ Created |
| `knowledge/official-wset/mock-exams/` | ✅ Created |
| `knowledge/official-wset/marking-keys/` | ✅ Created |

### knowledge/wine-with-jimmy/ (missing subfolders)
| Folder | Status |
|--------|--------|
| `knowledge/wine-with-jimmy/raw/` | ✅ Created |
| `knowledge/wine-with-jimmy/clean/` | ✅ Created |
| `knowledge/wine-with-jimmy/audio/` | ✅ Created |
| `knowledge/wine-with-jimmy/metadata/` | ✅ Created |
| `knowledge/wine-with-jimmy/index/` | ✅ Created |
| `knowledge/wine-with-jimmy/logs/` | ✅ Created |
| `knowledge/wine-with-jimmy/embeddings/` | ✅ Created |
| `knowledge/wine-with-jimmy/config/` | ⏭ Skipped — already existed |

### knowledge/question-bank/ (missing subfolders)
| Folder | Status |
|--------|--------|
| `knowledge/question-bank/raw/` | ⏭ Skipped — already existed |
| `knowledge/question-bank/structured/` | ✅ Created |
| `knowledge/question-bank/reports/` | ✅ Created |
| `knowledge/question-bank/enrichment/` | ✅ Created |
| `knowledge/question-bank/exports/` | ✅ Created |

### knowledge/ (standalone dirs)
| Folder | Status |
|--------|--------|
| `knowledge/benchmark-answers/` | ✅ Created |
| `knowledge/benchmark-wines/` | ✅ Created |
| `knowledge/calibration/` | ✅ Created |

### knowledge/nazareth/
| Folder | Status |
|--------|--------|
| `knowledge/nazareth/study-patterns/` | ✅ Created |
| `knowledge/nazareth/weak-areas/` | ✅ Created |
| `knowledge/nazareth/distinction-feedback/` | ✅ Created |
| `knowledge/nazareth/mock-history/` | ✅ Created |

### knowledge/enrichment/
| Folder | Status |
|--------|--------|
| `knowledge/enrichment/topic-mapping/` | ✅ Created |
| `knowledge/enrichment/difficulty/` | ✅ Created |
| `knowledge/enrichment/causal-chains/` | ✅ Created |
| `knowledge/enrichment/common-errors/` | ✅ Created |
| `knowledge/enrichment/distinction-notes/` | ✅ Created |

---

## 3. Docs Files

| Target file | Status | Notes |
|-------------|--------|-------|
| `docs/SYSTEM_ARCHITECTURE.md` | ✅ Created (placeholder) | Distinct from existing `system-architecture.md` (hyphen vs underscore) |
| `docs/DATA_GOVERNANCE.md` | ✅ Created (placeholder) | Did not exist |
| `docs/AGENT_BOUNDARIES.md` | ✅ Created (placeholder) | Did not exist |
| `docs/folder_structure_audit.md` | ✅ Created | This file |
| `docs/system-architecture.md` | ⏭ Untouched | Pre-existing file — not overwritten |
| `docs/ARCHITECTURE.md` | ⏭ Untouched | Pre-existing file — not overwritten |
| `docs/AI_CONTRACT.md` | ⏭ Untouched | Pre-existing file — not overwritten |
| `docs/DECISIONS.md` | ⏭ Untouched | Pre-existing file — not overwritten |
| `docs/product-requirements.md` | ⏭ Untouched | Pre-existing file — not overwritten |
| `docs/roadmap.md` | ⏭ Untouched | Pre-existing file — not overwritten |
| `docs/youtube-transcription-ingestion-pipeline.md` | ⏭ Untouched | Pre-existing file — not overwritten |

---

## 4. Potential Duplicates Detected

### docs/ — naming convention inconsistency

Two naming conventions exist side by side in `docs/`:

| Style | Files |
|-------|-------|
| `UPPER_SNAKE_CASE.md` | `AI_CONTRACT.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `SYSTEM_ARCHITECTURE.md` (new), `DATA_GOVERNANCE.md` (new), `AGENT_BOUNDARIES.md` (new) |
| `lower-kebab-case.md` | `system-architecture.md`, `product-requirements.md`, `roadmap.md`, `youtube-transcription-ingestion-pipeline.md` |

⚠️ **Potential semantic overlap:**
- `ARCHITECTURE.md` and `system-architecture.md` and `SYSTEM_ARCHITECTURE.md` may cover the same topic.
- `ARCHITECTURE.md` and `SYSTEM_ARCHITECTURE.md` are different file names on Windows (case-insensitive + different tokens) but serve potentially overlapping purposes.

**Recommended manual action:** Review and consolidate. Consider retiring `system-architecture.md` into `SYSTEM_ARCHITECTURE.md` once the latter is populated, then deleting the old file.

---

## 5. Typos Detected

| Finding | Action taken |
|---------|-------------|
| No `enrichet` folder found | No action needed — folder does not exist |
| No `official` vs `official-wset` duplicate found | No action needed |

---

## 6. Manual Actions Recommended

1. **Consolidate docs naming convention.** Decide on one convention (`UPPER_SNAKE_CASE.md` or `lower-kebab-case.md`) and migrate the older files. Candidate for removal after migration: `system-architecture.md` → content migrated to `SYSTEM_ARCHITECTURE.md`.

2. **Populate placeholder docs.** The three newly created files (`SYSTEM_ARCHITECTURE.md`, `DATA_GOVERNANCE.md`, `AGENT_BOUNDARIES.md`) contain only a header stub. Fill them in before connecting agents.

3. **Stage and commit the new folders in git.** Run:
   ```bash
   git add knowledge/ docs/
   git commit -m "chore: scaffold missing knowledge tree and placeholder docs"
   ```
   This will track all new `.gitkeep` files and the three new docs.

4. **Review `docs/ARCHITECTURE.md` vs `docs/SYSTEM_ARCHITECTURE.md`.** These likely describe the same system from the same author. Merge and delete the redundant file once decided.

5. **Do not delete `.gitkeep` files manually.** They exist solely to keep empty directories tracked by git. Once real files are placed in those directories, `.gitkeep` can be removed via `git rm`.

---

## 7. Safety Confirmation

| Check | Result |
|-------|--------|
| Files deleted | ❌ None |
| Files moved | ❌ None |
| Files overwritten | ❌ None |
| Code touched | ❌ None |
| Educational content modified | ❌ None |
| Folders renamed | ❌ None |
| Existing folders modified | ❌ None |
| New folders created | ✅ 29 |
| New placeholder docs created | ✅ 3 |
| Audit report written | ✅ 1 (this file) |

---

*Generated by Claude (Cowork mode) — additive-only folder scaffold pass*
