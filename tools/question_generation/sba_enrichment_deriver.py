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
BATCH_SIZE = 578              # bank-size output cap; precision decides coverage
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
    "CC_MECHANICAL_HARVEST_OXIDATION": {
        "subject": "la vendimia mecánica y el riesgo de oxidación",
        "causa": "La vendimia mecánica puede romper bayas antes de que la fruta llegue a la bodega.",
        "mecanismo": "El mosto liberado queda expuesto al oxígeno durante el transporte y la espera, iniciando reacciones oxidativas si no se procesa y protege con rapidez.",
        "efecto": "Puede aumentar la oxidación y reducir la frescura aromática frente a fruta intacta y cuidadosamente manipulada.",
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
    "HC_CELLAR_HYGIENE_MICROBIAL_CONTROL": {
        "subject": "la higiene de bodega y el control microbiano",
        "causa": "Los residuos de vino y los equipos sucios pueden albergar levaduras y bacterias alterantes.",
        "mecanismo": "La limpieza y desinfección estrictas eliminan reservorios microbianos y reducen la transferencia entre vinos y recipientes.",
        "efecto": "Disminuye la probabilidad de contaminación microbiana, aromas defectuosos e inestabilidad.",
    },
    "HC_COLD_TARTRATE_STABILIZATION": {
        "subject": "la estabilización tartárica por frío",
        "causa": "El vino contiene potasio y ácido tartárico disueltos que podrían formar cristales de bitartrato potásico.",
        "mecanismo": "El enfriamiento controlado reduce la solubilidad de los tartratos y provoca que cristalicen en bodega, donde pueden retirarse.",
        "efecto": "Es menos probable que aparezcan después del embotellado cristales inocuos pero visualmente indeseados.",
    },
    "HC_CONCRETE_THERMAL_INERTIA": {
        "subject": "la inercia térmica de los fermentadores de hormigón",
        "causa": "Los recipientes de hormigón tienen paredes gruesas y una masa térmica elevada.",
        "mecanismo": "Esa masa absorbe y libera calor lentamente, amortiguando cambios rápidos de temperatura durante la fermentación.",
        "efecto": "La temperatura puede mantenerse más estable de forma natural, aunque todavía puede requerirse refrigeración activa.",
    },
    "HC_COOL_FERMENTATION_AROMA_RETENTION": {
        "subject": "la fermentación a baja temperatura y la retención aromática",
        "causa": "Un mosto blanco o aromático fermenta a una temperatura relativamente baja y controlada.",
        "mecanismo": "La temperatura baja ralentiza la actividad de la levadura y reduce la volatilización y transformación rápida de compuestos aromáticos delicados.",
        "efecto": "El vino terminado conserva más aromas frescos y delicados de fruta y flores.",
    },
    "HC_PREBOTTLING_FILTRATION_CLARITY": {
        "subject": "la filtración previa al embotellado",
        "causa": "Antes de embotellar, el vino puede contener partículas, sedimento, levaduras o bacterias en suspensión.",
        "mecanismo": "La filtración hace pasar el vino por un medio que retiene partículas y, con poros suficientemente finos, microorganismos.",
        "efecto": "El vino embotellado queda más limpio y puede ganar estabilidad física y microbiológica.",
    },
    "HC_RED_FERMENTATION_EXTRACTION": {
        "subject": "la extracción durante la fermentación de tintos",
        "causa": "El mosto tinto fermenta con los hollejos mientras se gestiona el sombrero y la temperatura es suficientemente cálida.",
        "mecanismo": "El remontado renueva el contacto entre líquido y hollejos; el calor y el alcohol creciente favorecen la extracción de compuestos fenólicos.",
        "efecto": "Pasan al vino más color y tanino, aumentando su profundidad y estructura.",
    },
    "HC_MICROOXYGENATION_TANNIN_SOFTENING": {
        "subject": "la microoxigenación y la integración de los taninos",
        "causa": "Un vino tinto recibe dosis pequeñas y controladas de oxígeno durante su maduración.",
        "mecanismo": "El oxígeno controlado favorece reacciones entre taninos, pigmentos y otros compuestos fenólicos, promoviendo su polimerización e integración.",
        "efecto": "Los taninos pueden percibirse menos agresivos y más integrados, aunque el vino conserva estructura fenólica.",
    },
    "HC_STERILE_FILTRATION_MICROBIAL_STABILITY": {
        "subject": "la filtración estéril y la estabilidad microbiológica",
        "causa": "Antes del embotellado pueden quedar levaduras o bacterias alterantes viables en el vino.",
        "mecanismo": "Una membrana de grado estéril elimina físicamente los microorganismos justo antes de llenar botellas limpias.",
        "efecto": "Disminuye el riesgo de Brettanomyces, refermentación, turbidez, gas y aromas microbianos defectuosos en botella.",
    },
    "HC_CANOPY_AIRFLOW_FUNGAL_RISK": {
        "subject": "la ventilación del dosel y el riesgo de enfermedades fúngicas",
        "causa": "Un follaje denso alrededor de los racimos restringe el flujo de aire y conserva humedad después de la lluvia o el rocío.",
        "mecanismo": "Abrir el dosel mediante posicionamiento de brotes o deshoje mejora la ventilación y acelera el secado de los racimos.",
        "efecto": "Las condiciones son menos favorables para Botrytis y otros hongos; un dosel excesivamente denso aumenta la presión de enfermedad.",
    },
    "HC_CANOPY_SHADE_HEAT_PROTECTION": {
        "subject": "la sombra del dosel como protección frente al calor",
        "causa": "En un clima muy caluroso, los racimos corren riesgo de exposición solar excesiva, quemaduras y pérdida rápida de acidez.",
        "mecanismo": "Conservar suficiente follaje aporta sombra y reduce la temperatura de los racimos durante las horas más cálidas.",
        "efecto": "La fruta queda mejor protegida del daño térmico y puede conservar más frescura, aunque una sombra excesiva dificultaría la maduración.",
    },
    "HC_COVER_CROPS_EROSION_CONTROL": {
        "subject": "las cubiertas vegetales y el control de la erosión",
        "causa": "El suelo desnudo del viñedo queda expuesto al impacto y la escorrentía de la lluvia y a la acción del viento.",
        "mecanismo": "Las raíces de la cubierta fijan partículas del suelo y la vegetación superficial frena el agua y amortigua la lluvia.",
        "efecto": "Se pierde menos suelo por escorrentía o viento, reduciendo la erosión y ayudando a conservar la estructura del terreno.",
    },
    "HC_DRIP_IRRIGATION_PRECISION": {
        "subject": "la precisión del riego por goteo",
        "causa": "Las vides de una región seca necesitan agua suplementaria aplicada con eficiencia.",
        "mecanismo": "Las líneas de goteo liberan cantidades medidas de agua lenta y directamente en la zona radicular de cada vid.",
        "efecto": "El aporte de agua puede controlarse con precisión y con menos evaporación y escorrentía que una aplicación superficial amplia.",
    },
    "HC_EARLY_GROWTH_FROST_EXPOSURE": {
        "subject": "el crecimiento temprano y la exposición a heladas primaverales",
        "causa": "Una primavera inusualmente cálida o una poda temprana adelantan la brotación y otras fases vulnerables.",
        "mecanismo": "Los tejidos verdes tiernos aparecen cuando todavía pueden producirse noches bajo cero más adelante en primavera.",
        "efecto": "Aumenta el periodo de exposición a heladas y el riesgo de daño en brotes, flores y rendimiento.",
    },
    "HC_EXCESS_NITROGEN_DISEASE_RISK": {
        "subject": "el exceso de nitrógeno y el riesgo de enfermedad",
        "causa": "Un exceso de fertilización nitrogenada estimula un crecimiento vigoroso de brotes y hojas.",
        "mecanismo": "El dosel denso resultante sombrea los racimos, restringe el aire y retiene humedad alrededor de la fruta.",
        "efecto": "La maduración puede retrasarse y el dosel húmedo se vuelve más susceptible a enfermedades fúngicas.",
    },
    "HC_FLOWERING_RAIN_FRUIT_SET": {
        "subject": "la lluvia durante la floración y el cuajado",
        "causa": "La lluvia y un tiempo fresco e inestable coinciden con la floración de la vid.",
        "mecanismo": "La humedad interfiere con la polinización y la fecundación y puede hacer que las flores fallen o se desprendan.",
        "efecto": "El cuajado es pobre, se forman menos bayas y disminuye el rendimiento potencial.",
    },
    "HC_FROST_SHOOT_YIELD_DAMAGE": {
        "subject": "el daño de las heladas primaverales sobre brotes y rendimiento",
        "causa": "La temperatura cae bajo cero después de que hayan aparecido yemas y brotes tiernos.",
        "mecanismo": "La formación de hielo daña las células vivas de brotes, hojas e inflorescencias jóvenes.",
        "efecto": "Se pierde crecimiento primario y posibles racimos florales, reduciendo de forma importante el rendimiento de la campaña.",
    },
    "HC_FROST_SLOPE_AIR_DRAINAGE": {
        "subject": "la pendiente, el drenaje de aire frío y el riesgo de helada",
        "causa": "En noches despejadas de primavera se forma aire frío que desciende por ser más denso que el aire cálido.",
        "mecanismo": "Las laderas permiten que el aire frío se aleje, mientras los valles y depresiones lo acumulan alrededor de las vides.",
        "efecto": "La pendiente y la topografía condicionan mucho la exposición: las laderas con buen drenaje de aire suelen sufrir menos que las zonas bajas.",
    },
    "HC_LATE_HARVEST_FROST_EXPOSURE": {
        "subject": "la vendimia muy tardía y la exposición a heladas",
        "causa": "Las uvas permanecen en la vid hasta muy avanzado el otoño para ganar madurez o concentración.",
        "mecanismo": "El tiempo adicional de permanencia coincide con noches más frías y una probabilidad creciente de heladas.",
        "efecto": "Una helada puede dañar o congelar la fruta antes de la cosecha, amenazando el rendimiento y el estilo previsto.",
    },
    "HC_PHYLLOXERA_RESISTANT_ROOTSTOCK": {
        "subject": "el control de la filoxera mediante portainjertos resistentes",
        "causa": "La filoxera ataca y daña las raíces de las vides Vitis vinifera susceptibles.",
        "mecanismo": "La variedad vinífera deseada se injerta sobre un portainjerto de vid americana resistente que tolera o limita el daño radicular del insecto.",
        "efecto": "La parte aérea produce la uva prevista mientras las raíces resistentes aportan la principal defensa duradera frente a la filoxera.",
    },
    "HC_ANCESTRAL_SINGLE_FERMENTATION": {
        "subject": "el método ancestral y su fermentación única",
        "causa": "Un vino parcialmente fermentado se embotella antes de que termine su primera fermentación alcohólica.",
        "mecanismo": "La fermentación continúa dentro de la botella cerrada y el CO₂ producido por la levadura se disuelve en el vino en vez de escapar.",
        "efecto": "Las burbujas proceden de una sola fermentación continua; los ejemplos tradicionales pueden conservar sedimento porque el removido y el degüelle no son obligatorios.",
    },
    "HC_BASE_WINE_OXIDATION_DAMAGE": {
        "subject": "la oxidación del vino base para espumosos",
        "causa": "Un vino base delicado y de alta acidez queda expuesto a demasiado oxígeno antes de completar la elaboración del espumoso.",
        "mecanismo": "El oxígeno consume compuestos protectores y acelera la pérdida y transformación de los aromas primarios frescos.",
        "efecto": "El espumoso terminado puede mostrar menos frescura, aromas magullados o apagados y una calidad global inferior.",
    },
    "HC_BRUT_NATURE_NO_DOSAGE": {
        "subject": "la ausencia de dosificación en un Brut Nature",
        "causa": "Tras el degüelle, el productor decide no añadir azúcar mediante el licor de expedición.",
        "mecanismo": "Sin dosificación no aumenta el dulzor final; solo contribuye el azúcar residual que haya quedado de forma natural.",
        "efecto": "El vino puede etiquetarse Brut Nature o Zero Dosage si cumple el límite correspondiente, normalmente entre 0 y 3 g/L de azúcar residual.",
    },
    "HC_DISGORGEMENT_SEDIMENT_REMOVAL": {
        "subject": "el degüelle y la eliminación del sedimento",
        "causa": "Después del removido, el sedimento de levaduras queda concentrado en el cuello de la botella invertida.",
        "mecanismo": "Se congela el cuello y se retira el tapón corona; la presión interna expulsa el tapón helado que contiene las lías.",
        "efecto": "El sedimento se elimina rápidamente, conservando la mayor parte del CO₂ disuelto y limitando la oxidación.",
    },
    "HC_LIQUEUR_TIRAGE_SECOND_FERMENTATION": {
        "subject": "el licor de tiraje y la segunda fermentación",
        "causa": "Se añade a la mezcla de vinos base una cantidad medida de vino, azúcar, levadura, nutrientes y un agente clarificante.",
        "mecanismo": "La levadura añadida fermenta el azúcar dentro de la botella cerrada, produciendo alcohol y dióxido de carbono.",
        "efecto": "La segunda fermentación eleva ligeramente el alcohol y atrapa el CO₂ disuelto, creando presión y burbujas.",
    },
    "HC_PRESSURE_MOUSSE_INTENSITY": {
        "subject": "la presión y la intensidad de la espuma de un espumoso",
        "causa": "Un vino espumoso contiene menos CO₂ disuelto y desarrolla una presión inferior a unas tres atmósferas.",
        "mecanismo": "La menor presión ejerce menos fuerza para que el CO₂ abandone la solución al abrir y servir el vino.",
        "efecto": "La efervescencia se percibe más delicada y la espuma es más suave que en un vino de cinco a seis atmósferas, como suele ser Champagne.",
    },
    "HC_RIDDLING_SEDIMENT_COLLECTION": {
        "subject": "el removido y la acumulación del sedimento en el cuello",
        "causa": "Tras la segunda fermentación y la crianza, el sedimento de lías queda distribuido por el lateral de la botella.",
        "mecanismo": "El removido gira e inclina gradualmente la botella desde la posición horizontal hasta una posición vertical invertida.",
        "efecto": "El sedimento se desliza hasta el cuello, donde puede eliminarse de forma eficaz durante el degüelle.",
    },
    "HC_TANK_METHOD_FRUIT_RETENTION": {
        "subject": "el método de tanque y la conservación de la fruta primaria",
        "causa": "La segunda fermentación se realiza en un tanque cerrado resistente a la presión en lugar de cada botella final.",
        "mecanismo": "El acero inoxidable con temperatura controlada y un contacto relativamente corto con las lías limitan la oxidación y el desarrollo autolítico mientras retienen el CO₂ bajo presión.",
        "efecto": "El espumoso conserva aromas primarios frescos, frutales y florales y puede producirse con mayor rapidez y menor coste.",
    },
    "HC_TRADITIONAL_BOTTLE_SECOND_FERMENTATION": {
        "subject": "la segunda fermentación en botella del método tradicional",
        "causa": "Se añade licor de tiraje a la mezcla de vinos base y el vino se cierra en la botella en la que después se venderá.",
        "mecanismo": "La levadura realiza una segunda fermentación alcohólica en esa botella cerrada, por lo que el CO₂ producido se disuelve en el vino.",
        "efecto": "La presión y las burbujas se crean en la botella final, que después permite crianza sobre lías, removido y degüelle.",
    },
    "HC_BAROLO_TERTIARY_EVOLUTION": {
        "subject": "la evolución en botella del Barolo",
        "causa": "El Barolo de Nebbiolo parte de taninos altos y acidez alta, que aportan una estructura considerable para la guarda.",
        "mecanismo": "Durante la crianza en botella los taninos se polimerizan y suavizan, mientras los aromas primarios evolucionan gradualmente hacia compuestos terciarios.",
        "efecto": "El Barolo maduro conserva acidez y estructura y desarrolla notas terciarias como flores secas, cuero, tierra y alquitrán.",
    },
    "HC_BOTTLE_STORAGE_STABILITY": {
        "subject": "las condiciones estables para la guarda en botella",
        "causa": "Un vino embotellado se almacena durante un periodo prolongado antes de su servicio.",
        "mecanismo": "Un entorno fresco, oscuro, sin vibraciones y con temperatura estable ralentiza los cambios químicos; si el cierre es de corcho natural, la posición horizontal mantiene el vino en contacto con él.",
        "efecto": "Disminuye el riesgo de oxidación prematura y daño por calor, permitiendo que la evolución en botella avance de forma más lenta y uniforme.",
    },
    "HC_BOTTLE_TANNIN_SOFTENING": {
        "subject": "la suavización de taninos durante la crianza en botella",
        "causa": "Un vino tinto estructurado contiene abundantes taninos cuando se embotella.",
        "mecanismo": "Con el tiempo, las moléculas de tanino y pigmento se polimerizan en estructuras mayores y algunas terminan precipitando como sedimento.",
        "efecto": "Disminuye la proporción de taninos libres muy astringentes y la textura del vino se vuelve más suave e integrada.",
    },
    "HC_HEAT_PREMATURE_BOTTLE_AGEING": {
        "subject": "el efecto del calor excesivo sobre el vino embotellado",
        "causa": "El vino embotellado queda expuesto a temperaturas excesivas durante un periodo prolongado.",
        "mecanismo": "El calor acelera la oxidación y otras reacciones químicas y también puede aumentar la expansión y la presión dentro de la botella.",
        "efecto": "El vino evoluciona prematuramente, pierde fruta fresca y puede desarrollar sabores cocidos u oxidados.",
    },
    "HC_MAGNUM_SLOW_AGEING": {
        "subject": "el envejecimiento más lento en formato magnum",
        "causa": "Una magnum contiene el doble de vino que una botella estándar, pero utiliza un cierre y un espacio de cabeza de escala parecida.",
        "mecanismo": "Cada unidad de vino queda expuesta a una proporción menor del oxígeno presente en el espacio de cabeza o transmitido a través del cierre.",
        "efecto": "La evolución oxidativa suele ser más lenta, permitiendo que los vinos aptos para guarda evolucionen gradualmente y conserven frescura durante más tiempo.",
    },
    "HC_OLD_RED_SEDIMENT_SERVICE": {
        "subject": "el sedimento de los tintos añejos y su servicio cuidadoso",
        "causa": "Durante una larga crianza en botella, los taninos y pigmentos polimerizados pueden precipitar como sedimento en un tinto estructurado.",
        "mecanismo": "Colocar la botella en reposo y verter o decantar lentamente permite retener el depósito en la botella en lugar de dispersarlo por el vino.",
        "efecto": "El vino limpio se separa del sedimento granuloso y puede servirse sin remover el depósito.",
    },
    "HC_RED_WINE_AGEABILITY_STRUCTURE": {
        "subject": "la estructura que permite la guarda prolongada de un vino tinto",
        "causa": "Un tinto concentrado parte de taninos, acidez y fruta abundantes y, en estilos fortificados, también de alcohol y azúcar.",
        "mecanismo": "La acidez y otros componentes estables ralentizan el deterioro, mientras los taninos se polimerizan y el perfil concentrado evoluciona con el tiempo.",
        "efecto": "El vino tiene capacidad estructural para una guarda prolongada, durante la cual los taninos pueden integrarse y surgir complejidad terciaria; esa estructura permite la evolución, pero no garantiza mejora si el almacenamiento es deficiente.",
    },
    "HC_BARREL_LEES_WHITE_BODY": {
        "subject": "el uso combinado de barrica y contacto con lías en vinos blancos",
        "causa": "Un vino blanco fermenta o envejece en barrica mientras permanece en contacto con sus lías finas.",
        "mecanismo": "La madera aporta compuestos aromáticos y una entrada gradual de oxígeno; a la vez, la autólisis de las lías libera manoproteínas y polisacáridos que aumentan el peso y la textura en boca.",
        "efecto": "La combinación produce un vino blanco con más cuerpo, redondez y complejidad tanto textural como aromática.",
    },
    "HC_BATONNAGE_TEXTURE_COMPLEXITY": {
        "subject": "el bâtonnage y el contacto con las lías finas",
        "causa": "Tras la fermentación, las lías finas se depositan y pueden mantenerse en contacto con un vino blanco.",
        "mecanismo": "El bâtonnage remueve y resuspende las lías, aumentando el contacto del vino con manoproteínas, polisacáridos y compuestos de sabor procedentes de las levaduras.",
        "efecto": "El vino puede ganar textura cremosa, mayor peso en boca y más complejidad aromática.",
    },
    "HC_SPARKLING_AUTOLYTIC_AROMAS": {
        "subject": "la autólisis durante la crianza sobre lías de un espumoso",
        "causa": "Un vino espumoso de método tradicional permanece durante un periodo prolongado sobre las lías de la segunda fermentación.",
        "mecanismo": "Las células de levadura muertas sufren autólisis y liberan aminoácidos, péptidos, manoproteínas y otros compuestos que evolucionan con el tiempo.",
        "efecto": "El vino desarrolla complejidad autolítica con aromas de pan, galleta, tostado, brioche y pastelería.",
    },
    "HC_SPARKLING_LEES_TEXTURE": {
        "subject": "la crianza prolongada sobre lías en vinos espumosos",
        "causa": "Un espumoso de método tradicional pasa un periodo prolongado en contacto con las lías de la segunda fermentación.",
        "mecanismo": "La autólisis libera manoproteínas y polisacáridos que aumentan el peso en boca y ayudan a estabilizar las burbujas de CO₂; otros compuestos de levadura aportan aroma.",
        "efecto": "El espumoso gana textura cremosa, una espuma más fina y persistente y mayor complejidad con notas derivadas de la levadura.",
    },
    "HC_WHITE_LEES_TEXTURE_COMPLEXITY": {
        "subject": "la crianza sobre lías de vinos blancos",
        "causa": "Un vino blanco permanece en contacto con sus lías finas después de la fermentación.",
        "mecanismo": "Al descomponerse las células de levadura, la autólisis libera manoproteínas, polisacáridos y compuestos activos de sabor al vino.",
        "efecto": "El vino desarrolla mayor cuerpo, textura más cremosa y complejidad aromática y de sabor adicional.",
    },
    "HC_MLF_ACID_CONVERSION": {
        "subject": "la conversión de ácido málico en ácido láctico durante la FML",
        "causa": "Tras la fermentación alcohólica, las bacterias lácticas pueden realizar la fermentación maloláctica.",
        "mecanismo": "Las bacterias convierten el ácido málico, más punzante y con dos protones ácidos, en ácido láctico, más suave y con uno; liberan CO₂, pero no transforman el ácido tartárico.",
        "efecto": "La acidez titulable disminuye y el pH sube ligeramente, por lo que el vino resulta más suave y redondo sin perder la fracción de acidez tartárica.",
    },
    "HC_MLF_BLOCKING_FRESHNESS": {
        "subject": "el bloqueo de la fermentación maloláctica para conservar frescura",
        "causa": "El elaborador busca mantener la acidez punzante y la fruta primaria de un vino blanco fresco.",
        "mecanismo": "Al bloquear la fermentación maloláctica se evita que las bacterias conviertan el ácido málico, más punzante, en ácido láctico, más suave.",
        "efecto": "El vino conserva más acidez málica y frescura, con un perfil más crujiente y lineal y sin el carácter cremoso que puede acompañar a la FML.",
    },
    "HC_MLF_MICROBIAL_STABILITY": {
        "subject": "la fermentación maloláctica controlada y la estabilidad microbiológica",
        "causa": "Un vino que aún contiene ácido málico puede iniciar una fermentación maloláctica no deseada si quedan bacterias lácticas viables.",
        "mecanismo": "Completar la FML de forma controlada en bodega consume el ácido málico disponible antes de la estabilización y el embotellado.",
        "efecto": "Se reduce el riesgo de una FML posterior en botella y de sus posibles consecuencias: turbidez, gas o cambios aromáticos no deseados.",
    },
    "HC_MLF_STYLE_CONTROL": {
        "subject": "la decisión de inducir o bloquear la fermentación maloláctica",
        "causa": "El elaborador decide si el estilo buscado necesita acidez más suave y mayor redondez o, por el contrario, acidez más punzante y fruta primaria más fresca.",
        "mecanismo": "La FML puede inducirse mediante inoculación y una temperatura adecuada, o bloquearse mediante higiene, SO₂, frío, filtración y estabilización oportuna.",
        "efecto": "Inducir o bloquear la FML es una decisión deliberada de estilo y estabilidad, no una etapa automática en todos los vinos.",
    },
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
    "HC_BOTRYTIS_CONCENTRATION": {
        "subject": "la podredumbre noble y la concentración de la uva",
        "causa": "La Botrytis cinerea beneficiosa infecta uvas maduras cuando periodos húmedos o con niebla van seguidos de condiciones cálidas y secas.",
        "mecanismo": "El hongo perfora la piel de la baya y permite que el agua se evapore durante los periodos secos. Esta pérdida de agua concentra directamente los azúcares y los compuestos de sabor; al mismo tiempo, la Botrytis metaboliza parte de los ácidos de la uva.",
        "efecto": "La fruta adquiere mayor concentración de azúcar y sabor, una textura rica y aromas característicos de podredumbre noble. La acidez neta depende del equilibrio entre concentración y metabolismo de ácidos, por lo que no debe interpretarse como una regla simple de aumento de acidez.",
    },
    "HC_NOBLE_ROT_DEVELOPMENT_CONDITIONS": {
        "subject": "las condiciones climáticas para el desarrollo de la podredumbre noble",
        "causa": "La podredumbre noble se desarrolla cuando las uvas maduras reciben mañanas húmedas o con niebla seguidas de tardes más cálidas y secas.",
        "mecanismo": "La humedad o niebla matinal permite que Botrytis cinerea se establezca en las bayas; después, las tardes secas limitan la podredumbre gris destructiva y favorecen una evaporación controlada a través de las pieles perforadas. La humedad por sí sola no es suficiente.",
        "efecto": "La secuencia de mañanas húmedas o con niebla seguidas de tardes secas favorece la podredumbre noble beneficiosa y produce uvas pasificadas con azúcar, sabor y aromas botritizados concentrados.",
    },
    "HC_NIGHT_HARVEST_FRESHNESS": {
        "subject": "la vendimia nocturna en climas cálidos",
        "causa": "En un clima cálido, las uvas se vendimian durante la noche, cuando están más frías que después del calentamiento diurno.",
        "mecanismo": "La fruta más fría llega a bodega con menor riesgo de oxidación y pérdida de compuestos volátiles por el calor y necesita menos refrigeración inmediata antes del procesado.",
        "efecto": "Se conservan mejor los aromas frescos y la acidez que ya contiene la uva; la vendimia nocturna no crea ni aumenta por sí misma la acidez.",
    },
    "HC_EARLY_HARVEST_FRESHNESS_ALCOHOL": {
        "subject": "la vendimia anticipada y el equilibrio entre frescura y alcohol",
        "causa": "Las uvas se recogen antes de alcanzar una fase más avanzada de maduración.",
        "mecanismo": "Han acumulado menos azúcar y conservan más acidez natural que si permanecieran más tiempo en la vid.",
        "efecto": "El vino suele mostrar mayor frescura y menor alcohol potencial, siempre que la madurez aromática y fenólica sea suficiente.",
    },
    "HC_SELECTIVE_HAND_HARVEST_QUALITY": {
        "subject": "la vendimia manual selectiva",
        "causa": "Los vendimiadores inspeccionan y seleccionan los racimos individualmente durante la cosecha.",
        "mecanismo": "Los racimos dañados, enfermos, inmaduros o inadecuados pueden rechazarse antes de entrar en bodega.",
        "efecto": "La bodega recibe una selección de fruta más sana y uniforme, favoreciendo sabores limpios y el nivel de calidad buscado.",
    },
    "HC_SOUTH_FACING_EXPOSURE_RIPENESS": {
        "subject": "la exposición sur en el hemisferio norte",
        "causa": "En el hemisferio norte, una ladera orientada al sur recibe más radiación solar directa.",
        "mecanismo": "La mayor exposición solar calienta el sitio y favorece la fotosíntesis y la acumulación de azúcar durante la maduración.",
        "efecto": "La uva puede alcanzar mayor madurez y alcohol potencial que en una orientación más fresca y menos expuesta, siempre que el calor y el agua no sean limitantes.",
    },
    "HC_NEW_OAK_STRUCTURE_SPICE": {
        "subject": "las barricas nuevas y su aporte de estructura y especias",
        "causa": "El vino madura en barricas nuevas cuyos compuestos de la madera todavía no se han agotado por usos anteriores.",
        "mecanismo": "El vino extrae taninos y compuestos aromáticos del roble, como especias, tostado y vainilla, mientras la entrada lenta de oxígeno favorece la integración de la estructura.",
        "efecto": "El roble nuevo puede aportar especias, complejidad y estructura cuando su influencia está proporcionada e integrada con la fruta.",
    },
    "HC_BARREL_SIZE_OAK_CONTACT": {
        "subject": "el tamaño de la barrica y la proporción de contacto con el roble",
        "causa": "El mismo volumen de vino se distribuye en recipientes de roble pequeños en vez de grandes.",
        "mecanismo": "Una barrica pequeña ofrece más superficie de madera respecto al volumen de vino, aumentando el contacto con el roble y la transferencia de oxígeno por litro.",
        "efecto": "La influencia aromática y estructural del roble suele ser más marcada y desarrollarse más rápido que en un recipiente grande.",
    },
    "HC_FREQUENT_RACKING_OXYGEN": {
        "subject": "el trasiego frecuente durante la crianza",
        "causa": "El vino se transfiere repetidamente de un recipiente a otro durante su crianza.",
        "mecanismo": "Cada transferencia puede incorporar una cantidad controlada de aire al vino, además de separarlo del sedimento depositado.",
        "efecto": "Un trasiego más frecuente aumenta la exposición acumulada al oxígeno y puede acelerar la evolución oxidativa si no se controla cuidadosamente.",
    },
    "HC_OXIDATIVE_AGEING_TERTIARY": {
        "subject": "el envejecimiento oxidativo y el desarrollo de aromas terciarios",
        "causa": "El vino madura deliberadamente con un acceso controlado al oxígeno.",
        "mecanismo": "Las reacciones impulsadas por el oxígeno transforman los compuestos de fruta primaria y favorecen la aparición de aromas y sabores de evolución.",
        "efecto": "La fruta fresca pierde protagonismo y pueden desarrollarse notas terciarias de frutos secos, fruta desecada, caramelo o matices sabrosos, según el estilo.",
    },
    "HC_USED_OAK_OXYGEN_LOW_FLAVOUR": {
        "subject": "las barricas usadas y la oxigenación con poco sabor de roble",
        "causa": "El vino madura en barricas que ya han contenido vino durante uno o varios ciclos.",
        "mecanismo": "Los usos anteriores han agotado gran parte de los compuestos de sabor fácilmente extraíbles, pero la madera todavía permite una transferencia lenta de oxígeno.",
        "efecto": "El vino recibe efectos de textura y evolución por oxigenación controlada con mucho menos aroma o sabor de roble nuevo.",
    },
    "HC_ALTITUDE_SLOW_RIPENING_FRESHNESS": {
        "subject": "la altitud elevada, la maduración lenta y la frescura",
        "causa": "El viñedo se encuentra a gran altitud, donde las temperaturas ambientales, sobre todo nocturnas, son más bajas.",
        "mecanismo": "Las condiciones más frescas ralentizan la maduración y reducen la pérdida respiratoria de ácidos de la uva, a la vez que prolongan el desarrollo aromático.",
        "efecto": "La fruta de altura puede conservar más acidez y frescura aromática y madurar más lentamente que fruta comparable de menor altitud.",
    },
    "HC_DESTEMMING_GREEN_TANNIN_REDUCTION": {
        "subject": "el despalillado previo a la fermentación",
        "causa": "Los raspones se separan de los racimos antes de la fermentación alcohólica.",
        "mecanismo": "Al retirar los raspones se evita que sus compuestos fenólicos se extraigan hacia el mosto en fermentación.",
        "efecto": "El vino tiene menos probabilidad de adquirir taninos verdes y ásperos de los raspones, aunque todavía puede extraer tanino de hollejos y pepitas.",
    },
    "HC_HUMID_HARVEST_DILUTION": {
        "subject": "la lluvia o humedad persistente cerca de la vendimia",
        "causa": "Se producen lluvias importantes o condiciones persistentemente húmedas poco antes o durante la cosecha.",
        "mecanismo": "Las bayas pueden absorber agua y aumentar de tamaño, elevando el volumen de jugo respecto a los azúcares, ácidos y compuestos de sabor disueltos.",
        "efecto": "Los componentes de la uva pueden diluirse, reduciendo la concentración de azúcar y acidez y debilitando la intensidad de sabor; también aumenta la presión de enfermedades.",
    },
    "HC_MODERATE_WATER_STRESS_PHENOLICS": {
        "subject": "el estrés hídrico moderado y la concentración fenólica",
        "causa": "La vid sufre un déficit de agua moderado, no severo, durante el desarrollo y la maduración de las bayas.",
        "mecanismo": "Se limita el crecimiento de los brotes y las bayas permanecen más pequeñas, aumentando la proporción de hollejo rico en fenoles respecto al jugo.",
        "efecto": "Puede aumentar la concentración fenólica, incluido el potencial de color y tanino; un estrés severo, en cambio, detendría la fotosíntesis y la maduración.",
    },
    "HC_SANDY_SOIL_DRAINAGE": {
        "subject": "la estructura arenosa del suelo y el drenaje",
        "causa": "El suelo del viñedo contiene una proporción elevada de partículas de arena relativamente grandes.",
        "mecanismo": "Los poros mayores entre partículas permiten que el agua atraviese el suelo con más rapidez que en una estructura arcillosa fina y compacta.",
        "efecto": "La estructura arenosa favorece el drenaje libre y reduce la retención de agua, condicionando la disponibilidad hídrica de las raíces y el vigor.",
    },
    "HC_UMAMI_BITTER_ACID_PERCEPTION": {
        "subject": "el efecto del umami sobre la percepción del vino",
        "causa": "El vino se prueba con un alimento rico en umami.",
        "mecanismo": "El contraste sensorial puede reducir la fruta y suavidad percibidas del vino y hacer más evidentes sus elementos estructurales.",
        "efecto": "El vino puede parecer más amargo, ácido, secante o alcohólico que cuando se prueba sin ese alimento.",
    },
    "HC_PROTEIN_FAT_TANNIN_SOFTENING": {
        "subject": "los alimentos proteicos o grasos con un vino tánico",
        "causa": "Un vino de taninos marcados se sirve con un alimento que contiene proteínas o grasa.",
        "mecanismo": "Los taninos interactúan con las proteínas del alimento y disminuye su contacto directo con las proteínas salivales; la grasa también modifica el contraste táctil.",
        "efecto": "La astringencia puede sentirse menos agresiva y el conjunto resultar más equilibrado.",
    },
    "HC_ALCOHOL_CHILI_HEAT": {
        "subject": "el alcohol del vino y el picante de la comida",
        "causa": "Un vino con alcohol perceptible se consume con un alimento que contiene picante.",
        "mecanismo": "El alcohol aporta su propia sensación cálida y puede intensificar la irritación producida por la capsaicina en vez de neutralizarla.",
        "efecto": "La comida puede parecer más picante y el alcohol del vino más ardiente, haciendo el maridaje menos cómodo.",
    },
    "HC_ALCOHOL_BITTERNESS_PERCEPTION": {
        "subject": "el alcohol y la percepción de amargor",
        "causa": "Un vino contiene alcohol perceptible junto con compuestos de sabor amargo.",
        "mecanismo": "El etanol aporta calor y puede reforzar el impacto sensorial del amargor en vez de ocultarlo.",
        "efecto": "El amargor puede percibirse más intenso, sobre todo cuando el alcohol parece elevado o desequilibrado.",
    },
    "HC_FOOD_SWEETNESS_WINE_CONTRAST": {
        "subject": "el contraste entre un alimento dulce y el vino",
        "causa": "El alimento es más dulce que el vino con el que se sirve.",
        "mecanismo": "El dulzor de la comida crea un contraste que reduce el dulzor y la fruta percibidos del vino y deja más expuestos sus componentes ácidos y amargos.",
        "efecto": "El vino puede parecer más seco, ácido, amargo y menos frutal, especialmente cuando el propio vino es seco.",
    },
    "HC_SALT_TANNIN_BALANCE": {
        "subject": "la sal de la comida y la percepción de los taninos",
        "causa": "El vino se prueba con un alimento que contiene sal.",
        "mecanismo": "La sal puede reducir el amargor y el efecto secante percibidos y desplazar la atención hacia la fruta y el cuerpo del vino.",
        "efecto": "Los taninos pueden sentirse más suaves y la combinación entre vino y comida parecer más equilibrada.",
    },
    "HC_LOW_SERVICE_TEMPERATURE_TANNIN_AROMA": {
        "subject": "una temperatura de servicio demasiado baja en un tinto estructurado",
        "causa": "Un vino tinto estructurado se sirve a una temperatura excesivamente baja.",
        "mecanismo": "El frío reduce la volatilidad de los compuestos aromáticos y aumenta el protagonismo de las sensaciones táctiles firmes.",
        "efecto": "Los aromas se expresan menos y los taninos y la dureza parecen más marcados.",
    },
    "HC_SO2_OXIDATION_PROTECTION": {"subject": "el SO₂ como protección frente a la oxidación", "causa": "Se añade dióxido de azufre en una fase y dosis controladas de la vinificación.", "mecanismo": "El SO₂ fija productos de oxidación y limita las reacciones oxidativas, además de frenar microorganismos no deseados.", "efecto": "La fruta, el color y los aromas quedan mejor protegidos frente a la oxidación."},
    "HC_BRETTANOMYCES_ANIMAL_ODOR": {"subject": "la contaminación por Brettanomyces", "causa": "La levadura Brettanomyces crece en un vino susceptible o en equipos de bodega contaminados.", "mecanismo": "Produce fenoles volátiles capaces de dominar el perfil aromático.", "efecto": "El vino puede oler a establo, sudor de caballo, cuero, medicina u otros caracteres animales."},
    "HC_PERFUMED_DETERGENT_GLASS_CONTAMINATION": {"subject": "los residuos de detergente perfumado en las copas", "causa": "Las copas conservan residuos aromáticos de detergente o abrillantador.", "mecanismo": "El residuo aporta aromas ajenos y puede alterar la superficie de la copa y la espuma.", "efecto": "Los aromas y sabores propios del vino quedan enmascarados o distorsionados durante el servicio."},
    "HC_OPEN_BOTTLE_OXYGEN_CONTROL": {"subject": "la conservación de una botella abierta", "causa": "La botella abierta se vuelve a cerrar, se retira o desplaza parte del oxígeno y el vino se mantiene frío.", "mecanismo": "Un menor contacto con oxígeno y una temperatura baja ralentizan la oxidación y la actividad microbiana.", "efecto": "El vino restante conserva la frescura durante más tiempo que una botella abierta, cálida y expuesta al aire."},
    "HC_REDUCTION_SULFUR_ODORS": {"subject": "la reducción y los aromas azufrados", "causa": "El vino evoluciona con muy poco oxígeno o la levadura sufre estrés durante la fermentación, por ejemplo si falta nitrógeno asimilable.", "mecanismo": "La levadura estresada puede producir sulfuro de hidrógeno, y la falta de oxígeno puede permitir que persistan o se acumulen compuestos azufrados volátiles.", "efecto": "Puede oler a huevo podrido, col cocida, goma o cerilla, según el compuesto presente."},
    "HC_EXCESSIVE_WHITE_OXIDATION": {"subject": "la oxidación excesiva de un vino blanco", "causa": "El vino blanco recibe demasiado oxígeno durante la elaboración, la guarda o el servicio.", "mecanismo": "Las reacciones oxidativas consumen aromas frescos y oscurecen los pigmentos fenólicos.", "efecto": "El vino adquiere color dorado o marrón, notas de fruta magullada o frutos secos y pierde frescura."},
    "HC_TCA_MUSTY_CARDBOARD": {"subject": "la contaminación por TCA", "causa": "El vino se contamina con TCA, a menudo mediante corcho o materiales de bodega afectados.", "mecanismo": "El TCA se percibe a concentraciones muy bajas, suprime la fruta y aporta olores húmedos.", "efecto": "El vino parece apagado y huele a moho, sótano húmedo o cartón mojado."},
    "HC_VOLATILE_ACIDITY_VINEGAR_SOLVENT": {"subject": "la acidez volátil elevada", "causa": "Bacterias acéticas u otros microorganismos producen un exceso de ácidos volátiles y compuestos relacionados en un vino susceptible.", "mecanismo": "El ácido acético aporta un carácter punzante a vinagre y el acetato de etilo puede añadir aromas de disolvente o esmalte.", "efecto": "El vino puede mostrar picor desagradable, acidez avinagrada y aromas de disolvente que enmascaran la fruta."},
    "HC_UNDERRIPE_HARVEST_GREEN_AROMAS": {"subject": "la vendimia antes de la madurez aromática suficiente", "causa": "Las uvas se cosechan demasiado pronto, antes de alcanzar una madurez aromática y fenólica adecuada.", "mecanismo": "Los compuestos verdes y herbáceos siguen siendo prominentes porque la maduración no los ha reducido ni equilibrado con caracteres de fruta madura.", "efecto": "El vino puede mostrar aromas herbáceos o inmaduros, acidez más marcada y menor expresión de fruta madura."},
    "HC_MECHANIZATION_PRODUCTION_COST": {"subject": "el nivel de mecanización y los costes de producción", "causa": "El productor elige un determinado nivel de mecanización para las operaciones de viñedo o bodega.", "mecanismo": "La maquinaria sustituye parte de la mano de obra, pero introduce inversión, mantenimiento, combustible y depreciación; su efecto depende de la escala y del uso.", "efecto": "La mecanización modifica directamente la estructura de costes y puede reducir el coste unitario a escala adecuada, sin garantizarlo en toda explotación."},
    "HC_COOPERATIVE_SHARED_RESOURCES": {"subject": "la cooperativa vinícola y los recursos compartidos", "causa": "Los socios viticultores agrupan uvas, capital y organización mediante una cooperativa.", "mecanismo": "La cooperativa reparte entre muchos miembros los costes de equipos, personal técnico, elaboración, envasado y comercialización.", "efecto": "Cada viticultor puede acceder a infraestructura de vinificación y canales comerciales sin financiar por sí solo toda la inversión."},
    "HC_LOW_ACID_STRUCTURE_FLATNESS": {"subject": "la falta de acidez o estructura y la percepción de un vino plano", "causa": "El vino presenta acidez insuficiente o poca definición estructural en relación con su fruta, alcohol, dulzor y cuerpo.", "mecanismo": "La acidez aporta frescura y tensión, mientras componentes estructurales como acidez, tanino y cuerpo dan forma y progresión al paladar.", "efecto": "Si estos elementos de equilibrio son insuficientes, el vino puede parecer plano, apagado o poco definido en vez de fresco y persistente."},
    "HC_EXCLUSIVE_DISTRIBUTOR_MARKET_ACCESS": {"subject": "un distribuidor exclusivo y el acceso a un mercado extranjero", "causa": "El productor designa a un distribuidor exclusivo con capacidades establecidas en un mercado extranjero.", "mecanismo": "El distribuidor aporta conocimiento del mercado local, relaciones con clientes, logística y gestión legal o aduanera que el productor puede no tener directamente.", "efecto": "El productor puede entrar y atender ese mercado con menos infraestructura comercial duplicada, aunque la exclusividad no garantiza ventas ni una representación adecuada."},
    "HC_SCARCITY_DEMAND_PRICE_PRESSURE": {"subject": "la oferta limitada, la demanda fuerte y la presión sobre el precio", "causa": "La producción está estructuralmente limitada mientras la demanda de compradores supera ampliamente la oferta disponible.", "mecanismo": "Más compradores compiten por una cantidad pequeña de vino, aumentando la disposición a pagar y el poder de fijación de precios de productores e intermediarios.", "efecto": "La escasez combinada con demanda fuerte ejerce presión alcista sobre el precio de mercado, junto con otros factores como reputación, añada y distribución."},
    "HC_ALSACE_SUN_DRY_RIPENING": {"subject": "el sol, la escasa lluvia y la maduración de azúcares en Alsacia", "causa": "Alsacia recibe abundante insolación y lluvia relativamente escasa por el efecto de sombra pluviométrica de los Vosgos.", "mecanismo": "Cuando la vid dispone de agua suficiente, las condiciones soleadas y relativamente secas sostienen la fotosíntesis y una maduración larga y sana, y limitan la dilución causada por lluvia.", "efecto": "La uva puede alcanzar alta madurez de azúcares y concentración de sabor; un estrés hídrico severo, en cambio, frenaría la fotosíntesis y la maduración."},
    "HC_SO2_MICROBIAL_INHIBITION": {"subject": "el SO₂ y la inhibición microbiana", "causa": "El productor añade una dosis apropiada de dióxido de azufre al mosto o al vino.", "mecanismo": "La fracción antimicrobiana del SO₂ interfiere con el metabolismo microbiano; su eficacia depende especialmente del pH, la dosis, la fijación y la sensibilidad de cada organismo.", "efecto": "Se inhiben levaduras no deseadas y bacterias, ayudando a controlar la actividad microbiana sin implicar que se eliminen todos los microorganismos."},
    "HC_BENTONITE_PROTEIN_STABILITY": {"subject": "la bentonita y la estabilidad proteica", "causa": "Se mezcla arcilla bentonita con un vino que contiene proteínas inestables.", "mecanismo": "La arcilla cargada adsorbe las proteínas y sedimenta con ellas para que puedan retirarse.", "efecto": "Disminuye la probabilidad de que el vino forme una turbidez proteica después del embotellado."},
    "HC_MUST_CHILLING_FERMENTATION_CONTROL": {"subject": "el enfriamiento del mosto antes de fermentar", "causa": "El mosto fresco se enfría antes de que comience la fermentación alcohólica prevista.", "mecanismo": "La baja temperatura ralentiza levaduras y bacterias autóctonas y da tiempo para desfangar, proteger o inocular el mosto.", "efecto": "La fermentación puede iniciarse con un calendario y unas condiciones microbiológicas más controlados."},
    "HC_RACKING_OXYGEN_SEDIMENT": {"subject": "el trasiego durante la crianza", "causa": "El vino se transfiere desde un recipiente con lías o sedimento hacia otro limpio.", "mecanismo": "La transferencia separa los sólidos y puede introducir una cantidad controlada de oxígeno.", "efecto": "El vino queda más limpio y recibe una aireación limitada que puede favorecer la crianza si se gestiona con cuidado."},
    "HC_PRESSING_OXIDATION_RISK": {"subject": "el prensado y el riesgo de oxidación", "causa": "El jugo o mosto queda expuesto al aire durante un prensado y traslado mal protegidos.", "mecanismo": "El prensado crea nuevas superficies líquidas y puede liberar compuestos fenólicos oxidables mientras hay oxígeno disponible.", "efecto": "Puede acelerarse el pardeamiento y la pérdida de fruta fresca si no se controla el oxígeno."},
    "HC_HEAT_TRANSPORT_WINE_DAMAGE": {"subject": "el calor excesivo durante el transporte del vino", "causa": "El vino embotellado queda expuesto a temperaturas excesivas durante el transporte.", "mecanismo": "El calor acelera la oxidación y otras reacciones de evolución y puede expandir el vino y comprometer el cierre.", "efecto": "El vino puede desarrollar sabores cocidos, perder frescura y mostrar oxidación prematura."},
    "HC_REFERMENTATION_UNEXPECTED_BUBBLES": {"subject": "la refermentación microbiana en un vino tranquilo", "causa": "Quedan levaduras o bacterias viables y sustrato fermentable en un vino tranquilo embotellado.", "mecanismo": "Los microorganismos reanudan su actividad y producen dióxido de carbono que no puede escapar.", "efecto": "Pueden aparecer burbujas, presión, turbidez, sedimento o aromas defectuosos inesperados."},
    "HC_WARM_DRY_OVERRIPENING": {"subject": "el clima cálido y seco y el riesgo de sobremaduración", "causa": "Las uvas maduran en un clima cálido y seco con abundante calor y pocas interrupciones por lluvia.", "mecanismo": "La acumulación de azúcar y la pérdida de agua pueden avanzar rápidamente mientras disminuyen los ácidos si se retrasa la vendimia.", "efecto": "Aumenta el riesgo de sobremaduración, alcohol potencial alto, acidez baja y caracteres de fruta desecada."},
    "HC_CANOPY_VIGOUR_EXPOSURE": {"subject": "el manejo del dosel, el vigor y la exposición de los racimos", "causa": "Se gestionan brotes y hojas durante la temporada mediante poda en verde y otras operaciones de dosel.", "mecanismo": "Retirar o posicionar crecimiento limita la densidad vegetal y mejora la entrada de luz y la ventilación alrededor de los racimos.", "efecto": "Se controla el vigor y se equilibran la exposición de los racimos y sus condiciones de maduración."},
    "HC_LOW_VIGOUR_ROOTSTOCK_CONTROL": {"subject": "los portainjertos de bajo vigor", "causa": "La variedad se injerta sobre un portainjerto seleccionado por su vigor bajo o moderado.", "mecanismo": "El sistema radicular limita el crecimiento vegetativo frente a un portainjerto vigoroso, manteniendo una cosecha adecuada en condiciones apropiadas.", "efecto": "El dosel resulta más fácil de controlar sin depender de eliminar cosecha como herramienta principal."},
    "HC_CLONAL_SELECTION_STYLE_INFLUENCE": {"subject": "la selección clonal y su influencia en el estilo", "causa": "El viticultor propaga un clon de vid seleccionado por características heredables concretas.", "mecanismo": "La propagación vegetativa conserva los rasgos genéticos del clon, que pueden influir en el rendimiento, el tamaño de racimos o bayas, el momento de maduración, la susceptibilidad a enfermedades y la composición de la uva.", "efecto": "Elegir clones adecuados puede orientar la composición de la uva y, por tanto, el estilo del vino, aunque el sitio, la añada, la viticultura y la vinificación siguen siendo determinantes."},
    "HC_STEEP_SLOPE_SOLAR_RIPENING": {"subject": "las pendientes bien orientadas y la maduración en clima fresco", "causa": "Las vides crecen en una pendiente pronunciada cuya orientación recibe sol favorable en una región fresca.", "mecanismo": "El ángulo y la orientación de la ladera mejoran la intercepción de radiación directa, elevan la temperatura del dosel y de los racimos y sostienen la fotosíntesis en condiciones de maduración marginales.", "efecto": "La uva puede madurar con mayor fiabilidad y alcanzar más desarrollo de sabor y azúcar que en un sitio mal expuesto; la pendiente por sí sola no garantiza ese efecto."},
    "HC_SHORT_CYCLE_VARIETY_COOL_SEASON_FIT": {"subject": "las variedades de ciclo corto en estaciones frescas o breves", "causa": "La variedad necesita relativamente menos tiempo y acumulación térmica para avanzar desde la brotación hasta la madurez fisiológica y aromática.", "mecanismo": "Su ciclo fenológico más corto permite completar la maduración dentro de una estación breve o fresca antes de que bajen las temperaturas otoñales o aumenten los riesgos meteorológicos.", "efecto": "Tiene mayor probabilidad de alcanzar una madurez adecuada en regiones frescas o de estación corta que una variedad tardía, aunque el sitio y la añada siguen siendo importantes."},
    "HC_LATE_HARVEST_RIPENESS_BODY": {"subject": "la vendimia tardía, la madurez y el cuerpo del vino", "causa": "Uvas tintas sanas permanecen más tiempo en la vid antes de cosecharse mientras las condiciones todavía permiten madurar.", "mecanismo": "El tiempo adicional suele permitir más acumulación de azúcar y desarrollo de sabores y puede reducir el agua de la baya, mientras la acidez tiende a disminuir.", "efecto": "Tras la fermentación, el vino puede mostrar fruta más madura, alcohol más alto y mayor cuerpo, pero el resultado depende de la sanidad, el clima, el rendimiento, la extracción y la vinificación."},
    "HC_OLOROSO_AMONTILLADO_AGEING_PATH": {"subject": "las rutas de crianza de Oloroso y Amontillado", "causa": "El Oloroso se fortifica a un nivel que impide mantener un velo de flor estable, mientras el Amontillado comienza como vino de crianza biológica bajo flor antes de perder esa protección.", "mecanismo": "Sin la protección de la flor, el Oloroso permanece expuesto de forma controlada al oxígeno durante toda la maduración; el Amontillado primero desarrolla carácter biológico y después pasa a crianza oxidativa.", "efecto": "El Oloroso sigue una ruta de crianza exclusivamente oxidativa, mientras el Amontillado combina una fase biológica inicial con desarrollo oxidativo posterior."},
    "HC_ACID_FOOD_HIGH_ACID_WINE_BALANCE": {"subject": "el equilibrio entre un plato ácido y un vino de alta acidez", "causa": "Un plato con abundante acidez, como uno con vinagre, cítricos o ceviche, establece una referencia gustativa intensamente ácida.", "mecanismo": "Frente a esa referencia, un vino con acidez insuficiente puede perder definición y parecer ancho o plano, mientras un vino de alta acidez conserva frescura y equilibrio estructural.", "efecto": "Un blanco joven de alta acidez resulta un acompañamiento fiable porque mantiene su frescura junto al plato sin que la combinación parezca apagada o desequilibrada."},
    "HC_RESIDUAL_SUGAR_LOW_ALCOHOL_CHILI_PAIRING": {"subject": "el dulzor residual y el bajo alcohol con comida picante", "causa": "La capsaicina de un plato picante produce una sensación ardiente persistente, y el alcohol del vino puede añadir una sensación cálida independiente.", "mecanismo": "Un vino de menor graduación evita reforzar ese calor alcohólico, mientras algo de dulzor residual puede suavizar el contraste y hacer la combinación menos intensa sin neutralizar la capsaicina.", "efecto": "Un vino con alcohol moderado y algo de dulzor residual suele resultar más cómodo y equilibrado con comida picante que uno muy alcohólico o marcadamente tánico."},
    "HC_SOLAR_EXPOSURE_RED_COLOR": {"subject": "la exposición solar y el color de las uvas tintas", "causa": "Los racimos tintos reciben una exposición solar adecuada durante la maduración.", "mecanismo": "La luz favorece la síntesis de antocianos y la madurez del hollejo, siempre que no sea tan extrema que provoque calor o quemaduras.", "efecto": "Puede aumentar la acumulación de color en los hollejos y favorecer un tinto de color más profundo."},
    "HC_HUMBOLDT_CURRENT_FRESHNESS": {"subject": "la corriente de Humboldt y la frescura del Valle de Casablanca", "causa": "La corriente fría de Humboldt enfría el Pacífico cercano y favorece aire fresco y nieblas en el Valle de Casablanca.", "mecanismo": "Las temperaturas de cultivo más bajas ralentizan la maduración y reducen la pérdida respiratoria de ácidos.", "efecto": "La uva conserva acidez elevada y frescura aromática a pesar de la latitud chilena."},
    "HC_CARBONIC_MACERATION_FRUIT_LOW_TANNIN": {"subject": "la maceración carbónica en tintos jóvenes", "causa": "Racimos enteros y bayas intactas permanecen en un depósito rico en dióxido de carbono.", "mecanismo": "La fermentación intracelular genera ésteres frutales característicos y la escasa rotura y extracción limita la incorporación de taninos.", "efecto": "El tinto joven muestra fruta fresca intensa, poco tanino y una textura accesible."},
    "HC_WARM_CLIMATE_ACID_LOSS": {"subject": "el clima cálido y la pérdida de acidez natural", "causa": "Las uvas maduran bajo temperaturas cálidas de forma sostenida.", "mecanismo": "El calor acelera la respiración, especialmente el consumo de ácido málico, a medida que avanza la maduración.", "efecto": "La acidez natural de la uva tiende a ser menor que en condiciones comparables más frescas."},
    "HC_ALTITUDE_GRAPE_ACIDITY": {"subject": "la altitud y la retención de acidez en la uva", "causa": "El viñedo se sitúa a mayor altitud, donde las temperaturas suelen ser más bajas, sobre todo de noche.", "mecanismo": "La maduración más fresca ralentiza la respiración y reduce la pérdida de ácidos de la uva.", "efecto": "La fruta tiende a conservar más acidez natural que fruta comparable de una cota inferior y más cálida."},
    "HC_COOL_SPARKLING_BASE_ACIDITY": {"subject": "el clima fresco y la calidad del vino base para espumosos", "causa": "Las uvas destinadas al vino base crecen en clima fresco o en un sitio fresco de altitud.", "mecanismo": "Las temperaturas bajas ralentizan la acumulación de azúcar y conservan la acidez natural durante la maduración.", "efecto": "El vino base puede combinar acidez alta, alcohol moderado y sabores frescos adecuados para la segunda fermentación y la crianza sobre lías."},
    "HC_FORTIFICATION_STOPS_FERMENTATION": {"subject": "la fortificación para detener la fermentación", "causa": "Se añade aguardiente vínico a un vino que está fermentando.", "mecanismo": "El aguardiente eleva el alcohol hasta un nivel en el que la actividad de la levadura se detiene o resulta imposible.", "efecto": "La fermentación termina, aumenta el alcohol y queda azúcar residual si la fortificación se realiza antes de consumir todo el azúcar."},
    "HC_HIGH_FERMENTATION_TEMP_BURNT_AROMAS": {"subject": "una temperatura de fermentación excesivamente alta", "causa": "La fermentación de un vino tinto alcanza una temperatura excesiva.", "mecanismo": "El calor extremo estresa o inhibe las levaduras, acelera reacciones no deseadas y favorece la pérdida de compuestos aromáticos volátiles.", "efecto": "El vino puede perder fruta fresca y desarrollar caracteres cocidos, ásperos o quemados."},
    "HC_STAINLESS_TEMPERATURE_CONTROL": {"subject": "el control térmico en depósitos de acero inoxidable", "causa": "El mosto fermenta en un depósito de acero inoxidable equipado con control activo de temperatura.", "mecanismo": "Las camisas de refrigeración y la conductividad del recipiente permiten retirar el calor generado por las levaduras y ajustar con precisión la temperatura.", "efecto": "El productor puede controlar el ritmo de fermentación, reducir el estrés térmico y orientar el resultado aromático."},
    "HC_STAINLESS_PRIMARY_AROMA_PRESERVATION": {"subject": "el acero inoxidable y la conservación de aromas primarios", "causa": "El vino fermenta en un recipiente inerte de acero inoxidable con exposición limitada al oxígeno.", "mecanismo": "El acero no aporta sabores de madera y permite controlar una fermentación fresca sin introducir aromas ajenos a la fruta.", "efecto": "Los aromas frutales primarios pueden mantenerse más nítidos y frescos en el vino terminado."},
    "HC_SELECTED_YEAST_PREDICTABILITY": {"subject": "las levaduras seleccionadas y la predictibilidad de la fermentación", "causa": "El productor inocula el mosto con una población suficiente de una cepa de levadura seleccionada.", "mecanismo": "La cepa se establece rápidamente y posee tolerancias y características fermentativas conocidas.", "efecto": "La fermentación suele arrancar con rapidez y avanzar de forma más predecible que si depende solo de una población indígena no controlada."},
    "HC_HARVEST_COOLING_AROMA_PROTECTION": {"subject": "el enfriamiento de la vendimia y la protección aromática", "causa": "Las uvas calientes se enfrían poco después de la cosecha y antes de procesarlas.", "mecanismo": "La temperatura baja ralentiza la oxidación, la actividad microbiana y la pérdida o transformación de compuestos aromáticos volátiles.", "efecto": "Se conservan mejor los aromas primarios volátiles para la fermentación y el estilo previstos."},
    "HC_CLAY_WATER_RETENTION": {"subject": "la arcilla y la retención de agua del suelo", "causa": "El suelo contiene una proporción elevada de partículas de arcilla muy pequeñas.", "mecanismo": "Las partículas finas crean numerosos poros pequeños y una gran superficie que retienen agua mediante fuerzas capilares y de adsorción.", "efecto": "El suelo arcilloso suele drenar más despacio y conservar más agua que un suelo arenoso grueso."},
    "HC_COVER_CROP_SOIL_STRUCTURE": {"subject": "las cubiertas vegetales y la estructura del suelo", "causa": "Se cultivan cubiertas vegetales entre las hileras en lugar de mantener todo el suelo desnudo.", "mecanismo": "Sus raíces crean canales y aportan materia orgánica, mientras la vegetación amortigua la lluvia y parte de la presión del tránsito.", "efecto": "Con un manejo adecuado, mejoran la agregación y la porosidad y puede reducirse la compactación del suelo."},
    "HC_WELL_DRAINED_ROOT_DEVELOPMENT": {"subject": "el buen drenaje y el desarrollo radicular", "causa": "El suelo elimina el exceso de agua sin perder toda la humedad disponible para la vid.", "mecanismo": "El drenaje conserva oxígeno en la zona radicular y evita el encharcamiento prolongado, permitiendo que las raíces respiren y exploren el suelo.", "efecto": "Se favorecen el desarrollo radicular y el equilibrio de la vid; el drenaje por sí solo no garantiza la calidad del vino."},
    "HC_ICE_WATER_RAPID_CHILLING": {"subject": "el enfriamiento rápido de una botella con hielo y agua", "causa": "Una botella caliente se rodea con una mezcla de hielo y agua.", "mecanismo": "El agua líquida mantiene contacto continuo con el vidrio y transfiere calor con mayor eficacia que el aire frío o que unos pocos puntos de contacto con hielo.", "efecto": "La botella se enfría con rapidez y de forma uniforme sin diluir ni alterar el vino sellado."},
    "HC_AERATION_YOUNG_STRUCTURED_WINE": {"subject": "la aireación de un vino joven y estructurado", "causa": "Un tinto joven, fenólico y aromáticamente cerrado se expone deliberadamente al aire antes del servicio.", "mecanismo": "La mezcla con aire favorece la liberación de compuestos volátiles y puede disipar algunos caracteres cerrados o reductivos; no elimina los taninos de forma instantánea.", "efecto": "El vino puede mostrar mayor expresión aromática y parecer más abierto, aunque conserva su estructura tánica de base."},
    "HC_LARGE_BOWL_AROMA_EXPRESSION": {"subject": "una copa amplia para un tinto corpulento y complejo", "causa": "Un tinto de cuerpo completo y complejidad aromática se sirve en una copa de balón amplio.", "mecanismo": "La superficie ancha aumenta el contacto con el aire y el volumen de la copa crea espacio para que se acumulen compuestos aromáticos volátiles.", "efecto": "Los aromas complejos pueden abrirse y percibirse con mayor claridad que en una copa muy pequeña o estrecha."},
    "HC_SAFE_SPARKLING_CORK_OPENING": {"subject": "la apertura segura de un espumoso con corcho", "causa": "Una botella fría de espumoso contiene dióxido de carbono a presión detrás del corcho.", "mecanismo": "Sujetar firmemente el corcho, mantener la botella cerca de 45 grados y girar la botella permite liberar la presión poco a poco y bajo control.", "efecto": "Disminuye el riesgo de que el corcho salga despedido y se pierde menos vino y espuma."},
    "HC_GENTLE_CARBONATED_WINE_SERVICE": {"subject": "el servicio suave de un vino con gas carbónico residual", "causa": "El vino conserva dióxido de carbono disuelto cuando se abre y se sirve.", "mecanismo": "La agitación y un vertido rápido generan turbulencia y puntos de nucleación que liberan el gas con rapidez.", "efecto": "Evitar la agitación y servir lentamente limita la espuma repentina, el desbordamiento y la pérdida innecesaria de gas."},
    "HC_EXTRACTION_BODY_STRUCTURE": {"subject": "el nivel de extracción y la estructura del vino", "causa": "El productor modifica cuánto se extrae de los hollejos y otros sólidos durante la vinificación.", "mecanismo": "Un contacto y una extracción mayores transfieren más compuestos fenólicos, taninos, pigmentos y otras sustancias al vino en fermentación.", "efecto": "Con la misma fruta y dentro del mismo estilo, una extracción mayor suele aumentar la estructura y la sensación de cuerpo; no es el único factor que determina el cuerpo."},
    "HC_SHORT_MACERATION_LOW_COLOR": {"subject": "la maceración corta y la menor extracción de color", "causa": "El mosto tinto permanece poco tiempo en contacto con los hollejos.", "mecanismo": "El contacto limitado deja menos tiempo para que antocianos y otros pigmentos pasen de los hollejos al vino.", "efecto": "A igualdad de los demás factores, el tinto tendrá menor intensidad de color que otro sometido a una maceración eficaz más larga."},
    "HC_MUST_SETTLING_CLARIFICATION": {"subject": "el desfangado del mosto antes de fermentar", "causa": "El mosto recién prensado contiene sólidos de uva en suspensión antes de la fermentación alcohólica.", "mecanismo": "Enfriar y mantener el mosto permite que las partículas pesadas sedimenten para trasegar el jugo más limpio y separarlo del depósito.", "efecto": "El mosto se clarifica antes de fermentar, reduciendo sólidos gruesos y conservando el nivel de turbidez que busca el productor."},
    "HC_NEW_OAK_TANNIN_WHITE_WINE": {"subject": "el aporte de tanino de barrica nueva a un vino blanco", "causa": "Un vino blanco fermenta o madura en una barrica de roble nueva.", "mecanismo": "Como la madera aún no se ha agotado por usos anteriores, taninos y otros compuestos fenólicos del roble pueden disolverse en el vino.", "efecto": "El blanco puede ganar estructura fenólica y tanino además de aromas de roble; la magnitud depende de la barrica y del contacto."},
})

