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
| [2026-02-08-specification-driven-development.md](./2026-02-08-specification-driven-development.md) | Исследование подходов к Specification-Driven Development |
| [2026-02-08-specs-architecture.md](./2026-02-08-specs-architecture.md) | Архитектура specs/: папки, файлы, зоны ответственности |

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
│   ├── example-standards-validation-plan.md     #   План валидации стандартов
│   └── README.md                                #   Индекс примеров
├── 2026-02-08-specification-driven-development.md # Исследование SDD
├── 2026-02-08-specs-architecture.md    # Архитектура specs/
└── README.md                           # Этот файл (индекс)
```
