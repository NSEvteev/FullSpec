# Инструкции для LLM

Индекс всех инструкций проекта. Единая точка входа.

**Полное описание структуры:** [refactoring.md](/refactoring.md)

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

## Начало работы

> ⚠️ **Важно:** Все инструкции в этом индексе уже созданы как файлы-заглушки. Перед началом работы с проектом необходимо заполнить их содержимым.

| Ситуация | Команда | Описание |
|----------|---------|----------|
| Заполнение пустой инструкции | `/instruction-create` | Генерирует содержимое для существующей инструкции |
| Создание новой инструкции | `/instruction-create` | Создаёт новый файл инструкции (если его нет в индексе) |
| Изменение инструкции | `/instruction-update` | Проверяет файлы проекта на соответствие новым правилам |

**Рекомендуемый порядок заполнения:** см. "План создания инструкций" в [CLAUDE.md](/CLAUDE.md)

## Workflow статусы

| Статус | Значение |
|--------|----------|
| ⬜ | Не выполнено |
| ✅ | Выполнено |

| Столбец | Что означает |
|---------|--------------|
| Создано | Файл существует |
| Тип | Определён тип (`s` = standard, `p` = project) и зона ответственности |
| Заполнено | Содержимое написано |

## Дерево инструкций

```
/.claude/instructions/
  README.md                             ✅ индекс всех инструкций

  /src/                                 # правила разработки сервисов
    documentation.md                    ⬜ правила документирования кода
    /api/                               # проектирование API
      design.md                         ⬜ URL, методы, статусы, частичное обновление
      versioning.md                     ⬜ версионирование (/v1/, /v2/)
      deprecation.md                    ⬜ вывод API (заголовки, сроки, миграция)
      swagger.md                        ⬜ документация API (OpenAPI, /docs)
    /data/                              # форматы данных
      errors.md                         ⬜ формат ошибок (code, message, details)
      logging.md                        ⬜ формат логов (JSON, request_id)
      validation.md                     ⬜ валидация входных данных
      pagination.md                     ⬜ формат пагинации (page, limit, total)
    /runtime/                           # поведение в runtime
      health.md                         ⬜ проверки (/health, /ready, завершение)
      database.md                       ⬜ работа с БД (пул, миграции, транзакции)
      resilience.md                     ⬜ устойчивость (таймауты, повторы, предохранитель)
      realtime.md                       ⬜ real-time (polling, SSE, WebSocket)
    /dev/                               # разработка
      local.md                          ⬜ локальный запуск (hot reload, отладка)
      testing.md                        ⬜ тесты (unit, integration, моки)
      performance.md                    ⬜ производительность (профилирование, лимиты)
    /security/                          # безопасность
      auth.md                           ⬜ аутентификация (JWT между сервисами)
      audit.md                          ⬜ аудит (кто/что/когда, PII, GDPR)

  /platform/                            # правила инфраструктуры
    docker.md                           ⬜ работа с Docker (образы, compose)
    caching.md                          ⬜ кэширование (Redis, TTL, инвалидация)
    deployment.md                       ⬜ деплой (rolling, blue-green, откат)
    security.md                         ⬜ безопасность инфраструктуры
    /observability/                     # наблюдаемость
      overview.md                       ⬜ обзор (логи, метрики, трейсы)
      metrics.md                        ⬜ метрики (Prometheus, labels)
      tracing.md                        ⬜ трейсы (OpenTelemetry, span)
      logging.md                        ⬜ логи (Loki, корреляция)
      alerting.md                       ⬜ алерты (severity, маршрутизация)

  /tests/                               # правила тестирования
    e2e.md                              ⬜ e2e тесты (сценарии, инструменты)
    load.md                             ⬜ нагрузочные тесты (k6, пороги)
    fixtures.md                         ⬜ тестовые данные (фикстуры, фабрики)

  /doc/                                 # правила документации
    structure.md                        ⬜ структура (зеркалирование, ссылки на код)

  /shared/                              # правила общего кода
    contracts.md                        ⬜ контракты (OpenAPI, Protobuf, JSON Schema)
    events.md                           ⬜ события (именование, идемпотентность, DLQ)
    libs.md                             ⬜ общие библиотеки (ошибки, логи, валидация)
    assets.md                           ⬜ статика (иконки, шрифты, брендинг)
    i18n.md                             ⬜ локализация (формат ключей)

  /config/                              # правила конфигураций
    environments.md                     ⬜ окружения (dev/staging/prod)
    feature-flags.md                    ⬜ флаги функций (когда использовать)

  /git/                                 # правила Git
    workflow.md                         ⬜ рабочий процесс (ветки, PR)
    commits.md                          ⬜ коммиты (conventional, changelog)
    issues.md                           ⬜ задачи (префиксы, метки)

  /tools/                               # инструменты Claude
    skills.md                           ✅ индекс скиллов
    agents.md                           ✅ индекс агентов
```

