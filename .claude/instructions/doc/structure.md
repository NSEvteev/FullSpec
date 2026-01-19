---
type: project
description: Структура /doc/: зеркалирование, ссылки на код, ADR, runbooks
related:
  - src/documentation.md
---

# Структура документации

Правила организации документации в `/doc/`. Зеркалирует структуру `/src/`, `/shared/`, `/platform/`.

## Оглавление

- [Принцип зеркалирования](#принцип-зеркалирования)
- [Структура /doc/](#структура-doc)
- [Что зеркалируется](#что-зеркалируется)
- [Workflow документации](#workflow-документации)
- [Типы документов](#типы-документов)
- [Связанные инструкции](#связанные-инструкции)

---

## Принцип зеркалирования

**Правило:** Документация располагается рядом с тем, что документирует (colocation principle).

| Код | Документация |
|-----|--------------|
| `/src/auth/backend/handlers.ts` | `/doc/src/auth/backend/handlers.md` |
| `/shared/libs/errors/` | `/doc/shared/libs/errors.md` |
| `/platform/gateway/` | `/doc/platform/gateway/README.md` |

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

## Что зеркалируется

| Папка | Зеркалируется | Причина |
|-------|:-------------:|---------|
| `/src/` | ✅ | Сервисы требуют документации: API, архитектура, ADR, runbooks |
| `/shared/` | ✅ | Библиотеки и контракты нужно документировать для потребителей |
| `/platform/` | ✅ | Инфраструктура требует runbooks, инструкций по деплою |
| `/config/` | ❌ | Конфиги самодокументируемы (комментарии внутри YAML) |
| `/tests/` | ❌ | Тесты сами являются документацией (код = спецификация) |
| `/.github/` | ❌ | Workflows самодокументируемы (YAML с комментариями) |

---

## Workflow документации

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

### Этапы

1. **Дискуссия** — обсуждение подхода в `/.claude/discussions/`
2. **ADR** — фиксация решения в `/doc/src/{service}/specs/adr/`
3. **План** — детальный план в `/doc/src/{service}/specs/plans/`
4. **Код** — реализация в `/src/{service}/`
5. **Документация** — описание API в `/doc/src/{service}/`

---

## Типы документов

### README.md

Точка входа для каждой папки:
- Обзор содержимого
- Ссылки на ключевые файлы
- Быстрый старт

### ADR (Architecture Decision Records)

Фиксация архитектурных решений:
- Расположение: `/doc/src/{service}/specs/adr/`
- Формат: `NNNN-название.md`
- Содержит: контекст, решение, последствия

### Runbooks

Инструкции по эксплуатации:
- Общие: `/doc/runbooks/`
- Сервисные: `/doc/src/{service}/runbooks/`
- Инфраструктурные: `/doc/platform/runbooks/`

### Specs

Спецификации сервиса:
- `/specs/architecture/` — архитектурные описания
- `/specs/adr/` — решения
- `/specs/plans/` — планы реализации

---

## Связанные инструкции

- [src/documentation.md](../src/documentation.md) — документирование кода, ссылки src ↔ doc
