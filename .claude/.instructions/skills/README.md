---
description: Индекс инструкций для написания скиллов
standard: .structure/.instructions/standard-readme.md
index: .claude/.instructions/skills/README.md
---

# Инструкции /.claude/.instructions/skills/

Индекс инструкций для написания скиллов Claude Code.

**Полезные ссылки:**
- [Индекс скиллов](/.claude/skills/README.md)
- [CLAUDE.md](/CLAUDE.md) — точка входа

**Содержание:** стандарт скиллов, воркфлоу создания и изменения, валидация.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [Стандарты](#стандарты) | — | Форматы и правила |
| [Воркфлоу](#воркфлоу) | — | Создание и изменение |
| [Валидация](#валидация) | — | Проверка согласованности |
| [Скрипты](#скрипты) | — | Автоматизация |
| [Скиллы](#скиллы) | — | Скиллы для этой области |

```
/.claude/.instructions/skills/
├── README.md              # Этот файл (индекс)
├── standard-skill.md      # Стандарт скиллов
├── create-skill.md        # Создание скилла
├── modify-skill.md        # Изменение скилла
├── validation-skill.md    # Валидация скиллов
└── .scripts/              # Скрипты автоматизации
```

---

## Стандарты

### Стандарт скиллов

Формат и структура файлов SKILL.md в сокращённом формате.

**Оглавление:**
- [Назначение](./standard-skill.md#1-назначение)
- [Расположение](./standard-skill.md#2-расположение)
- [Frontmatter](./standard-skill.md#3-frontmatter)
- [Секции документа](./standard-skill.md#4-секции-документа)

**Инструкция:** [standard-skill.md](./standard-skill.md)

---

## Воркфлоу

### Создание скилла

Воркфлоу создания нового скилла в сокращённом формате.

**Оглавление:**
- [Принципы](./create-skill.md#принципы)
- [Шаги](./create-skill.md#шаги)
- [Чек-лист](./create-skill.md#чек-лист)

**Инструкция:** [create-skill.md](./create-skill.md)

### Изменение скилла

Воркфлоу обновления, деактивации и миграции скиллов.

**Оглавление:**
- [Обновление](./modify-skill.md#обновление)
- [Деактивация](./modify-skill.md#деактивация)
- [Миграция](./modify-skill.md#миграция)

**Инструкция:** [modify-skill.md](./modify-skill.md)

---

## Валидация

### Валидация скиллов

Проверка соответствия скиллов сокращённому формату (коды K001-K031).

**Оглавление:**
- [Когда валидировать](./validation-skill.md#когда-валидировать)
- [Коды ошибок](./validation-skill.md#коды-ошибок)
- [Чек-лист](./validation-skill.md#чек-лист)

**Инструкция:** [validation-skill.md](./validation-skill.md)

---

## Скрипты

| Скрипт | Назначение |
|--------|------------|
| [validate-skill.py](./.scripts/validate-skill.py) | Валидация скиллов по стандарту |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/skill-create](/.claude/skills/skill-create/SKILL.md) | Создание нового скилла | [create-skill.md](./create-skill.md) |
| [/skill-modify](/.claude/skills/skill-modify/SKILL.md) | Изменение скилла (обновление, деактивация, миграция) | [modify-skill.md](./modify-skill.md) |
| [/skill-validate](/.claude/skills/skill-validate/SKILL.md) | Валидация скилла | [validation-skill.md](./validation-skill.md) |
