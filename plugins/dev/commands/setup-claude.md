# /project:setup

Analyzes the current project and generates or updates the `CLAUDE.md` file with comprehensive context from installed marketplace plugins. Works with **any project type** (JavaScript, Python, Rust, Go, PHP, Ruby, Java, etc.).

## What It Does

This command follows the **CLAUDE.md Setup Workflow** which:

1. **Detects project type** - Scans for language-specific files (package.json, Cargo.toml, go.mod, etc.)
2. **Routes to sub-workflow** - Invokes the appropriate language-specific sub-workflow
3. **Extracts dependencies** - Reads language-specific dependency files
4. **Detects package manager** - Identifies the package manager for the detected language
5. **Matches technologies to plugins** - Uses plugin keywords and descriptions
6. **Extracts skill metadata** - Reads SKILL.md frontmatter for descriptions and updates
7. **Extracts critical rules** - Finds NEVER/MUST/ALWAYS patterns from skill documentation
8. **Resolves template variables** - Resolves language-specific variables (e.g., `[package-manager]`)
9. **Generates skill-linked tech stack** - Only versions technologies with relevant skills
10. **Generates comprehensive CLAUDE.md** - Creates or updates with all extracted context

## Supported Project Types

| Project Type | Detected Files |
|--------------|----------------|
| **JavaScript/TypeScript** | `package.json` |
| **Python (Poetry)** | `pyproject.toml` |
| **Python (pip)** | `setup.py`, `requirements.txt` |
| **Rust** | `Cargo.toml` |
| **Go** | `go.mod` |
| **PHP** | `composer.json` |
| **Ruby** | `Gemfile` |
| **Java (Maven)** | `pom.xml` |
| **Java (Gradle)** | `build.gradle`, `build.gradle.kts` |
| **Unknown/Generic** | None of the above |

## When to Use

- **Starting a new project** - Generate initial CLAUDE.md with all relevant context
- **Adding new technologies** - Update CLAUDE.md after adding dependencies
- **Onboarding** - Help Claude understand the project structure quickly
- **Project evolution** - Keep CLAUDE.md in sync as the project grows

## Usage

```bash
/project:setup
```

## Generated CLAUDE.md Structure

Each sub-workflow generates an appropriate CLAUDE.md for its language with language-appropriate sections. Common sections include:

```markdown
# [Project Name]

[Project description]

## Tech Stack
[Skill-linked version table - only technologies with relevant skills]

## Package Manager
[detected-package-manager] - Additional context about usage

## Runtime Environment
| Platform | Version |
|----------|---------|
| **[Language Runtime]** | [version] |
| **[package-manager]** | [version] |

[Section varies by language: Node.js/npm, Python/poetry, Rust/cargo, Go/go mod, etc.]

## Critical Rules
[Extracted NEVER/MUST/ALWAYS rules from all skills]

## Gotchas
[Common pitfalls and edge cases from skills]

## Available Skills (Auto-Activated)
Skills activate automatically based on context. You don't need to invoke them manually.

| Skill | Trigger | Description |
|-------|---------|-------------|
| `skill-name` | [When it activates] | [What it helps with] |

## Available Agents (Manual Invocation)
Use `/agents` to list agents or invoke directly:

| Agent | Purpose |
|-------|---------|
| `agent-name` | [What it does] |

[Include if the project has local agents defined]

## Commands
[Commands grouped by category: Development, Testing, Quality Checks, etc.]

## Project Structure
[ASCII tree showing key directories]

## Documentation
| Need | Reference |
|------|-----------|
| **Start here** | [AI_DOCUMENTATION_INDEX.md](AI_DOCUMENTATION_INDEX.md) |

## Workflows
[Core development workflows with step-by-step instructions]

## Quality Gates
Before committing, run:
[Validation commands]

## Workspaces
[If monorepo: List of workspace directories with descriptions]
```

**Note:** No footer with date or version numbers - git history already tracks when the file was modified.

## Language-Specific Workflows

Each language has its own sub-workflow with detailed examples and language-specific guidance:

| Project Type | Sub-Workflow |
|--------------|--------------|
| **JavaScript/TypeScript** | `claude-md-setup-javascript.md` |
| **Python** | `claude-md-setup-python.md` |
| **Rust** | `claude-md-setup-rust.md` |
| **Go** | `claude-md-setup-go.md` |
| **PHP** | `claude-md-setup-php.md` |
| **Ruby** | `claude-md-setup-ruby.md` |
| **Java** | `claude-md-setup-java.md` |
| **Generic** | `claude-md-setup-generic.md` |

See the full router workflow in `plugins/dev/workflows/claude-md-setup.md`.
