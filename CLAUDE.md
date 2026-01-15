# IP Labs Marketplace

Claude Code marketplace for Innovative Prospects development workflows covering React, Astro, Next.js, Convex, and Playwright.

## Overview

This marketplace provides **7 plugins** following the **Every marketplace methodology**:

- **Agents** = Review perspectives and personalities (how to think)
- **Skills** = Domain knowledge bases (what to know)
- **Workflows** = Development processes (how to work)
- **Commands** = Slash commands for common tasks
- **Hooks** = Automation triggers

## Marketplace Plugins

### Core Development

#### dev

Core development workflows, hooks, and commands.

**Skills:**

- `plan-manager` - Manage workflow plans and context documents
- `context7-skill-generator` - Automatically generate skills from Context7 MCP documentation
- `file-todos` - File-based todo system with dependency tracking
- `quality-severity` - P1/P2/P3 severity classification for issues

**Workflows:**

- `meta-workflow` - Automatic workflow selection and composition
- `tdd-workflow` - Test-driven development
- `ui-iteration-workflow` - Iterative UI development with visual feedback
- `bug-fix-workflow` - Systematic debugging approach
- `claude-md-setup` - Generate or update CLAUDE.md from marketplace plugins

**Commands:**

- `/project:setup` - Analyze project and generate/update CLAUDE.md
- `/project:new-page` - Create new Astro pages
- `/project:new-component` - Create React/Astro components
- `/project:new-blog-post` - Create blog posts
- `/project:test-ui` - Run Playwright tests
- `/skill:from-context7` - Generate a skill from Context7 MCP documentation

**Hooks:**

- `auto-archive-plans.py` - Automatically archive completed plans
- `meta-workflow-enforcer.py` - Enforce meta-workflow on every request

### Environment

#### coder

Coder workspace environment skills.

**Skills:**

- `coder-environment` - Coder workspace context, Docker-in-Docker, Kubernetes CLI

### Framework Skills

#### astro

Astro development skills.

**Skills:**

- `latest-astro` - Astro v4-v5 features, islands, content collections

#### react

React development skills.

**Skills:**

- `latest-react` - React 19, React Compiler, new hooks, actions

#### nextjs

Next.js development skills.

**Skills:**

- `latest-nextjs` - Next.js App Router, Server Components, performance

### Backend

#### convex

Convex development in Coder workspaces.

**Skills:**

- `coder-convex` - Convex integration patterns
- `coder-convex-setup` - Convex setup and configuration
- `convex-chef` - Convex Chef agent integration
- `convex-self-hosting` - Self-hosted Convex deployment, auth setup, environment config, troubleshooting, and production considerations

### Testing

#### playwright

Playwright E2E testing skills.

**Skills:**

- `playwright-test` - E2E testing patterns, fixtures, best practices

## Quick Reference

| Plugin     | Skills            | Commands   | Hooks   |
| ---------- | ----------------- | ---------- | ------- |
| dev        | 4 skills          | 6 commands | 2 hooks |
| coder      | coder-environment | -          | -       |
| astro      | latest-astro      | -          | -       |
| react      | latest-react      | -          | -       |
| nextjs     | latest-nextjs     | -          | -       |
| convex     | 4 skills          | -          | -       |
| playwright | playwright-test   | -          | -       |

## Usage

Plugins are automatically discovered by Claude Code. Skills are loaded based on project context.

### Setting Up a New Project

Use the `/project:setup` command to generate a CLAUDE.md file tailored to your project:

```bash
/project:setup
```

This will:

1. Scan your `package.json` for dependencies
2. Match technologies to marketplace plugins
3. Generate a CLAUDE.md with relevant skills, workflows, and commands

## Architecture

```
plugins/
├── dev/              # Core workflows, commands, hooks
├── coder/            # Coder workspace environment
├── astro/            # Astro framework skills
├── react/            # React framework skills
├── nextjs/           # Next.js framework skills
├── convex/           # Convex backend skills
└── playwright/       # Playwright testing skills
```

## License

MIT
