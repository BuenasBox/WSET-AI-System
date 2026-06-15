/**
 * gate.mjs — Headless pre-deploy regression gate for epistemiclab-dashboard.
 * Phase Z.2 production stabilization. Run BEFORE every deploy/push of the dashboard.
 *
 * Usage:
 *   DASHBOARD_ROOT=/path/to/epistemiclab-dashboard node gate.mjs
 * Requires: npm i puppeteer-core @sparticuz/chromium  (or set CHROME_PATH to a local Chrome)
 *
 * Gates (all must PASS):
 *   G1  File integrity: every HTML ends with </html>; every inline <script> parses
 *   G2  ORL: 4 session modes render stem/counter (1/2/4/4), full walk, finish, restart, 0 page errors
 *   G3  Adaptive SBA: 3 modes reach INICIAR MISIÓN; full express walk: unique IDs, 4 options, debrief
 *   G4  Adaptive SAT: 3 modes render wine + complete
 *   G5  Diagnostic SBA: full quick_drill advances q1→q5→map (no TRAIN loop), 0 page errors
 *   G6  Navigation: every nav link clear of overlays (elementFromPoint) + real click navigates
 *   G7  No placebo: no "—"-only feedback panels; question-specific guidance text
 *   G8  Localization: no English mode/nav labels in learner-visible text
 */
import fs from 'fs'; import path from 'path'; import http from 'http';
const ROOT = process.env.DASHBOARD_ROOT || path.resolve(process.cwd(), '../../../..', 'epistemiclab-dashboard');
const PORT = Number(process.env.GATE_PORT || 8077);
let chromium=null, puppeteer;
try { chromium = (await import('@sparticuz/chromium')).default; } catch {}
puppeteer = (await import('puppeteer-core')).default;

const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css'};
const server=http.createServer((req,res)=>{ let u=decodeURIComponent(req.url.split('?')[0]); if(u.endsWith('/'))u+='index.html';
  fs.readFile(path.join(ROOT,u),(e,d)=>{ if(e){res.writeHead(404);res.end();} else {res.writeHead(200,{'Content-Type':MIME[path.extname(u)]||'application/octet-stream'});res.end(d);} });});
await new Promise(r=>server.listen(PORT,r));
const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH || (chromium ? await chromium.executablePath() : undefined),
  args: chromium ? chromium.args : ['--no-sandbox'], headless: true });

const RELEASE_SCOPE=process.env.RELEASE_SCOPE||'full';
const WANT=(process.env.GATES||'').split(',').filter(Boolean);
const SBA_RELEASE_GATES=new Set(['G1','G3','G4','G5','G6','G7','G8','G9']);
const want=g=>WANT.length?WANT.includes(g):(RELEASE_SCOPE==='sba-corpus'?SBA_RELEASE_GATES.has(g):true);
const results=[]; const fail=(g,msg)=>results.push({gate:g, pass:false, msg});
const pass=(g,msg)=>results.push({gate:g, pass:true, msg});
const skip=(g,msg)=>results.push({gate:g, pass:true, skipped:true, msg});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function fresh(p,u){ await p.goto(`http://localhost:${PORT}${u}`,{waitUntil:'networkidle0'}); await p.evaluate(()=>localStorage.clear()); p._errs.length=0; await p.goto(`http://localhost:${PORT}${u}`,{waitUntil:'networkidle0'}); }
function track(p){ p._errs=[]; p.on('pageerror',e=>p._errs.push(String(e))); return p; }

if(RELEASE_SCOPE==='sba-corpus'&&!WANT.length) skip('G2','Open Response assets unchanged; excluded from SBA corpus release scope');

/* G1 — integrity */
if(want('G1')){
  let ok=true, msgs=[];
  for (const f of ['index.html','diagnostic-sba/index.html','adaptive-session/index.html','open-response-lab/index.html','full-simulation/index.html']){
    const s=fs.readFileSync(path.join(ROOT,f),'utf8');
    if(!/<\/html>\s*$/.test(s.trimEnd())){ok=false;msgs.push(f+' missing </html> (file truncation?)');}
    for(const m of s.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)){ try{new Function(m[1]);}catch(e){ok=false;msgs.push(f+' inline script: '+e.message);} }
  }
  ok?pass('G1','all files intact, scripts parse'):fail('G1',msgs.join(' | '));
}
const p = track(await browser.newPage());

