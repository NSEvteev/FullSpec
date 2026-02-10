---
description: Архитектурная документация — system, services, domains. Индекс архитектурных спецификаций проекта.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: specs/architecture/README.md
---

# /specs/architecture/ — Архитектура (живые документы)

Текущее состояние архитектуры. Обновляется при ADR→DONE. Содержит системную, сервисную и доменную архитектуру.

**Полезные ссылки:**
- [Спецификации проекта](../README.md)
- [Структура проекта](/.structure/README.md)

## Оглавление

- [1. Папки](#1-папки)
- [2. Дерево](#2-дерево)

---

## 1. Папки

### [system/](./system/README.md)

**Системная архитектура — межсервисные документы.**

### [services/](./services/README.md)

**Per-service архитектура — состояние каждого сервиса.**

### [domains/](./domains/README.md)

**Доменная архитектура — DDD контексты.**

---

## 2. Дерево

```
/specs/architecture/
├── domains/                 # Доменная архитектура (DDD)
├── services/                # Per-service архитектура
├── system/                  # Системная архитектура
└── README.md                # Этот файл
```
