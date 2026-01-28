# Драфт: Переработка флоу работы с инструкциями

**Дата:** 2026-01-28
**Статус:** DRAFT
**Связано:** [align-structure-instructions.md](./align-structure-instructions.md) (Фаза 5)

---

## Контекст

Этот драфт — детализация **Фазы 5** из `align-structure-instructions.md`, но с расширенным скоупом: не только скрипты, а весь объект "Инструкции".

### Иерархия компонентов (из align-structure-instructions.md)

```
┌─────────────────────────────────────────────────────────┐
│                    ИНСТРУКЦИИ (SSOT)                    │
│                                                         │
│  ┌──────────┐  ┌───────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Стандарт │  │ Валидация │  │Создание │  │Изменение│ │
│  │(справка) │  │(воркфлоу) │  │(воркфлоу)│  │(воркфлоу)│ │
│  └────┬─────┘  └─────┬─────┘  └────┬────┘  └────┬────┘ │
└───────┼──────────────┼─────────────┼───────────┼───────┘
        │              │             │           │
        │              ▼             ▼           ▼
        │         ┌──────────────────────────────────────┐
        │         │              СКРИПТЫ                 │
        │         │      (автоматизация рутины)          │
        │         └──────────────────────────────────────┘
        │              │             │           │
        │              ▼             ▼           ▼
        │         ┌──────────────────────────────────────┐
        │         │              СКИЛЛЫ                  │
        │         │   (триггер + параметры + → SSOT)     │
        │         └──────────────────────────────────────┘
        │              │             │           │
        ▼              ▼             ▼           ▼
┌─────────────────────────────────────────────────────────┐
│                       RULES                             │
│              (автозагрузка по paths)                    │
│                                                         │
│  - Ссылаются на скиллы (для воркфлоу)                  │
│  - Могут ссылаться на стандарты (справочно)            │
└─────────────────────────────────────────────────────────┘
```

### Принцип связей

| Тип инструкции | Скрипт | Скилл | Rule ссылается на |
|----------------|--------|-------|-------------------|
| Стандарт | — | — | Стандарт напрямую |
| Валидация | ✅ | ✅ | Скилл |
| Создание | ✅ | ✅ | Скилл |
| Изменение | ✅ | ✅ | Скилл |

**Принцип:** Каждый уровень ссылается на предыдущий, не дублирует.

### Облегчённый формат скиллов

Скилл **НЕ дублирует** шаги из инструкции. Скилл содержит только:
- Frontmatter с триггерами
- Ссылка на SSOT-инструкцию
- Формат вызова
- "→ Выполнить шаги из SSOT"
- Примеры

---

## 1. Проблема

Текущая папка `/.instructions/` не соответствует целевой концепции документирования объектов.

### Текущее состояние (устаревшее)

```
/.instructions/
├── README.md               # 11 секций (нестандартно)
├── structure.md            # Расположение
├── types.md                # Типы (standard/project)
├── validation.md           # Валидация
├── statuses.md             # Статусы в README
├── workflow.md             # Жизненный цикл (обзор)
├── workflow-create.md      # CREATE
├── workflow-update.md      # UPDATE
├── workflow-deactivate.md  # DEACTIVATE
├── patterns.md             # Паттерны поиска
├── examples.md             # Правила примеров
└── standard-instruction.md # Стандарт формата
```

**Проблемы:**
1. **Имена файлов** — нет типизированных префиксов (standard-, validation-, create-, modify-)
2. **README** — 11 секций вместо 5 фиксированных
3. **Смешение** — стандарты и воркфлоу на одном уровне без структуры
4. **Дублирование** — workflow.md + отдельные workflow-*.md
5. **Устаревшие концепции** — statuses.md (система статусов в README не используется)

---

## 2. Целевое состояние

### 2.1. Объект и свойства

```
Объект: Инструкции (instructions)
├── Свойство: Файл (формат, структура документа)
├── Свойство: Frontmatter (метаданные)
├── Свойство: Секции (содержание документа)
└── Свойство: Расположение (где хранить)
```

### 2.2. Матрица документов

| Свойство | standard- | validation- | create- | modify- |
|----------|:---------:|:-----------:|:-------:|:-------:|
| **Файл** | ✅ `standard-instruction` | ✅ `validation-instruction` | ✅ `create-instruction` | ✅ `modify-instruction` |
| **Frontmatter** | (часть standard-instruction) | (часть validation-instruction) | — | — |
| **Секции** | (часть standard-instruction) | (часть validation-instruction) | — | — |
| **Расположение** | (часть standard-instruction) | — | — | — |

