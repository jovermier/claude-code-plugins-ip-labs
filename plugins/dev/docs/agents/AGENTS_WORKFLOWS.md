# Agents, Subagents, and Workflows

> **Last Updated:** 2026-01-15
> **Claude Code Version:** 2.1+
> **Status:** Stable

---

## Executive Summary

**Agents and subagents** are specialized AI assistants that can execute specific, well-defined tasks within larger workflows. Subagents operate in their own context windows and report back to the main agent, enabling parallel processing, focused expertise, and complex multi-step automation.

**Why it matters:** Subagents transform Claude Code from a single general-purpose assistant into a team of specialized experts. Each subagent can focus on a specific domain (security, testing, documentation) while the main agent orchestrates the overall workflow.

**When to use them:**
- Complex tasks requiring specialized expertise
- Parallel processing of independent tasks
- Reproducible workflows (code reviews, testing)
- Enforcing standards and validation

---

## Quick Start

### Creating a Custom Subagent

**1. Create subagent configuration:**

```bash
mkdir -p .claude/agents
cat > .claude/agents/code-reviewer.md << 'EOF'
---
name: code-reviewer
description: Reviews code for quality, security, and best practices
---

# Code Reviewer

## Review Process
1. Analyze code structure and organization
2. Check for potential bugs or edge cases
3. Verify adherence to project conventions
4. Suggest improvements for readability
5. Ensure proper error handling

## Standards
- Follow ESLint rules
- Use TypeScript strict mode
- Handle errors appropriately
- Document complex logic
EOF
```

**2. Use the subagent:**

```bash
# In Claude Code
> @code-reviewer Review the changes in the current branch

# Or via slash command
> /agents code-reviewer
> Review the authentication changes
```

---

## Core Concepts

### 1. Subagent Isolation

Subagents operate in **separate context windows**:

```
Main Agent (You)
    ↓
    ├── @code-reviewer (separate context)
    ├── @security-scan (separate context)
    └── @test-coverage (separate context)
    ↓
Results aggregated back to Main Agent
```

**Benefits:**
- **Parallel processing:** Run multiple subagents simultaneously
- **Focused expertise:** Each subagent specializes in one area
- **Clean context:** Each subagent starts fresh without main conversation clutter

### 2. Subagent Invocation Methods

**Method 1: @mention**
```bash
> @code-reviewer Check src/auth/jwt.ts for security issues
```

**Method 2: Slash command**
```bash
> /agents code-reviewer
# Now in code-reviewer context
```

**Method 3: Task tool (automatic)**
```bash
> Review this PR for security, performance, and test coverage
# Main agent spawns @security, @performance, @test-coverage automatically
```

### 3. Hooks Integration

Hooks trigger subagents on specific events:

```bash
# Pre-commit hook
.claude/hooks/pre-commit.sh:
  claude -p "@test-runner Ensure all tests pass"
  claude -p "@code-reviewer Quick review of staged changes"

# Post-merge hook
.claude/hooks/post-merge.sh:
  claude -p "@docs-updater Update changelog"
```

---

## Built-in Agents

Claude Code includes several built-in agents:

| Agent | Purpose | Usage |
|-------|---------|-------|
| **Explore** | Fast codebase exploration with search | `@Explore find all API endpoints` |
| **general-purpose** | General tasks with all tools | Default agent |
| **Plan** | Software architecture and planning | `@Plan design a user auth system` |
| **code-simplicity-reviewer** | Review for over-engineering | `@code-simplicity-reviewer check this PR` |
| **performance-oracle** | Analyze performance bottlenecks | `@performance-oracle profile this function` |
| **security-sentinel** | Security audit and vulnerabilities | `@security-sentinel scan for XSS` |

---

## Patterns & Best Practices

### Pattern 1: Workflow Orchestration

Subagents as explicit workflow orchestrators:

```markdown
# .claude/agents/pr-workflow.md

---
name: pr-workflow
description: Orchestrates the complete PR workflow from creation to merge
---

# PR Workflow Orchestrator

## Process
1. @code-reviewer - Initial code review
2. @security-sentinel - Security check
3. @test-coverage - Ensure test coverage
4. @performance-oracle - Performance analysis
5. @docs-updater - Update documentation
6. Generate summary report
```

