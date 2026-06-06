# Frontend Source of Truth Reconciliation

**Fecha:** 2026-06-05  
**Método:** Inspección directa de GitHub API — SHAs de blobs y trees verificados por comparación criptográfica  
**Alcance:** Todos los paths de frontend en WSET-AI-System + repo epistemiclab-dashboard + URLs de producción

---

## 1. Pipeline de despliegue (fuente de verdad definitiva)

```
WSST-AI-System / frontend/diagnostic-sba/
        │
        │  (promoción manual o automática)
        ▼
WSET-AI-System / frontend/architecture-dashboard/
        │
        │  GitHub Actions: dashboard-daily-sync.yml
        │  cron: "17 10 * * *" (UTC) + workflow_dispatch
        │  comando: rsync -a --delete frontend/architecture-dashboard/ → epistemiclab-dashboard/
        ▼
BuenasBox / epistemiclab-dashboard  (repo GitHub Pages)
        │
        │  CNAME: epistemiclab.dpdns.org
        │  GitHub Pages (rama main)
        ▼
https://epistemiclab.dpdns.org/                       ← PRODUCCIÓN
https://epistemiclab.dpdns.org/diagnostic-sba/        ← PRODUCCIÓN
```

**El único repo que alimenta la publicación es `BuenasBox/epistemiclab-dashboard`.**  
`WSET-AI-System` es el repositorio de desarrollo; `epistemiclab-dashboard` es el artefacto de publicación.

---

## 2. Verificación de sincronización por SHA

### 2.1 diagnostic-sba — todos los paths son idénticos

Comparación de tree SHA para el directorio `diagnostic-sba/`:

| Ruta | Tree SHA | Estado |
|---|---|---|
| `WSET-AI-System/frontend/diagnostic-sba/` | `61fda2776b39651085225ea4ef0dfbdc690b7afc` | ✅ SINCRONIZADO |
| `WSET-AI-System/frontend/architecture-dashboard/diagnostic-sba/` | `61fda2776b39651085225ea4ef0dfbdc690b7afc` | ✅ SINCRONIZADO |
| `epistemiclab-dashboard/diagnostic-sba/` | `61fda2776b39651085225ea4ef0dfbdc690b7afc` | ✅ SINCRONIZADO |

Los tres comparten el mismo objeto git tree — son byte-por-byte idénticos.

Verificación por archivo individual:

| Archivo | Blob SHA | Tamaño |
|---|---|---|
| `index.html` | `4b57b10aad5d460f8d44bbb1e717ff93706da9a5` | 51,357 bytes |
| `preguntas.json` | `041cd052284084ae117f94d5631697f7269f664d` | 184,532 bytes |

Esas SHAs aparecen idénticas en los tres paths.

### 2.2 architecture-dashboard vs epistemiclab-dashboard — sincronización completa

| Archivo | Blob SHA en WSET-AI-System/frontend/architecture-dashboard/ | Blob SHA en epistemiclab-dashboard/ | Match |
|---|---|---|---|
| `.nojekyll` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | ✅ |
| `CNAME` | `f8f1ee471f8e5a8d43ff62b6924c6548db9aebb7` | `f8f1ee471f8e5a8d43ff62b6924c6548db9aebb7` | ✅ |
| `index.html` | `c7d7aace1dcd9176c669be2f652f8b5f7176a46d` | `c7d7aace1dcd9176c669be2f652f8b5f7176a46d` | ✅ |
| `robots.txt` | `df2f77d8f2ebbae9bb3a70b50518db8ebac9bbfc` | `df2f77d8f2ebbae9bb3a70b50518db8ebac9bbfc` | ✅ |
| `system_state.json` | `0d7bb494252d1d842b494105578b3b1b8358ac8c` | `0d7bb494252d1d842b494105578b3b1b8358ac8c` | ✅ |
| `diagnostic-sba/` (tree) | `61fda2776b39651085225ea4ef0dfbdc690b7afc` | `61fda2776b39651085225ea4ef0dfbdc690b7afc` | ✅ |

**`frontend/architecture-dashboard/` y `epistemiclab-dashboard/` son idénticos en todos los archivos.**  
El último sync del workflow (`chore: daily dashboard sync`, 2026-06-04) está vigente.

---

## 3. Tabla PATH | ESTADO

