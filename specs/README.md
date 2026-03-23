---
description: Спецификации проекта — два контура документации (analysis + docs) и стандарты.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: .structure/README.md
---

# /specs/ — Спецификации

Два контура документации: аналитика (процесс принятия решений) и документация для поставки (рабочий контекст разработчика).

**Полезные ссылки:**
- [Структура проекта](/.structure/README.md)
- [Архитектурные решения](/.claude/drafts/2026-02-19-sdd-structure.md)
- [Оркестратор реализации](/.claude/drafts/2026-02-19-sdd-orchestrator.md)

---

## Оглавление

- [1. Контуры документации](#1-контуры-документации)
- [2. Подпапки](#2-подпапки)
- [3. Дерево](#3-дерево)

---

## 1. Контуры документации

| Контур | Папка | Назначение | Аудитория |
|--------|-------|-----------|-----------|
| **Аналитика** | `analysis/` | Процесс принятия решений: дискуссии, проектирование, планирование тестов и задач | Пользователь + LLM при планировании |
| **Документация** | `docs/` | Рабочий контекст: описание сервисов, архитектура, конвенции, стандарты технологий | LLM-разработчик при написании кода |

---

## 2. Подпапки

### [analysis/](./analysis/)

**Аналитическая документация (контур 1).**

4-уровневая цепочка принятия решений. Группировка по изменению: `analysis/NNNN-{slug}/`.

| Уровень | Документ | Зона ответственности |
|---------|----------|---------------------|
| 1 | `discussion.md` | WHY + WHAT — проблема, требования, критерии успеха |
| 2 | `design.md` | AFFECTED + HOW + DETAILS — распределение ответственностей, контракты, решения |
| 3 | `plan-test.md` | HOW TO VERIFY — per-service acceptance-сценарии (TC-N), тестовые данные |
| 4 | `plan-dev.md` | WHAT TASKS — per-service задачи (TASK-N), подзадачи, маппинг GitHub Issues |
| Артефакт | `review.md` | Ревью кода: Контекст ревью (при WAITING) + итерации (при RUNNING), OPEN → RESOLVED |

Стандарт контура: [standard-analysis.md](./.instructions/analysis/standard-analysis.md)

### [docs/](./docs/)

**Документация для поставки (контур 2).**

Рабочий контекст LLM-разработчика. Содержит per-service документы (`{svc}.md`), системные документы (`.system/`) и стандарты технологий (`.technologies/`).

| Тип | Документ | Назначение |
|-----|----------|------------|
| Системный | `overview.md` | Архитектура, сервисы, потоки данных |
| Системный | `conventions.md` | Общие конвенции кодирования |
| Системный | `infrastructure.md` | Хранилища, окружения, CI/CD |
| Системный | `testing.md` | Стратегия тестирования, фреймворки |
| Per-service | `{svc}.md` | 10 секций: API, Data Model, потоки, Code Map и т.д. |
| Per-tech | `standard-{tech}.md` | Стандарт кодирования для конкретной технологии |

Стандарт контура: [standard-docs.md](./.instructions/docs/standard-docs.md)

### [.instructions/](./.instructions/)

**Стандарты и воркфлоу.**

Инструкции для создания, валидации и обновления документов specs/. Содержит стандарты обоих контуров (analysis/ и docs/), скрипты валидации и воркфлоу (create/modify).

Индекс: [.instructions/README.md](./.instructions/README.md)

---

## 3. Дерево

```
/specs/
├── analysis/                   # Контур 1: аналитика (4-уровневая цепочка + review.md)
│   ├── README.md               #   Индекс цепочек NNNN-{topic}
├── docs/                       # Контур 2: документация для поставки
│   ├── .system/                # Системные документы
│   │   ├── conventions.md
│   │   ├── infrastructure.md
│   │   ├── overview.md
│   │   ├── testing.md
│   ├── .technologies/          # Per-tech стандарты кодирования
│   │   ├── standard-example.md
│   ├── example.md              # Пример per-service документа
│   ├── README.md
├── .instructions/              # Стандарты и воркфлоу обоих контуров
│   ├── analysis/               # Стандарты контура analysis/
│   │   ├── design/
│   │   ├── discussion/
├── hotfixes/                        # Хранилище хотфиксов
│   │   ├── plan-dev/
│   │   ├── plan-test/
│   │   ├── review/             #   Стандарты review.md
│   │   ├── standard-analysis.md
│   ├── docs/                   # Стандарты контура docs/
│   │   ├── conventions/
│   │   ├── infrastructure/
│   │   ├── overview/
│   │   ├── readme/
│   │   ├── service/
│   │   ├── technology/
│   │   ├── testing/
│   │   ├── standard-docs.md
│   │   ├── validation-docs.md
│   ├── .scripts/               # Скрипты валидации (pre-commit)
│   ├── README.md
└── README.md                   # Этот файл
```
