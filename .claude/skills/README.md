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
| [review-branch](./review-branch/SKILL.md) | Локальное ревью ветки перед PR |
| [review-pr](./review-pr/SKILL.md) | Ревью Pull Request на GitHub |

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
