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

Each sub-workflow generates an appropriate CLAUDE.md for its language:

```markdown
# [Project Name]

[Project description]

## Tech Stack
[Skill-linked version table - only technologies with relevant skills]

## Package Manager
[detected-package-manager] - All commands use this package manager.

## Resolved Variables
[Template variables resolved to project-specific values]

## Critical Rules
[Extracted NEVER/MUST/ALWAYS rules from all skills]

## Marketplace Plugins
[Matched plugins table]

### Available Skills
[Skills with descriptions from frontmatter]

### Skill-Specific Guidance
[Extracted CLAUDE-specific sections from skills]

## Workflows
[Available workflows]

## Commands
[All relevant commands]

## Quality Gates
[Detected validation commands]

## Version Notes
[Breaking changes and new features by version]

## Development Notes
[User-preserved content]
```

## Example Output by Language

### JavaScript/TypeScript Project

```markdown
## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Next.js** | 16.1 | `latest-nextjs` | App Router, Server Components |
| **React** | 19.2 | `latest-react` | Compiler, Actions, new hooks |

## Package Manager

**pnpm** (detected from pnpm-lock.yaml)

## Resolved Variables

| Variable | Value | Source |
|----------|-------|--------|
| `package-manager` | `pnpm` | Detected from pnpm-lock.yaml |
| `test-script` | `test` | Found in package.json scripts |
| `dev-script` | `dev` | Found in package.json scripts |

## Commands

```bash
pnpm install         # Install dependencies
pnpm dev             # Start development server
pnpm test            # Run tests
pnpm build           # Build for production
pnpm lint            # Lint code
```
```

### Python Project

```markdown
## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Django** | 5.1 | `python-django` | Web framework |
| **pytest** | 8.0 | `python-pytest` | Testing framework |

## Package Manager

**poetry** (detected from pyproject.toml)

## Resolved Variables

| Variable | Value | Source |
|----------|-------|--------|
| `package-manager` | `poetry` | Detected from pyproject.toml |
| `test-command` | `pytest` | Python standard |
| `dev-command` | `python manage.py runserver` | Django standard |

## Commands

```bash
poetry install       # Install dependencies
poetry run pytest    # Run tests
python manage.py runserver  # Start development server
poetry build         # Build package
ruff check           # Lint code
```
```

### Rust Project

```markdown
## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Rust** | 1.75 | `rust-lang` | Language version |
| **tokio** | 1.35 | `rust-tokio` | Async runtime |

## Package Manager

**cargo** (Rust standard)

## Resolved Variables

| Variable | Value | Source |
|----------|-------|--------|
| `package-manager` | `cargo` | Rust standard |
| `test-command` | `cargo test` | Cargo standard |
| `dev-command` | `cargo run` | Cargo standard |

## Commands

```bash
cargo fetch          # Fetch dependencies
cargo test           # Run tests
cargo run            # Run application
cargo build          # Build for release
cargo clippy         # Lint code
```
```

## Notes

- **Skill-linked versioning** - Only technologies with matched skills are versioned in CLAUDE.md
- **Major.minor precision** - Versions show major.minor only (e.g., `16.1`, not `16.1.1`)
- **Strong tech-skill linkage** - Tech stack table explicitly links technologies to their relevant skills
- **Language-aware** - Each sub-workflow understands its ecosystem's conventions
- **Plugin discovery is dynamic** - No technologies are hardcoded
- **Matching uses keywords** - Plugins matched via `plugin.json` keywords and descriptions
- **Preserves user content** - Custom sections maintained during updates
- **Works with any marketplace** - Generic plugin discovery pattern

See the full workflow documentation in `plugins/dev/workflows/claude-md-setup.md`.
