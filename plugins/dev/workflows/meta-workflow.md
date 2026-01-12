---
name: meta-workflow
description: Master workflow that intelligently selects and composes other workflows based on task complexity
---

# Meta-Workflow: Adaptive Task Execution

This is the master workflow that determines the best approach for any task and composes specialized workflows as needed.

## The 7-Step Process (Updated: Quality Gates Before Scrutiny)

### Step 1: Plan Approach

**Assess the task and determine strategy**

Ask:

- What is the user asking for?
- What context do I already have?
- What workflows might apply?
- Is this simple enough to skip directly to execution?

**Decision Matrix:**

| Your Request      | Strategy                                | Example                       |
| ----------------- | --------------------------------------- | ----------------------------- |
| "What does X do?" | Direct response (information query)     | "What does this function do?" |
| "Fix typo"        | Direct execution                        | "Fix typo in heading"         |
| "New feature"     | Select workflow(s) - TDD + UI-iteration | "Add contact form"            |
| "Bug fix"         | Use bug-fix-workflow                    | "Navigation not working"      |
| "UI work"         | Use ui-iteration-workflow               | "Redesign hero section"       |
| "Tests needed"    | Use tdd-workflow                        | "Add form validation"         |
| "Complex task"    | Compose multiple workflows              | "New e-commerce checkout"     |

**Output:** Decision + selected workflow(s) OR "skip to step 4"

---

### Step 2: Explore (If Needed)

**Gather missing information**

Only execute if Step 1 determined more context is needed.

Actions:

- Read relevant files (use Glob/Grep to find them)
- Examine existing patterns in the codebase
- Check dependencies and imports
- Review similar existing implementations
- Look at git history for context
- **Update or create context documents** for areas explored

**Context Capture:**

- When exploring a new area, check if a context doc exists: `.claude/context/[area]--context.md`
- If not, create one using the context template (see [`plan-manager`](.claude/skills/plan-manager/SKILL.md) skill)
- Reference context docs with links, not duplicated content
- Run `update-indexes` after creating new context docs

**When to explore:**

- New feature area you haven't worked with
- Bug fix where root cause is unclear
- Task requires understanding existing patterns
- User asks something open-ended

**Output:** Return to Step 1 with updated context

---

### Step 3: Plan Solution

**Create detailed implementation plan**

Only execute if Step 1 determined a workflow is needed OR if task requires planning.

Actions:

- Based on selected workflow(s), create step-by-step plan
- List files that will be modified
- Identify potential risks or edge cases
- Specify testing approach
- Estimate complexity

**Plan Capture:**

- Create a plan document: `.claude/plans/active/YYYY-MM-DD--[slug].md`
- Use the plan template (see [`plan-manager`](.claude/skills/plan-manager/SKILL.md) skill)
- Set `status: planning` initially
- Reference related context documents

**If multiple workflows apply:**

- Compose them logically (e.g., TDD for behavior, then UI-iteration for visuals)
- Create unified plan that addresses both

**Output:** Detailed implementation plan + get user approval

---

### Step 3.5: Plan Scrutiny (Mandatory for All Plans)

**Multi-agent validation of plan and exploration completeness**

**CRITICAL: All subagents MUST read CLAUDE.md before starting their review**

Before proceeding to execution, validate the plan using multiple specialized subagents to ensure:

1. **Exploration Completeness** - 95%+ confidence all needed context was gathered
2. **Plan Viability** - 95%+ confidence the plan will work considering all edge cases

**Execute Parallel Scrutiny Agents:**

Each agent MUST be instructed to:
1. First read the full `CLAUDE.md` file at the project root
2. Review the **Skills Index** at `.claude/skills/index.md` to discover available skills
3. Then read the relevant workflow file(s)
4. Then perform their specialized review (invoking skills as needed)

