"""
patch_dashboard_html.py — Surgically patches the three epistemiclab-dashboard HTML pages.

Parts B, C, D, G (from production expansion plan):
  diagnostic-sba/index.html  — replaces QUESTIONS array with full bank + 4-mode selector + nav
  open-response-lab/index.html — updates session picker to 4 modes + nav
  adaptive-session/index.html  — replaces server fetch with client-side bank + SAT modes + nav
"""
import re
from pathlib import Path

DASH = Path(__file__).parent.parent.parent.parent / "epistemiclab-dashboard"
WSET = Path(__file__).parent.parent.parent

NAV_CSS = """
/* ---- Global Navigation ---- */
.global-nav {
  display: flex; align-items: center; justify-content: center;
  gap: 6px; padding: 8px 16px;
  background: var(--raised); border-bottom: 1px solid var(--border); flex-wrap: wrap;
}
.global-nav a {
  color: var(--text-2); text-decoration: none; font-size: 12px;
  padding: 4px 10px; border-radius: 4px; border: 1px solid var(--border);
  transition: color .15s, border-color .15s;
}
.global-nav a:hover { color: #e5c97a; border-color: #7a6230; }
.global-nav a.nav-active { color: #e5c97a; border-color: #7a6230; background: rgba(201,168,76,.08); }
"""

def nav_html(active, extra=""):
    links = [
        ("diagnostic-sba",   "SBA Cockpit",       "/diagnostic-sba/"),
        ("adaptive-session", "Adaptive Session",  "/adaptive-session/"),
        ("open-response-lab","Open Response Lab", "/open-response-lab/"),
    ]
    parts = []
    for key, label, href in links:
        cls = ' class="nav-active"' if key == active else ""
        parts.append(f'<a href="{href}"{cls}>{label}</a>')
    sep = '<span style="color:#525e6e;font-size:10px">·</span>'
    inner = sep.join(parts)
    style = f' style="{extra}"' if extra else ""
    return f'<nav class="global-nav"{style}>{inner}</nav>\n'

# ─────────────────────────────────────────────────────────────
# PART B — Diagnostic SBA
# ─────────────────────────────────────────────────────────────

SBA_OVERLAY_CSS = """
/* ---- Mode Overlay ---- */
.mode-overlay { display:none; position:fixed; inset:0; background:rgba(15,17,21,.96); z-index:500; align-items:center; justify-content:center; }
.mode-overlay.active { display:flex; }
.mode-card { background:var(--panel); border:1px solid var(--border); border-radius:12px; padding:32px 28px; max-width:480px; width:90%; text-align:center; }
.mode-card-eyebrow { font-size:11px; color:#525e6e; letter-spacing:.1em; text-transform:uppercase; margin-bottom:6px; }
.mode-card-title { font-size:22px; font-weight:700; color:#e5c97a; margin-bottom:4px; }
.mode-card-sub { font-size:12px; color:var(--text-2); margin-bottom:24px; }
.mode-buttons { display:flex; flex-direction:column; gap:10px; margin-bottom:20px; }
.mode-btn { background:var(--raised); border:1px solid var(--border); border-radius:8px; padding:14px 16px; cursor:pointer; text-align:left; color:var(--text); transition:border-color .15s,background .15s; }
.mode-btn:hover,.mode-btn.mode-featured { border-color:#7a6230; background:rgba(201,168,76,.06); }
.mode-btn.mode-featured .mode-btn-label { color:#e5c97a; }
.mode-btn-label { display:block; font-size:15px; font-weight:600; }
.mode-btn-count { display:block; font-size:12px; color:var(--text-2); margin-top:2px; }
.mode-btn-detail { display:block; font-size:11px; color:#525e6e; margin-top:2px; }
.mode-disclaimer { font-size:10px; color:#525e6e; }
"""

