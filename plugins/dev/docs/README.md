# Dev Plugin Documentation

> **Version:** 1.3.0
> **Last Updated:** 2026-01-15
> **Plugin:** Dev (Core development workflows, agents, commands, and skills)

Comprehensive documentation for the Dev plugin - Core development workflows, agents, commands, and skills for Innovative Prospects projects.

---

## 📚 Documentation Index

### 🆕 Skills (v1.3.0)
**Skill Lifecycle Management Suite** - 4 skills for complete skill development and optimization

| Document | Description |
|----------|-------------|
| [CLAUDE_SKILLS_ARCHITECTURE.md](skills/CLAUDE_SKILLS_ARCHITECTURE.md) | Skills architecture and Progressive Disclosure Architecture (PDA) patterns |

**Available Skills:**
- **skill-generator** - Generate production-ready Claude Code skills from descriptions
- **skill-reviewer** - Review skills for quality, best practices, and PDA compliance
- **skill-optimizer** - Refactor skills using PDA (80-95% token savings)
- **skill-architect** - Meta-orchestrator for complete skill lifecycle workflows

**Quick Start:**
```bash
# Create a new skill
@skill-architect Create a production-ready skill for processing JSON files

# Review and optimize existing skill
@skill-architect Audit .claude/skills/my-skill/ and optimize it

# Review skill library
@skill-architect Audit all my skills and prioritize improvements
```

### 👥 Agents (v1.1.0+)
**13 Specialized Agents** - 9 review agents + 4 research agents

| Document | Description |
|----------|-------------|
| [AGENTS_WORKFLOWS.md](agents/AGENTS_WORKFLOWS.md) | Agents, subagents, hooks, and workflow automation |

**Review Agents (9):**
- architecture-strategist - Architecture design evaluation
- agent-native-reviewer - Agent-native code review
- code-simplicity-reviewer - YAGNI and over-engineering checks
- data-integrity-guardian - Database integrity validation
- data-migration-expert - Migration safety verification
- deployment-verification-agent - Deployment readiness
- pattern-recognition-specialist - Pattern consistency
- performance-oracle - Performance analysis
- security-sentinel - Security audit and vulnerabilities

**Research Agents (4):**
- repo-research-analyst - Repository structure analysis
- best-practices-researcher - Industry best practices
- framework-docs-researcher - Framework documentation
- git-history-analyzer - Git history insights

### 📖 Guides
**Core Development Guides**

| Document | Description | Audience |
|----------|-------------|----------|
| [CLAUDE_CODE_COMPLETE_GUIDE.md](guides/CLAUDE_CODE_COMPLETE_GUIDE.md) | Comprehensive Claude Code feature overview | All users |
| [CLAUDE.md_PATTERNS.md](guides/CLAUDE.md_PATTERNS.md) | CLAUDE.md structure and best practices | All users |
| [CONTEXT_MANAGEMENT.md](guides/CONTEXT_MANAGEMENT.md) | Token optimization strategies | Cost-conscious users |

### 🔄 Workflows
**Development Workflows** - TDD, UI iteration, bug fix, meta-workflow

| Location | Description |
|----------|-------------|
| [../../workflows/](../../workflows/) | Workflow command definitions |
| `/workflows:plan` | Transform features into well-structured project plans |
| `/workflows:review` | Multi-agent parallel analysis with severity classification |
| `/workflows:compound` | Document solved problems as categorized knowledge |
| `/workflows:work` | Execute structured work with quality gates and scrutiny |

### 📋 Planning
**Research & Methodology**

| Document | Description |
|----------|-------------|
| [RESEARCH_PLAN.md](RESEARCH_PLAN.md) | Research methodology and documentation roadmap |

---

## 🚀 Quick Start by Goal

### I want to create or manage Claude Code Skills

