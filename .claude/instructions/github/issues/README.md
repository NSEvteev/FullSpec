---
type: index
description: Индекс инструкций по работе с GitHub Issues
---

# GitHub Issues

Инструкции по работе с задачами через GitHub Issues.

## Оглавление

| Файл | Описание |
|------|----------|
| [format.md](./format.md) | Формат задачи: заголовок, тело, префиксы |
| [labels.md](./labels.md) | Система меток (labels) |
| [workflow.md](./workflow.md) | Жизненный цикл Issue, state-машина |
| [commands.md](./commands.md) | Команды gh CLI |
| [errors.md](./errors.md) | Обработка ошибок |
| [examples.md](./examples.md) | Примеры использования |

---

## Принципы

1. **GitHub Issues — единственный источник задач** — локальные задачи не используем
2. **Префиксы обязательны** — формат `[PREFIX] Краткое описание`
3. **Метки по категориям** — сервис, тип, приоритет, статус
4. **Скиллы для управления** — автоматизация через `/issue-*`

---

## Скиллы

| Скилл | Назначение | Когда использовать |
|-------|------------|-------------------|
| [/issue-create](/.claude/skills/issue-create/SKILL.md) | Создание Issue | Новая задача |
| [/issue-update](/.claude/skills/issue-update/SKILL.md) | Обновление Issue | Изменение описания/меток |
| [/issue-execute](/.claude/skills/issue-execute/SKILL.md) | Выполнение Issue | Взять в работу и выполнить |
| [/issue-review](/.claude/skills/issue-review/SKILL.md) | Ревью решения | После выполнения задачи |
| [/issue-complete](/.claude/skills/issue-complete/SKILL.md) | Закрытие как выполненного | Задача выполнена |
| [/issue-delete](/.claude/skills/issue-delete/SKILL.md) | Закрытие как неактуального | Задача отменена |
| [/issue-reopen](/.claude/skills/issue-reopen/SKILL.md) | Переоткрытие Issue | Задача закрыта преждевременно |

---

## Связанные инструкции

- [git/workflow.md](../git/workflow.md) — ветки, PR, merge
- [git/commits.md](../git/commits.md) — Conventional commits
- [git/ci.md](../git/ci.md) — CI pipeline

---

## Quick Start

```bash
# Создать задачу
/issue-create --service auth "Добавить OAuth авторизацию"

# Взять в работу и выполнить
/issue-execute #123

# Закрыть после выполнения
/issue-complete #123
```

---

> **Путь:** `/.claude/instructions/issues/README.md`
