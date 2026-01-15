# Context Management and Token Optimization

> **Last Updated:** 2026-01-15
> **Claude Code Version:** 2.1+
> **Status:** Stable

---

## Executive Summary

**Context management** is the practice of efficiently providing information to Claude Code while minimizing token usage. Claude Code automatically pulls context into prompts, which consumes time and tokens. With proper context management, you can achieve **40-70% token reduction** while improving output quality.

**Why it matters:** Token usage directly impacts costs and response times. More importantly, efficient context management helps Claude Code focus on the most relevant information, leading to better code generation and fewer misunderstandings.

**When to use it:**
- Always - Context management is fundamental to using Claude Code effectively
- Large projects with extensive codebases
- Complex multi-file operations
- Cost-sensitive workflows

---

## Quick Start

### Basic Context Management

```bash
# 1. Use CLAUDE.md for project context
cat > CLAUDE.md << 'EOF'
# My Project

## Tech Stack
- React + TypeScript
- Node.js backend

## Commands
npm run dev      # Start dev server
npm test         # Run tests
EOF

# 2. Be specific in your requests
# Bad: "Fix the bug"
# Good: "Fix the TypeError in src/components/UserList.tsx:45"

# 3. Use progressive disclosure for large docs
# CLAUDE.md (main): Overview and links
# docs/API.md: Detailed API docs (loaded on-demand)
```

### Immediate Wins

```bash
# Specify exact files
> Read src/api/users.ts and src/types/user.ts and explain the user creation flow

# Use skipToken for conditional queries (in React)
const data = useQuery(api.users.get, userId ? { id: userId } : skipToken());

# Provide focused context
> In the payment service (src/services/payment.ts), the Stripe integration needs error handling
```

---

## Core Concepts

### 1. Context Window Economics

**Token Costs by Model:**
| Model | Input (per million) | Output (per million) |
|-------|-------------------|---------------------|
| Haiku | $1 | $5 |
| Sonnet | $3 | $15 |
| Opus | $15 | $75 |

**Optimization Impact:**
- **Poor context management:** 50KB per request × 100 requests = 5MB tokens/day
- **Good context management:** 10KB per request × 100 requests = 1MB tokens/day
- **Savings:** 80% reduction = $12/day savings for Sonnet

### 2. Progressive Disclosure Pattern

Load detailed information only when needed:

```
CLAUDE.md (3KB - always loaded)
├── Overview
├── Quick reference
└── Links to detailed docs

docs/API.md (15KB - loaded on demand)
docs/DATABASE.md (20KB - loaded on demand)
docs/DEPLOYMENT.md (10KB - loaded on demand)
```

**Token Usage Comparison:**
- **Monolithic:** 48KB loaded every time
- **Progressive:** 3KB + (15KB or 20KB or 10KB) as needed
- **Savings:** 37-45KB (77-94%) per request

### 3. Context Layers

```
Layer 1: Always Loaded (0-5KB)
├── CLAUDE.md (project root)
├── ~/.claude/CLAUDE.md (global settings)
└── Active file context

Layer 2: On-Demand (as needed)
├── Referenced documentation files
├── Related source files
└── Configuration files

Layer 3: External (via MCP)
├── Google Drive documents
├── Notion pages
├── Jira tickets
└── Design files
```

---

## Patterns & Best Practices

### Pattern 1: Focused Requests

**❌ Bad:**
```
> Fix the authentication bug
```
**Problems:**
- Claude must search entire codebase
- Loads many irrelevant files
- Unclear which auth system (there might be multiple)

**✅ Good:**
```
> Fix the JWT authentication bug in src/auth/jwt.ts where token refresh fails after 24 hours
```
**Benefits:**
- Claude knows exactly where to look
- Loads only relevant files
- Clear success criteria

### Pattern 2: File-Specific Context

**❌ Bad:**
```
> How does the payment system work?
```
**✅ Good:**
```
> Read src/payment/processor.ts and src/payment/stripe.ts and explain the charge workflow
```

### Pattern 3: Conditional Context Loading

In React with Convex:

```typescript
// ❌ Bad: Always loads user
const user = useQuery(api.users.get);

// ✅ Good: Only loads when userId exists
import { skipToken } from "convex/react";

const user = useQuery(api.users.get, userId ? { id: userId } : skipToken());
```

### Pattern 4: Reference Linking

In CLAUDE.md:

```markdown
# Project Overview

## Quick Reference
- Tech stack: React, TypeScript, Node.js
- Commands: `npm run dev`, `npm test`

## Detailed Documentation
**For API details:** See [docs/API.md](docs/API.md)
**For database schema:** See [docs/DATABASE.md](docs/DATABASE.md)
**For deployment:** See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
```

When you ask about APIs, Claude loads only `docs/API.md`.

### Pattern 5: MCP for External Context

Connect to external data sources instead of copying:

