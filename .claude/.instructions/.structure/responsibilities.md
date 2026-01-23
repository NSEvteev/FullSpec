# Зоны ответственности

---

## Формат

> **IN** — что входит | **OUT** — что НЕ входит (→ куда)

---

## 1. Инструкции

### .structure/ — Правила организации структуры

**SSOT:** `/.structure/` — фактическая структура (project.md, mapping.md, instructions.md)

| Файл | IN | OUT |
|------|-----|-----|
| `lifecycle.md` | Этапы, покрытие инструкциями | Детали этапов |
| `responsibilities.md` | IN/OUT для инструкций и папок | Правила реализации |
| `examples.md` | "Куда положить", "Где написать" | Шаблоны файлов |

### src/ — Разработка сервисов

| Папка | IN | OUT |
|-------|-----|-----|
| `src/` | lifecycle, structure, dependencies | Общие библиотеки → shared/ |
| `src/api/` | design, versioning, deprecation, realtime | Контракты → shared/contracts |
| `src/data/` | errors, logging, validation, pagination | Схемы событий → shared/ |
| `src/database/` | schema, migrations, transactions, pooling | Общие миграции → platform/ |
| `src/dev/` | local setup, hot reload, performance | CI/CD → .github/ |
| `src/health/` | /health, /ready, graceful shutdown | Alerting → platform/observability/ |
| `src/resilience/` | timeouts, retries, circuit breaker | Инфра-отказоустойчивость → platform/ |
| `src/security/` | auth, authorization, audit | Секреты, vault → platform/ |
| `src/testing/` | unit, integration внутри сервиса | E2E, load → tests/ |
| `src/frontend/` | UI, state, routing | Общие assets → shared/ |
| `src/docs/` | API docs, guides, runbooks | Архитектура → specs/ |

### platform/ — Инфраструктура

| Папка | IN | OUT |
|-------|-----|-----|
| `platform/` | docker, deployment, operations | Код сервисов → src/ |
| `platform/observability/` | logging, metrics, tracing, alerting | Логирование в коде → src/data/ |
| `platform/docs/` | docs, runbooks операций | Документация сервисов → src/docs/ |

### tests/ — Системные тесты

| Папка | IN | OUT |
|-------|-----|-----|
| `tests/` | e2e, load, smoke, integration между сервисами | Unit тесты → src/testing/ |

### shared/ — Общий код

| Папка | IN | OUT |
|-------|-----|-----|
| `shared/` | contracts, events, libs, assets, i18n | Код сервиса → src/ |
| `shared/docs/` | документация контрактов, событий, библиотек | Документация сервисов → src/docs/ |

### config/ — Конфигурации

| Папка | IN | OUT |
|-------|-----|-----|
| `config/` | environments, feature-flags | .env сервиса → /src/{service}/ |

### specs/ — Спецификации

| Папка | IN | OUT |
|-------|-----|-----|
| `specs/` | discussions, impact, adr, plans, architecture | Документация кода → */docs/ |

### .github/ — GitHub платформа

| Папка | IN | OUT |
|-------|-----|-----|
| `.github/` | actions, workflows, templates, CODEOWNERS | Git правила → .claude/git/ |
| `.github/issues/` | format, labels, workflow, commands | Спецификации → specs/ |

### .claude/ — Правила и Claude-сущности

| Папка | IN | OUT |
|-------|-----|-----|
| `.claude/git/` | commits, branches, review, merge | GitHub Actions → .github/ |
| `.claude/.instructions/` | types, validation, workflow, relations | Содержимое инструкций |
| `.claude/links/` | format, patterns, validation | Конкретные ссылки в файлах |
| `.claude/skills/` | rules, parameters, errors, state | Код скиллов → /.claude/skills/ |
| `.claude/agents/` | structure, prompts, tools | Код агентов → /.claude/agents/ |
| `.claude/scripts/` | naming, structure, hooks | Код скриптов → /.claude/scripts/ |
| `.claude/state/` | format, lifecycle, cleanup | Файлы состояний |
| `.claude/drafts/` | naming, lifecycle, cleanup | Файлы черновиков |