/* G2 — ORL */
if(want('G2'))try{
  await fresh(p,'/open-response-lab/');
  const sizes={short_practice:1,standard_practice:2,extended_practice:4,mock_theory_2:4}; let ok=true,msg=[];
  for(const [mode,size] of Object.entries(sizes)){
    await p.click(`button[data-session="${mode}"]`); await sleep(150);
    const r=await p.evaluate(()=>({pos:document.querySelector("[data-testid='question-position']").textContent, stem:document.querySelector("[data-testid='question-stem']").textContent.length}));
    if(r.pos!==`Pregunta 1 de ${size}`||r.stem<10){ok=false;msg.push(mode+':'+r.pos+' stemLen:'+r.stem);}
  }
  await p.click(`button[data-session="extended_practice"]`); await sleep(150);
  for(let i=0;i<4;i++){ await p.evaluate(()=>{document.getElementById('answer').value='Prueba de SO2 y oxidación.';}); await p.click('#submit-answer'); await sleep(120); if(i<3){await p.click('#next-question'); await sleep(120);} }
  await p.click('#finish-session'); await sleep(120);
  const done=await p.evaluate(()=>!document.querySelector("[data-testid='completion-panel']").hidden);
  if(!done){ok=false;msg.push('finish failed');}
  if(p._errs.length){ok=false;msg.push('pageerrors:'+p._errs[0]);}
  ok?pass('G2','ORL 4 modes + full walk + finish'):fail('G2',msg.join(' | '));
}catch(e){fail('G2',String(e).slice(0,120));}

/* G3+G4 — Adaptive */
if(want('G3'))try{
  let ok=true,msg=[];
  for(const m of ['express_10','standard_25','mock_theory_50']){
    await fresh(p,'/adaptive-session/');
    await p.evaluate(mode=>startAllowedAdp(mode),m); await sleep(300);
    const r=await p.evaluate(()=>({btn:[...document.querySelectorAll('#s0-content button')].some(b=>b.textContent.includes('INICIAR'))}));
    if(!r.btn){ok=false;msg.push(m+': no INICIAR');}
    if(p._errs.length){ok=false;msg.push(m+': '+p._errs[0].slice(0,60));}
  }
  // full express walk
  await fresh(p,'/adaptive-session/');
  await p.evaluate(()=>startAllowedAdp('express_10')); await sleep(300);
  await p.evaluate(()=>{[...document.querySelectorAll('#s0-content button')].find(b=>b.textContent.includes('INICIAR')).click();}); await sleep(250);
  const ids=new Set();
  for(let i=0;i<10;i++){
    const st=await p.evaluate(()=>({qid:STATE.payload.questions[STATE.qIdx].question_id, opts:document.querySelectorAll('#options-wrap .option-btn').length}));
    if(st.opts<2){ok=false;msg.push('q'+i+' opts:'+st.opts);break;}
    ids.add(st.qid);
    await p.evaluate(()=>document.querySelector('#options-wrap .option-btn').click());
    await p.evaluate(()=>document.getElementById('btn-continue').click());
    await p.waitForSelector('#screen-2.active',{timeout:3000});
    await p.evaluate(()=>document.getElementById('btn-next').click());
    await sleep(120);
  }
  if(ids.size!==10){ok=false;msg.push('unique ids '+ids.size+'/10');}
  const db=await p.evaluate(()=>[...document.querySelectorAll('.screen')].find(s=>s.classList.contains('active'))?.id);
  if(db!=='screen-3'){ok=false;msg.push('no debrief: '+db);}
  if(p._errs.length){ok=false;msg.push(p._errs[0].slice(0,80));}
  ok?pass('G3','adaptive SBA 3 modes + walk + debrief'):fail('G3',msg.join(' | '));
}catch(e){fail('G3',String(e).slice(0,120));}
if(want('G4'))try{
  let ok=true,msg=[];
  for(const m of ['sat_sprint','sat_practice','sat_mock']){
    await fresh(p,'/adaptive-session/');
    await p.evaluate(mode=>startAllowedAdp(mode),m); await sleep(300);
    const r=await p.evaluate(()=>({wine:!!document.querySelector('#sat-content textarea')}));
    if(!r.wine){ok=false;msg.push(m+': no wine/textarea');}
    if(p._errs.length){ok=false;msg.push(m+': '+p._errs[0].slice(0,60));}
  }
  ok?pass('G4','adaptive SAT 3 modes render'):fail('G4',msg.join(' | '));
}catch(e){fail('G4',String(e).slice(0,120));}

/* G5 — Diagnostic SBA full session */
if(want('G5'))try{
  await fresh(p,'/diagnostic-sba/');
  await p.evaluate(()=>startMode('quick_drill'));
  let ok=true,msg=[]; const seen=[];
  for(let i=0;i<5;i++){
    const qid=await p.evaluate(()=>currentQ().id); seen.push(qid);
    await p.evaluate(()=>{goToRead();goToCommit();selectOption(0);selectConf('seguro');commitAnswer();}); await sleep(700);
    await p.evaluate(()=>confirmCross()); await sleep(200);
    await p.evaluate(()=>{
      goToTrain();
      if(STATE.stage==='train' && currentQ().micro_drill){
        selectDrillOption(0);
        submitDrill();
        nextQuestion();
      }
    }); await sleep(250);
  }
  const st=await p.evaluate(()=>({stage:STATE.stage, n:STATE.attempts.length}));
  if(st.stage!=='map'){ok=false;msg.push('did not reach map: '+st.stage);}
  if(new Set(seen).size!==5){ok=false;msg.push('repetition: '+seen.join(','));}
  if(st.n!==5){ok=false;msg.push('attempts '+st.n);}
  if(p._errs.length){ok=false;msg.push(p._errs[0].slice(0,80));}
  ok?pass('G5','SBA q1→q5→map, no loop, ids '+seen.join(',')):fail('G5',msg.join(' | '));
}catch(e){fail('G5',String(e).slice(0,120));}

