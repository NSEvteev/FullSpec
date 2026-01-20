---
type: project
description: Окружения: development.yaml, staging.yaml, production.yaml
related:
  - config/feature-flags.md
  - platform/deployment.md
  - src/dev/local.md
---

# Конфигурации окружений

Описание структуры и правил работы с конфигурациями окружений в папке `/config/`.

## Оглавление

- [Структура](#структура)
- [Окружения](#окружения)
- [Формат файлов](#формат-файлов)
- [Правила](#правила)
- [Примеры](#примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## Структура

```
/config/
  /environments/
    development.yaml      ← локальная разработка
    staging.yaml          ← предпродакшн окружение
    production.yaml       ← продакшн окружение
  /features/              ← feature flags (опционально)
    features.yaml
```

---

## Окружения

| Окружение | Файл | Назначение |
|-----------|------|------------|
| Development | `development.yaml` | Локальная разработка, debug режим |
| Staging | `staging.yaml` | Тестирование перед продакшн |
| Production | `production.yaml` | Продакшн окружение |

### Когда какое использовать

| Сценарий | Окружение |
|----------|-----------|
| `make dev` | development |
| CI/CD тесты | staging |
| Релиз | production |

---

## Формат файлов

Формат: **YAML**

### Обязательные секции

| Секция | Описание |
|--------|----------|
| `database` | Подключение к БД |
| `redis` | Подключение к Redis (если используется) |
| `logging` | Уровень логирования |
| `services` | URL внешних сервисов |

### Структура файла

```yaml
# Описание окружения
environment: development  # development | staging | production

# База данных
database:
  host: localhost
  port: 5432
  name: app_dev
  pool_size: 5

# Кэширование
redis:
  host: localhost
  port: 6379

# Логирование
logging:
  level: debug  # debug | info | warning | error
  format: json

# Внешние сервисы
services:
  auth_url: http://localhost:8001
  notification_url: http://localhost:8002
```

---

## Правила

### 1. Секреты НЕ хранить в конфигах

**Запрещено** в YAML файлах:
- Пароли
- API ключи
- Токены
- Приватные ключи

**Где хранить секреты:**
- `.env` файлы (локально, в `.gitignore`)
- Переменные окружения в CI/CD
- Secrets manager (Vault, AWS Secrets Manager)

```yaml
# Плохо
database:
  password: secret123

# Хорошо — ссылка на переменную окружения
database:
  password: ${DATABASE_PASSWORD}
```

### 2. Различия между окружениями минимальны

Конфиги должны отличаться только:
- Хостами и портами
- Уровнем логирования
- Размерами пулов

**Не должны** отличаться:
- Структурой секций
- Именами ключей
- Форматом значений

### 3. Валидация конфигов

Каждый сервис при запуске **обязан**:
1. Загрузить конфиг соответствующего окружения
2. Проверить наличие обязательных секций
3. Fail-fast при отсутствии обязательных значений

### 4. Переопределение через ENV

Переменные окружения имеют **приоритет** над YAML:

```bash
# Переопределит значение из YAML
DATABASE_HOST=custom-host make dev
```

---

## Примеры

### development.yaml

```yaml
environment: development

database:
  host: localhost
  port: 5432
  name: app_dev
  pool_size: 5
  ssl: false

redis:
  host: localhost
  port: 6379

logging:
  level: debug
  format: json

services:
  auth_url: http://localhost:8001
  notification_url: http://localhost:8002

# Специфичное для разработки
debug:
  enabled: true
  profiling: true
```

### staging.yaml

```yaml
environment: staging

database:
  host: staging-db.internal
  port: 5432
  name: app_staging
  pool_size: 10
  ssl: true

redis:
  host: staging-redis.internal
  port: 6379

logging:
  level: info
  format: json

services:
  auth_url: https://auth.staging.example.com
  notification_url: https://notify.staging.example.com

debug:
  enabled: false
  profiling: false
```

### production.yaml

```yaml
environment: production

database:
  host: ${DATABASE_HOST}      # из secrets
  port: 5432
  name: app_production
  pool_size: 20
  ssl: true

redis:
  host: ${REDIS_HOST}         # из secrets
  port: 6379

logging:
  level: warning
  format: json

services:
  auth_url: https://auth.example.com
  notification_url: https://notify.example.com

debug:
  enabled: false
  profiling: false
```

---

## Связанные инструкции

- [feature-flags.md](./feature-flags.md) — флаги функций
- [platform/deployment.md](../platform/deployment.md) — стратегии деплоя
- [src/dev/local.md](../src/dev/local.md) — локальная разработка
