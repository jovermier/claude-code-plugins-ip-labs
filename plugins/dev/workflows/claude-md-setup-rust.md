# CLAUDE.md Setup Workflow - Rust

Generates `CLAUDE.md` for Rust projects (Cargo, crates, etc.).

## When to Use This Sub-Workflow

- Invoked by `claude-md-setup.md` when `Cargo.toml` is detected
- For any Rust project using Cargo

## The Workflow

### Step 1: Scan Marketplace Plugins

Discover all available plugins by reading the marketplace configuration.

### Step 2: Extract Skill Metadata

For EACH skill discovered, read its `SKILL.md` file and extract frontmatter and CLAUDE-specific sections.

### Step 3: Analyze the Workspace

```bash
# Check for Cargo.toml
cat Cargo.toml

# Check for lockfile
ls -la | grep -E "Cargo\.lock"

# Check for workspace
ls -la | grep -E "Cargo\.toml" | grep -E "workspace"

# Check for testing setup
ls -la tests/ 2>/dev/null

# Check for common Rust configs
ls -la | grep -E "(rustfmt\.toml|clippy\.toml|\.cargo/config)"
```

**Extract Technologies:**

- From `Cargo.toml`: All dependencies in `[dependencies]` and `[dev-dependencies]`
- From `Cargo.toml`: Workspace members if present
- From existing `CLAUDE.md`: Custom user content to preserve

**Package Manager Detection:**

```javascript
function detectPackageManagerRust() {
  return 'cargo'; // Rust always uses Cargo
}
```

**Version Detection (Skill-Linked):**

```javascript
function extractRustVersions(detectedTech, matchedPlugins) {
  const versioned = [];

  for (const tech of detectedTech) {
    const matchedSkill = findSkillForTech(tech, matchedPlugins);
    if (matchedSkill) {
      versioned.push({
        name: tech.name,
        displayName: tech.displayName,  // e.g., "tokio", "serde"
        displayVersion: tech.version,  // Keep semver as-is
        skill: matchedSkill.name,
        skillPlugin: matchedSkill.plugin
      });
    }
  }

  return versioned;
}
```

### Step 4: Match Technologies to Plugins

Match detected crates to marketplace plugins using keywords and descriptions.

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
    'package-manager': () => 'cargo',
    'install-command': () => 'cargo fetch',
    'test-command': () => 'cargo test',
    'dev-command': () => 'cargo run',
    'build-command': () => 'cargo build',
    'lint-command': () => 'cargo clippy',
    'format-command': () => 'cargo fmt',
    'doc-command': () => 'cargo doc',
  };

  const resolver = resolvers[variableName];
  return resolver ? resolver() : `[${variableName}]`;
}
```

### Step 6: Generate CLAUDE.md

**File Structure:**

```markdown
# [Project Name from Cargo.toml package.name]

[Project description]

## Tech Stack
[Detected technologies by category with versions]

## Package Manager
**cargo** - Rust standard package manager.

## Resolved Variables
[Template variables resolved to project-specific values]

## Critical Rules
[Extracted NEVER/MUST/ALWAYS rules from all skills]

## Marketplace Plugins
[Table of matched plugins]

### Available Skills
[Skills with descriptions from frontmatter]

## Workflows
[Core dev workflows + any from matched plugins]

## Commands
[All relevant commands]

## Quality Gates
[Detected validation commands]

## Development Notes
[User-preserved content]
```

## Example Output

```markdown
# My Rust Project

Rust application using Tokio for async runtime.

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **tokio** | 1.35 | `rust-tokio` | Async runtime |
| **serde** | 1.0 | `rust-serde` | Serialization |
| **clap** | 4.4 | `rust-clap` | CLI argument parsing |

## Package Manager

**cargo** (Rust standard)

## Resolved Variables

| Variable | Value |
|----------|-------|
| `package-manager` | `cargo` |
| `test-command` | `cargo test` |
| `dev-command` | `cargo run` |
| `build-command` | `cargo build` |
| `lint-command` | `cargo clippy` |
| `format-command` | `cargo fmt` |

## Commands

```bash
cargo fetch          # Fetch dependencies
cargo build          # Build project
cargo run            # Run application
cargo test           # Run tests
cargo clippy         # Lint code
cargo fmt            # Format code
cargo doc            # Generate documentation
cargo doc --open     # Generate and open documentation
```
```
