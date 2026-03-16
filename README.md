🌐 [English](README.md) | [Русский](README.ru.md)

# Project Template

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/NSEvteev/project_template/actions/workflows/ci.yml/badge.svg)](https://github.com/NSEvteev/project_template/actions/workflows/ci.yml)

A fullstack microservice project template with an AI-powered development process via [Claude Code](https://claude.ai/code).

The full cycle from idea to release — discussion, design, test planning, development planning, implementation, review, deploy — is automated through **70 skills**, **23 agents**, and **80+ validation scripts**.

> **Note:** Internal project documentation (instructions, standards, specs) is written in Russian. Claude Code understands Russian natively — just fork, customize, and let your Claude handle the rest.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Development Process](#development-process)
- [Commands](#commands)
- [Documentation](#documentation)
- [License](#license)

---

## Features

**Value delivery process** — 8 phases from idea to production, each automated by Claude Code skills. A single `/chain` command creates a full plan and guides you through every step.

**Analysis chain** — a formal document chain (Discussion → Design → Plan Tests → Plan Dev) with requirements traceability, status system, and cascading conflict detection.

**Instructions in every folder** — `.instructions/` with rules, standards, and validation scripts. Claude Code automatically picks up context via rules.

**Per-tech coding standards** — standards for TypeScript, React, FastAPI, PostgreSQL, Protobuf, and other technologies are generated from Design and bound to specific services.

**Pre-commit hooks** — README structure, rules, scripts, and skills validation on every commit. CI mirrors these checks on GitHub Actions.

**GitHub integration** — skills for Issues, Milestones, Labels, PRs, Releases. Standardized templates and labels.

---

## Quick Start

### New project from template

```bash
# 1. GitHub: "Use this template" → "Create a new repository"
# 2. Clone
git clone https://github.com/{owner}/{repo}.git
cd {repo}

# 3. Install hooks
make setup

# 4. Full setup via Claude Code
/init-project
```

Detailed guide: [initialization.md](.structure/initialization.md)

### Existing project

```bash
git clone https://github.com/NSEvteev/project_template.git
cd project_template

# Install pre-commit hooks (required!)
make setup

# Start services
make dev

# Stop services
make stop
```

### Requirements

| Tool | Purpose |
|------|---------|
| Docker + Docker Compose | Service containerization |
| Python 3.8+ | Validation scripts, pre-commit |
| Git | Version control |
| GitHub CLI (`gh`) | Issues, PRs, Releases |

---

## Project Structure

**Structure SSOT:** [.structure/README.md](.structure/README.md)

| Folder | Purpose |
|--------|---------|
| `src/` | Service source code |
| `shared/` | API contracts, events, shared libraries |
| `platform/` | Docker, Gateway, Kubernetes, monitoring |
| `config/` | Environment configs (dev/staging/prod) |
| `tests/` | System tests (e2e, integration, load) |
| `specs/` | Specifications, analysis chains, glossary |
| `.claude/` | Skills, rules, agents for Claude Code |
| `.github/` | Issue templates, CI/CD workflows |
| `.instructions/` | Meta-instructions — standards for writing instructions |
| `.structure/` | Structure SSOT, initialization |

Each folder contains `.instructions/` with working rules:

```
src/
├── .instructions/          # Service development standards
│   ├── standard-*.md       # Standards
│   └── README.md           # Index
├── {service}/              # Services
└── README.md
```

---

## Development Process

Any system change starts with `/chain`. A single command creates a TaskList with the full sequence from idea to release.

```
Phase 1 — Analysis (DRAFT → WAITING):
  1. Discussion        — why? requirements, success criteria
  2. Design            — how? services, API, data model, technologies
  3. Plan Tests        — how to verify? acceptance scenarios
  4. Plan Dev          — what tasks? TASK-N, blocks, dependencies

Phase 2 — Docs Sync:
  5. /docs-sync        — parallel agents: per-service docs,
                         per-tech standards, overview.md

Phase 3 — Launch:
  6. /dev-create       — Issues + Milestone + Branch → RUNNING

Phase 4 — Implementation:
  7. dev-agent         — code + tests + commits (by TASK-N)

Phase 5 — Final Validation:
  8. /test             — sync main, tests, lint, build → READY/NOT READY

Phase 6 — Delivery:
  9. /review           — branch review
 10. /pr-create        — Pull Request
 11. /merge            — Squash merge + sync main

Phase 7 — Completion:
 12. /chain-done       — DONE + update docs/

Phase 8 — Release:
 13. /release-create   — GitHub Release
```

Details: [standard-process.md](specs/.instructions/standard-process.md)

---

## Commands

```bash
make setup      # Install pre-commit hooks (required after cloning!)
make help       # Show all commands
make dev        # Start for development (docker-compose)
make stop       # Stop services
make test       # Unit/integration tests
make test-e2e   # E2E tests
make lint       # Linting
make build      # Build for production
make clean      # Cleanup (docker down -v)
```

---

## Documentation

| Document | Purpose |
|----------|---------|
| [CLAUDE.md](CLAUDE.md) | Entry point for Claude Code |
| [Initialization](.structure/initialization.md) | Setup, GitHub config, template workflow |
| [Project Structure](.structure/README.md) | Structure SSOT — folder tree, descriptions |
| [Quick Start](.structure/quick-start.md) | Quick Start for LLM |
| [Delivery Process](specs/.instructions/standard-process.md) | Full standard — 8 phases, statuses, skills |
| [Glossary](specs/glossary.md) | Project terms |
| [Pre-commit Hooks](.structure/pre-commit.md) | Setup and troubleshooting |

---

## License

This project is licensed under the [MIT License](LICENSE).
