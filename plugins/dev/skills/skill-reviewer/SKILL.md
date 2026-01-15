---
name: skill-reviewer
description: Reviews Claude Code skills for quality, best practices, and improvement opportunities. Use when evaluating skills, checking for PDA compliance, or identifying optimization opportunities.
allowed-tools: Read, Glob
---

# Skill Reviewer

## Purpose

Comprehensive review of Claude Code skills to ensure they follow best practices, use Progressive Disclosure Architecture (PDA) appropriately, and provide optimal user experience.

## When to Use

- User asks to "review this skill" or "check this skill"
- Evaluating skill quality before publishing
- Identifying improvement opportunities
- Checking for PDA compliance
- Validating skill structure and conventions

## Review Dimensions

### 1. Structure & Organization

**Check:**
- [ ] SKILL.md exists in correct location
- [ ] YAML frontmatter is valid and properly formatted
- [ ] Name follows conventions (lowercase, hyphens, <64 chars)
- [ ] Description is specific and includes trigger terms
- [ ] Description is under 1024 characters
- [ ] Description is in third person

**Common Issues:**
- Invalid YAML (missing `---`, wrong indentation)
- Reserved words in name (anthropic, claude)
- Vague description ("helps with documents")
- Description too long (>1024 chars)

### 2. Content Quality

**Check:**
- [ ] Clear purpose statement
- [ ] Numbered step-by-step instructions
- [ ] Concrete examples with inputs/outputs
- [ ] Appropriate level of detail
- [ ] Consistent terminology

**Common Issues:**
- Missing examples
- Abstract guidance without concrete steps
- Inconsistent terminology
- Too much or too little detail

### 3. Progressive Disclosure (PDA) Compliance

**Check:**
- [ ] SKILL.md is under 500 lines
- [ ] SKILL.md is under 10KB (ideally 3-5KB)
- [ ] Large content split into reference/ files
- [ ] References are one level deep from SKILL.md
- [ ] Links to detailed docs are clear

**PDA Assessment:**
```
If SKILL.md < 5KB: ✅ Basic structure is fine
If SKILL.md 5-10KB: ⚠️ Consider progressive disclosure
If SKILL.md > 10KB: ❌ Should use PDA
If SKILL.md > 20KB: ❌❌ Strongly recommend PDA refactor
```

**Common Issues:**
- Monolithic SKILL.md with all content inline
- Deeply nested references (SKILL.md → advanced.md → details.md)
- Missing progressive disclosure for large content

### 4. File Organization

**Check:**
- [ ] Forward slashes in all paths (cross-platform)
- [ ] Descriptive file names (not doc1.md, doc2.md)
- [ ] Scripts in scripts/ directory
- [ ] Reference docs in reference/ directory
- [ ] No Windows-style backslashes

**Common Issues:**
- Mixed path separators
- Generic file names
- Scripts and docs in wrong locations

### 5. Best Practices

**Check:**
- [ ] Single responsibility (one clear purpose)
- [ ] Error handling guidance
- [ ] Security considerations (if applicable)
- [ ] Dependencies documented
- [ ] Troubleshooting section

**Common Issues:**
- Too broad scope ("does everything")
- Missing error handling
- Undocumented dependencies

### 6. Token Efficiency

**Check:**
- [ ] Progressive disclosure used appropriately
- [ ] Reference files loaded on-demand
- [ ] Scripts for mechanical work
- [ ] No redundant information

**Efficiency Assessment:**
```
Excellent: 80-95% token savings (PDA well applied)
Good: 50-79% token savings (PDA partially applied)
Fair: 20-49% token savings (some optimization)
Poor: 0-19% token savings (encyclopedia approach)
```

## Review Process

1. **Read SKILL.md**
   - Parse YAML frontmatter
   - Check structure and organization
   - Evaluate content quality

2. **Check File Structure**
   - List all files in skill directory
   - Verify organization
   - Check file naming

3. **Assess PDA Compliance**
   - Estimate SKILL.md size
   - Check for reference/ directory
   - Evaluate progressive disclosure

4. **Identify Issues**
   - Categorize by severity (P1/P2/P3)
   - Provide specific recommendations
   - Suggest concrete fixes

5. **Generate Report**
   - Overall quality score
   - Detailed findings by dimension
   - Prioritized recommendations
   - Estimated token savings from improvements

## Output Format

```markdown
# Skill Review Report

## Overall Assessment
**Score:** [X/10]
**PDA Compliance:** [Yes/No/Partial]
**Recommendation:** [Approve/Improve/Refactor]

## Findings by Dimension

### Structure & Organization
[Issues found, if any]

### Content Quality
[Issues found, if any]

### PDA Compliance
[Current state, recommendations]

### File Organization
[Issues found, if any]

### Best Practices
[Issues found, if any]

### Token Efficiency
[Current efficiency, potential savings]

## Prioritized Recommendations

### P1 (Critical - Must Fix)
[Blocking issues]

### P2 (Important - Should Fix)
[Significant improvements]

### P3 (Nice-to-Have)
[Minor optimizations]

## Token Savings Estimate
[Current vs optimized comparison]
```

