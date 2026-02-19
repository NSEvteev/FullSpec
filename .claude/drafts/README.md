---
description: Черновики Claude — планы, анализы, спецификации в работе. Индекс активных и архивных черновиков.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: .claude/README.md
---

# /.claude/drafts/ — Черновики

Временные рабочие файлы Claude: планы, заметки, исследования.

Хранилище для размышлений, истории принятия решений и временных заметок. На основе drafts реализуется задуманное. Черновики могут быть источником материала для дискуссий в `/specs/analysis/`.

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
| [2026-02-10-specs-documents-plan.md](./2026-02-10-specs-documents-plan.md) | План выноса документов из архитектуры specs/ |
| [2026-02-15-specs-readme-format-gap.md](./2026-02-15-specs-readme-format-gap.md) | Проблема: README specs-папок не имеют процесса создания |
| [2026-02-19-sdd-orchestrator.md](./2026-02-19-sdd-orchestrator.md) | Оркестратор реализации SDD v2: последовательность, зависимости, чеклист миграции |
| [2026-02-19-sdd-structure.md](./2026-02-19-sdd-structure.md) | Структура SDD v2: два контура, решения, открытые вопросы |
| [2026-02-19-sdd-docs-testing.md](./2026-02-19-sdd-docs-testing.md) | docs/.system/testing.md: секции, шаблон, пример — стратегия тестирования |
| [2026-02-19-sdd-docs-service.md](./2026-02-19-sdd-docs-service.md) | docs/{svc}.md: 10 секций, шаблон, пример — сервисный документ |
| [2026-02-19-sdd-docs-technology.md](./2026-02-19-sdd-docs-technology.md) | docs/.technologies/standard-{tech}.md: секции, шаблон, пример — per-tech стандарт |
| [2026-02-19-holt-analysis-standard-conventions.md](./2026-02-19-holt-analysis-standard-conventions.md) | Анализ captain-holt: standard-conventions.md |
| [2026-02-19-holt-analysis-standard-infrastructure.md](./2026-02-19-holt-analysis-standard-infrastructure.md) | Анализ captain-holt: standard-infrastructure.md |
| [pre-release-cleanup.md](./pre-release-cleanup.md) | Финальная очистка проекта перед релизом (обновлённая) |
| [2026-02-09-specs-architecture-rework.md](./maybe-archive/2026-02-09-specs-architecture-rework.md) | План переработки архитектуры specs/ |
| [2026-02-15-impact-instructions-testing.md](./maybe-archive/2026-02-15-impact-instructions-testing.md) | Impact: инструкции, скрипты, скиллы + тестовые итерации |
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
│   ├── 2026-02-08-specs-architecture.md          #   Архитектура specs/ (SDD)
│   └── README.md                                #   Индекс примеров
├── maybe-archive/                      # Черновики на рассмотрении
│   ├── 2026-02-09-sdd-framework-comparison.md # Сравнение SDD с фреймворками
│   ├── 2026-02-09-specs-architecture-review.md  # Ревью архитектуры (раунд 1)
│   ├── 2026-02-09-specs-architecture-review-2.md # Ревью архитектуры (раунд 2)
│   ├── 2026-02-09-specs-architecture-rework.md # План переработки архитектуры
│   ├── 2026-02-09-task-master-analysis.md     # Анализ механик Task Master
│   └── 2026-02-15-impact-instructions-testing.md # Impact: инструкции + тесты
├── 2026-02-08-specification-driven-development.md # Исследование SDD
├── 2026-02-10-specs-documents-plan.md  # План выноса документов specs/
├── 2026-02-15-specs-readme-format-gap.md # README specs-папок: пробел в процессе
├── 2026-02-19-sdd-orchestrator.md      # Оркестратор реализации SDD v2
├── 2026-02-19-sdd-structure.md         # Структура SDD v2: решения
├── 2026-02-19-holt-analysis-standard-conventions.md # Анализ captain-holt: conventions
├── 2026-02-19-holt-analysis-standard-infrastructure.md # Анализ captain-holt: infrastructure
├── 2026-02-19-sdd-docs-testing.md      # docs/.system/testing.md
├── 2026-02-19-sdd-docs-service.md      # docs/{svc}.md
├── 2026-02-19-sdd-docs-technology.md   # docs/.technologies/standard-{tech}.md
├── pre-release-cleanup.md              # Финальная очистка (обновлённая)
└── README.md                           # Этот файл (индекс)
```
