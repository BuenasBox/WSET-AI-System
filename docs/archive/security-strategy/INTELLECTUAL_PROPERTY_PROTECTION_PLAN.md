# INTELLECTUAL PROPERTY PROTECTION PLAN — EpistemicLab
**Date**: 2026-06-15 | **Scope**: IP classification, protection strategy, migration roadmap  

---

## EXECUTIVE SUMMARY

EpistemicLab contains **~700+ proprietary items** (SBA questions, OR prompts, SAT wines, causal chains, misconceptions) plus **400+ enrichment assets** and **14 pedagogical IP nodes**. Current public exposure on GitHub creates **redistribution and competitive risk**.

This plan classifies IP by sensitivity, defines protection mechanisms, and provides a phased migration roadmap to move critical assets from public repos to private backends.

**Core Principle**: *Retrieval-first architecture enables separation of "question bank" (private) from "pedagogical engine" (can be public).*

---

## PART 1: IP ASSET CLASSIFICATION

### Tier 1 (CRITICAL — Exam-Sealed)
**Definition**: Exam-adjacent assets that could compromise assessment integrity if leaked to candidates.

| Asset | Count | Status | Protection | Risk Level |
|-------|-------|--------|-----------|-----------|
| **SBA Question Bank** | 578 items | Public JS | **PRIVATE API** | 🔴 CRITICAL |
| **Open Response Corpus** | 106 items | Public JS | **PRIVATE API** | 🔴 CRITICAL |
| **SAT Wine Prompts** | 6 wines | Public JS | **PRIVATE API** | 🔴 CRITICAL |

**Why Private**:
- Candidates could memorize answers if discovered
- Exam security depends on content confidentiality
- Revenue model depends on scarcity of practice items

**Current Exposure**: Directly downloadable via browser DevTools (seconds)

**Migration**: Move all three to authenticated backend API (Supabase RPC + auth token)

---

### Tier 2 (HIGH — Pedagogical IP)
**Definition**: Proprietary teaching frameworks and cognitive models.

| Asset | Count | Status | Protection | Risk Level |
|-------|-------|--------|-----------|-----------|
| **Causal-Chain Framework** | 14 nodes | Public JSON | **PRIVATE API** | 🔴 CRITICAL |
| **Misconception Models** | 20 nodes | Public JSON | **PRIVATE API** | 🔴 CRITICAL |
| **Enrichment Data** | 205 items | Public JSON | **PRIVATE API** | 🟠 HIGH |
| **Mentoring System** | 1 system | Public JS | **PRIVATE API** | 🟠 HIGH |
| **Learner Intelligence Taxonomy** | 1 system | Public JS | **PRIVATE API** | 🟠 HIGH |

**Why Private**:
- Represents years of R&D (visible in 215 doc files)
- Could be reverse-engineered into competing system
- Academic/research value (publishable IP)
- Competitive differentiation

**Current Exposure**: Public in GitHub repos (findable via search)

**Migration**: Move detection + injection logic to backend; serve only matched items to users

---

### Tier 3 (MEDIUM — Operational Details)
**Definition**: System design, configuration, strategy docs that aid reconnaissance.

| Asset | Count | Status | Protection | Risk Level |
|-------|-------|--------|-----------|-----------|
| **Architecture Docs** | 10 files | Public MD | Thin out | 🟠 HIGH |
| **Roadmap & Phase Docs** | 30+ files | Public MD | Remove | 🟠 HIGH |
| **Configuration Files** | 15+ files | Public JSON | Move to .env | 🟡 MEDIUM |
| **Access Control Design** | 5 files | Public JS | Public (needed) | 🟢 LOW |
| **API Contracts** | 10 docs | Public MD | Reference only | 🟡 MEDIUM |

**Why Restrict**:
- Roadmap reveals feature pipeline (competitive advantage)
- Architecture docs aid system cloning
- Phase history shows R&D timeline

**Current Exposure**: 215 docs in /docs/ directory (indexable)

**Migration**: Move strategic docs to private wiki; keep only public API contracts

---

### Tier 4 (LOW — Public-Facing)
**Definition**: Safe-to-disclose architectural principles, API contracts, governance.

