---
description: Корневая папка .claude — скиллы, агенты, rules, черновики, инструкции. Индекс конфигурации Claude Code.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
---

# .claude/ — Инструменты Claude Code

Хаб навигации по инструментам Claude Code для проекта.

**Полезные ссылки:**
- [Структура проекта](/.structure/README.md)

## Быстрый старт

| Задача | Что делать |
|--------|------------|
| Создать скилл | `/skill-create` |
| Создать инструкцию | `/instruction-create` |
| Создать Issue | `/issue-create` |
| Создать ветку | `/branch-create` |
| Создать папку | `/structure-create` |
| Проверить черновик | `/draft-validate` |
| Ревью кода | `/review` |

---

## Оглавление

- [1. Папки](#1-папки)
- [2. Файлы](#2-файлы)
- [3. Дерево](#3-дерево)

---

## 1. Папки

### 🔗 [.instructions/](./.instructions/README.md)

**Правила и стандарты.**

Как писать скиллы (`skills/`), rules (`rules/`), агентов (`agents/`), работать с черновиками (`drafts/`).

### 🔗 [skills/](./skills/README.md)

**Скиллы автоматизации (35).**

Команды для управления инструкциями, скриптами, скиллами, rules, агентами, ссылками, структурой, issues, milestones, labels, ветками, миграциями и ревью.

### 🔗 [rules/](./rules/)

**Контекстные правила.**

Rules для автоматической загрузки контекста при работе с файлами. Автозагрузка: `core.md` (скиллы, SSOT, шаблоны), `development.md` (процесс разработки), `instructions.md`, `code.md`, `standard-update.md`.

### 🔗 [agents/](./.instructions/agents/README.md)

**Автономные агенты.**

Конфигурации агентов Claude: `meta-reviewer` (семантический анализ документов), `meta-agent` (помощник по инструкциям).

### 🔗 [drafts/](./drafts/README.md)

**Черновики.**

Временные рабочие файлы: планы, заметки, исследования. Эталонные примеры в `examples/`.

---

## 2. Файлы

| Файл | Описание |
|------|----------|
| [CHANGELOG.md](./CHANGELOG.md) | История изменений .claude/ |
| [onboarding.md](./onboarding.md) | Руководство для новых участников |
| [settings.json](./settings.json) | Настройки Claude Code |

---

## 3. Дерево

```
/.claude/
├── .instructions/                      # Правила и стандарты
│   ├── agents/                         #   Как писать агентов
│   ├── drafts/                         #   Как работать с черновиками
│   ├── rules/                          #   Как писать rules
│   ├── skills/                         #   Как писать скиллы
│   └── README.md                       #   Индекс инструкций
├── agents/                             # Конфигурации агентов
├── drafts/                             # Черновики
│   ├── examples/                       #   Эталонные примеры
│   └── README.md                       #   Индекс черновиков
├── rules/                              # Rules для автозагрузки контекста
├── skills/                             # Скиллы (35)
│   └── README.md                       #   Индекс скиллов
├── CHANGELOG.md                        # История изменений .claude/
├── onboarding.md                       # Руководство для новых участников
├── README.md                           # Этот файл
├── settings.json                       # Настройки Claude Code
└── settings.local.json                 # Локальные настройки (не в git)
```

---

## Для новых участников

- [Onboarding](./onboarding.md) — руководство для новых участников
- [Changelog](./CHANGELOG.md) — история изменений системы

---

## Связанные документы

- [/CLAUDE.md](/CLAUDE.md) — точка входа для Claude Code
- [/README.md](/README.md) — описание проекта
