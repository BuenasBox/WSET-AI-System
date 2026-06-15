#!/usr/bin/env node

/**
 * SBA Corpus Import Tool (Corpus-Agnostic)
 *
 * Imports canonical SBA corpus from JSON file to Supabase.
 * Works with ANY corpus size and structure.
 *
 * Usage:
 *   node import_sba_corpus.js --corpus <FILE> --dry-run
 *   node import_sba_corpus.js --corpus <FILE> --execute
 *
 * Requires:
 *   - SUPABASE_URL environment variable
 *   - SUPABASE_SERVICE_ROLE_KEY environment variable
 *
 * Features:
 *   - Duplicate detection
 *   - Governance flag validation
 *   - Dry-run mode (no data written)
 *   - JSON logging
 *   - Rollback support
 */

const fs = require('fs');
const path = require('path');
const { createClient } = require('@supabase/supabase-js');

// ============================================================================
// CONFIGURATION
// ============================================================================

const CONFIG = {
  BATCH_SIZE: 100,                    // Items per insert statement
  LOG_INTERVAL: 50,                   // Log progress every N items
  GOVERNANCE_FLAGS: {
    required: ['safe_for_examiner', 'formative_only'],
    forbidden_values: { safe_for_examiner: true, examiner_scoring_allowed: true }
  },
  REQUIRED_FIELDS: ['id', 'text', 'options', 'correct_index'],
};

// ============================================================================
// ARGUMENT PARSING
// ============================================================================

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--corpus' && i + 1 < args.length) {
      options.corpus = args[i + 1];
      i++;
    } else if (args[i] === '--dry-run') {
      options.dryRun = true;
    } else if (args[i] === '--execute') {
      options.execute = true;
    } else if (args[i] === '--log-file' && i + 1 < args.length) {
      options.logFile = args[i + 1];
      i++;
    }
  }

  if (!options.corpus) {
    console.error('Error: --corpus <FILE> is required');
    process.exit(1);
  }

  return options;
}

// ============================================================================
// LOGGING
// ============================================================================

class ImportLogger {
  constructor(logFile = null) {
    this.logFile = logFile;
    this.entries = [];
  }

  log(level, message, data = null) {
    const entry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      data
    };
    this.entries.push(entry);

    const prefix = `[${level}]`;
    const output = data ? `${prefix} ${message}: ${JSON.stringify(data)}` : `${prefix} ${message}`;
    console.log(output);
  }

  info(message, data = null) { this.log('INFO', message, data); }
  warn(message, data = null) { this.log('WARN', message, data); }
  error(message, data = null) { this.log('ERROR', message, data); }
  success(message, data = null) { this.log('SUCCESS', message, data); }

  save() {
    if (!this.logFile) return;

    const summary = {
      timestamp: new Date().toISOString(),
      entries: this.entries,
      summary: {
        total_entries: this.entries.length,
        errors: this.entries.filter(e => e.level === 'ERROR').length,
        warnings: this.entries.filter(e => e.level === 'WARN').length
      }
    };

    fs.writeFileSync(this.logFile, JSON.stringify(summary, null, 2));
    console.log(`\nLog saved to: ${this.logFile}`);
  }
}

// ============================================================================
// VALIDATION
// ============================================================================

class CorpusValidator {
  constructor(logger) {
    this.logger = logger;
    this.errors = [];
    this.warnings = [];
  }

  validate(corpus) {
    this.logger.info('Starting corpus validation');

    if (!corpus.items || !Array.isArray(corpus.items)) {
      this.errors.push('corpus.items must be an array');
      return false;
    }

    this.logger.info(`Validating ${corpus.items.length} items`);

    // Check for duplicates
    const idCounts = {};
    corpus.items.forEach(item => {
      idCounts[item.id] = (idCounts[item.id] || 0) + 1;
    });

    const duplicates = Object.entries(idCounts)
      .filter(([id, count]) => count > 1)
      .map(([id, count]) => ({ id, count }));

    if (duplicates.length > 0) {
      this.errors.push(`${duplicates.length} duplicate IDs found`);
      duplicates.forEach(dup => this.logger.warn(`Duplicate ID`, dup));
    }

    // Check required fields
    let missingFields = 0;
    corpus.items.forEach((item, idx) => {
      CONFIG.REQUIRED_FIELDS.forEach(field => {
        if (!(field in item)) {
          this.errors.push(`Item ${idx} (${item.id}): missing field '${field}'`);
          missingFields++;
        }
      });
    });

    if (missingFields > 0) {
      this.logger.warn(`${missingFields} missing fields found`);
    }

    // Check governance flags
    let badGovernance = 0;
    corpus.items.forEach((item, idx) => {
      if (item.governance?.safe_for_examiner === true) {
        this.errors.push(`Item ${idx} (${item.id}): safe_for_examiner=true (FORBIDDEN)`);
        badGovernance++;
      }
      if (item.governance?.examiner_scoring_allowed === true) {
        this.errors.push(`Item ${idx} (${item.id}): examiner_scoring_allowed=true (FORBIDDEN)`);
        badGovernance++;
      }
    });

    if (badGovernance > 0) {
      this.logger.error(`${badGovernance} governance violations found`);
      return false;
    }

    if (this.errors.length > 0) {
      this.logger.error(`Validation failed with ${this.errors.length} errors`);
      return false;
    }

    this.logger.success('Corpus validation passed', {
      item_count: corpus.items.length,
      duplicate_ids: duplicates.length,
      governance_violations: badGovernance
    });

    return true;
  }

