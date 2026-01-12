#!/usr/bin/env python3
"""
Meta-Workflow Enforcer Hook

This UserPromptSubmit hook ensures Claude follows the meta-workflow for every request.
It analyzes the user's prompt and injects workflow instructions as additional context.
"""

import json
import re
import sys


def analyze_prompt(prompt: str) -> dict:
    """Analyze the prompt and determine workflow requirements."""

    prompt_lower = prompt.lower()

    # Simple queries - direct response, no workflow
    simple_patterns = [
        r'\b(what|how|why|explain|describe|show me|tell me)\b',
        r'\b(which|where|when|who)\b',
        r'\b(meaning|definition|overview)\b',
        r'\?$',  # Ends with question mark
    ]

    for pattern in simple_patterns:
        if re.search(pattern, prompt_lower, re.IGNORECASE):
            return {
                "task_type": "information_query",
                "workflow": "information_query",
                "instruction": "Direct response - no workflow needed"
            }

    # Simple changes - direct execution
    simple_change_patterns = [
        r'\b(fix|correct) typo\b',
        r'\bchange word\b',
        r'\bupdate text\b',
        r'\b(simple|quick) fix\b',
    ]

    for pattern in simple_change_patterns:
        if re.search(pattern, prompt_lower):
            return {
                "task_type": "simple_change",
                "workflow": "direct_execution",
                "instruction": "Execute directly, then run quality gates"
            }

    # New features/development - needs TDD
    feature_patterns = [
        r'\badd (a )?(new )?(feature|function|component|page|route)\b',
        r'\b(create|build|implement) (a )?(new )?\b',
        r'\bform\b.*\bvalidation\b',
        r'\b(user )?interaction\b',
        r'\bnavigation\b',
    ]

    for pattern in feature_patterns:
        if re.search(pattern, prompt_lower):
            return {
                "task_type": "feature_development",
                "workflow": "tdd",
                "instruction": "Read .claude/workflows/tdd-workflow.md and follow it"
            }

    # UI/design work - needs UI iteration
    ui_patterns = [
        r'\b(redesign|design|style|css|look|appearance|visual)\b',
        r'\b(hero|header|footer|layout|component)\b.*\b(redesign|update)\b',
        r'\b(make it|more )?(beautiful|pretty|nice|clean|modern)\b',
    ]

    for pattern in ui_patterns:
        if re.search(pattern, prompt_lower):
            return {
                "task_type": "ui_design",
                "workflow": "ui_iteration",
                "instruction": "Read .claude/workflows/ui-iteration-workflow.md and follow it"
            }

    # Bug fixes - needs bug fix workflow
    bug_patterns = [
        r'\b(bug|error|issue|problem|broken|not working|fail)\b',
        r'\b(debug|troubleshoot|fix)\b',
        r'\b(wrong|incorrect|unexpected)\b',
    ]

    for pattern in bug_patterns:
        if re.search(pattern, prompt_lower):
            return {
                "task_type": "bug_fix",
                "workflow": "bug_fix",
                "instruction": "Read .claude/workflows/bug-fix-workflow.md and follow it"
            }

    # Default: Complex task requiring planning
    return {
        "task_type": "complex_task",
        "workflow": "meta",
        "instruction": "Read .claude/workflows/meta-workflow.md and follow the full 5-step process"
    }


