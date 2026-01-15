# Claude Code Complete Guide

> **Last Updated:** 2026-01-15
> **Claude Code Version:** 2.1+
> **Status:** Stable

---

## Executive Summary

**Claude Code** is Anthropic's agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before. Unlike traditional chat-based AI assistants, Claude Code can directly edit files, run commands, and create commits, making it a true pair programmer that works where you already work.

**Why it matters:** Claude Code represents a paradigm shift from AI assistants that generate code to AI agents that can autonomously navigate, understand, and modify entire codebases. It combines the power of Claude's language models with file system access, command execution, and integration with external tools via MCP.

**When to use it:**
- Building features from natural language descriptions
- Debugging and fixing issues across complex codebases
- Navigating unfamiliar codebases
- Automating tedious development tasks
- Code reviews and refactoring

---

## Quick Start

### Installation

**macOS, Linux, WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD:**
```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**Alternative Methods:**
```bash
# Homebrew
brew install --cask claude-code

# WinGet
winget install Anthropic.ClaudeCode
```

### First Use

1. Run `claude` in your terminal
2. You'll be prompted to log in (requires Pro, Max, Teams, or Enterprise subscription)
3. Start coding!

**Example:**
```bash
cd my-project
claude

# In Claude Code:
> Add user authentication with JWT tokens
> Fix the failing test in src/tests/auth.test.ts
> Explain how the payment processing workflow works
```

---

## Core Concepts

### 1. Agentic Coding

Claude Code isn't just a code generator—it's an autonomous agent that can:
- **Read and understand** your entire codebase
- **Make plans** before implementing features
- **Execute commands** to test and verify changes
- **Edit files directly** with precise changes
- **Create commits** with descriptive messages

### 2. Terminal-Native Interface

Unlike web-based IDEs, Claude Code:
- Works in your existing terminal workflow
- Integrates with git, build tools, and scripts
- Can be piped to/from other Unix tools
- Supports CI/CD automation

**Example:**
```bash
# Pipe log analysis
tail -f app.log | claude -p "Slack me if you see any anomalies"

# CI automation
claude -p "If there are new text strings, translate them to French and raise a PR"
```

### 3. Context Awareness

Claude Code maintains awareness of:
- **Project structure** - All files and directories
- **Git history** - Commits, branches, changes
- **Configuration** - CLAUDE.md, settings, environment
- **External data** - Via MCP (Google Drive, Slack, etc.)

### 4. MCP Integration

The Model Context Protocol (MCP) enables Claude Code to:
- Connect to external data sources (Google Drive, Notion, Slack)
- Use custom tools and APIs
- Access design documents, tickets, and databases
- Extend capabilities with community-built servers

---

## What Claude Code Does

### Build Features from Descriptions

Tell Claude what you want in plain English:

```
> Add a dark mode toggle to the settings page
```

Claude will:
1. Analyze your codebase structure
2. Create a plan for implementation
3. Write the necessary code
4. Test and verify it works
5. Create a commit with a descriptive message

### Debug and Fix Issues

Describe bugs or paste error messages:

```
> The login form isn't submitting on mobile devices
> Fix the TypeError in src/components/UserProfile.tsx:45
```

Claude will:
1. Analyze the error and related code
2. Identify the root cause
3. Propose and implement a fix
4. Test the solution
5. Explain what was wrong

### Navigate Any Codebase

Ask questions about your code:

```
> How does the payment processing workflow work?
> Where is the user authentication logic?
> Show me the API endpoint for creating orders
```

Claude will:
1. Search through your codebase
2. Understand the relationships between files
3. Provide clear explanations with code references
4. Answer follow-up questions

### Automate Tedious Tasks

Handle repetitive work:

```
> Fix all the linting errors
> Resolve the merge conflicts in feature/auth-rewrite
> Write release notes for the changes in this PR
```

---

## Key Features (2026)

### Claude Code 2.1 Highlights

**LSP Support:**
- Go-to-definition
- Find references
- Hover documentation
- Enhanced code intelligence

**New Commands:**
- `/terminal-setup` - Configure terminal integration
- `/add-dir` - Add additional working directories
- `/agents` - Manage custom subagents
- `/bashes` - List background tasks

**Improved Navigation:**
- Better code understanding
- Enhanced file system operations
- Faster context loading

---

## Architecture

### Relationship to Other Claude Products

```
Claude Agent SDK (Foundation)
        ↑
        | (built on top of)
        |
Claude Code ←→ Claude Desktop
```

**Claude Code vs Claude Desktop vs Agent SDK:**

| Feature | Claude Code | Claude Desktop | Claude Agent SDK |
|---------|-------------|----------------|------------------|
| Interface | CLI | GUI | Build your own |
| Primary Use | Coding | General AI assistance | Custom applications |
| Autonomous | Yes | Via Code tab | Yes |
| File System | Yes | Yes | Yes |
| Terminal | Yes | Yes | Yes |
| Custom Agents | No | No | Yes |

---

## Configuration

### CLAUDE.md

The primary way to configure your project:

```markdown
# My Project

