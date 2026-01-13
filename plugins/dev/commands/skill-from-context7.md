---
name: skill-from-context7
description: Generate a skill from Context7 MCP documentation response
---

# /skill:from-context7

Generates a properly formatted skill file from Context7 MCP documentation in the current conversation.

## What It Does

This command captures the Context7 MCP response from the conversation and generates a new skill file with:

- **Proper YAML frontmatter** (name, description, updated date, source metadata)
- **Structured content** extracted from the documentation
- **Code examples** preserved in markdown
- **Appropriate file location** in the marketplace plugin structure

## When to Use

- **After using Context7** - When you've just retrieved documentation via Context7 MCP
- **Creating framework skills** - For React, Next.js, Astro, or other framework docs
- **Library documentation** - When you want to preserve up-to-date library knowledge
- **API references** - For capturing API patterns and usage

## Usage

```bash
/skill:from-context7
```

## How It Works

### 1. Analyzes Conversation

Scans the current conversation for:

- Context7 MCP tool invocations (`resolve-library-id`, `query-docs`)
- Documentation responses
- Code examples
- Version information

### 2. Prompts for Metadata

Asks for:

- **Skill name** - kebab-case identifier (e.g., `latest-nextjs`, `react-compiler`)
- **Description** - Brief summary of what the skill covers
- **Target plugin** - Which plugin to add the skill to (e.g., `nextjs`, `react`, `astro`)

### 3. Generates Skill File

Creates `plugins/{plugin}/skills/{skill-name}/SKILL.md` with:

```yaml
---
name: skill-name
description: Brief description
updated: YYYY-MM-DD
source: context7
library: library-name
version: detected-version
---
```

### 4. Structured Content

Organizes documentation into sections:

- **Overview** - Introduction and purpose
- **Key Features** - Main functionality
- **Code Examples** - Usage examples from docs
- **API Reference** - Important API patterns
- **Best Practices** - Usage recommendations
- **Migration Notes** - Version-specific guidance
- **Resources** - Links to official documentation

## Arguments

$ARGUMENTS

You can pass arguments directly:

```bash
/skill:from-context7 nextjs-middleware
```

Or with more detail:

```bash
/skill:from-context7 react-compiler --plugin react --description "React Compiler automatic optimization"
```

## Example Workflow

```bash
# 1. Query Context7 for documentation
How do I use Next.js 16 cache components? use context7

# 2. Generate skill from the response
/skill:from-context7

# 3. Provide prompted information:
#    Skill name: nextjs-cache-components
#    Description: Next.js 16 Cache Components programming model
#    Plugin: nextjs

# 4. Skill created:
#    plugins/nextjs/skills/nextjs-cache-components/SKILL.md
```

## Output

### Success

```
✓ Generated skill: plugins/nextjs/skills/nextjs-cache-components/SKILL.md
✓ Skill name: nextjs-cache-components
✓ Description: Next.js 16 Cache Components programming model
✓ Source: context7
✓ Library: /vercel/next.js
✓ Version: 16.0

Next steps:
- Review and edit the generated skill
- Run /update-indexes to add to skill index
- Test the skill with /skill nextjs-cache-components
```

### No Context7 Content Found

If no Context7 response is detected, you'll be prompted to:

1. Paste the documentation manually
2. Provide the library name
3. Specify the version (if known)

## File Structure

Generated skills follow the marketplace convention:

```
plugins/
├── nextjs/
│   └── skills/
│       └── nextjs-cache-components/
│           └── SKILL.md
├── react/
│   └── skills/
│       └── react-compiler/
│           └── SKILL.md
└── dev/
    └── skills/
        └── context7-skill-generator/
            └── SKILL.md
```

## Best Practices

1. **Use specific names** - `nextjs-middleware` not `nextjs-stuff`
2. **Keep descriptions brief** - One sentence summary
3. **Review before using** - Always check and edit generated skills
4. **Add project context** - Supplement with your project's patterns
5. **Update regularly** - Re-run when libraries have new versions

## Integration with Context7 MCP

This command works seamlessly with Context7 MCP when configured in your MCP settings:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

## Related Commands

- `/project:setup` - Generate CLAUDE.md from marketplace plugins
- `/update-indexes` - Update skill, workflow, and plan indexes

## Related Skills

- `context7-skill-generator` - The underlying skill for Context7 extraction

## Troubleshooting

### No Context7 content found

**Cause**: No Context7 tools were invoked in this conversation

**Solution**: Either:
- Use Context7 first (`use context7` in your prompt)
- Paste documentation manually when prompted

### Cannot determine plugin location

**Cause**: Unknown library or framework

**Solution**: Specify the plugin manually:
```bash
/skill:from-context7 my-skill --plugin custom
```

### Invalid skill name

**Cause**: Contains spaces or special characters

**Solution**: Use kebab-case:
```bash
/skill:from-context7 my-cool-skill  # ✓ Valid
/skill:from-context7 My Cool Skill  # ✗ Invalid
```
