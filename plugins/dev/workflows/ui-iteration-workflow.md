---
name: ui-iteration-workflow
description: Iterative UI development with visual feedback
---

# UI Iteration Workflow

Use this workflow when building or refining UI components to achieve high-quality visual results through iteration.

## Prerequisites

**Before starting this workflow, ensure you have full context:**

1. Read the project's `CLAUDE.md` file at the root directory
2. Review `.claude/skills/index.md` to discover available skills
3. Understand the design system and styling approach (Tailwind CSS)
4. Check existing components in `src/components/` and `src/components/shared/`
5. Review existing page patterns in `src/pages/`

**Important Design Guidelines from CLAUDE.md:**
- **NEVER** use Inter font - it's overused. Choose distinctive fonts.
- **AVOID** purple gradient on white - generic AI aesthetic.
- Use Tailwind utility classes for styling
- Check existing components before creating new ones
- Use `cn()` utility from `@/lib/utils.ts` for conditional classes

## Workflow

### 1. Start with the Frontend Design Skill

Invoke the frontend-design skill to set aesthetic direction:

```
Use the /compound-engineering:frontend-design skill to build a [component/page]
```

Alternatively, use the Skill tool with `skill: "compound-engineering:frontend-design"`

**When invoking the skill, remind it to:**
- First read `CLAUDE.md` for project context
- Follow existing design patterns
- Avoid generic AI aesthetics

### 2. Implement Initial Version

Let Claude create the first version of the component.

### 3. Take Screenshot

```bash
# Using Playwright - run specific test
[package-manager] run [test-script] -- tests/component-name.spec.ts

# Or manually visit in browser and screenshot
# Check if the dev server is running (use PM2 if available)
```

### 4. Review and Iterate

Give feedback on the visual result:

- "Make it more minimalist"
- "Add more spacing"
- "Use a bolder color palette"
- "Try a different font pairing"

### 5. Repeat 2-4

Iterate 2-3 times minimum. Claude's outputs improve significantly with iteration.

### 6. Final Polish

Once direction is solid, ask for refinements:

- "Check responsive design"
- "Verify accessibility"
- "Test dark mode support"
- "Add micro-interactions"

### 7. Quality Gates
Always run before committing:

```bash
[package-manager] run [typecheck-script]
[package-manager] run [lint-script]
[package-manager] run [build-script]
```

### 8. Commit

When satisfied, commit the changes.

## Best Practices

- **Be specific** about visual preferences
- **Reference existing designs** in the project for consistency
- **Check responsive breakpoints** after each major change
- **Use Playwright snapshots** to catch regressions
- **Test on multiple viewports** (mobile, tablet, desktop)

## Commands

```bash
# Run specific Playwright test
[package-manager] run [test-script] -- tests/component-name.spec.ts

# Update visual snapshots (after intentional changes)
[package-manager] run [test-script] -- --update-snapshots
```

**IMPORTANT:** Check your workspace environment for headed mode support. Some Coder workspaces may not support headed mode (visible browser). Use the preview server URL for visual verification.

## When to Use

- Building new pages
- Creating new components
- Redesigning existing UI
- Adding visual features
- Design system development
