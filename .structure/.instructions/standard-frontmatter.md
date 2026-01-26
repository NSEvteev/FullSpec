---
description: SSOT правил оформления frontmatter для .md файлов проекта
standard: .structure/.instructions/standard-readme.md
index: .structure/.instructions/README.md
---

# Frontmatter

SSOT правил оформления frontmatter для всех `.md` файлов проекта.

**Полезные ссылки:**
- [Инструкции для .structure](./README.md)
- [Структура проекта](../README.md)

---

## Обязательные поля

| Поле | Назначение | Пример |
|------|------------|--------|
| `description` | Краткое описание документа | `SSOT структуры проекта` |
| `standard` | Стандарт формата документа | `.structure/.instructions/standard-readme.md` |
| `index` | README текущей папки | `.structure/.instructions/README.md` |

---

## description

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

---

## standard

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

---

## index

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

## Пример

```yaml
---
description: Валидация путей и формата файлов инструкций
standard: .instructions/standard-instruction.md
index: .instructions/README.md
---
```

**Для README:**

```yaml
---
description: Индекс инструкций для работы с инструкциями
standard: .structure/.instructions/standard-readme.md
index: .instructions/README.md
---
```
