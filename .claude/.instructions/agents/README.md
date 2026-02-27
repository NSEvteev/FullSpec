---
description: Инструкции для Claude Code агентов — стандарт формата AGENT.md, создание, изменение, валидация. Индекс документов и скриптов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
index: .claude/.instructions/agents/README.md
---

# Инструкции /.claude/agents/

Индекс инструкций для папки agents/.

**Полезные ссылки:**
- [Инструкции .claude/](../README.md)
- [.claude/](../../README.md)

**Содержание:** конфигурация агентов, типы, промпты.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для этой области |

```
/.claude/.instructions/agents/
├── .scripts/
│   ├── create-agent-file.py  # Создание файла агента
│   ├── find-agent-refs.py    # Поиск ссылок на агента
│   ├── list-agents.py        # Список агентов
│   └── validate-agent.py     # Скрипт валидации
├── README.md                 # Этот файл (индекс)
├── create-agent.md           # Создание агентов
├── modify-agent.md           # Изменение агентов
├── standard-agent.md         # Стандарт агентов
└── validation-agent.md       # Валидация агентов
```

---

# 1. Стандарты

## 1.1. Стандарт агентов

Формат конфигураций, типы и правила написания промптов для агентов Claude.

**Оглавление:**
- [Назначение агентов](./standard-agent.md#1-назначение-агентов)
- [Типы агентов](./standard-agent.md#2-типы-агентов)
- [Формат конфигурации](./standard-agent.md#3-формат-конфигурации)
- [Правила написания промптов](./standard-agent.md#4-правила-написания-промптов)
- [Контекст для агента](./standard-agent.md#5-контекст-для-агента)
- [Примеры промптов](./standard-agent.md#6-примеры-промптов)
- [Расположение и именование](./standard-agent.md#7-расположение-и-именование)
- [Обработка ошибок](./standard-agent.md#8-обработка-ошибок)
- [Отмена и прерывание](./standard-agent.md#9-отмена-и-прерывание)
- [Безопасность](./standard-agent.md#10-безопасность)

**Инструкция:** [standard-agent.md](./standard-agent.md)

---

# 2. Воркфлоу

## 2.1. Создание агентов

Пошаговый процесс создания нового агента для Claude Code.

**Оглавление:**
- [Определить необходимость](./create-agent.md#шаг-1-определить-необходимость)
- [Выбрать тип агента](./create-agent.md#шаг-2-выбрать-тип-агента)
- [Собрать контекст](./create-agent.md#шаг-3-собрать-контекст)
- [Написать промпт](./create-agent.md#шаг-5-написать-промпт)
- [Чек-лист](./create-agent.md#чек-лист)

**Инструкция:** [create-agent.md](./create-agent.md)

## 2.2. Изменение агентов

Обновление, деактивация и миграция агентов.

**Оглавление:**
- [Типы изменений](./modify-agent.md#типы-изменений)
- [Обновление](./modify-agent.md#обновление)
- [Деактивация](./modify-agent.md#деактивация)
- [Миграция](./modify-agent.md#миграция)
- [Чек-лист](./modify-agent.md#чек-лист)

**Инструкция:** [modify-agent.md](./modify-agent.md)

---

# 3. Валидация

## 3.1. Валидация агентов

Валидация конфигурации и промпта агента на соответствие стандарту.

**Оглавление:**
- [Когда валидировать](./validation-agent.md#когда-валидировать)
- [Шаги валидации](./validation-agent.md#шаги)
- [Чек-лист](./validation-agent.md#чек-лист)
- [Типичные ошибки](./validation-agent.md#типичные-ошибки)

**Инструкция:** [validation-agent.md](./validation-agent.md)

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [create-agent-file.py](./.scripts/create-agent-file.py) | Создание файла агента по шаблону | [create-agent.md](./create-agent.md) |
| [list-agents.py](./.scripts/list-agents.py) | Список агентов для проверки уникальности | [create-agent.md](./create-agent.md) |
| [find-agent-refs.py](./.scripts/find-agent-refs.py) | Поиск ссылок на агента | [modify-agent.md](./modify-agent.md) |
| [validate-agent.py](./.scripts/validate-agent.py) | Валидация конфигурации агента | [validation-agent.md](./validation-agent.md) |

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/agent-create](/.claude/skills/agent-create/SKILL.md) | Создание нового агента | [create-agent.md](./create-agent.md) |
| [/agent-modify](/.claude/skills/agent-modify/SKILL.md) | Изменение, деактивация и миграция агента | [modify-agent.md](./modify-agent.md) |
| [/agent-validate](/.claude/skills/agent-validate/SKILL.md) | Валидация конфигурации агента | [validation-agent.md](./validation-agent.md) |

---

# 6. Активные агенты

| Агент | Тип | Назначение |
|-------|-----|------------|
| [meta-reviewer](/.claude/agents/meta-reviewer/AGENT.md) | plan | Семантический анализ документов на ясность и однозначность |
| [meta-agent](/.claude/agents/meta-agent/AGENT.md) | general-purpose | Помощник по созданию инструкций, скиллов, правил и структуры проекта |
| [discussion-reviewer](/.claude/agents/discussion-reviewer/AGENT.md) | general-purpose | Ревью дискуссий SDD на полноту — анализ по объектам, генерация PROP-N рекомендаций |
| [design-agent-first](/.claude/agents/design-agent-first/AGENT.md) | general-purpose | Первая фаза создания Design SDD — Unified Scan, Clarify, Резюме + Выбор технологий + заголовки SVC-N |
| [design-agent-second](/.claude/agents/design-agent-second/AGENT.md) | general-purpose | Вторая фаза создания Design SDD — заполнение SVC-N (9 подсекций), INT-N, STS-N |
| [design-reviewer](/.claude/agents/design-reviewer/AGENT.md) | general-purpose | Ревью проектирования SDD на полноту — покрытие Impact, SVC/INT/STS, зона ответственности |
| [technology-agent](/.claude/agents/technology-agent/AGENT.md) | general-purpose | Создание и обновление per-tech стандарта (standard-{tech}.md + validation-{tech}.md + rule + реестр) |
| [technology-reviewer](/.claude/agents/technology-reviewer/AGENT.md) | explore | Ревью содержания per-tech стандартов — 7 критериев качества, кросс-стандартная согласованность |
| [code-reviewer](/.claude/agents/code-reviewer/AGENT.md) | general-purpose | Ревью кода — анализ diff, сверка с постановкой из specs/analysis/, 7 критериев качества |
| [rollback-agent](/.claude/agents/rollback-agent/AGENT.md) | general-purpose | Откат analysis chain (ROLLING_BACK → REJECTED) — экономит контекст основного LLM |
| [chain-done-agent](/.claude/agents/chain-done-agent/AGENT.md) | general-purpose | Завершение analysis chain (REVIEW → DONE) с обновлением docs/ — экономит контекст основного LLM |
| [dev-agent](/.claude/agents/dev-agent/AGENT.md) | general-purpose | Агент разработки — выполнение блока задач (BLOCK-N) из Plan Dev, CONFLICT-детекция |
