# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

**Структура:** [.structure/README.md](/.structure/README.md) — SSOT структуры проекта

**Quick Start:** [quick-start.md](/.structure/quick-start.md)

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
make test-load  # Нагрузочные тесты
make test-smoke # Smoke тесты (post-deploy)
make lint       # Линтинг
make build     # Сборка для production
make clean     # Очистка (docker down -v)
```

> **Первый шаг:** После клонирования выполни `make setup`. Подробнее: [initialization.md](/.structure/initialization.md)

## Инициализация

**Новый проект?** Выполни `/init-project` — полная настройка GitHub, docs/, среда, customization.

| Команда | Когда |
|---------|-------|
| `make setup` | Минимум — pre-commit хуки |
| `make init` | Автоматизация — setup + labels + verify |
| `/init-project` | Полная настройка с Claude (интерактивно) |
| `/init-project --check` | Healthcheck — проверка без изменений |

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

## Разработка

**Любое изменение системы начинается с:** `/chain`

**SSOT:** [standard-process.md](/specs/.instructions/standard-process.md) — полный стандарт процесса поставки ценности.

`/chain` создаёт TaskList с полной последовательностью от идеи до релиза. Каждая задача — конкретный скилл в правильном порядке. Прогресс виден в TaskList.

| Команда | Когда |
|---------|-------|
| `/chain` | Новая фича, изменение поведения, баг |
| `/chain --hotfix` | Критический баг в production |
| `/chain --doc-only` | Опечатки, форматирование (без chain) |
| `/chain --resume` | Продолжить после прерывания |

### 7 фаз процесса

| Фаза | Что происходит | Ключевые скиллы/агенты |
|------|---------------|----------------------|
| 1. Analysis chain | Discussion → Design → Plan Tests → Plan Dev (каждый: DRAFT → WAITING) | `/discussion-create`, `/design-create`, `/plan-test-create`, `/plan-dev-create` |
| 2. Docs Sync | Параллельные агенты: per-service docs, per-tech стандарты, overview.md | `/docs-sync` (service/technology/system-agent + reviewers) |
| 3. Запуск | Issues + Milestone + Branch → вся цепочка RUNNING | `/dev-create` |
| 4. Реализация | Код по TASK-N (блоки, волны, CONFLICT-детекция) + коммиты | dev-agent, `/commit` |
| 5. Доставка в main | Branch Review → PR → PR Review → Merge → Sync | `/review`, `/pr-create`, `/merge` |
| 6. Завершение | RUNNING → REVIEW → DONE (docs/ AS IS, system-agent mode=done) | code-reviewer, `/chain-done` |
| 7. Поставка | Pre-release → Release → Deploy | `/release-create`, `/post-release` |

**Путь B (CONFLICT):** обратная связь код → спеки. Каскад → разрешение → повторный запуск.
**Путь C:** Rollback (rollback-agent), Hotfix, Bug-fix bundle, Doc-only.

## Задачи на 2026-02-27

~~**Драфт docs-sync-after-dev**~~ — реализован (`c449939`). 13 задач, 4 агента, 2 скилла, 27 файлов. [Архив](/.claude/drafts/examples/2026-02-27-docs-sync-after-dev.md)

## Паттерны

- Unit-тесты внутри сервиса: `/src/{service}/tests/`
- Системные тесты между сервисами: `/tests/`
- Секреты НИКОГДА не коммитятся — только `.env.example`
