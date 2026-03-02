---
description: Стандарт Docker конфигураций для dev, test и production окружений проекта
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: platform/.instructions/README.md
---

# Стандарт Docker

Версия стандарта: 1.1

Стандарт Docker конфигураций для dev-среды, тестового окружения и production builds. Определяет формат Dockerfile, docker-compose конвенции, сети, volumes, порты, health checks и hot reload.

**Полезные ссылки:**
- [Инструкции](./README.md)
- [infrastructure.md](/specs/docs/.system/infrastructure.md) — SSOT сервисов и портов

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |

## Оглавление

- [1. Dockerfile формат](#1-dockerfile-формат)
- [2. Compose конвенции](#2-compose-конвенции)
- [3. Сети](#3-сети)
- [4. Volumes](#4-volumes)
- [5. Порты](#5-порты)
- [6. Health checks](#6-health-checks)
- [7. Environment](#7-environment)
- [8. Тестовое окружение](#8-тестовое-окружение)
- [9. Hot reload](#9-hot-reload)
- [10. Жизненный цикл Docker-файлов](#10-жизненный-цикл-docker-файлов)

---

## 1. Dockerfile формат

### Multi-stage builds

Каждый Dockerfile содержит минимум два target:

| Target | Назначение | Команда запуска |
|--------|-----------|----------------|
| `development` | Dev-среда и тесты с hot reload | `uvicorn --reload` / `nodemon` / `air` |
| `production` | Production-оптимизированный образ | `gunicorn` / `node` / бинарник |

Тестовое окружение использует target `development` (отдельный test stage не нужен).

```dockerfile
# === Base ===
FROM python:3.12-slim AS base
WORKDIR /app
RUN addgroup --system app && adduser --system --group app

# === Development ===
FROM base AS development
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

# === Production ===
FROM base AS production
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER app
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001"]
```

### Правила

- **Non-root user:** Всегда `USER app` (не root). Создать пользователя в base stage.
- **Layer caching:** Зависимости (`requirements.txt`, `package.json`, `go.mod`+`go.sum`) копировать **перед** кодом — layer cache не инвалидируется при изменении кода.
- **Alpine — только для инфраструктуры** (`postgres:16-alpine`, `redis:7-alpine`). Для сервисов приложения — `python:3.12-slim` / `node:20-slim` (Alpine вызывает проблемы с musl-libc). Использование Alpine в сервисах запрещено.
- **No build secrets:** Никаких секретов в `COPY` или `ENV` во время build.
- **HEALTHCHECK в Dockerfile — не используется.** Health checks определяются на уровне docker-compose (§ 6). В Kubernetes — через liveness/readiness probes (вне зоны этого документа).

### .dockerignore

Обязательные исключения (по языкам):

```
# Общие
.git/
.env
tests/

# Python
__pycache__/
*.pyc
.venv/
*.egg-info/
.pytest_cache/
.mypy_cache/

# Node.js
node_modules/
dist/
.next/

# Go
bin/
*.exe
```

---

## 2. Compose конвенции

### Формат файлов

| Файл | Назначение | Путь |
|------|-----------|------|
| `docker-compose.yml` | Dev-окружение (основной) | `platform/docker/docker-compose.yml` |
| `docker-compose.test.yml` | Тестовое окружение | `platform/docker/docker-compose.test.yml` |

Production-окружение не управляется через docker-compose. Compose используется только для локальной разработки (dev) и CI-тестирования (test). Production-развёртывание — через Kubernetes (вне зоны этого документа).

Не используем override-файлы (`docker-compose.override.yml`). Каждое окружение — отдельный файл.

### Именование

- Сервисы: kebab-case, совпадает с именем папки в `src/` (`auth`, `task`, `notification`, `admin`).
- Networks: kebab-case с суффиксом окружения (`app-network` → name: `myapp-dev`).
- Volumes: kebab-case (`pgdata`, `redis-data`).
- `container_name:` — не указывать (Docker генерирует автоматически). Явный `container_name` ломает параллельный запуск в CI.

### Target в Compose

В docker-compose указывать `target: development` — иначе Docker соберёт последний stage (production):

```yaml
build:
  context: ../../src/auth
  dockerfile: ../../platform/docker/Dockerfile.auth
  target: development
```

### Restart policy

| Окружение | Политика | Причина |
|-----------|---------|---------|
| Dev | `restart: unless-stopped` | Авто-перезапуск при падении |
| Test | `restart: "no"` | Тесты управляют жизненным циклом |

### Зависимости

Всегда `depends_on` с `condition: service_healthy`:

```yaml
depends_on:
  postgres:
    condition: service_healthy
  redis:
    condition: service_healthy
```

Не используем `depends_on` без condition — это гарантирует только порядок запуска, не готовность.

### Версия Compose

Docker Compose V2 (`docker compose`, не `docker-compose`). Поле `version:` в файле не указываем (устарело с Compose V2).

---

## 3. Сети

Одна bridge-сеть per environment с явным именем:

```yaml
networks:
  app-network:
    driver: bridge
    name: myapp-dev  # явное имя, не зависит от имени папки
```

| Окружение | Имя сети |
|-----------|---------|
| dev | `myapp-dev` |
| test | `myapp-test` |

Явное имя (`name:`) обязательно — без него Docker генерирует имя из имени папки, что ненадёжно.

---

## 4. Volumes

### Типы volumes

| Тип | Когда использовать | Пример |
|-----|-------------------|--------|
| Named volume | Персистентные данные (БД) | `pgdata:/var/lib/postgresql/data` |
| Bind mount | Код для hot reload | `../../src/auth:/app` |
| Anonymous volume | Защита зависимостей от bind mount | `/app/node_modules` |

### Named volumes (обязательные)

```yaml
volumes:
  pgdata:       # PostgreSQL data
  redis-data:   # Redis data
  rabbitmq-data: # RabbitMQ data
```

### Anonymous volume для зависимостей

При bind mount кода, зависимости внутри контейнера перезаписываются хостовой папкой. Anonymous volume предотвращает это:

**Node.js:**
```yaml
volumes:
  - ../../src/auth:/app          # bind mount кода
  - /app/node_modules            # anonymous — зависимости остаются из образа
```

**Python (если venv внутри `/app`):**
```yaml
volumes:
  - ../../src/auth:/app
  - /app/.venv                   # anonymous — сохраняет venv из образа
```

Если Python-зависимости установлены в системные пути образа (`/usr/local/lib`) — anonymous volume не нужен.

---

## 5. Порты

Порты фиксированы — SSOT: [infrastructure.md](/specs/docs/.system/infrastructure.md).

| Сервис | Порт | Протокол |
|--------|------|----------|
| gateway | 8000 | HTTP |
| auth | 8001 | HTTP |
| task | 8002 | HTTP |
| notification | 8003 | HTTP |
| admin | 8004 | HTTP |
| PostgreSQL | 5432 | TCP |
| Redis | 6379 | TCP |
| RabbitMQ | 5672 | AMQP |
| RabbitMQ Management | 15672 | HTTP |

Формат маппинга: `"{host_port}:{container_port}"` (в кавычках — YAML может интерпретировать как число).

---

## 6. Health checks

### Инфраструктура (обязательно)

| Сервис | Команда | Интервал | Retries |
|--------|---------|---------|---------|
| PostgreSQL | `pg_isready -U ${POSTGRES_USER}` | 5s | 5 |
| Redis | `redis-cli ping` | 5s | 5 |
| RabbitMQ | `rabbitmq-diagnostics -q ping` | 10s | 5 |

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-myapp}"]
  interval: 5s
  timeout: 5s
  retries: 5
  start_period: 10s
```

### Сервисы приложения (обязательно при наличии `/health`)

Если сервис реализует endpoint `GET /health` — health check в docker-compose обязателен. Порт подставлять из § 5 для каждого сервиса:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:{port}/health"]
  interval: 10s
  timeout: 5s
  retries: 3
```

---

## 7. Environment

### Файлы переменных окружения

| Файл | Коммитится | Назначение |
|------|-----------|-----------|
| `.env.example` | Да | Шаблон с описанием всех переменных. Dev-значения по умолчанию |
| `.env` | Нет (`.gitignore`) | Локальные значения. Копия `.env.example` с изменениями |
| `.env.test` | Да | Значения для тестов. Только публичные значения (localhost URLs, порты) |

### Правила

- `.env.example` содержит **рабочие dev-значения** — `cp .env.example .env` сразу работает.
- Секреты в `.env.example` — placeholder: `POSTGRES_PASSWORD=changeme`.
- Каждая переменная задокументирована комментарием.
- `.env.test` содержит только публичные тестовые значения. Если тест требует секрет — использовать mock/stub или CI/CD-переменные окружения.

### SSOT переменных

Переменные окружения определены в [infrastructure.md](/specs/docs/.system/infrastructure.md). Docker-конфигурации ссылаются на них, не дублируют.

---

## 8. Тестовое окружение

`docker-compose.test.yml` — изолированное окружение для integration/e2e тестов.

### Отличия от dev

| Параметр | Dev | Test |
|----------|-----|------|
| Сеть | `myapp-dev` | `myapp-test` |
| PostgreSQL storage | Named volume (`pgdata`) | `tmpfs` (RAM-диск) |
| Redis storage | Named volume (`redis-data`) | Без persistence |
| Bind mounts | Да (hot reload) | Нет |
| Сервисы приложения | Да (stub) | Нет (запускаются тест-раннером) |

### tmpfs для тестовой БД

```yaml
postgres-test:
  image: postgres:16-alpine
  tmpfs:
    - /var/lib/postgresql/data
```

RAM-диск — мгновенная очистка между тестами, быстрая запись.

### Testcontainers (рекомендация для per-service тестов)

Для integration-тестов внутри `src/{svc}/tests/` рекомендуется [Testcontainers](https://testcontainers.com/) вместо общего docker-compose.test.yml — каждый тест поднимает свои контейнеры, полная изоляция.

---

## 9. Hot reload

### Bind mount + reload flag

Код монтируется через bind mount, сервис запускается с флагом авто-перезагрузки:

| Технология | Флаг | Команда |
|-----------|------|---------|
| Python (uvicorn) | `--reload` | `uvicorn main:app --reload` |
| Node.js (nodemon) | — | `nodemon index.js` |
| Go (air) | — | `air` |

### Windows + WSL2

Bind mounts из Windows-файловой системы в WSL2 контейнеры работают медленно и не поддерживают `inotify` (hot reload не срабатывает).

**Решение:** Хранить код в файловой системе WSL2 (`/home/user/projects/`), не в `/mnt/c/`. Это обеспечивает нативную скорость и inotify.

### Anonymous volume для зависимостей

При bind mount кода зависимости из образа перезаписываются. Механизм и примеры — см. [§ 4 Volumes](#4-volumes) → Anonymous volume для зависимостей.

---

## 10. Жизненный цикл Docker-файлов

Docker-файлы создаются и обновляются на разных фазах процесса:

| Фаза | Что происходит | Кто выполняет |
|------|---------------|---------------|
| Фаза 2 (/docs-sync) | **Scaffolding** — создаются заглушки для новых сервисов | Оркестратор /docs-sync |
| Фаза 4 (Реализация) | **Реализация** — заглушки дополняются реальным кодом, healthcheck раскомментируется | dev-agent |
| Фаза 5 (/test) | **Валидация** — `docker compose up --wait` проверяет health checks | Оркестратор /test |

### Scaffolding (Фаза 2)

При `/docs-sync` для каждого **нового** сервиса (mode=create) создаётся:

| Артефакт | Файл | Содержание |
|----------|------|------------|
| Dockerfile | `platform/docker/Dockerfile.{svc}` | Multi-stage шаблон по технологии (§ 1) |
| Compose блок | `platform/docker/docker-compose.yml` | Блок сервиса с закомментированным healthcheck |
| База данных | `platform/docker/init-db.sql` | `CREATE DATABASE myapp_{svc}` (если PostgreSQL) |
| Env переменные | `.env.example`, `.env.test` | Per-service переменные (DB, Redis, URL) |
| Dockerignore | `src/{svc}/.dockerignore` | Исключения по технологии |

> **SSOT:** [create-docs-sync.md](/specs/.instructions/create-docs-sync.md) Step 2 п. 4.

### Реализация (Фаза 4)

dev-agent при работе над сервисом:
- Дополняет `Dockerfile.{svc}` реальными зависимостями и командами (scaffolding уже создан — не создавать заново)
- Раскомментирует healthcheck в `docker-compose.yml` после реализации `GET /health`
- Обновляет `.env.example` / `.env.test` при добавлении новых переменных

### Откат

При откате цепочки (Path C.1) Docker scaffolding удаляется: `Dockerfile.{svc}`, блок из `docker-compose.yml`, запись из `init-db.sql`, переменные из `.env`, `.dockerignore` из `src/{svc}/`.
