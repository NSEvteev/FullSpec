---
description: Инструкции для GitHub Releases — стандарт, создание, валидация. Индекс документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/releases/README.md
---

# Инструкции /.github/.instructions/releases/

Релизы и деплой.

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [SSOT .github](../../README.md)

**Содержание:** Версионирование, Changelog, процесс релиза, Hotfix, Rollback.

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
/.github/.instructions/releases/
├── README.md                    # Этот файл (индекс)
├── standard-release.md          # Стандарт релизов (версионирование, changelog, процесс, hotfix, rollback)
├── validation-release.md        # Валидация Release (pre/post чеклист)
└── create-release.md            # Воркфлоу создания Release
```

---

# 1. Стандарты

## 1.1. Стандарт релизов

Версионирование, changelog, процесс релиза, hotfix, rollback.

**Оглавление:**
- [Назначение](./standard-release.md#1-назначение)
- [Версионирование](../milestones/standard-milestone.md#4-версионирование-semver)
- [Changelog](./standard-release.md#5-changelog)
- [Жизненный цикл](./standard-release.md#8-жизненный-цикл-release)
- [Подготовка](./standard-release.md#9-подготовка-релиза)
- [Создание](./standard-release.md#10-создание-релиза)
- [Публикация](./standard-release.md#11-публикация-на-production)
- [Hotfix](./standard-release.md#12-hotfix-релиз)
- [Rollback](./standard-release.md#13-rollback-процесс)

**Инструкция:** [standard-release.md](./standard-release.md)

---

# 2. Воркфлоу

## 2.1. Создание Release

Пошаговый процесс создания GitHub Release для LLM: определение версии → проверки → сборка body → публикация → CHANGELOG.

**Инструкция:** [create-release.md](./create-release.md)

---

# 3. Валидация

## 3.1. Валидация Release

Чеклист проверки GitHub Release: pre-release готовность, объект Release, Release Notes, CHANGELOG.md, деплой.

**Инструкция:** [validation-release.md](./validation-release.md)

---

# 4. Скрипты

*Нет скриптов.*

---

# 5. Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/post-release](/.claude/skills/post-release/SKILL.md) | Post-release валидация | [validation-release.md](./validation-release.md) |
| [/release-create](/.claude/skills/release-create/SKILL.md) | Создание GitHub Release | [create-release.md](./create-release.md) |