NODE_ES.update({
    "HC_MADEIRA_HEAT_OXIDATIVE_AGEING": {
        "subject": "el calor y la crianza oxidativa de Madeira",
        "causa": "El Madeira fortificado madura con exposición al calor y al oxígeno, de forma más rápida mediante estufagem o más gradual mediante canteiro.",
        "mecanismo": "El calor y la oxidación controlada transforman los aromas de fruta fresca, mientras la acidez natural elevada sigue siendo un elemento estructural importante.",
        "efecto": "El vino desarrolla notas de nuez, caramelo y fruta seca; en Malmsey, el dulzor elevado queda equilibrado por la acidez.",
    },
    "HC_MOSCATO_ASTI_FERMENTATION_ARREST": {
        "subject": "la detención de la fermentación en Moscato d'Asti",
        "causa": "Un mosto aromático de Moscatel fermenta bajo presión y la fermentación se detiene antes de consumir todo el azúcar de la uva.",
        "mecanismo": "El enfriamiento y la filtración frenan la levadura, conservan azúcar residual, limitan la producción de alcohol y retienen aromas primarios y parte del dióxido de carbono.",
        "efecto": "El vino resulta ligeramente espumoso, dulce, de baja graduación y con aromas florales y de uva marcados.",
    },
    "HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION": {
        "subject": "el secado parcial de uvas antes de la fermentación",
        "causa": "Uvas maduras y sanas se secan después de la vendimia antes de iniciar la fermentación alcohólica.",
        "mecanismo": "La evaporación de agua concentra azúcares, ácidos, compuestos de sabor y fenoles en las bayas.",
        "efecto": "El vino puede alcanzar alcohol potencial alto, cuerpo considerable y sabores concentrados de fruta madura o desecada; la sanidad y el control del secado siguen siendo esenciales.",
    },
    "HC_OAK_LIGNIN_VANILLIN": {
        "subject": "la lignina del roble y la formación de vainillina",
        "causa": "La madera de roble se sazona y tuesta antes de utilizarse como barrica.",
        "mecanismo": "El calor y el secado degradan parte de la lignina y forman aldehídos aromáticos como la vainillina, que después puede extraerse hacia el vino.",
        "efecto": "El vino puede adquirir aroma de vainilla junto con otros caracteres de roble; la intensidad depende del origen, tostado, edad y tiempo de contacto de la barrica.",
    },
    "HC_FRENCH_AMERICAN_OAK_STYLE": {
        "subject": "el origen del roble y la intensidad de sus aromas",
        "causa": "El vino madura en barricas elaboradas con especies y estructuras de grano asociadas habitualmente al roble francés o americano.",
        "mecanismo": "La especie, el grano, el secado y el tostado modifican la extracción de lactonas, vainillina, taninos y compuestos tostados.",
        "efecto": "El roble americano suele aportar vainilla y coco más evidentes, mientras el francés suele percibirse más sutil; la tonelería, el tostado y el uso previo pueden cambiar ambos patrones.",
    },
    "HC_NATURAL_CORK_SLOW_OXYGEN": {
        "subject": "el corcho natural y la evolución lenta en botella",
        "causa": "Un vino apto para guarda se sella con corcho natural y se conserva en condiciones estables.",
        "mecanismo": "El cierre y el oxígeno inicial del espacio de cabeza exponen al vino a cantidades muy pequeñas de oxígeno con el tiempo, aunque la transmisión varía entre corchos y condiciones de almacenamiento.",
        "efecto": "La evolución química lenta puede favorecer integración y aromas terciarios, pero el corcho no garantiza una mejora y un aporte excesivo o variable puede causar oxidación prematura.",
    },
})