### 2.3. Целевая структура (8 файлов + README)

```
/.instructions/
├── README.md                  # Индекс (5 секций)
│
├── # Объект: Инструкции
├── standard-instruction.md    # Стандарт формата инструкции
├── validation-instruction.md  # Валидация инструкций
├── create-instruction.md      # Создание инструкции
├── modify-instruction.md      # Изменение/деактивация
│
├── # Объект: Скрипты
├── standard-script.md         # Стандарт формата скрипта
├── validation-script.md       # Валидация скриптов
├── create-script.md           # Создание скрипта
├── modify-script.md           # Изменение скрипта
│
└── .scripts/
    └── validate-instruction.py
```

### 2.4. Два объекта документирования

```
/.instructions/ документирует 2 объекта:

Объект: Инструкции (instruction)
├── standard-instruction.md    # Формат, frontmatter, секции, расположение
├── validation-instruction.md  # Проверка формата
├── create-instruction.md      # Создание новой инструкции
└── modify-instruction.md      # Обновление, деактивация, миграция

Объект: Скрипты (script)
├── standard-script.md         # Формат: shebang, docstring, структура
├── validation-script.md       # Проверка формата скрипта
├── create-script.md           # Создание нового скрипта
└── modify-script.md           # Изменение скрипта
```

**Примечание:** Скрипты без frontmatter — метаданные в docstring.

---

## 3. План миграции файлов

### 3.1. Что куда переносится

| Старый файл | Действие | Целевой файл |
|-------------|----------|--------------|
| `standard-instruction.md` | **Расширить** | `standard-instruction.md` |
| `structure.md` | Интегрировать → | `standard-instruction.md` |
| `types.md` | Интегрировать → | `standard-instruction.md` |
| `validation.md` | **Переименовать** | `validation-instruction.md` |
| `workflow-create.md` | **Переименовать** | `create-instruction.md` |
| `workflow-update.md` | Объединить → | `modify-instruction.md` |
| `workflow-deactivate.md` | Объединить → | `modify-instruction.md` |
| `workflow.md` | **Удалить** | — (обзор не нужен) |
| `statuses.md` | **Удалить** | — (устарело) |
| `patterns.md` | Интегрировать → | `modify-instruction.md` |
| `examples.md` | **Удалить** | — (общие правила) |

### 3.2. Новое содержание файлов

#### standard-instruction.md (расширенный)

```markdown
# Стандарт инструкций

## Оглавление
- [1. Назначение](#1-назначение)
- [2. Расположение](#2-расположение)
- [3. Типы инструкций](#3-типы-инструкций)
- [4. Формат файла](#4-формат-файла)
- [5. Frontmatter](#5-frontmatter)
- [6. Секции документа](#6-секции-документа)
- [7. Примеры](#7-примеры)

Источники:
- structure.md (секция 2)
- types.md (секция 3)
- текущий standard-instruction.md (секции 4-6)
```

#### validation-instruction.md (из validation.md)

```markdown
# Валидация инструкций

## Оглавление
- [1. Когда валидировать](#1-когда-валидировать)
- [2. Что проверяется](#2-что-проверяется)
- [3. Коды ошибок](#3-коды-ошибок)
- [4. Чек-лист](#4-чек-лист)
```

#### create-instruction.md (из workflow-create.md)

```markdown
# Создание инструкции

## Оглавление
- [1. Когда создавать](#1-когда-создавать)
- [2. Шаги создания](#2-шаги-создания)
- [3. Чек-лист](#3-чек-лист)
```

#### modify-instruction.md (объединение)

```markdown
# Изменение инструкции

## Оглавление
- [1. Обновление инструкции](#1-обновление-инструкции)
- [2. Деактивация инструкции](#2-деактивация-инструкции)
- [3. Миграция инструкции](#3-миграция-инструкции)
- [4. Паттерны поиска ссылок](#4-паттерны-поиска-ссылок)
- [5. Чек-лист](#5-чек-лист)

Источники:
- workflow-update.md (секция 1)
- workflow-deactivate.md (секция 2)
- workflow.md → MIGRATE (секция 3)
- patterns.md (секция 4)
```

