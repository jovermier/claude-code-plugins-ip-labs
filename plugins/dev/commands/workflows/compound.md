---
name: workflows:compound
description: Document solved problems as categorized knowledge with YAML frontmatter for fast lookup and future reference
argument-hint: "[problem title or 'current']"
---

# Workflows: Compound - Knowledge Documentation

## Introduction

The `/workflows:compound` command captures solved problems as structured documentation. This creates a knowledge base that compounds over time, making solutions reusable and reducing future problem-solving time.

## Main Tasks

### Phase 1: Identify Problem

1. **Understand What Was Solved**
   - What was the problem?
   - What were the symptoms?
   - What was tried before finding the solution?

2. **Extract Key Information**
   - Root cause analysis
   - Solution implemented
   - Code changes made
   - Lessons learned

### Phase 2: Categorize

Choose appropriate categories:
- **authentication**: Login, auth flows, permissions
- **api**: REST, GraphQL, API design
- **database**: Queries, migrations, schema design
- **performance**: Optimization, caching, indexing
- **testing**: Unit tests, integration tests, E2E
- **deployment**: CI/CD, migrations, provisioning
- **ui**: Components, layouts, responsive design
- **architecture**: System design, patterns, structure
- **security**: Vulnerabilities, encryption, OWASP
- **debugging**: Troubleshooting techniques

### Phase 3: Create Document

Create solution document in `docs/solutions/[category]/[problem-name].md`

## Solution Document Template

```markdown
---
category: [category]
tags: [tag1, tag2, tag3]
related: [related-doc1.md, related-doc2.md]
solved: 2026-01-12
difficulty: easy | medium | hard
frequency: common | occasional | rare
---

# [Problem Title]

## Problem Statement
[Clear description of the problem that was solved]

**Symptoms:**
- [Symptom 1]
- [Symptom 2]
- [Symptom 3]

**Context:**
- [Technology/Framework]
- [Environment]
- [Constraints]

## Investigation

**What Was Tried:**
1. **[Attempt 1]** - [Result: Why it didn't work]
2. **[Attempt 2]** - [Result: Why it didn't work]
3. **[Attempt 3]** - [Result: This worked!]

**Root Cause:**
[The underlying cause of the problem]

## Solution

### Implementation
[Detailed explanation of the solution]

**Code Changes:**
\`\`\`typescript
[Before - if applicable]
// Problematic code
\`\`\`

\`\`\`typescript
[After - The fix]
// Working code
\`\`\`

**Files Modified:**
- `src/[file].ts` - [What changed]
- `src/[file].test.ts` - [Tests added]

### Why This Works
[Explanation of why the solution solves the problem]

## Lessons Learned

**Key Takeaways:**
1. [Lesson 1]
2. [Lesson 2]
3. [Lesson 3]

**What to Watch For:**
- [Common sign that this problem is occurring]
- [How to prevent it in the future]

## References

### Internal
- [Related solution doc](link)
- [Related issue/PR](link)

### External
- [Documentation](link) - [What helped]
- [Stack Overflow](link) - [Relevant answer]
- [GitHub Issue](link) - [Related discussion]

## Quick Reference

**Error Message:** [If applicable]
**Quick Fix:** [One-line solution]
**Verification:** [How to verify it's fixed]
```

## Directory Structure

```
docs/solutions/
├── authentication/
│   ├── jwt-implementation.md
│   ├── oauth-flow.md
│   └── session-management.md
├── api/
│   ├── rest-versioning.md
│   ├── graphql-pagination.md
│   └── rate-limiting.md
├── database/
│   ├── n-plus-one-queries.md
│   ├── migration-safety.md
│   └── index-optimization.md
├── performance/
│   ├── query-optimization.md
│   ├── caching-strategy.md
│   └── memory-leaks.md
├── testing/
│   ├── mocking-external-services.md
│   ├── e2e-setup.md
│   └── test-organization.md
├── deployment/
│   ├── zero-downtime-migrations.md
│   ├── rollback-strategy.md
│   └── environment-config.md
├── ui/
│   ├── responsive-layout.md
│   ├── component-patterns.md
│   └── state-management.md
├── architecture/
│   ├── layer-separation.md
│   ├── dependency-injection.md
│   └── microservices-communication.md
├── security/
│   ├── xss-prevention.md
│   ├── csrf-protection.md
│   └── secret-management.md
└── debugging/
    ├── race-conditions.md
    ├── memory-profiling.md
    └── log-analysis.md
```

