---
name: bug-fix-workflow
description: Systematic workflow for debugging and fixing issues
---

# Bug Fix Workflow

Systematic approach to identifying, understanding, and fixing bugs in the Astro application.

## Prerequisites

**Before starting this workflow, ensure you have full context:**

1. Read the project's `CLAUDE.md` file at the root directory
2. Review `.claude/skills/index.md` to discover available skills
3. Understand the project architecture (Astro + React, Convex backend, PM2 deployment)
4. Review relevant code sections before making changes

## Workflow

### 1. Reproduce the Bug

First, clearly reproduce the issue:

```bash
# Check if dev server is running
# Use PM2 if available (check coder-environment skill), or check the process manually
# If running, visit the site directly

# If dev server is NOT running:
lsof -i :[dev-port]  # Check if port is in use
[package-manager] start   # Only if both checks confirm nothing is running

# Visit the affected page/route
# Note exact steps to reproduce
# Take screenshots of the issue
```

### 2. Gather Context

Use Claude to explore relevant code:

```
Read the files that handle [affected feature]
Look for recent changes to [affected area]
```

**Check project context from CLAUDE.md:**
- Dev server configuration (check process manager and port)
- Backend services may be running via containers
- Check logs for errors

### 3. Identify Root Cause

Ask Claude to analyze:

```
Analyze why [bug description] is happening
Check git history for recent changes to [file]
```

### 4. Create Fix Plan

Before coding, create a plan:

```
Think about how to fix [bug description]
What could break if we change [code area]?
```

**Consider CLAUDE.md conventions:**
- Astro components for static content, React for interactivity
- Tailwind CSS for styling
- Use existing shared components when possible
- Follow project file organization

### 5. Implement Fix

Apply the solution and verify:

- Run `[package-manager] run [typecheck-script]`
- Run `[package-manager] run [lint-script]`
- Test the fix manually
- Run relevant tests

### 6. Add Regression Test

Create a test to prevent this bug from returning:

```typescript
test("[bug description] should not occur", async ({ page }) => {
  // Test that verifies the fix
});
```

### 7. Verify & Commit

- All tests pass
- Manual testing confirms fix
- No new issues introduced

## Common Bug Patterns

### Build Errors

1. Check `[package-manager] run [typecheck-script]` for type errors
2. Check imports and file paths
3. Verify component syntax for your framework

### Styling Issues

1. Check Tailwind class names
2. Verify CSS specificity
3. Check responsive breakpoints
4. Inspect element in browser

### Runtime Errors

1. Check browser console
2. Check server logs (use PM2 if available, or container logs for Docker):

   ```bash
   # Check process manager logs (e.g., PM2)
   # View recent log entries

   # Container logs (if using containers)
   # View logs to diagnose issues
   ```

3. Verify data fetching
4. Check async/await usage

### Navigation Issues

1. Verify route exists in `src/pages/`
2. Check link hrefs are correct
3. Test dynamic routes with slugs

## Quick Commands

```bash
# Type checking
[package-manager] run [typecheck-script]

# Linting
[package-manager] run [lint-script]

# Auto-fix linting
[package-manager] run [lint:fix-script]

# Run all tests
[package-manager] run [test-script]

# Run specific test
[package-manager] run [test-script] -- tests/bug-name.spec.ts
```

## Tips

- Take screenshots of visual bugs for reference
- Check git blame for recent changes to problematic code
- Use systematic debugging: isolate variables, check assumptions
- For complex bugs, break down the problem into smaller testable parts
- Always check server status before starting/stopping servers