SBA_OVERLAY_HTML = """<!-- MODE OVERLAY -->
<div id="mode-overlay" class="mode-overlay active">
  <div class="mode-card">
    <div class="mode-card-eyebrow">Diagnostic SBA Cockpit</div>
    <div class="mode-card-title">Selecciona modo</div>
    <div class="mode-card-sub">119 preguntas aprobadas · safe_for_examiner: false</div>
    <div class="mode-buttons">
      <button class="mode-btn" onclick="startMode('quick_drill')">
        <span class="mode-btn-label">Quick Drill</span>
        <span class="mode-btn-count">5 preguntas</span>
      </button>
      <button class="mode-btn" onclick="startMode('express')">
        <span class="mode-btn-label">Express</span>
        <span class="mode-btn-count">10 preguntas</span>
      </button>
      <button class="mode-btn mode-featured" onclick="startMode('standard')">
        <span class="mode-btn-label">Estándar</span>
        <span class="mode-btn-count">25 preguntas</span>
      </button>
      <button class="mode-btn" onclick="startMode('mock_theory_1')">
        <span class="mode-btn-label">Mock Theory · Parte 1</span>
        <span class="mode-btn-count">50 preguntas · distribución oficial WSET</span>
        <span class="mode-btn-detail">RA1=8 · RA2=28 · RA3=5 · RA4=5 · RA5=4</span>
      </button>
    </div>
    <div class="mode-disclaimer">PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET</div>
  </div>
</div>
"""

SBA_QUESTIONS_JS = r"""
// QUESTIONS: dynamic from window.PREGUNTAS_BANK
let QUESTIONS = [];
let ACTIVE_MODE = null;
const SBA_RK = 'wset_sba_recent_v2';
function sbaRecent(){try{return JSON.parse(localStorage.getItem(SBA_RK)||'[]');}catch(e){return[];}}
function sbaSave(ids){try{localStorage.setItem(SBA_RK,JSON.stringify(ids.slice(-60)));}catch(e){}}
function sbaShuf(arr,seed){
  const a=arr.slice();let s=Math.abs(((seed||Date.now()))&0x7fffffff);
  for(let i=a.length-1;i>0;i--){s=(s*1664525+1013904223)&0x7fffffff;const j=s%(i+1);[a[i],a[j]]=[a[j],a[i]];}
  return a;
}
const MOCK_RA={RA1:8,RA2:28,RA3:5,RA4:5,RA5:4};
function bankToQ(item){
  return {
    id:item.id, source_question_id:item.source_question_id,
    topic:item.topic||'—', ra:item.ra||'—', difficulty:item.difficulty||'—',
    cognitive_skill:item.ra?('RA: '+item.ra):'—', est_time:'45–90 s',
    text:item.text||'', options:item.options||[],
    correct_index:typeof item.correct_index==='number'?item.correct_index:0,
    correct_letter:item.correct_letter||'A',
    feedback_by_mode:item.feedback_by_mode||null, causal_chain:item.causal_chain||null,
    distractor_traps:item.distractor_traps||null, misconception:item.misconception||null,
    cross_exam_challenge:item.cross_exam_challenge||null, sat_relevance:item.sat_relevance||null,
    micro_drill:item.micro_drill||null,
  };
}
function loadMode(mode){
  const bank=window.PREGUNTAS_BANK;
  if(!bank||!bank.items){console.error('PREGUNTAS_BANK not loaded');return;}
  ACTIVE_MODE=mode;
  const recent=sbaRecent(); const all=bank.items.slice(); let selected=[];
  if(mode==='mock_theory_1'){
    const byRa={};
    all.forEach(i=>{const r=i.ra||'RA1';(byRa[r]=byRa[r]||[]).push(i);});
    Object.entries(MOCK_RA).forEach(([ra,need])=>{
      const pool=sbaShuf(byRa[ra]||[],Date.now()+ra.charCodeAt(2));
      const fresh=pool.filter(i=>!recent.includes(i.source_question_id));
      const stale=pool.filter(i=>recent.includes(i.source_question_id));
      selected.push(...[...fresh,...stale].slice(0,need));
    });
    selected=sbaShuf(selected,Date.now());
  } else {
    const size={quick_drill:5,express:10,standard:25}[mode]||10;
    const fresh=sbaShuf(all.filter(i=>!recent.includes(i.source_question_id)),Date.now());
    const stale=sbaShuf(all.filter(i=>recent.includes(i.source_question_id)),Date.now()+1);
    selected=[...fresh,...stale].slice(0,size);
  }
  QUESTIONS=selected.map(bankToQ);
  sbaSave([...recent,...QUESTIONS.map(q=>q.source_question_id)]);
}
function startMode(mode){
  loadMode(mode);
  document.getElementById('mode-overlay').classList.remove('active');
  STATE.stage='prepare'; STATE.questionIndex=0;
  STATE.selectedOption=null; STATE.selectedConfidence=null; STATE.selectedTag=null;
  render();
}
"""

