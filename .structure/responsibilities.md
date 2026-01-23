# Зоны ответственности папок проекта (SSOT)

Фактические IN и границы для папок проекта.

> **Правила:** [/.claude/.instructions/.structure/responsibilities.md](/.claude/.instructions/.structure/responsibilities.md) — формат IN/Границы, как определять ответственность
> **Инструкции:** [/.claude/.instructions/responsibilities.md](/.claude/.instructions/responsibilities.md) — зоны ответственности инструкций

---

## Оглавление

| Секция | Строка |
|--------|--------|
| [Корневые файлы](#корневые-файлы) | 27 |
| [/src/](#src--исходный-код-сервисов) | 67 |
| [/platform/](#platform--общая-инфраструктура) | 171 |
| [/tests/](#tests--системные-тесты) | 285 |
| [/shared/](#shared--общий-код-между-сервисами) | 349 |
| [/config/](#config--конфигурации-окружений) | 443 |
| [/specs/](#specs--спецификации-проекта) | 477 |
| [/.github/](#github--github-платформа) | 561 |
| [/.claude/](#claude--инструменты-claude) | 615 |

---

## Корневые файлы

---

### README.md

**IN:** Описание проекта, quick start, структура, ссылки на ключевые файлы, badges

**Границы:**
- обзор проекта, как начать -> здесь
- детальная документация -> */docs/

---

### CLAUDE.md

**IN:** Ссылки на инструкции, статус проекта, правила навигации, граф зависимостей скиллов

**Границы:**
- навигация для Claude -> здесь
- содержимое инструкций -> /.claude/.instructions/

---

### Makefile

**IN:** make help, dev, test, lint, build — команды разработки

**Границы:**
- команды локальной разработки -> здесь
- скрипты деплоя -> /platform/scripts/

---

### .gitignore

**IN:** Паттерны игнорирования для git: __pycache__, node_modules, .env, *.log

---

## /src/ — Исходный код сервисов

> **Инструкция:** [/.claude/.instructions/src/](/.claude/.instructions/src/)

---

### /src/

**IN:** Папки сервисов (auth/, notify/, pay/), каждая — независимый сервис

**Границы:**
- код конкретного сервиса -> здесь
- общий код между сервисами -> /shared/

---

### /src/{service}/

**IN:** README.md, Makefile, .env.example, requirements.txt/package.json, docs/, backend/, frontend/, database/, tests/

**Границы:**
- всё для работы сервиса -> здесь
- спецификации и ADR -> /specs/services/{service}/

---

### /src/{service}/docs/

**IN:** API docs, guides, runbooks сервиса, CHANGELOG.md

**Границы:**
- документация конкретного сервиса -> здесь
- архитектурные решения -> /specs/services/{service}/adr/

---

### /src/{service}/backend/

**IN:** handlers/, routes/, services/, models/, utils/, main.py

**Границы:**
- бизнес-логика сервиса -> здесь
- миграции БД -> database/

---

### /src/{service}/backend/v*/

**IN:** Версионированные handlers, routes (v1/, v2/)

**Границы:**
- версионированный API код -> здесь
- общий код между версиями -> backend/shared/

---

### /src/{service}/backend/shared/

**IN:** models, utils, middleware общие для версий API одного сервиса

**Границы:**
- код между версиями API сервиса -> здесь
- библиотеки для всей системы -> /shared/libs/

---

### /src/{service}/backend/health/

**IN:** health.py, ready.py — handlers для /health, /ready

**Границы:**
- health check эндпоинты -> здесь
- бизнес-логика сервиса -> services/

---

### /src/{service}/database/

**IN:** schema.sql, migrations/, seeds/

**Границы:**
- схема и миграции сервиса -> здесь
- общие схемы для контрактов -> /shared/contracts/

---

### /src/{service}/frontend/

**IN:** components/, pages/, state/, hooks/, assets/

**Границы:**
- UI сервиса -> здесь
- общие assets (иконки, шрифты) -> /shared/assets/

---

### /src/{service}/tests/

**IN:** unit/, integration/ — тесты внутри сервиса, conftest.py, fixtures/

**Границы:**
- тесты внутри сервиса -> здесь
- E2E тесты между сервисами -> /tests/

---

## /platform/ — Общая инфраструктура

> **Инструкция:** [/.claude/.instructions/platform/](/.claude/.instructions/platform/)

---

### /platform/

**IN:** docker/, gateway/, monitoring/, k8s/, scripts/, docs/, runbooks/

**Границы:**
- инфраструктура системы -> здесь
- бизнес-код сервисов -> /src/

---

### /platform/docker/

**IN:** docker-compose.yml, docker-compose.override.yml, Dockerfile.base, Dockerfile.{service}

**Границы:**
- общие Docker конфигурации -> здесь
- конфиги внутри сервиса -> /src/{service}/

---

### /platform/gateway/

**IN:** traefik.yml, nginx.conf, routing rules, SSL certificates

**Границы:**
- reverse proxy, routing -> здесь
- бизнес-логика -> /src/

---

### /platform/monitoring/

**IN:** prometheus/, grafana/, loki/, alertmanager/

**Границы:**
- настройки мониторинга -> здесь
- код логирования в сервисах -> /src/

---

### /platform/monitoring/prometheus/

**IN:** prometheus.yml, alerts.yml, rules/*.yml

**Границы:**
- сбор метрик, алерты -> здесь
- визуализация -> grafana/

---

### /platform/monitoring/grafana/

**IN:** dashboards/*.json, provisioning/, datasources.yml

**Границы:**
- дашборды, визуализация -> здесь
- правила алертов -> prometheus/

---

### /platform/monitoring/loki/

**IN:** loki-config.yml, promtail.yml

**Границы:**
- агрегация логов -> здесь
- код логирования -> /src/

---

### /platform/k8s/

**IN:** deployments/, services/, ingress/, configmaps/, secrets/, namespaces/

**Границы:**
- Kubernetes манифесты -> здесь
- Docker compose для локальной разработки -> docker/

---

### /platform/scripts/

**IN:** deploy.sh, backup.sh, restore.sh, migrate.sh, rollback.sh

**Границы:**
- инфраструктурные скрипты -> здесь
- скрипты Claude -> /.claude/scripts/

---

### /platform/docs/

**IN:** architecture.md, infrastructure.md, disaster-recovery.md

**Границы:**
- документация платформы -> здесь
- документация сервисов -> /src/{service}/docs/

---

### /platform/runbooks/

**IN:** deploy.md, rollback.md, database-full.md, incident-response.md

**Границы:**
- операционные runbooks -> здесь
- runbooks сервисов -> /src/{service}/docs/

---

## /tests/ — Системные тесты

> **Инструкция:** [/.claude/.instructions/tests/](/.claude/.instructions/tests/)

---

### /tests/

**IN:** e2e/, integration/, load/, smoke/, fixtures/, conftest.py, pytest.ini

**Границы:**
- системные тесты -> здесь
- unit тесты сервиса -> /src/{service}/tests/

---

### /tests/e2e/

**IN:** User flows, сценарии через UI/API, test_checkout_flow.py

**Границы:**
- end-to-end сценарии -> здесь
- unit тесты -> /src/{service}/tests/unit/

---

### /tests/integration/

**IN:** Тесты между сервисами, test_auth_notify.py, test_pay_notify.py

**Границы:**
- интеграция между сервисами -> здесь
- интеграция внутри сервиса -> /src/{service}/tests/integration/

---

### /tests/load/

**IN:** k6 скрипты, сценарии нагрузки, load_test.js, stress_test.js

**Границы:**
- нагрузочное тестирование -> здесь
- функциональные тесты -> e2e/

---

### /tests/smoke/

**IN:** Health checks, базовая работоспособность, test_all_services_up.py

**Границы:**
- быстрая проверка системы -> здесь
- детальные тесты -> e2e/, integration/

---

### /tests/fixtures/

**IN:** users.json, products.json, orders.json — общие тестовые данные

**Границы:**
- fixtures для системных тестов -> здесь
- fixtures для тестов сервиса -> /src/{service}/tests/fixtures/

---

## /shared/ — Общий код между сервисами

> **Инструкция:** [/.claude/.instructions/shared/](/.claude/.instructions/shared/)

---

### /shared/

**IN:** contracts/, events/, libs/, assets/, i18n/, docs/

**Границы:**
- код для нескольких сервисов -> здесь
- код конкретного сервиса -> /src/{service}/

---

### /shared/contracts/

**IN:** openapi/, protobuf/, json-schema/

**Границы:**
- API контракты -> здесь
- реализация handlers -> /src/

---

### /shared/contracts/openapi/

**IN:** auth.yaml, users.yaml, orders.yaml — OpenAPI спецификации

**Границы:**
- REST API контракты -> здесь
- gRPC контракты -> protobuf/

---

### /shared/contracts/protobuf/

**IN:** auth.proto, users.proto, orders.proto — Protocol Buffers

**Границы:**
- gRPC контракты -> здесь
- REST контракты -> openapi/

---

### /shared/events/

**IN:** user.created.json, order.placed.json — схемы событий

**Границы:**
- схемы событий -> здесь
- код publishers/subscribers -> /src/

---

### /shared/libs/

**IN:** errors/, logging/, validation/, http-client/, utils/

**Границы:**
- утилиты для всех сервисов -> здесь
- бизнес-логика -> /src/

---

### /shared/assets/

**IN:** icons/, fonts/, images/ — общие статические ресурсы

**Границы:**
- общие assets -> здесь
- assets сервиса -> /src/{service}/frontend/assets/

---

### /shared/i18n/

**IN:** en.json, ru.json, de.json — переводы

**Границы:**
- файлы переводов -> здесь
- текст в коде -> /src/

---

### /shared/docs/

**IN:** contracts.md, events.md, libs.md — документация shared

**Границы:**
- документация общего кода -> здесь
- документация сервисов -> /src/{service}/docs/

---

## /config/ — Конфигурации окружений

> **Инструкция:** [/.claude/.instructions/config/](/.claude/.instructions/config/)

---

### /config/

**IN:** *.yaml (development, staging, production), feature-flags/

**Границы:**
- общие конфигурации окружений -> здесь
- .env файлы сервиса -> /src/{service}/

---

### /config/*.yaml

**IN:** development.yaml, staging.yaml, production.yaml — конфиги окружений

**Границы:**
- не-секретные конфигурации -> здесь
- секреты -> vault / env vars

---

### /config/feature-flags/

**IN:** flags.yaml, rollout.yaml — feature flags

**Границы:**
- конфигурация флагов -> здесь
- логика применения флагов -> /src/

---

## /specs/ — Спецификации проекта

> **Инструкция:** [/.claude/.instructions/specs/](/.claude/.instructions/specs/)

---

### /specs/

**IN:** discussions/, impact/, services/, glossary.md, README.md

**Границы:**
- архитектура, планы, решения -> здесь
- документация кода -> */docs/

---

### /specs/discussions/

**IN:** Обсуждения фич, идеи, proposals — DISC-*.md

**Границы:**
- обсуждение идей -> здесь
- принятые решения -> services/{service}/adr/

---

### /specs/impact/

**IN:** Анализ влияния изменений — IMPACT-*.md

**Границы:**
- анализ влияния -> здесь
- планы реализации -> services/{service}/plans/

---

### /specs/services/

**IN:** Папки по сервисам: auth/, notify/, pay/

**Границы:**
- спецификации сервисов -> здесь
- код сервисов -> /src/

---

### /specs/services/{service}/

**IN:** README.md, architecture.md, adr/, plans/

**Границы:**
- архитектура сервиса -> здесь
- код сервиса -> /src/{service}/

---

### /specs/services/{service}/adr/

**IN:** ADR-*.md — архитектурные решения

**Границы:**
- принятые решения -> здесь
- обсуждения -> /specs/discussions/

---

### /specs/services/{service}/plans/

**IN:** Roadmap, feature plans — PLAN-*.md

**Границы:**
- планы реализации -> здесь
- задачи -> GitHub Issues

---

### /specs/glossary.md

**IN:** Термины проекта, определения, аббревиатуры

**Границы:**
- определения терминов -> здесь
- документация API -> */docs/

---

## /.github/ — GitHub платформа

> **Инструкция:** [/.claude/.instructions/.github/](/.claude/.instructions/.github/)

---

### /.github/

**IN:** workflows/, ISSUE_TEMPLATE/, PULL_REQUEST_TEMPLATE.md, CODEOWNERS

**Границы:**
- GitHub конфигурации -> здесь
- код проекта -> /src/

---

### /.github/workflows/

**IN:** ci.yml, deploy.yml, release.yml, codeql.yml

**Границы:**
- CI/CD пайплайны -> здесь
- скрипты деплоя -> /platform/scripts/

---

### /.github/ISSUE_TEMPLATE/

**IN:** bug.md, feature.md, task.md — шаблоны Issues

**Границы:**
- шаблоны для GitHub Issues -> здесь
- спецификации -> /specs/

---

### /.github/PULL_REQUEST_TEMPLATE.md

**IN:** Чек-лист для PR, секции (Summary, Testing, Checklist)

**Границы:**
- шаблон PR -> здесь
- правила ревью -> инструкции

---

### /.github/CODEOWNERS

**IN:** Mapping путей -> reviewers (@team/backend, @team/frontend)

**Границы:**
- кто ревьюит какие файлы -> здесь
- процессы ревью -> инструкции

---

## /.claude/ — Инструменты Claude

> **Инструкция:** [/.claude/.instructions/.claude/](/.claude/.instructions/.claude/)

---

### /.claude/

**IN:** .instructions/, skills/, agents/, templates/, scripts/, state/, drafts/, settings.json, settings.local.json

**Границы:**
- инструменты Claude -> здесь
- код проекта -> /src/

---

### /.claude/.instructions/

**IN:** Правила для LLM, зеркальная структура проекта (src/, platform/, tests/, etc.)

**Границы:**
- правила "как делать" -> здесь
- документация "что есть" -> */docs/

---

### /.claude/skills/

**IN:** {skill}/SKILL.md, {skill}/tests/ — скиллы Claude

**Границы:**
- скиллы (автоматизация задач) -> здесь
- инструкции (правила) -> .instructions/

---

### /.claude/agents/

**IN:** {agent}.md — определения агентов

**Границы:**
- агенты (сложные workflow) -> здесь
- скиллы (атомарные задачи) -> skills/

---

### /.claude/templates/

**IN:** specs/, git/, platform/, doc/, tests/ — шаблоны для артефактов

**Границы:**
- шаблоны (заготовки) -> здесь
- готовые файлы -> соответствующие папки

---

### /.claude/scripts/

**IN:** *.py — Python скрипты автоматизации, hooks

**Границы:**
- скрипты Claude -> здесь
- инфра-скрипты -> /platform/scripts/

---

### /.claude/state/

**IN:** *.json — файлы состояний агентов (не в git)

**Границы:**
- runtime состояния -> здесь
- конфигурации -> /config/

---

### /.claude/drafts/

**IN:** *.md — планы, заметки, SSOT-документы (в git)

**Границы:**
- рабочие черновики -> здесь
- финальные спецификации -> /specs/

---

### /.claude/settings.json

**IN:** Конфигурация Claude Code (permissions, paths) — в git

**Границы:**
- настройки Claude -> здесь
- секреты -> env vars

---

### /.claude/settings.local.json

**IN:** Персональные настройки (не в git)

**Границы:**
- личные настройки разработчика -> здесь
- общие настройки команды -> settings.json
