---
name: workflows:work
description: Execute structured work with quality gates and agent scrutiny. For implementing features from plans or todos with automatic quality checkpoints.
argument-hint: "[plan-file or todo-file or task description]"
---

# Workflows: Work - Structured Work Execution

## Introduction

The `/workflows:work` command executes structured implementation work with quality gates and specialized agent scrutiny. Use it when implementing features from plans, completing todos, or working on complex tasks that require quality verification.

## Main Tasks

### Phase 1: Understand the Work

1. **Identify Input Type**
   - **Plan file**: Extract plan steps and execute them
   - **Todo file**: Implement the acceptance criteria
   - **Task description**: Create mini-plan and execute

2. **Assess Complexity**
   - **Simple**: Single file, <50 lines of code → Direct execution
   - **Medium**: 2-5 files, 50-200 lines → Plan + scrutiny
   - **Complex**: 5+ files, 200+ lines, or architectural changes → Full workflow

### Phase 2: Create/Update Plan (if needed)

For medium/complex work or when starting from a task description:

1. **Break Down the Work**
   - List implementation steps in dependency order
   - Identify files to create/modify
   - Note testing requirements
   - Mark complexity for each step

2. **Create Work Document**
   ```markdown
   ---
   created: 2026-01-12
   status: in_progress
   priority: p2
   workflow: work
   quality_gates_passed: false
   ---

   # [Task Title]

   ## Steps
   ### Step 1: [Name]
   - [ ] [Task 1]
   - [ ] [Task 2]

   ### Step 2: [Name]
   - [ ] [Task 1]
   ```

### Phase 3: Execute Implementation

1. **Follow the Plan**
   - Work through steps in order
   - Update step status as you go
   - Mark discoveries in the work document

2. **During Implementation**
   - Be explicit about what you're doing
   - Call out decisions as you make them
   - Update `updated:` timestamp

### Phase 4: Quality Gates (Mandatory)

After implementation, run quality gates in a closed loop:

1. **Type Check**
   ```bash
   [package-manager] typecheck
   ```

2. **Lint**
   ```bash
   [package-manager] lint
   ```

3. **Build**
   ```bash
   [package-manager] build
   ```

4. **Tests (if applicable)**
   ```bash
   [package-manager] test
   ```

**Loop until all pass** - Fix and re-run failing gates

### Phase 5: Agent Scrutiny (for non-trivial changes)

After quality gates pass, launch parallel review agents:

```bash
# For code changes:
Agent 1: code-simplicity-reviewer
Agent 2: security-sentinel
Agent 3: performance-oracle
Agent 4: pattern-recognition-specialist
Agent 5: architecture-strategist

# For database changes, add:
Agent 6: data-migration-expert
Agent 7: data-integrity-guardian

# For deployments, add:
Agent 8: deployment-verification-agent
```

**Severity Classification:**
- **P1**: Must fix before marking work complete
- **P2**: Should fix if time permits
- **P3**: Track for future

### Phase 6: Complete and Archive

1. **Update Work Document**
   ```yaml
   status: completed
   completed: 2026-01-12
   quality_gates_passed: true
   scrutiny:
     p1_findings: 0
     p2_findings: 2
     p3_findings: 1
   ```

2. **Create Todos for Remaining Issues**
   - P2 findings → Create P2 todos
   - P3 findings → Create P3 todos

3. **Archive/Mark Complete**
   - Plans: Move to archive
   - Todos: Mark status: complete

## Key Principles

- **Quality First**: Quality gates must pass before scrutiny
- **Parallel Agents**: Launch review agents simultaneously
- **Severity-Based**: P1 blocks completion, P2/P3 tracked
- **Transparent**: Keep work document updated throughout
- **Complete**: Don't mark complete until user confirms

## Quality Checklist

- [ ] All steps executed or documented
- [ ] Quality gates passing (typecheck, lint, build, tests)
- [ ] Agent scrutiny completed
- [ ] All P1 findings addressed
- [ ] P2/P3 findings documented in todos
- [ ] Work document updated with completion status
- [ ] User confirms work is complete

## Common Pitfalls

- **Skipping Quality Gates**: Always run all gates before scrutiny
- **Sequential Agents**: Launch all agents in parallel for speed
- **Ignoring P1s**: P1 findings must be fixed before completion
- **Forgetting Updates**: Keep work document current throughout
- **Early Completion**: Don't mark complete until user confirms

## Quick Usage Examples

**Example 1: Work from a plan**
> User: `/workflows:work plans/active/2026-01-12-add-auth.md`

> Agent: I'll implement the authentication feature from the plan. Let me work through the steps...

[Executes plan, runs quality gates, launches scrutiny agents, completes]

**Example 2: Work from a todo**
> User: `/workflows:work todos/123-pending-p2-fix-n-plus-one.md`

> Agent: I'll fix the N+1 query issue described in the todo...

[Implements fix, verifies with queries, runs quality gates, completes]

**Example 3: Work from task description**
> User: `/workflows:work Add password reset flow`

> Agent: I'll create a plan and implement the password reset feature...

[Creates mini-plan, executes, quality gates, scrutiny, completes]

## Output Format

### Work Complete Summary
```markdown
## Work Complete: [Title]

**Files Modified:**
- `src/auth/reset.ts` (new)
- `src/auth/reset.test.ts` (new)
- `src/components/ResetForm.tsx` (modified)

**Quality Gates:**
- ✅ Type Check: Passing
- ✅ Lint: Passing
- ✅ Build: Passing
- ✅ Tests: Passing (8/8)

**Scrutiny Results:**
- P1 Findings: 0
- P2 Findings: 1 (performance: consider caching)
- P3 Findings: 2 (code cleanup opportunities)

**Todos Created:**
- `124-pending-p3-add-password-reset-caching.md`
- `125-pending-p3-refactor-reset-validator.md`

**Status:** ✅ Complete
```

## Related Commands

- `/workflows:plan` - Create detailed plans before work
- `/workflows:review` - Review existing code with agents
- `/workflows:compound` - Document learnings after work
- `/todo` - Create todos for P2/P3 findings

## Related Skills

- `file-todos` - For tracking P2/P3 findings
- `quality-severity` - For severity classification
- `plan-manager` - For work document management
