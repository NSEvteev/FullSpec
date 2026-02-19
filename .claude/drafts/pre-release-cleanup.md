# Финальная очистка проекта перед релизом

Чек-лист всего, что нужно удалить из проекта-шаблона перед его публикацией/использованием. Все перечисленные элементы — тестовые данные, созданные при разработке инструментов и процессов.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. SDD-документы (realtime notifications)](#1-sdd-документы-realtime-notifications)
  - [2. Технологии (PostgreSQL, Redis)](#2-технологии-postgresql-redis)
  - [3. Архитектурные заглушки сервисов](#3-архитектурные-заглушки-сервисов)
  - [4. GitHub метки svc:*](#4-github-метки-svc)
  - [5. Planned Changes в архитектуре](#5-planned-changes-в-архитектуре)
  - [6. Черновики](#6-черновики)
  - [7. Прочее](#7-прочее)
- [Порядок удаления](#порядок-удаления)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** Подготовка проекта-шаблона к релизу
**Почему создан:** В процессе разработки SDD-фреймворка, инструкций и скриптов были созданы тестовые данные (дискуссия, импакт, дизайн "realtime notifications"; стандарты PostgreSQL/Redis; заглушки сервисов). Эти данные нужны были для проверки процессов, но не должны попасть в чистый шаблон.

## Содержание

### 1. SDD-документы (realtime notifications)

Полный цикл тестового SDD-документа: Discussion → Impact → Design.

| Файл | Что это |
|------|---------|
| `specs/discussion/disc-0001-realtime-notifications.md` | Тестовая дискуссия |
| `specs/impact/impact-0001-realtime-notifications.md` | Тестовый импакт |
| `specs/design/design-0001-realtime-notifications.md` | Тестовый дизайн |

**Способ удаления:** Удалить файлы. README в каждой папке обновить (убрать строки из таблиц).

### 2. Технологии (PostgreSQL, Redis)

Per-tech стандарты и всё связанное с ними.

| Файл | Что это |
|------|---------|
| `specs/technologies/standard-postgresql.md` | Тестовый стандарт |
| `specs/technologies/validation-postgresql.md` | Тестовая валидация |
| `specs/technologies/standard-redis.md` | Тестовый стандарт |
| `specs/technologies/validation-redis.md` | Тестовая валидация |
| `specs/.instructions/.scripts/validate-postgresql-code.py` | Тестовый скрипт валидации кода |
| `specs/.instructions/.scripts/validate-redis-code.py` | Тестовый скрипт валидации кода |
| `.claude/rules/postgresql.md` | Rule автозагрузки стандарта |
| `.claude/rules/redis.md` | Rule автозагрузки стандарта |

**Дополнительные изменения:**
- `.pre-commit-config.yaml` — удалить хуки #15 (`postgresql-code-validate`) и #16 (`redis-code-validate`)
- `.structure/pre-commit.md` — удалить строки из таблицы "Активные хуки"
- `specs/technologies/README.md` — удалить строки из таблицы и дерева

### 3. Архитектурные заглушки сервисов

| Файл | Что это |
|------|---------|
| `specs/architecture/services/auth.md` | Заглушка сервиса |
| `specs/architecture/services/frontend.md` | Заглушка сервиса |
| `specs/architecture/services/gateway.md` | Заглушка сервиса |
| `specs/architecture/services/notification.md` | Заглушка сервиса |

**Дополнительные изменения:**
- `specs/architecture/services/README.md` — удалить строки из таблицы и дерева

### 4. GitHub метки svc:*

| Метка | Что это |
|-------|---------|
| `svc:notification` | Тестовая метка сервиса |
| `svc:frontend` | Тестовая метка сервиса |
| `svc:gateway` | Тестовая метка сервиса |
| `svc:auth` | Тестовая метка сервиса |

**Способ удаления:**
- `.github/labels.yml` — удалить 4 записи svc:*
- GitHub (remote) — удалить метки через `gh label delete`

### 5. Planned Changes в архитектуре

Ссылки на тестовый SDD-документ в architecture:

| Файл | Что удалить |
|------|-------------|
| `specs/architecture/domains/context-map.md` | Секция "Planned Changes" |
| `specs/architecture/system/overview.md` | Секция "Planned Changes" |

### 6. Черновики

Все черновики — это рабочие заметки разработки фреймворка.

| Файл | Решение |
|------|---------|
| `drafts/2026-02-08-specification-driven-development.md` | Удалить |
| `drafts/2026-02-10-specs-documents-plan.md` | Удалить |
| `drafts/2026-02-15-specs-readme-format-gap.md` | Удалить |
| `drafts/2026-02-16-per-tech-validation-scripts.md` | Удалить |
| `drafts/maybe-archive/*` (6 файлов) | Удалить всю папку |
| `drafts/examples/*` | **Оставить** (эталонные примеры) |
| Этот файл (`pre-release-cleanup.md`) | Удалить последним |

**Дополнительные изменения:**
- `drafts/README.md` — обновить таблицу и дерево

### 7. Прочее

| Элемент | Что это | Действие |
|---------|---------|----------|
| `.claude/settings.local.json` | Локальные настройки | В `.gitignore` (уже untracked) |

---

## Порядок удаления

> Порядок важен из-за перекрёстных ссылок и pre-commit хуков.

1. **Сначала** — скрипты и pre-commit хуки (иначе хуки будут ругаться на отсутствие файлов)
2. **Затем** — SDD-документы + архитектурные заглушки + Planned Changes
3. **Затем** — технологии + rules
4. **Затем** — labels (yml + remote)
5. **Затем** — черновики (кроме examples/)
6. **Последним** — этот файл + обновление всех README

---

## Решения

- **SDD-примеры:** Не оставлять. Примеров в `drafts/examples/` достаточно. Возможно позже будут созданы "общие сервисы" (вход, аутентификация, API gateway) — но это новая работа, а не сохранение тестовых данных.
- **maybe-archive/:** Удалить целиком. Не переносить в examples/.
- **Автоматизация:** Ручное удаление по чек-листу. Без скрипта.
