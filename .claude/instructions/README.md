# Инструкции для LLM

Индекс всех инструкций проекта. Единая точка входа.

## Структура

Инструкции организованы по **4 scope**:

| Раздел | Scope | Описание | Папка проекта |
|--------|-------|----------|---------------|
| [service/](#service--разработка-сервиса) | Один сервис | Разработка внутри `/src/{service}/` | `/src/{service}/` |
| [system/](#system--система) | Вся система | Инфраструктура, тесты, конфиги | `/platform/`, `/tests/`, `/shared/`, `/config/` |
| [workflow/](#workflow--процессы) | Процессы | Git, GitHub, спецификации, документация | `/specs/`, `/doc/`, `/.github/` |
| [meta/](#meta--claude-сущности) | Claude | Правила для инструкций, скиллов, агентов | `/.claude/` |

---

## Дерево инструкций

```
/.claude/instructions/
├── README.md                    # Этот файл
│
├── service/                     # Разработка внутри сервиса
│   ├── *.md                     #   lifecycle, structure, dependencies
│   ├── api/                     #   Проектирование API
│   ├── data/                    #   Форматы данных
│   ├── database/                #   База данных
│   ├── dev/                     #   Локальная разработка
│   ├── health/                  #   Health checks
│   ├── resilience/              #   Устойчивость
│   ├── security/                #   Безопасность
│   ├── testing/                 #   Unit/integration тесты
│   └── frontend/                #   Клиентский код (опционально)
│
├── system/                      # Общее для всей системы
│   ├── platform/                #   Инфраструктура
│   │   └── observability/       #     Наблюдаемость
│   ├── tests/                   #   Системные тесты
│   ├── shared/                  #   Общий код
│   └── config/                  #   Конфигурации
│
├── workflow/                    # Процессы и документация
│   ├── git/                     #   Git процессы
│   ├── github/                  #   GitHub платформа
│   │   └── issues/              #     GitHub Issues
│   ├── specs/                   #   Спецификации
│   └── docs/                    #   Документация
│
└── meta/                        # Правила для Claude-сущностей
    ├── instructions/            #   Правила инструкций
    ├── links/                   #   Правила ссылок
    ├── skills/                  #   Правила скиллов
    ├── agents/                  #   Правила агентов
    ├── scripts/                 #   Правила скриптов
    ├── state/                   #   Правила состояний
    └── templates/               #   Правила шаблонов
```

---

## service/ — Разработка сервиса

Scope: код и конфигурация **одного** сервиса в `/src/{service}/`.

### service/*.md — Управление сервисом

| Инструкция | Описание |
|------------|----------|
| [lifecycle.md](./service/lifecycle.md) | Создание, обновление, удаление сервиса |
| [structure.md](./service/structure.md) | Структура папок /src/{service}/ |
| [dependencies.md](./service/dependencies.md) | dependencies.yaml, граф зависимостей |

### service/api/ — Проектирование API

| Инструкция | Описание |
|------------|----------|
| [design.md](./service/api/design.md) | URL, методы, статусы, partial update |
| [versioning.md](./service/api/versioning.md) | Версионирование (/v1/, /v2/) |
| [deprecation.md](./service/api/deprecation.md) | Вывод API (Sunset header, сроки) |
| [swagger.md](./service/api/swagger.md) | OpenAPI, Swagger UI на /docs |
| [realtime.md](./service/api/realtime.md) | WebSocket, SSE, polling |

### service/data/ — Форматы данных

| Инструкция | Описание |
|------------|----------|
| [errors.md](./service/data/errors.md) | Формат ошибок (code, message, details) |
| [logging.md](./service/data/logging.md) | Формат логов (JSON, request_id) |
| [pagination.md](./service/data/pagination.md) | Пагинация (page, limit, total) |
| [validation.md](./service/data/validation.md) | Валидация входных данных |

### service/database/ — База данных

| Инструкция | Описание |
|------------|----------|
| [database.md](./service/database/database.md) | Schema, migrations, transactions, pooling |

### service/dev/ — Локальная разработка

| Инструкция | Описание |
|------------|----------|
| [local.md](./service/dev/local.md) | Локальный запуск, hot reload, отладка |
| [performance.md](./service/dev/performance.md) | Профилирование, бенчмарки, лимиты |

### service/health/ — Health checks

| Инструкция | Описание |
|------------|----------|
| [health.md](./service/health/health.md) | /health, /ready, graceful shutdown |

### service/resilience/ — Устойчивость

| Инструкция | Описание |
|------------|----------|
| [resilience.md](./service/resilience/resilience.md) | Timeouts, retries, circuit breaker |

### service/security/ — Безопасность

| Инструкция | Описание |
|------------|----------|
| [auth.md](./service/security/auth.md) | JWT, аутентификация между сервисами |
| [audit.md](./service/security/audit.md) | Аудит-логи, PII, GDPR |

### service/testing/ — Тестирование сервиса

| Инструкция | Описание |
|------------|----------|
| [testing.md](./service/testing/testing.md) | Unit и integration тесты, моки |
| [unit.md](./service/testing/unit.md) | Стандарты unit-тестов |

### service/frontend/ — Клиентский код

> Папка создана, инструкции будут добавлены при необходимости.

---

## system/ — Система

Scope: инфраструктура, общий код, конфигурации — всё, что **не принадлежит одному сервису**.

### system/platform/ — Инфраструктура

| Инструкция | Описание |
|------------|----------|
| [docker.md](./system/platform/docker.md) | Dockerfile, docker-compose, multi-stage |
| [deployment.md](./system/platform/deployment.md) | Rolling update, blue-green, canary |
| [caching.md](./system/platform/caching.md) | Redis, TTL, cache-aside |
| [operations.md](./system/platform/operations.md) | Runbooks, incidents, postmortems |
| [security.md](./system/platform/security.md) | Dependabot, GitLeaks, Semgrep |

### system/platform/observability/ — Наблюдаемость

| Инструкция | Описание |
|------------|----------|
| [overview.md](./system/platform/observability/overview.md) | Logs, metrics, traces — три столпа |
| [logging.md](./system/platform/observability/logging.md) | Loki, корреляция с request_id |
| [metrics.md](./system/platform/observability/metrics.md) | Prometheus, labels, типы метрик |
| [tracing.md](./system/platform/observability/tracing.md) | OpenTelemetry, W3C traceparent |
| [alerting.md](./system/platform/observability/alerting.md) | Severity levels, routing, runbooks |

### system/tests/ — Системные тесты

| Инструкция | Описание |
|------------|----------|
| [e2e.md](./system/tests/e2e.md) | End-to-end сценарии |
| [integration.md](./system/tests/integration.md) | Интеграция между сервисами |
| [load.md](./system/tests/load.md) | Нагрузочные тесты (k6) |
| [smoke.md](./system/tests/smoke.md) | Быстрая проверка работоспособности |
| [fixtures.md](./system/tests/fixtures.md) | Тестовые данные, фабрики |
| [formats.md](./system/tests/formats.md) | Форматы тестов |
| [project-testing.md](./system/tests/project-testing.md) | Индекс тестирования проекта |

### system/shared/ — Общий код

| Инструкция | Описание |
|------------|----------|
| [contracts.md](./system/shared/contracts.md) | OpenAPI, Protobuf, JSON Schema |
| [events.md](./system/shared/events.md) | Схемы событий, идемпотентность |
| [libs.md](./system/shared/libs.md) | Общие библиотеки (errors, logging) |
| [assets.md](./system/shared/assets.md) | Иконки, шрифты, брендинг |
| [i18n.md](./system/shared/i18n.md) | Локализация |

### system/config/ — Конфигурации

| Инструкция | Описание |
|------------|----------|
| [environments.md](./system/config/environments.md) | dev, staging, production |
| [feature-flags.md](./system/config/feature-flags.md) | Feature flags, rollout |

---

## workflow/ — Процессы

Scope: **как работаем** — git, GitHub, спецификации, документация.

### workflow/git/ — Git процессы

| Инструкция | Описание |
|------------|----------|
| [commits.md](./workflow/git/commits.md) | Conventional commits |
| [workflow.md](./workflow/git/workflow.md) | GitHub Flow, ветки, PR |
| [review.md](./workflow/git/review.md) | Code review, CODEOWNERS |
| [issues.md](./workflow/git/issues.md) | Связь с GitHub Issues |

### workflow/github/ — GitHub платформа

| Инструкция | Описание |
|------------|----------|
| [actions.md](./workflow/github/actions.md) | CI/CD, GitHub Actions |

### workflow/github/issues/ — GitHub Issues

| Инструкция | Описание |
|------------|----------|
| [format.md](./workflow/github/issues/format.md) | Формат заголовка, префиксы |
| [labels.md](./workflow/github/issues/labels.md) | Система меток |
| [workflow.md](./workflow/github/issues/workflow.md) | Жизненный цикл Issue |
| [commands.md](./workflow/github/issues/commands.md) | Команды gh CLI |
| [errors.md](./workflow/github/issues/errors.md) | Обработка ошибок |
| [examples.md](./workflow/github/issues/examples.md) | Примеры использования |

### workflow/specs/ — Спецификации

| Инструкция | Описание |
|------------|----------|
| [discussions.md](./workflow/specs/discussions.md) | Формат дискуссий |
| [impact.md](./workflow/specs/impact.md) | Импакт-анализ |
| [adr.md](./workflow/specs/adr.md) | ADR, архитектурные решения |
| [plans.md](./workflow/specs/plans.md) | Планы реализации |
| [architecture.md](./workflow/specs/architecture.md) | Архитектура сервиса |
| [glossary.md](./workflow/specs/glossary.md) | Глоссарий терминов |
| [statuses.md](./workflow/specs/statuses.md) | Система статусов |
| [workflow.md](./workflow/specs/workflow.md) | Полный workflow |
| [rules.md](./workflow/specs/rules.md) | Правила и запреты |
| [naming.md](./workflow/specs/naming.md) | Именование файлов |
| [indexes.md](./workflow/specs/indexes.md) | Индексы документов |
| [relations.md](./workflow/specs/relations.md) | Связи между документами |
| [output.md](./workflow/specs/output.md) | Форматы вывода |
| [errors.md](./workflow/specs/errors.md) | Обработка ошибок |
| [examples.md](./workflow/specs/examples.md) | Примеры |

### workflow/docs/ — Документация

| Инструкция | Описание |
|------------|----------|
| [structure.md](./workflow/docs/structure.md) | Структура /doc/ |
| [rules.md](./workflow/docs/rules.md) | Правила документации |
| [templates.md](./workflow/docs/templates.md) | Выбор шаблона |
| [workflow.md](./workflow/docs/workflow.md) | Workflow docs-* скиллов |
| [errors.md](./workflow/docs/errors.md) | Обработка ошибок |
| [examples.md](./workflow/docs/examples.md) | Примеры |

---

## meta/ — Claude-сущности

Scope: **как создавать и поддерживать** инструкции, скиллы, агенты и другие Claude-артефакты.

### meta/instructions/ — Правила инструкций

| Инструкция | Описание |
|------------|----------|
| [structure.md](./meta/instructions/structure.md) | Расположение и допустимые папки |
| [types.md](./meta/instructions/types.md) | Типы (standard/project) |
| [validation.md](./meta/instructions/validation.md) | Валидация формата |
| [statuses.md](./meta/instructions/statuses.md) | Система статусов |
| [workflow.md](./meta/instructions/workflow.md) | Жизненный цикл |
| [workflow-create.md](./meta/instructions/workflow-create.md) | CREATE workflow |
| [workflow-update.md](./meta/instructions/workflow-update.md) | UPDATE workflow |
| [workflow-deactivate.md](./meta/instructions/workflow-deactivate.md) | DEACTIVATE workflow |
| [patterns.md](./meta/instructions/patterns.md) | Паттерны поиска |
| [relations.md](./meta/instructions/relations.md) | Связи между инструкциями |
| [examples.md](./meta/instructions/examples.md) | Примеры |

### meta/links/ — Правила ссылок

| Инструкция | Описание |
|------------|----------|
| [format.md](./meta/links/format.md) | Форматы ссылок |
| [patterns.md](./meta/links/patterns.md) | Regex-паттерны |
| [workflow.md](./meta/links/workflow.md) | Жизненный цикл |
| [validation.md](./meta/links/validation.md) | Правила валидации |
| [edge-cases.md](./meta/links/edge-cases.md) | Граничные случаи |
| [examples.md](./meta/links/examples.md) | Примеры |

### meta/skills/ — Правила скиллов

| Инструкция | Описание |
|------------|----------|
| [rules.md](./meta/skills/rules.md) | Правило одного действия |
| [parameters.md](./meta/skills/parameters.md) | Стандартные параметры |
| [workflow.md](./meta/skills/workflow.md) | Шаблоны воркфлоу |
| [errors.md](./meta/skills/errors.md) | Коды ошибок |
| [output.md](./meta/skills/output.md) | Форматы вывода |
| [state.md](./meta/skills/state.md) | Временные файлы |
| [integration.md](./meta/skills/integration.md) | Интеграция скиллов |
| [validation.md](./meta/skills/validation.md) | Валидация |
| [examples.md](./meta/skills/examples.md) | Примеры |

### meta/agents/, meta/scripts/, meta/state/, meta/templates/

> Папки созданы, инструкции будут добавлены при необходимости.

---

## Связанные ресурсы

- [CLAUDE.md](/CLAUDE.md) — точка входа для Claude
- [/.claude/skills/README.md](/.claude/skills/README.md) — индекс скиллов
- [/.claude/templates/README.md](/.claude/templates/README.md) — шаблоны
- [new_structure_of_project.md](/new_structure_of_project.md) — описание 4-scope структуры