| Asset | Status | Reason |
|-------|--------|--------|
| **Governance Flags** (`safe_for_examiner=false`) | Public | Must be transparent (exam safety) |
| **Public API Documentation** | Public | Needed for integration |
| **Security Policy** | Public | Required for trust |
| **Terms of Service** | Public | Legal requirement |
| **README & Getting Started** | Public | Marketing material |

---

## PART 2: CURRENT EXPOSURE INVENTORY

### What's PUBLIC Right Now

**Frontend Repo** (`epistemiclab-dashboard`):
```
├── diagnostic-sba/preguntas_data.js       [Tier 1 CRITICAL]
├── adaptive-session/session_bank.js       [Tier 1 CRITICAL]
├── open-response-lab/lab_payload.js       [Tier 1 CRITICAL]
├── adaptive-session/coach_data.js         [Tier 2 HIGH]
├── adaptive-session/learner_intelligence.js [Tier 2 HIGH]
├── shared/access-control.js               [Tier 3 MEDIUM]
└── docs/*.md                              [Tier 3 MEDIUM]
```

**Backend Repo** (`WSET-AI-System-push`):
```
├── knowledge/knowledge-map/causal-chains/ [Tier 2 CRITICAL]
├── knowledge/knowledge-map/misconceptions/ [Tier 2 CRITICAL]
├── knowledge/question-bank/enrichment/    [Tier 2 HIGH]
├── knowledge/config/                      [Tier 3 MEDIUM]
├── docs/ (215 files)                      [Tier 3 HIGH]
└── tools/ (system code)                   [Tier 4 LOW]
```

**Downloadability**: ALL Tier 1 & 2 assets are trivially downloadable in < 1 minute.

---

## PART 3: PROTECTION MECHANISMS

### Mechanism 1: Retrieval-First Architecture ✓
**Current State**: WSET-AI-System already uses retrieval-first (not generative).

**How It Helps**: 
- Questions can live in private database
- Retrieval engine can be open-source (pedagogically valuable)
- Separation of "content" (private) from "system" (shareable) is native

**Implementation**: Already in place; just needs content API layer

---

### Mechanism 2: Private Backend API
**What**: Move content from public JS files to authenticated backend

**Pattern**:
```
Frontend (public) → API call (auth token) → Supabase RPC → Private content
```

**Benefits**:
- Content never in client JS
- Per-user/per-session content selection
- Rate limiting + access control
- Audit trail

**Scope**:
- [ ] SBA question bank (Tier 1)
- [ ] OR corpus (Tier 1)
- [ ] SAT wines (Tier 1)
- [ ] Causal chains (Tier 2)
- [ ] Misconceptions (Tier 2)
- [ ] Coach data (Tier 2)

---

### Mechanism 3: Repository Privacy
**Option A**: Make repos private
- Pro: All assets protected at source
- Con: Eliminates open-source narrative

**Option B**: Keep public but remove Tier 1-2 assets
- Pro: Maintain transparency (pedagogy code visible)
- Con: Requires careful content curation

**Recommendation**: Option A (private repos) for now; open-source later when differentiation secured

---

### Mechanism 4: License & Copyright Protection
**Current**: Not documented

**Recommended**:
```
LICENSE (proprietary)
├── WSET-AI-System: Proprietary (all rights reserved)
├── epistemiclab-dashboard: Proprietary (all rights reserved)
└── Knowledge assets: Proprietary (copyright © 2026 BuenasBox)

NOTICE.md
├── Causal-chain framework: Patent-pending (2026-06-XX)
├── Misconception models: Copyright (2026)
├── Mentoring system: Proprietary
```

---

### Mechanism 5: Access Control & Licensing
**Current**: Token-based (auth via Supabase)

**Recommended Tiers**:
```
Public (read docs only)
  ↓
Demo (basic SBA: first 5 items)
  ↓
Premium (full SBA + OR, no SAT)
  ↓
Full Access (all content + SAT)
  ↓
Enterprise (custom corpus)
```

**Implementation**: Already partially in place via plan codes

---

### Mechanism 6: Watermarking & Telemetry
**Purpose**: Detect if assets are being shared illegally

**Implementation**:
```javascript
// Not yet implemented
const contentWatermark = {
  recipient_id: "user_12345",
  issued_at: "2026-06-15T10:30:00Z",
  valid_until: "2026-06-22T10:30:00Z",
  usage_rights: "personal_study_only"
};
```

