#!/usr/bin/env node

/**
 * Evidence Citation Validator
 * Validates that responses include proper citations for factual claims.
 * Supports repository facts, web facts, and configuration citations.
 *
 * Usage:
 *   node validate-evidence.js              # Validate stdin
 *   node validate-evidence.js file.md      # Validate file
 *   node validate-evidence.js --check      # Exit with error on issues
 */

const fs = require('fs');
const path = require('path');

// Citation patterns
const CITATION_PATTERNS = {
  // Repository: [filename.ext](relative/path#Lstart-Lend)
  repository: /\[([^\]]+\.(md|tsx?|jsx?|json|ya?ml|sql|graphql))\]\(([^)]+)#L\d+-?\d*\)/g,

  // Web: [Title](URL) - Accessed: YYYY-MM-DD
  web: /\[([^\]]+)\]\((https?:\/\/[^)]+)\)\s*(-\s*(?:Accessed|Retrieved):\s*\d{4}-\d{2}-\d{2})?/gi,

  // Config: [config.ext](path#Lline)
  config: /\[([^\]]+\.(json|ya?ml|toml|ini|env))\]\(([^)]+)#[L]\d+\)/g,

  // Database: [table_name] or schema.table references
  database: /\b([a-z_]+\.?[a-z_]+)\s*(?:table|view|column)\b/gi,
};

// Factual claim patterns that require citations
const FACTUAL_CLAIM_PATTERNS = [
  /The project uses|The app uses|This uses|uses\s+\w+/gi,
  /According to|Based on|Research shows|Documentation says/gi,
  /Configuration is|Setting is|Value is|configured to/gi,
  /Architecture includes|System has|Features include|includes\s+\w+/gi,
  /defined in|located in|found in|specified in/gi,
  /as described in|as shown in|see|refer to/gi,
];

function validateCitations(text, options = {}) {
  const issues = [];
  const suggestions = [];

  // Detect factual claims
  let hasFactualClaims = false;
  for (const pattern of FACTUAL_CLAIM_PATTERNS) {
    const matches = text.match(pattern);
    if (matches && matches.length > 0) {
      hasFactualClaims = true;
      if (options.verbose) {
        suggestions.push(`Found factual claim pattern: "${matches[0]}"`);
      }
    }
  }

  // Count citations by type
  const repoCitations = (text.match(CITATION_PATTERNS.repository) || []).length;
  const webCitations = (text.match(CITATION_PATTERNS.web) || []).length;
  const configCitations = (text.match(CITATION_PATTERNS.config) || []).length;
  const totalCitations = repoCitations + webCitations + configCitations;

  // Validate web citations have access dates
  const webLinks = text.match(/https?:\/\/[^\s\)]+/g) || [];
  const properWebCitations = text.match(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)\s*(-\s*(?:Accessed|Retrieved):\s*\d{4}-\d{2}-\d{2})/gi) || [];

  // Check for issues
  if (hasFactualClaims && totalCitations === 0) {
    issues.push('Factual claims detected but no citations found');
    suggestions.push('Add citations using: [file.ext](path#Lstart-Lend) or [Title](url) - Accessed: YYYY-MM-DD');
  }

  if (webLinks.length > properWebCitations.length) {
    const missingDates = webLinks.length - properWebCitations.length;
    issues.push(`${missingDates} web link(s) missing access dates`);
    suggestions.push('Web citations should include access date: [Title](url) - Accessed: YYYY-MM-DD');
  }

  // Check for specific patterns without citations
  if (/\b(according to|as described in|see|refer to)\b/i.test(text) && totalCitations === 0) {
    issues.push('Reference phrases found but no citations included');
    suggestions.push('When using "according to", "see", or "refer to", include a citation');
  }

  // Check for bare URLs (not in markdown link format)
  const bareUrls = text.match(/(?<!\]\()[\s(]https?:\/\/[^\s\)]+/g) || [];
  if (bareUrls.length > 0) {
    issues.push(`${bareUrls.length} bare URL(s) found`);
    suggestions.push('Format URLs as markdown links: [Title](url)');
  }

  return {
    hasIssues: issues.length > 0,
    issues,
    suggestions,
    stats: {
      totalCitations,
      repoCitations,
      webCitations,
      configCitations,
      bareUrls: bareUrls.length,
      hasFactualClaims,
    },
  };
}

function formatReport(validation, options = {}) {
  const lines = [];

  if (options.json) {
    return JSON.stringify(validation, null, 2);
  }

  lines.push('=== Evidence Citation Validation ===\n');

  // Stats
  lines.push('Statistics:');
  lines.push(`  Total citations: ${validation.stats.totalCitations}`);
  lines.push(`  Repository citations: ${validation.stats.repoCitations}`);
  lines.push(`  Web citations: ${validation.stats.webCitations}`);
  lines.push(`  Config citations: ${validation.stats.configCitations}`);
  lines.push(`  Bare URLs: ${validation.stats.bareUrls}`);
  lines.push(`  Factual claims: ${validation.stats.hasFactualClaims ? 'Yes' : 'No'}`);
  lines.push('');

  // Issues
  if (validation.hasIssues) {
    lines.push('Issues:');
    validation.issues.forEach(issue => {
      lines.push(`  ❌ ${issue}`);
    });
    lines.push('');

    if (validation.suggestions.length > 0) {
      lines.push('Suggestions:');
      validation.suggestions.forEach(suggestion => {
        lines.push(`  💡 ${suggestion}`);
      });
      lines.push('');
    }
  } else {
    lines.push('✅ No evidence citation issues found\n');
  }

  return lines.join('\n');
}

function main() {
  const args = process.argv.slice(2);
  const options = {
    check: args.includes('--check'),
    verbose: args.includes('--verbose') || args.includes('-v'),
    json: args.includes('--json'),
  };

  // Get input text
  let input;
  const fileArg = args.find(arg => !arg.startsWith('--'));

  if (fileArg && !fileArg.startsWith('-')) {
    // Read from file
    try {
      input = fs.readFileSync(fileArg, 'utf8');
    } catch (err) {
      console.error(`Error reading file: ${err.message}`);
      process.exit(2);
    }
  } else if (!process.stdin.isTTY) {
    // Read from stdin
    input = fs.readFileSync(0, 'utf8');
  } else {
    console.error('Usage: validate-evidence.js [file.md] [--check] [--verbose] [--json]');
    console.error('  pipe input via stdin or provide file path');
    process.exit(1);
  }

  // Validate
  const validation = validateCitations(input, options);

  // Output report
  if (!options.json || options.check) {
    console.log(formatReport(validation, options));
  }

  if (options.json) {
    console.log(JSON.stringify(validation, null, 2));
  }

  // Exit code
  if (options.check && validation.hasIssues) {
    process.exit(1);
  }

  process.exit(0);
}

if (require.main === module) {
  main();
}

module.exports = { validateCitations, CITATION_PATTERNS };
