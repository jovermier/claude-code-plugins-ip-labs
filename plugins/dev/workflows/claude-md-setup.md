# CLAUDE.md Setup Workflow (Main Router)

Detects project type and routes to the appropriate language-specific sub-workflow for generating `CLAUDE.md`.

## When to Use This Workflow

- Invoked by `/project:setup` command
- When starting a new project
- After adding new technologies to the project
- When onboarding to an existing project

## Architecture

```
claude-md-setup.md (Router)
├── Detects project type
├── Routes to sub-workflow:
    ├── claude-md-setup-javascript.md  # Node.js, TypeScript, Next.js, React, etc.
    ├── claude-md-setup-python.md      # Python, Django, FastAPI, etc.
    ├── claude-md-setup-rust.md        # Rust, Cargo
    ├── claude-md-setup-go.md          # Go modules
    ├── claude-md-setup-php.md          # PHP, Composer
    ├── claude-md-setup-ruby.md        # Ruby, Bundler
    └── claude-md-setup-generic.md     # Fallback for unknown types
```

## The Workflow

### Step 1: Detect Project Type

Scan the project directory to identify the language/ecosystem:

```bash
# Detect project type by checking common files
ls -la | grep -E "(package\.json|pyproject\.toml|setup\.py|requirements\.txt|Cargo\.toml|go\.mod|composer\.json|Gemfile|pom\.xml|build\.gradle)"
```

**Project Type Detection Logic:**

```javascript
function detectProjectType() {
  const files = listFiles('.');

  // JavaScript / TypeScript
  if (files.includes('package.json')) {
    return {
      type: 'javascript',
      subWorkflow: 'claude-md-setup-javascript.md',
      manager: detectPackageManagerJS()
    };
  }

  // Python
  if (files.includes('pyproject.toml')) {
    return { type: 'python', subWorkflow: 'claude-md-setup-python.md', manager: 'poetry' };
  }
  if (files.includes('setup.py') || files.includes('requirements.txt')) {
    return { type: 'python', subWorkflow: 'claude-md-setup-python.md', manager: 'pip' };
  }

  // Rust
  if (files.includes('Cargo.toml')) {
    return { type: 'rust', subWorkflow: 'claude-md-setup-rust.md', manager: 'cargo' };
  }

  // Go
  if (files.includes('go.mod')) {
    return { type: 'go', subWorkflow: 'claude-md-setup-go.md', manager: 'go' };
  }

  // PHP
  if (files.includes('composer.json')) {
    return { type: 'php', subWorkflow: 'claude-md-setup-php.md', manager: 'composer' };
  }

  // Ruby
  if (files.includes('Gemfile')) {
    return { type: 'ruby', subWorkflow: 'claude-md-setup-ruby.md', manager: 'bundler' };
  }

  // Java
  if (files.includes('pom.xml')) {
    return { type: 'java', subWorkflow: 'claude-md-setup-java.md', manager: 'maven' };
  }
  if (files.includes('build.gradle') || files.includes('build.gradle.kts')) {
    return { type: 'java', subWorkflow: 'claude-md-setup-java.md', manager: 'gradle' };
  }

  // Fallback: Generic/Unknown
  return { type: 'generic', subWorkflow: 'claude-md-setup-generic.md', manager: null };
}

function detectPackageManagerJS() {
  const lockfiles = listFiles('.').filter(f =>
    f.match(/(pnpm-lock|yarn\.lock|package-lock|bun\.lockb)/)
  );

  if (lockfiles.includes('pnpm-lock.yaml')) return 'pnpm';
  if (lockfiles.includes('bun.lockb')) return 'bun';
  if (lockfiles.includes('yarn.lock')) return 'yarn';
  return 'npm'; // default
}
```

### Step 2: Route to Sub-Workflow

Invoke the appropriate language-specific sub-workflow:

```
[Detected Project Type] → [Sub-Workflow]

┌─────────────────┬─────────────────────────────────────┐
│ Project Type    │ Sub-Workflow                        │
├─────────────────┼─────────────────────────────────────┤
│ JavaScript      │ claude-md-setup-javascript.md       │
│ Python          │ claude-md-setup-python.md           │
│ Rust            │ claude-md-setup-rust.md             │
│ Go              │ claude-md-setup-go.md               │
│ PHP             │ claude-md-setup-php.md              │
│ Ruby            │ claude-md-setup-ruby.md             │
│ Java (Maven)    │ claude-md-setup-java.md             │
│ Java (Gradle)   │ claude-md-setup-java.md             │
│ Unknown/Generic │ claude-md-setup-generic.md          │
└─────────────────┴─────────────────────────────────────┘
```

Each sub-workflow is responsible for:
1. Extracting language-specific dependencies and versions
2. Detecting language-specific package managers and commands
3. Matching to language-specific marketplace plugins
4. Generating CLAUDE.md with appropriate structure

### Step 3: Generate CLAUDE.md

The sub-workflow returns the generated CLAUDE.md content, which this workflow writes to the project root.

**Preservation Strategy:**

If `CLAUDE.md` already exists, preserve these sections:
- Custom project description (between title and first `##`)
- `## Critical Rules` - User may have added project-specific rules
- `## Development Notes` - User's custom notes
- Any custom sections not in standard template

## Sub-Workflow Reference

Each sub-workflow follows this contract:

**Input:**
```javascript
{
  projectType: 'javascript' | 'python' | 'rust' | 'go' | 'php' | 'ruby' | 'java' | 'generic',
  packageManager: string | null,
  projectRoot: string,
  existingClaudeMd: string | null
}
```

**Output:**
```javascript
{
  content: string,  // Full CLAUDE.md content
  sections: {
    description: string,
    criticalRules: string[],
    techStack: TechStackEntry[],
    resolvedVariables: Record<string, string>,
    workflows: WorkflowReference[],
    commands: CommandReference[]
  }
}
```

See individual sub-workflow files for language-specific implementation details.
