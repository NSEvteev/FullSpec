---
type: project
description: Индекс скиллов, правила создания, параметры
related:
  - tools/agents.md
  - tools/claude-testing.md
---

# Индекс скиллов

Скиллы — команды для автоматизации повторяющихся задач.

## Правила

### Правило одного действия

Скилл выполняет **1 действие** над объектом:
- `create` — создание
- `update` — обновление
- `delete` — удаление

### Формат названия

```
{объект}-{действие}
```

Примеры: `skill-create`, `agent-update`, `doc-delete`

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
| [skill-create](/.claude/skills/skill-create/SKILL.md) | Создание нового скилла | `/skill-create`, "создай скилл" |
| [skill-update](/.claude/skills/skill-update/SKILL.md) | Обновление скиллов при добавлении нового | `/skill-update`, "обнови скиллы" |
| [skill-delete](/.claude/skills/skill-delete/SKILL.md) | Обновление существующих скиллов при удалении скилла | `/skill-delete`, "удали скилл" |

### agent-management

Управление агентами.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| — | — | — |

### instruction-management

Управление инструкциями.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [instruction-create](/.claude/skills/instruction-create/SKILL.md) | Создание новой инструкции | `/instruction-create`, "создай инструкцию" |
| [instruction-update](/.claude/skills/instruction-update/SKILL.md) | Проверка файлов на соответствие инструкции | `/instruction-update`, "проверь инструкцию" |
| [instruction-delete](/.claude/skills/instruction-delete/SKILL.md) | Очистка ссылок при удалении инструкции | `/instruction-delete`, "удали инструкцию" |

### documentation

Работа с документацией.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [doc-create](/.claude/skills/doc-create/SKILL.md) | Создание документации для файла в /src/ | `/doc-create`, "создай документацию" |
| [doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление документации при изменении кода | `/doc-update`, "обнови документацию" |
| [doc-delete](/.claude/skills/doc-delete/SKILL.md) | Пометка документации при удалении файла | `/doc-delete`, "удали документацию" |
| [links-create](/.claude/skills/links-create/SKILL.md) | Создание ссылок на файлы и папки | `/links-create`, "создай ссылки" |
| [links-update](/.claude/skills/links-update/SKILL.md) | Обновление ссылок в связанных документах | `/links-update`, "обнови ссылки" |
| [links-delete](/.claude/skills/links-delete/SKILL.md) | Пометка битых ссылок при удалении файлов | `/links-delete`, "удали ссылки" |
| [context-update](/.claude/skills/context-update/SKILL.md) | Распространение контекста по графу документов | `/context-update`, "пошарь контекст" |
| [context-delete](/.claude/skills/context-delete/SKILL.md) | Очистка контекста при удалении документа | `/context-delete`, "удали контекст" |

### meta

Мета-скиллы для улучшения работы с LLM.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [prompt-update](/.claude/skills/prompt-update/SKILL.md) | Улучшение и обогащение промтов | `/prompt`, "улучши промт" |

### git

Git операции.

| Скилл | Описание | Триггеры |
|-------|----------|----------|
| [issue-create](/.claude/skills/issue-create/SKILL.md) | Создание GitHub Issue с правильным форматом | `/issue-create`, "создай задачу" |
| [issue-update](/.claude/skills/issue-update/SKILL.md) | Обновление описания и меток Issue | `/issue-update`, "обнови задачу" |
| [issue-execute](/.claude/skills/issue-execute/SKILL.md) | Взятие Issue в работу и выполнение | `/issue-execute`, "возьми задачу" |
| [issue-review](/.claude/skills/issue-review/SKILL.md) | Ревью решения перед закрытием Issue | `/issue-review`, "проверь решение" |
| [issue-complete](/.claude/skills/issue-complete/SKILL.md) | Закрытие Issue как выполненного | `/issue-complete`, "заверши задачу" |
| [issue-delete](/.claude/skills/issue-delete/SKILL.md) | Закрытие Issue как неактуального | `/issue-delete`, "удали задачу" |

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
| `WebFetch` | HTTP запросы к URL |
| `WebSearch` | Поиск в интернете |
| `Task` | Запуск подзадач (агентов) |

---

## Добавление нового скилла

Используй команду `/skill-create` или скажи "создай скилл".

---

## Стандарт параметров

Единообразие параметров скиллов для предсказуемого поведения.

### Общие флаги

| Флаг | Описание | Тип | Пример |
|------|----------|-----|--------|
| `--dry-run` | Показать план без выполнения | boolean | `--dry-run` |
| `--auto` | Автоматический режим без подтверждений | boolean | `--auto` |
| `--depth N` | Глубина обхода связей (по умолчанию 1) | number | `--depth 2` |
| `--diff` | Показать diff изменений | boolean | `--diff` |
| `--no-issue` | Не создавать/не связывать Issue | boolean | `--no-issue` |

### Правила использования

**Правило:** Все скиллы должны поддерживать `--dry-run` для предварительного просмотра.

**Правило:** Флаги с отрицанием начинаются с `--no-` (например, `--no-issue`).

**Правило:** Числовые параметры указываются после имени через пробел (`--depth 2`).

### Совместимость флагов

| Комбинация | Результат |
|------------|-----------|
| `--dry-run --auto` | Показать план (auto игнорируется) |
| `--depth 0` | Без рекурсивного обхода |
| `--diff --dry-run` | Показать предполагаемые изменения |

---

## Связанные инструкции

- [agents.md](agents.md) — индекс агентов
- [claude-testing.md](claude-testing.md) — тестирование Claude Code
