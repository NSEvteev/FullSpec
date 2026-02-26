---
description: Инструкции для GitHub Actions — стандарт workflow, валидация, безопасность. Индекс документов и подпапок.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/actions/README.md
---

# Инструкции /.github/.instructions/actions/

GitHub Actions и автоматизация.

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [SSOT .github](../../README.md)

**Содержание:** Workflows, Security, CI/CD.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [Вложенные области](#вложенные-области) | — | Подобласти инструкций |
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для этой области |

```
/.github/.instructions/actions/
├── deploy/                             # Deploy workflow (environments, rollback)
│   ├── README.md
│   ├── standard-deploy.md
│   └── validation-deploy.md
├── security/                           # Безопасность (Dependabot, CodeQL)
│   ├── README.md
│   └── standard-security.md
├── standard-action.md                  # Структура YAML, триггеры, jobs/steps
├── validation-action.md                # Валидация workflow файлов (A001-A007)
└── README.md                           # Этот файл (индекс)
```

---

## Вложенные области

| Область | Описание | Индекс |
|---------|----------|--------|
| [deploy/](./deploy/) | Deploy workflow: триггеры, environments, dynamic discovery, rollback | [README](./deploy/README.md) |
| [security/](./security/) | Безопасность: Dependabot, CodeQL, Secret Scanning | [README](./security/README.md) |

---

# 1. Стандарты

| Документ | Описание |
|----------|----------|
| [standard-action.md](./standard-action.md) | Структура YAML, триггеры, jobs/steps, secrets, best practices |

---

# 2. Воркфлоу

*Нет воркфлоу.*

---

# 3. Валидация

| Документ | Описание |
|----------|----------|
| [validation-action.md](./validation-action.md) | Валидация workflow файлов (A001-A007) |

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-action.py](../.scripts/validate-action.py) | Валидация workflow файлов (A001-A007) | [validation-action.md](./validation-action.md) |

---

# 5. Скиллы

*Нет скиллов.*
