"""SBA enrichment deriver — Phase P.1 (pedagogical batch 1).

Deterministically derives learner-facing enrichment for SBA items from
EXISTING knowledge assets only (causal-chain nodes + item fields). No new
pedagogy is authored: every output is a template over existing content, with
per-field provenance. Fields are populated ONLY under strong signal; when
evidence is insufficient the field is omitted and the UI keeps its panel
hidden (no placebo, no invented causal chains).

Outputs a SIDECAR file — the master bank is never modified:
    knowledge/question-bank/enrichment/sba_enrichment_v1.json

Derivation rules (constants below):
  - causal_chain: only when >= MIN_KEYWORD_HITS distinct trigger keywords of a
    node appear in the item's keywords+stem AND the best node is unique
    (ties are ambiguous -> not populated). Node text comes from the Spanish
    layer NODE_ES; a matched node without translation is skipped (guard).
  - feedback_by_mode: three deterministic Spanish templates (Mentor Guia /
    Entrenador Tecnico / Revisor Estricto) built only from item fields and the
    matched chain.
  - micro_drill: anchored on the matched causal node (clean axis — the dirty
    `topic` field is NOT used as a discrimination axis). Options are correct
    options of OTHER batch items matched to DIFFERENT nodes: all content is
    existing and true; distractors are true statements about other mechanisms.

Governance: formative only; safe_for_examiner=False; no marks, no scoring.
No LLM, no API, no network. Deterministic: same inputs -> same output bytes.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CHAINS_DIR = REPO / "knowledge" / "knowledge-map" / "causal-chains"
FRONTEND_BANK = REPO / "frontend" / "diagnostic-sba" / "preguntas_data.js"
SIDECAR_OUT = REPO / "knowledge" / "question-bank" / "enrichment" / "sba_enrichment_v1.json"
REPORT_OUT = REPO / "docs" / "ENRICHMENT_BATCH1_SAMPLE.md"

# ---- Derivation thresholds (the contract of "strong signal") ----
# v2 (precision-first, after batch-1 review found false positives caused by
# substring matching and over-generic node triggers):
#   - word-boundary matching on accent-normalized text (no substrings)
#   - generic triggers are banned (stoplist below)
#   - the node must explain the CORRECT ANSWER: >=1 specific trigger in the
#     stem AND >=1 in the correct option text, >=2 distinct overall
#   - regional-identification / simple-factual stems never get causal chains
MIN_KEYWORD_HITS = 2          # distinct specific triggers across stem+keywords+correct
REQUIRE_STEM_HIT = True       # >=1 specific trigger in the stem
REQUIRE_CORRECT_OPTION_HIT = True  # >=1 specific trigger in the correct option
REQUIRE_UNIQUE_BEST = True    # tie between nodes -> ambiguous -> skip
BATCH_SIZE = 50               # upper bound; precision decides actual coverage
MIN_TRIGGER_LEN = 4           # very short triggers are noise
MIN_DRILL_OPTION_LEN = 20     # chars; shorter correct options don't make drills
DRILL_DISTRACTOR_COUNT = 3
REPORT_SAMPLE_SIZE = 50       # small precise batch: report lists everything

# Triggers too generic to carry causal meaning on their own (banned even if a
# node lists them). Accent-normalized lowercase.
GENERIC_TRIGGERS = {
    "vino", "vinos", "wine", "wines", "uva", "uvas", "grape", "grapes",
    "fermentacion", "fermentation", "mosto", "must", "alcohol", "levadura",
    "yeast", "acidez", "acidity", "dulce", "sweet", "color", "colour",
    "aroma", "aromas", "crianza", "ageing", "aging", "clima", "climate",
    "suelo", "soil", "region", "calidad", "quality", "estilo", "style",
}

# Stems that ask for regional identification or simple factual recall do not
# get causal chains (the causal node cannot "explain" an identification).
IDENTIFICATION_PATTERNS = (
    r"\bque\s+region\b", r"\bcual\s+region\b", r"\bque\s+pais\b",
    r"\bque\s+denominacion\b", r"\bque\s+zona\b", r"\bque\s+valle\b",
    r"\bdonde\b", r"\bfamos[oa]s?\s+por\b", r"\bse\s+encuentra\b",
    r"\bse\s+ubica\b", r"\bsinonimo\b", r"\bque\s+uva\b",
    r"\bque\s+variedad\b", r"\bcomo\s+se\s+llama\b", r"\bque\s+nombre\b",
    # definitional stems: the causal node cannot "explain" a definition
    r"\bque\s+es\s+(un|una|el|la)\b", r"\bque\s+indica\b", r"\bque\s+significa\b",
)

# Negative-polarity stems: the "correct answer" is a deliberately FALSE statement
# (identify the incorrect/false/except option). Enriching these would feed the
# micro-drill a false statement as a true option — teaching the wrong thing.
# Excluded entirely (precision guard, added after batch-2 audit).
NEGATIVE_POLARITY_PATTERNS = (
    r"\bincorrect[ao]\b", r"\bfals[ao]\b", r"\bno\s+es\s+correct[ao]\b",
    r"\bexcepto\b", r"\bno\s+corresponde\b", r"\bmenos\s+probable\b",
    r"\bno\s+influye\b", r"\bno\s+es\s+cierto\b",
)

GOVERNANCE = {
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "formative_only": True,
    "derived_content": True,
    "uses_llm": False,
    "uses_api": False,
}

# ---------------------------------------------------------------------------
# Spanish layer for causal-chain nodes (learner-facing). A node that matches
# but has no entry here is NOT populated (localization guard, same policy as
# distinction_coach_exporter). `subject` is the noun phrase used by drills.
# ---------------------------------------------------------------------------
NODE_ES: dict[str, dict[str, str]] = {
    "CC_DESTEMMING_TANNIN_STRUCTURE": {
        "subject": "el despalillado antes de la fermentación",
        "causa": "Los raspones pueden estar presentes con las uvas antes de la fermentación y aportar taninos verdes y astringentes.",
        "mecanismo": "Si los raspones permanecen durante la fermentación, de ellos se extraen taninos y compuestos fenólicos verdes hacia el mosto.",
        "efecto": "El despalillado elimina esa fuente de taninos verdes, dando taninos más suaves y redondos y una estructura más limpia en boca.",
    },
    "CC_MACERATION_EXTRACTION": {
        "subject": "la maceración y la gestión del sombrero en tintos",
        "causa": "En la vinificación en tinto, el color y los taninos se extraen principalmente de los hollejos durante el contacto entre el mosto en fermentación y las partes sólidas.",
        "mecanismo": "La maceración y las técnicas de manejo del sombrero (remontado, bazuqueo, délestage) aumentan el contacto entre el líquido y los hollejos, permitiendo que pasen más color y taninos al vino.",
        "efecto": "Una mayor extracción produce tintos de color más profundo, mayor estructura tánica y una impresión más completa en boca.",
    },
    "CC_SOIL_DRAINAGE_VINE_VIGOUR": {
        "subject": "el drenaje del suelo y el vigor de la vid",
        "causa": "La textura y composición del suelo determinan la eficacia con la que el agua drena en el viñedo.",
        "mecanismo": "En suelos bien drenados, las raíces deben profundizar para encontrar agua, lo que limita el vigor excesivo de la planta y reduce los recursos destinados al follaje.",
        "efecto": "Un vigor menor favorece fruta más concentrada, con mejor concentración de sabor y, en general, mayor potencial de calidad.",
    },
    "CC_SPRING_FROST_TOPOGRAPHY": {
        "subject": "las heladas primaverales y la topografía del viñedo",
        "causa": "El riesgo de heladas primaverales depende en gran medida de la topografía del viñedo y del movimiento del aire frío por el terreno.",
        "mecanismo": "El aire frío es más denso que el cálido: desciende y se acumula en zonas bajas como valles y hondonadas, mientras que las laderas con buen drenaje de aire permiten que el aire frío se aleje.",
        "efecto": "Las vides en valles o depresiones están más expuestas a las heladas primaverales; las situadas en laderas con buen drenaje de aire frío tienen menor riesgo.",
    },
    "CC_SULPHITES_PRESERVATION": {
        "subject": "el uso de SO₂ y sus excesos",
        "causa": "El dióxido de azufre (SO₂) se usa como conservante antioxidante y antimicrobiano en la vinificación.",
        "mecanismo": "Usado en exceso, el SO₂ puede suprimir demasiado la actividad microbiana y fermentativa y dejar caracteres sulfurosos residuales perceptibles.",
        "efecto": "El vino puede mostrar aromas reductivos (cerilla, goma quemada, azufre) y su carácter frutal puede quedar enmascarado.",
    },
    "HC_OAK_AGEING_COMPLEXITY": {
        "subject": "la crianza en barrica de roble",
        "causa": "El vino criado en barrica de roble recibe pequeñas cantidades continuas de oxígeno a través de los poros de la madera y absorbe compuestos de la propia madera, como vainillina y lactonas.",
        "mecanismo": "La microoxigenación lenta suaviza los taninos por polimerización y redondea la estructura; a la vez, los compuestos de la madera aportan vainilla, especias, tostado y humo.",
        "efecto": "Los vinos criados en roble nuevo suelen mostrar taninos más suaves, mayor complejidad y aromas secundarios (vainilla, tostado, cedro, especias) sobre la fruta primaria.",
    },
    "CC_BOTTLE_AGEING_SEDIMENT": {
        "subject": "la crianza prolongada en botella de tintos estructurados",
        "causa": "Un tinto con suficiente tanino, pigmento y estructura se cría en botella durante un periodo prolongado (años o décadas).",
        "mecanismo": "Los taninos y los antocianos se polimerizan (se unen en moléculas mayores) y acaban precipitando; la estructura se suaviza a medida que disminuyen los taninos libres.",
        "efecto": "Se forma sedimento en la botella; el vino desarrolla aromas terciarios (cuero, tierra, fruta seca, champiñón, tabaco) y los taninos se integran y suavizan.",
    },
    "CC_FLOR_BIOLOGICAL_AGEING": {
        "subject": "la crianza biológica bajo velo de flor",
        "causa": "La levadura de flor (un velo de cepas de Saccharomyces cerevisiae) se forma en la superficie del vino en botas parcialmente llenas.",
        "mecanismo": "El velo protege al vino del oxígeno; la levadura metaboliza etanol y glicerol produciendo acetaldehído, y su autólisis aporta aminoácidos.",
        "efecto": "El vino desarrolla carácter de crianza biológica: notas de almendra, masa de pan y levadura, color pálido, tanino bajo y protección frente a la oxidación pese a la crianza en bota.",
    },
    "CC_FORTIFICATION_RESIDUAL_SUGAR": {
        "subject": "la fortificación durante la fermentación",
        "causa": "Se añade aguardiente vínico (alcohol neutro de alta graduación) a un mosto o vino parcialmente fermentado.",
        "mecanismo": "La adición eleva el alcohol hasta un nivel (típicamente 15–18% vol.) en el que la levadura no sobrevive: la fermentación se detiene y queda azúcar sin fermentar en el vino.",
        "efecto": "El vino terminado conserva azúcar residual del mosto sin fermentar, dando un estilo dulce o semidulce.",
    },
    "CC_FRACTIONAL_BLENDING_CONSISTENCY": {
        "subject": "el sistema de solera y criaderas",
        "causa": "Se establece un sistema de solera: una serie de botas (criaderas) ordenadas por edad, cada una con vino en distinta etapa de maduración.",
        "mecanismo": "Al extraer vino de las botas más viejas (la solera) para embotellar, estas se rellenan parcialmente con vino más joven de la siguiente criadera, y la cascada continúa por todos los niveles.",
        "efecto": "Cada saca contiene una mezcla de añadas; la incorporación constante de vino viejo y joven mantiene una edad media y un estilo estables año tras año.",
    },
}

_RA_TOPIC_RE = re.compile(r"^RA\d")

# --- Phase P.2 batch-2 knowledge expansion: ES layer for climate/site nodes ---
# Mechanism nodes only (explain the WHY). Attribute nodes (tannin sensation,
# generic warm->alcohol) intentionally excluded: high false-positive risk.
NODE_ES.update({
    "HC_ALTITUDE_TEMPERATURE": {
        "subject": "la altitud y su efecto sobre la temperatura y la acidez",
        "causa": "Los viñedos a mayor altitud experimentan temperaturas más bajas, sobre todo de noche, que los situados a menor elevación en la misma región.",
        "mecanismo": "Las temperaturas más bajas ralentizan la maduración y reducen la respiración nocturna que, de otro modo, consumiría ácido málico; así se conserva la acidez natural mientras el azúcar se acumula durante el día.",
        "efecto": "Los vinos de altura suelen mostrar mayor acidez total, más frescura y mayor precisión aromática; el alcohol puede ser más bajo si la maduración es incompleta.",
    },
    "HC_COOL_CLIMATE_STYLE": {
        "subject": "el clima fresco y su estilo de vino",
        "causa": "En las regiones de clima fresco, las temperaturas medias del periodo de maduración son lo bastante bajas como para que la uva madure despacio, a veces de forma incompleta, en una temporada más corta.",
        "mecanismo": "La maduración lenta y fresca preserva el ácido málico y tartárico de la uva, porque las noches no aceleran lo suficiente la respiración de los ácidos, y la acumulación de azúcar es más limitada.",
        "efecto": "Los vinos de clima fresco suelen presentar acidez alta, menor alcohol, cuerpo más ligero y aromas primarios que tienden a manzana verde, cítricos y notas herbáceas.",
    },
    "HC_DIURNAL_RANGE_FRESHNESS": {
        "subject": "la amplitud térmica entre el día y la noche",
        "causa": "Las regiones con gran amplitud térmica —donde los días cálidos favorecen la acumulación de azúcar pero las noches frescas frenan la respiración— generan un patrón de maduración característico.",
        "mecanismo": "El calor diurno permite que la fotosíntesis y el desarrollo de azúcar avancen, mientras que las noches frescas frenan la degradación respiratoria del ácido tartárico y málico, conservando la acidez.",
        "efecto": "Los vinos de gran amplitud térmica retienen más acidez, muestran un carácter aromático marcado y preciso, y suelen exhibir una frescura o vibración que los distingue de los de clima más cálido y uniforme.",
    },
    "HC_YIELD_CONCENTRATION": {
        "subject": "el bajo rendimiento y la concentración de la uva",
        "causa": "Cuando una vid produce menos racimos —por las condiciones del sitio, la variedad o técnicas como la vendimia verde— cada baya recibe una mayor proporción de los recursos de la planta.",
        "mecanismo": "Con menos racimos compitiendo por la producción fotosintética de la vid, cada baya acumula más azúcar, compuestos de sabor y componentes estructurales como antocianos y taninos.",
        "efecto": "Los vinos de vides de bajo rendimiento suelen mostrar mayor intensidad aromática, más concentración de sabor, color más pronunciado en tintos y taninos más estructurados.",
    },
    "CC_COOL_CLIMATE_ACIDITY": {
        "subject": "el clima fresco y la retención de acidez",
        "causa": "Un entorno de cultivo fresco (temperaturas más bajas, gran altitud o latitud alta) marca el ritmo de maduración de la uva.",
        "mecanismo": "La maduración lenta retrasa la acumulación de azúcar y preserva los ácidos naturales de la uva (málico y tartárico), reduciendo la velocidad a la que se metaboliza el málico antes de la vendimia.",
        "efecto": "Los vinos conservan mayor acidez, muestran frescura y nervio, y suelen tener niveles de alcohol más bajos.",
    },
    "HC_CONTINENTALITY_STYLE": {
        "subject": "el clima continental",
        "causa": "Un clima continental se da en regiones alejadas de la influencia moderadora de grandes masas de agua, con veranos cálidos pero inviernos fríos y una gran diferencia de temperatura entre estaciones y entre el día y la noche.",
        "mecanismo": "La temporada de cultivo corta y definida, con fuertes oscilaciones térmicas, hace que la uva madure en días cálidos mientras las noches frescas frenan la respiración del ácido málico y tartárico, conservando la acidez; el final abrupto de la temporada limita la sobremaduración.",
        "efecto": "Los vinos de clima continental suelen mostrar acidez alta, estructura tánica firme en tintos y una marcada variación entre añadas, porque la temporada ajustada hace que la madurez dependa mucho del clima del año.",
    },
    "HC_MARITIME_MODERATION": {
        "subject": "la influencia marítima u oceánica",
        "causa": "Un clima marítimo u oceánico se da en regiones próximas al mar o al océano, cuya gran masa térmica se calienta y se enfría lentamente a lo largo del año.",
        "mecanismo": "El agua cercana modera los extremos de temperatura: mantiene veranos más frescos e inviernos más suaves que los sitios de interior a la misma latitud, reduce el riesgo de heladas y de calor excesivo y alarga la temporada, aunque puede traer lluvia y humedad.",
        "efecto": "Los vinos de clima marítimo tienden a una maduración moderada y uniforme, con acidez conservada y elegancia; la temporada más larga y suave favorece estilos equilibrados, siendo la lluvia de la añada un riesgo clave.",
    },
    "HC_WATER_STRESS_CONCENTRATION": {
        "subject": "el estrés hídrico leve y la concentración de la uva",
        "causa": "El estrés hídrico leve ocurre cuando la vid dispone de un acceso al agua limitado pero no críticamente escaso durante la maduración, a menudo en suelos de buen drenaje o bajo riego controlado (por goteo) en climas secos.",
        "mecanismo": "El agua limitada hace que la vid frene el crecimiento de brotes y follaje y derive recursos a las bayas; el tamaño de la baya se mantiene pequeño, aumentando la proporción de piel respecto al jugo, mientras se concentran azúcar, antocianos y compuestos de sabor. Un estrés severo, en cambio, detiene la maduración.",
        "efecto": "El estrés hídrico leve tiende a producir bayas más pequeñas con mayor concentración de sabor, color y tanino y mayor potencial de calidad; el riego excesivo o la lluvia los diluyen y pueden reducir la calidad.",
    },
})


def _norm(text: str) -> str:
    """Lowercase + strip accents for robust word-boundary matching."""
    import unicodedata
    nfd = unicodedata.normalize("NFD", str(text).lower())
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def _es_contractions(text: str) -> str:
    """Spanish copy polish: 'de el' -> 'del', 'a el' -> 'al' (not before proper El)."""
    text = re.sub(r"\bde el\b", "del", text)
    text = re.sub(r"\ba el\b", "al", text)
    return text


def _has_word(trigger_norm: str, text_norm: str) -> bool:
    return re.search(r"(?<![0-9a-z])" + re.escape(trigger_norm) + r"(?![0-9a-z])", text_norm) is not None


def _is_identification_stem(stem: str) -> bool:
    stem_n = _norm(stem)
    return any(re.search(pat, stem_n) for pat in IDENTIFICATION_PATTERNS)


def _is_negative_polarity_stem(stem: str) -> bool:
    stem_n = _norm(stem)
    return any(re.search(pat, stem_n) for pat in NEGATIVE_POLARITY_PATTERNS)


def load_chain_nodes() -> list[dict]:
    nodes = []
    for path in sorted(CHAINS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        triggers = data.get("trigger_keywords")
        steps = data.get("steps")
        if not triggers or not steps:
            continue
        by_label = {s.get("label"): s.get("text", "") for s in steps}
        if not all(k in by_label for k in ("cause", "mechanism", "effect")):
            continue
        specific = [
            _norm(k) for k in triggers
            if len(_norm(k)) >= MIN_TRIGGER_LEN and _norm(k) not in GENERIC_TRIGGERS
        ]
        if not specific:
            continue  # node has no specific triggers left -> unusable
        nodes.append({
            "node_id": data.get("node_id") or data.get("chain_id"),
            "keywords": sorted(set(specific)),
        })
    return nodes


def load_frontend_items() -> list[dict]:
    src = FRONTEND_BANK.read_text(encoding="utf-8")
    payload = json.loads(src.split("=", 1)[1].rstrip().rstrip(";"))
    return payload["items"]


def match_item(item: dict, nodes: list[dict]):
    """Precision-first matching. Returns match dict or (None, reason)."""
    stem = item.get("text", "")
    if _is_identification_stem(stem):
        return None, "identification_stem"
    if _is_negative_polarity_stem(stem):
        return None, "negative_polarity_stem"
    ci = item.get("correct_index", 0)
    correct = (item.get("options") or [""])[ci]
    stem_n = _norm(stem)
    correct_n = _norm(correct)
    kw_n = _norm(" ".join(item.get("keywords", [])))
    surface_n = stem_n + " " + kw_n + " " + correct_n

    scored = []
    for node in nodes:
        all_hits = sorted({k for k in node["keywords"] if _has_word(k, surface_n)})
        if not all_hits:
            continue
        stem_hits = [k for k in all_hits if _has_word(k, stem_n)]
        correct_hits = [k for k in all_hits if _has_word(k, correct_n)]
        scored.append((len(all_hits), node["node_id"], all_hits, stem_hits, correct_hits))
    scored.sort(key=lambda t: (-t[0], t[1]))
    if not scored:
        return None, "no_hits"
    best = scored[0]
    if best[0] < MIN_KEYWORD_HITS:
        return None, "below_threshold"
    if REQUIRE_STEM_HIT and not best[3]:
        return None, "no_stem_hit"
    if REQUIRE_CORRECT_OPTION_HIT and not best[4]:
        return None, "no_correct_option_hit"
    if REQUIRE_UNIQUE_BEST and len(scored) > 1 and scored[1][0] == best[0]:
        return None, "ambiguous_tie"
    if best[1] not in NODE_ES:
        return None, "no_spanish_layer"
    return {
        "node_id": best[1],
        "matched_keywords": best[2],
        "stem_hits": best[3],
        "correct_option_hits": best[4],
        "score": best[0],
    }, None


def _numeric_id(item_id: str) -> int:
    m = re.search(r"(\d+)$", item_id)
    return int(m.group(1)) if m else 0


def select_batch(items: list[dict], nodes: list[dict]):
    pool, rejections = [], {}
    for item in items:
        match, reason = match_item(item, nodes)
        if match:
            pool.append({"item": item, "match": match})
        elif reason not in ("no_hits",):
            rejections[reason] = rejections.get(reason, 0) + 1
    pool.sort(key=lambda e: (
        not e["item"].get("gold", False),       # gold first
        e["item"].get("ra") != "RA2",           # prefer RA2
        -e["match"]["score"],                   # strongest signal
        _numeric_id(e["item"]["id"]),           # deterministic order
    ))
    return pool[:BATCH_SIZE], rejections


def topic_display(item: dict) -> str | None:
    topic = str(item.get("topic", "")).strip()
    if not topic or _RA_TOPIC_RE.match(topic):
        return None  # topic field is an RA echo -> not meaningful for learners
    return topic.replace("_", " ")


def build_feedback_by_mode(item: dict, chain_es: dict) -> dict:
    letter = item.get("correct_letter", "A")
    ci = item.get("correct_index", 0)
    correct = (item.get("options") or [""])[ci]
    ra = item.get("ra", "—")
    topic = topic_display(item)
    topic_part = f" Tema: {topic}." if topic else ""
    subject = chain_es["subject"]
    return {
        "mentor": _es_contractions(
            f"La respuesta correcta es {letter}: «{correct}». La clave está en {subject}: "
            f"{chain_es['mecanismo']} Por eso, {chain_es['efecto'][0].lower()}{chain_es['efecto'][1:]}"
        ),
        "trainer": _es_contractions(
            f"Concepto técnico ({ra}):{topic_part} Fija el mecanismo de {subject}: "
            f"{chain_es['causa']} → {chain_es['mecanismo']} "
            f"En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones."
        ),
        "reviewer": _es_contractions(
            f"Exigencia de repaso ({ra}): debes poder justificar por qué «{correct}» es correcta "
            f"y por qué las otras tres opciones no lo son, citando el mecanismo de {subject}. "
            f"Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3."
        ),
    }


def build_micro_drill(entry: dict, batch: list[dict]):
    """Node-anchored drill. Distractors = correct options of batch items matched
    to OTHER nodes (existing, true statements about different mechanisms)."""
    item = entry["item"]
    node_id = entry["match"]["node_id"]
    ci = item.get("correct_index", 0)
    correct = (item.get("options") or [""])[ci]
    if len(correct) < MIN_DRILL_OPTION_LEN:
        return None
    subject = NODE_ES[node_id]["subject"]

    pool = [
        e for e in batch
        if e["match"]["node_id"] != node_id
        and len((e["item"].get("options") or [""])[e["item"].get("correct_index", 0)]) >= MIN_DRILL_OPTION_LEN
    ]
    pool.sort(key=lambda e: _numeric_id(e["item"]["id"]))
    distractors, seen_nodes, seen_text = [], set(), {correct}
    for e in pool:
        if len(distractors) >= DRILL_DISTRACTOR_COUNT:
            break
        d_node = e["match"]["node_id"]
        d_text = (e["item"].get("options") or [""])[e["item"].get("correct_index", 0)]
        if d_node in seen_nodes or d_text in seen_text:
            continue
        distractors.append(d_text)
        seen_nodes.add(d_node)
        seen_text.add(d_text)
    if len(distractors) < DRILL_DISTRACTOR_COUNT:
        return None

    correct_index = int(hashlib.md5(item["id"].encode()).hexdigest(), 16) % (DRILL_DISTRACTOR_COUNT + 1)
    options = list(distractors)
    options.insert(correct_index, correct)
    return {
        "prompt": _es_contractions(f"Consolidación: ¿cuál de estas afirmaciones corresponde a {subject}?"),
        "options": options,
        "correct_index": correct_index,
        "explanation": _es_contractions(f"«{correct}» corresponde a {subject}. Las demás afirmaciones son correctas, pero describen otros mecanismos."),
        "remediation_signal": _es_contractions(f"Revisa la cadena causal de {subject}"),
    }


def derive() -> dict:
    nodes = load_chain_nodes()
    items = load_frontend_items()
    batch, rejections = select_batch(items, nodes)

    enriched = {}
    for entry in batch:
        item, match = entry["item"], entry["match"]
        chain_es = NODE_ES[match["node_id"]]
        record = {
            "item_id": item["id"],
            "causal_chain": {
                "causa": chain_es["causa"],
                "mecanismo": chain_es["mecanismo"],
                "efecto": chain_es["efecto"],
            },
            "feedback_by_mode": build_feedback_by_mode(item, chain_es),
            "_provenance": {
                "causal_chain": {
                    "derived_from": match["node_id"],
                    "matched_keywords": match["matched_keywords"],
                    "stem_hits": match["stem_hits"],
                    "correct_option_hits": match["correct_option_hits"],
                    "match_score": match["score"],
                },
                "feedback_by_mode": {"derived_from": f"template_v1 + {match['node_id']}"},
            },
        }
        drill = build_micro_drill(entry, batch)
        if drill:
            record["micro_drill"] = drill
            record["_provenance"]["micro_drill"] = {
                "derived_from": f"node_anchored_v1 ({match['node_id']})",
                "distractor_source": "correct options of batch items matched to other nodes",
            }
        enriched[item["source_question_id"]] = record

    fingerprint = hashlib.sha256(
        (FRONTEND_BANK.read_text(encoding="utf-8") + json.dumps(NODE_ES, sort_keys=True, ensure_ascii=False)).encode()
    ).hexdigest()[:16]

    return {
        "schema_version": "sba_enrichment_v1",
        "phase": "P.1-batch1-v2-precision",
        "derivation": {
            "min_keyword_hits": MIN_KEYWORD_HITS,
            "require_stem_hit": REQUIRE_STEM_HIT,
            "require_correct_option_hit": REQUIRE_CORRECT_OPTION_HIT,
            "require_unique_best": REQUIRE_UNIQUE_BEST,
            "word_boundary_matching": True,
            "generic_triggers_banned": sorted(GENERIC_TRIGGERS),
            "identification_stems_excluded": True,
            "batch_size": BATCH_SIZE,
            "policy": "precision first: populate only when the node explains the correct answer; omit otherwise; never invent content",
        },
        "rejection_stats": rejections,
        "input_fingerprint": fingerprint,
        "governance": dict(GOVERNANCE),
        "items_by_source_question_id": enriched,
    }


def write_sidecar(payload: dict | None = None) -> Path:
    data = payload or derive()
    if data["governance"]["safe_for_examiner"] is not False:
        raise ValueError("Governance violation")
    SIDECAR_OUT.parent.mkdir(parents=True, exist_ok=True)
    SIDECAR_OUT.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return SIDECAR_OUT


def write_report(payload: dict | None = None) -> Path:
    data = payload or derive()
    items = data["items_by_source_question_id"]
    bank = {i["id"]: i for i in load_frontend_items()}
    lines = [
        "# ENRICHMENT BATCH 1 — Reporte de muestra para aprobación",
        "",
        f"Lote: **{len(items)} ítems** · derivación determinista desde nodos causales CC_/HC_ "
        f"(umbral: ≥{MIN_KEYWORD_HITS} trigger keywords, mejor nodo único, capa ES con guard).",
        f"Con micro_drill: **{sum(1 for r in items.values() if 'micro_drill' in r)}** · "
        f"fingerprint de entrada: `{data['input_fingerprint']}`",
        "",
        "Política v2 (precisión primero): word-boundary, triggers genéricos prohibidos, el nodo debe",
        "explicar la respuesta correcta (hit en stem Y en opción correcta), stems de identificación excluidos.",
        "",
        f"Rechazos por regla: `{json.dumps(data.get('rejection_stats', {}), ensure_ascii=False)}`",
        "",
        "---",
        "",
    ]
    sample = list(items.items())[:REPORT_SAMPLE_SIZE]
    for sqid, rec in sample:
        item = bank[rec["item_id"]]
        prov = rec["_provenance"]["causal_chain"]
        ci = item.get("correct_index", 0)
        lines += [
            f"## {rec['item_id']} (sq {sqid}) · {item.get('ra')} · gold={item.get('gold')}",
            "",
            f"**Pregunta:** {item.get('text')}",
            f"**Correcta ({item.get('correct_letter')}):** {(item.get('options') or [''])[ci]}",
            f"**Nodo:** `{prov['derived_from']}` · score {prov['match_score']} · en stem: {', '.join(prov['stem_hits'])} · en respuesta correcta: {', '.join(prov['correct_option_hits'])}",
            "",
            f"- **Causa:** {rec['causal_chain']['causa']}",
            f"- **Mecanismo:** {rec['causal_chain']['mecanismo']}",
            f"- **Efecto:** {rec['causal_chain']['efecto']}",
            "",
            f"**Mentor Guía:** {rec['feedback_by_mode']['mentor']}",
            "",
            f"**Entrenador Técnico:** {rec['feedback_by_mode']['trainer']}",
            "",
            f"**Revisor Estricto:** {rec['feedback_by_mode']['reviewer']}",
            "",
        ]
        if "micro_drill" in rec:
            d = rec["micro_drill"]
            lines.append(f"**Micro-drill:** {d['prompt']}")
            for idx, opt in enumerate(d["options"]):
                mark = " ✅" if idx == d["correct_index"] else ""
                lines.append(f"  - {chr(65+idx)}. {opt}{mark}")
            lines.append(f"  - _Explicación:_ {d['explanation']}")
        else:
            lines.append("**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.")
        lines += ["", "---", ""]
    lines += [
        "",
        "*Documento formativo. Sin autoridad de examinador. safe_for_examiner: false.*",
        "",
    ]
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")
    return REPORT_OUT


if __name__ == "__main__":
    payload = derive()
    sidecar = write_sidecar(payload)
    report = write_report(payload)
    n = len(payload["items_by_source_question_id"])
    drills = sum(1 for r in payload["items_by_source_question_id"].values() if "micro_drill" in r)
    print(f"Sidecar: {sidecar} ({n} items, {drills} drills)")
    print(f"Report:  {report}")
