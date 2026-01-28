---
description: Индекс инструкций для написания скиллов
standard: .structure/.instructions/standard-readme.md
index: .claude/.instructions/skills/README.md
---

# Инструкции /.claude/.instructions/skills/

Стандарты и воркфлоу для написания скиллов Claude Code.

**Полезные ссылки:**
- [CLAUDE.md](/CLAUDE.md) — точка входа
- [Индекс скиллов](/.claude/skills/README.md)

---

## Оглавление

- [1. Объекты](#1-объекты)
- [2. Инструкции](#2-инструкции)
- [3. Скрипты](#3-скрипты)
- [4. Скиллы](#4-скиллы)
- [5. Связанные](#5-связанные)

---

## 1. Объекты

В этой папке описан 1 объект:

| Объект | Файлы | Описание |
|--------|-------|----------|
| **Скиллы** | `*-skill.md` | Как писать скиллы |

Каждый объект имеет 4 типа документов:

| Тип | Назначение |
|-----|------------|
| `standard-*` | Стандарт формата (КАК оформлять) |
| `validation-*` | Валидация (проверка соответствия) |
| `create-*` | Создание (воркфлоу) |
| `modify-*` | Изменение/удаление (воркфлоу) |

---

## 2. Инструкции

| Файл | Описание |
|------|----------|
| [standard-skill.md](./standard-skill.md) | Стандарт формата скиллов |
| [validation-skill.md](./validation-skill.md) | Валидация скиллов (коды K001-K031) |
| [create-skill.md](./create-skill.md) | Воркфлоу создания скилла |
| [modify-skill.md](./modify-skill.md) | Обновление, удаление, миграция |

### Ключевые правила

- Скилл = триггер + ссылка на SSOT-инструкцию
- Сокращённый формат: 40-60 строк (макс 80)
- Frontmatter: name, description, allowed-tools, category, triggers
- Именование: `{object}-{action}`, kebab-case, латиница

---

## 3. Скрипты

**Скрипты для этой области отсутствуют.**

---

## 4. Скиллы

Скиллы для работы со скиллами:

| Скилл | Назначение |
|-------|------------|
| [/skill-create](/.claude/skills/skill-create/SKILL.md) | Создание нового скилла |
| [/skill-update](/.claude/skills/skill-update/SKILL.md) | Обновление связанных скиллов |
| [/skill-delete](/.claude/skills/skill-delete/SKILL.md) | Удаление скилла |
| [/skill-migrate](/.claude/skills/skill-migrate/SKILL.md) | Переименование скилла |

---

## 5. Связанные

| Ресурс | Описание |
|--------|----------|
| [/.claude/skills/README.md](/.claude/skills/README.md) | Индекс скиллов (категории, триггеры) |
| [/.instructions/](/.instructions/README.md) | Как писать инструкции |
| [/specs/.instructions/](/specs/.instructions/README.md) | Как писать specs |

---

```
/.claude/.instructions/skills/
├── README.md              # Этот файл
├── standard-skill.md      # Стандарт скиллов
├── validation-skill.md    # Валидация скиллов
├── create-skill.md        # Создание скилла
└── modify-skill.md        # Изменение скилла
```

