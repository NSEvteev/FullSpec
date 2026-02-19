---
description: Индекс инструкций для specs/
standard: .structure/.instructions/standard-readme.md
index: specs/.instructions/README.md
---

# Инструкции /specs/

Индекс инструкций для папки specs/.

**Полезные ссылки:**
- [specs/](../README.md)

**Содержание:** документация для поставки (docs/), типы документов, межсервисная информация.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | standard-docs.md | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | validation-docs.md | Проверка согласованности |
| [4. Per-document стандарты](#4-per-document-стандарты) | docs/*/ | Стандарт каждого типа документа |
| [5. Скрипты](#5-скрипты) | validate-docs.py | Автоматизация |
| [6. Скиллы](#6-скиллы) | — | Скиллы для этой области |

```
/specs/.instructions/
├── .scripts/
│   ├── validate-docs-overview.py     # Валидация формата docs/.system/overview.md
│   ├── validate-docs-readme.py       # Валидация формата docs/README.md
│   └── validate-docs.py              # Валидация структуры docs/
├── docs/
│   ├── conventions/
│   │   └── standard-conventions.md   # Стандарт docs/.system/conventions.md
│   ├── overview/
│   │   ├── modify-overview.md        # Воркфлоу модификации overview.md
│   │   ├── standard-overview.md      # Стандарт docs/.system/overview.md
│   │   └── validation-overview.md    # Валидация docs/.system/overview.md
│   └── readme/
│       ├── standard-readme.md        # Стандарт docs/README.md
│       └── validation-readme.md      # Валидация docs/README.md
├── standard-docs.md                  # Мета-стандарт документации для поставки (docs/)
├── validation-docs.md                # Валидация наличия обязательных документов docs/
└── README.md                         # Этот файл (индекс)
```

---

# 1. Стандарты

| Инструкция | Описание |
|------------|----------|
| [standard-docs.md](./standard-docs.md) | Стандарт документации для поставки (контур docs/) — структура, типы документов, принципы |

---

# 2. Воркфлоу

*Нет воркфлоу.*

---

# 3. Валидация

| Инструкция | Описание |
|------------|----------|
| [validation-docs.md](./validation-docs.md) | Валидация структуры docs/ — наличие обязательных документов, файлов-примеров |

---

# 4. Per-document стандарты

Стандарты для каждого типа документа в `specs/docs/`. Расположены в подпапках `docs/{тип}/`.

| Тип документа | Стандарт | Статус |
|---------------|---------|--------|
| docs/README.md | [standard-readme.md](./docs/readme/standard-readme.md) | done |
| {svc}.md | `docs/service/standard-service.md` | — |
| overview.md | [standard-overview.md](./docs/overview/standard-overview.md) | done |
| conventions.md | [standard-conventions.md](./docs/conventions/standard-conventions.md) | done |
| infrastructure.md | `docs/infrastructure/standard-infrastructure.md` | — |
| testing.md | `docs/testing/standard-testing.md` | — |
| standard-{tech}.md | `docs/technology/standard-technology.md` | — |

---

# 5. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-docs.py](./.scripts/validate-docs.py) | Проверка наличия обязательных документов docs/ | [validation-docs.md](./validation-docs.md) |
| [validate-docs-overview.py](./.scripts/validate-docs-overview.py) | Валидация формата docs/.system/overview.md | [validation-overview.md](./docs/overview/validation-overview.md) |
| [validate-docs-readme.py](./.scripts/validate-docs-readme.py) | Валидация формата docs/README.md | [validation-readme.md](./docs/readme/validation-readme.md) |

---

# 6. Скиллы

*Нет скиллов.*
