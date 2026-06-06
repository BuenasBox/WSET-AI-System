# Phase 4A.3.8.3A - Repository & Checkout Reconciliation

Fecha de verificacion: 2026-06-06
Alcance: reconciliacion solamente; sin remediacion, restauracion, deployment ni commit.

## Resultado ejecutivo

**Fuente de verdad unificada: NO.**

El checkout activo y `origin/main` representan dos puntas divergentes:

- El checkout activo contiene `0b77440` (LES Foundation), pero no contiene
  `8eab69e`, `6495808`, `f092b59` ni `9fe4a3d`.
- `origin/main` contiene Adaptive Rules, Dashboard actualizado, Master Bank y el
  fix validado de Slow Golden, pero no contiene `0b77440`.
- El baseline golden y el test harness son identicos entre ambas puntas. El
  resultado 3/7 del checkout activo se explica por inputs y comparator anteriores
  al fix `9fe4a3d`, no por un baseline distinto.

No debe iniciarse Topic Signals ni Adaptive Composer hasta que una operacion de
integracion separada y autorizada produzca una linea que contenga ambas puntas y
vuelva a verificar sus gates.

## 1. Entorno exacto

Ruta absoluta del checkout:

```text
C:\Users\esand\.codex\worktrees\ea47\WSET-AI-System
```

`git rev-parse --show-toplevel`:

```text
C:/Users/esand/.codex/worktrees/ea47/WSET-AI-System
```

`git remote -v`:

```text
origin  https://github.com/BuenasBox/WSET-AI-System.git (fetch)
origin  https://github.com/BuenasBox/WSET-AI-System.git (push)
```

Rama activa:

```text
codex/phase-4a3-7-open-response-lab
```

Estado de tracking:

```text
[origin/codex/phase-4a3-7-open-response-lab: gone]
```

El mensaje `[gone]` es real: `git ls-remote` no devolvio esa rama remota.

`git status --short --branch`:

```text
## codex/phase-4a3-7-open-response-lab...origin/codex/phase-4a3-7-open-response-lab [gone]
```

El resto del estado consiste en artefactos runtime/generados y un directorio
`manual-import` no rastreado, clasificados en la seccion 5.

## 2. Linea canonica

Se consulto el remoto y se actualizo la referencia remote-tracking, sin cambiar
el working tree.

| Ref | Hash | Estado |
|---|---|---|
| `HEAD` | `0b77440babf66677a9ccd8ccc8c632bba233095f` | LES Foundation |
| `main` local | `90524ff247e696e0b3b4b16c63f232fc670a6f74` | checkout principal local, atrasado |
| `origin/main` | `1531cda543d9a57aeb684859cc1e71229e342791` | punta actual confirmada por `git ls-remote` |

Divergencias:

| Comparacion | Izquierda exclusiva | Derecha exclusiva | Interpretacion |
|---|---:|---:|---|
| `HEAD...main` | 1 | 1 | divergencia desde `917e4b5` |
| `HEAD...origin/main` | 1 | 13 | HEAD ahead 1, behind 13 |
| `main...origin/main` | 0 | 12 | `main` local behind 12 |

Merge bases:

```text
HEAD vs main:        917e4b5171bdc12f6f5b125c0372db7e82f3b431
HEAD vs origin/main: 917e4b5171bdc12f6f5b125c0372db7e82f3b431
main vs origin/main: 90524ff247e696e0b3b4b16c63f232fc670a6f74
```

El checkout principal adicional detectado en
`C:\Users\esand\OneDrive\Documents\WSET-AI-System` esta en `main` a `90524ff`,
behind 12 respecto de `origin/main`, con cambios locales. Tampoco es por si solo
la linea canonica actual.

## 3. Commits requeridos

| Commit | Subject real | En HEAD | En main local | En origin/main |
|---|---|---:|---:|---:|
| `8eab69e` | `docs(adaptive): add adaptive session pedagogical rules` | NO | NO | YES |
| `0b77440` | `feat(phase-4a3-8-3): add learner state foundation` | YES | NO | NO |
| `6495808` | `feat(dashboard): publish repository maturity model` | NO | NO | YES |
| `f092b59` | `Merge PR #3: canonical Master Bank infrastructure` | NO | NO | YES |

Resultado: la rama utilizada para esta verificacion no contiene tres de los
cuatro commits requeridos. `origin/main` contiene esos tres, pero le falta LES
Foundation.

El commit SBA 36 `f846f27` es ancestro tanto de HEAD como de `origin/main`.

## 4. Slow Golden

Comando ejecutado en el checkout activo:

```powershell
$env:RUN_SLOW_TESTS='1'
python -m unittest tests.test_golden_self_eval -v
```

Resultado real:

```text
Ran 7 tests
FAILED (failures=4)
3 OK / 4 failed
```

Pasaron:

- `test_governance_flags_unchanged`
- `test_no_retrieval_gaps`
- `test_no_sat_weaknesses`

Fallaron:

- `test_known_retrieval_weakness_not_worse`
- `test_no_failure_labels`
- `test_no_new_missing_causal_chains`
- `test_no_new_retrieval_weaknesses`

Metricas observadas:

```text
missing_keyword_support: 17, baseline maximum 5
shallow_retrieval: 13
shallow_reasoning: 12
missing_causal_link: 1
new retrieval weaknesses: shallow_retrieval, missing_causal_link_support
new missing causal chain: cause -> mechanism -> effect
```

