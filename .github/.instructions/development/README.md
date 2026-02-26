---
description: Инструкции для процесса локальной разработки — стандарт, валидация перед push. Индекс документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/development/README.md
---

# Инструкции /.github/.instructions/development/

Инструкции для процесса локальной разработки.

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [SSOT .github](../../README.md)

**Содержание:** Процесс работы в feature-ветке, make-команды, тестирование, локальные проверки качества.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы и агенты](#5-скиллы-и-агенты) | — | Скиллы и агенты для этой области |

```
/.github/.instructions/development/
├── README.md                      # Этот файл (индекс)
├── create-development.md           # Воркфлоу запуска разработки по analysis chain
├── modify-development.md           # Воркфлоу процесса разработки в feature-ветке
├── standard-development.md        # Стандарт локальной разработки
└── validation-development.md      # Валидация процесса разработки
```

---

# 1. Стандарты

## 1.1. Стандарт локальной разработки

Процесс работы в feature-ветке, make-команды, тестирование, локальные проверки качества.

**Оглавление:**
- [Запуск разработки](./standard-development.md#0-запуск-разработки)
- [Взятие задачи](./standard-development.md#1-взятие-задачи)
- [Процесс разработки](./standard-development.md#2-процесс-разработки)
- [Make-команды](./standard-development.md#3-make-команды)
- [Тестирование](./standard-development.md#4-тестирование)
- [Проверки качества](./standard-development.md#5-проверки-качества)
- [Работа с зависимостями](./standard-development.md#6-работа-с-зависимостями)
- [Завершение работы над Issue](./standard-development.md#7-завершение-работы-над-issue)
- [Запреты и ограничения](./standard-development.md#8-запреты-и-ограничения)
- [Требования по уровням критичности сервисов](./standard-development.md#9-требования-по-уровням-критичности-сервисов)

**Инструкция:** [standard-development.md](./standard-development.md)

---

# 2. Воркфлоу

## 2.1. Запуск разработки по analysis chain

Воркфлоу перехода analysis chain из WAITING в RUNNING: создание Issues, Milestone, ветки.

**Инструкция:** [create-development.md](./create-development.md)

## 2.2. Процесс разработки в feature-ветке

Воркфлоу работы в feature-ветке: взятие задачи, написание кода, тестирование, коммит. Используется когда ветка уже в RUNNING.

**Инструкция:** [modify-development.md](./modify-development.md)

---

# 3. Валидация

## 3.1. Валидация процесса разработки

Проверка соблюдения процесса локальной разработки: тесты, линтер, сборка, зависимости, полнота реализации.

**Инструкция:** [validation-development.md](./validation-development.md)

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [check-chain-readiness.py](../.scripts/check-chain-readiness.py) | Проверка готовности цепочки (4/4 WAITING, 0 маркеров) | [create-development.md](./create-development.md) |
| [dev-next-issue.py](../.scripts/dev-next-issue.py) | Определение следующего незаблокированного Issue | [modify-development.md](./modify-development.md) |

---

# 5. Скиллы и агенты

| Артефакт | Назначение | Инструкция |
|----------|------------|------------|
| [/dev-create](/.claude/skills/dev-create/SKILL.md) | Запуск разработки по analysis chain (WAITING → RUNNING) | [create-development.md](./create-development.md) |
| [dev-agent](/.claude/agents/dev-agent/AGENT.md) | Агент разработки — выполняет BLOCK-N (RUNNING) | [modify-development.md](./modify-development.md) |
