# CLAUDE.md Setup Workflow

Analyzes the project and generates or updates `CLAUDE.md` with relevant marketplace skills, workflows, critical rules, version-specific context, and project guidance. This workflow dynamically discovers all available plugins and extracts skill-specific content for comprehensive project documentation.

## When to Use This Workflow

- Invoked by `/project:setup` command
- When starting a new project
- After adding new technologies to the project
- When onboarding to an existing project

## The Workflow

### Step 1: Scan Marketplace Plugins

Discover all available plugins by reading the marketplace configuration:

```bash
# Find marketplace plugins directory (locations to check):
# 1. ~/.claude/plugins/cache/ - User-level installed marketplace plugins (PRIMARY)
# 2. ~/claude-code-plugins-ip-labs/plugins/ - Development/local plugins (if present)
# 3. .claude/plugins/ - Project-local plugins

# User-level cache structure:
# ~/.claude/plugins/cache/
#   └── <marketplace-name>/  # e.g., ip-labs-marketplace
#       ├── astro/1.0.0/.claude-plugin/plugin.json
#       ├── nextjs/1.0.0/.claude-plugin/plugin.json
#       ├── react/1.0.0/.claude-plugin/plugin.json
#       ├── playwright/1.0.0/.claude-plugin/plugin.json
#       └── dev/1.1.0/.claude-plugin/plugin.json

# For each marketplace in ~/.claude/plugins/cache/:
for marketplace in ~/.claude/plugins/cache/*/; do
  for plugin_dir in "$marketplace"*/; do
    plugin_json="$plugin_dir/.claude-plugin/plugin.json"
    skills_dir="$plugin_dir/skills/"

    # Read plugin metadata from plugin.json
    cat "$plugin_json"

    # Find all skills in this plugin
    find "$skills_dir" -name "SKILL.md" -path "*/skills/*/SKILL.md"
  done
done
```

For each plugin, extract:
- **Plugin name** - From `name` field
- **Description** - What the plugin provides
- **Keywords** - Searchable tags for matching
- **Skills** - Array of skill paths (scan `skills/` directory if not specified)
- **Commands** - Array of command paths (if applicable)
- **Workflows** - Scan `workflows/` directory

**Plugin Registry Structure:**

```yaml
# Build a registry like this:
plugins:
  - name: [plugin-name]  # e.g., "nextjs", "playwright", "react"
    description: [what it provides]
    keywords: [tag1, tag2, ...]
    skills:
      - name: [skill-name-from-directory]  # e.g., "latest-nextjs"
        path: [full-path-to-skill]  # ~/.claude/plugins/cache/marketplace/plugin/version/skills/skill-name/
        description: [from SKILL.md frontmatter]
        updated: [from SKILL.md frontmatter]
        claude_sections: [extracted CLAUDE-specific sections]
        critical_rules: [extracted critical rules]
        version_context: [extracted version-specific notes]
    commands: [command-path-1, ...]
    workflows: [workflow-path-1, ...]

# Example: ~/.claude/plugins/cache/<marketplace>/nextjs/1.0.0/skills/latest-nextjs/SKILL.md
# Frontmatter extracted:
#   name: latest-nextjs
#   description: Latest Next.js 16 features, App Router, Server Components
#   updated: 2026-01-11
```

### Step 2: Extract Skill Metadata (CRITICAL)

For EACH skill discovered, read its `SKILL.md` file and extract:

**Frontmatter Fields:**
```yaml
# Extract these fields from SKILL.md frontmatter (between --- markers):
name: skill-name
description: One-line description of what the skill provides
updated: ISO date or version reference
```

**CLAUDE-Specific Sections:**

Look for these special sections in SKILL.md that should be included in CLAUDE.md:

| Section Pattern | Purpose |
|----------------|---------|
| `## CLAUDE\.md Requirements` | Explicit instructions for CLAUDE.md |
| `## For CLAUDE\.md` | Content meant for CLAUDE.md |
| `## CLAUDE Context` | Context specifically for Claude |
| `## Critical Rules` | Important rules that must be documented |
| `## Gotchas` | Common pitfalls to avoid |
| `## Breaking Changes` | Version-specific breaking changes |
| `## Version Notes` | Version-specific context |
| `## Project Setup` | Setup instructions for this technology |

