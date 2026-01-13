# CLAUDE.md Setup Workflow - JavaScript/TypeScript

Generates `CLAUDE.md` for JavaScript/TypeScript projects (Node.js, Next.js, React, Vue, etc.).

**Input from Router:** Receives pre-built `marketplaceRegistry` and project detection results. DO NOT re-scan plugins.

## The Workflow

### Step 1: Analyze Workspace

```bash
cat package.json
ls -la | grep -E "\.config\.|tsconfig\.json"
cat CLAUDE.md 2>/dev/null || echo "No existing CLAUDE.md"
```

Extract dependencies/devDependencies with versions, framework names from configs, testing frameworks.

### Step 2: Match Technologies to Skills

For each detected technology, find matching plugins and skills from the `marketplaceRegistry`:

**Matching Process:**

1. For each dependency in `package.json` (both `dependencies` and `devDependencies`):
   - Extract the package name and version
   - Check if the package name matches any plugin keywords or descriptions

2. For each matching plugin:
   - Get all skills from that plugin
   - Check if the skill name relates to the technology (substring match, case-insensitive)

3. Build a matched skills list with:
   - Technology name and version
   - Matching skill name and path
   - Plugin name and description

4. Always include skills from `dev` and `coder` plugins regardless of dependencies

**Note:** If dependencies use catalog entries (e.g., `react: catalog:`), read the version from `pnpm-workspace.yaml` catalog if available.

### Step 3: Extract Skill Content

For each matched skill, read the SKILL.md file (use path from registry) and extract:

**From SKILL.md frontmatter** (between the `---` markers):
- `name`: The skill identifier
- `description`: When this skill activates
- `updated`: Last modification date

**From SKILL.md body content, extract these sections:**
- `## CLAUDE\.md Requirements` or `## For CLAUDE\.md` or `## CLAUDE Context`
- `## Critical Rules` - Look for NEVER/MUST/ALWAYS patterns
- `## Gotchas` - Common pitfalls and edge cases
- `## Breaking Changes` - Version-specific breaking changes
- `## Version Notes` - Version-specific context and features

### Step 4: Detect Package Manager and Runtime

```bash
# Detect package manager from lockfiles
ls -la | grep -E "(pnpm-lock.yaml|bun.lockb|yarn.lock|package-lock.json)"

# Get runtime versions (if available)
node --version 2>/dev/null
pnpm --version 2>/dev/null
npm --version 2>/dev/null
yarn --version 2>/dev/null
bun --version 2>/dev/null
```

| Lockfile | Package Manager |
|----------|-----------------|
| `pnpm-lock.yaml` | pnpm |
| `bun.lockb` | bun |
| `yarn.lock` | yarn |
| `package-lock.json` | npm |

### Step 5: Extract Commands from package.json

From `package.json` scripts, categorize commands by purpose:

**Development:**
- `dev`, `start`, `serve` - Start development server

**Code Generation:**
- `codegen`, `generate` - Generate types or code

**Quality Checks:**
- `typecheck`, `check:types`, `check` - TypeScript validation
- `lint`, `eslint` - Linting
- `format`, `prettier` - Code formatting

**Testing:**
- `test`, `vitest`, `jest` - Unit tests
- `test:e2e`, `playwright`, `e2e` - End-to-end tests

**Build:**
- `build`, `compile` - Production build

For each script found, record the command name and a brief description of what it does.

### Step 6: Generate CLAUDE.md

**File Structure:**

```markdown
# [Project Name]

[Project description - 1-2 sentences]

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Next.js** | 16.1 | `latest-nextjs` | App Router, Server Components, Turbopack |
| **React** | 19.2 | `latest-react` | React Compiler, Actions, new hooks |
| **TypeScript** | 5.9 | - | Type safety across monorepo |

**Note:** Only technologies with relevant skills are shown. See `package.json` for full dependencies.

## Package Manager

**[package-manager]** (detected from `[lockfile-name]`) - [Optional: Additional context like "Required for all commands"]

## Runtime Environment

| Platform | Version |
|----------|---------|
| **Node.js** | [version from `node --version`] |
| **[package-manager]** | [version from package-manager --version] |

[Include this section if runtime versions are available]

## Critical Rules

[Extracted NEVER/MUST/ALWAYS rules from all matched skills - preserve existing rules if CLAUDE.md exists]

## Gotchas

[Common pitfalls from skills - preserve existing if CLAUDE.md exists]

## Available Skills (Auto-Activated)

Skills activate automatically based on context. You don't need to invoke them manually.

| Skill | Trigger | Description |
|-------|---------|-------------|
| `skill-name` | [When it activates] | [What it helps with] |

[Table format with: Skill name, Trigger conditions, Description]

## Available Agents (Manual Invocation)

Use `/agents` to list agents or invoke directly:

| Agent | Purpose |
|-------|---------|
| `agent-name` | [What it does] |

[Include if the project has local agents defined]

## Commands

### Development

```bash
[package-manager] dev              # Start development server
```

### Code Generation

```bash
[package-manager] codegen          # Generate types
```

### Quality Checks

```bash
[package-manager] check            # Run typecheck + lint
[package-manager] typecheck        # TypeScript validation
[package-manager] lint             # ESLint check
[package-manager] lint:fix         # ESLint with auto-fix
[package-manager] format           # Prettier format
```

### Testing

```bash
[package-manager] test             # Run unit tests
[package-manager] test:e2e         # Run E2E tests
```

[Group commands logically by purpose. Use code blocks with actual commands.]

## Project Structure

```
[Project tree showing key directories]
```

[Optional: ASCII tree structure of important directories]

## Documentation

| Need | Reference |
|------|-----------|
| **Start here** | [AI_DOCUMENTATION_INDEX.md](AI_DOCUMENTATION_INDEX.md) |
| **[Topic 1]** | [path/to/doc.md](path/to/doc.md) |

[Markdown link format for clickable references]

## Workflows

### [Workflow Name 1]

1. Step one
2. Step two
3. Step three

[Core development workflows relevant to the project]

## Quality Gates

Before committing, run:

```bash
[package-manager] check            # TypeScript + ESLint
[package-manager] test             # Unit tests
```

[Detected validation commands from package.json scripts]

## Workspaces

[If monorepo detected (pnpm-workspace.yaml, workspaces field, or turbo):]

- **[workspace-name]**: [Brief description]
- **[workspace-name]**: [Brief description]

[List all workspace directories with their purposes]
```

