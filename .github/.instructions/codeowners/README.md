---
description: Инструкции для CODEOWNERS — стандарт формата, валидация. Индекс документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/codeowners/README.md
---

# /.github/.instructions/codeowners/ — CODEOWNERS

Инструкции для создания и редактирования файла CODEOWNERS.

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [.github](../../README.md)

**Регламентирует:** `.github/CODEOWNERS`

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |

```
/.github/.instructions/codeowners/
├── README.md                           # Этот файл (индекс)
├── standard-codeowners.md              # Стандарт синтаксиса CODEOWNERS
└── validation-codeowners.md            # Валидация CODEOWNERS
```

---

# 1. Стандарты

- [standard-codeowners.md](./standard-codeowners.md) — Синтаксис, правила и паттерны CODEOWNERS

---

# 2. Воркфлоу

*Не требуется (файл создаётся разово и редактируется вручную)*

---

# 3. Валидация

- [validation-codeowners.md](./validation-codeowners.md) — Валидация CODEOWNERS (автоматически через pre-commit)
