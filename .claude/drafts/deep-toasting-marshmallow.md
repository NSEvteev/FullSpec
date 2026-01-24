# План: Создание инструкций для всех папок проекта

> **TODO (24.01.2026):** Начать выполнение этого плана. Добавить напоминание в CLAUDE.md.

## Критичное знание

> **Инструкции = ТОЛЬКО стандарты (КАК делать)**
> Они НЕ описывают структуру папок — это делает README.

> **SSOT (Single Source of Truth):** Каждая инструкция должна быть единственным источником правды для своей области. Если инструкция использует что-то из проекта — ссылаться на источник SSOT, НЕ дублировать.

---

## Текущее состояние

| Область | Статус | Файлов |
|---------|--------|--------|
| `/.instructions/` | ГОТОВО | 15 |
| `/specs/.instructions/` | ГОТОВО | 17 |
| `/.claude/.instructions/` | ГОТОВО | 10 |
| `/src/`, `/platform/`, `/tests/`, `/shared/`, `/config/`, `/.github/` | TODO | 0 |

**Проблема:** `coverage.md` не включает саму `/.instructions/` — нужно исправить.

---

## Последовательность обработки

### Порядок (по зависимостям)

```
0. /.instructions/  → Обновить coverage.md + добавить SSOT в шаблон
1. /shared/         → Базовые контракты (используются везде)
2. /src/            → Исходный код (зависит от /shared/)
3. /tests/          → Тесты (зависит от /src/ и /shared/)
4. /config/         → Конфигурации (используется /src/ и /platform/)
5. /platform/       → Инфраструктура (зависит от /config/)
6. /.github/        → CI/CD (зависит от всего)
```

**Граф зависимостей:**
```
/shared/ → /src/ → /tests/
              ↑
         /config/ → /platform/ → /.github/
```

---

## Фаза 0: Обновление /.instructions/

**Задачи:**
1. Добавить `/.instructions/` в `coverage.md` (статус: ГОТОВО)
2. Добавить секцию SSOT в `template-instruction.md`

**Секция SSOT для шаблона:**
```markdown
---

## Источники правды (SSOT)

> Инструкция НЕ дублирует содержимое SSOT, только ссылается.

| Что | Путь | Описание |
|-----|------|----------|
| {Название} | `{путь}` | {когда использовать} |

**Внешние стандарты:**
- [{Стандарт}]({url}) — {описание}
```

---

## Фаза 1: /shared/.instructions/

**Зона ответственности:** contracts, events, libs, assets, i18n

| Файл | Описание | SSOT |
|------|----------|------|
| `README.md` | Индекс | — |
| `contracts.md` | Проектирование API контрактов | `/shared/contracts/`, OpenAPI 3.1 |
| `events.md` | Проектирование событий | `/shared/events/`, CloudEvents |
| `libs.md` | Создание общих библиотек | `/shared/libs/` |
| `versioning.md` | Версионирование контрактов | SemVer |

---

## Фаза 2: /src/.instructions/

**Зона ответственности:** сервисы, backend, database, frontend

| Путь | Описание | SSOT |
|------|----------|------|
| `README.md` | Индекс | — |
| `api/README.md` | Индекс API | — |
| `api/design.md` | Проектирование REST API | `/shared/contracts/openapi/`, RFC 7231 |
| `api/versioning.md` | Версионирование API | SemVer |
| `api/errors.md` | Формат ошибок | `/shared/libs/errors/`, RFC 7807 |
| `data/README.md` | Индекс данных | — |
| `data/validation.md` | Валидация данных | `/shared/libs/validation/`, JSON Schema |
| `data/logging.md` | Логирование | `/shared/libs/logging/`, OpenTelemetry |
| `data/migrations.md` | Миграции БД | — |

---

## Фаза 3: /tests/.instructions/

**Зона ответственности:** e2e, integration, load, smoke, fixtures

| Файл | Описание | SSOT |
|------|----------|------|
| `README.md` | Индекс | — |
| `e2e.md` | E2E тесты | `/tests/e2e/` |
| `integration.md` | Интеграционные тесты | `/tests/integration/` |
| `load.md` | Нагрузочные тесты (k6) | `/tests/load/`, k6 docs |
| `fixtures.md` | Тестовые данные | `/tests/fixtures/` |
| `naming.md` | Именование тестов | — |

---

## Фаза 4: /config/.instructions/

**Зона ответственности:** окружения, feature-flags, секреты

| Файл | Описание | SSOT |
|------|----------|------|
| `README.md` | Индекс | — |
| `environments.md` | Конфигурация окружений | `/config/*.yaml`, 12-factor app |
| `feature-flags.md` | Feature flags | `/config/feature-flags/` |
| `secrets.md` | Управление секретами | — |

---

## Фаза 5: /platform/.instructions/

**Зона ответственности:** docker, k8s, monitoring, gateway, scripts

| Файл | Описание | SSOT |
|------|----------|------|
| `README.md` | Индекс | — |
| `docker.md` | Dockerfile правила | `/platform/docker/`, Docker best practices |
| `k8s.md` | Kubernetes манифесты | `/platform/k8s/` |
| `monitoring.md` | Мониторинг | `/platform/monitoring/`, Prometheus conventions |
| `gateway.md` | API Gateway | `/platform/gateway/` |
| `scripts.md` | Инфра-скрипты | `/platform/scripts/` |

---

## Фаза 6: /.github/.instructions/

**Зона ответственности:** workflows, templates, CODEOWNERS

| Файл | Описание | SSOT |
|------|----------|------|
| `README.md` | Индекс | — |
| `workflows.md` | CI/CD workflows | `/.github/workflows/`, GitHub Actions docs |
| `templates.md` | Шаблоны Issues/PR | `/.github/ISSUE_TEMPLATE/` |
| `codeowners.md` | CODEOWNERS | `/.github/CODEOWNERS` |

---

## Использование скилла

Для каждой инструкции использовать `/instruction-create`:

```
/instruction-create /shared/.instructions/contracts.md
```

---

## Верификация

После каждой фазы:
1. Проверить frontmatter (type, description, governed-by, related)
2. Проверить SSOT ссылки (файлы существуют)
3. Обновить `coverage.md` (статус TODO → ГОТОВО)
4. Проверить навигационные ссылки

---

## Critical Files

- `/.instructions/coverage.md` — трекер прогресса
- `/.instructions/template-instruction.md` — шаблон (добавить SSOT)
- `/.structure/.instructions/template-readme.md` — шаблон README папки
- `/.claude/skills/instruction-create/SKILL.md` — скилл создания