NODE_ES.update({
    "HC_OAKED_WHITE_SERVICE_TEMPERATURE": {"subject": "la temperatura de servicio de un blanco con crianza en roble", "causa": "Un blanco seco tiene cuerpo, aromas de roble y complejidad.", "mecanismo": "Servirlo moderadamente fresco conserva la frescura y permite que se expresen más aromas y textura que a una temperatura excesivamente baja.", "efecto": "Un intervalo cercano a 10-13 °C puede equilibrar frescura y expresión en muchos blancos con cuerpo y roble."},
    "HC_SPARKLING_SERVICE_TEMPERATURE": {"subject": "la temperatura fresca de servicio de un espumoso", "causa": "El espumoso contiene dióxido de carbono disuelto y se prepara para el servicio.", "mecanismo": "El frío retiene mejor el gas, reduce la formación brusca de espuma y conserva frescura; un frío extremo puede apagar los aromas.", "efecto": "Los espumosos secos suelen servirse bien fríos, ajustando la temperatura según su complejidad y tiempo de crianza."},
    "HC_LIGHT_WHITE_SERVICE_TEMPERATURE": {"subject": "la temperatura de servicio de un blanco seco y ligero", "causa": "Un blanco ligero depende de su frescura y de aromas primarios delicados.", "mecanismo": "El servicio frío realza la acidez y limita la sensación alcohólica, aunque una temperatura demasiado baja reduce la expresión aromática.", "efecto": "Un intervalo cercano a 6-8 °C suele ser apropiado para blancos secos sencillos y ligeros."},
    "HC_AMONTILLADO_SERVICE_TEMPERATURE": {"subject": "la temperatura de servicio de un Amontillado", "causa": "Un Amontillado seco combina desarrollo biológico y oxidativo.", "mecanismo": "Un enfriamiento moderado conserva frescura y controla el calor alcohólico sin ocultar sus aromas de frutos secos y carácter sabroso.", "efecto": "Una temperatura cercana a 13 °C puede equilibrar frescura, alcohol y expresión aromática."},
    "HC_SAIGNEE_ROSE_EXTRACTION": {"subject": "el sangrado para elaborar un rosado", "causa": "Se separa jugo de una vinificación tinta después de un periodo de contacto con los hollejos.", "mecanismo": "Antes del sangrado, el contacto extrae pigmento, sabor y parte de los compuestos fenólicos de las pieles tintas.", "efecto": "Frente a un rosado pálido de mezcla, puede resultar un vino de color más profundo, fruta más madura y mayor estructura fenólica."},
    "HC_MOSEL_COOL_SLOPE_ACIDITY": {"subject": "el clima fresco y las pendientes del Mosel", "causa": "Los viñedos del Mosel combinan clima fresco y septentrional con pendientes empinadas y bien expuestas.", "mecanismo": "El frío ralentiza la respiración y conserva los ácidos, mientras la exposición de la ladera mejora la captación solar y ayuda a completar la maduración.", "efecto": "El Riesling puede mantener acidez alta y frescura a la vez que alcanza madurez aromática en los mejores sitios."},
    "HC_WARM_CLIMATE_RIPE_FRUIT_ALCOHOL": {"subject": "el clima cálido, la fruta madura y el alcohol potencial", "causa": "Uvas tintas maduran con calor sostenido y suficiente insolación.", "mecanismo": "La acumulación rápida de azúcar eleva el alcohol potencial y la maduración avanzada desplaza el perfil hacia fruta negra madura o desecada.", "efecto": "El vino puede mostrar mayor cuerpo, alcohol y fruta negra madura, siempre que el calor y el estrés hídrico no sean excesivos."},
    "HC_MOSEL_RESIDUAL_SUGAR_LOW_ALCOHOL": {"subject": "el azúcar residual y el bajo alcohol en estilos del Mosel", "causa": "Un Riesling de clima fresco fermenta hasta un estilo que conserva parte del azúcar de la uva.", "mecanismo": "Al detener la fermentación antes de convertir todo el azúcar, queda dulzor residual y se produce menos alcohol, mientras la acidez alta equilibra el conjunto.", "efecto": "Muchos estilos dulces o semidulces del Mosel combinan azúcar residual perceptible, alcohol bajo y acidez alta."},
    "HC_LONG_MACERATION_LARGE_CASK": {"subject": "la maceración larga y la crianza en grandes toneles", "causa": "Un tinto estructurado permanece largo tiempo con los hollejos y después madura en un recipiente grande, a menudo usado.", "mecanismo": "La maceración extrae abundantes fenoles, mientras el gran volumen reduce la superficie de madera por litro y limita el sabor intenso de roble nuevo.", "efecto": "El vino conserva estructura firme y puede evolucionar gradualmente sin quedar dominado por aromas de roble nuevo."},
})

