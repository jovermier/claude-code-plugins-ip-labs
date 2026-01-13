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

Check for workflows in `.claude/workflows/` and `~/.claude/workflows/`.

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
