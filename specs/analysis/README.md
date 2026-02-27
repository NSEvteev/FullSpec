---
description: Индекс аналитических цепочек SDD — все NNNN-{topic} со статусами и ссылками на документы.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: specs/README.md
---

# /specs/analysis/ — Аналитический контур

4-уровневая цепочка принятия решений: Discussion → Design → Plan Tests → Plan Dev. Артефакт ревью: review.md.

**Полезные ссылки:**
- [specs/](../README.md)
- [Стандарт контура](../.instructions/analysis/standard-analysis.md)

---

## Оглавление

- [Структура цепочки](#структура-цепочки)
- [Цепочки](#цепочки)
- [Статусы цепочек](#статусы-цепочек)

---

## Структура цепочки

Каждая цепочка хранится в папке `specs/analysis/NNNN-{topic}/`:

| Документ | Уровень | Зона ответственности |
|----------|---------|---------------------|
| `discussion.md` | 1 | WHY + WHAT — проблема, требования, критерии успеха |
| `design.md` | 2 | AFFECTED + HOW — распределение ответственностей, контракты, решения |
| `plan-test.md` | 3 | HOW TO VERIFY — per-service acceptance-сценарии (TC-N) |
| `plan-dev.md` | 4 | WHAT TASKS — per-service задачи (TASK-N), маппинг GitHub Issues |
| `review.md` | Артефакт | Ревью кода: Контекст ревью + итерации (OPEN → RESOLVED) |

---

## Цепочки

| ID | Тема | Статус | Design | Milestone | Описание |
|----|------|--------|--------|-----------|----------|
| 0001 | task-dashboard | WAITING | design.md | v0.1.0 | Task Dashboard — дашборд управления задачами |

---

## Статусы цепочек

<!-- BEGIN:analysis-status -->
| NNNN | Тема | Disc | Design | P.Test | P.Dev | Review | Branch | Milestone |
|------|------|------|--------|--------|-------|--------|--------|-----------|
| 0001 | task-dashboard | W | W | W | — | — | 0001-task-dashboard | v0.1.0 |
<!-- END:analysis-status -->

*Обновляется через `/analysis-status --update`*

---

## Дерево

```
specs/analysis/
├── 0001-task-dashboard/
│   ├── discussion.md           # Task Dashboard
│   ├── design.md               # Task Dashboard — Design
│   ├── plan-test.md            # Task Dashboard — Plan Tests
│   └── plan-dev.md             # Task Dashboard — Plan Dev
└── README.md                   # Этот файл (индекс цепочек)
```
