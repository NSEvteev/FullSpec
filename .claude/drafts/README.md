---
description: Черновики Claude — планы, заметки и исследования
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: .claude/README.md
---

# /.claude/drafts/ — Черновики

Временные рабочие файлы Claude: планы, заметки, исследования.

Хранилище для размышлений, истории принятия решений и временных заметок. На основе drafts реализуется задуманное. Черновики могут быть источником материала для дискуссий в `/specs/discussion/`.

**Полезные ссылки:**
- [Claude Code окружение](../README.md)
- [Структура проекта](/.structure/README.md)

---

## Оглавление

- [1. Файлы](#1-файлы)
- [2. Подпапки](#2-подпапки)
- [3. Дерево](#3-дерево)

---

## 1. Файлы

| Файл | Описание |
|------|----------|
| [2026-02-08-specification-driven-development.md](./2026-02-08-specification-driven-development.md) | Исследование подходов к Specification-Driven Development |
| [2026-02-08-specs-architecture.md](./2026-02-08-specs-architecture.md) | Архитектура specs/: папки, файлы, зоны ответственности |
| [2026-02-10-specs-documents-plan.md](./2026-02-10-specs-documents-plan.md) | План выноса документов из архитектуры specs/ |
| [2026-02-09-specs-architecture-rework.md](./maybe-archive/2026-02-09-specs-architecture-rework.md) | План переработки архитектуры specs/ |
| [2026-02-09-sdd-framework-comparison.md](./maybe-archive/2026-02-09-sdd-framework-comparison.md) | Сравнение SDD-подхода с фреймворками |
| [2026-02-09-task-master-analysis.md](./maybe-archive/2026-02-09-task-master-analysis.md) | Анализ механик Task Master для адаптации в SDD |
| [2026-02-09-specs-architecture-review.md](./maybe-archive/2026-02-09-specs-architecture-review.md) | Ревью архитектуры specs/ (раунд 1): пробелы, двусмысленности, противоречия |
| [2026-02-09-specs-architecture-review-2.md](./maybe-archive/2026-02-09-specs-architecture-review-2.md) | Ревью архитектуры specs/ (раунд 2): анализ пробелов и двусмысленностей |

---

## 2. Подпапки

### [examples/](./examples/README.md)

**Эталонные черновики.**

Коллекция "хороших" черновиков для использования как примеры в промптах. Не имеет зеркала в `.instructions/`.

### [maybe-archive/](./maybe-archive/)

**Черновики на рассмотрении для архивации.**

Черновики, содержание которых перенесено в основные документы. Ожидают решения: удалить или оставить как историю.

---

## 3. Дерево

```
/.claude/drafts/
├── examples/                           # Эталонные примеры
│   ├── example-cross-standards-ssot-analysis.md #   Анализ SSOT между стандартами
│   ├── example-github-platform-research.md      #   Исследование GitHub платформы
│   ├── example-standards-validation-plan.md     #   План валидации стандартов
│   └── README.md                                #   Индекс примеров
├── maybe-archive/                         # Черновики на рассмотрении
│   ├── 2026-02-09-sdd-framework-comparison.md # Сравнение SDD с фреймворками
│   ├── 2026-02-09-specs-architecture-review.md  # Ревью архитектуры (раунд 1)
│   ├── 2026-02-09-specs-architecture-review-2.md # Ревью архитектуры (раунд 2)
│   ├── 2026-02-09-specs-architecture-rework.md # План переработки архитектуры
│   └── 2026-02-09-task-master-analysis.md     # Анализ механик Task Master
├── 2026-02-08-specification-driven-development.md # Исследование SDD
├── 2026-02-08-specs-architecture.md    # Архитектура specs/
├── 2026-02-10-specs-documents-plan.md # План выноса документов specs/
└── README.md                           # Этот файл (индекс)
```
