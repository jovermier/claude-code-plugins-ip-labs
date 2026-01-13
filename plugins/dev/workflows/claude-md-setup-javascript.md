# CLAUDE.md Setup Workflow - JavaScript/TypeScript

Generates `CLAUDE.md` for JavaScript/TypeScript projects (Node.js, Next.js, React, Vue, etc.).

## ⚠️ CRITICAL EXECUTION INSTRUCTIONS

**THIS IS NOT DOCUMENTATION - THESE ARE STEPS YOU MUST ACTUALLY EXECUTE**

When following this workflow:
1. **YOU MUST EXECUTE THE BASH COMMANDS** shown in each step
2. **YOU MUST READ THE FILES** that the commands discover
3. **YOU MUST EXTRACT METADATA** from discovered plugins and skills
4. **YOU MUST USE THE EXTRACTED DATA** to generate the CLAUDE.md

Do NOT treat the code blocks in this workflow as illustrative examples. They are **mandatory execution steps**.

## When to Use This Sub-Workflow

- Invoked by `claude-md-setup.md` when `package.json` is detected
- For any Node.js project (Express, Next.js, React, Vue, Angular, etc.)
- For TypeScript projects

## The Workflow

### Step 1: Scan Marketplace Plugins (CRITICAL - MUST EXECUTE)

**YOU MUST ACTUALLY EXECUTE THESE COMMANDS** to discover all available plugins. This is not illustrative - these are mandatory discovery steps.

**MUST SCAN IN THIS ORDER:**

1. **PRIMARY**: `~/.claude/plugins/cache/` - User-level installed marketplace plugins
2. **SECONDARY**: `~/claude-code-plugins-ip-labs/plugins/` - Development/local plugins (if present)
3. **TERTIARY**: `.claude/plugins/` - Project-local plugins

```bash
# ACTUAL COMMANDS YOU MUST RUN:

# 1. Check if user-level plugin cache exists
ls -la ~/.claude/plugins/cache/ 2>/dev/null || echo "No user plugin cache"

# 2. Find all plugin.json files in user-level cache
find ~/.claude/plugins/cache/ -name "plugin.json" 2>/dev/null

# 3. For each marketplace in ~/.claude/plugins/cache/, list plugins
for marketplace in ~/.claude/plugins/cache/*/; do
  echo "Marketplace: $marketplace"
  find "$marketplace" -name "plugin.json" -exec echo "  Plugin: {}" \;
done

# Expected output structure:
# ~/.claude/plugins/cache/
#   └── ip-labs-marketplace/
#       ├── astro/1.0.0/.claude-plugin/plugin.json
#       ├── nextjs/1.0.0/.claude-plugin/plugin.json
#       ├── react/1.0.0/.claude-plugin/plugin.json
#       ├── playwright/1.0.0/.claude-plugin/plugin.json
#       └── dev/1.2.0/.claude-plugin/plugin.json

# 4. Find all SKILL.md files in user-level cache
find ~/.claude/plugins/cache/ -name "SKILL.md" 2>/dev/null

# 5. Check dev plugins directory
find ~/claude-code-plugins-ip-labs/plugins/ -name "plugin.json" 2>/dev/null

# 6. Check project-local plugins
find .claude/ -name "SKILL.md" -path "*/skills/*/SKILL.md" 2>/dev/null
```

**For EACH plugin.json found, YOU MUST:**
1. Read the `plugin.json` file to extract: `name`, `description`, `keywords`, `version`
2. Find all `SKILL.md` files in that plugin's `skills/` directory
3. For each `SKILL.md`, read the frontmatter (between `---` markers) to extract: `name`, `description`, `updated`

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

**IMPORTANT**: After building this registry, YOU MUST use it to:
1. Match detected technologies (from package.json) to plugin keywords
2. Only version technologies that have matching skills
3. Include the `Skill` column in the Tech Stack table with the skill name

### Step 2: Extract Skill Metadata (MUST READ EACH SKILL)

**YOU MUST READ EACH SKILL.md FILE FOUND IN STEP 1** - Do not skip this step.

For EACH skill discovered in Step 1, read its `SKILL.md` file and extract:

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

### Tech Stack Table (WITH SKILL COLUMN - REQUIRED)

```markdown
## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Next.js** | 16.1 | `latest-nextjs` | App Router, Server Components, async params |
| **React** | 19.2 | `latest-react` | Compiler, Actions, new hooks |
| **Playwright** | 1.57 | `playwright-test` | E2E testing, accessibility |
```

**CRITICAL**: The `Skill` column MUST be included for technologies that have matching marketplace plugins. This links the technology to its specialized skill.

### Resolved Variables

```markdown
## Resolved Variables

| Variable | Value | Source |
|----------|-------|--------|
| `package-manager` | `pnpm` | Detected from pnpm-lock.yaml |
| `test-script` | `test` | Found in package.json scripts |
| `dev-script` | `dev` | Found in package.json scripts |
```