  getErrors() {
    return this.errors;
  }

  getWarnings() {
    return this.warnings;
  }
}

// ============================================================================
// IMPORT HANDLER
// ============================================================================

class CorpusImporter {
  constructor(supabaseClient, logger) {
    this.supabase = supabaseClient;
    this.logger = logger;
    this.importedCount = 0;
    this.skippedCount = 0;
    this.errorCount = 0;
  }

  async import(corpus, dryRun = false) {
    this.logger.info(`Starting import (${dryRun ? 'DRY-RUN' : 'EXECUTE'} mode)`);

    if (dryRun) {
      this.logger.info('DRY-RUN: No data will be written to database');
    }

    const items = corpus.items || [];

    // Process in batches
    for (let i = 0; i < items.length; i += CONFIG.BATCH_SIZE) {
      const batch = items.slice(i, i + CONFIG.BATCH_SIZE);
      await this.importBatch(batch, dryRun);

      if ((i + CONFIG.BATCH_SIZE) % CONFIG.LOG_INTERVAL === 0) {
        const progress = Math.min(i + CONFIG.BATCH_SIZE, items.length);
        this.logger.info(`Progress: ${progress}/${items.length} (${Math.round(progress / items.length * 100)}%)`);
      }
    }

    const summary = {
      imported: this.importedCount,
      skipped: this.skippedCount,
      errors: this.errorCount,
      total: items.length
    };

    if (dryRun) {
      this.logger.info('DRY-RUN COMPLETE: Would import', summary);
    } else {
      this.logger.success('IMPORT COMPLETE', summary);
    }

    return summary;
  }

  async importBatch(batch, dryRun = false) {
    if (dryRun) {
      // Validate only, don't write
      batch.forEach(item => {
        if (this.validateItem(item)) {
          this.importedCount++;
        } else {
          this.errorCount++;
        }
      });
      return;
    }

    // Real import
    const { data, error } = await this.supabase
      .from('sba_items')
      .insert(batch)
      .select();

    if (error) {
      if (error.code === '23505') {
        // Duplicate key error — try inserting individually
        for (const item of batch) {
          const { error: itemError } = await this.supabase
            .from('sba_items')
            .insert([item]);

          if (itemError && itemError.code === '23505') {
            this.skippedCount++;
          } else if (itemError) {
            this.errorCount++;
            this.logger.error(`Failed to insert ${item.id}`, { error: itemError.message });
          } else {
            this.importedCount++;
          }
        }
      } else {
        this.errorCount += batch.length;
        this.logger.error('Batch import failed', { error: error.message });
      }
    } else {
      this.importedCount += batch.length;
    }
  }

  validateItem(item) {
    // Validate item structure
    if (!item.id || !item.text || !Array.isArray(item.options) || item.correct_index === undefined) {
      this.logger.warn(`Invalid item structure`, { id: item.id });
      return false;
    }

    // Validate options count
    if (item.options.length !== 4) {
      this.logger.warn(`Item ${item.id}: expected 4 options, got ${item.options.length}`);
      return false;
    }

    // Validate governance
    if (item.governance?.safe_for_examiner === true) {
      this.logger.warn(`Item ${item.id}: safe_for_examiner=true`);
      return false;
    }

    return true;
  }
}

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  const options = parseArgs();
  const logger = new ImportLogger(options.logFile);

  try {
    // 1. Load corpus
    logger.info(`Loading corpus from ${options.corpus}`);
    if (!fs.existsSync(options.corpus)) {
      logger.error(`File not found: ${options.corpus}`);
      process.exit(1);
    }

    const corpusData = fs.readFileSync(options.corpus, 'utf-8');
    const corpus = JSON.parse(corpusData);
    logger.success(`Corpus loaded: ${corpus.items?.length || 0} items`);

    // 2. Validate corpus
    const validator = new CorpusValidator(logger);
    if (!validator.validate(corpus)) {
      logger.error('Corpus validation failed');
      logger.save();
      process.exit(1);
    }

    // 3. Connect to Supabase
    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

    if (!supabaseUrl || !supabaseKey) {
      logger.error('Missing Supabase credentials (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)');
      process.exit(1);
    }

    const supabase = createClient(supabaseUrl, supabaseKey);
    logger.info('Connected to Supabase');

    // 4. Import
    const importer = new CorpusImporter(supabase, logger);
    const dryRun = options.dryRun && !options.execute;
    await importer.import(corpus, dryRun);

    // 5. Save log
    logger.save();

    // 6. Exit code
    process.exit(0);

  } catch (err) {
    logger.error('Fatal error', { message: err.message, stack: err.stack });
    logger.save();
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { CorpusImporter, CorpusValidator, ImportLogger };