**Usage:**
```bash
> @pr-workflow Handle this PR from start to finish
```

### Pattern 2: Parallel Processing

Run independent checks in parallel:

```bash
# Main agent spawns multiple subagents simultaneously
> Check this PR for security, performance, and test coverage

# Behind the scenes:
@security-sentinel → Scanning for vulnerabilities
@performance-oracle → Analyzing performance
@test-coverage → Checking test coverage
# All run in parallel, results aggregated
```

### Pattern 3: Sequential Validation

Chain subagents for quality gates:

```markdown
# .claude/agents/quality-gate.md

---
name: quality-gate
description: Ensures code meets all quality standards before merge
---

# Quality Gate

## Sequence (must pass in order)
1. **Lint Check** - Run ESLint and TypeScript compiler
2. **Unit Tests** - All tests must pass
3. **Code Review** - @code-reviewer approval
4. **Security Scan** - @security-sentinel approval
5. **Performance Check** - @performance-oracle approval

## Failure Handling
- If any step fails, stop and report
- Do not proceed to next step
- Provide specific feedback for fixes
```

### Pattern 4: Domain Experts

Specialized subagents for specific domains:

```markdown
# .claude/agents/database-expert.md

---
name: database-expert
description: Expert in database design, queries, and optimization
---

# Database Expert

## Expertise
- PostgreSQL query optimization
- Index design and placement
- Schema migration planning
- Transaction management
- Data integrity

## When to Use
- Designing new database schemas
- Optimizing slow queries
- Planning migrations
- Analyzing database performance

## Process
1. Analyze query patterns
2. Check for proper indexing
3. Verify transaction usage
4. Suggest optimizations
5. Ensure data integrity
```

### Pattern 5: Enforcer Subagents

Subagents that enforce specific rules:

```markdown
# .claude/agents/convention-enforcer.md

---
name: convention-enforcer
description: Enforces project coding conventions and standards
---

# Convention Enforcer

## Rules to Enforce
1. **No console.log** in production code
2. **All functions must have type hints**
3. **Component files must be < 300 lines**
4. **No implicit any types**
5. **Error handling required for async operations**

## Enforcement
- Check code against rules
- Flag violations
- Suggest fixes
- Block merge if critical violations
```

---

## Creating Custom Subagents

### Subagent Structure

```bash
.claude/agents/
├── my-agent.md         # Required: Agent definition
├── reference/          # Optional: Domain-specific docs
│   └── api-specs.md
└── scripts/            # Optional: Utility scripts
    └── validate.sh
```

### Minimal Subagent Template

```markdown
---
name: my-agent
description: Brief description of what this agent does and when to use it
---

# Agent Name

## Purpose
[What this agent specializes in]

## Process
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output
[What the agent produces]
```

### Advanced Subagent with Skills

```markdown
---
name: full-stack-reviewer
description: Comprehensive review covering frontend, backend, and integration
skills:
  - react-review
  - nodejs-review
  - api-review
---

# Full Stack Reviewer

## Frontend Review (@react-review)
- Component structure
- State management
- Performance optimization
- Accessibility

## Backend Review (@nodejs-review)
- API design
- Error handling
- Security practices
- Performance

## Integration Review (@api-review)
- Contract adherence
- Data validation
- Error propagation
- Testing coverage

## Report Format
```markdown
# Review Summary

## Frontend Issues
[Issues found]

## Backend Issues
[Issues found]

## Integration Issues
[Issues found]

## Recommendations
[Actionable recommendations]
```
```

---

## Hooks and Workflows

### Pre-Tool-Use Hooks

Trigger before specific tools:

```markdown
# .claude/hooks/pre-tool-use.yml

PreToolUse:
  - matcher: "Write|Edit"
    hooks:
      - type: command
        command: "./scripts/validate-format.sh $TOOL_INPUT"
        once: true
```

### Post-Tool-Use Hooks

Trigger after tool execution:

