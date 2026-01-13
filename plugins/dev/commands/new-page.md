---
name: new-page
description: Create a new application page following project conventions
---

# Create New Application Page

Create a new application page at the specified route following the project's established patterns.

## Steps

1. **Discover the project structure**

   - **First, check for `CLAUDE.md`** at the project root - read it to find documented tech stack, frameworks, and conventions
   - If CLAUDE.md exists, use the documented framework and patterns directly
   - Otherwise, identify the framework from `package.json` dependencies

2. **Review existing pages** - If CLAUDE.md didn't specify patterns, find 2-3 similar pages to understand:

   - File naming conventions (kebab-case, camelCase, PascalCase)
   - Component structure and imports
   - Layout usage patterns
   - Meta/SEO handling approach
   - Styling approach (CSS modules, Tailwind, styled-components, etc.)

3. **Create the page** following discovered patterns:

   - Use the correct file extension (`.tsx`, `.jsx`, `.vue`, `.svelte`, etc.)
   - Match existing component structure and imports
   - Apply the same SEO/meta pattern (if applicable)
   - Use the project's layout/wrapper pattern
   - Follow the styling system already in use
   - Reuse shared components where applicable

4. **Verify the implementation**:

   - Run typecheck if configured: check `package.json` for "typecheck", "check", "tsc", "vue-tsc" scripts
   - Run linter if configured: check for "lint" script
   - Build the project if typecheck/lint unavailable
   - Check the page renders at the correct route

5. **Add to navigation** (optional)
   - Only if explicitly requested by the user
   - Follow existing navigation patterns (config files, nav components, etc.)

## Arguments

$ARGUMENTS

**Examples**:

- `/new-page dashboard/analytics` - Creates a new dashboard analytics page
- `/new-page about/team` - Creates a new about team page

The route path will be interpreted based on the detected framework's conventions.
