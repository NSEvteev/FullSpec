---
type: standard
description: Индекс инструкций для создания и поддержки скиллов
related:
  - /.claude/skills/README.md
  - tests/claude-testing.md
---

# Инструкции для скиллов

Правила создания, структурирования и поддержки скиллов Claude Code.

## Оглавление

| Инструкция | Описание |
|------------|----------|
| [rules.md](./rules.md) | Правила скиллов: одно действие, именование, структура |
| [workflow.md](./workflow.md) | Шаблон воркфлоу: шаги, паттерны, --dry-run |
| [parameters.md](./parameters.md) | Стандарт параметров: флаги, совместимость |
| [errors.md](./errors.md) | Обработка ошибок: коды, форматы, откат |
| [output.md](./output.md) | Форматы вывода: иконки, структура сообщений |
| [state.md](./state.md) | Временные файлы: .claude/state/, кэш, логи |

---

## Связь с индексом скиллов

**Индекс скиллов:** [/.claude/skills/README.md](/.claude/skills/README.md) — содержит:
- Таблицы скиллов по категориям
- Триггеры вызова

**Эти инструкции** — содержат:
- Правила создания скиллов
- Стандарты качества
- Шаблоны и паттерны

---

## Скиллы для работы с инструкциями

| Скилл | Описание |
|-------|----------|
| [/skill-create](/.claude/skills/skill-create/SKILL.md) | Создание нового скилла |
| [/skill-update](/.claude/skills/skill-update/SKILL.md) | Обновление скиллов |
| [/skill-delete](/.claude/skills/skill-delete/SKILL.md) | Удаление скилла |

---

## Связанные инструкции

- [/.claude/skills/README.md](/.claude/skills/README.md) — индекс скиллов (категории, триггеры)
- [tests/claude-testing.md](../tests/claude-testing.md) — тестирование скиллов
- [shared/scope.md](../shared/scope.md) — определение scope (claude/project)

---

> **Путь:** `/.claude/instructions/skills/README.md`