1. Read [skills/CLAUDE_SKILLS_ARCHITECTURE.md](skills/CLAUDE_SKILLS_ARCHITECTURE.md)
2. Use **@skill-architect** to:
   - Create new skills: `@skill-architect Create a skill for X`
   - Review skills: `@skill-architect Review my skill`
   - Optimize skills: `@skill-architect Optimize this skill`
   - Audit all skills: `@skill-architect Audit all my skills`

### I want to use agents for code review

1. Read [agents/AGENTS_WORKFLOWS.md](agents/AGENTS_WORKFLOWS.md)
2. Use specific agents:
   - `@security-sentinel` - Security audit
   - `@performance-oracle` - Performance analysis
   - `@code-simplicity-reviewer` - Check for over-engineering
   - Or use `/workflows:review` for multi-agent parallel review

### I want to configure my project

1. Read [guides/CLAUDE.md_PATTERNS.md](guides/CLAUDE.md_PATTERNS.md)
2. Use `/project:setup` to generate CLAUDE.md for your project
3. Apply progressive disclosure for large projects

### I want to reduce token usage

1. Read [guides/CONTEXT_MANAGEMENT.md](guides/CONTEXT_MANAGEMENT.md)
2. Apply PDA patterns to skills and CLAUDE.md
3. Use @skill-optimizer to refactor existing skills

### I want to learn Claude Code features

1. Read [guides/CLAUDE_CODE_COMPLETE_GUIDE.md](guides/CLAUDE_CODE_COMPLETE_GUIDE.md)
2. Explore agents, workflows, and commands
3. Practice with real projects

---

## 🎯 Feature Overview by Version

### v1.3.0 - Skill Lifecycle Management (Latest)

**4 New Skills:**
- **skill-generator** - Generate skills from descriptions with best practices
- **skill-reviewer** - Quality assessment with scoring (1-10) and P1/P2/P3 classification
- **skill-optimizer** - PDA refactoring achieving 80-95% token savings
- **skill-architect** - Meta-orchestrator for complete skill lifecycle workflows

**Key Benefits:**
- Automate skill creation from natural language
- Ensure quality standards with automated reviews
- Optimize token usage with PDA refactoring
- Manage skill libraries with audit workflows

**New Documentation:**
- 8 comprehensive documents organized by feature
- Progressive Disclosure Architecture (PDA) patterns
- Token optimization strategies
- Agent and workflow guides

### v1.2.0 - Multi-Language Support

- **Multi-language CLAUDE.md generation** - Supports JavaScript, Python, Rust, Go, PHP, Ruby, Java
- **Sub-workflow architecture** - Routes to language-specific workflows
- **Context7 Skill Generator** - Generate skills from MCP documentation
- **Command:** `/skill:from-context7` - Generate skills from Context7 MCP docs

### v1.1.0 - Agents & Workflows

- **13 Specialized Agents** - Review and research agents
- **4 Workflow Commands** - `/workflows:plan`, `/workflows:review`, `/workflows:compound`, `/workflows:work`
- **2 Additional Commands** - `/deepen-plan`, `/todo`
- **3 Enhanced Skills** - file-todos, quality-severity, plan-manager
- **P1/P2/P3 Severity** - Quality classification system
- **File-based Todo System** - Dependency tracking
- **Knowledge Compounding** - Solutions index system

### v1.0.0 - Initial Release

- **Core Workflow Commands** - `/project:setup`, `/project:new-page`, `/project:new-blog-post`, `/project:test-ui`
- **Meta-workflow** - Project orchestration
- **TDD Workflow** - Test-driven development
- **UI Iteration Workflow** - Visual development iteration
- **Bug Fix Workflow** - Systematic debugging
- **Auto-archive Plan Hooks** - Automatic plan cleanup
- **Meta-workflow Enforcer Hooks** - Workflow enforcement

---

## 📖 Reading Guide

### By Experience Level