/* G6 — navigation */
if(want('G6'))try{
  let ok=true,msg=[];
  for(const u of ['/diagnostic-sba/','/adaptive-session/','/open-response-lab/','/full-simulation/']){
    await p.goto(`http://localhost:${PORT}${u}`,{waitUntil:'networkidle0'});
    const bad=await p.evaluate(()=>{
      const out=[];
      document.querySelectorAll('.global-nav').forEach((nav,ni)=>{ nav.scrollIntoView({block:'center'});
        nav.querySelectorAll('a').forEach(a=>{ const r=a.getBoundingClientRect(); const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
          if(t!==a&&!a.contains(t)) out.push(ni+':'+a.getAttribute('href')+' by '+(t?(t.id||t.className||t.tagName):'null')); });});
      return out;});
    if(bad.length){ok=false;msg.push(u+' blocked: '+bad.join(';'));}
  }
  await p.goto(`http://localhost:${PORT}/diagnostic-sba/`,{waitUntil:'networkidle0'});
  try{ await Promise.all([p.waitForNavigation({timeout:5000}), p.click('.global-nav a[href="/adaptive-session/"]')]); }
  catch(e){ ok=false; msg.push('real click failed'); }
  const hub=await (async()=>{ await p.goto(`http://localhost:${PORT}/`,{waitUntil:'networkidle0'}); return p.evaluate(()=>document.querySelectorAll('a.exp-card').length); })();
  if(hub<4){ok=false;msg.push('hub cards '+hub+'/4');}
  ok?pass('G6','all nav links clear + click navigates + hub 4 cards'):fail('G6',msg.join(' | '));
}catch(e){fail('G6',String(e).slice(0,120));}

/* G7 — no placebo panels */
if(want('G7'))try{
  await fresh(p,'/diagnostic-sba/');
  await p.evaluate(()=>{
    const it=PREGUNTAS_BANK.items.find(i=>!i.causal_chain&&!i.feedback_by_mode&&!i.micro_drill);
    QUESTIONS=[bankToQ(it)]; STATE.questionIndex=0; STATE.stage='prepare'; render();
  });
  await p.evaluate(()=>{goToRead();goToCommit();selectOption(0);selectConf('seguro');commitAnswer();}); await sleep(700);
  await p.evaluate(()=>confirmCross()); await sleep(200);
  const r=await p.evaluate(()=>({
    dash:[...document.querySelectorAll('.feedback-block p')].filter(x=>x.textContent.trim()==='—').length,
    causalDash:[...document.querySelectorAll('.causal-node-text')].filter(x=>x.textContent.trim()==='—').length,
    guide:[...document.querySelectorAll('.feedback-block p')].map(x=>x.textContent).join(' ').includes('La respuesta correcta es'),
    selector:(()=>{const s=document.getElementById('mentorMode');return s? s.offsetParent!==null:false;})()
  }));
  (r.dash===0&&r.causalDash===0&&r.guide&&!r.selector)?pass('G7','no "—" panels, specific guidance, selector hidden')
    :fail('G7',JSON.stringify(r));
}catch(e){fail('G7',String(e).slice(0,120));}

/* G8 — localization */
if(want('G8'))try{
  let hits=[];
  for(const u of ['/diagnostic-sba/','/adaptive-session/','/open-response-lab/','/full-simulation/']){
    await p.goto(`http://localhost:${PORT}${u}`,{waitUntil:'networkidle0'});
    const h=await p.evaluate(()=>{
      const out=new Set(); const re=/(Quick Drill|Short Practice|Standard Practice|Extended Practice|SAT Sprint|SAT Practice|SAT Mock Exam|Open Response Lab|Adaptive Session|SBA Cockpit)/g;
      const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
      while(w.nextNode()){let m;while((m=re.exec(w.currentNode.textContent)))out.add(m[1]);}
      return [...out];});
    if(h.length)hits.push(u+': '+h.join(','));
  }
  hits.length?fail('G8',hits.join(' | ')):pass('G8','no English learner-facing labels');
}catch(e){fail('G8',String(e).slice(0,120));}

