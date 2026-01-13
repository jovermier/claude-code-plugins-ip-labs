# CLAUDE.md Setup Workflow - Ruby

Generates `CLAUDE.md` for Ruby projects (Bundler, Rails, Sinatra, etc.).

## When to Use This Sub-Workflow

- Invoked by `claude-md-setup.md` when `Gemfile` is detected
- For any Ruby project using Bundler
- For Rails, Sinatra, or other Ruby frameworks

## The Workflow

### Step 1: Scan Marketplace Plugins

Discover all available plugins by reading the marketplace configuration.

### Step 2: Extract Skill Metadata

For EACH skill discovered, read its `SKILL.md` file and extract frontmatter and CLAUDE-specific sections.

### Step 3: Analyze the Workspace

```bash
# Check for Gemfile
cat Gemfile

# Check for lockfile
ls -la | grep -E "Gemfile\.lock"

# Detect framework
ls -la | grep -E "(config/application\.rb|config\.ru|Rakefile)"

# Check for testing setup
ls -la spec/ 2>/dev/null || ls -la test/ 2>/dev/null

# Check for common Ruby configs
ls -la | grep -E "(rspec|rubocop|\.ruby-version)"
```

**Extract Technologies:**

- From `Gemfile`: All gems with version constraints
- From `Gemfile.lock`: Actual resolved versions
- From directories: Framework detection (Rails: config/application.rb, Sinatra: config.ru)
- From existing `CLAUDE.md`: Custom user content to preserve

**Package Manager Detection:**

```javascript
function detectPackageManagerRuby() {
  return 'bundler'; // Ruby always uses Bundler
}
```

**Version Detection (Skill-Linked):**

```javascript
function extractRubyVersions(detectedTech, matchedPlugins) {
  const versioned = [];

  for (const tech of detectedTech) {
    const matchedSkill = findSkillForTech(tech, matchedPlugins);
    if (matchedSkill) {
      versioned.push({
        name: tech.name,
        displayName: tech.displayName,  // e.g., "rails", "sinatra", "rspec"
        displayVersion: tech.version,  // Keep gem version as-is
        skill: matchedSkill.name,
        skillPlugin: matchedSkill.plugin
      });
    }
  }

  return versioned;
}
```

### Step 4: Match Technologies to Plugins

Match detected gems to marketplace plugins using keywords and descriptions.

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
  const framework = detectRubyFramework(project);

  const resolvers = {
    'package-manager': () => 'bundle',
    'install-command': () => 'bundle install',
    'test-command': () => framework === 'rails' ? 'bin/rails test' : 'rspec',
    'dev-command': () => detectRubyDevCommand(project, framework),
    'build-command': () => 'bundle exec rake build',
    'lint-command': () => 'rubocop',
    'format-command': () => 'rubocop -a',
  };

  const resolver = resolvers[variableName];
  return resolver ? resolver() : `[${variableName}]`;
}

function detectRubyFramework(project) {
  if (project.hasFile('config/application.rb') || project.hasFile('bin/rails')) return 'rails';
  if (project.hasFile('config.ru')) return 'sinatra';
  if (project.hasFile('spec/spec_helper.rb')) return 'rspec';
  return null;
}

function detectRubyDevCommand(project, framework) {
  if (framework === 'rails') return 'bin/rails server';
  if (framework === 'sinatra') return 'bundle exec rackup';
  return 'bundle exec ruby'; // Generic
}
```

### Step 6: Generate CLAUDE.md

**File Structure:**

```markdown
# [Project Name from Gemfile or directory]

[Project description]

## Tech Stack
[Detected technologies by category with versions]

## Package Manager
**bundle** (Bundler) - Ruby dependency manager.

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
| Information queries (ending with `?`) | Direct response | "What does this method do?" |
| Simple changes ("fix typo", "change word") | Direct execution + quality gates | "Fix typo in heading" |
| New features | TDD workflow | "Add new model" |
| Bug fixes | Bug-fix workflow | "Fix N+1 query" |
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

### Rails Project

```markdown
# My Rails App

Ruby on Rails web application.

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Ruby** | 3.2 | `ruby-lang` | Language version |
| **Rails** | 7.1 | `ruby-rails` | Web framework |
| **RSpec** | 3.12 | `ruby-rspec` | Testing framework |

## Package Manager

**bundle** (Bundler, detected from Gemfile)

## Resolved Variables

| Variable | Value |
|----------|-------|
| `package-manager` | `bundle` |
| `install-command` | `bundle install` |
| `test-command` | `bin/rails test` |
| `dev-command` | `bin/rails server` |
| `lint-command` | `rubocop` |

## Commands

```bash
bundle install           # Install dependencies
bin/rails server         # Start development server
bin/rails test           # Run tests
bin/rails db:migrate     # Run database migrations
bin/rails console        # Open Rails console
rubocop                  # Lint code
rubocop -a               # Auto-fix lint issues
```
```