```bash
# Launch multiple specialized review agents in parallel
# Each agent scrutinizes the plan from a different perspective
# AGENT PROMPT TEMPLATE:
# "First, read the CLAUDE.md file at the project root to understand
#  the full project context, conventions, and guidelines.
#  Then review .claude/skills/index.md to discover available skills.
#  Then perform your review as:"

Agent 1: Context Completeness Reviewer
  INSTRUCTION: "First read CLAUDE.md. Then review .claude/skills/index.md. Then review the plan for:
  - Was the explore step thorough?
  - Are there gaps in our understanding of the codebase?
  - Did we miss relevant files, patterns, or dependencies?
  - Are context documents accurate and complete?
  - Use relevant skills (e.g., plan-manager) for deeper analysis if needed."

Agent 2: Edge Case Analyzer
  INSTRUCTION: "First read CLAUDE.md. Then review .claude/skills/index.md. Then review the plan for:
  - What edge cases might break this implementation?
  - Are error scenarios handled?
  - What about empty states, null/undefined values, race conditions?
  - Does the plan account for accessibility, responsive design, i18n?
  - Use relevant skills for framework-specific edge case analysis if needed."

Agent 3: Architecture & Patterns Reviewer
  INSTRUCTION: "First read CLAUDE.md. Then review .claude/skills/index.md. Then review the plan for:
  - Does this follow project conventions described in CLAUDE.md?
  - Are we introducing anti-patterns?
  - Will this integrate cleanly with existing code?
  - Are dependencies managed correctly?
  - Use framework skills (latest-astro, latest-react, etc.) for framework-specific review if needed."

Agent 4: Risk Assessment Reviewer
  INSTRUCTION: "First read CLAUDE.md. Then review .claude/skills/index.md. Then review the plan for:
  - What could go wrong during implementation?
  - Are there potential breaking changes?
  - What's the rollback strategy?
  - Are test cases comprehensive?
  - Use playwright-test skill for test strategy review if needed."
```

**Scrutiny Process:**

1. Each agent independently reviews the plan document
2. Agents provide specific findings with:
   - **Severity**: Critical / High / Medium / Low
   - **Finding**: Description of concern
   - **Recommendation**: Specific action to address
   - **Confidence Score**: 0-100% on plan viability
3. Aggregate findings and address any Critical/High severity issues
4. Update plan document with scrutiny results in `scrutiny:` section
5. Get final user approval if significant changes were made

**Output:** Validated plan with scrutiny findings + confidence scores OR refined plan

---

### Step 4: Execute

**Implement the solution**

Actions:

- Follow the plan from Step 3 (or execute directly if skipped from Step 1)
- Create/modify files as needed
- Follow project conventions from CLAUDE.md
- Use appropriate tools (Edit, Write, etc.)
- Work systematically through the plan

**During execution:**

- Be explicit about what you're doing
- Call out decisions as you make them
- Pause if you encounter something unexpected
- **Update plan document**: Mark each step's status as you progress (`pending` → `in_progress` → `completed`)
- **Update `updated:` timestamp** whenever you modify the plan

**Plan Tracking:**

- Set `status: in_progress` and `started: <date>` when beginning execution
- Update individual step statuses as you work through them
- Add notes to steps for discoveries, deviations, or decisions

**Output:** Implementation complete

---

### Step 5: Quality Gates

**Validate and verify**

**Always run these gates in a closed loop until all pass:**

Read the project's `CLAUDE.md` file to find the Quality Gates section. This section should define the specific commands to run for:

1. **Type Checks** - Type checking and validation
2. **Lint Check** - Code quality and style enforcement
3. **Build Verification** - Production build validation
4. **Run Tests** (if applicable) - Unit, integration, and E2E tests

**If CLAUDE.md doesn't have a Quality Gates section:**

Look for common scripts in `package.json`:
- Type checking scripts (e.g., typecheck, check, validate)
- Linting scripts (e.g., lint, lint:fix)
- Build scripts (e.g., build, compile)
- Test scripts (e.g., test, test:unit, test:e2e)

5. **Manual Verification**
   - Did I address the user's request?
   - Did I follow the selected workflow?
   - Are there any obvious issues?
   - Should I suggest next steps?

**If any gate fails:**