**Privacy Consideration**: Ensure GDPR-compliant telemetry

---

## PART 4: MIGRATION ROADMAP

### Phase S.2 (Safe Hardening) — Weeks 1-2
**Goal**: Move Tier 1 assets to private API; no breaking changes

#### S.2.1: Supabase RPC Layer
```sql
-- Create RPC function to fetch questions
CREATE OR REPLACE FUNCTION get_user_sba_questions(user_id UUID, count INT DEFAULT 25)
RETURNS TABLE (...) AS $$
  SELECT * FROM sba_bank
  WHERE user_id_hash = md5(user_id || 'salt')
  LIMIT count;
$$ LANGUAGE SQL;

-- Implement similar for OR, SAT, enrichment
```

**Implementation**: 
- [ ] Design RPC signatures
- [ ] Migrate data to Supabase Tables
- [ ] Test RLS policies
- [ ] Implement frontend API client

**Risk**: Minimal (API layer added, existing JS remains as fallback)

#### S.2.2: Frontend API Migration
**Old** (public JS):
```javascript
const questions = window.PREGUNTAS_BANK.items;
```

**New** (private API):
```javascript
const response = await fetch('/api/questions', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const questions = await response.json();
```

**Implementation**:
- [ ] Add `/api/questions`, `/api/or-items`, `/api/sat-wines`
- [ ] Implement auth token check
- [ ] Add rate limiting
- [ ] Migrate UI to use API

**Risk**: Medium (requires testing, potential UX disruption)

#### S.2.3: Deprecate Public JS Files
- Keep `preguntas_data.js` but mark as deprecated
- Add comment: "Use `/api/questions` instead (requires auth)"
- Set 1-year deprecation timeline

**Migration Path**:
```
Week 1: API live alongside JS
Week 2: Migrate all routes to API
Week 3: JS file becomes stub
Month 2: Remove JS file
```

#### S.2.4: Causal-Chain Injection API
**Current**: Embedded in content, visible to all

**New**: Served on-demand via RPC
```sql
CREATE OR REPLACE FUNCTION get_matched_causal_chains(question_id INT)
RETURNS TABLE (chain_id TEXT, causa TEXT, mecanismo TEXT, efecto TEXT) AS $$
  SELECT * FROM causal_chains
  WHERE question_id IN (
    SELECT matched_from_question FROM causal_chain_matches
    WHERE question_id = $1
  );
$$ LANGUAGE SQL;
```

**Implementation**:
- [ ] Migrate chains to Supabase table
- [ ] Implement RPC with RLS
- [ ] Frontend requests on-demand
- [ ] Cache locally (1 hour TTL)

---

### Phase S.3 (Private Repos) — Weeks 3-4
**Goal**: Move sensitive docs out of public view; tighten repos

#### S.3.1: Repository Visibility
```
Option 1 (Recommended):
  - Make WSET-AI-System-push PRIVATE
  - Make epistemiclab-dashboard PRIVATE
  - Maintain public mirror with only /tools and /docs (no content)

Option 2 (Progressive):
  - Keep repos public but remove /docs
  - Move strategic docs to private GitHub Wiki
  - Commit sanitized docs only (API contracts, architecture overview)
```