SBA_RESTART_OLD = "function restartSession() {\n  STATE.stage = 'prepare';\n  STATE.questionIndex = 0;\n  STATE.selectedOption = null;\n  STATE.selectedConfidence = null;\n  STATE.selectedTag = null;\n  STATE.crossChanged = false;\n  STATE.drillSelectedOption = null;\n  STATE.drillSubmitted = false;\n  STATE.session = { answered:0, correct:0, overconfident:0, hesitated:0, causalWeakness:0, trapSusceptibility:0 };\n  resetConfGauge();\n  setCausalBars(0);\n  activateMisconGlyph(false);\n  document.querySelectorAll('.hes-dot').forEach(d => d.classList.remove('triggered'));\n  document.getElementById('hesLabel').textContent = '—';\n  render();\n  window.scrollTo({top:0,behavior:'smooth'});\n}"

SBA_RESTART_NEW = "function restartSession() {\n  STATE.crossChanged=false; STATE.drillSelectedOption=null; STATE.drillSubmitted=false;\n  STATE.session={answered:0,correct:0,overconfident:0,hesitated:0,causalWeakness:0,trapSusceptibility:0};\n  resetConfGauge(); setCausalBars(0); activateMisconGlyph(false);\n  document.querySelectorAll('.hes-dot').forEach(d=>d.classList.remove('triggered'));\n  document.getElementById('hesLabel').textContent='—';\n  document.getElementById('mode-overlay').classList.add('active');\n  window.scrollTo({top:0,behavior:'smooth'});\n}"

def patch_sba(c):
    # 1. CSS + script tag
    c = c.replace('</style>\n</head>', SBA_OVERLAY_CSS + NAV_CSS + '</style>\n<script src="preguntas_data.js"></script>\n</head>')
    # 2. Nav + overlay after progress bar
    PB = '<div class="progress-bar-wrap"><div class="progress-bar" id="progressBar"></div></div>'
    c = c.replace(PB, PB + '\n' + nav_html("diagnostic-sba") + SBA_OVERLAY_HTML)
    # 3. Replace QUESTIONS array
    qs = c.find('const QUESTIONS = [')
    qe = c.find('];', qs) + 2
    c = c[:qs] + SBA_QUESTIONS_JS + c[qe:]
    # 4. Resilient feedback_by_mode
    c = c.replace(
        'const feedback = q.feedback_by_mode[STATE.mentorMode] || q.feedback_by_mode.mentor;',
        'const _fbm=q.feedback_by_mode||{}; const feedback=_fbm[STATE.mentorMode]||_fbm.mentor||\'Repasa el concepto relacionado con esta pregunta.\';'
    )
    # 5. Causal chain field guards
    for f in ['causa','mecanismo','efecto']:
        c = c.replace(f'${{q.causal_chain.{f}}}',      f'${{(q.causal_chain&&q.causal_chain.{f})||"—"}}')
        c = c.replace(f'escapeHtml(q.causal_chain.{f})', f'escapeHtml((q.causal_chain&&q.causal_chain.{f})||"—")')
    # 6. Other rich fields
    rf = [('distractor_traps','\'—\''),('misconception','\'—\''),('sat_relevance','\'—\''),
          ('cross_exam_challenge','\'¿Tu razonamiento cubre causa, mecanismo y efecto?\'')]
    for field, fb in rf:
        c = c.replace(f'escapeHtml(q.{field})', f'escapeHtml(q.{field}||{fb})')
        c = c.replace(f'${{q.{field}}}',         f'${{q.{field}||"—"}}')
    # 7. micro_drill null guard
    c = c.replace('const drill = q.micro_drill;', 'const drill=q.micro_drill||null;\n  if(!drill){goToRead();return;}')
    # 8. Replace restartSession
    c = c.replace(SBA_RESTART_OLD, SBA_RESTART_NEW)
    # 9. DOMContentLoaded no-op
    c = c.replace(
        "document.addEventListener('DOMContentLoaded', function() {\n  render();\n});",
        "document.addEventListener('DOMContentLoaded',function(){\n  // Mode overlay visible; quiz starts on mode selection.\n});"
    )
    # 10. Footer nav
    c = c.replace('</body>', nav_html("diagnostic-sba","margin-top:12px") + '</body>')
    return c

