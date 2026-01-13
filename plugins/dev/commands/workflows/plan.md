---
name: workflows:plan
description: Transform feature descriptions into well-structured project plans following conventions, with parallel research agents for each section
argument-hint: "[feature description]"
---

# Workflows: Plan - Structured Project Planning

## Introduction

The `/workflows:plan` command transforms feature descriptions into comprehensive, well-structured project plans. It uses parallel research agents to add depth and best practices to each section of the plan.

## Main Tasks

### Phase 1: Understand Requirements

1. **Parse Feature Description**
   - Identify core functionality
   - Extract user goals
   - Note constraints and requirements

2. **Ask Clarifying Questions** (if needed)
   - Tech stack preferences
   - Performance requirements
   - Security considerations
   - Timeline constraints

### Phase 2: Parallel Research

Launch research agents in parallel to inform the plan:

| Agent | Research Focus |
|-------|----------------|
| `repo-research-analyst` | Repository patterns and conventions |
| `framework-docs-researcher` | Framework-specific best practices |
| `best-practices-researcher` | General industry best practices |
| `git-history-analyzer` | Historical context for related code |

### Phase 3: Plan Creation

Create a structured plan with sections:

#### 1. Overview
- Feature summary
- Goals and success criteria
- Constraints and assumptions

#### 2. Technical Approach
- Architecture decisions
- Technology choices (with rationale)
- Data models and schemas
- API contracts (if applicable)

#### 3. Implementation Steps
- Ordered list of implementation tasks
- Dependencies between steps
- Estimated complexity

#### 4. Testing Strategy
- Unit test approach
- Integration test coverage
- E2E test scenarios
- Performance testing (if needed)

#### 5. Deployment Considerations
- Migration requirements
- Configuration changes
- Feature flag strategy
- Rollback plan

### Phase 4: Write Plan File

Save plan to `plugins/dev/plans/[feature-name].plan.md`

## Plan Template

```markdown
# Plan: [Feature Name]

**Created:** [YYYY-MM-DD]
**Status:** Draft | Approved | In Progress | Complete
**Priority:** P1 | P2 | P3

## Overview

### Summary
[2-3 sentence description of the feature]

### Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

### Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

### Constraints
- **Performance:** [Requirements]
- **Security:** [Requirements]
- **Compatibility:** [Requirements]
- **Timeline:** [Requirements]

## Technical Approach

### Architecture
[Diagram or description of how components interact]

### Technology Choices
| Technology | Purpose | Rationale |
|------------|---------|-----------|
| [Name] | [Purpose] | [Why chosen] |

### Data Model
\`\`\`typescript
[Type definitions or schema]
\`\`\`

### API Design (if applicable)
\`\`\`typescript
[API contracts]
\`\`\`

## Implementation Steps

### Step 1: [Task Name]
**Complexity:** Low | Medium | High
**Dependencies:** None

**Tasks:**
- [ ] [Subtask 1]
- [ ] [Subtask 2]

**Definition of Done:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Step 2: [Task Name]
**Complexity:** Low | Medium | High
**Dependencies:** Step 1

**Tasks:**
- [ ] [Subtask 1]
- [ ] [Subtask 2]

**Definition of Done:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

[Continue for all steps...]

## Testing Strategy

### Unit Tests
- [ ] [Test scenario 1]
- [ ] [Test scenario 2]
- Target coverage: [X]%

### Integration Tests
- [ ] [Test scenario 1]
- [ ] [Test scenario 2]

### E2E Tests
- [ ] [Test scenario 1]
- [ ] [Test scenario 2]

### Performance Tests (if applicable)
- [ ] [Test scenario 1]
- [ ] [Test scenario 2]

## Deployment Plan

### Pre-Deployment
- [ ] [Pre-deployment task 1]
- [ ] [Pre-deployment task 2]

### Deployment Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Post-Deployment Verification
- [ ] [Verification check 1]
- [ ] [Verification check 2]

### Rollback Plan
[Steps to rollback if issues occur]

## Open Questions
1. [Question 1]
2. [Question 2]

## Risks and Mitigations
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Mitigation] |

## Related Issues/PRs
- #[issue-number]: [Title]
- #[issue-number]: [Title]

## References
- [Link 1]
- [Link 2]
```

## Key Principles

- **Parallel Research**: Use multiple agents simultaneously for speed
- **Evidence-Based**: Base decisions on research, not assumptions
- **Structured Output**: Follow consistent plan format
- **Actionable Steps**: Break down into implementable tasks
- **Risk-Aware**: Identify and plan for risks

## Quality Checklist

- [ ] Research completed for all relevant areas
- [ ] Plan follows template structure
- [ ] Implementation steps are ordered by dependency
- [ ] Each step has clear definition of done
- [ ] Testing strategy is comprehensive
- [ ] Deployment plan includes rollback
- [ ] Open questions documented
- [ ] Risks identified with mitigations

## Common Pitfalls

- **Skipping Research**: Don't write plans without gathering context
- **Vague Steps**: Make each step specific and actionable
- **Missing Dependencies**: Clearly show what depends on what
- **Undefined Success**: Ensure success criteria are measurable
- **No Rollback Plan**: Always consider how to undo changes

## Quick Usage Examples

**Example 1: Plan a new feature**
> User: `/workflows:plan Add user authentication with JWT`

> Assistant: I'll create a comprehensive plan for JWT authentication. Let me gather research in parallel first...

[Launches research agents, creates detailed plan with architecture, steps, testing, deployment]

**Example 2: Plan a refactor**
> User: `/workflows:plan Refactor user service to use repository pattern`

> Assistant: I'll create a plan for refactoring to the repository pattern. Let me research the current codebase first...

[Analyzes current code, researches repository pattern best practices, creates migration plan]

**Example 3: Plan an API change**
> User: `/workflows:plan Add GraphQL API for orders`

> Assistant: I'll create a plan for adding GraphQL. Let me research GraphQL patterns and the current order system...

[Researches GraphQL, analyzes current REST API, creates migration plan with backwards compatibility]

## Related Skills

- `/deepen-plan` - For enhancing existing plans with deeper research
- `/plan-manager` - For managing plan lifecycle
- `/quality-severity` - For assessing task priorities