**Implementation**:
- [ ] Create private mirror repo (if needed)
- [ ] Migrate sensitive docs to Wiki
- [ ] Update .gitignore (add /docs, knowledge/* except public)
- [ ] Force-push to remove history (if necessary)

**Risk**: Breaking change for users cloning repos; mitigation = proper communication

#### S.3.2: Documentation Split
**Public Docs** (Keep in repo):
- README.md (project overview)
- ARCHITECTURE.md (high-level system design only)
- API.md (public API contract)
- SECURITY.md (security policy)
- GOVERNANCE.md (governance flags + compliance)
- CONTRIBUTING.md (dev setup)

**Private Docs** (Move to Wiki/Confluence):
- ROADMAP.md (strategic planning)
- PHASE_*.md (internal execution)
- DESIGN_*.md (proprietary design decisions)
- RESEARCH_*.md (research & findings)
- PERFORMANCE_*.md (optimization strategy)

**Implementation**:
- [ ] Review 215 docs; classify each
- [ ] Migrate 100+ strategic docs to private Wiki
- [ ] Keep 10-15 public reference docs
- [ ] Update .gitignore (add /docs except /docs/public/)

---

### Phase S.4 (Longterm) — Ongoing
**Goal**: Formalize IP protection; establish open-source strategy

#### S.4.1: Patent Applications
- Causal-chain framework (pedagogical method)
- Misconception detection system
- Learner intelligence model

**Timeline**: Consult with IP attorney

#### S.4.2: Licensing Strategy
```
Option 1: Proprietary (current)
  - All rights reserved
  - Commercial license required
  - Education license available

Option 2: Hybrid
  - Pedagogy engine: Open-source (AGPL/GPL)
  - Content assets: Proprietary
  - Supabase RPC layer: Open (reference)

Option 3: Academic
  - Educational research license
  - Open for non-commercial use
  - Commercial licensing separate
```

**Recommendation**: Evaluate Option 2 (hybrid) after market traction

#### S.4.3: Open-Source Strategy
**Candidates for open-source** (when IP secured):
- Retrieval engine (`tools/retrieval/`)
- Tutor rendering (`tools/tutor/`)
- Misconception detection (logic, not data)
- SAT reasoning (framework, not wines)
- Causal-chain rendering (architecture, not content)

**Not open-sourceable**:
- Question bank (proprietary)
- Enrichment data (proprietary)
- Mentor profiles (proprietary)
- Strategic docs (competitive)

---

## PART 5: DATA MIGRATION SPECIFICS

### Migration Path for Each Asset

#### SBA Question Bank (578 items)
**Current**: `diagnostic-sba/preguntas_data.js` (public)
**Target**: Supabase table `sba_items` (private, auth-gated)

```sql
CREATE TABLE sba_items (
  id TEXT PRIMARY KEY,
  source_question_id TEXT,
  topic TEXT,
  ra TEXT,
  difficulty TEXT,
  text TEXT,
  options JSONB,
  correct_index INT,
  correct_letter TEXT,
  keywords JSONB,
  gold BOOLEAN,
  governance JSONB,
  causal_chain JSONB,
  feedback_by_mode JSONB,
  micro_drill JSONB,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- RLS Policy: Users can only see items from their subscription tier
ALTER TABLE sba_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY sba_read_policy ON sba_items
  FOR SELECT USING (
    auth.uid() = current_user_id AND
    user_subscription_tier >= required_tier
  );
```

**Data Migration Script**:
```python
import json
import supabase

with open('preguntas_data.js') as f:
  data = json.load(f)
  
for item in data['items']:
  supabase.table('sba_items').insert(item)
```

**Frontend API Change**:
```javascript
// Old
const items = window.PREGUNTAS_BANK.items;

// New
const response = await supabase
  .from('sba_items')
  .select('*')
  .limit(25);
```

#### Causal-Chain Framework (14 nodes)
**Current**: `knowledge/knowledge-map/causal-chains/` (public JSON)
**Target**: Supabase table `causal_chains` + `causal_chain_matches`

```sql
CREATE TABLE causal_chains (
  id TEXT PRIMARY KEY,
  source TEXT, -- 'official' or 'heuristic'
  classification TEXT,
  official BOOLEAN,
  formative_only BOOLEAN,
  causa TEXT,
  mecanismo TEXT,
  efecto TEXT,
  formulacion_examen TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE causal_chain_matches (
  question_id INT,
  chain_id TEXT,
  confidence FLOAT,
  FOREIGN KEY (chain_id) REFERENCES causal_chains(id)
);
```

**Injection Logic** (moves to backend RPC):
```sql
CREATE FUNCTION get_causal_chains_for_question(q_id INT)
RETURNS TABLE (id TEXT, causa TEXT, ...) AS $$
  SELECT cc.* FROM causal_chains cc
  JOIN causal_chain_matches ccm ON cc.id = ccm.chain_id
  WHERE ccm.question_id = $1;
$$ LANGUAGE SQL;
```

#### Misconception Models (20 nodes)
**Current**: `knowledge/knowledge-map/misconceptions/` (public JSON)
**Target**: Supabase table `misconceptions`

```sql
CREATE TABLE misconceptions (
  id TEXT PRIMARY KEY,
  title TEXT,
  description TEXT,
  detection_keywords JSONB,
  detection_signals JSONB,
  intervention_directive TEXT,
  causal_chain_target TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- RLS: Only serve detected misconceptions to user
-- Backend decides if user triggered misconception
```

**Injection Logic** (moves to backend):
- Detection: Stays in backend (`tools/orchestrator/misconception_prepass.py`)
- Delivery: Via private RPC, not public JSON

---

## PART 6: IMPLEMENTATION CHECKLIST

### Pre-Migration
- [ ] Backup all public data
- [ ] Document current API contracts
- [ ] Review RLS policies with Supabase
- [ ] Plan rollback strategy
- [ ] Communicate deprecation timeline

### Phase S.2 (Content API)
- [ ] Design RPC function signatures
- [ ] Create Supabase tables
- [ ] Implement RLS policies
- [ ] Migrate data (SBA, OR, SAT, causal chains, misconceptions)
- [ ] Build frontend API client
- [ ] Add rate limiting & logging
- [ ] Test authentication flow
- [ ] Deploy API alongside old JS
- [ ] Migrate all routes to new API
- [ ] Deprecate old JS files

### Phase S.3 (Repository Privacy)
- [ ] Classify 215 docs
- [ ] Create private GitHub Wiki
- [ ] Migrate strategic docs to Wiki
- [ ] Update .gitignore
- [ ] Set repos to private (or create private mirror)
- [ ] Update README with deprecation notices
- [ ] Announce to users/contributors

### Phase S.4 (Licensing & IP)
- [ ] Consult IP attorney (patents)
- [ ] Draft proprietary LICENSE file
- [ ] Document copyright notices
- [ ] Plan open-source strategy
- [ ] Identify candidates for eventual open-source

---

## PART 7: RISK MITIGATION

### Risk: API Overload from Leaked Keys
**Scenario**: Private API keys exposed, attackers flood requests
**Mitigation**:
- Implement rate limiting (per IP, per user)
- Monitor for unusual request patterns
- Use short-lived tokens (15 min expiry)
- Rotate secrets regularly

### Risk: Data Breach During Migration
**Scenario**: Data exposed during Supabase migration
**Mitigation**:
- Encrypt data in transit (HTTPS)
- Use Supabase backup before migration
- Test in staging environment first
- Have rollback plan ready

### Risk: Breaking Change for Users
**Scenario**: Users cloning old repo can't fetch data
**Mitigation**:
- Deprecation timeline (6-12 months)
- Clear migration guide in README
- API fallback (serve cached data if API unavailable)
- Email notifications to active users

### Risk: Insufficient RLS Configuration
**Scenario**: RLS misconfigured, users see other users' data
**Mitigation**:
- Test RLS in staging with multiple user accounts
- Implement row-level audit logging
- Supabase security review (external audit)
- Query logging + monitoring

---

## PART 8: SUCCESS METRICS

| Metric | Target | Timeline |
|--------|--------|----------|
| **Tier 1 assets in private API** | 100% | End of Phase S.2 (Week 2) |
| **Frontend JS files deprecated** | 100% | End of Phase S.3 (Week 4) |
| **Strategic docs in private Wiki** | 90%+ | End of Phase S.3 (Week 4) |
| **API rate limiting implemented** | ✓ | Week 2 |
| **RLS policies audited** | ✓ | Week 3 |
| **Zero data breaches during migration** | ✓ | Ongoing |
| **Users successfully migrated to API** | 95%+ | Week 4 |
| **Public repo cleanliness** | 0 Tier-1/2 assets | End of Phase S.3 |

---

## GOVERNANCE & COMPLIANCE

| Aspect | Status | Action |
|--------|--------|--------|
| **GDPR (Content)** | Unknown | Supabase audit + data processing agreement |
| **GDPR (Learner Data)** | Unknown | Privacy policy review + RLS verification |
| **Copyright** | Undeclared | Add LICENSE file + copyright notice |
| **Patents** | Potential | Consult IP attorney for causal-chain framework |
| **Commercial Terms** | Needed | Define "personal use" vs "institutional" licensing |
| **Data Retention** | Unknown | Policy needed (delete after 1 year? indefinitely?) |

---

**IP Protection Plan completed**: 2026-06-15  
**Phased migration ready for Phase S.2 implementation**
