---
description: Спецификационная документация SDD (Specification-Driven Development) — архитектура, design, тесты, глоссарий.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: specs/README.md
---

# /specs/ — Спецификации проекта

Спецификации, архитектурные решения, планы развития проекта. Управляется через SDD (Specification-Driven Development).

**Полезные ссылки:**
- [Структура проекта](/.structure/README.md)
- [Инструкции](/specs/.instructions/README.md)

---

## Оглавление

- [1. Папки](#1-папки)
- [2. Файлы](#2-файлы)
- [3. Дерево](#3-дерево)

---

## 1. Папки

### [discussion/](./discussion/README.md)

**Дискуссии — точка входа для новых идей.**

### [impact/](./impact/README.md)

**Импакт-анализ — какие сервисы затронуты.**

### [design/](./design/README.md)

**Проектирование — декомпозиция Impact на per-service решения.**

### [architecture/](./architecture/README.md)

**Архитектура (живые документы) — текущее состояние системы.**

### [tests/](./tests/README.md)

**Тесты (живые документы) — текущая тестовая документация.**

### [services/](./services/)

**Per-service спецификации — ADR, планы тестов, планы разработки (уровни 4-6 SDD).**

### [glossary/](./glossary/README.md)

**Глоссарий терминов по доменам.**

---

## 2. Файлы

*Нет файлов.*

---

## 3. Дерево

```
/specs/
├── .instructions/                      # Правила для каждого объекта
│   ├── discussion/                     #   Стандарт дискуссий
│   ├── impact/                         #   Стандарт импакт-анализа
│   ├── design/                         #   Стандарт проектирования
│   ├── adr/                            #   Стандарт ADR
│   ├── plan-test/                      #   Стандарт планов тестов (ATDD)
│   ├── plan-dev/                       #   Стандарт планов
│   ├── living-docs/                    #   Стандарты живых документов
│   │   ├── architecture/              #     Архитектура
│   │   ├── tests/                     #     Тесты
│   │   └── glossary/                  #     Глоссарий
│   ├── standard-specs-reference.md     #   Справочник SDD (статусы, каскады, frontmatter)
│   ├── standard-specs-workflow.md      #   Навигатор SDD (воркфлоу, стадии → SSOT)
│   └── README.md                       #   Индекс инструкций
│
├── discussion/                         # Уровень 1: ЗАЧЕМ и ЧТО
│   ├── disc-NNNN-topic.md
│   └── README.md
│
├── impact/                             # Уровень 2: НА ЧТО ВЛИЯЕТ
│   ├── impact-NNNN-topic.md
│   └── README.md
│
├── design/                             # Уровень 3: КАК ВСТРАИВАЕМ
│   ├── design-NNNN-topic.md            #   Секции по сервисам + блоки взаимодействия
│   └── README.md
│
├── services/                           # Уровни 4-6: по сервисам
│   └── {service}/
│       ├── adr/                        #   Уровень 4: КАК КОНКРЕТНО
│       │   ├── adr-NNNN-topic.md
│       │   └── README.md
│       ├── plan-test/                  #   Уровень 5: КАК ПРОВЕРЯЕМ (ATDD)
│       │   ├── plan-test-NNNN-topic.md
│       │   └── README.md
│       ├── plan-dev/                   #   Уровень 6: ЧТО ДЕЛАЕМ
│       │   ├── plan-dev-NNNN-topic.md
│       │   └── README.md
│       └── README.md                   #   Индекс сервиса
│
├── architecture/                       # Живое состояние архитектуры
│   ├── system/                        #   Системная архитектура
│   │   ├── overview.md                #     Сервисы, потоки, высокоуровневая карта
│   │   ├── data-flows.md             #     Потоки данных между сервисами
│   │   └── infrastructure.md         #     Deployment, networking, monitoring
│   ├── services/                      #   Per-service архитектура
│   │   └── {service}.md               #     Компоненты, tech stack, API, data model, Code Map
│   ├── domains/                       #   Доменная архитектура (DDD)
│   │   ├── {domain}.md                #     Один файл на bounded context
│   │   └── context-map.md             #     Карта взаимодействия контекстов
│   └── README.md
│
├── tests/                              # Живое состояние тестов
│   ├── system/                        #   Зеркало /tests/ — межсервисные
│   │   ├── e2e/
│   │   ├── integration/
│   │   ├── load/
│   │   └── README.md
│   ├── services/                      #   Зеркало /src/{svc}/tests/
│   │   └── {service}/
│   │       ├── e2e/
│   │       ├── integration/
│   │       ├── unit/
│   │       └── README.md
│   └── README.md
│
├── glossary/                           # Терминология (по доменам)
│   ├── {domain}.md
│   └── README.md
│
└── README.md                           # Этот файл (точка входа)
```
