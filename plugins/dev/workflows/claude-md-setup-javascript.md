# CLAUDE.md Setup Workflow - JavaScript/TypeScript

Generates `CLAUDE.md` for JavaScript/TypeScript projects (Node.js, Next.js, React, Vue, etc.).

**Input from Router:** Receives pre-built `marketplaceRegistry` and project detection results. DO NOT re-scan plugins.

## The Workflow

### Step 1: Analyze Workspace

```bash
cat package.json
ls -la | grep -E "\.config\.|tsconfig\.json"
cat CLAUDE.md 2>/dev/null || echo "No existing CLAUDE.md"
```

Extract dependencies/devDependencies with versions, framework names from configs, testing frameworks.

### Step 2: Match Technologies to Skills

Use `marketplaceRegistry.matchByKeywords()` to find matching plugins. Always include `dev` and `coder` plugins.

```javascript
function matchSkills(detectedTech, marketplaceRegistry) {
  const matched = [];
  for (const tech of detectedTech) {
    const plugins = marketplaceRegistry.matchByKeywords(tech.keywords);
    for (const plugin of plugins) {
      for (const skill of plugin.skills) {
        if (skill.name.toLowerCase().includes(tech.name.toLowerCase()) ||
            tech.name.toLowerCase().includes(skill.name.toLowerCase())) {
          matched.push({ tech, skill, plugin });
        }
      }
    }
  }
  return matched;
}
```

### Step 3: Extract Skill Content

For each matched skill, read the SKILL.md file (use path from registry):

```javascript
function extractSkillContent(skillPath) {
  const content = readFile(`${skillPath}/SKILL.md`);
  return {
    frontmatter: content.match(/^---\n([\s\S]+?)\n---/),
    claudeSections: extractClaudeSections(content),
    criticalRules: extractCriticalRules(content),
    versionContext: extractVersionContext(content)
  };
}
```

**Extract these sections from each SKILL.md:**
- `## CLAUDE\.md Requirements`
- `## For CLAUDE\.md`
- `## CLAUDE Context`
- `## Critical Rules`
- `## Gotchas`
- `## Breaking Changes`
- `## Version Notes`

### Step 4: Resolve Template Variables

```javascript
function resolveVariables(matchedSkills, packageJson, packageManager) {
  const scripts = packageJson.scripts || {};
  return {
    'package-manager': packageManager,
    'test-script': findScript(['test', 'test:unit', 'vitest', 'jest'], scripts),
    'test:e2e-script': findScript(['test:e2e', 'playwright', 'e2e'], scripts),
    'dev-script': findScript(['dev', 'start', 'serve'], scripts),
    'build-script': findScript(['build', 'compile', 'bundle'], scripts),
    'lint-script': findScript(['lint', 'eslint', 'check'], scripts),
    'typecheck-script': findScript(['typecheck', 'check:types', 'check'], scripts),
  };
}
```

### Step 5: Detect Quality Gates

```javascript
function detectQualityGates(packageJson) {
  const scripts = packageJson.scripts || {};
  const patterns = {
    typecheck: ['typecheck', 'check:types', 'check'],
    lint: ['lint', 'lint:fix', 'eslint'],
    format: ['format', 'prettier'],
    build: ['build', 'compile'],
    test: ['test', 'vitest', 'jest'],
    'test:e2e': ['test:e2e', 'playwright', 'e2e'],
  };
  // Return first matching script for each gate type
}
```

### Step 6: Generate CLAUDE.md

**File Structure:**

```markdown
# [Project Name]

[Description]

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Next.js** | 16.1 | `latest-nextjs` | App Router, Server Components |

**Note:** Only technologies with relevant skills shown. See `package.json` for full dependencies.

## Package Manager

[detected-package-manager]

## Resolved Variables

| Variable | Value | Source |
|----------|-------|--------|
| package-manager | pnpm | pnpm-lock.yaml |

## Critical Rules

[Extracted NEVER/MUST/ALWAYS rules from skills]

## Marketplace Plugins

### Available Skills

[Table of skills with descriptions from frontmatter]

### Skill-Specific Guidance

[Extracted CLAUDE-specific sections from skills]

## Workflows

[Core dev workflows + from matched plugins]

## Commands

[All relevant commands]

## Quality Gates

[Detected validation commands]

## Version Notes

[Version-specific context from skills]

## Git & Commit Conventions

[Standard conventions]

## Development Notes

[Preserved user content]
```

**If CLAUDE.md exists, preserve:**
- Custom project description
- `## Critical Rules`
- `## Development Notes`
- Any custom sections

**Update these sections completely:**
- Tech Stack, Package Manager, Resolved Variables
- Marketplace Plugins, Available Skills, Skill-Specific Guidance
- Workflows, Commands, Quality Gates, Version Notes

### Step 7: Validate

1. File exists in project root
2. Valid markdown structure
3. All skill/workflow references exist
4. Detected tech matches dependencies
5. Skills have descriptions from frontmatter
