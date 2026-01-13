---
name: file-todos
description: This skill should be used when managing the file-based todo tracking system in the todos/ directory. Triggers on requests like "create a todo", "update todo status", "manage todos", "check todo dependencies".
updated: 2026-01-12
---

# File-Based Todo System

## Core Philosophy

The file-based todo system provides persistent, trackable work items using markdown files with YAML frontmatter. This enables better organization, dependency tracking, and historical documentation of work.

## Key Sections

### Todo File Structure

**Location:** `todos/[issue-id]-[status]-[priority]-[description].md`

**Naming Convention:**
- `issue-id`: GitHub issue number (optional, use "no-issue" if none)
- `status`: `pending`, `ready`, or `complete`
- `priority`: `p1` (critical), `p2` (important), or `p3` (nice-to-have)
- `description`: Short kebab-case description

**Example:** `123-ready-p2-add-authentication.md`

### Frontmatter Schema

```yaml
---
status: pending|ready|complete
priority: p1|p2|p3
issue: "123"  # GitHub issue number
dependencies: ["456-other-todo.md"]
created: 2026-01-12
updated: 2026-01-12
related_prs: ["456"]
assignee: username
estimated_hours: 4
tags: [authentication, security]
---
```

### Status Lifecycle

1. **pending** - Todo is created but not ready to start
2. **ready** - Todo is ready to be worked on (dependencies met)
3. **complete** - Todo is finished and verified

Transition rules:
- `pending` → `ready`: When all dependencies are satisfied
- `ready` → `complete`: When acceptance criteria are met

### Priority Levels

- **P1 (Critical)**: Blocks release or causes data loss
- **P2 (Important)**: Significant improvement but not blocking
- **P3 (Nice-to-Have)**: Enhancements, optimizations, polish

### Todo Template

```markdown
---
status: pending
priority: p2
issue: "123"
dependencies: []
created: 2026-01-12
updated: 2026-01-12
---

# [Title]

## Problem Statement
[Clear description of the issue or problem to solve]

## Findings
- [ ] Finding 1
- [ ] Finding 2
- [ ] Finding 3

## Solutions
1. Concrete step 1
2. Concrete step 2
3. Concrete step 3

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Work Log
- 2026-01-12: Initial creation
- 2026-01-13: Investigated solution options
```

## Usage Examples

**Example 1: Creating a new todo**
> User: "Create a todo for adding JWT authentication"

> Assistant: I'll create a new todo file for JWT authentication.

```markdown
---
status: pending
priority: p1
issue: "no-issue"
dependencies: []
created: 2026-01-12
updated: 2026-01-12
tags: [authentication, security]
---

# Add JWT Authentication

## Problem Statement
Application currently has no authentication mechanism. Users need secure access to protected routes.

## Findings
- [ ] Research JWT library options
- [ ] Identify required API endpoints
- [ ] Document authentication flow

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
```

**Example 2: Updating todo status**
> User: "Mark todo 123 as ready"

> Assistant: I'll update the todo status to ready and verify all dependencies are met.

**Example 3: Checking dependencies**
> User: "What todos are blocking work on 123?"

> Assistant: I'll check the dependencies listed in the todo and report their current status.

## Workflows

### Creating a Todo
1. Determine priority level (p1/p2/p3)
2. Check for related GitHub issues
3. Identify any blocking dependencies
4. Create file with proper naming convention
5. Fill in template sections

### Updating a Todo
1. Read existing todo file
2. Update status/acceptance criteria/findings
3. Update `updated` date in frontmatter
4. Add entry to work log

### Completing a Todo
1. Verify all acceptance criteria are met
2. Update status to `complete`
3. Add completion note to work log
4. Check if any dependent todos can now be marked `ready`

## Success Criteria
- [ ] Todo files follow naming convention
- [ ] All required frontmatter fields present
- [ ] Dependencies properly tracked
- [ ] Status transitions follow lifecycle rules
- [ ] Work log maintained for historical tracking

## Integration with Workflows

The file-based todo system integrates with:
- **Triage workflow**: Categorize findings into todos
- **Review workflow**: Create todos for P1/P2 findings
- **Plan workflow**: Break plans into actionable todos

## Commands

Use the `/todo` command for todo management:
- `/todo list` - List all todos (with optional `--status` and `--priority` filters)
- `/todo create` - Create new todo interactively
- `/todo update <file>` - Update todo status or add findings
- `/todo show <file>` - Display full todo details
