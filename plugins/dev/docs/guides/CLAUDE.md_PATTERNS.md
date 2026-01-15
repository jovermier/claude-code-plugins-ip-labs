# CLAUDE.md Patterns and Best Practices

> **Last Updated:** 2026-01-15
> **Claude Code Version:** 2.1+
> **Status:** Stable

---

## Executive Summary

**CLAUDE.md** is a project-specific configuration file that Claude Code automatically loads to understand your codebase, development practices, and workflow preferences. It serves as the primary mechanism for providing context about your project without having to repeatedly explain conventions, build processes, or architectural decisions.

**Why it matters:** A well-structured CLAUDE.md transforms Claude Code from a generic coding assistant into a knowledgeable team member who understands your project's specific patterns, conventions, and workflows. This reduces token usage, improves output quality, and eliminates repetitive prompting.

**When to use it:**
- Every software project should have a CLAUDE.md
- Keep it in your project root (or `~/.claude/` for global settings)
- Update it as your project evolves
- Use progressive disclosure for large configurations

---

## Quick Start

### Minimal CLAUDE.md

```markdown
# My Project

## Tech Stack
- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: PostgreSQL

## Commands
- `npm run dev` - Start development server
- `npm test` - Run tests
- `npm run build` - Build for production

## Conventions
- Use functional components with hooks
- Follow ESLint rules
- Write tests for new features
```

### Place It in Your Project Root

```bash
my-project/
├── CLAUDE.md      # Put it here
├── src/
├── package.json
└── README.md
```

---

## Core Concepts

### 1. Progressive Disclosure

For complex projects, use the PDA (Progressive Disclosure Architecture) pattern:

**CLAUDE.md (main file - 2-3KB):**
```markdown
# Project Overview

[Brief overview and quick reference]

## Architecture
[High-level structure]

## Additional Documentation
- **API Reference**: See [docs/API.md](docs/API.md)
- **Database Schema**: See [docs/DATABASE.md](docs/DATABASE.md)
- **Deployment**: See [docs/DEPLOY.md](docs/DEPLOY.md)
```

**docs/API.md (loaded on-demand):**
```markdown
# API Reference

[Detailed API documentation]
```

This approach:
- Keeps CLAUDE.md concise and focused
- Loads detailed documentation only when needed
- Saves tokens (40-70% reduction typical)
- Easier to maintain

### 2. Section Types

Essential CLAUDE.md sections:

**Architecture & Structure:**
```
## Project Structure
/src/components    # React components
/src/hooks         # Custom hooks
/src/utils         # Utility functions
/src/api           # API clients
```

**Build Commands:**
```
## Development Commands
npm run dev        # Start dev server on port 3000
npm run build      # Build for production
npm run test       # Run tests
npm run lint       # Run ESLint
```

**Code Conventions:**
```
## Coding Standards
- Use TypeScript strict mode
- Functional components only
- Props interfaces in separate files
- No implicit any types
```

**Workflow Patterns:**
```
## Development Workflow
1. Create feature branch
2. Implement changes
3. Run tests and lint
4. Create PR with description
5. Request review
```

### 3. Global vs Project CLAUDE.md

**Global CLAUDE.md** (`~/.claude/CLAUDE.md`):
- Personal preferences
- Cross-project conventions
- Tool configurations
- Editor settings

**Project CLAUDE.md** (`/project/CLAUDE.md`):
- Project-specific architecture
- Build commands
- Team conventions
- Deployment processes

Project CLAUDE.md overrides global settings for that project.

---

## Patterns & Best Practices

### Pattern 1: The "Forcing Function"

Use CLAUDE.md to enforce good practices:

```markdown
# Project Conventions

## Before Making Changes
ALWAYS:
1. Read the existing code patterns
2. Check for similar implementations
3. Ask if unclear about conventions

## Code Review Checklist
- [ ] Tests added/updated
- [ ] No console.log statements
- [ ] TypeScript strict mode compliance
- [ ] ESLint passing
- [ ] Documentation updated

## What NOT to Do
- Don't refactor unrelated code
- Don't add dependencies without justification
- Don't skip tests
- Don't ignore TypeScript errors
```

