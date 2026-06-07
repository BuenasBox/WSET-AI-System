# PROJECT_STATE_FOR_CLAUDE_RESTART — Handoff para CLAUDE

Fecha local: 2026-06-07  
Repo local: C:\Dev\WSET-AI-System-push

> Propósito: documento autoritativo para que Claude retome trabajo sin perder contexto ni romper el estado verde actual. No ejecutar cambios: NO commit, NO push, NO activar flags, NO editar snapshots.

---

## 1. Resumen ejecutivo (máx. 15 líneas)
- Backend/runtime está verde y verificado: full test suite pasada localmente (1878 tests OK, skipped=9).  
- Incidente crítico resuelto: rebase rompió learning runtime; se recuperó compatibilidad legacy+moderno en tools/learner_model/learning_event_runtime.py — build_next_session_signals ahora soporta ambos consumidores.  
- Estado Git: rama main, HEAD en commit 6229e9d, origin/main sincronizado. Working tree informado como limpio (sin commits pendientes). Untracked: pendiente verificación local (especial atención frontend.zip).  
- Gobernanza: safe_for_examiner=False; examiner_scoring_allowed=False; uses_llm/uses_api/uses_embeddings/uses_vector_db/cloud_services_active = False (enforced en tools/constants.py).  
- Prioridad siguiente: inventario y consolidación del frontend; exponer adaptive-session como experiencia principal para pruebas con Nazareth. No tocar runtime salvo emergencia.

---

## 2. Estado Git (hechos confirmados)
- Branch actual: main.  
- HEAD: commit 6229e9d (confirmado por contexto).  
- origin/main: sincronizado con HEAD (confirmado).  
- git working tree: informado como sin commits pendientes que requieran push (confirmado por contexto).  
- Untracked / artefactos no verificados: frontend.zip (posible), otros artefactos locales en knowledge/nazareth/ (machine-local; NO comitear). — PENDIENTE DE VERIFICAR con `git status`.  
- Commits pendientes para push: ninguno (confirmado).

Comandos recomendados a ejecutar antes de tocar código:
- git status
- git log --oneline --decorate -n 5
- git rev-parse HEAD
- git branch -a

---

## 3. Estado de tests (hechos confirmados)
- Comando ejecutado (confirmado): python -m unittest discover -s tests -v  
- Resultado: OK (todos verdes en la verificación reciente).  
- Total tests: 1878  
- Skipped: 9  
- Failures/Errors: 0 (en la ejecución declarada)  
- Tiempo: ~32.008s (ejecución reportada)  
- Advertencias importantes: ninguna en la última ejecución; historial de 3 errores Windows en otro momento resuelto.

Nota: varios docs (AGENTS.md / CLAUDE.md) contienen historiales anteriores de conteos de tests — el valor actualizado y verificado es 1878.

---

## 4. Arquitectura — Panorama y módulos clave (roles y estado)
Hechos verificados en el código fuente y tests.

- tools/learner_model/learning_event_runtime.py  
  - Responsabilidad: runtime del evento de aprendizaje y orquestación del adaptive loop.  
  - Estado: recuperado tras rebase; soporta consumidores legacy y modernos; build_next_session_signals adaptado para dict-candidates y comparaciones legacy. Cobertura por tests de integración.

- tools/learner_model/adaptive_composer.py  
  - Responsabilidad: componer la siguiente experiencia desde señales adaptativas.  
  - Estado: implementado; integrado en adaptive loop pero requiere pruebas de UI/integración.

- tools/learner_model/adaptive_signal_consumer.py  
  - Responsabilidad: interpretar señales adaptativas y producir acciones/transformaciones.  
  - Estado: compatibilizado con runtime; cubierto por tests unitarios/integración.

- tools/learner_model/open_response_evaluator.py  
  - Responsabilidad: evaluación heurística de respuestas abiertas (sin LLM).  
  - Estado: implementado y probado.

