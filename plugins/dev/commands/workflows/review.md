---
name: workflows:review
description: Perform exhaustive code reviews using multi-agent parallel analysis with ultra-thinking and worktrees
argument-hint: "[branch-name or PR number]"
---

# Workflows: Review - Multi-Agent Code Review

## Introduction

The `/workflows:review` command performs comprehensive code reviews by launching multiple specialized agents in parallel. Each agent independently analyzes the changes from their unique perspective, providing thorough coverage across security, performance, architecture, simplicity, and patterns.

## Main Tasks

### Phase 1: Setup and Context Gathering

1. **Identify Review Target**
   - If branch-name provided: Find commits diverging from main
   - If PR number: Use `gh pr view` to fetch details
   - If neither: Check current branch vs main

2. **Create Worktree** (Optional but Recommended)
   ```bash
   git worktree add ../worktree-review [branch-name]
   ```
   - Allows reviewing in isolated environment
   - Keeps main workspace clean
   - Enables side-by-side comparison

3. **Gather Changes**
   - Get full diff with context
   - List all modified files
   - Identify affected components

### Phase 2: Parallel Agent Execution

Launch the following agents in parallel using the Task tool:

| Agent | Focus | Subagent Type |
|-------|-------|---------------|
| Architecture Strategist | System design, component boundaries, architectural patterns | general-purpose |
| Security Sentinel | OWASP Top 10, vulnerabilities, secret exposure | general-purpose |
| Performance Oracle | Performance bottlenecks, optimization opportunities | general-purpose |
| Code Simplicity Reviewer | YAGNI compliance, over-engineering, unnecessary complexity | general-purpose |
| Pattern Recognition Specialist | Design patterns, anti-patterns, code consistency | general-purpose |

**Execution Pattern:**
```
For each agent:
1. Read the agent's SKILL.md for context
2. Provide the diff/changes as context
3. Instruct the agent to analyze from their specialty perspective
4. Collect findings with severity classifications (P1/P2/P3)
```

### Phase 3: Findings Aggregation

1. **Collect All Agent Outputs**
   - Gather findings from each parallel agent
   - Standardize severity classifications
   - Remove duplicate findings

2. **Prioritize by Severity**
   - **P1 (Critical)**: List first, require blocking
   - **P2 (Important)**: List second, recommend fixing
   - **P3 (Nice-to-Have)**: List last, track for later

3. **Generate Review Report**
   - Summary statistics (X findings: Y P1, Z P2, W P3)
   - Categorized findings by severity
   - File-by-file breakdown
   - Actionable recommendations

### Phase 4: Todo Creation

For each **P1** and **P2** finding:
1. Create todo file in `todos/` directory
2. Use naming convention: `[issue-id]-pending-[severity]-[description].md`
3. Link to related code files and line numbers
4. Set dependencies if findings are related

## Key Principles

- **Parallel Execution**: Run all agents simultaneously for speed
- **Independent Analysis**: Each agent works without knowledge of others
- **Severity-First**: Critical issues take priority
- **Actionable Output**: Every finding includes specific fix steps
- **Persistent Tracking**: High-severity findings become todos

## Quality Checklist

- [ ] All review agents launched in parallel
- [ ] Findings include P1/P2/P3 severity
- [ ] P1 issues have blocking recommendations
- [ ] P1/P2 findings have corresponding todos created
- [ ] Report includes file locations and line numbers
- [ ] Duplicate findings deduplicated
- [ ] Worktree cleaned up after review

## Common Pitfalls

- **Sequential Agent Execution**: Launch all agents in one message, not one by one
  - *Solution*: Use multiple Task tool calls in a single response

- **Missing Context**: Agents need the actual diff, not just file list
  - *Solution*: Provide `git diff main...HEAD` output with sufficient context

- **Inconsistent Severity**: Different agents may classify same issue differently
  - *Solution*: Re-classify during aggregation phase for consistency

- **Forgot Cleanup**: Worktrees left behind after review
  - *Solution*: Always run `git worktree remove ../worktree-review` at the end

## Quick Usage Examples

**Example 1: Review current branch**
> User: `/workflows:review`

> Assistant: I'll review the changes on your current branch compared to main.

[Launches 5 parallel agents, aggregates findings, creates todos]

**Example 2: Review specific PR**
> User: `/workflows:review 123`

> Assistant: I'll review PR #123.

[Fetches PR details, launches parallel agents on PR diff]

**Example 3: Review feature branch**
> User: `/workflows:review feature/add-auth`

> Assistant: I'll review the feature/add-auth branch.

[Checks out branch comparison, launches parallel agents]

## Sample Output

```markdown
# Code Review Report: feature/add-auth

## Summary
- **15 total findings** across 8 files
- **2 P1 (Critical)** - Blocking merge
- **5 P2 (Important)** - Should fix
- **8 P3 (Nice-to-Have)** - Enhancements

## P1 Findings (Blocking)

### Issue #1: Hardcoded JWT Secret
**Severity:** P1 (Critical)
**Category:** Security
**File:** src/auth/jwt.ts
**Lines:** 15

**Problem:**
JWT secret is hardcoded in source code, exposing it to version control.

**Impact:**
Attackers with repository access can forge authentication tokens.

**Fix:**
1. Move secret to environment variable
2. Use `process.env.JWT_SECRET`
3. Add to `.env.example`

**Created Todo:** `001-pending-p1-hardcoded-jwt-secret.md`

---

## P2 Findings (Should Fix)

### Issue #3: N+1 Query Pattern
**Severity:** P2 (Important)
**Category:** Performance
**File:** src/users/repo.ts
**Lines:** 45-50

**Problem:**
User posts are fetched in a loop, causing N+1 queries.

**Impact:**
Response time scales O(n) with user count. At 100 users, 101 queries executed.

**Fix:**
Use eager loading or data loader pattern.

**Created Todo:** `002-pending-p2-n-plus-one-queries.md`
```

## Related Skills

- `/quality-severity` - For classifying issue severity
- `/file-todos` - For managing todo creation
