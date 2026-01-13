# CLAUDE.md Setup Workflow - PHP

Generates `CLAUDE.md` for PHP projects (Composer, Laravel, Symfony, etc.).

## When to Use This Sub-Workflow

- Invoked by `claude-md-setup.md` when `composer.json` is detected
- For any PHP project using Composer
- For Laravel, Symfony, or other PHP frameworks

## The Workflow

### Step 1: Scan Marketplace Plugins

Discover all available plugins by reading the marketplace configuration.

### Step 2: Extract Skill Metadata

For EACH skill discovered, read its `SKILL.md` file and extract frontmatter and CLAUDE-specific sections.

### Step 3: Analyze the Workspace

```bash
# Check for composer.json
cat composer.json

# Check for lockfile
ls -la | grep -E "composer\.lock"

# Detect framework
ls -la | grep -E "(artisan|symfony|bin/console)"

# Check for testing setup
ls -la tests/ 2>/dev/null

# Check for common PHP configs
ls -la | grep -E "(phpunit\.xml|\.php-cs-fixer|phpstan)"
```

**Extract Technologies:**

- From `composer.json`: All `require` and `require-dev` packages with versions
- From directories: Framework detection (Laravel: artisan, Symfony: bin/console)
- From existing `CLAUDE.md`: Custom user content to preserve

**Package Manager Detection:**

```javascript
function detectPackageManagerPHP() {
  return 'composer'; // PHP always uses Composer
}
```

**Version Detection (Skill-Linked):**

```javascript
function extractPHPVersions(detectedTech, matchedPlugins) {
  const versioned = [];

  for (const tech of detectedTech) {
    const matchedSkill = findSkillForTech(tech, matchedPlugins);
    if (matchedSkill) {
      versioned.push({
        name: tech.name,
        displayName: tech.displayName,  // e.g., "laravel/framework", "symfony/console"
        displayVersion: tech.version,  // Keep composer version constraint
        skill: matchedSkill.name,
        skillPlugin: matchedSkill.plugin
      });
    }
  }

  return versioned;
}
```

### Step 4: Match Technologies to Plugins

Match detected packages to marketplace plugins using keywords and descriptions.

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
  const framework = detectFramework(project);

  const resolvers = {
    'package-manager': () => 'composer',
    'install-command': () => 'composer install',
    'test-command': () => framework === 'laravel' ? 'php artisan test' : 'vendor/bin/phpunit',
    'dev-command': () => detectPHPDevCommand(project, framework),
    'build-command': () => 'composer build',
    'lint-command': () => 'vendor/bin/phpcs' || 'phpstan analyse',
    'format-command': () => 'vendor/bin/php-cs-fixer fix',
  };

  const resolver = resolvers[variableName];
  return resolver ? resolver() : `[${variableName}]`;
}

function detectFramework(project) {
  if (project.hasFile('artisan')) return 'laravel';
  if (project.hasFile('bin/console')) return 'symfony';
  return null;
}

function detectPHPDevCommand(project, framework) {
  if (framework === 'laravel') return 'php artisan serve';
  if (framework === 'symfony') return 'symfony server:start';
  return 'php -S localhost:8000'; // Built-in server
}
```

### Step 6: Generate CLAUDE.md

**File Structure:**

```markdown
# [Project Name from composer.json]

[Project description]

## Tech Stack
[Detected technologies by category with versions]

## Package Manager
**composer** - PHP package manager.

## Resolved Variables
[Template variables resolved to project-specific values]

## Critical Rules
[Extracted NEVER/MUST/ALWAYS rules from all skills]

## Marketplace Plugins
[Table of matched plugins]

### Available Skills
[Skills with descriptions from frontmatter]

## Workflows

### Meta-Workflow (Default)

The **meta-workflow** is the default workflow that auto-routes all requests based on task complexity. It is enforced via the `meta-workflow-enforcer` hook from the dev plugin.

**Task Type Detection:**

| Request Type | Strategy | Example |
|--------------|----------|---------|
| Information queries (ending with `?`) | Direct response | "What does this function do?" |
| Simple changes ("fix typo", "change word") | Direct execution + quality gates | "Fix typo in heading" |
| New features | TDD workflow | "Add new controller" |
| Bug fixes | Bug-fix workflow | "Fix database query error" |
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

### Laravel Project

```markdown
# My Laravel App

Laravel web application.

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **PHP** | 8.2 | `php-lang` | Language version |
| **Laravel** | 10.3 | `php-laravel` | Web framework |
| **PHPUnit** | 10.0 | `php-phpunit` | Testing framework |

## Package Manager

**composer** (detected from composer.json)

## Resolved Variables

| Variable | Value |
|----------|-------|
| `package-manager` | `composer` |
| `install-command` | `composer install` |
| `test-command` | `php artisan test` |
| `dev-command` | `php artisan serve` |
| `lint-command` | `vendor/bin/phpcs` |

## Commands

```bash
composer install          # Install dependencies
php artisan serve         # Start development server
php artisan test          # Run tests
php artisan migrate       # Run database migrations
php artisan tinker        # Open REPL
vendor/bin/phpcs          # Lint code
vendor/bin/php-cs-fixer fix  # Format code
```
```