### Pattern 2: Architecture Documentation

```markdown
# Architecture Overview

## Frontend (React)
- State: Zustand for global state
- Data fetching: React Query
- Routing: React Router v6
- Styling: Tailwind CSS

## Backend (Node.js)
- Framework: Express
- Database: PostgreSQL with Prisma
- Auth: JWT tokens
- API: RESTful with OpenAPI spec

## Data Flow
1. Client → API Gateway
2. API Gateway → Service Layer
3. Service Layer → Database
4. Response back through chain
```

### Pattern 3: Domain-Specific Context

For projects with specialized domains:

```markdown
# Business Domain

## Key Terms
- **Tenant**: Organization using our platform
- **User**: Individual user within a tenant
- **Subscription**: Billing entity
- **Quota**: Usage limits per tenant

## Business Rules
- Users belong to exactly one tenant
- Tenants can have multiple subscriptions
- Quotas are enforced at tenant level
- Free tier: 1000 API calls/month

## Common Patterns
When working with multi-tenant features:
1. Always scope queries by tenant_id
2. Never mix tenant data in responses
3. Validate tenant access on every request
```

### Pattern 4: Environment-Specific Configuration

```markdown
# Environment Configuration

## Development
- Database: localhost:5432
- Redis: localhost:6379
- API: http://localhost:3000

## Staging
- Database: staging-db.internal
- Redis: staging-redis.internal
- API: https://staging-api.example.com

## Production
- Database: Uses cloud proxy
- Redis: Uses ElastiCache
- API: https://api.example.com

## Environment Variables Required
- DATABASE_URL
- REDIS_URL
- JWT_SECRET
- API_KEY
```

### Pattern 5: Workflow Automation

```markdown
# Automated Workflows

## When Creating a New Feature
1. Feature branch from main
2. Implement with tests
3. Run: `npm run verify` (lint + test + typecheck)
4. Update CLAUDE.md if architecture changes
5. Create PR with template

## When Fixing Bugs
1. Create branch: `bugfix/description`
2. Add reproduction test
3. Fix the bug
4. Verify test passes
5. Add regression test
6. Create PR

## PR Template
## Description
[Brief description of changes]

## Type
- [ ] Feature
- [ ] Bugfix
- [ ] Refactor
- [ ] Documentation

## Testing
[How this was tested]

## Checklist
- [ ] Tests pass
- [ ] Lint passes
- [ ] Types check
- [ ] Documentation updated
```

---

## Common Pitfalls

### ❌ Bad: Monolithic File

```markdown
# Everything in one file

## API Endpoints (500 lines of API docs)
## Database Schema (300 lines of schema)
## Frontend Components (400 lines of component docs)
## Deployment Process (200 lines)
...
```

**Problems:**
- Loads everything, every time
- Slow token consumption
- Hard to navigate
- Difficult to maintain

### ✅ Good: Progressive Disclosure

```markdown
# Project Overview

[Brief overview]

## Documentation
- **API**: See [docs/API.md](docs/API.md)
- **Database**: See [docs/DATABASE.md](docs/DATABASE.md)
- **Components**: See [docs/COMPONENTS.md](docs/COMPONENTS.md)
- **Deployment**: See [docs/DEPLOY.md](docs/DEPLOY.md)
```

### ❌ Bad: Vague Instructions

```markdown
## Conventions
Write good code.
Follow best practices.
```

### ✅ Good: Specific Guidelines

```markdown
## Conventions
- Use functional components with hooks
- Props interfaces must be in separate `.types.ts` files
- Maximum component length: 200 lines
- Always handle errors with try-catch
- Use React Query for data fetching
```

### ❌ Bad: Outdated Information

```markdown
## Commands
npm run start  # This was changed 6 months ago
```

### ✅ Good: Maintained Documentation

```markdown
## Commands (Last Updated: 2026-01-15)
npm run dev        # Start development server (port 3000)
npm run build      # Production build
npm run test       # Run tests with coverage
npm run lint       # Run ESLint with auto-fix
```

