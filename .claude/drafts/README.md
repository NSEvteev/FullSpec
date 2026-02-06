---
description: Черновики Claude — планы, заметки и исследования
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: .claude/README.md
---

# /.claude/drafts/ — Черновики

Временные рабочие файлы Claude: планы, заметки, исследования.

Хранилище для размышлений, истории принятия решений и временных заметок. На основе drafts реализуется задуманное. Черновики могут быть источником материала для дискуссий в `/specs/discussions/`.

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
| [2026-02-03-github-ssot-refactoring.md](./2026-02-03-github-ssot-refactoring.md) | SSOT-рефакторинг .github/ |
| [2026-02-05-github-instructions.md](./2026-02-05-github-instructions.md) | GitHub-инструкции: реструктуризация и валидация (объединённый) |

---

## 2. Подпапки

### [examples/](./examples/README.md)

**Эталонные черновики.**

Коллекция "хороших" черновиков для использования как примеры в промптах. Не имеет зеркала в `.instructions/`.

---

## 3. Дерево

```
/.claude/drafts/
├── examples/                           # Эталонные примеры
│   ├── example-cross-standards-ssot-analysis.md #   Анализ SSOT между стандартами
│   ├── example-github-platform-research.md      #   Исследование GitHub платформы
│   └── README.md                                #   Индекс примеров
├── README.md                           # Этот файл (индекс)
├── 2026-02-03-recommendations-standard-development-workflow.md # TODO: добавить описание
├── 2026-02-03-recommendations-standard-release-workflow.md # TODO: добавить описание
├── 2026-02-03-recommendations-standard-release.md # TODO: добавить описание
├── 2026-02-05-github-instructions.md   # GitHub-инструкции (объединённый)
├── 2026-02-05-holt-analysis-standard-branching.md # Семантический анализ standard-branching.md
├── 2026-02-05-holt-analysis-standard-commit.md # Семантический анализ standard-commit.md
├── 2026-02-05-holt-analysis-standard-development.md # Семантический анализ standard-development.md
├── 2026-02-05-holt-analysis-standard-review.md # Семантический анализ standard-review.md
├── 2026-02-05-holt-analysis-standard-sync.md # Семантический анализ standard-sync.md
└── 2026-02-05-standards-validation-plan.md # План валидации стандартов
```