# ─────────────────────────────────────────────────────────────
# PART C — Open Response Lab
# ─────────────────────────────────────────────────────────────

ORL_BTN_OLD = ('<button type="button" data-session="short" aria-pressed="true">Corta · 3</button>\n'
               '        <button type="button" data-session="standard" aria-pressed="false">Estándar · 5</button>\n'
               '        <button type="button" data-session="long" aria-pressed="false">Larga · 10</button>')

ORL_BTN_NEW = ('<button type="button" data-session="short_practice" aria-pressed="true">Short Practice · 1</button>\n'
               '        <button type="button" data-session="standard_practice" aria-pressed="false">Standard Practice · 2</button>\n'
               '        <button type="button" data-session="extended_practice" aria-pressed="false">Extended Practice · 4</button>\n'
               '        <button type="button" data-session="mock_theory_2" aria-pressed="false">Mock Theory Part 2 · 4</button>')

def patch_orl(c):
    c = c.replace('</style>', NAV_CSS + '</style>', 1)
    # nav after <body>
    bi = c.find('<body>')
    if bi >= 0: c = c[:bi+6] + '\n' + nav_html("open-response-lab") + c[bi+6:]
    c = c.replace(ORL_BTN_OLD, ORL_BTN_NEW)
    c = c.replace('aria-label="Tamaño de sesión"', 'aria-label="Modo de sesión"')
    c = c.replace(
        'Runtime local privado para práctica formativa de respuesta abierta.',
        '26 preguntas aprobadas · 4 modos de práctica · safe_for_examiner: false'
    )
    c = c.replace('</body>', nav_html("open-response-lab","margin-top:12px") + '</body>')
    return c

# ─────────────────────────────────────────────────────────────
# PART D — Adaptive Session
# ─────────────────────────────────────────────────────────────

