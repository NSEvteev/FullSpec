🌐 [English](README.md) | [Русский](README.ru.md)

# Project Template

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/NSEvteev/project_template/actions/workflows/ci.yml/badge.svg)](https://github.com/NSEvteev/project_template/actions/workflows/ci.yml)

**AI coding assistants are powerful — but without structure, every project reinvents the wheel.** Requirements live in chat history, decisions aren't documented, and "just build it" leads to rework.

Project Template adds a structured development process so that you and your AI **agree on what to build before writing code** — and then automate the entire journey from idea to production release.

> **Note:** Internal project files (instructions, standards, specs) are written in Russian. Claude Code understands Russian natively — fork, customize with your own Claude, and it just works.

---

## See It in Action

One command. Full lifecycle.

```
You: /chain
     "Add user authentication with OAuth2"

Claude creates a plan and guides you through:

  ✓ Discussion     — clarify requirements, define success criteria
  ✓ Design         — choose services, API contracts, data model
  ✓ Plan Tests     — write acceptance scenarios before code
  ✓ Plan Dev       — break into tasks with dependencies
  ✓ Docs Sync      — generate per-service docs and coding standards
  ✓ Dev Launch     — create GitHub Issues, Milestone, branch
  ✓ Implementation — write code task by task, with validation
  ✓ Review & PR    — automated code review and pull request
  ✓ Release        — GitHub Release with changelog

Every decision is traced. Every step is validated. Nothing falls through the cracks.
```

---

## Quick Start

```bash
# 1. GitHub: "Use this template" → "Create a new repository"

# 2. Clone and setup
git clone https://github.com/{owner}/{repo}.git
cd {repo}
make setup

# 3. Start building
/chain
```

<details>
<summary><b>Requirements</b></summary>

| Tool | Purpose |
|------|---------|
| [Claude Code](https://claude.ai/code) | AI-powered development assistant |
| Docker + Docker Compose | Service containerization |
| Python 3.8+ | Validation scripts, pre-commit |
| Git + GitHub CLI (`gh`) | Version control, Issues, PRs |

Detailed setup: [initialization.md](.structure/initialization.md)

</details>

---

## Why This Template?

### The problem

AI assistants generate code fast — but **what** code? Without a shared understanding of requirements, architecture, and success criteria, you get:
- Features nobody asked for
- Conflicting implementations across services
- No test coverage for edge cases
- "It works on my machine" releases

### How we solve it

| Without structure | With Project Template |
|---|---|
| Requirements live in chat history | Formal Discussion doc with success criteria |
| Architecture decisions are ad-hoc | Design doc with service contracts and data models |
| Tests are an afterthought | Test Plan written before code |
| Tasks are vague | Dev Plan with dependencies and blocks |
| Standards vary by developer | Per-tech coding standards auto-generated |
| Docs are always outdated | Living docs synced from specs |
| Release is manual and scary | Automated validation → PR → Release pipeline |

### What's inside

- **70 skills** — slash commands that automate every step (`/chain`, `/commit`, `/review`, `/release-create`)
- **23 agents** — parallel workers for analysis, code review, documentation sync
- **80+ validation scripts** — pre-commit hooks + CI ensure nothing breaks silently
- **16 context rules** — Claude automatically loads relevant standards when touching specific files
- **9 per-tech standards** — TypeScript, React, FastAPI, PostgreSQL, Protobuf, OpenAPI, AsyncAPI, Tailwind CSS

---

## The 8 Phases

```
Phase 1 — Analysis        Discussion → Design → Plan Tests → Plan Dev
Phase 2 — Docs Sync       Per-service docs, per-tech standards, overview
Phase 3 — Launch           GitHub Issues + Milestone + Branch
Phase 4 — Implementation   Code by tasks, with conflict detection
Phase 5 — Validation       Tests, lint, build, e2e → READY / NOT READY
Phase 6 — Delivery         Code review → PR → Merge
Phase 7 — Completion       Update living docs, close chain
Phase 8 — Release          GitHub Release + deploy
```

Each phase has dedicated skills and agents. Phases run in order, but within each phase parallel agents speed things up.

Full process: [standard-process.md](specs/.instructions/standard-process.md)

---

## Project Structure

Every folder contains `.instructions/` — Claude reads them automatically.

```
src/           → Service source code (backend, database, tests)
shared/        → API contracts, events, shared libraries
platform/      → Docker, Gateway, Kubernetes, monitoring
config/        → Environment configs (dev / staging / prod)
tests/         → System tests (e2e, integration, load, smoke)
specs/         → Specifications and analysis chains
.claude/       → Skills (70), agents (23), rules (16)
.github/       → CI/CD workflows, issue templates, labels
.instructions/ → Meta-instructions for writing instructions
```

Full tree: [.structure/README.md](.structure/README.md)

---

## Commands

```bash
make setup      # Install pre-commit hooks (required after cloning!)
make help       # Show all commands
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

| Document | What you'll find |
|----------|-----------------|
| [Initialization](.structure/initialization.md) | Setup guide for 3 platforms (Windows, macOS, Linux) |
| [Project Structure](.structure/README.md) | Full folder tree with descriptions |
| [Delivery Process](specs/.instructions/standard-process.md) | 8 phases, statuses, skills, agents |
| [CLAUDE.md](CLAUDE.md) | Entry point for Claude Code |
| [Glossary](specs/glossary.md) | Project terminology |

---

## License

[MIT](LICENSE) — use it, modify it, ship it.
