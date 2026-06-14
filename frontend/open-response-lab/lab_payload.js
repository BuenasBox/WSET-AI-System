window.OPEN_RESPONSE_LAB_PAYLOAD = {
  "lab_contract": "private_open_response_lab_runtime_mvp",
  "activation_status": "active_private_lab",
  "pool_size": 41,
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
        "open_response_798"
      ],
      "source_question_ids": [
        "798"
      ]
    },
    "standard_practice": {
      "session_size": 2,
      "item_ids": [
        "open_response_798",
        "open_response_799"
      ],
      "source_question_ids": [
        "798",
        "799"
      ]
    },
    "extended_practice": {
      "session_size": 4,
      "item_ids": [
        "open_response_798",
        "open_response_799",
        "open_response_800",
        "open_response_801"
      ],
      "source_question_ids": [
        "798",
        "799",
        "800",
        "801"
      ]
    },
    "mock_theory_2": {
      "session_size": 4,
      "item_ids": [
        "open_response_798",
        "open_response_799",
        "open_response_800",
        "open_response_853"
      ],
      "source_question_ids": [
        "798",
        "799",
        "800",
        "853"
      ]
    }
  },
  "items": [
    {
      "item_id": "open_response_18",
      "source_question_id": "18",
      "stem": "\u00bfCu\u00e1l es una consecuencia del uso excesivo de sulfitos?",
      "topic": "winemaking",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_798",
      "source_question_id": "798",
      "stem": "Explique c\u00f3mo pr\u00e1cticas sostenibles certificadas u org\u00e1nicas pueden aumentar los costes de producci\u00f3n y contribuir a la diferenciaci\u00f3n comercial del vino.",
      "topic": "sostenibilidad",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_799",
      "source_question_id": "799",
      "stem": "Justifica el uso de la fermentaci\u00f3n malol\u00e1ctica en la producci\u00f3n de ciertos estilos de vino blanco y c\u00f3mo contribuye a la calidad final.",
      "topic": "fermentaci\u00f3n malol\u00e1ctica",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "fermentaci\u00f3n",
        "malol\u00e1ctica"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_800",
      "source_question_id": "800",
      "stem": "Explica c\u00f3mo la altitud puede influir en el estilo de un vino tinto.",
      "topic": "altitud",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "altitud"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_801",
      "source_question_id": "801",
      "stem": "Explique c\u00f3mo la orientaci\u00f3n y la pendiente del vi\u00f1edo pueden afectar la maduraci\u00f3n de la uva.",
      "topic": "orientaci\u00f3n",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "maduraci\u00f3n",
        "pendiente",
        "orientaci\u00f3n"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_802",
      "source_question_id": "802",
      "stem": "Describa c\u00f3mo las pr\u00e1cticas de manejo en la bodega pueden reducir el riesgo de oxidaci\u00f3n en vinos blancos.",
      "topic": "oxidaci\u00f3n",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_803",
      "source_question_id": "803",
      "stem": "Explique la influencia de la elecci\u00f3n de levaduras en el perfil sensorial del vino.",
      "topic": "levaduras",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_804",
      "source_question_id": "804",
      "stem": "Explique c\u00f3mo el drenaje del suelo puede influir en el vigor de la vid y en el estilo del vino.",
      "topic": "suelo",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_805",
      "source_question_id": "805",
      "stem": "Compare c\u00f3mo la elecci\u00f3n de roble americano o franc\u00e9s puede afectar los aromas, el tanino y la integraci\u00f3n del roble en vinos tintos.",
      "topic": "roble",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "aroma",
        "tanino",
        "aroma",
        "roble"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_806",
      "source_question_id": "806",
      "stem": "Describa dos t\u00e9cnicas de manejo del dosel (canopy management) y sus beneficios.",
      "topic": "manejo del dosel",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "component_order": [
            "feature1",
            "feature2"
          ],
          "elaboration_required": false,
          "explanation_forbidden": true
        },
        "required_signals": [],
        "forbidden_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to"
        ]
      }
    },
    {
      "item_id": "open_response_807",
      "source_question_id": "807",
      "stem": "Explique c\u00f3mo el riego y el manejo del dosel pueden reducir los efectos de la sequ\u00eda o del calor extremo sobre la maduraci\u00f3n de la uva.",
      "topic": "decisiones humanas",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "maduraci\u00f3n"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_808",
      "source_question_id": "808",
      "stem": "Explica por qu\u00e9 la densidad de plantaci\u00f3n es un factor clave en la gesti\u00f3n del vi\u00f1edo y c\u00f3mo afecta el estilo y costo del vino producido.",
      "topic": "densidad de plantaci\u00f3n",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_809",
      "source_question_id": "809",
      "stem": "Compare el uso de levaduras seleccionadas y levaduras aut\u00f3ctonas en fermentaci\u00f3n, considerando control, consistencia, complejidad potencial y riesgos.",
      "topic": "levaduras seleccionadas",
      "RA": "RA1",
      "command_verb": "compare",
      "expected_concepts": [
        "fermentaci\u00f3n"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 4,
          "component_order": [
            "dimension1",
            "dimension2",
            "dimension3",
            "synthesis"
          ],
          "elaboration_required": true,
          "both_items_required": true,
          "similarities_and_differences": true
        },
        "required_signals": [
          "whereas",
          "while",
          "both",
          "similarly",
          "in contrast",
          "however"
        ],
        "forbidden_signals": [
          "more important",
          "better"
        ]
      }
    },
    {
      "item_id": "open_response_810",
      "source_question_id": "810",
      "stem": "Analice c\u00f3mo el estr\u00e9s h\u00eddrico moderado puede reducir el rendimiento, concentrar las bayas e influir potencialmente en el coste y el precio del vino.",
      "topic": "estr\u00e9s h\u00eddrico",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_811",
      "source_question_id": "811",
      "stem": "Describe c\u00f3mo la latitud y la altitud interact\u00faan para influir en el estilo del vino en una regi\u00f3n de clima c\u00e1lido.",
      "topic": "latitud",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "clima",
        "altitud"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_812",
      "source_question_id": "812",
      "stem": "Explique c\u00f3mo un estr\u00e9s h\u00eddrico moderado, si no es excesivo, puede influir en el vigor de la vid, el tama\u00f1o de las bayas y la concentraci\u00f3n del vino.",
      "topic": "estr\u00e9s h\u00eddrico",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_813",
      "source_question_id": "813",
      "stem": "Menciona un riesgo enol\u00f3gico del uso de levaduras aut\u00f3ctonas.",
      "topic": "levaduras aut\u00f3ctonas",
      "RA": "RA1",
      "command_verb": "state",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "state",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 1,
          "elaboration_required": false,
          "brevity_required": true
        },
        "required_signals": [],
        "forbidden_signals": [
          "because",
          "therefore",
          "this explains",
          "opinion"
        ]
      }
    },
    {
      "item_id": "open_response_814",
      "source_question_id": "814",
      "stem": "Justifica por qu\u00e9 un viticultor utilizar\u00eda poda en invierno.",
      "topic": "poda de invierno",
      "RA": "RA1",
      "command_verb": "justify",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "justify",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "component_order": [
            "position_restatement",
            "reason1",
            "reason2"
          ],
          "elaboration_required": true,
          "evidence_required": true,
          "minimum_reasons": 3
        },
        "required_signals": [
          "because",
          "therefore",
          "due to",
          "since"
        ],
        "forbidden_signals": [
          "opinion",
          "I disagree"
        ]
      }
    },
    {
      "item_id": "open_response_815",
      "source_question_id": "815",
      "stem": "Describe un beneficio t\u00e9cnico de la fermentaci\u00f3n en acero inoxidable.",
      "topic": "acero inoxidable",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "fermentaci\u00f3n"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 2,
          "component_order": [
            "feature1",
            "feature2"
          ],
          "elaboration_required": false,
          "explanation_forbidden": true
        },
        "required_signals": [],
        "forbidden_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to"
        ]
      }
    },
    {
      "item_id": "open_response_816",
      "source_question_id": "816",
      "stem": "Analiza los efectos de la maceraci\u00f3n prolongada en la vinificaci\u00f3n de vinos tintos desde el punto de vista del estilo y calidad final.",
      "topic": "maceraci\u00f3n prolongada",
      "RA": "RA1",
      "command_verb": "evaluate",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "factor1",
            "factor2",
            "synthesis"
          ],
          "elaboration_required": true,
          "multiple_factors_required": true,
          "synthesis_required": true
        },
        "required_signals": [
          "because",
          "therefore",
          "significant",
          "important",
          "factor",
          "contributes"
        ],
        "forbidden_signals": [
          "opinion",
          "I think",
          "probably"
        ]
      }
    },
    {
      "item_id": "open_response_817",
      "source_question_id": "817",
      "stem": "Compare c\u00f3mo suelos arenosos y arcillosos pueden afectar la disponibilidad de agua, el vigor de la vid y el estilo del vino.",
      "topic": "suelo",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_853",
      "source_question_id": "853",
      "stem": "Explique qu\u00e9 indica la a\u00f1ada (vintage) en una etiqueta de vino y por qu\u00e9 no corresponde al a\u00f1o de embotellado.",
      "topic": "wine_law_and_labelling",
      "RA": "RA5",
      "command_verb": "why",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "why",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "component_order": [
            "cause",
            "mechanism"
          ],
          "elaboration_required": false
        },
        "required_signals": [
          "because",
          "due to",
          "since",
          "caused by",
          "because of",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "I think",
          "seems like",
          "probably"
        ]
      }
    },
    {
      "item_id": "open_response_854",
      "source_question_id": "854",
      "stem": "Explique por qu\u00e9 los vinos DOP est\u00e1n sujetos a regulaciones m\u00e1s estrictas que los vinos IGP.",
      "topic": "wine_law_and_labelling",
      "RA": "RA5",
      "command_verb": "why",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "why",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 2,
          "component_order": [
            "cause",
            "mechanism"
          ],
          "elaboration_required": false
        },
        "required_signals": [
          "because",
          "due to",
          "since",
          "caused by",
          "because of",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "I think",
          "seems like",
          "probably"
        ]
      }
    },
    {
      "item_id": "open_response_855",
      "source_question_id": "855",
      "stem": "Explique los requisitos m\u00ednimos de crianza asociados al t\u00e9rmino Reserva en un vino tinto espa\u00f1ol.",
      "topic": "wine_law_and_labelling",
      "RA": "RA5",
      "command_verb": "explain",
      "expected_concepts": [
        "crianza"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {
          "minimum_components": 3,
          "component_order": [
            "cause",
            "mechanism",
            "effect"
          ],
          "elaboration_required": true,
          "causal_chain_required": true
        },
        "required_signals": [
          "because",
          "due to",
          "therefore",
          "since",
          "causes",
          "leads to",
          "results in"
        ],
        "forbidden_signals": [
          "opinion",
          "probably",
          "I think"
        ]
      }
    },
    {
      "item_id": "open_response_856",
      "source_question_id": "856",
      "stem": "Compare Kabinett y Trockenbeerenauslese dentro del sistema Pr\u00e4dikat alem\u00e1n en t\u00e9rminos de madurez y concentraci\u00f3n.",
      "topic": "wine_law_and_labelling",
      "RA": "RA5",
      "command_verb": "compare",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 4,
          "component_order": [
            "dimension1",
            "dimension2",
            "dimension3",
            "synthesis"
          ],
          "elaboration_required": true,
          "both_items_required": true,
          "similarities_and_differences": true
        },
        "required_signals": [
          "whereas",
          "while",
          "both",
          "similarly",
          "in contrast",
          "however"
        ],
        "forbidden_signals": [
          "more important",
          "better"
        ]
      }
    },
    {
      "item_id": "open_response_857",
      "source_question_id": "857",
      "stem": "Compare los canales on-trade y off-trade e indique d\u00f3nde se consume el vino en cada caso.",
      "topic": "wine_business",
      "RA": "RA5",
      "command_verb": "compare",
      "expected_concepts": [],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": false,
        "structure_rules": {
          "minimum_components": 4,
          "component_order": [
            "dimension1",
            "dimension2",
            "dimension3",
            "synthesis"
          ],
          "elaboration_required": true,
          "both_items_required": true,
          "similarities_and_differences": true
        },
        "required_signals": [
          "whereas",
          "while",
          "both",
          "similarly",
          "in contrast",
          "however"
        ],
        "forbidden_signals": [
          "more important",
          "better"
        ]
      }
    },
    {
      "item_id": "open_response_2001",
      "source_question_id": "2001",
      "stem": "Compare the climates and resulting wine styles of Sancerre (Loire Valley) and Pouilly-Fum\u00e9.",
      "topic": "Loire white wines",
      "RA": "RA2",
      "command_verb": "compare",
      "expected_concepts": [
        "climate",
        "terroir",
        "wine style",
        "Loire Valley"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2002",
      "source_question_id": "2002",
      "stem": "Assess the quality of a wine that shows: pale gold color, lemon/green fruit on the nose, crisp acidity, medium body, and a clean, dry finish.",
      "topic": "wine assessment",
      "RA": "RA1",
      "command_verb": "assess",
      "expected_concepts": [
        "quality",
        "color",
        "aroma",
        "acidity",
        "body"
      ],
      "evaluation_config": {
        "verb_definition_key": "assess",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2003",
      "source_question_id": "2003",
      "stem": "How does the use of whole-bunch fermentation in red wine production affect the final wine's structure and flavor profile?",
      "topic": "fermentation",
      "RA": "RA2",
      "command_verb": "how",
      "expected_concepts": [
        "fermentation",
        "structure",
        "tannin",
        "flavor"
      ],
      "evaluation_config": {
        "verb_definition_key": "how",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2004",
      "source_question_id": "2004",
      "stem": "Justify why small oak barrels are preferred over large oak vats for aging premium red Burgundy.",
      "topic": "oak aging",
      "RA": "RA2",
      "command_verb": "justify",
      "expected_concepts": [
        "oak",
        "aging",
        "oak influence",
        "Burgundy"
      ],
      "evaluation_config": {
        "verb_definition_key": "justify",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2005",
      "source_question_id": "2005",
      "stem": "Evaluate the significance of vintage variation in establishing a Bordeaux wine's classification and market price.",
      "topic": "vintage",
      "RA": "RA3",
      "command_verb": "evaluate",
      "expected_concepts": [
        "vintage",
        "classification",
        "weather",
        "quality"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2006",
      "source_question_id": "2006",
      "stem": "Describe the typical sensory characteristics of a premium, dry Riesling from the Mosel region.",
      "topic": "Riesling",
      "RA": "RA1",
      "command_verb": "describe",
      "expected_concepts": [
        "Riesling",
        "Mosel",
        "color",
        "aroma",
        "acidity",
        "body"
      ],
      "evaluation_config": {
        "verb_definition_key": "describe",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2007",
      "source_question_id": "2007",
      "stem": "Why is temperature control during fermentation critical for producing white wines with preserved fruit character and lower alcohol levels?",
      "topic": "fermentation control",
      "RA": "RA2",
      "command_verb": "why",
      "expected_concepts": [
        "temperature",
        "fermentation",
        "alcohol",
        "fruit"
      ],
      "evaluation_config": {
        "verb_definition_key": "why",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2008",
      "source_question_id": "2008",
      "stem": "Discuss the contrasting approaches to oak use in red Bordeaux versus Burgundy, considering the influence of terroir on winemaking decisions.",
      "topic": "regional winemaking",
      "RA": "RA3",
      "command_verb": "discuss",
      "expected_concepts": [
        "oak",
        "Bordeaux",
        "Burgundy",
        "terroir",
        "winemaking"
      ],
      "evaluation_config": {
        "verb_definition_key": "discuss",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2009",
      "source_question_id": "2009",
      "stem": "Identify and explain the significance of malolactic fermentation in transforming the acidity and flavor profile of red wines.",
      "topic": "malolactic fermentation",
      "RA": "RA2",
      "command_verb": "identify and explain",
      "expected_concepts": [
        "malolactic",
        "acidity",
        "flavor",
        "fermentation"
      ],
      "evaluation_config": {
        "verb_definition_key": "identify and explain",
        "requires_causal_chain": true,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2010",
      "source_question_id": "2010",
      "stem": "Outline the main factors that determine the potential for aging in premium white Burgundy wines.",
      "topic": "aging potential",
      "RA": "RA2",
      "command_verb": "outline",
      "expected_concepts": [
        "aging",
        "acidity",
        "structure",
        "alcohol",
        "oak"
      ],
      "evaluation_config": {
        "verb_definition_key": "outline",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2011",
      "source_question_id": "2011",
      "stem": "State the primary purpose of acid addition during winemaking in regions where grapes do not achieve sufficient natural acidity.",
      "topic": "winemaking adjustments",
      "RA": "RA1",
      "command_verb": "state",
      "expected_concepts": [
        "acidity",
        "winemaking",
        "ripeness"
      ],
      "evaluation_config": {
        "verb_definition_key": "state",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2012",
      "source_question_id": "2012",
      "stem": "List the main grape varieties used in the production of premium Sherry, and identify which category (fino, amontillado, oloroso) they are associated with.",
      "topic": "Sherry",
      "RA": "RA1",
      "command_verb": "list",
      "expected_concepts": [
        "Sherry",
        "grape variety",
        "fermentation",
        "fortification"
      ],
      "evaluation_config": {
        "verb_definition_key": "list",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2013",
      "source_question_id": "2013",
      "stem": "Explain how the altitude of a vineyard influences grape ripening, sugar accumulation, and the final alcohol level in the wine.",
      "topic": "altitude",
      "RA": "RA1",
      "command_verb": "explain",
      "expected_concepts": [
        "altitude",
        "temperature",
        "ripening",
        "sugar",
        "alcohol"
      ],
      "evaluation_config": {
        "verb_definition_key": "explain",
        "requires_causal_chain": true,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2014",
      "source_question_id": "2014",
      "stem": "Compare the production methods and resulting characteristics of sparkling wines made using the Traditional Method versus the Charmat Method.",
      "topic": "sparkling wine",
      "RA": "RA2",
      "command_verb": "compare",
      "expected_concepts": [
        "sparkling wine",
        "fermentation",
        "method",
        "bubbles"
      ],
      "evaluation_config": {
        "verb_definition_key": "compare",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    },
    {
      "item_id": "open_response_2015",
      "source_question_id": "2015",
      "stem": "Evaluate the impact of climate change on WSET Level 3 growing regions, considering ripening patterns, acidity levels, and wine style evolution.",
      "topic": "climate change",
      "RA": "RA3",
      "command_verb": "evaluate",
      "expected_concepts": [
        "climate",
        "ripening",
        "acidity",
        "style",
        "regions"
      ],
      "evaluation_config": {
        "verb_definition_key": "evaluate",
        "requires_causal_chain": false,
        "structure_rules": {},
        "required_signals": [],
        "forbidden_signals": [],
        "source": "phase_p2_4_expansion"
      }
    }
  ],
  "evaluation_by_item_id": {
    "open_response_18": {
      "item_id": "open_response_18",
      "source_question_id": "18",
      "expected_concepts": [
        "sulfitos",
        "SO2",
        "inhibici\u00f3n de levaduras salvajes",
        "protecci\u00f3n antimicrobiana",
        "RA1",
        "winemaking",
        "sulphur_dioxide_management"
      ],
      "optional_causal_chain": "dosis de SO2 -> inhibici\u00f3n microbiana -> menor actividad de levaduras salvajes",
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
    "open_response_798": {
      "item_id": "open_response_798",
      "source_question_id": "798",
      "expected_concepts": [
        "sostenibilidad",
        "sostenible",
        "certificaci\u00f3n",
        "org\u00e1nico",
        "biodin\u00e1mico",
        "coste",
        "costo",
        "precio",
        "mano de obra",
        "rendimiento",
        "diferenciaci\u00f3n",
        "percepci\u00f3n",
        "consumidor",
        "mercado",
        "RA1",
        "coste de producci\u00f3n",
        "diferenciaci\u00f3n comercial"
      ],
      "optional_causal_chain": "sostenibilidad -> coste -> precio",
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
    "open_response_799": {
      "item_id": "open_response_799",
      "source_question_id": "799",
      "expected_concepts": [
        "fermentaci\u00f3n malol\u00e1ctica",
        "malol\u00e1ctica",
        "\u00e1cido m\u00e1lico",
        "\u00e1cido l\u00e1ctico",
        "acidez",
        "suave",
        "suaviza",
        "textura",
        "cremosa",
        "cremosidad",
        "diacetilo",
        "mantequilla",
        "l\u00e1ctico",
        "cuerpo",
        "complejidad",
        "calidad",
        "estilo",
        "RA1",
        "vino blanco"
      ],
      "optional_causal_chain": "malol\u00e1ctica -> acidez -> textura",
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
    "open_response_800": {
      "item_id": "open_response_800",
      "source_question_id": "800",
      "expected_concepts": [
        "altitud",
        "altura",
        "temperatura",
        "fr\u00edo",
        "fresco",
        "rango diurno",
        "oscilaci\u00f3n t\u00e9rmica",
        "maduraci\u00f3n",
        "madura",
        "lenta",
        "despacio",
        "acidez",
        "az\u00facar",
        "alcohol",
        "estilo",
        "frescura",
        "RA1",
        "clima",
        "estilo de vino tinto"
      ],
      "optional_causal_chain": "altitud -> temperatura -> maduraci\u00f3n",
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
    "open_response_801": {
      "item_id": "open_response_801",
      "source_question_id": "801",
      "expected_concepts": [
        "orientaci\u00f3n",
        "pendiente",
        "ladera",
        "exposici\u00f3n",
        "sol",
        "solar",
        "insolaci\u00f3n",
        "drenaje",
        "agua",
        "maduraci\u00f3n",
        "madura",
        "az\u00facar",
        "acidez",
        "sombra",
        "temperatura",
        "RA1",
        "exposici\u00f3n solar"
      ],
      "optional_causal_chain": "orientaci\u00f3n -> exposici\u00f3n -> maduraci\u00f3n",
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
    "open_response_802": {
      "item_id": "open_response_802",
      "source_question_id": "802",
      "expected_concepts": [
        "oxidaci\u00f3n",
        "ox\u00edgeno",
        "proteger",
        "protecci\u00f3n",
        "sulfuroso",
        "SO2",
        "inerte",
        "gas inerte",
        "temperatura",
        "fr\u00edo",
        "prensado",
        "dep\u00f3sito",
        "aromas",
        "fruta",
        "frescura",
        "color",
        "pardeamiento",
        "RA1",
        "vino blanco",
        "bodega",
        "manejo del ox\u00edgeno"
      ],
      "optional_causal_chain": "ox\u00edgeno -> oxidaci\u00f3n -> aromas",
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
    "open_response_803": {
      "item_id": "open_response_803",
      "source_question_id": "803",
      "expected_concepts": [
        "levadura",
        "levaduras",
        "fermentaci\u00f3n",
        "aromas",
        "\u00e9steres",
        "perfil sensorial",
        "sensorial",
        "levadura seleccionada",
        "seleccionada",
        "control",
        "predecible",
        "estilo",
        "fruta",
        "compuestos arom\u00e1ticos",
        "RA1"
      ],
      "optional_causal_chain": "levadura -> fermentaci\u00f3n -> aromas",
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
    "open_response_804": {
      "item_id": "open_response_804",
      "source_question_id": "804",
      "expected_concepts": [
        "suelo",
        "drenaje",
        "agua",
        "retenci\u00f3n",
        "vigor",
        "ra\u00edces",
        "rendimiento",
        "concentraci\u00f3n",
        "maduraci\u00f3n",
        "estilo",
        "RA1"
      ],
      "optional_causal_chain": "suelo -> drenaje -> vigor",
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
    "open_response_805": {
      "item_id": "open_response_805",
      "source_question_id": "805",
      "expected_concepts": [
        "roble",
        "americano",
        "franc\u00e9s",
        "vainilla",
        "coco",
        "dulce",
        "especias",
        "cedro",
        "tostado",
        "tanino",
        "integraci\u00f3n",
        "perfil sensorial",
        "estructura",
        "complejidad",
        "nuevo",
        "RA1",
        "roble americano",
        "roble franc\u00e9s"
      ],
      "optional_causal_chain": "roble americano -> vainilla -> perfil",
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
    "open_response_806": {
      "item_id": "open_response_806",
      "source_question_id": "806",
      "expected_concepts": [
        "manejo del dosel",
        "dosel",
        "canopy",
        "deshojado",
        "hojas",
        "posicionamiento de brotes",
        "brotes",
        "exposici\u00f3n",
        "sol",
        "maduraci\u00f3n",
        "aireaci\u00f3n",
        "circulaci\u00f3n de aire",
        "enfermedad",
        "hongos",
        "sombra",
        "racimos",
        "RA1",
        "t\u00e9cnicas de vi\u00f1edo",
        "sanidad de la uva"
      ],
      "optional_causal_chain": "deshojado -> exposici\u00f3n -> maduraci\u00f3n",
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
    "open_response_807": {
      "item_id": "open_response_807",
      "source_question_id": "807",
      "expected_concepts": [
        "decisiones humanas",
        "gesti\u00f3n",
        "vi\u00f1a",
        "vi\u00f1edo",
        "riego",
        "estr\u00e9s h\u00eddrico",
        "sequ\u00eda",
        "calor",
        "calor extremo",
        "dosel",
        "manejo del dosel",
        "exposici\u00f3n",
        "sombra",
        "maduraci\u00f3n",
        "equilibrio",
        "RA1"
      ],
      "optional_causal_chain": "riego -> estr\u00e9s h\u00eddrico -> maduraci\u00f3n",
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
    "open_response_808": {
      "item_id": "open_response_808",
      "source_question_id": "808",
      "expected_concepts": [
        "densidad de plantaci\u00f3n",
        "densidad",
        "plantaci\u00f3n",
        "competencia",
        "vigor",
        "rendimiento",
        "producci\u00f3n",
        "cosecha",
        "concentraci\u00f3n",
        "uva",
        "estilo",
        "coste",
        "costo",
        "mano de obra",
        "mecanizaci\u00f3n",
        "precio",
        "RA1"
      ],
      "optional_causal_chain": "densidad -> competencia -> vigor",
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
    "open_response_809": {
      "item_id": "open_response_809",
      "source_question_id": "809",
      "expected_concepts": [
        "levadura",
        "levaduras",
        "levaduras seleccionadas",
        "seleccionadas",
        "levaduras aut\u00f3ctonas",
        "aut\u00f3ctonas",
        "salvajes",
        "fermentaci\u00f3n",
        "control",
        "consistencia",
        "predecible",
        "variabilidad",
        "complejidad",
        "aromas",
        "riesgo",
        "parada fermentativa",
        "aromas no deseados",
        "RA1"
      ],
      "optional_causal_chain": "levaduras seleccionadas -> control -> consistencia",
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
    "open_response_810": {
      "item_id": "open_response_810",
      "source_question_id": "810",
      "expected_concepts": [
        "estr\u00e9s h\u00eddrico",
        "agua",
        "moderado",
        "baya",
        "bayas peque\u00f1as",
        "concentraci\u00f3n",
        "piel",
        "rendimiento",
        "coste",
        "costo",
        "precio",
        "maduraci\u00f3n",
        "az\u00facar",
        "RA1"
      ],
      "optional_causal_chain": "estr\u00e9s h\u00eddrico -> baya -> concentraci\u00f3n",
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
    "open_response_811": {
      "item_id": "open_response_811",
      "source_question_id": "811",
      "expected_concepts": [
        "latitud",
        "altitud",
        "altura",
        "clima c\u00e1lido",
        "temperatura",
        "calor",
        "maduraci\u00f3n",
        "r\u00e1pida",
        "acidez",
        "rango diurno",
        "oscilaci\u00f3n t\u00e9rmica",
        "frescura",
        "alcohol",
        "estilo",
        "RA1"
      ],
      "optional_causal_chain": "latitud -> temperatura -> maduraci\u00f3n",
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
    "open_response_812": {
      "item_id": "open_response_812",
      "source_question_id": "812",
      "expected_concepts": [
        "estr\u00e9s h\u00eddrico",
        "agua",
        "moderado",
        "vigor",
        "crecimiento vegetativo",
        "baya",
        "bayas peque\u00f1as",
        "concentraci\u00f3n",
        "maduraci\u00f3n",
        "rendimiento",
        "az\u00facar",
        "RA1"
      ],
      "optional_causal_chain": "estr\u00e9s h\u00eddrico -> vigor -> concentraci\u00f3n",
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
    "open_response_813": {
      "item_id": "open_response_813",
      "source_question_id": "813",
      "expected_concepts": [
        "levaduras aut\u00f3ctonas",
        "aut\u00f3ctonas",
        "salvajes",
        "fermentaci\u00f3n",
        "riesgo",
        "parada fermentativa",
        "lenta",
        "impredecible",
        "aromas no deseados",
        "defectos",
        "control",
        "calidad",
        "RA1",
        "riesgo enol\u00f3gico"
      ],
      "optional_causal_chain": "levaduras aut\u00f3ctonas -> riesgo",
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
    "open_response_814": {
      "item_id": "open_response_814",
      "source_question_id": "814",
      "expected_concepts": [
        "poda",
        "poda de invierno",
        "invierno",
        "yemas",
        "brotes",
        "rendimiento",
        "vigor",
        "equilibrio",
        "maduraci\u00f3n",
        "calidad",
        "uva",
        "vid",
        "RA1",
        "equilibrio de la vid"
      ],
      "optional_causal_chain": "poda -> yemas -> rendimiento",
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
    "open_response_815": {
      "item_id": "open_response_815",
      "source_question_id": "815",
      "expected_concepts": [
        "acero inoxidable",
        "inoxidable",
        "temperatura",
        "control de temperatura",
        "fermentaci\u00f3n",
        "inerte",
        "aromas primarios",
        "fruta",
        "frescura",
        "limpio",
        "ox\u00edgeno",
        "sabor",
        "RA1",
        "estilo fresco"
      ],
      "optional_causal_chain": "acero inoxidable -> temperatura -> aromas",
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
    "open_response_816": {
      "item_id": "open_response_816",
      "source_question_id": "816",
      "expected_concepts": [
        "maceraci\u00f3n prolongada",
        "maceraci\u00f3n",
        "extracci\u00f3n",
        "color",
        "tanino",
        "antocianos",
        "fenoles",
        "estructura",
        "cuerpo",
        "envejecimiento",
        "guarda",
        "astringencia",
        "amargor",
        "equilibrio",
        "calidad",
        "RA1",
        "vino tinto",
        "estilo"
      ],
      "optional_causal_chain": "maceraci\u00f3n -> extracci\u00f3n -> tanino",
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
    "open_response_817": {
      "item_id": "open_response_817",
      "source_question_id": "817",
      "expected_concepts": [
        "suelo",
        "arena",
        "arcilla",
        "drenaje",
        "retenci\u00f3n de agua",
        "agua",
        "vigor",
        "rendimiento",
        "concentraci\u00f3n",
        "maduraci\u00f3n",
        "estilo",
        "RA1"
      ],
      "optional_causal_chain": "arena -> drenaje -> vigor",
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
    "open_response_853": {
      "item_id": "open_response_853",
      "source_question_id": "853",
      "expected_concepts": [
        "a\u00f1ada",
        "a\u00f1o",
        "uva",
        "cosechada",
        "vinificada",
        "RA5",
        "wine_law_and_labelling",
        "vintage_labelling"
      ],
      "optional_causal_chain": "a\u00f1ada declarada -> a\u00f1o de cosecha de la uva -> no a\u00f1o de embotellado",
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
    "open_response_854": {
      "item_id": "open_response_854",
      "source_question_id": "854",
      "expected_concepts": [
        "DOP",
        "IGP",
        "origen",
        "producci\u00f3n",
        "regulaciones",
        "RA5",
        "wine_law_and_labelling",
        "dop_igp_hierarchy"
      ],
      "optional_causal_chain": "v\u00ednculo m\u00e1s estrecho con el origen -> normas de producci\u00f3n m\u00e1s restrictivas",
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
    "open_response_855": {
      "item_id": "open_response_855",
      "source_question_id": "855",
      "expected_concepts": [
        "Reserva",
        "tres a\u00f1os",
        "doce meses",
        "barrica",
        "botella",
        "RA5",
        "wine_law_and_labelling",
        "spanish_reserva_ageing"
      ],
      "optional_causal_chain": "Reserva tinto -> m\u00ednimo tres a\u00f1os totales -> al menos doce meses en barrica",
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
    "open_response_856": {
      "item_id": "open_response_856",
      "source_question_id": "856",
      "expected_concepts": [
        "Kabinett",
        "Trockenbeerenauslese",
        "ligero",
        "concentrado",
        "dulce",
        "RA5",
        "wine_law_and_labelling",
        "german_pradikat"
      ],
      "optional_causal_chain": "mayor madurez de la uva -> mayor concentraci\u00f3n -> categor\u00eda Pr\u00e4dikat superior",
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
    "open_response_857": {
      "item_id": "open_response_857",
      "source_question_id": "857",
      "expected_concepts": [
        "on-trade",
        "off-trade",
        "restaurantes",
        "bares",
        "supermercados",
        "vinotecas",
        "RA5",
        "wine_business",
        "distribution_channels"
      ],
      "optional_causal_chain": "on-trade -> consumo en el punto de venta; off-trade -> consumo posterior",
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
          "acidez vol\u00e1til alta"
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
          "car\u00e1cter varietal y regional muy definido",
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
          "Development stage correctly identified (joven/en evoluci\u00f3n/evolucionado)",
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
        "example": "Primary fruit only, short finish \u2192 'Outstanding quality'",
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
        "correction": "For simple wines: state 'simple' (1 mark) + 4\u20135 primary descriptors. Do not invent secondary or tertiary aromas."
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
        "hint": "Work through Appearance in order: clarity \u2192 intensity \u2192 colour. Each element has its own scale. Colour must match the wine type (white, ros\u00e9, red)."
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
        "hint": "For MCQ, eliminate clearly wrong options first. The correct answer will be fully accurate, not partially. WSET uses precise vocabulary \u2014 'dry' is not the same as 'off-dry'."
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
  "evaluation_metadata": {
    "schema_version": "open_response_evaluation_v1",
    "command_verbs_loaded": [
      "assess",
      "compare",
      "describe",
      "discuss",
      "evaluate",
      "explain",
      "how",
      "identify and explain",
      "justify",
      "list",
      "outline",
      "state",
      "why"
    ],
    "enrichment_timestamp": "phase_p2_3",
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
      "new_pool_size": 41,
      "timestamp": "phase_p2_4_expansion"
    }
  ]
};
