---
description: Системная архитектура — общая структура, компоненты, межсервисное взаимодействие. Индекс системных документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: specs/architecture/system/README.md
---

# /specs/architecture/system/ — Системная архитектура

Межсервисные архитектурные документы: общая топология, взаимодействие сервисов, инфраструктура.

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
| [overview.md](overview.md) | Обзор системной архитектуры — сервисы, потоки, инфраструктура |
| [data-flows.md](data-flows.md) | Детальные потоки данных между сервисами |
| [infrastructure.md](infrastructure.md) | Deployment, networking, мониторинг |

---

## 2. Дерево

```
/specs/architecture/system/
├── overview.md              # Обзор системной архитектуры
├── data-flows.md            # Потоки данных между сервисами
├── infrastructure.md        # Инфраструктура
└── README.md                # Этот файл
```
