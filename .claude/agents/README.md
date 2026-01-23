---
type: standard
description: Индекс агентов, правила создания, теги
related:
  - /.claude/skills/README.md
  - /.claude/.instructions/tests/claude-testing.md
---

# Индекс агентов

Агенты — специализированные помощники для выполнения комплексных задач.

## Правила

### Структура агента

```
/.claude/agents/{название}.md
```

### Frontmatter агента

```yaml
---
name: {название}
description: {описание}
tags: [{тег1}, {тег2}, ...]
skills: [{скилл1}, {скилл2}, ...]
---
```

### Связь с скиллами

- Теги агента соответствуют категориям скиллов
- При создании скилла — предлагается назначить агенту с подходящими тегами
- Список скиллов агента хранится в `skills:` frontmatter

---

## Теги агентов

Теги определяют сферу деятельности агента и используются для автоматического связывания со скиллами.

| Тег | Описание | Категории скиллов |
|-----|----------|-------------------|
| `skill-management` | Управление скиллами | skill-management |
| `agent-management` | Управление агентами | agent-management |
| `instruction-management` | Управление инструкциями | instruction-management |
| `documentation` | Работа с документацией | documentation |
| `git` | Git операции | git |
| `code` | Работа с кодом | code |
| `testing` | Тестирование | testing |
| `infrastructure` | Инфраструктура | infrastructure |

---

## Список агентов

> **Статус:** Агенты ещё не созданы. Таблица заполняется автоматически при использовании `/agent-create`.

| Агент | Описание | Теги | Скиллы |
|-------|----------|------|--------|
| *(пусто)* | Используй `/agent-create` для создания первого агента | — | — |

### Рекомендуемые агенты для создания

| Агент | Назначение | Теги |
|-------|------------|------|
| `documentation-manager` | Управление документацией проекта (discuss → architecture → ADR) | `documentation` |
| `code-reviewer` | Автоматический code review по чек-листу | `code`, `git` |
| `test-runner` | Запуск и анализ тестов | `testing` |
| `release-manager` | Управление релизами и changelog | `git`, `infrastructure` |

---

## Добавление нового агента

Используй команду `/agent-create` или скажи "создай агента".

---

## Автоматизация

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| [/agent-create](/.claude/skills/agent-create/SKILL.md) | Создание нового агента по шаблону |
| `/agent-update` | *(планируется)* Обновление агента |
| `/agent-delete` | *(планируется)* Удаление агента |

---

## Связанные инструкции

- [skills/README.md](/.claude/skills/README.md) — индекс скиллов
- [instructions/tests/claude-testing.md](/.claude/.instructions/tests/claude-testing.md) — тестирование агентов
