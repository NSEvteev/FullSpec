---
description: Индекс инструкций для написания инструкций и скриптов
standard: .structure/.instructions/standard-readme.md
index: .instructions/README.md
---

# Инструкции /.instructions/

Стандарты и воркфлоу для написания инструкций и скриптов автоматизации.

**Полезные ссылки:**
- [CLAUDE.md](/CLAUDE.md) — точка входа
- [Структура проекта](/.structure/README.md)

---

## Оглавление

- [1. Объекты](#1-объекты)
- [2. Инструкции](#2-инструкции)
- [3. Скрипты](#3-скрипты)
- [4. Скиллы](#4-скиллы)
- [5. Связанные](#5-связанные)

---

## 1. Объекты

В этой папке описаны 2 объекта:

| Объект | Файлы | Описание |
|--------|-------|----------|
| **Инструкции** | `*-instruction.md` | Как писать инструкции |
| **Скрипты** | `*-script.md` | Как писать скрипты автоматизации |

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
| [standard-instruction.md](./standard-instruction.md) | Стандарт формата инструкций |
| [validation-instruction.md](./validation-instruction.md) | Валидация инструкций (коды I001-I031) |
| [create-instruction.md](./create-instruction.md) | Воркфлоу создания инструкции |
| [modify-instruction.md](./modify-instruction.md) | Обновление, деактивация, миграция |

### Ключевые правила

- Инструкции = ТОЛЬКО стандарты (КАК делать)
- README описывает структуру (ЧТО есть)
- Frontmatter обязателен: `description`, `standard`, `index`
- Именование: kebab-case, латиница

---

## 3. Скрипты

| Файл | Описание |
|------|----------|
| [standard-script.md](./standard-script.md) | Стандарт формата скриптов |
| [validation-script.md](./validation-script.md) | Валидация скриптов (коды S001-S031) |
| [create-script.md](./create-script.md) | Воркфлоу создания скрипта |
| [modify-script.md](./modify-script.md) | Обновление, рефакторинг, удаление |

### Ключевые правила

- Документация в docstring (не frontmatter)
- Shebang обязателен: `#!/usr/bin/env python3`
- UTF-8 для Windows в `main()`
- Exit codes: 0 = успех, 1 = ошибка

---

## 4. Скиллы

**Скиллы для этой области отсутствуют.**

Воркфлоу описаны в инструкциях:
- [create-instruction.md](./create-instruction.md) — создание
- [modify-instruction.md](./modify-instruction.md) — обновление, деактивация

---

## 5. Связанные

| Ресурс | Описание |
|--------|----------|
| [/.claude/.instructions/skills/](/.claude/.instructions/skills/README.md) | Как писать скиллы |
| [/specs/.instructions/](/specs/.instructions/README.md) | Как писать specs |
| [/.structure/.instructions/](/.structure/.instructions/README.md) | Как управлять структурой |

---

```
/.instructions/
├── README.md                    # Этот файл
├── standard-instruction.md      # Стандарт инструкций
├── validation-instruction.md    # Валидация инструкций
├── create-instruction.md        # Создание инструкции
├── modify-instruction.md        # Изменение инструкции
├── standard-script.md           # Стандарт скриптов
├── validation-script.md         # Валидация скриптов
├── create-script.md             # Создание скрипта
└── modify-script.md             # Изменение скрипта
```