ADP_EXTRA_CSS = """
/* ---- Adaptive Mode Overlay ---- */
.adp-ol{display:none;position:fixed;inset:0;background:rgba(15,17,21,.97);z-index:500;align-items:center;justify-content:center;padding:20px;}
.adp-ol.active{display:flex;}
.adp-card{background:#171b22;border:1px solid #252c38;border-radius:12px;padding:28px 24px;max-width:520px;width:100%;}
.adp-eyebrow{font-size:11px;color:#525e6e;letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px;}
.adp-title{font-size:20px;font-weight:700;color:#e5c97a;margin-bottom:4px;}
.adp-sub{font-size:12px;color:#a7b0be;margin-bottom:14px;}
.adp-slabel{font-size:11px;color:#a7b0be;letter-spacing:.05em;text-transform:uppercase;margin:14px 0 7px;padding-left:8px;border-left:2px solid #c9a84c;}
.adp-btns{display:flex;flex-direction:column;gap:7px;}
.adp-btn{background:#1e2430;border:1px solid #252c38;border-radius:7px;padding:11px 14px;cursor:pointer;text-align:left;color:#f5f7fa;transition:border-color .15s;}
.adp-btn:hover{border-color:#7a6230;}
.adp-btn.adp-sat{border-color:#4a3e8c;}
.adp-btn.adp-sat:hover{background:rgba(139,124,246,.07);border-color:#7b6df5;}
.adp-blabel{display:block;font-size:14px;font-weight:600;}
.adp-bsub{display:block;font-size:11px;color:#a7b0be;margin-top:2px;}
.adp-disc{font-size:10px;color:#525e6e;text-align:center;margin-top:14px;}
"""

ADP_OVERLAY_HTML = """<!-- ADAPTIVE MODE OVERLAY -->
<div id="adp-ol" class="adp-ol active">
  <div class="adp-card">
    <div class="adp-eyebrow">Adaptive Session</div>
    <div class="adp-title">Selecciona modo</div>
    <div class="adp-sub">119 preguntas SBA + 6 prompts SAT · safe_for_examiner: false</div>
    <div class="adp-slabel">Teoría · SBA</div>
    <div class="adp-btns">
      <button class="adp-btn" onclick="startAdp('express_10')"><span class="adp-blabel">Express · 10</span><span class="adp-bsub">10 preguntas · ~15 min</span></button>
      <button class="adp-btn" onclick="startAdp('standard_25')"><span class="adp-blabel">Estándar · 25</span><span class="adp-bsub">25 preguntas · ~35 min</span></button>
      <button class="adp-btn" onclick="startAdp('mock_theory_50')"><span class="adp-blabel">Mock Theory Part 1 · 50</span><span class="adp-bsub">RA1=8 · RA2=28 · RA3=5 · RA4=5 · RA5=4 · ~75 min</span></button>
    </div>
    <div class="adp-slabel">Cata SAT</div>
    <div class="adp-btns">
      <button class="adp-btn adp-sat" onclick="startAdp('sat_sprint')"><span class="adp-blabel">SAT Sprint</span><span class="adp-bsub">1 vino · práctica rápida</span></button>
      <button class="adp-btn adp-sat" onclick="startAdp('sat_practice')"><span class="adp-blabel">SAT Practice</span><span class="adp-bsub">2 vinos · práctica completa</span></button>
      <button class="adp-btn adp-sat" onclick="startAdp('sat_mock')"><span class="adp-blabel">SAT Mock Exam</span><span class="adp-bsub">2 vinos · 30 min · simulación examen</span></button>
    </div>
    <div class="adp-disc">PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET</div>
  </div>
</div>
"""

ADP_SAT_SCREEN = """<!-- SCREEN SAT -->
<div id="screen-sat" class="screen" role="main" aria-label="Práctica SAT">
  <div class="content" id="sat-content"></div>
</div>
"""

