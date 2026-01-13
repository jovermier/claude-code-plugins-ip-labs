# CLAUDE.md Setup Workflow (Main Router)

Detects project type and routes to the appropriate language-specific sub-workflow for generating `CLAUDE.md`.

## When to Use This Workflow

- Invoked by `/project:setup` command
- When starting a new project
- After adding new technologies to the project
- When onboarding to an existing project

## The Workflow

### Step 1: Scan ALL Marketplace Plugins (CENTRALIZED)

All marketplace plugins are scanned once in the router, then passed to sub-workflows. This ensures consistent plugin/skill discovery across all project types.

**Execute these commands:**

```bash
# 1. Check user-level plugin cache (PRIMARY)
ls -la ~/.claude/plugins/cache/ 2>/dev/null || echo "No user plugin cache"

# 2. Find all plugin.json files
find ~/.claude/plugins/cache/ -name "plugin.json" 2>/dev/null

# 3. Find all SKILL.md files
find ~/.claude/plugins/cache/ -name "SKILL.md" -path "*/skills/*/SKILL.md" 2>/dev/null

# 4. Check dev plugins directory (SECONDARY)
find ~/claude-code-plugins-ip-labs/plugins/ -name "plugin.json" 2>/dev/null

# 5. Check project-local plugins (TERTIARY)
find .claude/ -name "SKILL.md" -path "*/skills/*/SKILL.md" 2>/dev/null
```

**For EACH plugin.json found:**
1. Read `plugin.json` to extract: `name`, `description`, `keywords`, `version`
2. Find all `SKILL.md` files in that plugin's `skills/` directory
3. For each `SKILL.md`, read frontmatter (between `---` markers) to extract: `name`, `description`, `updated`

**Build This Registry:**

```javascript
const marketplaceRegistry = {
  plugins: [
    {
      name: "nextjs",
      version: "1.0.0",
      description: "Next.js framework skills",
      keywords: ["nextjs", "next.js", "ssr", "react"],
      skills: [
        {
          name: "latest-nextjs",
          path: "~/.claude/plugins/cache/.../skills/latest-nextjs/",
          description: "Latest Next.js features",
          updated: "2026-01-11"
        }
      ]
    }
  ],
  findPlugin: function(name) { /* ... */ },
  findSkill: function(name) { /* ... */ },
  matchByKeywords: function(keywords) { /* ... */ }
};
```

### Step 2: Detect Project Type

```bash
ls -la | grep -E "(package\.json|pyproject\.toml|setup\.py|requirements\.txt|Cargo\.toml|go\.mod|composer\.json|Gemfile|pom\.xml|build\.gradle)"
```

| File Present | Sub-Workflow |
|--------------|--------------|
| package.json | claude-md-setup-javascript.md |
| pyproject.toml, setup.py, requirements.txt | claude-md-setup-python.md |
| Cargo.toml | claude-md-setup-rust.md |
| go.mod | claude-md-setup-go.md |
| composer.json | claude-md-setup-php.md |
| Gemfile | claude-md-setup-ruby.md |
| pom.xml | claude-md-setup-java.md |
| build.gradle, build.gradle.kts | claude-md-setup-java.md |
| Anything else | claude-md-setup-generic.md |

Also detect package manager from lockfiles:
- pnpm-lock.yaml → pnpm
- bun.lockb → bun
- yarn.lock → yarn
- package-lock.json → npm

### Step 3: READ AND FOLLOW the Sub-Workflow

**CRITICAL:** You MUST explicitly READ the sub-workflow file and then FOLLOW each step in it.

1. **Read the full sub-workflow file:**
   - Read `plugins/dev/workflows/claude-md-setup-[detected-type].md`
   - Read the ENTIRE file, not just the first part

2. **Follow EACH step in that sub-workflow in order:**
   - Execute the bash commands shown
   - Extract the data specified
   - Generate the CLAUDE.md content as instructed

3. **DO NOT skip steps or generate CLAUDE.md yourself.**

Example:
```
Detected: package.json → JavaScript project
ACTION: Read plugins/dev/workflows/claude-md-setup-javascript.md
THEN: Follow each step in that file exactly
```

**The sub-workflow will produce the CLAUDE.md content.**

### Step 4: Write CLAUDE.md

Write the generated CLAUDE.md content to the project root.

**Preservation Strategy:**

If `CLAUDE.md` exists, the sub-workflow will have already preserved:
- Custom project description (between title and first `##`)
- `## Critical Rules`
- `## Development Notes`
- Any custom sections not in standard template

## Why This Architecture

**Centralized scanning:** Router scans plugins once → single source of truth, consistent matching across all project types.

**Explicit delegation:** Router explicitly reads and delegates to sub-workflow → ensures the sub-workflow is actually followed.
