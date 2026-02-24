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

### SDD v2 миграция (оркестратор: `.claude/drafts/2026-02-19-sdd-orchestrator.md`)

Все фазы 0-10 выполнены. Очистка завершена.

### Сессия 2026-02-22 — выполнено

1. ✅ `.claude/drafts/2026-02-22-review-document-design.md` — все задачи #3-#16 выполнены: standard-review.md v1.1, validation-review.md, create-review.md, /review-create, /review (N+1 агентов), code-reviewer v2.0, validate-review.py, create-review-file.py, extract-svc-context.py, prerequisite check
2. ✅ `.claude/drafts/2026-02-22-process-map.md` — приведён к стандарту черновика (переименован, добавлены секции, обновлены пробелы)
3. `.claude/drafts/2026-02-20-post-push-review.md` — добавлена секция 6 (review-инфраструктура)

### Сессия 2026-02-24 — выполнено

1. ✅ `.claude/drafts/2026-02-22-holt-analysis-standard-review.md` — верифицировано: все 15 из 15 рекомендаций уже включены в standard-review.md v1.1
2. ✅ `specs/.instructions/analysis/review/` — рекомендации holt-анализа применены (P2 нумерация RV-N, пояснение § 5.2 и все остальные)
3. ✅ `.claude/drafts/2026-02-24-review-status-integration.md` — REVIEW как 8-й статус: 17 задач (standard/modify/validation/create/review), миграция 6 стандартов
4. ✅ `.claude/drafts/2026-02-24-dev-skill.md` — /dev + /analysis-status: 12 задач, миграция standard-development.md
5. ✅ Миграции всех 7 standard-*.md завершены (агенты параллельно), 0 расхождений
6. ✅ Группы B/C version drift исправлены (12 файлов: добавлен standard-version в frontmatter)
7. ✅ `.claude/drafts/2026-02-24-dev-restructure.md` — реструктуризация /dev → /dev-create + /dev, создание modify-development.md, интеграция validation-development.md в review
8. ✅ `.claude/drafts/2026-02-24-dev-scripts.md` — check-chain-readiness.py и dev-next-issue.py, интеграция в create/modify-development.md, регистрация в README

### Следующая сессия

1. `.claude/drafts/2026-02-20-post-push-review.md` — провести полный code review блоков 1-8 (приоритет: блок 1 ветвление → блок 5 code-reviewer → блок 8 dev-scripts)