---

## 4. Новый README

### 4.1. Структура (5 фиксированных секций)

```markdown
---
description: Индекс инструкций для работы с инструкциями проекта
standard: .structure/.instructions/standard-readme.md
index: .instructions/README.md
---

# Инструкции /.instructions/

Индекс инструкций для работы с инструкциями проекта.

**Полезные ссылки:**
- [Структура проекта](/.structure/README.md)

**Содержание:** стандарт формата, создание, изменение, валидация.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | standard-instruction.md | Формат и правила |
| [2. Воркфлоу](#2-воркфлоу) | create-, modify- | Создание и изменение |
| [3. Валидация](#3-валидация) | validation-instruction.md | Проверка |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для области |

```
/.instructions/
├── README.md                  # Этот файл (индекс)
├── standard-instruction.md    # Стандарт формата
├── validation-instruction.md  # Валидация
├── create-instruction.md      # Создание
├── modify-instruction.md      # Изменение/деактивация
└── .scripts/
    └── validate-instruction.py
```

---

# 1. Стандарты

## 1.1. Стандарт инструкций

Формат, структура и правила оформления инструкций.

**Оглавление:**
- [Назначение](./standard-instruction.md#1-назначение)
- [Расположение](./standard-instruction.md#2-расположение)
- [Типы](./standard-instruction.md#3-типы-инструкций)
- [Формат файла](./standard-instruction.md#4-формат-файла)

**Инструкция:** [standard-instruction.md](./standard-instruction.md)

---

# 2. Воркфлоу

## 2.1. Создание инструкции

Воркфлоу создания новой инструкции в проекте.

**Оглавление:**
- [Когда создавать](./create-instruction.md#1-когда-создавать)
- [Шаги создания](./create-instruction.md#2-шаги-создания)
- [Чек-лист](./create-instruction.md#3-чек-лист)

**Инструкция:** [create-instruction.md](./create-instruction.md)

## 2.2. Изменение инструкции

Обновление, деактивация и миграция инструкций.

**Оглавление:**
- [Обновление](./modify-instruction.md#1-обновление-инструкции)
- [Деактивация](./modify-instruction.md#2-деактивация-инструкции)
- [Миграция](./modify-instruction.md#3-миграция-инструкции)

**Инструкция:** [modify-instruction.md](./modify-instruction.md)

---

# 3. Валидация

## 3.1. Валидация инструкций

Проверка формата и согласованности инструкций.

**Оглавление:**
- [Когда валидировать](./validation-instruction.md#1-когда-валидировать)
- [Что проверяется](./validation-instruction.md#2-что-проверяется)
- [Коды ошибок](./validation-instruction.md#3-коды-ошибок)

**Инструкция:** [validation-instruction.md](./validation-instruction.md)

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-instruction.py](./.scripts/validate-instruction.py) | Валидация формата | [validation-instruction.md](./validation-instruction.md) |

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/instruction-create](/.claude/skills/instruction-create/SKILL.md) | Создание инструкции | [create-instruction.md](./create-instruction.md) |
| [/instruction-update](/.claude/skills/instruction-update/SKILL.md) | Проверка соответствия | [modify-instruction.md](./modify-instruction.md) |
| [/instruction-deactivate](/.claude/skills/instruction-deactivate/SKILL.md) | Деактивация | [modify-instruction.md](./modify-instruction.md) |
```

---

## 5. Сравнение: было → стало

### Визуализация миграции

```
БЫЛО (11 файлов):                             СТАЛО (8 файлов):

/.instructions/                               /.instructions/
├── README.md ─────────────────────────────→ ├── README.md (5 секций)
│                                            │
│                                            │ # Объект: Инструкции
├── standard-instruction.md ───────┐         │
├── structure.md ──────────────────┼───────→ ├── standard-instruction.md
├── types.md ──────────────────────┘         │
├── validation.md ─────────────────────────→ ├── validation-instruction.md
├── workflow-create.md ────────────────────→ ├── create-instruction.md
├── workflow.md ───────────┐                 │
├── workflow-update.md ────┼───────────────→ ├── modify-instruction.md
├── workflow-deactivate.md ┼                 │
├── patterns.md ───────────┘                 │
│                                            │ # Объект: Скрипты (NEW)
│                                            ├── standard-script.md
│                                            ├── validation-script.md
│                                            ├── create-script.md
│                                            ├── modify-script.md
│                                            │
├── statuses.md ───────────────────────────→ УДАЛИТЬ (устарело)
├── examples.md ───────────────────────────→ УДАЛИТЬ (общие правила)
│                                            │
└── .scripts/                                └── .scripts/
    └── *.py ──────────────────────────────→     └── *.py (без изменений)
```

