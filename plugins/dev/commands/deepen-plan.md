---
name: deepen-plan
description: Enhance a plan with parallel research agents for each section, adding depth, best practices, and implementation details
argument-hint: "[plan-name or 'current']"
---

# Deepen Plan - Enhanced Planning with Research

## Introduction

The `/deepen-plan` command takes an existing plan and enhances it with comprehensive research. Each section of the plan is researched in parallel by specialized agents, adding best practices, implementation details, and context.

## Main Tasks

### Phase 1: Parse Existing Plan

1. **Read the Plan**
   - Identify all sections
   - Extract key decisions
   - Note gaps and areas needing detail

2. **Identify Research Areas**
   - Technology choices needing validation
   - Architecture patterns needing research
   - Implementation approaches needing best practices
   - Testing strategies needing examples

### Phase 2: Parallel Research by Section

Launch research agents for each plan section:

| Section | Research Agent | Output |
|---------|---------------|--------|
| **Technical Approach** | `framework-docs-researcher` | Framework-specific patterns, API usage |
| **Architecture** | `best-practices-researcher` | Design patterns, architectural principles |
| **Implementation** | `repo-research-analyst` | Codebase patterns, conventions |
| **Context** | `git-history-analyzer` | Historical context, related code evolution |

### Phase 3: Section Enhancement

For each plan section, add:

#### Technical Approach Enhancement
- **Framework Examples**: Concrete code examples from official docs
- **API References**: Links to relevant API documentation
- **Version Notes**: Version-specific considerations
- **Gotchas**: Common pitfalls and how to avoid them

#### Architecture Enhancement
- **Pattern Explanations**: Why each pattern is appropriate
- **Alternatives Considered**: Why other approaches weren't chosen
- **Trade-offs**: What's gained vs what's lost
- **Real-World Examples**: Links to open source examples

#### Implementation Enhancement
- **Code Snippets**: Example implementations
- **File Locations**: Where code should go
- **Conventions**: Codebase-specific patterns to follow
- **Dependencies**: What libraries/packages needed

#### Testing Enhancement
- **Test Examples**: Concrete test scenarios with code
- **Framework Usage**: How to use the test framework
- **Coverage Targets**: What to test vs what's covered elsewhere
- **Mocking Strategies**: How to handle external dependencies

### Phase 4: Update Plan

Enhance the plan file with:
- Code examples for each implementation step
- Links to documentation and references
- Best practice recommendations
- Common pitfalls to avoid
- Alternative approaches considered

## Enhanced Plan Template Additions

### For Each Implementation Step:

```markdown
### Step N: [Task Name]

**Research-Based Enhancements:**

**Best Practices:**
- [Practice 1]: [Explanation with source]
- [Practice 2]: [Explanation with source]

**Code Example:**
\`\`\`typescript
[Concrete example from framework docs or best practices]
\`\`\`

**Source:** [Link to documentation]

**Common Pitfalls:**
- ❌ [Pitfall 1]: [What happens and how to avoid]
- ❌ [Pitfall 2]: [What happens and how to avoid]

**Codebase Conventions:**
- [Convention 1]: [How this codebase does it]
- [Convention 2]: [File organization pattern]

**Files to Create/Modify:**
- `src/[path]/[file].ts` - [Purpose]
- `src/[path]/[file].test.ts` - [Purpose]
```

### For Technical Approach Section:

```markdown
## Technical Approach (Enhanced)

### Architecture Decisions

**Decision 1: [Decision Name]**
**What:** [Description]

**Why This Approach:**
- [Reason 1]: [Explanation]
- [Reason 2]: [Explanation]

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Not Chosen |
|-------------|------|------|----------------|
| [Name] | [Pros] | [Cons] | [Reason] |
| [Name] | [Pros] | [Cons] | [Reason] |

**Best Practice Reference:**
- [Source]: [Link to official docs or reputable source]
- **Key Insight:** [What to learn from this source]

**Real-World Example:**
From [Project Name]:
> [Relevant example with link]

### Technology Choices

| Technology | Best Practice Reference | Key Documentation |
|------------|------------------------|-------------------|
| [Name] | [Source link] | [Doc link] |
| [Name] | [Source link] | [Doc link] |
```

### For Testing Section:

```markdown
## Testing Strategy (Enhanced)

### Framework-Specific Patterns

**For [Testing Framework]:**
- **Official Docs:** [Link]
- **Best Practices:** [Summary with source]

**Unit Test Example:**
\`\`\`typescript
import { describe, it, expect } from '[framework]';

describe('[Feature]', () => {
  it('should [behavior]', () => {
    // Arrange
    const input = [test data];

    // Act
    const result = [function](input);

    // Assert
    expect(result).toEqual([expected]);
  });
});
\`\`\`

**Integration Test Example:**
\`\`\`typescript
[Example with mocking external dependencies]
\`\`\`

### Coverage Targets

Based on research for this type of feature:
- **Unit Tests:** Target [X]% coverage
- **Edge Cases:** [List specific cases to test]
- **Error Paths:** [List error scenarios]

**Reference:** [Source for coverage recommendations]
```

## Key Principles

- **Parallel Research**: All sections researched simultaneously
- **Evidence-Based**: Every enhancement backed by sources
- **Code Examples**: Concrete examples for all implementation steps
- **Best Practices**: Incorporate industry standards
- **Codebase Aware**: Respect existing conventions

## Quality Checklist

- [ ] All plan sections enhanced with research
- [ ] Code examples provided for implementation steps
- [ ] Best practice references included
- [ ] Common pitfalls documented
- [ ] Alternatives considered and documented
- [ ] All sources cited
- [ ] Codebase conventions incorporated

## Common Pitfalls

- **Generic Examples**: Use framework-specific, not generic examples
- **Outdated Info**: Ensure docs are current
- **Ignoring Conventions**: Research the codebase's patterns too
- **Over-Engineering**: Don't add unnecessary complexity
- **Missing Sources**: Always cite where information came from

## Quick Usage Examples

**Example 1: Deepen current plan**
> User: `/deepen-plan`

> Assistant: I'll enhance the current plan with parallel research. Let me launch research agents for each section...

[Reads current plan, launches parallel research, adds code examples and best practices]

**Example 2: Deepen specific plan**
> User: `/deepen-plan authentication.plan.md`

> Assistant: I'll enhance the authentication plan. Let me research each section...

[Reads authentication plan, launches targeted research, adds JWT best practices, security considerations]

**Example 3: Deepen plan section**
> User: `/deepen-plan api-changes.plan.md --section testing`

> Agent: I'll focus on deepening the testing section...

[Researches testing best practices for the API, adds comprehensive test examples]

## Related Commands

- `/workflows:plan` - Create a new plan
- `/plan-manager` - Manage plan lifecycle
