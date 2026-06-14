/**
 * Phase P2.3: Learner Evaluation Tracker
 * Tracks learner performance across the 4-dimensional evaluation framework.
 * Stores patterns: verb compliance, concept coverage, causal reasoning, structure adherence.
 */

(function(window) {
  'use strict';

  const STORAGE_KEY = 'wset_or_evaluation_tracking_v1';

  /**
   * Initialize or load existing tracking data
   */
  function initializeTracker() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }

    return {
      session_id: Date.now().toString(),
      started_at: new Date().toISOString(),
      evaluations: [],
      verb_patterns: {},
      dimension_patterns: {
        content_correctness: [],
        structural_correctness: [],
        command_verb_compliance: [],
        distinction_chain_completeness: []
      },
      concept_coverage: {},
      causal_reasoning_strength: [],
      governance_flags: {
        safe_for_examiner: false,
        examiner_scoring_allowed: false,
        formative_only: true
      }
    };
  }

  /**
   * Record a 4-dimensional evaluation result
   */
  function recordEvaluation(itemId, evaluation) {
    const tracker = initializeTracker();

    const record = {
      timestamp: new Date().toISOString(),
      item_id: itemId,
      evaluation: evaluation,
      dimensions_summary: {
        content_correctness: evaluation.evaluation?.content_correctness || {},
        structural_correctness: evaluation.evaluation?.structural_correctness || {},
        command_verb_compliance: evaluation.evaluation?.command_verb_compliance || {},
        distinction_chain_completeness: evaluation.evaluation?.distinction_chain_completeness || {}
      }
    };

    tracker.evaluations.push(record);

    // Track verb compliance patterns
    const verbUsed = evaluation.evaluation?.command_verb_compliance?.verb_requested;
    if (verbUsed) {
      if (!tracker.verb_patterns[verbUsed]) {
        tracker.verb_patterns[verbUsed] = {
          attempts: 0,
          full_compliance_count: 0,
          compliance_status_distribution: {}
        };
      }
      tracker.verb_patterns[verbUsed].attempts++;

      const status = evaluation.evaluation?.command_verb_compliance?.compliance_status;
      if (status === 'full') {
        tracker.verb_patterns[verbUsed].full_compliance_count++;
      }
      tracker.verb_patterns[verbUsed].compliance_status_distribution[status] =
        (tracker.verb_patterns[verbUsed].compliance_status_distribution[status] || 0) + 1;
    }

    // Track concept coverage
    const concepts = evaluation.evaluation?.content_correctness?.concepts_detected || [];
    concepts.forEach(concept => {
      if (!tracker.concept_coverage[concept]) {
        tracker.concept_coverage[concept] = { count: 0, items: [] };
      }
      tracker.concept_coverage[concept].count++;
      tracker.concept_coverage[concept].items.push(itemId);
    });

    // Track causal reasoning patterns
    const causalChains = evaluation.evaluation?.content_correctness?.causal_chains_found || [];
    if (causalChains.length > 0) {
      const causalIntegrity = evaluation.evaluation?.content_correctness?.causal_integrity || 'unknown';
      tracker.causal_reasoning_strength.push({
        timestamp: record.timestamp,
        chain_count: causalChains.length,
        integrity: causalIntegrity,
        chains: causalChains
      });
    }

    // Track dimension patterns
    Object.keys(tracker.dimension_patterns).forEach(dimension => {
      const dimData = evaluation.evaluation?.[dimension];
      if (dimData) {
        tracker.dimension_patterns[dimension].push({
          timestamp: record.timestamp,
          item_id: itemId,
          data: dimData
        });
      }
    });

    saveTracker(tracker);
    return record;
  }

  /**
   * Save tracker to localStorage
   */
  function saveTracker(tracker) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tracker));
      return true;
    } catch (e) {
      console.warn('Could not save evaluation tracker:', e);
      return false;
    }
  }

  /**
   * Get verb mastery summary
   */
  function getVerbMasterySummary() {
    const tracker = initializeTracker();
    const summary = {};

    Object.entries(tracker.verb_patterns).forEach(([verb, stats]) => {
      const rate = stats.attempts > 0 ? stats.full_compliance_count / stats.attempts : 0;
      summary[verb] = {
        attempts: stats.attempts,
        mastery_rate: (rate * 100).toFixed(1) + '%',
        full_compliance: stats.full_compliance_count,
        distribution: stats.compliance_status_distribution
      };
    });

    return summary;
  }

  /**
   * Get concept coverage summary
   */
  function getConceptCoverageSummary() {
    const tracker = initializeTracker();
    const summary = {
      total_concepts_seen: Object.keys(tracker.concept_coverage).length,
      concepts: {}
    };

    Object.entries(tracker.concept_coverage).forEach(([concept, data]) => {
      summary.concepts[concept] = {
        frequency: data.count,
        in_items: data.items.length
      };
    });

    return summary;
  }

  /**
   * Get causal reasoning pattern
   */
  function getCausalReasoningPattern() {
    const tracker = initializeTracker();
    if (tracker.causal_reasoning_strength.length === 0) {
      return { status: 'no_data' };
    }

    const recent = tracker.causal_reasoning_strength.slice(-5);
    const avgChains = recent.reduce((sum, r) => sum + r.chain_count, 0) / recent.length;
    const integrityDistribution = {};

    tracker.causal_reasoning_strength.forEach(r => {
      integrityDistribution[r.integrity] = (integrityDistribution[r.integrity] || 0) + 1;
    });

    return {
      total_causal_responses: tracker.causal_reasoning_strength.length,
      average_chains_per_response: avgChains.toFixed(2),
      recent_integrity: integrityDistribution,
      trend: avgChains > 1.5 ? 'strengthening' : 'developing'
    };
  }

  /**
   * Get learner intelligence summary (all dimensions)
   */
  function getLearnerIntelligenceSummary() {
    const tracker = initializeTracker();

    return {
      session_id: tracker.session_id,
      total_evaluations: tracker.evaluations.length,
      verb_mastery: getVerbMasterySummary(),
      concept_coverage: getConceptCoverageSummary(),
      causal_reasoning: getCausalReasoningPattern(),
      governance: tracker.governance_flags,
      last_updated: new Date().toISOString()
    };
  }

  /**
   * Clear all tracking data
   */
  function clearTracker() {
    localStorage.removeItem(STORAGE_KEY);
  }

  // Export to window
  window.LEARNER_EVALUATION_TRACKER = {
    recordEvaluation,
    getVerbMasterySummary,
    getConceptCoverageSummary,
    getCausalReasoningPattern,
    getLearnerIntelligenceSummary,
    clearTracker,
    initializeTracker
  };

})(window);
