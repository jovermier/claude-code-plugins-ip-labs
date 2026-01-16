---
name: git-workflow
description: Manages git operations including commits, pull requests, merge requests, and branching. Use when creating commits, handling git conflicts, managing branches, or reviewing git history. Enforces clean commit messages without author attribution.
allowed-tools: Bash
---

# Git Workflow

## Purpose

Handle git operations with best practices for commit messages, pull/merge requests, and branch management. Ensures clean, professional git history without author attribution in descriptions.

## Critical Rule: No Author Attribution

**NEVER include author names in commit message bodies, PR descriptions, or MR descriptions.**

- **Forbidden patterns:** "Co-Authored-By:", "Authored by:", "Written by:", "Created by:"
- **Rationale:** Git already tracks authors via metadata. Adding names to descriptions creates noise and maintenance burden.
- **Correct approach:** Let git's authorship metadata handle attribution. Focus descriptions on WHAT and WHY, not WHO.

### Examples

**❌ WRONG - Author in description:**
```
feat: add new feature

Co-Authored-By: Claude <noreply@anthropic.com>
```

**✅ CORRECT - Clean description:**
```
feat: add new feature

Add authentication middleware with JWT token validation.
Includes login endpoint and refresh token rotation.
```

## When to Use

- Creating git commits
- Creating pull requests or merge requests
- Managing git branches
- Resolving merge conflicts
- Reviewing git history
- Amending commits (following safety rules)

## Process

### Creating Commits

1. **Stage relevant files**
   ```bash
   git add [files]
   ```

2. **Write commit message**
   - Use [Conventional Commits](https://www.conventionalcommits.org/) format (commitlint spec)
   - Format: `type(scope): description`
   - Keep subject line under 72 characters
   - Wrap body at 72 characters
   - Focus on WHAT and WHY, not HOW
   - **NEVER** add Co-Authored-By or author attribution

3. **Create commit**
   ```bash
   git commit -m "$(cat <<'EOF'
   type(scope): brief description

   Detailed explanation of changes and reasoning.
   EOF
   )"
   ```

### Commit Message Types

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Code style (formatting, no logic change) |
| `refactor` | Code refactoring |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Maintenance, build process, dependencies |

### Creating Pull/Merge Requests

1. **Ensure clean branch name**
   ```bash
   git checkout -b feature/short-description
   ```

2. **Push to remote**
   ```bash
   git push -u origin feature/short-description
   ```

3. **Create PR/MR with gh CLI**
   ```bash
   gh pr create --title "type(scope): description" --body "$(cat <<'EOF'
   ## Summary
   - Bullet point 1
   - Bullet point 2

   ## Changes
   - Detailed change 1
   - Detailed change 2

   ## Testing
   - Test case 1
   - Test case 2
   EOF
   )"
   ```

**PR/MR Description Template:**
```markdown
## Summary
[Brief overview - 2-3 bullet points]

## Changes
- [Specific change 1]
- [Specific change 2]
- [Specific change 3]

## Testing
- [Test case 1]
- [Test case 2]

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Handling Merge Conflicts

1. **Ensure main branch is up to date**
   ```bash
   git checkout main
   git pull
   ```

2. **Rebase feature branch**
   ```bash
   git checkout feature/branch
   git rebase main
   ```

3. **Resolve conflicts**
   - Open conflicted files
   - Look for `<<<<<`, `====`, `>>>>>` markers
   - Choose correct content
   - Remove conflict markers
   - Save files

4. **Continue rebase**
   ```bash
   git add [resolved-files]
   git rebase --continue
   ```

5. **Force push if needed**
   ```bash
   git push --force-with-lease
   ```

### Git Safety Rules

**NEVER do these without explicit user permission:**
- `git push --force` (use `--force-with-lease` instead)
- `git reset --hard` (warn user they'll lose work)
- `git clean -fd` (warn about untracked files)
- `git commit --amend` after push (requires force push)

**Always warn user before:**
- Force pushing
- Hard resetting
- Cleaning untracked files
- Rewriting public history

### Branch Naming Conventions

```
feature/feature-name
bugfix/bug-description
hotfix/critical-fix
refactor/code-improvement
docs/documentation-update
test/test-coverage
release/version-number
```

## Common Commands Reference

```bash
# Status
git status

# Branch operations
git branch                    # List branches
git checkout -b new-branch    # Create and switch
git branch -d old-branch      # Delete local
git push origin --delete branch-name  # Delete remote

# Staging
git add .                     # Stage all
git add file.txt              # Stage specific
git restore --staged file.txt # Unstage

# Commits
git commit -m "message"       # Commit staged
git log --oneline -5          # Recent commits
git show HEAD                 # Show last commit

# Remote sync
git fetch                     # Get remote changes
git pull                      # Fetch + merge
git push                      # Send to remote
```

## Troubleshooting

### "Commit message is empty"
- Ensure message is in quotes
- Check for unclosed heredoc (`EOF`)
- Verify no trailing backslashes

### "Nothing to commit"
- Check `git status` to see if files are staged
- Use `git add` to stage changes first

### "Failed to push some refs"
- Remote has new commits: `git pull` first
- Diverged branches: `git pull --rebase` then resolve conflicts

### Merge conflict markers not found
- Run `git status` to see conflicted files
- Open each file and search for `<<<<<`

## Quality Checklist

Before completing git operations:
- [ ] Commit message follows conventional format
- [ ] No author attribution in description
- [ ] Subject line under 72 characters
- [ ] Body wrapped at 72 characters
- [ ] Branch name follows conventions
- [ ] PR/MR description includes summary and testing
- [ ] No sensitive data in commits
- [ ] Conflicts resolved (if applicable)

## Integration with Other Skills

- **file-todos** - Track TODO items in commits
- **workflows:compound** - Document solved problems