NODE_ES.update({
    "HC_TOKAJI_ASZU_BERRY_ADDITION": {"subject": "la adición de bayas Aszú botritizadas", "causa": "Bayas seleccionadas y concentradas por podredumbre noble se añaden al mosto en fermentación o al vino base.", "mecanismo": "La maceración transfiere azúcar, acidez, sabor y compuestos derivados de la botrytis desde las bayas concentradas al líquido.", "efecto": "El Tokaji Aszú gana dulzor, concentración y complejidad botritizada, equilibrados por su acidez."},
    "HC_INDIGENOUS_YEAST_COMPLEXITY_VARIABILITY": {"subject": "las levaduras indígenas y la expresión del vino", "causa": "La fermentación comienza con poblaciones de levaduras presentes en la uva y la bodega, no con una sola cepa seleccionada.", "mecanismo": "La sucesión de cepas puede producir una gama más diversa de metabolitos antes de que Saccharomyces complete la fermentación.", "efecto": "El vino puede mostrar un carácter distintivo o complejo, pero con menor previsibilidad de aroma, velocidad y final de fermentación."},
    "HC_VINTAGE_CHAMPAGNE_EXTENDED_AGEING": {"subject": "la selección de añada y la crianza extendida de un Champagne vintage", "causa": "El productor declara una sola cosecha seleccionada y normalmente la madura más tiempo que su Champagne sin añada estándar.", "mecanismo": "La crianza prolongada sobre lías aumenta el desarrollo autolítico y la integración, mientras la fruta de un año conserva carácter de añada.", "efecto": "El vino puede mostrar mayor estructura, complejidad desarrollada y potencial de guarda."},
    "HC_PRIORAT_LICORELLA_LOW_YIELD_CONCENTRATION": {"subject": "las laderas de licorella y la concentración en Priorat", "causa": "Vides viejas de Garnacha y Cariñena crecen en laderas cálidas, secas, pobres y de drenaje libre.", "mecanismo": "La disponibilidad limitada de agua y nutrientes restringe vigor y rendimiento, mientras la insolación permite madurar una cosecha pequeña.", "efecto": "Las uvas maduras de bajo rendimiento pueden producir tintos concentrados, intensos y estructurados."},
    "HC_BORDEAUX_BLEND_VINTAGE_VARIATION": {"subject": "el ensamblaje bordelés frente a la variación de añada", "causa": "Las variedades bordelesas responden de manera distinta al tiempo de cada temporada y maduran en momentos diferentes.", "mecanismo": "Mezclar variedades y lotes permite combinar componentes que rindieron de forma desigual y equilibrar fruta, acidez, tanino y cuerpo.", "efecto": "El vino final puede resultar más equilibrado y coherente que si dependiera de un único componente afectado por la añada."},
})

