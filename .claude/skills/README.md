---
description: SSOT-индекс всех скиллов Claude Code — полный список команд с описаниями и статусами. Справочник навигации.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
---

# Индекс скиллов

Скиллы — команды для автоматизации повторяющихся задач.

---

## Правила

### Правило одного действия

Скилл выполняет **1 действие** над объектом:
- `create` — создание
- `modify` — изменение (обновление, деактивация, миграция)
- `validate` — валидация

### Формат названия

```
{объект}-{действие}
```

Примеры: `skill-create`, `skill-modify`, `links-validate`

### Расположение

```
/.claude/skills/{название}/
    SKILL.md
```

---

## Категории

### skill-management

Управление скиллами.

| Скилл | Описание |
|-------|----------|
| [skill-create](./skill-create/SKILL.md) | Создание нового скилла |
| [skill-modify](./skill-modify/SKILL.md) | Изменение скилла (обновление, деактивация, миграция) |
| [skill-validate](./skill-validate/SKILL.md) | Валидация скилла по стандарту |

### instructions

Управление инструкциями.

| Скилл | Описание |
|-------|----------|
| [instruction-create](./instruction-create/SKILL.md) | Создание новой инструкции |
| [instruction-modify](./instruction-modify/SKILL.md) | Обновление, деактивация, миграция |
| [instruction-validate](./instruction-validate/SKILL.md) | Валидация формата инструкции |

### scripts

Управление скриптами автоматизации.

| Скилл | Описание |
|-------|----------|
| [script-create](./script-create/SKILL.md) | Создание нового скрипта |
| [script-modify](./script-modify/SKILL.md) | Обновление, рефакторинг, удаление |
| [script-validate](./script-validate/SKILL.md) | Валидация формата скрипта |
| [principles-validate](./principles-validate/SKILL.md) | Валидация принципов программирования |

### documentation

Работа с документацией и структурой.

| Скилл | Описание |
|-------|----------|
| [links-validate](./links-validate/SKILL.md) | Валидация ссылок в markdown-документах |
| [list-search](./list-search/SKILL.md) | Поиск по всей документации проекта |
| [structure-create](./structure-create/SKILL.md) | Создание новой папки в структуре |
| [structure-modify](./structure-modify/SKILL.md) | Изменение папки (rename/move/delete) |
| [structure-validate](./structure-validate/SKILL.md) | Валидация согласованности SSOT структуры |

### rules

Управление rules для автоматической загрузки контекста.

| Скилл | Описание |
|-------|----------|
| [rule-create](./rule-create/SKILL.md) | Создание нового rule-файла |
| [rule-modify](./rule-modify/SKILL.md) | Изменение, деактивация и миграция rule |
| [rule-validate](./rule-validate/SKILL.md) | Валидация формата и структуры rule |

### agents

Управление агентами Claude.

| Скилл | Описание |
|-------|----------|
| [agent-create](./agent-create/SKILL.md) | Создание нового агента |
| [agent-modify](./agent-modify/SKILL.md) | Изменение, деактивация и миграция |
| [agent-validate](./agent-validate/SKILL.md) | Валидация конфигурации и промпта агента |

### github

Работа с объектами GitHub (labels, milestones, issues, PR).

| Скилл | Описание |
|-------|----------|
| [labels-validate](./labels-validate/SKILL.md) | Валидация labels.yml и меток на Issues/PR |
| [labels-modify](./labels-modify/SKILL.md) | Изменение меток GitHub |
| [milestone-create](./milestone-create/SKILL.md) | Создание Milestone по стандарту |
| [milestone-modify](./milestone-modify/SKILL.md) | Изменение, закрытие и удаление Milestone |
| [milestone-validate](./milestone-validate/SKILL.md) | Валидация Milestone по стандарту |
| [issue-create](./issue-create/SKILL.md) | Создание GitHub Issue по стандарту |
| [issue-validate](./issue-validate/SKILL.md) | Валидация GitHub Issue по стандарту |
| [issue-modify](./issue-modify/SKILL.md) | Изменение GitHub Issue по стандарту |
| [branch-create](./branch-create/SKILL.md) | Создание ветки по стандарту |
| [commit](./commit/SKILL.md) | Создание коммита по Conventional Commits |
| [pr-create](./pr-create/SKILL.md) | Создание PR с автосбором Issues из chain |
| [review](./review/SKILL.md) | Ревью кода (ветка или PR) |
| [merge](./merge/SKILL.md) | Merge PR с pre/post проверками и sync |
| [post-release](./post-release/SKILL.md) | Post-release валидация (Release, Notes, CHANGELOG, деплой) |
| [release-create](./release-create/SKILL.md) | Создание GitHub Release (chains, pre-release, Notes, публикация) |

