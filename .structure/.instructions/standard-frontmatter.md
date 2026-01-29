---
description: SSOT правил оформления frontmatter для .md файлов проекта
standard: .instructions/standard-instruction.md
index: .structure/.instructions/README.md
---

# Стандарт frontmatter

SSOT правил оформления frontmatter для всех `.md` файлов проекта.

**Полезные ссылки:**
- [Инструкции для .structure](./README.md)
- [Структура проекта](../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-links.md](./validation-links.md) (проверка frontmatter) |
| Создание | — |
| Модификация | — |

## Оглавление

- [1. Обязательные поля](#1-обязательные-поля)
  - [description](#description)
  - [standard](#standard)
  - [index](#index)
- [2. Дополнительные поля для скиллов](#2-дополнительные-поля-для-скиллов)
- [3. Примеры](#3-примеры)

---

## 1. Обязательные поля

| Поле | Назначение | Пример |
|------|------------|--------|
| `description` | Краткое описание документа | `SSOT структуры проекта` |
| `standard` | Стандарт формата документа | `.structure/.instructions/standard-readme.md` |
| `index` | README текущей папки | `.structure/.instructions/README.md` |

### description

Одно предложение для индексации и поиска.

**Правила:**
- Содержит **ключевые слова** (frontmatter, README, валидация)
- Указывает **область применения** (для .md файлов, для specs/)
- Описывает **что делает**, а не что это

**Примеры:**

| ✅ Хорошо | ❌ Плохо |
|----------|---------|
| `SSOT правил оформления frontmatter` | `Документация` |
| `Стандарт оформления README — формат и шаблон` | `Инструкция` |
| `Правила валидации ссылок между документами` | `Правила` |

### standard

Путь к стандарту формата, по которому создан документ.

**Правила:**
- Путь относительный от корня проекта (без ведущего `/`)
- Файл должен существовать

**Стандарты форматов:**

| Тип документа | standard |
|---------------|----------|
| README папки проекта | `.structure/.instructions/standard-readme.md` |
| README папки инструкций | `.structure/.instructions/standard-readme.md` |
| Файл инструкции | `.instructions/standard-instruction.md` |

### index

Путь к README текущей папки (индекс).

**Правила:**
- Путь относительный от корня проекта (без ведущего `/`)
- Для README файлов — ссылка на себя
- Файл должен существовать

**Примеры:**

| Файл | index |
|------|-------|
| `.instructions/validation.md` | `.instructions/README.md` |
| `.instructions/README.md` | `.instructions/README.md` |
| `.structure/.instructions/standard-frontmatter.md` | `.structure/.instructions/README.md` |

---

## 2. Дополнительные поля для скиллов

Скиллы (файлы `SKILL.md`) требуют дополнительных полей во frontmatter.

| Поле | Назначение | Пример |
|------|------------|--------|
| `name` | Имя скилла (kebab-case) | `structure-create` |
| `allowed-tools` | Разрешённые инструменты | `Read, Bash, Glob, Grep, Write, Edit` |
| `triggers` | Триггеры вызова | см. ниже |

### name

Уникальный идентификатор скилла в формате `{object}-{action}`.

**Правила:**
- Kebab-case
- Латиница
- Формат: `{объект}-{действие}`

### allowed-tools

Список инструментов, которые скилл может использовать.

**Доступные инструменты:**

| Инструмент | Описание |
|------------|----------|
| `Bash` | Выполнение команд в терминале |
| `Read` | Чтение файлов |
| `Write` | Создание файлов |
| `Edit` | Редактирование файлов |
| `Glob` | Поиск файлов по паттерну |
| `Grep` | Поиск в содержимом файлов |

### triggers

Триггеры для вызова скилла.

```yaml
triggers:
  commands:
    - /{skill-name}
  phrases:
    ru:
      - {фраза на русском}
    en:
      - {phrase in english}
```

---

## 3. Примеры

### Инструкция

```yaml
---
description: Валидация путей и формата файлов инструкций
standard: .instructions/standard-instruction.md
index: .instructions/README.md
---
```

### README

```yaml
---
description: Индекс инструкций для работы с инструкциями
standard: .structure/.instructions/standard-readme.md
index: .instructions/README.md
---
```

### Скилл

```yaml
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
    en:
      - create folder
---
```