ADP_BANK_JS = r"""
// ═══════════════════════════════════════════════════════════
// SESSION BANK CLIENT (window.SESSION_BANK from session_bank.js)
// ═══════════════════════════════════════════════════════════
const ADP_RK='wset_adp_recent_v2';
const ADP_MRA={RA1:8,RA2:28,RA3:5,RA4:5,RA5:4};
function adpRec(){try{return JSON.parse(localStorage.getItem(ADP_RK)||'[]');}catch(e){return[];}}
function adpSav(ids){try{localStorage.setItem(ADP_RK,JSON.stringify(ids.slice(-80)));}catch(e){}}
function adpShuf(arr,salt){
  const a=arr.slice();let s=Math.abs(((salt||Date.now()))&0x7fffffff);
  for(let i=a.length-1;i>0;i--){s=(s*1664525+1013904223)&0x7fffffff;const j=s%(i+1);[a[i],a[j]]=[a[j],a[i]];}
  return a;
}
function buildSBA(mode){
  const bk=window.SESSION_BANK;
  if(!bk||!bk.sba_items){console.error('SESSION_BANK missing');return null;}
  const all=bk.sba_items, rec=adpRec(); let sel=[];
  if(mode==='mock_theory_50'){
    const byRa={};
    all.forEach(i=>{const r=i.ra||'RA1';(byRa[r]=byRa[r]||[]).push(i);});
    Object.entries(ADP_MRA).forEach(([ra,n])=>{
      const pool=adpShuf(byRa[ra]||[],ra.charCodeAt(2));
      sel.push(...[...pool.filter(i=>!rec.includes(i.source_question_id)),...pool.filter(i=>rec.includes(i.source_question_id))].slice(0,n));
    });
    sel=adpShuf(sel,42);
  } else {
    const sz={express_10:10,standard_25:25}[mode]||10;
    sel=[...adpShuf(all.filter(i=>!rec.includes(i.source_question_id)),1),...adpShuf(all.filter(i=>rec.includes(i.source_question_id)),2)].slice(0,sz);
  }
  adpSav([...rec,...sel.map(i=>i.source_question_id)]);
  const ml={express_10:'EXPRESS_10',standard_25:'STANDARD_25',mock_theory_50:'MOCK_THEORY_50'}[mode]||mode;
  return {
    generated_at:new Date().toISOString(), session_mode:ml,
    pool_size:all.length, pool_source:'session_bank_v1', target_size:sel.length,
    governance:{safe_for_examiner:false,examiner_scoring_allowed:false,training_item_only:true},
    mission_briefing:{strong_areas:[],weak_areas:[],active_misconceptions:[],causal_gaps:[],
      session_objective:'Sesión de entrenamiento formativo WSET L3'},
    questions:sel.map(i=>({
      question_id:i.id, priority_score:1, stem:i.text,
      options:(i.options||[]).map((t,x)=>({label:['A','B','C','D'][x]||String(x),text:t})),
      correct_answer:i.correct_letter||'A', topic:i.topic||'—', ra_id:i.ra||'—',
      difficulty:i.difficulty||'—', challenge_type:'theory_foundation',
      feedback:'Repasa el concepto relacionado con esta pregunta.',
    }))
  };
}
function buildSAT(mode){
  const bk=window.SESSION_BANK;
  if(!bk||!bk.sat_prompts){console.error('SESSION_BANK missing sat_prompts');return null;}
  const cnt=(mode==='sat_sprint')?1:2;
  const sel=adpShuf(bk.sat_prompts,Date.now()).slice(0,cnt);
  return {type:'sat',mode,duration_minutes:mode==='sat_mock'?30:null,wines:sel,
    governance:{safe_for_examiner:false,examiner_scoring_allowed:false,training_item_only:true}};
}

let _satTmr=null, _satSec=0;

function startAdp(mode){
  document.getElementById('adp-ol').classList.remove('active');
  if(mode.startsWith('sat_')){
    STATE.satPayload=buildSAT(mode); STATE.satWineIdx=0;
    showScreen('screen-sat'); renderSAT();
    if(STATE.satPayload&&STATE.satPayload.duration_minutes){
      _satSec=STATE.satPayload.duration_minutes*60; clearInterval(_satTmr);
      _satTmr=setInterval(()=>{
        _satSec=Math.max(0,_satSec-1);
        const el=document.getElementById('sat-timer');
        if(el){const m=Math.floor(_satSec/60),s=_satSec%60;el.textContent=m+':'+String(s).padStart(2,'0');el.style.color=_satSec<120?'#e45c5c':'#c9a84c';}
        if(!_satSec)clearInterval(_satTmr);
      },1000);
    }
  } else {
    STATE.payload=buildSBA(mode); STATE.screen=0; STATE.qIdx=0; STATE.selected=null; STATE.confirmed=false;
    showScreen('screen-0'); renderScreen0();
  }
}

function renderSAT(){
  const p=STATE.satPayload; if(!p)return;
  const wines=p.wines||[], idx=STATE.satWineIdx||0, wine=wines[idx], el=document.getElementById('sat-content');
  if(!wine||!el)return;
  const tot=wines.length, dur=p.duration_minutes;
  el.innerHTML=`<div style="max-width:640px;margin:0 auto;padding:24px 0">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px">
      <div><div style="font-size:11px;color:#525e6e;letter-spacing:.1em;text-transform:uppercase">Cata SAT · Vino ${idx+1} de ${tot}</div>
      <div style="font-size:18px;font-weight:700;color:#e5c97a;margin-top:4px">${escapeHtml(wine.wine_name)}</div></div>
      ${dur?`<div style="text-align:right"><div style="font-size:10px;color:#525e6e">Tiempo restante</div><div id="sat-timer" style="font-size:20px;font-weight:700;color:#c9a84c">${dur}:00</div></div>`:''}
    </div>
    <div style="background:#1e2430;border:1px solid #252c38;border-radius:8px;padding:16px;margin-bottom:14px">
      <div style="font-size:11px;color:#a7b0be;margin-bottom:8px">DESCRIPCIÓN</div>
      <div style="font-size:13px;color:#f5f7fa;line-height:1.6">${escapeHtml(wine.description)}</div>
    </div>
    <div style="background:#1e2430;border:1px solid #252c38;border-radius:8px;padding:16px;margin-bottom:14px">
      <div style="font-size:11px;color:#a7b0be;margin-bottom:8px">TU ANÁLISIS SAT</div>
      <div style="font-size:12px;color:#525e6e;margin-bottom:8px">Orden WSET: Aspecto → Nariz → Boca → Conclusiones</div>
      <textarea id="sat-resp-${wine.prompt_id}" style="width:100%;min-height:160px;background:#0f1115;border:1px solid #252c38;border-radius:6px;color:#f5f7fa;font-size:13px;padding:12px;font-family:inherit;resize:vertical;box-sizing:border-box"
        placeholder="ASPECTO: [intensidad] [color]&#10;NARIZ: [intensidad] · [aromas]&#10;BOCA: [dulzor] · [acidez] · [tanino] · [alcohol] · [cuerpo] · [sabores] · [final]&#10;CONCLUSIONES: [calidad] · [potencial]"></textarea>
    </div>
    <div style="background:rgba(201,168,76,.07);border:1px solid #7a6230;border-radius:8px;padding:12px;margin-bottom:16px">
      <div style="font-size:11px;color:#c9a84c;margin-bottom:4px">NOTA FORMATIVA</div>
      <div style="font-size:12px;color:#a7b0be">${escapeHtml(wine.training_note)}</div>
    </div>
    <div style="display:flex;gap:10px;justify-content:flex-end">
      ${idx+1<tot
        ?`<button onclick="STATE.satWineIdx++;renderSAT();window.scrollTo({top:0,behavior:'smooth'})" style="background:#1e2430;border:1px solid #7a6230;border-radius:6px;padding:9px 20px;color:#e5c97a;cursor:pointer;font-size:13px">Siguiente →</button>`
        :`<button onclick="finishSAT()" style="background:#1e2430;border:1px solid #2ec27e;border-radius:6px;padding:9px 20px;color:#2ec27e;cursor:pointer;font-size:13px">Finalizar ✓</button>`}
    </div>
  </div>`;
}

function finishSAT(){
  clearInterval(_satTmr);
  document.getElementById('sat-content').innerHTML=`<div style="text-align:center;padding:60px 20px">
    <div style="font-size:40px;margin-bottom:14px">✓</div>
    <div style="font-size:18px;font-weight:700;color:#e5c97a;margin-bottom:8px">Práctica SAT completada</div>
    <div style="font-size:12px;color:#a7b0be;margin-bottom:22px">Entrenamiento formativo. Evaluación oficial requiere Examiner WSET acreditado.</div>
    <button onclick="document.getElementById('adp-ol').classList.add('active')" style="background:#1e2430;border:1px solid #7a6230;border-radius:6px;padding:9px 20px;color:#e5c97a;cursor:pointer;font-size:13px">← Nueva sesión</button>
  </div>`;
}

"""

