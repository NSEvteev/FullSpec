🌐 [English](README.md) | [Русский](README.ru.md)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo.svg">
    <img alt="FullSpec" src="assets/logo.svg" width="600">
  </picture>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://github.com/NSEvteev/FullSpec/actions/workflows/ci.yml"><img src="https://github.com/NSEvteev/FullSpec/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
</p>

A spec-driven development framework for [Claude Code](https://claude.ai/code). Structured process from requirements to production — specifications first, then code.

FullSpec organizes the development lifecycle into a chain of formal documents (Discussion → Design → Plan Tests → Plan Dev) where each step is validated before the next begins. The result: traceable decisions, consistent architecture, and automated delivery.

> Internal project files (instructions, standards, specs) are written in Russian. Claude Code understands Russian natively — fork, customize with your own Claude, and it works as-is.

---

## How It Works

```
/chain "Add user authentication with OAuth2"

Phase 1 — Analysis
  ✓ Discussion     — requirements and success criteria
  ✓ Design         — services, API contracts, data model
  ✓ Plan Tests     — acceptance scenarios (written before code)
  ✓ Plan Dev       — tasks with dependencies and execution blocks

Phase 2 — Docs Sync
  ✓ Per-service documentation and coding standards generated

Phase 3–4 — Implementation
  ✓ GitHub Issues + Milestone + Branch created
  ✓ Code written task by task, validated against specs

Phase 5–8 — Delivery
  ✓ Tests, lint, build → Code review → PR → Merge → Release
```

One command starts the process. Each phase has dedicated skills and agents. Decisions are traced from requirements through design to code.

---

## Quick Start

```bash
# 1. GitHub: "Use this template" → "Create a new repository"

# 2. Clone and setup
git clone https://github.com/{owner}/{repo}.git
cd {repo}
make setup

# 3. Configure Claude's language
#    Add to CLAUDE.md or tell Claude directly:
#    "Always respond in English"

# 4. Start building
/chain
```

> **Tip:** Internal instructions are in Russian, but Claude reads them and responds in any language. Add `Always respond in {your language}` to `CLAUDE.md` — Claude will communicate with you in your language while following Russian-written specs internally.

<details>
<summary><b>Requirements</b></summary>

| Tool | Purpose |
|------|---------|
| [Claude Code](https://claude.ai/code) | AI development assistant |
| Docker + Docker Compose | Service containerization |
| Python 3.8+ | Validation scripts, pre-commit hooks |
| Git + GitHub CLI (`gh`) | Version control, Issues, PRs |

Detailed setup: [initialization.md](.structure/initialization.md)

</details>

---

## What It Gives You

| Aspect | Without specs | With FullSpec |
|--------|--------------|---------------|
| Requirements | Scattered across chat history | Formal document with success criteria |
| Architecture | Decided ad-hoc during coding | Design doc with contracts and data models |
| Testing | Written after implementation | Test plan defined before code |
| Task planning | Vague, unordered | Tasks with dependencies and execution blocks |
| Coding standards | Inconsistent across team | Per-tech standards generated from Design |
| Documentation | Out of date | Living docs synced from specifications |
| Release | Manual, error-prone | Automated: validation → PR → release |

---

## What's Inside

| Component | Count | Purpose |
|-----------|-------|---------|
| Skills | 70 | Slash commands for every step: `/chain`, `/commit`, `/review`, `/release-create` |
| Agents | 23 | Parallel workers for analysis, code review, documentation sync |
| Validation scripts | 80+ | Pre-commit hooks and CI checks |
| Context rules | 16 | Auto-load relevant standards when editing specific file types |
| Per-tech standards | 9 | TypeScript, React, FastAPI, PostgreSQL, Protobuf, OpenAPI, AsyncAPI, Tailwind CSS |

---

## Project Structure

Every folder contains `.instructions/` — Claude reads them automatically and applies relevant standards.

```
src/           → Service source code (backend, database, tests)
shared/        → API contracts, events, shared libraries
platform/      → Docker, Gateway, Kubernetes, monitoring
config/        → Environment configs (dev / staging / prod)
tests/         → System tests (e2e, integration, load, smoke)
specs/         → Specifications and analysis chains
.claude/       → Skills, agents, context rules
.github/       → CI/CD workflows, issue templates, labels
.instructions/ → Standards for writing instructions
```

Full tree: [.structure/README.md](.structure/README.md)

---

## Commands

```bash
make setup      # Install pre-commit hooks (required after cloning)
make help       # List all available commands
make dev        # Start services (docker-compose)
make stop       # Stop services
make test       # Unit & integration tests
make test-e2e   # End-to-end tests
make lint       # Linting
make build      # Production build
make clean      # Full cleanup (docker down -v)
```

---

## Documentation

| Document | Contents |
|----------|----------|
| [Initialization](.structure/initialization.md) | Setup guide for Windows, macOS, Linux |
| [Project Structure](.structure/README.md) | Folder tree with descriptions |
| [Delivery Process](specs/.instructions/standard-process.md) | 8 phases, statuses, skills, agents |
| [CLAUDE.md](CLAUDE.md) | Entry point for Claude Code |
| [Glossary](specs/glossary.md) | Project terminology |

---

## Contact

Questions, feedback, collaboration: [n.s.evteev@ya.ru](mailto:n.s.evteev@ya.ru)

---

## License

[MIT](LICENSE)
