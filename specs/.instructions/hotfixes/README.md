---
description: Индекс инструкций для hotfixes/ — стандарт, воркфлоу создания и валидация хотфиксов.
standard: .structure/.instructions/standard-readme.md
index: specs/.instructions/hotfixes/README.md
---

# Инструкции /specs/hotfixes/

Индекс инструкций для папки hotfixes/.

**Полезные ссылки:**
- [Инструкции specs/](../README.md)
- [specs/hotfixes/](../../hotfixes/README.md)

**Содержание:** стандарт хотфикса, воркфлоу создания, валидация.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | [standard-hotfix.md](./standard-hotfix.md) | Формат и правила оформления hotfix.md |
| [2. Воркфлоу](#2-воркфлоу) | [create-hotfix.md](./create-hotfix.md) | Воркфлоу создания хотфикса (SSOT для /hotfix) |
| [3. Валидация](#3-валидация) | [validation-hotfix.md](./validation-hotfix.md) | Проверка hotfix.md |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | [/hotfix](/.claude/skills/hotfix/SKILL.md) | Процесс хотфикса |

```
/specs/.instructions/hotfixes/
├── README.md                # Этот файл (индекс)
├── standard-hotfix.md       # Стандарт файла хотфикса
├── create-hotfix.md         # Воркфлоу создания (SSOT для /hotfix)
└── validation-hotfix.md     # Валидация hotfix.md
```

---

# 1. Стандарты

### [standard-hotfix.md](./standard-hotfix.md)

**Стандарт файла хотфикса.**
Frontmatter, обязательные секции, статусы, именование, коммиты и откат.

---

# 2. Воркфлоу

### [create-hotfix.md](./create-hotfix.md)

**Воркфлоу создания хотфикса (SSOT для /hotfix).**
7 шагов от проблемы до коммита в main. Принципы, TaskList-шаблон, чек-лист, оркестрация агентов.

---

# 3. Валидация

### [validation-hotfix.md](./validation-hotfix.md)

**Валидация hotfix.md.**
Обязательные секции, frontmatter, формат impact-таблиц.

---

# 4. Скрипты

*Нет скриптов.*

---

# 5. Скиллы

### [/hotfix](/.claude/skills/hotfix/SKILL.md)

**Процесс хотфикса.**
Диагностика бага/инцидента, impact analysis, параллельное исправление кода и документации.
