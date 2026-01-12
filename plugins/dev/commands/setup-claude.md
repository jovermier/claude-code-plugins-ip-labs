# /project:setup

Analyzes the current project and generates or updates the `CLAUDE.md` file with relevant skills, workflows, and project context from the installed marketplace plugins.

## What It Does

1. **Discovers project technologies** by analyzing `package.json`, config files, and directory structure
2. **Scans marketplace plugins** to discover all available skills, workflows, and commands
3. **Matches technologies to plugins** using plugin keywords and descriptions
4. **Creates or updates CLAUDE.md** with:
   - Project description and tech stack
   - Relevant skills from matched plugins
   - Applicable workflows and commands
   - Project-specific conventions and patterns

## When to Use

- **Starting a new project** - Generate initial CLAUDE.md with all relevant context
- **Adding new technologies** - Update CLAUDE.md after adding dependencies
- **Onboarding** - Help Claude understand the project structure quickly
- **Project evolution** - Keep CLAUDE.md in sync as the project grows

## Usage

```bash
/project:setup
```

## The Process

This command follows the [CLAUDE.md Setup Workflow](../workflows/claude-md-setup.md) which:

1. **Scans the marketplace plugins**
   - Reads all `plugin.json` files from the `plugins/` directory
   - Collects available skills, commands, and workflows
   - Builds a registry of plugin capabilities

2. **Analyzes the workspace**
   - Reads `package.json` for dependencies
   - Checks for framework config files
   - Examines directory structure

3. **Matches technologies to plugins**
   - Compares detected dependencies against plugin keywords
   - Matches config patterns to plugin descriptions
   - Selects relevant skills from matched plugins

4. **Generates CLAUDE.md**
   - Creates new file if none exists
   - Preserves existing custom content when updating
   - Adds sections: Tech Stack, Available Skills, Workflows, Commands

## Example Output

```markdown
# My Project

A web application built with modern frameworks.

## Tech Stack

- **Frontend**: [Detected frameworks from package.json]
- **Backend**: [Detected backend technologies]
- **Testing**: [Testing frameworks]

## Available Skills

| Skill | Plugin | Purpose |
|-------|--------|---------|
| [skill-name] | [plugin] | [From plugin description] |

## Workflows

- [Workflow Name](path) - [Description]

## Commands

| Command | Purpose |
|---------|---------|
| `/command:name` | [Description] |
```

## Notes

- This command discovers all plugins dynamically - no technologies are hardcoded
- Plugin matching uses `keywords` and `description` from each plugin's `plugin.json`
- Existing CLAUDE.md content is preserved during updates