**Critical Rules Extraction:**

Extract content from sections containing:
- "CRITICAL", "IMPORTANT", "MUST", "NEVER", "ALWAYS"
- Code examples with "DON'T" or "WRONG" vs "DO" or "CORRECT"
- Configuration warnings
- Environment-specific notes

**Version-Aware Context:**

Extract version-specific information:
- Major version requirements
- Breaking changes between versions
- New features in recent versions
- Migration guides

### Step 3: Analyze the Workspace

Gather comprehensive project information:

```bash
# Check for package.json (if exists)
cat package.json

# Look for framework configs
ls -la | grep -E "\.config\."

# Check for backend directories
ls -la | grep -E "(api|server|backend|functions)"

# Check for testing setup
ls -la tests/ 2>/dev/null || ls -la __tests__/ 2>/dev/null || echo "No tests directory"

# Check for existing CLAUDE.md
cat CLAUDE.md 2>/dev/null || echo "No existing CLAUDE.md"

# Check for lockfiles to detect package manager
ls -la | grep -E "(pnpm-lock|yarn.lock|package-lock|bun.lockb)"
```

**Extract Technologies:**

- From `package.json`: All dependencies and devDependencies with versions
- From config files: Framework names (parse filename patterns like `*.config.{js,ts,mjs}`)
- From directories: Backend frameworks, testing frameworks
- From existing `CLAUDE.md`: Custom user content to preserve

**Version Detection (Skill-Linked):**

Only extract versions for technologies that have **matched skills**. This creates a strong linkage between detected tech and relevant skills.

```javascript
// AFTER matching plugins (Step 4), build tech-skill linkage:
function extractVersionedTech(detectedTech, matchedPlugins) {
  const versioned = [];

  for (const tech of detectedTech) {
    // Find if there's a matched skill for this technology
    const matchedSkill = findSkillForTech(tech, matchedPlugins);

    if (matchedSkill) {
      const version = parseVersion(tech.version);
      versioned.push({
        name: tech.name,
        displayName: tech.displayName,  // e.g., "Next.js", "React"
        major: version.major,           // e.g., 16
        minor: version.minor,           // e.g., 1
        displayVersion: `${version.major}.${version.minor}`,  // "16.1" - NO patch
        skill: matchedSkill.name,       // e.g., "latest-nextjs"
        skillPlugin: matchedSkill.plugin // e.g., "nextjs"
      });
    }
  }

  return versioned;
}

function parseVersion(versionString) {
  // Parse semver, return major.minor (skip patch)
  const clean = versionString.replace(/^[\^~]/, '');  // Remove ^ or ~
  const parts = clean.split('.');
  return {
    major: parts[0] || '0',
    minor: parts[1] || '0',
    patch: parts[2] || '0'  // Captured but NOT used in display
  };
}

// Example output:
// [
//   { name: "next", displayName: "Next.js", major: "16", minor: "1",
//     displayVersion: "16.1", skill: "latest-nextjs", skillPlugin: "nextjs" },
//   { name: "react", displayName: "React", major: "19", minor: "1",
//     displayVersion: "19.1", skill: "latest-react", skillPlugin: "react" }
// ]
```

**Key Principles:**

1. **No skill = no version listed** - If there's no matched skill, the technology is not versioned in CLAUDE.md
2. **Major.minor only** - Never include patch numbers (e.g., `16.1.1` → `16.1`)
3. **Skill linkage** - Each versioned tech explicitly links to its relevant skill
4. **Project relevance** - Only skills matched to the project create version entries

**Detect Package Manager:**

Check lockfiles in priority order:
1. `bun.lockb` → bun
2. `pnpm-lock.yaml` → pnpm
3. `yarn.lock` → yarn
4. `package-lock.json` → npm (default fallback)

