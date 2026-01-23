---
type: project
description: Индекс инструкций по конфигурации окружений и фича-флагов
related:
  - platform/deployment.md
  - platform/docker.md
  - src/dev/local.md
---

# Инструкции /config/

Инструкции по конфигурации окружений и управлению фича-флагами.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Environments](#1-environments) | [environments.md](./environments.md) | Конфигурация окружений |
| [2. Feature Flags](#2-feature-flags) | [feature-flags.md](./feature-flags.md) | Управление фича-флагами |

---

# 1. Environments

Конфигурации окружений: development, staging, production.

**Содержание:** структура `/config/environments/`, формат YAML файлов, правила хранения секретов, переопределение через ENV.

### Окружения

| Окружение | Файл | Назначение |
|-----------|------|------------|
| Development | `development.yaml` | Локальная разработка, debug режим |
| Staging | `staging.yaml` | Тестирование перед продакшн |
| Production | `production.yaml` | Продакшн окружение |

### Ключевые правила

| Правило | Описание |
|---------|----------|
| Секреты через ENV | Пароли, токены, ключи — через `${VAR}` |
| Минимальные различия | Только хосты, порты, уровни логов |
| Fail-fast валидация | Сервис проверяет конфиг при запуске |

**Инструкция:** [environments.md](./environments.md)

---

# 2. Feature Flags

Правила использования флагов функций для управления релизами.

**Содержание:** когда использовать флаги, YAML vs Unleash, структура флага, жизненный цикл, правила удаления.

### Варианты реализации

| Вариант | Когда использовать |
|---------|-------------------|
| YAML файл | До 10 флагов, нет A/B тестов |
| Unleash | Много флагов, A/B тесты, динамическое управление |

### Ключевые правила

| Правило | Описание |
|---------|----------|
| Временность | Флаги живут максимум 3 месяца |
| Обязательные поля | enabled, description, owner, created, expires |
| Тестирование | Оба состояния (true/false) должны быть покрыты |

**Инструкция:** [feature-flags.md](./feature-flags.md)

---

## Связанные инструкции

- [platform/deployment.md](../platform/deployment.md) — стратегии деплоя и окружения
- [platform/docker.md](../platform/docker.md) — Docker конфигурация
- [src/dev/local.md](../src/dev/local.md) — локальная разработка

## Связанные скиллы

| Скилл | Назначение |
|-------|------------|
| [/environment-check](/.claude/skills/environment-check/SKILL.md) | Проверка окружения (gh, git, python) |
