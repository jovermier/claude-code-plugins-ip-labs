# IP Labs Marketplace

Claude Code marketplace for Innovative Prospects development workflows.

## Overview

This marketplace provides plugins, skills, agents, workflows, and commands for full-stack development with comprehensive code review and quality assurance capabilities.

**Version:** 1.1.0

**Key Features:**
- **13 Specialized Agents** (9 review + 4 research) - Parallel agent orchestration
- **File-Based Todo System** - Persistent work tracking with YAML frontmatter
- **Quality Gate Severity Levels** - P1/P2/P3 classification for issues
- **Knowledge Compounding** - Solution documentation for future reference
- **Integrated Meta-Workflow** - Agents automatically used during development

## Plugins

| Plugin | Agents | Commands | Skills | Workflows | Description |
|--------|--------|----------|--------|-----------|-------------|
| [dev](plugins/dev/) | 13 | 11 | 8 | 7 | Core workflows, agents, commands, skills, and todo management |
| [coder](plugins/coder/) | - | - | 2 | - | Coder workspace management and hahomelabs configuration |
| [astro](plugins/astro/) | - | - | 1 | - | Astro v4-v5 features, islands, content collections |
| [react](plugins/react/) | - | - | 1 | - | React 19, React Compiler, modern hooks and patterns |
| [nextjs](plugins/nextjs/) | - | - | 1 | - | App Router, Server Components, performance |
| [convex](plugins/convex/) | - | - | 4 | - | Self-hosted Convex backend development |
| [nhost](plugins/nhost/) | - | - | 2 | - | Hasura, PostgreSQL extensions, and Docker CLI |
| [graphql](plugins/graphql/) | - | 1 | 1 | - | GraphQL workflow with codegen and type safety |
| [playwright](plugins/playwright/) | - | - | 2 | - | E2E testing patterns and best practices |