## Quality Scoring

**Excellent (9-10):**
- All best practices followed
- PDA optimally applied
- Clear, concise, actionable
- Token savings >80%

**Good (7-8):**
- Most best practices followed
- PDA appropriately used
- Minor improvements possible
- Token savings 50-80%

**Fair (5-6):**
- Some best practices missing
- PDA partially applied or not needed
- Several improvements recommended
- Token savings 20-50%

**Poor (1-4):**
- Many best practices violated
- PDA not applied when needed
- Significant refactoring needed
- Token savings <20%

## Common Recommendations

### For Structure Issues
- "Fix YAML frontmatter formatting"
- "Rename skill to follow conventions"
- "Rewrite description to be more specific"
- "Add missing examples"

### For PDA Issues
- "Split large SKILL.md using progressive disclosure"
- "Move detailed docs to reference/ files"
- "Create on-demand loading structure"
- "Reduce SKILL.md to <5KB"

### For Organization Issues
- "Reorganize files into standard structure"
- "Rename files to be more descriptive"
- "Convert paths to forward slashes"
- "Move scripts to scripts/ directory"

### For Content Issues
- "Add concrete examples with inputs/outputs"
- "Include error handling guidance"
- "Add troubleshooting section"
- "Document dependencies"

## Severity Classification

**P1 (Critical):**
- Blocks usage or understanding
- Fundamental flaws in structure
- Missing essential information
- Security vulnerabilities

**P2 (Important):**
- Should be addressed
- Significant gaps
- Risky approaches
- Performance issues

**P3 (Nice-to-Have):**
- Consider for polish
- Minor improvements
- Optimizations
- Style consistency

## Integration with Other Skills

After review, recommend:
- **skill-generator** - If major restructuring needed
- **skill-optimizer** - If PDA refactor recommended
- **manual review** - For nuanced decisions

## Examples

### Example 1: Excellent Skill

**Input:** Well-structured skill with PDA

**Review:**
```
# Skill Review Report

## Overall Assessment
**Score:** 9/10
**PDA Compliance:** Yes
**Recommendation:** Approve

### Findings
All dimensions met or exceeded standards.
Minor suggestion: Add troubleshooting section.

### Token Efficiency
Current: 3KB + on-demand loading
Savings: 92%
```

### Example 2: Needs PDA Refactor

**Input:** 50KB monolithic SKILL.md

**Review:**
```
# Skill Review Report

## Overall Assessment
**Score:** 4/10
**PDA Compliance:** No
**Recommendation:** Refactor with PDA

### PDA Compliance
**Current:** 50KB monolithic file
**Recommended:** Split using progressive disclosure

### Token Savings Estimate
**Current:** 50KB per request
**Optimized:** 3KB + 8KB average = 11KB
**Savings:** 78% (39KB per request)

### P1 Recommendations
- Split SKILL.md into orchestrator + reference files
- Create reference/ directory for detailed docs
- Implement on-demand loading pattern
```

## Quality Checklist Template

```markdown
## Review Checklist

### YAML Frontmatter
- [ ] Valid format (starts/ends with `---`)
- [ ] Name: lowercase, hyphens, <64 chars
- [ ] No reserved words (anthropic, claude)
- [ ] Description: specific, includes triggers
- [ ] Description: <1024 characters
- [ ] Description: third person
- [ ] Allowed tools: appropriate for skill

### Content Structure
- [ ] Clear purpose statement
- [ ] Numbered process steps
- [ ] Concrete examples
- [ ] Error handling guidance
- [ ] Troubleshooting section

### PDA Compliance
- [ ] SKILL.md <500 lines
- [ ] SKILL.md <10KB
- [ ] Progressive disclosure used if >10KB
- [ ] References one level deep
- [ ] On-demand loading implemented

### File Organization
- [ ] Standard directory structure
- [ ] Forward slash paths
- [ ] Descriptive file names
- [ ] Scripts in scripts/
- [ ] References in reference/

### Best Practices
- [ ] Single responsibility
- [ ] Consistent terminology
- [ ] Dependencies documented
- [ ] Security considered
- [ ] Token efficient
```

## See Also

- [SKILL_GENERATOR.md](.claude/skills/skill-generator/SKILL.md) - Create new skills
- [SKILL_OPTIMIZER.md](.claude/skills/skill-optimizer/SKILL.md) - Optimize existing skills
- [SKILL_ARCHITECT.md](.claude/skills/skill-architect/SKILL.md) - Complete workflow
- [CLAUDE_SKILLS_ARCHITECTURE.md](../../../docs/CLAUDE_SKILLS_ARCHITECTURE.md) - Reference documentation

## Sources

Based on:
- [CLAUDE_SKILLS_ARCHITECTURE.md](../../../docs/CLAUDE_SKILLS_ARCHITECTURE.md)
- Official Anthropic skill authoring best practices
