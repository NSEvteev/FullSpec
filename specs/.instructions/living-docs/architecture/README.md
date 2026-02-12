---
description: Инструкции для фиксированных файлов архитектуры — существование, структура, обязательные секции, валидация.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: specs/.instructions/living-docs/architecture/README.md
---

# /specs/.instructions/living-docs/architecture/ — Фиксированные файлы архитектуры

Стандарт существования и структуры фиксированных файлов `specs/architecture/` (system/ и domains/). Управляет обязательными секциями, frontmatter и валидацией. Обновление файлов регулируется [standard-service.md](../service/standard-service.md).

**Полезные ссылки:**
- [Живые документы](../README.md)
- [Инструкции /specs/](../../README.md)

**Содержание:** стандарт структуры, валидация, скрипт проверки.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Валидация](#2-валидация) | — | Проверка согласованности |
| [3. Скрипты](#3-скрипты) | — | Автоматизация |

```
/specs/.instructions/living-docs/architecture/
├── standard-architecture.md   # Стандарт фиксированных файлов
├── validation-architecture.md # Валидация
└── README.md                  # Этот файл (индекс)
```

---

# 1. Стандарты

## 1.1. Стандарт фиксированных файлов архитектуры

Существование, структура и обязательные секции для 4 фиксированных файлов `specs/architecture/`.

**Оглавление:**
- [Назначение](./standard-architecture.md#1-назначение)
- [Расположение и именование](./standard-architecture.md#2-расположение-и-именование)
- [Frontmatter](./standard-architecture.md#3-frontmatter)
- [Обязательные секции](./standard-architecture.md#4-обязательные-секции)
- [Шаблоны](./standard-architecture.md#5-шаблоны)
- [Чек-лист качества](./standard-architecture.md#6-чек-лист-качества)

**Инструкция:** [standard-architecture.md](./standard-architecture.md)

---

# 2. Валидация

## 2.1. Валидация фиксированных файлов архитектуры

Проверка существования, frontmatter, обязательных секций и согласованности с services/.

**Оглавление:**
- [Когда валидировать](./validation-architecture.md#1-когда-валидировать)
- [Автоматическая валидация](./validation-architecture.md#2-автоматическая-валидация)
- [Коды ошибок](./validation-architecture.md#3-коды-ошибок)
- [Чек-лист](./validation-architecture.md#4-чек-лист)
- [Скрипты](./validation-architecture.md#5-скрипты)

**Инструкция:** [validation-architecture.md](./validation-architecture.md)

---

# 3. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-architecture.py](../../.scripts/validate-architecture.py) | Валидация фиксированных файлов + согласованность services/ | [validation-architecture.md](./validation-architecture.md) |