### Baseline cargado

El test define:

```text
GOLDEN_PATH = KNOWLEDGE_DIR / "self-eval" / "golden_brutal_output.json"
```

Archivo efectivo de este checkout:

```text
C:\Users\esand\.codex\worktrees\ea47\WSET-AI-System\knowledge\self-eval\golden_brutal_output.json
```

Baseline:

```text
failure_labels: {}
retrieval_weaknesses.missing_keyword_support: 5
causal_chains_missing: {}
sat_weakness_question_ids: []
retrieval_gap_question_ids: []
```

El test harness y el baseline son byte-equivalentes entre HEAD y `origin/main`:

| Archivo | Hash HEAD | Hash origin/main | Igual |
|---|---|---|---:|
| `tests/test_golden_self_eval.py` | `6390a73c671f74b0cf2906d52832e1649d515be8` | mismo | YES |
| `knowledge/self-eval/golden_brutal_output.json` | `14d76b5baf481281afc28433a4904c04ad5ffaf1` | mismo | YES |

### Comparacion con el entorno 7/7

El reporte versionado
`docs/PHASE_4A_3_7_53B_SLOW_GOLDEN_METADATA_FIX_VERIFICATION.md` identifica el
checkout verde como:

```text
C:\Dev\WSET-AI-System-push
```

Ese reporte confirma:

```text
Suite regular: 1432 OK, 9 skipped
Slow Golden: 7/7 OK
Golden baseline: sin cambios
```

La linea verde contiene `9fe4a3d fix(self-eval): reconcile slow golden metadata`,
ahora ancestro de `origin/main`. Ese commit cambio:

- `knowledge/question-bank/structured/wset3_questions.json`
- `tools/self_eval/answer_comparator.py`
- `tests/test_self_eval_loop.py`

No cambio `tests/test_golden_self_eval.py` ni
`knowledge/self-eval/golden_brutal_output.json`.

Los archivos relevantes que si difieren entre HEAD y `origin/main` son:

| Archivo | HEAD | origin/main |
|---|---|---|
| `knowledge/question-bank/structured/wset3_questions.json` | `2f6dd2b8e55dadb42cc7893cfd29074e1272d471` | `e71d6050255156fc58d303bc0125389b77252419` |
| `tools/self_eval/answer_comparator.py` | `9bb520ff76fa20a5cd66d2134d81ff9f2a8d4503` | `7268d65640185e07860223cb726b8afe9d82835c` |

Conclusion Slow Golden: el estado 3/7 de este checkout es reproducible y
corresponde a una linea anterior al fix validado. No demuestra una regresion del
baseline vigente.

## 5. Artefactos locales

No se elimino ni restauro ningun artefacto.

### RUNTIME_LOCAL

- `knowledge/nazareth/self_eval_feedback.json`
- `knowledge/self-eval/pedagogical_memory.json`

### GENERATED

- `knowledge/retrieval-sandbox/orchestrator_context_retrieval_debug.csv`
- `knowledge/self-eval/attempts/*/latest_context_package.json`
- `knowledge/self-eval/attempts/*/self_eval_result.json`
- `knowledge/self-eval/attempts/*/tutor_attempt.md`
- `knowledge/self-eval/attempts/*/tutor_context_package.json`
- `knowledge/self-eval/self_eval_results.csv`
- `knowledge/self-eval/self_eval_results.jsonl`
- `knowledge/self-eval/self_eval_summary.md`

Conteo observado despues de la verificacion:

```text
98 archivos modificados bajo knowledge/self-eval/attempts/
4 agregados self-eval modificados
1 retrieval debug modificado
1 learner feedback runtime modificado
```

### UNKNOWN

- `knowledge/wine-with-jimmy/manual-import/manifests/.gitkeep`

Es el unico archivo local no rastreado visible con
`git ls-files --others --exclude-standard`. Se clasifica `UNKNOWN` porque no hay
evidencia suficiente en esta reconciliacion para declararlo runtime o generado.

## 6. Fuente de verdad

Pregunta: ¿Este checkout es la misma linea canonica utilizada para SBA 36
activos, Dashboard actualizado, Slow Golden 7/7, Master Bank Infrastructure y
LES Foundation?

**NO**

Evidencia:

- SBA 36: **YES**, `f846f27` es ancestro de HEAD.
- Dashboard actualizado: **NO**, falta `6495808`.
- Slow Golden 7/7: **NO**, falta `9fe4a3d`; la ejecucion actual da 3/7.
- Master Bank Infrastructure: **NO**, falta `f092b59`.
- LES Foundation: **YES**, HEAD es `0b77440`.

`origin/main` presenta la combinacion inversa relevante:

- contiene SBA 36, Dashboard, Slow Golden fix y Master Bank;
- no contiene LES Foundation `0b77440`.

Por tanto, ninguna de las dos puntas actuales es una fuente de verdad completa
para el conjunto solicitado.

## Recomendacion final

Detener el inicio de Topic Signals y Adaptive Composer. La siguiente accion debe
ser una fase separada, explicitamente autorizada, de integracion Git entre
`origin/main@1531cda` y `0b77440`, seguida por verificacion completa. Esta
reconciliacion no ejecuta esa accion ni prescribe el mecanismo concreto de merge.