**Detect Quality Gates:**

Scan the `scripts` section in `package.json` for quality gate commands:

| Gate Type | Script Name Patterns (priority order) |
|-----------|---------------------------------------|
| Type Checks | `typecheck`, `check:types`, `check`, `validate` |
| Linting | `lint`, `lint:fix`, `lint:check` |
| Formatting | `format`, `format:check`, `prettier` |
| Build | `build`, `compile`, `bundle` |
| Unit Tests | `test`, `test:unit`, `vitest`, `jest` |
| E2E Tests | `test:e2e`, `playwright`, `cy:run` |
| Codegen | `codegen`, `generate`, `graphql-codegen` |

### Step 4: Match Technologies to Plugins

Compare detected technologies against plugin keywords and descriptions:

**Matching Algorithm:**

```javascript
function matchPlugins(plugins, detectedTech) {
  return plugins.filter(plugin => {
    // Check keywords for direct matches
    const keywordMatch = plugin.keywords.some(kw =>
      detectedTech.some(tech =>
        tech.toLowerCase().includes(kw.toLowerCase()) ||
        kw.toLowerCase().includes(tech.toLowerCase())
      )
    );

    // Check descriptions for mentions
    const descMatch = detectedTech.some(tech =>
      plugin.description.toLowerCase().includes(tech.toLowerCase())
    );

    return keywordMatch || descMatch;
  });
}
```

**Always Include These Plugins:**

- **`dev`** - Core workflows, agents, todos (always relevant)
- **`coder`** - If running in a Coder workspace (check for `/coder` indicator)

### Step 4.5: Resolve Skill Template Variables (CRITICAL)

Skills contain **template variables** (placeholders) that need to be resolved against the actual project configuration. These variables appear in skill documentation as `[variable-name]` and must be replaced with project-specific values.

**Why This Matters:**

When a skill says:
- "Use `[package-manager] run test`" - the actual value (pnpm/npm/yarn) must be documented
- "Check `[dev-port]` is available" - the actual port (3000/5173/etc) must be known
- "Run `[test-script]`" - the actual script name must be resolved

**Variable Detection:**

Scan all matched skills' `SKILL.md` files for template variable patterns:

```javascript
function extractTemplateVariables(skillContent) {
  // Find all [variable-name] patterns
  const variablePattern = /\[([a-z_-]+)\]/gi;
  const matches = skillContent.match(variablePattern) || [];

  // Extract unique variable names
  const uniqueVars = [...new Set(matches)];
  return uniqueVars; // e.g., ['[package-manager]', '[test-script]', '[dev-port]']
}
```

**Common Template Variables:**

| Variable | Description | How to Resolve |
|----------|-------------|----------------|
| `[package-manager]` | Package manager to use | Detect from lockfiles (pnpm/yarn/npm/bun) |
| `[package_manager]` | Same as above (underscore variant) | Same as above |
| `[test-script]` | Test command name | Find in package.json scripts |
| `[test:e2e-script]` | E2E test command | Find `test:e2e`, `playwright` in scripts |
| `[dev-script]` | Dev server command | Find `dev`, `start` in scripts |
| `[build-script]` | Build command | Find `build` in scripts |
| `[lint-script]` | Lint command | Find `lint` in scripts |
| `[dev-port]` | Dev server port | Check config files or defaults |
| `[prod-port]` | Production port | Check config files or defaults |
| `[workspace-name]` | Coder workspace name | Check environment or prompt user |
| `[base-url]` | Base URL for tests | Check environment/config |
| `[app-directory]` | App source directory | Find `src/`, `app/`, etc. |
| `[config-file]` | Config file location | Find relevant config files |

**Variable Resolution Strategy:**

