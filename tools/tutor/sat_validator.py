"""SAT Answer Validator — Phase X.3/X.4 runtime consumer.

Deterministic, formative-only validator for WSET Level 3 SAT responses.
Consumes Phase X.1 knowledge assets from:
  knowledge/sat-framework/
  knowledge/evaluator-framework/
  knowledge/distinction-patterns/

GOVERNANCE INVARIANTS (immutable):
  safe_for_examiner = False
  examiner_scoring_allowed = False
  no marks assigned
  formative guidance only
  deterministic output
  zero LLM / zero API

Input schema (dict):
  wine_type: "white" | "red" | "sparkling" | "rosé" | "sweet"  (default "white")
  is_simple: bool   -- caller declares wine is simple (affects exception logic)
  appearance:
    clarity: str | None
    intensity: str | None
    colour: str | None
  nose:
    intensity: str | None
    primary_aromas: list[str]
    secondary_aromas: list[str]
    tertiary_aromas: list[str]
    development: str | None
    is_simple: bool
  palate:
    sweetness: str | None
    acidity: str | None
    tannin: str | None          (red wine)
    alcohol: str | None
    body: str | None
    mousse: str | None          (sparkling)
    flavour_intensity: str | None
    primary_flavours: list[str]
    secondary_flavours: list[str]
    tertiary_flavours: list[str]
    finish: str | None
    is_simple: bool
  conclusions:
    quality_level: str | None
    readiness: str | None

Output (all keys always present):
  governance: dict
  structural_issues: list[str]
  scale_errors: list[str]
  mark_allocation_feedback: dict
  simple_wine_exception: dict
  quality_justification: dict
  readiness_reasoning: dict        (Phase X.4)
  response_structure: dict         (Phase X.5)
  distinction_gap: dict
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Governance constants — immutable
# ---------------------------------------------------------------------------
VALIDATOR_GOVERNANCE: dict[str, Any] = {
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "uses_llm": False,
    "uses_api": False,
    "uses_embeddings": False,
    "uses_vector_db": False,
    "cloud_services_active": False,
    "formative_only": True,
    "no_marks_assigned": True,
}

# ---------------------------------------------------------------------------
# Knowledge asset paths
# ---------------------------------------------------------------------------
_KR = Path("knowledge")
_SAT_STRUCTURE_PATH = _KR / "sat-framework" / "sat_structure.json"
_SAT_SCALES_PATH = _KR / "sat-framework" / "sat_scales.json"
_SAT_QUALITY_PATH = _KR / "sat-framework" / "sat_quality_framework.json"
_MARK_ALLOC_PATH = _KR / "evaluator-framework" / "mark_allocation_rules.json"
_DESCRIPTOR_PATTERNS_PATH = _KR / "distinction-patterns" / "descriptor_patterns.json"
_QUALITY_REASONING_PATH = _KR / "distinction-patterns" / "quality_reasoning_patterns.json"
_READINESS_PATTERNS_PATH = _KR / "distinction-patterns" / "readiness_reasoning_patterns.json"
_RESPONSE_STRUCTURES_PATH = _KR / "distinction-patterns" / "response_structures.json"
_EVIDENCE_REQ_PATH = _KR / "evaluator-framework" / "evidence_requirements.json"

# ---------------------------------------------------------------------------
# Scale value sets — built from sat_scales.json at module load
# ---------------------------------------------------------------------------

def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_scale_sets() -> dict[str, frozenset[str]]:
    """Return scale lookup dict with qualified keys to avoid section collisions.

    Keys: both "section.element" (always) and unqualified "element" when
    the element name is unique across all sections.
    "intensity" appears in both appearance and nose — always use qualified form.
    """
    scales = _load_json(_SAT_SCALES_PATH)["scales"]
    result: dict[str, frozenset[str]] = {}
    seen: dict[str, int] = {}

    for section, elements in scales.items():
        for element, spec in elements.items():
            vals = spec.get("values", [])
            if not isinstance(vals, list):
                continue
            fset = frozenset(v.lower().strip() for v in vals)
            result[f"{section}.{element}"] = fset
            seen[element] = seen.get(element, 0) + 1

    # Unqualified alias only for elements that appear in exactly one section
    for section, elements in scales.items():
        for element, spec in elements.items():
            if seen.get(element, 0) == 1:
                vals = spec.get("values", [])
                if isinstance(vals, list):
                    result[element] = frozenset(v.lower().strip() for v in vals)

    return result


_SCALE_SETS: dict[str, frozenset[str]] = _build_scale_sets()

# Quality level valid values
_QUALITY_VALID: frozenset[str] = _SCALE_SETS.get(
    "quality_level",
    frozenset(["defectuoso", "pobre", "aceptable", "bueno", "muy bueno", "excelente"])
)

# Readiness valid values — from readiness_reasoning_patterns.json
_READINESS_HAS_POTENTIAL = "se puede beber ahora, pero tiene potencial para el envejecimiento"
_READINESS_DRINK_NOW = "beber ahora: no adecuado para el envejecimiento o para un mayor envejecimiento"
_READINESS_TOO_YOUNG = "demasiado joven"
_READINESS_TOO_OLD = "demasiado viejo"
_READINESS_VALID: frozenset[str] = frozenset([
    _READINESS_HAS_POTENTIAL,
    _READINESS_DRINK_NOW,
    _READINESS_TOO_YOUNG,
    _READINESS_TOO_OLD,
])

# Tertiary descriptor keywords — for simple-wine violation detection
_TERTIARY_KEYWORDS: frozenset[str] = frozenset([
    "miel", "honey", "nuez", "nutty", "avellana", "petróleo", "kerosene", "queroseno",
    "mermelada", "cuero", "leather", "tabaco", "tobacco", "piso forestal", "forest floor",
    "tierra", "champiñón", "mushroom", "caza", "ciruela pasa", "prune",
    "higo", "alquitrán", "albaricoque seco", "dried apricot", "heno",
    "almendra", "hazelnut", "walnut", "toffee", "caramelo",
    "café", "chocolate",  # can be tertiary oxidative
    "hojas mojadas", "vegetal", "cárnico",
])

# Generic (non-specific) descriptors — penalised in distinction gap
_GENERIC_DESCRIPTORS: frozenset[str] = frozenset([
    "frutal", "fruity", "complejo", "complex", "agradable", "nice", "bueno",
    "pleasant", "pleasurable", "rico", "rich flavor", "nice fruit",
    "aromas agradables", "buen aroma",
])

# Known secondary descriptors (for category-error detection)
_SECONDARY_DESCRIPTORS: frozenset[str] = frozenset([
    "vainilla", "vanilla", "cedro", "cedar", "ahumado", "smoke", "humo",
    "clavo", "cloves", "mantequilla", "butter", "nata", "cream",
    "galleta", "biscuit", "pan", "bread", "brioche", "tostado", "toast",
    "pastelería", "nuez moscada", "coco", "butterscotch",
])

# Known tertiary descriptors (for category-error detection if placed in primary)
_TERTIARY_ONLY_DESCRIPTORS: frozenset[str] = frozenset([
    "miel", "honey", "petróleo", "queroseno", "kerosene", "petrol",
    "cuero", "leather", "tabaco", "tobacco", "piso forestal", "forest floor",
    "tierra", "champiñón", "mushroom", "ciruela pasa", "prune",
    "albaricoque seco", "dried apricot",
])


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_sat_response(response: dict[str, Any]) -> dict[str, Any]:
    """Validate a SAT response dict and return structured formative guidance.

    Returns a dict with keys:
      governance, structural_issues, scale_errors,
      mark_allocation_feedback, simple_wine_exception,
      quality_justification, distinction_gap
    """
    wine_type = str(response.get("wine_type", "white")).lower()
    is_simple_top = bool(response.get("is_simple", False))

    appearance = response.get("appearance") or {}
    nose = response.get("nose") or {}
    palate = response.get("palate") or {}
    conclusions = response.get("conclusions") or {}

    nose_simple = bool(nose.get("is_simple", False)) or is_simple_top
    palate_simple = bool(palate.get("is_simple", False)) or is_simple_top

    structural_issues = _check_structural_completeness(
        wine_type, appearance, nose, palate, conclusions
    )
    scale_errors = _check_scale_values(wine_type, appearance, nose, palate, conclusions)
    mark_feedback = _build_mark_allocation_feedback(
        wine_type, appearance, nose, palate, conclusions,
        nose_simple, palate_simple
    )
    simple_exc = _check_simple_wine_exception(
        nose, palate, nose_simple, palate_simple
    )
    quality_just = _check_quality_justification(nose, palate, conclusions)
    readiness = _check_readiness_reasoning(nose, palate, conclusions, is_simple_top)
    response_structure = _check_response_structure(wine_type, nose, palate, is_simple_top)
    distinction = _build_distinction_gap_report(nose, palate)

    return {
        "governance": dict(VALIDATOR_GOVERNANCE),
        "structural_issues": structural_issues,
        "scale_errors": scale_errors,
        "mark_allocation_feedback": mark_feedback,
        "simple_wine_exception": simple_exc,
        "quality_justification": quality_just,
        "readiness_reasoning": readiness,
        "response_structure": response_structure,
        "distinction_gap": distinction,
    }


# ---------------------------------------------------------------------------
# Component 1 — Structural completeness
# ---------------------------------------------------------------------------

def _check_structural_completeness(
    wine_type: str,
    appearance: dict,
    nose: dict,
    palate: dict,
    conclusions: dict,
) -> list[str]:
    issues: list[str] = []

    # Appearance
    if not appearance.get("intensity"):
        issues.append("Aspecto: falta intensidad del color (pálida / media / profunda)")
    if not appearance.get("colour"):
        issues.append("Aspecto: falta indicación de color")

    # Nose
    if not nose.get("intensity"):
        issues.append("Nariz: falta intensidad del aroma (ligera / media / media(+) / pronunciada)")
    primaries = _str_list(nose.get("primary_aromas"))
    if not primaries:
        issues.append("Nariz: falta al menos un descriptor de aroma primario")
    if not nose.get("development"):
        issues.append("Nariz: falta estado de evolución (joven / en evolución / evolucionado)")

    # Palate — core elements always required
    required_palate = {
        "sweetness": "dulzor",
        "acidity": "acidez",
        "alcohol": "alcohol",
        "body": "cuerpo",
        "flavour_intensity": "intensidad del sabor",
        "finish": "final",
    }
    for key, label in required_palate.items():
        if not palate.get(key):
            issues.append(f"Boca: falta {label}")

    if wine_type == "red" and not palate.get("tannin"):
        issues.append("Boca: falta tanino (obligatorio para vino tinto)")
    if wine_type == "sparkling" and not palate.get("mousse"):
        issues.append("Boca: falta burbuja/mousse (obligatorio para vino espumoso)")

    primary_flavours = _str_list(palate.get("primary_flavours"))
    if not primary_flavours:
        issues.append("Boca: falta al menos un descriptor de sabor primario")

    # Conclusions
    if not conclusions.get("quality_level"):
        issues.append("Conclusiones: falta nivel de calidad")
    if not conclusions.get("readiness"):
        issues.append("Conclusiones: falta estado para el consumo/potencial")

    return issues


# ---------------------------------------------------------------------------
# Component 2 — Scale value validation
# ---------------------------------------------------------------------------

def _check_scale_values(
    wine_type: str,
    appearance: dict,
    nose: dict,
    palate: dict,
    conclusions: dict,
) -> list[str]:
    errors: list[str] = []

    checks: list[tuple[str, Any, str]] = [
        ("appearance.intensity", appearance.get("intensity"), "appearance.intensity"),
        ("nose.intensity", nose.get("intensity"), "nose.intensity"),
        ("nose.development", nose.get("development"), "development"),
        ("palate.sweetness", palate.get("sweetness"), "sweetness"),
        ("palate.acidity", palate.get("acidity"), "acidity"),
        ("palate.alcohol", palate.get("alcohol"), "alcohol"),
        ("palate.body", palate.get("body"), "body"),
        ("palate.flavour_intensity", palate.get("flavour_intensity"), "flavour_intensity"),
        ("palate.finish", palate.get("finish"), "finish"),
        ("conclusions.quality_level", conclusions.get("quality_level"), "quality_level"),
    ]
    if wine_type == "red":
        checks.append(("palate.tannin", palate.get("tannin"), "tannin"))
    if wine_type == "sparkling":
        checks.append(("palate.mousse", palate.get("mousse"), "mousse"))

    for field_path, value, scale_name in checks:
        if value is None:
            continue  # absence already caught by structural check
        valid = _SCALE_SETS.get(scale_name, frozenset())
        if valid and str(value).lower().strip() not in valid:
            errors.append(
                f"Valor de escala inválido en '{field_path}': «{value}». "
                f"Valores permitidos: {sorted(valid)}"
            )

    return errors


# ---------------------------------------------------------------------------
# Component 3 — Mark allocation feedback (no marks assigned)
# ---------------------------------------------------------------------------

def _build_mark_allocation_feedback(
    wine_type: str,
    appearance: dict,
    nose: dict,
    palate: dict,
    conclusions: dict,
    nose_simple: bool,
    palate_simple: bool,
) -> dict[str, Any]:
    feedback: dict[str, Any] = {}

    # Appearance
    a_present = [k for k in ("intensity", "colour") if appearance.get(k)]
    feedback["appearance"] = {
        "coverage": "complete" if len(a_present) == 2 else (
            "partial" if a_present else "missing"
        ),
        "elements_present": a_present,
        "elements_missing": [k for k in ("intensity", "colour") if not appearance.get(k)],
        "guidance": (
            "Aspecto completo."
            if len(a_present) == 2
            else "Aspecto incompleto: añade los elementos que faltan."
        ),
    }

    # Nose
    nose_primaries = _str_list(nose.get("primary_aromas"))
    nose_secondaries = _str_list(nose.get("secondary_aromas"))
    nose_tertiaries = _str_list(nose.get("tertiary_aromas"))
    nose_intensity = bool(nose.get("intensity"))
    nose_development = bool(nose.get("development"))

    if nose_simple:
        nose_guidance = (
            "Nariz (vino simple): correcto declarar «simple» + aromas primarios. "
            "No se esperan descriptores secundarios ni terciarios."
        )
        nose_coverage = "complete" if (nose_intensity and nose_primaries and nose_development) else "partial"
    else:
        missing_nose = []
        if not nose_secondaries:
            missing_nose.append("aromas secundarios (roble/FML/lías)")
        if not nose_tertiaries:
            missing_nose.append("aromas terciarios (crianza en botella)")
        if not nose_intensity:
            missing_nose.append("intensidad")
        if not nose_development:
            missing_nose.append("evolución")
        nose_coverage = "complete" if not missing_nose else "partial"
        nose_guidance = (
            "Nariz completa." if not missing_nose
            else f"Nariz parcial — faltan: {', '.join(missing_nose)}."
        )

    feedback["nose"] = {
        "coverage": nose_coverage,
        "primary_aromas_count": len(nose_primaries),
        "secondary_present": bool(nose_secondaries),
        "tertiary_present": bool(nose_tertiaries),
        "development_stated": nose_development,
        "guidance": nose_guidance,
    }

    # Palate
    core_palate_keys = ["sweetness", "acidity", "alcohol", "body",
                        "flavour_intensity", "finish"]
    if wine_type == "red":
        core_palate_keys.insert(2, "tannin")
    if wine_type == "sparkling":
        core_palate_keys.append("mousse")

    palate_present = [k for k in core_palate_keys if palate.get(k)]
    palate_missing = [k for k in core_palate_keys if not palate.get(k)]
    p_primaries = _str_list(palate.get("primary_flavours"))
    p_secondaries = _str_list(palate.get("secondary_flavours"))
    p_tertiaries = _str_list(palate.get("tertiary_flavours"))

    palate_flavour_issues = []
    if palate_simple:
        if p_secondaries or p_tertiaries:
            palate_flavour_issues.append(
                "Vino declarado simple: no se esperan sabores secundarios/terciarios"
            )
    else:
        if not p_secondaries:
            palate_flavour_issues.append("faltan sabores secundarios")
        if not p_tertiaries:
            palate_flavour_issues.append("faltan sabores terciarios")

    palate_coverage = (
        "complete" if not palate_missing and not palate_flavour_issues
        else "partial" if palate_present
        else "missing"
    )
    guidance_parts = []
    if palate_missing:
        guidance_parts.append(f"Elementos de escala faltantes: {', '.join(palate_missing)}")
    if palate_flavour_issues:
        guidance_parts.extend(palate_flavour_issues)

    feedback["palate"] = {
        "coverage": palate_coverage,
        "scale_elements_present": palate_present,
        "scale_elements_missing": palate_missing,
        "primary_flavours_count": len(p_primaries),
        "secondary_present": bool(p_secondaries),
        "tertiary_present": bool(p_tertiaries),
        "guidance": " | ".join(guidance_parts) if guidance_parts else "Boca completa.",
    }

    # Conclusions
    q_present = bool(conclusions.get("quality_level"))
    r_present = bool(conclusions.get("readiness"))
    feedback["conclusions"] = {
        "coverage": "complete" if (q_present and r_present) else (
            "partial" if (q_present or r_present) else "missing"
        ),
        "quality_level_stated": q_present,
        "readiness_stated": r_present,
        "guidance": (
            "Conclusiones completas."
            if (q_present and r_present)
            else "Conclusiones incompletas: añade nivel de calidad y estado para el consumo."
        ),
    }

    return feedback


# ---------------------------------------------------------------------------
# Component 4 — Simple wine exception enforcer
# ---------------------------------------------------------------------------

def _check_simple_wine_exception(
    nose: dict,
    palate: dict,
    nose_simple: bool,
    palate_simple: bool,
) -> dict[str, Any]:
    """Detect tertiary aromas/flavours for a wine declared simple.

    A learner declaring the wine 'simple' should NOT include tertiary descriptors —
    doing so is the most costly structural error on simple-wine SATs.
    """
    nose_tertiaries = _str_list(nose.get("tertiary_aromas"))
    palate_tertiaries = _str_list(palate.get("tertiary_flavours"))

    # Also scan primary lists for known tertiary-only terms (misplaced category)
    nose_primaries = _str_list(nose.get("primary_aromas"))
    palate_primaries = _str_list(palate.get("primary_flavours"))
    misplaced_in_primary = [
        d for d in nose_primaries + palate_primaries
        if d.lower().strip() in _TERTIARY_ONLY_DESCRIPTORS
    ]

    is_applicable = nose_simple or palate_simple
    violation = False
    messages: list[str] = []

    if is_applicable:
        if nose_tertiaries:
            violation = True
            messages.append(
                f"Nariz: se declaró «simple» pero se incluyen aromas terciarios: "
                f"{nose_tertiaries}. Para un vino simple, los terciarios no aplican — "
                f"no los inventes ni los incluyas."
            )
        if palate_tertiaries:
            violation = True
            messages.append(
                f"Boca: se declaró «simple» pero se incluyen sabores terciarios: "
                f"{palate_tertiaries}. Para un vino simple, los terciarios no aplican."
            )
        if misplaced_in_primary:
            violation = True
            messages.append(
                f"Descriptores terciarios encontrados en la lista de primarios: "
                f"{misplaced_in_primary}. Comprueba la categoría."
            )

    return {
        "is_applicable": is_applicable,
        "declared_simple_nose": nose_simple,
        "declared_simple_palate": palate_simple,
        "violation": violation,
        "messages": messages,
        "guidance": (
            "No aplica — el vino no fue declarado simple."
            if not is_applicable
            else (
                "Excepción de vino simple correctamente aplicada: no se encontraron terciarios inapropiados."
                if not violation
                else " ".join(messages)
            )
        ),
    }


# ---------------------------------------------------------------------------
# Component 5 — Quality justification checker
# ---------------------------------------------------------------------------

def _check_quality_justification(
    nose: dict,
    palate: dict,
    conclusions: dict,
) -> dict[str, Any]:
    """Verify the quality level claimed is supported by tasting observations."""
    quality = str(conclusions.get("quality_level") or "").lower().strip()
    if not quality:
        return {
            "quality_stated": None,
            "alignment": "missing",
            "supporting_evidence": [],
            "missing_evidence": ["No se indicó nivel de calidad."],
            "guidance": "Añade un nivel de calidad de la escala oficial.",
        }

    nose_primaries = _str_list(nose.get("primary_aromas"))
    nose_secondaries = _str_list(nose.get("secondary_aromas"))
    nose_tertiaries = _str_list(nose.get("tertiary_aromas"))
    nose_intensity = str(nose.get("intensity") or "").lower().strip()
    finish = str(palate.get("finish") or "").lower().strip()
    nose_simple = bool(nose.get("is_simple", False))
    palate_simple = bool(palate.get("is_simple", False))
    is_simple = nose_simple or palate_simple

    supporting: list[str] = []
    missing: list[str] = []

    has_secondary = bool(nose_secondaries) or bool(_str_list(palate.get("secondary_flavours")))
    has_tertiary = bool(nose_tertiaries) or bool(_str_list(palate.get("tertiary_flavours")))
    has_primary = bool(nose_primaries)
    has_long_finish = finish in {"largo", "medio(+)"}
    has_pronounced = nose_intensity in {"pronunciada", "media(+)"}

    # Evidence assessment per quality level
    if quality == "excelente":
        if has_tertiary:
            supporting.append("aromas/sabores terciarios presentes")
        else:
            missing.append("aromas terciarios requeridos para 'excelente' — no encontrados")
        if has_long_finish:
            supporting.append(f"final {finish}")
        else:
            missing.append("final largo o medio(+) requerido para 'excelente'")
        if has_secondary:
            supporting.append("aromas/sabores secundarios presentes")
        else:
            missing.append("aromas secundarios requeridos para 'excelente'")
        if has_pronounced:
            supporting.append(f"intensidad {nose_intensity}")
        else:
            missing.append("intensidad pronunciada o media(+) requerida para 'excelente'")

    elif quality == "muy bueno":
        if has_secondary:
            supporting.append("aromas/sabores secundarios presentes")
        else:
            missing.append("aromas secundarios requeridos para 'muy bueno'")
        if has_tertiary:
            supporting.append("aromas/sabores terciarios presentes")
        else:
            missing.append("aromas terciarios esperados para 'muy bueno'")
        if has_long_finish:
            supporting.append(f"final {finish}")
        else:
            missing.append("final medio(+) o largo esperado para 'muy bueno'")

    elif quality == "bueno":
        if has_primary:
            supporting.append("aromas primarios presentes")
        if has_secondary:
            supporting.append("alguna complejidad secundaria")
        if has_tertiary:
            missing.append(
                "Para 'bueno' con terciarios presentes, considera si 'muy bueno' o 'excelente' sería más adecuado"
            )

    elif quality == "aceptable":
        if is_simple:
            supporting.append("vino declarado simple — 'aceptable' es coherente")
        else:
            if not has_secondary and not has_tertiary:
                supporting.append("sin complejidad secundaria/terciaria — coherente con 'aceptable'")
            else:
                missing.append(
                    "Se detectan secundarios/terciarios — 'aceptable' podría estar por debajo del nivel real del vino"
                )

    elif quality in {"defectuoso", "pobre"}:
        if any("turbio" in str(v).lower() for v in [
            nose.get("intensity"), palate.get("sweetness")
        ]):
            supporting.append("indicadores de defecto detectados")
        else:
            missing.append(
                f"Para '{quality}' se requiere identificar un defecto específico o desequilibrio claro"
            )

    # Overclaim / underclaim detection
    alignment: str
    if quality == "excelente" and len(missing) >= 2:
        alignment = "overclaimed"
    elif quality in {"aceptable", "pobre"} and has_secondary and has_tertiary:
        alignment = "underclaimed"
    elif not missing:
        alignment = "aligned"
    elif not supporting:
        alignment = "unsupported"
    else:
        alignment = "partially_supported"

    guidance_map = {
        "aligned": "El nivel de calidad está bien justificado por las observaciones de cata.",
        "overclaimed": (
            f"Nivel '{quality}' puede estar sobredimensionado. "
            f"Evidencia que falta: {'; '.join(missing)}."
        ),
        "underclaimed": (
            f"Nivel '{quality}' puede estar por debajo del nivel real. "
            "El vino muestra complejidad secundaria y terciaria."
        ),
        "unsupported": (
            f"No se encontró evidencia que sustente '{quality}'. "
            f"Añade observaciones que justifiquen este nivel."
        ),
        "partially_supported": (
            f"Justificación parcial para '{quality}'. "
            + (f"Evidencia presente: {'; '.join(supporting)}. " if supporting else "")
            + (f"Falta: {'; '.join(missing)}." if missing else "")
        ),
        "missing": "Indica un nivel de calidad.",
    }

    return {
        "quality_stated": quality,
        "alignment": alignment,
        "supporting_evidence": supporting,
        "missing_evidence": missing,
        "guidance": guidance_map.get(alignment, ""),
    }


# ---------------------------------------------------------------------------
# Component 6 — Readiness reasoning checker (Phase X.4)
# ---------------------------------------------------------------------------

def _check_readiness_reasoning(
    nose: dict,
    palate: dict,
    conclusions: dict,
    is_simple: bool,
) -> dict[str, Any]:
    """Verify the readiness/drinking-window claim is consistent with SAT observations.

    Consumes readiness_reasoning_patterns.json signal mapping.
    Returns formative guidance only. No marks assigned. safe_for_examiner: False.

    Alignment values:
      aligned | overclaimed | inconsistent | partially_supported |
      missing | invalid_scale_value
    """
    readiness = str(conclusions.get("readiness") or "").lower().strip()

    if not readiness:
        return {
            "readiness_stated": None,
            "alignment": "missing",
            "consistency_issues": [],
            "guidance": (
                "No se indicó estado para el consumo. "
                "Añade el readiness usando uno de los valores oficiales de la escala."
            ),
        }

    if readiness not in _READINESS_VALID:
        return {
            "readiness_stated": readiness,
            "alignment": "invalid_scale_value",
            "consistency_issues": [
                f"«{readiness}» no es un valor oficial de readiness."
            ],
            "guidance": (
                "Usa exactamente uno de los valores de escala oficiales: "
                f"{sorted(_READINESS_VALID)}"
            ),
        }

    # Gather observation signals
    nose_development = str(nose.get("development") or "").lower().strip()
    nose_secondaries = _str_list(nose.get("secondary_aromas"))
    nose_tertiaries = _str_list(nose.get("tertiary_aromas"))
    palate_finish = str(palate.get("finish") or "").lower().strip()
    p_secondaries = _str_list(palate.get("secondary_flavours"))
    p_tertiaries = _str_list(palate.get("tertiary_flavours"))

    has_secondary = bool(nose_secondaries) or bool(p_secondaries)
    has_tertiary = bool(nose_tertiaries) or bool(p_tertiaries)
    has_long_finish = palate_finish in {"largo", "medio(+)"}
    is_developed = nose_development in {"en evolución", "evolucionado"}
    is_young_development = nose_development == "joven"

    issues: list[str] = []
    alignment = "aligned"

    if readiness == _READINESS_HAS_POTENTIAL:
        # Overclaim: simple wine cannot have ageing potential
        if is_simple:
            issues.append(
                "Vino declarado simple: afirmar 'potencial de guarda' no es coherente. "
                "Un vino simple no tiene la estructura para el envejecimiento."
            )
            alignment = "overclaimed"
        # Overclaim: no secondary or tertiary development to support ageing
        elif not has_secondary and not has_tertiary:
            issues.append(
                "Se afirma potencial de guarda pero no se detectaron aromas/sabores "
                "secundarios ni terciarios. El potencial de envejecimiento se apoya en "
                "complejidad de desarrollo — justifica qué estructura lo sustenta."
            )
            alignment = "overclaimed"
        # Weak support: young development, no finish evidence
        elif is_young_development and not has_long_finish:
            issues.append(
                "Desarrollo 'joven' sin final medio(+) o largo: el potencial de guarda "
                           "puede estar poco sustentado. Menciona qué característica justifica el envejecimiento."
            )
            alignment = "partially_supported"

    elif readiness == _READINESS_DRINK_NOW:
        # Inconsistent: tertiary aromas suggest some development and potential
        if has_tertiary and not is_simple:
            issues.append(
                "Se detectan aromas/sabores terciarios pero se declara sin potencial de guarda. "
                "Los terciarios indican cierto desarrollo — considera si el vino aún tiene algo de potencial."
            )
            alignment = "partially_supported"
        # Inconsistent: long finish without ageing potential is unusual
        elif has_long_finish and has_secondary and not is_simple:
            issues.append(
                "Final largo y complejidad secundaria con 'sin potencial de guarda': "
                "si el vino tiene final largo y aromas secundarios, "
                "considera si 'se puede beber ahora, pero tiene potencial' sería mas adecuado."
            )
            alignment = "partially_supported"

    elif readiness == _READINESS_TOO_YOUNG:
        # Inconsistent: developed nose contradicts "too young"
        if is_developed:
            issues.append(
                f"Evolucion '{nose_development}' es inconsistente con 'demasiado joven'. "
                "Un vino en evolucion o evolucionado ya ha superado la fase de cierre."
            )
            alignment = "inconsistent"
        # Weak signal: tertiary aromas contradict "too young"
        elif has_tertiary:
            issues.append(
                "Aromas terciarios presentes pero se declara 'demasiado joven'. "
                "Los terciarios indican desarrollo avanzado -- revisa la coherencia."
            )
            alignment = "partially_supported"

    elif readiness == _READINESS_TOO_OLD:
        # Inconsistent: young development contradicts "too old"
        if is_young_development:
            issues.append(
                "Desarrollo 'joven' es inconsistente con 'demasiado viejo'. "
                "Un vino con desarrollo joven raramente esta pasado."
            )
            alignment = "inconsistent"

    guidance = (
        "Readiness justificado y coherente con las observaciones de cata."
        if not issues
        else " | ".join(issues)
    )

    return {
        "readiness_stated": readiness,
        "alignment": alignment,
        "consistency_issues": issues,
        "guidance": guidance,
    }


# ---------------------------------------------------------------------------
# Component 8 -- Response structure / ordering validator (Phase X.5)
# ---------------------------------------------------------------------------

def _check_response_structure(
    wine_type: str,
    nose: dict,
    palate: dict,
    is_simple: bool,
) -> dict[str, Any]:
    """Check internal ordering and structural conventions within SAT sections.

    Consumes response_structures.json information_ordering_principles.
    Checks:
      1. Nose development position: should be stated after aromas (not before primaries)
      2. Palate ordering: scale values before flavour descriptors
      3. Wine-type structural consistency (simple vs complex vs sweet)
      4. Mandatory information_ordering_principles compliance

    Returns formative guidance only. No marks exposed. safe_for_examiner: False.
    """
    issues: list[str] = []
    guidance: list[str] = []

    # --- Nose: development must come last (after aromas) ---
    # Proxy: if development is stated but no primary aromas, ordering is suspicious
    nose_development = str(nose.get("development") or "").strip()
    nose_primaries = _str_list(nose.get("primary_aromas"))
    nose_secondaries = _str_list(nose.get("secondary_aromas"))
    nose_tertiaries = _str_list(nose.get("tertiary_aromas"))

    if nose_development and not nose_primaries:
        issues.append("ordering_nose_development_without_aromas")
        guidance.append(
            "Nariz: se indica estado de evolucion pero no hay descriptores de aroma. "
            "El orden correcto es: intensidad → aromas primarios → secundarios → terciarios → evolucion al final."
        )

    # --- Palate: scale values before flavour descriptors ---
    # Check: if flavour descriptors present but structural scale values missing,
    # the learner may have put descriptors first and omitted scale values
    p_primaries = _str_list(palate.get("primary_flavours"))
    has_flavours = bool(p_primaries)
    missing_scale = []
    for key in ("sweetness", "acidity", "alcohol", "body", "flavour_intensity"):
        if not palate.get(key):
            missing_scale.append(key)
    if has_flavours and missing_scale:
        issues.append("ordering_palate_flavours_before_scale")
        guidance.append(
            "Boca: se registran sabores pero faltan valores de escala estructurales. "
            "El orden correcto es: dulzor → acidez → [tanino] → alcohol → cuerpo → intensidad → "
            "sabores → final. Completa los valores de escala antes de los descriptores."
        )

    # --- Mandatory ordering principles ---
    # Quality must be stated before readiness (checked via structural completeness,
    # but we can note ordering here if quality is absent while readiness is present)
    # This complements Component 1 without duplicating

    # --- Wine-type structural consistency ---
    # Simple wine: should not have secondary/tertiary structure stated
    if is_simple:
        if nose_secondaries or nose_tertiaries:
            issues.append("structure_simple_wine_excess_complexity")
            guidance.append(
                "Estructura: vino declarado simple pero la respuesta incluye aromas secundarios o terciarios. "
                "Para un vino simple: intensidad → 'simple' → aromas primarios → evolucion. "
                "No se esperan secundarios ni terciarios."
            )
        p_secondaries = _str_list(palate.get("secondary_flavours"))
        p_tertiaries = _str_list(palate.get("tertiary_flavours"))
        if p_secondaries or p_tertiaries:
            issues.append("structure_simple_wine_palate_excess")
            guidance.append(
                "Boca: vino declarado simple con sabores secundarios o terciarios incluidos. "
                "Para un vino simple solo se esperan descriptores primarios."
            )

    # Complex (non-simple, non-sweet) wine: should have secondary aromas in nose
    elif wine_type not in ("sweet",):
        if not nose_secondaries and nose_primaries:
            issues.append("structure_complex_wine_missing_secondary")
            guidance.append(
                "Nariz: vino complejo sin aromas secundarios. "
                "Para un vino no simple, identifica la fuente de los aromas secundarios "
                "(roble: vainilla, cedro; FML: mantequilla, nata; lias: galleta, brioche)."
            )

    # Sweet/aged wine: high acidity is a key structural signal
    if wine_type == "sweet":
        acidity = str(palate.get("acidity") or "").lower().strip()
        if acidity and acidity not in {"alta", "media(+)"}:
            issues.append("structure_sweet_wine_acidity")
            guidance.append(
                "Boca: vino dulce con acidez que no es alta o media(+). "
                "Los vinos dulces de calidad tienen alta acidez como contrapeso al dulzor — "
                "es una de las senales estructurales clave para este tipo de vino."
            )

    status = "conformant" if not issues else "issues_found"

    return {
        "status": status,
        "ordering_issues": issues,
        "guidance": guidance,
        "formative_note": (
            "Orientacion formativa sobre estructura y orden. "
            "No asigna notas ni representa evaluacion oficial."
        ),
    }


# ---------------------------------------------------------------------------
# Component 7 -- Distinction gap report
# ---------------------------------------------------------------------------

def _build_distinction_gap_report(
    nose: dict,
    palate: dict,
) -> dict[str, Any]:
    """Identify gap between current response and distinction-level descriptor usage."""
    all_nose = (
        _str_list(nose.get("primary_aromas"))
        + _str_list(nose.get("secondary_aromas"))
        + _str_list(nose.get("tertiary_aromas"))
    )
    all_palate = (
        _str_list(palate.get("primary_flavours"))
        + _str_list(palate.get("secondary_flavours"))
        + _str_list(palate.get("tertiary_flavours"))
    )
    all_descriptors = all_nose + all_palate

    # Generic descriptors check
    generic_found = [
        d for d in all_descriptors
        if d.lower().strip() in _GENERIC_DESCRIPTORS
    ]

    # Category error check: secondary terms placed as primary
    nose_primaries = _str_list(nose.get("primary_aromas"))
    p_primaries = _str_list(palate.get("primary_flavours"))
    wrong_category: list[str] = []
    for d in nose_primaries + p_primaries:
        dn = d.lower().strip()
        if dn in _SECONDARY_DESCRIPTORS:
            wrong_category.append(f"'{d}' es secundario (roble/FML) -- no primario")
        elif dn in _TERTIARY_ONLY_DESCRIPTORS:
            wrong_category.append(f"'{d}' es terciario -- no primario")

    # Tertiary / secondary presence
    has_tertiary = bool(
        _str_list(nose.get("tertiary_aromas"))
        + _str_list(palate.get("tertiary_flavours"))
    )
    has_secondary = bool(
        _str_list(nose.get("secondary_aromas"))
        + _str_list(palate.get("secondary_flavours"))
    )

    # Specificity check
    primary_count = len(
        _str_list(nose.get("primary_aromas")) + _str_list(palate.get("primary_flavours"))
    )

    guidance: list[str] = []
    if generic_found:
        guidance.append(
            f"Descriptores genericos detectados: {generic_found}. "
            "Reemplaza por terminos especificos (p.ej. 'cereza roja' en vez de 'frutal')."
        )
    if wrong_category:
        guidance.append(
            "Errores de categoria: " + " | ".join(wrong_category) + ". "
            "Clasifica correctamente en primario/secundario/terciario."
        )
    if not has_secondary and not bool(nose.get("is_simple")):
        guidance.append(
            "No se detectaron descriptores secundarios (roble, FML, lias). "
            "Para nivel distincion, identifica la fuente de los aromas secundarios."
        )
    if not has_tertiary and not bool(nose.get("is_simple")):
        guidance.append(
            "No se detectaron descriptores terciarios (crianza en botella: miel, cuero, tabaco...). "
            "Omitirlos es la causa #1 de perdida de puntos para candidatos a distincion."
        )
    if 0 < primary_count < 3 and not bool(nose.get("is_simple")):
        guidance.append(
            f"Solo {primary_count} descriptor(es) primario(s) en total. "
            "Para nivel distincion se recomiendan 3-5 descriptores primarios especificos."
        )

    level = (
        "distinction_ready"
        if (has_secondary and has_tertiary and not generic_found and not wrong_category)
        else "approaching_distinction"
        if (has_secondary or has_tertiary)
        else "pass_level"
    )

    return {
        "level_indicator": level,
        "generic_descriptors_found": generic_found,
        "category_errors": wrong_category,
        "tertiary_present": has_tertiary,
        "secondary_present": has_secondary,
        "primary_descriptor_count": primary_count,
        "guidance": guidance,
        "formative_note": (
            "Este informe es orientacion formativa. "
            "La evaluacion oficial requiere un examinador WSET acreditado."
        ),
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]
