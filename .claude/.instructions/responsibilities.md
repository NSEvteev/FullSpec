# Зоны ответственности инструкций

IN и границы для всех инструкций проекта.

> **Правила:** [/.claude/.instructions/.structure/responsibilities.md](/.claude/.instructions/.structure/responsibilities.md) — формат IN/Границы, как определять ответственность
> **Папки проекта:** [/.structure/responsibilities.md](/.structure/responsibilities.md) — зоны ответственности папок проекта

---

## Оглавление

| Секция | Строка |
|--------|--------|
| [.structure/](#structure--правила-организации-структуры) | 29 |
| [src/](#src--разработка-сервисов) | 65 |
| [platform/](#platform--инфраструктура) | 179 |
| [tests/](#tests--системные-тесты) | 213 |
| [shared/](#shared--общий-код) | 227 |
| [config/](#config--конфигурации) | 251 |
| [specs/](#specs--спецификации) | 265 |
| [.github/](#github--github-платформа) | 279 |
| [.claude/](#claude--правила-и-claude-сущности) | 303 |

---

## .structure/ — Правила организации структуры

**SSOT:** `/.structure/` — фактическая структура (project.md, mapping.md, responsibilities.md)

---

### lifecycle.md

**IN:** Этапы жизненного цикла проекта, покрытие инструкциями на каждом этапе, матрица "этап -> инструкции"

**Границы:**
- какие этапы существуют -> здесь
- детальное описание каждого этапа -> соответствующие инструкции

---

### responsibilities.md

**IN:** IN/Границы для всех инструкций и папок проекта, SSOT зон ответственности

**Границы:**
- что куда класть (IN) -> здесь
- как это реализовать (правила) -> соответствующие инструкции

---

### examples.md

**IN:** Примеры "Куда положить файл?", "Где написать код?", типичные кейсы выбора папки

**Границы:**
- примеры маршрутизации -> здесь
- шаблоны файлов -> /.claude/templates/

---

## src/ — Разработка сервисов

---

### src/

**IN:** lifecycle.md, structure.md, dependencies.md — правила структуры сервисов, зависимости

**Границы:**
- правила для кода сервисов -> здесь
- общие библиотеки между сервисами -> shared/

---

### src/api/

**IN:** design.md, versioning.md, deprecation.md, realtime.md — правила проектирования API

**Границы:**
- как проектировать API -> здесь
- OpenAPI/Proto контракты -> shared/contracts/

---

### src/data/

**IN:** errors.md, logging.md, validation.md, pagination.md — правила работы с данными

**Границы:**
- форматы ошибок, логов, валидации -> здесь
- схемы событий для всех сервисов -> shared/events/

---

### src/database/

**IN:** schema.md, migrations.md, transactions.md, pooling.md — правила работы с БД

**Границы:**
- схемы и миграции сервиса -> здесь
- общие схемы платформы -> platform/

---

### src/dev/

**IN:** local.md, hot-reload.md, performance.md — локальная разработка и отладка

**Границы:**
- настройка локального окружения -> здесь
- CI/CD пайплайны -> .github/workflows/

---

### src/health/

**IN:** health.md, ready.md, graceful-shutdown.md — правила health checks

**Границы:**
- /health, /ready эндпоинты -> здесь
- alerting на основе health -> platform/observability/

---

### src/resilience/

**IN:** timeouts.md, retries.md, circuit-breaker.md — правила отказоустойчивости кода

**Границы:**
- паттерны в коде сервиса -> здесь
- инфраструктурная отказоустойчивость -> platform/

---

### src/security/

**IN:** auth.md, authorization.md, audit.md — правила безопасности в коде

**Границы:**
- аутентификация, авторизация в сервисе -> здесь
- управление секретами, vault -> platform/

---

### src/testing/

**IN:** unit.md, integration.md — правила тестирования внутри сервиса

**Границы:**
- unit/integration тесты сервиса -> здесь
- E2E, load тесты системы -> tests/

---

### src/frontend/

**IN:** ui.md, state.md, routing.md — правила фронтенд-разработки

**Границы:**
- UI компоненты сервиса -> здесь
- общие assets (иконки, шрифты) -> shared/assets/

---

### src/docs/

**IN:** api-docs.md, guides.md, runbooks.md — правила документации сервиса

**Границы:**
- документация конкретного сервиса -> здесь
- архитектурные решения -> specs/

---

## platform/ — Инфраструктура

---

### platform/

**IN:** docker.md, deployment.md, operations.md — правила инфраструктуры

**Границы:**
- конфигурации инфраструктуры -> здесь
- бизнес-код сервисов -> src/

---

### platform/observability/

**IN:** logging.md, metrics.md, tracing.md, alerting.md — правила observability

**Границы:**
- настройки мониторинга, алертов -> здесь
- код логирования в сервисах -> src/data/

---

### platform/docs/

**IN:** docs.md, runbooks.md — документация операций

**Границы:**
- операционная документация платформы -> здесь
- документация сервисов -> src/docs/

---

## tests/ — Системные тесты

---

### tests/

**IN:** e2e.md, load.md, smoke.md, integration.md — правила системных тестов

**Границы:**
- тесты между сервисами, E2E -> здесь
- unit тесты внутри сервиса -> src/testing/

---

## shared/ — Общий код

---

### shared/

**IN:** contracts.md, events.md, libs.md, assets.md, i18n.md — правила общего кода

**Границы:**
- код, используемый несколькими сервисами -> здесь
- код конкретного сервиса -> src/

---

### shared/docs/

**IN:** документация контрактов, событий, библиотек

**Границы:**
- документация shared/ модулей -> здесь
- документация сервисов -> src/docs/

---

## config/ — Конфигурации

---

### config/

**IN:** environments.md, feature-flags.md — правила конфигураций

**Границы:**
- конфигурации окружений -> здесь
- .env файлы сервиса -> src/{service}/

---

## specs/ — Спецификации

---

### specs/

**IN:** discussions.md, impact.md, adr.md, plans.md, architecture.md — правила спецификаций

**Границы:**
- архитектурные решения, планы -> здесь
- документация кода -> */docs/

---

## .github/ — GitHub платформа

---

### .github/

**IN:** actions.md, workflows.md, templates.md, CODEOWNERS.md — правила GitHub

**Границы:**
- CI/CD, шаблоны GitHub -> здесь
- git правила (коммиты, ветки) -> .github/git/

---

### .github/issues/

**IN:** format.md, labels.md, workflow.md, commands.md — правила работы с Issues

**Границы:**
- формат и workflow Issues -> здесь
- спецификации фич -> specs/

---

## .claude/ — Правила и Claude-сущности

---

### .github/git/

**IN:** commits.md, branches.md, review.md, merge.md — правила Git

**Границы:**
- правила коммитов, веток, ревью -> здесь
- GitHub Actions -> .github/workflows/

---

### .claude/.instructions/

**IN:** types.md, validation.md, workflow.md, relations.md — правила инструкций

**Границы:**
- мета-правила для инструкций -> здесь
- содержимое конкретных инструкций -> соответствующие файлы

---

### .structure/links/

**IN:** format.md, patterns.md, validation.md — правила ссылок

**Границы:**
- форматы и паттерны ссылок -> здесь
- конкретные ссылки в файлах -> сами файлы

---

### .claude/skills/

**IN:** rules.md, parameters.md, errors.md, state.md — правила скиллов

**Границы:**
- как писать скиллы -> здесь
- код конкретных скиллов -> /.claude/skills/{skill}/

---

### .claude/agents/

**IN:** structure.md, prompts.md, tools.md — правила агентов

**Границы:**
- как писать агентов -> здесь
- код конкретных агентов -> /.claude/agents/{agent}.md

---

### .claude/scripts/

**IN:** naming.md, structure.md, hooks.md — правила скриптов

**Границы:**
- как писать скрипты -> здесь
- код конкретных скриптов -> /.claude/scripts/{script}.py

---

### .claude/state/

**IN:** format.md, lifecycle.md, cleanup.md — правила состояний

**Границы:**
- формат файлов состояний -> здесь
- сами файлы состояний -> /.claude/state/{state}.json

---

### .claude/drafts/

**IN:** naming.md, lifecycle.md, cleanup.md — правила черновиков

**Границы:**
- формат и жизненный цикл черновиков -> здесь
- сами черновики -> /.claude/drafts/{draft}.md
