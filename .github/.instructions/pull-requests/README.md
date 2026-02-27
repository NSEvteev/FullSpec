---
description: Инструкции для GitHub Pull Requests — стандарт, шаблон PR. Индекс документов и подпапок.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/pull-requests/README.md
---

# /.github/.instructions/pull-requests/ — GitHub Pull Requests

Инструкции для работы с GitHub Pull Requests (объекты GitHub, не файлы).

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [.github](../../README.md)

**Регламентирует:** GitHub Pull Requests (объекты в GitHub)

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [Вложенные области](#вложенные-области) | — | Подобласти инструкций |
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |

```
/.github/.instructions/pull-requests/
├── pr-template/                   # Шаблон PULL_REQUEST_TEMPLATE.md
│   ├── README.md
│   ├── standard-pr-template.md
│   └── validation-pr-template.md
├── README.md                      # Этот файл (индекс)
├── create-pull-request.md         # Воркфлоу создания PR
└── standard-pull-request.md       # Стандарт Pull Requests
```

---

## Вложенные области

| Область | Описание | Индекс |
|---------|----------|--------|
| [pr-template/](./pr-template/) | Инструкции для PR template | [README](./pr-template/README.md) |

---

# 1. Стандарты

- [standard-pull-request.md](./standard-pull-request.md) — Процесс работы с Pull Requests

---

# 2. Воркфлоу

- [create-pull-request.md](./create-pull-request.md) — Воркфлоу создания PR (chain → script → title/body/labels → push → preview → gh pr create)

*Будет добавлен modify-pull-request.md*

**Скилл:**

| Скилл | Назначение |
|-------|------------|
| [/pr-create](/.claude/skills/pr-create/SKILL.md) | Создание PR с автосбором Issues из chain |

---

# 3. Валидация

*Будет добавлен validation-pull-request.md*