```markdown
# .claude/hooks/post-tool-use.yml

PostToolUse:
  - matcher: "Write.*\\.tsx?$"
    hooks:
      - type: agent
        agent: "convention-enforcer"
        prompt: "Check the modified file for convention compliance"
```

### Stop Hooks

Trigger at session end:

```markdown
# .claude/hooks/stop.yml

Stop:
  - type: agent
    agent: "session-summary"
    prompt: "Summarize the work completed in this session"
```

### Workflow Hooks

Complex multi-step workflows:

```markdown
# .claude/hooks/workflows/pr-review.yml

name: pr-review
description: Complete PR review workflow

steps:
  - name: initial-review
    agent: code-reviewer
    prompt: "Review the changes in this PR"

  - name: security-check
    agent: security-sentinel
    prompt: "Scan for security vulnerabilities"

  - name: test-coverage
    agent: test-coverage
    prompt: "Ensure adequate test coverage"

  - name: performance-check
    agent: performance-oracle
    prompt: "Analyze performance impact"

  - name: generate-report
    agent: report-generator
    prompt: "Compile all findings into a summary report"
```

---

## Real-World Examples

### Example 1: Automated PR Review

```bash
# .claude/agents/pr-automation.md

---
name: pr-automation
description: Automates the complete PR review and approval process
---

# PR Automation Agent

## Workflow
When a PR is created:

1. **Initial Analysis**
   - Read all changed files
   - Categorize changes (feature, bugfix, refactor, docs)
   - Estimate complexity

2. **Specialized Reviews** (parallel)
   - @code-reviewer - Code quality and patterns
   - @security-sentinel - Security vulnerabilities
   - @performance-oracle - Performance impact
   - @test-coverage - Test coverage verification

3. **Integration Check**
   - Verify no breaking changes
   - Check backward compatibility
   - Validate data migrations (if any)

4. **Documentation**
   - @docs-updater - Update relevant docs
   - Generate changelog entry

5. **Report Generation**
   - Compile all findings
   - Calculate risk score
   - Provide approval/rejection recommendation

## Output Format
```markdown
# PR Review Report

## Summary
[High-level overview]

## Findings
### Code Quality
[Issues found]

### Security
[Issues found]

### Performance
[Impact analysis]

### Test Coverage
[Coverage report]

## Recommendation
[Approve/Request Changes/Reject]

## Action Items
[List of required changes]
```
```

### Example 2: Continuous Integration

```bash
# .claude/hooks/ci-pipeline.yml

name: ci-pipeline
description: CI pipeline with automated quality checks

steps:
  - name: lint
    command: npm run lint
    on_failure: block

  - name: typecheck
    command: npm run typecheck
    on_failure: block

  - name: test
    command: npm test -- --coverage
    on_failure: block

  - name: security-scan
    agent: security-sentinel
    prompt: "Quick security scan of changed files"
    on_failure: warn

  - name: performance-check
    agent: performance-oracle
    prompt: "Check for performance regressions"
    on_failure: warn

  - name: build
    command: npm run build
    on_failure: block
```

### Example 3: Multi-Agent Debugging

```bash
# When debugging a complex issue:

> The payment flow is failing intermittently. Investigate.

# Main agent spawns specialized subagents:

@database-expert → Check for deadlocks or connection issues
@network-analyzer → Check API call patterns
@logging-analyzer → Analyze error logs for patterns
@race-condition-detector → Check for timing issues

# Each subagent works in parallel
# Main agent synthesizes findings
```

---

## Advanced Techniques

### Agent Chaining

Chain agents for complex workflows:

```bash
# Output of one agent becomes input to next

> @code-generator Generate a REST API for user management
# → Generates code

> @code-reviewer Review the generated API
# → Reviews code

> @test-generator Generate tests for the API
# → Generates tests

> @performance-oracle Optimize the API
# → Optimizes performance
```

### Agent Composition

Create composite agents from simpler agents:

```markdown
# .claude/agents/full-stack-validator.md

---
name: full-stack-validator
description: Validates both frontend and backend code
composed_of:
  - frontend-validator
  - backend-validator
---

# Full Stack Validator

## Frontend Validation
Runs @frontend-validator on all .tsx, .ts files in src/

## Backend Validation
Runs @backend-validator on all .ts files in api/

## Integration Validation
Checks frontend-backend API contracts match
```

