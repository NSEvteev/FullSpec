# Новая структура проекта

## Введение

**Цель:** Реорганизация `/.claude/instructions/` для чёткого разделения ответственности по scope.

**Проблема текущей структуры:**
- `services/`, `src/`, `platform/`, `tests/` существуют на одном уровне, хотя логически связаны
- Нет чёткого разделения "что относится к сервису" vs "что относится к системе"
- `git/` и `issues/` смешивают процессы и инструменты

**Решение:** 4 раздела по scope:

| Раздел | Scope | Описание |
|--------|-------|----------|
| `service/` | Один сервис | Разработка внутри `/src/{service}/` |
| `system/` | Вся система | Общая инфраструктура, тесты, конфиги |
| `workflow/` | Процессы | Git, GitHub, спецификации, документация |
| `meta/` | Claude | Правила для инструкций, скиллов, агентов |

**Связанные документы:**
- [migration_plan.md](./migration_plan.md) — план миграции и что меняется

---

## 1. Структура инструкций

```
/.claude/instructions/
│
├── service/                     # Разработка внутри сервиса (scope = service)
│   ├── *.md                     #   Управление сервисом: lifecycle, structure, dependencies
│   ├── api/
│   │   └── *.md                 #   Проектирование API: design, versioning, deprecation
│   ├── data/
│   │   └── *.md                 #   Форматы данных: errors, logging, validation, pagination
│   ├── database/
│   │   └── *.md                 #   База данных: schema, migrations, transactions, pooling
│   ├── health/
│   │   └── *.md                 #   Health checks: /health, /ready, graceful shutdown
│   ├── resilience/
│   │   └── *.md                 #   Устойчивость: timeouts, retries, circuit breaker
│   ├── security/
│   │   └── *.md                 #   Безопасность: auth, audit
│   ├── testing/
│   │   └── *.md                 #   Тестирование сервиса: unit, integration
│   └── frontend/
│       └── *.md                 #   Клиентский код (опционально)
│
├── system/                      # Общее для всей системы (scope = system)
│   ├── platform/
│   │   ├── *.md                 #   Инфраструктура: docker, deployment, operations
│   │   └── observability/
│   │       └── *.md             #   Наблюдаемость: logging, metrics, tracing, alerting
│   ├── tests/
│   │   └── *.md                 #   Системные тесты: e2e, load, smoke
│   ├── shared/
│   │   └── *.md                 #   Общий код: contracts, events, libs
│   └── config/
│       └── *.md                 #   Конфигурации: environments, feature-flags
│
├── workflow/                    # Процессы и документация
│   ├── git/                     #   ← ПРОЦЕССЫ (система контроля версий)
│   │   └── *.md                 #   Git процессы: commits, branches, review, merge
│   ├── github/                  #   ← ИНСТРУМЕНТ (платформа) → /.github/
│   │   ├── *.md                 #   GitHub платформа: actions, templates, CODEOWNERS
│   │   └── issues/
│   │       └── *.md             #   GitHub Issues: format, labels, workflow
│   ├── specs/
│   │   └── *.md                 #   Спецификации: discussions, impact, adr, plans
│   └── docs/
│       └── *.md                 #   Документация: structure, templates, rules
│
└── meta/                        # Мета-инструкции (правила для Claude-сущностей)
    ├── instructions/
    │   └── *.md                 #   Правила инструкций: types, validation, workflow
    ├── links/
    │   └── *.md                 #   Правила ссылок: format, patterns, validation
    ├── skills/
    │   └── *.md                 #   Правила скиллов: rules, parameters, errors
    ├── agents/
    │   └── *.md                 #   Правила агентов: structure, prompts, tools
    ├── scripts/
    │   └── *.md                 #   Правила скриптов: naming, structure, hooks
    └── state/
        └── *.md                 #   Правила состояний: format, lifecycle, cleanup
```

---

## 2. Структура папок проекта