# Explicitly reviewed promotions supplement matcher v2 without changing it.
# Every entry is deterministic, node-bound, provenance-rich, and caveated.
MANUAL_REVIEW_PROMOTIONS: dict[str, dict[str, str]] = {
    "wset3_11": {"node_id": "CC_COOL_CLIMATE_ACIDITY", "reason": "El clima fresco explica directamente la retención de acidez de la respuesta correcta.", "caveat": "La continentalidad por sí sola no garantiza acidez alta; importan la temperatura de maduración, el sitio y la añada."},
    "wset3_65": {"node_id": "HC_EXCESSIVE_WHITE_OXIDATION", "reason": "El nodo explica el apagamiento de fruta, el cambio de color y las notas de nuez de la opción correcta.", "caveat": "Las notas de nuez pueden ser buscadas en estilos oxidativos; aquí se interpretan como defecto dentro del contexto de la pregunta."},
    "wset3_104": {"node_id": "HC_MADEIRA_HEAT_OXIDATIVE_AGEING", "reason": "El calor, la oxidación y la acidez explican el perfil sensorial de Malmsey envejecido.", "caveat": "Malmsey describe el estilo más dulce de Madeira; otros estilos muestran distinto nivel de dulzor."},
    "wset3_113": {"node_id": "HC_COOL_SPARKLING_BASE_ACIDITY", "reason": "La acidez suficiente del vino base permite conservar frescura tras la segunda fermentación y la crianza.", "caveat": "La acidez no es el único requisito técnico; sanidad, alcohol y estabilidad del vino base también importan."},
    "wset3_208": {"node_id": "CC_FLOR_BIOLOGICAL_AGEING", "reason": "La flor protege frente al oxígeno y genera el carácter biológico señalado por la respuesta.", "caveat": "La percepción salina no procede de añadir sal y varía con el vino y el contexto sensorial."},
    "wset3_210": {"node_id": "HC_OXIDATIVE_AGEING_TERTIARY", "reason": "La larga crianza oxidativa en toneles explica el carácter desarrollado del Tawny con indicación de edad.", "caveat": "La indicación expresa un perfil de edad, no la edad exacta de cada componente de la mezcla."},
    "wset3_219": {"node_id": "HC_MOSCATO_ASTI_FERMENTATION_ARREST", "reason": "La fermentación detenida explica conjuntamente el dulzor, el bajo alcohol y los aromas florales.", "caveat": "El estilo es ligeramente espumoso y no debe generalizarse a todos los vinos de Moscatel."},
    "wset3_230": {"node_id": "HC_CONTINENTALITY_STYLE", "reason": "La temporada continental y sus oscilaciones térmicas explican acidez y estructura firme en tintos aptos.", "caveat": "El resultado depende de variedad, madurez, sitio y añada; no todos los tintos continentales son idénticos."},
    "wset3_251": {"node_id": "HC_MARITIME_MODERATION", "reason": "La influencia oceánica modera extremos y favorece maduración más uniforme y estilos frescos.", "caveat": "La lluvia y la humedad marítimas también pueden elevar el riesgo de enfermedad y dilución."},
    "wset3_266": {"node_id": "HC_ALTITUDE_SLOW_RIPENING_FRESHNESS", "reason": "La altitud y las noches frescas explican la maduración lenta y la retención de acidez.", "caveat": "La altitud no garantiza calidad por sí sola; exposición, agua, suelo y manejo siguen siendo decisivos."},
    "wset3_282": {"node_id": "HC_OXIDATIVE_AGEING_TERTIARY", "reason": "La crianza prolongada con roble y oxígeno controlado explica la evolución terciaria de la opción.", "caveat": "La categoría regional y el tiempo de crianza no garantizan por sí solos calidad ni un perfil único."},
    "wset3_321": {"node_id": "HC_COOL_CLIMATE_STYLE", "reason": "El clima continental fresco de Chablis explica maduración lenta, acidez alta y alcohol moderado.", "caveat": "La añada y la ubicación dentro de Chablis modifican madurez y concentración."},
    "wset3_339": {"node_id": "HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION", "reason": "El secado parcial previo a la fermentación explica la concentración del mosto para Amarone.", "caveat": "El secado debe controlarse para evitar podredumbre no deseada y no es equivalente a añadir azúcar."},
    "wset3_341": {"node_id": "HC_ALTITUDE_GRAPE_ACIDITY", "reason": "La altitud y el clima fresco reducen la pérdida respiratoria de ácidos y explican la respuesta.", "caveat": "En Mosel, latitud, exposición y pendiente interactúan; la altitud no actúa de forma aislada."},
    "wset3_345": {"node_id": "HC_MARITIME_MODERATION", "reason": "La influencia marítima modera el clima y explica la maduración equilibrada de Cabernet Sauvignon.", "caveat": "La influencia marítima también trae variabilidad de lluvia y no elimina los riesgos de la añada."},
    "wset3_401": {"node_id": "HC_NEW_OAK_STRUCTURE_SPICE", "reason": "El roble nuevo explica el aporte de especias, estructura y oxigenación controlada de la opción.", "caveat": "El uso de roble nuevo no es universal ni garantiza calidad; debe integrarse con la fruta."},
    "wset3_421": {"node_id": "HC_CONTINENTALITY_STYLE", "reason": "La amplitud térmica continental explica la combinación de madurez, tanino y acidez de la respuesta.", "caveat": "La intensidad final depende además de variedad, rendimiento, extracción, crianza y añada."},
    "wset3_460": {"node_id": "HC_SELECTED_YEAST_PREDICTABILITY", "reason": "Una cepa seleccionada permite orientar la fermentación y hacer más predecible su perfil aromático.", "caveat": "La levadura influye, pero no controla por sí sola todo el perfil aromático del vino."},
    "wset3_466": {"node_id": "HC_SELECTED_YEAST_PREDICTABILITY", "reason": "Las características conocidas de una levadura seleccionada explican el mayor control fermentativo.", "caveat": "La predictibilidad depende también de temperatura, nutrientes, higiene y composición del mosto."},
    "wset3_499": {"node_id": "HC_OAK_LIGNIN_VANILLIN", "reason": "La degradación de lignina genera vainillina y explica directamente las notas de vainilla.", "caveat": "La vainilla no depende solo de la lignina: origen, tostado, edad y contacto del roble modifican su intensidad."},
    "wset3_514": {"node_id": "HC_SO2_MICROBIAL_INHIBITION", "reason": "El sulfitado inhibe microorganismos no deseados y explica el control antes de la fermentación.", "caveat": "El SO2 no esteriliza el mosto ni sustituye higiene, temperatura y una inoculación adecuada."},
    "wset3_669": {"node_id": "HC_CONTINENTALITY_STYLE", "reason": "El clima continental de Piemonte explica maduración ajustada, acidez conservada y tanino firme.", "caveat": "La variedad y el mesoclima determinan cuánto se expresa este patrón."},
    "wset3_673": {"node_id": "HC_FRENCH_AMERICAN_OAK_STYLE", "reason": "La composición y el grano del roble explican la diferencia habitual de intensidad aromática.", "caveat": "Es una tendencia, no una regla absoluta; tostado, tonelero, edad y tamaño pueden cambiar el resultado."},
    "wset3_740": {"node_id": "HC_CANOPY_VIGOUR_EXPOSURE", "reason": "La gestión del dosel regula luz, ventilación y vigor, afectando directamente la madurez de la fruta.", "caveat": "La exposición óptima depende del clima; demasiada luz y calor pueden quemar o deshidratar los racimos."},
    "wset3_850": {"node_id": "HC_NATURAL_CORK_SLOW_OXYGEN", "reason": "La transmisión limitada de oxígeno explica la evolución gradual asociada a cierres de corcho natural.", "caveat": "La porosidad no garantiza mejora y existe variación entre corchos; demasiado oxígeno acelera la oxidación."},
}

