---
description: Архитектурная документация — system, services, domains. Индекс архитектурных спецификаций проекта.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: specs/architecture/README.md
---

# /specs/architecture/ — Архитектура (живые документы)

Текущее состояние архитектуры. Файлы system/ и domains/ создаются при инициализации проекта как пустые шаблоны, заполняются Planned Changes при Design → WAITING, обновляются до AS IS при Design → DONE. Per-service файлы создаются при ADR → DONE.

**Полезные ссылки:**
- [Спецификации проекта](../README.md)
- [Структура проекта](/.structure/README.md)

## Оглавление

- [1. Папки](#1-папки)
- [2. Quick Scan для Impact](#2-quick-scan-для-impact)
- [3. Дерево](#3-дерево)

---

## 1. Папки

### [system/](./system/README.md)

**Системная архитектура — межсервисные документы.**

### [services/](./services/README.md)

**Per-service архитектура — состояние каждого сервиса.**

### [domains/](./domains/README.md)

**Доменная архитектура — DDD контексты.**

---

## 2. Quick Scan для Impact

При проведении Impact Analysis — порядок чтения архитектурных документов:

| # | Что читать | Зачем |
|---|-----------|-------|
| 1 | [services/README.md](./services/README.md) — таблица сервисов | Список существующих сервисов, технологии, API |
| 2 | [system/overview.md](./system/overview.md) | Общая картина, потоки между сервисами |
| 3 | `services/{svc}.md` — Резюме + Planned Changes | Детали по затронутым сервисам |

Подробнее: [standard-service.md § 8](../.instructions/living-docs/service/standard-service.md#8-quick-scan-для-impact)

---

## 3. Дерево

```
/specs/architecture/
├── domains/                 # Доменная архитектура (DDD)
│   ├── context-map.md       #   Карта взаимодействия контекстов
│   └── README.md
├── services/                # Per-service архитектура
│   └── README.md
├── system/                  # Системная архитектура
│   ├── overview.md          #   Обзор: сервисы, потоки, инфраструктура
│   ├── data-flows.md        #   Потоки данных между сервисами
│   ├── infrastructure.md    #   Deployment, networking, мониторинг
│   └── README.md
└── README.md                # Этот файл
```
