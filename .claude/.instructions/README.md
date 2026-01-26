# Инструкции для LLM

Индекс всех инструкций проекта. Единая точка входа.

## Структура

**Принцип:** Инструкции зеркалируют структуру проекта.

| Раздел | Папка проекта | Описание |
|--------|---------------|----------|
| [structure/](#structure--фундамент) | — | Фундамент: структура проекта и инструкций |
| [src/](#src--разработка-сервисов) | `/src/` | Разработка сервисов |
| [platform/](#platform--инфраструктура) | `/platform/` | Инфраструктура |
| [tests/](#tests--системные-тесты) | `/tests/` | Системные тесты |
| [shared/](#shared--общий-код) | `/shared/` | Общий код |
| [config/](#config--конфигурации) | `/config/` | Конфигурации |
| [specs/](#specs--спецификации) | `/specs/` | Спецификации |
| [github/](#github--github-платформа) | `/.github/` | GitHub платформа |
| [.claude/](#meta--правила-и-claude) | `/.claude/` | Правила (git, links...) + Claude-сущности |

**Маппинг:** Папка `/X/` → инструкции `X/`. Правила → `.claude/`.

---

## Дерево инструкций

**Принцип:** Строгое зеркалирование — каждая папка проекта = папка инструкций.

```
/.claude/.instructions/
├── README.md                    # Этот файл
│
├── structure/                   # Фундамент
│
├── src/                         # → /src/{service}/
│   ├── api/                     # → backend/v*/
│   ├── data/                    # → backend/ (форматы)
│   ├── database/                # → database/
│   │   └── migrations/          # → database/migrations/
│   ├── dev/                     #   Локальная разработка
│   ├── health/                  # → backend/health/
│   ├── resilience/              # → backend/ (устойчивость)
│   ├── security/                # → backend/ (безопасность)
│   ├── testing/                 # → tests/
│   │   ├── unit/                # → tests/unit/
│   │   └── integration/         # → tests/integration/
│   ├── frontend/                # → frontend/
│   └── docs/                    # → docs/
│
├── platform/                    # → /platform/
│   ├── docker/                  # → docker/
│   ├── gateway/                 # → gateway/
│   ├── monitoring/              # → monitoring/
│   │   ├── prometheus/          # → monitoring/prometheus/
│   │   ├── grafana/             # → monitoring/grafana/
│   │   └── loki/                # → monitoring/loki/
│   ├── k8s/                     # → k8s/
│   ├── scripts/                 # → scripts/
│   ├── docs/                    # → docs/
│   └── runbooks/                # → runbooks/
│
├── tests/                       # → /tests/
│   ├── e2e/                     # → e2e/
│   ├── integration/             # → integration/
│   ├── load/                    # → load/
│   ├── smoke/                   # → smoke/
│   └── fixtures/                # → fixtures/
│
├── shared/                      # → /shared/
│   ├── contracts/               # → contracts/
│   │   ├── openapi/             # → contracts/openapi/
│   │   └── protobuf/            # → contracts/protobuf/
│   ├── events/                  # → events/
│   ├── libs/                    # → libs/
│   ├── assets/                  # → assets/
│   ├── i18n/                    # → i18n/
│   └── docs/                    # → docs/
│
├── config/                      # → /config/
│   └── feature-flags/           # → feature-flags/
│
├── specs/                       # → /specs/
│   ├── discussions/             # → discussions/
│   ├── impact/                  # → impact/
│   └── services/                # → services/
│       ├── adr/                 # → {service}/adr/
│       └── plans/               # → {service}/plans/
│
├── github/                      # → /.github/
│   ├── workflows/               # → workflows/
│   └── issues/                  # → ISSUE_TEMPLATE/
│
└── .claude/                        # → /.claude/ + правила
    ├── git/                     #   Git правила
    ├── docs/                    #   Правила документации
    ├── instructions/            #   Правила инструкций
    ├── links/                   #   Правила ссылок
    ├── skills/                  #   Правила скиллов
    ├── agents/                  #   Правила агентов
    ├── scripts/                 #   Правила скриптов
    ├── state/                   #   Правила состояний
    ├── templates/               #   Правила шаблонов
    └── drafts/                  #   Правила черновиков
```

---

## .structure/ — Фундамент

Scope: **корневая информация** о структуре проекта.

| Файл | Описание |
|------|----------|
| [README.md](../.structure/README.md) | SSOT: структура папок проекта, зоны ответственности |

---

## src/ — Разработка сервисов

Scope: код и конфигурация сервисов в `/src/{service}/`.

### src/*.md — Управление сервисом

| Инструкция | Описание |
|------------|----------|
| [lifecycle.md](./src/lifecycle.md) | Создание, обновление, удаление сервиса |
| [structure.md](./src/structure.md) | Структура папок /src/{service}/ |
| [dependencies.md](./src/dependencies.md) | dependencies.yaml, граф зависимостей |

### src/api/ — Проектирование API

| Инструкция | Описание |
|------------|----------|
| [design.md](./src/api/design.md) | URL, методы, статусы, partial update |
| [versioning.md](./src/api/versioning.md) | Версионирование (/v1/, /v2/) |
| [deprecation.md](./src/api/deprecation.md) | Вывод API (Sunset header, сроки) |
| [swagger.md](./src/api/swagger.md) | OpenAPI, Swagger UI на /docs |
| [realtime.md](./src/api/realtime.md) | WebSocket, SSE, polling |

### src/data/ — Форматы данных

| Инструкция | Описание |
|------------|----------|
| [errors.md](./src/data/errors.md) | Формат ошибок (code, message, details) |
| [logging.md](./src/data/logging.md) | Формат логов (JSON, request_id) |
| [pagination.md](./src/data/pagination.md) | Пагинация (page, limit, total) |
| [validation.md](./src/data/validation.md) | Валидация входных данных |

### src/database/ — База данных

| Папка/Файл | Описание |
|------------|----------|
| [migrations/](./src/database/migrations/) | Правила миграций |
| database.md | Schema, transactions, pooling |

### src/dev/ — Локальная разработка

| Инструкция | Описание |
|------------|----------|
| [local.md](./src/dev/local.md) | Локальный запуск, hot reload, отладка |
| [performance.md](./src/dev/performance.md) | Профилирование, бенчмарки, лимиты |

### src/health/ — Health checks

| Инструкция | Описание |
|------------|----------|
| [health.md](./src/health/health.md) | /health, /ready, graceful shutdown |

### src/resilience/ — Устойчивость

| Инструкция | Описание |
|------------|----------|
| [resilience.md](./src/resilience/resilience.md) | Timeouts, retries, circuit breaker |

### src/security/ — Безопасность

| Инструкция | Описание |
|------------|----------|
| [auth.md](./src/security/auth.md) | JWT, аутентификация между сервисами |
| [audit.md](./src/security/audit.md) | Аудит-логи, PII, GDPR |

### src/testing/ — Тестирование сервиса

| Папка/Файл | Описание |
|------------|----------|
| [unit/](./src/testing/unit/) | Стандарты unit-тестов |
| [integration/](./src/testing/integration/) | Стандарты integration-тестов |
| testing.md | Общие правила тестирования |

### src/frontend/ — Клиентский код

> Папка создана, инструкции будут добавлены при необходимости.

### src/docs/ — Документация сервиса

> Папка создана, инструкции будут добавлены при необходимости.

---

## platform/ — Инфраструктура

Scope: инфраструктура проекта в `/platform/`.

### platform/*.md — Основные инструкции

| Папка | Описание |
|-------|----------|
| [docker/](./platform/docker/) | Dockerfile, docker-compose, multi-stage |
| [gateway/](./platform/gateway/) | API Gateway, Traefik, Nginx |
| [k8s/](./platform/k8s/) | Kubernetes манифесты |
| [scripts/](./platform/scripts/) | Инфраструктурные скрипты |
| [docs/](./platform/docs/) | Документация инфраструктуры |
| [runbooks/](./platform/runbooks/) | Runbooks операций |

**Файлы:** deployment.md, caching.md, operations.md, security.md

### platform/monitoring/ — Мониторинг

| Папка | Описание |
|-------|----------|
| [prometheus/](./platform/monitoring/prometheus/) | Сбор метрик |
| [grafana/](./platform/monitoring/grafana/) | Дашборды |
| [loki/](./platform/monitoring/loki/) | Сбор логов |

**Файлы:** overview.md, logging.md, metrics.md, tracing.md, alerting.md

---

## tests/ — Системные тесты

Scope: системные тесты проекта в `/tests/`.

| Папка | Описание |
|-------|----------|
| [e2e/](./tests/e2e/) | End-to-end сценарии |
| [integration/](./tests/integration/) | Интеграция между сервисами |
| [load/](./tests/load/) | Нагрузочные тесты (k6) |
| [smoke/](./tests/smoke/) | Быстрая проверка работоспособности |
| [fixtures/](./tests/fixtures/) | Тестовые данные, фабрики |

**Файлы:** formats.md, project-testing.md

---

## shared/ — Общий код

Scope: общий код проекта в `/shared/`.

| Папка | Описание |
|-------|----------|
| [contracts/](./shared/contracts/) | Контракты API |
| [contracts/openapi/](./shared/contracts/openapi/) | REST контракты (OpenAPI) |
| [contracts/protobuf/](./shared/contracts/protobuf/) | gRPC контракты (Protobuf) |
| [events/](./shared/events/) | Схемы событий |
| [libs/](./shared/libs/) | Общие библиотеки |
| [assets/](./shared/assets/) | Статические ресурсы |
| [i18n/](./shared/i18n/) | Локализация |
| [docs/](./shared/docs/) | Документация общего кода |

---

## config/ — Конфигурации

Scope: конфигурации окружений в `/config/`.

| Папка | Описание |
|-------|----------|
| [feature-flags/](./config/feature-flags/) | Feature flags, rollout |

**Файлы:** environments.md

---

## specs/ — Спецификации

Scope: спецификации проекта в `/specs/`.

| Папка | Описание |
|-------|----------|
| [discussions/](./specs/discussions/) | Формат дискуссий |
| [impact/](./specs/impact/) | Импакт-анализ |
| [services/](./specs/services/) | Шаблон для сервисов |
| [services/adr/](./specs/services/adr/) | ADR (архитектурные решения) |
| [services/plans/](./specs/services/plans/) | Планы реализации |

**Файлы:** architecture.md, glossary.md, statuses.md, workflow.md, rules.md, naming.md, indexes.md, relations.md, output.md, errors.md, examples.md

---

## github/ — GitHub платформа

Scope: GitHub-специфичные настройки в `/.github/`.

| Папка | Описание |
|-------|----------|
| [workflows/](./.github/workflows/) | CI/CD, GitHub Actions |
| [issues/](./.github/issues/) | Шаблоны и правила Issues |

### github/issues/ — GitHub Issues

| Инструкция | Описание |
|------------|----------|
| format.md | Формат заголовка, префиксы |
| labels.md | Система меток |
| workflow.md | Жизненный цикл Issue |
| commands.md | Команды gh CLI |
| errors.md | Обработка ошибок |
| examples.md | Примеры использования |

---

## .claude/ — Правила и Claude-сущности

Scope: правила (git, links...) и Claude-артефакты в `/.claude/`.

### .github/git/ — Git правила

| Инструкция | Описание |
|------------|----------|
| [commits.md](./.github/git/commits.md) | Conventional commits |
| [workflow.md](./.github/git/workflow.md) | GitHub Flow, ветки, PR |
| [review.md](./.github/git/review.md) | Code review, CODEOWNERS |
| [issues.md](./.github/git/issues.md) | Связь с GitHub Issues |

### .claude/docs/ — Правила документации

| Инструкция | Описание |
|------------|----------|
| [structure.md](./.claude/docs/structure.md) | Структура документации |
| [templates.md](./.claude/docs/templates.md) | Шаблоны документов |
| [workflow.md](./.claude/docs/workflow.md) | Процесс документирования |
| [rules.md](./.claude/docs/rules.md) | Правила оформления |
| [errors.md](./.claude/docs/errors.md) | Обработка ошибок |
| [examples.md](./.claude/docs/examples.md) | Примеры |

### .claude/.instructions/ — Правила инструкций

| Инструкция | Описание |
|------------|----------|
| [structure.md](./.claude/.instructions/structure.md) | Расположение и допустимые папки |
| [types.md](./.claude/.instructions/types.md) | Типы (standard/project) |
| [validation.md](./.claude/.instructions/validation.md) | Валидация формата |
| [statuses.md](./.claude/.instructions/statuses.md) | Система статусов |
| [workflow.md](./.claude/.instructions/workflow.md) | Жизненный цикл |
| [workflow-create.md](./.claude/.instructions/workflow-create.md) | CREATE workflow |
| [workflow-update.md](./.claude/.instructions/workflow-update.md) | UPDATE workflow |
| [workflow-deactivate.md](./.claude/.instructions/workflow-deactivate.md) | DEACTIVATE workflow |
| [patterns.md](./.claude/.instructions/patterns.md) | Паттерны поиска |
| [examples.md](./.claude/.instructions/examples.md) | Примеры |

### .structure/.instructions/ — Стандарты структуры

| Инструкция | Описание |
|------------|----------|
| [standard-links.md](/.structure/.instructions/standard-links.md) | Типы и форматы ссылок |
| [standard-readme.md](/.structure/.instructions/standard-readme.md) | Стандарт README |
| [workflow-modify.md](/.structure/.instructions/workflow-modify.md) | Изменение папок |

### .claude/skills/ — Правила скиллов

| Инструкция | Описание |
|------------|----------|
| [rules.md](./.claude/skills/rules.md) | Правило одного действия |
| [parameters.md](./.claude/skills/parameters.md) | Стандартные параметры |
| [workflow.md](./.claude/skills/workflow.md) | Шаблоны воркфлоу |
| [errors.md](./.claude/skills/errors.md) | Коды ошибок |
| [output.md](./.claude/skills/output.md) | Форматы вывода |
| [state.md](./.claude/skills/state.md) | Временные файлы |
| [integration.md](./.claude/skills/integration.md) | Интеграция скиллов |
| [validation.md](./.claude/skills/validation.md) | Валидация |
| [examples.md](./.claude/skills/examples.md) | Примеры |

### .claude/agents/, .claude/scripts/, .claude/state/, .claude/templates/, .claude/drafts/

> Папки созданы, инструкции будут добавлены при необходимости.

---

## Связанные ресурсы

- [CLAUDE.md](/CLAUDE.md) — точка входа для Claude
- [/.claude/skills/README.md](/.claude/skills/README.md) — индекс скиллов
- [/.claude/templates/README.md](/.claude/templates/README.md) — шаблоны
- [new_structure_of_project.md](/.claude/drafts/new_structure_of_project.md) — описание зеркальной структуры
