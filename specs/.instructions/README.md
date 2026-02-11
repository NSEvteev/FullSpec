---
description: Инструкции для спецификационной документации SDD — ADR, design, discussion, impact, plans. Индекс всех подпапок.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: specs/.instructions/README.md
---

# /specs/.instructions/ — Инструкции

Инструкции для работы с документами спецификаций `/specs/`.

**Полезные ссылки:**
- [Спецификации](/specs/README.md)
- [Структура проекта](/.structure/README.md)

---

## Оглавление

- [1. Подпапки](#1-подпапки)
- [2. Файлы](#2-файлы)
- [3. Дерево](#3-дерево)

---

## 1. Подпапки

### [discussion/](./discussion/README.md)

**Инструкции для дискуссий.**

### [impact/](./impact/README.md)

**Инструкции для импакт-анализа.**

### [design/](./design/README.md)

**Инструкции для проектирования.**

### [adr/](./adr/README.md)

**Инструкции для ADR (Architecture Decision Records).**

### [plan-test/](./plan-test/README.md)

**Инструкции для планов тестов (ATDD).**

### [plan-dev/](./plan-dev/README.md)

**Инструкции для планов разработки.**

### [living-docs/](./living-docs/README.md)

**Инструкции для живых документов (architecture, tests, glossary).**

---

## 2. Файлы

### [standard-specs-reference.md](./standard-specs-reference.md)

**Справочник SDD — общие механики: статусы, каскады, связи, обратная связь, Clarify-паттерн, именование, запреты.**

### [standard-specs-workflow.md](./standard-specs-workflow.md)

**Навигатор SDD — воркфлоу от намерения до разработки: стадии, уровни, фильтрация, Shared код, Upward feedback, Planned Changes.**

---

## 3. Дерево

```
/specs/.instructions/
├── .scripts/                       # Скрипты валидации
│   └── validate-discussion.py
├── adr/                            # Инструкции для ADR
│   └── README.md
├── design/                         # Инструкции для проектирования
│   └── README.md
├── discussion/                     # Инструкции для дискуссий
│   └── README.md
├── impact/                         # Инструкции для импакт-анализа
│   └── README.md
├── living-docs/                    # Инструкции для живых документов
│   ├── architecture/               #   Архитектура
│   │   └── README.md
│   ├── glossary/                   #   Глоссарий
│   │   └── README.md
│   ├── tests/                      #   Тесты
│   │   └── README.md
│   └── README.md
├── plan-dev/                       # Инструкции для планов разработки
│   └── README.md
├── plan-test/                      # Инструкции для планов тестов (ATDD)
│   └── README.md
├── standard-specs-reference.md     # Справочник SDD (механики)
├── standard-specs-workflow.md      # Навигатор SDD (воркфлоу)
└── README.md                       # Этот файл (индекс)
```
