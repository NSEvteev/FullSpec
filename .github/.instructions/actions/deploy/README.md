---
description: Инструкции для Deploy workflow — стандарт деплоя, валидация, environments, dynamic discovery. Индекс документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.3
index: .github/.instructions/actions/deploy/README.md
---

# Инструкции /.github/.instructions/actions/deploy/

Deploy workflow — автоматический деплой при публикации Release.

**Полезные ссылки:**
- [Инструкции Actions](../README.md)
- [Standard Release](../../releases/standard-release.md)

**Содержание:** стандарт деплоя, валидация workflow.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для этой области |

```
/.github/.instructions/actions/deploy/
├── README.md                 # Этот файл (индекс)
├── standard-deploy.md        # Стандарт deploy workflow
└── validation-deploy.md      # Валидация deploy.yml
```

---

# 1. Стандарты

## 1.1. Стандарт деплоя

Правила deploy workflow: триггеры, dynamic service discovery, environments, rollback.

**Оглавление:**
- [Назначение](./standard-deploy.md#1-назначение)
- [Файлы и расположение](./standard-deploy.md#2-файлы-и-расположение)
- [Триггер](./standard-deploy.md#3-триггер)
- [Dynamic service discovery](./standard-deploy.md#4-dynamic-service-discovery)

**Инструкция:** [standard-deploy.md](./standard-deploy.md)

---

# 2. Воркфлоу

*Нет воркфлоу (deploy.yml создаётся при /init-project).*

---

# 3. Валидация

## 3.1. Валидация deploy.yml

Проверка deploy.yml на соответствие стандарту (D001-D008).

**Оглавление:**
- [Проверки](./validation-deploy.md#проверки)
- [Чек-лист](./validation-deploy.md#чек-лист)

**Инструкция:** [validation-deploy.md](./validation-deploy.md)

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-deploy.py](../../.scripts/validate-deploy.py) | Валидация deploy.yml (D001-D008) | [validation-deploy.md](./validation-deploy.md) |

---

# 5. Скиллы

*Нет скиллов.*