- tools/learner_model/wwj_remediation.py  
  - Responsabilidad: pipeline de remediación (WWJ).  
  - Estado: integrado y validado por tests.

- tools/orchestrator/strategic_planner.py  
  - Responsabilidad: planner pedagógico determinista (puro, sin side-effects).  
  - Estado: implementado, aislado, probado. Carga secuencia de topics desde knowledge/config/wset3_topic_sequence.json.

- tools/orchestrator/* (orchestrator.py, les_reconciler.py, learner_state.py, session_ledger.py, ledger_summary.py)  
  - Responsabilidad: orquestación del loop cognitivo, LES, reconciliación, ledger, resumen CLI.  
  - Estado: integrado; tests de integración presentes. Planner wired-in pero inert (no influye en Tutor salvo observación escrita).

- tools/retrieval/tutor_retrieval_sandbox.py  
  - Responsabilidad: motor de retrieval determinista, scoring, diversity, governance filters, causal-chain matching.  
  - Estado: maduro; compatibilidad con planner hints y gates (parseo y gates implementados; gates OFF por defecto).

- tools/question_generation/ (human_review_resolution.py, diagnostic_sba_validator.py, static_demo_exporter.py, structured_question_bank_adapter.py)  
  - Responsabilidad: pipelines de generación y validación de preguntas; export demo estático.  
  - Estado: implementados; reconciliación Active Set vs Gold Bank pendiente.

- tools/tutor/* (answer_builder.py, sat_reasoner.py, pedagogical_strategy/)  
  - Responsabilidad: ensamblado determinista de respuestas, SAT reasoning, PSL (Pedagogical Strategy Layer).  
  - Estado: answer_builder y sat_reasoner maduros y cubiertos por snapshots/tests. PSL implementado pero feature-flagged OFF (no activo).

- knowledge/*  
  - Incluye knowledge-map (misconceptions, causal-chains), question-bank estructurado, configs. Estado: indexado y usado por retrieval/tutor.

- frontend/*  
  - Varios prototipos estáticos: architecture-dashboard, adaptive-session, diagnostic-sba, diagnostic-sba-v2, diagnostic-sba-v2.2, open-response-lab. Estado: prototipos en repo; deployment efectivo proviene de un repo separado (BuenasBox/epistemiclab-dashboard).

---

## 5. Governance — invariantes (verificación en código)
Variables y estado (revisión en tools/constants.py y tests de gobernanza):
- safe_for_examiner = False  — CONFIRMADO  
- examiner_scoring_allowed = False — CONFIRMADO  
- uses_llm = False — CONFIRMADO  
- uses_api = False — CONFIRMADO  
- uses_embeddings = False — CONFIRMADO  
- uses_vector_db = False — CONFIRMADO  
- cloud_services_active = False — CONFIRMADO

Enforcement locations:
- tools/constants.py  
- retrieval filters (tools/retrieval/*)  
- tutor rendering (tools/tutor/answer_builder.py)  
- snapshot tests and governance unit tests

No cambiar estos flags sin autorización explícita y plan de verificación.

---

## 6. Adaptive loop — estado detallado (learning_event_runtime + composer + consumer)
Hechos:
- learning_event_runtime.py fue recuperado y reconciliado; tests pasan.  
- build_next_session_signals actualizado para soportar consumidores legacy y modernos (candidates dict compat).  
- adaptive_signal_consumer.py y adaptive_composer.py están presentes y testeados; wiring en adaptive loop está activo en código de orchestrator/runtime.  
- Compatibilidad con contratos legacy: mantenida; runtime compara strings y dict-candidates según necesidad.

Cobertura y riesgos:
- Tests unitarios e integración cubren paths críticos (runtime + adaptive loop).  
- Riesgos: si se cambian contratos de candidate shape o se activan gates experimentales (planner injections, PSL) puede romper compatibilidad.  
- Recomendación: no modificar contratos sin tests adicionales.

---

## 7. Frontend — inventario y auditoría (por carpeta)
Hecho: inventario basado en estructura repo; contenido exacto de cada index.html y assets marcado como "pendiente" cuando no se puede confirmar sin listar archivos localmente.

Carpeta | Contiene index.html | Entrada / entry point | Propósito actual | Deploy-readiness | Comentarios
---|---:|---|---|---:|---
frontend/architecture-dashboard/ | Sí (síntesis) | index.html | Dashboard de producto — canonical dev source | Parcial: requiere navegación a experiencias | Recomendado como raíz de deploy dev-canonical
frontend/adaptive-session/ | Sí | index.html | Experiencia inmersiva adaptativa (prototipo) | Parcial: necesita integración con dashboard y pruebas | Mejor candidato para experiencia principal
frontend/diagnostic-sba/ | Sí | index.html | Cockpit SBA estático (preguntas.json, 18 ítems) | Parcial: funciona como prototipo estático | Variante operativa en producción externa
frontend/diagnostic-sba-v2/ | Sí | index.html | Fork/iteración del cockpit | Duplicado/posible huérfano | Consolidar
frontend/diagnostic-sba-v2.2/ | Sí | index.html | Otra iteración | Duplicado/posible huérfano | Consolidar
frontend/open-response-lab/ | Sí | index.html | Laboratorio de respuesta abierta | Parcial: prototipo | Integrar con adaptive-session si procede
frontend/* (otros assets) | assets, css, js | N/A | Recursos estáticos | Revisar | Posible frontend.zip (PENDIENTE)

Notas:
- Archivo frontend.zip: riesgo de artefacto no versionado; existencia PENDIENTE DE VERIFICAR en working tree.  
- session_data/session_payload.json: existe en repo histórico? presencia PENDIENTE DE VERIFICAR (no comitear LES payloads).  
- Múltiples index.html indican duplicación; rutas huérfanas probables (v2/v2.2). Inventario de archivos recomendado.

---

## 8. Frontend Experience Audit (UX analysis)
Hechos e inferencias basadas en prototipos:

- architecture-dashboard: representa panel de control / catálogo de experiencias; está pensado como entry para navegación entre demos. Buen candidato para raíz de deploy dev.  
- adaptive-session: prototipo inmersivo y adaptativo; representa la experiencia alumno que debe ser priorizada — señales, adaptivity, remediations integradas.  
- diagnostic-sba variants: variantes del mismo cockpit; v2/v2.2 probablemente experimentales o forks; redundantes y deben consolidarse.  
- open-response-lab: laboratorio de práctica de respuestas abiertas; complementario a adaptive-session.

Recomendación principal:
- Primary student experience = frontend/adaptive-session integrada desde architecture-dashboard (dashboard → adaptive-session). Consolidar diagnostic-sba variantes en una sola implementación alimentada por Gold Bank. Mantener disclaimers formativos visibles.

---

## 9. Deployment — estado y rutas
Hechos:
- Rutas públicas conocidas (provistas en docs/context):  
  - https://epistemiclab.dpdns.org/  
  - https://epistemiclab.dpdns.org/diagnostic-sba/  
- Fuente de producción: BuenasBox/epistemiclab-dashboard (repositorio separado). WSET-AI-System/origin/gh-pages no es la fuente productiva por defecto; histórico solamente.  
- Build outputs: frontend artefactos estáticos en frontend/*; no pipeline de CI/CD activado en este repo por defecto.  
- Root de deploy (dev-canonical): frontend/architecture-dashboard (recomendado). Producción real gestionada fuera del repo.

Riesgo: mover carpetas sin coordinar con BuenasBox/epistemiclab-dashboard puede romper deploys activos.

---

## 10. Phase audit (tabla — marcar solo completado si evidencia en código/tests)
Phase | Status | Evidencia | Confianza
---|---:|---|---:
Phase 1A strategic_planner | Complete | tools/orchestrator/strategic_planner.py + tests/test_strategic_planner.py | Alta
Phase 1B orchestrator integration | Complete | orchestrator.py wiring + integration tests | Alta
Phase 2A/B/C ledger & CLI | Complete | session_ledger.py, ledger_summary.py + tests | Alta
Phase 3A planner gates / retrieval hints | Complete (gates OFF) | retrieval sandbox helpers + tests | Alta
Phase 3B WSET L3 topic seq | Complete | knowledge/config/wset3_topic_sequence.json + tests | Alta
Phase 3A.8 readiness review | Complete (recommend OFF) | docs/PLANNER_CAUSAL_CHAIN_ACTIVATION_REVIEW.md | Alta
Phase 4A diagnostic SBA workstream (partial) | Parcial | frontend/diagnostic-sba prototype, docs/ACTIVE_SET_RECONCILIATION_PLAN.md | Media
Phase 4A.3.7.11 human review resolution | Parcial / needs verification | tools/question_generation/human_review_resolution.py exists; integration tests parciales | Media
Phase 4A.3.7.33B Active Set reconciliation | Pendiente | docs/ACTIVE_SET_RECONCILIATION_PLAN.md — trabajo definido | Baja→Media
Phase 4A.3.9 / 4A.3.9.2 learning event runtime + adaptive loop | Complete | learning_event_runtime.py recovered + tests verdes | Alta

Notas: marcar “Complete” solo cuando hay código + pruebas automáticas que verifican comportamiento. Varias fases documentadas en docs pero requieren ejecución/integración adicional (ver columna Evidencia).

---

## 11. Qué quedó terminado (implementado y validado por tests)
Listado comprobado:
- Strategic planner (fase 1A) + integración inert (1B).  
- Retrieval sandbox completo y hardened para planner hints.  
- learning_event_runtime.py + adaptive loop wiring + adaptive_signal_consumer + adaptive_composer (recuperados y testeados).  
- tools/tutor/answer_builder.py + sat_reasoner.py + snapshot regression harness.  
- Question bank converter y protecciones para preguntas Abierta.  
- Ledger/session_ledger y ledger_summary CLI.  
- HC_* heuristic causal-chain nodes e integración de esquema.

---

## 12. Qué quedó parcialmente implementado / técnicas incompletas
- Active Set reconciliation (Phase 4A.3.7.33B) — plan y docs presentes; implementación de reemplazo Gold en demo pendiente.  
- Human review resolution completo en pipeline — existen módulos, falta integración final end-to-end.  
- Frontend: múltiples prototipos sin navegación consolidada; duplicación diagnostic-sba*.  
- PSL (Pedagogical Strategy Layer) implementado pero flag OFF — no integrado en runtime.  
- session_data/session_payload.json y frontend.zip — existencia y uso a verificar (PENDIENTE).

---

## 13. Riesgos técnicos actuales (resumen)
- Contratos legacy vs modernos (aun riesgo si se cambian shapes de candidates).  
- Duplicación frontend y artefactos huérfanos (v2, v2.2).  
- Artefactos zip/no-versionados (frontend.zip) — riesgo de leakage.  
- Deuda semántica en nombres de fases (peligro al mover carpetas/renombrar).  
- Riesgo alto de romper tests verdes si se tocan runtime o snapshots sin seguir Verification Gate.  
- Riesgo de exponer datos LES (knowledge/nazareth/) si se comitean por error.

---

## 14. Recomendación de tareas siguientes (muy concretas)
A. Trabajo seguro inmediato (bajo riesgo)
- Ejecutar y confirmar: git status; git log --oneline --decorate -n 5; git rev-parse HEAD; python -m unittest discover -s tests -v (no modificar código).  
- Inventario frontend: listar index.html y assets en cada frontend/*; detectar frontend.zip. Comandos: dir /b frontend\* /s (Windows) o PowerShell Get-ChildItem.  
- Verificar presencia de session_payload.json y mover/archivar localmente si contiene LES (NO COMMIT).  
- Revisar docs/ACTIVE_SET_RECONCILIATION_PLAN.md y preparar listado de preguntas demo a reemplazar (sin modificar).

B. Trabajo que requiere cuidado arquitectónico (mediano riesgo)
- Consolidar diagnostic-sba variants en una única implementación y migrar datos Gold.  
- Integrar navigation: architecture-dashboard → adaptive-session; implementar pruebas end-to-end locales (http-server simple).  
- Preparar staging export del frontend/adaptive-session para validación con Nazareth (coordinar con BuenasBox/epistemiclab-dashboard).

C. Trabajo que NO debe hacerse (prohibido por ahora)
- Activar flags: ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION, ENABLE_PLANNER_QUERY_EXPANSION, ENABLE_PEDAGOGICAL_STRATEGY_LAYER.  
- Introducir LLMs, APIs externas, embeddings, vector DBs, o cloud services.  
- Comitear artefactos dentro de knowledge/nazareth/ o cualquier runtime LES.  
- Modificar snapshots sin plan de verificación.

---

## 15. Plan recomendado para frontend (pasos, sin ejecutar)
1. Inventario exhaustivo de frontend/* (listar index.html, assets, rutas).  
2. Decidir raíz de deploy dev-canonical (recomendado: frontend/architecture-dashboard).  
3. Añadir navegación desde dashboard a adaptive-session y diagnostic-sba (un único punto de entrada).  
4. Consolidar diagnostic-sba variants y eliminar duplicados (mantener backup local, NO comitear basura).  
5. Integrar adaptive-session como experiencia principal para pruebas Nazareth; mantener disclaimers formativos.  
6. Probar local con servidor estático y ejecutar backend tests en paralelo.  
7. Coordinar con BuenasBox/epistemiclab-dashboard para export/deploy final.

---

## 16. Checklist obligatorio para CLAUDE antes de tocar código
- git status  
- git log --oneline --decorate -n 5  
- git rev-parse HEAD  
- python -m unittest discover -s tests -v  
- Revisar listados frontend (index.html por carpeta)  
- NO commit/push sin autorización explícita

Comandos (Windows PowerShell):
- git status
- git log --oneline --decorate -n 5
- git rev-parse HEAD
- python -m unittest discover -s tests -v
- Get-ChildItem -Recurse -Filter index.html -Path .\frontend\

---

## 17. Evidencias/artefactos clave (rutas)
- tools/learner_model/learning_event_runtime.py  
- tools/learner_model/adaptive_composer.py  
- tools/learner_model/adaptive_signal_consumer.py  
- tools/learner_model/open_response_evaluator.py  
- tools/learner_model/wwj_remediation.py  
- tools/orchestrator/strategic_planner.py  
- tools/retrieval/tutor_retrieval_sandbox.py  
- tools/question_generation/ (human_review_resolution.py, diagnostic_sba_validator.py, static_demo_exporter.py)  
- tools/tutor/answer_builder.py  
- knowledge/knowledge-map/  
- frontend/architecture-dashboard/  
- frontend/adaptive-session/  
- frontend/diagnostic-sba/ (v2, v2.2)  
- docs/ACTIVE_SET_RECONCILIATION_PLAN.md  
- docs/PROJECT_CURRENT_STATE.md

---

## 18. Hechos confirmados vs inferencias / elementos pendientes
- Hechos confirmados: tests verdes (1878), HEAD 6229e9d, origin/main sync, learning_event_runtime reparado, governance flags OFF, planner gates OFF.  
- Inferencias / pendientes de verificación: existencia de frontend.zip, contenido exacto de cada index.html y assets, session_payload.json en working tree. Marcar como "PENDIENTE DE VERIFICAR" y NO comitear.

---

## 19. Resumen breve para entrega inmediata
Backend y runtime están en estado estable y con cobertura de pruebas. Siguiente prioridad operacional: inventario y consolidación del frontend; exponer adaptive-session como experiencia principal para pruebas con Nazareth. No tocar flags ni runtime sin autorización y sin pasar la suite de tests. Mantener protección de LES (knowledge/nazareth/) y no comitear artefactos locales.

---