- **Diagnose the failure first:**

  ```bash
  # For test failures - check server logs
  # Use PM2 if available (check coder-environment skill), or container logs

  # Check process status
  # Use appropriate process manager commands
  ```

- Fix the issue
- Re-run the gate
- Don't proceed until all pass
- **Loop until all gates pass** - This is a tight feedback loop for automated checks

**Output:** All quality gates passing

---

### Step 6: Implementation Scrutiny (Mandatory for All Non-Trivial Code Changes)

**Multi-agent validation of implementation quality**

**CRITICAL: All subagents MUST read CLAUDE.md before starting their review**

After quality gates pass, validate the implementation using multiple specialized subagents to ensure:

1. **Best Practices** - 95%+ confidence code follows best practices
2. **Edge Case Coverage** - 95%+ confidence all edge cases are handled
3. **No Regressions** - 95%+ confidence no new bugs were introduced
4. **Documentation** - 95%+ confidence plan status was properly documented

**Why this comes AFTER quality gates:**

- Agents review code that already passes all automated checks
- More efficient - no need to re-scrutinize after fixing typecheck/lint errors
- Final "green light" before completion

**Execute Parallel Scrutiny Agents:**

Each agent MUST be instructed to:
1. First read the full `CLAUDE.md` file at the project root
2. Review the **Skills Index** at `.claude/skills/index.md` to discover available skills
3. Then read the relevant workflow file(s)
4. Then perform their specialized review (invoking skills as needed)

```bash
# Launch multiple specialized review agents in parallel
# Each agent scrutinizes the implementation from a different perspective
# AGENT PROMPT TEMPLATE:
# "First, read the CLAUDE.md file at the project root to understand
#  the full project context, conventions, and guidelines.
#  Then review .claude/skills/index.md to discover available skills.
#  Then perform your review as:"

Agent 1: Code Quality Reviewer
  INSTRUCTION: "First read CLAUDE.md. Then review .claude/skills/index.md. Then review the implementation for:
  - Does this code follow project conventions in CLAUDE.md?
  - Are variable names clear and descriptive?
  - Is the code DRY (Don't Repeat Yourself)?
  - Are functions single-purpose and focused?
  - Are there any code smells or anti-patterns?
  - Use framework skills (latest-astro, latest-react, etc.) for framework-specific review if needed."

Agent 2: Edge Case & Error Handling Reviewer
  INSTRUCTION: "First read CLAUDE.md. Then review .claude/skills/index.md. Then review the implementation for:
  - Are all error cases handled?
  - What happens with null/undefined values?
  - Are race conditions prevented?
  - Are boundaries and limits validated?
  - Is defensive programming applied appropriately?
  - Use framework skills for framework-specific edge case patterns if needed."

Agent 3: Integration & Regression Reviewer
  INSTRUCTION: "First read CLAUDE.md. Then review .claude/skills/index.md. Then review the implementation for:
  - Does this integrate cleanly with existing code?
  - Could this break existing functionality?
  - Are all imports and dependencies correct?
  - Did we properly update related files?
  - Are type definitions accurate and complete?
  - Use framework skills for integration patterns if needed."

Agent 4: Testing & Documentation Reviewer
  INSTRUCTION: "First read CLAUDE.md. Then review .claude/skills/index.md. Then review the implementation for:
  - Are tests comprehensive for the changes?
  - Do tests cover edge cases?
  - Is the plan document updated with completion status?
  - Are comments clear where needed?
  - Will future maintainers understand this code?
  - Use playwright-test skill for test quality review if tests were modified."

Agent 5: Security & Performance Reviewer
  INSTRUCTION: "First read CLAUDE.md. Then review .claude/skills/index.md. Then review the implementation for:
  - Are there any security vulnerabilities (XSS, injection, etc.)?
  - Are user inputs properly validated?
  - Could this introduce performance issues?
  - Are queries optimized?
  - Is memory usage appropriate?
  - Use relevant skills for framework-specific security patterns if needed."
```

**Scrutiny Process:**