### Таблица соответствия

| Старый файл | Судьба | Новый файл | Секция |
|-------------|--------|------------|--------|
| standard-instruction.md | **Расширить** | standard-instruction.md | Формат, frontmatter, секции |
| structure.md | Интегрировать | standard-instruction.md | Расположение |
| types.md | Интегрировать | standard-instruction.md | Типы (standard/project) |
| validation.md | **Переименовать** | validation-instruction.md | — |
| workflow-create.md | **Переименовать** | create-instruction.md | — |
| workflow.md | Удалить | — | — (обзор не нужен) |
| workflow-update.md | Объединить | modify-instruction.md | Обновление |
| workflow-deactivate.md | Объединить | modify-instruction.md | Деактивация |
| patterns.md | Интегрировать | modify-instruction.md | Паттерны поиска |
| statuses.md | **Удалить** | — | — (устарело) |
| examples.md | **Удалить** | — | — (общие правила) |

---

## 6. Воркфлоу создания папки инструкций

При создании **любой** папки инструкций (не только `/.instructions/`) используется следующий воркфлоу:

### Шаги

```
1. Определить объекты
   └── Какие объекты документируются в этой папке инструкций?

2. Создать драфт
   └── Обсудить объекты и их свойства
   └── Определить какие файлы нужны (4 или меньше на объект)

3. Создать дерево документов
   └── Для каждого объекта создать все его файлы одним скопом
   └── (standard-, validation-, create-, modify-)

4. Ревью решения
   └── Все ли вопросы учтены?
   └── Нужны ли скрипты для процессов?

5. Создать скрипты
   └── Для валидации, создания, модификации
   └── Только если нужны

6. Повторить ревью (шаг 4)
   └── Пока не нужны новые скрипты

7. Создать скиллы
   └── Облегчённый формат (→ SSOT)

8. Создать rules
   └── Для автозагрузки по paths
```

### Диаграмма

```
┌──────────────────┐
│ 1. Определить    │
│    объекты       │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 2. Создать драфт │
│    (обсуждение)  │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 3. Создать       │
│    документы     │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 4. Ревью         │◄────────┐
└────────┬─────────┘         │
         ▼                   │
    ┌─────────┐              │
    │ Нужны   │── Да ──►┌────┴───────────┐
    │скрипты? │         │ 5. Создать     │
    └────┬────┘         │    скрипты     │
         │ Нет          └────────────────┘
         ▼
┌──────────────────┐
│ 7. Создать       │
│    скиллы        │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 8. Создать       │
│    rules         │
└──────────────────┘
```

---

## 7. План выполнения для /.instructions/

> **Примечание:** Новые файлы временно создаём в `/.instructions_new/` для сравнения с текущими.

### Фаза 1: Создание файлов для объекта "Инструкции"

> Создаём в `/.instructions_new/`

1. [ ] Создать `standard-instruction.md` (расширенный)
   - Объединить: structure.md + types.md + текущий standard-instruction.md
2. [ ] Создать `validation-instruction.md`
   - Переработать validation.md
3. [ ] Создать `create-instruction.md`
   - Переработать workflow-create.md
4. [ ] Создать `modify-instruction.md`
   - Объединить: workflow-update.md + workflow-deactivate.md + patterns.md + MIGRATE

### Фаза 2: Создание файлов для объекта "Скрипты"

> Создаём в `/.instructions_new/`

5. [ ] Создать `standard-script.md`
   - Формат: shebang, docstring (описание, использование, примеры), структура
6. [ ] Создать `validation-script.md`
   - Проверка формата скрипта
7. [ ] Создать `create-script.md`
   - Воркфлоу создания нового скрипта
8. [ ] Создать `modify-script.md`
   - Воркфлоу изменения скрипта

### Фаза 3: Ревью и README

> Создаём в `/.instructions_new/`

9. [ ] Ревью: все ли вопросы учтены?
10. [ ] Создать README.md (5 фиксированных секций, 2 объекта)

### Фаза 4: Создание скриптов