## Architecture
- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: PostgreSQL

## Build Commands
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run dev` - Start development server

## Conventions
- Use functional components with hooks
- Follow ESLint configuration
- Write tests for new features

## Workflows
- Before coding: Create a plan
- After coding: Run tests and lint
```

### Environment Variables

```bash
# API Configuration
export ANTHROPIC_BASE_URL="https://api.anthropic.com"

# Config Directory
export CLAUDE_CONFIG_DIR="~/.claude"
```

### Settings.json

```json
{
  "model": "claude-sonnet-4-5-20250514",
  "mcpServers": ["notion", "slack"],
  "allowedTools": ["Read", "Write", "Edit", "Bash"],
  "temperature": 0.7
}
```

---

## Best Practices

### 1. Start with Clear Descriptions

**Good:**
```
> Add JWT-based authentication with login, logout, and token refresh
```

**Bad:**
```
> Add auth
```

### 2. Use CLAUDE.md for Context

Keep project-specific information in CLAUDE.md:
- Build commands
- Architecture decisions
- Code conventions
- Testing practices

### 3. Leverage MCP for External Data

Connect Claude Code to your tools:
- Google Drive for design docs
- Jira for ticket management
- Slack for notifications
- Notion for documentation

### 4. Review Before Committing

Always review Claude's changes:
- Check for unintended modifications
- Run tests to verify behavior
- Read commit messages before accepting

### 5. Use Subagents for Complex Tasks

Break complex work into specialized subagents:
```
> @code-review Review the changes in this PR
> @security-scan Check for vulnerabilities
> @test-coverage Ensure tests cover new code
```

---

## Common Workflows

### Feature Development

```bash
# 1. Describe the feature
> Add user profile editing with avatar upload

# 2. Review the plan
# Claude will outline the approach

# 3. Implement
# Claude writes the code

# 4. Test
# Claude runs tests and fixes issues

# 5. Commit
# Claude creates a descriptive commit
```

### Debugging

```bash
# 1. Describe the issue
> Tests are failing when I try to create a new user

# 2. Investigate
# Claude analyzes logs, tests, and code

# 3. Fix
# Claude identifies and fixes the root cause

# 4. Verify
# Claude confirms the fix works
```

### Code Review

```bash
# 1. Review changes
> Review the changes in the current branch

# 2. Get feedback
# Claude provides detailed analysis

# 3. Address issues
> Fix the security issues identified in the review
```

---

## Cost Management

### Model Selection

| Model | Cost (per million tokens) | Best For |
|-------|--------------------------|----------|
| Haiku | $1 input / $5 output | Simple tasks, large files |
| Sonnet | $3 input / $15 output | Most development work |
| Opus | $15 input / $75 output | Complex reasoning |

### Optimization Tips

1. **Use Haiku** for simple tasks (file reading, basic analysis)
2. **Be specific** in your requests to reduce back-and-forth
3. **Use CLAUDE.md** to avoid repeating context
4. **Monitor usage** with cost tracking tools

### Typical Costs

- **Average:** $6 per developer per day
- **90% of users:** Less than $12 per day
- **Pro Plan:** $20/month (5x usage)
- **Max Plan:** $100/month (~25x usage)

---

## Troubleshooting

### Common Issues

**"Claude can't find my files"**
- Ensure you're in the correct directory
- Check that files are not in .gitignore
- Use `/add-dir` to add additional directories

**"Context is too large"**
- Use CLAUDE.md to provide focused context
- Consider using subagents for specific tasks
- Split large requests into smaller ones

**"Claude is making unwanted changes"**
- Be more specific in your requests
- Review changes before accepting commits
- Use `--dry-run` to preview changes

---

## See Also

- [CLAUDE_SKILLS_ARCHITECTURE.md](CLAUDE_SKILLS_ARCHITECTURE.md) - Skills and Progressive Disclosure Architecture
- [CLAUDE.md_PATTERNS.md](CLAUDE.md_PATTERNS.md) - CLAUDE.md structure and best practices
- [CONTEXT_MANAGEMENT.md](CONTEXT_MANAGEMENT.md) - Token optimization strategies
- [AGENTS_WORKFLOWS.md](AGENTS_WORKFLOWS.md) - Agents, subagents, and hooks
- [MCP_INTEGRATION.md](MCP_INTEGRATION.md) - MCP setup and usage

---

## Sources

### Official Documentation
- [Claude Code Overview](https://code.claude.com/docs/en/overview)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Slash Commands Reference](https://code.claude.com/docs/en/slash-commands)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Cost Management](https://code.claude.com/docs/en/costs)

### Community Resources
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code)
- [Claude Code 2.1 Review](https://medium.com/@joe.njenga/claude-code-2-1-is-here-i-tested-all-16-new-changes-dont-miss-this-update-ea9ca008dab7)
- [How I Use Every Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)

---

*This guide is maintained alongside Claude Code's rapid development. Check the [RESEARCH_PLAN.md](RESEARCH_PLAN.md) for updates.*
