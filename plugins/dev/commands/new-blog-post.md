---
name: new-blog-post
description: Create a new blog post following content patterns
---

# Create New Blog Post

Create a new markdown blog post in the content collection.

## Steps

1. **Review existing posts** - Check `src/content/blog/` for format and style
2. **Create the markdown file** with:
   - SEO-friendly filename (kebab-case)
   - Frontmatter (title, description, date, publish: true/false)
   - Proper markdown formatting
   - Code examples with syntax highlighting
   - Internal links to related posts

3. **Frontmatter template**:
   ```yaml
   ---
   title: "Your Post Title"
   description: "A compelling description for SEO and previews"
   date: 2026-01-09
   publish: true
   tags: ['tag1', 'tag2']
   ---
   ```

4. **Add images** (if needed):
   - Place in `public/images/blog/`
   - Reference with absolute paths: `/images/blog/filename.webp`

5. **Test rendering**:
   - Build the site: `[package-manager] run [build-script]`
   - Check blog route
   - Verify formatting and links

## Arguments
$ARGUMENTS

**Example**: `/new-blog-post "Astro Performance Tips"`

Creates a new blog post with proper frontmatter and markdown structure
