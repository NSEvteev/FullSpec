# SSOT — Single Source of Truth

Паттерн единого источника истины в проекте.

## Что такое SSOT

**SSOT (Single Source of Truth)** — принцип, при котором каждый тип артефакта имеет один авторитетный документ (стандарт), определяющий его структуру и правила.

**Зачем нужен:**
- Исключает противоречия между документами
- Упрощает обновление — меняешь в одном месте
- Гарантирует единообразие всех экземпляров

## Как определить SSOT-документ

Если в документе есть метка:

```
**SSOT:** [название](путь)
```

— это означает, что перед работой с этим документом **ОБЯЗАТЕЛЬНО** нужно прочитать указанный файл.

## Иерархия документов

```
Стандарт (standard-*.md)
    ↓
Workflows (create-*, modify-*, validation-*)
    ↓
Экземпляры (конкретные инструкции, скиллы, rules)
```

| Уровень | Описание | Пример |
|---------|----------|--------|
| Стандарт | Определяет структуру и правила | `standard-instruction.md` |
| Workflows | Процедуры работы со стандартом | `create-instruction.md`, `validation-instruction.md` |
| Экземпляры | Конкретные экземпляры | `/.instructions/backend/api-design.md` |

## Правило работы с SSOT

> **КРИТИЧНО:** Если видишь метку `**SSOT:** [файл](путь)` — прочитай файл перед выполнением.
> Нельзя работать по памяти или предположениям.

## Примеры из проекта

### Пример 1: Инструкции

| Роль | Файл |
|------|------|
| Стандарт | `/.instructions/standard-instruction.md` |
| Workflows | `/.instructions/create-instruction.md` |
| Экземпляры | `/.instructions/backend/api-design.md` |

### Пример 2: Скиллы

| Роль | Файл |
|------|------|
| Стандарт | `/.claude/.instructions/skills/standard-skill.md` |
| Workflows | `/.claude/.instructions/skills/create-skill.md` |
| Экземпляры | `/.claude/skills/instruction-create/SKILL.md` |

### Пример 3: Rules

| Роль | Файл |
|------|------|
| Стандарт | `/.claude/.instructions/rules/standard-rule.md` |
| Workflows | `/.claude/.instructions/rules/create-rule.md` |
| Экземпляры | `/.claude/rules/core.md` |

## Исключения

Следующие файлы **не имеют** SSOT-стандарта:

- `/CLAUDE.md` — корневой файл проекта
- `/README.md` — корневой README
- `/CONTRIBUTING.md` — гайд для контрибьюторов
- `/.claude/drafts/*.md` — черновики (frontmatter опционален)

## Версионирование

Каждый стандарт имеет версию в frontmatter:

```yaml
---
standard-version: v1.2
---
```

При изменении стандарта **ОБЯЗАТЕЛЬНА** миграция всех зависимых документов через `/migration-create`.

## Связанные документы

- [Артефакты системы](./artifacts.md) — типы артефактов и их SSOT
- [Quick Start](./quick-start.md) — быстрое введение
