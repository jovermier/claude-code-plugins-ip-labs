---
name: skill-architect
description: Orchestrates complete skill lifecycle from creation to optimization. Use for comprehensive skill development, reviewing skills, or managing skill quality.
skills: skill-generator, skill-reviewer, skill-optimizer
---

# Skill Architect

## Purpose

Meta-orchestrator for the complete Claude Code skill lifecycle. Manages skill creation, review, optimization, and quality assurance through coordinated subagent workflows.

## When to Use

- User asks to "manage skills" or "oversee skill development"
- Complete skill lifecycle management
- Quality assurance for skill libraries
- Team skill development workflows
- Comprehensive skill audits

## Available Subagents

This orchestrator coordinates three specialized skills:

1. **@skill-generator** - Creates new skills from descriptions
2. **@skill-reviewer** - Reviews skills for quality and best practices
3. **@skill-optimizer** - Refactors skills using PDA

## Workflows

### Workflow 1: Create and Review

**Use when:** Creating a new skill with quality assurance

```
1. @skill-generator
   - Generate SKILL.md from user description
   - Create directory structure
   - Apply best practices

2. @skill-reviewer
   - Review generated skill
   - Identify any issues
   - Provide quality score

3. Report and Iterate (if needed)
   - Present skill to user
   - Address review feedback
   - Finalize skill
```

**Trigger phrases:**
- "Create a skill for X and review it"
- "Generate and check a new skill"
- "Make a skill for X with quality check"

### Workflow 2: Audit and Optimize

**Use when:** Improving existing skills

```
1. @skill-reviewer
   - Review existing skill
   - Identify improvement opportunities
   - Calculate potential savings

2. @skill-optimizer
   - Apply recommended improvements
   - Implement PDA refactoring
   - Optimize token usage

3. Validation
   - Compare before/after
   - Verify functionality preserved
   - Report improvements
```

**Trigger phrases:**
- "Audit this skill and optimize it"
- "Review and improve this skill"
- "Check and fix this skill"

### Workflow 3: Complete Lifecycle

**Use when:** End-to-end skill development

```
1. Requirements Gathering
   - Understand skill purpose
   - Identify use cases
   - Determine scope

2. @skill-generator
   - Create initial skill
   - Structure content
   - Add examples

3. @skill-reviewer
   - Quality assessment
   - Best practices check
   - Improvement recommendations

4. @skill-optimizer (if needed)
   - Apply optimizations
   - Implement PDA
   - Reduce token usage

5. Final Review
   - Validate improvements
   - Confirm quality standards
   - Deliver production-ready skill
```

**Trigger phrases:**
- "Create a production-ready skill for X"
- "Develop a complete skill from scratch"
- "Build and validate a skill"

### Workflow 4: Skill Library Audit

**Use when:** Reviewing multiple skills

```
1. Discover Skills
   - Find all skills in .claude/skills/
   - List each skill with metadata

2. @skill-reviewer (parallel)
   - Review each skill
   - Generate quality scores
   - Identify common issues

3. Aggregate Report
   - Overall quality assessment
   - Prioritized improvements
   - Token savings opportunities

4. Recommendations
   - Which skills need optimization
   - Which skills are excellent
   - Best practices to share
```

**Trigger phrases:**
- "Audit all my skills"
- "Review my skill library"
- "Check all skills for quality"

## Output Format

### For Creation Workflows

```markdown
# Skill Creation Complete

## Skill Overview
**Name:** [skill-name]
**Location:** .claude/skills/[skill-name]/
**Size:** [X] KB

## Quality Assessment
**Score:** [X/10]
**PDA Compliance:** Yes/No
**Status:** Ready for use / Needs improvements

## What Was Created
1. SKILL.md - Main orchestrator
2. reference/ - Detailed documentation
3. scripts/ - Utility scripts (if applicable)

## Usage
Invoke with: [example invocation]

## Next Steps
- [ ] Test the skill
- [ ] Adjust if needed
- [ ] Add to version control
```

### For Optimization Workflows

```markdown
# Skill Optimization Complete

## Summary
**Skill:** [skill-name]
**Original Size:** [X] KB
**Optimized Size:** [Y] KB
**Token Savings:** [Z]%

## Improvements Made
### Structure
- [Changes]

### Content
- [Changes]

### Token Efficiency
- [Changes]

## Quality Improvements
**Before:** Score [X]/10
**After:** Score [Y]/10

## Cost Impact
At 100 requests/day:
- Before: $[cost]/year
- After: $[new cost]/year
- Saved: $[savings]/year

## Validation
✅ Functionality preserved
✅ All links work
✅ Performance improved
```

### For Audit Workflows

