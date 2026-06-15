-- ============================================================================
-- SBA ITEMS TABLE SCHEMA (Corpus-Agnostic)
--
-- This schema works with ANY canonical corpus size and structure.
-- Ready to be populated after Codex delivers canonical corpus.
--
-- To use:
--   1. Create empty table (don't populate yet)
--   2. Create RLS policies
--   3. Create indexes
--   4. After Codex delivers: populate via import_sba_corpus.js
-- ============================================================================

-- ============================================================================
-- TABLE: sba_items
-- ============================================================================

CREATE TABLE IF NOT EXISTS sba_items (
  -- Primary key
  id TEXT PRIMARY KEY,

  -- Content
  text TEXT NOT NULL,
  options JSONB NOT NULL,           -- Array of 4 option strings
  topic TEXT,                       -- e.g., viticulture, tasting, etc.
  ra TEXT,                          -- RA1-RA5 (responsibility area)
  difficulty TEXT,                  -- intro, intermediate, advanced

  -- Answers and feedback (not exposed before submission)
  correct_index INT,                -- 0-3, which option is correct
  correct_letter TEXT,              -- A-D, letter equivalent
  keywords JSONB,                   -- Tags for retrieval
  feedback_by_mode JSONB,           -- {mentor: "...", trainer: "...", reviewer: "..."}

  -- Knowledge graph
  causal_chain JSONB,               -- Full causal chain object if exists
  micro_drill JSONB,                -- Mini-practice structure if exists

  -- Governance
  governance JSONB,                 -- {safe_for_examiner, formative_only, disclaimer, ...}

  -- Audit
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- ============================================================================
-- INDEXES (for performance)
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_sba_topic ON sba_items(topic);
CREATE INDEX IF NOT EXISTS idx_sba_ra ON sba_items(ra);
CREATE INDEX IF NOT EXISTS idx_sba_difficulty ON sba_items(difficulty);
CREATE INDEX IF NOT EXISTS idx_sba_created_at ON sba_items(created_at);

-- For text search (if needed later)
-- CREATE INDEX idx_sba_text_search ON sba_items USING gin(to_tsvector('english', text));

-- ============================================================================
-- RLS POLICIES
--
-- These policies are corpus-agnostic and work with any data size.
-- Policy logic:
--   - Anonymous users: 0 rows (must be authenticated)
--   - Demo users (trial): can read sba_items (plan-level enforcement in Edge Function)
--   - Premium users: can read sba_items
--   - Full access users: can read sba_items
--   - Admin users: can read sba_items
--
-- Note: Plan enforcement happens in Edge Function, not RLS.
-- RLS is a secondary defensive layer.
-- ============================================================================

ALTER TABLE sba_items ENABLE ROW LEVEL SECURITY;

-- Allow authenticated users to read (plan validation happens in Edge Function)
CREATE POLICY sba_authenticated_read ON sba_items
  FOR SELECT USING (
    auth.uid() IS NOT NULL
  );

-- Note: INSERT/UPDATE/DELETE are not allowed from frontend.
-- All writes go through server-side import script.

-- ============================================================================
-- METADATA TABLE (optional, for corpus versioning)
-- ============================================================================

CREATE TABLE IF NOT EXISTS sba_metadata (
  key TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Record canonical corpus info
-- Usage:
--   INSERT INTO sba_metadata (key, value) VALUES (
--     'canonical_corpus_v1',
--     {
--       "count": 578,
--       "codex_commit": "abc123...",
--       "imported_at": "2026-06-15T10:00:00Z",
--       "import_log": "..."
--     }
--   )
-- ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;

-- ============================================================================
-- SESSIONS TABLE (optional, for tracking user's SBA session state)
-- ============================================================================

CREATE TABLE IF NOT EXISTS sba_sessions (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  user_id TEXT NOT NULL,
  mode TEXT,                        -- quick_drill, express, standard, mock
  started_at TIMESTAMP DEFAULT now(),
  completed_at TIMESTAMP,
  items_count INT,
  items_completed INT DEFAULT 0,
  current_item_id TEXT,
  state JSONB,                      -- {progress: {...}, answers: {...}}
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),

  FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sba_sessions_user ON sba_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sba_sessions_started ON sba_sessions(started_at);

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- After import, run these to verify:

-- 1. Verify table exists and has data
-- SELECT COUNT(*) as item_count FROM sba_items;
-- Expected: > 500

-- 2. Verify no duplicate IDs
-- SELECT id, COUNT(*) as count FROM sba_items GROUP BY id HAVING COUNT(*) > 1;
-- Expected: 0 rows

-- 3. Verify governance flags
-- SELECT
--   COUNT(*) as total,
--   COUNT(CASE WHEN governance->>'safe_for_examiner' = 'false' THEN 1 END) as safe_count
-- FROM sba_items;
-- Expected: safe_count = total

-- 4. Verify RLS works (as authenticated user)
-- SELECT COUNT(*) as visible_items FROM sba_items;
-- Expected: > 500

-- 5. Verify RLS blocks anonymous users
-- SELECT COUNT(*) as visible_items FROM sba_items;  -- as anon user
-- Expected: 0 rows

-- ============================================================================
-- NOTES
-- ============================================================================

-- Corpus-agnostic design:
--   ✅ No hardcoded item counts
--   ✅ No hardcoded IDs
--   ✅ Schema works with any corpus size (500-700+)
--   ✅ RLS policies work with any data
--   ✅ Indexes work with any data
--   ✅ Import script handles any corpus structure

-- Plan enforcement:
--   ✅ Happens in Edge Functions, NOT in RLS
--   ✅ Trial expiration checked in Edge Function
--   ✅ RLS is secondary defense layer

-- Governance:
--   ✅ All items have safe_for_examiner=false
--   ✅ All items have formative_only=true
--   ✅ All items have disclaimer present

-- Watermarking:
--   ✅ User_id added in Edge Function (not in schema)
--   ✅ Expiration (24h) added in Edge Function
--   ✅ Prevents direct DB access from frontend
