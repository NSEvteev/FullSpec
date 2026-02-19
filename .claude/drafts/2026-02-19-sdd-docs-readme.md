# docs/README.md — индекс сервисов

Спецификация docs/README.md: секции, шаблон, пример. Чистый навигатор по сервисам и системным документам.

## Контекст

**Задача:** Определить формат docs/README.md — индексного файла контура docs/, содержащего таблицу сервисов и ссылки на системные документы.

**Источник:** `.claude/drafts/2026-02-19-sdd-chain-rethink.md` (строки 265-381)

**Связанные файлы:**
- `2026-02-19-sdd-structure.md` — общая структура и решения
- `2026-02-19-sdd-docs-overview.md` — overview.md (архитектурный слой, на который ссылается README)
- `2026-02-19-sdd-docs-service.md` — формат {svc}.md (на которые ссылается таблица)

---

## Содержание

Чистый навигатор. Архитектурная информация — в `.system/overview.md`.

### Секции docs/README.md

| # | Секция | Содержание |
|---|--------|-----------|
| 1 | **Заголовок** | Название системы, одно предложение назначения |
| 2 | **Сервисы** | Таблица: сервис, назначение, ключевые технологии, ссылка на {svc}.md |
| 3 | **Системные документы** | Ссылки на .system/overview.md, .system/conventions.md, .system/infrastructure.md |
| 4 | **Стандарты технологий** | Ссылки на .technologies/standard-{tech}.md |
| 5 | **Дерево** | ASCII-дерево docs/ |

### Шаблон: docs/README.md

`````markdown
# {Название системы}

{Одно предложение — назначение системы.}

**Архитектура:** [overview.md](.system/overview.md) — связи сервисов, data flows, контекстная карта доменов.

## Сервисы

| Сервис | Назначение | Технологии | Документ |
|--------|-----------|-----------|---------|
| {svc} | {что делает, 5-10 слов} | {lang}, {db}, {mq} | [{svc}.md]({svc}.md) |

## Системные документы

| Документ | Описание |
|----------|----------|
| [overview.md](.system/overview.md) | Архитектура системы: связи сервисов, сквозные потоки, контекстная карта |
| [conventions.md](.system/conventions.md) | Конвенции API: формат ошибок, пагинация, auth + shared-интерфейсы |
| [infrastructure.md](.system/infrastructure.md) | Платформа: деплой, сети, мониторинг, окружения |
| [testing.md](.system/testing.md) | Тестирование: типы, структура, мокирование, команды |

## Стандарты технологий

| Технология | Стандарт |
|-----------|---------|
| {tech} | [standard-{tech}.md](.technologies/standard-{tech}.md) |

## Дерево

```
specs/docs/
├── .system/
│   ├── conventions.md
│   ├── infrastructure.md
│   └── overview.md
├── .technologies/
│   └── standard-{tech}.md
├── {svc1}.md
├── {svc2}.md
└── README.md
```
`````

### Пример: docs/README.md

`````markdown
# MyApp

Платформа управления задачами с real-time уведомлениями и ролевым доступом.

**Архитектура:** [overview.md](.system/overview.md) — связи сервисов, data flows, контекстная карта доменов.

## Сервисы

| Сервис | Назначение | Технологии | Документ |
|--------|-----------|-----------|---------|
| auth | Аутентификация, авторизация, управление пользователями | Python, PostgreSQL | [auth.md](auth.md) |
| notification | Push-уведомления в реальном времени через WebSocket | Python, PostgreSQL, Redis | [notification.md](notification.md) |
| task | Управление задачами, проектами, назначениями | Python, PostgreSQL | [task.md](task.md) |
| admin | Административная панель, управление ролями | Python, PostgreSQL | [admin.md](admin.md) |

## Системные документы

| Документ | Описание |
|----------|----------|
| [overview.md](.system/overview.md) | Архитектура системы: связи сервисов, сквозные потоки, контекстная карта |
| [conventions.md](.system/conventions.md) | Конвенции API: формат ошибок, пагинация, auth + shared-интерфейсы |
| [infrastructure.md](.system/infrastructure.md) | Платформа: деплой, сети, мониторинг, окружения |
| [testing.md](.system/testing.md) | Тестирование: типы, структура, мокирование, команды |

## Стандарты технологий

| Технология | Стандарт |
|-----------|---------|
| Python | [standard-python.md](.technologies/standard-python.md) |
| PostgreSQL | [standard-postgresql.md](.technologies/standard-postgresql.md) |
| Redis | [standard-redis.md](.technologies/standard-redis.md) |

## Дерево

```
specs/docs/
├── .system/
│   ├── conventions.md       # Конвенции API, shared-интерфейсы
│   ├── infrastructure.md    # Платформа, деплой, мониторинг
│   ├── overview.md          # Архитектура, связи, потоки
│   └── testing.md           # Тестирование: типы, структура, команды
├── .technologies/
│   ├── standard-postgresql.md  # Стандарт PostgreSQL
│   ├── standard-python.md      # Стандарт Python
│   └── standard-redis.md       # Стандарт Redis
├── admin.md                 # Админ-панель
├── auth.md                  # Аутентификация
├── notification.md          # Уведомления
├── task.md                  # Задачи
└── README.md                # Этот файл
```
`````

---

## Аудит старых документов

| Старый документ | Что переиспользовать |
|-----------------|---------------------|
| `specs/architecture/services/README.md` | Текущий формат таблицы сервисов (адаптировать колонки) |
