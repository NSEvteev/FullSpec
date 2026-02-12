---
description: Доменная архитектура проекта — DDD-контексты, границы доменов, взаимодействия. Индекс доменных документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: specs/architecture/domains/README.md
---

# /specs/architecture/domains/ — Доменная архитектура

Документы доменной архитектуры: bounded contexts, агрегаты, доменные события.

**Полезные ссылки:**
- [architecture/](../README.md)
- [Спецификации проекта](../../README.md)
- [Структура проекта](/.structure/README.md)

## Оглавление

- [1. Файлы](#1-файлы)
- [2. Дерево](#2-дерево)

---

## 1. Файлы

| Файл | Описание |
|------|----------|
| [context-map.md](context-map.md) | Карта взаимодействия между bounded contexts |

Per-domain файлы (`{domain}.md`) создаются при первом Design → WAITING.

---

## 2. Дерево

```
/specs/architecture/domains/
├── context-map.md           # Карта взаимодействия контекстов
└── README.md                # Этот файл
```

Per-domain файлы (`{domain}.md`) создаются динамически при первом Design → WAITING.