| Path | Estado | Rol en Pipeline | Notas |
|---|---|---|---|
| `BuenasBox/epistemiclab-dashboard/` | **PRODUCTION** | Repo GitHub Pages publicado en `epistemiclab.dpdns.org` | Artefacto de publicación — no se edita directamente |
| `WSET-AI-System/frontend/architecture-dashboard/` | **DEPLOYMENT_SOURCE** | Fuente del rsync diario hacia epistemiclab-dashboard | Actualmente 100% sincronizado con producción |
| `WSET-AI-System/frontend/diagnostic-sba/` | **CANONICAL_SOURCE** | Directorio de trabajo para el cockpit SBA activo | Idéntico a architecture-dashboard/diagnostic-sba/ — cambios aquí se promueven |
| `WSET-AI-System/frontend/diagnostic-sba-v2.2/` | **EXPERIMENTAL** | NO está en el pipeline de publicación | Versión siguiente (89,429 bytes vs 51,357 en prod); SHA distinto `b3e7652...` |
| `WSET-AI-System/frontend/diagnostic-sba-v2/` | **LEGACY** | NO está en el pipeline de publicación | Versión anterior |
| `WSET-AI-System/frontend/open-response-lab/` | **EXPERIMENTAL** | NO está en el pipeline de publicación | Laboratorio OR, no desplegado |

---

## 4. Respuesta a las preguntas del encargo

### ¿Cuál es la ruta de producción real?

| URL | Ruta en epistemiclab-dashboard |
|---|---|
| `https://epistemiclab.dpdns.org/` | `epistemiclab-dashboard/index.html` |
| `https://epistemiclab.dpdns.org/diagnostic-sba/` | `epistemiclab-dashboard/diagnostic-sba/index.html` |

### ¿Cuál repositorio alimenta esa publicación?

**`BuenasBox/epistemiclab-dashboard`** — único y exclusivo.  
Alimentado por `WSET-AI-System` vía `.github/workflows/dashboard-daily-sync.yml`.

---

## 5. Falsos positivos corregidos

El documento `docs/FRONTEND_STATE_AUDIT.md` (generado el mismo día) reportó tres brechas. A la luz de esta reconciliación:

| Brecha reportada | Veredicto | Evidencia |
|---|---|---|
| "Divergencia entre `frontend/diagnostic-sba/preguntas.json` y `frontend/architecture-dashboard/diagnostic-sba/preguntas.json`" | **FALSO POSITIVO** | Ambos archivos tienen SHA `041cd052...` — idénticos |
| "v2.2 vs cockpit desplegado — tamaños distintos, posible versión más reciente no promovida" | **NO ES BRECHA DE PRODUCCIÓN** | `diagnostic-sba-v2.2/` es EXPERIMENTAL, no participa en el pipeline. La diferencia es intencional y esperada. |
| "Conteo exacto de architecture-dashboard/preguntas.json desconocido" | **RESUELTO** | SHA `041cd052...` confirma que es el mismo archivo que la fuente; 36 items confirmados |

---

## 6. Definición de fuente única para futuras auditorías

> **Regla:** Toda auditoría de frontend que reporte una brecha de producción debe demostrar que el archivo en cuestión existe en `epistemiclab-dashboard/` (o en `frontend/architecture-dashboard/` con SHA verificable de sync reciente). Archivos en `frontend/diagnostic-sba-v2*/`, `frontend/diagnostic-sba-v*/`, o `frontend/open-response-lab/` son EXPERIMENTAL o LEGACY y no constituyen brechas de producción.

### Fuentes canónicas por componente

| Componente | Fuente canónica de edición | Ruta de promoción |
|---|---|---|
| Cockpit Diagnóstico SBA (activo) | `frontend/diagnostic-sba/` | `→ frontend/architecture-dashboard/diagnostic-sba/ → epistemiclab-dashboard/diagnostic-sba/` |
| Dashboard principal (`/`) | `frontend/architecture-dashboard/index.html` | `→ epistemiclab-dashboard/index.html` |
| System state | `frontend/architecture-dashboard/system_state.json` (generado por `tools/dashboard/update_architecture_dashboard_state.py`) | `→ epistemiclab-dashboard/system_state.json` |
| Cockpit SBA v2.2 (experimental) | `frontend/diagnostic-sba-v2.2/` | No promovido a producción |

---

## 7. Estado del workflow de publicación

**Archivo:** `.github/workflows/dashboard-daily-sync.yml`  
**Trigger:** Diario `cron: "17 10 * * *"` (UTC) + `workflow_dispatch`  
**Pasos:**
1. Checkout WSET-AI-System
2. `python tools/dashboard/update_architecture_dashboard_state.py --write` — refresca `system_state.json`
3. Valida `system_state.json` con `python -m json.tool`
4. Corre tests de contrato del dashboard
5. `rsync -a --delete frontend/architecture-dashboard/ → epistemiclab-dashboard/`
6. Commit + push a `epistemiclab-dashboard/main`

**Último sync confirmado:** 2026-06-04 (`chore: daily dashboard sync`)  
**Token requerido:** `EPISTEMICLAB_DASHBOARD_TOKEN` (fine-grained PAT con Contents: Read+write para epistemiclab-dashboard)

---

*Reconciliación basada en inspección directa de GitHub API. Ninguún archivo modificado.*