```markdown
# Skill Library Audit Report

## Overview
**Total Skills:** [N]
**Average Score:** [X]/10
**Skills Needing Work:** [N]

## Skills by Quality

### Excellent (9-10)
- [skill-1]
- [skill-2]

### Good (7-8)
- [skill-3]
- [skill-4]

### Needs Improvement (5-6)
- [skill-5]
- [skill-6]

### Poor (1-4)
- [skill-7]
- [skill-8]

## Common Issues Found
1. [Issue] - [Count] skills affected
2. [Issue] - [Count] skills affected

## Prioritized Recommendations

### P1 (Critical)
- [Recommendations]

### P2 (Important)
- [Recommendations]

### P3 (Nice-to-Have)
- [Recommendations]

## Token Optimization Opportunity
**Current Usage:** [X] MB/day
**Potential Savings:** [Y] MB/day ([Z]%)
**Annual Cost Savings:** $[amount]

## Next Steps
1. Address P1 issues
2. Optimize skills with low scores
3. Apply best practices to all skills
```

## Quality Gates

Each workflow includes quality checks:

### Creation Quality Gates
- [ ] YAML frontmatter valid
- [ ] Description specific and actionable
- [ ] Clear instructions with examples
- [ ] Appropriate use of PDA
- [ ] No reserved words in name
- [ ] File paths use forward slashes

### Optimization Quality Gates
- [ ] Token savings achieved
- [ ] Functionality preserved
- [ ] Links verified working
- [ ] Structure improved
- [ ] User experience enhanced

### Review Quality Gates
- [ ] All dimensions evaluated
- [ ] Severity classification applied
- [ ] Recommendations actionable
- [ ] Token savings calculated
- [ ] Report comprehensive

## Best Practices Applied

This orchestrator ensures:

1. **Progressive Disclosure**
   - Skills use PDA when appropriate
   - Token-efficient design
   - On-demand loading

2. **Quality Standards**
   - Consistent structure
   - Clear documentation
   - Actionable examples

3. **Best Practices**
   - Gerund naming
   - Third-person descriptions
   - Forward slash paths
   - Single responsibility

4. **Token Optimization**
   - Minimal SKILL.md size
   - Reference files for details
   - Scripts for mechanical work

## Integration

This orchestrator works with:

- **skill-generator** - For skill creation
- **skill-reviewer** - For quality assessment
- **skill-optimizer** - For improvement

## Advanced Features

### Batch Operations

Process multiple skills:

```
> Audit and optimize all skills in .claude/skills/
# Runs @skill-reviewer on each
# Runs @skill-optimizer on those needing improvement
# Generates aggregate report
```

### Skill Templates

Create from templates:

```
> Create a generator skill following the generator template
# Uses predefined pattern
# Applies best practices automatically
# Delivers consistent structure
```

### Continuous Improvement

Ongoing quality management:

```
> Set up skill quality monitoring
# Establishes quality baseline
# Recommends regular reviews
# Tracks improvements over time
```

## Examples

### Example 1: Create Complete Skill

**User:** "Create a production-ready skill for processing JSON files with validation and transformation"

**Workflow:**
```
1. @skill-generator
   Creates: json-processor/
   ├── SKILL.md (4KB orchestrator)
   ├── reference/
   │   ├── json-schema.md
   │   ├── transformations.md
   │   └── validation.md
   └── scripts/
       ├── validate.py
       └── transform.py

2. @skill-reviewer
   Score: 9/10
   PDA Compliance: Yes
   Status: Ready for use

3. Report
   Skill created and validated
   All quality gates passed
   Ready for production use
```

### Example 2: Optimize Poor Skill

**User:** "This 50KB skill is slow and expensive. Fix it."

**Workflow:**
```
1. @skill-reviewer
   Score: 3/10
   Issues: Monolithic, no PDA, token-inefficient
   Recommendation: Major refactor

2. @skill-optimizer
   Before: 50KB SKILL.md
   After: 3KB SKILL.md + reference/ files
   Savings: 84%

3. Validation
   Functionality: Preserved
   Performance: 5x faster
   Cost: $12/day → $2/day
```

### Example 3: Library Audit

**User:** "Review all my skills and tell me what needs improvement"

**Workflow:**
```
1. Discovery
   Found 12 skills

2. @skill-reviewer (parallel)
   3 Excellent (9-10)
   5 Good (7-8)
   3 Fair (5-6)
   1 Poor (2)

3. @skill-optimizer (for 4 low-scoring skills)
   Average improvement: 73% token reduction

4. Report
   Overall quality improved from 6.5 to 8.2
   Projected annual savings: $1,200
```

## See Also

- [SKILL_GENERATOR.md](.claude/skills/skill-generator/SKILL.md) - Create skills
- [SKILL_REVIEWER.md](.claude/skills/skill-reviewer/SKILL.md) - Review skills
- [SKILL_OPTIMIZER.md](.claude/skills/skill-optimizer/SKILL.md) - Optimize skills
- [CLAUDE_SKILLS_ARCHITECTURE.md](../../../docs/CLAUDE_SKILLS_ARCHITECTURE.md) - Reference documentation
- [docs/README.md](../../../docs/README.md) - All documentation

## Sources

Based on:
- [CLAUDE_SKILLS_ARCHITECTURE.md](../../../docs/CLAUDE_SKILLS_ARCHITECTURE.md)
- [AGENTS_WORKFLOWS.md](../../../docs/AGENTS_WORKFLOWS.md)
- Progressive Disclosure Architecture principles
