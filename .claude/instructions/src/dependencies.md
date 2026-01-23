---
type: standard
description: Управление зависимостями между сервисами через dependencies.yaml
governed-by: services/README.md
related:
  - services/lifecycle.md
  - services/structure.md
  - shared/contracts.md
---

# Зависимости сервисов

Управление зависимостями между сервисами через файл `dependencies.yaml`.

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [services/README.md](./README.md)

## Оглавление

- [Формат dependencies.yaml](#формат-dependenciesyaml)
- [Типы зависимостей](#типы-зависимостей)
- [Обязательность](#обязательность)
- [Визуализация графа](#визуализация-графа)
- [Валидация](#валидация)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Формат dependencies.yaml

Каждый сервис содержит файл `dependencies.yaml` в корне:

```yaml
# /src/{service}/dependencies.yaml

# Метаинформация о сервисе
service:
  name: auth
  version: 1.0.0
  owner: auth-team

# Зависимости от других сервисов
dependencies:
  services:
    - name: users
      required: true
      version: ">=1.0.0"
      description: Получение данных пользователя
      endpoints:
        - GET /api/v1/users/{id}
        - GET /api/v1/users/by-email

    - name: notification
      required: false
      version: ">=1.0.0"
      description: Отправка email при регистрации
      endpoints:
        - POST /api/v1/notifications/email

  # Внешние зависимости (БД, кэш, очереди)
  external:
    - name: redis
      type: cache
      required: true
      description: Хранение сессий и rate limiting

    - name: postgres
      type: database
      required: true
      description: Хранение данных аутентификации

    - name: rabbitmq
      type: queue
      required: false
      description: Асинхронные события
```

---

## Типы зависимостей

### Сервисные зависимости (services)

Зависимости от других микросервисов проекта.

| Поле | Тип | Обязательно | Описание |
|------|-----|:-----------:|----------|
| `name` | string | ✅ | Имя сервиса |
| `required` | boolean | ✅ | Обязательность |
| `version` | string | ❌ | Версия API (semver) |
| `description` | string | ✅ | Зачем нужен |
| `endpoints` | list | ❌ | Используемые endpoints |

### Внешние зависимости (external)

Зависимости от внешних систем.

| Поле | Тип | Обязательно | Описание |
|------|-----|:-----------:|----------|
| `name` | string | ✅ | Имя системы |
| `type` | string | ✅ | Тип: database, cache, queue, storage |
| `required` | boolean | ✅ | Обязательность |
| `description` | string | ✅ | Зачем нужен |

### Типы внешних зависимостей

| Тип | Примеры |
|-----|---------|
| `database` | PostgreSQL, MongoDB, MySQL |
| `cache` | Redis, Memcached |
| `queue` | RabbitMQ, Kafka, SQS |
| `storage` | S3, MinIO, GCS |
| `search` | Elasticsearch, Algolia |

---

## Обязательность

### required: true

- Сервис **не может работать** без этой зависимости
- При старте проверяется доступность
- Падение зависимости = падение сервиса

### required: false

- Сервис **может работать** без этой зависимости
- Функциональность деградирует gracefully
- Используется для опциональных фич

### Пример

```yaml
dependencies:
  services:
    # Без users сервис auth не работает
    - name: users
      required: true
      description: Получение данных пользователя

    # Без notification работает, но без email-уведомлений
    - name: notification
      required: false
      description: Отправка email при регистрации
```

---

## Визуализация графа

### Построение графа зависимостей

```bash
# TODO: Скрипт для визуализации
python /.claude/scripts/deps-graph.py --output graph.png
```

### Пример графа

```
┌─────────┐     ┌─────────┐     ┌──────────────┐
│  auth   │────▶│  users  │────▶│   postgres   │
└─────────┘     └─────────┘     └──────────────┘
     │
     ▼
┌─────────┐
│  redis  │
└─────────┘
     │
     ▼ (optional)
┌──────────────┐
│ notification │
└──────────────┘
```

---

## Валидация

### Проверки при старте сервиса

1. **Обязательные зависимости доступны**
2. **Версии совместимы** (если указаны)
3. **Нет циклических зависимостей**

### Проверки при CI/CD

```yaml
# .github/workflows/validate-deps.yml
- name: Validate dependencies
  run: python /.claude/scripts/validate-deps.py
```

### Циклические зависимости

**ЗАПРЕЩЕНО:** A → B → C → A

Если обнаружена циклическая зависимость:
1. Пересмотреть архитектуру
2. Вынести общий код в shared библиотеку
3. Использовать события вместо прямых вызовов

---

## Примеры

### Пример 1: Auth Service

```yaml
# /src/auth/dependencies.yaml
service:
  name: auth
  version: 1.0.0

dependencies:
  services:
    - name: users
      required: true
      version: ">=1.0.0"
      description: Получение данных пользователя для аутентификации
      endpoints:
        - GET /api/v1/users/{id}
        - GET /api/v1/users/by-email

  external:
    - name: redis
      type: cache
      required: true
      description: Хранение сессий и токенов

    - name: postgres
      type: database
      required: true
      description: Хранение refresh токенов
```

### Пример 2: Notification Service

```yaml
# /src/notification/dependencies.yaml
service:
  name: notification
  version: 1.0.0

dependencies:
  services: []  # Нет зависимостей от других сервисов

  external:
    - name: postgres
      type: database
      required: true
      description: Хранение шаблонов и истории отправок

    - name: rabbitmq
      type: queue
      required: true
      description: Очередь отправки сообщений

    - name: smtp
      type: external
      required: true
      description: SMTP сервер для email
```

### Пример 3: Gateway Service

```yaml
# /src/gateway/dependencies.yaml
service:
  name: gateway
  version: 1.0.0

dependencies:
  services:
    - name: auth
      required: true
      description: Валидация токенов
      endpoints:
        - POST /api/v1/auth/validate

    - name: users
      required: true
      description: Получение информации о пользователе
      endpoints:
        - GET /api/v1/users/{id}

    - name: notification
      required: false
      description: Отправка уведомлений
      endpoints:
        - POST /api/v1/notifications

  external:
    - name: redis
      type: cache
      required: true
      description: Rate limiting и кэширование
```

---

## Скиллы

**Скиллы для этой области пока отсутствуют.**

> **TODO:** Создать скиллы:
> - `/deps-validate` — валидация зависимостей
> - `/deps-graph` — визуализация графа

---

## Связанные инструкции

- [lifecycle.md](./lifecycle.md) — создание и удаление сервиса
- [structure.md](./structure.md) — структура папок сервиса
- [shared/contracts.md](../shared/contracts.md) — контракты между сервисами
- [shared/events.md](../shared/events.md) — события между сервисами
