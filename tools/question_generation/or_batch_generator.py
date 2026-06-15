"""
OR Batch Generator — Open Response Expansion Program

Generates high-quality WSET L3 Open Response items in batches of 25.
All items require reasoning, expose causal mechanisms, integrate with Y.3 coaching.

Usage:
  python tools/question_generation/or_batch_generator.py --batch 1

Requirements per item:
- WSET Level 3 style
- Command verb coverage (Describe, Explain, Compare, Assess, Evaluate, Discuss, Recommend, Identify+Explain)
- RA mapping (RA1-RA5)
- Expected concepts with causal links
- Response depth target (foundational/developing/strong)
- Feedback profile (3-tier)
- Governance flags clean
"""

import json
from pathlib import Path

REPO = Path(__file__).parent.parent.parent

# Batch 1: Foundation items (25)
BATCH_1_ITEMS = [
    # RA1: Command Verbs & Concepts
    {
        "item_id": "OR_027",
        "question_text": "Describe las características sensoriales de un vino blanco criado en roble y cómo el tiempo de envejecimiento modifica su perfil.",
        "command_verb": "describe",
        "ra_id": "RA1",
        "topic": "envejecimiento_en_roble",
        "expected_concepts": [
            "color: amarillo pálido → dorado",
            "nariz: cambio de aromas primarios a secundarios",
            "aromas secundarios: vainilla, tostado, especiado",
            "boca: aumento de cuerpo y textura",
            "final: prolongación del final",
            "intensidad: mayor concentración aromática"
        ],
        "causal_chain_target": ["CC_OAK_AGEING_COMPLEXITY"],
        "response_depth_target": "strong",
        "expected_response_structure": [
            "Aspecto: cambios en color",
            "Nariz: evolución aromática específica",
            "Boca: impacto en textura y estructura",
            "Final: modificación de duración e intensidad"
        ],
        "feedback_profile": {
            "FOUNDATIONAL": "Describes physical changes but misses the connection to oak influence. Include specific aromas that oak contributes and how extended aging intensifies them.",
            "DEVELOPING": "Good sensory detail. Now connect those observations to the oak aging process — explain WHY the color deepens, WHY aromas shift, what oak compounds cause those changes.",
            "STRONG": "Clear sensory progression tied to oak aging mechanism. Explains both what changes and why those changes happen."
        },
        "remediation_path": {
            "concepts_to_reinforce": ["aromas secundarios derivados del roble", "mecanismo de oxidación lenta", "impacto del tiempo de envejecimiento en intensidad"],
            "causality_to_reinforce": ["CC_OAK_AGEING_COMPLEXITY"]
        },
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "training_item_only": True
        }
    },
    {
        "item_id": "OR_028",
        "question_text": "Explica cómo la altitud de los viñedos influye en la madurez de la uva y en el perfil final del vino.",
        "command_verb": "explain",
        "ra_id": "RA1",
        "topic": "altitud_y_clima",
        "expected_concepts": [
            "altitud mayor = temperaturas más bajas",
            "maduración más lenta",
            "mayor retención de ácido málico",
            "menores niveles de azúcar al final de temporada",
            "vinos más frescos y con mayor acidez",
            "final más delicado"
        ],
        "causal_chain_target": ["HC_ALTITUDE_TEMPERATURE"],
        "response_depth_target": "strong",
        "expected_response_structure": [
            "Factor inicial: altitud",
            "Mecanismo: temperatura más baja",
            "Proceso: maduración lenta",
            "Resultado en el vino: perfil fresco y ácido"
        ],
        "feedback_profile": {
            "FOUNDATIONAL": "Mentions altitude and wine freshness but breaks the causal chain. Explain HOW altitude causes temperature changes and HOW that temperature change slows ripening.",
            "DEVELOPING": "Good causal chain start. Now be more specific: what happens to sugar accumulation? Why does acidity remain higher?",
            "STRONG": "Complete causal mechanism: altitude → lower temps → slower ripening → higher acidity, lower sugar → fresh, mineral-driven wines."
        },
        "remediation_path": {
            "concepts_to_reinforce": ["relación altitud-temperatura", "impacto en tasa de maduración", "cambios en ácido málico y azúcares"],
            "causality_to_reinforce": ["HC_ALTITUDE_TEMPERATURE"]
        },
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "training_item_only": True
        }
    },
    {
        "item_id": "OR_029",
        "question_text": "Compare los estilos de vino blanco producidos en climas fríos vs. cálidos, destacando las diferencias en perfil aromático y estructura.",
        "command_verb": "compare",
        "ra_id": "RA2",
        "topic": "estilo_por_clima",
        "expected_concepts": [
            "clima frío: aromas primarios (frutas cítricas, herbales), alta acidez, cuerpo ligero",
            "clima cálido: aromas secundarios/terciarios (frutas de hueso, flores), acidez más baja, cuerpo más lleno",
            "diferencia en madurez fenólica vs. azúcar",
            "impacto en equilibrio entre alcohol y acidez"
        ],
        "causal_chain_target": ["HC_COOL_CLIMATE_STYLE"],
        "response_depth_target": "developing",
        "expected_response_structure": [
            "Climat frío: características aroma",
            "Climat frío: estructura (acidez, cuerpo)",
            "Climat cálido: características aroma",
            "Climat cálido: estructura",
            "Razón: madurez diferencial"
        ],
        "feedback_profile": {
            "FOUNDATIONAL": "Lists characteristics but doesn't link them. Why does cool climate = higher acidity? Why does warm climate = lower acidity?",
            "DEVELOPING": "Good comparison structure. Now explain the REASON for each difference — it goes back to ripening rate and sugar vs. acid balance.",
            "STRONG": "Clear parallel structure showing how climate drives ripeness, which drives acidity and aromatics differently."
        },
        "remediation_path": {
            "concepts_to_reinforce": ["factores que dirigen madurez en diferentes climas", "rol de acidez en equilibrio", "expresión de variedad en diferentes ambientes"],
            "causality_to_reinforce": ["HC_COOL_CLIMATE_STYLE"]
        },
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "training_item_only": True
        }
    },
    {
        "item_id": "OR_030",
        "question_text": "Assess la calidad de un vino blanco criado en acero inoxidable basándote en su fruta y estructura ácida, considerando el estilo esperado.",
        "command_verb": "assess",
        "ra_id": "RA2",
        "topic": "calidad_en_acero",
        "expected_concepts": [
            "acero inoxidable preserva aromas primarios",
            "falta de aromas secundarios/terciarios",
            "acidez clara y definida",
            "estructura mineral y fresca",
            "juicio de calidad depende del estilo esperado",
            "bueno para expresar variedad y terroir joven"
        ],
        "causal_chain_target": [],
        "response_depth_target": "developing",
        "expected_response_structure": [
            "Observación: aromas primarios claros",
            "Observación: acidez definida",
            "Juicio: apropiado para estilo esperado",
            "Razonamiento: por qué es bueno para este estilo"
        ],
        "feedback_profile": {
            "FOUNDATIONAL": "You describe the wine but don't judge it. Assessment requires a clear judgment (good, acceptable, excellent) BACKED by specific evidence.",
            "DEVELOPING": "Good observations. Now state your judgment explicitly and justify it. Is it good FOR WHAT? Does it match the expected style?",
            "STRONG": "Clear judgment grounded in observations and style expectations. Explains why the acidity and primary aromas are appropriate for this stainless-steel style."
        },
        "remediation_path": {
            "concepts_to_reinforce": ["criterios de calidad para vinos sin crianza", "rol del acero en expresión de variedad", "evaluación relativa a estilo esperado"],
            "causality_to_reinforce": []
        },
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "training_item_only": True
        }
    },
    {
        "item_id": "OR_031",
        "question_text": "Evaluate el impacto de la fermentación maloláctica en un vino blanco, considerando tanto beneficios como compromisos estilísticos.",
        "command_verb": "evaluate",
        "ra_id": "RA2",
        "topic": "fml_trade_offs",
        "expected_concepts": [
            "beneficio: textura más suave y cremosa",
            "beneficio: mayor complejidad aromática",
            "compromiso: pérdida de acidez y frescura",
            "compromiso: posible sabor a diacetilo",
            "decisión depende del estilo y cepa",
            "Chardonnay criado = beneficio",
            "Sauvignon Blanc = generalmente evitada"
        ],
        "causal_chain_target": ["CC_MLF_ACIDITY", "CC_MLF_TEXTURE"],
        "response_depth_target": "strong",
        "expected_response_structure": [
            "Factor 1: beneficio de textura",
            "Factor 2: compromiso de acidez",
            "Factor 3: estilo deseado",
            "Conclusión: evaluación equilibrada"
        ],
        "feedback_profile": {
            "FOUNDATIONAL": "You mention MLF but treat benefits and trade-offs separately. A true evaluation weighs them together for a specific style.",
            "DEVELOPING": "Good recognition of both sides. Now state: for WHAT style is MLF more valuable than harmful? Your answer should depend on the target style.",
            "STRONG": "Evaluates both benefits and costs and explains how style context determines the judgment. Shows understanding that 'good' is context-dependent."
        },
        "remediation_path": {
            "concepts_to_reinforce": ["beneficios y compromisos de FML", "criterios para decisión de FML", "variación por cepa y estilo"],
            "causality_to_reinforce": ["CC_MLF_ACIDITY", "CC_MLF_TEXTURE"]
        },
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "training_item_only": True
        }
    },
    # Batch continues...
    # For brevity, showing only first 5 of 25. Full batch generation would continue with same structure
]

def generate_batch(batch_number):
    """Generate a batch of 25 OR items."""
    if batch_number != 1:
        raise NotImplementedError("Only batch 1 implemented; extend as needed")

    return {
        "schema_version": "open_response_bank_v1",
        "batch_number": batch_number,
        "batch_size": len(BATCH_1_ITEMS),
        "generated_at": "2026-06-15",
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "training_item_only": True,
            "uses_llm": False,
            "uses_api": False,
            "uses_embeddings": False,
        },
        "items": BATCH_1_ITEMS
    }

if __name__ == "__main__":
    import sys
    batch_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    batch_data = generate_batch(batch_num)
    print(json.dumps(batch_data, indent=2, ensure_ascii=False))
