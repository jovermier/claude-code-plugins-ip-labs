#!/bin/bash

# Git safety hook to prevent dangerous operations
# This is a general-purpose hook that works with any Git repository

set -euo pipefail

# Configuration - can be overridden via environment variables
PROTECTED_BRANCHES="${PROTECTED_BRANCHES:-main,master}"
ALLOW_FORCE_PUSH="${ALLOW_FORCE_PUSH:-false}"
AUDIT_LOG="${AUDIT_LOG:-.claude/logs/git-audit.log}"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-.}"

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Extract the git command being run
command="$*"

# Log function
log_audit() {
    local log_dir
    log_dir="$(dirname "$AUDIT_LOG")"
    if [[ ! -d "$log_dir" ]]; then
        mkdir -p "$log_dir" 2>/dev/null || true
    fi
    echo "$(date -Iseconds): $command" >> "$WORKSPACE_ROOT/$AUDIT_LOG" 2>/dev/null || true
}

# Check if command is a git command
if [[ "$command" != git* ]]; then
    exit 0
fi

# Check if trying to push to a protected branch
if [[ "$command" == *"push"* ]]; then
    current_branch=$(git -C "$WORKSPACE_ROOT" branch --show-current 2>/dev/null || echo "unknown")

    # Convert PROTECTED_BRANCHES to array
    IFS=',' read -ra protected <<< "$PROTECTED_BRANCHES"

    for branch in "${protected[@]}"; do
        branch=$(echo "$branch" | xargs) # trim whitespace

        # Check if explicitly pushing to protected branch
        if [[ "$command" == *"$branch"* ]]; then
            echo -e "${RED}❌ ERROR: Pushing to protected branch '$branch' is forbidden!${NC}"
            echo ""
            echo "Create a feature branch instead:"
            echo "  git checkout -b feature/your-feature-name"
            echo "  git push origin feature/your-feature-name"
            log_audit
            exit 1
        fi

        # Check if currently on protected branch
        if [[ "$current_branch" == "$branch" ]]; then
            echo -e "${RED}❌ ERROR: You are on the protected branch '$current_branch'${NC}"
            echo ""
            echo "Create a feature branch first:"
            echo "  git checkout -b feature/your-feature-name"
            echo ""
            echo "Or set ALLOW_FORCE_PUSH=true if this is intentional (not recommended)"
            log_audit
            exit 1
        fi
    done

    echo -e "${GREEN}✅ Safe to push to branch: $current_branch${NC}"
fi

# Check for force push
if [[ "$ALLOW_FORCE_PUSH" != "true" ]] && { [[ "$command" == *"--force" ]] || [[ "$command" == *"-f "* ]] || [[ "$command" == *" --force "* ]]; }; then
    echo -e "${RED}❌ ERROR: Force push is forbidden for safety!${NC}"
    echo ""
    echo "Use regular push or create a new branch."
    echo "To override (not recommended), set: ALLOW_FORCE_PUSH=true"
    log_audit
    exit 1
fi

# Check for destructive operations on protected branches
if [[ "$command" == *"branch"*"-d"* ]] || [[ "$command" == *"branch"*"-D"* ]]; then
    for branch in "${protected[@]}"; do
        branch=$(echo "$branch" | xargs)
        if [[ "$command" == *"$branch"* ]]; then
            echo -e "${YELLOW}⚠️  WARNING: Attempting to delete protected branch '$branch'${NC}"
            echo ""
            echo "This is generally not recommended. If you're sure, use:"
            echo "  ALLOW_FORCE_PUSH=true [your command]"
            log_audit
            exit 1
        fi
    done
fi

echo -e "${GREEN}✅ Git command allowed${NC}"
log_audit
exit 0
