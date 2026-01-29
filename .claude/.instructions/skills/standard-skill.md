---
description: Стандарт формата скиллов
standard: .instructions/standard-instruction.md
index: .claude/.instructions/skills/README.md
---

# Стандарт скиллов

Формат и структура файлов SKILL.md.

**Полезные ссылки:**
- [Инструкции для скиллов](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-skill.md](./validation-skill.md) |
| Создание | [create-skill.md](./create-skill.md) |
| Модификация | [modify-skill.md](./modify-skill.md) |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Расположение](#2-расположение)
- [3. Frontmatter](#3-frontmatter)
- [4. Секции документа](#4-секции-документа)
- [5. Примеры](#5-примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## 1. Назначение

**Скилл = триггер + ссылка на SSOT-инструкцию.**

Скилл НЕ содержит логику — он только:
- Определяет команду и фразы для вызова
- Указывает на SSOT-инструкцию с деталями
- Описывает формат вызова и параметры

**Когда создавать скилл:**
- Есть SSOT-инструкция с воркфлоу
- Нужен удобный триггер для вызова
- Действие повторяется

**Когда НЕ создавать скилл:**
- Нет SSOT-инструкции (сначала создать инструкцию!)
- Разовое действие
- Простое действие без воркфлоу

**Принцип:**
```
1. Инструкция (SSOT)     ← Сначала
2. Скилл (триггер)       ← Потом
```

---

## 2. Расположение

```
/.claude/skills/{skill-name}/SKILL.md
```

### Правила именования

| Правило | Пример ✅ | Пример ❌ |
|---------|----------|----------|
| Формат `{object}-{action}` | `structure-create` | `create-structure` |
| Kebab-case | `skill-create` | `skillCreate` |
| Латиница | `links-validate` | `ссылки-валидация` |

### Типы скиллов

Скиллы создаются только трёх типов:

| Тип | Действие | Инструкция |
|-----|----------|------------|
| `create` | Создание объекта | `create-{object}.md` |
| `modify` | Изменение объекта | `modify-{object}.md` |
| `validate` | Валидация объекта | `validation-{object}.md` |

---

## 3. Frontmatter

**SSOT:** [standard-frontmatter.md](/.structure/.instructions/standard-frontmatter.md#2-дополнительные-поля-для-скиллов)

Скиллы используют расширенный frontmatter с дополнительными полями: [1. Обязательные поля](/.structure/.instructions/standard-frontmatter.md#1-обязательные-поля) + [2. Дополнительные поля для скиллов](/.structure/.instructions/standard-frontmatter.md#2-дополнительные-поля-для-скиллов))

---

## 4. Секции документа

### Обязательные секции

| Секция | Содержание |
|--------|------------|
| **SSOT** | Ссылка на инструкцию (сразу после заголовка) |
| **Формат вызова** | Синтаксис + таблица параметров |
| **Воркфлоу** | Предупреждение + "→ Выполнить шаги из SSOT" |
| **Чек-лист** | Ссылка на чек-лист в SSOT |
| **Примеры** | 2-3 примера вызова |

### Шаблон

```markdown
# {Название}

**SSOT:** [{инструкция}.md]({путь к инструкции})

## Формат вызова

/{skill-name} <параметр> [--опция]

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<параметр>` | Описание | Да |
| `--опция` | Описание | Нет |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [{инструкция}.md]({путь})

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [{инструкция}.md#чек-лист]({путь}#чек-лист)

## Примеры

/{skill-name} example1
/{skill-name} example2 --option value
```

### Стандартные флаги

| Флаг | Описание | Тип |
|------|----------|-----|
| `--dry-run` | Показать план без выполнения | boolean |
| `--auto` | Автоматический режим без подтверждений | boolean |

---

## 5. Примеры

### Пример: structure-create

```markdown
---
name: structure-create
description: Создание новой папки в структуре проекта
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
triggers:
  commands:
    - /structure-create
  phrases:
    ru:
      - создай папку
      - добавь папку
    en:
      - create folder
---

# Создание папки

**SSOT:** [create-structure.md](/.structure/.instructions/create-structure.md)

## Формат вызова

/structure-create <путь> [--description "Описание"]

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `<путь>` | Путь к новой папке | Да |
| `--description` | Описание для SSOT | Нет (спросит) |

## Воркфлоу

> ⚠️ **Перед выполнением** прочитать [create-structure.md](/.structure/.instructions/create-structure.md)

→ Выполнить шаги из SSOT-инструкции.

## Чек-лист

→ См. [create-structure.md#чек-лист](/.structure/.instructions/create-structure.md#чек-лист)

## Примеры

/structure-create docs --description "Документация проекта"
/structure-create src/utils --description "Утилиты"
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-skill.py](./.scripts/validate-skill.py) | Валидация скиллов по стандарту | [validation-skill.md](./validation-skill.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/skill-create](/.claude/skills/skill-create/SKILL.md) | Создание скилла | [create-skill.md](./create-skill.md) |
| [/skill-modify](/.claude/skills/skill-modify/SKILL.md) | Изменение скилла | [modify-skill.md](./modify-skill.md) |
| [/skill-validate](/.claude/skills/skill-validate/SKILL.md) | Валидация скилла | [validation-skill.md](./validation-skill.md) |
