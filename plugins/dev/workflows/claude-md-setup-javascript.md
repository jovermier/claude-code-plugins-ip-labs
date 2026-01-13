# CLAUDE.md Setup Workflow - JavaScript/TypeScript

Generates `CLAUDE.md` for JavaScript/TypeScript projects (Node.js, Next.js, React, Vue, etc.).

## When to Use This Sub-Workflow

- Invoked by `claude-md-setup.md` when `package.json` is detected
- For any Node.js project (Express, Next.js, React, Vue, Angular, etc.)
- For TypeScript projects

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

**Plugin Registry Structure:**

```yaml
# Build a registry like this:
plugins:
  - name: [plugin-name]  # e.g., "nextjs", "playwright", "react"
    description: [what it provides]
    keywords: [tag1, tag2, ...]
    skills:
      - name: [skill-name-from-directory]  # e.g., "latest-nextjs"
        path: [full-path-to-skill]
        description: [from SKILL.md frontmatter]
        updated: [from SKILL.md frontmatter]
        claude_sections: [extracted CLAUDE-specific sections]
        critical_rules: [extracted critical rules]
        version_context: [extracted version-specific notes]
```

### Step 2: Extract Skill Metadata

For EACH skill discovered, read its `SKILL.md` file and extract:

**Frontmatter Fields:**
```yaml
# Extract these fields from SKILL.md frontmatter (between --- markers):
name: skill-name
description: One-line description of what the skill provides
updated: ISO date or version reference
```

**CLAUDE-Specific Sections:**

Look for these special sections in SKILL.md:

| Section Pattern | Purpose |
|----------------|---------|
| `## CLAUDE\.md Requirements` | Explicit instructions for CLAUDE.md |
| `## For CLAUDE\.md` | Content meant for CLAUDE.md |
| `## CLAUDE Context` | Context specifically for Claude |
| `## Critical Rules` | Important rules that must be documented |
| `## Gotchas` | Common pitfalls to avoid |
| `## Breaking Changes` | Version-specific breaking changes |
| `## Version Notes` | Version-specific context |

### Step 3: Analyze the Workspace

```bash
# Check for package.json
cat package.json

# Look for framework configs
ls -la | grep -E "\.config\."

# Check for TypeScript
ls -la | grep -E "tsconfig\.json"

# Check for testing setup
ls -la tests/ 2>/dev/null || ls -la __tests__/ 2>/dev/null

# Check for lockfiles to detect package manager
ls -la | grep -E "(pnpm-lock|yarn.lock|package-lock|bun.lockb)"
```

**Extract Technologies:**

- From `package.json`: All dependencies and devDependencies with versions
- From config files: Framework names (next.config.js, vite.config.js, etc.)
- From directories: Backend frameworks, testing frameworks
- From existing `CLAUDE.md`: Custom user content to preserve

**Version Detection (Skill-Linked):**

Only extract versions for technologies that have **matched skills**:

```javascript
function extractVersionedTech(detectedTech, matchedPlugins) {
  const versioned = [];

  for (const tech of detectedTech) {
    const matchedSkill = findSkillForTech(tech, matchedPlugins);
    if (matchedSkill) {
      const version = parseVersion(tech.version);
      versioned.push({
        name: tech.name,
        displayName: tech.displayName,  // e.g., "Next.js", "React"
        major: version.major,
        minor: version.minor,
        displayVersion: `${version.major}.${version.minor}`,  // "16.1" - NO patch
        skill: matchedSkill.name,
        skillPlugin: matchedSkill.plugin
      });
    }
  }

  return versioned;
}

function parseVersion(versionString) {
  const clean = versionString.replace(/^[\^~]/, '');
  const parts = clean.split('.');
  return {
    major: parts[0] || '0',
    minor: parts[1] || '0',
    patch: parts[2] || '0'  // Captured but NOT used in display
  };
}
```

**Package Manager Detection:**

Check lockfiles in priority order:
1. `bun.lockb` → bun
2. `pnpm-lock.yaml` → pnpm
3. `yarn.lock` → yarn
4. `package-lock.json` → npm (default fallback)

### Step 4: Match Technologies to Plugins

```javascript
function matchPlugins(plugins, detectedTech) {
  return plugins.filter(plugin => {
    const keywordMatch = plugin.keywords.some(kw =>
      detectedTech.some(tech =>
        tech.toLowerCase().includes(kw.toLowerCase()) ||
        kw.toLowerCase().includes(tech.toLowerCase())
      )
    );

    const descMatch = detectedTech.some(tech =>
      plugin.description.toLowerCase().includes(tech.toLowerCase())
    );

    return keywordMatch || descMatch;
  });
}
```

**Always Include These Plugins:**

- **`dev`** - Core workflows, agents, todos (always relevant)
- **`coder`** - If running in a Coder workspace

### Step 5: Resolve Template Variables

```javascript
function resolveVariables(variables, project) {
  const resolved = {};
  for (const variable of variables) {
    const key = variable.replace(/[\[\]]/g, '').toLowerCase();
    resolved[key] = resolveVariable(key, project);
  }
  return resolved;
}

function resolveVariable(variableName, project) {
  const resolvers = {
    'package-manager': () => detectPackageManager(),
    'test-script': () => findScript('test', project.packageJson),
    'dev-script': () => findScript('dev', project.packageJson),
    'build-script': () => findScript('build', project.packageJson),
    'lint-script': () => findScript('lint', project.packageJson),
  };

  const resolver = resolvers[variableName];
  return resolver ? resolver() : `[${variableName}]`;
}

function findScript(type, packageJson) {
  const scripts = packageJson.scripts || {};
  const patterns = {
    'test': ['test', 'test:unit', 'vitest', 'jest'],
    'dev': ['dev', 'start', 'serve'],
    'build': ['build', 'compile', 'bundle'],
    'lint': ['lint', 'eslint', 'check']
  };

  const typePatterns = patterns[type] || [type];
  for (const pattern of typePatterns) {
    if (scripts[pattern]) return pattern;
  }
  return null;
}
```

### Step 6: Generate CLAUDE.md

**File Structure:**

```markdown
# [Project Name from package.json]

[Project description]

## Tech Stack

[Detected technologies by category with versions]

## Package Manager

[detected-package-manager] - All commands use this package manager.

## Resolved Variables

[Template variables resolved to project-specific values]

## Critical Rules

[Extracted NEVER/MUST/ALWAYS rules from all skills]

## Marketplace Plugins

[Table of matched plugins]

### Available Skills

[Skills with descriptions from frontmatter]

### Skill-Specific Guidance

[Extracted CLAUDE-specific sections from skills]

## Workflows

[Core dev workflows + any from matched plugins]

## Commands

[All relevant commands]

## Quality Gates

[Detected validation commands]

## Version Notes

[Breaking changes and new features by version]

## Development Notes

[User-preserved content]
```

## Example Output

### Tech Stack Table

```markdown
## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Next.js** | 16.1 | `latest-nextjs` | App Router, Server Components, async params |
| **React** | 19.2 | `latest-react` | Compiler, Actions, new hooks |
| **Playwright** | 1.57 | `playwright-test` | E2E testing, accessibility |
```

### Resolved Variables

```markdown
## Resolved Variables

| Variable | Value | Source |
|----------|-------|--------|
| `package-manager` | `pnpm` | Detected from pnpm-lock.yaml |
| `test-script` | `test` | Found in package.json scripts |
| `dev-script` | `dev` | Found in package.json scripts |
```
