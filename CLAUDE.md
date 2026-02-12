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

- [ ] Удалить шаблоны `question.yml` и `feature-request.yml` из `.github/ISSUE_TEMPLATE/` — в SDD эти точки входа покрыты specs/ (Discussion + Clarify). Обновить `standard-issue-template.md`, `create-issue.md`, `standard-issue.md`, labels.

## Ревью 2026-02-13: Service Lifecycle Fix

Незакоммиченные изменения из черновика [2026-02-12-service-lifecycle-fix.md](/.claude/drafts/2026-02-12-service-lifecycle-fix.md). Двухфазное создание services/{svc}.md, секция Changelog, stub/full детекция.

**Изменённые файлы (8):**
- [ ] [standard-frontmatter.md](/.structure/.instructions/standard-frontmatter.md) — новый § 5 (архитектурный frontmatter, stub/full)
- [ ] [standard-service.md](/specs/.instructions/living-docs/service/standard-service.md) — lifecycle, триггеры, § 5.8 Changelog, шаблоны
- [ ] [standard-specs.md](/specs/.instructions/standard-specs.md) — mermaid, Greenfield, ADR DONE, Changelog
- [ ] [standard-architecture.md](/specs/.instructions/living-docs/architecture/standard-architecture.md) — Changelog в шаблонах и чек-листах
- [ ] [search-docs.py](/.instructions/.scripts/search-docs.py) — новый `--type service`
- [ ] [service/README.md](/specs/.instructions/living-docs/service/README.md) — добавлены create/modify
- [ ] [.claude/skills/README.md](/.claude/skills/README.md) — service-create, service-modify
- [ ] [.claude/drafts/README.md](/.claude/drafts/README.md) — запись о черновике

**Новые файлы (7):**
- [ ] [create-service.md](/specs/.instructions/living-docs/service/create-service.md) — stub при Design WAITING
- [ ] [modify-service.md](/specs/.instructions/living-docs/service/modify-service.md) — 6 сценариев обновления (A-F)
- [ ] [validation-service.md](/specs/.instructions/living-docs/service/validation-service.md) — SVC014, stub-режим
- [ ] [validate-service.py](/specs/.instructions/.scripts/validate-service.py) — SVC001-SVC014, auto stub/full
- [ ] [service-create/SKILL.md](/.claude/skills/service-create/SKILL.md) — скилл создания
- [ ] [service-modify/SKILL.md](/.claude/skills/service-modify/SKILL.md) — скилл изменения
- [ ] [service-architecture.md](/.claude/rules/service-architecture.md) — rule для specs/architecture/services/

**После ревью:** удалить этот раздел, закоммитить.
