---
type: project
description: Индекс инструкций по тестированию
related:
  - /.claude/skills/README.md
  - /.claude/instructions/README.md
---

# Тестирование

Индекс инструкций по тестированию проекта и Claude Code.

## Инструкции

| Инструкция | Описание | Тип |
|------------|----------|-----|
| [claude-testing.md](./claude-testing.md) | Тестирование скиллов и инструкций Claude | standard |
| [project-testing.md](./project-testing.md) | Общие правила тестирования проекта | standard |
| [unit.md](./unit.md) | Стандарты unit-тестов | standard |
| [integration.md](./integration.md) | Стандарты интеграционных тестов | standard |
| [e2e.md](./e2e.md) | Стандарты end-to-end тестов | standard |
| [fixtures.md](./fixtures.md) | Тестовые данные и фикстуры | standard |

---

## Быстрый старт

| Задача | Инструкция | Скилл |
|--------|------------|-------|
| Создать тест для скилла | [claude-testing.md](./claude-testing.md) | `/test-create` |
| Создать unit-тест | [unit.md](./unit.md) | `/test-create` |
| Запустить тесты | [project-testing.md](./project-testing.md) | `/test-execute` |
| Проверить качество теста | [claude-testing.md](./claude-testing.md) | `/test-review` |

---

## Scope: claude vs project

| Аспект | claude | project |
|--------|--------|---------|
| Что тестирует | Скиллы, инструкции | Код приложения |
| Расположение тестов | `.claude/skills/*/tests.md` | `/tests/`, `/src/*/tests/` |
| Типы тестов | smoke, functional, integration | unit, integration, e2e |
| Инструмент | Claude Code | Jest, pytest, etc. |

> **SSOT:** Определение scope описано в [scope-detection.md](/.claude/templates/scope-detection.md).

---

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/test-create](/.claude/skills/test-create/SKILL.md) | Создание теста с автоопределением scope |
| [/test-update](/.claude/skills/test-update/SKILL.md) | Обновление теста |
| [/test-execute](/.claude/skills/test-execute/SKILL.md) | Запуск тестов |
| [/test-review](/.claude/skills/test-review/SKILL.md) | Ревью теста |
| [/test-complete](/.claude/skills/test-complete/SKILL.md) | Отметка теста как пройденного |
| [/test-delete](/.claude/skills/test-delete/SKILL.md) | Удаление теста |
| [/test-coverage](/.claude/skills/test-coverage/SKILL.md) | Анализ покрытия |

---

## Связанные инструкции

- [instructions/README.md](/.claude/instructions/README.md) — общий индекс инструкций
- [skills/README.md](/.claude/skills/README.md) — индекс скиллов
