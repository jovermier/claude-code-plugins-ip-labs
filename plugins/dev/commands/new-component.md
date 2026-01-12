---
name: new-component
description: Create a new React or Astro component
---

# Create New Component

Create a new reusable component following project conventions.

## Decision Tree

**Ask**: Does this component need client-side interactivity?

- **Yes** → Create React component (`.tsx`)
- **No** → Create Astro component (`.astro`)

## Steps

1. **Check existing components** - Search `src/components/shared/` for similar patterns
2. **Determine component location**:
   - `src/components/shared/` - Reusable across pages
   - `src/components/` - Page-specific components
3. **Create the component** with:

   - TypeScript prop types
   - Tailwind CSS styling
   - Proper imports
   - JSDoc comments if needed

4. **Test the component**:

   - Import and use in a test page
   - Check responsive behavior
   - Verify accessibility
   - Run `[package-manager] run [typecheck-script]`

5. **Document** (if complex) - Add usage examples in comments

## Arguments

$ARGUMENTS

**Example**: `/new-component ProductCard`

Creates a new component with proper TypeScript types and Tailwind styling
