# CLAUDE.md Setup Workflow

Analyzes the project and generates or updates `CLAUDE.md` with relevant marketplace skills, workflows, and project context. This workflow dynamically discovers all available plugins without hardcoding any specific technologies.

## When to Use This Workflow

- Invoked by `/project:setup` command
- When starting a new project
- After adding new technologies to the project
- When onboarding to an existing project

## The Workflow

### Step 1: Scan Marketplace Plugins

Discover all available plugins by reading the marketplace configuration:

```bash
# Read marketplace configuration
cat .claude-plugin/marketplace.json

# List all plugin directories
ls -la plugins/
```

For each plugin, extract:
- **Plugin name** - From `name` field
- **Description** - What the plugin provides
- **Keywords** - Searchable tags for matching
- **Skills** - Array of skill paths
- **Commands** - Array of command paths (if applicable)
- **Hooks** - Array of hook paths (if applicable)

**Plugin Registry Structure:**

```yaml
# Build a registry like this:
plugins:
  - name: [plugin-name]
    description: [what it provides]
    keywords: [tag1, tag2, ...]
    skills: [skill-path-1, skill-path-2, ...]
    commands: [command-path-1, ...]  # if present
```

### Step 2: Analyze the Workspace

Gather information about the project:

```bash
# Check for package.json (if exists)
cat package.json

# Look for framework configs
ls -la | grep -E "\.config\."

# Check for backend directories
ls -la | grep -E "(api|server|backend|functions)"

# Check for testing setup
ls -la tests/ 2>/dev/null || ls -la __tests__/ 2>/dev/null || echo "No tests directory"
```

**Extract Technologies:**

- From `package.json`: All dependencies and devDependencies with their versions
- From config files: Framework names (parse filename patterns like `*.config.{js,ts,mjs}`)
- From directories: Backend frameworks, testing frameworks

**Detect Quality Gates from package.json:**

Scan the `scripts` section in `package.json` for quality gate commands:

| Gate Type | Script Name Patterns (checked in priority order) |
|-----------|---------------------------------------------------|
| Type Checks | `typecheck`, `check`, `validate` |
| Linting | `lint`, `lint:fix` |
| Build | `build`, `compile`, `bundle` |
| Tests | `test`, `test:unit`, `test:e2e` |

For each category, find the first matching script name and generate the full command using the detected package manager.

**Version Detection:**

When extracting dependencies, capture and report major versions for frameworks that have significant version-specific features. This is important because major version releases often introduce breaking changes or new capabilities that should be documented.

For each dependency, extract:
- Package name
- Installed version (from `package.json` or `package-lock.json`)
- Major version number (e.g., 19.x, 5.x, 4.x)

Include major versions in the Tech Stack section when the version is significant for development decisions or feature availability.

### Step 3: Match Technologies to Plugins

Compare detected technologies against plugin keywords and descriptions:

```python
# Pseudocode for matching
detected_tech = extract_from_package_json() + extract_from_configs()

matched_plugins = []
for plugin in scan_marketplace():
    # Check if any detected tech matches plugin keywords
    if any(tech in plugin.keywords for tech in detected_tech):
        matched_plugins.append(plugin)
    # Also check descriptions for mentions
    elif any(tech.lower() in plugin.description.lower() for tech in detected_tech):
        matched_plugins.append(plugin)
```

**Matching Logic:**

| Detection Source | Match Against |
|------------------|--------------|
| `package.json` dependencies | Plugin `keywords` array |
| Config filenames | Plugin `description` text |
| Directory patterns | Plugin `keywords` array |

### Step 4: Collect Skills, Workflows, and Commands

For each matched plugin, collect its resources:

**Skills:**
- Read each skill's `SKILL.md` file
- Extract the `description` from frontmatter
- Build a table of available skills

**Workflows:**
- Always include core workflows from the `dev` plugin (meta-workflow, TDD, UI iteration, bug-fix)
- Include any additional workflows from matched plugins

**Commands:**
- Collect all commands from the `dev` plugin
- Include commands from other matched plugins (if any)

### Step 5: Generate or Update CLAUDE.md

**If CLAUDE.md doesn't exist:**

Create a new file with this structure:

```markdown
# [Project Name from package.json or directory]

[Generate a brief 1-2 sentence description based on detected technologies]

## Tech Stack

List detected technologies by category, including major versions when significant:

- **Frontend**: [Framework name and major version]
- **Backend**: [Backend technologies with versions if applicable]
- **Testing**: [Testing frameworks with versions]
- **Tooling**: [Build tools, linters, etc.]

## Package Manager

[detected-package-manager] - Always use this package manager for all commands in this project.

## Available Skills

| Skill | Plugin | Purpose |
|-------|--------|---------|
| [skill-name-from-path] | [plugin-name] | [skill description] |
| ... | ... | ... |

*Note: Skill descriptions come from each skill's SKILL.md frontmatter*

## Workflows

List all relevant workflows:

- [Meta-Workflow](.claude/workflows/meta-workflow.md) - Automatic workflow selection and composition
- [TDD Workflow](.claude/workflows/tdd-workflow.md) - Test-driven development
- [UI Iteration Workflow](.claude/workflows/ui-iteration-workflow.md) - Iterative UI development with visual feedback
- [Bug Fix Workflow](.claude/workflows/bug-fix-workflow.md) - Systematic debugging approach

*Include additional workflows from matched plugins here*

## Commands

| Command | Purpose |
|---------|---------|
| `/project:setup` | Regenerate this CLAUDE.md file |
| [command-from-plugin] | [command description] |

## Quality Gates

Run these commands after making changes to verify code quality:

```bash
# Type Checks
[package-manager] run [detected-typecheck-script]

