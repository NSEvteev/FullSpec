---
description: SSOT-индекс всех скиллов проекта
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

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [skill-create](./skill-create/SKILL.md) | Создание нового скилла | `/skill-create`, "создай скилл" |
| [skill-modify](./skill-modify/SKILL.md) | Изменение скилла (обновление, деактивация, миграция) | `/skill-modify`, "измени скилл" |
| [skill-validate](./skill-validate/SKILL.md) | Валидация скилла по стандарту | `/skill-validate`, "проверь скилл" |

### instructions

Управление инструкциями.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [instruction-create](./instruction-create/SKILL.md) | Создание новой инструкции | `/instruction-create`, "создай инструкцию" |
| [instruction-modify](./instruction-modify/SKILL.md) | Обновление, деактивация, миграция | `/instruction-modify`, "измени инструкцию" |
| [instruction-validate](./instruction-validate/SKILL.md) | Валидация формата инструкции | `/instruction-validate`, "проверь инструкцию" |

### scripts

Управление скриптами автоматизации.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [script-create](./script-create/SKILL.md) | Создание нового скрипта | `/script-create`, "создай скрипт" |
| [script-modify](./script-modify/SKILL.md) | Обновление, рефакторинг, удаление | `/script-modify`, "измени скрипт" |
| [script-validate](./script-validate/SKILL.md) | Валидация формата скрипта | `/script-validate`, "проверь скрипт" |
| [principles-validate](./principles-validate/SKILL.md) | Валидация принципов программирования | `/principles-validate`, "проверь принципы" |

### documentation

Работа с документацией и структурой.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [links-validate](./links-validate/SKILL.md) | Валидация ссылок в markdown-документах | `/links-validate`, "проверь ссылки" |
| [structure-create](./structure-create/SKILL.md) | Создание новой папки в структуре | `/structure-create`, "создай папку" |
| [structure-modify](./structure-modify/SKILL.md) | Изменение папки (rename/move/delete) | `/structure-modify`, "переименуй папку" |
| [structure-validate](./structure-validate/SKILL.md) | Валидация согласованности SSOT структуры | `/structure-validate`, "проверь структуру" |

### rules

Управление rules для автоматической загрузки контекста.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [rule-create](./rule-create/SKILL.md) | Создание нового rule-файла | `/rule-create`, "создай rule" |
| [rule-modify](./rule-modify/SKILL.md) | Изменение, деактивация и миграция rule | `/rule-modify`, "измени rule" |
| [rule-validate](./rule-validate/SKILL.md) | Валидация формата и структуры rule | `/rule-validate`, "проверь rule" |

### agents

Управление агентами Claude.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [agent-create](./agent-create/SKILL.md) | Создание нового агента | `/agent-create`, "создай агента" |
| [agent-modify](./agent-modify/SKILL.md) | Изменение, деактивация и миграция | `/agent-modify`, "измени агента" |
| [agent-validate](./agent-validate/SKILL.md) | Валидация конфигурации и промпта агента | `/agent-validate`, "проверь агента" |

### github

Работа с объектами GitHub (labels, milestones, issues, PR).

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [labels-validate](./labels-validate/SKILL.md) | Валидация labels.yml и меток на Issues/PR | `/labels-validate`, "проверь метки" |
| [labels-modify](./labels-modify/SKILL.md) | Изменение меток GitHub | `/labels-modify`, "измени метки" |
| [milestone-create](./milestone-create/SKILL.md) | Создание Milestone по стандарту | `/milestone-create`, "создай milestone" |
| [milestone-modify](./milestone-modify/SKILL.md) | Изменение, закрытие и удаление Milestone | `/milestone-modify`, "закрой milestone" |
| [milestone-validate](./milestone-validate/SKILL.md) | Валидация Milestone по стандарту | `/milestone-validate`, "проверь milestone" |
| [issue-create](./issue-create/SKILL.md) | Создание GitHub Issue по стандарту | `/issue-create`, "создай issue" |
| [issue-validate](./issue-validate/SKILL.md) | Валидация GitHub Issue по стандарту | `/issue-validate`, "проверь issue" |
| [issue-modify](./issue-modify/SKILL.md) | Изменение GitHub Issue по стандарту | `/issue-modify`, "измени issue" |
| [branch-create](./branch-create/SKILL.md) | Создание ветки по стандарту | `/branch-create`, "создай ветку" |
| [review-branch](./review-branch/SKILL.md) | Локальное ревью ветки перед PR | `/review-branch`, "ревью ветки" |
| [review-pr](./review-pr/SKILL.md) | Ревью Pull Request на GitHub | `/review-pr`, "ревью PR" |

### drafts

Работа с черновиками.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [draft-validate](./draft-validate/SKILL.md) | Валидация черновика по стандарту | `/draft-validate`, "проверь черновик" |

### migration

Миграция при обновлении стандартов.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [migration-create](./migration-create/SKILL.md) | Выполнение миграции | `/migration-create`, "выполни миграцию" |
| [migration-validate](./migration-validate/SKILL.md) | Валидация миграции | `/migration-validate`, "проверь миграцию" |

---

## Справочник allowed-tools

| Инструмент | Описание |
|------------|----------|
| `Bash` | Выполнение команд в терминале |
| `Read` | Чтение файлов |
| `Write` | Создание файлов |
| `Edit` | Редактирование файлов |
| `Glob` | Поиск файлов по паттерну |
| `Grep` | Поиск в содержимом файлов |

---

## Стандарт параметров

### Общие флаги

| Флаг | Описание | Тип |
|------|----------|-----|
| `--dry-run` | Показать план без выполнения | boolean |
| `--auto` | Автоматический режим без подтверждений | boolean |

**Правило:** Все скиллы должны поддерживать `--dry-run` для предварительного просмотра.

---

## Добавление нового скилла

Используй команду `/skill-create` или скажи "создай скилл".

---
