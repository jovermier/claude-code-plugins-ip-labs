---
name: test-ui
description: Run Playwright tests and verify visual changes
---

# Test UI with Playwright

Run E2E tests to verify visual changes and catch regressions.

## Workflow

1. **Check if dev server is running**:

   ```bash
   # Check if dev server is running (use PM2 if available)
   lsof -i :[dev-port]          # Check if port is in use
   ```

   Only start dev server if port is free:

   ```bash
   [package-manager] start
   ```

2. **Run Playwright tests**:

   ```bash
   [package-manager] run [test-script]
   ```

3. **Review results** - Check for:

   - Failed tests
   - Visual regressions in screenshots
   - Console errors
   - Network issues

4. **If tests fail, check server logs**:

   ```bash
   # Check process manager logs (e.g., PM2 if available)
   # View recent log entries to diagnose issues

   # Check container logs (if using containers)
   # View logs to diagnose issues
   ```

5. **Update snapshots** (if changes are intentional):

   ```bash
   [package-manager] run [test-script] -- --update-snapshots
   ```

**IMPORTANT:** Check your workspace environment for headed mode support. Some workspaces may not support headed mode (visible browser) for Playwright tests. Use the preview server URL for visual verification.

## When to Use

- After UI changes
- Before committing visual work
- When adding new pages/routes
- After component updates

## Arguments

$ARGUMENTS

**Examples**:

- `/test-ui` - Run all tests
- `/test-ui home` - Run tests matching "home"

**Note:** Headed mode support depends on your workspace configuration.
