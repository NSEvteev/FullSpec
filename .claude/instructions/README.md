# Инструкции для LLM

Индекс всех инструкций проекта. Единая точка входа.

**Полное описание структуры:** [refactoring.md](/refactoring.md)

## Оглавление

- [Паттерн](#паттерн)
- [Начало работы](#начало-работы)
- [Workflow статусы](#workflow-статусы)
- [Дерево инструкций](#дерево-инструкций)
- [/src/ — Правила разработки сервисов](#src--правила-разработки-сервисов)
- [/platform/ — Правила инфраструктуры](#platform--правила-инфраструктуры)
- [/tests/ — Правила тестирования](#tests--правила-тестирования)
- [/doc/ — Правила документации](#doc--правила-документации)
- [/shared/ — Правила общего кода](#shared--правила-общего-кода)
- [/config/ — Правила конфигураций](#config--правила-конфигураций)
- [/git/ — Правила Git](#git--правила-git)
- [/tools/ — Инструменты Claude](#tools--инструменты-claude)

---

## Паттерн

Инструкции для папки `/X/` находятся в `/.claude/instructions/X/`.

| Папка проекта | Инструкции |
|---------------|------------|
| `/src/` | `/.claude/instructions/src/` |
| `/doc/` | `/.claude/instructions/doc/` |
| `/shared/` | `/.claude/instructions/shared/` |
| `/config/` | `/.claude/instructions/config/` |
| `/platform/` | `/.claude/instructions/platform/` |
| `/tests/` | `/.claude/instructions/tests/` |

**Внутренние инструкции:**
- `/.claude/instructions/git/` — Git workflow, коммиты, issues
- `/.claude/instructions/tools/` — агенты и скиллы

---

## Начало работы

> **Важно:** Инструкции в этом индексе ещё не созданы. Перед началом работы с проектом необходимо создать и заполнить их.

| Ситуация | Команда | Описание |
|----------|---------|----------|
| Создание инструкции | `/instruction-create` | Создаёт файл и генерирует содержимое |
| Изменение инструкции | `/instruction-update` | Проверяет файлы проекта на соответствие новым правилам |

**Рекомендуемый порядок:** начинать с инструкций типа `standard`, затем `project`.

---

## Workflow статусы

| Статус | Значение |
|--------|----------|
| ⬜ | Не выполнено |
| ✅ | Выполнено |

| Столбец | Что означает |
|---------|--------------|
| Тип | `standard` — требования (как делать), `project` — специфика (что есть) |
| Создано | Файл существует |
| Заполнено | Содержимое написано |

---

## Дерево инструкций

> ✅ Все папки созданы. Файлы создаются по мере необходимости через `/instruction-create`.

```
/.claude/instructions/
  README.md                             # индекс всех инструкций

  /src/                                 # правила разработки сервисов
    documentation.md                    # правила документирования кода
    /api/                               # проектирование API
      design.md                         # URL, методы, статусы, частичное обновление
      versioning.md                     # версионирование (/v1/, /v2/)
      deprecation.md                    # вывод API (заголовки, сроки, миграция)
      swagger.md                        # документация API (OpenAPI, /docs)
    /data/                              # форматы данных
      errors.md                         # формат ошибок (code, message, details)
      logging.md                        # формат логов (JSON, request_id)
      validation.md                     # валидация входных данных
      pagination.md                     # формат пагинации (page, limit, total)
    /runtime/                           # поведение в runtime
      health.md                         # проверки (/health, /ready, завершение)
      database.md                       # работа с БД (пул, миграции, транзакции)
      resilience.md                     # устойчивость (таймауты, повторы, предохранитель)
      realtime.md                       # real-time (polling, SSE, WebSocket)
    /dev/                               # разработка
      local.md                          # локальный запуск (hot reload, отладка)
      testing.md                        # тесты (unit, integration, моки)
      performance.md                    # производительность (профилирование, лимиты)
    /security/                          # безопасность
      auth.md                           # аутентификация (JWT между сервисами)
      audit.md                          # аудит (кто/что/когда, PII, GDPR)

  /platform/                            # правила инфраструктуры
    docker.md                           # работа с Docker (образы, compose)
    caching.md                          # кэширование (Redis, TTL, инвалидация)
    deployment.md                       # деплой (rolling, blue-green, откат)
    security.md                         # безопасность инфраструктуры
    /observability/                     # наблюдаемость
      overview.md                       # обзор (логи, метрики, трейсы)
      metrics.md                        # метрики (Prometheus, labels)
      tracing.md                        # трейсы (OpenTelemetry, span)
      logging.md                        # логи (Loki, корреляция)
      alerting.md                       # алерты (severity, маршрутизация)
    operations.md                       # runbooks, incidents, postmortems

  /tests/                               # правила тестирования проекта
    unit.md                             # unit-тесты (изоляция, моки)
    integration.md                      # интеграционные тесты (БД, API)
    e2e.md                              # e2e тесты (сценарии, инструменты)
    smoke.md                            # smoke-тесты (быстрая проверка)
    load.md                             # нагрузочные тесты (k6, пороги)
    fixtures.md                         # тестовые данные (фикстуры, фабрики)

  /doc/                                 # правила документации
    structure.md                        # структура (зеркалирование, ссылки на код)

  /shared/                              # правила общего кода
    contracts.md                        # контракты (OpenAPI, Protobuf, JSON Schema)
    events.md                           # события (именование, идемпотентность, DLQ)
    libs.md                             # общие библиотеки (ошибки, логи, валидация)
    assets.md                           # статика (иконки, шрифты, брендинг)
    i18n.md                             # локализация (формат ключей)

  /config/                              # правила конфигураций
    environments.md                     # окружения (dev/staging/prod)
    feature-flags.md                    # флаги функций (когда использовать)

  /git/                                 # правила Git
    workflow.md                         # рабочий процесс (ветки, PR)
    commits.md                          # коммиты (conventional, changelog)
    issues.md                           # задачи (префиксы, метки)
    ci.md                               # CI/CD pipeline, GitHub Actions, quality gates
    review.md                           # code review: чек-лист, CODEOWNERS, правила

  /tools/                               # инструменты Claude
    skills.md                           # индекс скиллов
    agents.md                           # индекс агентов
    claude-testing.md                   # тестирование Claude Code (smoke tests)
    project-testing.md                  # тестирование проекта (unit, e2e, load)
```

---

## /src/ — Правила разработки сервисов

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [documentation.md](./src/documentation.md) | Документирование кода: ссылки на /doc/, комментарии, README | standard | ✅ | ✅ |
| **api/** | Проектирование REST API ||||
| [design.md](./src/api/design.md) | URL naming (kebab-case), HTTP методы, статус-коды, partial update, bulk operations | standard | ⬜ | ⬜ |
| [versioning.md](./src/api/versioning.md) | Версионирование API через URL (/v1/, /v2/), gRPC package versioning | standard | ⬜ | ⬜ |
| [deprecation.md](./src/api/deprecation.md) | Вывод API: Sunset header, Deprecation header, сроки, migration guide | standard | ⬜ | ⬜ |
| [swagger.md](./src/api/swagger.md) | OpenAPI спецификация, Swagger UI на /docs, автогенерация | standard | ⬜ | ⬜ |
| **data/** | Форматы данных ||||
| [errors.md](./src/data/errors.md) | Единый формат ошибок: {error: {code, message, details, request_id}} | standard | ⬜ | ⬜ |
| [logging.md](./src/data/logging.md) | Structured JSON logging: timestamp, level, service, request_id, message | standard | ⬜ | ⬜ |
| [validation.md](./src/data/validation.md) | Валидация входных данных, формат ошибок по полям, JSON Schema | standard | ⬜ | ⬜ |
| [pagination.md](./src/data/pagination.md) | Формат пагинации: {data, pagination: {page, limit, total, total_pages}} | standard | ⬜ | ⬜ |
| **runtime/** | Поведение сервисов в runtime ||||
| [health.md](./src/runtime/health.md) | Health checks: /health, /ready, graceful shutdown (SIGTERM, 30s) | standard | ⬜ | ⬜ |
| [database.md](./src/runtime/database.md) | Connection pooling, миграции, транзакции, saga pattern, snake_case | standard | ⬜ | ⬜ |
| [resilience.md](./src/runtime/resilience.md) | Устойчивость: таймауты, повторы (retry), circuit breaker, fallbacks | standard | ⬜ | ⬜ |
| [realtime.md](./src/runtime/realtime.md) | Real-time: polling vs SSE vs WebSocket, когда что использовать | standard | ⬜ | ⬜ |
| **dev/** | Разработка ||||
| [local.md](./src/dev/local.md) | Локальная разработка: make dev, hot reload, debug порты, IDE | project | ⬜ | ⬜ |
| [testing.md](./src/dev/testing.md) | Unit и integration тесты, моки, покрытие, расположение тестов | standard | ⬜ | ⬜ |
| [performance.md](./src/dev/performance.md) | Профилирование, бенчмарки, лимиты: p99 < 200ms, память < 512MB | standard | ⬜ | ⬜ |
| **security/** | Безопасность ||||
| [auth.md](./src/security/auth.md) | Аутентификация между сервисами: JWT, service accounts | standard | ⬜ | ⬜ |
| [audit.md](./src/security/audit.md) | Аудит-логи (кто/что/когда), PII, GDPR, data retention | standard | ⬜ | ⬜ |

---

## /platform/ — Правила инфраструктуры

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [docker.md](./platform/docker.md) | Dockerfile best practices, docker-compose, образы, multi-stage | standard | ⬜ | ⬜ |
| [caching.md](./platform/caching.md) | Redis: cache-aside, TTL, key naming ({service}:{entity}:{id}) | standard | ⬜ | ⬜ |
| [deployment.md](./platform/deployment.md) | Деплой: rolling update, blue-green, canary, автооткат | standard | ⬜ | ⬜ |
| [security.md](./platform/security.md) | Безопасность: Dependabot, GitLeaks, Semgrep, scanning в CI | standard | ⬜ | ⬜ |
| **observability/** | Наблюдаемость (три столпа) ||||
| [overview.md](./platform/observability/overview.md) | Обзор: logs (Loki), metrics (Prometheus), traces (Tempo) | standard | ⬜ | ⬜ |
| [metrics.md](./platform/observability/metrics.md) | Prometheus метрики: naming, labels, типы (counter, gauge, histogram) | standard | ⬜ | ⬜ |
| [tracing.md](./platform/observability/tracing.md) | Distributed tracing: OpenTelemetry, span, W3C traceparent | standard | ⬜ | ⬜ |
| [logging.md](./platform/observability/logging.md) | Централизованные логи: Loki, корреляция с request_id | standard | ⬜ | ⬜ |
| [alerting.md](./platform/observability/alerting.md) | Алертинг: severity levels, routing, связь с runbooks | standard | ⬜ | ⬜ |
| [operations.md](./platform/operations.md) | Операции: runbooks, incidents, postmortems | standard | ⬜ | ⬜ |

---

## /tests/ — Правила тестирования

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [project-testing.md](./tools/project-testing.md) | Тестирование проекта (unit, e2e, load) | project | ✅ | ✅ |
| [unit.md](./tests/unit.md) | Unit-тесты: изоляция, моки, покрытие | standard | ⬜ | ⬜ |
| [integration.md](./tests/integration.md) | Интеграционные тесты: БД, API, сервисы | standard | ⬜ | ⬜ |
| [e2e.md](./tests/e2e.md) | End-to-end тесты: сценарии пользователя, инструменты | standard | ⬜ | ⬜ |
| [smoke.md](./tests/smoke.md) | Smoke-тесты: быстрая проверка работоспособности | standard | ⬜ | ⬜ |
| [load.md](./tests/load.md) | Нагрузочные тесты: k6, пороги производительности | standard | ⬜ | ⬜ |
| [fixtures.md](./tests/fixtures.md) | Тестовые данные: фикстуры, фабрики, seeds | standard | ⬜ | ⬜ |

---

## /doc/ — Правила документации

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [structure.md](./doc/structure.md) | Структура /doc/: зеркалирование, ссылки на код, ADR, runbooks | project | ✅ | ✅ |

---

## /shared/ — Правила общего кода

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [contracts.md](./shared/contracts.md) | API контракты: OpenAPI, Protobuf, JSON Schema | standard | ⬜ | ⬜ |
| [events.md](./shared/events.md) | События: naming ({service}.{entity}.{action}), идемпотентность, DLQ | standard | ⬜ | ⬜ |
| [libs.md](./shared/libs.md) | Общие библиотеки: errors, logging, validation | project | ⬜ | ⬜ |
| [assets.md](./shared/assets.md) | Статические ресурсы: иконки, шрифты, брендинг | project | ⬜ | ⬜ |
| [i18n.md](./shared/i18n.md) | Локализация: формат ключей, структура /shared/i18n/{locale}/ | standard | ⬜ | ⬜ |

---

## /config/ — Правила конфигураций

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [environments.md](./config/environments.md) | Окружения: development.yaml, staging.yaml, production.yaml | project | ⬜ | ⬜ |
| [feature-flags.md](./config/feature-flags.md) | Feature flags: когда использовать, YAML vs Unleash | standard | ⬜ | ⬜ |

---

## /git/ — Правила Git

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [workflow.md](./git/workflow.md) | Git workflow: GitHub Flow, ветки (main + feature/fix), PR | standard | ✅ | ✅ |
| [commits.md](./git/commits.md) | Conventional commits: feat/fix/breaking, автогенерация CHANGELOG | standard | ✅ | ✅ |
| [issues.md](./git/issues.md) | GitHub Issues: префиксы ([AUTH], [NOTIFY]), labels, gh commands | standard | ✅ | ✅ |
| [ci.md](./git/ci.md) | CI/CD: pipeline структура, GitHub Actions, quality gates | standard | ✅ | ✅ |
| [review.md](./git/review.md) | Code review: чек-лист, CODEOWNERS, правила approve | standard | ✅ | ✅ |

---

## /tools/ — Инструменты Claude

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [skills.md](./tools/skills.md) | Индекс скиллов: команды автоматизации, категории, триггеры | project | ✅ | ✅ |
| [agents.md](./tools/agents.md) | Индекс агентов: специализированные агенты, их роли и скиллы | project | ✅ | ✅ |
| [claude-testing.md](./tools/claude-testing.md) | Тестирование Claude Code: smoke tests, проверка скиллов | standard | ✅ | ✅ |
| [project-testing.md](./tools/project-testing.md) | Тестирование проекта (unit, e2e, load) | project | ✅ | ✅ |