1. Each agent independently reviews all changed files
2. Agents provide specific findings with:
   - **Severity**: Critical / High / Medium / Low
   - **File**: Affected file path
   - **Line**: Specific line reference
   - **Finding**: Description of concern
   - **Recommendation**: Specific action to address
   - **Confidence Score**: 0-100% on implementation quality
3. Aggregate findings and address any Critical/High severity issues
4. If Critical/High issues found:
   - Fix them
   - Re-run quality gates (Step 5) - loop back
   - Re-run scrutiny (Step 6) - loop back
5. Update plan document with scrutiny results in `scrutiny:` section

**Output:** Validated implementation with scrutiny findings + confidence scores

---

### Step 7: Plan Completion (Two-Stage Confirmation)

**Finalize and archive with user confirmation and quality gate verification**

#### Stage 1: User Confirmation

Before marking any work as complete, ask the user:

> "I believe the work is complete. Do you agree, or are there changes/problems you've uncovered?"

- **If user confirms**: Proceed to Stage 2
- **If user identifies issues**: Address them, then return to Stage 1
- **If user requests changes**: Make changes, then return to Stage 1

**Do NOT set `status: completed` until after Stage 2 passes.**

#### Stage 2: Quality Gate Verification

Only after user confirms, run the quality gates defined in the project's `CLAUDE.md`:

```bash
# Read CLAUDE.md Quality Gates section and run the defined commands:
# - Type checks
# - Linting
# - Build
# - Tests
```

**If CLAUDE.md doesn't define quality gates**, check `package.json` for common scripts.

**If all gates pass:**

- Set `status: completed`
- Set `completed: <date>`
- Set `quality_gates_passed: true`
- The auto-archive hook will automatically move the plan to archive

**If any gate fails:**

- Inform the user: "Quality checks failed. Would you like me to fix these now, or defer completion?"
- If user wants fixes: Fix issues, re-run gates, then repeat Stage 2
- If user wants to defer: Keep status as `in_progress`, add note about failed gates

**Output:** Summary of changes + verification status + archiving confirmation

---

## Workflow Composition Examples

### Example 1: New Contact Form (Composed)

```
Step 1: New feature → Select TDD + UI-iteration workflows
Step 2: Explore existing forms, validation patterns
Step 3: Plan - Combine TDD (behavior) + UI-iteration (visuals)
Step 3.5: Plan Scrutiny - Multi-agent review of plan completeness
Step 4: Execute
        - Write tests first (TDD)
        - Implement form behavior
        - Design and iterate on UI (UI-iteration)
Step 5: Quality gates - Loop until all pass (typecheck, lint, tests, build)
Step 6: Implementation Scrutiny - Multi-agent code review of passing code
Step 7: Plan completion - Two-stage confirmation:
        Stage 1: Ask user "Do you agree the work is complete?"
        Stage 2: Run quality gates
        → Archive plan document
```

### Example 2: Simple Typo Fix (Direct)

```
Step 1: Simple change → Skip to step 4
Step 2: (skipped)
Step 3: (skipped)
Step 3.5: (skipped - no plan)
Step 4: Execute - Fix typo directly
Step 5: Quality gates - typecheck (only)
Step 6: (skipped - trivial change)
Step 7: (skipped - no plan)
```

### Example 3: Bug in Navigation (Single Workflow)

```
Step 1: Bug fix → Select bug-fix-workflow
Step 2: Explore - Read navigation code, check console
Step 3: Plan - Follow bug-fix-workflow planning
Step 3.5: Plan Scrutiny - Validate root cause analysis
Step 4: Execute - Implement fix
Step 5: Quality gates - Loop until pass (typecheck, lint, manual test)
Step 6: Implementation Scrutiny - Review fix for edge cases
Step 7: Plan completion - Two-stage confirmation:
        Stage 1: Ask user "Do you agree the work is complete?"
        Stage 2: Run quality gates
        → Archive plan document
```

### Example 4: Redesign Homepage (Composed)

