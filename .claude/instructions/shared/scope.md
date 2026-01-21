---
type: standard
description: Определение scope (claude/project) для test-* и doc-* скиллов
related:
  - tests/claude-testing.md
  - tests/formats.md
  - doc/rules.md
---

# Определение Scope

Единый источник правил определения scope для test-* и doc-* скиллов.

## Оглавление

- [Принцип](#принцип)
- [Алгоритм определения](#алгоритм-определения)
- [Маппинг путей](#маппинг-путей)
- [Scope для тестов](#scope-для-тестов)
- [Scope для документации](#scope-для-документации)
- [Примеры](#примеры)
- [FAQ](#faq)
- [Связанные инструкции](#связанные-инструкции)

---

## Принцип

Один набор скиллов `test-*` и `doc-*` для всех типов. Scope определяется **автоматически по пути**.

| Scope | Описание |
|-------|----------|
| `claude` | Инструменты Claude (скиллы, инструкции, агенты) |
| `project` | Код и документация проекта |

---

## Алгоритм определения

```
                     /test-* [target]
                            │
            ┌───────────────┼───────────────┐
            │               │               │
      target есть?    --scope указан?   ничего нет
            │               │               │
            ▼               ▼               ▼
     Определить по    Использовать      Спросить:
     ПУТИ target      указанный         [1] claude
                                        [2] project
                                        [3] all
```

---

## Маппинг путей

### Путь → Scope

| Путь начинается с | Scope | Описание |
|-------------------|-------|----------|
| `.claude/skills/*` | `claude` | Скиллы |
| `.claude/instructions/*` | `claude` | Инструкции |
| `.claude/agents/*` | `claude` | Агенты |
| `.claude/templates/*` | `claude` | Шаблоны |
| `.claude/discussions/*` | `claude` | Дискуссии |
| `src/*` | `project` | Код проекта |
| `tests/*` | `project` | Тесты проекта |
| `shared/*` | `project` | Общий код |
| `config/*` | `project` | Конфигурации |
| `platform/*` | `project` | Инфраструктура |
| `doc/*` | `project` | Документация проекта |

### Правило по умолчанию

Если путь не соответствует ни одному паттерну:
1. Если путь внутри репозитория → `project`
2. Если путь вне репозитория → ошибка

---

## Scope для тестов

### Где хранить тесты

| Scope | Объект | Расположение | Формат |
|-------|--------|--------------|--------|
| `claude` | Скилл | `{skill}/SKILL.md` раздел "Тестирование" | Markdown |
| `claude` | Скилл (много тестов) | `{skill}/tests.md` | Markdown |
| `claude` | Инструкция | `{instruction}.test.md` | Markdown |
| `project` | Модуль | `src/X/Y.test.ts` или `tests/X/Y.test.ts` | TypeScript |
| `project` | Сервис | `tests/integration/*.test.ts` | TypeScript |
| `project` | API | `tests/e2e/*.test.ts` | TypeScript |

### Типы тестов по scope

| Scope | Типы |
|-------|------|
| `claude` | smoke, functional, integration |
| `project` | unit, integration, e2e, smoke, load |

---

## Scope для документации

### Где хранить документацию

| Scope | Объект | Расположение |
|-------|--------|--------------|
| `claude` | Скилл | `.claude/skills/{skill}/SKILL.md` |
| `claude` | Инструкция | `.claude/instructions/{path}.md` |
| `claude` | Агент | `.claude/agents/{agent}.md` |
| `project` | Сервис | `doc/src/{service}/README.md` |
| `project` | API | `doc/src/{service}/specs/api.md` |
| `project` | ADR | `doc/src/{service}/specs/adr/*.md` |
| `project` | Архитектура | `doc/architecture/*.md` |

---

## Примеры

### Тесты

```bash
# Claude scope (автоопределение)
/test-create .claude/skills/test-create
# → scope: claude

/test-execute .claude/skills/README.md
# → scope: claude

# Project scope (автоопределение)
/test-create src/auth/validator.ts
# → scope: project

/test-execute tests/integration/
# → scope: project

# Явное указание scope
/test-execute --scope all
# → запустить все тесты обоих scopes

# Без параметров — спросить
/test-execute
# → "Какой scope запустить? [1] claude [2] project [3] all"
```

### Документация

```bash
# Claude scope (автоопределение)
/doc-create .claude/skills/new-skill
# → scope: claude

/doc-update .claude/instructions/git/workflow.md
# → scope: claude

# Project scope (автоопределение)
/doc-create src/auth
# → scope: project, создаст doc/src/auth/README.md

/doc-update doc/architecture/overview.md
# → scope: project
```

---

## FAQ

### Что делать, если путь неоднозначен?

Если файл может относиться к обоим scopes:
1. Приоритет — **явное указание** `--scope`
2. Если не указано — **спросить у пользователя**

### Можно ли переопределить scope?

Да, флаг `--scope` имеет приоритет:

```bash
/test-execute .claude/skills/test-create --scope project
# Выполнит project-тесты, несмотря на путь .claude/
```

### Как добавить новый путь в маппинг?

1. Обновить этот файл (scope.md)
2. Все скиллы автоматически получат обновление через ссылку

---

## Скиллы

> Специфичные скиллы для этой области отсутствуют. Используйте общие скиллы проекта.

---

## Связанные инструкции

- [tests/claude-testing.md](../tests/claude-testing.md) — тестирование скиллов
- [tests/formats.md](../tests/formats.md) — форматы тестов
- [doc/rules.md](../doc/rules.md) — правила документации

---

> **Путь:** `/.claude/instructions/shared/scope.md`