```javascript
function resolveVariables(variables, project) {
  const resolved = {};

  for (const variable of variables) {
    const key = variable.replace(/[\[\]]/g, '').toLowerCase(); // [package-manager] -> package-manager

    resolved[key] = resolveVariable(key, project);
  }

  return resolved;
}

function resolveVariable(variableName, project) {
  const resolvers = {
    'package-manager': () => detectPackageManager(),
    'package_manager': () => detectPackageManager(),
    'test-script': () => findScript('test', project.packageJson),
    'test:e2e-script': () => findScript('test:e2e', project.packageJson),
    'dev-script': () => findScript('dev', project.packageJson),
    'build-script': () => findScript('build', project.packageJson),
    'lint-script': () => findScript('lint', project.packageJson),
    'dev-port': () => detectPort('dev', project.configs),
    'prod-port': () => detectPort('prod', project.configs),
    'base-url': () => detectBaseURL(project.configs, project.env),
    'app-directory': () => findAppDirectory(project.directories),
    'config-file': () => findConfigFile(project.files),
  };

  const resolver = resolvers[variableName];
  return resolver ? resolver() : `[${variableName}]`;
}

function findScript(type, packageJson) {
  const scripts = packageJson.scripts || {};

  // Priority patterns for each type
  const patterns = {
    'test': ['test', 'test:unit', 'vitest', 'jest'],
    'test:e2e': ['test:e2e', 'playwright', 'e2e', 'cy:run'],
    'dev': ['dev', 'start', 'serve'],
    'build': ['build', 'compile', 'bundle'],
    'lint': ['lint', 'eslint', 'check']
  };

  const typePatterns = patterns[type] || [type];
  for (const pattern of typePatterns) {
    if (scripts[pattern]) {
      return pattern; // Return the script name, not the full command
    }
  }

  return null;
}

function detectPort(type, configs) {
  // Check common config locations
  const configChecks = [
    () => configs.nextConfig?.port, // next.config.js
    () => configs.viteConfig?.server?.port, // vite.config.js
    () => configs.env?.[`${type.toUpperCase()}_PORT`], // .env files
  ];

  for (const check of configChecks) {
    const port = check();
    if (port) return port;
  }

  // Default ports by type
  const defaults = { dev: 3000, prod: 8080 };
  return defaults[type] || 3000;
}

function detectBaseURL(configs, env) {
  // Check in order: env var, config file, default
  return env.BASE_URL ||
         env.PLAYWRIGHT_BASE_URL ||
         env.APP_SERVER_URL ||
         configs.playwrightConfig?.use?.baseURL ||
         'http://localhost:3000';
}
```

**Document Resolved Variables in CLAUDE.md:**

Add a new section `## Resolved Variables` to CLAUDE.md:

```markdown
## Resolved Variables

Skills reference template variables that are resolved for this project:

| Variable | Resolved Value | Source |
|----------|----------------|--------|
| `package-manager` | `pnpm` | Detected from pnpm-lock.yaml |
| `test-script` | `test` | Found in package.json scripts |
| `test:e2e-script` | `test:e2e` | Found in package.json scripts |
| `dev-script` | `dev` | Found in package.json scripts |
| `dev-port` | `3000` | Detected from next.config.js |
| `base-url` | `http://localhost:3000` | From .env.local |

**For skill authors:** Use `[package-manager]` in skill documentation and it will be resolved to the actual package manager for each project.
```

**Example Resolution:**

Input from `playwright-test/SKILL.md`:
```markdown
## Running Tests

```bash
# Run all tests
[package-manager] run [test-script]

# Run E2E tests
[package-manager] run [test:e2e-script]
```
```

Resolution for MyCritters project:
- `[package-manager]` → `pnpm` (from pnpm-lock.yaml)
- `[test-script]` → `test` (found in package.json)
- `[test:e2e-script]` → `test:e2e` (found in package.json)

Output in CLAUDE.md:
```markdown
## Resolved Variables

| Variable | Value | Source |
|----------|-------|--------|
| package-manager | pnpm | pnpm-lock.yaml |
| test-script | test | package.json |
| test:e2e-script | test:e2e | package.json |

