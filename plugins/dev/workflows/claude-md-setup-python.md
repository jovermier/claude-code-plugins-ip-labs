# CLAUDE.md Setup Workflow - Python

Generates `CLAUDE.md` for Python projects (Django, FastAPI, Flask, Poetry, pip, etc.).

## When to Use This Sub-Workflow

- Invoked by `claude-md-setup.md` when Python files are detected (`pyproject.toml`, `setup.py`, `requirements.txt`)
- For any Python project (Django, FastAPI, Flask, etc.)
- For projects using Poetry or pip

## The Workflow

### Step 1: Scan Marketplace Plugins

Discover all available plugins by reading the marketplace configuration:

```bash
# Find marketplace plugins directory
# 1. ~/.claude/plugins/cache/ - User-level installed marketplace plugins (PRIMARY)
# 2. ~/claude-code-plugins-ip-labs/plugins/ - Development/local plugins
# 3. .claude/plugins/ - Project-local plugins

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
- **Skills** - Array of skill paths

### Step 2: Extract Skill Metadata

For EACH skill discovered, read its `SKILL.md` file and extract:

**Frontmatter Fields:**
```yaml
name: skill-name
description: One-line description of what the skill provides
updated: ISO date or version reference
```

**CLAUDE-Specific Sections:**

| Section Pattern | Purpose |
|----------------|---------|
| `## CLAUDE\.md Requirements` | Explicit instructions for CLAUDE.md |
| `## For CLAUDE\.md` | Content meant for CLAUDE.md |
| `## CLAUDE Context` | Context specifically for Claude |
| `## Critical Rules` | Important rules that must be documented |
| `## Gotchas` | Common pitfalls to avoid |

### Step 3: Analyze the Workspace

```bash
# Check for Python project files
cat pyproject.toml 2>/dev/null || cat setup.py 2>/dev/null || cat requirements.txt

# Detect framework
ls -la | grep -E "(manage\.py|app\.py|wsgi\.py|asgi\.py)"

# Check for lockfiles
ls -la | grep -E "(poetry\.lock|Pipfile\.lock|requirements\.txt)"

# Check for testing setup
ls -la tests/ 2>/dev/null || ls -la test/ 2>/dev/null

# Check for common Python configs
ls -la | grep -E "(pytest\.ini|tox\.ini|\.flake8|ruff\.toml|pyproject\.toml)"
```

**Extract Technologies:**

- From `pyproject.toml`: All dependencies (project.dependencies, project.optional-dependencies)
- From `setup.py`: install_requires, extras_require
- From `requirements.txt`: All packages with versions
- From directories: Framework detection (Django: manage.py, Flask: app.py, FastAPI: typically main.py)
- From existing `CLAUDE.md`: Custom user content to preserve

**Package Manager Detection:**

```javascript
function detectPackageManagerPython() {
  const files = listFiles('.');

  if (files.includes('poetry.lock')) return 'poetry';
  if (files.includes('Pipfile.lock')) return 'pipenv';
  if (files.includes('pyproject.toml') && hasPoetrySection()) return 'poetry';
  if (files.includes('requirements.txt') || files.includes('setup.py')) return 'pip';
  return 'pip'; // default fallback
}
```

**Version Detection (Skill-Linked):**

```javascript
function extractPythonVersions(detectedTech, matchedPlugins) {
  const versioned = [];

  for (const tech of detectedTech) {
    const matchedSkill = findSkillForTech(tech, matchedPlugins);
    if (matchedSkill) {
      const version = parsePythonVersion(tech.version);
      versioned.push({
        name: tech.name,
        displayName: tech.displayName,  // e.g., "Django", "FastAPI"
        displayVersion: version,  // Keep as-is for Python (e.g., "5.1", "0.104.1")
        skill: matchedSkill.name,
        skillPlugin: matchedSkill.plugin
      });
    }
  }

  return versioned;
}
```

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
  const pm = project.packageManager; // 'poetry' or 'pip'

  const resolvers = {
    'package-manager': () => pm,
    'install-command': () => pm === 'poetry' ? 'poetry install' : 'pip install -r requirements.txt',
    'test-command': () => findPythonCommand('test', project),
    'dev-command': () => findPythonCommand('dev', project),
    'build-command': () => pm === 'poetry' ? 'poetry build' : 'python -m build',
    'lint-command': () => findPythonCommand('lint', project),
    'format-command': () => findPythonCommand('format', project),
  };

  const resolver = resolvers[variableName];
  return resolver ? resolver() : `[${variableName}]`;
}
```

### Step 6: Generate CLAUDE.md

**File Structure:**

```markdown
# [Project Name from pyproject.toml or directory]

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

### Meta-Workflow (Default)

The **meta-workflow** is the default workflow that auto-routes all requests based on task complexity. It is enforced via the `meta-workflow-enforcer` hook from the dev plugin.

**Task Type Detection:**

| Request Type | Strategy | Example |
|--------------|----------|---------|
| Information queries (ending with `?`) | Direct response | "What does this function do?" |
| Simple changes ("fix typo", "change word") | Direct execution + quality gates | "Fix typo in heading" |
| New features | TDD workflow | "Add new endpoint" |
| Bug fixes | Bug-fix workflow | "Fix authentication bug" |
| Complex tasks | Full 7-step meta-workflow | "Add new feature with tests" |

**The 7-Step Meta-Workflow Process:**

1. **Plan Approach** - Assess task and determine strategy
2. **Explore** (if needed) - Gather missing context
3. **Plan Solution** (if complex) - Create implementation plan
4. **Step 3.5: Plan Scrutiny** - Multi-agent validation with P1/P2/P3 severity
5. **Execute** - Implement following the plan
6. **Quality Gates** - Closed-loop until all pass
7. **Implementation Scrutiny** - Multi-agent review
8. **Plan Completion** - Two-stage confirmation

**Severity Classification:**
- **P1 (Critical)**: Blocks implementation/merge
- **P2 (Important)**: Should address
- **P3 (Nice-to-Have)**: Consider

**Available Workflow Commands:**

| Command | Purpose |
|---------|---------|
| `/workflows:plan` | Create structured plans with parallel research |
| `/workflows:work` | Execute plans with quality gates |
| `/workflows:review` | Multi-agent parallel code reviews |
| `/workflows:compound` | Document learnings as knowledge |
| `/deepen-plan` | Enhance plans with research |
| `/todo` | File-based todo management |

## Commands
[All relevant commands]

## Quality Gates
[Detected validation commands]

## Development Notes
[User-preserved content]
```

## Example Output

### Django Project with Poetry

```markdown
# My Django Project

Django web application using Poetry for dependency management.

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Django** | 5.1 | `python-django` | Web framework |
| **pytest-django** | 4.7 | `python-pytest` | Testing framework |
| **gunicorn** | 21.2 | `python-gunicorn` | WSGI server |

## Package Manager

**poetry** (detected from poetry.lock)

## Commands

```bash
poetry install                  # Install dependencies
python manage.py runserver      # Start development server
pytest                          # Run tests
ruff check                      # Lint code
poetry build                    # Build package
```
```

### FastAPI Project with pip

```markdown
# My FastAPI App

FastAPI application with async support.

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **FastAPI** | 0.104 | `python-fastapi` | Web framework |
| **uvicorn** | 0.24 | `python-uvicorn` | ASGI server |

## Package Manager

**pip** (detected from requirements.txt)

## Commands

```bash
pip install -r requirements.txt   # Install dependencies
uvicorn main:app --reload         # Start development server
pytest                            # Run tests
ruff check                        # Lint code
```
```