> Создаём в `/.instructions_new/.scripts/`

11. [ ] Ревью: нужны ли скрипты?
12. [ ] Создать скрипты валидации (если нужны)
13. [ ] Повторить ревью → пока скрипты не нужны

### Фаза 5: Миграция из временной папки

14. [ ] Сравнить `/.instructions_new/` с `/.instructions/`
15. [ ] Удалить старые файлы из `/.instructions/`:
    - structure.md, types.md, validation.md
    - workflow.md, workflow-create.md, workflow-update.md, workflow-deactivate.md
    - patterns.md, examples.md, statuses.md
16. [ ] Переместить файлы из `/.instructions_new/` → `/.instructions/`
17. [ ] Удалить `/.instructions_new/`

### Фаза 6: Удаление скиллов

18. [ ] Удалить `/.claude/skills/instruction-create/`
19. [ ] Удалить `/.claude/skills/instruction-update/`
20. [ ] Удалить `/.claude/skills/instruction-deactivate/`
21. [ ] Обновить `/.claude/skills/README.md`
22. [ ] Обновить `CLAUDE.md` (убрать instruction-* из списка)

### Фаза 7: Обновление ссылок

23. [ ] Запустить `/links-validate`
24. [ ] Исправить битые ссылки

### Фаза 8: Скиллы (отложено)

25. [ ] Создать новые скиллы (облегчённый формат → SSOT)

### Фаза 9: Rules (отложено)

26. [ ] Создать `/.claude/rules/instructions.md`

**Концепция Rule:**

```
Пользователь работает с .instructions/
         ↓
Rule автоматически загружается (paths match)
         ↓
Rule: "Используй /instruction-create или /instruction-deactivate"
         ↓
Skill читает SSOT-инструкцию и выполняет
```

**Формат rule:**

```markdown
---
paths:
  - ".instructions/**"
  - "**/.instructions/**"
---

# Инструкции

При создании инструкции:
→ `/instruction-create`

При изменении инструкции:
→ `/instruction-update` (проверка соответствия)

При деактивации инструкции:
→ `/instruction-deactivate`
```

---

## 8. Скиллы (отложено)

**Решение:** Удалить текущие скиллы. Новые создадим после миграции инструкций.

Формат новых скиллов — облегчённый (SSOT-ссылка, без дублирования шагов).

---

## 9. Решения по открытым вопросам

### Q1: Что делать со скриптами? ✅

**Решение:** Создать папку `/.instructions/.scripts/` (по аналогии с `.structure/.instructions/.scripts/`)

### Q2: Скиллы instruction-* ✅

**Решение:** Удалить текущие скиллы. Новые создадим позже, после миграции инструкций.

Скиллы на удаление:
- `/.claude/skills/instruction-create/`
- `/.claude/skills/instruction-update/`
- `/.claude/skills/instruction-deactivate/`

### Q3: Нужен ли скилл /instruction-migrate? ✅

**Решение:** Скиллы не нужны сейчас. Фокус на инструкциях.

### Q4: Что делать с шаблонами? ✅

**Решение:** Оставить `/.claude/templates/instructions/`, но потом переделать и переименовать в новой структуре.

---

## 10. Связь с Фазой 5 (align-structure-instructions.md)

Фаза 5 из `align-structure-instructions.md` планировала:

```
Объект: Инструкции
└── Свойство: Скрипты (.scripts/)
    ├── standard-scripts.md
    ├── validation-scripts.md
    ├── create-scripts.md
    └── modify-scripts.md
```

**Решение:** Скрипты — это **отдельный объект**, а не свойство инструкций.

Итого в `/.instructions/` будет **2 объекта**:
1. **Инструкции** — 4 файла (standard-, validation-, create-, modify-instruction.md)
2. **Скрипты** — 4 файла (standard-, validation-, create-, modify-script.md)

**Примечание:** Скрипты без frontmatter — метаданные в docstring.

---

## 11. Связанные документы

- [align-structure-instructions.md](./align-structure-instructions.md) — общий план выравнивания (Фазы 1-5)
- [object-documentation-structure.md](./object-documentation-structure.md) — концепция 4 типов документов
- [/.structure/.instructions/standard-readme.md](/.structure/.instructions/standard-readme.md) — стандарт README
- [/.structure/.instructions/README.md](/.structure/.instructions/README.md) — эталон README инструкций