**Usage:** When skills reference `[package-manager] run test`, use `pnpm run test` for this project.
```

**Advanced Variables:**

Some variables require more sophisticated detection:

| Variable | Detection Method |
|----------|------------------|
| `[workspace-name]` | Check `CODER_WORKSPACE_NAME` env var, or prompt user |
| `[hasura-console-url]` | Check for Hasura backend config, default to localhost:9695 |
| `[graphql-role]` | Check project patterns (e.g., user/employee/admin) |
| `[backend-url]` | Check backend service configs or environment |
| `[database-name]` | Check database connection strings or configs |

### Step 5: Generate Comprehensive CLAUDE.md

**File Structure:**

```markdown
# [Project Name from package.json or directory]

[Custom project description - preserve if exists, otherwise generate 1-2 sentences based on tech stack]

## Tech Stack

[Detected technologies by category with versions]

## Package Manager

[detected-package-manager] - All commands use this package manager.

## Resolved Variables

[Template variables from skills, resolved to project-specific values]

## Critical Rules

[Extracted critical rules from all matched skills - NEVER/MUST/ALWAYS patterns]

## Marketplace Plugins

[Table of matched plugins]

### Available Skills

[Table with skill names, descriptions from frontmatter, and last updated]

### Skill-Specific Guidance

[For each matched skill, include CLAUDE-specific sections extracted from SKILL.md]

## Workflows

[Core dev workflows + any from matched plugins]

## Commands

[All relevant commands]

## Quality Gates

[Detected quality gate commands]

## Version Notes

[Version-specific context from matched skills]

## Git & Commit Conventions

[Standard conventions section]

## Development Notes

