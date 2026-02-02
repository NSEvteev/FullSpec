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
  - [standard_version](#standard_version-(для-файлов-cозданных-по-стандарту))
  - [index](#index)
- [2. Дополнительные поля для скиллов](#2-дополнительные-поля-для-скиллов)
- [3. Дополнительные поля для агентов](#3-дополнительные-поля-для-агентов)
- [4. Примеры](#4-примеры)

---

> **Шаблоны — из примеров SSOT.** При создании файлов использовать шаблоны из секции "Примеры". Запрещено придумывать свой формат.

---

## 1. Обязательные поля

| Поле | Назначение | Пример |
|------|------------|--------|
| `description` | Краткое описание документа | `SSOT структуры проекта` |
| `standard` | Стандарт формата документа | `.structure/.instructions/standard-readme.md` |
| `standard-version` | Версия стандарта формата документа | `v1.2` |
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
| Файл скилла (SKILL.md) | `.claude/.instructions/skills/standard-skill.md` |
| Файл агента (AGENT.md) | `.claude/.instructions/agents/standard-agent.md` |


### standard_version (для файлов, созданных по стандарту)

Версия стандарта, по которому создан документ. Позволяет отслеживать актуальность документов при обновлении стандартов.

| Поле | Назначение | Пример |
|------|------------|--------|
| `standard_version` | Версия стандарта на момент создания/обновления | `v1.2` |

**Правила:**
- Указывать версию стандарта из поля `version` в frontmatter стандарта
- При обновлении документа — проверить актуальность версии стандарта
- Если стандарт обновился — мигрировать документ и обновить `standard_version`


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

## 3. Дополнительные поля для агентов

Агенты (файлы `AGENT.md`) имеют расширенный frontmatter с полями для конфигурации модели, инструментов и хуков.

**SSOT:** [standard-agent.md § 3. Формат конфигурации](/.claude/.instructions/agents/standard-agent.md#3-формат-конфигурации)

---

## 4. Примеры

### Инструкция

```yaml
---
description: Валидация путей и формата файлов инструкций
standard: .instructions/standard-instruction.md
standard_version: v1.0
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
standard: .claude/.instructions/skills/standard-skill.md
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

