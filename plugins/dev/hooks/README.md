# Git Safety Hook

Prevents destructive Git operations on protected branches.

## What It Does

- Blocks pushes to protected branches (default: `main`, `master`)
- Prevents force pushes (can be overridden via `ALLOW_FORCE_PUSH=true`)
- Prevents deletion of protected branches
- Logs all commands to audit log

## Installation

Add to your `.claude/settings.json` hooks:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "./.claude/hooks/git-safety-check.sh",
        "enabled": true
      }
    ]
  }
}
```

## Configuration

Set environment variables to customize behavior:

| Variable | Default | Description |
|----------|---------|-------------|
| `PROTECTED_BRANCHES` | `main,master` | Comma-separated list of protected branches |
| `ALLOW_FORCE_PUSH` | `false` | Allow force pushes when set to `true` |
| `AUDIT_LOG` | `.claude/logs/git-audit.log` | Path to audit log file |
| `WORKSPACE_ROOT` | `.` | Root directory of the workspace |

## Examples

```bash
# Allow force push for one-time operation
ALLOW_FORCE_PUSH=true git push --force

# Set custom protected branches
PROTECTED_BRANCHES=main,master,production,staging ./git-safety-check.sh git push

# Custom audit log location
AUDIT_LOG=/var/log/git-audit.log ./git-safety-check.sh git push
```