MANUAL_REVIEW_PROMOTIONS.update({
    "wset3_28": {"node_id": "HC_BRUT_NATURE_NO_DOSAGE", "reason": "La ausencia de dosificación explica el mínimo azúcar residual de Brut Nature.", "caveat": "La acidez alta procede del vino base y del estilo, no de omitir la dosificación."},
    "wset3_49": {"node_id": "HC_OAKED_WHITE_SERVICE_TEMPERATURE", "reason": "Una temperatura moderadamente fresca equilibra frescura, textura y aromas de roble.", "caveat": "El intervalo exacto depende del cuerpo, la complejidad y la temperatura ambiente."},
    "wset3_67": {"node_id": "HC_SPARKLING_SERVICE_TEMPERATURE", "reason": "El servicio frío conserva CO2, controla la espuma y mantiene la frescura.", "caveat": "Los espumosos complejos pueden expresarse mejor algo menos fríos que los estilos sencillos."},
    "wset3_76": {"node_id": "HC_LOW_SERVICE_TEMPERATURE_TANNIN_AROMA", "reason": "Un tinto ligero se sirve fresco para conservar fruta sin apagar aromas ni endurecer demasiado la estructura.", "caveat": "La temperatura recomendada es orientativa y debe ajustarse al cuerpo, tanino y ambiente."},
    "wset3_212": {"node_id": "HC_TANK_METHOD_FRUIT_RETENTION", "reason": "El método de tanque y el contacto corto con lías explican fruta fresca y limitada autólisis.", "caveat": "El dulzor y la acidez concretos dependen de la uva, la dosificación y el equilibrio final."},
    "wset3_227": {"node_id": "HC_SAIGNEE_ROSE_EXTRACTION", "reason": "El contacto previo con hollejos explica mayor color, fruta madura y estructura fenólica.", "caveat": "Saignée no garantiza siempre más tanino; variedad, tiempo y temperatura de contacto modifican el resultado."},
    "wset3_247": {"node_id": "HC_MOSEL_COOL_SLOPE_ACIDITY", "reason": "El clima fresco conserva acidez y las pendientes bien expuestas ayudan a completar la maduración.", "caveat": "La pendiente ayuda a la madurez; no crea acidez por sí sola."},
    "wset3_262": {"node_id": "HC_WARM_CLIMATE_RIPE_FRUIT_ALCOHOL", "reason": "El calor explica azúcar, alcohol potencial y fruta negra madura en Merlot.", "caveat": "La suavidad del tanino depende también de madurez fenólica, extracción y crianza."},
    "wset3_322": {"node_id": "HC_MOSEL_COOL_SLOPE_ACIDITY", "reason": "El clima frío conserva acidez y la exposición de pendiente permite madurez aromática.", "caveat": "Latitud, río, orientación, suelo y añada también influyen en el resultado."},
    "wset3_323": {"node_id": "HC_WARM_CLIMATE_RIPE_FRUIT_ALCOHOL", "reason": "El clima cálido de Barossa explica fruta negra madura, cuerpo y alcohol potencial.", "caveat": "El roble es una decisión de bodega y no una consecuencia automática del clima."},
    "wset3_329": {"node_id": "HC_LIGHT_WHITE_SERVICE_TEMPERATURE", "reason": "El frío moderado conserva frescura y delicadeza en un blanco seco ligero.", "caveat": "Una temperatura demasiado baja puede ocultar los aromas primarios."},
    "wset3_347": {"node_id": "HC_COOL_CLIMATE_STYLE", "reason": "La maduración fresca explica fruta roja y acidez vibrante en Pinot Noir.", "caveat": "El uso de roble es una decisión de productor y varía entre regiones y niveles de calidad."},
    "wset3_358": {"node_id": "HC_FRENCH_AMERICAN_OAK_STYLE", "reason": "La tendencia aromática del roble americano explica su uso tradicional y sus notas más evidentes.", "caveat": "Tostado, edad, tamaño y uso previo de la barrica pueden cambiar el perfil."},
    "wset3_367": {"node_id": "HC_FROST_SHOOT_YIELD_DAMAGE", "reason": "La brotación temprana en clima fresco explica la exposición de Champagne a heladas primaverales.", "caveat": "El riesgo varía con topografía, fase fenológica y condiciones de cada añada."},
    "wset3_386": {"node_id": "HC_MOSEL_RESIDUAL_SUGAR_LOW_ALCOHOL", "reason": "Retener azúcar implica convertir menos azúcar en alcohol y explica el contraste de la respuesta.", "caveat": "No todos los Riesling del Mosel son dulces ni todos los del Pfalz son secos."},
    "wset3_389": {"node_id": "HC_FRENCH_AMERICAN_OAK_STYLE", "reason": "El uso tradicional de roble americano explica parte del perfil de crianza de Rioja.", "caveat": "La calidad no depende únicamente del origen del roble; fruta, tonelería y tiempo de crianza también cuentan."},
    "wset3_390": {"node_id": "HC_MARITIME_MODERATION", "reason": "La mayor moderación costera de Sonoma frente a Napa ayuda a explicar estilos más frescos.", "caveat": "Ambas regiones contienen mesoclimas diversos y la comparación no se aplica a todos los vinos."},
    "wset3_393": {"node_id": "HC_LONG_MACERATION_LARGE_CASK", "reason": "La maceración larga y los grandes toneles explican estructura y crianza con roble menos dominante.", "caveat": "La práctica varía por productor y convive con estilos modernos de maceración y barrica diferentes."},
    "wset3_396": {"node_id": "HC_MARITIME_MODERATION", "reason": "La influencia oceánica modera temperaturas y explica el marco climático del Loira.", "caveat": "La influencia continental aumenta hacia el este y el Loira no tiene un clima uniforme."},
    "wset3_413": {"node_id": "HC_OAK_AGEING_COMPLEXITY", "reason": "La crianza prolongada en roble explica integración, oxigenación y aromas secundarios o terciarios.", "caveat": "Reserva es una categoría regulada; el tiempo no garantiza por sí solo calidad ni complejidad."},
    "wset3_701": {"node_id": "HC_AMONTILLADO_SERVICE_TEMPERATURE", "reason": "El enfriamiento moderado equilibra alcohol y expresión aromática en Amontillado.", "caveat": "La cifra es orientativa y puede ajustarse al estilo, la copa y la temperatura ambiente."},
    "wset3_715": {"node_id": "HC_LOW_SERVICE_TEMPERATURE_TANNIN_AROMA", "reason": "Un tinto de cuerpo medio se sirve fresco, pero no tan frío como para apagar aromas o endurecer taninos.", "caveat": "El intervalo depende de alcohol, tanino, cuerpo, crianza y condiciones de servicio."},
    "wset3_723": {"node_id": "HC_EXCESSIVE_WHITE_OXIDATION", "reason": "La oxidación transforma fruta fresca y puede generar nuez, manzana cocida y caramelo.", "caveat": "Esos aromas pueden ser buscados en estilos oxidativos; son defecto sólo cuando contradicen el estilo previsto."},
    "wset3_726": {"node_id": "HC_SPARKLING_SERVICE_TEMPERATURE", "reason": "El servicio bien frío conserva presión y frescura en un espumoso seco.", "caveat": "Los espumosos de larga crianza pueden servirse algo más cálidos para expresar complejidad."},
    "wset3_738": {"node_id": "HC_FOOD_SWEETNESS_WINE_CONTRAST", "reason": "Un alimento más dulce reduce por contraste el dulzor y la fruta percibidos del vino.", "caveat": "El efecto depende de la diferencia real de dulzor y del equilibrio de acidez del espumoso."},
})