```bash
# ❌ Bad: Copy paste documentation
> Here's the API spec from Google Docs: [pastes 50KB]
> Now implement this endpoint

# ✅ Good: Use MCP
> Read the payment API spec from Google Drive and implement the charge endpoint
```

### Pattern 6: Scoped Context

```markdown
# Scoped Context Sections

## Frontend Development
When working on React components:
- Use functional components with hooks
- Follow component naming: PascalCase
- Co-locate types in `.types.ts` files
- See [docs/FRONTEND.md](docs/FRONTEND.md) for details

## Backend Development
When working on API routes:
- Validate input with Zod
- Return consistent format: { data, error }
- Add error logging
- See [docs/BACKEND.md](docs/BACKEND.md) for details

## Database Operations
When working with database:
- Use transactions for multi-table operations
- Add indexes for foreign keys
- See [docs/DATABASE.md](docs/DATABASE.md) for details
```

---

## Advanced Techniques

### 1. Context Caching

Claude automatically caches frequently accessed files. Optimize for this:

```markdown
# CLAUDE.md

## Core Files (Cached)
- src/config.ts - Configuration constants
- src/types/index.ts - Shared types
- src/utils/api.ts - API client

## Task-Specific Files (Loaded on Demand)
- src/features/user/ - User-related features
- src/features/payment/ - Payment-related features
- src/features/admin/ - Admin-related features
```

### 2. Context Pruning

Periodically review and optimize:

```markdown
# CLAUDE.md Maintenance

## Last Context Review: 2026-01-15
## Sections Removed:
- Old deployment instructions (moved to docs/DEPLOYMENT.md)
- Deprecated API docs (removed entirely)
## Sections Added:
- MCP configuration
- New testing guidelines
```

### 3. Intelligent Memory Management

Use Claude Code's memory features:

```markdown
# Project Memory

## Key Decisions
- **2025-12-01:** Migrated from Redux to Zustand for state management
- **2025-11-15:** Adopted Prisma ORM for database access
- **2025-10-01:** Switched to TypeScript strict mode

## Recurring Issues
- **Image uploads timeout on slow connections** - See src/lib/upload/#L45
- **JWT refresh fails at exactly 24 hours** - See src/auth/jwt.ts#L89

## Architecture Notes
- Tenant isolation enforced at API layer
- All database queries scoped by tenant_id
- Webhooks processed asynchronously with queue
```

### 4. Multi-Project Context

For monorepos or workspaces:

```markdown
# Monorepo Root CLAUDE.md

## Repository Overview
This is a Turborepo with apps and packages.

## App-Specific Context
**For web app:** See [apps/web/CLAUDE.md](apps/web/CLAUDE.md)
**For API:** See [apps/api/CLAUDE.md](apps/api/CLAUDE.md)
**For shared UI:** See [packages/ui/CLAUDE.md](packages/ui/CLAUDE.md)

## Shared Context
**All projects use:**
- TypeScript strict mode
- ESLint with shared config
- Shared types from @acme/types
```

---

## Token Optimization Strategies

### Strategy 1: Model Selection

Use the right model for the task:

| Task | Recommended Model | Why |
|------|------------------|-----|
| File reading, navigation | Haiku | Fast, cheap |
| Code generation | Sonnet | Balanced power/cost |
| Complex debugging | Opus | Maximum reasoning |
| Large file analysis | Haiku | Cost-effective |

### Strategy 2: Request Batching

```bash
# ❌ Bad: Many small requests
> What does functionA do?
> What does functionB do?
> What does functionC do?

# ✅ Good: Single batched request
> Read src/utils.ts and explain what functions A, B, and C do
```

### Strategy 3: Incremental Context

Start small, add context as needed:

```bash
# Step 1: Quick overview
> Summarize the payment workflow

# Step 2: Add context if needed
> Now read src/payment/stripe.ts for details about Stripe integration

# Step 3: Focus on specific issue
> In that file, explain the error handling on line 45
```

### Strategy 4: Context Budgeting

Set token budgets per task type:

```markdown
# Context Budgets

## Quick Questions (< 5KB)
- "What does this function do?"
- "Where is X used?"
- "Show me the Y component"

## Feature Implementation (10-20KB)
- Read relevant files
- Understand patterns
- Implement feature

## Major Refactoring (20-50KB)
- Read entire module
- Understand architecture
- Plan refactoring
- Implement changes
```

### Strategy 5: Avoid Redundancy

```markdown
# CLAUDE.md

## What Claude Already Knows
(Check Claude's built-in knowledge before adding)
✗ How React hooks work
✗ What TypeScript is
✗ Basic git commands
✗ REST API concepts

## What Claude Needs from You
✓ Project-specific architecture
✓ Custom conventions
✓ Build commands
✓ Business domain rules
```

---

## Monitoring and Measurement

### Track Token Usage

```bash
# Use cost tracking tools
npx ccusage

# Check usage in Claude Code
claude --stats

# Monitor per-session usage
claude --session-stats
```

### Optimization Metrics