```
/
├── src/                         # Исходный код сервисов (← service/)
│   └── {service}/
│       ├── *.md, *.yaml         #   Точка входа: README, Makefile, dependencies.yaml, .env.example
│       ├── backend/
│       │   ├── v*/              #   Версионированный API: handlers, routes, services
│       │   │   └── *.ts
│       │   ├── shared/
│       │   │   └── *.ts         #   Общий код между версиями: models, utils
│       │   └── health/
│       │       └── *.ts         #   Health endpoints: /health, /ready
│       ├── database/
│       │   ├── *.sql            #   Схема БД: schema.sql
│       │   └── migrations/
│       │       └── *.sql        #   Миграции: 001_init.sql, 002_add_users.sql
│       ├── frontend/
│       │   └── *.*              #   Клиентский код (опционально)
│       └── tests/
│           ├── unit/
│           │   └── *.test.ts    #   Unit тесты сервиса
│           └── integration/
│               └── *.test.ts    #   Integration тесты сервиса
│
├── platform/                    # Общая инфраструктура (← system/platform/)
│   ├── docker/
│   │   └── *.yml                #   Docker конфигурации: docker-compose.yml, docker-compose.dev.yml
│   ├── gateway/
│   │   └── *.*                  #   API Gateway: Traefik/Nginx конфиги
│   ├── monitoring/
│   │   ├── prometheus/
│   │   │   └── *.yml            #   Сбор метрик: prometheus.yml, alerts.yml
│   │   ├── grafana/
│   │   │   └── *.json           #   Дашборды: dashboards/*.json
│   │   └── loki/
│   │       └── *.yml            #   Сбор логов: loki-config.yml
│   ├── k8s/
│   │   └── *.yaml               #   Kubernetes манифесты: deployments, services
│   └── scripts/
│       └── *.sh                 #   Инфраструктурные скрипты: deploy.sh, backup.sh
│
├── tests/                       # Системные тесты (← system/tests/)
│   ├── e2e/
│   │   └── *.test.ts            #   End-to-end сценарии: user-flow.test.ts
│   ├── integration/
│   │   └── *.test.ts            #   Интеграция между сервисами: auth-users.test.ts
│   ├── load/
│   │   └── *.js                 #   Нагрузочные тесты (k6): load-test.js
│   ├── smoke/
│   │   └── *.test.ts            #   Smoke тесты: health-check.test.ts
│   └── fixtures/
│       └── *.json               #   Общие тестовые данные: users.json
│
├── shared/                      # Общий код между сервисами (← system/shared/)
│   ├── contracts/
│   │   ├── openapi/
│   │   │   └── *.yaml           #   REST контракты: auth.yaml, users.yaml
│   │   └── protobuf/
│   │       └── *.proto          #   gRPC контракты: auth.proto
│   ├── events/
│   │   └── *.json               #   Схемы событий: user.created.json
│   ├── libs/
│   │   └── *.*                  #   Общие библиотеки: errors, logging, validation
│   ├── assets/
│   │   └── *.*                  #   Статические ресурсы: иконки, шрифты
│   └── i18n/
│       └── *.json               #   Локализация: en.json, ru.json
│
├── config/                      # Конфигурации окружений (← system/config/)
│   ├── *.yaml                   #   Окружения: development.yaml, staging.yaml, production.yaml
│   └── feature-flags/
│       └── *.yaml               #   Feature flags: flags.yaml
│
├── specs/                       # Спецификации проекта (← workflow/specs/)
│   ├── discussions/
│   │   └── *.md                 #   Дискуссии: 001-new-feature.md
│   ├── impact/
│   │   └── *.md                 #   Импакт-анализ: 001-feature-impact.md
│   ├── services/
│   │   └── {service}/
│   │       ├── *.md             #   Описание сервиса: README.md, architecture.md
│   │       ├── adr/
│   │       │   └── *.md         #   Архитектурные решения: 001-initial.md
│   │       └── plans/
│   │           └── *.md         #   Планы реализации: feature-plan.md
│   └── glossary.md              #   Глоссарий терминов проекта
│
├── doc/                         # Документация проекта (← workflow/docs/)
│   ├── *.md                     #   Общая документация: README.md, glossary.md
│   ├── runbooks/
│   │   └── *.md                 #   Общие runbooks (system): database-full.md, high-load.md
│   ├── src/
│   │   └── {service}/
│   │       ├── *.md             #   Документация кода сервиса
│   │       └── runbooks/
│   │           └── *.md         #   Runbooks сервиса (service): token-issues.md
│   ├── shared/
│   │   └── *.md                 #   Документация общего кода
│   └── platform/
│       ├── *.md                 #   Документация инфраструктуры
│       └── runbooks/
│           └── *.md             #   Runbooks инфраструктуры (system): deploy.md, rollback.md
│
├── .github/                     # GitHub платформа (← workflow/github/) ⚠️ ТРЕБОВАНИЕ GITHUB
│   ├── workflows/               #   ⚠️ Путь фиксирован платформой
│   │   └── *.yml                #   CI/CD pipelines: ci.yml, deploy.yml
│   ├── ISSUE_TEMPLATE/          #   ⚠️ Путь фиксирован платформой
│   │   └── *.md                 #   Шаблоны Issues: bug.md, feature.md
│   ├── PULL_REQUEST_TEMPLATE.md #   Шаблон PR
│   └── CODEOWNERS               #   Владельцы кода
│
└── .claude/                     # Инструменты Claude (← meta/)
    ├── instructions/
    │   └── *.md                 #   Инструкции для LLM
    ├── skills/
    │   └── */SKILL.md           #   Скиллы: skill-create/, docs-update/
    ├── agents/
    │   └── *.md                 #   Агенты: researcher.md, coder.md
    ├── templates/
    │   └── *.*                  #   Шаблоны: specs/, docs/, git/
    ├── scripts/
    │   └── *.py                 #   Скрипты автоматизации: protect-specs.py, validate-deps.py
    └── state/
        └── *.json               #   Состояния агентов: agent-progress.json (не в git)
```

