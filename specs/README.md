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

### [glossary/](./glossary/README.md)

**Глоссарий терминов по доменам.**

---

## 2. Файлы

*Нет файлов.*

---

## 3. Дерево

```
/specs/
├── .instructions/               # Инструкции для работы со спецификациями
├── architecture/                # Живые документы архитектуры
│   ├── domains/                 #   Доменная архитектура (DDD)
│   ├── services/                #   Per-service архитектура
│   └── system/                  #   Системная архитектура
├── design/                      # Проектирование
├── discussion/                  # Дискуссии (идеи, исследования)
├── glossary/                    # Глоссарий по доменам
├── impact/                      # Импакт-анализ
├── services/                    # Per-service спецификации (ADR, тест-спеки, планы)
├── tests/                       # Живые документы тестов
│   ├── services/                #   Сервисные тесты
│   └── system/                  #   Системные тесты
└── README.md                    # Этот файл
```