**Статус:** ✅ Готово (3) | ⬜ Не создано (40)

---

## /src/ — Правила разработки сервисов

| Инструкция | Описание | Создано | Тип | Заполнено |
|------------|----------|:-------:|:---:|:---------:|
| **api/** | Проектирование REST API ||||
| [design.md](./src/api/design.md) | URL naming (kebab-case), HTTP методы (GET/POST/PUT/PATCH/DELETE), статус-коды, partial update (JSON Merge Patch), bulk operations | ⬜ | ⬜ | ⬜ |
| [versioning.md](./src/api/versioning.md) | Версионирование API через URL (/v1/, /v2/), gRPC package versioning, совместимость версий | ⬜ | ⬜ | ⬜ |
| [deprecation.md](./src/api/deprecation.md) | Вывод API из эксплуатации: Sunset header, Deprecation header, сроки (минимум 3 месяца), migration guide | ⬜ | ⬜ | ⬜ |
| [swagger.md](./src/api/swagger.md) | OpenAPI спецификация, Swagger UI на /docs, автогенерация документации | ⬜ | ⬜ | ⬜ |
| **data/** | Форматы данных ||||
| [errors.md](./src/data/errors.md) | Единый формат ошибок: {error: {code, message, details, request_id}}, коды ошибок, ошибки валидации | ⬜ | ⬜ | ⬜ |
| [logging.md](./src/data/logging.md) | Structured JSON logging: timestamp, level, service, request_id, message, context. Уровни логирования | ⬜ | ⬜ | ⬜ |
| [validation.md](./src/data/validation.md) | Валидация входных данных, формат ошибок валидации по полям, JSON Schema | ⬜ | ⬜ | ⬜ |
| [pagination.md](./src/data/pagination.md) | Формат пагинации: {data, pagination: {page, limit, total, total_pages}}, offset-based подход | ⬜ | ⬜ | ⬜ |
| **runtime/** | Поведение сервисов в runtime ||||
| [health.md](./src/runtime/health.md) | Health checks: /health (liveness), /ready (readiness), graceful shutdown (SIGTERM, timeout 30s), проверка зависимостей | ⬜ | ⬜ | ⬜ |
| [database.md](./src/runtime/database.md) | Connection pooling, миграции (только forward), транзакции, saga pattern для cross-service, snake_case naming | ⬜ | ⬜ | ⬜ |
| [resilience.md](./src/runtime/resilience.md) | Устойчивость: таймауты, повторы (retry), circuit breaker, fallbacks | ⬜ | ⬜ | ⬜ |
| [realtime.md](./src/runtime/realtime.md) | Real-time коммуникация: polling vs SSE vs WebSocket, когда что использовать, heartbeat | ⬜ | ⬜ | ⬜ |
| **dev/** | Разработка ||||
| [local.md](./src/dev/local.md) | Локальная разработка: make dev, hot reload, debug порты (9229 Node.js, 5678 Python), IDE настройки | ⬜ | ⬜ | ⬜ |
| [testing.md](./src/dev/testing.md) | Unit и integration тесты, моки, покрытие кода, расположение тестов в /src/{service}/tests/ | ⬜ | ⬜ | ⬜ |
| [performance.md](./src/dev/performance.md) | Профилирование, бенчмарки, лимиты производительности: p99 < 200ms, память < 512MB | ⬜ | ⬜ | ⬜ |
| **security/** | Безопасность ||||
| [auth.md](./src/security/auth.md) | Аутентификация между сервисами: JWT, service accounts, подпись токенов, проверка | ⬜ | ⬜ | ⬜ |
| [audit.md](./src/security/audit.md) | Аудит-логи (кто/что/когда), PII (не логировать, маскировать), GDPR, data retention, right to be forgotten | ⬜ | ⬜ | ⬜ |
| **другое** |||||
| [documentation.md](./src/documentation.md) | Документирование кода: ссылки на /doc/, комментарии, README в сервисах | ⬜ | ⬜ | ⬜ |

---

## /platform/ — Правила инфраструктуры

| Инструкция | Описание | Создано | Тип | Заполнено |
|------------|----------|:-------:|:---:|:---------:|
| [docker.md](./platform/docker.md) | Dockerfile best practices, docker-compose, образы, multi-stage builds | ⬜ | ⬜ | ⬜ |
| [caching.md](./platform/caching.md) | Redis кэширование: паттерн cache-aside, TTL обязателен, key naming ({service}:{entity}:{id}), инвалидация | ⬜ | ⬜ | ⬜ |
| [deployment.md](./platform/deployment.md) | Стратегии деплоя: rolling update (default), blue-green, canary, автоматический rollback при падении health | ⬜ | ⬜ | ⬜ |
| [security.md](./platform/security.md) | Безопасность инфраструктуры: Dependabot, GitLeaks, Semgrep, security scanning в CI | ⬜ | ⬜ | ⬜ |
| **observability/** | Наблюдаемость (три столпа) ||||
| [overview.md](./platform/observability/overview.md) | Обзор observability: logs (Loki), metrics (Prometheus), traces (Tempo), корреляция через request_id и trace_id | ⬜ | ⬜ | ⬜ |
| [metrics.md](./platform/observability/metrics.md) | Prometheus метрики: naming conventions, labels, типы метрик (counter, gauge, histogram) | ⬜ | ⬜ | ⬜ |
| [tracing.md](./platform/observability/tracing.md) | Distributed tracing: OpenTelemetry, span, trace_id, propagation через W3C traceparent | ⬜ | ⬜ | ⬜ |
| [logging.md](./platform/observability/logging.md) | Централизованные логи: Loki, корреляция с request_id, структура логов | ⬜ | ⬜ | ⬜ |
| [alerting.md](./platform/observability/alerting.md) | Алертинг: severity levels, routing, связь с runbooks | ⬜ | ⬜ | ⬜ |

---

## /tests/ — Правила тестирования

| Инструкция | Описание | Создано | Тип | Заполнено |
|------------|----------|:-------:|:---:|:---------:|
| [e2e.md](./tests/e2e.md) | End-to-end тесты: сценарии пользователя, инструменты, расположение в /tests/e2e/ | ⬜ | ⬜ | ⬜ |
| [load.md](./tests/load.md) | Нагрузочные тесты: k6, пороги производительности, сценарии в /tests/load/ | ⬜ | ⬜ | ⬜ |
| [fixtures.md](./tests/fixtures.md) | Тестовые данные: фикстуры, фабрики, seeds, расположение | ⬜ | ⬜ | ⬜ |

---

## /doc/ — Правила документации

| Инструкция | Описание | Создано | Тип | Заполнено |
|------------|----------|:-------:|:---:|:---------:|
| [structure.md](./doc/structure.md) | Структура /doc/: зеркалирование src/shared/platform, ссылки на код, ADR, runbooks, specs | ⬜ | ⬜ | ⬜ |

---

## /shared/ — Правила общего кода

| Инструкция | Описание | Создано | Тип | Заполнено |
|------------|----------|:-------:|:---:|:---------:|
| [contracts.md](./shared/contracts.md) | API контракты: OpenAPI (REST), Protobuf (gRPC), JSON Schema (events), расположение в /shared/contracts/ | ⬜ | ⬜ | ⬜ |
| [events.md](./shared/events.md) | События для очередей: naming ({service}.{entity}.{action}), идемпотентность (event_id), DLQ, схемы | ⬜ | ⬜ | ⬜ |
| [libs.md](./shared/libs.md) | Общие библиотеки: /shared/libs/errors/, /shared/libs/logging/, /shared/libs/validation/ | ⬜ | ⬜ | ⬜ |
| [assets.md](./shared/assets.md) | Статические ресурсы: иконки, шрифты, брендинг в /shared/assets/ | ⬜ | ⬜ | ⬜ |
| [i18n.md](./shared/i18n.md) | Локализация: формат ключей, структура /shared/i18n/{locale}/, JSON файлы | ⬜ | ⬜ | ⬜ |

---

## /config/ — Правила конфигураций

| Инструкция | Описание | Создано | Тип | Заполнено |
|------------|----------|:-------:|:---:|:---------:|
| [environments.md](./config/environments.md) | Окружения: development.yaml, staging.yaml, production.yaml, структура конфигов | ⬜ | ⬜ | ⬜ |
| [feature-flags.md](./config/feature-flags.md) | Feature flags: когда использовать, простой вариант (YAML), продвинутый (Unleash) | ⬜ | ⬜ | ⬜ |

---

## /git/ — Правила Git

| Инструкция | Описание | Создано | Тип | Заполнено |
|------------|----------|:-------:|:---:|:---------:|
| [workflow.md](./git/workflow.md) | Git workflow: GitHub Flow, ветки (main + feature/fix), PR процесс, code review | ⬜ | ⬜ | ⬜ |
| [commits.md](./git/commits.md) | Conventional commits: feat/fix/breaking, формат сообщений, автогенерация CHANGELOG | ⬜ | ⬜ | ⬜ |
| [issues.md](./git/issues.md) | GitHub Issues: префиксы ([AUTH], [NOTIFY]), labels (service:*), gh commands | ⬜ | ⬜ | ⬜ |

---

## /tools/ — Инструменты Claude

| Инструкция | Описание | Создано | Тип | Заполнено |
|------------|----------|:-------:|:---:|:---------:|
| [skills.md](./tools/skills.md) | Индекс скиллов: список команд автоматизации, категории, триггеры | ✅ | ✅ (p) | ✅ |
| [agents.md](./tools/agents.md) | Индекс агентов: специализированные агенты, их роли и скиллы | ✅ | ✅ (p) | ✅ |