---

## Real-World Examples

### Example 1: Full-Stack Web App

```markdown
# E-Commerce Platform

## Tech Stack
**Frontend:**
- React 19 + TypeScript
- Zustand (state)
- React Query (data)
- Tailwind CSS (styling)

**Backend:**
- Node.js + Express
- PostgreSQL + Prisma
- JWT authentication
- Stripe payments

## Project Structure
```
/frontend
  /src
    /components    # Reusable UI components
    /pages         # Route components
    /hooks         # Custom React hooks
    /api           # API client functions
    /store         # Zustand stores
    /types         # TypeScript types
/backend
  /src
    /routes        # Express route handlers
    /services      # Business logic
    /models        # Prisma models
    /middleware    # Express middleware
    /utils         # Utility functions
```

## Commands
**Frontend:**
```bash
cd frontend
npm run dev        # Port 3000
npm run build
npm run test
npm run lint
```

**Backend:**
```bash
cd backend
npm run dev        # Port 4000
npm run migrate    # Run database migrations
npm run seed       # Seed database
npm run test
```

## Conventions
- Use async/await, no callbacks
- Always validate input with Zod
- Return consistent response format: `{ data, error }`
- Log all errors with context
- Write unit tests for services
- Write integration tests for routes

## Authentication
- JWT tokens stored in httpOnly cookies
- Protected routes verify token in middleware
- Token refresh handled automatically
- Session timeout: 24 hours

## Payment Flow
1. Client creates payment intent via API
2. Server calls Stripe to create intent
3. Client confirms payment with Stripe.js
4. Webhook handles payment confirmation
5. Server updates order status

## Environment Variables
```
DATABASE_URL=
JWT_SECRET=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
FRONTEND_URL=
```

## Additional Documentation
- [API Reference](docs/API.md)
- [Database Schema](docs/DATABASE.md)
- [Deployment Guide](docs/DEPLOY.md)
```

### Example 2: Monorepo Configuration

```markdown
# Monorepo Root CLAUDE.md

## Repository Structure
This is a Turborepo monorepo with the following packages:

```
/apps
  /web              # Next.js frontend
  /api              # Express backend
/packages
  /ui               # Shared UI components
  /types            # Shared TypeScript types
  /utils            # Shared utilities
  /config           # Shared ESLint/TSConfig
```

## Commands
**From root:**
```bash
npm run dev         # Start all apps in development
npm run build       # Build all packages
npm run test        # Run all tests
npm run lint        # Lint all packages
```

**Package-specific:**
```bash
cd apps/web
npm run dev         # Start only web app
```

## Conventions
- Internal packages use `workspace:*` protocol
- Shared types in `@acme/types`
- Shared UI in `@acme/ui`
- Always build packages before apps
- Use Turbo for task orchestration

## Dependencies
- Add shared dependencies to relevant `/package` folder
- Add dev dependencies to root
- Never duplicate dependencies across packages

## Additional Documentation
- [Web App](apps/web/CLAUDE.md)
- [API](apps/api/CLAUDE.md)
- [UI Package](packages/ui/CLAUDE.md)
```

### Example 3: Machine Learning Project

```markdown
# ML Model Training Pipeline

## Tech Stack
- Python 3.11
- PyTorch 2.0
- Hydra for configuration
- Weights & Biases for tracking
- Docker for environments

## Project Structure
```
/data               # Datasets (not in git)
/src
  /data             # Data loading and preprocessing
  /models           # Model architectures
  /training         # Training loops and utilities
  /evaluation       # Metrics and evaluation
  /inference        # Inference code
/configs            # Hydra configuration files
/notebooks          # Jupyter notebooks for exploration
```

## Commands
```bash
# Training
python src/train.py model=resnet50 data=cifar10

# Evaluation
python src/evaluate.py checkpoint=/path/to/checkpoint.ckpt

# Inference
python src/inference.py --input image.jpg --checkpoint model.ckpt

# Testing
pytest tests/

