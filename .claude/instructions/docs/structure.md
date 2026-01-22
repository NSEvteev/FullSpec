---
type: project
description: Структура /doc/, документирование кода, шаблоны, workflow
governed-by: docs/README.md
related:
  - docs/rules.md
  - docs/templates.md
  - git/issues.md
---

# Структура и документирование

Правила организации зеркалирования документации в директорию `/doc/`.

## Оглавление

- [1. ЧТО: Структура /doc/](#1-что-структура-doc)
  - [Принцип зеркалирования](#принцип-зеркалирования)
  - [Что зеркалируется](#что-зеркалируется)
  - [Типы документов](#типы-документов)
  - [Дерево /doc/](#дерево-doc)
- [2. ГДЕ: Структура сервиса /src/](#2-где-структура-сервиса-src)
  - [Дерево файлов сервиса](#дерево-файлов-сервиса)
  - [Обязательные файлы](#обязательные-файлы)
  - [dependencies.yaml](#dependenciesyaml)
- [3. КАК: Документирование кода](#3-как-документирование-кода)
  - [README.md сервиса](#readmemd-сервиса)
  - [Ссылки в коде](#ссылки-в-коде)
  - [Комментарии](#комментарии)
- [4. Workflow документации](#4-workflow-документации)
- [5. Шаблоны документации](#5-шаблоны-документации)
- [6. Скиллы](#6-скиллы)
- [7. Примеры](#7-примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## 1. ЧТО: Структура /doc/

### Принцип зеркалирования

**Правило:** Документация располагается рядом с тем, что документирует (colocation principle).

| Код | Документация |
|-----|--------------|
| `/src/auth/backend/handlers.ts` | `/doc/src/auth/backend/handlers.md` |
| `/shared/libs/errors/` | `/doc/shared/libs/errors.md` |
| `/platform/gateway/` | `/doc/platform/gateway/README.md` |

### Что зеркалируется

**Правило:** Зеркалируются только папки, содержимое которых требует документации.

| Папка | Зеркалируется | Причина |
|-------|:-------------:|---------|
| `/src/` | ✅ | Сервисы требуют документации: API, runbooks |
| `/shared/` | ✅ | Библиотеки и контракты нужно документировать для потребителей |
| `/platform/` | ✅ | Инфраструктура требует runbooks, инструкций по деплою |
| `/config/` | ❌ | Конфиги самодокументируемы (комментарии внутри YAML) |
| `/tests/` | ❌ | Тесты сами являются документацией (код = спецификация) |
| `/.github/` | ❌ | Workflows самодокументируемы (YAML с комментариями) |

### Типы документов в /doc/

**Правило:** Каждый тип документа имеет своё место в структуре.

| Тип | Расположение | Назначение |
|-----|--------------|------------|
| README.md | Корень каждой папки | Точка входа: обзор, ссылки, быстрый старт |
| API docs | `/doc/src/{service}/backend/` | Документация API, handlers |
| Schema docs | `/doc/src/{service}/database/` | Документация схемы БД |
| Runbooks | `/doc/runbooks/`, `/doc/src/{service}/runbooks/` | Инструкции по эксплуатации |

> **Примечание:** Спецификации сервисов (ADR, Plans, Architecture) хранятся в `/specs/`.
> См. [/.claude/instructions/specs/](../specs/README.md)

### Дерево /doc/

```
/doc/
  README.md                 # как работать с документацией
  glossary.md               # глоссарий терминов проекта
  /runbooks/                # общие runbooks (инфра, БД)
    database-full.md
    high-load.md
    backup-restore.md

  # Зеркало /src/ — документация сервисов
  /src/
    /auth/
      README.md             # обзор сервиса
      /backend/
        handlers.md
        api.md
      /database/
        schema.md
      /runbooks/            # runbooks этого сервиса
        token-issues.md

  # Зеркало /shared/ — документация библиотек и контрактов
  /shared/
    README.md
    /contracts/
      README.md
    /libs/
      errors.md
      logging.md

  # Зеркало /platform/ — документация инфраструктуры
  /platform/
    README.md
    /gateway/
      README.md
    /docker/
      README.md
    /monitoring/
      README.md
    /runbooks/
      deploy.md
      rollback.md
      incident-response.md
```

---

## 2. ГДЕ: Структура сервиса /src/

> **SSOT:** Структура сервиса описана в [services/structure.md](../services/structure.md)

Каждый сервис в `/src/{service}/` имеет стандартную структуру:

```
/src/{service}/
├── README.md               # Точка входа
├── Makefile                # Команды сервиса
├── dependencies.yaml       # Зависимости
├── .env.example            # Переменные окружения
├── /backend/               # Серверный код
├── /database/              # Схема и миграции
└── /tests/                 # Unit тесты
```

> См. также:
> - [services/lifecycle.md](../services/lifecycle.md) — создание и удаление сервиса
> - [services/dependencies.md](../services/dependencies.md) — формат dependencies.yaml

---

## 3. КАК: Документирование кода

### README.md сервиса

Каждый сервис содержит `README.md` — точку входа.

> **SSOT:** Шаблон README.md сервиса — в [services/structure.md](../services/structure.md#readmemd-сервиса)

### Ссылки в коде

Файлы кода содержат ссылку на документацию в начале:

**Python:**
```python
"""
Auth handlers.

Документация: /doc/src/auth/backend/handlers.md
"""
```

**TypeScript/JavaScript:**
```typescript
/**
 * Auth handlers.
 *
 * Документация: /doc/src/auth/backend/handlers.md
 */
```

### Комментарии

- Комментировать **"почему"**, а не **"что"**
- Код должен быть самодокументируемым
- Сложная логика требует пояснения
- Использовать JSDoc/docstrings для публичных API

```python
# ❌ Плохо — описывает "что"
# Увеличиваем счётчик на 1
counter += 1

# ✅ Хорошо — объясняет "почему"
# Пропускаем первую строку CSV (заголовки)
counter += 1
```

---

## 4. Workflow документации

### Область ответственности /doc/

`/doc/` отвечает **только за документирование кода** — зеркалирование `/src/`, `/shared/`, `/platform/`.

```
/src/{service}/                     # код
    ↓ (docs-create)
/doc/src/{service}/                 # документация кода
```

> **Полный workflow разработки** (от идеи до реализации) описан в [/.claude/instructions/specs/workflow.md](../specs/workflow.md).
> Спецификации (Discussion → Impact → ADR → Plan) живут в `/specs/`.

### Связь src ↔ doc

**Правило:** При создании файла в `/src/{service}/{path}` — создать `/doc/src/{service}/{path}.md` и добавить ссылку в начало файла.

| Файл в /src/ | Документация в /doc/ |
|--------------|---------------------|
| `/src/auth/` | `/doc/src/auth/` |
| `/src/auth/backend/handlers.ts` | `/doc/src/auth/backend/handlers.md` |
| `/src/notification/database/schema.sql` | `/doc/src/notification/database/schema.md` |

### Скиллы

| Событие | Действие | Скилл |
|---------|----------|-------|
| Создан файл в `/src/` | Создать документацию в `/doc/src/` | `/docs-create` |
| Изменён файл в `/src/` | Обновить документацию | `/docs-update` |
| Удалён файл из `/src/` | Пометить документацию, создать Issue | `/docs-delete` |

---

## 5. Шаблоны документации

**Шаблоны:** [templates.md](./templates.md)

Шаблоны зависят от типа файла (backend, database, frontend, minimal). Выбирайте подходящий.

---

## 6. Скиллы

Скиллы для автоматизации работы с документацией:

| Скилл | Назначение |
|-------|------------|
| [/docs-create](/.claude/skills/docs-create/SKILL.md) | Создание документации для нового файла в /src/ |
| [/docs-update](/.claude/skills/docs-update/SKILL.md) | Обновление документации при изменении кода |
| [/docs-delete](/.claude/skills/docs-delete/SKILL.md) | Пометка документации при удалении файла |
| [/docs-reindex](/.claude/skills/docs-reindex/SKILL.md) | Полная переиндексация документации |

### /docs-create

Создаёт:
1. Файл `/doc/src/{service}/{path}.md` по шаблону
2. Ссылку на документацию в исходном файле

### /docs-update

Обновляет документацию при изменении:
- Сигнатур функций/методов
- Структуры модуля
- Зависимостей

### /docs-delete

При удалении файла из `/src/`:
1. Помечает документацию в `/doc/` как требующую ревью
2. Создаёт GitHub Issue для отслеживания

---

## 7. Примеры

### Пример 1: Документирование нового сервиса

**Задача:** Создать документацию для сервиса `auth`.

**Структура:**
```
/doc/src/auth/
  README.md                     # обзор сервиса
  /backend/
    handlers.md                 # документация handlers.ts
    api.md                      # описание API
  /runbooks/
    token-issues.md             # что делать при проблемах с токенами
```

> **Спецификации сервиса** (ADR, Plans, Architecture) создаются в `/specs/services/auth/`.
> См. [/.claude/instructions/specs/](../specs/README.md)

### Пример 2: Runbook

**Файл:** `/doc/src/auth/runbooks/token-issues.md`

```markdown
# Token Issues Runbook

## Симптомы

- Пользователи получают 401 Unauthorized
- Логи: "Token validation failed"

## Диагностика

1. Проверить время на серверах: `date`
2. Проверить секрет JWT: `kubectl get secret jwt-secret`

## Решение

1. Если время разошлось — синхронизировать NTP
2. Если секрет изменился — перезапустить сервис
```

### Пример 3: Файл с обработчиками

**Файл:** `/src/auth/backend/handlers.py`

```python
"""
Обработчики аутентификации.

Документация: /doc/src/auth/backend/handlers.md
"""

def login(request):
    """
    Аутентификация пользователя.

    Args:
        request: HTTP запрос с credentials

    Returns:
        JWT токен при успехе
    """
    # Проверяем rate limit перед валидацией
    # (защита от brute-force атак)
    check_rate_limit(request.ip)
    ...
```

---

## Связанные инструкции

- [git/issues.md](../git/issues.md) — создание Issue при удалении документации
- [/.claude/templates/README.md](/.claude/templates/README.md) — SSOT шаблоны документации

---

> **Путь:** `/.claude/instructions/docs/structure.md`