**Before Optimization:**
- Average request: 25KB tokens
- Cost per day: $15
- Response time: 8 seconds

**After Optimization:**
- Average request: 8KB tokens
- Cost per day: $5
- Response time: 3 seconds

**Improvement:**
- Token reduction: 68%
- Cost reduction: 67%
- Speed improvement: 63%

---

## Common Pitfalls

### ❌ Pitfall 1: Over-Providing Context

```
> Here's the entire codebase history, every README, all documentation, and our company wiki. Now implement a login form.
```

**Problem:** Too much noise, expensive, slow

**Fix:**
```
> Implement a login form using JWT authentication. See src/auth/jwt.ts for reference patterns.
```

### ❌ Pitfall 2: Under-Providing Context

```
> Fix it
```

**Problem:** Claude doesn't know what "it" is

**Fix:**
```
> Fix the failing test in src/tests/auth.test.ts:123
```

### ❌ Pitfall 3: Ignoring Progressive Disclosure

One 100KB CLAUDE.md with everything

**Fix:** Split into focused files with progressive disclosure

### ❌ Pitfall 4: Redundant Context

```markdown
## What is React
React is a JavaScript library for building user interfaces...
## What is TypeScript
TypeScript is a typed superset of JavaScript...
```

**Fix:** Remove - Claude already knows this

### ❌ Pitfall 5: Not Using MCP

Copying and pasting external documentation

**Fix:** Connect MCP and reference external sources

---

## Real-World Examples

### Example 1: Large Codebase Navigation

**Scenario:** Find where user permissions are checked

**❌ Bad Approach:**
```bash
> How do permissions work in this codebase?
# Claude loads 100+ files searching
```

**✅ Good Approach:**
```bash
> Find all files that check user permissions, focusing on src/auth/ and src/middleware/
# Claude loads targeted directory
# Result: Fast, accurate, fewer tokens
```

### Example 2: Feature Implementation

**Scenario:** Add user profile editing

**❌ Bad Approach:**
```bash
> Add user profile editing
# Claude asks many questions
# Loads entire codebase
# Takes multiple iterations
```

**✅ Good Approach:**
```bash
> Add user profile editing to the settings page (src/pages/Settings.tsx).
> Use the existing user API (src/api/users.ts) and follow the pattern in src/pages/Profile.tsx.
> Include avatar upload using the upload utility (src/lib/upload.ts).
# Claude loads exactly what it needs
# Implementation is correct first try
```

### Example 3: Bug Fix

**Scenario:** Fix intermittent timeout

**❌ Bad Approach:**
```bash
> Fix the timeout bug
# Claude searches everywhere
# Wastes tokens on unrelated code
```

**✅ Good Approach:**
```bash
> The image upload times out on slow connections. See src/lib/upload.ts:45 where the timeout is set to 5000ms.
> Also check src/components/Uploader.tsx for the retry logic.
# Claude focuses on exact problem
# Quick fix, minimal tokens
```

---

## Tools and Automation

### Auto-Generation Tools

```bash
# Generate CLAUDE.md from project structure
npx claude-code-best-practices

# Analyze token usage
npx ccusage --analyze

# Optimize context
npx context-optimizer
```

### MCP Servers for Context

```bash
# Connect to documentation sources
claude plugin install notion
claude plugin install google-drive
claude plugin install confluence

# Use them in requests
> Read the API spec from Notion and implement the user endpoints
```

---

## See Also

- [CLAUDE.md_PATTERNS.md](CLAUDE.md_PATTERNS.md) - CLAUDE.md structure and best practices
- [CLAUDE_SKILLS_ARCHITECTURE.md](CLAUDE_SKILLS_ARCHITECTURE.md) - Skills and PDA patterns
- [CLAUDE_CODE_COMPLETE_GUIDE.md](CLAUDE_CODE_COMPLETE_GUIDE.md) - Comprehensive Claude Code guide
- [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md) - Cost management strategies

---

## Sources

### Official Documentation
- [Claude Code Cost Management](https://code.claude.com/docs/en/costs)
- [Context Management Guide](https://claudecode.io/guides/context-management)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Manage Claude's Memory](https://code.claude.com/docs/en/memory)

### Community Resources
- [Mastering Context Management in CLI](https://medium.com/@lalatenduswain/mastering-context-management-in-claude-code-cli-your-guide-to-efficient-ai-assisted-coding-83753129b28e)
- [Token Management 2026](https://richardporter.dev/blog/claude-code-token-management)
- [Context Engineering for Claude Code](https://thomaslandgraf.substack.com/p/context-engineering-for-claude-code)

### Tools
- [ccusage - Cost tracking](https://ccusage.com/)
- [claude-code-best-practices - Auto-generate CLAUDE.md](https://github.com/awattar/claude-code-best-practices)

---

*Effective context management is the difference between Claude Code being an expensive chatbot and a powerful, cost-effective development tool. Start with focused requests, use progressive disclosure, and always provide just enough context—not too much, not too little.*
