#!/usr/bin/env python3
"""
Auto-Archive Plans Hook

This PrePromptSubmit hook automatically archives completed plans.
When a plan has `status: completed` in its frontmatter, it gets moved
from `.claude/plans/active/` to `.claude/plans/archive/` and the
indexes are regenerated.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def parse_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter between --- markers
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}

        frontmatter_text = match.group(1)
        frontmatter = {}

        # Parse simple key: value pairs
        for line in frontmatter_text.split('\n'):
            if ':' in line and not line.strip().startswith('#'):
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()

        # Parse boolean fields
        for key in ['quality_gates_passed']:
            if key in frontmatter:
                value = frontmatter[key].lower()
                frontmatter[key] = value in ['true', 'yes', '1']

        return frontmatter
    except Exception:
        return {}


def should_archive_plan(frontmatter: dict, plan_name: str) -> tuple[bool, str]:
    """Determine if a plan should be archived.

    Returns:
        tuple: (should_archive, warning_message)
    """
    status = frontmatter.get('status')
    quality_gates_passed = frontmatter.get('quality_gates_passed', False)

    # Only archive if status is completed
    if status != 'completed':
        return False, ""

    # Check if quality gates have passed
    if not quality_gates_passed:
        warning = (
            f"Warning: Plan '{plan_name}' has status=completed but quality_gates_passed is false/missing. "
            f"Archiving anyway, but this may indicate the workflow was not followed correctly."
        )
        return True, warning

    return True, ""


def update_references(repo_root: Path, plan_name: str) -> int:
    """Update references to the moved plan in all markdown files.

    Returns the number of files updated.
    """
    old_path = f"plans/active/{plan_name}"
    new_path = f"plans/archive/{plan_name}"

    files_updated = []

    # Search all .md files in .claude directory
    for md_file in repo_root.glob('**/*.md'):
        # Skip the archived plan itself and indexes (auto-generated)
        if md_file.name == plan_name or md_file.parent.name == 'indexes':
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if file contains reference to old path
            if old_path in content:
                # Update the reference
                updated_content = content.replace(old_path, new_path)

                # Only write if something changed
                if updated_content != content:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    files_updated.append(str(md_file.relative_to(repo_root)))
        except Exception:
            # Skip files that can't be read/written
            continue

    return files_updated


def main():
    """Main hook execution."""

    # Get paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    plans_active_dir = repo_root / 'plans' / 'active'
    plans_archive_dir = repo_root / 'plans' / 'archive'
    update_indexes_script = repo_root / 'bin' / 'update-indexes.sh'

    # Ensure archive directory exists
    plans_archive_dir.mkdir(parents=True, exist_ok=True)

    # Find completed plans in active directory
    archived_plans = []
    warnings = []

    for plan_file in plans_active_dir.glob('*.md'):
        # Skip template files
        if plan_file.name.startswith('.'):
            continue

        frontmatter = parse_frontmatter(plan_file)

        # Check if plan should be archived
        should_archive, warning = should_archive_plan(frontmatter, plan_file.name)

        if warning:
            warnings.append(warning)

        if should_archive:
            # Move to archive
            archive_path = plans_archive_dir / plan_file.name

            # Handle name collisions (unlikely but possible)
            if archive_path.exists():
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                archive_path = plans_archive_dir / f"{plan_file.stem}-{timestamp}{plan_file.suffix}"

            plan_file.rename(archive_path)
            archived_plans.append(plan_file.name)

    # If any plans were archived, update references and indexes
    all_updated_files = []
    if archived_plans:
        # Update references in other files
        for plan_name in archived_plans:
            updated = update_references(repo_root, plan_name)
            if updated:
                all_updated_files.extend(updated)

        # Update indexes
        try:
            subprocess.run(
                [str(update_indexes_script)],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True
            )
        except Exception as e:
            # Log but don't fail - archival is more important than indexes
            print(f"Warning: Failed to update indexes: {e}", file=sys.stderr)

    # Build additional context if plans were archived
    additional_context = ""

    # Add warnings first (if any)
    if warnings:
        additional_context += "\n## Archive Warnings\n\n"
        for warning in warnings:
            additional_context += f"- {warning}\n"
        additional_context += "\n"

    if archived_plans:
        plan_list = ', '.join(archived_plans)
        additional_context += f"\n## Auto-Archived Plans\n\nThe following completed plans were automatically moved to archive:\n- {plan_list}\n\n"
        if all_updated_files:
            additional_context += f"References updated in:\n"
            for f in all_updated_files:
                additional_context += f"- {f}\n"
        additional_context += "Indexes have been updated.\n"

    # Return JSON output
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PrePromptSubmit",
            "additionalContext": additional_context
        }
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