/* G9 — enrichment integrity (Phase P.1): enriched items activate real panels;
   non-enriched items keep them hidden (no placebo) */
if(want('G9'))try{
  await fresh(p,'/diagnostic-sba/');
  let ok=true,msg=[];
  // --- enriched item (batch 1) ---
  await p.evaluate(()=>{
    const it=PREGUNTAS_BANK.items.find(i=>i.id==='wset3_17');
    QUESTIONS=[bankToQ(it)]; STATE.questionIndex=0; STATE.stage='prepare'; render();
  });
  await p.evaluate(()=>{goToRead();goToCommit();selectOption(0);selectConf('seguro');commitAnswer();});
  await p.waitForFunction(()=>STATE.stage==='cross',{timeout:4000});   // wait out commitAnswer's timer
  await p.evaluate(()=>confirmCross());
  await p.waitForFunction(()=>STATE.stage==='reveal'&&document.querySelector('.feedback-block'),{timeout:4000});
  await sleep(150);
  const r=await p.evaluate(()=>({
    selectorVisible: document.getElementById('mentorMode').offsetParent!==null,
    causal:[...document.querySelectorAll('.causal-node-text')].map(x=>x.textContent.trim()),
    mentorTitle:[...document.querySelectorAll('.feedback-block-title')].map(x=>x.textContent).pop(),
  }));
  if(!r.selectorVisible){ok=false;msg.push('selector hidden on enriched item');}
  if(r.causal.length!==3||r.causal.some(t=>!t||t==='—')){ok=false;msg.push('causal panel incomplete: '+JSON.stringify(r.causal).slice(0,60));}
  // mentor switching changes body
  const bodies=[];
  for(const m of ['mentor','trainer','reviewer']){
    await p.evaluate(mm=>{document.getElementById('mentorMode').value=mm;updateMentorMode();STATE.stage='reveal';render();},m);
    await sleep(120);
    bodies.push(await p.evaluate(()=>[...document.querySelectorAll('.feedback-block')].pop().querySelector('p').textContent.trim()));
  }
  if(new Set(bodies).size!==3){ok=false;msg.push('mentor modes not distinct ('+new Set(bodies).size+'/3)');}
  // drill renders + submits
  await p.evaluate(()=>goToTrain()); await sleep(250);
  const d=await p.evaluate(()=>({drill:!!document.querySelector('.drill-section'),opts:document.querySelectorAll('.drill-opt-btn').length}));
  if(!d.drill||d.opts!==4){ok=false;msg.push('drill missing on enriched item');}
  await p.evaluate(()=>{selectDrillOption(0);submitDrill();}); await sleep(150);
  const ex=await p.evaluate(()=>document.getElementById('drillExplanation').textContent.length>5);
  if(!ex){ok=false;msg.push('drill explanation empty');}
  // ES copy check on rendered learner text
  const es=await p.evaluate(()=>/\b(?:de el|a el)\b/.test(document.getElementById('mainContent').textContent));
  if(es){ok=false;msg.push('contraction artifact rendered');}
  // --- non-enriched item: no placebo ---
  await p.evaluate(()=>{
    const it=PREGUNTAS_BANK.items.find(i=>!i.causal_chain&&!i.feedback_by_mode);
    QUESTIONS=[bankToQ(it)]; STATE.questionIndex=0; STATE.stage='prepare'; render();
  });
  await p.evaluate(()=>{goToRead();goToCommit();selectOption(0);selectConf('seguro');commitAnswer();});
  await p.waitForFunction(()=>STATE.stage==='cross',{timeout:4000});
  await p.evaluate(()=>confirmCross());
  await p.waitForFunction(()=>STATE.stage==='reveal'&&document.querySelector('.feedback-block'),{timeout:4000});
  await sleep(150);
  const n=await p.evaluate(()=>({
    selectorVisible: document.getElementById('mentorMode').offsetParent!==null,
    causalPanel: !!document.querySelector('.causal-chain'),
  }));
  if(n.selectorVisible){ok=false;msg.push('selector visible on non-enriched item');}
  if(n.causalPanel){ok=false;msg.push('causal panel on non-enriched item');}
  if(p._errs.length){ok=false;msg.push(p._errs[0].slice(0,80));}
  ok?pass('G9','enriched item: selector+3 mentores distintos+cadena+drill; non-enriched: hidden')
    :fail('G9',msg.join(' | '));
}catch(e){fail('G9',String(e).slice(0,140));}

await browser.close(); server.close();
let allPass=true;
for(const r of results){ console.log((r.skipped?'SKIP':(r.pass?'PASS':'FAIL'))+'  '+r.gate+'  '+r.msg); if(!r.pass)allPass=false; }
console.log(allPass?'\n✅ ALL GATES GREEN — safe to deploy':'\n❌ GATE FAILURE — do not deploy');
process.exit(allPass?0:1);