# Linting
[package-manager] run [detected-lint-script]

# Build
[package-manager] run [detected-build-script]

# Tests (if applicable)
[package-manager] run [detected-test-script]
```

*Note: Package manager is detected automatically from lockfiles. Scripts are extracted from package.json.*

## Development Notes

[Any project-specific conventions, patterns, or notes - leave this section empty or add a placeholder if none detected]
```

**If CLAUDE.md exists:**

1. Read the existing file
2. Preserve these sections (if they exist):
   - Custom project description (between title and Tech Stack)
   - Development notes section
   - Any user-added content not in standard sections
3. Update these sections completely:
   - Tech Stack (re-detect from current package.json)
   - Package Manager (re-detect from lockfiles)
   - Available Skills (refresh from current marketplace)
   - Workflows (add/remove based on matched plugins)
   - Commands (refresh command list)
   - Quality Gates (re-detect scripts from package.json)

### Step 6: Quality Gates

After generating or updating CLAUDE.md:

1. **Verify file exists** - CLAUDE.md should be in project root
2. **Check formatting** - Should be valid markdown
3. **Verify plugin paths** - All skill/workflow/command references should exist
4. **Confirm accuracy** - Detected technologies should match actual dependencies

## Generic Plugin Discovery Example

The workflow works with any marketplace plugins. Here's how it processes plugins generically:

```javascript
// Generic dependency extraction with version detection
function extractDependencies(packageJson) {
  const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
  return Object.entries(deps).map(([name, version]) => {
    const majorVersion = version.replace(/^[\^~]/, '').split('.')[0];
    return { name, version, majorVersion };
  });
}

// Generic plugin scanning - works for ANY marketplace
function scanMarketplace(marketplacePath) {
  const marketplaceConfig = readJson(`${marketplacePath}/marketplace.json`);
  const plugins = [];

  for (const pluginRef of marketplaceConfig.plugins) {
    const pluginPath = `${marketplacePath}/${pluginRef.source}`;
    const pluginConfig = readJson(`${pluginPath}/.claude-plugin/plugin.json`);

    plugins.push({
      name: pluginConfig.name,
      description: pluginConfig.description,
      keywords: pluginConfig.keywords || [],
      skills: pluginRef.skills || [],
      commands: pluginRef.commands || [],
      workflows: discoverWorkflows(pluginPath) // Scan workflows/ directory
    });
  }

  return plugins;
}

// Generic matching - works for ANY technology
function matchPlugins(plugins, detectedTech) {
  return plugins.filter(plugin => {
    const techLower = detectedTech.toLowerCase();
    return plugin.keywords.some(kw => kw.toLowerCase().includes(techLower)) ||
           plugin.description.toLowerCase().includes(techLower);
  });
}

// Detect quality gates from package.json scripts
function detectQualityGates(packageJson) {
  const scripts = packageJson.scripts || {};
  const packageManager = detectPackageManager();

  const qualityGates = {
    typecheck: null,
    lint: null,
    build: null,
    test: null
  };

  // For each category, search scripts for matching names
  // Patterns are checked in priority order, first match wins
  const categories = [
    { key: 'typecheck', patterns: ['typecheck', 'check', 'validate'] },
    { key: 'lint', patterns: ['lint', 'lint:fix'] },
    { key: 'build', patterns: ['build', 'compile', 'bundle'] },
    { key: 'test', patterns: ['test', 'test:unit', 'test:e2e'] }
  ];

  for (const category of categories) {
    for (const pattern of category.patterns) {
      if (scripts[pattern]) {
        qualityGates[category.key] = `${packageManager} run ${pattern}`;
        break;
      }
    }
  }

  return qualityGates;
}

// Detect package manager from lockfile
function detectPackageManager() {
  // Check for lockfiles in priority order
  const lockfiles = [
    { file: 'bun.lockb', manager: 'bun' },
    { file: 'pnpm-lock.yaml', manager: 'pnpm' },
    { file: 'yarn.lock', manager: 'yarn' },
    { file: 'package-lock.json', manager: 'npm' }
  ];

  for (const { file, manager } of lockfiles) {
    if (exists(file)) return manager;
  }

  return 'npm'; // default fallback
}
```

## Notes

- This workflow is **completely generic** - it discovers plugins dynamically from `marketplace.json`
- No technologies are hardcoded; matching uses `keywords` and `description` from each plugin
- The workflow will automatically work with any new plugins added to the marketplace
- Updates preserve user-added content while refreshing generated sections
