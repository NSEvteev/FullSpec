# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-03-24

### Added

**Hotfix process**
- `/hotfix` command — separate workflow for bugs, production incidents, and small fix bundles
- `standard-hotfix.md` — full standard with 7 phases: triage, diagnosis, impact analysis, parallel fix (code + docs), validation, delivery
- `create-hotfix.md` — orchestration workflow with TaskList generation
- `validation-hotfix.md` — 14-point validation checklist
- `hotfix-docs-agent` — parallel document updater (one agent per affected doc)
- `hotfix-docs-search-agent` — impact analysis scanner (one agent per scope: analysis/docs/technologies/system/pipelines)
- `hotfix.md` rule — auto-suggests `/hotfix` for bug-related requests

**Discussion improvements**
- PROP classification (Formal/Decision) in discussion, design, and plan-test creation workflows
- "Rejected proposals" section in `standard-discussion.md` with validation script (D024)

**Development improvements**
- Per-service fix agents pattern: one agent = one service, no exceptions
- Fix iteration cycle after review (algorithm, constraints, max 3 iterations)
- Stronger SSOT enforcement in Task 7 of chain workflow

### Changed
- `/chain` simplified to pure Happy Path (15 tasks) — bugs and hotfixes moved to `/hotfix`
- Removed `--hotfix` and `--bug-bundle` modes from `/chain`
- `core.md` rule extended with "Strict SSOT adherence" section and hotfix skill reference

## [1.0.0] - 2026-03-16

First public release. 498 commits of building a complete AI-powered development template.

### Added

**Core process (8 phases)**
- `/chain` command — full lifecycle orchestration from idea to production
- Analysis chain: Discussion → Design → Plan Tests → Plan Dev (DRAFT → WAITING status flow)
- Docs Sync: parallel agents for per-service docs, per-tech standards, system overview
- Dev launch: `/dev-create` — Issues + Milestone + Branch automation
- Implementation: `dev-agent` with TASK-N blocks, waves, CONFLICT detection
- Final validation: `/test` — sync main, docker, tests/lint/build/e2e
- Delivery: `/review` → `/pr-create` → `/merge` pipeline
- Completion: `/chain-done` — DONE cascade, docs update
- Release: `/release-create` + `/post-release` validation

**Skills (70)**
- Analysis: discussion, design, plan-test, plan-dev (create/modify/validate each)
- GitHub: issue, milestone, labels, branch (create/modify/validate)
- Development: commit, pr-create, merge, review, review-create
- Documentation: instruction, service, technology, docs-sync (create/modify/validate)
- Infrastructure: docker-up, test, test-ui, init-project
- Meta: skill, agent, rule, script, structure (create/modify/validate)
- Utilities: chain, chain-done, rollback-chain, list-search, links-validate, release-create, post-release, analysis-status, draft-validate, migration-create, migration-validate, principles-validate

**Agents (23)**
- Analysis: design-agent-first, design-agent-second, plantest-agent, plandev-agent
- Review: code-reviewer, design-reviewer, discussion-reviewer, plantest-reviewer, plandev-reviewer, meta-reviewer
- Documentation: service-agent, service-reviewer, technology-agent, technology-reviewer, system-agent, system-reviewer
- Development: dev-agent, docker-agent, issue-agent, issue-reviewer
- Utilities: meta-agent, rollback-agent, test-ui-agent

**Per-tech coding standards (9)**
- TypeScript (+ security), React, Tailwind CSS, FastAPI, PostgreSQL, Protobuf, OpenAPI, AsyncAPI

**CI/CD**
- 3 GitHub Actions workflows: CI, Deploy, Pre-release
- Pre-commit hooks: README structure, rules, scripts, skills, branch name validation
- 80+ Python validation scripts

**Project infrastructure**
- Microservice folder structure: src/, shared/, platform/, config/, tests/
- `.instructions/` in every folder with standards and validation
- 16 context rules for automatic Claude Code guidance
- Labels system with sync script
- Issue/PR templates
- CODEOWNERS, SECURITY.md, dependabot.yml
- Makefile with 20+ commands
- Backport/forward-port workflow for template improvements

**Documentation**
- CLAUDE.md — entry point for Claude Code
- Initialization guide (12 sections, 3 OS platforms)
- Structure SSOT with full tree diagram
- Quick Start for LLM
- Glossary
- Onboarding guide

### Changed
- License: proprietary → MIT

[1.1.0]: https://github.com/NSEvteev/FullSpec/releases/tag/v1.1.0
[1.0.0]: https://github.com/NSEvteev/FullSpec/releases/tag/v1.0.0
