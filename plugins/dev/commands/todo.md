---
name: todo
description: Manage file-based todos with create, list, update, and dependency tracking
argument-hint: "[list|create|update|status] [options]"
---

# Todo Command - File-Based Todo Management

Manage todos using the file-based todo system with YAML frontmatter.

## Usage

### List Todos

List todos by status, priority, or filter by tag.

```bash
# List all todos
/todo list

# List by status
/todo list --status pending
/todo list --status ready
/todo list --status complete

# List by priority
/todo list --priority p1
/todo list --priority p2

# List incomplete todos (default)
/todo list
```

**Output Format:**
```
## Todos (5 pending, 2 ready)

### P1 (Critical) - 2 items
- [123-pending-p1-hardcoded-jwt-secret.md](todos/123-pending-p1-hardcoded-jwt-secret.md)
  Hardcoded JWT secret in source code
  Created: 2026-01-12 | Dependencies: none

### P2 (Important) - 3 items
- [124-pending-p2-n-plus-one-queries.md](todos/124-pending-p2-n-plus-one-queries.md)
  N+1 query pattern in user list
  Created: 2026-01-12 | Dependencies: 123-pending-p1-hardcoded-jwt-secret.md
```

### Create Todo

Create a new todo interactively.

```bash
/todo create
```

**Prompts:**
1. **Title**: Short description
2. **Priority**: p1 (Critical), p2 (Important), or p3 (Nice-to-Have)
3. **Issue**: Related GitHub issue number (optional)
4. **Dependencies**: Comma-separated list of related todo files (optional)

**Creates file:** `todos/[no-issue]-pending-[priority]-[slug].md`

### Update Todo

Update todo status or add findings.

```bash
# Update status
/todo update <todo-file> --status ready
/todo update <todo-file> --status complete

# Add finding
/todo update <todo-file> --add "Potential SQL injection in login"

# Mark finding checked
/todo update <todo-file> --check 1  # Marks first finding as checked
```

### Show Todo

Display full todo details.

```bash
/todo show <todo-file>
```

## Todo File Format

Todos are stored as markdown files with YAML frontmatter:

```markdown
---
status: pending
priority: p2
issue: "123"
dependencies: ["456-other-todo.md"]
created: 2026-01-12
updated: 2026-01-12
related_prs: ["456"]
---

# Add JWT Authentication

## Problem Statement
Application currently has no authentication mechanism.

## Findings
- [ ] Need to research JWT libraries
- [ ] Must identify required API endpoints
- [ ] Need to document authentication flow

## Solutions
1. Install JWT library
2. Create auth service
3. Add login/logout endpoints
4. Implement middleware for protected routes

## Acceptance Criteria
- [ ] Users can log in with credentials
- [ ] JWT tokens are validated on protected routes
- [ ] Token refresh mechanism works
- [ ] Logout invalidates tokens

## Work Log
- 2026-01-12: Initial creation
- 2026-01-13: Researched JWT libraries, chose jsonwebtoken
```

## Status Lifecycle

```
pending → ready → complete
   ↑         ↓
   └─────────┘
     (blocked)
```

- **pending**: Todo is created but not ready to start
- **ready**: Todo is ready to be worked on (dependencies met)
- **complete**: Todo is finished and acceptance criteria met
- **blocked**: Todo is blocked by a dependency

## Priority Levels

| Priority | Name | Description | Examples |
|----------|------|-------------|----------|
| **p1** | Critical | Blocks release or causes data loss | Security vulnerabilities, data corruption |
| **p2** | Important | Significant improvement but not blocking | Performance issues, code quality |
| **p3** | Nice-to-Have | Enhancements, optimizations, polish | Code cleanup, documentation |

## Quick Examples

**Create a critical todo:**
```bash
/todo create
Title: Fix SQL injection in login
Priority: p1
Issue: 456
Dependencies: (none)
```

**List all pending todos:**
```bash
/todo list --status pending
```

**Mark todo as ready:**
```bash
/todo update 456-pending-p1-sql-injection.md --status ready
```

**Complete a todo:**
```bash
/todo update 456-ready-p1-sql-injection.md --status complete
```

**Add a finding:**
```bash
/todo update 789-pending-p2-optimize-query.md --add "Found missing index on user_id"
```

## Related Skills

- `file-todos` - Full todo system documentation
- `quality-severity` - Severity classification guidelines
- `plan-manager` - Plan and todo lifecycle management