**Beginner:**
1. [guides/CLAUDE_CODE_COMPLETE_GUIDE.md](guides/CLAUDE_CODE_COMPLETE_GUIDE.md)
2. [guides/CLAUDE.md_PATTERNS.md](guides/CLAUDE.md_PATTERNS.md)
3. [skills/CLAUDE_SKILLS_ARCHITECTURE.md](skills/CLAUDE_SKILLS_ARCHITECTURE.md)

**Intermediate:**
1. [guides/CONTEXT_MANAGEMENT.md](guides/CONTEXT_MANAGEMENT.md)
2. [agents/AGENTS_WORKFLOWS.md](agents/AGENTS_WORKFLOWS.md)
3. Practice with skill-architect workflows

**Advanced:**
1. [RESEARCH_PLAN.md](RESEARCH_PLAN.md)
2. Create custom agents and workflows
3. Contribute skills to marketplace

### By Goal

| Goal | Read This |
|------|-----------|
| Install and learn Claude Code | [guides/CLAUDE_CODE_COMPLETE_GUIDE.md](guides/CLAUDE_CODE_COMPLETE_GUIDE.md) |
| Configure my project | [guides/CLAUDE.md_PATTERNS.md](guides/CLAUDE.md_PATTERNS.md) |
| Reduce token costs | [guides/CONTEXT_MANAGEMENT.md](guides/CONTEXT_MANAGEMENT.md) |
| Create reusable skills | [skills/CLAUDE_SKILLS_ARCHITECTURE.md](skills/CLAUDE_SKILLS_ARCHITECTURE.md) |
| Automate workflows | [agents/AGENTS_WORKFLOWS.md](agents/AGENTS_WORKFLOWS.md) |
| Use agents for review | [agents/AGENTS_WORKFLOWS.md](agents/AGENTS_WORKFLOWS.md) |
| Understand documentation | [RESEARCH_PLAN.md](RESEARCH_PLAN.md) |

---

## 🎯 Key Concepts

### Progressive Disclosure Architecture (PDA)

The unifying pattern across all Claude Code customization:

- **SKILL.md** - Orchestrator with routing logic (3-5KB)
- **reference/** - Detailed documentation loaded on-demand
- **scripts/** - Executable utilities (zero token cost)
- **AI reasoning** - Claude handles intelligence and adaptation

**Result:** 80-95% token savings for complex skills/projects

### Context Management

Efficient information delivery to Claude Code:

- **Global CLAUDE.md** - Personal preferences
- **Project CLAUDE.md** - Project-specific context
- **Progressive disclosure** - Load details on-demand
- **MCP integration** - Connect to external sources

**Result:** 40-70% token reduction, improved output quality

### Agent Orchestration

Specialized AI assistants for specific tasks:

- **Subagents** - Isolated contexts for focused expertise
- **Hooks** - Trigger on events (pre/post tool use)
- **Workflows** - Multi-step automation pipelines

**Result:** Scalable automation, consistent quality

---

## 🛠️ Dev Plugin Structure

```
plugins/dev/
├── agents/              # 13 specialized agents (9 review + 4 research)
├── bin/                 # Utility scripts
├── commands/            # Slash command definitions
├── context/             # Context providers
├── docs/                # This documentation
│   ├── agents/          # Agent documentation
│   │   └── AGENTS_WORKFLOWS.md
│   ├── guides/          # Core guides
│   │   ├── CLAUDE_CODE_COMPLETE_GUIDE.md
│   │   ├── CLAUDE.md_PATTERNS.md
│   │   └── CONTEXT_MANAGEMENT.md
│   ├── skills/          # Skill documentation
│   │   └── CLAUDE_SKILLS_ARCHITECTURE.md
│   ├── workflows/       # Workflow docs (placeholder)
│   ├── README.md        # This file
│   └── RESEARCH_PLAN.md # Research methodology
├── hooks/               # Event hooks (auto-archive, enforcer)
├── indexes/             # Plan indexes
├── plans/               # Workflow plans
├── skills/              # 10 skills total
│   ├── skill-generator  # 🆕 Generate skills
│   ├── skill-reviewer   # 🆕 Review skills
│   ├── skill-optimizer  # 🆕 Optimize skills
│   ├── skill-architect  # 🆕 Skill orchestration
│   ├── context7-skill-generator
│   ├── file-todos
│   ├── plan-manager
│   └── quality-severity
└── workflows/           # Workflow definitions
    ├── bug-fix-workflow.md
    ├── claude-md-setup-generic.md
    ├── meta-workflow.md
    ├── tdd-workflow.md
    └── ui-iteration-workflow.md
```

---

## 📊 Documentation Statistics

| Document | Lines | Focus |
|----------|-------|-------|
| skills/CLAUDE_SKILLS_ARCHITECTURE.md | ~690 | Skills & PDA patterns |
| agents/AGENTS_WORKFLOWS.md | ~600 | Agents & automation |
| guides/CLAUDE_CODE_COMPLETE_GUIDE.md | ~500 | Feature overview |
| guides/CLAUDE.md_PATTERNS.md | ~550 | CLAUDE.md patterns |
| guides/CONTEXT_MANAGEMENT.md | ~550 | Token optimization |
| RESEARCH_PLAN.md | ~400 | Research methodology |

**Total:** ~3,300 lines of comprehensive documentation

---

## 🔗 Related Resources

### Official Documentation
- [Claude Code Docs](https://code.claude.com/docs/en/overview)
- [Agent SDK Docs](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [MCP Protocol](https://modelcontextprotocol.io/)

### Community Resources
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code)
- [SkillsMP Marketplace](https://skillsmp.com/)
- [Plugin Repository](https://github.com/jovermier/claude-code-plugins-ip-labs)

### Key Articles
- [Claude Code 2.1 Review](https://medium.com/@joe.njenga/claude-code-2-1-is-here-i-tested-all-16-new-changes-dont-miss-this-update-ea9ca008dab7)
- [Best Practices for Agentic Coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Skills Deep Dive](https://medium.com/spillwave-solutions/claude-code-skills-deep-dive-part-1-82b572ad9450)

---

## 📝 Version History

### v1.3.0 (2026-01-15)

**Skill Lifecycle Management Suite**
- Added 4 new skills for complete skill development
- Added comprehensive documentation organized by feature
- Progressive Disclosure Architecture support
- Token optimization strategies

### v1.2.0 (2026-01-13)

**Multi-Language Support**
- Multi-language CLAUDE.md generation
- Context7 Skill Generator
- Language-specific sub-workflows

### v1.1.0 (2026-01-12)

**Agents & Workflows**
- 13 specialized agents
- 4 workflow commands
- P1/P2/P3 severity system
- File-based todo system

### v1.0.0 (2026-01-12)

**Initial Release**
- Core workflows and meta-workflow
- TDD, UI iteration, bug fix workflows
- Plan management skill

---

## ❓ FAQ

**Q: Which skill should I use first?**
A: Start with **@skill-architect** - it orchestrates the complete skill lifecycle.

**Q: How do I reduce token usage?**
A: Use **@skill-optimizer** to refactor skills with PDA, or read [guides/CONTEXT_MANAGEMENT.md](guides/CONTEXT_MANAGEMENT.md).

**Q: How do I review code quality?**
A: Use specific agents like **@security-sentinel** or **@performance-oracle**, or use `/workflows:review` for comprehensive review.

**Q: How do I create a CLAUDE.md?**
A: Use `/project:setup` command to generate CLAUDE.md for your project type.

---

*For complete changelog, see [../../CHANGELOG.md](../../CHANGELOG.md)*

*This documentation is maintained alongside Claude Code's rapid development. For the latest information, always refer to the official [Claude Code documentation](https://code.claude.com/docs/en/overview).*
