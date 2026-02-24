---
description: Стандарт единой системы поиска по документации проекта — API скриптов, типы сущностей, формат вывода, интеграция с Claude Code.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .structure/.instructions/README.md
---

# Стандарт поиска по документации

Единая система поиска по всей документации проекта: инструкции, скиллы, агенты, правила, README и скрипты.

**Полезные ссылки:**
- [Инструкции .structure/](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | — |
| Создание | — |
| Модификация | — |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Типы сущностей](#2-типы-сущностей)
- [3. API конвенция](#3-api-конвенция)
  - [Обязательные аргументы](#обязательные-аргументы)
  - [Формат вывода](#формат-вывода)
- [4. Скрипты поиска](#4-скрипты-поиска)
  - [Единый поиск](#единый-поиск)
  - [Специализированные скрипты](#специализированные-скрипты)
- [5. Интеграция с Claude Code](#5-интеграция-с-claude-code)

---

## 1. Назначение

Система поиска позволяет находить документы, скрипты и конфигурации по ключевым словам. Используется при:

- Навигации по проекту (поиск нужной инструкции)
- Проверке дубликатов перед созданием нового объекта
- Аудите документации (полный список сущностей определённого типа)

---

## 2. Типы сущностей

| Тип | Источник | Идентификатор |
|-----|----------|---------------|
| `instruction` | `**/.instructions/*.md` (без README) | stem файла |
| `skill` | `.claude/skills/*/SKILL.md` | frontmatter `name` |
| `agent` | `.claude/agents/*/AGENT.md` | frontmatter `name` |
| `rule` | `.claude/rules/*.md` | stem файла |
| `readme` | `**/README.md` с frontmatter | путь к папке |
| `script` | `**/.instructions/.scripts/*.py` | stem файла |

---

## 3. API конвенция

### Обязательные аргументы

Каждый list-скрипт должен поддерживать:

| Аргумент | Описание | По умолчанию |
|----------|----------|-------------|
| `--search <query>` | Поиск по имени и описанию (case-insensitive substring) | — |
| `--json` | Вывод в формате JSON | `false` |
| `--repo <dir>` | Корень репозитория | `.` |

### Формат вывода

**Единый формат элемента (JSON):**

```json
{
    "type": "instruction",
    "name": "standard-links",
    "path": ".structure/.instructions/standard-links.md",
    "description": "Стандарт ссылок в документах проекта",
    "area": ".structure"
}
```

| Поле | Описание |
|------|----------|
| `type` | Тип сущности: instruction, skill, agent, rule, readme, script |
| `name` | Имя (stem файла или frontmatter name) |
| `path` | Относительный путь от корня репозитория |
| `description` | Описание из frontmatter или docstring |
| `area` | Родительская область (папка перед `.instructions/`) |

**Текстовый вывод:**

```
Найдено: N (тип: all)

## instruction

  standard-links
    Путь: .structure/.instructions/standard-links.md
    Описание: Стандарт ссылок
```

---

## 4. Скрипты поиска

### Единый поиск

| Скрипт | Назначение | Расположение |
|--------|------------|-------------|
| [search-docs.py](/.instructions/.scripts/search-docs.py) | Поиск по всей документации | `.instructions/.scripts/` |

```bash
python .instructions/.scripts/search-docs.py --search "валидация"
python .instructions/.scripts/search-docs.py --type skill --search "создание"
python .instructions/.scripts/search-docs.py --type all --json
```

### Специализированные скрипты

| Скрипт | Тип | Расположение |
|--------|-----|-------------|
| [list-instructions.py](/.instructions/.scripts/list-instructions.py) | instruction | `.instructions/.scripts/` |
| [list-skills.py](/.claude/.instructions/skills/.scripts/list-skills.py) | skill | `.claude/.instructions/skills/.scripts/` |
| [list-agents.py](/.claude/.instructions/agents/.scripts/list-agents.py) | agent | `.claude/.instructions/agents/.scripts/` |
| [list-rules.py](/.claude/.instructions/rules/.scripts/list-rules.py) | rule | `.claude/.instructions/rules/.scripts/` |
| [parse-docstrings.py](/.instructions/.scripts/parse-docstrings.py) | script | `.instructions/.scripts/` |

Все специализированные скрипты поддерживают `--search`, `--json`, `--repo`.

---

## 5. Интеграция с Claude Code

**Скилл:** [`/list-search`](/.claude/skills/list-search/SKILL.md) — вызывает `search-docs.py`.

**Rule:** [`core.md`](/.claude/rules/core.md) — секция "Поиск по описаниям" ссылается на `/list-search` и `search-docs.py`.

**Когда использовать:**
- При поиске документов, скриптов или скиллов по ключевым словам
- Перед созданием нового объекта (проверка дубликатов)
- При навигации по проекту