```
Step 1: UI work → Select UI-iteration workflow
Step 2: Explore - Review existing homepage, design system
Step 3: Plan - Follow UI-iteration planning
Step 3.5: Plan Scrutiny - Validate design approach
Step 4: Execute - Design and iterate through versions
Step 5: Quality gates - Loop until pass (typecheck, lint, visual regression)
Step 6: Implementation Scrutiny - Review component quality
Step 7: Plan completion - Two-stage confirmation:
        Stage 1: Ask user "Do you agree the work is complete?"
        Stage 2: Run quality gates
        → Archive plan document
```

---

## Quick Reference

### Available Workflows to Compose

| Workflow         | When to Use             | File                                         |
| ---------------- | ----------------------- | -------------------------------------------- |
| **TDD**          | Behavior-heavy features | `.claude/workflows/tdd-workflow.md`          |
| **UI Iteration** | Visual/design work      | `.claude/workflows/ui-iteration-workflow.md` |
| **Bug Fix**      | Debugging issues        | `.claude/workflows/bug-fix-workflow.md`      |

### Quality Gates Commands

Quality gates should be defined in the project's `CLAUDE.md` file under a "Quality Gates" section.

**If not defined in CLAUDE.md**, look for common scripts in `package.json`:

- Type checking scripts (typecheck, check, validate)
- Linting scripts (lint, lint:fix)
- Build scripts (build, compile)
- Test scripts (test, test:unit, test:e2e)

---

## Meta-Workflow Rules

1. **Always start at Step 1** - Never skip the approach decision
2. **Explore only when needed** - Don't read files unnecessarily
3. **Plan for complexity** - Simple tasks can skip Step 3 (and thus Step 3.5)
4. **Scrutinize all plans** - Step 3.5 is mandatory when Step 3 creates a plan
5. **Quality gates are closed-loop** - Step 5 loops until all pass (tight feedback loop)
6. **Scrutinize after gates pass** - Step 6 reviews code that already passes automated checks
7. **Scrutiny findings loop back** - Critical/High issues trigger Step 5 → Step 6 re-run
8. **Compose workflows intelligently** - Multiple workflows can apply
9. **Be explicit** - State which step you're on
10. **Ask when uncertain** - If the approach is unclear, ask the user

### When to Skip Steps

**Step 3.5 (Plan Scrutiny)** - Skip when:

- No plan was created (direct execution from Step 1)
- Change is trivial (typo, simple text update)

**Step 6 (Implementation Scrutiny)** - Skip when:

- No code was written (documentation only)
- Change is trivial (single-line fix, obvious typo)

**Step 7 (Plan Completion)** - Skip when:

- No plan was created (direct execution)

When in doubt, run scrutiny - it's better to over-verify than introduce bugs.

### Key Flow Pattern

**Quality Gates Loop (Step 5):** Tight automated feedback loop

- Run type checks → fail → fix → re-run
- Run linting → fail → fix → re-run
- Run build → fail → fix → re-run
- Repeat quickly until all pass

**Scrutiny Loop (Step 6):** Deeper human-like review

- Only runs AFTER all quality gates pass
- If issues found: fix → re-run Step 5 → re-run Step 6
- More expensive, so we want stable code first

---

## For Claude: How to Use This Workflow

When a user makes a request, mentally run through:

1. **What kind of request is this?** → Determines Step 1 output
2. **Do I need more context?** → Determines if Step 2 runs
3. **How complex is this?** → Determines if Step 3 runs
4. **Validate the plan** → Step 3.5 (if Step 3 ran)
5. **Execute** → Step 4
6. **Quality gates (closed loop)** → Step 5 (always - loop until pass)
7. **Scrutinize implementation** → Step 6 (if non-trivial)
8. **Complete plan with two-stage confirmation** → Step 7 (if plan exists)
   - Stage 1: Ask user "Do you agree the work is complete?"
   - Stage 2: Run quality gates
   - Then set status: completed

**Then explicitly state:**

> "Based on your request, I'll [describe approach]. Let me start by [Step X]."

This keeps the user informed and makes the workflow transparent.
