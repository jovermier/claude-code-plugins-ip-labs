---
name: tdd-workflow
description: Test-driven development workflow for Astro components
---

# Test-Driven Development Workflow

Use TDD when building new features or components that have clear, testable behavior.

## Prerequisites

**Before starting this workflow, ensure you have full context:**

1. Read the project's `CLAUDE.md` file at the root directory
2. Review `.claude/skills/index.md` to discover available skills (e.g., playwright-test, latest-astro, latest-react)
3. Understand the project conventions (Astro + React, Tailwind CSS, TypeScript)
4. Check if similar components already exist in `src/components/`
5. Review existing test patterns in `tests/`

## Workflow

### 1. Write Tests First
Create a Playwright test that defines the expected behavior:

```typescript
// tests/example-component.spec.ts
import { test, expect } from '@playwright/test';

test('component behaves correctly', async ({ page }) => {
  await page.goto('/');  // Use root-relative paths
  await expect(page.locator('selector')).toBeVisible();
});
```

**IMPORTANT**: Do NOT write any implementation code yet. Only tests.

### 2. Run Tests (Watch Them Fail)
```bash
[package-manager] run [test-script]
```

Confirm tests fail with clear error messages indicating what's missing.

**If tests fail unexpectedly** (not due to missing implementation):
```bash
# Check if server is running and healthy
# Use PM2 if available (check coder-environment skill), or check process manually
# View logs to diagnose issues
```

### 3. Write Minimal Implementation
Write just enough code to make tests pass. Don't over-engineer.

**Follow CLAUDE.md conventions:**
- Use Astro components (`.astro`) for static content
- Use React components (`.tsx`) when client interactivity is needed
- Use Tailwind utility classes for styling
- Use `@/` alias for imports
- Follow existing component patterns

### 4. Run Tests Again
```bash
[package-manager] run [test-script]
```

Iterate on the implementation until all tests pass.

### 5. Refactor (Optional)
Once tests pass, improve code quality while keeping tests green.

### 6. Quality Gates
Always run before committing:

```bash
[package-manager] run [typecheck-script]
[package-manager] run [lint-script]
[package-manager] run [build-script]
```

### 7. Commit
Commit both tests and implementation together.

## When to Use TDD
- New component behaviors
- Form validation
- User interactions (clicks, form submissions)
- Navigation flows
- Conditional rendering based on state

## When NOT to Use TDD
- Pure styling changes (use visual regression instead)
- Static content (use Playwright rendering tests)
- Exploration/prototyping

## Tips
- Be specific about expected behavior in test descriptions
- Test user-visible behavior, not implementation details
- Use `page.locator()` with semantic selectors
- Test edge cases (empty states, error states, loading states)