### Conditional Agent Selection

Main agent chooses appropriate subagent:

```bash
> Check this code for issues

# Main agent analyzes:
# - If authentication code → @security-sentinel
# - If performance-critical → @performance-oracle
# - If complex logic → @code-reviewer
# - If database queries → @database-expert
```

---

## Best Practices

### 1. Focused Responsibility

Each subagent should have **one clear purpose**:

```markdown
# ❌ Bad: Too broad
---
name: do-everything
description: Handles all code-related tasks
---

# ✅ Good: Focused
---
name: typescript-validator
description: Validates TypeScript code for strict mode compliance
---
```

### 2. Clear Input/Output Contracts

Specify what the agent expects and produces:

```markdown
# .claude/agents/api-contract-validator.md

---
name: api-contract-validator
description: Validates API implementations against OpenAPI spec
---

# API Contract Validator

## Input
- OpenAPI spec file (YAML/JSON)
- Implementation files to validate

## Output
```markdown
# Validation Report

## Compliance
[Percentage of spec compliance]

## Violations
[List of spec violations]

## Missing Endpoints
[Endpoints defined but not implemented]

## Extra Endpoints
[Endpoints implemented but not in spec]
```
```

### 3. Error Handling

Specify how agents should handle failures:

```markdown
# .claude/agents/migration-runner.md

---
name: migration-runner
description: Runs database migrations safely
---

# Migration Runner

## Process
1. Backup database
2. Run migration in transaction
3. Verify success
4. Commit or rollback

## Error Handling
- If migration fails: Rollback and restore backup
- If verification fails: Rollback and alert
- If backup fails: Do not proceed

## Safety Checks
- Never run without backup
- Always use transactions
- Verify before committing
```

### 4. Performance Considerations

Parallelize independent tasks:

```markdown
# ❌ Bad: Sequential
1. @security-sentinel (10s)
2. @performance-oracle (10s)
3. @test-coverage (10s)
Total: 30s

# ✅ Good: Parallel
@security-sentinel (10s) ┐
@performance-oracle (10s) ├→ All run together
@test-coverage (10s)    ┘
Total: 10s
```

---

## Troubleshooting

### Common Issues

**"Subagent not found"**
- Check agent file exists in `.claude/agents/`
- Verify YAML frontmatter is valid
- Check name matches exactly

**"Subagent produces unexpected results"**
- Review agent instructions for clarity
- Check if agent has necessary skills
- Verify input/output contracts

**"Hooks not triggering"**
- Check hook file location (`.claude/hooks/`)
- Verify YAML syntax
- Check event type (PreToolUse, PostToolUse, Stop)

**"Performance degradation with many subagents"**
- Consider parallel vs sequential execution
- Review agent complexity
- Cache results where appropriate

---

## See Also

- [CLAUDE_SKILLS_ARCHITECTURE.md](CLAUDE_SKILLS_ARCHITECTURE.md) - Skills for agent capabilities
- [CLAUDE_CODE_COMPLETE_GUIDE.md](CLAUDE_CODE_COMPLETE_GUIDE.md) - Comprehensive Claude Code guide
- [CLAUDE.md_PATTERNS.md](CLAUDE.md_PATTERNS.md) - Configuration patterns

---

## Sources

### Official Documentation
- [Create Custom Subagents](https://code.claude.com/docs/en/sub-agents)
- [Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [Settings Reference](https://code.claude.com/docs/en/settings)

### Community Resources
- [17 Best Claude Code Workflows](https://medium.com/@joe.njenga/17-best-claude-code-workflows-that-separate-amateurs-from-pros-instantly-level-up-5075680d4c49)
- [Best Practices for Subagents](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- [How I Use Every Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)

### Advanced Topics
- [Understanding Claude Code: Skills vs Commands vs Subagents](https://www.youngleaders.tech/p/claude-skills-commands-subagents-plugins)
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

---

*Subagents are the key to scaling Claude Code from a helpful assistant to an automated development team. Start with focused, single-purpose agents and compose them into powerful workflows.*
