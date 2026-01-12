#!/usr/bin/env bash
# Auto-generate index files for .claude directories
# Usage: .claude/bin/update-indexes.sh

set -euo pipefail

CLAUDE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INDEX_DIR="$CLAUDE_DIR/indexes"

# Create indexes directory if it doesn't exist
mkdir -p "$INDEX_DIR"

# Function to generate index markdown
generate_index() {
    local dir="$1"
    local output="$2"
    local title="$3"

    {
        echo "# $title"
        echo ""
        echo "Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
        echo ""
        echo "| File | Last Modified | Status | Description |"
        echo "|------|--------------|--------|-------------|"

        # Find all .md files, sort by modification time (newest first)
        find "$dir" -type f -name "*.md" ! -name ".template.md" ! -name "_index.md" -printf "%T@ %p\n" | \
            sort -rn | \
            while read -r timestamp filepath; do
                filename=$(basename "$filepath")
                mtime=$(date -d "@${timestamp%.*}" -u +"%Y-%m-%d %H:%M UTC" 2>/dev/null || date -r "${timestamp%.*}" -u +"%Y-%m-%d %H:%M UTC")

                # Try to extract status from frontmatter
                status=$(grep -m 1 '^status:' "$filepath" 2>/dev/null | sed 's/status: //' || echo "N/A")

                # Try to extract description/purpose from frontmatter
                description=$(grep -m 1 '^description:' "$filepath" 2>/dev/null | sed 's/description: //' || echo "")

                # Make relative path for display
                relpath="${filepath#$CLAUDE_DIR/}"

                # Extract title from first heading or use filename
                title_val=$(grep -m 1 '^# ' "$filepath" 2>/dev/null | sed 's/^# //' || echo "")
                if [[ -z "$title_val" ]]; then
                    title_val="$filename"
                fi

                # Create clickable link
                link="[$title_val]($relpath)"

                echo "| $link | $mtime | $status | $description |"
            done
    } > "$output"
}

# Generate indexes
generate_index "$CLAUDE_DIR/plans" "$INDEX_DIR/_plans.md" "Plans Index"
generate_index "$CLAUDE_DIR/context" "$INDEX_DIR/_context.md" "Context Index"
generate_index "$CLAUDE_DIR/workflows" "$INDEX_DIR/_workflows.md" "Workflows Index"

echo "Updated indexes:"
echo "  - $INDEX_DIR/_plans.md"
echo "  - $INDEX_DIR/_context.md"
echo "  - $INDEX_DIR/_workflows.md"