## Key Principles

- **Categorized**: Organize by domain for easy lookup
- **Searchable**: Use tags and related links
- **Actionable**: Include code examples
- **Complete**: Document what didn't work too
- **Indexed**: Update index when adding new docs

## Output Examples

### Simple Problem
```markdown
---
category: debugging
tags: [javascript, typescript, async]
solved: 2026-01-12
difficulty: easy
frequency: common
---

# Async/Await Not Waiting

## Problem Statement
Async function wasn't waiting for promise to resolve.

**Symptoms:**
- Code executing before async operation completed
- Undefined values when expecting data

## Solution
Forgot `await` keyword before promise call.

\`\`\`typescript
// Wrong
const data = fetchData();

// Right
const data = await fetchData();
\`\`\`

**Quick Fix:** Add `await` before async calls
```

### Complex Problem
```markdown
---
category: performance
tags: [database, sql, optimization]
solved: 2026-01-12
difficulty: hard
frequency: occasional
---

# N+1 Query Problem in User List

## Problem Statement
Loading user list with posts was extremely slow. 1000 users took 30 seconds.

## Root Cause
Fetching posts for each user in a loop (N+1 queries).

## Solution
Eager loading with JOIN.

\`\`\`sql
-- Before: N+1 queries
SELECT * FROM users;
-- Then for each user:
SELECT * FROM posts WHERE user_id = ?;

-- After: 1 query
SELECT users.*, posts.*
FROM users
LEFT JOIN posts ON posts.user_id = users.id;
\`\`\`

**Performance:** 30s → 200ms

## Lessons Learned
- Always check for queries in loops
- Use EXPLAIN to analyze queries
- Consider eager loading for relationships
```

## Quality Checklist

- [ ] Problem clearly described
- [ ] Root cause identified
- [ ] Solution includes code examples
- [ ] Lessons learned documented
- [ ] Category and tags appropriate
- [ ] Related documents linked
- [ ] Quick reference included
- [ ] Verification steps provided

## Common Pitfalls

- **Vague Descriptions**: Be specific about symptoms
- **Missing Context**: Include technology/environment info
- **Only Success**: Document what didn't work too
- **No Code**: Always include code examples
- **Outdated**: Update docs when better solutions found

## Quick Usage Examples

**Example 1: Document current solution**
> User: `/workflows:compound`

> Agent: What problem did you just solve? I'll help document it as a solution...

[Asks questions, creates categorized solution document]

**Example 2: Document specific problem**
> User: `/workflows:compound JWT authentication setup`

> Agent: I'll create a solution document for JWT authentication...

[Creates doc with JWT setup, common pitfalls, verification steps]

**Example 3: Compound multiple solutions**
> User: `/workflows:compound --all`

> Agent: I'll review recent work and create solution docs for all solved problems...

[Reviews recent commits/PRs, creates multiple solution docs]

## Index Management

Update `docs/solutions/index.md` when adding new docs:

```markdown
# Solutions Index

## Authentication
- [JWT Implementation](authentication/jwt-implementation.md)
- [OAuth Flow](authentication/oauth-flow.md)

## API
- [REST Versioning](api/rest-versioning.md)
- [GraphQL Pagination](api/graphql-pagination.md)

[... continue for all categories]
```

## Related Skills

- `/plan-manager` - For managing documentation alongside plans
- `/file-todos` - For tracking solution documentation tasks