MANUAL_REVIEW_PROMOTIONS.update({
    "wset3_8": {"node_id": "HC_TOKAJI_ASZU_BERRY_ADDITION", "reason": "La adición de bayas botritizadas concentradas explica el dulzor, la intensidad y la complejidad del Tokaji Aszú.", "caveat": "El método concreto y las proporciones varían; la podredumbre noble y la acidez son tan importantes como la adición."},
    "wset3_34": {"node_id": "HC_INDIGENOUS_YEAST_COMPLEXITY_VARIABILITY", "reason": "La diversidad de levaduras locales puede aportar metabolitos y un carácter más distintivo.", "caveat": "La expresión del terruño es una interpretación estilística, no una garantía; también aumenta la variabilidad y el riesgo de fermentación."},
    "wset3_44": {"node_id": "HC_PROTEIN_FAT_TANNIN_SOFTENING", "reason": "Las proteínas y la grasa reducen el contraste astringente y pueden hacer que el tanino parezca más suave.", "caveat": "La sal también puede suavizar la percepción, pero el resultado depende de la intensidad, la cocción y otros componentes del plato."},
    "wset3_55": {"node_id": "HC_VOLATILE_ACIDITY_VINEGAR_SOLVENT", "reason": "El ácido acético y el acetato de etilo explican los aromas de vinagre y disolvente.", "caveat": "Concentraciones bajas pueden formar parte de algunos estilos; se considera defecto cuando domina o desequilibra el vino."},
    "wset3_69": {"node_id": "HC_ACID_FOOD_HIGH_ACID_WINE_BALANCE", "reason": "La acidez refresca frente a la grasa y evita que una salsa cremosa resulte pesada.", "caveat": "La intensidad aromática, el dulzor y la sal del plato también deben ser compatibles con el vino."},
    "wset3_77": {"node_id": "HC_TCA_MUSTY_CARDBOARD", "reason": "Un corcho contaminado puede transferir TCA al vino y apagar la fruta.", "caveat": "El TCA también puede proceder de otros materiales contaminados de la bodega; no todo defecto de corcho es TCA."},
    "wset3_79": {"node_id": "HC_PROTEIN_FAT_TANNIN_SOFTENING", "reason": "Las proteínas y la grasa de la carne reducen la astringencia percibida de un tinto tánico.", "caveat": "Salsa, sal, picante y grado de cocción pueden cambiar el equilibrio del maridaje."},
    "wset3_96": {"node_id": "HC_MADEIRA_HEAT_OXIDATIVE_AGEING", "reason": "El estufagem aplica calentamiento prolongado y acelera el desarrollo característico de Madeira.", "caveat": "Estufagem es una vía de maduración; canteiro usa calor ambiental más suave y tiempos más largos."},
    "wset3_116": {"node_id": "HC_VINTAGE_CHAMPAGNE_EXTENDED_AGEING", "reason": "La selección de una añada y la crianza prolongada sobre lías explican mayor estructura, complejidad y longevidad potencial.", "caveat": "La comparación es con el estilo sin añada del mismo productor; una añada declarada no garantiza superioridad absoluta."},
    "wset3_122": {"node_id": "HC_SPARKLING_AUTOLYTIC_AROMAS", "reason": "La autólisis durante la crianza sobre lías explica pan tostado y frutos secos, mientras la uva base conserva acidez.", "caveat": "La intensidad autolítica depende del tiempo sobre lías y no todos los Cava muestran el mismo desarrollo."},
    "wset3_200": {"node_id": "HC_VINTAGE_CHAMPAGNE_EXTENDED_AGEING", "reason": "La fruta de una sola cosecha y la crianza extendida explican el carácter de añada y el desarrollo del estilo.", "caveat": "El nivel de dulzor depende de la dosificación; vintage no significa automáticamente seco en todos los casos."},
    "wset3_225": {"node_id": "HC_TRADITIONAL_BOTTLE_SECOND_FERMENTATION", "reason": "La segunda fermentación en botella distingue el método tradicional de Franciacorta del método de tanque típico de Prosecco.", "caveat": "La diferencia de estilo también depende de variedades, tiempo sobre lías, presión y dosificación."},
    "wset3_233": {"node_id": "HC_WARM_CLIMATE_RIPE_FRUIT_ALCOHOL", "reason": "El clima mediterráneo cálido favorece madurez, cuerpo y fruta madura, mientras aumenta la pérdida de acidez.", "caveat": "Languedoc contiene zonas frescas y estilos diversos; altitud, costa, rendimiento y cosecha pueden conservar más acidez."},
    "wset3_249": {"node_id": "HC_PRIORAT_LICORELLA_LOW_YIELD_CONCENTRATION", "reason": "Las laderas secas y pobres de licorella restringen vigor y rendimiento, ayudando a explicar la concentración de Garnacha y Cariñena.", "caveat": "La licorella no aporta un sabor directo y único; edad de la vid, exposición, agua y decisiones de bodega también influyen."},
    "wset3_253": {"node_id": "HC_BAROLO_TERTIARY_EVOLUTION", "reason": "Nebbiolo aporta tanino y acidez altos que requieren y soportan crianza prolongada.", "caveat": "La duración y el recipiente de crianza varían por productor; no toda crianza larga mejora automáticamente el vino."},
    "wset3_274": {"node_id": "HC_OAK_AGEING_COMPLEXITY", "reason": "La crianza más larga permite integración estructural y desarrollo aromático frente a un Chianti joven.", "caveat": "Riserva es una categoría regulada; la complejidad depende también de fruta, extracción, recipiente y guarda en botella."},
    "wset3_284": {"node_id": "HC_MARITIME_MODERATION", "reason": "La niebla reduce temperatura y radiación efectiva durante parte del día, ralentizando maduración y pérdida de acidez.", "caveat": "El efecto varía dentro de Napa y la niebla no sustituye las necesidades de agua ni determina por sí sola la calidad."},
    "wset3_292": {"node_id": "HC_ALTITUDE_SLOW_RIPENING_FRESHNESS", "reason": "La altitud enfría las noches y ayuda a conservar acidez y fruta fresca durante la maduración.", "caveat": "La radiación, orientación, agua y variedad modifican el efecto; la altitud no garantiza un perfil único."},
    "wset3_302": {"node_id": "HC_CARBONIC_MACERATION_FRUIT_LOW_TANNIN", "reason": "La maceración carbónica o semicarbónica explica fruta roja intensa, tanino bajo y consumo temprano.", "caveat": "Beaujolais Nouveau también depende de Gamay, rendimientos, selección y una crianza muy corta."},
    "wset3_328": {"node_id": "HC_COOL_CLIMATE_STYLE", "reason": "La maduración en clima relativamente fresco conserva acidez y favorece el perfil cítrico de lima del Riesling.", "caveat": "Las notas de lima no proceden sólo del clima; variedad, sitio, cosecha y evolución en botella también cuentan."},
    "wset3_357": {"node_id": "HC_RED_WINE_AGEABILITY_STRUCTURE", "reason": "La concentración de color y tanino aporta estructura capaz de sostener una guarda prolongada.", "caveat": "El potencial de guarda también requiere acidez, fruta suficiente, elaboración limpia y almacenamiento adecuado."},
    "wset3_366": {"node_id": "HC_WARM_CLIMATE_RIPE_FRUIT_ALCOHOL", "reason": "La maduración cálida acumula azúcar y fruta negra madura, explicando alcohol alto y notas especiadas en Zinfandel.", "caveat": "Fecha de cosecha, viñedo, rendimiento y elaboración pueden producir estilos más frescos o menos alcohólicos."},
    "wset3_394": {"node_id": "HC_STEEP_SLOPE_SOLAR_RIPENING", "reason": "La pendiente y la exposición solar aumentan la intercepción de luz y ayudan a madurar la uva en el relieve del Douro Superior.", "caveat": "Orientación, altitud, disponibilidad de agua, suelo y añada modifican el efecto; la pendiente no garantiza calidad por sí sola."},
    "wset3_420": {"node_id": "HC_BORDEAUX_BLEND_VINTAGE_VARIATION", "reason": "Mezclar variedades con respuestas distintas a la añada permite equilibrar componentes fuertes y débiles.", "caveat": "El ensamblaje no corrige fruta defectuosa y puede complementarse con selección, manejo de viñedo y clasificación de lotes."},
    "wset3_439": {"node_id": "HC_MOSEL_COOL_SLOPE_ACIDITY", "reason": "La pendiente y orientación aumentan la captación solar y ayudan a completar la maduración en el clima fresco del Mosel.", "caveat": "El río, la roca, la altitud, la añada y el manejo del viñedo también contribuyen a la calidad."},
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


def _build_enrichment_record(
    entry: dict,
    batch: list[dict],
    promotion: dict[str, str] | None = None,
) -> dict:
    item, match = entry["item"], entry["match"]
    chain_es = NODE_ES[match["node_id"]]
    causal_provenance = {
        "derived_from": match["node_id"],
        "matched_keywords": match["matched_keywords"],
        "stem_hits": match["stem_hits"],
        "correct_option_hits": match["correct_option_hits"],
        "match_score": match["score"],
    }
    if promotion:
        causal_provenance.update({
            "node_id": match["node_id"],
            "derived_from": "manual_review_v1",
            "promotion_method": "manual_review_v1",
            "review_reason": promotion["reason"],
            "learner_caveat": promotion["caveat"],
        })
    record = {
        "item_id": item["id"],
        "causal_chain": {
            "causa": chain_es["causa"],
            "mecanismo": chain_es["mecanismo"],
            "efecto": chain_es["efecto"],
        },
        "feedback_by_mode": build_feedback_by_mode(item, chain_es),
        "_provenance": {
            "causal_chain": causal_provenance,
            "feedback_by_mode": {"derived_from": f"template_v1 + {match['node_id']}"},
        },
    }
    if promotion:
        caveat = promotion["caveat"]
        record["feedback_by_mode"]["mentor"] += f" Matiz: {caveat}"
        record["feedback_by_mode"]["trainer"] += f" Matiz: {caveat}"
        record["feedback_by_mode"]["reviewer"] += f" Matiz: {caveat}"
    drill = build_micro_drill(entry, batch)
    if drill:
        record["micro_drill"] = drill
        record["_provenance"]["micro_drill"] = {
            "derived_from": f"node_anchored_v1 ({match['node_id']})",
            "distractor_source": "correct options of batch items matched to other nodes",
        }
    return record


def derive() -> dict:
    nodes = load_chain_nodes()
    items = load_frontend_items()
    batch, rejections = select_batch(items, nodes)

    enriched = {}
    for entry in batch:
        enriched[entry["item"]["source_question_id"]] = _build_enrichment_record(entry, batch)

    items_by_id = {item["id"]: item for item in items}
    for item_id, promotion in MANUAL_REVIEW_PROMOTIONS.items():
        item = items_by_id[item_id]
        if _is_identification_stem(item["text"]) or _is_negative_polarity_stem(item["text"]):
            raise ValueError(f"Unsafe manual promotion: {item_id}")
        ci = item.get("correct_index", 0)
        correct = (item.get("options") or [""])[ci]
        entry = {
            "item": item,
            "match": {
                "node_id": promotion["node_id"],
                "matched_keywords": [],
                "stem_hits": [],
                "correct_option_hits": [correct],
                "score": 0,
            },
        }
        enriched[item["source_question_id"]] = _build_enrichment_record(
            entry,
            batch,
            promotion=promotion,
        )

    fingerprint = hashlib.sha256(
        (
            FRONTEND_BANK.read_text(encoding="utf-8")
            + json.dumps(NODE_ES, sort_keys=True, ensure_ascii=False)
            + json.dumps(MANUAL_REVIEW_PROMOTIONS, sort_keys=True, ensure_ascii=False)
        ).encode()
    ).hexdigest()[:16]

    return {
        "schema_version": "sba_enrichment_v1",
        "phase": "P.6-batch6-manual-review",
        "derivation": {
            "min_keyword_hits": MIN_KEYWORD_HITS,
            "require_stem_hit": REQUIRE_STEM_HIT,
            "require_correct_option_hit": REQUIRE_CORRECT_OPTION_HIT,
            "require_unique_best": REQUIRE_UNIQUE_BEST,
            "word_boundary_matching": True,
            "generic_triggers_banned": sorted(GENERIC_TRIGGERS),
            "identification_stems_excluded": True,
            "manual_review_promotion_count": len(MANUAL_REVIEW_PROMOTIONS),
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
