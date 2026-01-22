# Инструкции для LLM

Индекс всех инструкций проекта. Единая точка входа.

**Полное описание структуры:** [README.md](/README.md)

## Оглавление

- [Паттерн](#паттерн)
- [Правила структуры проекта](#правила-структуры-проекта)
- [Начало работы](#начало-работы)
- [Workflow статусы](#workflow-статусы)
- [Дерево инструкций](#дерево-инструкций)
- [/config/ — Правила конфигураций](#config--правила-конфигураций)
- [/doc/ — Правила документации](#doc--правила-документации)
- [/git/ — Правила Git](#git--правила-git)
- [/instructions/ — Мета-инструкции](#instructions--мета-инструкции)
- [/links/ — Правила работы со ссылками](#links--правила-работы-со-ссылками)
- [/platform/ — Правила инфраструктуры](#platform--правила-инфраструктуры)
- [/shared/ — Правила общего кода](#shared--правила-общего-кода)
- [/skills/ — Правила скиллов](#skills--правила-скиллов)
- [/specs/ — Правила спецификаций](#specs--правила-спецификаций)
- [/src/ — Правила разработки сервисов](#src--правила-разработки-сервисов)
- [/tests/ — Правила тестирования](#tests--правила-тестирования)

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
- `/.claude/instructions/tools/` — документирование кода
- `/.claude/instructions/tests/` — тестирование (включая Claude Code)

---

## Правила структуры проекта

### Какие файлы должны быть в корне

**Правило:** В корне только файлы, которые:
- Нужны инструментам, ожидающим их в корне (git, Docker, IDE)
- Являются точками входа для людей или LLM

| Категория | Файлы | Почему в корне |
|-----------|-------|----------------|
| Точки входа | README.md, CLAUDE.md | Первое, что видит человек/LLM |
| Запуск проекта | docker-compose.*, Makefile | Docker и make ищут в корне |
| Git | .gitignore, .pre-commit-config.yaml | Git ожидает в корне |
| Docker | .dockerignore | Docker ожидает в корне |
| IDE/редакторы | .editorconfig, .prettierrc, .eslintrc.js | IDE ищут конфиги в корне |
| Метаданные | LICENSE, CHANGELOG.md | Стандартное расположение |

### Чеклист: добавление файла в корень

Перед добавлением файла в корень:
1. ❓ Инструмент требует файл именно в корне?
2. ❓ Это точка входа (README, CLAUDE.md)?
3. ❓ Файл относится ко всему проекту, а не к конкретной папке?

**Если нет — файл должен быть в соответствующей папке:**
- Конфиги окружений → `/config/`
- Скрипты → `/platform/scripts/` или `/.claude/scripts/`
- Документация → `/doc/`

### Чеклист: добавление новой папки в корень

**Правило:** Новая корневая папка — исключение, не норма.

Перед созданием:
1. ❓ Можно ли поместить в существующую папку?
2. ❓ Будет ли использоваться регулярно (не одноразово)?
3. ❓ Есть ли чёткая зона ответственности, не пересекающаяся с другими?

**Если ответ "да" на все три:**
1. Добавить папку в `/README.md` (раздел "Структура проекта")
2. Создать `/.claude/instructions/{название}/` с инструкциями
3. Обновить таблицу связей папок и инструкций

---

## Начало работы

> **Статус:** Создано **104 из 104** инструкций (100%). Все инструкции созданы и заполнены.
>
> **Обновлено 2025-01-21:** Добавлены README.md индексы для всех папок (10 файлов).
> **Обновлено 2025-01-21:** Добавлена папка `/skills/` (7 файлов), scope.md, formats.md, claude-functional.md.

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

> ✅ Все папки и файлы созданы. Прогресс: 100% (104 инструкции, включая 14 README индексов).

```
/.claude/instructions/
  README.md                             # индекс всех инструкций

  /config/                              # правила конфигураций
    environments.md                     # окружения (dev/staging/prod)
    feature-flags.md                    # флаги функций (когда использовать)

  /doc/                                 # правила документации
    README.md                           # индекс документации
    structure.md                        # структура (зеркалирование, ссылки на код)
    templates.md                        # шаблоны документации
    rules.md                            # правила для doc-* скиллов

  /git/                                 # правила Git
    README.md                           # индекс Git инструкций
    ci.md                               # CI/CD pipeline, GitHub Actions, quality gates
    commits.md                          # коммиты (conventional, changelog)
    issues.md                           # задачи (префиксы, метки)
    review.md                           # code review: чек-лист, CODEOWNERS, правила
    workflow.md                         # рабочий процесс (ветки, PR)

  /instructions/                        # мета-инструкции
    README.md                           # индекс мета-инструкций
    structure.md                        # расположение инструкций
    types.md                            # типы (standard/project)
    validation.md                       # валидация формата
    statuses.md                         # система статусов
    workflow.md                         # жизненный цикл
    patterns.md                         # паттерны поиска

  /links/                               # правила работы со ссылками
    README.md                           # индекс ссылок
    format.md                           # форматы ссылок
    patterns.md                         # regex-паттерны
    workflow.md                         # жизненный цикл
    validation.md                       # правила валидации
    edge-cases.md                       # граничные случаи

  /platform/                            # правила инфраструктуры
    README.md                           # индекс инфраструктуры
    caching.md                          # кэширование (Redis, TTL, инвалидация)
    deployment.md                       # деплой (rolling, blue-green, откат)
    docker.md                           # работа с Docker (образы, compose)
    /observability/                     # наблюдаемость
      alerting.md                       # алерты (severity, маршрутизация)
      logging.md                        # логи (Loki, корреляция)
      metrics.md                        # метрики (Prometheus, labels)
      overview.md                       # обзор (логи, метрики, трейсы)
      tracing.md                        # трейсы (OpenTelemetry, span)
    operations.md                       # runbooks, incidents, postmortems
    security.md                         # безопасность инфраструктуры

  /shared/                              # правила общего кода
    README.md                           # индекс общего кода
    scope.md                            # определение scope (claude/project)
    assets.md                           # статика (иконки, шрифты, брендинг)
    contracts.md                        # контракты (OpenAPI, Protobuf, JSON Schema)
    events.md                           # события (именование, идемпотентность, DLQ)
    i18n.md                             # локализация (формат ключей)
    libs.md                             # общие библиотеки (ошибки, логи, валидация)

  /skills/                              # правила скиллов
    README.md                           # индекс правил скиллов
    rules.md                            # правило одного действия, форматы
    parameters.md                       # стандартные параметры (--dry-run, --auto)
    workflow.md                         # шаблоны воркфлоу
    errors.md                           # обработка ошибок
    output.md                           # форматы вывода
    state.md                            # временные файлы (.claude/state/)

  /specs/                               # правила спецификаций /specs/
    README.md                           # индекс, структура, связи
    statuses.md                         # унифицированная система статусов
    workflow.md                         # полный workflow от идеи до реализации
    discussions.md                      # формат и чек-листы дискуссий
    impact.md                           # импакт-анализ, связь с ADR
    adr.md                              # ADR, breaking changes, конфликты
    plans.md                            # планы реализации, GitHub Issues
    architecture.md                     # архитектура сервиса (живой документ)
    glossary.md                         # глоссарий терминов
    rules.md                            # скиллы, шаблоны, запреты

  /src/                                 # правила разработки сервисов
    README.md                           # индекс правил разработки
    /api/                               # проектирование API
      README.md                         # индекс API
      deprecation.md                    # вывод API (заголовки, сроки, миграция)
      design.md                         # URL, методы, статусы, частичное обновление
      swagger.md                        # документация API (OpenAPI, /docs)
      versioning.md                     # версионирование (/v1/, /v2/)
    /data/                              # форматы данных
      README.md                         # индекс форматов данных
      errors.md                         # формат ошибок (code, message, details)
      logging.md                        # формат логов (JSON, request_id)
      pagination.md                     # формат пагинации (page, limit, total)
      validation.md                     # валидация входных данных
    /dev/                               # разработка
      README.md                         # индекс разработки
      local.md                          # локальный запуск (hot reload, отладка)
      performance.md                    # производительность (профилирование, лимиты)
      testing.md                        # тесты (unit, integration, моки)
    /runtime/                           # поведение в runtime
      README.md                         # индекс runtime
      database.md                       # работа с БД (пул, миграции, транзакции)
      health.md                         # проверки (/health, /ready, завершение)
      realtime.md                       # real-time (polling, SSE, WebSocket)
      resilience.md                     # устойчивость (таймауты, повторы, предохранитель)
    /security/                          # безопасность
      README.md                         # индекс безопасности
      audit.md                          # аудит (кто/что/когда, PII, GDPR)
      auth.md                           # аутентификация (JWT между сервисами)

  /tests/                               # правила тестирования
    README.md                           # индекс тестирования
    formats.md                          # форматы тестов (статусы, типы, шаблоны)
    claude-testing.md                   # тестирование Claude Code (smoke tests)
    claude-functional.md                # функциональное тестирование скиллов
    e2e.md                              # e2e тесты (сценарии, инструменты)
    fixtures.md                         # тестовые данные (фикстуры, фабрики)
    integration.md                      # интеграционные тесты (БД, API)
    load.md                             # нагрузочные тесты (k6, пороги)
    project-testing.md                  # тестирование проекта (индекс)
    smoke.md                            # smoke-тесты (быстрая проверка)
    unit.md                             # unit-тесты (изоляция, моки)
```

---

## /config/ — Правила конфигураций

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [environments.md](./config/environments.md) | Окружения: development.yaml, staging.yaml, production.yaml | project | ✅ | ✅ |
| [feature-flags.md](./config/feature-flags.md) | Feature flags: когда использовать, YAML vs Unleash | standard | ✅ | ✅ |

---

## /doc/ — Правила документации

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [structure.md](./doc/structure.md) | Структура /doc/, документирование кода, шаблоны, workflow | project | ✅ | ✅ |

---

## /git/ — Правила Git

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [ci.md](./git/ci.md) | CI/CD: pipeline структура, GitHub Actions, quality gates | standard | ✅ | ✅ |
| [commits.md](./git/commits.md) | Conventional commits: feat/fix/breaking, автогенерация CHANGELOG | standard | ✅ | ✅ |
| [issues.md](./git/issues.md) | GitHub Issues: префиксы ([AUTH], [NOTIFY]), labels, gh commands | standard | ✅ | ✅ |
| [review.md](./git/review.md) | Code review: чек-лист, CODEOWNERS, правила approve | standard | ✅ | ✅ |
| [workflow.md](./git/workflow.md) | Git workflow: GitHub Flow, ветки (main + feature/fix), PR | standard | ✅ | ✅ |

---

## /instructions/ — Мета-инструкции

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [structure.md](./instructions/structure.md) | Расположение и допустимые папки | standard | ✅ | ✅ |
| [types.md](./instructions/types.md) | Типы инструкций (standard/project) | standard | ✅ | ✅ |
| [validation.md](./instructions/validation.md) | Валидация путей и формата | standard | ✅ | ✅ |
| [statuses.md](./instructions/statuses.md) | Система статусов в README.md | standard | ✅ | ✅ |
| [workflow.md](./instructions/workflow.md) | Жизненный цикл (CREATE, UPDATE, DEACTIVATE) | standard | ✅ | ✅ |
| [patterns.md](./instructions/patterns.md) | Паттерны поиска ссылок | standard | ✅ | ✅ |

---

## /links/ — Правила работы со ссылками

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [format.md](./links/format.md) | Форматы ссылок (standard, folder, marked) | standard | ✅ | ✅ |
| [patterns.md](./links/patterns.md) | Regex-паттерны поиска | standard | ✅ | ✅ |
| [workflow.md](./links/workflow.md) | Жизненный цикл (CREATE → UPDATE → DELETE → VALIDATE) | standard | ✅ | ✅ |
| [validation.md](./links/validation.md) | Правила валидации ссылок | standard | ✅ | ✅ |
| [edge-cases.md](./links/edge-cases.md) | Граничные случаи | standard | ✅ | ✅ |

---

## /platform/ — Правила инфраструктуры

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [caching.md](./platform/caching.md) | Redis: cache-aside, TTL, key naming ({service}:{entity}:{id}) | standard | ✅ | ✅ |
| [deployment.md](./platform/deployment.md) | Деплой: rolling update, blue-green, canary, автооткат | standard | ✅ | ✅ |
| [docker.md](./platform/docker.md) | Dockerfile best practices, docker-compose, образы, multi-stage | standard | ✅ | ✅ |
| **observability/** | Наблюдаемость (три столпа) ||||
| [alerting.md](./platform/observability/alerting.md) | Алертинг: severity levels, routing, связь с runbooks | standard | ✅ | ✅ |
| [logging.md](./platform/observability/logging.md) | Централизованные логи: Loki, корреляция с request_id | standard | ✅ | ✅ |
| [metrics.md](./platform/observability/metrics.md) | Prometheus метрики: naming, labels, типы (counter, gauge, histogram) | standard | ✅ | ✅ |
| [overview.md](./platform/observability/overview.md) | Обзор: logs (Loki), metrics (Prometheus), traces (Tempo) | standard | ✅ | ✅ |
| [tracing.md](./platform/observability/tracing.md) | Distributed tracing: OpenTelemetry, span, W3C traceparent | standard | ✅ | ✅ |
| [operations.md](./platform/operations.md) | Операции: runbooks, incidents, postmortems | standard | ✅ | ✅ |
| [security.md](./platform/security.md) | Безопасность: Dependabot, GitLeaks, Semgrep, scanning в CI | standard | ✅ | ✅ |

---

## /shared/ — Правила общего кода

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [scope.md](./shared/scope.md) | **Определение scope (claude/project)** — SSOT для test-*/doc-* скиллов | standard | ✅ | ✅ |
| [assets.md](./shared/assets.md) | Статические ресурсы: иконки, шрифты, брендинг | project | ✅ | ✅ |
| [contracts.md](./shared/contracts.md) | API контракты: OpenAPI, Protobuf, JSON Schema | standard | ✅ | ✅ |
| [events.md](./shared/events.md) | События: naming ({service}.{entity}.{action}), идемпотентность, DLQ | standard | ✅ | ✅ |
| [i18n.md](./shared/i18n.md) | Локализация: формат ключей, структура /shared/i18n/{locale}/ | standard | ✅ | ✅ |
| [libs.md](./shared/libs.md) | Общие библиотеки: errors, logging, validation | project | ✅ | ✅ |

---

## /skills/ — Правила скиллов

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [rules.md](./skills/rules.md) | Правило одного действия, форматы названий, allowed-tools, категории | standard | ✅ | ✅ |
| [parameters.md](./skills/parameters.md) | Стандартные параметры (--dry-run, --auto, --json, --verbose) | standard | ✅ | ✅ |
| [workflow.md](./skills/workflow.md) | Шаблоны воркфлоу, структура шагов, fail-fast проверки | standard | ✅ | ✅ |
| [errors.md](./skills/errors.md) | Коды ошибок, паттерны обработки, откат изменений | standard | ✅ | ✅ |
| [output.md](./skills/output.md) | Форматы вывода, иконки, JSON формат | standard | ✅ | ✅ |
| [state.md](./skills/state.md) | Временные файлы (.claude/state/), кэш, логи | standard | ✅ | ✅ |

---

## /specs/ — Правила спецификаций

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [README.md](./specs/README.md) | Индекс инструкций /specs/, структура, связи | standard | ✅ | ✅ |
| [statuses.md](./specs/statuses.md) | Унифицированная система статусов документов | standard | ✅ | ✅ |
| [workflow.md](./specs/workflow.md) | Полный workflow от идеи до реализации | standard | ✅ | ✅ |
| [discussions.md](./specs/discussions.md) | Формат и чек-листы для дискуссий | standard | ✅ | ✅ |
| [impact.md](./specs/impact.md) | Импакт-анализ, связь с ADR | standard | ✅ | ✅ |
| [adr.md](./specs/adr.md) | ADR, проверка бизнес-логики, breaking changes | standard | ✅ | ✅ |
| [plans.md](./specs/plans.md) | Планы реализации, GitHub Issues | standard | ✅ | ✅ |
| [architecture.md](./specs/architecture.md) | Архитектура сервиса (живой документ) | standard | ✅ | ✅ |
| [glossary.md](./specs/glossary.md) | Глоссарий терминов проекта | standard | ✅ | ✅ |
| [rules.md](./specs/rules.md) | Скиллы, шаблоны, запреты | standard | ✅ | ✅ |

---

## /src/ — Правила разработки сервисов

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| **api/** | Проектирование REST API ||||
| [deprecation.md](./src/api/deprecation.md) | Вывод API: Sunset header, Deprecation header, сроки, migration guide | standard | ✅ | ✅ |
| [design.md](./src/api/design.md) | URL naming (kebab-case), HTTP методы, статус-коды, partial update, bulk operations | standard | ✅ | ✅ |
| [swagger.md](./src/api/swagger.md) | OpenAPI спецификация, Swagger UI на /docs, автогенерация | standard | ✅ | ✅ |
| [versioning.md](./src/api/versioning.md) | Версионирование API через URL (/v1/, /v2/), gRPC package versioning | standard | ✅ | ✅ |
| **data/** | Форматы данных ||||
| [errors.md](./src/data/errors.md) | Единый формат ошибок: {error: {code, message, details, request_id}} | standard | ✅ | ✅ |
| [logging.md](./src/data/logging.md) | Structured JSON logging: timestamp, level, service, request_id, message | standard | ✅ | ✅ |
| [pagination.md](./src/data/pagination.md) | Формат пагинации: {data, pagination: {page, limit, total, total_pages}} | standard | ✅ | ✅ |
| [validation.md](./src/data/validation.md) | Валидация входных данных, формат ошибок по полям, JSON Schema | standard | ✅ | ✅ |
| **dev/** | Разработка ||||
| [local.md](./src/dev/local.md) | Локальная разработка: make dev, hot reload, debug порты, IDE | project | ✅ | ✅ |
| [performance.md](./src/dev/performance.md) | Профилирование, бенчмарки, лимиты: p99 < 200ms, память < 512MB | standard | ✅ | ✅ |
| [testing.md](./src/dev/testing.md) | Unit и integration тесты, моки, покрытие, расположение тестов | standard | ✅ | ✅ |
| **runtime/** | Поведение сервисов в runtime ||||
| [database.md](./src/runtime/database.md) | Connection pooling, миграции, транзакции, saga pattern, snake_case | standard | ✅ | ✅ |
| [health.md](./src/runtime/health.md) | Health checks: /health, /ready, graceful shutdown (SIGTERM, 30s) | standard | ✅ | ✅ |
| [realtime.md](./src/runtime/realtime.md) | Real-time: polling vs SSE vs WebSocket, когда что использовать | standard | ✅ | ✅ |
| [resilience.md](./src/runtime/resilience.md) | Устойчивость: таймауты, повторы (retry), circuit breaker, fallbacks | standard | ✅ | ✅ |
| **security/** | Безопасность ||||
| [audit.md](./src/security/audit.md) | Аудит-логи (кто/что/когда), PII, GDPR, data retention | standard | ✅ | ✅ |
| [auth.md](./src/security/auth.md) | Аутентификация между сервисами: JWT, service accounts | standard | ✅ | ✅ |

---

## /tests/ — Правила тестирования

| Инструкция | Описание | Тип | Создано | Заполнено |
|------------|----------|-----|:-------:|:---------:|
| [formats.md](./tests/formats.md) | **Форматы тестов: статусы, типы, шаблоны** | standard | ✅ | ✅ |
| [claude-testing.md](./tests/claude-testing.md) | Тестирование Claude Code: smoke tests, скиллы, инструкции | standard | ✅ | ✅ |
| [claude-functional.md](./tests/claude-functional.md) | Функциональное тестирование скиллов Claude | standard | ✅ | ✅ |
| [e2e.md](./tests/e2e.md) | End-to-end тесты: сценарии пользователя, инструменты | standard | ✅ | ✅ |
| [fixtures.md](./tests/fixtures.md) | Тестовые данные: фикстуры, фабрики, seeds | standard | ✅ | ✅ |
| [integration.md](./tests/integration.md) | Интеграционные тесты: БД, API, сервисы | standard | ✅ | ✅ |
| [load.md](./tests/load.md) | Нагрузочные тесты: k6, пороги производительности | standard | ✅ | ✅ |
| [project-testing.md](./tests/project-testing.md) | Тестирование проекта (индекс, unit, e2e, load) | project | ✅ | ✅ |
| [smoke.md](./tests/smoke.md) | Smoke-тесты: быстрая проверка работоспособности | standard | ✅ | ✅ |
| [unit.md](./tests/unit.md) | Unit-тесты: изоляция, моки, покрытие | standard | ✅ | ✅ |

---