def main():
    """Main hook execution."""

    try:
        # Read hook input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    prompt = input_data.get("prompt", "")

    if not prompt:
        # No prompt to analyze
        sys.exit(0)

    # Analyze the prompt
    analysis = analyze_prompt(prompt)

    # Build context to inject
    context_parts = [
        f"\n## Meta-Workflow Assessment",
        f"\n**Task Type:** {analysis['task_type']}",
        f"**Required Workflow:** {analysis['workflow']}",
        f"**Instruction:** {analysis['instruction']}",
    ]

    # Add specific instructions based on workflow
    if analysis['workflow'] == 'tdd':
        context_parts.extend([
            "\n**TDD Workflow Steps:**",
            "1. Read CLAUDE.md at project root for full context",
            "2. Read .claude/workflows/tdd-workflow.md",
            "3. Write tests FIRST",
            "4. Confirm tests fail",
            "5. Write implementation",
            "6. Run tests until they pass",
            "7. Quality gates: typecheck, lint, build, test",
        ])
    elif analysis['workflow'] == 'ui_iteration':
        context_parts.extend([
            "\n**UI Iteration Workflow Steps:**",
            "1. Read CLAUDE.md at project root for full context",
            "2. Read .claude/workflows/ui-iteration-workflow.md",
            "3. Use frontend-design skill for aesthetic direction",
            "4. Implement initial version",
            "5. Take screenshot",
            "6. Iterate 2-3 times based on feedback",
            "7. Quality gates: typecheck, lint, build, test",
        ])
    elif analysis['workflow'] == 'bug_fix':
        context_parts.extend([
            "\n**Bug Fix Workflow Steps:**",
            "1. Read CLAUDE.md at project root for full context",
            "2. Read .claude/workflows/bug-fix-workflow.md",
            "3. Reproduce the bug",
            "4. Explore code to find root cause",
            "5. Create fix plan",
            "6. Implement fix",
            "7. Add regression test",
            "8. Quality gates: typecheck, lint, build, test",
        ])
    elif analysis['workflow'] == 'meta':
        context_parts.extend([
            "\n**Full Meta-Workflow Required:**",
            "1. Read CLAUDE.md at project root for full context",
            "2. Read .claude/workflows/meta-workflow.md",
            "3. Follow all 7 steps:",
            "   - Step 1: Plan Approach",
            "   - Step 2: Explore (if needed)",
            "   - Step 3: Plan Solution",
            "   - Step 3.5: Plan Scrutiny (if plan created)",
            "   - Step 4: Execute",
            "   - Step 5: Quality Gates (NEVER SKIP - loop until pass)",
            "   - Step 6: Implementation Scrutiny (if non-trivial)",
            "   - Step 7: Plan Completion (Two-Stage Confirmation)",
            "",
            "**CRITICAL - All Subagents Must Read CLAUDE.md and Skills Index:**",
            "- When launching subagents in Step 3.5 (Plan Scrutiny), instruct each to:",
            "  1. First read CLAUDE.md",
            "  2. Then review .claude/skills/index.md to discover available skills",
            "  3. Then perform review (invoking skills as needed)",
            "- When launching subagents in Step 6 (Implementation Scrutiny), instruct each to:",
            "  1. First read CLAUDE.md",
            "  2. Then review .claude/skills/index.md to discover available skills",
            "  3. Then perform review (invoking skills as needed)",
            "",
            "**CRITICAL - Step 7 Two-Stage Confirmation:**",
            "- Stage 1: Ask user \"Do you agree the work is complete, or are there changes/problems?\"",
            "- Stage 2: Run quality gates (typecheck, lint, build, test)",
            "- ONLY set status: completed and quality_gates_passed: true after BOTH stages pass",
        ])
    elif analysis['workflow'] == 'direct_execution':
        context_parts.extend([
            "\n**Direct Execution:**",
            "1. Read CLAUDE.md at project root for full context",
            "2. Make the change directly",
            "3. Run quality gates from CLAUDE.md or package.json",
            "4. Done",
        ])
    else:  # information_query
        context_parts.extend([
            "\n**Information Query:**",
            "Provide a direct response without workflow execution.",
        ])

    # Always remind about quality gates (only for workflows that require execution)
    if analysis['workflow'] != 'information_query':
        context_parts.extend([
            "\n**IMPORTANT - Quality Gates (Step 5):**",
            "After execution, ALWAYS run quality gates defined in CLAUDE.md.",
            "\n1. Read CLAUDE.md and find the Quality Gates section",
            "2. If not defined, look for common scripts in package.json:",
            "   - Type checks: typecheck, check, validate",
            "   - Linting: lint, lint:fix",
            "   - Build: build, compile",
            "   - Tests: test, test:e2e, test:unit, test:all",
            "\nNever skip quality gates.",
        ])

    # Join context and output
    additional_context = "\n".join(context_parts)

    # Return JSON output with additionalContext
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional_context
        }
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
