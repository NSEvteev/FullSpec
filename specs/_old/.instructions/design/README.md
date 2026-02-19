---
description: Инструкции для design-документов — спецификации компонентов, API, UI. Индекс документов design/.
standard: .structure/.instructions/standard-readme.md
index: specs/.instructions/design/README.md
---

# Инструкции /specs/design/

Индекс инструкций для папки design/.

**Полезные ссылки:**
- [Инструкции specs/](../README.md)
- [specs/](../../README.md)

**Содержание:** standard-design.md, validation-design.md, create-design.md, modify-design.md

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | create-design.md, modify-design.md | Создание и изменение |
| [3. Валидация](#3-валидация) | validation-design.md | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для этой области |

```
/specs/.instructions/design/
├── README.md                # Этот файл (индекс)
├── standard-design.md       # Стандарт проектирования SDD
├── validation-design.md     # Валидация документов проектирования
├── create-design.md         # Воркфлоу создания проектирования
└── modify-design.md         # Воркфлоу изменения проектирования
```

---

# 1. Стандарты

| Документ | Описание |
|----------|----------|
| [standard-design.md](./standard-design.md) | Стандарт проектирования SDD — зона КАК РАСПРЕДЕЛЯЕМ (РЕШАТЕЛЬ), секции по сервисам, блоки взаимодействия, контракты API, системные тест-сценарии, шаблон, чек-лист качества |

---

# 2. Воркфлоу

| Документ | Описание |
|----------|----------|
| [create-design.md](./create-design.md) | Воркфлоу создания документа проектирования SDD — Deep Scan, Clarify, генерация секций SVC/INT/STS, валидация, артефакты, перевод DRAFT → WAITING |
| [modify-design.md](./modify-design.md) | Воркфлоу изменения документа проектирования SDD — операции по статусам, переходы жизненного цикла, откат артефактов |

---

# 3. Валидация

| Документ | Описание |
|----------|----------|
| [validation-design.md](./validation-design.md) | Валидация документов проектирования SDD — frontmatter, именование, секции SVC/INT/STS, нумерация, маркеры, зона ответственности. 40 кодов ошибок (D001-D040) |

---

# 4. Скрипты

| Скрипт | Описание |
|--------|----------|
| [create-design-file.py](../.scripts/create-design-file.py) | Создание файла проектирования из шаблона (parent Impact → design-NNNN-topic.md) |
| [validate-design.py](../.scripts/validate-design.py) | Автоматическая валидация документа проектирования (40 кодов D001-D040) |

---

# 5. Скиллы

| Скилл | Описание |
|-------|----------|
| [/design-create](/.claude/skills/design-create/SKILL.md) | Создание документа проектирования (multi-agent оркестрация) |
| [/design-modify](/.claude/skills/design-modify/SKILL.md) | Изменение документа проектирования |
| [/design-validate](/.claude/skills/design-validate/SKILL.md) | Валидация документа проектирования |
