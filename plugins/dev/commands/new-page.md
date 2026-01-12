---
name: new-page
description: Create a new Astro page following project conventions
---

# Create New Astro Page

Create a new Astro page at the specified route following the project's established patterns.

## Steps

1. **Analyze the route** - Determine the correct path in `src/pages/`
2. **Review similar pages** - Check existing pages for patterns (index.astro, about.astro, etc.)
3. **Create the page** - Build the page with:

   - Proper SEO component usage
   - Layout integration
   - Responsive design
   - Tailwind CSS styling
   - Content from `src/components/shared/` where applicable

4. **Verify the implementation**:

   - Run `[package-manager] run [typecheck-script]`
   - Run `[package-manager] run [lint-script]`
   - Check the page renders at correct route
   - Verify responsive design

5. **Add to navigation** (if needed) - Update Header.astro with new link

## Arguments

$ARGUMENTS

**Example**: `/new-page services/seo-audit`

Creates a new page at `src/pages/services/seo-audit.astro`