---

## 3. Маппинг: Инструкции → Папки проекта

| Инструкция | Папка проекта | Описание |
|------------|---------------|----------|
| **service/** | `/src/{service}/` | Разработка внутри сервиса |
| `service/api/` | `/src/{service}/backend/v*/` | Проектирование API |
| `service/data/` | `/src/{service}/backend/` | Форматы данных |
| `service/database/` | `/src/{service}/database/` | База данных |
| `service/health/` | `/src/{service}/backend/health/` | Health checks |
| `service/resilience/` | `/src/{service}/backend/` | Устойчивость |
| `service/security/` | `/src/{service}/backend/` | Безопасность сервиса |
| `service/testing/` | `/src/{service}/tests/` | Unit/integration тесты |
| `service/frontend/` | `/src/{service}/frontend/` | Клиентский код (опционально) |
| **system/** | — | Общее для всей системы |
| `system/platform/` | `/platform/` | Инфраструктура |
| `system/platform/observability/` | `/platform/monitoring/` | Наблюдаемость |
| `system/tests/` | `/tests/` | Системные тесты (e2e, load) |
| `system/shared/` | `/shared/` | Общий код |
| `system/config/` | `/config/` | Конфигурации окружений |
| **workflow/** | — | Процессы и документация |
| `workflow/git/` | — | Git процессы: commits, branches, review |
| `workflow/github/` | `/.github/` ⚠️ | GitHub платформа (путь фиксирован) |
| `workflow/github/issues/` | `/.github/ISSUE_TEMPLATE/` | GitHub Issues |
| `workflow/specs/` | `/specs/` | Спецификации (ADR, plans) |
| `workflow/docs/` | `/doc/` | Документация проекта |
| **meta/** | `/.claude/` | Правила для Claude-сущностей |
| `meta/instructions/` | `/.claude/instructions/` | Правила инструкций |
| `meta/skills/` | `/.claude/skills/` | Правила скиллов |
| `meta/agents/` | `/.claude/agents/` | Правила агентов |
| `meta/scripts/` | `/.claude/scripts/` | Правила скриптов |
| `meta/state/` | `/.claude/state/` | Правила состояний |
| `meta/links/` | — | Правила ссылок |

---

## 4. Диаграмма связей

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            ИНСТРУКЦИИ                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   service/           system/            workflow/          meta/         │
│   ┌────────┐        ┌──────────┐       ┌──────────┐      ┌───────┐      │
│   │ api    │        │ platform │       │ git      │←proc │ instr.│      │
│   │ data   │        │  observ. │       │ github   │←tool │ links │      │
│   │database│        │ tests    │       │  issues  │      │ skills│      │
│   │ health │        │ shared   │       │ specs    │      │ agents│      │
│   │ resil. │        │ config   │       │ docs     │      │scripts│      │
│   │ secur. │        │          │       │          │      │ state │      │
│   │ testing│        │          │       │          │      │       │      │
│   │frontend│        │          │       │          │      │       │      │
│   └───┬────┘        └────┬─────┘       └────┬─────┘      └───┬───┘      │
│       │                  │                  │                │           │
└───────┼──────────────────┼──────────────────┼────────────────┼───────────┘
        │                  │                  │                │
        ▼                  ▼                  ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                             ПРОЕКТ                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   /src/{service}/    /platform/         /specs/           /.claude/      │
│   ┌────────┐        ┌──────────┐       ┌──────────┐      ┌───────┐      │
│   │backend │        │ docker   │       │ discuss. │      │ instr.│      │
│   │  v1/v2 │        │ gateway  │       │ impact   │      │ skills│      │
│   │  health│        │ monitor. │       │ services │      │ agents│      │
│   │database│        ├──────────┤       ├──────────┤      │ templ.│      │
│   │tests   │        │ /tests/  │       │ /doc/    │      │scripts│      │
│   └────────┘        │ /shared/ │       ├──────────┤      │ state │      │
│                     │ /config/ │       │ /.github/│⚠️    └───────┘      │
│                     └──────────┘       └──────────┘                      │
│                                                                          │
│   ⚠️ /.github/ — путь фиксирован платформой GitHub                       │
│   ←proc = ПРОЦЕССЫ, ←tool = ИНСТРУМЕНТ                                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Жизненный цикл сервиса: покрытие инструкциями

| Этап | Что происходит | Инструкции |
|------|----------------|------------|
| **1. Идея** | Обсуждение, формулировка | `workflow/specs/` (discussions) |
| **2. Анализ** | Импакт, зависимости | `workflow/specs/` (impact) |
| **3. Проектирование** | Архитектура, ADR | `workflow/specs/` (adr, architecture) |
| **4. Планирование** | План, задачи | `workflow/specs/` (plans) + `workflow/github/issues/` |
| **5. Создание** | Scaffold сервиса | `service/` (lifecycle, structure) |
| **6. Разработка** | Код, API, БД | `service/` (api, data, database, health, resilience, security) |
| **7. Тестирование** | Unit, integration, e2e | `service/testing/` + `system/tests/` |
| **8. Документация** | API docs, README | `workflow/docs/` |
| **9. Code Review** | PR, review | `workflow/git/` (review) |
| **10. CI/CD** | Сборка, деплой | `workflow/github/` (actions) + `system/platform/` |
| **11. Мониторинг** | Логи, метрики, трейсы | `system/platform/observability/` |
| **12. Алертинг** | Уведомления | `system/platform/observability/` (alerting) |
| **13. Поддержка** | Runbooks, инциденты | `workflow/docs/` (runbooks) + `system/platform/` (operations) |
| **14. Обновление** | Новые версии API | `service/api/` (versioning, deprecation) |
| **15. Удаление** | Вывод из эксплуатации | `service/` (lifecycle) |

