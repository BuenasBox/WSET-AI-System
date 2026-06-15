/**
 * Phase P2.3: Command Verbs Loader
 * Loads command verb definitions and exposes them to the frontend.
 * Enables verb-specific coaching and evaluation guidance.
 */

(function(window) {
  'use strict';

  // Command verb definitions embedded in frontend
  const COMMAND_VERBS = {
    explain: {
      verb: "explain",
      cognitive_level: "causal reasoning",
      definition: "Give reasons for why something happens, or describe the process by which it happens",
      expected_response: {
        format: "Causal chain with 3+ components (cause → mechanism → effect)",
        do: [
          "Identify the initial factor or cause",
          "Explain the process or mechanism that connects cause to effect",
          "Name the final result or effect"
        ],
        do_not: [
          "Merely describe facts without explaining why",
          "State opinions instead of evidence-based reasons"
        ]
      },
      mentor_hint: "Start with 'Because' or 'Due to'. Walk through the steps: Factor → Mechanism → Effect.",
      compliance_checks: {
        required_signals: ["because", "due to", "therefore", "since", "causes", "leads to", "results in"],
        forbidden_signals: ["opinion", "I think"],
        structure_rules: {
          minimum_components: 3,
          causal_chain_required: true
        }
      }
    },

    describe: {
      verb: "describe",
      cognitive_level: "observation",
      definition: "Give a detailed account of the characteristics, features, or appearance of something",
      expected_response: {
        format: "Organized list of observable features, qualities, or attributes",
        do: [
          "Use precise, specific descriptors",
          "Cover multiple dimensions or aspects",
          "Use WSET vocabulary for wine characteristics"
        ],
        do_not: [
          "Explain why things are that way",
          "Interpret or judge the quality"
        ]
      },
      mentor_hint: "Paint a picture with words. What do you see, smell, taste? Use technical terms.",
      compliance_checks: {
        required_signals: [],
        forbidden_signals: ["because", "due to", "therefore", "since", "causes", "leads to"],
        structure_rules: {
          minimum_components: 2,
          explanation_forbidden: true
        }
      }
    },

    justify: {
      verb: "justify",
      cognitive_level: "reasoning + defence",
      definition: "Give reasons or evidence in support of a stated position or choice",
      expected_response: {
        format: "Evidence chain that directly supports the stated position",
        do: [
          "Select the strongest, most specific supporting evidence",
          "Link evidence directly to the position",
          "Use WSET vocabulary"
        ],
        do_not: [
          "Argue against the position",
          "Give generic descriptions unrelated to the claim"
        ]
      },
      mentor_hint: "Restate the position, then give 3+ specific reasons. Link each directly to the claim.",
      compliance_checks: {
        required_signals: ["because", "therefore", "due to", "since"],
        forbidden_signals: ["opinion", "I disagree"],
        structure_rules: {
          minimum_components: 2,
          evidence_required: true,
          minimum_reasons: 3
        }
      }
    },

    assess: {
      verb: "assess",
      cognitive_level: "judgement + justification",
      definition: "Make a judgement about the quality, merit, or worth of something, with supporting reasons",
      expected_response: {
        format: "Quality assessment with evidence, using WSET quality descriptors",
        do: [
          "State the quality level (excellent, very good, good, acceptable, poor)",
          "Give specific evidence that supports your assessment",
          "Use WSET quality vocabulary"
        ],
        do_not: [
          "Give a mark or score",
          "Judge without evidence"
        ]
      },
      mentor_hint: "Start with your quality judgement, then explain what in the wine supports that view.",
      compliance_checks: {
        required_signals: ["quality", "outstanding", "excellent", "very good", "good", "acceptable"],
        forbidden_signals: [],
        structure_rules: {
          minimum_components: 2,
          evidence_required: true,
          judgement_first: true
        }
      }
    },

    evaluate: {
      verb: "evaluate",
      cognitive_level: "synthesis + reasoning",
      definition: "Assess the significance, importance, or impact of something, considering multiple factors",
      expected_response: {
        format: "Multi-factor analysis with synthesis of key factors",
        do: [
          "Identify multiple relevant factors",
          "Assess the impact or significance of each",
          "Synthesize into an overall conclusion"
        ],
        do_not: [
          "List factors without analysis",
          "Focus on only one factor"
        ]
      },
      mentor_hint: "Consider 3+ factors, explain why each matters, then draw a conclusion.",
      compliance_checks: {
        required_signals: ["because", "therefore", "significant", "important", "factor", "contributes"],
        forbidden_signals: [],
        structure_rules: {
          minimum_components: 3,
          synthesis_required: true,
          multiple_factors_required: true
        }
      }
    },

    compare: {
      verb: "compare",
      cognitive_level: "analysis + synthesis",
      definition: "Identify similarities and differences between two or more items across shared dimensions",
      expected_response: {
        format: "Point-by-point comparison across shared dimensions",
        do: [
          "Address both similarities and differences",
          "Use parallel structure for clarity",
          "Cover multiple dimensions"
        ],
        do_not: [
          "Describe each item separately",
          "Cover only one item in detail"
        ]
      },
      mentor_hint: "Organize by dimension: 'In terms of X, Item A is [Y] whereas Item B is [Z]...'",
      compliance_checks: {
        required_signals: ["whereas", "while", "both", "similarly", "in contrast", "however"],
        forbidden_signals: ["more important", "better"],
        structure_rules: {
          minimum_components: 4,
          both_items_required: true,
          similarities_and_differences: true
        }
      }
    },

    why: {
      verb: "why",
      cognitive_level: "causal reasoning (compressed)",
      definition: "Explain the reason or cause for something happening",
      expected_response: {
        format: "Concise causal explanation (cause → effect)",
        do: [
          "Identify the cause",
          "Connect directly to the effect",
          "Keep concise but complete"
        ],
        do_not: [
          "Give opinion instead of reason",
          "State the effect without explaining the cause"
        ]
      },
      mentor_hint: "Answer: 'Because [reason]'. Use causal connectors.",
      compliance_checks: {
        required_signals: ["because", "due to", "since", "caused by"],
        forbidden_signals: ["opinion", "I think"],
        structure_rules: {
          minimum_components: 2,
          component_order: ["cause", "mechanism"]
        }
      }
    },

    how: {
      verb: "how",
      cognitive_level: "procedural reasoning + mechanism",
      definition: "Describe the process or method by which something happens or is done",
      expected_response: {
        format: "Sequence of steps or stages in a process",
        do: [
          "Identify the starting point",
          "List steps in sequence (first, then, next, after)",
          "Name the final result"
        ],
        do_not: [
          "Give reasons (that's 'why')",
          "Skip steps in the sequence"
        ]
      },
      mentor_hint: "Use: 'First... Then... After that... Finally...'",
      compliance_checks: {
        required_signals: ["first", "then", "next", "after", "during"],
        forbidden_signals: [],
        structure_rules: {
          minimum_components: 3,
          sequence_required: true
        }
      }
    },

    discuss: {
      verb: "discuss",
      cognitive_level: "balanced analysis + synthesis",
      definition: "Examine a topic from multiple perspectives, presenting different viewpoints and drawing conclusions",
      expected_response: {
        format: "Multi-perspective analysis with synthesis",
        do: [
          "Present multiple viewpoints or perspectives",
          "Explain the reasoning for each perspective",
          "Draw an informed conclusion"
        ],
        do_not: [
          "Present only one viewpoint",
          "State opinions without reasoning"
        ]
      },
      mentor_hint: "Show both sides: 'On one hand... On the other hand... However, ...'",
      compliance_checks: {
        required_signals: ["on one hand", "on the other hand", "however", "alternatively"],
        forbidden_signals: [],
        structure_rules: {
          minimum_components: 2,
          perspectives_required: 2
        }
      }
    },

    recommend: {
      verb: "recommend",
      cognitive_level: "application + justified choice",
      definition: "Select an appropriate option for the stated context and support it with evidence",
      expected_response: {
        format: "Clear recommendation followed by evidence and practical consequences",
        do: [
          "State the recommendation explicitly",
          "Use evidence from the scenario",
          "Explain why it suits the intended style or customer"
        ],
        do_not: [
          "List options without choosing",
          "Recommend without evidence"
        ]
      },
      mentor_hint: "State the choice first, then link each reason to the scenario: 'I recommend X because...'.",
      compliance_checks: {
        required_signals: ["recommend", "because", "suitable", "therefore"],
        forbidden_signals: ["always", "guaranteed"],
        structure_rules: {
          minimum_components: 3,
          evidence_required: true
        }
      }
    },

    // Compatibility alias used by bank schemas: identify_and_explain
    "identify and explain": {
      verb: "identify and explain",
      cognitive_level: "recall + comprehension",
      definition: "Name or identify something AND explain what it is or why it is significant",
      expected_response: {
        format: "Two-part response: [Part 1: Identification] [Part 2: Explanation]",
        do: [
          "Clearly identify the item in Part 1",
          "Use 'is called', 'is known as', or similar",
          "In Part 2, explain why or what it means"
        ],
        do_not: [
          "Identify without explaining",
          "Explain without clearly identifying"
        ]
      },
      mentor_hint: "Part 1: 'X is called Y because...' Part 2: 'This is significant because...'",
      compliance_checks: {
        required_signals: ["is", "called", "known as"],
        required_in_part2: ["because", "therefore"],
        forbidden_signals: [],
        structure_rules: {
          minimum_components: 2,
          two_part_structure: true
        }
      }
    },

    outline: {
      verb: "outline",
      cognitive_level: "synthesis + organization",
      definition: "Give a concise summary of the main points or structure of something",
      expected_response: {
        format: "Brief, organized list of key points, stages, or factors",
        do: [
          "Identify main/key points only",
          "Use clear structure (numbering or hierarchy)",
          "Keep each point brief and focused"
        ],
        do_not: [
          "Provide elaborate explanations",
          "Include minor details"
        ]
      },
      mentor_hint: "Use: '1. [Key point] 2. [Key point] ...' Keep it brief.",
      compliance_checks: {
        required_signals: ["main", "key", "primary", "stage", "step", "factor"],
        forbidden_signals: [],
        structure_rules: {
          minimum_components: 3,
          brief_format_required: true
        }
      }
    },

    state: {
      verb: "state",
      cognitive_level: "recall",
      definition: "Give a clear, direct statement of fact or information",
      expected_response: {
        format: "Concise, direct statement(s) of fact",
        do: [
          "Be direct and clear",
          "Use precise, technical language",
          "Answer only what is asked"
        ],
        do_not: [
          "Add explanations or reasons",
          "Give lengthy elaborations"
        ]
      },
      mentor_hint: "Answer directly without explanation. One or two sentences.",
      compliance_checks: {
        required_signals: [],
        forbidden_signals: ["because", "therefore", "due to", "since"],
        structure_rules: {
          minimum_components: 1,
          elaboration_required: false,
          brevity_required: true
        }
      }
    },

    list: {
      verb: "list",
      cognitive_level: "recall",
      definition: "Provide a series of items or points, usually in a simple enumeration",
      expected_response: {
        format: "Enumerated series of items",
        do: [
          "Use clear enumeration (1., 2., 3. or •, •, •)",
          "List only the items requested",
          "Use consistent formatting"
        ],
        do_not: [
          "Add explanations to each item",
          "Organize hierarchically unless asked"
        ]
      },
      mentor_hint: "Use: '1. [Item] 2. [Item] 3. [Item]...'",
      compliance_checks: {
        required_signals: [],
        forbidden_signals: [],
        structure_rules: {
          minimum_components: 1,
          elaboration_required: false,
          enumeration_format: true
        }
      }
    }
  };

  /**
   * Get a command verb definition by name
   */
  function getVerbDefinition(verbName) {
    return COMMAND_VERBS[verbName] || null;
  }

  /**
   * Get all available command verbs
   */
  function getAllVerbs() {
    return Object.keys(COMMAND_VERBS);
  }

  /**
   * Get mentor hint for a verb
   */
  function getMentorHint(verbName) {
    const verb = COMMAND_VERBS[verbName];
    return verb ? verb.mentor_hint : null;
  }

  /**
   * Get compliance checks for a verb
   */
  function getComplianceChecks(verbName) {
    const verb = COMMAND_VERBS[verbName];
    return verb ? verb.compliance_checks : null;
  }

  // Export to window
  window.COMMAND_VERBS_LOADER = {
    getVerbDefinition,
    getAllVerbs,
    getMentorHint,
    getComplianceChecks,
    COMMAND_VERBS
  };

})(window);
