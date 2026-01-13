# CLAUDE.md Setup Workflow - Generic

Generates `CLAUDE.md` for projects without a detected language-specific ecosystem.

## When to Use This Sub-Workflow

- Invoked by `claude-md-setup.md` when no specific language is detected
- For projects using uncommon build systems
- For polyglot projects with multiple languages
- As a fallback when project type cannot be determined

## The Workflow

### Step 1: Scan Marketplace Plugins

Discover all available plugins by reading the marketplace configuration.

### Step 2: Extract Skill Metadata

For EACH skill discovered, read its `SKILL.md` file and extract frontmatter and CLAUDE-specific sections.

### Step 3: Analyze the Workspace

```bash
# Check for any project files
ls -la

# Look for common patterns
ls -la | grep -E "(Makefile|justfile|Taskfile|CMakeLists\.txt|meson\.build)"

# Check for source directories
ls -la src/ 2>/dev/null || ls -la lib/ 2>/dev/null

# Check for documentation
ls -la README.md 2>/dev/null || ls -la CONTRIBUTING.md 2>/dev/null
```

**Extract Information:**

- From existing `CLAUDE.md`: Custom user content to preserve
- From `README.md`: Project description and setup instructions
- From directory structure: General project organization

### Step 4: Generate Minimal CLAUDE.md

Since the project type is unknown, generate a minimal CLAUDE.md with:

```markdown
# [Project Name from directory name]

[Description from README.md or placeholder]

## Project Structure

[Detected directory structure]

## Documentation

- [README.md](README.md) - Project overview and setup

## Available Workflows

### Meta-Workflow (Default)

The **meta-workflow** is the default workflow that auto-routes all requests based on task complexity. It is enforced via the `meta-workflow-enforcer` hook from the dev plugin.

**Task Type Detection:**

| Request Type | Strategy | Example |
|--------------|----------|---------|
| Information queries (ending with `?`) | Direct response | "What does this function do?" |
| Simple changes ("fix typo", "change word") | Direct execution + quality gates | "Fix typo in heading" |
| New features | TDD workflow | "Add new feature" |
| Bug fixes | Bug-fix workflow | "Fix bug" |
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

Check for additional workflows in `.claude/workflows/` and `~/.claude/workflows/`.

## Development Notes

Add your project-specific notes here.
```

## Notes

This generic workflow provides a basic CLAUDE.md template. Users should manually edit to add:
- Project-specific commands
- Build instructions
- Testing procedures
- Development workflow details

For better integration, consider adding a standard project file (package.json, Cargo.toml, etc.) or create a custom `.claude/workflows/` setup.
