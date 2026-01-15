# Claude Code Skills Architecture Guide

A comprehensive guide to structuring and breaking down complex Claude Code Skills using Progressive Disclosure Architecture (PDA).

> **Last Updated:** 2026-01-15
> **Based on:** Official Anthropic documentation and community best practices

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [When to Break Down Skills](#when-to-break-down-skills)
3. [Progressive Disclosure Architecture (PDA)](#progressive-disclosure-architecture-pda)
4. [The Three Pillars of PDA](#the-three-pillars-of-pda)
5. [Skill Structure Patterns](#skill-structure-patterns)
6. [Best Practices](#best-practices)
7. [Common Anti-Patterns](#common-anti-patterns)
8. [Implementation Examples](#implementation-examples)

---

## Core Principles

### The Orchestrator Philosophy

> **"A skill should be an orchestrator, not an encyclopedia."**

The fundamental insight from the Claude Code community is that complex skills should **route** to appropriate resources rather than containing all knowledge inline. This is achieved through Progressive Disclosure Architecture (PDA).

### Why This Matters

**Traditional "Encyclopedia" Approach:**
- Loads ALL documentation every time, even if you only need a small portion
- Slower response times due to unnecessary context processing
- Higher costs (every invocation uses maximum tokens)
- Maintenance nightmares (50KB+ monolithic files)
- Context pollution (unrelated documentation crowds working space)

**PDA "Orchestrator" Approach:**
- Loads only what's needed, when needed
- Faster responses (minimal context overhead)
- Lower costs (80-95% token savings typical)
- Easier maintenance (modular structure)
- Clear separation of concerns

### Token Efficiency Comparison

| Approach | Initial Load | On-Demand Load | Total | Savings |
|----------|--------------|----------------|-------|---------|
| Encyclopedia | 50KB (everything) | 0KB | 50KB | - |
| Orchestrator | 3KB (routing) | 5KB (targeted) | 8KB | 84% |
| Orchestrator (different task) | 3KB (routing) | 8KB (targeted) | 11KB | 78% |

---

## When to Break Down Skills

### Apply PDA When Your Skill:

- Has **>10KB** of reference documentation
- Supports **multiple distinct use cases** (each needs different docs)
- Integrates with **external APIs** or complex tools
- Requires **mechanical processing** (file conversion, API calls, data transformation)
- Will **grow over time** (more features means more documentation)

### Stay with Basic Skills When:

- Total size **<5KB** (all instructions fit comfortably)
- All information is **always needed** (no conditional loading benefit)
- **Simple workflow** (no external scripts or APIs needed)
- **Stable and focused** (won't grow significantly)

### Quick Self-Assessment

Answer these questions about your skill:

1. **Would my skill prompt exceed 10KB with all documentation?**
   - Yes → Consider PDA (reference files will help)

2. **Do different use cases need different documentation?**
   - Yes → Consider PDA (lazy loading will help)

3. **Does my skill call external APIs or tools?**
   - Yes → Consider PDA (scripts will help)

4. **Will I need to update or expand this skill regularly?**
   - Yes → Consider PDA (easier maintenance)

**If you answered "Yes" to 2 or more questions → Use PDA**

---

## Progressive Disclosure Architecture (PDA)

### What is PDA?

PDA is a design pattern built on three techniques that work together:

1. **Reference Files & Lazy Loading** - Heavy documentation lives in separate files, loaded on-demand
2. **Scripts for Mechanical Work** - API calls and data processing move to external scripts
3. **AI Resilience Layer** - Claude provides intelligence for edge cases, error interpretation, and UX

### How Claude Code Natively Supports PDA

**No special frameworks needed.** Claude Code's built-in tools provide everything:

1. **Read Tool** - Enables natural lazy loading of reference files
2. **Bash Tool** - Enables external script execution
3. **AI Reasoning** - Built-in intelligence for decision-making and error handling

### The Inflection Point

- **Below 5KB:** Basic skills are fine
- **Above 10KB:** PDA starts paying dividends quickly
- **At 50KB+:** PDA is essential (78-94% savings)

---

## The Three Pillars of PDA

### Pillar 1: Reference Files & Lazy Loading

Heavy documentation lives in separate files outside the skill. The skill loads only what's needed, when needed.

**Why This Matters:**
- Saves tokens by avoiding unnecessary loading (80–95% savings typical)
- Faster response times (less context to process)
- Easier maintenance (update specific references without touching skill logic)
- Scales gracefully (add new references without bloating core skill)

**Example Structure:**
```
plantuml/
├── SKILL.md                    # 3KB orchestrator
└── reference/
    ├── plantuml_sequence.md    # 8KB - loaded only for sequence diagrams
    ├── plantuml_class.md       # 10KB - loaded only for class diagrams
    ├── plantuml_flowchart.md   # 5KB - loaded only for flowcharts
    ├── plantuml_er.md          # 7KB - loaded only for ER diagrams
    └── plantuml_state.md       # 6KB - loaded only for state diagrams
```

### Pillar 2: Scripts for Mechanical Work

API calls, data processing, and complex operations move to external scripts. The skill prompt stays focused on decision logic.

**Why This Matters:**
- Scripts run outside Claude's context (zero token cost for implementation)
- Reusable across skills and projects
- Testable independently (unit tests, integration tests)
- Language-appropriate (use Python for data processing, Bash for system ops)

**Example Structure:**
```
notion-uploader/
├── SKILL.md                    # 3KB orchestrator
└── scripts/
    ├── upload.py               # Handles Notion API calls
    ├── format.py               # Converts markdown to Notion format
    └── validate.py             # Validates input before upload
```

### Pillar 3: AI Resilience Layer

Claude provides the intelligence layer for edge cases, error interpretation, and user experience.

**Why This Matters:**
- Handles ambiguity and unexpected situations gracefully
- Interprets errors from scripts and references in user-friendly ways
- Adapts to context (user skill level, project requirements)
- Asks clarifying questions when needed

**What AI Handles:**
- Decision-making (which references to load based on request analysis)
- Error interpretation (translating script errors into user-friendly guidance)
- Graceful degradation (handling errors with helpful suggestions)
- Context adaptation (adjusting to user skill level and project needs)

---

## Skill Structure Patterns

### Recommended Directory Structure

```
my-skill/
├── SKILL.md              # Main orchestrator (3-5KB max)
├── reference/            # Detailed docs loaded on-demand
│   ├── use-case-1.md
│   ├── use-case-2.md
│   └── api-details.md
└── scripts/              # Executable utilities
    ├── validate.py
    └── process.sh
```

### Three Core Patterns (Cover 90% of Use Cases)

#### Pattern 1: Generator Skills

Create content from user descriptions.

```
# [Type] Generator Skill

**Purpose:** Generate [content type] from user requirements

**Process:**
1. Analyze user requirements and goals
2. Generate [content type] using domain best practices
3. Validate output for correctness and quality
4. Present to user with refinement options

**Examples:**
- Diagram generators (PlantUML, Mermaid, draw.io)
- Report generators (test reports, status reports)
- Code scaffolding (boilerplate, project structures)
```

#### Pattern 2: Integrator Skills

Enable Claude to connect to external services.

```
# [Service] Integration Skill

**Purpose:** Integrate with [external service]

**Process:**
1. Understand user's goal and requirements
2. Prepare data in format required by [service]
3. Call [tool/script/API] to perform action
4. Handle response (success, errors, warnings)
5. Report results to user with actionable details

**Examples:**
- Notion uploader (publish documentation)
- Confluence publisher (team knowledge base)
- Jira ticket creator (project management)
```

#### Pattern 3: Converter Skills

Transform content between formats.

```
# [Format A] to [Format B] Converter

**Purpose:** Convert content between formats

**Process:**
1. Read source file
2. Parse [Format A] structure
3. Transform to [Format B] structure
4. Write output file
5. Verify conversion accuracy and completeness

**Examples:**
- Markdown to PDF (professional documents)
- Jupyter notebook to Python script (code extraction)
- DOCX to Markdown (content migration)
```

### Pattern Recognition

- Need to **create** something? → Generator pattern
- Need to **connect** to an external service? → Integrator pattern
- Need to **transform** between formats? → Converter pattern

Most complex skills combine these patterns.

---

## Best Practices

### Core Quality Guidelines

**Description Writing:**
- Be specific and include key terms
- Include both what the Skill does AND when to use it
- Write in third person (e.g., "Processes Excel files" not "I can help you process")
- Maximum 1024 characters

**SKILL.md Structure:**
- Keep body under 500 lines for optimal performance
- Use clear, numbered steps (Claude follows sequential instructions well)
- Provide concrete examples with expected inputs and outputs
- Single responsibility - one job, well-defined

**File Organization:**
- Use forward slashes in all paths (Unix-style, works cross-platform)
- Keep references one level deep from SKILL.md (avoid deeply nested references)
- Include tables of contents in reference files longer than 100 lines
- Name files descriptively (e.g., `form_validation_rules.md` not `doc2.md`)

**Naming Conventions:**
- Use gerund form (verb + -ing) for skill names
- Lowercase letters, numbers, and hyphens only
- Maximum 64 characters

**Good examples:**
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`

**Avoid:**
- Vague names: `helper`, `utils`, `tools`
- Overly generic: `documents`, `data`, `files`
- Reserved words: `anthropic-helper`, `claude-tools`

### Progressive Disclosure Patterns

#### Pattern 1: High-Level Guide with References

```
# PDF Processing

## Quick start

Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

#### Pattern 2: Domain-Specific Organization

For skills with multiple domains, organize content by domain:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

**SKILL.md:**
```
# BigQuery Data Analysis

## Available datasets

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)
**Product**: API usage, features, adoption → See [reference/product.md](reference/product.md)
**Marketing**: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)
```

#### Pattern 3: Conditional Details

Show basic content, link to advanced content:

```
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

### Workflow Patterns

For complex tasks, provide checklists that Claude can copy and use:

```
## PDF form filling workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**

Run: `python scripts/analyze_form.py input.pdf`

This extracts form fields and their locations, saving to `fields.json`.
```

### Degrees of Freedom

Match the level of specificity to the task's fragility and variability.

**High Freedom** (text-based instructions):
- Use when multiple approaches are valid
- Decisions depend on context
- Heuristics guide the approach

**Medium Freedom** (pseudocode or scripts with parameters):
- Use when a preferred pattern exists
- Some variation is acceptable
- Configuration affects behavior

**Low Freedom** (specific scripts, few or no parameters):
- Use when operations are fragile and error-prone
- Consistency is critical
- A specific sequence must be followed

---

## Common Anti-Patterns

### Avoid The Encyclopedia

```
❌ BAD: plantuml.md (50KB monolith)

## Sequence Diagram Syntax
[8KB of detailed documentation]
## Class Diagram Syntax
[10KB of detailed documentation]
## ER Diagram Syntax
[7KB of detailed documentation]
...
```

**Problems:**
- Token waste (loads everything, uses only what's needed)
- Slow response times
- Higher costs
- Maintenance nightmare
- Context pollution

### Avoid Too Many Options

```
❌ BAD: Too many choices (confusing)

"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

✅ GOOD: Provide a default (with escape hatch)

"Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
```

### Avoid Deeply Nested References

```
❌ BAD: Too deep

# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...

✅ GOOD: One level deep

# SKILL.md

**Basic usage**: [instructions in SKILL.md]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

### Avoid Time-Sensitive Information

```
❌ BAD: Will become wrong

"If you're doing this before August 2025, use the old API.
After August 2025, use the new API."

✅ GOOD: Use "old patterns" section

## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`

This endpoint is no longer supported.
</details>
```

### Avoid Windows-Style Paths

```
❌ BAD
scripts\helper.py
reference\guide.md

✅ GOOD
scripts/helper.py
reference/guide.md
```

Unix-style paths work across all platforms.

---

## Implementation Examples

### Example 1: PlantUML Skill (PDA Pattern)

**Directory Structure:**
```
plantuml/
├── SKILL.md                    # 3KB orchestrator
└── reference/
    ├── plantuml_sequence.md    # 8KB
    ├── plantuml_class.md       # 10KB
    ├── plantuml_flowchart.md   # 5KB
    └── plantuml_er.md          # 7KB
```

**SKILL.md (simplified):**
```
---
name: plantuml-diagrams
description: Generate PlantUML diagrams from descriptions. Use when creating sequence diagrams, class diagrams, flowcharts, ER diagrams, or state diagrams.
allowed-tools: Read, Bash
---

# PlantUML Diagram Generator

Analyze user request to determine diagram type.

**For sequence diagrams:**
1. Read reference/plantuml_sequence.md
2. Generate PlantUML code using loaded syntax
3. Bash: scripts/plantuml.sh generate [code]
4. Return image path to user

**For class diagrams:**
1. Read reference/plantuml_class.md
2. Generate PlantUML code using loaded syntax
3. Bash: scripts/plantuml.sh generate [code]
4. Return image path to user

**For flowcharts:**
1. Read reference/plantuml_flowchart.md
2. Generate PlantUML code using loaded syntax
3. Bash: scripts/plantuml.sh generate [code]
4. Return image path to user
```

### Example 2: Notion Uploader Skill (Script Pattern)

**Directory Structure:**
```
notion-uploader/
├── SKILL.md                    # 3KB orchestrator
├── reference/
│   └── notion-api.md          # 15KB API documentation
└── scripts/
    ├── upload.py               # Notion API integration
    └── validate.py             # Input validation
```

**SKILL.md (simplified):**
```
---
name: notion-uploader
description: Upload markdown content to Notion. Use when publishing documentation, notes, or content to Notion databases or pages.
allowed-tools: Read, Bash(python:*)
---

# Notion Uploader

**Process:**
1. Validate input file: `python scripts/validate.py [file]`
2. Read reference/notion-api.md for API details if needed
3. Upload to Notion: `python scripts/upload.py [file] [database-id]`
4. Report results with URL

**Error Handling:**
- If validation fails, show specific errors and suggest fixes
- If upload fails, check API credentials and permissions
- If format conversion fails, suggest markdown corrections
```

### Example 3: Multi-Domain BigQuery Skill (Domain Pattern)

**Directory Structure:**
```
bigquery-skill/
├── SKILL.md                    # 2KB orchestrator
└── reference/
    ├── finance.md              # Revenue, ARR, billing metrics
    ├── sales.md                # Opportunities, pipeline, accounts
    ├── product.md              # API usage, features, adoption
    └── marketing.md            # Campaigns, attribution, email
```

**SKILL.md (simplified):**
```
---
name: bigquery-analytics
description: Analyze business data in BigQuery across finance, sales, product, and marketing domains. Use when querying revenue metrics, sales pipeline, API usage, or campaign performance.
allowed-tools: Read, Bash
---

# BigQuery Data Analysis

## Available datasets

**Finance**: Revenue, ARR, billing → Read [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline, accounts → Read [reference/sales.md](reference/sales.md)
**Product**: API usage, features, adoption → Read [reference/product.md](reference/product.md)
**Marketing**: Campaigns, attribution, email → Read [reference/marketing.md](reference/marketing.md)

## Process

1. Determine domain from user request
2. Read appropriate reference file for schema and metrics
3. Construct query using proper table and field names
4. Execute query and format results
```

---

## Key Takeaways

1. **Skills are prompt extensions** - They add specialized knowledge to Claude's context, activate on-demand when needed
2. **PDA is a design pattern, not a framework** - Use Read for lazy loading, Bash for script execution, AI for reasoning
3. **Orchestrator beats encyclopedia** - Load what you need, when you need it (80-95% token savings)
4. **Token efficiency matters at scale** - Below 5KB: basic skills fine; Above 10KB: PDA pays dividends
5. **Not every skill needs PDA** - Simple, focused skills (<5KB): stay basic; Growing, multi-purpose skills (>10KB): apply PDA
6. **Claude Code has everything you need** - Read, Bash, and AI reasoning enable PDA naturally

---

## Additional Resources

### Official Documentation
- [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Skill authoring best practices - Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### Community Resources
- [Claude Code Skills Deep Dive Part 1 | Rick Hightower](https://medium.com/spillwave-solutions/claude-code-skills-deep-dive-part-1-82b572ad9450)
- [Claude Skills and CLAUDE.md: a practical 2026 guide](https://www.gend.co/blog/claude-skills-claude-md-guide)
- [VoltAgent/awesome-claude-skills](https://github.com/VoltAgent/awesome-claude-skills)
- [SkillsMP: Agent Skills Marketplace](https://skillsmp.com/)

### Related Concepts
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

---

## See Also

- [CLAUDE_CODE_COMPLETE_GUIDE.md](CLAUDE_CODE_COMPLETE_GUIDE.md) - Comprehensive Claude Code feature overview
- [CLAUDE.md_PATTERNS.md](CLAUDE.md_PATTERNS.md) - CLAUDE.md structure and best practices
- [CONTEXT_MANAGEMENT.md](CONTEXT_MANAGEMENT.md) - Token optimization strategies
- [AGENTS_WORKFLOWS.md](AGENTS_WORKFLOWS.md) - Agents, subagents, and hooks

---

*This document synthesizes knowledge from official Anthropic documentation and community best practices as of January 2026.*
