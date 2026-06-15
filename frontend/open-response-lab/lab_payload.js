window.OPEN_RESPONSE_LAB_PAYLOAD = {
  "lab_contract": "private_open_response_lab_runtime_mvp",
  "activation_status": "active_private_lab",
  "pool_size": 148,
  "storage_key": "wset_open_response_lab_private_v1",
  "session_options": {
    "short_practice": 1,
    "standard_practice": 2,
    "extended_practice": 4,
    "mock_theory_2": 4
  },
  "sessions": {
    "short_practice": {
      "session_size": 1,
      "item_ids": [
        "OR_117"
      ],
      "source_question_ids": [
        "OR_117"
      ]
    },
    "standard_practice": {
      "session_size": 2,
      "item_ids": [
        "OR_117",
        "OR_118"
      ],
      "source_question_ids": [
        "OR_117",
        "OR_118"
      ]
    },
    "extended_practice": {
      "session_size": 4,
      "item_ids": [
        "OR_117",
        "OR_118",
        "OR_119",
        "OR_120"
      ],
      "source_question_ids": [
        "OR_117",
        "OR_118",
        "OR_119",
        "OR_120"
      ]
    },
    "mock_theory_2": {
      "session_size": 4,
      "item_ids": [
        "OR_117",
        "OR_118",
        "OR_119",
        "OR_125"
      ],
      "source_question_ids": [
        "OR_117",
        "OR_118",
        "OR_119",
        "OR_125"
      ]
    }
  },
  "items": [
    {
      "item_id": "OR_001",
      "source_question_id": "OR_001",
      "stem": "Explique cómo prácticas sostenibles certificadas u orgánicas pueden aumentar los costes de producción y contribuir a la diferenciación comercial del vino.",
      "topic": "sostenibilidad",
      "RA": "RA1",
      "command_verb": "how",
      "expected_concepts": [
        "certificación orgánica o sostenible",
        "aumento de costes de producción",
        "mano de obra intensiva",
        "rendimientos más bajos",
        "diferenciación en el mercado",
        "valor percibido por el consumidor",
        "precio premium"
      ],
      "evaluation_config": {
        "verb_definition_key": "how",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "certificación orgánica o sostenible",
          "aumento de costes de producción",
          "mano de obra intensiva",
          "rendimientos más bajos",
          "diferenciación en el mercado",
          "valor percibido por el consumidor",
          "precio premium"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_002",
      "source_question_id": "OR_002",
      "stem": "Justifica el uso de la fermentación maloláctica en la producción de ciertos estilos de vino blanco y cómo contribuye al estilo y la calidad.",
      "topic": "fermentación maloláctica",
      "RA": "RA1",
      "command_verb": "justify",
      "expected_concepts": [
        "conversión de ácido málico a ácido láctico",
        "reducción de la acidez total",
        "perfil de acidez más suave",
        "mayor textura y cuerpo",
        "notas cremosas o mantecosas (diacetilo)",
        "adecuación para estilos con crianza en roble",
        "inapropiada para estilos frescos y aromáticos"
      ],
      "evaluation_config": {
        "verb_definition_key": "justify",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "conversión de ácido málico a ácido láctico",
          "reducción de la acidez total",
          "perfil de acidez más suave",
          "mayor textura y cuerpo",
          "notas cremosas o mantecosas (diacetilo)",
          "adecuación para estilos con crianza en roble",
          "inapropiada para estilos frescos y aromáticos"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_003",
      "source_question_id": "OR_003",
      "stem": "Explica cómo la altitud puede influir en el estilo de un vino tinto.",
      "topic": "altitud",
      "RA": "RA1",
      "command_verb": "how",
      "expected_concepts": [
        "temperaturas más bajas a mayor altitud",
        "maduración más lenta",
        "mayor retención de acidez",
        "menor contenido alcohólico",
        "aromas más frescos y primarios",
        "mayor variación diurna de temperatura"
      ],
      "evaluation_config": {
        "verb_definition_key": "how",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "temperaturas más bajas a mayor altitud",
          "maduración más lenta",
          "mayor retención de acidez",
          "menor contenido alcohólico",
          "aromas más frescos y primarios",
          "mayor variación diurna de temperatura"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_004",
      "source_question_id": "OR_004",
      "stem": "Explique cómo la orientación y la pendiente del viñedo pueden afectar la maduración de la uva.",
      "topic": "orientación y pendiente",
      "RA": "RA1",
      "command_verb": "how",
      "expected_concepts": [
        "orientación sur (hemisferio norte) maximiza exposición solar",
        "mayor ángulo de incidencia de la luz",
        "mayor acumulación de calor en la uva",
        "pendiente favorece el drenaje",
        "pendiente reduce el riesgo de heladas (aire frío drena)",
        "efecto sobre ritmo de maduración"
      ],
      "evaluation_config": {
        "verb_definition_key": "how",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "orientación sur (hemisferio norte) maximiza exposición solar",
          "mayor ángulo de incidencia de la luz",
          "mayor acumulación de calor en la uva",
          "pendiente favorece el drenaje",
          "pendiente reduce el riesgo de heladas (aire frío drena)",
          "efecto sobre ritmo de maduración"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_005",
      "source_question_id": "OR_005",
      "stem": "Describa cómo las prácticas de manejo en la bodega pueden reducir el riesgo de oxidación en vinos blancos.",
      "topic": "oxidación en bodega",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "uso de sulfitos (SO₂) como antioxidante",
        "protección con gas inerte (nitrógeno, CO₂ argón)",
        "control de temperatura en fermentación y almacenamiento",
        "uso de depósitos de acero inoxidable",
        "manipulación cuidadosa para evitar contacto con oxígeno",
        "llenado completo de depósitos"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "uso de sulfitos (SO₂) como antioxidante",
          "protección con gas inerte (nitrógeno, CO₂ argón)",
          "control de temperatura en fermentación y almacenamiento",
          "uso de depósitos de acero inoxidable",
          "manipulación cuidadosa para evitar contacto con oxígeno",
          "llenado completo de depósitos"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_006",
      "source_question_id": "OR_006",
      "stem": "Explique la influencia de la elección de levaduras en el perfil sensorial del vino.",
      "topic": "levaduras y perfil sensorial",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "levaduras producen compuestos aromáticos secundarios",
        "ésteres y alcoholes superiores según cepa",
        "producción de diacetilo en algunas cepas",
        "levaduras neutras vs levaduras aromáticas",
        "efecto sobre intensidad y complejidad aromática",
        "influencia sobre carácter frutal o floral"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "levaduras producen compuestos aromáticos secundarios",
          "ésteres y alcoholes superiores según cepa",
          "producción de diacetilo en algunas cepas",
          "levaduras neutras vs levaduras aromáticas",
          "efecto sobre intensidad y complejidad aromática",
          "influencia sobre carácter frutal o floral"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_007",
      "source_question_id": "OR_007",
      "stem": "Explique cómo el drenaje del suelo puede influir en el vigor de la vid y en el estilo del vino.",
      "topic": "drenaje de suelo y vigor",
      "RA": "RA1",
      "command_verb": "how",
      "expected_concepts": [
        "buen drenaje restringe disponibilidad de agua",
        "estrés hídrico moderado reduce vigor vegetativo",
        "menor vigor concentra energía en el fruto",
        "bayas más pequeñas y concentradas",
        "vinos con mayor concentración de compuestos",
        "suelos con mal drenaje favorecen vigor excesivo"
      ],
      "evaluation_config": {
        "verb_definition_key": "how",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "buen drenaje restringe disponibilidad de agua",
          "estrés hídrico moderado reduce vigor vegetativo",
          "menor vigor concentra energía en el fruto",
          "bayas más pequeñas y concentradas",
          "vinos con mayor concentración de compuestos",
          "suelos con mal drenaje favorecen vigor excesivo"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_008",
      "source_question_id": "OR_008",
      "stem": "Compare cómo la elección de roble americano o francés puede afectar los aromas, el tanino y la integración del roble en el vino.",
      "topic": "roble americano vs francés",
      "RA": "RA1",
      "command_verb": "compare",
      "expected_concepts": [
        "roble americano: grano más abierto, mayor extracción de aromas",
        "roble americano: notas de coco, vainilla, eneldo más pronunciadas",
        "roble francés: grano más fino, extracción más sutil",
        "roble francés: notas especiadas y tostadas más elegantes",
        "tanino de roble americano más duro inicialmente",
        "micro-oxigenación diferente según porosidad del grano",
        "integración más rápida del roble americano en algunos estilos"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "roble americano: grano más abierto, mayor extracción de aromas",
          "roble americano: notas de coco, vainilla, eneldo más pronunciadas",
          "roble francés: grano más fino, extracción más sutil",
          "roble francés: notas especiadas y tostadas más elegantes",
          "tanino de roble americano más duro inicialmente",
          "micro-oxigenación diferente según porosidad del grano",
          "integración más rápida del roble americano en algunos estilos"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_009",
      "source_question_id": "OR_009",
      "stem": "Describa dos técnicas de manejo del dosel (canopy management) y sus beneficios.",
      "topic": "manejo del dosel",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "deshojar (leaf removal): mayor exposición solar y aireación de racimos",
        "deshojado reduce humedad y riesgo de enfermedades fúngicas",
        "poda en verde (green harvest): reducción de carga de fruta",
        "poda en verde concentra compuestos en las bayas restantes",
        "levantamiento de pámpanos (shoot positioning)",
        "mejora de madurez y sanidad de la uva"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "deshojar (leaf removal): mayor exposición solar y aireación de racimos",
          "deshojado reduce humedad y riesgo de enfermedades fúngicas",
          "poda en verde (green harvest): reducción de carga de fruta",
          "poda en verde concentra compuestos en las bayas restantes",
          "levantamiento de pámpanos (shoot positioning)",
          "mejora de madurez y sanidad de la uva"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_010",
      "source_question_id": "OR_010",
      "stem": "Explique cómo el riego y el manejo del dosel pueden reducir los efectos de la sequía o del calor extremo sobre la maduración.",
      "topic": "riego y dosel ante estrés climático",
      "RA": "RA1",
      "command_verb": "how",
      "expected_concepts": [
        "riego de precisión evita estrés hídrico excesivo",
        "mantenimiento de la función fotosintética en calor extremo",
        "deshojado en la cara este reduce exposición al calor de la tarde",
        "dosel proporciona sombra que modera la temperatura del racimo",
        "balance entre madurez y preservación de acidez",
        "riego excesivo puede causar vigor y dilución"
      ],
      "evaluation_config": {
        "verb_definition_key": "how",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "riego de precisión evita estrés hídrico excesivo",
          "mantenimiento de la función fotosintética en calor extremo",
          "deshojado en la cara este reduce exposición al calor de la tarde",
          "dosel proporciona sombra que modera la temperatura del racimo",
          "balance entre madurez y preservación de acidez",
          "riego excesivo puede causar vigor y dilución"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_011",
      "source_question_id": "OR_011",
      "stem": "Explica por qué la densidad de plantación es un factor clave en la gestión del viñedo y cómo afecta el estilo y costo de producción.",
      "topic": "densidad de plantación",
      "RA": "RA1",
      "command_verb": "why",
      "expected_concepts": [
        "alta densidad: competencia por agua y nutrientes entre vides",
        "competencia induce estrés hídrico moderado y mayor concentración",
        "raíces más profundas en alta densidad",
        "alta densidad aumenta costo (más plantas, más labores)",
        "baja densidad: mecanización más fácil, menor costo",
        "relación densidad–rendimiento–concentración–precio del vino"
      ],
      "evaluation_config": {
        "verb_definition_key": "why",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "alta densidad: competencia por agua y nutrientes entre vides",
          "competencia induce estrés hídrico moderado y mayor concentración",
          "raíces más profundas en alta densidad",
          "alta densidad aumenta costo (más plantas, más labores)",
          "baja densidad: mecanización más fácil, menor costo",
          "relación densidad–rendimiento–concentración–precio del vino"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_012",
      "source_question_id": "OR_012",
      "stem": "Compare el uso de levaduras seleccionadas y levaduras autóctonas en fermentación, considerando control, consistencia, complejidad y riesgo.",
      "topic": "levaduras seleccionadas vs autóctonas",
      "RA": "RA1",
      "command_verb": "compare",
      "expected_concepts": [
        "levaduras seleccionadas: mayor control y consistencia de resultado",
        "levaduras seleccionadas: perfil aromático predecible",
        "levaduras autóctonas: mayor complejidad y carácter de terroir",
        "levaduras autóctonas: mayor riesgo de fermentación atascada",
        "levaduras autóctonas: producción de compuestos no deseados",
        "elección condicionada por el estilo objetivo del viticultor"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "levaduras seleccionadas: mayor control y consistencia de resultado",
          "levaduras seleccionadas: perfil aromático predecible",
          "levaduras autóctonas: mayor complejidad y carácter de terroir",
          "levaduras autóctonas: mayor riesgo de fermentación atascada",
          "levaduras autóctonas: producción de compuestos no deseados",
          "elección condicionada por el estilo objetivo del viticultor"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_013",
      "source_question_id": "OR_013",
      "stem": "Analice cómo el estrés hídrico moderado puede reducir el rendimiento, concentrar las bayas e influir potencialmente en el precio del vino.",
      "topic": "estrés hídrico y precio",
      "RA": "RA1",
      "command_verb": "evaluate",
      "expected_concepts": [
        "estrés hídrico moderado reduce tamaño de bayas",
        "mayor proporción de piel respecto al volumen total",
        "concentración de compuestos (color, tanino, azúcar)",
        "menor rendimiento por hectárea",
        "menor rendimiento aumenta coste de producción",
        "mayor concentración puede justificar precio más alto",
        "límite: estrés severo daña la vid y reduce calidad"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "estrés hídrico moderado reduce tamaño de bayas",
          "mayor proporción de piel respecto al volumen total",
          "concentración de compuestos (color, tanino, azúcar)",
          "menor rendimiento por hectárea",
          "menor rendimiento aumenta coste de producción",
          "mayor concentración puede justificar precio más alto",
          "límite: estrés severo daña la vid y reduce calidad"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_014",
      "source_question_id": "OR_014",
      "stem": "Describe cómo la latitud y la altitud interactúan para influir en el estilo del vino en una región de clima cálido.",
      "topic": "latitud y altitud en clima cálido",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "latitud baja: mayor irradiación solar y temperaturas cálidas",
        "altitud compensa el calor mediante temperaturas más bajas",
        "variación diurna de temperatura en viñedos de altitud",
        "retención de acidez a mayor altitud",
        "menor acumulación de azúcar y menor alcohol potencial",
        "aromas más frescos en vinos de altitud en clima cálido"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "latitud baja: mayor irradiación solar y temperaturas cálidas",
          "altitud compensa el calor mediante temperaturas más bajas",
          "variación diurna de temperatura en viñedos de altitud",
          "retención de acidez a mayor altitud",
          "menor acumulación de azúcar y menor alcohol potencial",
          "aromas más frescos en vinos de altitud en clima cálido"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_015",
      "source_question_id": "OR_015",
      "stem": "Explique cómo un estrés hídrico moderado, si no es excesivo, puede influir en el vigor de la vid, el tamaño de las bayas y la concentración de compuestos.",
      "topic": "estrés hídrico moderado y concentración",
      "RA": "RA1",
      "command_verb": "how",
      "expected_concepts": [
        "estrés hídrico moderado reduce crecimiento vegetativo",
        "menor vigor concentra energía en el fruto",
        "bayas más pequeñas con menor contenido de agua",
        "mayor relación piel/pulpa",
        "mayor concentración de antocianos, taninos y azúcares",
        "distinción entre estrés moderado (beneficioso) y severo (dañino)"
      ],
      "evaluation_config": {
        "verb_definition_key": "how",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "estrés hídrico moderado reduce crecimiento vegetativo",
          "menor vigor concentra energía en el fruto",
          "bayas más pequeñas con menor contenido de agua",
          "mayor relación piel/pulpa",
          "mayor concentración de antocianos, taninos y azúcares",
          "distinción entre estrés moderado (beneficioso) y severo (dañino)"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_016",
      "source_question_id": "OR_016",
      "stem": "Menciona un riesgo enológico del uso de levaduras autóctonas.",
      "topic": "riesgos de levaduras autóctonas",
      "RA": "RA1",
      "command_verb": "state",
      "expected_concepts": [
        "fermentación atascada (stuck fermentation)",
        "producción de compuestos no deseados (ácido acético, etil acetato)",
        "inconsistencia entre cosechas",
        "menor tolerancia al alcohol de algunas cepas autóctonas"
      ],
      "evaluation_config": {
        "verb_definition_key": "state",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "fermentación atascada (stuck fermentation)",
          "producción de compuestos no deseados (ácido acético, etil acetato)",
          "inconsistencia entre cosechas",
          "menor tolerancia al alcohol de algunas cepas autóctonas"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_017",
      "source_question_id": "OR_017",
      "stem": "Justifica por qué un viticultor utilizaría poda en invierno.",
      "topic": "poda de invierno",
      "RA": "RA1",
      "command_verb": "justify",
      "expected_concepts": [
        "control del rendimiento de la vid",
        "gestión del vigor vegetativo",
        "determinación del número de yemas productivas",
        "equilibrio entre producción y calidad",
        "eliminación de madera vieja o enferma",
        "preparación de la estructura de la vid para la temporada"
      ],
      "evaluation_config": {
        "verb_definition_key": "justify",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "control del rendimiento de la vid",
          "gestión del vigor vegetativo",
          "determinación del número de yemas productivas",
          "equilibrio entre producción y calidad",
          "eliminación de madera vieja o enferma",
          "preparación de la estructura de la vid para la temporada"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_018",
      "source_question_id": "OR_018",
      "stem": "Describe un beneficio técnico de la fermentación en acero inoxidable.",
      "topic": "fermentación en acero inoxidable",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "control preciso de temperatura",
        "fermentación a temperatura baja preserva aromas primarios",
        "material neutro: no añade aromas al vino",
        "facilidad de limpieza y control de higiene",
        "preservación de la frescura y el carácter frutal"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "control preciso de temperatura",
          "fermentación a temperatura baja preserva aromas primarios",
          "material neutro: no añade aromas al vino",
          "facilidad de limpieza y control de higiene",
          "preservación de la frescura y el carácter frutal"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_019",
      "source_question_id": "OR_019",
      "stem": "Analiza los efectos de la maceración prolongada en la vinificación de vinos tintos desde el punto de vista del estilo y la calidad.",
      "topic": "maceración prolongada",
      "RA": "RA1",
      "command_verb": "evaluate",
      "expected_concepts": [
        "mayor extracción de antocianos (color)",
        "mayor extracción de taninos de pepitas y hollejo",
        "taninos pueden volverse más duros si la extracción es excesiva",
        "mayor estructura y potencial de envejecimiento",
        "riesgo de amargor o astringencia excesiva",
        "adecuación para estilos de guarda, no para vinos de consumo temprano"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "mayor extracción de antocianos (color)",
          "mayor extracción de taninos de pepitas y hollejo",
          "taninos pueden volverse más duros si la extracción es excesiva",
          "mayor estructura y potencial de envejecimiento",
          "riesgo de amargor o astringencia excesiva",
          "adecuación para estilos de guarda, no para vinos de consumo temprano"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_020",
      "source_question_id": "OR_020",
      "stem": "Compare cómo suelos arenosos y arcillosos pueden afectar la disponibilidad de agua, el vigor de la vid y el estilo del vino.",
      "topic": "suelos arenosos vs arcillosos",
      "RA": "RA1",
      "command_verb": "compare",
      "expected_concepts": [
        "suelo arenoso: buen drenaje, baja retención de agua",
        "suelo arenoso: estrés hídrico moderado, bayas concentradas",
        "suelo arcilloso: alta retención de agua",
        "suelo arcilloso: mayor disponibilidad hídrica, mayor vigor potencial",
        "mayor vigor puede diluir compuestos y reducir concentración",
        "suelo arenoso: barrera contra Phylloxera (histórico)"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "suelo arenoso: buen drenaje, baja retención de agua",
          "suelo arenoso: estrés hídrico moderado, bayas concentradas",
          "suelo arcilloso: alta retención de agua",
          "suelo arcilloso: mayor disponibilidad hídrica, mayor vigor potencial",
          "mayor vigor puede diluir compuestos y reducir concentración",
          "suelo arenoso: barrera contra Phylloxera (histórico)"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_021",
      "source_question_id": "OR_021",
      "stem": "Identifica la región vinícola australiana reconocida por producir Shiraz especiado y de gran concentración.",
      "topic": "regiones_mundiales",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "Barossa Valley",
        "Shiraz/Syrah",
        "clima cálido",
        "gran concentración",
        "notas especiadas y de fruta madura"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "Barossa Valley",
          "Shiraz/Syrah",
          "clima cálido",
          "gran concentración",
          "notas especiadas y de fruta madura"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_022",
      "source_question_id": "OR_022",
      "stem": "Describe el sistema de clasificación por crus en viticultura y menciona una región donde se aplica.",
      "topic": "regiones_mundiales",
      "RA": "RA2",
      "command_verb": "describe",
      "expected_concepts": [
        "crus como viñedos clasificados",
        "clasificación por calidad del terroir",
        "Borgoña",
        "Premier Cru / Grand Cru"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "crus como viñedos clasificados",
          "clasificación por calidad del terroir",
          "Borgoña",
          "Premier Cru / Grand Cru"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_023",
      "source_question_id": "OR_023",
      "stem": "Explica qué significa la categoría 'Gran Reserva' en los vinos tintos españoles y menciona una región que la regule.",
      "topic": "regiones_mundiales",
      "RA": "RA2",
      "command_verb": "explain",
      "expected_concepts": [
        "Gran Reserva como categoría de crianza prolongada",
        "mínimo 5 años totales",
        "al menos 18 meses en barrica",
        "Ribera del Duero o Rioja"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "Gran Reserva como categoría de crianza prolongada",
          "mínimo 5 años totales",
          "al menos 18 meses en barrica",
          "Ribera del Duero o Rioja"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_024",
      "source_question_id": "OR_024",
      "stem": "Identifica una categoría de vino tinto español que exige un mínimo de 3 años de crianza total y explica brevemente sus requisitos.",
      "topic": "regiones_mundiales",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "Rioja Reserva",
        "mínimo 3 años de crianza total",
        "al menos 1 año en barrica de roble",
        "combinación de crianza en madera y botella"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "Rioja Reserva",
          "mínimo 3 años de crianza total",
          "al menos 1 año en barrica de roble",
          "combinación de crianza en madera y botella"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_025",
      "source_question_id": "OR_025",
      "stem": "Identifica una región vinícola con clima mediterráneo de influencia marítima y explica cómo este clima afecta al estilo de sus vinos.",
      "topic": "regiones_mundiales",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "Stellenbosch",
        "clima mediterráneo",
        "influencia marítima de la Corriente de Benguela",
        "veranos cálidos moderados",
        "vinos con buena estructura y acidez"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "Stellenbosch",
          "clima mediterráneo",
          "influencia marítima de la Corriente de Benguela",
          "veranos cálidos moderados",
          "vinos con buena estructura y acidez"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_026",
      "source_question_id": "OR_026",
      "stem": "Nombra dos regiones italianas conocidas por producir vinos elaborados con Nebbiolo.",
      "topic": "regiones_mundiales",
      "RA": "RA2",
      "command_verb": "list",
      "expected_concepts": [
        "Barolo",
        "Barbaresco",
        "Piemonte",
        "Nebbiolo como variedad de alta acidez y taninos firmes"
      ],
      "evaluation_config": {
        "verb_definition_key": "list",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "Barolo",
          "Barbaresco",
          "Piemonte",
          "Nebbiolo como variedad de alta acidez y taninos firmes"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_027",
      "source_question_id": "OR_027",
      "stem": "Identifica dos regiones conocidas por su Sauvignon Blanc y describe brevemente el estilo característico de cada una.",
      "topic": "regiones_mundiales",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "Marlborough (Nueva Zelanda) — aromas intensos de maracuyá y hierba, alta acidez",
        "Loire (Sancerre/Pouilly-Fumé) — estilo más mineral y herbáceo, acidez viva"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "Marlborough (Nueva Zelanda) — aromas intensos de maracuyá y hierba, alta acidez",
          "Loire (Sancerre/Pouilly-Fumé) — estilo más mineral y herbáceo, acidez viva"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_028",
      "source_question_id": "OR_028",
      "stem": "Explica qué es el despalillado y por qué se realiza durante la vinificación de vinos tintos.",
      "topic": "vinificacion_tinto",
      "RA": "RA1",
      "command_verb": "why",
      "expected_concepts": [
        "separación de bayas del raspón",
        "eliminar los tallos verdes",
        "reducir taninos vegetales",
        "mejorar la calidad de los taninos"
      ],
      "evaluation_config": {
        "verb_definition_key": "why",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "separación de bayas del raspón",
          "eliminar los tallos verdes",
          "reducir taninos vegetales",
          "mejorar la calidad de los taninos"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_029",
      "source_question_id": "OR_029",
      "stem": "Identifica una región vinícola conocida por sus suelos volcánicos y explica cómo pueden influir en el estilo del vino.",
      "topic": "regiones_mundiales",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "Etna (Sicilia)",
        "suelos volcánicos basálticos",
        "mineralidad",
        "buen drenaje",
        "acidez elevada"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "Etna (Sicilia)",
          "suelos volcánicos basálticos",
          "mineralidad",
          "buen drenaje",
          "acidez elevada"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_030",
      "source_question_id": "OR_030",
      "stem": "Identifica la región argentina conocida por sus viñedos de mayor altitud y describe las condiciones climáticas que los caracterizan.",
      "topic": "regiones_mundiales",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "Salta (Cafayate)",
        "viñedos a gran altitud",
        "alta amplitud térmica",
        "radiación UV intensa",
        "acidez preservada por temperaturas nocturnas frescas"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "foundational"
        },
        "required_signals": [
          "Salta (Cafayate)",
          "viñedos a gran altitud",
          "alta amplitud térmica",
          "radiación UV intensa",
          "acidez preservada por temperaturas nocturnas frescas"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_031",
      "source_question_id": "OR_031",
      "stem": "Nombra dos regiones reconocidas por elaborar vinos afectados por podredumbre noble (Botrytis cinerea) y explica brevemente el proceso.",
      "topic": "vinificacion_dulces",
      "RA": "RA2",
      "command_verb": "list",
      "expected_concepts": [
        "Sauternes (Francia)",
        "Tokaj (Hungría)",
        "condiciones de humedad alternada con periodos secos",
        "concentración de azúcares y aromas",
        "podredumbre noble"
      ],
      "evaluation_config": {
        "verb_definition_key": "list",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "Sauternes (Francia)",
          "Tokaj (Hungría)",
          "condiciones de humedad alternada con periodos secos",
          "concentración de azúcares y aromas",
          "podredumbre noble"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_032",
      "source_question_id": "OR_032",
      "stem": "Describe las características sensoriales de un vino blanco criado en roble y cómo el tiempo de envejecimiento modifica su perfil.",
      "topic": "oak_ageing_sensory",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "color evolution",
        "secondary aromas",
        "vanillin and toasted notes",
        "texture increase",
        "finish prolongation"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "color evolution",
          "secondary aromas",
          "vanillin and toasted notes",
          "texture increase",
          "finish prolongation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_033",
      "source_question_id": "OR_033",
      "stem": "Explica cómo la altitud de los viñedos influye en la madurez de la uva y en el perfil final del vino.",
      "topic": "altitude_ripeness",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "temperature decrease",
        "slower ripening",
        "malic acid retention",
        "sugar accumulation delay",
        "fresh profile result"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "temperature decrease",
          "slower ripening",
          "malic acid retention",
          "sugar accumulation delay",
          "fresh profile result"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_034",
      "source_question_id": "OR_034",
      "stem": "Compare los estilos de vino blanco producidos en climas fríos vs. cálidos, destacando las diferencias en perfil aromático y estructura.",
      "topic": "climate_style_differences",
      "RA": "RA2",
      "command_verb": "compare",
      "expected_concepts": [
        "cool climate: primary aromas",
        "cool climate: higher acidity",
        "warm climate: secondary/tertiary aromas",
        "warm climate: lower acidity",
        "ripeness differential"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "cool climate: primary aromas",
          "cool climate: higher acidity",
          "warm climate: secondary/tertiary aromas",
          "warm climate: lower acidity",
          "ripeness differential"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_035",
      "source_question_id": "OR_035",
      "stem": "Assess la calidad de un vino blanco criado en acero inoxidable basándote en su fruta y estructura ácida, considerando el estilo esperado.",
      "topic": "stainless_steel_quality",
      "RA": "RA2",
      "command_verb": "assess",
      "expected_concepts": [
        "primary aromas preserved",
        "clear acidity",
        "mineral structure",
        "style-dependent judgment",
        "variety expression"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "primary aromas preserved",
          "clear acidity",
          "mineral structure",
          "style-dependent judgment",
          "variety expression"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_036",
      "source_question_id": "OR_036",
      "stem": "Evaluate el impacto de la fermentación maloláctica en un vino blanco, considerando tanto beneficios como compromisos estilísticos.",
      "topic": "mlf_tradeoffs",
      "RA": "RA2",
      "command_verb": "evaluate",
      "expected_concepts": [
        "texture softening",
        "aromatic complexity",
        "acidity loss",
        "freshness compromise",
        "diacetyl risk",
        "style-dependent value"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "texture softening",
          "aromatic complexity",
          "acidity loss",
          "freshness compromise",
          "diacetyl risk",
          "style-dependent value"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_037",
      "source_question_id": "OR_037",
      "stem": "Discuss la sostenibilidad en la viticultura moderna y cómo las prácticas certificadas impactan tanto el coste como la percepción del consumidor.",
      "topic": "sustainability_economics",
      "RA": "RA1",
      "command_verb": "discuss",
      "expected_concepts": [
        "certification types",
        "production cost increase",
        "premium pricing",
        "consumer perception",
        "market positioning",
        "labor intensity"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "certification types",
          "production cost increase",
          "premium pricing",
          "consumer perception",
          "market positioning",
          "labor intensity"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_038",
      "source_question_id": "OR_038",
      "stem": "Recommend un enfoque de vinificación para un Riesling seco de clima frío que busca máxima expresión de terroir.",
      "topic": "riesling_dry_vinification",
      "RA": "RA3",
      "command_verb": "recommend",
      "expected_concepts": [
        "temperature control during fermentation",
        "stainless steel fermentation",
        "prevent MLF",
        "minimal oak",
        "early bottling",
        "preserve acidity"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "temperature control during fermentation",
          "stainless steel fermentation",
          "prevent MLF",
          "minimal oak",
          "early bottling",
          "preserve acidity"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_039",
      "source_question_id": "OR_039",
      "stem": "Identify and explain los factores que hacen que la Borgoña sea una región de vinos finos, conectando terroir con estilo.",
      "topic": "burgundy_terroir_style",
      "RA": "RA3",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "continental climate",
        "limestone-rich soils",
        "cool growing season",
        "low yields",
        "Pinot Noir/Chardonnay varieties",
        "regional regulations",
        "expression of place"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "continental climate",
          "limestone-rich soils",
          "cool growing season",
          "low yields",
          "Pinot Noir/Chardonnay varieties",
          "regional regulations",
          "expression of place"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_040",
      "source_question_id": "OR_040",
      "stem": "Describe los cambios en color, aroma y estructura que ocurren cuando un vino tinto joven se expone al aire después de descorchar.",
      "topic": "red_wine_oxidation_sensory",
      "RA": "RA3",
      "command_verb": "describe",
      "expected_concepts": [
        "color brightening",
        "tannin softening",
        "aroma opening",
        "fruit expression increase",
        "alcohol perception change",
        "structural integration"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "color brightening",
          "tannin softening",
          "aroma opening",
          "fruit expression increase",
          "alcohol perception change",
          "structural integration"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_041",
      "source_question_id": "OR_041",
      "stem": "Explica por qué algunos viñedos de Cabernet Sauvignon en Burdeos alcanzan mayor concentración tanínica que otros en el mismo viñedo.",
      "topic": "tannin_concentration_variation",
      "RA": "RA4",
      "command_verb": "explain",
      "expected_concepts": [
        "berry size variation",
        "skin-to-juice ratio",
        "ripeness level",
        "exposition differences",
        "soil drainage variation",
        "terroir micro-variation"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "berry size variation",
          "skin-to-juice ratio",
          "ripeness level",
          "exposition differences",
          "soil drainage variation",
          "terroir micro-variation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_042",
      "source_question_id": "OR_042",
      "stem": "Compare el potencial de envejecimiento entre un Barolo de uvas de viña vieja vs. viña joven, explicando las razones.",
      "topic": "vineyard_age_aging_potential",
      "RA": "RA4",
      "command_verb": "compare",
      "expected_concepts": [
        "old vine: deeper roots",
        "old vine: lower yields",
        "old vine: higher concentration",
        "old vine: higher tannins",
        "aging structure benefit",
        "complexity development"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "old vine: deeper roots",
          "old vine: lower yields",
          "old vine: higher concentration",
          "old vine: higher tannins",
          "aging structure benefit",
          "complexity development"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_043",
      "source_question_id": "OR_043",
      "stem": "Assess la calidad de un vino tinto que muestra estructura tánica fuerte pero aroma de frutas difuso, considerando edad probable.",
      "topic": "tannin_aroma_age_judgment",
      "RA": "RA4",
      "command_verb": "assess",
      "expected_concepts": [
        "tannin maturity indicator",
        "aroma volatility",
        "age estimation",
        "structure vs. development",
        "aging trajectory",
        "quality judgment context"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "tannin maturity indicator",
          "aroma volatility",
          "age estimation",
          "structure vs. development",
          "aging trajectory",
          "quality judgment context"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_044",
      "source_question_id": "OR_044",
      "stem": "Evaluate la influencia del corcho natural vs. alternativas de cierre en la evolución a largo plazo de un Burdeos tinto de guarda.",
      "topic": "closure_aging_impact",
      "RA": "RA4",
      "command_verb": "evaluate",
      "expected_concepts": [
        "oxygen permeability",
        "cork taint risk",
        "alternative closure benefits",
        "TCA contamination",
        "consistent aging",
        "cost trade-offs"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "oxygen permeability",
          "cork taint risk",
          "alternative closure benefits",
          "TCA contamination",
          "consistent aging",
          "cost trade-offs"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_045",
      "source_question_id": "OR_045",
      "stem": "Discuss la relevancia de los taninos en la estructura y evolución de vinos tintos, y cómo el winemaker puede gestionarlos.",
      "topic": "tannin_management",
      "RA": "RA5",
      "command_verb": "discuss",
      "expected_concepts": [
        "tannin sources",
        "seed tannins: astringency",
        "skin tannins: structure",
        "extraction control",
        "temperature management",
        "aging benefits",
        "softening mechanisms"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "tannin sources",
          "seed tannins: astringency",
          "skin tannins: structure",
          "extraction control",
          "temperature management",
          "aging benefits",
          "softening mechanisms"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_046",
      "source_question_id": "OR_046",
      "stem": "Recommend una estrategia de mezcla (blend) para un vino tinto que busca equilibrio entre estructura, fruit, y elegancia.",
      "topic": "red_blend_strategy",
      "RA": "RA5",
      "command_verb": "recommend",
      "expected_concepts": [
        "varietal roles in blend",
        "Cabernet for structure",
        "Merlot for flesh",
        "Petit Verdot for aging",
        "balance proportions",
        "tasting evaluation iterative"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "varietal roles in blend",
          "Cabernet for structure",
          "Merlot for flesh",
          "Petit Verdot for aging",
          "balance proportions",
          "tasting evaluation iterative"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_047",
      "source_question_id": "OR_047",
      "stem": "Identify and explain las características que permiten diferenciar un vino tinto de Napa Valley de uno similar de Sonoma, basándote en clima y suelo.",
      "topic": "napa_sonoma_terroir_distinction",
      "RA": "RA5",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "valley floor: riper fruit",
        "hillside: structure and complexity",
        "fog influence variation",
        "soil mineral expression",
        "Cabernet ripeness difference",
        "regional identity"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "valley floor: riper fruit",
          "hillside: structure and complexity",
          "fog influence variation",
          "soil mineral expression",
          "Cabernet ripeness difference",
          "regional identity"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_048",
      "source_question_id": "OR_048",
      "stem": "Describe el proceso de elaboración de un vino espumoso tradicional (méthode champenoise) y cómo afecta al sabor final.",
      "topic": "traditional_sparkling_method",
      "RA": "RA3",
      "command_verb": "describe",
      "expected_concepts": [
        "primary fermentation",
        "secondary fermentation in bottle",
        "autolysis",
        "yeast contact",
        "creamy texture",
        "complex aromatic development",
        "bubble formation"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "primary fermentation",
          "secondary fermentation in bottle",
          "autolysis",
          "yeast contact",
          "creamy texture",
          "complex aromatic development",
          "bubble formation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_049",
      "source_question_id": "OR_049",
      "stem": "Explica cómo el diurnal temperature range (DTR) en viñedos afecta la frescura y complejidad aromatic del vino final.",
      "topic": "diurnal_range_freshness",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "warm day: sugar accumulation",
        "cool night: acid retention",
        "DTR benefit: both sugar and acidity",
        "flavor maturity vs. acid balance",
        "ideal DTR zones",
        "aromatic complexity from acid preservation"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "warm day: sugar accumulation",
          "cool night: acid retention",
          "DTR benefit: both sugar and acidity",
          "flavor maturity vs. acid balance",
          "ideal DTR zones",
          "aromatic complexity from acid preservation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_050",
      "source_question_id": "OR_050",
      "stem": "Compare la elegancia y potencial de envejecimiento de vinos dulces elaborados por botrytis (noble rot) vs. deshidratación de uvas.",
      "topic": "sweet_wine_production_methods",
      "RA": "RA2",
      "command_verb": "compare",
      "expected_concepts": [
        "botrytis: noble rot complexity",
        "botrytis: honey and citrus notes",
        "botrytis: acidity retention",
        "drying: concentration",
        "drying: less complexity",
        "aging potential variation"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "botrytis: noble rot complexity",
          "botrytis: honey and citrus notes",
          "botrytis: acidity retention",
          "drying: concentration",
          "drying: less complexity",
          "aging potential variation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_051",
      "source_question_id": "OR_051",
      "stem": "Assess la calidad de un vino fortificado que muestra balance entre alcohol, sweetness, y complejidad aromática.",
      "topic": "fortified_wine_quality",
      "RA": "RA1",
      "command_verb": "assess",
      "expected_concepts": [
        "alcohol role: structure and preservation",
        "sweetness level appropriateness",
        "aroma complexity",
        "aging indicators",
        "style expectations",
        "balance judgment"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "alcohol role: structure and preservation",
          "sweetness level appropriateness",
          "aroma complexity",
          "aging indicators",
          "style expectations",
          "balance judgment"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_052",
      "source_question_id": "OR_052",
      "stem": "Evaluate los beneficios y riesgos de utilizar microoxygenation durante la crianza de un vino tinto para suavizar táninos.",
      "topic": "microoxygenation_risk_benefit",
      "RA": "RA2",
      "command_verb": "evaluate",
      "expected_concepts": [
        "tannin polymerization",
        "color stabilization",
        "oxidation risk",
        "over-oxidation possibility",
        "cost consideration",
        "style impact unpredictability"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "tannin polymerization",
          "color stabilization",
          "oxidation risk",
          "over-oxidation possibility",
          "cost consideration",
          "style impact unpredictability"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_053",
      "source_question_id": "OR_053",
      "stem": "Discuss la importancia del pH y su interacción con acidez, táninos, y color en la estabilidad y evolución del vino.",
      "topic": "ph_stability_interaction",
      "RA": "RA3",
      "command_verb": "discuss",
      "expected_concepts": [
        "pH vs. titratable acidity distinction",
        "microbiological stability",
        "tannin color expression",
        "oxidation sensitivity",
        "aging trajectory impact",
        "winemaker pH management tools"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "pH vs. titratable acidity distinction",
          "microbiological stability",
          "tannin color expression",
          "oxidation sensitivity",
          "aging trajectory impact",
          "winemaker pH management tools"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_054",
      "source_question_id": "OR_054",
      "stem": "Recommend un calendario de cosecha (picking schedule) para un viñedo de Chardonnay que busca elaborar un espumoso de alta elegancia.",
      "topic": "sparkling_chardonnay_harvest",
      "RA": "RA4",
      "command_verb": "recommend",
      "expected_concepts": [
        "lower alcohol target",
        "higher acidity retention",
        "optimal ripeness for aroma",
        "timing precision",
        "multiple picks vs. single",
        "analytical targets: brix, pH, TA"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "lower alcohol target",
          "higher acidity retention",
          "optimal ripeness for aroma",
          "timing precision",
          "multiple picks vs. single",
          "analytical targets: brix, pH, TA"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_055",
      "source_question_id": "OR_055",
      "stem": "Identify and explain los mecanismos por los cuales el canopy management (manipulación del dosel) impacta la composición de la uva.",
      "topic": "canopy_management_grape_composition",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "leaf area management",
        "fruit exposure balance",
        "sugar accumulation",
        "phenolic ripeness",
        "sunlight interception",
        "shade prevention"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "leaf area management",
          "fruit exposure balance",
          "sugar accumulation",
          "phenolic ripeness",
          "sunlight interception",
          "shade prevention"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_056",
      "source_question_id": "OR_056",
      "stem": "Describe la evolución sensorial de un vino envejecido en botella durante 10-15 años, explicando los cambios químicos subyacentes.",
      "topic": "bottle_aging_evolution",
      "RA": "RA5",
      "command_verb": "describe",
      "expected_concepts": [
        "tannin polymerization",
        "color brick formation",
        "secondary aromatics development",
        "fruit to earth shift",
        "texture integration",
        "aromatic complexity peak"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "tannin polymerization",
          "color brick formation",
          "secondary aromatics development",
          "fruit to earth shift",
          "texture integration",
          "aromatic complexity peak"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_057",
      "source_question_id": "OR_057",
      "stem": "Describe the role of cork's porosity in enabling the slow oxidation that allows a fine red wine to age gracefully in the bottle.",
      "topic": "cork_oxygen_transmission",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "cork structure and microporosity",
        "oxygen transmission rate",
        "slow oxidation benefits",
        "tannin polymerization",
        "color brick development",
        "aromatic integration"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "cork structure and microporosity",
          "oxygen transmission rate",
          "slow oxidation benefits",
          "tannin polymerization",
          "color brick development",
          "aromatic integration"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_058",
      "source_question_id": "OR_058",
      "stem": "Explain why a wine from a warm vintage in Bordeaux might have higher alcohol but lower acidity than a cool vintage from the same vineyard.",
      "topic": "vintage_climate_variation",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "temperature impact on ripening",
        "sugar accumulation rate",
        "malic acid retention",
        "phenolic maturity variation",
        "vintage character expression"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "temperature impact on ripening",
          "sugar accumulation rate",
          "malic acid retention",
          "phenolic maturity variation",
          "vintage character expression"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_059",
      "source_question_id": "OR_059",
      "stem": "Compare the sensory and structural impact of malolactic fermentation on Chardonnay vs. Sauvignon Blanc, explaining why producers choose differently for each varietal.",
      "topic": "varietal_mlf_strategy",
      "RA": "RA2",
      "command_verb": "compare",
      "expected_concepts": [
        "Chardonnay: benefits from MLF texture",
        "Sauvignon Blanc: benefits from acidity preservation",
        "acidity role in style",
        "aromatic complexity vs. freshness",
        "producer intent and market positioning"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Chardonnay: benefits from MLF texture",
          "Sauvignon Blanc: benefits from acidity preservation",
          "acidity role in style",
          "aromatic complexity vs. freshness",
          "producer intent and market positioning"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_060",
      "source_question_id": "OR_060",
      "stem": "Assess a Pinot Noir showing bright red fruit aromas, silky tannins, and good acidity balance at age 5, determining whether it is still in its primary character or approaching maturity evolution.",
      "topic": "tannin_maturity_age_assessment",
      "RA": "RA2",
      "command_verb": "assess",
      "expected_concepts": [
        "tannin softening indicators",
        "aroma stability vs. evolution",
        "age estimation from structure",
        "remaining drinking window",
        "peak expression timeline"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "tannin softening indicators",
          "aroma stability vs. evolution",
          "age estimation from structure",
          "remaining drinking window",
          "peak expression timeline"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_061",
      "source_question_id": "OR_061",
      "stem": "Evaluate the trade-offs between using temperature-controlled stainless steel fermentation (for aroma retention) vs. open vat fermentation (for tannin extraction and contact) in red winemaking.",
      "topic": "fermentation_vessel_trade_offs",
      "RA": "RA3",
      "command_verb": "evaluate",
      "expected_concepts": [
        "temperature control precision",
        "aroma volatility",
        "tannin extraction dynamics",
        "spoilage risk",
        "winemaker intent and market target",
        "cost considerations"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "temperature control precision",
          "aroma volatility",
          "tannin extraction dynamics",
          "spoilage risk",
          "winemaker intent and market target",
          "cost considerations"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_062",
      "source_question_id": "OR_062",
      "stem": "Discuss the implications of residual sugar in a dry-appearing wine (below 1 g/L perceived sweetness threshold) and why some producers deliberately leave RS while others work to eliminate it completely.",
      "topic": "residual_sugar_strategy",
      "RA": "RA3",
      "command_verb": "discuss",
      "expected_concepts": [
        "RS and tannin perception",
        "microbial stability",
        "food pairing implications",
        "consumer expectations",
        "production philosophy",
        "climate and ripeness variation"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "RS and tannin perception",
          "microbial stability",
          "food pairing implications",
          "consumer expectations",
          "production philosophy",
          "climate and ripeness variation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_063",
      "source_question_id": "OR_063",
      "stem": "Recommend a complete winemaking protocol for a cool-climate Riesling that targets a dry, mineral style with maximum expression of terroir and site-specific character.",
      "topic": "riesling_terroir_expression_protocol",
      "RA": "RA4",
      "command_verb": "recommend",
      "expected_concepts": [
        "harvest timing for acidity retention",
        "whole-bunch pressing",
        "cool fermentation temperature",
        "yeast strain selection",
        "malolactic prevention",
        "early bottling",
        "oak avoidance"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "harvest timing for acidity retention",
          "whole-bunch pressing",
          "cool fermentation temperature",
          "yeast strain selection",
          "malolactic prevention",
          "early bottling",
          "oak avoidance"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_064",
      "source_question_id": "OR_064",
      "stem": "Identify and explain the key vineyard site factors that make the Mosel region in Germany structurally suited to producing ultra-fresh, low-alcohol wines with high acidity.",
      "topic": "mosel_terroir_structure",
      "RA": "RA4",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "steep south-facing slopes maximize sunlight",
        "cool continental influence",
        "slate soil drainage",
        "altitude and temperature",
        "late harvest ripeness without excessive alcohol",
        "acidity preservation natural advantage"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "steep south-facing slopes maximize sunlight",
          "cool continental influence",
          "slate soil drainage",
          "altitude and temperature",
          "late harvest ripeness without excessive alcohol",
          "acidity preservation natural advantage"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_065",
      "source_question_id": "OR_065",
      "stem": "Describe the physical and chemical changes that occur when a fortified wine (Port, Sherry) ages oxidatively vs. reductively, and how each aging style influences final character.",
      "topic": "fortified_aging_oxidative_reductive",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "oxidative aging (oxygen contact)",
        "reductive aging (sealed environment)",
        "color development",
        "aromatic evolution",
        "tannin integration",
        "complexity tier progression"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "oxidative aging (oxygen contact)",
          "reductive aging (sealed environment)",
          "color development",
          "aromatic evolution",
          "tannin integration",
          "complexity tier progression"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_066",
      "source_question_id": "OR_066",
      "stem": "Explain the relationship between soil type, water availability during veraison, and the final concentration of tannins and phenolic ripeness in red grapes.",
      "topic": "soil_water_phenolic_ripeness",
      "RA": "RA2",
      "command_verb": "explain",
      "expected_concepts": [
        "water stress during veraison",
        "tannin synthesis activation",
        "phenolic maturity markers",
        "grape concentration",
        "soil drainage role",
        "irrigation decisions impact"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "water stress during veraison",
          "tannin synthesis activation",
          "phenolic maturity markers",
          "grape concentration",
          "soil drainage role",
          "irrigation decisions impact"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_067",
      "source_question_id": "OR_067",
      "stem": "Compare noble rot (Botrytis cinerea) development in Sauternes vs. Tokaji, explaining how climate, humidity, morning fog, and vineyard management create different expressions of sweet complexity.",
      "topic": "noble_rot_regional_expression",
      "RA": "RA3",
      "command_verb": "compare",
      "expected_concepts": [
        "Sauternes: maritime humidity and Gironde moisture",
        "Tokaji: continental cool nights and lake effect",
        "noble rot timing and intensity",
        "concentration levels",
        "aromatic profiles variation",
        "acidity retention differences"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "Sauternes: maritime humidity and Gironde moisture",
          "Tokaji: continental cool nights and lake effect",
          "noble rot timing and intensity",
          "concentration levels",
          "aromatic profiles variation",
          "acidity retention differences"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_068",
      "source_question_id": "OR_068",
      "stem": "Assess the quality and style consistency of a barrel-fermented Chardonnay that shows both primary orchard fruit and developed oak-driven spice, determining whether oak integration is balanced or dominating.",
      "topic": "oak_integration_balance_assessment",
      "RA": "RA4",
      "command_verb": "assess",
      "expected_concepts": [
        "primary fruit preservation",
        "oak vanillin and toasted character integration",
        "texture development",
        "balance vs. imbalance markers",
        "oak age and intensity",
        "malolactic influence"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "primary fruit preservation",
          "oak vanillin and toasted character integration",
          "texture development",
          "balance vs. imbalance markers",
          "oak age and intensity",
          "malolactic influence"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_069",
      "source_question_id": "OR_069",
      "stem": "Evaluate the risks and benefits of using enzyme treatments to increase extraction and aroma release during red grape maceration, considering both sensory outcomes and production goals.",
      "topic": "enzyme_treatment_maceration",
      "RA": "RA2",
      "command_verb": "evaluate",
      "expected_concepts": [
        "enzyme action on cell walls",
        "tannin extraction increase",
        "color development",
        "aroma compound release",
        "time reduction benefit",
        "potential over-extraction risk",
        "cost efficiency"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "enzyme action on cell walls",
          "tannin extraction increase",
          "color development",
          "aroma compound release",
          "time reduction benefit",
          "potential over-extraction risk",
          "cost efficiency"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_070",
      "source_question_id": "OR_070",
      "stem": "Discuss how climate change is altering traditional wine regions' capacity to produce their signature styles, and what viticultural and winemaking adaptations producers are implementing to maintain character.",
      "topic": "climate_change_adaptation",
      "RA": "RA4",
      "command_verb": "discuss",
      "expected_concepts": [
        "warmer growing seasons",
        "earlier harvest timing",
        "higher potential alcohol",
        "lower acidity challenges",
        "higher altitude vineyard migration",
        "varietal shifting",
        "water scarcity adaptation",
        "style preservation strategies"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "warmer growing seasons",
          "earlier harvest timing",
          "higher potential alcohol",
          "lower acidity challenges",
          "higher altitude vineyard migration",
          "varietal shifting",
          "water scarcity adaptation",
          "style preservation strategies"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_071",
      "source_question_id": "OR_071",
      "stem": "Recommend a structured tasting protocol for evaluating 6 different oak regimes (new vs. used, different origins, different toast levels) applied to the same base wine, to isolate oak's specific impact.",
      "topic": "oak_regime_evaluation_protocol",
      "RA": "RA5",
      "command_verb": "recommend",
      "expected_concepts": [
        "control wine requirement",
        "blind tasting methodology",
        "flavor compound identification",
        "tannin structure comparison",
        "aroma intensity progression",
        "systematic note-taking",
        "statistical comparison approach"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "control wine requirement",
          "blind tasting methodology",
          "flavor compound identification",
          "tannin structure comparison",
          "aroma intensity progression",
          "systematic note-taking",
          "statistical comparison approach"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_072",
      "source_question_id": "OR_072",
      "stem": "Identify and explain how volcanic soils (particularly in regions like Alsace, Tokaji, and New Zealand) influence wine structure, mineral expression, and aging potential.",
      "topic": "volcanic_soil_mineral_expression",
      "RA": "RA3",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "volcanic soil composition (basalt, pumice)",
        "mineral nutrient availability",
        "drainage properties",
        "mineral compound uptake in fruit",
        "terroir expression intensity",
        "aging structure from minerals"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "volcanic soil composition (basalt, pumice)",
          "mineral nutrient availability",
          "drainage properties",
          "mineral compound uptake in fruit",
          "terroir expression intensity",
          "aging structure from minerals"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_073",
      "source_question_id": "OR_073",
      "stem": "Describe the sensory evolution of a bottled sparkling wine during secondary fermentation and post-disgorged aging, highlighting how autolytic yeast contact creates complexity.",
      "topic": "sparkling_autolysis_evolution",
      "RA": "RA2",
      "command_verb": "describe",
      "expected_concepts": [
        "secondary fermentation CO2 production",
        "yeast autolysis process",
        "amino acid and nucleotide release",
        "creamy texture development",
        "bread/biscuit aroma emergence",
        "bubble structure refinement"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "secondary fermentation CO2 production",
          "yeast autolysis process",
          "amino acid and nucleotide release",
          "creamy texture development",
          "bread/biscuit aroma emergence",
          "bubble structure refinement"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_074",
      "source_question_id": "OR_074",
      "stem": "Explain why a Nebbiolo wine at 10 years old, despite having moderate alcohol (14%), can still show intense tannins that feel astringent, whereas a Pinot Noir at the same age feels silky.",
      "topic": "tannin_structure_varietal_difference",
      "RA": "RA5",
      "command_verb": "explain",
      "expected_concepts": [
        "Nebbiolo: thick-skinned grape variety",
        "phenolic tannin concentration",
        "polymerization rate",
        "tannin structure chemical differences",
        "aging softening variation by variety",
        "sensory threshold differences"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Nebbiolo: thick-skinned grape variety",
          "phenolic tannin concentration",
          "polymerization rate",
          "tannin structure chemical differences",
          "aging softening variation by variety",
          "sensory threshold differences"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_075",
      "source_question_id": "OR_075",
      "stem": "Compare two identical harvest lots split into different cellar conditions (temperature-controlled vs. non-climate-controlled, oak vs. stainless, sealed vs. vented), predicting how each will diverge in character.",
      "topic": "cellar_conditions_divergence",
      "RA": "RA1",
      "command_verb": "compare",
      "expected_concepts": [
        "temperature stability impact",
        "oxidation rate variation",
        "oxygen transmission",
        "spoilage risk scenarios",
        "aging trajectory prediction",
        "compound evolution speed"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "temperature stability impact",
          "oxidation rate variation",
          "oxygen transmission",
          "spoilage risk scenarios",
          "aging trajectory prediction",
          "compound evolution speed"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_076",
      "source_question_id": "OR_076",
      "stem": "Assess the maturity stage of a Bordeaux blend showing dried fruit, resolved tannins, and subtle mineral secondary aromas, determining whether immediate consumption or continued aging is optimal.",
      "topic": "bordeaux_maturity_drinking_window",
      "RA": "RA5",
      "command_verb": "assess",
      "expected_concepts": [
        "primary to secondary aroma transition",
        "tannin integration timeline",
        "color and clarity markers",
        "flavor intensity plateau",
        "drinking window definition",
        "cellaring continuation decision"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "primary to secondary aroma transition",
          "tannin integration timeline",
          "color and clarity markers",
          "flavor intensity plateau",
          "drinking window definition",
          "cellaring continuation decision"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_077",
      "source_question_id": "OR_077",
      "stem": "Evaluate whether hand-harvesting vs. mechanical harvesting for a delicate Pinot Noir affects quality, considering grape damage, oxidation exposure, berry separation, and final wine outcomes.",
      "topic": "harvest_method_quality_impact",
      "RA": "RA3",
      "command_verb": "evaluate",
      "expected_concepts": [
        "mechanical efficiency and speed",
        "grape skin integrity",
        "oxidation during transport",
        "stems and leaf contamination",
        "vineyard slope accessibility",
        "cost efficiency comparison",
        "quality vs. production tradeoff"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "mechanical efficiency and speed",
          "grape skin integrity",
          "oxidation during transport",
          "stems and leaf contamination",
          "vineyard slope accessibility",
          "cost efficiency comparison",
          "quality vs. production tradeoff"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_078",
      "source_question_id": "OR_078",
      "stem": "Discuss the role of wine glass shape and size in releasing and concentrating aromas, directing flow patterns to the nose, and how different glass styles suit different wine types.",
      "topic": "glass_design_aroma_perception",
      "RA": "RA1",
      "command_verb": "discuss",
      "expected_concepts": [
        "bowl shape and aroma capture",
        "rim opening size",
        "surface area for oxidation",
        "flow dynamics",
        "temperature maintenance",
        "psychological expectation",
        "sensory expression optimization"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "bowl shape and aroma capture",
          "rim opening size",
          "surface area for oxidation",
          "flow dynamics",
          "temperature maintenance",
          "psychological expectation",
          "sensory expression optimization"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_079",
      "source_question_id": "OR_079",
      "stem": "Recommend a complete protocol for evaluating whether a wine at 8 years is approaching its peak drinking window or still has significant aging potential, including sensory and analytical benchmarks.",
      "topic": "peak_drinking_window_assessment_protocol",
      "RA": "RA4",
      "command_verb": "recommend",
      "expected_concepts": [
        "color development observation",
        "aroma evolution stage identification",
        "tannin integration level",
        "acidity preservation check",
        "residual sugar stability",
        "bottle variation acknowledgment",
        "cellar condition consideration"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "color development observation",
          "aroma evolution stage identification",
          "tannin integration level",
          "acidity preservation check",
          "residual sugar stability",
          "bottle variation acknowledgment",
          "cellar condition consideration"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_080",
      "source_question_id": "OR_080",
      "stem": "Identify and explain the viticultural practices that define the traditional Burgundy classification system (Grand Cru vs. Premier Cru vs. Village), connecting soil, microclimate, and site hierarchy to quality expression.",
      "topic": "burgundy_classification_soil_hierarchy",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "soil composition limestone variation",
        "aspect and sun exposure gradient",
        "drainage and minerality",
        "historical selection by Benedictine monks",
        "classification continuity",
        "site-specific expression documentation"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "soil composition limestone variation",
          "aspect and sun exposure gradient",
          "drainage and minerality",
          "historical selection by Benedictine monks",
          "classification continuity",
          "site-specific expression documentation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_081",
      "source_question_id": "OR_081",
      "stem": "Describe the complete evolution of a sweet wine made from botrytized grapes over 20 years in bottle, from initial concentration and honey aromas to mature complexity and integration.",
      "topic": "botrytized_sweet_wine_maturation",
      "RA": "RA2",
      "command_verb": "describe",
      "expected_concepts": [
        "initial honey and apricot aromas",
        "secondary citrus and spice development",
        "tannin softening in sweet context",
        "acidity preservation role",
        "oxidative browning",
        "tertiary complexity emergence",
        "long aging potential"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "initial honey and apricot aromas",
          "secondary citrus and spice development",
          "tannin softening in sweet context",
          "acidity preservation role",
          "oxidative browning",
          "tertiary complexity emergence",
          "long aging potential"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_082",
      "source_question_id": "OR_082",
      "stem": "Describe the sensory journey through a horizontal tasting of the same wine from 5 consecutive vintages (e.g., Pauillac 2014-2018), identifying which vintage shows optimal maturity balance.",
      "topic": "horizontal_vintage_tasting_evolution",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "vintage weather variation impact",
        "aging progression across similar wines",
        "maturity markers",
        "consistency within producer style",
        "optimal drinking window identification"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "vintage weather variation impact",
          "aging progression across similar wines",
          "maturity markers",
          "consistency within producer style",
          "optimal drinking window identification"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_083",
      "source_question_id": "OR_083",
      "stem": "Explain the biochemistry of why sparkling wines aged on lees for 3 years develop richer, more complex aromas than those aged for only 1 year, despite the same yeast strain.",
      "topic": "lees_autolysis_time_complexity",
      "RA": "RA2",
      "command_verb": "explain",
      "expected_concepts": [
        "yeast cell wall breakdown over time",
        "amino acid release kinetics",
        "nucleotide release",
        "aldehyde and alcohol interactions",
        "complexity tier progression",
        "aromatic compound generation rate"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "yeast cell wall breakdown over time",
          "amino acid release kinetics",
          "nucleotide release",
          "aldehyde and alcohol interactions",
          "complexity tier progression",
          "aromatic compound generation rate"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_084",
      "source_question_id": "OR_084",
      "stem": "Compare the commercial viability and quality potential of a small, hand-crafted winery in a cool climate vs. a large-scale mechanized operation in a warm climate, assessing which can achieve premium pricing.",
      "topic": "production_scale_climate_economics",
      "RA": "RA3",
      "command_verb": "compare",
      "expected_concepts": [
        "quality/quantity trade-off",
        "labor cost variation by region",
        "climate risk and vintage consistency",
        "market positioning flexibility",
        "brand identity development",
        "export potential variation"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "quality/quantity trade-off",
          "labor cost variation by region",
          "climate risk and vintage consistency",
          "market positioning flexibility",
          "brand identity development",
          "export potential variation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_085",
      "source_question_id": "OR_085",
      "stem": "Assess a Cabernet Sauvignon showing mature leather, tobacco, and dried fruit aromas but with a surprisingly tight, tannic structure, evaluating whether this indicates a problem or represents a highly ageworthy wine.",
      "topic": "aroma_structure_mismatch_assessment",
      "RA": "RA4",
      "command_verb": "assess",
      "expected_concepts": [
        "phenolic ripeness indicators",
        "tannin polymerization status",
        "color development consistency",
        "barrel aging effects",
        "vintage character variation",
        "individual wine potential"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "phenolic ripeness indicators",
          "tannin polymerization status",
          "color development consistency",
          "barrel aging effects",
          "vintage character variation",
          "individual wine potential"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_086",
      "source_question_id": "OR_086",
      "stem": "Evaluate the environmental impact of converting to biodynamic farming in an established vineyard, considering soil recovery timeline, pest management transition challenges, and potential quality changes.",
      "topic": "biodynamic_conversion_assessment",
      "RA": "RA5",
      "command_verb": "evaluate",
      "expected_concepts": [
        "soil microbiome recovery",
        "pest and disease management evolution",
        "certification timeline",
        "yield variation during transition",
        "quality attribute changes",
        "market positioning benefits"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "soil microbiome recovery",
          "pest and disease management evolution",
          "certification timeline",
          "yield variation during transition",
          "quality attribute changes",
          "market positioning benefits"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_087",
      "source_question_id": "OR_087",
      "stem": "Discuss how climate zones (cool, moderate, warm, hot) in wine regions create fundamentally different winemaking strategies, from harvest timing to fermentation choices to oak aging philosophy.",
      "topic": "climate_zone_winemaking_paradigm",
      "RA": "RA1",
      "command_verb": "discuss",
      "expected_concepts": [
        "ripeness achievement strategies",
        "acidity management approaches",
        "color and tannin development",
        "fermentation temperature control",
        "oak influence suitability",
        "alcohol risk mitigation"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "ripeness achievement strategies",
          "acidity management approaches",
          "color and tannin development",
          "fermentation temperature control",
          "oak influence suitability",
          "alcohol risk mitigation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_088",
      "source_question_id": "OR_088",
      "stem": "Recommend a complete blending strategy and trial protocol for a winemaker aiming to create a 3-varietal red blend that achieves both immediate approachability and 20-year aging potential.",
      "topic": "strategic_aging_blend_development",
      "RA": "RA2",
      "command_verb": "recommend",
      "expected_concepts": [
        "varietal role definition",
        "tannin structure balance",
        "acidity preservation",
        "aromatics complexity",
        "early fruit expression",
        "long-term evolution potential"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "varietal role definition",
          "tannin structure balance",
          "acidity preservation",
          "aromatics complexity",
          "early fruit expression",
          "long-term evolution potential"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_089",
      "source_question_id": "OR_089",
      "stem": "Identify and explain the terroir components (soil, aspect, elevation, microclimate) that make the Barossa Valley structurally different from the Adelaide Hills, 60km apart, resulting in dramatically different wine styles.",
      "topic": "micro_terroir_regional_distinction",
      "RA": "RA3",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "Barossa: warm valley floor ripeness",
        "Adelaide Hills: cool altitude freshness",
        "soil composition differences",
        "maritime influence variation",
        "ripeness profiles",
        "style expression signature"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "Barossa: warm valley floor ripeness",
          "Adelaide Hills: cool altitude freshness",
          "soil composition differences",
          "maritime influence variation",
          "ripeness profiles",
          "style expression signature"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_090",
      "source_question_id": "OR_090",
      "stem": "Describe the complete oxidation curve of a fine Oloroso Sherry over 50 years of solera aging, tracking color, aroma, texture, and structural changes at key intervals.",
      "topic": "oloroso_oxidative_maturation_curve",
      "RA": "RA4",
      "command_verb": "describe",
      "expected_concepts": [
        "solera system continuous blending",
        "controlled oxidation progression",
        "color browning increments",
        "aromatic complexity tiers",
        "alcohol and acidity stability",
        "final integration achievement"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "solera system continuous blending",
          "controlled oxidation progression",
          "color browning increments",
          "aromatic complexity tiers",
          "alcohol and acidity stability",
          "final integration achievement"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_091",
      "source_question_id": "OR_091",
      "stem": "Explain how the geographic origin (soil mineralogy, elevation, aspect, precipitation) of a Pinot Noir vineyard directly influences whether the final wine will display earthy, mineral-driven character vs. fruit-forward expressiveness.",
      "topic": "geology_aromatics_expression_link",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "soil mineral composition",
        "nutrient availability to vines",
        "water stress effects",
        "transpiration patterns",
        "phenolic ripeness",
        "aromatic compound accumulation pathways"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "soil mineral composition",
          "nutrient availability to vines",
          "water stress effects",
          "transpiration patterns",
          "phenolic ripeness",
          "aromatic compound accumulation pathways"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_092",
      "source_question_id": "OR_092",
      "stem": "Compare the structural and aromatic development of two Riesling wines from the same vintage but different vineyard sites—one steep slate slope, one flat alluvial plain—tracing 10-year aging trajectories.",
      "topic": "site_terroir_riesling_evolution",
      "RA": "RA4",
      "command_verb": "compare",
      "expected_concepts": [
        "slope drainage and ripeness",
        "alluvial soil water retention",
        "mineral expression variation",
        "acidity preservation",
        "aging potential difference",
        "complexity development rate"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "slope drainage and ripeness",
          "alluvial soil water retention",
          "mineral expression variation",
          "acidity preservation",
          "aging potential difference",
          "complexity development rate"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_093",
      "source_question_id": "OR_093",
      "stem": "Assess a Chardonnay from a warm vintage showing full ripeness markers (14.5% alcohol, tropical fruit) but with wine-maker's note indicating cool-climate winemaking technique, determining quality consistency.",
      "topic": "technique_vintage_alignment_assessment",
      "RA": "RA2",
      "command_verb": "assess",
      "expected_concepts": [
        "ripeness potential vs. technique intent",
        "alcohol expression vs. acid preservation",
        "aroma profile alignment",
        "structure development",
        "style coherence evaluation",
        "producer philosophy expression"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "ripeness potential vs. technique intent",
          "alcohol expression vs. acid preservation",
          "aroma profile alignment",
          "structure development",
          "style coherence evaluation",
          "producer philosophy expression"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_094",
      "source_question_id": "OR_094",
      "stem": "Evaluate the commercial and qualitative implications of using indigenous yeast fermentation vs. selected commercial strains for a high-value Burgundy-style Pinot Noir, considering consistency, expressiveness, and market perception.",
      "topic": "indigenous_yeast_strategy",
      "RA": "RA3",
      "command_verb": "evaluate",
      "expected_concepts": [
        "fermentation predictability variation",
        "aromatic profile diversity",
        "malolactic interaction timing",
        "risk of stuck fermentation",
        "terroir expression enhancement",
        "consumer perception and marketing"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "fermentation predictability variation",
          "aromatic profile diversity",
          "malolactic interaction timing",
          "risk of stuck fermentation",
          "terroir expression enhancement",
          "consumer perception and marketing"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_095",
      "source_question_id": "OR_095",
      "stem": "Discuss the trade-offs between modern sustainability certifications (organic, biodynamic, natural) and traditional conventional viticulture in terms of yield, quality, cost, and environmental genuine benefit.",
      "topic": "sustainability_certification_trade_offs",
      "RA": "RA5",
      "command_verb": "discuss",
      "expected_concepts": [
        "yield reduction reality",
        "input cost changes",
        "chemical residue impacts",
        "soil recovery benefits",
        "marketing value vs. production cost",
        "certification program trade-offs",
        "genuine environmental metrics"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "yield reduction reality",
          "input cost changes",
          "chemical residue impacts",
          "soil recovery benefits",
          "marketing value vs. production cost",
          "certification program trade-offs",
          "genuine environmental metrics"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_096",
      "source_question_id": "OR_096",
      "stem": "Recommend a complete protocol for conducting a 10-wine comparative tasting evaluating the impact of different cork closures (natural, technical, synthetic, screw cap) on a 10-year-aged Bordeaux.",
      "topic": "closure_impact_comparative_protocol",
      "RA": "RA1",
      "command_verb": "recommend",
      "expected_concepts": [
        "oxygen transmission variation",
        "TCA taint incidence",
        "cork integration consistency",
        "blind assessment methodology",
        "aging trajectory tracking",
        "chemical analysis integration"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "oxygen transmission variation",
          "TCA taint incidence",
          "cork integration consistency",
          "blind assessment methodology",
          "aging trajectory tracking",
          "chemical analysis integration"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_097",
      "source_question_id": "OR_097",
      "stem": "Identify and explain how the three distinct soil zones within the Chablis region (Kimmeridgian limestone, Portlandian limestone, Jurassic clay) each produce characteristic mineral-driven white wine styles.",
      "topic": "chablis_limestone_terroir_expression",
      "RA": "RA5",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "Kimmeridgian: shells and mineral intensity",
        "Portlandian: limestone with clay blend",
        "soil chemistry and mineral uptake",
        "pH influence",
        "aroma profile distinction",
        "aging potential variation"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Kimmeridgian: shells and mineral intensity",
          "Portlandian: limestone with clay blend",
          "soil chemistry and mineral uptake",
          "pH influence",
          "aroma profile distinction",
          "aging potential variation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_098",
      "source_question_id": "OR_098",
      "stem": "Describe the complete 3-phase harvest decision-making process for a grower managing multiple parcels in a vintage where some blocks ripen early while others lag, optimizing for quality across diverse conditions.",
      "topic": "parcel_selective_harvest_strategy",
      "RA": "RA2",
      "command_verb": "describe",
      "expected_concepts": [
        "analytical ripeness (Brix/TA/pH)",
        "phenolic maturity assessment",
        "disease and pest pressure",
        "weather forecast integration",
        "quality target definition",
        "separate lot production strategy"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "analytical ripeness (Brix/TA/pH)",
          "phenolic maturity assessment",
          "disease and pest pressure",
          "weather forecast integration",
          "quality target definition",
          "separate lot production strategy"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_099",
      "source_question_id": "OR_099",
      "stem": "Explain the cascade effect whereby residual sugar in a lower-alcohol wine (below 12.5%) changes not only sweetness perception but also tannin expression, acidity balance, and food pairing suitability.",
      "topic": "residual_sugar_perceptual_cascade",
      "RA": "RA3",
      "command_verb": "explain",
      "expected_concepts": [
        "RS and tannin softening perception",
        "acid and sweetness balance interaction",
        "alcohol and structure relationship",
        "food pairing dynamics",
        "flavor intensity masking effects",
        "viscosity and texture effects"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "RS and tannin softening perception",
          "acid and sweetness balance interaction",
          "alcohol and structure relationship",
          "food pairing dynamics",
          "flavor intensity masking effects",
          "viscosity and texture effects"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_100",
      "source_question_id": "OR_100",
      "stem": "Compare the market economics and production challenges of small-batch, limited-release wines vs. high-volume flagship brands from the same winery, evaluating profitability and brand positioning strategies.",
      "topic": "production_scale_brand_strategy",
      "RA": "RA1",
      "command_verb": "compare",
      "expected_concepts": [
        "production efficiency economies of scale",
        "quality-cost relationship",
        "brand tier positioning",
        "marketing spend ratios",
        "distribution channel differences",
        "collector vs. consumer market"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "production efficiency economies of scale",
          "quality-cost relationship",
          "brand tier positioning",
          "marketing spend ratios",
          "distribution channel differences",
          "collector vs. consumer market"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_101",
      "source_question_id": "OR_101",
      "stem": "Assess a Sauvignon Blanc from a warm region displaying higher-than-expected acidity (9.5 g/L TA) and grassy, herbaceous aromas normally associated with cool-climate styles, determining whether this is anomalous or represents valid expression.",
      "topic": "regional_anomaly_quality_assessment",
      "RA": "RA5",
      "command_verb": "assess",
      "expected_concepts": [
        "climate expectation vs. actual expression",
        "terroir anomaly possibility",
        "winemaker intervention effects",
        "acidity source determination",
        "aroma profile origins",
        "quality merit independent of category"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "climate expectation vs. actual expression",
          "terroir anomaly possibility",
          "winemaker intervention effects",
          "acidity source determination",
          "aroma profile origins",
          "quality merit independent of category"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_102",
      "source_question_id": "OR_102",
      "stem": "Evaluate whether extended maceration (30+ days) on skins for a white wine (e.g., orange/natural wine style) produces legitimately improved complexity or represents excessive oxidation risk and microbiological spoilage danger.",
      "topic": "extended_maceration_risk_benefit",
      "RA": "RA4",
      "command_verb": "evaluate",
      "expected_concepts": [
        "tannin extraction from skins",
        "color and oxidative browning",
        "aromatic compound release",
        "spoilage organism growth risk",
        "SO2 preservation challenge",
        "style achievement vs. execution risk"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "tannin extraction from skins",
          "color and oxidative browning",
          "aromatic compound release",
          "spoilage organism growth risk",
          "SO2 preservation challenge",
          "style achievement vs. execution risk"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_103",
      "source_question_id": "OR_103",
      "stem": "Discuss the implications of using synthetic or alternative closures (screw caps, glass stoppers, plastic corks) on wine aging, perceived quality, tradition, sustainability, and long-term market adoption.",
      "topic": "closure_technology_market_evolution",
      "RA": "RA2",
      "command_verb": "discuss",
      "expected_concepts": [
        "oxygen control precision",
        "TCA contamination elimination",
        "consumer perception lag",
        "tradition vs. innovation tension",
        "environmental footprint comparison",
        "aging reliability and consistency"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "oxygen control precision",
          "TCA contamination elimination",
          "consumer perception lag",
          "tradition vs. innovation tension",
          "environmental footprint comparison",
          "aging reliability and consistency"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_104",
      "source_question_id": "OR_104",
      "stem": "Recommend a complete vineyard management plan for converting a 20-hectare conventional vineyard to organic certification over 5 years, including pest management, soil recovery, and transition vintage handling.",
      "topic": "conventional_organic_transition_plan",
      "RA": "RA3",
      "command_verb": "recommend",
      "expected_concepts": [
        "soil health restoration timeline",
        "pest and disease integrated management",
        "yield expectation during transition",
        "harvest timing decisions",
        "separate vintage production consideration",
        "marketing and certification strategy"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "soil health restoration timeline",
          "pest and disease integrated management",
          "yield expectation during transition",
          "harvest timing decisions",
          "separate vintage production consideration",
          "marketing and certification strategy"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_105",
      "source_question_id": "OR_105",
      "stem": "Identify and explain how the glacial heritage of New Zealand's South Island (Marlborough, Central Otago) creates distinctive soil compositions and microclimates that define regional wine styles.",
      "topic": "glacial_geology_soil_wine_expression",
      "RA": "RA4",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "glacial valley formation and aspect",
        "soil minerality from glacial deposit",
        "temperature extremes from altitude",
        "diurnal temperature range benefit",
        "water drainage patterns",
        "regional style consistency"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "developing"
        },
        "required_signals": [
          "glacial valley formation and aspect",
          "soil minerality from glacial deposit",
          "temperature extremes from altitude",
          "diurnal temperature range benefit",
          "water drainage patterns",
          "regional style consistency"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_106",
      "source_question_id": "OR_106",
      "stem": "Describe the complete evolution of a Tokaji Aszú wine from harvest (noble rot concentration), through fermentation arrest, aging in wooden casks, and 10+ year bottle maturation, tracking quality and character transformation.",
      "topic": "tokaji_aszu_complete_maturation_arc",
      "RA": "RA2",
      "command_verb": "describe",
      "expected_concepts": [
        "botrytized berry concentration",
        "fermentation control complexity",
        "solera-style blending",
        "oxidative maturation in cask",
        "botrytis complexity emergence",
        "long-aging capacity",
        "tertiary aromatics development"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "botrytized berry concentration",
          "fermentation control complexity",
          "solera-style blending",
          "oxidative maturation in cask",
          "botrytis complexity emergence",
          "long-aging capacity",
          "tertiary aromatics development"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_107",
      "source_question_id": "OR_107",
      "stem": "Describe the climatic and harvest conditions required to produce Icewine or Eiswein from grapes frozen naturally on the vine.",
      "topic": "icewine_natural_freezing_conditions",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "ripe healthy grapes retained on the vine",
        "sustained sub-zero temperature",
        "water freezes within the berries",
        "harvest and pressing while frozen",
        "low yield and concentrated must"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "ripe healthy grapes retained on the vine",
          "sustained sub-zero temperature",
          "water freezes within the berries",
          "harvest and pressing while frozen",
          "low yield and concentrated must"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_108",
      "source_question_id": "OR_108",
      "stem": "Explain why delaying harvest for Icewine or Eiswein increases both potential concentration and the risk of losing the crop.",
      "topic": "icewine_delayed_harvest_risk",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "extended hang time",
        "water loss before freezing",
        "required freezing event",
        "bird and animal damage",
        "rot and adverse weather",
        "very low and uncertain yield"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "extended hang time",
          "water loss before freezing",
          "required freezing event",
          "bird and animal damage",
          "rot and adverse weather",
          "very low and uncertain yield"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_109",
      "source_question_id": "OR_109",
      "stem": "Compare the vineyard conditions needed for Icewine or Eiswein with those needed for botrytised wines such as Sauternes.",
      "topic": "icewine_botrytis_vineyard_comparison",
      "RA": "RA1",
      "command_verb": "compare",
      "expected_concepts": [
        "natural freezing versus noble rot",
        "healthy frozen fruit versus Botrytis-infected fruit",
        "cold winter event",
        "humid mornings and dry afternoons",
        "different crop-loss risks",
        "concentration by ice separation versus berry dehydration"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "natural freezing versus noble rot",
          "healthy frozen fruit versus Botrytis-infected fruit",
          "cold winter event",
          "humid mornings and dry afternoons",
          "different crop-loss risks",
          "concentration by ice separation versus berry dehydration"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_110",
      "source_question_id": "OR_110",
      "stem": "Assess whether a vineyard site with frequent autumn fog but slow afternoon drying is suitable for consistent Sauternes production.",
      "topic": "sauternes_botrytis_site_suitability",
      "RA": "RA1",
      "command_verb": "assess",
      "expected_concepts": [
        "humidity encourages Botrytis infection",
        "dry afternoons favour noble rot",
        "persistent moisture raises grey rot risk",
        "selective picking requirement",
        "vintage variability",
        "qualified suitability judgement"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "humidity encourages Botrytis infection",
          "dry afternoons favour noble rot",
          "persistent moisture raises grey rot risk",
          "selective picking requirement",
          "vintage variability",
          "qualified suitability judgement"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_111",
      "source_question_id": "OR_111",
      "stem": "Evaluate the decision to retain botrytis-prone parcels for Tokaji Aszú when autumn rainfall is becoming less predictable.",
      "topic": "tokaji_botrytis_climate_risk",
      "RA": "RA1",
      "command_verb": "evaluate",
      "expected_concepts": [
        "site exposure and humidity",
        "need for beneficial Botrytis",
        "risk of rain and grey rot",
        "selective harvesting cost",
        "vintage variation",
        "alternative dry-wine use",
        "balanced conclusion"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "site exposure and humidity",
          "need for beneficial Botrytis",
          "risk of rain and grey rot",
          "selective harvesting cost",
          "vintage variation",
          "alternative dry-wine use",
          "balanced conclusion"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_112",
      "source_question_id": "OR_112",
      "stem": "Discuss the vineyard and harvest risks involved when grapes intended for passito production are left to reach very high ripeness before drying.",
      "topic": "passito_high_ripeness_harvest_risk",
      "RA": "RA1",
      "command_verb": "discuss",
      "expected_concepts": [
        "extended ripening",
        "sugar accumulation and acid loss",
        "rot and weather exposure",
        "bird damage",
        "careful bunch selection",
        "yield reduction",
        "trade-off between concentration and freshness"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "extended ripening",
          "sugar accumulation and acid loss",
          "rot and weather exposure",
          "bird damage",
          "careful bunch selection",
          "yield reduction",
          "trade-off between concentration and freshness"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_113",
      "source_question_id": "OR_113",
      "stem": "Recommend fermentation choices for an Icewine producer seeking high residual sugar, fresh acidity, and a clean fruit profile.",
      "topic": "icewine_fermentation_choices",
      "RA": "RA2",
      "command_verb": "recommend",
      "expected_concepts": [
        "very concentrated must",
        "slow difficult fermentation",
        "temperature control",
        "suitable yeast selection",
        "fermentation stopped or naturally arrested",
        "retention of acidity and primary fruit",
        "microbial stability"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "very concentrated must",
          "slow difficult fermentation",
          "temperature control",
          "suitable yeast selection",
          "fermentation stopped or naturally arrested",
          "retention of acidity and primary fruit",
          "microbial stability"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_114",
      "source_question_id": "OR_114",
      "stem": "Identify the concentration mechanism used in Icewine or Eiswein and explain how it influences fermentation and residual sugar.",
      "topic": "icewine_concentration_and_residual_sugar",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "water freezes in the berry",
        "concentrated juice separated during pressing",
        "high sugar must",
        "osmotic stress on yeast",
        "slow or incomplete fermentation",
        "high residual sugar",
        "acid-sweetness balance"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "water freezes in the berry",
          "concentrated juice separated during pressing",
          "high sugar must",
          "osmotic stress on yeast",
          "slow or incomplete fermentation",
          "high residual sugar",
          "acid-sweetness balance"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_115",
      "source_question_id": "OR_115",
      "stem": "Describe the principal production stages used to create Tokaji Aszú from individually selected aszú berries.",
      "topic": "tokaji_aszu_production_stages",
      "RA": "RA2",
      "command_verb": "describe",
      "expected_concepts": [
        "selection of botrytised aszú berries",
        "base wine or fermenting must",
        "maceration of aszú material",
        "pressing",
        "slow fermentation",
        "residual sugar",
        "maturation"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "selection of botrytised aszú berries",
          "base wine or fermenting must",
          "maceration of aszú material",
          "pressing",
          "slow fermentation",
          "residual sugar",
          "maturation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_116",
      "source_question_id": "OR_116",
      "stem": "Explain how adding aszú berries to a base wine or fermenting must creates the sweetness, acidity, and flavour concentration of Tokaji Aszú.",
      "topic": "tokaji_aszu_berry_addition_mechanism",
      "RA": "RA2",
      "command_verb": "explain",
      "expected_concepts": [
        "botrytised dehydrated berries",
        "high sugar and acid concentration",
        "maceration and extraction",
        "transfer of botrytis-derived flavours",
        "difficult slow fermentation",
        "retained residual sugar",
        "balanced concentrated style"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "botrytised dehydrated berries",
          "high sugar and acid concentration",
          "maceration and extraction",
          "transfer of botrytis-derived flavours",
          "difficult slow fermentation",
          "retained residual sugar",
          "balanced concentrated style"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_117",
      "source_question_id": "OR_117",
      "stem": "Compare the production choices used to create Tokaji Aszú and Sauternes after botrytised grapes reach the winery.",
      "topic": "tokaji_sauternes_production_comparison",
      "RA": "RA2",
      "command_verb": "compare",
      "expected_concepts": [
        "aszú berry selection and addition",
        "direct pressing of botrytised Sauternes grapes",
        "maceration difference",
        "high-sugar fermentation challenge",
        "residual sugar management",
        "maturation choices",
        "style consequences"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "aszú berry selection and addition",
          "direct pressing of botrytised Sauternes grapes",
          "maceration difference",
          "high-sugar fermentation challenge",
          "residual sugar management",
          "maturation choices",
          "style consequences"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_118",
      "source_question_id": "OR_118",
      "stem": "Assess a Sauternes producer's decision to ferment separate picking lots before blending them into the final wine.",
      "topic": "sauternes_separate_lot_fermentation",
      "RA": "RA2",
      "command_verb": "assess",
      "expected_concepts": [
        "multiple selective pickings",
        "variation in botrytis and ripeness",
        "lot-specific fermentation control",
        "quality selection",
        "blending flexibility",
        "higher labour and winery cost",
        "qualified judgement"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "multiple selective pickings",
          "variation in botrytis and ripeness",
          "lot-specific fermentation control",
          "quality selection",
          "blending flexibility",
          "higher labour and winery cost",
          "qualified judgement"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_119",
      "source_question_id": "OR_119",
      "stem": "Evaluate the use of new oak during fermentation and maturation for a concentrated botrytised wine from Sauternes.",
      "topic": "sauternes_new_oak_tradeoffs",
      "RA": "RA2",
      "command_verb": "evaluate",
      "expected_concepts": [
        "oxygen exposure and texture",
        "oak-derived flavours",
        "integration with concentrated fruit",
        "cost",
        "risk of masking botrytis character",
        "ageing potential",
        "balanced conclusion"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "oxygen exposure and texture",
          "oak-derived flavours",
          "integration with concentrated fruit",
          "cost",
          "risk of masking botrytis character",
          "ageing potential",
          "balanced conclusion"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_120",
      "source_question_id": "OR_120",
      "stem": "Discuss how drying grapes on the vine, on mats, or in controlled rooms changes the risks and style options available to a passito producer.",
      "topic": "passito_drying_method_choices",
      "RA": "RA2",
      "command_verb": "discuss",
      "expected_concepts": [
        "water loss and concentration",
        "on-vine weather exposure",
        "mat drying and handling",
        "controlled-room airflow and humidity",
        "rot risk",
        "rate of drying",
        "freshness and flavour differences",
        "cost"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "water loss and concentration",
          "on-vine weather exposure",
          "mat drying and handling",
          "controlled-room airflow and humidity",
          "rot risk",
          "rate of drying",
          "freshness and flavour differences",
          "cost"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_121",
      "source_question_id": "OR_121",
      "stem": "Recommend a method for retaining residual sugar in a non-fortified sweet wine and justify the controls needed after fermentation stops.",
      "topic": "non_fortified_sweet_wine_fermentation_stop",
      "RA": "RA2",
      "command_verb": "recommend",
      "expected_concepts": [
        "fermentation interruption or natural arrest",
        "temperature reduction",
        "yeast removal by filtration",
        "sulfur dioxide where appropriate",
        "residual sugar target",
        "microbial stability",
        "balanced style"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "fermentation interruption or natural arrest",
          "temperature reduction",
          "yeast removal by filtration",
          "sulfur dioxide where appropriate",
          "residual sugar target",
          "microbial stability",
          "balanced style"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_122",
      "source_question_id": "OR_122",
      "stem": "Identify the concentration mechanisms used in botrytised and passito wines and explain how each mechanism changes grape composition before fermentation.",
      "topic": "botrytis_passito_concentration_mechanisms",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "Botrytis perforates berry skins",
        "water evaporation",
        "grape drying by air and time",
        "concentration of sugar and acid",
        "flavour transformation",
        "reduced juice yield",
        "different microbial and oxidation risks"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Botrytis perforates berry skins",
          "water evaporation",
          "grape drying by air and time",
          "concentration of sugar and acid",
          "flavour transformation",
          "reduced juice yield",
          "different microbial and oxidation risks"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_123",
      "source_question_id": "OR_123",
      "stem": "Describe how pressing, fermentation, blending, and maturation choices create the final style of Sauternes.",
      "topic": "sauternes_style_creation",
      "RA": "RA2",
      "command_verb": "describe",
      "expected_concepts": [
        "low juice yield from botrytised grapes",
        "difficult pressing",
        "high-sugar fermentation",
        "retained residual sugar",
        "lot selection and blending",
        "oak maturation",
        "high acidity balancing sweetness"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "low juice yield from botrytised grapes",
          "difficult pressing",
          "high-sugar fermentation",
          "retained residual sugar",
          "lot selection and blending",
          "oak maturation",
          "high acidity balancing sweetness"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_124",
      "source_question_id": "OR_124",
      "stem": "Explain why high acidity is essential to the balance and ageing potential of concentrated non-fortified sweet wines.",
      "topic": "sweet_wine_acidity_balance_ageing",
      "RA": "RA2",
      "command_verb": "explain",
      "expected_concepts": [
        "sweetness can feel cloying without acidity",
        "acidity provides freshness",
        "structural balance",
        "preservation and ageing",
        "concentrated flavour",
        "long finish",
        "style quality depends on integration rather than sugar alone"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "sweetness can feel cloying without acidity",
          "acidity provides freshness",
          "structural balance",
          "preservation and ageing",
          "concentrated flavour",
          "long finish",
          "style quality depends on integration rather than sugar alone"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_125",
      "source_question_id": "OR_125",
      "stem": "Compare the production and maturation choices that distinguish Ruby-style Port from Tawny-style Port.",
      "topic": "port_ruby_tawny_comparison",
      "RA": "RA4",
      "command_verb": "compare",
      "expected_concepts": [
        "fortification during fermentation",
        "fruit preservation in Ruby styles",
        "limited oxygen exposure",
        "extended oxidative cask ageing for Tawny",
        "colour change",
        "primary fruit versus nut and dried-fruit character",
        "blending and category style"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "fortification during fermentation",
          "fruit preservation in Ruby styles",
          "limited oxygen exposure",
          "extended oxidative cask ageing for Tawny",
          "colour change",
          "primary fruit versus nut and dried-fruit character",
          "blending and category style"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_126",
      "source_question_id": "OR_126",
      "stem": "Assess whether a high-quality, structured Port should be released as Late Bottled Vintage or held for declaration as Vintage Port.",
      "topic": "port_lbv_vintage_category_decision",
      "RA": "RA4",
      "command_verb": "assess",
      "expected_concepts": [
        "vintage quality and concentration",
        "producer declaration decision",
        "cask ageing duration",
        "filtration and readiness",
        "bottle ageing requirement",
        "commercial timing",
        "style and longevity judgement"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "vintage quality and concentration",
          "producer declaration decision",
          "cask ageing duration",
          "filtration and readiness",
          "bottle ageing requirement",
          "commercial timing",
          "style and longevity judgement"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_127",
      "source_question_id": "OR_127",
      "stem": "Evaluate the production decisions required to make Fino rather than Oloroso Sherry.",
      "topic": "sherry_fino_oloroso_production_decisions",
      "RA": "RA4",
      "command_verb": "evaluate",
      "expected_concepts": [
        "base wine assessment",
        "fortification strength",
        "flor survival for Fino",
        "higher fortification prevents flor for Oloroso",
        "biological versus oxidative ageing",
        "solera maturation",
        "style consequences"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "base wine assessment",
          "fortification strength",
          "flor survival for Fino",
          "higher fortification prevents flor for Oloroso",
          "biological versus oxidative ageing",
          "solera maturation",
          "style consequences"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_128",
      "source_question_id": "OR_128",
      "stem": "Discuss how flor management and the solera system contribute to consistency and complexity in biologically aged Sherry.",
      "topic": "sherry_flor_solera_consistency",
      "RA": "RA4",
      "command_verb": "discuss",
      "expected_concepts": [
        "partially filled vessels",
        "flor protection from oxidation",
        "acetaldehyde-derived character",
        "fractional blending",
        "refreshing younger wine",
        "consistency across releases",
        "complexity from prolonged maturation"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "partially filled vessels",
          "flor protection from oxidation",
          "acetaldehyde-derived character",
          "fractional blending",
          "refreshing younger wine",
          "consistency across releases",
          "complexity from prolonged maturation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_129",
      "source_question_id": "OR_129",
      "stem": "Recommend a production and maturation approach for a Madeira producer seeking a medium-dry style with freshness and controlled oxidative complexity.",
      "topic": "madeira_medium_dry_production_recommendation",
      "RA": "RA4",
      "command_verb": "recommend",
      "expected_concepts": [
        "appropriate grape or sweetness target",
        "timing of fortification",
        "retention of high acidity",
        "estufagem or canteiro choice",
        "controlled heat and oxygen exposure",
        "maturation duration",
        "balance of freshness and oxidative character"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "appropriate grape or sweetness target",
          "timing of fortification",
          "retention of high acidity",
          "estufagem or canteiro choice",
          "controlled heat and oxygen exposure",
          "maturation duration",
          "balance of freshness and oxidative character"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_130",
      "source_question_id": "OR_130",
      "stem": "Identify the principal Madeira style categories from dry to sweet and explain how production choices support those differences.",
      "topic": "madeira_style_categories",
      "RA": "RA4",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "Sercial dry",
        "Verdelho medium-dry",
        "Bual medium-sweet",
        "Malmsey sweet",
        "fortification timing",
        "residual sugar",
        "high acidity",
        "heat and oxidative maturation"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Sercial dry",
          "Verdelho medium-dry",
          "Bual medium-sweet",
          "Malmsey sweet",
          "fortification timing",
          "residual sugar",
          "high acidity",
          "heat and oxidative maturation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_131",
      "source_question_id": "OR_131",
      "stem": "Describe how the timing and purpose of fortification differ between Port and dry Sherry production.",
      "topic": "port_sherry_fortification_timing",
      "RA": "RA4",
      "command_verb": "describe",
      "expected_concepts": [
        "Port fortified during fermentation",
        "yeast activity stops",
        "residual sugar retained",
        "Sherry base wine fermented dry first",
        "post-fermentation fortification",
        "fortification level directs ageing style",
        "different final sweetness and structure"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Port fortified during fermentation",
          "yeast activity stops",
          "residual sugar retained",
          "Sherry base wine fermented dry first",
          "post-fermentation fortification",
          "fortification level directs ageing style",
          "different final sweetness and structure"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_132",
      "source_question_id": "OR_132",
      "stem": "Explain how grape drying, fermentation arrest, and oxidative maturation create the concentrated style of Rutherglen Muscat.",
      "topic": "rutherglen_muscat_style_creation",
      "RA": "RA4",
      "command_verb": "explain",
      "expected_concepts": [
        "very ripe or partially raisined Muscat grapes",
        "high sugar concentration",
        "fortification stops fermentation",
        "high residual sugar",
        "warm oxidative maturation",
        "blending across ages",
        "rich dried-fruit and caramel character"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "very ripe or partially raisined Muscat grapes",
          "high sugar concentration",
          "fortification stops fermentation",
          "high residual sugar",
          "warm oxidative maturation",
          "blending across ages",
          "rich dried-fruit and caramel character"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_133",
      "source_question_id": "OR_133",
      "stem": "Compare how you would serve Tokaji Aszú and Sauternes to customers, considering temperature, glass size, portion, and explanation of style.",
      "topic": "tokaji_sauternes_service_comparison",
      "RA": "RA5",
      "command_verb": "compare",
      "expected_concepts": [
        "cool service temperature",
        "small suitable glass",
        "modest portion",
        "high sweetness and acidity",
        "aromatic intensity",
        "age and complexity explanation",
        "customer preference"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "cool service temperature",
          "small suitable glass",
          "modest portion",
          "high sweetness and acidity",
          "aromatic intensity",
          "age and complexity explanation",
          "customer preference"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_134",
      "source_question_id": "OR_134",
      "stem": "Assess the storage and decanting plan for a mature Vintage Port with substantial sediment that will be served this evening.",
      "topic": "mature_vintage_port_storage_decanting",
      "RA": "RA5",
      "command_verb": "assess",
      "expected_concepts": [
        "bottle storage before service",
        "allowing sediment to settle",
        "careful opening",
        "decanting from sediment",
        "service timing",
        "appropriate temperature",
        "monitoring fragile mature aromas"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "bottle storage before service",
          "allowing sediment to settle",
          "careful opening",
          "decanting from sediment",
          "service timing",
          "appropriate temperature",
          "monitoring fragile mature aromas"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_135",
      "source_question_id": "OR_135",
      "stem": "Evaluate Icewine and Sauternes as pairings for a lemon tart, then recommend the more suitable option.",
      "topic": "icewine_sauternes_food_pairing",
      "RA": "RA5",
      "command_verb": "evaluate",
      "expected_concepts": [
        "wine should be at least as sweet as the dessert",
        "lemon acidity",
        "wine acidity and freshness",
        "flavour intensity",
        "botrytis and oak character in Sauternes",
        "clean fruit profile in Icewine",
        "reasoned recommendation"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "wine should be at least as sweet as the dessert",
          "lemon acidity",
          "wine acidity and freshness",
          "flavour intensity",
          "botrytis and oak character in Sauternes",
          "clean fruit profile in Icewine",
          "reasoned recommendation"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_136",
      "source_question_id": "OR_136",
      "stem": "Discuss how you would advise a customer choosing among dry, medium-dry, medium-sweet, and sweet Madeira styles.",
      "topic": "madeira_customer_advice",
      "RA": "RA5",
      "command_verb": "discuss",
      "expected_concepts": [
        "customer sweetness preference",
        "high acidity across styles",
        "aperitif versus dessert use",
        "food pairing",
        "age and complexity",
        "service temperature",
        "open-bottle stability"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "customer sweetness preference",
          "high acidity across styles",
          "aperitif versus dessert use",
          "food pairing",
          "age and complexity",
          "service temperature",
          "open-bottle stability"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_137",
      "source_question_id": "OR_137",
      "stem": "Recommend a serving sequence for Fino, Amontillado, and Pedro Ximénez Sherry during a multi-course meal.",
      "topic": "sherry_service_sequence",
      "RA": "RA5",
      "command_verb": "recommend",
      "expected_concepts": [
        "Fino first and well chilled",
        "dry light style with savoury starters",
        "Amontillado next with richer dishes",
        "Pedro Ximénez last with dessert or as dessert",
        "increasing sweetness and intensity",
        "appropriate glass and portion",
        "temperature adjustment"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Fino first and well chilled",
          "dry light style with savoury starters",
          "Amontillado next with richer dishes",
          "Pedro Ximénez last with dessert or as dessert",
          "increasing sweetness and intensity",
          "appropriate glass and portion",
          "temperature adjustment"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_138",
      "source_question_id": "OR_138",
      "stem": "Identify one expected oxidative character in mature Madeira or Oloroso Sherry and explain how to distinguish it from a wine fault when advising a customer.",
      "topic": "fortified_oxidative_character_fault_advice",
      "RA": "RA5",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "expected nutty dried-fruit or caramel character",
        "intentional oxidative maturation",
        "style consistency",
        "fault indicators such as unintended stale or acetic character",
        "condition and intensity assessment",
        "customer explanation",
        "replacement when genuinely faulty"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "expected nutty dried-fruit or caramel character",
          "intentional oxidative maturation",
          "style consistency",
          "fault indicators such as unintended stale or acetic character",
          "condition and intensity assessment",
          "customer explanation",
          "replacement when genuinely faulty"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_139",
      "source_question_id": "OR_139",
      "stem": "Explain how the duration of skin contact during fermentation affects the color, tannin extraction, and final style of a dry rosé wine.",
      "topic": "rosé_skin_contact_production",
      "RA": "RA2",
      "command_verb": "explain",
      "expected_concepts": [
        "brief skin contact during fermentation",
        "phenolic extraction from red grape skins",
        "color intensity from anthocyanin transfer",
        "tannin balance in rosé vs red wines",
        "timing of skin separation from must",
        "production method choice: saignée vs pressing",
        "final wine style: dry, fresh, or structured depending on contact duration"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "brief skin contact during fermentation",
          "phenolic extraction from red grape skins",
          "color intensity from anthocyanin transfer",
          "tannin balance in rosé vs red wines",
          "timing of skin separation from must",
          "production method choice: saignée vs pressing",
          "final wine style: dry, fresh, or structured depending on contact duration"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_140",
      "source_question_id": "OR_140",
      "stem": "Compare the production choices available for dry rosé wines in Provence, Navarra, and the Rhône Valley, and discuss how each region's climate influences those choices.",
      "topic": "rosé_regional_production_variation",
      "RA": "RA2",
      "command_verb": "compare",
      "expected_concepts": [
        "Provence: pale color, fresh, minimal oak, early harvest for acidity",
        "Navarra: deeper color, higher alcohol potential, longer skin contact, some oak aging",
        "Rhône/Tavel: darkest color, higher tannin, longer maceration, warm climate ripeness",
        "climate influence on ripe grape availability and harvest timing",
        "production method as region-specific convention",
        "oak aging decisions by region and market positioning",
        "acid preservation in hot climates"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Provence: pale color, fresh, minimal oak, early harvest for acidity",
          "Navarra: deeper color, higher alcohol potential, longer skin contact, some oak aging",
          "Rhône/Tavel: darkest color, higher tannin, longer maceration, warm climate ripeness",
          "climate influence on ripe grape availability and harvest timing",
          "production method as region-specific convention",
          "oak aging decisions by region and market positioning",
          "acid preservation in hot climates"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_141",
      "source_question_id": "OR_141",
      "stem": "Discuss the decanting decision for a young Vintage Port (5–10 years old) versus a mature Vintage Port (20+ years), considering sediment formation, oxidative aging, and the balance between tannin softening and aroma evolution.",
      "topic": "mature_port_decanting_strategy",
      "RA": "RA5",
      "command_verb": "discuss",
      "expected_concepts": [
        "Vintage Port sediment formation over decades",
        "tannin evolution in bottle: gradual softening and integration",
        "oxidative character development in fortified wine",
        "oxygen ingress through cork over long aging",
        "young Port: high tannin, benefit from aeration, minimal sediment",
        "mature Port: soft tannin, complex tertiary aromas, significant sediment",
        "decanting as a service choice: timing, vessel, duration",
        "preservation of aromatic complexity in old Port",
        "health and consumption safety in aged wine"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Vintage Port sediment formation over decades",
          "tannin evolution in bottle: gradual softening and integration",
          "oxidative character development in fortified wine",
          "oxygen ingress through cork over long aging",
          "young Port: high tannin, benefit from aeration, minimal sediment",
          "mature Port: soft tannin, complex tertiary aromas, significant sediment",
          "decanting as a service choice: timing, vessel, duration",
          "preservation of aromatic complexity in old Port",
          "health and consumption safety in aged wine"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_142",
      "source_question_id": "OR_142",
      "stem": "Compare the decanting and aeration strategy for a structured young Burgundy (Pinot Noir) with that of a young Bordeaux (Cabernet Sauvignon blend), considering differences in tannin structure, barrel-aging method, and aromatic volatility.",
      "topic": "burgundy_bordeaux_aeration_strategy",
      "RA": "RA5",
      "command_verb": "compare",
      "expected_concepts": [
        "Burgundy: smaller oak (225-liter puncheon), high-surface-area oxidation",
        "Bordeaux: large oak (225–500-liter barrel), slower oxidation",
        "Pinot Noir tannin structure: softer, integrated during barrel aging",
        "Cabernet tannin structure: firmer, requires longer aging for integration",
        "volatile aromatic compounds: fresh fruit in young wine, how aeration affects expression",
        "decanting duration: brief aeration vs. extended air exposure",
        "service glassware choice and aeration effect",
        "oxidation risk: controlled aeration vs. over-exposure"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Burgundy: smaller oak (225-liter puncheon), high-surface-area oxidation",
          "Bordeaux: large oak (225–500-liter barrel), slower oxidation",
          "Pinot Noir tannin structure: softer, integrated during barrel aging",
          "Cabernet tannin structure: firmer, requires longer aging for integration",
          "volatile aromatic compounds: fresh fruit in young wine, how aeration affects expression",
          "decanting duration: brief aeration vs. extended air exposure",
          "service glassware choice and aeration effect",
          "oxidation risk: controlled aeration vs. over-exposure"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_143",
      "source_question_id": "OR_143",
      "stem": "Assess a red wine with SAT appearance notes of 'pale-to-medium color with brownish edge.' Using production theory, explain what these observations suggest about the wine's age, production method, or storage history, and what causal mechanisms created those colors.",
      "topic": "sat_appearance_to_production_theory",
      "RA": "RA1",
      "command_verb": "assess",
      "expected_concepts": [
        "SAT appearance scale: pale to deep color intensity",
        "hue shift: bright red/purple (young) → garnet (mature) → brown (old)",
        "brownish edge as sign of oxidation in bottle over time",
        "pale color: light extraction, cool climate, lighter varietal, or sulfite protection during storage",
        "medium color with brown edge: moderately mature bottle, possible bottle oxidation or heat damage",
        "production method affecting initial color: carbonic maceration (lighter), long maceration (deeper)",
        "storage conditions: light exposure, temperature, cork condition, aging potential"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "SAT appearance scale: pale to deep color intensity",
          "hue shift: bright red/purple (young) → garnet (mature) → brown (old)",
          "brownish edge as sign of oxidation in bottle over time",
          "pale color: light extraction, cool climate, lighter varietal, or sulfite protection during storage",
          "medium color with brown edge: moderately mature bottle, possible bottle oxidation or heat damage",
          "production method affecting initial color: carbonic maceration (lighter), long maceration (deeper)",
          "storage conditions: light exposure, temperature, cork condition, aging potential"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_144",
      "source_question_id": "OR_144",
      "stem": "A white wine shows SAT nose notes of 'butter, cream, and vanilla alongside stone fruit.' Discuss the production choices that created these characteristics, and explain how malolactic fermentation and oak contact work together to produce this profile.",
      "topic": "sat_nose_to_mlf_oak_production",
      "RA": "RA2",
      "command_verb": "discuss",
      "expected_concepts": [
        "SAT nose categories: primary (varietal), secondary (fermentation), tertiary (aging)",
        "butter and cream notes: diacetyl from malolactic fermentation",
        "vanilla: oak contact (French oak typically smoother than American)",
        "stone fruit: primary varietal character (Chardonnay typical)",
        "malolactic fermentation as a deliberate production choice",
        "timing of MLF: in-barrel vs. pre-barrel, complete vs. partial",
        "oak contact: barrel type, new vs. used, duration",
        "microbial stability: MLF implications for pH and SO₂",
        "style intent: fruit-forward vs. creamy oxidative styles"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "SAT nose categories: primary (varietal), secondary (fermentation), tertiary (aging)",
          "butter and cream notes: diacetyl from malolactic fermentation",
          "vanilla: oak contact (French oak typically smoother than American)",
          "stone fruit: primary varietal character (Chardonnay typical)",
          "malolactic fermentation as a deliberate production choice",
          "timing of MLF: in-barrel vs. pre-barrel, complete vs. partial",
          "oak contact: barrel type, new vs. used, duration",
          "microbial stability: MLF implications for pH and SO₂",
          "style intent: fruit-forward vs. creamy oxidative styles"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_145",
      "source_question_id": "OR_145",
      "stem": "A Madeira wine shows oxidative characteristics in the nose and palate: dried fruit, nutty, and caramel notes. Explain how the intentional heating and oxidative aging that define Madeira production create these characteristics, and contrast them with oxidative defects that would indicate wine fault.",
      "topic": "madeira_oxidation_vs_fault_differentiation",
      "RA": "RA4",
      "command_verb": "explain",
      "expected_concepts": [
        "Madeira estufagem: controlled heat aging (warm room 45–50°C or heated wine tanks)",
        "oxidative ripening during estufagem: browning, oxidation of phenolics, Maillard reactions",
        "dried fruit, nut, caramel, chocolate notes as characteristic Madeira profile",
        "long-term bottle storage after estufagem: slow oxidation through cork",
        "fault indicators: sharpness, volatility, acetic acid (vinegar), cork taint (musty)",
        "maderization: unintended oxidation in still wine (a fault), vs. intentional in Madeira (desired)",
        "sensorial cues for distinguishing intentional from unintended oxidation",
        "food pairing implications: oxidative character enables food pairing that young wine cannot achieve"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "Madeira estufagem: controlled heat aging (warm room 45–50°C or heated wine tanks)",
          "oxidative ripening during estufagem: browning, oxidation of phenolics, Maillard reactions",
          "dried fruit, nut, caramel, chocolate notes as characteristic Madeira profile",
          "long-term bottle storage after estufagem: slow oxidation through cork",
          "fault indicators: sharpness, volatility, acetic acid (vinegar), cork taint (musty)",
          "maderization: unintended oxidation in still wine (a fault), vs. intentional in Madeira (desired)",
          "sensorial cues for distinguishing intentional from unintended oxidation",
          "food pairing implications: oxidative character enables food pairing that young wine cannot achieve"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_146",
      "source_question_id": "OR_146",
      "stem": "Recommend appropriate storage conditions (temperature, light, humidity, bottle position) for three different wine types: a young dry white wine for early consumption, a structured red wine intended for 10+ years aging, and a mature fortified wine (Tawny Port) purchased for immediate enjoyment.",
      "topic": "wine_storage_condition_recommendations",
      "RA": "RA5",
      "command_verb": "recommend",
      "expected_concepts": [
        "young white wine: cool (10–12°C), dark, short-term storage (months to 2 years), upright bottle position",
        "structured red wine for aging: consistent cool temperature (12–15°C), dark, horizontal position (cork must stay moist), humidity 50–80% for cork integrity",
        "Tawny Port: tolerant of temperature variation, lower UV sensitivity (oxidized already), upright position (ready to drink), shelf-stable",
        "temperature stability as critical factor: fluctuation causes expansion/contraction, cork movement, oxidation acceleration",
        "light exposure: UV-induced premature oxidation in white/light wines",
        "humidity: cork drying in low-humidity environments, cork rot in high humidity",
        "bottle position: cork contact critical for sealing; screw-cap and synthetic closures reduce this concern",
        "storage location suitability: wine fridge, cellar, closet vs. above radiator"
      ],
      "evaluation_config": {
        "verb_definition_key": "recommend",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "young white wine: cool (10–12°C), dark, short-term storage (months to 2 years), upright bottle position",
          "structured red wine for aging: consistent cool temperature (12–15°C), dark, horizontal position (cork must stay moist), humidity 50–80% for cork integrity",
          "Tawny Port: tolerant of temperature variation, lower UV sensitivity (oxidized already), upright position (ready to drink), shelf-stable",
          "temperature stability as critical factor: fluctuation causes expansion/contraction, cork movement, oxidation acceleration",
          "light exposure: UV-induced premature oxidation in white/light wines",
          "humidity: cork drying in low-humidity environments, cork rot in high humidity",
          "bottle position: cork contact critical for sealing; screw-cap and synthetic closures reduce this concern",
          "storage location suitability: wine fridge, cellar, closet vs. above radiator"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_147",
      "source_question_id": "OR_147",
      "stem": "A customer asks whether a wine is safe to drink given their concerns about sulfites, histamines, and high alcohol content. As a sommelier, describe how you would assess the customer's health needs, advise on wine selection criteria, and explain the science behind these constituents.",
      "topic": "health_allergen_customer_advice",
      "RA": "RA5",
      "command_verb": "describe",
      "expected_concepts": [
        "sulfite sensitivity: true allergy vs. sensitivity to high SO₂ levels",
        "SO₂ levels by wine type: sweet wines (higher), dry wines (lower), organic wines (variable)",
        "histamines: higher in red wine (skin contact) than white, accumulate with age and microbial activity",
        "high alcohol wines: above 15%, thermophilic yeast and sugar-to-alcohol conversion, sensorial warmth/burn",
        "alcohol sensitivity: individual variation, medications, health conditions",
        "customer intake: asking about specific symptoms, allergies, medications",
        "wine selection guidance: low-sulfite options, histamine-lower white wines, lower-alcohol alternatives (12–13%)",
        "transparent communication: limitations of sommelier role vs. medical advice",
        "labeling and transparency: SO₂ declarations (often mandatory in EU), histamine not required"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "sulfite sensitivity: true allergy vs. sensitivity to high SO₂ levels",
          "SO₂ levels by wine type: sweet wines (higher), dry wines (lower), organic wines (variable)",
          "histamines: higher in red wine (skin contact) than white, accumulate with age and microbial activity",
          "high alcohol wines: above 15%, thermophilic yeast and sugar-to-alcohol conversion, sensorial warmth/burn",
          "alcohol sensitivity: individual variation, medications, health conditions",
          "customer intake: asking about specific symptoms, allergies, medications",
          "wine selection guidance: low-sulfite options, histamine-lower white wines, lower-alcohol alternatives (12–13%)",
          "transparent communication: limitations of sommelier role vs. medical advice",
          "labeling and transparency: SO₂ declarations (often mandatory in EU), histamine not required"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    },
    {
      "item_id": "OR_148",
      "source_question_id": "OR_148",
      "stem": "Analyze how vintage variation in a classic region like Bordeaux (warm vs. cool year) influences the winemaker's production choices regarding harvest timing, fermentation temperature, malolactic fermentation, oak aging duration, and final blending decisions.",
      "topic": "regional_vintage_variation_production_adaptation",
      "RA": "RA2",
      "command_verb": "analyze",
      "expected_concepts": [
        "vintage definition: annual variation in growing conditions and harvest quality",
        "warm vintage: higher sugar ripeness, lower acid, ripe tannin, earlier harvest possible",
        "cool vintage: lower sugar, higher acid retention, greener tannin, delayed harvest risk",
        "harvest timing decision: balance ripeness against acid preservation",
        "fermentation temperature: control for yeast health and aroma expression",
        "malolactic fermentation: timing and extent as response to acid level and wine structure",
        "oak aging: duration adjustment (longer in cool vintage for structure integration, shorter in warm for balance)",
        "blending decision: varietal proportions adjusted by vintage character (more Cabernet in cool year for structure, more Merlot in warm year for softness)",
        "appellation regulations: constraint on flexibility (e.g., Bordeaux blending rules)"
      ],
      "evaluation_config": {
        "verb_definition_key": "analyze",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "response_depth_target": "strong"
        },
        "required_signals": [
          "vintage definition: annual variation in growing conditions and harvest quality",
          "warm vintage: higher sugar ripeness, lower acid, ripe tannin, earlier harvest possible",
          "cool vintage: lower sugar, higher acid retention, greener tannin, delayed harvest risk",
          "harvest timing decision: balance ripeness against acid preservation",
          "fermentation temperature: control for yeast health and aroma expression",
          "malolactic fermentation: timing and extent as response to acid level and wine structure",
          "oak aging: duration adjustment (longer in cool vintage for structure integration, shorter in warm for balance)",
          "blending decision: varietal proportions adjusted by vintage character (more Cabernet in cool year for structure, more Merlot in warm year for softness)",
          "appellation regulations: constraint on flexibility (e.g., Bordeaux blending rules)"
        ],
        "forbidden_signals": [
          "mark",
          "score",
          "percentage",
          "pass_fail",
          "wset_equivalence",
          "examiner_judgement",
          "official_grade"
        ],
        "source": "open_response_bank_v1"
      }
    }
  ],
  "evaluation_by_item_id": {
    "OR_001": {
      "item_id": "OR_001",
      "source_question_id": "OR_001",
      "expected_concepts": [
        "certificación orgánica o sostenible",
        "aumento de costes de producción",
        "mano de obra intensiva",
        "rendimientos más bajos",
        "diferenciación en el mercado",
        "valor percibido por el consumidor",
        "precio premium"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Tu respuesta menciona la sostenibilidad pero no explica el mecanismo económico. Necesitas conectar las prácticas específicas (mayor mano de obra, menores rendimientos) con el aumento de costes, y luego explicar cómo esos costes se recuperan mediante diferenciación comercial y precios premium.",
        "DEVELOPING_RESPONSE": "Buen intento. Identificas el vínculo entre prácticas sostenibles y coste, pero la explicación del mecanismo de diferenciación comercial necesita más detalle. Considera cómo la certificación funciona como señal de valor para el consumidor y justifica un precio mayor.",
        "STRONG_RESPONSE": "Respuesta sólida que conecta las prácticas sostenibles con sus implicaciones económicas y de posicionamiento comercial."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_002": {
      "item_id": "OR_002",
      "source_question_id": "OR_002",
      "expected_concepts": [
        "conversión de ácido málico a ácido láctico",
        "reducción de la acidez total",
        "perfil de acidez más suave",
        "mayor textura y cuerpo",
        "notas cremosas o mantecosas (diacetilo)",
        "adecuación para estilos con crianza en roble",
        "inapropiada para estilos frescos y aromáticos"
      ],
      "optional_causal_chain": "CC_MLF_ACIDITY -> CC_MLF_TEXTURE -> CC_MLF_DIACETYL",
      "causal_chain_reference": [
        "CC_MLF_ACIDITY",
        "CC_MLF_TEXTURE",
        "CC_MLF_DIACETYL"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identificas la FML pero no explicas el mecanismo. Una respuesta completa debe explicar la conversión de ácido málico a láctico, el cambio en el perfil de acidez, y por qué eso es deseable en ciertos estilos de vino blanco (como Chardonnay con crianza en roble) pero no en otros.",
        "DEVELOPING_RESPONSE": "Buen fundamento. Mencionas la reducción de acidez, pero profundiza en la textura y el diacetilo como aspectos adicionales, y en los estilos para los que la FML es apropiada o inapropiada.",
        "STRONG_RESPONSE": "Respuesta completa: cubre el mecanismo causal, el impacto en acidez y textura, y la lógica de estilo que justifica su uso selectivo."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_003": {
      "item_id": "OR_003",
      "source_question_id": "OR_003",
      "expected_concepts": [
        "temperaturas más bajas a mayor altitud",
        "maduración más lenta",
        "mayor retención de acidez",
        "menor contenido alcohólico",
        "aromas más frescos y primarios",
        "mayor variación diurna de temperatura"
      ],
      "optional_causal_chain": "CC_COOL_CLIMATE_ACIDITY -> CC_COOL_CLIMATE_ALCOHOL -> CC_COOL_CLIMATE_AROMA",
      "causal_chain_reference": [
        "CC_COOL_CLIMATE_ACIDITY",
        "CC_COOL_CLIMATE_ALCOHOL",
        "CC_COOL_CLIMATE_AROMA"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas que la altitud afecta el clima, pero necesitas explicar el mecanismo: temperaturas más bajas → maduración más lenta → mayor retención de acidez y menor alcohol. Incluye cómo esto afecta el estilo del vino tinto.",
        "DEVELOPING_RESPONSE": "Buen enfoque. Conectas la altitud con el clima y el estilo. Para profundizar, explica la variación diurna de temperatura como factor adicional que preserva aromas frescos en regiones cálidas.",
        "STRONG_RESPONSE": "Respuesta completa: cubre el mecanismo temperatura → maduración → acidez/alcohol/aroma, con referencia a la variación diurna como efecto adicional."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_004": {
      "item_id": "OR_004",
      "source_question_id": "OR_004",
      "expected_concepts": [
        "orientación sur (hemisferio norte) maximiza exposición solar",
        "mayor ángulo de incidencia de la luz",
        "mayor acumulación de calor en la uva",
        "pendiente favorece el drenaje",
        "pendiente reduce el riesgo de heladas (aire frío drena)",
        "efecto sobre ritmo de maduración"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas la orientación pero no explicas el mecanismo. Necesitas conectar: orientación sur → mayor exposición solar → mayor calor → maduración más rápida. La pendiente tiene un efecto adicional sobre el drenaje del aire frío y la reducción de heladas.",
        "DEVELOPING_RESPONSE": "Buen enfoque sobre la exposición solar. Para completar la respuesta, añade el efecto de la pendiente sobre el drenaje del aire frío (reducción del riesgo de heladas) y el drenaje del agua.",
        "STRONG_RESPONSE": "Respuesta completa: cubre exposición solar, acumulación de calor, drenaje del aire y del agua como factores que la orientación y pendiente controlan."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_005": {
      "item_id": "OR_005",
      "source_question_id": "OR_005",
      "expected_concepts": [
        "uso de sulfitos (SO₂) como antioxidante",
        "protección con gas inerte (nitrógeno, CO₂ argón)",
        "control de temperatura en fermentación y almacenamiento",
        "uso de depósitos de acero inoxidable",
        "manipulación cuidadosa para evitar contacto con oxígeno",
        "llenado completo de depósitos"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas el control de oxígeno pero sin especificar prácticas. Una respuesta completa incluye: uso de sulfitos, gases inertes, temperatura baja, minimización del contacto con el aire durante trasiegos y llenado.",
        "DEVELOPING_RESPONSE": "Buen intento. Cubre la protección con SO₂ o gases inertes. Para completar, añade cómo el control de temperatura y el llenado completo de depósitos minimizan el riesgo residual.",
        "STRONG_RESPONSE": "Respuesta completa que identifica múltiples mecanismos de protección antioxidante y su lógica."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_006": {
      "item_id": "OR_006",
      "source_question_id": "OR_006",
      "expected_concepts": [
        "levaduras producen compuestos aromáticos secundarios",
        "ésteres y alcoholes superiores según cepa",
        "producción de diacetilo en algunas cepas",
        "levaduras neutras vs levaduras aromáticas",
        "efecto sobre intensidad y complejidad aromática",
        "influencia sobre carácter frutal o floral"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas que las levaduras afectan el aroma, pero necesitas especificar qué compuestos producen y cómo distintas cepas generan perfiles diferentes (ésteres vs diacetilo vs carácter neutro).",
        "DEVELOPING_RESPONSE": "Buen enfoque. Identificas el vínculo levaduras–aromas. Para profundizar, menciona compuestos específicos (ésteres, alcoholes superiores) y la diferencia entre levaduras neutras y aromáticas.",
        "STRONG_RESPONSE": "Respuesta completa: identifica compuestos aromáticos específicos, distingue entre tipos de levaduras y conecta la elección con el estilo final del vino."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_007": {
      "item_id": "OR_007",
      "source_question_id": "OR_007",
      "expected_concepts": [
        "buen drenaje restringe disponibilidad de agua",
        "estrés hídrico moderado reduce vigor vegetativo",
        "menor vigor concentra energía en el fruto",
        "bayas más pequeñas y concentradas",
        "vinos con mayor concentración de compuestos",
        "suelos con mal drenaje favorecen vigor excesivo"
      ],
      "optional_causal_chain": "CC_SOIL_DRAINAGE_VINE_VIGOUR",
      "causal_chain_reference": [
        "CC_SOIL_DRAINAGE_VINE_VIGOUR"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas el drenaje del suelo pero no explicas el mecanismo causal completo: drenaje → disponibilidad de agua → vigor de la vid → concentración de bayas → estilo del vino. Necesitas conectar estos eslabones.",
        "DEVELOPING_RESPONSE": "Buen intento. Conectas el drenaje con el vigor. Para completar, explica cómo el menor vigor concentra la energía de la vid en el fruto y qué efectos tiene en el estilo del vino.",
        "STRONG_RESPONSE": "Respuesta completa que articula la cadena causal drenaje → agua → vigor → concentración → estilo."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_008": {
      "item_id": "OR_008",
      "source_question_id": "OR_008",
      "expected_concepts": [
        "roble americano: grano más abierto, mayor extracción de aromas",
        "roble americano: notas de coco, vainilla, eneldo más pronunciadas",
        "roble francés: grano más fino, extracción más sutil",
        "roble francés: notas especiadas y tostadas más elegantes",
        "tanino de roble americano más duro inicialmente",
        "micro-oxigenación diferente según porosidad del grano",
        "integración más rápida del roble americano en algunos estilos"
      ],
      "optional_causal_chain": "CC_OAK_FLAVOUR -> CC_OAK_TANNIN -> CC_OAK_MICROOX",
      "causal_chain_reference": [
        "CC_OAK_FLAVOUR",
        "CC_OAK_TANNIN",
        "CC_OAK_MICROOX"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas diferencias entre roble americano y francés, pero necesitas especificar el mecanismo (grano abierto vs fino), los compuestos aromáticos distintos (coco y vainilla vs especias) y el impacto diferente en el tanino y la micro-oxigenación.",
        "DEVELOPING_RESPONSE": "Buen enfoque comparativo. Para llegar a strong, profundiza en cómo la estructura del grano determina la tasa de extracción y cómo esto afecta la integración del roble según el estilo de vino.",
        "STRONG_RESPONSE": "Respuesta completa: compara los mecanismos de extracción, los perfiles aromáticos y el impacto en tanino y micro-oxigenación de cada tipo de roble."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_009": {
      "item_id": "OR_009",
      "source_question_id": "OR_009",
      "expected_concepts": [
        "deshojar (leaf removal): mayor exposición solar y aireación de racimos",
        "deshojado reduce humedad y riesgo de enfermedades fúngicas",
        "poda en verde (green harvest): reducción de carga de fruta",
        "poda en verde concentra compuestos en las bayas restantes",
        "levantamiento de pámpanos (shoot positioning)",
        "mejora de madurez y sanidad de la uva"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas técnicas de dosel pero sin explicar el beneficio. Necesitas describir la técnica específica (qué se hace) y el resultado (por qué beneficia la maduración o la sanidad).",
        "DEVELOPING_RESPONSE": "Describes las técnicas correctamente. Para completar, conecta cada técnica con su mecanismo: cómo el deshojado reduce la humedad y mejora la exposición, o cómo la poda en verde concentra compuestos.",
        "STRONG_RESPONSE": "Respuesta completa: describe dos técnicas con su mecanismo causal y el beneficio concreto sobre madurez, sanidad o concentración."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_010": {
      "item_id": "OR_010",
      "source_question_id": "OR_010",
      "expected_concepts": [
        "riego de precisión evita estrés hídrico excesivo",
        "mantenimiento de la función fotosintética en calor extremo",
        "deshojado en la cara este reduce exposición al calor de la tarde",
        "dosel proporciona sombra que modera la temperatura del racimo",
        "balance entre madurez y preservación de acidez",
        "riego excesivo puede causar vigor y dilución"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas el riego y el dosel pero sin explicar cómo cada uno actúa sobre el problema del calor o la sequía. Necesitas conectar cada práctica con su mecanismo de protección (riego → hidratación → función fotosintética; dosel → sombra → temperatura del racimo).",
        "DEVELOPING_RESPONSE": "Buen enfoque. Cubre uno de los dos mecanismos. Para una respuesta strong, explica ambos (riego y dosel) con sus mecanismos específicos y menciona el riesgo de exceso de riego (dilución).",
        "STRONG_RESPONSE": "Respuesta completa que explica riego y dosel como complementos, con el mecanismo de cada uno y las limitaciones del exceso."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_011": {
      "item_id": "OR_011",
      "source_question_id": "OR_011",
      "expected_concepts": [
        "alta densidad: competencia por agua y nutrientes entre vides",
        "competencia induce estrés hídrico moderado y mayor concentración",
        "raíces más profundas en alta densidad",
        "alta densidad aumenta costo (más plantas, más labores)",
        "baja densidad: mecanización más fácil, menor costo",
        "relación densidad–rendimiento–concentración–precio del vino"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas la densidad pero sin explicar el mecanismo económico o el efecto sobre el estilo. Necesitas articular: alta densidad → competencia → estrés → concentración → calidad potencial; y: más plantas → mayor costo de establecimiento y labor.",
        "DEVELOPING_RESPONSE": "Buena base. Conectas la densidad con la competencia o el costo. Para strong, integra ambas dimensiones: el efecto de la competencia en el estilo del vino Y el impacto económico de mayor vs menor densidad.",
        "STRONG_RESPONSE": "Respuesta completa que articula el mecanismo de competencia, el efecto sobre el estilo del vino y la implicación económica de cada elección."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_012": {
      "item_id": "OR_012",
      "source_question_id": "OR_012",
      "expected_concepts": [
        "levaduras seleccionadas: mayor control y consistencia de resultado",
        "levaduras seleccionadas: perfil aromático predecible",
        "levaduras autóctonas: mayor complejidad y carácter de terroir",
        "levaduras autóctonas: mayor riesgo de fermentación atascada",
        "levaduras autóctonas: producción de compuestos no deseados",
        "elección condicionada por el estilo objetivo del viticultor"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas los dos tipos de levaduras pero sin comparar sus características en detalle. Una respuesta completa requiere: control vs complejidad, consistencia vs riesgo, y los casos en que cada tipo es preferible.",
        "DEVELOPING_RESPONSE": "Buena comparación parcial. Cubre control y riesgo. Para strong, añade la dimensión de complejidad aromática vs terroir que ofrecen las autóctonas, y la lógica comercial detrás de cada elección.",
        "STRONG_RESPONSE": "Respuesta completa que compara los cuatro ejes (control, consistencia, complejidad, riesgo) con ejemplos o contextos de aplicación."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_013": {
      "item_id": "OR_013",
      "source_question_id": "OR_013",
      "expected_concepts": [
        "estrés hídrico moderado reduce tamaño de bayas",
        "mayor proporción de piel respecto al volumen total",
        "concentración de compuestos (color, tanino, azúcar)",
        "menor rendimiento por hectárea",
        "menor rendimiento aumenta coste de producción",
        "mayor concentración puede justificar precio más alto",
        "límite: estrés severo daña la vid y reduce calidad"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas el estrés hídrico y la concentración pero sin articular la cadena completa. Necesitas conectar: estrés → bayas pequeñas → mayor piel/volumen → concentración → menor rendimiento → mayor coste → precio potencialmente más alto.",
        "DEVELOPING_RESPONSE": "Buen análisis de la concentración. Para strong, añade el vínculo económico: cómo el menor rendimiento afecta el coste y cómo la mayor concentración puede (pero no automáticamente) justificar un precio premium.",
        "STRONG_RESPONSE": "Análisis completo: mecanismo físico de concentración, impacto en rendimiento y coste, y lógica de precio premium con la advertencia del estrés excesivo."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_014": {
      "item_id": "OR_014",
      "source_question_id": "OR_014",
      "expected_concepts": [
        "latitud baja: mayor irradiación solar y temperaturas cálidas",
        "altitud compensa el calor mediante temperaturas más bajas",
        "variación diurna de temperatura en viñedos de altitud",
        "retención de acidez a mayor altitud",
        "menor acumulación de azúcar y menor alcohol potencial",
        "aromas más frescos en vinos de altitud en clima cálido"
      ],
      "optional_causal_chain": "CC_COOL_CLIMATE_ACIDITY -> CC_COOL_CLIMATE_ALCOHOL",
      "causal_chain_reference": [
        "CC_COOL_CLIMATE_ACIDITY",
        "CC_COOL_CLIMATE_ALCOHOL"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas latitud y altitud, pero sin explicar cómo interactúan. En un clima cálido, la altitud puede compensar el calor de la latitud baja. Necesitas explicar el mecanismo: altitud → menor temperatura → maduración más lenta → acidez y aromas frescos.",
        "DEVELOPING_RESPONSE": "Buen enfoque sobre la compensación altitudinal. Para profundizar, añade la variación diurna de temperatura como factor adicional que preserva acidez y aromas en climas cálidos a altitud.",
        "STRONG_RESPONSE": "Respuesta completa: articula la interacción latitud–altitud con sus efectos sobre temperatura, acidez, alcohol y carácter aromático."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_015": {
      "item_id": "OR_015",
      "source_question_id": "OR_015",
      "expected_concepts": [
        "estrés hídrico moderado reduce crecimiento vegetativo",
        "menor vigor concentra energía en el fruto",
        "bayas más pequeñas con menor contenido de agua",
        "mayor relación piel/pulpa",
        "mayor concentración de antocianos, taninos y azúcares",
        "distinción entre estrés moderado (beneficioso) y severo (dañino)"
      ],
      "optional_causal_chain": "CC_SOIL_DRAINAGE_VINE_VIGOUR",
      "causal_chain_reference": [
        "CC_SOIL_DRAINAGE_VINE_VIGOUR"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas el estrés hídrico pero sin articular el mecanismo. Necesitas explicar: estrés moderado → menor crecimiento vegetativo → energía hacia el fruto → bayas más pequeñas → mayor concentración. Y distinguir esto del estrés severo.",
        "DEVELOPING_RESPONSE": "Buena explicación del mecanismo de concentración. Para profundizar, añade la distinción entre estrés moderado (beneficioso) y severo (daña la fotosíntesis y la maduración).",
        "STRONG_RESPONSE": "Respuesta completa: articula el mecanismo causal y distingue claramente entre los efectos del estrés moderado y del severo."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_016": {
      "item_id": "OR_016",
      "source_question_id": "OR_016",
      "expected_concepts": [
        "fermentación atascada (stuck fermentation)",
        "producción de compuestos no deseados (ácido acético, etil acetato)",
        "inconsistencia entre cosechas",
        "menor tolerancia al alcohol de algunas cepas autóctonas"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Menciona un riesgo válido, pero sin explicar por qué ocurre. Por ejemplo: la fermentación atascada ocurre porque las levaduras autóctonas pueden no tolerar altos niveles de alcohol o no ser competitivas frente a otras.",
        "DEVELOPING_RESPONSE": "Identificas el riesgo y su causa. Para profundizar, añade una consecuencia práctica para el vino resultante.",
        "STRONG_RESPONSE": "Respuesta completa: identifica el riesgo, explica el mecanismo y la consecuencia sobre el vino."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_017": {
      "item_id": "OR_017",
      "source_question_id": "OR_017",
      "expected_concepts": [
        "control del rendimiento de la vid",
        "gestión del vigor vegetativo",
        "determinación del número de yemas productivas",
        "equilibrio entre producción y calidad",
        "eliminación de madera vieja o enferma",
        "preparación de la estructura de la vid para la temporada"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas la poda pero sin explicar la justificación específica. Necesitas conectar: poda en invierno → control de yemas → control del rendimiento → equilibrio calidad/cantidad.",
        "DEVELOPING_RESPONSE": "Buen enfoque sobre el control del rendimiento. Para completar, añade el objetivo de la poda sobre la estructura de la vid y la eliminación de madera vieja.",
        "STRONG_RESPONSE": "Justificación completa: control de rendimiento, gestión del vigor, preparación estructural de la vid para la temporada siguiente."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_018": {
      "item_id": "OR_018",
      "source_question_id": "OR_018",
      "expected_concepts": [
        "control preciso de temperatura",
        "fermentación a temperatura baja preserva aromas primarios",
        "material neutro: no añade aromas al vino",
        "facilidad de limpieza y control de higiene",
        "preservación de la frescura y el carácter frutal"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas un beneficio, pero sin explicar el mecanismo. Por ejemplo: el control de temperatura → fermentación lenta y fría → preservación de aromas volátiles primarios → vino más fresco y frutal.",
        "DEVELOPING_RESPONSE": "Identificas el beneficio y la causa. Para completar, añade el efecto específico sobre el estilo del vino.",
        "STRONG_RESPONSE": "Respuesta completa: beneficio técnico identificado, mecanismo explicado y efecto sobre el estilo del vino."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_019": {
      "item_id": "OR_019",
      "source_question_id": "OR_019",
      "expected_concepts": [
        "mayor extracción de antocianos (color)",
        "mayor extracción de taninos de pepitas y hollejo",
        "taninos pueden volverse más duros si la extracción es excesiva",
        "mayor estructura y potencial de envejecimiento",
        "riesgo de amargor o astringencia excesiva",
        "adecuación para estilos de guarda, no para vinos de consumo temprano"
      ],
      "optional_causal_chain": "CC_MACERATION_EXTRACTION",
      "causal_chain_reference": [
        "CC_MACERATION_EXTRACTION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas más color y tanino, pero necesitas analizar los efectos positivos y negativos: mayor extracción puede dar estructura y potencial de envejecimiento, pero el exceso produce amargor o astringencia. La adecuación depende del estilo objetivo.",
        "DEVELOPING_RESPONSE": "Buen análisis de la extracción. Para strong, añade la distinción entre extracción adecuada (estructura, color) y excesiva (astringencia, amargor), y cómo el tiempo de maceración se usa como herramienta de estilo.",
        "STRONG_RESPONSE": "Análisis completo: mecanismo de extracción, efectos positivos y negativos, y lógica de estilo que determina la duración de la maceración."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_020": {
      "item_id": "OR_020",
      "source_question_id": "OR_020",
      "expected_concepts": [
        "suelo arenoso: buen drenaje, baja retención de agua",
        "suelo arenoso: estrés hídrico moderado, bayas concentradas",
        "suelo arcilloso: alta retención de agua",
        "suelo arcilloso: mayor disponibilidad hídrica, mayor vigor potencial",
        "mayor vigor puede diluir compuestos y reducir concentración",
        "suelo arenoso: barrera contra Phylloxera (histórico)"
      ],
      "optional_causal_chain": "CC_SOIL_DRAINAGE_VINE_VIGOUR",
      "causal_chain_reference": [
        "CC_SOIL_DRAINAGE_VINE_VIGOUR"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas los tipos de suelo pero sin comparar sus efectos de manera estructurada. Necesitas contrastar: arena (drenaje → estrés → concentración) vs arcilla (retención → vigor → dilución potencial) y el efecto de cada uno en el estilo del vino.",
        "DEVELOPING_RESPONSE": "Buena comparación sobre drenaje y vigor. Para profundizar, añade cómo el diferente vigor en cada suelo se traduce en características distintas del vino (estructura, concentración, alcohol).",
        "STRONG_RESPONSE": "Comparación completa: mecanismo de drenaje y retención, efecto sobre vigor, y consecuencias en el estilo del vino para cada tipo de suelo."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_021": {
      "item_id": "OR_021",
      "source_question_id": "OR_021",
      "expected_concepts": [
        "Barossa Valley",
        "Shiraz/Syrah",
        "clima cálido",
        "gran concentración",
        "notas especiadas y de fruta madura"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Correcto al identificar Barossa Valley. Añade que su clima cálido produce Shiraz de gran concentración y notas de fruta madura y especias.",
        "DEVELOPING_RESPONSE": "Buena identificación. Incorpora el vínculo entre el clima cálido continental del Barossa y el perfil del Shiraz para completar la explicación.",
        "STRONG_RESPONSE": "Respuesta sólida: identifica Barossa Valley, vincula el clima cálido con el estilo del Shiraz y describe sus características de concentración y perfil especiado."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_022": {
      "item_id": "OR_022",
      "source_question_id": "OR_022",
      "expected_concepts": [
        "crus como viñedos clasificados",
        "clasificación por calidad del terroir",
        "Borgoña",
        "Premier Cru / Grand Cru"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Mencionas los crus pero no explicas su significado. Los crus son viñedos clasificados según la calidad del terroir; en la Borgoña se distinguen Premier Cru y Grand Cru.",
        "DEVELOPING_RESPONSE": "Buen comienzo. Añade que los crus representan una jerarquía de calidad basada en el terroir y que la Borgoña es la región más conocida por este sistema.",
        "STRONG_RESPONSE": "Respuesta sólida: explica el concepto de cru como viñedo clasificado por calidad de terroir, menciona la Borgoña y distingue los niveles Premier Cru y Grand Cru."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_023": {
      "item_id": "OR_023",
      "source_question_id": "OR_023",
      "expected_concepts": [
        "Gran Reserva como categoría de crianza prolongada",
        "mínimo 5 años totales",
        "al menos 18 meses en barrica",
        "Ribera del Duero o Rioja"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identificas Gran Reserva como categoría de larga crianza, pero necesitas especificar los requisitos mínimos de tiempo y mencionar una denominación.",
        "DEVELOPING_RESPONSE": "Buen intento. Añade los tiempos mínimos de crianza y menciona Rioja o Ribera del Duero como denominación que aplica esta categoría.",
        "STRONG_RESPONSE": "Respuesta completa: define Gran Reserva con sus tiempos mínimos de crianza y menciona una región española que regula esta categoría."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_024": {
      "item_id": "OR_024",
      "source_question_id": "OR_024",
      "expected_concepts": [
        "Rioja Reserva",
        "mínimo 3 años de crianza total",
        "al menos 1 año en barrica de roble",
        "combinación de crianza en madera y botella"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identificas Reserva pero no detallas los requisitos. Para Rioja Reserva: mínimo 3 años en total, con al menos 1 año en barrica de roble.",
        "DEVELOPING_RESPONSE": "Buen intento. Especifica que Rioja Reserva requiere al menos 1 año en barrica y el resto en botella, sumando un mínimo de 3 años.",
        "STRONG_RESPONSE": "Respuesta completa: identifica Rioja Reserva, describe el requisito mínimo de 3 años con al menos 1 año en barrica de roble."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_025": {
      "item_id": "OR_025",
      "source_question_id": "OR_025",
      "expected_concepts": [
        "Stellenbosch",
        "clima mediterráneo",
        "influencia marítima de la Corriente de Benguela",
        "veranos cálidos moderados",
        "vinos con buena estructura y acidez"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identificas la región pero no explicas el mecanismo climático. En Stellenbosch, la influencia marítima modera los veranos cálidos, preservando acidez y aportando frescura.",
        "DEVELOPING_RESPONSE": "Buen comienzo. Añade el rol de la corriente marítima en moderar la temperatura y su impacto en la acidez y frescura de los vinos.",
        "STRONG_RESPONSE": "Respuesta sólida: identifica Stellenbosch, vincula el clima mediterráneo-marítimo con el perfil equilibrado de sus vinos: buena estructura y acidez moderada."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_026": {
      "item_id": "OR_026",
      "source_question_id": "OR_026",
      "expected_concepts": [
        "Barolo",
        "Barbaresco",
        "Piemonte",
        "Nebbiolo como variedad de alta acidez y taninos firmes"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Solo mencionas una región. Barolo y Barbaresco son las dos denominaciones principales del Piemonte basadas en Nebbiolo.",
        "DEVELOPING_RESPONSE": "Bien identificadas las dos regiones. Añade que ambas pertenecen al Piemonte y que el Nebbiolo se caracteriza por alta acidez y taninos firmes.",
        "STRONG_RESPONSE": "Respuesta completa: menciona Barolo y Barbaresco, sitúa ambas en el Piemonte y describe el perfil del Nebbiolo."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_027": {
      "item_id": "OR_027",
      "source_question_id": "OR_027",
      "expected_concepts": [
        "Marlborough (Nueva Zelanda) — aromas intensos de maracuyá y hierba, alta acidez",
        "Loire (Sancerre/Pouilly-Fumé) — estilo más mineral y herbáceo, acidez viva"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Solo describes una región. Para completar, compara Marlborough (frutosidad tropical, alta acidez) con una región del Loire como Sancerre (mineralidad, herbáceo).",
        "DEVELOPING_RESPONSE": "Buen intento. Añade más detalle sobre el contraste de estilos: Marlborough más exuberante y frutal; Sancerre más mineral y contenido.",
        "STRONG_RESPONSE": "Respuesta completa: contrasta Marlborough (frutas tropicales, acidez alta) con Loire/Sancerre (mineral, herbáceo, más austero)."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_028": {
      "item_id": "OR_028",
      "source_question_id": "OR_028",
      "expected_concepts": [
        "separación de bayas del raspón",
        "eliminar los tallos verdes",
        "reducir taninos vegetales",
        "mejorar la calidad de los taninos"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Defines el despalillado como separación de bayas, pero no explicas por qué. Se hace para eliminar los raspones y reducir los taninos vegetales que aportan amargor.",
        "DEVELOPING_RESPONSE": "Buen intento. Añade que el raspón contiene taninos verdes y astringentes que aportarían amargor y dureza si se incluyen en la fermentación.",
        "STRONG_RESPONSE": "Respuesta completa: el despalillado separa las bayas del raspón para evitar la extracción de taninos vegetales que aportarían amargor y astringencia al vino tinto."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_029": {
      "item_id": "OR_029",
      "source_question_id": "OR_029",
      "expected_concepts": [
        "Etna (Sicilia)",
        "suelos volcánicos basálticos",
        "mineralidad",
        "buen drenaje",
        "acidez elevada"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identificas la región pero no explicas la influencia de los suelos. Los suelos volcánicos aportan mineralidad y buen drenaje, favoreciendo vinos de alta acidez.",
        "DEVELOPING_RESPONSE": "Buen intento. Añade que los suelos volcánicos basálticos del Etna son pobres en nutrientes, con buen drenaje, lo que se traduce en vinos con perfil mineral y acidez marcada.",
        "STRONG_RESPONSE": "Respuesta sólida: identifica el Etna, describe los suelos volcánicos basálticos y vincula sus propiedades (drenaje, mineralidad) con el perfil del vino."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_030": {
      "item_id": "OR_030",
      "source_question_id": "OR_030",
      "expected_concepts": [
        "Salta (Cafayate)",
        "viñedos a gran altitud",
        "alta amplitud térmica",
        "radiación UV intensa",
        "acidez preservada por temperaturas nocturnas frescas"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identificas Salta, pero no detallas las condiciones. Salta tiene viñedos de hasta 3000 m, con gran amplitud térmica que preserva la acidez y concentra los aromas.",
        "DEVELOPING_RESPONSE": "Buen intento. Añade el impacto de la altitud extrema: radiación UV alta, temperaturas nocturnas frescas y gran diferencia térmica diurna/nocturna.",
        "STRONG_RESPONSE": "Respuesta completa: identifica Salta/Cafayate, menciona la gran altitud, describe la amplitud térmica, la radiación UV y la preservación de acidez."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_031": {
      "item_id": "OR_031",
      "source_question_id": "OR_031",
      "expected_concepts": [
        "Sauternes (Francia)",
        "Tokaj (Hungría)",
        "condiciones de humedad alternada con periodos secos",
        "concentración de azúcares y aromas",
        "podredumbre noble"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Solo menciona una región. Añade la segunda (Sauternes o Tokaj) y explica que la botrytis deshidrata la baya concentrando azúcares y aromas complejos.",
        "DEVELOPING_RESPONSE": "Buen intento. Detalla el mecanismo: la botrytis perfora la piel, permitiendo la evaporación del agua y la concentración de azúcares, ácidos y aromas.",
        "STRONG_RESPONSE": "Respuesta completa: menciona Sauternes y Tokaj, describe la alternancia húmedo-seco que activa la botrytis noble y el mecanismo de concentración en la baya."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_032": {
      "item_id": "OR_032",
      "source_question_id": "OR_032",
      "expected_concepts": [
        "color evolution",
        "secondary aromas",
        "vanillin and toasted notes",
        "texture increase",
        "finish prolongation"
      ],
      "optional_causal_chain": "HC_OAK_AGEING_COMPLEXITY",
      "causal_chain_reference": [
        "HC_OAK_AGEING_COMPLEXITY"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_033": {
      "item_id": "OR_033",
      "source_question_id": "OR_033",
      "expected_concepts": [
        "temperature decrease",
        "slower ripening",
        "malic acid retention",
        "sugar accumulation delay",
        "fresh profile result"
      ],
      "optional_causal_chain": "HC_ALTITUDE_TEMPERATURE",
      "causal_chain_reference": [
        "HC_ALTITUDE_TEMPERATURE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_034": {
      "item_id": "OR_034",
      "source_question_id": "OR_034",
      "expected_concepts": [
        "cool climate: primary aromas",
        "cool climate: higher acidity",
        "warm climate: secondary/tertiary aromas",
        "warm climate: lower acidity",
        "ripeness differential"
      ],
      "optional_causal_chain": "HC_COOL_CLIMATE_STYLE",
      "causal_chain_reference": [
        "HC_COOL_CLIMATE_STYLE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_035": {
      "item_id": "OR_035",
      "source_question_id": "OR_035",
      "expected_concepts": [
        "primary aromas preserved",
        "clear acidity",
        "mineral structure",
        "style-dependent judgment",
        "variety expression"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_036": {
      "item_id": "OR_036",
      "source_question_id": "OR_036",
      "expected_concepts": [
        "texture softening",
        "aromatic complexity",
        "acidity loss",
        "freshness compromise",
        "diacetyl risk",
        "style-dependent value"
      ],
      "optional_causal_chain": "CC_MLF_ACIDITY -> CC_MLF_TEXTURE",
      "causal_chain_reference": [
        "CC_MLF_ACIDITY",
        "CC_MLF_TEXTURE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_037": {
      "item_id": "OR_037",
      "source_question_id": "OR_037",
      "expected_concepts": [
        "certification types",
        "production cost increase",
        "premium pricing",
        "consumer perception",
        "market positioning",
        "labor intensity"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_038": {
      "item_id": "OR_038",
      "source_question_id": "OR_038",
      "expected_concepts": [
        "temperature control during fermentation",
        "stainless steel fermentation",
        "prevent MLF",
        "minimal oak",
        "early bottling",
        "preserve acidity"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_039": {
      "item_id": "OR_039",
      "source_question_id": "OR_039",
      "expected_concepts": [
        "continental climate",
        "limestone-rich soils",
        "cool growing season",
        "low yields",
        "Pinot Noir/Chardonnay varieties",
        "regional regulations",
        "expression of place"
      ],
      "optional_causal_chain": "HC_COOL_CLIMATE_STYLE",
      "causal_chain_reference": [
        "HC_COOL_CLIMATE_STYLE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_040": {
      "item_id": "OR_040",
      "source_question_id": "OR_040",
      "expected_concepts": [
        "color brightening",
        "tannin softening",
        "aroma opening",
        "fruit expression increase",
        "alcohol perception change",
        "structural integration"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_041": {
      "item_id": "OR_041",
      "source_question_id": "OR_041",
      "expected_concepts": [
        "berry size variation",
        "skin-to-juice ratio",
        "ripeness level",
        "exposition differences",
        "soil drainage variation",
        "terroir micro-variation"
      ],
      "optional_causal_chain": "HC_YIELD_CONCENTRATION",
      "causal_chain_reference": [
        "HC_YIELD_CONCENTRATION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_042": {
      "item_id": "OR_042",
      "source_question_id": "OR_042",
      "expected_concepts": [
        "old vine: deeper roots",
        "old vine: lower yields",
        "old vine: higher concentration",
        "old vine: higher tannins",
        "aging structure benefit",
        "complexity development"
      ],
      "optional_causal_chain": "HC_YIELD_CONCENTRATION",
      "causal_chain_reference": [
        "HC_YIELD_CONCENTRATION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_043": {
      "item_id": "OR_043",
      "source_question_id": "OR_043",
      "expected_concepts": [
        "tannin maturity indicator",
        "aroma volatility",
        "age estimation",
        "structure vs. development",
        "aging trajectory",
        "quality judgment context"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_044": {
      "item_id": "OR_044",
      "source_question_id": "OR_044",
      "expected_concepts": [
        "oxygen permeability",
        "cork taint risk",
        "alternative closure benefits",
        "TCA contamination",
        "consistent aging",
        "cost trade-offs"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_045": {
      "item_id": "OR_045",
      "source_question_id": "OR_045",
      "expected_concepts": [
        "tannin sources",
        "seed tannins: astringency",
        "skin tannins: structure",
        "extraction control",
        "temperature management",
        "aging benefits",
        "softening mechanisms"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_046": {
      "item_id": "OR_046",
      "source_question_id": "OR_046",
      "expected_concepts": [
        "varietal roles in blend",
        "Cabernet for structure",
        "Merlot for flesh",
        "Petit Verdot for aging",
        "balance proportions",
        "tasting evaluation iterative"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_047": {
      "item_id": "OR_047",
      "source_question_id": "OR_047",
      "expected_concepts": [
        "valley floor: riper fruit",
        "hillside: structure and complexity",
        "fog influence variation",
        "soil mineral expression",
        "Cabernet ripeness difference",
        "regional identity"
      ],
      "optional_causal_chain": "HC_COOL_CLIMATE_STYLE",
      "causal_chain_reference": [
        "HC_COOL_CLIMATE_STYLE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_048": {
      "item_id": "OR_048",
      "source_question_id": "OR_048",
      "expected_concepts": [
        "primary fermentation",
        "secondary fermentation in bottle",
        "autolysis",
        "yeast contact",
        "creamy texture",
        "complex aromatic development",
        "bubble formation"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_049": {
      "item_id": "OR_049",
      "source_question_id": "OR_049",
      "expected_concepts": [
        "warm day: sugar accumulation",
        "cool night: acid retention",
        "DTR benefit: both sugar and acidity",
        "flavor maturity vs. acid balance",
        "ideal DTR zones",
        "aromatic complexity from acid preservation"
      ],
      "optional_causal_chain": "HC_DIURNAL_RANGE_FRESHNESS",
      "causal_chain_reference": [
        "HC_DIURNAL_RANGE_FRESHNESS"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_050": {
      "item_id": "OR_050",
      "source_question_id": "OR_050",
      "expected_concepts": [
        "botrytis: noble rot complexity",
        "botrytis: honey and citrus notes",
        "botrytis: acidity retention",
        "drying: concentration",
        "drying: less complexity",
        "aging potential variation"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_051": {
      "item_id": "OR_051",
      "source_question_id": "OR_051",
      "expected_concepts": [
        "alcohol role: structure and preservation",
        "sweetness level appropriateness",
        "aroma complexity",
        "aging indicators",
        "style expectations",
        "balance judgment"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_052": {
      "item_id": "OR_052",
      "source_question_id": "OR_052",
      "expected_concepts": [
        "tannin polymerization",
        "color stabilization",
        "oxidation risk",
        "over-oxidation possibility",
        "cost consideration",
        "style impact unpredictability"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_053": {
      "item_id": "OR_053",
      "source_question_id": "OR_053",
      "expected_concepts": [
        "pH vs. titratable acidity distinction",
        "microbiological stability",
        "tannin color expression",
        "oxidation sensitivity",
        "aging trajectory impact",
        "winemaker pH management tools"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_054": {
      "item_id": "OR_054",
      "source_question_id": "OR_054",
      "expected_concepts": [
        "lower alcohol target",
        "higher acidity retention",
        "optimal ripeness for aroma",
        "timing precision",
        "multiple picks vs. single",
        "analytical targets: brix, pH, TA"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_055": {
      "item_id": "OR_055",
      "source_question_id": "OR_055",
      "expected_concepts": [
        "leaf area management",
        "fruit exposure balance",
        "sugar accumulation",
        "phenolic ripeness",
        "sunlight interception",
        "shade prevention"
      ],
      "optional_causal_chain": "HC_CANOPY_VIGOUR_EXPOSURE",
      "causal_chain_reference": [
        "HC_CANOPY_VIGOUR_EXPOSURE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_056": {
      "item_id": "OR_056",
      "source_question_id": "OR_056",
      "expected_concepts": [
        "tannin polymerization",
        "color brick formation",
        "secondary aromatics development",
        "fruit to earth shift",
        "texture integration",
        "aromatic complexity peak"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_057": {
      "item_id": "OR_057",
      "source_question_id": "OR_057",
      "expected_concepts": [
        "cork structure and microporosity",
        "oxygen transmission rate",
        "slow oxidation benefits",
        "tannin polymerization",
        "color brick development",
        "aromatic integration"
      ],
      "optional_causal_chain": "HC_BOTTLE_STORAGE_STABILITY",
      "causal_chain_reference": [
        "HC_BOTTLE_STORAGE_STABILITY"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_058": {
      "item_id": "OR_058",
      "source_question_id": "OR_058",
      "expected_concepts": [
        "temperature impact on ripening",
        "sugar accumulation rate",
        "malic acid retention",
        "phenolic maturity variation",
        "vintage character expression"
      ],
      "optional_causal_chain": "HC_WARM_DRY_OVERRIPENING",
      "causal_chain_reference": [
        "HC_WARM_DRY_OVERRIPENING"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_059": {
      "item_id": "OR_059",
      "source_question_id": "OR_059",
      "expected_concepts": [
        "Chardonnay: benefits from MLF texture",
        "Sauvignon Blanc: benefits from acidity preservation",
        "acidity role in style",
        "aromatic complexity vs. freshness",
        "producer intent and market positioning"
      ],
      "optional_causal_chain": "HC_MLF_ACID_CONVERSION",
      "causal_chain_reference": [
        "HC_MLF_ACID_CONVERSION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_060": {
      "item_id": "OR_060",
      "source_question_id": "OR_060",
      "expected_concepts": [
        "tannin softening indicators",
        "aroma stability vs. evolution",
        "age estimation from structure",
        "remaining drinking window",
        "peak expression timeline"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_061": {
      "item_id": "OR_061",
      "source_question_id": "OR_061",
      "expected_concepts": [
        "temperature control precision",
        "aroma volatility",
        "tannin extraction dynamics",
        "spoilage risk",
        "winemaker intent and market target",
        "cost considerations"
      ],
      "optional_causal_chain": "HC_STAINLESS_TEMPERATURE_CONTROL",
      "causal_chain_reference": [
        "HC_STAINLESS_TEMPERATURE_CONTROL"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_062": {
      "item_id": "OR_062",
      "source_question_id": "OR_062",
      "expected_concepts": [
        "RS and tannin perception",
        "microbial stability",
        "food pairing implications",
        "consumer expectations",
        "production philosophy",
        "climate and ripeness variation"
      ],
      "optional_causal_chain": "HC_RESIDUAL_SUGAR_LOW_ALCOHOL_CHILI_PAIRING",
      "causal_chain_reference": [
        "HC_RESIDUAL_SUGAR_LOW_ALCOHOL_CHILI_PAIRING"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_063": {
      "item_id": "OR_063",
      "source_question_id": "OR_063",
      "expected_concepts": [
        "harvest timing for acidity retention",
        "whole-bunch pressing",
        "cool fermentation temperature",
        "yeast strain selection",
        "malolactic prevention",
        "early bottling",
        "oak avoidance"
      ],
      "optional_causal_chain": "HC_COOL_FERMENTATION_AROMA_RETENTION",
      "causal_chain_reference": [
        "HC_COOL_FERMENTATION_AROMA_RETENTION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_064": {
      "item_id": "OR_064",
      "source_question_id": "OR_064",
      "expected_concepts": [
        "steep south-facing slopes maximize sunlight",
        "cool continental influence",
        "slate soil drainage",
        "altitude and temperature",
        "late harvest ripeness without excessive alcohol",
        "acidity preservation natural advantage"
      ],
      "optional_causal_chain": "HC_STEEP_SLOPE_SOLAR_RIPENING",
      "causal_chain_reference": [
        "HC_STEEP_SLOPE_SOLAR_RIPENING"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_065": {
      "item_id": "OR_065",
      "source_question_id": "OR_065",
      "expected_concepts": [
        "oxidative aging (oxygen contact)",
        "reductive aging (sealed environment)",
        "color development",
        "aromatic evolution",
        "tannin integration",
        "complexity tier progression"
      ],
      "optional_causal_chain": "HC_OXIDATIVE_AGEING_TERTIARY",
      "causal_chain_reference": [
        "HC_OXIDATIVE_AGEING_TERTIARY"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_066": {
      "item_id": "OR_066",
      "source_question_id": "OR_066",
      "expected_concepts": [
        "water stress during veraison",
        "tannin synthesis activation",
        "phenolic maturity markers",
        "grape concentration",
        "soil drainage role",
        "irrigation decisions impact"
      ],
      "optional_causal_chain": "HC_MODERATE_WATER_STRESS_PHENOLICS",
      "causal_chain_reference": [
        "HC_MODERATE_WATER_STRESS_PHENOLICS"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_067": {
      "item_id": "OR_067",
      "source_question_id": "OR_067",
      "expected_concepts": [
        "Sauternes: maritime humidity and Gironde moisture",
        "Tokaji: continental cool nights and lake effect",
        "noble rot timing and intensity",
        "concentration levels",
        "aromatic profiles variation",
        "acidity retention differences"
      ],
      "optional_causal_chain": "HC_NOBLE_ROT_DEVELOPMENT_CONDITIONS",
      "causal_chain_reference": [
        "HC_NOBLE_ROT_DEVELOPMENT_CONDITIONS"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_068": {
      "item_id": "OR_068",
      "source_question_id": "OR_068",
      "expected_concepts": [
        "primary fruit preservation",
        "oak vanillin and toasted character integration",
        "texture development",
        "balance vs. imbalance markers",
        "oak age and intensity",
        "malolactic influence"
      ],
      "optional_causal_chain": "HC_NEW_OAK_STRUCTURE_SPICE",
      "causal_chain_reference": [
        "HC_NEW_OAK_STRUCTURE_SPICE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_069": {
      "item_id": "OR_069",
      "source_question_id": "OR_069",
      "expected_concepts": [
        "enzyme action on cell walls",
        "tannin extraction increase",
        "color development",
        "aroma compound release",
        "time reduction benefit",
        "potential over-extraction risk",
        "cost efficiency"
      ],
      "optional_causal_chain": "HC_EXTRACTION_BODY_STRUCTURE",
      "causal_chain_reference": [
        "HC_EXTRACTION_BODY_STRUCTURE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_070": {
      "item_id": "OR_070",
      "source_question_id": "OR_070",
      "expected_concepts": [
        "warmer growing seasons",
        "earlier harvest timing",
        "higher potential alcohol",
        "lower acidity challenges",
        "higher altitude vineyard migration",
        "varietal shifting",
        "water scarcity adaptation",
        "style preservation strategies"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_071": {
      "item_id": "OR_071",
      "source_question_id": "OR_071",
      "expected_concepts": [
        "control wine requirement",
        "blind tasting methodology",
        "flavor compound identification",
        "tannin structure comparison",
        "aroma intensity progression",
        "systematic note-taking",
        "statistical comparison approach"
      ],
      "optional_causal_chain": "HC_BARREL_SIZE_OAK_CONTACT",
      "causal_chain_reference": [
        "HC_BARREL_SIZE_OAK_CONTACT"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_072": {
      "item_id": "OR_072",
      "source_question_id": "OR_072",
      "expected_concepts": [
        "volcanic soil composition (basalt, pumice)",
        "mineral nutrient availability",
        "drainage properties",
        "mineral compound uptake in fruit",
        "terroir expression intensity",
        "aging structure from minerals"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_073": {
      "item_id": "OR_073",
      "source_question_id": "OR_073",
      "expected_concepts": [
        "secondary fermentation CO2 production",
        "yeast autolysis process",
        "amino acid and nucleotide release",
        "creamy texture development",
        "bread/biscuit aroma emergence",
        "bubble structure refinement"
      ],
      "optional_causal_chain": "HC_SPARKLING_AUTOLYTIC_AROMAS",
      "causal_chain_reference": [
        "HC_SPARKLING_AUTOLYTIC_AROMAS"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_074": {
      "item_id": "OR_074",
      "source_question_id": "OR_074",
      "expected_concepts": [
        "Nebbiolo: thick-skinned grape variety",
        "phenolic tannin concentration",
        "polymerization rate",
        "tannin structure chemical differences",
        "aging softening variation by variety",
        "sensory threshold differences"
      ],
      "optional_causal_chain": "HC_RED_WINE_AGEABILITY_STRUCTURE",
      "causal_chain_reference": [
        "HC_RED_WINE_AGEABILITY_STRUCTURE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_075": {
      "item_id": "OR_075",
      "source_question_id": "OR_075",
      "expected_concepts": [
        "temperature stability impact",
        "oxidation rate variation",
        "oxygen transmission",
        "spoilage risk scenarios",
        "aging trajectory prediction",
        "compound evolution speed"
      ],
      "optional_causal_chain": "HC_BOTTLE_STORAGE_STABILITY",
      "causal_chain_reference": [
        "HC_BOTTLE_STORAGE_STABILITY"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_076": {
      "item_id": "OR_076",
      "source_question_id": "OR_076",
      "expected_concepts": [
        "primary to secondary aroma transition",
        "tannin integration timeline",
        "color and clarity markers",
        "flavor intensity plateau",
        "drinking window definition",
        "cellaring continuation decision"
      ],
      "optional_causal_chain": "HC_BAROLO_TERTIARY_EVOLUTION",
      "causal_chain_reference": [
        "HC_BAROLO_TERTIARY_EVOLUTION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_077": {
      "item_id": "OR_077",
      "source_question_id": "OR_077",
      "expected_concepts": [
        "mechanical efficiency and speed",
        "grape skin integrity",
        "oxidation during transport",
        "stems and leaf contamination",
        "vineyard slope accessibility",
        "cost efficiency comparison",
        "quality vs. production tradeoff"
      ],
      "optional_causal_chain": "HC_SELECTIVE_HAND_HARVEST_QUALITY",
      "causal_chain_reference": [
        "HC_SELECTIVE_HAND_HARVEST_QUALITY"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_078": {
      "item_id": "OR_078",
      "source_question_id": "OR_078",
      "expected_concepts": [
        "bowl shape and aroma capture",
        "rim opening size",
        "surface area for oxidation",
        "flow dynamics",
        "temperature maintenance",
        "psychological expectation",
        "sensory expression optimization"
      ],
      "optional_causal_chain": "HC_LARGE_BOWL_AROMA_EXPRESSION",
      "causal_chain_reference": [
        "HC_LARGE_BOWL_AROMA_EXPRESSION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_079": {
      "item_id": "OR_079",
      "source_question_id": "OR_079",
      "expected_concepts": [
        "color development observation",
        "aroma evolution stage identification",
        "tannin integration level",
        "acidity preservation check",
        "residual sugar stability",
        "bottle variation acknowledgment",
        "cellar condition consideration"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_080": {
      "item_id": "OR_080",
      "source_question_id": "OR_080",
      "expected_concepts": [
        "soil composition limestone variation",
        "aspect and sun exposure gradient",
        "drainage and minerality",
        "historical selection by Benedictine monks",
        "classification continuity",
        "site-specific expression documentation"
      ],
      "optional_causal_chain": "HC_BURGUNDY_SITE_HIERARCHY_CONCENTRATION",
      "causal_chain_reference": [
        "HC_BURGUNDY_SITE_HIERARCHY_CONCENTRATION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_081": {
      "item_id": "OR_081",
      "source_question_id": "OR_081",
      "expected_concepts": [
        "initial honey and apricot aromas",
        "secondary citrus and spice development",
        "tannin softening in sweet context",
        "acidity preservation role",
        "oxidative browning",
        "tertiary complexity emergence",
        "long aging potential"
      ],
      "optional_causal_chain": "HC_BOTRYTIS_CONCENTRATION",
      "causal_chain_reference": [
        "HC_BOTRYTIS_CONCENTRATION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_082": {
      "item_id": "OR_082",
      "source_question_id": "OR_082",
      "expected_concepts": [
        "vintage weather variation impact",
        "aging progression across similar wines",
        "maturity markers",
        "consistency within producer style",
        "optimal drinking window identification"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_083": {
      "item_id": "OR_083",
      "source_question_id": "OR_083",
      "expected_concepts": [
        "yeast cell wall breakdown over time",
        "amino acid release kinetics",
        "nucleotide release",
        "aldehyde and alcohol interactions",
        "complexity tier progression",
        "aromatic compound generation rate"
      ],
      "optional_causal_chain": "HC_SPARKLING_LEES_TEXTURE",
      "causal_chain_reference": [
        "HC_SPARKLING_LEES_TEXTURE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_084": {
      "item_id": "OR_084",
      "source_question_id": "OR_084",
      "expected_concepts": [
        "quality/quantity trade-off",
        "labor cost variation by region",
        "climate risk and vintage consistency",
        "market positioning flexibility",
        "brand identity development",
        "export potential variation"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_085": {
      "item_id": "OR_085",
      "source_question_id": "OR_085",
      "expected_concepts": [
        "phenolic ripeness indicators",
        "tannin polymerization status",
        "color development consistency",
        "barrel aging effects",
        "vintage character variation",
        "individual wine potential"
      ],
      "optional_causal_chain": "HC_BOTTLE_TANNIN_SOFTENING",
      "causal_chain_reference": [
        "HC_BOTTLE_TANNIN_SOFTENING"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_086": {
      "item_id": "OR_086",
      "source_question_id": "OR_086",
      "expected_concepts": [
        "soil microbiome recovery",
        "pest and disease management evolution",
        "certification timeline",
        "yield variation during transition",
        "quality attribute changes",
        "market positioning benefits"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_087": {
      "item_id": "OR_087",
      "source_question_id": "OR_087",
      "expected_concepts": [
        "ripeness achievement strategies",
        "acidity management approaches",
        "color and tannin development",
        "fermentation temperature control",
        "oak influence suitability",
        "alcohol risk mitigation"
      ],
      "optional_causal_chain": "HC_CONTINENTALITY_STYLE",
      "causal_chain_reference": [
        "HC_CONTINENTALITY_STYLE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_088": {
      "item_id": "OR_088",
      "source_question_id": "OR_088",
      "expected_concepts": [
        "varietal role definition",
        "tannin structure balance",
        "acidity preservation",
        "aromatics complexity",
        "early fruit expression",
        "long-term evolution potential"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_089": {
      "item_id": "OR_089",
      "source_question_id": "OR_089",
      "expected_concepts": [
        "Barossa: warm valley floor ripeness",
        "Adelaide Hills: cool altitude freshness",
        "soil composition differences",
        "maritime influence variation",
        "ripeness profiles",
        "style expression signature"
      ],
      "optional_causal_chain": "HC_ALTITUDE_SLOW_RIPENING_FRESHNESS",
      "causal_chain_reference": [
        "HC_ALTITUDE_SLOW_RIPENING_FRESHNESS"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_090": {
      "item_id": "OR_090",
      "source_question_id": "OR_090",
      "expected_concepts": [
        "solera system continuous blending",
        "controlled oxidation progression",
        "color browning increments",
        "aromatic complexity tiers",
        "alcohol and acidity stability",
        "final integration achievement"
      ],
      "optional_causal_chain": "HC_OLOROSO_AMONTILLADO_AGEING_PATH",
      "causal_chain_reference": [
        "HC_OLOROSO_AMONTILLADO_AGEING_PATH"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_091": {
      "item_id": "OR_091",
      "source_question_id": "OR_091",
      "expected_concepts": [
        "soil mineral composition",
        "nutrient availability to vines",
        "water stress effects",
        "transpiration patterns",
        "phenolic ripeness",
        "aromatic compound accumulation pathways"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_092": {
      "item_id": "OR_092",
      "source_question_id": "OR_092",
      "expected_concepts": [
        "slope drainage and ripeness",
        "alluvial soil water retention",
        "mineral expression variation",
        "acidity preservation",
        "aging potential difference",
        "complexity development rate"
      ],
      "optional_causal_chain": "HC_MOSEL_COOL_SLOPE_ACIDITY",
      "causal_chain_reference": [
        "HC_MOSEL_COOL_SLOPE_ACIDITY"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_093": {
      "item_id": "OR_093",
      "source_question_id": "OR_093",
      "expected_concepts": [
        "ripeness potential vs. technique intent",
        "alcohol expression vs. acid preservation",
        "aroma profile alignment",
        "structure development",
        "style coherence evaluation",
        "producer philosophy expression"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_094": {
      "item_id": "OR_094",
      "source_question_id": "OR_094",
      "expected_concepts": [
        "fermentation predictability variation",
        "aromatic profile diversity",
        "malolactic interaction timing",
        "risk of stuck fermentation",
        "terroir expression enhancement",
        "consumer perception and marketing"
      ],
      "optional_causal_chain": "HC_YEAST_STRAIN_AROMA_PROFILE",
      "causal_chain_reference": [
        "HC_YEAST_STRAIN_AROMA_PROFILE"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_095": {
      "item_id": "OR_095",
      "source_question_id": "OR_095",
      "expected_concepts": [
        "yield reduction reality",
        "input cost changes",
        "chemical residue impacts",
        "soil recovery benefits",
        "marketing value vs. production cost",
        "certification program trade-offs",
        "genuine environmental metrics"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_096": {
      "item_id": "OR_096",
      "source_question_id": "OR_096",
      "expected_concepts": [
        "oxygen transmission variation",
        "TCA taint incidence",
        "cork integration consistency",
        "blind assessment methodology",
        "aging trajectory tracking",
        "chemical analysis integration"
      ],
      "optional_causal_chain": "HC_NATURAL_CORK_SLOW_OXYGEN",
      "causal_chain_reference": [
        "HC_NATURAL_CORK_SLOW_OXYGEN"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_097": {
      "item_id": "OR_097",
      "source_question_id": "OR_097",
      "expected_concepts": [
        "Kimmeridgian: shells and mineral intensity",
        "Portlandian: limestone with clay blend",
        "soil chemistry and mineral uptake",
        "pH influence",
        "aroma profile distinction",
        "aging potential variation"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_098": {
      "item_id": "OR_098",
      "source_question_id": "OR_098",
      "expected_concepts": [
        "analytical ripeness (Brix/TA/pH)",
        "phenolic maturity assessment",
        "disease and pest pressure",
        "weather forecast integration",
        "quality target definition",
        "separate lot production strategy"
      ],
      "optional_causal_chain": "HC_HARVEST_BRIX_RIPENESS_DECISION",
      "causal_chain_reference": [
        "HC_HARVEST_BRIX_RIPENESS_DECISION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_099": {
      "item_id": "OR_099",
      "source_question_id": "OR_099",
      "expected_concepts": [
        "RS and tannin softening perception",
        "acid and sweetness balance interaction",
        "alcohol and structure relationship",
        "food pairing dynamics",
        "flavor intensity masking effects",
        "viscosity and texture effects"
      ],
      "optional_causal_chain": "HC_RESIDUAL_SUGAR_LOW_ALCOHOL_CHILI_PAIRING",
      "causal_chain_reference": [
        "HC_RESIDUAL_SUGAR_LOW_ALCOHOL_CHILI_PAIRING"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_100": {
      "item_id": "OR_100",
      "source_question_id": "OR_100",
      "expected_concepts": [
        "production efficiency economies of scale",
        "quality-cost relationship",
        "brand tier positioning",
        "marketing spend ratios",
        "distribution channel differences",
        "collector vs. consumer market"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_101": {
      "item_id": "OR_101",
      "source_question_id": "OR_101",
      "expected_concepts": [
        "climate expectation vs. actual expression",
        "terroir anomaly possibility",
        "winemaker intervention effects",
        "acidity source determination",
        "aroma profile origins",
        "quality merit independent of category"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_102": {
      "item_id": "OR_102",
      "source_question_id": "OR_102",
      "expected_concepts": [
        "tannin extraction from skins",
        "color and oxidative browning",
        "aromatic compound release",
        "spoilage organism growth risk",
        "SO2 preservation challenge",
        "style achievement vs. execution risk"
      ],
      "optional_causal_chain": "HC_RED_FERMENTATION_EXTRACTION",
      "causal_chain_reference": [
        "HC_RED_FERMENTATION_EXTRACTION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_103": {
      "item_id": "OR_103",
      "source_question_id": "OR_103",
      "expected_concepts": [
        "oxygen control precision",
        "TCA contamination elimination",
        "consumer perception lag",
        "tradition vs. innovation tension",
        "environmental footprint comparison",
        "aging reliability and consistency"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_104": {
      "item_id": "OR_104",
      "source_question_id": "OR_104",
      "expected_concepts": [
        "soil health restoration timeline",
        "pest and disease integrated management",
        "yield expectation during transition",
        "harvest timing decisions",
        "separate vintage production consideration",
        "marketing and certification strategy"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_105": {
      "item_id": "OR_105",
      "source_question_id": "OR_105",
      "expected_concepts": [
        "glacial valley formation and aspect",
        "soil minerality from glacial deposit",
        "temperature extremes from altitude",
        "diurnal temperature range benefit",
        "water drainage patterns",
        "regional style consistency"
      ],
      "optional_causal_chain": "HC_DIURNAL_RANGE_FRESHNESS",
      "causal_chain_reference": [
        "HC_DIURNAL_RANGE_FRESHNESS"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_106": {
      "item_id": "OR_106",
      "source_question_id": "OR_106",
      "expected_concepts": [
        "botrytized berry concentration",
        "fermentation control complexity",
        "solera-style blending",
        "oxidative maturation in cask",
        "botrytis complexity emergence",
        "long-aging capacity",
        "tertiary aromatics development"
      ],
      "optional_causal_chain": "HC_TOKAJI_ASZU_BERRY_ADDITION",
      "causal_chain_reference": [
        "HC_TOKAJI_ASZU_BERRY_ADDITION"
      ],
      "feedback_profile": {},
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_107": {
      "item_id": "OR_107",
      "source_question_id": "OR_107",
      "expected_concepts": [
        "ripe healthy grapes retained on the vine",
        "sustained sub-zero temperature",
        "water freezes within the berries",
        "harvest and pressing while frozen",
        "low yield and concentrated must"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "List the required vineyard conditions and distinguish natural vine freezing from commercial freezing.",
        "DEVELOPING_RESPONSE": "Connect sub-zero conditions and frozen water to the small volume of concentrated juice obtained at pressing.",
        "STRONG_RESPONSE": "Maintain a precise sequence from ripe grapes through natural freezing, frozen harvest, pressing, concentration, and low yield."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_108": {
      "item_id": "OR_108",
      "source_question_id": "OR_108",
      "expected_concepts": [
        "extended hang time",
        "water loss before freezing",
        "required freezing event",
        "bird and animal damage",
        "rot and adverse weather",
        "very low and uncertain yield"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identify at least two crop risks created by leaving ripe grapes on the vine.",
        "DEVELOPING_RESPONSE": "Explain the trade-off between waiting for freezing concentration and exposing the crop to damage and loss.",
        "STRONG_RESPONSE": "Show how delayed harvest creates concentration potential while simultaneously increasing biological, weather, labour, and yield risk."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_109": {
      "item_id": "OR_109",
      "source_question_id": "OR_109",
      "expected_concepts": [
        "natural freezing versus noble rot",
        "healthy frozen fruit versus Botrytis-infected fruit",
        "cold winter event",
        "humid mornings and dry afternoons",
        "different crop-loss risks",
        "concentration by ice separation versus berry dehydration"
      ],
      "optional_causal_chain": "HC_BOTRYTIS_CONCENTRATION",
      "causal_chain_reference": [
        "HC_BOTRYTIS_CONCENTRATION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Set out both methods in parallel rather than describing only one.",
        "DEVELOPING_RESPONSE": "Link each environment to its distinct concentration mechanism and vineyard risk.",
        "STRONG_RESPONSE": "Use a balanced comparison covering climate, berry condition, harvest timing, concentration mechanism, and risk."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_110": {
      "item_id": "OR_110",
      "source_question_id": "OR_110",
      "expected_concepts": [
        "humidity encourages Botrytis infection",
        "dry afternoons favour noble rot",
        "persistent moisture raises grey rot risk",
        "selective picking requirement",
        "vintage variability",
        "qualified suitability judgement"
      ],
      "optional_causal_chain": "HC_BOTRYTIS_CONCENTRATION",
      "causal_chain_reference": [
        "HC_BOTRYTIS_CONCENTRATION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "State a suitability judgement and support it with both a benefit and a risk.",
        "DEVELOPING_RESPONSE": "Distinguish conditions that promote noble rot from conditions that allow destructive grey rot.",
        "STRONG_RESPONSE": "Give a qualified judgement based on infection, afternoon drying, selection costs, crop loss, and vintage consistency."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_111": {
      "item_id": "OR_111",
      "source_question_id": "OR_111",
      "expected_concepts": [
        "site exposure and humidity",
        "need for beneficial Botrytis",
        "risk of rain and grey rot",
        "selective harvesting cost",
        "vintage variation",
        "alternative dry-wine use",
        "balanced conclusion"
      ],
      "optional_causal_chain": "HC_BOTRYTIS_CONCENTRATION",
      "causal_chain_reference": [
        "HC_BOTRYTIS_CONCENTRATION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identify the potential reward and at least one climate-related downside.",
        "DEVELOPING_RESPONSE": "Weigh Aszú concentration and value against crop failure, selection cost, and alternative parcel use.",
        "STRONG_RESPONSE": "Reach a conditional conclusion that reflects site suitability, vintage uncertainty, labour, and market value."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_112": {
      "item_id": "OR_112",
      "source_question_id": "OR_112",
      "expected_concepts": [
        "extended ripening",
        "sugar accumulation and acid loss",
        "rot and weather exposure",
        "bird damage",
        "careful bunch selection",
        "yield reduction",
        "trade-off between concentration and freshness"
      ],
      "optional_causal_chain": "HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION",
      "causal_chain_reference": [
        "HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Cover both the intended ripeness benefit and the risks of waiting.",
        "DEVELOPING_RESPONSE": "Connect high ripeness to sugar, acidity, crop health, selection, and final style.",
        "STRONG_RESPONSE": "Discuss competing outcomes and explain why harvest decisions must balance concentration, freshness, and sound fruit."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_113": {
      "item_id": "OR_113",
      "source_question_id": "OR_113",
      "expected_concepts": [
        "very concentrated must",
        "slow difficult fermentation",
        "temperature control",
        "suitable yeast selection",
        "fermentation stopped or naturally arrested",
        "retention of acidity and primary fruit",
        "microbial stability"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Make a clear production recommendation rather than listing possible techniques.",
        "DEVELOPING_RESPONSE": "Explain how each fermentation choice protects fruit, balances sweetness, and manages a high-sugar must.",
        "STRONG_RESPONSE": "Give a coherent production sequence with reasons, trade-offs, and stability controls."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_114": {
      "item_id": "OR_114",
      "source_question_id": "OR_114",
      "expected_concepts": [
        "water freezes in the berry",
        "concentrated juice separated during pressing",
        "high sugar must",
        "osmotic stress on yeast",
        "slow or incomplete fermentation",
        "high residual sugar",
        "acid-sweetness balance"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Name freezing as the mechanism, then explain rather than stopping at identification.",
        "DEVELOPING_RESPONSE": "Trace the effect from frozen water separation to must concentration and yeast stress.",
        "STRONG_RESPONSE": "Complete the chain through fermentation behaviour, residual sugar, and final balance."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_115": {
      "item_id": "OR_115",
      "source_question_id": "OR_115",
      "expected_concepts": [
        "selection of botrytised aszú berries",
        "base wine or fermenting must",
        "maceration of aszú material",
        "pressing",
        "slow fermentation",
        "residual sugar",
        "maturation"
      ],
      "optional_causal_chain": "HC_TOKAJI_ASZU_BERRY_ADDITION",
      "causal_chain_reference": [
        "HC_TOKAJI_ASZU_BERRY_ADDITION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Place the production stages in a clear chronological order.",
        "DEVELOPING_RESPONSE": "Add how aszú berry addition and maceration transfer sugar, acidity, and flavour.",
        "STRONG_RESPONSE": "Describe the complete process accurately from berry selection through maceration, fermentation, residual sugar, and maturation."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_116": {
      "item_id": "OR_116",
      "source_question_id": "OR_116",
      "expected_concepts": [
        "botrytised dehydrated berries",
        "high sugar and acid concentration",
        "maceration and extraction",
        "transfer of botrytis-derived flavours",
        "difficult slow fermentation",
        "retained residual sugar",
        "balanced concentrated style"
      ],
      "optional_causal_chain": "HC_TOKAJI_ASZU_BERRY_ADDITION",
      "causal_chain_reference": [
        "HC_TOKAJI_ASZU_BERRY_ADDITION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Do not treat berry addition as simple sweetening; explain extraction and fermentation effects.",
        "DEVELOPING_RESPONSE": "Connect dehydrated berry composition to maceration, yeast conditions, and retained sweetness.",
        "STRONG_RESPONSE": "Show the full mechanism linking berry condition, extraction, fermentation difficulty, acidity, sweetness, and complexity."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_117": {
      "item_id": "OR_117",
      "source_question_id": "OR_117",
      "expected_concepts": [
        "aszú berry selection and addition",
        "direct pressing of botrytised Sauternes grapes",
        "maceration difference",
        "high-sugar fermentation challenge",
        "residual sugar management",
        "maturation choices",
        "style consequences"
      ],
      "optional_causal_chain": "HC_TOKAJI_ASZU_BERRY_ADDITION -> HC_BOTRYTIS_CONCENTRATION",
      "causal_chain_reference": [
        "HC_TOKAJI_ASZU_BERRY_ADDITION",
        "HC_BOTRYTIS_CONCENTRATION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Use parallel points for both wines and identify at least one important production difference.",
        "DEVELOPING_RESPONSE": "Explain how berry handling, extraction, fermentation, and maturation shape each style.",
        "STRONG_RESPONSE": "Deliver a balanced production comparison with clear consequences for sweetness, acidity, flavour, and texture."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_118": {
      "item_id": "OR_118",
      "source_question_id": "OR_118",
      "expected_concepts": [
        "multiple selective pickings",
        "variation in botrytis and ripeness",
        "lot-specific fermentation control",
        "quality selection",
        "blending flexibility",
        "higher labour and winery cost",
        "qualified judgement"
      ],
      "optional_causal_chain": "HC_BOTRYTIS_CONCENTRATION",
      "causal_chain_reference": [
        "HC_BOTRYTIS_CONCENTRATION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "State whether the decision is suitable and give evidence.",
        "DEVELOPING_RESPONSE": "Balance precision and blending flexibility against cost, complexity, and small volumes.",
        "STRONG_RESPONSE": "Reach a style- and quality-based judgement supported by picking variation, fermentation control, selection, and cost."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_119": {
      "item_id": "OR_119",
      "source_question_id": "OR_119",
      "expected_concepts": [
        "oxygen exposure and texture",
        "oak-derived flavours",
        "integration with concentrated fruit",
        "cost",
        "risk of masking botrytis character",
        "ageing potential",
        "balanced conclusion"
      ],
      "optional_causal_chain": "HC_NEW_OAK_STRUCTURE_SPICE -> HC_BOTRYTIS_CONCENTRATION",
      "causal_chain_reference": [
        "HC_NEW_OAK_STRUCTURE_SPICE",
        "HC_BOTRYTIS_CONCENTRATION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Include both benefits and disadvantages of new oak.",
        "DEVELOPING_RESPONSE": "Relate oak intensity and oxygen exposure to the wine's concentration, botrytis character, and intended style.",
        "STRONG_RESPONSE": "Weigh integration, complexity, structure, masking risk, cost, and ageing before reaching a conditional conclusion."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_120": {
      "item_id": "OR_120",
      "source_question_id": "OR_120",
      "expected_concepts": [
        "water loss and concentration",
        "on-vine weather exposure",
        "mat drying and handling",
        "controlled-room airflow and humidity",
        "rot risk",
        "rate of drying",
        "freshness and flavour differences",
        "cost"
      ],
      "optional_causal_chain": "HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION",
      "causal_chain_reference": [
        "HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Name the methods and give at least one consequence for each.",
        "DEVELOPING_RESPONSE": "Connect drying environment and speed to rot risk, concentration, flavour, and cost.",
        "STRONG_RESPONSE": "Discuss the methods comparatively and explain how practical control changes both risk and final style."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_121": {
      "item_id": "OR_121",
      "source_question_id": "OR_121",
      "expected_concepts": [
        "fermentation interruption or natural arrest",
        "temperature reduction",
        "yeast removal by filtration",
        "sulfur dioxide where appropriate",
        "residual sugar target",
        "microbial stability",
        "balanced style"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Choose one method and state how it stops yeast activity.",
        "DEVELOPING_RESPONSE": "Add the post-fermentation controls needed to prevent refermentation.",
        "STRONG_RESPONSE": "Recommend a coherent method and justify timing, yeast control, stability, and style consequences."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_122": {
      "item_id": "OR_122",
      "source_question_id": "OR_122",
      "expected_concepts": [
        "Botrytis perforates berry skins",
        "water evaporation",
        "grape drying by air and time",
        "concentration of sugar and acid",
        "flavour transformation",
        "reduced juice yield",
        "different microbial and oxidation risks"
      ],
      "optional_causal_chain": "HC_BOTRYTIS_CONCENTRATION -> HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION",
      "causal_chain_reference": [
        "HC_BOTRYTIS_CONCENTRATION",
        "HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identify both mechanisms before explaining their effects.",
        "DEVELOPING_RESPONSE": "Show how both remove water but differ in biological action, flavour development, and risk.",
        "STRONG_RESPONSE": "Explain each mechanism through berry change, composition, yield, flavour, and fermentation consequences."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_123": {
      "item_id": "OR_123",
      "source_question_id": "OR_123",
      "expected_concepts": [
        "low juice yield from botrytised grapes",
        "difficult pressing",
        "high-sugar fermentation",
        "retained residual sugar",
        "lot selection and blending",
        "oak maturation",
        "high acidity balancing sweetness"
      ],
      "optional_causal_chain": "HC_BOTRYTIS_CONCENTRATION",
      "causal_chain_reference": [
        "HC_BOTRYTIS_CONCENTRATION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Put the winery stages in sequence and include residual sugar.",
        "DEVELOPING_RESPONSE": "Connect each production choice to sweetness, acidity, texture, flavour, or quality.",
        "STRONG_RESPONSE": "Describe a complete production pathway and its cumulative impact on style."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_124": {
      "item_id": "OR_124",
      "source_question_id": "OR_124",
      "expected_concepts": [
        "sweetness can feel cloying without acidity",
        "acidity provides freshness",
        "structural balance",
        "preservation and ageing",
        "concentrated flavour",
        "long finish",
        "style quality depends on integration rather than sugar alone"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Move beyond saying acidity balances sweetness; explain the sensory and ageing effects.",
        "DEVELOPING_RESPONSE": "Connect acidity to freshness, structure, finish, preservation, and integration.",
        "STRONG_RESPONSE": "Show why sugar concentration alone is insufficient and how acidity supports balance, complexity, and development."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_125": {
      "item_id": "OR_125",
      "source_question_id": "OR_125",
      "expected_concepts": [
        "fortification during fermentation",
        "fruit preservation in Ruby styles",
        "limited oxygen exposure",
        "extended oxidative cask ageing for Tawny",
        "colour change",
        "primary fruit versus nut and dried-fruit character",
        "blending and category style"
      ],
      "optional_causal_chain": "CC_FORTIFICATION_RESIDUAL_SUGAR",
      "causal_chain_reference": [
        "CC_FORTIFICATION_RESIDUAL_SUGAR"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Compare both styles using the same production and maturation headings.",
        "DEVELOPING_RESPONSE": "Link vessel, oxygen exposure, and ageing duration to colour and flavour differences.",
        "STRONG_RESPONSE": "Provide a balanced comparison from shared fortification through divergent maturation and final style."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_126": {
      "item_id": "OR_126",
      "source_question_id": "OR_126",
      "expected_concepts": [
        "vintage quality and concentration",
        "producer declaration decision",
        "cask ageing duration",
        "filtration and readiness",
        "bottle ageing requirement",
        "commercial timing",
        "style and longevity judgement"
      ],
      "optional_causal_chain": "CC_FORTIFICATION_RESIDUAL_SUGAR",
      "causal_chain_reference": [
        "CC_FORTIFICATION_RESIDUAL_SUGAR"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "State a category recommendation and support it with wine evidence.",
        "DEVELOPING_RESPONSE": "Consider maturation, release timing, bottle development, market position, and vintage quality.",
        "STRONG_RESPONSE": "Reach a qualified category judgement that integrates wine structure, ageing pathway, commercial timing, and intended style."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_127": {
      "item_id": "OR_127",
      "source_question_id": "OR_127",
      "expected_concepts": [
        "base wine assessment",
        "fortification strength",
        "flor survival for Fino",
        "higher fortification prevents flor for Oloroso",
        "biological versus oxidative ageing",
        "solera maturation",
        "style consequences"
      ],
      "optional_causal_chain": "CC_FLOR_BIOLOGICAL_AGEING -> CC_FORTIFICATION_RESIDUAL_SUGAR",
      "causal_chain_reference": [
        "CC_FLOR_BIOLOGICAL_AGEING",
        "CC_FORTIFICATION_RESIDUAL_SUGAR"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identify the fortification and ageing decision for each style.",
        "DEVELOPING_RESPONSE": "Explain why fortification level controls flor and therefore the ageing environment.",
        "STRONG_RESPONSE": "Evaluate the linked decisions from base-wine selection through fortification, flor, solera ageing, and style."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_128": {
      "item_id": "OR_128",
      "source_question_id": "OR_128",
      "expected_concepts": [
        "partially filled vessels",
        "flor protection from oxidation",
        "acetaldehyde-derived character",
        "fractional blending",
        "refreshing younger wine",
        "consistency across releases",
        "complexity from prolonged maturation"
      ],
      "optional_causal_chain": "CC_FLOR_BIOLOGICAL_AGEING",
      "causal_chain_reference": [
        "CC_FLOR_BIOLOGICAL_AGEING"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Explain both flor and solera rather than treating them as the same process.",
        "DEVELOPING_RESPONSE": "Connect vessel conditions and fractional blending to protection, flavour, continuity, and complexity.",
        "STRONG_RESPONSE": "Discuss the interaction of biological ageing and systematic blending, including benefits and management demands."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_129": {
      "item_id": "OR_129",
      "source_question_id": "OR_129",
      "expected_concepts": [
        "appropriate grape or sweetness target",
        "timing of fortification",
        "retention of high acidity",
        "estufagem or canteiro choice",
        "controlled heat and oxygen exposure",
        "maturation duration",
        "balance of freshness and oxidative character"
      ],
      "optional_causal_chain": "HC_MADEIRA_HEAT_OXIDATIVE_AGEING -> CC_FORTIFICATION_RESIDUAL_SUGAR",
      "causal_chain_reference": [
        "HC_MADEIRA_HEAT_OXIDATIVE_AGEING",
        "CC_FORTIFICATION_RESIDUAL_SUGAR"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Make a clear method recommendation and state the intended sweetness level.",
        "DEVELOPING_RESPONSE": "Justify fortification timing, heating method, oxygen exposure, acidity retention, and maturation.",
        "STRONG_RESPONSE": "Present a coherent style-led production plan with explicit trade-offs between speed, cost, freshness, and complexity."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_130": {
      "item_id": "OR_130",
      "source_question_id": "OR_130",
      "expected_concepts": [
        "Sercial dry",
        "Verdelho medium-dry",
        "Bual medium-sweet",
        "Malmsey sweet",
        "fortification timing",
        "residual sugar",
        "high acidity",
        "heat and oxidative maturation"
      ],
      "optional_causal_chain": "HC_MADEIRA_HEAT_OXIDATIVE_AGEING -> CC_FORTIFICATION_RESIDUAL_SUGAR",
      "causal_chain_reference": [
        "HC_MADEIRA_HEAT_OXIDATIVE_AGEING",
        "CC_FORTIFICATION_RESIDUAL_SUGAR"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identify the style sequence accurately before explaining production.",
        "DEVELOPING_RESPONSE": "Link sweetness to fortification timing while retaining the shared acidity, heating, and oxidation framework.",
        "STRONG_RESPONSE": "Explain the complete style range with accurate category, sweetness, structural, and maturation distinctions."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_131": {
      "item_id": "OR_131",
      "source_question_id": "OR_131",
      "expected_concepts": [
        "Port fortified during fermentation",
        "yeast activity stops",
        "residual sugar retained",
        "Sherry base wine fermented dry first",
        "post-fermentation fortification",
        "fortification level directs ageing style",
        "different final sweetness and structure"
      ],
      "optional_causal_chain": "CC_FORTIFICATION_RESIDUAL_SUGAR -> CC_FLOR_BIOLOGICAL_AGEING",
      "causal_chain_reference": [
        "CC_FORTIFICATION_RESIDUAL_SUGAR",
        "CC_FLOR_BIOLOGICAL_AGEING"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "State when fortification occurs in each wine.",
        "DEVELOPING_RESPONSE": "Explain the purpose and effect on yeast, residual sugar, alcohol, and subsequent ageing.",
        "STRONG_RESPONSE": "Describe both timelines accurately and connect timing to sweetness, biological or oxidative ageing, and final style."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_132": {
      "item_id": "OR_132",
      "source_question_id": "OR_132",
      "expected_concepts": [
        "very ripe or partially raisined Muscat grapes",
        "high sugar concentration",
        "fortification stops fermentation",
        "high residual sugar",
        "warm oxidative maturation",
        "blending across ages",
        "rich dried-fruit and caramel character"
      ],
      "optional_causal_chain": "HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION -> CC_FORTIFICATION_RESIDUAL_SUGAR",
      "causal_chain_reference": [
        "HC_APPASSIMENTO_GRAPE_DRYING_CONCENTRATION",
        "CC_FORTIFICATION_RESIDUAL_SUGAR"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Include concentration, fortification, and maturation in the causal sequence.",
        "DEVELOPING_RESPONSE": "Connect each stage to sugar, alcohol, residual sweetness, texture, and oxidative flavour.",
        "STRONG_RESPONSE": "Explain the complete production chain and how cumulative concentration and ageing create the final style."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_133": {
      "item_id": "OR_133",
      "source_question_id": "OR_133",
      "expected_concepts": [
        "cool service temperature",
        "small suitable glass",
        "modest portion",
        "high sweetness and acidity",
        "aromatic intensity",
        "age and complexity explanation",
        "customer preference"
      ],
      "optional_causal_chain": "HC_SERVICE_TEMPERATURE_GLASS_PROTOCOL",
      "causal_chain_reference": [
        "HC_SERVICE_TEMPERATURE_GLASS_PROTOCOL"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Compare both wines through practical service headings.",
        "DEVELOPING_RESPONSE": "Explain how temperature, portion, glassware, sweetness, acidity, and maturity affect the experience.",
        "STRONG_RESPONSE": "Give a customer-centred comparison with practical service detail and clear style communication."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_134": {
      "item_id": "OR_134",
      "source_question_id": "OR_134",
      "expected_concepts": [
        "bottle storage before service",
        "allowing sediment to settle",
        "careful opening",
        "decanting from sediment",
        "service timing",
        "appropriate temperature",
        "monitoring fragile mature aromas"
      ],
      "optional_causal_chain": "HC_OLD_RED_SEDIMENT_SERVICE -> HC_BOTTLE_STORAGE_STABILITY",
      "causal_chain_reference": [
        "HC_OLD_RED_SEDIMENT_SERVICE",
        "HC_BOTTLE_STORAGE_STABILITY"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Give a judgement on the plan and identify the sediment risk.",
        "DEVELOPING_RESPONSE": "Add bottle handling, settling, light-assisted decanting, timing, and temperature.",
        "STRONG_RESPONSE": "Assess the complete service sequence while balancing sediment removal against the fragility of a mature fortified wine."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_135": {
      "item_id": "OR_135",
      "source_question_id": "OR_135",
      "expected_concepts": [
        "wine should be at least as sweet as the dessert",
        "lemon acidity",
        "wine acidity and freshness",
        "flavour intensity",
        "botrytis and oak character in Sauternes",
        "clean fruit profile in Icewine",
        "reasoned recommendation"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Consider sweetness and acidity before naming a preferred wine.",
        "DEVELOPING_RESPONSE": "Weigh structural and flavour interactions for both options.",
        "STRONG_RESPONSE": "Evaluate both pairings and make a conditional recommendation grounded in sweetness, acidity, intensity, and flavour compatibility."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_136": {
      "item_id": "OR_136",
      "source_question_id": "OR_136",
      "expected_concepts": [
        "customer sweetness preference",
        "high acidity across styles",
        "aperitif versus dessert use",
        "food pairing",
        "age and complexity",
        "service temperature",
        "open-bottle stability"
      ],
      "optional_causal_chain": "HC_MADEIRA_HEAT_OXIDATIVE_AGEING -> HC_SERVICE_TEMPERATURE_GLASS_PROTOCOL",
      "causal_chain_reference": [
        "HC_MADEIRA_HEAT_OXIDATIVE_AGEING",
        "HC_SERVICE_TEMPERATURE_GLASS_PROTOCOL"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Organise the advice by customer need rather than merely listing Madeira categories.",
        "DEVELOPING_RESPONSE": "Connect sweetness, acidity, occasion, pairing, temperature, and storage after opening.",
        "STRONG_RESPONSE": "Provide flexible customer advice across the style range with practical service and use cases."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_137": {
      "item_id": "OR_137",
      "source_question_id": "OR_137",
      "expected_concepts": [
        "Fino first and well chilled",
        "dry light style with savoury starters",
        "Amontillado next with richer dishes",
        "Pedro Ximénez last with dessert or as dessert",
        "increasing sweetness and intensity",
        "appropriate glass and portion",
        "temperature adjustment"
      ],
      "optional_causal_chain": "HC_AMONTILLADO_SERVICE_TEMPERATURE -> HC_SERVICE_TEMPERATURE_GLASS_PROTOCOL",
      "causal_chain_reference": [
        "HC_AMONTILLADO_SERVICE_TEMPERATURE",
        "HC_SERVICE_TEMPERATURE_GLASS_PROTOCOL"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Give a clear sequence and one reason for each position.",
        "DEVELOPING_RESPONSE": "Use sweetness, intensity, food, temperature, and portion to justify the order.",
        "STRONG_RESPONSE": "Recommend a coherent progression that protects delicate styles and matches increasing flavour and sweetness."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_138": {
      "item_id": "OR_138",
      "source_question_id": "OR_138",
      "expected_concepts": [
        "expected nutty dried-fruit or caramel character",
        "intentional oxidative maturation",
        "style consistency",
        "fault indicators such as unintended stale or acetic character",
        "condition and intensity assessment",
        "customer explanation",
        "replacement when genuinely faulty"
      ],
      "optional_causal_chain": "HC_MADEIRA_HEAT_OXIDATIVE_AGEING",
      "causal_chain_reference": [
        "HC_MADEIRA_HEAT_OXIDATIVE_AGEING"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identify a valid expected character and explain why it is not automatically a fault.",
        "DEVELOPING_RESPONSE": "Contrast intentional maturation character with evidence of poor condition or unintended oxidation.",
        "STRONG_RESPONSE": "Give a precise sensory distinction and a customer-safe action based on condition rather than assumption."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_139": {
      "item_id": "OR_139",
      "source_question_id": "OR_139",
      "expected_concepts": [
        "brief skin contact during fermentation",
        "phenolic extraction from red grape skins",
        "color intensity from anthocyanin transfer",
        "tannin balance in rosé vs red wines",
        "timing of skin separation from must",
        "production method choice: saignée vs pressing",
        "final wine style: dry, fresh, or structured depending on contact duration"
      ],
      "optional_causal_chain": "HC_MACERATION_EXTRACTION",
      "causal_chain_reference": [
        "HC_MACERATION_EXTRACTION"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identify skin contact as the source of color and tannin in rosé, but do not yet connect duration to specific style outcomes.",
        "DEVELOPING_RESPONSE": "Link extended skin contact to deeper color and higher tannin, and explain why rosé uses shorter contact than red wine. Begin connecting contact duration to final style characteristics.",
        "STRONG_RESPONSE": "Show a continuous causal chain: duration of skin contact → anthocyanin extraction → color depth, tannin extraction → wine style ranging from pale, fresh rosé to darker, more tannic styles. Distinguish saignée (continuous bleeding) from pressing (post-fermentation extraction)."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_140": {
      "item_id": "OR_140",
      "source_question_id": "OR_140",
      "expected_concepts": [
        "Provence: pale color, fresh, minimal oak, early harvest for acidity",
        "Navarra: deeper color, higher alcohol potential, longer skin contact, some oak aging",
        "Rhône/Tavel: darkest color, higher tannin, longer maceration, warm climate ripeness",
        "climate influence on ripe grape availability and harvest timing",
        "production method as region-specific convention",
        "oak aging decisions by region and market positioning",
        "acid preservation in hot climates"
      ],
      "optional_causal_chain": "HC_ALTITUDE_TEMPERATURE -> HC_CLIMAT_RIPENESS_TIMING",
      "causal_chain_reference": [
        "HC_ALTITUDE_TEMPERATURE",
        "HC_CLIMAT_RIPENESS_TIMING"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Name the three regions and note that they produce rosés of different colors. Do not yet connect climate to production method.",
        "DEVELOPING_RESPONSE": "Describe the color progression (pale Provence → darker Tavel) and link this to skin contact duration. Begin explaining how climate (warm vs. cooler, altitude) influences harvest timing and acid retention.",
        "STRONG_RESPONSE": "Show how each region's climate determines ripeness level and residual acid at harvest, which then drives production choices: shorter maceration and earlier harvest in cool Provence to preserve freshness, longer contact and oak potential in warm Tavel. Explain the causal chain from climate → harvest timing → production method → final style."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_141": {
      "item_id": "OR_141",
      "source_question_id": "OR_141",
      "expected_concepts": [
        "Vintage Port sediment formation over decades",
        "tannin evolution in bottle: gradual softening and integration",
        "oxidative character development in fortified wine",
        "oxygen ingress through cork over long aging",
        "young Port: high tannin, benefit from aeration, minimal sediment",
        "mature Port: soft tannin, complex tertiary aromas, significant sediment",
        "decanting as a service choice: timing, vessel, duration",
        "preservation of aromatic complexity in old Port",
        "health and consumption safety in aged wine"
      ],
      "optional_causal_chain": "HC_BOTTLE_TANNIN_SOFTENING -> HC_BAROLO_TERTIARY_EVOLUTION -> HC_OLD_RED_SEDIMENT_SERVICE",
      "causal_chain_reference": [
        "HC_BOTTLE_TANNIN_SOFTENING",
        "HC_BAROLO_TERTIARY_EVOLUTION",
        "HC_OLD_RED_SEDIMENT_SERVICE"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Acknowledge that Port ages in bottle and sediment forms, but do not yet distinguish young from mature or explain the causal link between aging and decanting necessity.",
        "DEVELOPING_RESPONSE": "Explain that young Port benefits from decanting aeration and mature Port has soft tannin already. Begin connecting sediment formation to aging duration and oxidative character development.",
        "STRONG_RESPONSE": "Present the full causal chain for each age category: young Port → high tannin, low sediment, volatile aromas → aeration useful, decant before service. Mature Port → soft tannin, high sediment, stable oxidative character → gentle decant to separate sediment while preserving aromatic integrity. Show how oxidative aging in the bottle transforms the wine's character and how service strategy must adapt."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_142": {
      "item_id": "OR_142",
      "source_question_id": "OR_142",
      "expected_concepts": [
        "Burgundy: smaller oak (225-liter puncheon), high-surface-area oxidation",
        "Bordeaux: large oak (225–500-liter barrel), slower oxidation",
        "Pinot Noir tannin structure: softer, integrated during barrel aging",
        "Cabernet tannin structure: firmer, requires longer aging for integration",
        "volatile aromatic compounds: fresh fruit in young wine, how aeration affects expression",
        "decanting duration: brief aeration vs. extended air exposure",
        "service glassware choice and aeration effect",
        "oxidation risk: controlled aeration vs. over-exposure"
      ],
      "optional_causal_chain": "HC_AERATION_YOUNG_STRUCTURED_WINE -> HC_BARREL_SIZE_OAK_CONTACT",
      "causal_chain_reference": [
        "HC_AERATION_YOUNG_STRUCTURED_WINE",
        "HC_BARREL_SIZE_OAK_CONTACT"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identify that both wines benefit from aeration but do not yet explain the differences in their aeration needs or the regional production differences.",
        "DEVELOPING_RESPONSE": "Explain that Burgundy receives more oxidation during barrel aging (smaller, more surface area) and therefore may need less decanting aeration; Bordeaux in larger barrel receives less barrel oxidation and may benefit from more aeration. Begin connecting production method to service strategy.",
        "STRONG_RESPONSE": "Construct a full causal chain for each region: Burgundy barrel method → higher oxidation in barrel → softer tannin at bottling → moderate aeration for aromatic expression, short decant (30 min) OR immediate service. Bordeaux barrel method → controlled barrel oxidation → firmer tannin at bottling → longer aeration beneficial for tannin integration and aromatic opening, decant 1–2 hours. Show how production method determines bottle-maturity profile and thus service strategy."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_143": {
      "item_id": "OR_143",
      "source_question_id": "OR_143",
      "expected_concepts": [
        "SAT appearance scale: pale to deep color intensity",
        "hue shift: bright red/purple (young) → garnet (mature) → brown (old)",
        "brownish edge as sign of oxidation in bottle over time",
        "pale color: light extraction, cool climate, lighter varietal, or sulfite protection during storage",
        "medium color with brown edge: moderately mature bottle, possible bottle oxidation or heat damage",
        "production method affecting initial color: carbonic maceration (lighter), long maceration (deeper)",
        "storage conditions: light exposure, temperature, cork condition, aging potential"
      ],
      "optional_causal_chain": "HC_BAROLO_TERTIARY_EVOLUTION -> HC_BOTTLE_STORAGE_STABILITY -> HC_HEAT_PREMATURE_BOTTLE_AGEING",
      "causal_chain_reference": [
        "HC_BAROLO_TERTIARY_EVOLUTION",
        "HC_BOTTLE_STORAGE_STABILITY",
        "HC_HEAT_PREMATURE_BOTTLE_AGEING"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Describe what pale-to-medium with brownish edge means (a relatively mature wine) but do not yet explain the causal mechanisms that created those colors.",
        "DEVELOPING_RESPONSE": "Connect the brownish edge to oxidation and maturity in bottle. Begin explaining how production method (maceration duration) and initial color extraction affect the starting point for aging.",
        "STRONG_RESPONSE": "Explain the full causal chain: initial color determined by grape varietal + maceration method + extraction during fermentation. During storage in bottle → gradual oxidation through natural cork permeability → color shift from red/purple toward garnet and brown. Brownish edge specifically indicates advanced age or oxidative stress. Link this back to production choices: wines with intention for aging receive longer maceration and deeper initial color; wines for early drinking receive shorter maceration and lighter initial color. Storage conditions (temperature stability, light, cork quality) then determine the rate of color evolution."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_144": {
      "item_id": "OR_144",
      "source_question_id": "OR_144",
      "expected_concepts": [
        "SAT nose categories: primary (varietal), secondary (fermentation), tertiary (aging)",
        "butter and cream notes: diacetyl from malolactic fermentation",
        "vanilla: oak contact (French oak typically smoother than American)",
        "stone fruit: primary varietal character (Chardonnay typical)",
        "malolactic fermentation as a deliberate production choice",
        "timing of MLF: in-barrel vs. pre-barrel, complete vs. partial",
        "oak contact: barrel type, new vs. used, duration",
        "microbial stability: MLF implications for pH and SO₂",
        "style intent: fruit-forward vs. creamy oxidative styles"
      ],
      "optional_causal_chain": "HC_MLF_ACIDITY_TEXTURE -> HC_MLF_STYLE_CONTROL -> HC_BARREL_SIZE_OAK_CONTACT",
      "causal_chain_reference": [
        "HC_MLF_ACIDITY_TEXTURE",
        "HC_MLF_STYLE_CONTROL",
        "HC_BARREL_SIZE_OAK_CONTACT"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identify butter/cream as coming from MLF and vanilla from oak, but do not yet explain the causal relationship between these production methods and the sensorial outcome.",
        "DEVELOPING_RESPONSE": "Explain that MLF converts malic acid and produces diacetyl (butter), and that oak contact provides vanilla/spice. Begin connecting these to intentional style creation.",
        "STRONG_RESPONSE": "Build the full causal chain: winemaker chooses to allow MLF → malic acid converted to lactic acid by bacteria → production of diacetyl as byproduct → butter/cream character in nose. Simultaneously, barrel contact → oak phenolics extraction → vanilla/spice/toastiness. The combination of both choices creates a 'buttery oak-aged white' style distinct from unoaked fruit-forward whites. Explain how timing of MLF (in-barrel accelerates oak integration) and barrel selection (French vs. American oak and new vs. used) refine the final balance."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_145": {
      "item_id": "OR_145",
      "source_question_id": "OR_145",
      "expected_concepts": [
        "Madeira estufagem: controlled heat aging (warm room 45–50°C or heated wine tanks)",
        "oxidative ripening during estufagem: browning, oxidation of phenolics, Maillard reactions",
        "dried fruit, nut, caramel, chocolate notes as characteristic Madeira profile",
        "long-term bottle storage after estufagem: slow oxidation through cork",
        "fault indicators: sharpness, volatility, acetic acid (vinegar), cork taint (musty)",
        "maderization: unintended oxidation in still wine (a fault), vs. intentional in Madeira (desired)",
        "sensorial cues for distinguishing intentional from unintended oxidation",
        "food pairing implications: oxidative character enables food pairing that young wine cannot achieve"
      ],
      "optional_causal_chain": "HC_MADEIRA_HEAT_OXIDATIVE_AGEING -> HC_EXCESSIVE_WHITE_OXIDATION -> HC_OPEN_BOTTLE_OXYGEN_CONTROL",
      "causal_chain_reference": [
        "HC_MADEIRA_HEAT_OXIDATIVE_AGEING",
        "HC_EXCESSIVE_WHITE_OXIDATION",
        "HC_OPEN_BOTTLE_OXYGEN_CONTROL"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Identify Madeira's heat-aging process and note that it creates oxidative character, but do not yet distinguish between intentional oxidation and wine fault.",
        "DEVELOPING_RESPONSE": "Explain that Madeira's estufagem creates dried fruit and nutty notes through intentional oxidation. Begin identifying a few sensorial cues (acid sharpness, vinegar tones) that would indicate fault rather than intent.",
        "STRONG_RESPONSE": "Show the complete causal chain: estufagem (controlled 45–50°C heat) → rapid oxidation of phenolics, sugars, amino acids → brown color, dried-fruit aromas, caramel/chocolate notes, lower acidity. Then contrast: intentional Madeira oxidation is balanced, warm, integrative; wine fault oxidation is sharp, volatile, unpleasant (acetic acid, vinegar character). Explain how sensorial assessment distinguishes: Madeira shows smooth caramel and balanced acidity; maderization shows sharp acidity and chemical off-notes. Connect this to product history: Madeira's heat treatment is a documented production choice; maderization indicates storage failure."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_146": {
      "item_id": "OR_146",
      "source_question_id": "OR_146",
      "expected_concepts": [
        "young white wine: cool (10–12°C), dark, short-term storage (months to 2 years), upright bottle position",
        "structured red wine for aging: consistent cool temperature (12–15°C), dark, horizontal position (cork must stay moist), humidity 50–80% for cork integrity",
        "Tawny Port: tolerant of temperature variation, lower UV sensitivity (oxidized already), upright position (ready to drink), shelf-stable",
        "temperature stability as critical factor: fluctuation causes expansion/contraction, cork movement, oxidation acceleration",
        "light exposure: UV-induced premature oxidation in white/light wines",
        "humidity: cork drying in low-humidity environments, cork rot in high humidity",
        "bottle position: cork contact critical for sealing; screw-cap and synthetic closures reduce this concern",
        "storage location suitability: wine fridge, cellar, closet vs. above radiator"
      ],
      "optional_causal_chain": "HC_BOTTLE_STORAGE_STABILITY -> HC_HEAT_PREMATURE_BOTTLE_AGEING",
      "causal_chain_reference": [
        "HC_BOTTLE_STORAGE_STABILITY",
        "HC_HEAT_PREMATURE_BOTTLE_AGEING"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Provide basic storage recommendations (cool, dark, quiet) without explaining the causal link between storage condition and wine preservation.",
        "DEVELOPING_RESPONSE": "For each wine type, explain why certain conditions matter (e.g., young white needs cool to slow oxidation, red needs horizontal for cork contact). Begin connecting storage choices to wine's aging potential and intended consumption timeline.",
        "STRONG_RESPONSE": "For each wine type, explain the complete causal chain: young white is sensitive to oxidation → requires cool, dark, stable temperature environment. Structured red intends long aging → requires horizontal position to maintain cork hydration → requires consistent cool temperature to prevent tannin evolution acceleration → requires darkness to prevent UV oxidation. Mature Tawny Port is pre-oxidized and stable → tolerates wider temperature and light range → can be stored upright → suitable for long-term shelf storage. Show how storage strategy is driven by wine's composition, aging intent, and closure type."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_147": {
      "item_id": "OR_147",
      "source_question_id": "OR_147",
      "expected_concepts": [
        "sulfite sensitivity: true allergy vs. sensitivity to high SO₂ levels",
        "SO₂ levels by wine type: sweet wines (higher), dry wines (lower), organic wines (variable)",
        "histamines: higher in red wine (skin contact) than white, accumulate with age and microbial activity",
        "high alcohol wines: above 15%, thermophilic yeast and sugar-to-alcohol conversion, sensorial warmth/burn",
        "alcohol sensitivity: individual variation, medications, health conditions",
        "customer intake: asking about specific symptoms, allergies, medications",
        "wine selection guidance: low-sulfite options, histamine-lower white wines, lower-alcohol alternatives (12–13%)",
        "transparent communication: limitations of sommelier role vs. medical advice",
        "labeling and transparency: SO₂ declarations (often mandatory in EU), histamine not required"
      ],
      "optional_causal_chain": null,
      "causal_chain_reference": [],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Acknowledge the customer's concerns and provide basic wine categories (organic, low-alcohol) without explaining the science or intake process.",
        "DEVELOPING_RESPONSE": "Explain what sulfites do (preservation) and that red wine contains higher histamines. Begin discussing how to gather customer information and suggest specific wine types.",
        "STRONG_RESPONSE": "Conduct a structured intake: ask about specific symptoms, reactions, medications, and allergies. Explain the science: SO₂ is a natural fermentation byproduct and intentional preservative; levels vary by wine type and producer; true sulfite allergy is rare. Histamines are amine compounds from microbial and enzymatic activity; higher in red (skin contact) and aged wines; lower in fresh, young white wines. Alcohol fermentation converts sugars; thermophilic yeasts produce higher-alcohol wines with sensorial intensity. Recommend based on science: low-alcohol white wine (histamine-lower, lighter alcohol), minimal-added-SO₂ options, or winemaker-specific knowledge of production. Clarify your role: recommend based on wine knowledge, not as medical advice; customer should consult physician for true allergies."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    },
    "OR_148": {
      "item_id": "OR_148",
      "source_question_id": "OR_148",
      "expected_concepts": [
        "vintage definition: annual variation in growing conditions and harvest quality",
        "warm vintage: higher sugar ripeness, lower acid, ripe tannin, earlier harvest possible",
        "cool vintage: lower sugar, higher acid retention, greener tannin, delayed harvest risk",
        "harvest timing decision: balance ripeness against acid preservation",
        "fermentation temperature: control for yeast health and aroma expression",
        "malolactic fermentation: timing and extent as response to acid level and wine structure",
        "oak aging: duration adjustment (longer in cool vintage for structure integration, shorter in warm for balance)",
        "blending decision: varietal proportions adjusted by vintage character (more Cabernet in cool year for structure, more Merlot in warm year for softness)",
        "appellation regulations: constraint on flexibility (e.g., Bordeaux blending rules)"
      ],
      "optional_causal_chain": "HC_BORDEAUX_BLEND_VINTAGE_VARIATION -> HC_ALTITUDE_TEMPERATURE",
      "causal_chain_reference": [
        "HC_BORDEAUX_BLEND_VINTAGE_VARIATION",
        "HC_ALTITUDE_TEMPERATURE"
      ],
      "feedback_profile": {
        "FOUNDATIONAL_RESPONSE": "Acknowledge that vintages differ in ripeness and identify at least two production choices that vary by vintage without explaining the causal logic.",
        "DEVELOPING_RESPONSE": "Explain that warm vintages produce riper fruit and cooler vintages higher acid, and that these differences drive harvest timing and oak aging decisions. Begin linking vintage character to fermentation management.",
        "STRONG_RESPONSE": "Show the complete causal chain for both scenarios: warm vintage → higher sugar, lower acid at harvest → harvest earlier if weather permits, use cooler fermentation to preserve volatiles, limited MLF to retain structure, moderate oak (12–18 months) for balance, blend toward softer varietals (more Merlot). Cool vintage → lower sugar, higher acid at harvest → harvest later if weather allows, manage fermentation carefully to avoid stuck fermentation, encourage complete MLF for acid softening, longer oak aging (18–24 months) for phenolic integration, blend toward structuring varietals (more Cabernet). Show how each decision flows from the vintage's fundamental character and how the producer uses technique to optimize quality within the vintage's potential."
      },
      "governance_flags": {
        "safe_for_examiner": false,
        "examiner_scoring_allowed": false,
        "official_wset_question": false,
        "training_item_only": true,
        "uses_llm": false,
        "uses_api": false,
        "uses_embeddings": false,
        "uses_vector_db": false,
        "cloud_services_active": false,
        "public_frontend_active": false,
        "open_response_lab_active": false
      }
    }
  },
  "feedback_fields": {
    "present_concepts": "concepts_detected",
    "missing_concepts": "concepts_absent",
    "causal_link_feedback": "missing_causal_reasoning",
    "revision_suggestion": "improvement_suggestions"
  },
  "feedback_prohibited": [
    "mark",
    "score",
    "percentage",
    "pass_fail",
    "wset_equivalence",
    "examiner_judgement",
    "official_grade"
  ],
  "evaluation_metadata": {
    "schema_version": "open_response_evaluation_v1",
    "command_verbs_loaded": [
      "explain",
      "describe",
      "justify",
      "assess",
      "evaluate",
      "compare",
      "why",
      "how",
      "discuss",
      "identify and explain",
      "outline",
      "state",
      "list",
      "recommend"
    ],
    "governance": {
      "safe_for_examiner": false,
      "examiner_scoring_allowed": false,
      "formative_only": true
    }
  },
  "expansion_history": [
    {
      "phase": "P2.4",
      "items_added": 15,
      "new_pool_size": 148
    },
    {
      "phase": "OR_EXPANSION_BATCH_4",
      "items_added": 32,
      "new_pool_size": 148
    }
  ],
  "assessment_intelligence": {
    "schema_version": "assessment_intelligence_v1",
    "phase": "X.1",
    "activation_status": "active_private_lab",
    "governance": {
      "safe_for_examiner": false,
      "examiner_scoring_allowed": false,
      "training_use_only": true
    },
    "command_verbs": {
      "describe": {
        "cognitive_level": "recall + observation",
        "definition": "State the characteristics, features, or appearance of something. Do not explain causes or reasons.",
        "do": [
          "Name features",
          "Use SAT vocabulary (for tasting questions)",
          "Be specific",
          "Cover all relevant dimensions"
        ],
        "do_not": [
          "Explain why",
          "Give opinions",
          "Compare to other examples",
          "Add causes or mechanisms"
        ]
      },
      "explain": {
        "cognitive_level": "comprehension + causal reasoning",
        "definition": "Give reasons for, or account for, a fact, phenomenon, or outcome. Must include a cause-and-effect relationship.",
        "do": [
          "State the cause",
          "State the mechanism or process",
          "State the outcome or effect",
          "Use WSET technical vocabulary"
        ],
        "do_not": [
          "Merely name or list (that is describing, not explaining)",
          "Give unsupported assertions"
        ]
      },
      "compare": {
        "cognitive_level": "analysis + synthesis",
        "definition": "Identify similarities and differences between two or more items. Both similarities AND differences are expected unless otherwise stated.",
        "do": [
          "Address both similarities and differences",
          "Use parallel structure for clarity",
          "Cover multiple dimensions"
        ],
        "do_not": [
          "Describe each item separately without linking them",
          "Cover only one item in detail"
        ]
      },
      "assess": {
        "cognitive_level": "evaluation + evidence-based judgement",
        "definition": "Make an informed judgement about the value, quality, or significance of something, based on stated criteria.",
        "do": [
          "State a clear judgement",
          "Support with specific tasting or regional evidence",
          "Use appropriate WSET criteria"
        ],
        "do_not": [
          "Give unsupported opinion",
          "List observations without a conclusion"
        ]
      },
      "evaluate": {
        "cognitive_level": "critical thinking + synthesis",
        "definition": "Make a substantiated judgement, weighing the significance of evidence. Often implies a broader or more nuanced consideration than 'assess'.",
        "do": [
          "Weigh multiple pieces of evidence",
          "State a clear conclusion",
          "Acknowledge complexity where relevant"
        ],
        "do_not": [
          "Simply list facts (that is describing)",
          "Give opinion without evidence"
        ]
      },
      "discuss": {
        "cognitive_level": "balanced analysis + synthesis",
        "definition": "Examine or explore a topic from multiple perspectives. Implies consideration of more than one viewpoint or dimension.",
        "do": [
          "Present at least two perspectives or factors",
          "Support each with evidence",
          "Show relationships between perspectives"
        ],
        "do_not": [
          "Present only one viewpoint",
          "Give opinion without evidence for each perspective"
        ]
      },
      "recommend": {
        "cognitive_level": "application + justified choice",
        "definition": "Select an appropriate option for the stated context and support the choice with relevant evidence and practical consequences.",
        "do": [
          "State the recommendation explicitly",
          "Use evidence from the scenario",
          "Explain why the recommendation suits the intended style or customer",
          "Acknowledge a material trade-off where relevant"
        ],
        "do_not": [
          "List options without choosing",
          "Recommend without evidence",
          "Present personal preference as sufficient justification"
        ]
      },
      "identify and explain": {
        "cognitive_level": "recall + comprehension",
        "definition": "Two-part task: (1) Name or spot the item/concept/characteristic, then (2) give reasons or explain its significance. Both parts are required.",
        "do": [
          "Clearly name what you are identifying",
          "Then explain its significance or function",
          "Use technical vocabulary"
        ],
        "do_not": [
          "Only name without explanation",
          "Only explain without clearly identifying first"
        ]
      },
      "justify": {
        "cognitive_level": "reasoning + defence of position",
        "definition": "Give reasons or evidence in support of a stated position or choice. The position is given; you must defend it.",
        "do": [
          "Select the strongest, most specific supporting evidence",
          "Link evidence directly to the position",
          "Use WSET vocabulary"
        ],
        "do_not": [
          "Argue against the position",
          "Give generic descriptions unrelated to the claim"
        ]
      }
    },
    "sat_quality_levels": {
      "defectuoso": {
        "level_en": "faulty",
        "description": "Wine has identifiable faults that make it unpleasant or undrinkable",
        "signal_observations": [
          "turbio",
          "no limpia (nariz)",
          "Brett",
          "corcho",
          "oxidado",
          "reducido",
          "acidez volátil alta"
        ]
      },
      "pobre": {
        "level_en": "poor",
        "description": "Significant flaws or imbalances; lacks quality without being outright faulty",
        "signal_observations": [
          "intensidad ligera sin complejidad",
          "final corto",
          "desequilibrio de acidez/alcohol/tanino"
        ]
      },
      "aceptable": {
        "level_en": "acceptable",
        "description": "Straightforward wine with limited complexity; no obvious faults",
        "signal_observations": [
          "aromas simples",
          "fruta primaria solo",
          "final corto a medio",
          "poco cuerpo"
        ]
      },
      "bueno": {
        "level_en": "good",
        "description": "Good expression of variety and/or region; some complexity",
        "signal_observations": [
          "fruta primaria bien definida",
          "algo de complejidad secundaria",
          "final medio",
          "equilibrio correcto"
        ]
      },
      "muy bueno": {
        "level_en": "very good",
        "description": "Clearly expressive, well-structured, some complexity; could improve with ageing",
        "signal_observations": [
          "aromas secundarios y terciarios presentes",
          "final medio(+) a largo",
          "equilibrio claro",
          "complejidad"
        ]
      },
      "excelente": {
        "level_en": "outstanding",
        "description": "Exceptional complexity, length, balance and expression; will develop further",
        "signal_observations": [
          "aromas terciarios pronunciados",
          "final largo",
          "equilibrio perfecto",
          "carácter varietal y regional muy definido",
          "potencial de envejecimiento claro"
        ]
      }
    },
    "evidence_requirements": {
      "principles": {
        "descriptor_validity": "Aroma/flavour descriptors must be accurate and correct for the wine",
        "flexibility": "Examiners accept descriptors beyond the WSET Lexicon if accurate",
        "primary_secondary_tertiary_required": "For complex wines, marks require evidence from ALL THREE aroma categories",
        "simple_wine_exception": "For demonstrably simple wines, 'simple' can substitute tertiary requirement; remaining marks from primary only",
        "flavour_mirrors_aroma": "Palate flavour descriptors should mirror nose aroma descriptors",
        "conclusion_must_be_supported": "Quality and readiness conclusions must flow from tasting observations"
      },
      "strong_patterns": {
        "distinction_level_response": [
          "Clear intensity statement for nose and palate",
          "Primary descriptors: specific (e.g., 'lemon, peach, melon, pineapple') not generic ('fruity')",
          "Secondary: MLF (butter/cream/cheese) or oak (vanilla/cedar/smoke/toast) identified and attributed",
          "Tertiary: bottle-age (honey/nutty/petroleum/leather/tobacco/forest floor) identified and attributed",
          "Development stage correctly identified (joven/en evolución/evolucionado)",
          "All palate scale elements addressed: sweetness, acidity, [tannin for reds], alcohol, body, intensity, finish",
          "Quality level matches wine complexity evidenced (e.g., very good = secondary+tertiary noted)",
          "Readiness conclusion is logical given development stage observed"
        ]
      }
    },
    "common_response_failures": [
      {
        "id": "CRF_01",
        "failure": "Describing when explaining is required",
        "description": "Candidate lists facts without providing causal links",
        "example": "Warm climates have riper fruit. (for an explain question)",
        "correction": "State the mechanism: 'Higher temperatures accelerate sugar accumulation and phenolic ripening, producing wines with higher alcohol and riper fruit character.'"
      },
      {
        "id": "CRF_02",
        "failure": "Insufficient breadth for mark allocation",
        "description": "Candidate gives one detailed point for a 4-mark question",
        "example": "MLF softens wine acidity. (1 point only for 4-mark question)",
        "correction": "MLF converts malic to lactic acid (1); reducing overall acidity (1); adding creamy/buttery texture (1); used for full-bodied white wines requiring less sharp acidity (1)"
      },
      {
        "id": "CRF_03",
        "failure": "Non-SAT vocabulary in tasting",
        "description": "Candidate uses sensory language outside the WSET SAT scale",
        "example": "The wine tastes elegant and complex",
        "correction": "Use scale terms: 'medium(+) intensity, clear secondary and tertiary complexity, well-balanced, long finish'"
      },
      {
        "id": "CRF_04",
        "failure": "Quality level inconsistent with tasting notes",
        "description": "Candidate selects Outstanding after noting simple/primary character",
        "example": "Primary fruit only, short finish → 'Outstanding quality'",
        "correction": "Simple wine with short finish = Acceptable quality"
      },
      {
        "id": "CRF_05",
        "failure": "Omitting readiness conclusion",
        "description": "Candidate completes quality but forgets readiness scale",
        "example": null,
        "correction": "Always conclude with both quality level AND readiness level for Unit 2"
      },
      {
        "id": "CRF_06",
        "failure": "Mixing descriptors across categories",
        "description": "Candidate assigns tertiary descriptors as primary (e.g. honey listed as primary aroma)",
        "example": "Primary: honey, citrus, vanilla",
        "correction": "Honey is tertiary (bottle ageing); vanilla is secondary (oak); citrus is primary. Assign correctly to earn marks."
      },
      {
        "id": "CRF_07",
        "failure": "Ignoring the simple wine exception",
        "description": "Candidate attempts to identify tertiary aromas for a simple wine and loses time/marks on non-existent complexity",
        "example": null,
        "correction": "For simple wines: state 'simple' (1 mark) + 4–5 primary descriptors. Do not invent secondary or tertiary aromas."
      }
    ],
    "improvement_patterns": [
      {
        "id": "IP_01",
        "from": "Vague descriptor",
        "to": "Specific WSET descriptor",
        "example_before": "smells fruity",
        "example_after": "primary aromas of ripe black cherry, plum, and cassis"
      },
      {
        "id": "IP_02",
        "from": "Opinion-based quality",
        "to": "Evidence-grounded quality",
        "example_before": "I think this is a very good wine",
        "example_after": "Very good quality: medium(+) intensity, secondary oak complexity (vanilla, cedar), balanced structure, medium(+) finish"
      },
      {
        "id": "IP_03",
        "from": "Description when explanation required",
        "to": "Causal chain",
        "example_before": "Cool climates have high acidity",
        "example_after": "In cool climates, lower temperatures slow sugar accumulation and preserve malic acid, resulting in higher acidity in the finished wine"
      },
      {
        "id": "IP_04",
        "from": "Single-sided comparison",
        "to": "Linked comparison",
        "example_before": "Chablis is cool. Meursault uses oak.",
        "example_after": "Chablis is cool and unoaked, producing lean mineral Chardonnay; Meursault has a slightly warmer mesoclimate and typically uses oak ageing, producing fuller, richer wines"
      },
      {
        "id": "IP_05",
        "from": "Missing structural elements in SAT",
        "to": "Complete palate coverage",
        "example_before": "The palate has red fruit and oak flavours",
        "example_after": "Dry; high acidity; medium tannin; medium(+) alcohol; medium(+) body; medium(+) intensity; primary red cherry, secondary vanilla and cedar; medium(+) finish"
      },
      {
        "id": "IP_06",
        "from": "Tertiary aromas omitted for complex wine",
        "to": "All three aroma categories covered",
        "example_before": "Aromas of red cherry, vanilla, and toast",
        "example_after": "Primary: red cherry, raspberry. Secondary: vanilla, cedar (oak), buttery (MLF). Tertiary: leather, earth, forest floor (bottle development)"
      }
    ],
    "mentor_hints_by_topic": {
      "SAT_appearance": {
        "common_errors": [
          "Forgetting to assess clarity",
          "Using non-SAT vocabulary (e.g. 'pretty', 'dark')"
        ],
        "hint": "Work through Appearance in order: clarity → intensity → colour. Each element has its own scale. Colour must match the wine type (white, rosé, red)."
      },
      "SAT_nose": {
        "common_errors": [
          "Mixing primary/secondary/tertiary without assigning categories",
          "Listing generic 'fruit' without specifics"
        ],
        "hint": "After stating condition (clean/faulty) and intensity, identify aromas by category: primary (fruit, floral, vegetal), secondary (oak, MLF, yeast), tertiary (bottle ageing, oxidation). At least one specific descriptor per category earns the mark."
      },
      "SAT_palate": {
        "common_errors": [
          "Omitting acidity or tannin assessment",
          "Treating 'body' as a flavour rather than a structural element",
          "Confusing finish length scales"
        ],
        "hint": "For palate, cover all nine elements in order: sweetness, acidity, tannin (red only), alcohol, body, flavour intensity, flavour characteristics, finish. Body and finish are structural conclusions, not flavours."
      },
      "SAT_quality": {
        "common_errors": [
          "Selecting quality level without justification from tasting notes",
          "Using 'excelente' for wines with no tertiary complexity"
        ],
        "hint": "Quality level must be consistent with your tasting notes. Outstanding requires: pronounced intensity + all three aroma categories + balance + long finish. Simple wines cannot be outstanding."
      },
      "SAT_readiness": {
        "common_errors": [
          "Mismatching readiness with development stage",
          "Selecting 'demasiado joven' for a developing wine"
        ],
        "hint": "'Can drink now but has potential' is the correct answer for most premium wines with developing complexity. Only select 'too young' if the wine is clearly unresolved (high unintegrated tannin, no development)."
      },
      "short_answer_structure": {
        "common_errors": [
          "Giving only one reason for a multi-mark question",
          "Explaining without specifying the cause"
        ],
        "hint": "Count the marks. A 4-mark explain question needs 4 distinct causal links. One thorough sentence per link is the target. Do not repeat the same point in different words."
      },
      "MCQ_strategy": {
        "common_errors": [
          "Overthinking distractors",
          "Selecting partially correct answers"
        ],
        "hint": "For MCQ, eliminate clearly wrong options first. The correct answer will be fully accurate, not partially. WSET uses precise vocabulary — 'dry' is not the same as 'off-dry'."
      }
    }
  },
  "governance_flags": {
    "safe_for_examiner": false,
    "examiner_scoring_allowed": false,
    "official_wset_question": false,
    "training_item_only": true,
    "uses_llm": false,
    "uses_api": false,
    "uses_embeddings": false,
    "uses_vector_db": false,
    "cloud_services_active": false,
    "public_frontend_active": false,
    "open_response_lab_active": false
  },
  "source_bank_total": 148
};