# Type checking
mypy src/
```

## Conventions
- Configuration via YAML files in `/configs`
- Use Hydra for experiment management
- Log everything to W&B
- Checkpoints saved to `/checkpoints`
- Random seeds set for reproducibility
- Type hints required on all functions

## Data Pipeline
1. Raw data in `/data/raw`
2. Preprocessed data in `/data/processed`
3. Caching with joblib
4. Augmentation in training loop
5. Normalization per dataset statistics

## Model Versioning
- Models tracked with DVC
- Checkpoints: `{model_name}_{epoch}_{metric}.ckpt`
- Best model symlink: `best.ckpt`
- Metadata in W&B run

## Additional Documentation
- [Data Formats](docs/DATA.md)
- [Model Architectures](docs/MODELS.md)
- [Experiment Tracking](docs/EXPERIMENTS.md)
```

---

## Advanced Patterns

### Conditional Instructions

```markdown
# Task-Specific Guidelines

## When Working on Frontend
- Use Tailwind for styling
- Test responsive design
- Check accessibility
- Optimize images

## When Working on Backend
- Always validate input
- Handle errors gracefully
- Log with correlation IDs
- Rate limit public endpoints

## When Working on Database
- Use transactions for multi-table operations
- Add indexes for foreign keys
- Consider query performance
- Document migrations

## When Deploying
- Run all tests first
- Check environment variables
- Monitor error rates
- Have rollback ready
```

### Multi-Language Projects

```markdown
# Multi-Language Project

## Language-Specific Guidelines

### Python
- Follow PEP 8
- Use type hints
- Docstrings for public functions
- Black formatter

### TypeScript
- Use strict mode
- No implicit any
- Interface for objects
- Type for functions

### SQL
- UppercASE keywords
- snake_case identifiers
- Index foreign keys
- Comment complex queries
```

---

## Maintenance Strategy

### When to Update CLAUDE.md

**Update when:**
- Architecture changes
- New dependencies added
- Build commands change
- Conventions evolve
- New team members join

**Review schedule:**
- Monthly: Check for accuracy
- Quarterly: Major restructure if needed
- Annually: Complete refresh

### Version Control

```markdown
# CLAUDE.md Maintenance

**Last Reviewed:** 2026-01-15
**Version:** 2.0
**Maintainer:** Team Lead

## Changelog
### v2.0 (2026-01-15)
- Added progressive disclosure pattern
- Reorganized by section type
- Added real-world examples

### v1.0 (2025-06-01)
- Initial version
```

---

## See Also

- [CLAUDE_CODE_COMPLETE_GUIDE.md](CLAUDE_CODE_COMPLETE_GUIDE.md) - Comprehensive Claude Code guide
- [CLAUDE_SKILLS_ARCHITECTURE.md](CLAUDE_SKILLS_ARCHITECTURE.md) - Skills and PDA patterns
- [CONTEXT_MANAGEMENT.md](CONTEXT_MANAGEMENT.md) - Token optimization strategies

---

## Sources

### Official Documentation
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Code Overview](https://code.claude.com/docs/en/overview)
- [Context Management Guide](https://claudecode.io/guides/context-management)

### Community Resources
- [Creating the Perfect CLAUDE.md](https://dometrain.com/blog/creating-the-perfect-claudemd-for-claude-code/)
- [CLAUDE.md Structure and Best Practices](https://callmephilip.com/posts/notes-on-claude-md-structure-and-best-practices/)
- [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Managing Large CLAUDE.md Files](https://www.reddit.com/r/ClaudeAI/comments/1lr6occ/tip_managing_large_claudemd_files_with_document/)
- [Definitive Guide to Claude Code](https://jpcaparas.medium.com/the-definitive-guide-to-claude-code-from-first-install-to-production-workflows-6d37a6d33e40)

### Tools
- [claude-code-best-practices](https://github.com/awattar/claude-code-best-practices) - Auto-generate CLAUDE.md

---

*Remember: CLAUDE.md is a living document. Keep it updated as your project evolves to ensure Claude Code always has the most accurate context.*