[User-added content preserved, or placeholder if none]
```

**Detailed Section Templates:**

### Tech Stack Template (Skill-Linked)

```markdown
## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Next.js** | 16.1 | [`latest-nextjs`](#) | App Router, Server Components, async params |
| **React** | 19.1 | [`latest-react`](#) | Compiler, Actions, new hooks |
| **Playwright** | 1.57 | [`playwright-test`](#) | E2E testing, accessibility |

**Note:** Only technologies with relevant skills are shown. See `package.json` for full dependencies.
```

**Template Logic:**

```javascript
// Generate tech stack table from versioned tech
function generateTechStackTable(versionedTech) {
  const rows = versionedTech.map(tech => {
    return `| **${tech.displayName}** | ${tech.displayVersion} | \`${tech.skill}\` | ${getSkillPurpose(tech.skill)} |`;
  });

  return [
    '| Technology | Version | Skill | Purpose |',
    '|------------|---------|-------|---------|',
    ...rows,
    '',
    '**Note:** Only technologies with relevant skills are shown. See `package.json` for full dependencies.'
  ].join('\n');
}

function getSkillPurpose(skillName) {
  // Extract from skill frontmatter or description
  const skill = findSkill(skillName);
  return skill?.description || 'See skill docs';
}
```

### Critical Rules Template

```markdown
## Critical Rules

Extract rules from skills that match these patterns:

- **NEVER** [action] - [consequence]
- **ALWAYS** [action] - [reason]
- **MUST** [requirement] - [explanation]
- **CRITICAL** [warning] - [impact]

### From [Skill Name]

[Extract rules from this skill's SKILL.md]
```

### Skill-Specific Guidance Template

```markdown
### Skill: [Skill Name]

[Extracted content from CLAUDE-specific sections in SKILL.md]

**Key Patterns:**

[Extract common patterns/best practices]

**Version Notes:**

[Extract version-specific information]
```

### Version Notes Template

```markdown
## Version Notes

### [Framework Name] [Major Version]

**Breaking Changes:**
- [Change from skill docs]
- [Migration note if available]

**New Features:**
- [Feature from skill docs]
- [Feature from skill docs]

**Migration:**
- [Migration guide excerpt if available]
```

**If CLAUDE.md Exists - Preservation Strategy:**

1. **Read existing file** and parse into sections
2. **Preserve these sections exactly:**
   - Custom project description (between title and first `##`)
   - `## Critical Rules` - User may have added project-specific rules
   - `## Development Notes` - User's custom notes
   - Any custom sections not in standard template
3. **Update these sections completely:**
   - `## Tech Stack` - Re-detect from package.json
   - `## Package Manager` - Re-detect from lockfiles
   - `## Resolved Variables` - Re-resolve template variables from skills
   - `## Marketplace Plugins` - Refresh from current marketplace
   - `## Available Skills` - Refresh with descriptions from frontmatter
   - `## Skill-Specific Guidance` - Re-extract from SKILL.md files
   - `## Workflows` - Add/remove based on matched plugins
   - `## Commands` - Refresh command list
   - `## Quality Gates` - Re-detect from package.json
   - `## Version Notes` - Re-extract from skills
4. **Merge strategy:**
   - Append new critical rules to existing (don't duplicate)
   - Update version notes while preserving user notes
   - Keep user-added sections at the end

### Step 6: Skill Content Extraction (NEW)

For each matched skill, extract and organize content:

**Frontmatter Extraction:**

```javascript
function extractSkillFrontmatter(skillPath) {
  const content = readFile(`${skillPath}/SKILL.md`);
  const frontmatterMatch = content.match(/^---\n([\s\S]+?)\n---/);

  if (frontmatterMatch) {
    return parseYaml(frontmatterMatch[1]);
    // Expected fields: name, description, updated
  }
  return null;
}
```

**CLAUDE-Specific Section Extraction:**

```javascript
function extractClaudeSections(skillPath) {
  const content = readFile(`${skillPath}/SKILL.md`);
  const sections = {};

  // Patterns to look for
  const patterns = [
    /## CLAUDE\.md Requirements\n([\s\S]*?)(?=\n##|$)/,
    /## For CLAUDE\.md\n([\s\S]*?)(?=\n##|$)/,
    /## CLAUDE Context\n([\s\S]*?)(?=\n##|$)/,
    /## Critical Rules\n([\s\S]*?)(?=\n##|$)/,
    /## Gotchas\n([\s\S]*?)(?=\n##|$)/,
    /## Breaking Changes\n([\s\S]*?)(?=\n##|$)/,
  ];

  for (const pattern of patterns) {
    const match = content.match(pattern);
    if (match) {
      sections[match[0]] = match[1].trim();
    }
  }

  return sections;
}
```

**Critical Rules Extraction:**

```javascript
function extractCriticalRules(skillPath) {
  const content = readFile(`${skillPath}/SKILL.md`);
  const rules = [];

  // Look for code blocks with DON'T vs DO patterns
  const codeBlocks = content.match(/```[\s\S]*?```/g) || [];
  for (const block of codeBlocks) {
    if (block.includes('// ❌ WRONG') || block.includes('// ✅ CORRECT')) {
      rules.push({
        type: 'code-pattern',
        content: block
      });
    }
  }

  // Look for bullet points with NEVER/ALWAYS/MUST
  const lines = content.split('\n');
  for (const line of lines) {
    if (line.match(/- \*\*(NEVER|ALWAYS|MUST|CRITICAL)\*\*/)) {
      rules.push({
        type: 'rule',
        content: line
      });
    }
  }

  return rules;
}
```

**Version Context Extraction:**

```javascript
function extractVersionContext(skillPath, packageName) {
  const content = readFile(`${skillPath}/SKILL.md`);
  const context = {};

  // Look for version-specific sections
  const versionSection = content.match(new RegExp(
    `## ${packageName} \\d+\\.\\d+.*?\\n([\\s\\S]*?)(?=\\n##|$)`
  ));

  if (versionSection) {
    context.version_notes = versionSection[1];
  }

  // Look for breaking changes
  const breakingChanges = content.match(
    /## Breaking Changes\n([\s\S]*?)(?=\n##|$)/
  );

  if (breakingChanges) {
    context.breaking_changes = breakingChanges[1];
  }

  // Look for migration guides
  const migration = content.match(
    /## Migration Guide\n([\s\S]*?)(?=\n##|$)/
  );

  if (migration) {
    context.migration_guide = migration[1];
  }

  return context;
}
```

### Step 7: Quality Gates Validation

After generating or updating CLAUDE.md:

1. **Verify file exists** - CLAUDE.md should be in project root
2. **Check markdown formatting** - Valid markdown structure
3. **Verify all paths exist** - Skill/workflow/command references
4. **Confirm accuracy** - Detected tech matches actual dependencies
5. **Check frontmatter extraction** - All skills have descriptions
6. **Validate critical rules** - Rules are properly formatted
7. **Test links** - Any relative links should resolve

## Enhanced Examples

### Skill Frontmatter Example

Input `SKILL.md`:
```markdown
---
name: latest-nextjs
description: Latest Next.js 16 features, App Router, Server Components
updated: 2026-01-11
---

# Latest Next.js Skill

[...content...]
```

Output in CLAUDE.md:
```markdown
| Skill | Plugin | Purpose | Updated |
|-------|--------|---------|---------|
| `latest-nextjs` | nextjs | Latest Next.js 16 features, App Router, Server Components | 2026-01-11 |
```

### Critical Rules Extraction Example

From `playwright-test/SKILL.md`:
```markdown
## Base URL Configuration

**CRITICAL**: Base URLs should be configured in the Playwright config file(s), never in test files.

**DON'T** - Never add `webServer` configuration:
```typescript
// ❌ WRONG - Do not configure webServer
export default defineConfig({
  webServer: { command: "pnpm start" }
});
```

**DO** - The config file already handles base URL:
```typescript
// ✅ CORRECT - Server managed externally
export default defineConfig({
  use: { baseURL }
});
```
```

Output in CLAUDE.md:
```markdown
## Critical Rules

### Playwright Testing

- **CRITICAL**: Base URLs configured in config files, never in test files
- **NEVER** add `webServer` configuration - server is managed externally
- **ALWAYS** use root-relative paths in test files (e.g., `await page.goto("/")`)
- **NEVER** hardcode `localhost` URLs - use environment variables
```

### Version Context Example

From `latest-nextjs/SKILL.md`:
```markdown
## Next.js 16 (Released October 2025)

### Breaking Changes

#### Async Route Parameters (Breaking Change)

Route parameters are now async:

```tsx
// Before Next.js 16
export default async function Page({ params, searchParams }) {
  const id = params.id;
}

// Next.js 16+
export default async function Page({ params, searchParams }) {
  const id = await params.id; // Now async!
}
```
```

Output in CLAUDE.md:
```markdown
## Version Notes

### Next.js 16

**Breaking Changes:**
- Route parameters are now async - use `await params.id` instead of `params.id`
- `middleware.ts` renamed to `proxy.ts`

**Migration:**
```bash
npx @next/codemod@canary middleware-to-proxy
```
```

## Implementation Notes

### What Makes This Enhanced

1. **Skill-linked versioning** - Only technologies with matched skills are versioned (not full dependency dump)
2. **Major.minor precision** - Versions show major.minor only (no patch noise)
3. **Strong tech-skill linkage** - Tech stack table explicitly links technologies to their relevant skills
4. **Skill frontmatter extraction** - Descriptions and updated dates from SKILL.md
5. **Template variable resolution** - Resolves `[package-manager]`, `[test-script]`, etc. against project
6. **Better preservation** - Maintains user-added content during updates
7. **Quality gates detection** - Auto-discovers validation commands

### Version Detection Strategy

The workflow intentionally **does NOT** list every dependency. Instead:

1. **Detect all technologies** from package.json, configs, directories
2. **Match plugins** using keywords and descriptions
3. **Extract versions ONLY** for matched technologies
4. **Display major.minor** - Skip patch versions entirely
5. **Link to skills** - Each tech entry references its relevant skill

This ensures CLAUDE.md focuses on **actionable context** rather than duplicating package.json.

### Generic Discovery

This workflow works with ANY marketplace plugins:

- No hardcoded technologies
- Matching uses plugin `keywords` and `description`
- Skills are discovered from `skills/` directories
- Frontmatter follows YAML convention
- CLAUDE-specific sections use standard heading patterns