**Totals:** 13 agents, 12 commands, 22 skills, 7 workflows

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add [your-org]/ip-labs-marketplace
```

Then install individual plugins:

```bash
/plugin install dev@ip-labs-marketplace
/plugin install coder@ip-labs-marketplace
/plugin install astro@ip-labs-marketplace
/plugin install react@ip-labs-marketplace
/plugin install nextjs@ip-labs-marketplace
/plugin install convex@ip-labs-marketplace
/plugin install nhost@ip-labs-marketplace
/plugin install graphql@ip-labs-marketplace
/plugin install playwright@ip-labs-marketplace
```

To update the marketplace and installed plugins:

```bash
/plugin marketplace update ip-labs-marketplace
```

## Quick Start

### 1. Project Setup
Generate a project-specific CLAUDE.md file:

```bash
/project:setup
```

### 2. Create a Plan
Start a new feature with a structured plan using parallel research:

```bash
/workflows:plan Add user authentication with JWT
```

### 3. Execute Work
Implement with quality gates and agent scrutiny:

```bash
/workflows:work plans/active/2026-01-12-add-auth.md
```

### 4. Review Code
Run comprehensive parallel agent review:

```bash
/workflows:review
```

### 5. Track Work
Manage todos with the file-based system:

```bash
/todo list
/todo create
```

## Dev Plugin Components

### Agents (13)

#### Review Agents (9)
| Agent | Purpose |
|-------|---------|
| `architecture-strategist` | System design validation and architectural patterns |
| `agent-native-reviewer` | AI accessibility and agent parity verification |
| `code-simplicity-reviewer` | YAGNI enforcement and over-engineering detection |
| `data-integrity-guardian` | Referential integrity and transaction boundaries |
| `data-migration-expert` | Database migration safety and ID mapping validation |
| `deployment-verification-agent` | Pre-deployment checklists and rollback procedures |
| `pattern-recognition-specialist` | Design patterns and anti-patterns analysis |
| `performance-oracle` | Performance optimization and bottleneck analysis |
| `security-sentinel` | OWASP compliance and vulnerability scanning |

#### Research Agents (4)
| Agent | Purpose |
|-------|---------|
| `repo-research-analyst` | Repository structure and pattern analysis |
| `best-practices-researcher` | External best practices research |
| `framework-docs-researcher` | Framework documentation lookup |
| `git-history-analyzer` | Historical context and code evolution |

### Commands (11)

#### Workflow Commands
| Command | Purpose |
|---------|---------|
| `/workflows:plan` | Create structured project plans with parallel research |
| `/workflows:review` | Multi-agent parallel code review |
| `/workflows:compound` | Document solved problems as knowledge |
| `/workflows:work` | Structured work execution with quality gates |
| `/deepen-plan` | Enhance existing plans with research |
| `/todo` | File-based todo management |

#### Project Commands
| Command | Purpose |
|---------|---------|
| `/project:setup` | Generate project-specific CLAUDE.md |
| `/project:new-page` | Create new page with component |
| `/project:new-component` | Create new component with test |
| `/project:new-blog-post` | Create new blog post |
| `/test-ui` | Test UI component changes |

### Skills (8)
| Skill | Purpose |
|-------|---------|
| `file-todos` | File-based todo system with YAML frontmatter |
| `quality-severity` | P1/P2/P3 quality gate classification |
| `plan-manager` | Plan lifecycle management |
| `context7-skill-generator` | Generate skills from Context7 MCP documentation |
| `skill-generator` | Generate production-ready Claude Code skills from descriptions |
| `skill-reviewer` | Review skills for quality, best practices, and PDA compliance |
| `skill-optimizer` | Refactor skills using Progressive Disclosure Architecture (80-95% token savings) |
| `skill-architect` | Meta-orchestrator coordinating complete skill lifecycle workflows |

### Workflows (7)
| Workflow | Purpose |
|----------|---------|
| `meta-workflow` | Project orchestration with integrated agent scrutiny |
| `tdd-workflow` | Test-driven development process |
| `ui-iteration-workflow` | UI component iteration with screenshots |
| `bug-fix-workflow` | Systematic bug fixing process |

## Quality Gates

Issues are classified with severity levels:

| Severity | Description | Examples |
|----------|-------------|----------|
| **P1 (Critical)** | Blocks merge | Security vulnerabilities, data corruption, breaking changes |
| **P2 (Important)** | Should fix | Performance issues, architectural concerns, code clarity |
| **P3 (Nice-to-Have)** | Enhancement | Code cleanup, optimizations, documentation |

## File-Based Todo System

Todos are stored as markdown files with YAML frontmatter:

```markdown
---
status: pending
priority: p2
issue: "123"
dependencies: []
created: 2026-01-12
updated: 2026-01-12
---

# Add JWT Authentication

## Problem Statement
Application has no authentication.

## Acceptance Criteria
- [ ] Users can log in
- [ ] JWT tokens validated
- [ ] Logout works
```

## Architecture

This marketplace follows the [Every marketplace methodology](https://github.com/EveryInc/compound-engineering-plugin):

- **Agents** = Specialized review perspectives (how to think)
- **Skills** = Domain knowledge (what to know)
- **Workflows** = Development processes (how to work)
- **Commands** = Slash commands for common tasks
- **Hooks** = Automation triggers

## Directory Structure

```
ip-labs-marketplace/
├── plugins/
│   ├── dev/
│   │   ├── agents/
│   │   │   ├── review/          # 9 review agents
│   │   │   ├── research/        # 4 research agents
│   │   │   ├── design/          # (future expansion)
│   │   │   ├── workflow/        # (future expansion)
│   │   │   └── docs/            # Documentation
│   │   ├── commands/
│   │   │   └── workflows/       # Workflow commands
│   │   ├── skills/
│   │   ├── workflows/
│   │   ├── hooks/
│   │   ├── indexes/            # Plan and context index templates
│   │   └── CHANGELOG.md
│   ├── coder/                  # Coder workspace environment
│   ├── react/                  # React framework skills
│   ├── astro/                  # Astro framework skills
│   ├── nextjs/                 # Next.js framework skills
│   ├── convex/                 # Convex backend skills
│   ├── nhost/                  # Hasura/PostgreSQL skills
│   ├── graphql/                # GraphQL workflow and codegen
│   └── playwright/             # E2E testing skills
├── todos/                      # File-based todos
├── plans/                      # Project plans
└── docs/solutions/             # Knowledge base
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

This marketplace is heavily influenced by the [Every Inc. compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin).
