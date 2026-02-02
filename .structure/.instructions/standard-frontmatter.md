---
description: SSOT правил оформления frontmatter для .md файлов проекта
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .structure/.instructions/README.md
---

# Стандарт frontmatter

Версия стандарта: 1.1

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
  - [standard-version](#standard-version)
  - [index](#index)
- [2. Дополнительные поля для скиллов](#2-дополнительные-поля-для-скиллов)
- [3. Дополнительные поля для агентов](#3-дополнительные-поля-для-агентов)
- [4. Примеры](#4-примеры)
- [5. Обработка конфликтов версий](#5-обработка-конфликтов-версий)
- [6. Валидация frontmatter](#6-валидация-frontmatter)
- [7. Типичные ошибки](#7-типичные-ошибки)
- [8. Особые случаи](#8-особые-случаи)
- [9. Интеграция с Claude Code](#9-интеграция-с-claude-code)

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
| README папки проекта | `.structure/.instructions/standard-readme.md` (секция 2) |
| README папки инструкций | `.structure/.instructions/standard-readme.md` (секция 3) |
| Файл инструкции | `.instructions/standard-instruction.md` |
| Файл скилла (SKILL.md) | `.claude/.instructions/skills/standard-skill.md` |
| Файл агента (AGENT.md) | `.claude/.instructions/agents/standard-agent.md` |

> **Примечание:** README папки проекта и README папки инструкций используют один стандарт, но разные секции внутри него.


### standard-version

Версия стандарта, указанного в поле `standard`. Обязательно для всех файлов со стандартом.

Позволяет отслеживать актуальность документов при обновлении стандартов.

| Поле | Назначение | Пример |
|------|------------|--------|
| `standard-version` | Версия стандарта на момент создания/обновления | `v1.2` |

**Правила:**
- Указывать версию из заголовка `Версия стандарта: X.Y` в файле-стандарте
- При редактировании зависимого документа — сверить `standard-version` с актуальной версией стандарта
- Если версия стандарта изменилась — мигрировать документ по новому стандарту, обновить `standard-version`

**Синхронизация версий:**

| Скрипт | Назначение | Путь |
|--------|------------|------|
| `bump-standard-version.py` | Увеличить версию стандарта | [.instructions/.scripts/bump-standard-version.py](/.instructions/.scripts/bump-standard-version.py) |
| `sync-standard-version.py` | Синхронизировать зависимые файлы | [.instructions/.scripts/sync-standard-version.py](/.instructions/.scripts/sync-standard-version.py) |
| `check-version-drift.py` | Проверить расхождения версий | [.instructions/.scripts/check-version-drift.py](/.instructions/.scripts/check-version-drift.py) |

**Когда обновлять standard-version:**

| Действие | Кто обновляет |
|----------|---------------|
| Изменение стандарта → bump версии в стандарте | Автор стандарта (через `bump-standard-version.py`) |
| Миграция зависимого файла | Автор файла (вручную обновить frontmatter) |
| CI/CD проверка | Автоматически (`check-version-drift.py` в pipeline) |

**Пример workflow:**
```bash
# 1. После изменения стандарта — увеличить версию
python .instructions/.scripts/bump-standard-version.py .instructions/standard-instruction.md

# 2. Синхронизировать зависимые файлы
python .instructions/.scripts/sync-standard-version.py .instructions/standard-instruction.md

# 3. Проверить все версии (CI/CD)
python .instructions/.scripts/check-version-drift.py
```


### index

Путь к README текущей папки (индекс).

**Правила:**
- Путь относительный от корня проекта (без ведущего `/`)
- Для README файлов — путь к самому файлу (например, `.instructions/README.md` указывает на себя)
- Файл должен существовать

**Примеры:**

| Файл | index |
|------|-------|
| `.instructions/validation.md` | `.instructions/README.md` |
| `.instructions/README.md` | `.instructions/README.md` |
| `.structure/.instructions/standard-frontmatter.md` | `.structure/.instructions/README.md` |

**Граничные случаи:**

| Случай | Значение index |
|--------|----------------|
| Корневой `README.md` | `README.md` (ссылка на себя) |
| Файл в `.scripts/` (без README) | README родительской папки (`.instructions/README.md`) |
| `CLAUDE.md` | `README.md` (корневой индекс) |

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

**Примеры:**

| Объект | Действие | Имя скилла |
|--------|----------|------------|
| structure | create | `structure-create` |
| api-client | validate | `api-client-validate` |
| links | validate | `links-validate` |
| draft | validate | `draft-validate` |

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

**Формат значения:**

```yaml
# Вариант 1: строка (через запятую)
allowed-tools: Read, Bash, Glob, Grep, Write, Edit

# Вариант 2: YAML-массив
allowed-tools:
  - Read
  - Bash
  - Glob
```

**Правила:**
- Регистр: первая буква заглавная (`Read`, `Bash`, НЕ `read`, `bash`)
- Все инструменты: не указывать поле (по умолчанию все доступны)

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
standard-version: v1.0
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
standard-version: v1.0
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

### Агент

```yaml
---
name: todo-finder
description: Поиск TODO/FIXME комментариев в кодовой базе
standard: .claude/.instructions/agents/standard-agent.md
standard-version: v1.1
index: .claude/.instructions/agents/README.md
type: explore
model: haiku
tools: Read, Grep, Glob
permissionMode: plan
max_turns: 10
version: v1.0
---
```

---

## 5. Обработка конфликтов версий

**Что делать при расхождении версий:**

| Ситуация | Действие |
|----------|----------|
| Стандарт обновился (v1.0 → v1.1) | Автор стандарта запускает `sync-standard-version.py` ИЛИ создаёт миграционную инструкцию |
| Файл со старой версией | Использовать можно, но рекомендуется обновить при следующем редактировании |
| Критичное изменение стандарта | Автор стандарта создаёт задачи на миграцию всех зависимых файлов |

---

## 6. Валидация frontmatter

**Автоматическая проверка:**
- Выполняется через [validation-links.md](./validation-links.md) (проверяет ссылки в полях `standard`, `index`)

**Ручная проверка (если автоматика недоступна):**
- [ ] Все обязательные поля присутствуют
- [ ] Значения полей соответствуют типу документа
- [ ] Файлы, указанные в `standard` и `index`, существуют
- [ ] Версия `standard-version` соответствует версии в файле-стандарте

---

## 7. Типичные ошибки

| Ошибка | Почему неправильно | Как исправить |
|--------|-------------------|---------------|
| `standard: /standard-instruction.md` | Ведущий `/` запрещён | `standard: .instructions/standard-instruction.md` |
| `standard_version: v1.0` | Подчёркивание вместо дефиса | `standard-version: v1.0` |
| `index: .instructions/` | Ссылка на папку без файла | `index: .instructions/README.md` |
| `allowed-tools: read, bash` | Строчные буквы | `allowed-tools: Read, Bash` |
| Отсутствие `description` | Обязательное поле | Добавить `description: ...` |

---

## 8. Особые случаи

### Файлы в корне проекта

| Файл | standard | index |
|------|----------|-------|
| `CLAUDE.md` | `.instructions/standard-instruction.md` | `README.md` |
| `CONTRIBUTING.md` | `.instructions/standard-instruction.md` | `README.md` |
| `README.md` | `.structure/.instructions/standard-readme.md` | `README.md` (ссылка на себя) |

### Файлы вне стандартных папок

- Если папка имеет `.instructions/` → использовать стандарты из неё
- Если нет `.instructions/` → ссылаться на ближайший родительский стандарт
- Технические файлы (`.gitignore`, `package.json`) → frontmatter не требуется

---

## 9. Интеграция с Claude Code

**Использование frontmatter:**

| Поле | Как использует Claude Code |
|------|----------------------------|
| `description` | Индексация для поиска по документам |
| `standard` | Автоподгрузка стандарта при работе с файлом |
| `index` | Построение навигации по проекту |
| `allowed-tools` | Ограничение инструментов для скиллов |

