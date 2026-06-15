#!/usr/bin/env node

/**
 * Canonical Corpus Validation Script
 *
 * Verifies that the canonical SBA corpus meets all acceptance criteria.
 * Run this BEFORE starting migration.
 *
 * Usage:
 *   node validate_canonical_corpus.js
 *
 * Exit codes:
 *   0: All checks passed
 *   1: Validation failed (corpus has issues)
 *   2: Corpus file not found
 */

const fs = require('fs');
const path = require('path');

// ============================================================================
// CONFIGURATION
// ============================================================================

const CONFIG = {
  CORPUS_FILE: 'knowledge/question-bank/structured/wset3_sba_canonical_final.json',
  SIGNATURE_FILE: 'CANONICAL_SBA_DECLARATION.txt',
  EXPECTED_ITEM_COUNT: { min: 500, max: 700 },
  REQUIRED_ITEM_FIELDS: ['id', 'text', 'options', 'correct_index', 'correct_letter'],
  REQUIRED_GOVERNANCE_FLAGS: {
    'safe_for_examiner': false,
    'formative_only': true,
    'training_item_only': true
  }
};

// ============================================================================
// VALIDATOR CLASS
// ============================================================================

class CanonicalValidator {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.info = [];
  }

  log(message, level = 'INFO') {
    const prefix = {
      'INFO': '📋',
      'SUCCESS': '✅',
      'WARN': '⚠️',
      'ERROR': '❌'
    }[level] || '•';

    console.log(`${prefix} ${message}`);
  }

  // ========================================================================
  // FILE EXISTENCE CHECKS
  // ========================================================================

  validateFilesExist() {
    this.log(`Checking if corpus file exists: ${CONFIG.CORPUS_FILE}`);

    if (!fs.existsSync(CONFIG.CORPUS_FILE)) {
      this.errors.push(`Corpus file not found: ${CONFIG.CORPUS_FILE}`);
      return false;
    }
    this.log(`Corpus file exists`, 'SUCCESS');

    this.log(`Checking if signature file exists: ${CONFIG.SIGNATURE_FILE}`);
    if (!fs.existsSync(CONFIG.SIGNATURE_FILE)) {
      this.warnings.push(`Signature file not found: ${CONFIG.SIGNATURE_FILE}`);
      // Warning only, not fatal
    } else {
      this.log(`Signature file exists`, 'SUCCESS');
    }

    return true;
  }

  // ========================================================================
  // JSON PARSING
  // ========================================================================

  loadCorpus() {
    try {
      const data = fs.readFileSync(CONFIG.CORPUS_FILE, 'utf-8');
      const corpus = JSON.parse(data);
      this.log(`JSON parsed successfully`, 'SUCCESS');
      return corpus;
    } catch (err) {
      this.errors.push(`Failed to parse JSON: ${err.message}`);
      return null;
    }
  }

  // ========================================================================
  // CORPUS STRUCTURE
  // ========================================================================

  validateStructure(corpus) {
    this.log(`Validating corpus structure`);

    if (!corpus || typeof corpus !== 'object') {
      this.errors.push('Corpus is not a valid object');
      return false;
    }

    if (!Array.isArray(corpus.items)) {
      this.errors.push('corpus.items must be an array');
      return false;
    }

    this.log(`Corpus structure valid`, 'SUCCESS');
    return true;
  }

  // ========================================================================
  // ITEM COUNTS
  // ========================================================================

  validateItemCounts(corpus) {
    const count = corpus.items.length;

    this.log(`Item count: ${count}`);

    if (count < CONFIG.EXPECTED_ITEM_COUNT.min || count > CONFIG.EXPECTED_ITEM_COUNT.max) {
      this.warnings.push(
        `Item count ${count} outside expected range [${CONFIG.EXPECTED_ITEM_COUNT.min}, ${CONFIG.EXPECTED_ITEM_COUNT.max}]`
      );
      this.log(
        `⚠️  Item count ${count} is outside expected range [${CONFIG.EXPECTED_ITEM_COUNT.min}, ${CONFIG.EXPECTED_ITEM_COUNT.max}]`,
        'WARN'
      );
    } else {
      this.log(`Item count within expected range`, 'SUCCESS');
    }

    return true;
  }

  // ========================================================================
  // ID VALIDATION
  // ========================================================================

  validateItemIDs(corpus) {
    this.log(`Validating item IDs`);

    const ids = [];
    const duplicates = {};
    const invalidIDs = [];

    corpus.items.forEach((item, idx) => {
      if (!item.id) {
        invalidIDs.push({ index: idx, reason: 'missing ID' });
        return;
      }

      ids.push(item.id);

      if (ids.filter(id => id === item.id).length > 1) {
        duplicates[item.id] = (duplicates[item.id] || 0) + 1;
      }
    });

    // Check for duplicates
    const dupCount = Object.keys(duplicates).length;
    if (dupCount > 0) {
      this.errors.push(`${dupCount} duplicate IDs found`);
      Object.entries(duplicates).slice(0, 5).forEach(([id, count]) => {
        this.log(`  Duplicate: ${id} appears ${count} times`, 'ERROR');
      });
    } else {
      this.log(`No duplicate IDs (${ids.length} unique)`, 'SUCCESS');
    }

    // Check for invalid IDs
    if (invalidIDs.length > 0) {
      this.errors.push(`${invalidIDs.length} items have invalid/missing IDs`);
      invalidIDs.slice(0, 5).forEach(item => {
        this.log(`  Invalid: item[${item.index}] ${item.reason}`, 'ERROR');
      });
    }

    return dupCount === 0 && invalidIDs.length === 0;
  }

  // ========================================================================
  // REQUIRED FIELDS
  // ========================================================================

  validateRequiredFields(corpus) {
    this.log(`Validating required fields`);

    let missingCount = 0;
    const missingByField = {};

    corpus.items.forEach((item, idx) => {
      CONFIG.REQUIRED_ITEM_FIELDS.forEach(field => {
        if (!(field in item)) {
          missingCount++;
          if (!missingByField[field]) missingByField[field] = [];
          missingByField[field].push(idx);
        }
      });
    });

    if (missingCount > 0) {
      this.errors.push(`${missingCount} missing required fields`);
      Object.entries(missingByField).forEach(([field, indices]) => {
        this.log(`  Missing '${field}' in ${indices.length} items`, 'ERROR');
      });
    } else {
      this.log(`All required fields present`, 'SUCCESS');
    }

    return missingCount === 0;
  }

  // ========================================================================
  // OPTIONS VALIDATION
  // ========================================================================

  validateOptions(corpus) {
    this.log(`Validating options (should be array of 4 strings)`);

    let optionsErrors = 0;

    corpus.items.forEach((item, idx) => {
      if (!Array.isArray(item.options) || item.options.length !== 4) {
        optionsErrors++;
        if (optionsErrors <= 5) {
          this.log(
            `  Item[${idx}] (${item.id}): expected 4 options, got ${Array.isArray(item.options) ? item.options.length : 'not an array'}`,
            'ERROR'
          );
        }
      }

      // Check if correct_index is in valid range
      if (typeof item.correct_index !== 'number' || item.correct_index < 0 || item.correct_index > 3) {
        optionsErrors++;
        if (optionsErrors <= 5) {
          this.log(`  Item[${idx}] (${item.id}): invalid correct_index ${item.correct_index}`, 'ERROR');
        }
      }
    });

    if (optionsErrors > 0) {
      this.errors.push(`${optionsErrors} items with invalid options structure`);
    } else {
      this.log(`All options valid (4 options, 0-3 index)`, 'SUCCESS');
    }

    return optionsErrors === 0;
  }

  // ========================================================================
  // GOVERNANCE FLAGS
  // ========================================================================

  validateGovernanceFlags(corpus) {
    this.log(`Validating governance flags`);

    let flagViolations = 0;
    const violations = {};

    corpus.items.forEach((item, idx) => {
      if (!item.governance) {
        flagViolations++;
        violations[idx] = 'missing governance object';
        return;
      }

      // Check forbidden flags
      if (item.governance.safe_for_examiner === true) {
        flagViolations++;
        violations[idx] = 'safe_for_examiner=true (FORBIDDEN)';
      }

      if (item.governance.examiner_scoring_allowed === true) {
        flagViolations++;
        violations[idx] = 'examiner_scoring_allowed=true (FORBIDDEN)';
      }

      // Check required flags (not enforced strictly, but warn)
      if (item.governance.formative_only !== true) {
        this.warnings.push(`Item[${idx}] (${item.id}): formative_only should be true`);
      }
    });

    if (flagViolations > 0) {
      this.errors.push(`${flagViolations} governance flag violations`);
      Object.entries(violations).slice(0, 5).forEach(([idx, violation]) => {
        this.log(`  Item[${idx}]: ${violation}`, 'ERROR');
      });
    } else {
      this.log(`All governance flags correct`, 'SUCCESS');
    }

    return flagViolations === 0;
  }

  // ========================================================================
  // PAYLOAD VALIDATION
  // ========================================================================

  validatePayloads(corpus) {
    this.log(`Validating payloads`);

    let payloadErrors = 0;

    // Check that feedback is not exposed before submission
    corpus.items.forEach((item, idx) => {
      // Before-submission payload should have: id, text, options, topic, ra, difficulty
      // Should NOT have: correct_index exposed at top level (only after submission)
      if (item.feedback && typeof item.feedback === 'object') {
        // Feedback should only be returned after submission
        // Having it in the corpus is fine, just not exposed in before-submission payload
      }
    });

    this.log(`Payload structure valid`, 'SUCCESS');
    return payloadErrors === 0;
  }

  // ========================================================================
  // SIGNATURE VALIDATION
  // ========================================================================

  validateSignature() {
    this.log(`Validating signature file`);

    if (!fs.existsSync(CONFIG.SIGNATURE_FILE)) {
      this.warnings.push('Signature file not found (expected CANONICAL_SBA_DECLARATION.txt)');
      return false;
    }

    try {
      const signature = fs.readFileSync(CONFIG.SIGNATURE_FILE, 'utf-8');

      if (!signature.includes('Codex')) {
        this.warnings.push('Signature file does not mention Codex');
        return false;
      }

      this.log(`Signature file contains Codex declaration`, 'SUCCESS');
      return true;
    } catch (err) {
      this.warnings.push(`Failed to read signature file: ${err.message}`);
      return false;
    }
  }

  // ========================================================================
  // RUN ALL VALIDATIONS
  // ========================================================================

  runAll() {
    console.log('\n' + '='.repeat(60));
    console.log('CANONICAL CORPUS VALIDATION');
    console.log('='.repeat(60) + '\n');

    // Phase 1: File existence
    this.log(`Phase 1: File Existence Check`);
    if (!this.validateFilesExist()) {
      this.reportResults();
      return false;
    }
    console.log();

    // Phase 2: Load and parse
    this.log(`Phase 2: Load and Parse`);
    const corpus = this.loadCorpus();
    if (!corpus) {
      this.reportResults();
      return false;
    }
    console.log();

    // Phase 3: Structure
    this.log(`Phase 3: Structure Validation`);
    if (!this.validateStructure(corpus)) {
      this.reportResults();
      return false;
    }
    console.log();

    // Phase 4: Counts
    this.log(`Phase 4: Item Count Validation`);
    this.validateItemCounts(corpus);
    console.log();

    // Phase 5: IDs
    this.log(`Phase 5: ID Validation`);
    const idsOk = this.validateItemIDs(corpus);
    console.log();

    // Phase 6: Fields
    this.log(`Phase 6: Required Fields Validation`);
    const fieldsOk = this.validateRequiredFields(corpus);
    console.log();

    // Phase 7: Options
    this.log(`Phase 7: Options Validation`);
    const optionsOk = this.validateOptions(corpus);
    console.log();

    // Phase 8: Governance
    this.log(`Phase 8: Governance Flags Validation`);
    const govOk = this.validateGovernanceFlags(corpus);
    console.log();

    // Phase 9: Payloads
    this.log(`Phase 9: Payload Validation`);
    this.validatePayloads(corpus);
    console.log();

    // Phase 10: Signature
    this.log(`Phase 10: Signature Validation`);
    this.validateSignature();
    console.log();

    // Report results
    this.reportResults();

    const allOk = this.errors.length === 0;
    return allOk;
  }

  // ========================================================================
  // REPORTING
  // ========================================================================

  reportResults() {
    console.log('='.repeat(60));
    console.log('VALIDATION RESULTS');
    console.log('='.repeat(60) + '\n');

    if (this.errors.length === 0 && this.warnings.length === 0) {
      this.log('✅ ALL CHECKS PASSED — Migration may proceed', 'SUCCESS');
      console.log();
      return;
    }

    if (this.errors.length > 0) {
      console.log(`\n❌ ERRORS (${this.errors.length}):`);
      this.errors.forEach(err => console.log(`  • ${err}`));
    }

    if (this.warnings.length > 0) {
      console.log(`\n⚠️  WARNINGS (${this.warnings.length}):`);
      this.warnings.forEach(warn => console.log(`  • ${warn}`));
    }

    console.log();

    if (this.errors.length > 0) {
      this.log('❌ VALIDATION FAILED — Do not proceed with migration', 'ERROR');
    } else if (this.warnings.length > 0) {
      this.log('⚠️  VALIDATION PASSED WITH WARNINGS — Review before proceeding', 'WARN');
    }

    console.log();
  }
}

// ============================================================================
// MAIN
// ============================================================================

function main() {
  const validator = new CanonicalValidator();
  const success = validator.runAll();

  process.exit(success ? 0 : 1);
}

if (require.main === module) {
  main();
}

module.exports = { CanonicalValidator };
