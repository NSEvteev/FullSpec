---
type: standard
description: Стандартная структура папок сервиса в /src/{service}/
governed-by: services/README.md
related:
  - services/lifecycle.md
  - services/dependencies.md
  - docs/structure.md
---

# Структура сервиса

Стандартная структура папок и файлов сервиса в `/src/{service}/`.

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [services/README.md](./README.md)

## Оглавление

- [Дерево файлов](#дерево-файлов)
- [Обязательные файлы](#обязательные-файлы)
- [README.md сервиса](#readmemd-сервиса)
- [Makefile](#makefile)
- [Папки](#папки)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Дерево файлов

```
/src/{service}/
├── README.md               # Точка входа, ссылка на документацию
├── Makefile                # Команды сервиса (build, test, run)
├── dependencies.yaml       # Зависимости от других сервисов
├── .env.example            # Шаблон переменных окружения
│
├── /backend/               # Серверный код
│   ├── /v1/                # Версия API v1
│   ├── /v2/                # Версия API v2
│   ├── /shared/            # Общая логика между версиями
│   └── /health/            # Health check endpoints
│
├── /frontend/              # Клиентский код (если есть)
│
├── /database/              # Работа с БД
│   ├── schema.sql          # Текущая схема
│   ├── /migrations/        # Миграции
│   └── /seeds/             # Тестовые данные
│
└── /tests/                 # Unit/integration тесты
```

---

## Обязательные файлы

| Файл | Назначение | Обязателен |
|------|------------|:----------:|
| `README.md` | Точка входа в сервис | ✅ |
| `Makefile` | Команды сервиса | ✅ |
| `dependencies.yaml` | Зависимости от других сервисов | ✅ |
| `.env.example` | Шаблон переменных окружения | ✅ |

---

## README.md сервиса

Каждый сервис содержит `README.md` — точку входа с полной информацией.

### Шаблон

```markdown
# {Service} Service

{Краткое описание назначения сервиса — 1-2 предложения}

📖 **Документация:** [/doc/src/{service}/](/doc/src/{service}/)
📋 **Спецификации:** [/specs/services/{service}/](/specs/services/{service}/)

## Быстрый старт

\`\`\`bash
# Запуск для разработки
make dev

# Запуск тестов
make test
\`\`\`

## Зависимости

| Сервис | Обязательный | Назначение |
|--------|:------------:|------------|
| users | ✅ | Получение данных пользователя |
| notification | ❌ | Отправка email |

**Внешние:**
- Redis — хранение сессий

## Переменные окружения

См. [.env.example](.env.example)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `PORT` | Порт сервиса | `8080` |
| `DATABASE_URL` | URL базы данных | — |
| `JWT_SECRET` | Секрет для JWT | — |

## Команды

| Команда | Описание |
|---------|----------|
| `make dev` | Запуск для разработки |
| `make test` | Запуск тестов |
| `make build` | Сборка |
| `make migrate` | Применить миграции |

## API

- Swagger UI: `GET /docs`
- Health check: `GET /health`
- Readiness: `GET /ready`
```

---

## Makefile

Стандартные targets для Makefile сервиса:

```makefile
.PHONY: dev test build migrate lint

# Запуск для разработки
dev:
	@echo "Starting ${SERVICE} in dev mode..."
	# команда запуска

# Запуск тестов
test:
	@echo "Running tests..."
	# команда тестов

# Сборка
build:
	@echo "Building ${SERVICE}..."
	# команда сборки

# Применить миграции
migrate:
	@echo "Running migrations..."
	# команда миграций

# Линтинг
lint:
	@echo "Running linter..."
	# команда линтера
```

---

## Папки

### /backend/

Серверный код сервиса.

```
/backend/
├── /v1/                    # Версия API
│   ├── handlers.ts         # HTTP handlers
│   ├── routes.ts           # Маршруты
│   └── services.ts         # Бизнес-логика
├── /shared/                # Общий код между версиями
│   ├── models.ts           # Модели данных
│   └── utils.ts            # Утилиты
└── /health/                # Health endpoints
    └── handlers.ts
```

### /database/

Работа с базой данных.

```
/database/
├── schema.sql              # Текущая схема (для документации)
├── /migrations/            # Миграции
│   ├── 001_init.sql
│   ├── 002_add_users.sql
│   └── ...
└── /seeds/                 # Тестовые данные
    └── test_data.sql
```

### /frontend/ (опционально)

Клиентский код, если сервис включает UI.

```
/frontend/
├── /src/
│   ├── /components/
│   ├── /pages/
│   └── /utils/
├── package.json
└── ...
```

### /tests/

Unit и integration тесты сервиса.

```
/tests/
├── /unit/                  # Unit тесты
│   ├── handlers.test.ts
│   └── services.test.ts
├── /integration/           # Integration тесты
│   └── api.test.ts
└── /fixtures/              # Тестовые данные
    └── users.json
```

---

## Примеры

### Пример: Auth Service

```
/src/auth/
├── README.md
├── Makefile
├── dependencies.yaml
├── .env.example
├── /backend/
│   ├── /v1/
│   │   ├── handlers.ts     # login, logout, refresh
│   │   ├── routes.ts
│   │   └── services.ts     # JWT generation, validation
│   └── /health/
│       └── handlers.ts
├── /database/
│   ├── schema.sql
│   └── /migrations/
│       ├── 001_init.sql
│       └── 002_add_sessions.sql
└── /tests/
    ├── /unit/
    │   └── jwt.test.ts
    └── /integration/
        └── auth-flow.test.ts
```

### Пример: Notification Service (с frontend)

```
/src/notification/
├── README.md
├── Makefile
├── dependencies.yaml
├── .env.example
├── /backend/
│   └── /v1/
│       ├── handlers.ts     # send, templates
│       └── services.ts     # email, push, sms
├── /frontend/              # Админка для шаблонов
│   ├── /src/
│   └── package.json
└── /tests/
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/spec-create](/.claude/skills/spec-create/SKILL.md) | Создание сервиса через `--new` флаг |

---

## Связанные инструкции

- [lifecycle.md](./lifecycle.md) — создание и удаление сервиса
- [dependencies.md](./dependencies.md) — зависимости между сервисами
- [docs/structure.md](../docs/structure.md) — документация сервиса в /doc/
