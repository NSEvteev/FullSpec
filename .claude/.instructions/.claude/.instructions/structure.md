---
type: standard
description: Расположение и структура папок инструкций
governed-by: instructions/README.md
related:
  - instructions/types.md
  - instructions/validation.md
---

# Структура инструкций

Правила расположения инструкций в проекте.

**Индекс:** [/.claude/.instructions/README.md](/.claude/.instructions/README.md) | **Папка:** [instructions/README.md](./README.md)

## Оглавление

- [Базовая папка](#базовая-папка)
- [Зеркалирование структуры](#зеркалирование-структуры)
- [Допустимые папки](#допустимые-папки)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Базовая папка

Все инструкции находятся в: **/.claude/.instructions/**

---

## Зеркалирование структуры

Инструкции зеркалируют структуру проекта:

| Папка проекта | Папка инструкций |
|---------------|------------------|
| /src/ | /.claude/.instructions/src/ |
| /platform/ | /.claude/.instructions/platform/ |
| /tests/ | /.claude/.instructions/tests/ |
| /doc/ | /.claude/.instructions/docs/ |
| /shared/ | /.claude/.instructions/shared/ |
| /config/ | /.claude/.instructions/config/ |

---

## Допустимые папки

### Папки проекта

| Папка | Назначение |
|-------|------------|
| src/ | Исходный код сервисов |
| platform/ | Инфраструктура и деплой |
| tests/ | Системные тесты |
| doc/ | Документация |
| shared/ | Общий код и контракты |
| config/ | Конфигурации окружений |

### Внутренние папки Claude

| Папка | Назначение |
|-------|------------|
| git/ | Git workflow, commits, issues |
| skills/ | Скиллы Claude |
| agents/ | Агенты Claude |
| specs/ | Спецификации |
| services/ | Управление сервисами (создание, структура, lifecycle) |
| instructions/ | Мета-инструкции (эта папка) |

---

## Примеры

### Инструкция для API

```
/.claude/.instructions/src/api/design.md
```

### Инструкция для Docker

```
/.claude/.instructions/platform/docker.md
```

### Инструкция для Git commits

```
/.claude/.instructions/git/commits.md
```

### Инструкция для тестирования

```
/.claude/.instructions/tests/e2e.md
```

---

## Скиллы

**Скиллы для этой области отсутствуют.**

Структура папок валидируется скриптом `instruction-validate.py`.

---

## Связанные инструкции

- [types.md](./types.md) — типы инструкций
- [validation.md](./validation.md) — валидация путей
