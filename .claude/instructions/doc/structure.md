---
type: project
description: Структура /doc/: зеркалирование, ссылки на код, ADR, runbooks
related:
  - tools/documentation.md
---

# Структура документации

Правила организации документации в `/doc/`. Зеркалирует структуру `/src/`, `/shared/`, `/platform/`.

## Оглавление

- [Правила](#правила)
  - [Принцип зеркалирования](#принцип-зеркалирования)
  - [Что зеркалируется](#что-зеркалируется)
  - [Типы документов](#типы-документов)
  - [Workflow документации](#workflow-документации)
- [Структура /doc/](#структура-doc)
- [Примеры](#примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

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
| `/src/` | ✅ | Сервисы требуют документации: API, архитектура, ADR, runbooks |
| `/shared/` | ✅ | Библиотеки и контракты нужно документировать для потребителей |
| `/platform/` | ✅ | Инфраструктура требует runbooks, инструкций по деплою |
| `/config/` | ❌ | Конфиги самодокументируемы (комментарии внутри YAML) |
| `/tests/` | ❌ | Тесты сами являются документацией (код = спецификация) |
| `/.github/` | ❌ | Workflows самодокументируемы (YAML с комментариями) |

### Типы документов

**Правило:** Каждый тип документа имеет своё место в структуре.

| Тип | Расположение | Назначение |
|-----|--------------|------------|
| README.md | Корень каждой папки | Точка входа: обзор, ссылки, быстрый старт |
| ADR | `/doc/src/{service}/specs/adr/` | Фиксация архитектурных решений |
| Runbooks | `/doc/runbooks/`, `/doc/src/{service}/runbooks/` | Инструкции по эксплуатации |
| Specs | `/doc/src/{service}/specs/` | Архитектура, планы реализации |

**Формат ADR:**
- Название: `NNNN-название.md`
- Содержит: контекст, решение, последствия

### Workflow документации

**Правило:** Документация создаётся по этапам от дискуссии до кода.

```
Дискуссия (/.claude/discussions/)
    ↓ (решение принято)
/doc/src/{service}/specs/adr/       # ADR
    ↓
/doc/src/{service}/specs/plans/     # план реализации
    ↓
/src/{service}/                     # код
    ↓
/doc/src/{service}/backend/         # документация кода
```

**Этапы:**

1. **Дискуссия** — обсуждение подхода в `/.claude/discussions/`
2. **ADR** — фиксация решения в `/doc/src/{service}/specs/adr/`
3. **План** — детальный план в `/doc/src/{service}/specs/plans/`
4. **Код** — реализация в `/src/{service}/`
5. **Документация** — описание API в `/doc/src/{service}/`

---

## Структура /doc/

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
      /specs/               # спецификации
        /architecture/      # архитектурные описания
        /adr/               # ADR этого сервиса
          0001-jwt-tokens.md
        /plans/             # планы реализации
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

## Примеры

### Пример 1: Документирование нового сервиса

**Задача:** Создать документацию для сервиса `auth`.

**Структура:**
```
/doc/src/auth/
  README.md                     # обзор сервиса
  /specs/
    /adr/
      0001-jwt-tokens.md        # решение по токенам
    /plans/
      oauth-implementation.md   # план реализации OAuth
  /backend/
    handlers.md                 # документация handlers.ts
    api.md                      # описание API
  /runbooks/
    token-issues.md             # что делать при проблемах с токенами
```

### Пример 2: Добавление ADR

**Задача:** Зафиксировать решение использовать JWT токены.

**Файл:** `/doc/src/auth/specs/adr/0001-jwt-tokens.md`

```markdown
# 0001: Использование JWT токенов

## Статус

Принято

## Контекст

Нужен механизм аутентификации для микросервисной архитектуры.

## Решение

Использовать JWT токены с коротким временем жизни (15 мин) и refresh токены.

## Последствия

- (+) Stateless аутентификация
- (+) Легко масштабируется
- (-) Нельзя отозвать токен до истечения
```

### Пример 3: Создание runbook

**Задача:** Документировать процедуру при проблемах с токенами.

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

---

## Автоматизация

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Создание документации для файла в /src/ |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление документации при изменении кода |
| [/doc-delete](/.claude/skills/doc-delete/SKILL.md) | Пометка документации при удалении файла |

---

## Связанные инструкции

- [tools/documentation.md](../tools/documentation.md) — документирование кода, ссылки src ↔ doc