---

## 2. Папки проекта

### Корневые файлы

| Файл | IN | OUT |
|------|-----|-----|
| `README.md` | Описание проекта, quick start, ссылки | Детальная документация → */docs/ |
| `CLAUDE.md` | Ссылки на инструкции, статус проекта, правила | Содержимое инструкций → /.claude/.instructions/ |
| `Makefile` | make help, dev, test, lint, build | Скрипты деплоя → /platform/scripts/ |
| `.gitignore` | Паттерны игнорирования | — |

### /src/ — Исходный код сервисов

| Папка | IN | OUT |
|-------|-----|-----|
| `/src/` | Папки сервисов | Общий код → /shared/ |
| `/src/{service}/` | README, Makefile, .env.example, dependencies | Спецификации → /specs/ |
| `/src/{service}/docs/` | API docs, guides, runbooks сервиса | Архитектура → /specs/ |
| `/src/{service}/backend/` | handlers, routes, services, models | Миграции БД → database/ |
| `/src/{service}/backend/v*/` | Версионированные handlers, routes | Общий код между версиями → shared/ |
| `/src/{service}/backend/shared/` | models, utils между версиями API | Общие библиотеки системы → /shared/libs/ |
| `/src/{service}/backend/health/` | /health, /ready handlers | Бизнес-логика |
| `/src/{service}/database/` | schema.sql, migrations/ | Общие схемы → /shared/contracts/ |
| `/src/{service}/frontend/` | UI компоненты, pages, state | Общие assets → /shared/assets/ |
| `/src/{service}/tests/` | unit/, integration/ | E2E тесты → /tests/ |

### /platform/ — Общая инфраструктура

