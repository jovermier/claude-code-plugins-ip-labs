# Changelog

All notable changes to the dev plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-01-13

### Added
- **Multi-language CLAUDE.md generation** - `/project:setup` now supports any project type
- **Sub-workflow architecture** - Router workflow detects project type and routes to language-specific sub-workflow
- **7 new language-specific sub-workflows:**
  - `claude-md-setup-javascript.md` - JavaScript/TypeScript (Node.js, Next.js, React, Vue)
  - `claude-md-setup-python.md` - Python (Django, FastAPI, Flask, Poetry, pip)
  - `claude-md-setup-rust.md` - Rust (Cargo, crates)
  - `claude-md-setup-go.md` - Go (go modules)
  - `claude-md-setup-php.md` - PHP (Composer, Laravel, Symfony)
  - `claude-md-setup-ruby.md` - Ruby (Bundler, Rails, Sinatra)
  - `claude-md-setup-java.md` - Java (Maven, Gradle, Spring Boot)
  - `claude-md-setup-generic.md` - Fallback for unknown project types
- **Language-aware template variable resolution** - Resolves `[package-manager]`, `[test-command]`, etc. per ecosystem
- **Framework-specific command detection** - Detects dev, test, build commands for each language/framework
- **Context7 Skill Generator** - Automatically generates skills from Context7 MCP documentation responses
- **Command:** `/skill:from-context7` - Generate a skill from Context7 MCP documentation

### Changed
- **`/project:setup` command** - Now works with any project type, not just JavaScript
- **`claude-md-setup.md`** - Converted from JavaScript-specific to router workflow
- **Plugin description** - Updated to mention multi-language CLAUDE.md generation

## [1.1.0] - 2026-01-12

### Added
- **13 Specialized Agents:**
  - Review Agents (9): architecture-strategist, agent-native-reviewer, code-simplicity-reviewer, data-integrity-guardian, data-migration-expert, deployment-verification-agent, pattern-recognition-specialist, performance-oracle, security-sentinel
  - Research Agents (4): repo-research-analyst, best-practices-researcher, framework-docs-researcher, git-history-analyzer
- **4 Workflow Commands:** `/workflows:plan`, `/workflows:review`, `/workflows:compound`, `/workflows:work`
- **2 Additional Commands:** `/deepen-plan`, `/todo`
- **3 Skills:** file-todos, quality-severity, plan-manager (enhanced)
- **Agent discovery pattern** in meta-workflow scrutiny steps
- **P1/P2/P3 severity classification** integrated into workflow
- **File-based todo system** with dependency tracking
- **Knowledge compounding** system with docs/solutions directory
- Todo template at [todos/.template.md](../../todos/.template.md)
- Solutions index at [docs/solutions/_index.md](../../docs/solutions/_index.md)

### Changed
- Meta-workflow.md Step 3.5 (Plan Scrutiny) now uses agent discovery with 5 parallel agents
- Meta-workflow.md Step 6 (Implementation Scrutiny) now uses agent discovery with 9 parallel agents
- All findings classified with P1/P2/P3 severity levels
- Plans include scrutiny results and quality gate status
- Meta-workflow decision matrix updated to include new workflow commands
- marketplace.json updated to v1.1.0 with all new components

### Fixed
- marketplace.json now accurately lists all agents, commands, and skills
- Meta-workflow maintains plugin-agnostic design with agent discovery pattern

## [1.0.0] - 2026-01-12

### Added
- Initial dev plugin release
- Core workflow commands (`/project:setup`, `/project:new-page`, etc.)
- Meta-workflow for project orchestration
- TDD workflow for test-driven development
- UI iteration workflow
- Bug fix workflow
- Auto-archive plan hooks
- Meta-workflow enforcer hooks
- Plan management skill (`/plan-manager`)