def patch_adaptive(c):
    # 1. CSS + session_bank.js
    c = c.replace('</style>\n</head>', ADP_EXTRA_CSS + NAV_CSS + '</style>\n<script src="session_bank.js"></script>\n</head>')
    # 2. Nav + overlay before first HTML comment block (<!-- ===)
    fc = c.find('<!-- ===')
    if fc >= 0: c = c[:fc] + nav_html("adaptive-session") + ADP_OVERLAY_HTML + '\n' + c[fc:]
    # 3. SAT screen before JS comment
    js_cmt = '<!-- =========================================================\n     JAVASCRIPT'
    c = c.replace(js_cmt, ADP_SAT_SCREEN + '\n' + js_cmt)
    # 4. satPayload/satWineIdx in STATE
    c = c.replace('const STATE = {\n  payload:    null,', 'const STATE = {\n  payload:    null,\n  satPayload: null,\n  satWineIdx: 0,')
    # 5. Bank JS before init()
    ii = c.find('async function init()')
    if ii >= 0: c = c[:ii] + ADP_BANK_JS + c[ii:]
    # 6. Patch init() fetch to no-op
    c = c.replace(
        "const res = await fetch('../session_data/session_payload.json');",
        "// Session built client-side; no fetch needed.\n    return;"
    )
    # 7. DOMContentLoaded no-op
    c = c.replace(
        "document.addEventListener('DOMContentLoaded', init);",
        "document.addEventListener('DOMContentLoaded',function(){/* mode overlay visible */});"
    )
    # 8. Footer nav
    c = c.replace('</body>', nav_html("adaptive-session","margin-top:12px") + '</body>')
    return c


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
def main():
    import shutil

    sba_src = DASH / "diagnostic-sba" / "index.html"
    c = sba_src.read_text(encoding="utf-8")
    cp = patch_sba(c)
    sba_src.write_text(cp, encoding="utf-8")
    print(f"[OK] Diagnostic SBA: {len(c):,} → {len(cp):,} chars")

    orl_src = DASH / "open-response-lab" / "index.html"
    c = orl_src.read_text(encoding="utf-8")
    cp = patch_orl(c)
    orl_src.write_text(cp, encoding="utf-8")
    print(f"[OK] Open Response Lab: {len(c):,} → {len(cp):,} chars")

    adp_src = DASH / "adaptive-session" / "index.html"
    c = adp_src.read_text(encoding="utf-8")
    cp = patch_adaptive(c)
    adp_src.write_text(cp, encoding="utf-8")
    print(f"[OK] Adaptive Session: {len(c):,} → {len(cp):,} chars")

    copies = [
        (WSET/"frontend"/"diagnostic-sba"/"preguntas_data.js",  DASH/"diagnostic-sba"/"preguntas_data.js"),
        (WSET/"frontend"/"open-response-lab"/"lab_payload.js",  DASH/"open-response-lab"/"lab_payload.js"),
        (WSET/"frontend"/"adaptive-session"/"session_bank.js",  DASH/"adaptive-session"/"session_bank.js"),
    ]
    for src, dst in copies:
        if src.exists():
            shutil.copy2(src, dst)
            print(f"[OK] Copied {src.name} ({src.stat().st_size:,}b) → {dst.parent.name}/")
        else:
            print(f"[WARN] Missing: {src}")

    print("\nAll patches applied.")

if __name__ == "__main__":
    main()