**Do NOT include arbitrary version numbers or "Last Updated" dates.** Git history already tracks when the file was modified. Only include a version if it comes from a meaningful source (git tag, workflow version, etc.).

**If CLAUDE.md exists, preserve:**
- Custom project description (between title and first `##`)
- `## Critical Rules`
- `## Gotchas` (or similar custom sections)
- Any custom sections not in standard template

**Update these sections completely:**
- Tech Stack, Package Manager, Runtime Environment
- Available Skills, Available Agents
- Commands, Documentation, Workflows, Quality Gates, Workspaces

### Step 7: Validate

1. File exists in project root
2. Valid markdown structure
3. All skill/workflow references exist
4. Detected tech matches dependencies
5. Skills have descriptions from frontmatter

---

## Example Output

For a Next.js project using pnpm, the generated CLAUDE.md might look like:

```markdown
# My Project

Full-stack TypeScript web application with Next.js 16 and React 19.

## Tech Stack

| Technology | Version | Skill | Purpose |
|------------|---------|-------|---------|
| **Next.js** | 16.1 | `latest-nextjs` | App Router, Server Components, Turbopack |
| **React** | 19.2 | `latest-react` | React Compiler, Actions, new hooks |
| **TypeScript** | 5.9 | - | Type safety across project |
| **Tailwind CSS** | 4.1 | - | Styling with CSS modules |
| **Vitest** | 4.0 | `testing-infrastructure` | Unit testing |

**Note:** Only technologies with relevant skills are shown. See `package.json` for full dependencies.

## Package Manager

**pnpm** (detected from pnpm-lock.yaml) - Required for all commands. Do not use npm or npx.

## Runtime Environment

| Platform | Version |
|----------|---------|
| **Node.js** | 24.12.0 |
| **pnpm** | 10.27.0 |

## Critical Rules

- **NEVER** edit files in `src/generated/` - These are auto-generated by codegen
- **MUST** run `pnpm codegen` after GraphQL changes - Backend must be running first
- **ALWAYS** use pnpm - No npx commands

## Gotchas

- Codegen fails if backend is not running - Check `docker ps | grep backend`
- Test files must use `.tsx` extension for JSX - Always `import React` explicitly

## Available Skills (Auto-Activated)

Skills activate automatically based on context. You don't need to invoke them manually.

| Skill | Trigger | Description |
|-------|---------|-------------|
| `latest-nextjs` | Creating Next.js features | App Router, Server Components, Turbopack |
| `latest-react` | React component work | React Compiler, Actions, new hooks |
| `testing-infrastructure` | Running tests | Vitest, Playwright, PM2 test services |

## Commands

### Development

```bash
pnpm dev              # Start development server
pnpm build            # Build for production
```

### Code Generation

```bash
pnpm codegen          # Generate GraphQL types (backend must be running)
```

### Quality Checks

```bash
pnpm check            # Run typecheck + lint
pnpm typecheck        # TypeScript validation
pnpm lint             # ESLint check
pnpm lint:fix         # ESLint with auto-fix
pnpm format           # Prettier format
```

### Testing

```bash
pnpm test             # Run unit tests
pnpm test:e2e         # Run E2E tests
```

## Documentation

| Need | Reference |
|------|-----------|
| **Start here** | [AI_DOCUMENTATION_INDEX.md](AI_DOCUMENTATION_INDEX.md) |
| **Frontend** | [apps/web/AI_DOCUMENTATION_INDEX.md](apps/web/AI_DOCUMENTATION_INDEX.md) |

## Workflows

### Creating a GraphQL Operation

1. Create `.user.graphql` file in `src/graphql/`
2. Write your query/mutation
3. Run `pnpm codegen`
4. Use generated types in your code

## Quality Gates

Before committing, run:

```bash
pnpm check            # TypeScript + ESLint
pnpm test             # Unit tests
```
```

**Note:** No footer with date or version - git history already tracks this information.
