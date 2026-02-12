---
description: Инструкции для живой документации сервисов — сервисная, системная и доменная архитектура. Индекс документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: specs/.instructions/living-docs/service/README.md
---

# /specs/.instructions/living-docs/service/ — Сервисная документация

Инструкции для живых документов архитектуры `/specs/architecture/`.

**Полезные ссылки:**
- [Живые документы](../README.md)
- [Инструкции /specs/](../../README.md)

---

## Оглавление

- [1. Файлы](#1-файлы)
- [2. Дерево](#2-дерево)

---

## 1. Файлы

### [standard-service.md](./standard-service.md)

**Стандарт живых документов архитектуры — сущность сервиса, Quick Scan для Impact, Code Map, границы автономии LLM, Planned Changes.**

### [validation-service.md](./validation-service.md)

**Валидация сервисных документов services/{svc}.md — frontmatter, секции, формат таблиц, согласованность с README и labels.**

### [create-service.md](./create-service.md)

**Воркфлоу создания сервисного документа services/{svc}.md — от Design → WAITING до создания stub с Резюме и Planned Changes, обновления README и labels.**

### [modify-service.md](./modify-service.md)

**Воркфлоу изменения сервисного документа services/{svc}.md — обновление при ADR/Design событиях, деактивация и миграция сервиса.**

---

## 2. Дерево

```
/specs/.instructions/living-docs/service/
├── standard-service.md            # Стандарт живых документов архитектуры
├── validation-service.md          # Валидация сервисных документов
├── create-service.md              # Воркфлоу создания (stub при Design → WAITING)
├── modify-service.md              # Воркфлоу изменения (ADR/Design события)
└── README.md                      # Этот файл (индекс)
```
