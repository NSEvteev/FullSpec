# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

**Структура:** [.structure/README.md](/.structure/README.md) — SSOT структуры проекта

**Quick Start:** [quick-start.md](/.structure/quick-start.md) | [SSOT](/.structure/ssot.md) | [Артефакты](/.structure/artifacts.md)

**Onboarding:** [onboarding.md](/.claude/onboarding.md)

**Правила:** контекст загружается автоматически из `/.claude/rules/` при работе с файлами.

**AskUserQuestion:** При предложении вариантов выбора использовать `AskUserQuestion` tool.

## Команды

```bash
make setup     # Установить pre-commit хуки (ОБЯЗАТЕЛЬНО после клонирования!)
make help      # Показать все команды
make dev       # Запустить для разработки (docker-compose)
make stop      # Остановить сервисы
make test      # Unit/integration тесты
make test-e2e  # E2E тесты
make lint      # Линтинг
make build     # Сборка для production
make clean     # Очистка (docker down -v)
```

> **Первый шаг:** После клонирования выполни `make setup`. Подробнее: [initialization.md](/.structure/initialization.md)

## Архитектура

Микросервисный fullstack проект с разделением:

| Папка | Назначение |
|-------|------------|
| `/src/{service}/` | Код сервиса (backend/, database/, tests/) |
| `/shared/` | Контракты API, события, общие библиотеки |
| `/platform/` | Docker, Gateway, Kubernetes, мониторинг |
| `/config/` | Конфигурации окружений (dev/staging/prod) |
| `/tests/` | Системные тесты (e2e, integration, load) |
| `/.claude/` | Скиллы, rules, агенты, инструкции |

## Паттерны

- Unit-тесты внутри сервиса: `/src/{service}/tests/`
- Системные тесты между сервисами: `/tests/`
- Секреты НИКОГДА не коммитятся — только `.env.example`

## Задачи

### Черновики — порядок реализации (15 файлов, 13 активных)

Порядок определён графом зависимостей: docker-dev блокирует 3 черновика.
После каждого артефакта — обновить SSOT-ссылки в `standard-process.md` §8/§10.

**Выполнено:**
- [x] **rename-agents-meta** — `.claude/drafts/2026-02-25-rename-agents-meta.md` (7 задач)

**Поглощены / отклонены:**
- ~~sync-skill (G7)~~ → merge-skill
- ~~feature-freeze~~ → отклонён
- ~~smoke-tests~~ → deploy-workflow
- ~~cicd-enhancements~~ → tests-and-platform
- ~~post-release-validation~~ → deploy-workflow
- ~~post-release (G8)~~ → deploy-workflow

**Порядок реализации (последовательный):**

| # | Черновик | Файл | Задач | Блокирован | Блокирует |
|---|---------|------|-------|-----------|-----------|
| 1 | **commit-skill (G5)** | `.claude/drafts/2026-02-24-commit-skill.md` | 10 | — | — |
| 2 | **merge-skill (G6+G7)** | `.claude/drafts/2026-02-24-merge-skill.md` | 6 | — | — |
| 3 | **pr-create (G2)** | `.claude/drafts/2026-02-24-pr-create.md` | 8 | — | — |
| 4 | **rollback-skill (G9)** | `.claude/drafts/2026-02-24-rollback-skill.md` | 5 | — | — |
| 5 | **chain-done (G11)** | `.claude/drafts/2026-02-24-chain-done.md` | 5 | — | — |
| 6 | **docker-dev** | `.claude/drafts/2026-02-24-docker-dev.md` | 8 | — | #7, #10, #12 |
| 7 | **tests-and-platform** | `.claude/drafts/2026-02-24-tests-and-platform.md` | 8 | #6 (частично: задачи 4,8) | #10 |
| 8 | **shared-contracts** | `.claude/drafts/2026-02-24-shared-contracts.md` | 9 | — | — |
| 9 | **user-process-guide** | `.claude/drafts/2026-02-24-user-process-guide.md` | 10 | — | — |
| 10 | **conflict-detect (G10)** | `.claude/drafts/2026-02-24-conflict-detect.md` | 16 | #6, #7 | — |
| 11 | **security-scan** | `.claude/drafts/2026-02-25-security-scan.md` | 12 | — | — |
| 12 | **deploy-workflow** | `.claude/drafts/2026-02-25-deploy-workflow.md` | 12 | #6 | — |
| 13 | **init-project (G1)** | `.claude/drafts/2026-02-24-init-project.md` | 15 | все предыдущие (концептуально) | — |
| 14 | **release-create (G3)** | `.claude/drafts/2026-02-24-release-create.md` | 6 | — | — |

**Итого:** 130 задач в 14 черновиках.

**Граф зависимостей:**
- #1–#4 — независимые, можно в любом порядке
- #5 docker-dev — критический путь, блокирует #6 (частично), #9 (полностью), #11 (Dockerfile)
- #6 tests-and-platform — задачи 6,7 независимы; задачи 4,8 ждут docker-dev
- #7, #8 — независимые, параллельны с #5–#6
- #9 conflict-detect — самый сложный (16 задач), ждёт #5 + #6
- #10 security-scan — независим, но логически после infra (#5–#8)
- #11 deploy-workflow — ждёт docker-dev (Dockerfile формат)
- #12 init-project — финальный оркестратор, обновляет initialization.md
- #13 release-create — независим, но логически последний