| Папка | IN | OUT |
|-------|-----|-----|
| `/platform/` | docker, gateway, monitoring, k8s, scripts | Код сервисов → /src/ |
| `/platform/docker/` | docker-compose.yml, Dockerfile.* | Конфиги сервиса → /src/{service}/ |
| `/platform/gateway/` | Traefik/Nginx конфиги, routing rules | Бизнес-логика |
| `/platform/monitoring/` | prometheus/, grafana/, loki/ | Код логирования → /src/ |
| `/platform/monitoring/prometheus/` | prometheus.yml, alerts.yml, rules/ | Дашборды → grafana/ |
| `/platform/monitoring/grafana/` | dashboards/*.json, provisioning/ | Алерты → prometheus/ |
| `/platform/monitoring/loki/` | loki-config.yml, promtail.yml | Код логирования → /src/ |
| `/platform/k8s/` | deployments, services, ingress, secrets | Docker compose → docker/ |
| `/platform/scripts/` | deploy.sh, backup.sh, restore.sh | Скрипты Claude → /.claude/scripts/ |
| `/platform/docs/` | Документация /platform/ | Код → /platform/ |
| `/platform/runbooks/` | deploy.md, rollback.md, database-full.md | Доки сервисов → /src/{service}/docs/ |

### /tests/ — Системные тесты

| Папка | IN | OUT |
|-------|-----|-----|
| `/tests/` | e2e, integration, load, smoke, fixtures | Unit тесты → /src/{service}/tests/ |
| `/tests/e2e/` | User flows, сценарии через UI/API | Unit тесты |
| `/tests/integration/` | Тесты между сервисами | Тесты внутри сервиса → /src/ |
| `/tests/load/` | k6 скрипты, сценарии нагрузки | Функциональные тесты |
| `/tests/smoke/` | Health checks, базовая работоспособность | Детальные тесты |
| `/tests/fixtures/` | users.json, products.json | Моки сервиса → /src/{service}/tests/ |

### /shared/ — Общий код между сервисами

| Папка | IN | OUT |
|-------|-----|-----|
| `/shared/` | contracts, events, libs, assets, i18n | Код сервисов → /src/ |
| `/shared/contracts/` | openapi/*.yaml, protobuf/*.proto | Код handlers → /src/ |
| `/shared/contracts/openapi/` | auth.yaml, users.yaml | gRPC → protobuf/ |
| `/shared/contracts/protobuf/` | auth.proto, users.proto | REST → openapi/ |
| `/shared/events/` | user.created.json, order.placed.json | Код publishers → /src/ |
| `/shared/libs/` | errors, logging, validation, http-client | Бизнес-логика → /src/ |
| `/shared/assets/` | icons, fonts, images | UI компоненты → /src/{service}/frontend/ |
| `/shared/i18n/` | en.json, ru.json | Тексты в коде → /src/ |
| `/shared/docs/` | Документация /shared/ | Код → /shared/ |

### /config/ — Конфигурации окружений

| Папка | IN | OUT |
|-------|-----|-----|
| `/config/` | environments, feature-flags | .env сервисов → /src/{service}/ |
| `/config/*.yaml` | development.yaml, staging.yaml, production.yaml | Секреты → vault/env vars |
| `/config/feature-flags/` | flags.yaml, rollout rules | Бизнес-логика |

### /specs/ — Спецификации проекта

| Папка | IN | OUT |
|-------|-----|-----|
| `/specs/` | discussions, impact, services, glossary | Документация кода → */docs/ |
| `/specs/discussions/` | Обсуждения фич, идеи, proposals | Решения → adr/ |
| `/specs/impact/` | Анализ влияния изменений | Планы реализации → plans/ |
| `/specs/services/` | Папки по сервисам | Код → /src/ |
| `/specs/services/{service}/` | README, architecture.md | Код сервиса → /src/{service}/ |
| `/specs/services/{service}/adr/` | Архитектурные решения | Дискуссии → /specs/discussions/ |
| `/specs/services/{service}/plans/` | Roadmap, feature plans | Issues → GitHub |
| `/specs/glossary.md` | Термины проекта | Документация API → */docs/ |

### /.github/ — GitHub платформа

| Папка | IN | OUT |
|-------|-----|-----|
| `/.github/` | workflows, templates, CODEOWNERS | Код → /src/ |
| `/.github/workflows/` | ci.yml, deploy.yml, release.yml | Скрипты деплоя → /platform/scripts/ |
| `/.github/ISSUE_TEMPLATE/` | bug.md, feature.md, task.md | Спецификации → /specs/ |
| `/.github/PULL_REQUEST_TEMPLATE.md` | Чек-лист для PR | Review правила → инструкции |
| `/.github/CODEOWNERS` | Mapping путей → reviewers | Процессы → инструкции |

### /.claude/ — Инструменты Claude

| Папка | IN | OUT |
|-------|-----|-----|
| `/.claude/` | instructions, skills, agents, templates, scripts, state, drafts, settings | Код проекта → /src/ |
| `/.claude/.instructions/` | Правила для LLM (зеркальная структура) | Документация → */docs/ |
| `/.claude/skills/` | SKILL.md для каждого скилла | Инструкции → instructions/ |
| `/.claude/agents/` | Определения агентов: prompts, tools | Скиллы → skills/ |
| `/.claude/templates/` | Шаблоны для создания артефактов | Готовые файлы |
| `/.claude/scripts/` | Python скрипты автоматизации, hooks | Инфра-скрипты → /platform/scripts/ |
| `/.claude/state/` | JSON файлы состояний агентов (не в git) | Конфигурации → /config/ |
| `/.claude/drafts/` | Планы, заметки, SSOT-документы (в git) | Спецификации → /specs/ |
| `/.claude/settings.json` | Конфигурация Claude Code (в git) | Секреты → env vars |
| `/.claude/settings.local.json` | Персональные настройки (не в git) | Общие настройки → settings.json |
