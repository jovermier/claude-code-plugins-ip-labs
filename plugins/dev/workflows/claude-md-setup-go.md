# CLAUDE.md Setup Workflow - Go

Generates `CLAUDE.md` for Go projects (Go modules, etc.).

## When to Use This Sub-Workflow

- Invoked by `claude-md-setup.md` when `go.mod` is detected
- For any Go project using Go modules

## The Workflow

### Step 1: Scan Marketplace Plugins

Discover all available plugins by reading the marketplace configuration.

### Step 2: Extract Skill Metadata

For EACH skill discovered, read its `SKILL.md` file and extract frontmatter and CLAUDE-specific sections.

### Step 3: Analyze the Workspace

```bash
# Check for go.mod
cat go.mod

# Check for go.sum
ls -la | grep -E "go\.sum"

# Check for main package
ls -la cmd/ 2>/dev/null || ls -la main.go 2>/dev/null

# Check for testing setup
ls -la *_test.go 2>/dev/null || ls -la tests/ 2>/dev/null
```

**Extract Technologies:**

- From `go.mod`: Go version and all dependencies
- From directory structure: Project layout (cmd/, pkg/, internal/, etc.)
- From existing `CLAUDE.md`: Custom user content to preserve

**Package Manager Detection:**

```javascript
function detectPackageManagerGo() {
  return 'go'; // Go always uses go modules
}
```

**Version Detection:**

```javascript
function extractGoVersions(detectedTech, matchedPlugins) {
  const versioned = [];

  // Extract Go version from go.mod
  const goVersion = parseGoVersion(readFile('go.mod'));

  for (const tech of detectedTech) {
    const matchedSkill = findSkillForTech(tech, matchedPlugins);
    if (matchedSkill) {
      versioned.push({
        name: tech.name,
        displayName: tech.displayName,  // e.g., "gin", "echo"
        displayVersion: tech.version || 'latest',
        skill: matchedSkill.name,
        skillPlugin: matchedSkill.plugin
      });
    }
  }

  return versioned;
}
```

### Step 4: Match Technologies to Plugins

Match detected dependencies to marketplace plugins using keywords and descriptions.

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
    'package-manager': () => 'go',
    'install-command': () => 'go mod download',
    'test-command': () => 'go test ./...',
    'dev-command': () => detectGoDevCommand(project),
    'build-command': () => detectGoBuildCommand(project),
    'lint-command': () => 'golangci-lint run',
    'format-command': () => 'gofmt -w .',
    'tidy-command': () => 'go mod tidy',
  };

  const resolver = resolvers[variableName];
  return resolver ? resolver() : `[${variableName}]`;
}

function detectGoDevCommand(project) {
  // Check for common patterns
  if (project.hasFile('cmd/server/main.go')) return 'go run cmd/server/main.go';
  if (project.hasFile('main.go')) return 'go run main.go';
  if (project.hasFile('cmd/api/main.go')) return 'go run cmd/api/main.go';
  return 'go run .'; // Default
}

function detectGoBuildCommand(project) {
  // Check for common patterns
  if (project.hasFile('cmd/server/main.go')) return 'go build -o bin/server cmd/server/main.go';
  if (project.hasFile('main.go')) return 'go build -o bin/app main.go';
  return 'go build'; // Default
}
```

### Step 6: Generate CLAUDE.md

**File Structure:**

```markdown
# [Project Name from go.mod or directory]

[Project description]

## Tech Stack
[Detected technologies by category with versions]

## Package Manager
**go** - Go modules package manager.

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
| New features | TDD workflow | "Add new handler" |
| Bug fixes | Bug-fix workflow | "Fix panic in goroutine" |
| Complex tasks | Full 7-step meta-workflow | "Add new service with tests" |

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

```markdown
# My Go Service

Go web service using Gin framework.

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Go** | 1.21 | `go-lang` | Language version |
| **gin-gonic** | 1.9 | `go-gin` | Web framework |
| **gorm** | 1.25 | `go-gorm` | ORM |

## Package Manager

**go** (Go modules)

## Resolved Variables

| Variable | Value |
|----------|-------|
| `package-manager` | `go` |
| `test-command` | `go test ./...` |
| `dev-command` | `go run cmd/server/main.go` |
| `build-command` | `go build -o bin/server cmd/server/main.go` |
| `lint-command` | `golangci-lint run` |
| `tidy-command` | `go mod tidy` |

## Commands

```bash
go mod download       # Download dependencies
go mod tidy           # Clean up dependencies
go run cmd/server/main.go   # Run application
go test ./...         # Run tests
go build              # Build project
golangci-lint run     # Lint code
gofmt -w .            # Format code
```
```
