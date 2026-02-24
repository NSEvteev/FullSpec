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

*Цепочки появятся здесь при создании через `/discussion-create`.*

---

## Статусы цепочек

<!-- BEGIN:analysis-status -->
| NNNN | Тема | Disc | Design | P.Test | P.Dev | Review | Branch | Milestone |
|------|------|------|--------|--------|-------|--------|--------|-----------|
<!-- END:analysis-status -->

*Обновляется через `/analysis-status --update`*

---

## Дерево

```
specs/analysis/
└── README.md                   # Этот файл (индекс цепочек)
```

> При создании цепочки через `/discussion-create` появится `NNNN-{topic}/` с файлами: discussion.md, design.md, plan-test.md, plan-dev.md, review.md.
