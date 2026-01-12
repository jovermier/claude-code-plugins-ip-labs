# IP (Innovative Prospects) Labs Marketplace

Claude Code marketplace for Innovative Prospects development workflows.

## Overview

This marketplace provides plugins, skills, workflows, and commands for full-stack development with:

- **React** - React 19, React Compiler, modern hooks and patterns
- **Astro** - Latest Astro features (v4-v5), islands, content collections
- **Next.js** - App Router, Server Components, performance optimization
- **Convex** - Self-hosted Convex in Coder workspaces
- **Playwright** - E2E testing patterns and best practices

## Plugins

| Plugin | Description |
|--------|-------------|
| `dev` | Core workflows, hooks, and commands |
| `coder` | Coder workspace environment |
| `astro` | Astro framework skills |
| `react` | React framework skills |
| `nextjs` | Next.js framework skills |
| `convex` | Convex backend skills |
| `playwright` | Playwright testing skills |

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add jovermier/claude-code-plugins-ip-labs
```

Then install individual plugins:

```bash
/plugin install dev@ip-labs-marketplace
/plugin install coder@ip-labs-marketplace
/plugin install astro@ip-labs-marketplace
/plugin install react@ip-labs-marketplace
/plugin install nextjs@ip-labs-marketplace
/plugin install convex@ip-labs-marketplace
/plugin install playwright@ip-labs-marketplace
```

To update the marketplace and installed plugins:

```bash
/plugin marketplace update ip-labs-marketplace
```

## Usage

Plugins are automatically discovered. Use the `/project:setup` command to generate a project-specific CLAUDE.md file.

```bash
/project:setup
```

## Architecture

This marketplace follows the **Every marketplace methodology**:

- **Agents** = Review perspectives (how to think)
- **Skills** = Domain knowledge (what to know)
- **Workflows** = Development processes (how to work)
- **Commands** = Slash commands for common tasks
- **Hooks** = Automation triggers

## License

MIT License - see [LICENSE](LICENSE) for details.