### process

Оркестрация процесса поставки ценности.

| Скилл | Описание |
|-------|----------|
| [chain](./chain/SKILL.md) | Оркестратор полного цикла (TaskList от идеи до релиза) |
| [hotfix](./hotfix/SKILL.md) | Процесс хотфикса (диагностика, impact analysis, исправление) |
| [init-project](./init-project/SKILL.md) | Инициализация проекта (Фаза 0, GitHub, docs/, customization) |

### specs

Работа со спецификациями SDD (Discussion, Design, Plan Tests, Plan Dev, Services, Technologies).

| Скилл | Описание |
|-------|----------|
| [discussion-create](./discussion-create/SKILL.md) | Создание документа дискуссии |
| [discussion-modify](./discussion-modify/SKILL.md) | Изменение документа дискуссии |
| [discussion-validate](./discussion-validate/SKILL.md) | Валидация документа дискуссии |
| [design-create](./design-create/SKILL.md) | Создание документа проектирования |
| [design-modify](./design-modify/SKILL.md) | Изменение документа проектирования |
| [design-validate](./design-validate/SKILL.md) | Валидация документа проектирования |
| [plan-test-create](./plan-test-create/SKILL.md) | Создание документа плана тестов |
| [plan-test-modify](./plan-test-modify/SKILL.md) | Изменение документа плана тестов |
| [plan-test-validate](./plan-test-validate/SKILL.md) | Валидация документа плана тестов |
| [plan-dev-create](./plan-dev-create/SKILL.md) | Создание документа плана разработки |
| [plan-dev-modify](./plan-dev-modify/SKILL.md) | Изменение документа плана разработки |
| [plan-dev-validate](./plan-dev-validate/SKILL.md) | Валидация документа плана разработки |
| [dev-create](./dev-create/SKILL.md) | Запуск разработки по analysis chain (WAITING → RUNNING) |
| [docker-up](./docker-up/SKILL.md) | Поднятие Docker dev-окружения (compose up, healthcheck, шаг 5.1) |
| [test](./test/SKILL.md) | Финальная валидация (sync main, tests, lint, build, отчёт READY/NOT READY, шаг 5.2) |
| [test-ui](./test-ui/SKILL.md) | Playwright UI smoke-тесты (SMOKE-NNN сценарии, скриншоты, отчёт PASS/FAIL, шаг 5.3) |
| [docs-sync](./docs-sync/SKILL.md) | Синхронизация specs/docs/ после analysis chain (service/technology/system агенты + ревью) |
| [chain-done](./chain-done/SKILL.md) | Завершение analysis chain (REVIEW → DONE, system-agent mode=done, cross-chain) |
| [analysis-status](./analysis-status/SKILL.md) | Статус analysis chain (одна/все цепочки, dashboard) |
| [rollback-chain](./rollback-chain/SKILL.md) | Откат analysis chain (ROLLING_BACK → REJECTED) — 5 фаз оркестрации |
| [review-create](./review-create/SKILL.md) | Создание review.md при Plan Dev → WAITING |
| [review-validate](./review-validate/SKILL.md) | Валидация документа ревью кода |
| [service-create](./service-create/SKILL.md) | Создание specs/docs/{svc}.md — per-service документ |
| [service-modify](./service-modify/SKILL.md) | Изменение specs/docs/{svc}.md (обновление, деактивация, миграция) |
| [service-validate](./service-validate/SKILL.md) | Валидация specs/docs/{svc}.md по стандарту |
| [technology-create](./technology-create/SKILL.md) | Создание per-tech стандарта (N агентов параллельно) |
| [technology-modify](./technology-modify/SKILL.md) | Изменение per-tech стандарта |
| [technology-validate](./technology-validate/SKILL.md) | Валидация per-tech стандарта |

### drafts

Работа с черновиками.

| Скилл | Описание |
|-------|----------|
| [draft-validate](./draft-validate/SKILL.md) | Валидация черновика по стандарту |

### migration

Миграция при обновлении стандартов.

| Скилл | Описание |
|-------|----------|
| [migration-create](./migration-create/SKILL.md) | Выполнение миграции |
| [migration-validate](./migration-validate/SKILL.md) | Валидация миграции |

---

## Добавление нового скилла

Используй команду `/skill-create` или скажи "создай скилл".

---
