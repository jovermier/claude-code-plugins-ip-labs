# Solutions Index

Knowledge base of solved problems and their solutions. Each solution documents a problem that was encountered, the investigation process, and the final resolution.

## Categories

### Authentication
Solutions related to user authentication, authorization, JWT, OAuth, and session management.

### API
REST, GraphQL, API design, versioning, and integration patterns.

### Database
Query optimization, migrations, schema design, indexing, and data integrity.

### Performance
Optimization, caching, load balancing, and performance tuning.

### Testing
Unit tests, integration tests, E2E tests, and testing strategies.

### Deployment
CI/CD, migrations, provisioning, and deployment strategies.

### UI
Components, layouts, responsive design, and state management.

### Architecture
System design, patterns, layering, and architectural decisions.

### Security
Vulnerabilities, OWASP compliance, encryption, and security best practices.

### Debugging
Troubleshooting techniques, log analysis, and debugging strategies.

## Adding Solutions

Use the `/workflows:compound` command to document a solved problem:

```bash
/workflows:compound [problem-title]
```

Or manually create a file in the appropriate category directory using the solution template.

## Solution Template

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
[Clear description of the problem]

## Investigation
[What was tried and what was learned]

## Solution
[How the problem was solved]

## Code Example
\`\`\`language
[Code snippet showing the solution]
\`\`\`

## Prevention
[How to prevent this in the future]

## References
- [Link to related documentation]
- [Link to related issue/PR]
```

## Quick Reference

By Category:
- [Authentication](authentication/) - JWT, OAuth, sessions
- [API](api/) - REST, GraphQL, design patterns
- [Database](database/) - Queries, migrations, indexing
- [Performance](performance/) - Optimization, caching
- [Testing](testing/) - Unit, integration, E2E
- [Deployment](deployment/) - CI/CD, migrations
- [UI](ui/) - Components, layouts
- [Architecture](architecture/) - Design, patterns
- [Security](security/) - Vulnerabilities, OWASP
- [Debugging](debugging/) - Troubleshooting
