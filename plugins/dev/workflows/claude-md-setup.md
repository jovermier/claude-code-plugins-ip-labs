# CLAUDE.md Setup Workflow (Main Router)

Detects project type and routes to the appropriate language-specific sub-workflow for generating `CLAUDE.md`.

## When to Use This Workflow

- Invoked by `/project:setup` command
- When starting a new project
- After adding new technologies to the project
- When onboarding to an existing project

## Architecture

```
claude-md-setup.md (Router)
├── Step 1: Scan ALL Marketplace Plugins (CENTRALIZED)
│   └── Builds complete plugin/skill registry
├── Step 2: Detect Project Type
├── Step 3: Route to sub-workflow WITH REGISTRY
└── Sub-workflows receive pre-scanned registry:
    ├── claude-md-setup-javascript.md  # Node.js, TypeScript, Next.js, React, etc.
    ├── claude-md-setup-python.md      # Python, Django, FastAPI, etc.
    ├── claude-md-setup-rust.md        # Rust, Cargo
    ├── claude-md-setup-go.md          # Go modules
    ├── claude-md-setup-php.md         # PHP, Composer
    ├── claude-md-setup-ruby.md        # Ruby, Bundler
    ├── claude-md-setup-java.md        # Java, Maven, Gradle
    └── claude-md-setup-generic.md     # Fallback for unknown types
```

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

**Build This Registry Structure:**

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
          updated: "2026-01-11",
          claudeSections: {},
          criticalRules: [],
          versionContext: {}
        }
      ]
    }
  ],

  // Helper functions for sub-workflows
  findPlugin: function(name) { /* ... */ },
  findSkill: function(name) { /* ... */ },
  matchByKeywords: function(keywords) { /* ... */ }
};
```

**IMPORTANT:** Pass this registry to the sub-workflow in Step 3.

### Step 2: Detect Project Type

```bash
ls -la | grep -E "(package\.json|pyproject\.toml|setup\.py|requirements\.txt|Cargo\.toml|go\.mod|composer\.json|Gemfile|pom\.xml|build\.gradle)"
```

**Detection Logic:**

```javascript
function detectProjectType() {
  const files = listFiles('.');

  if (files.includes('package.json'))
    return { type: 'javascript', subWorkflow: 'claude-md-setup-javascript.md', manager: detectPackageManagerJS() };
  if (files.includes('pyproject.toml'))
    return { type: 'python', subWorkflow: 'claude-md-setup-python.md', manager: 'poetry' };
  if (files.includes('setup.py') || files.includes('requirements.txt'))
    return { type: 'python', subWorkflow: 'claude-md-setup-python.md', manager: 'pip' };
  if (files.includes('Cargo.toml'))
    return { type: 'rust', subWorkflow: 'claude-md-setup-rust.md', manager: 'cargo' };
  if (files.includes('go.mod'))
    return { type: 'go', subWorkflow: 'claude-md-setup-go.md', manager: 'go' };
  if (files.includes('composer.json'))
    return { type: 'php', subWorkflow: 'claude-md-setup-php.md', manager: 'composer' };
  if (files.includes('Gemfile'))
    return { type: 'ruby', subWorkflow: 'claude-md-setup-ruby.md', manager: 'bundler' };
  if (files.includes('pom.xml'))
    return { type: 'java', subWorkflow: 'claude-md-setup-java.md', manager: 'maven' };
  if (files.includes('build.gradle') || files.includes('build.gradle.kts'))
    return { type: 'java', subWorkflow: 'claude-md-setup-java.md', manager: 'gradle' };

  return { type: 'generic', subWorkflow: 'claude-md-setup-generic.md', manager: null };
}

function detectPackageManagerJS() {
  const lockfiles = listFiles('.').filter(f => f.match(/(pnpm-lock|yarn\.lock|package-lock|bun\.lockb)/));
  if (lockfiles.includes('pnpm-lock.yaml')) return 'pnpm';
  if (lockfiles.includes('bun.lockb')) return 'bun';
  if (lockfiles.includes('yarn.lock')) return 'yarn';
  return 'npm';
}
```

### Step 3: Route to Sub-Workflow WITH REGISTRY

| Project Type  | Sub-Workflow                   |
|---------------|--------------------------------|
| JavaScript    | claude-md-setup-javascript.md  |
| Python        | claude-md-setup-python.md      |
| Rust          | claude-md-setup-rust.md        |
| Go            | claude-md-setup-go.md          |
| PHP           | claude-md-setup-php.md         |
| Ruby          | claude-md-setup-ruby.md        |
| Java          | claude-md-setup-java.md        |
| Generic       | claude-md-setup-generic.md     |

**Input to Sub-Workflow:**

```javascript
{
  marketplaceRegistry: {
    plugins: Plugin[],
    findPlugin: (name: string) => Plugin | null,
    findSkill: (name: string) => Skill | null,
    matchByKeywords: (keywords: string[]) => Plugin[]
  },
  projectType: 'javascript' | 'python' | 'rust' | 'go' | 'php' | 'ruby' | 'java' | 'generic',
  packageManager: string | null,
  projectRoot: string,
  existingClaudeMd: string | null
}
```

**Sub-workflows MUST:**
- Use the pre-built registry (NOT re-scan plugins)
- Extract language-specific dependencies and versions
- Match detected tech to skills in the registry
- Generate CLAUDE.md with appropriate structure

### Step 4: Generate CLAUDE.md

The sub-workflow returns the generated CLAUDE.md content. Write it to the project root.

**Preservation Strategy:**

If `CLAUDE.md` exists, preserve:
- Custom project description (between title and first `##`)
- `## Critical Rules`
- `## Development Notes`
- Any custom sections not in standard template

## Why Centralized Scanning Is More Reliable

**Before:** Each sub-workflow scans independently → duplication, inconsistency, maintenance burden

**After:** Router scans once → single source of truth, consistent matching, easier maintenance
