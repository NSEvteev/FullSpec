# Docker dev-среда — план и обучение

Настройка Docker-окружения для локальной разработки и тестирования. Включает план обучения пользователя (первый опыт с Docker).

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** Создать Docker-окружение для разработки и тестирования, написать стандарт для platform/docker/
**Почему создан:** `platform/docker/` пуст, `make dev` ссылается на docker-compose, но конфигурации нет. Пользователь не использовал Docker ранее — нужно обучение
**Связанные файлы:**
- `platform/docker/` — пусто (.gitkeep + README)
- `platform/.instructions/` — нет стандартов
- `Makefile` — `make dev`, `make stop`, `make clean` ссылаются на docker-compose
- `.structure/README.md` — описание platform/docker/
- `.claude/drafts/2026-02-24-tests-and-platform.md` — аудит тестов (связанная тема)

## Содержание

### Часть A: Что нужно создать

| # | Артефакт | Путь | Назначение |
|---|---------|------|-----------|
| 1 | **docker-compose.yml** | `platform/docker/docker-compose.yml` | Основная dev-конфигурация (БД, Redis, сервисы) |
| 2 | **docker-compose.test.yml** | `platform/docker/docker-compose.test.yml` | Тестовая конфигурация (изолированные зависимости) |
| 3 | **Dockerfile.{service}** | `platform/docker/Dockerfile.{service}` | Образ каждого сервиса |
| 4 | **.env.example** | `platform/docker/.env.example` | Переменные окружения (без секретов) |
| 5 | **standard-docker.md** | `platform/.instructions/standard-docker.md` | Стандарт Docker конфигураций |

### Часть B: Обучение пользователя

Пользователь не работал с Docker ранее. Нужно:

1. **Что такое Docker** — контейнер vs виртуальная машина, образ vs контейнер, docker-compose
2. **Установка** — Docker Desktop для Windows, WSL2 (если не настроен)
3. **Основные команды** — `docker compose up`, `docker compose down`, `docker compose logs`
4. **Как это работает в проекте** — `make dev` → поднимает все сервисы, `make stop` → останавливает
5. **Troubleshooting** — порты заняты, не хватает памяти, пересборка образа

Где размещать обучение:
- Короткий раздел в `platform/docker/README.md` (quick start)
- Ссылка на Docker Desktop docs для установки
- Примеры команд в контексте проекта

### Часть C: Стандарт Docker

`platform/.instructions/standard-docker.md` должен покрывать:

| Секция | Содержание |
|--------|-----------|
| Именование | Сервисы: kebab-case, образы: `{project}-{service}` |
| Compose структура | Profiles (dev/test/prod), depends_on, healthcheck |
| Сети | Одна сеть per environment, именование |
| Volumes | Named volumes для данных, bind mounts для кода |
| Переменные | .env файлы, секреты через Docker secrets или .env.local |
| Тестовое окружение | docker-compose.test.yml — изолированные БД, ephemeral данные |
| Multi-stage builds | Уменьшение размера образа, отделение dev/prod |

### Часть D: Интеграция в standard-process.md

- **Фаза 0 (шаг 0.3):** Установка Docker Desktop, `make setup` включает проверку Docker
- **Фаза 3 (шаг 3.1):** `make dev` поднимает зависимости перед разработкой
- **Фаза 3 (шаг 3.2):** `make test` может использовать docker-compose.test.yml для интеграционных тестов
- **§8:** Добавить `standard-docker.md` в строку Фаза 0

## Решения

- Docker необходим для проекта — микросервисная архитектура без него не работает локально
- Нужен и dev-compose и test-compose
- Обучение пользователя — обязательная часть (README + примеры)
- `standard-docker.md` — первый стандарт для platform/

## Открытые вопросы

- WSL2: нужен ли для Windows, или Docker Desktop справляется без него?
- Hot reload: bind mount + file watcher или пересборка?
- Порты: фиксированные (5432 для PG) или динамические?
- Нужен ли Makefile target `make docker-build` отдельно от `make dev`?
- Тестовая БД: отдельный контейнер с ephemeral данными или schema-only?

---

## Что уже описано в проекте

### Makefile (`/Makefile`)

Уже содержит Docker-зависимые команды, но без реальных конфигурационных файлов:

- `make dev` — `docker-compose -f docker-compose.dev.yml up` (файл `docker-compose.dev.yml` не существует)
- `make stop` — `docker-compose down`
- `make build` — `docker-compose build`
- `make clean` — `docker-compose down -v --remove-orphans`

**Проблема:** Makefile ссылается на `docker-compose.dev.yml` в корне, но драфт планирует `platform/docker/docker-compose.yml`. Нужно согласовать путь: либо обновить Makefile на `docker-compose -f platform/docker/docker-compose.yml up`, либо разместить compose-файл в корне.

### infrastructure.md (`/specs/docs/.system/infrastructure.md`)

Визуализация (пример MyApp) уже описывает полную Docker-инфраструктуру:

- **Сервисы и порты:** 5 сервисов (auth:8001, task:8002, notification:8003, admin:8004, gateway:8000) с Docker-хостами по имени контейнера
- **Хранилища:** PostgreSQL (postgres:5432), Redis (redis:6379) — все как Docker containers в dev
- **Message Broker:** RabbitMQ (rabbitmq:5672, Management UI на 15672)
- **Service Discovery:** env-переменные с URL (`AUTH_SERVICE_URL=http://auth:8001` и т.д.)
- **Окружения:** dev = Docker containers, staging = AWS managed, prod = AWS HA
- **Мониторинг:** dev = `docker-compose logs -f {svc}`
- **Секреты:** dev = `.env` файл, prod = AWS Secrets Manager

**Значение для docker-compose.yml:** infrastructure.md фактически является спецификацией для docker-compose — оттуда берутся имена контейнеров, порты, env-переменные, healthcheck-эндпоинты.

### standard-infrastructure.md (`/specs/.instructions/docs/infrastructure/standard-infrastructure.md`)

Стандарт формата infrastructure.md содержит принцип:

> **SSOT конфигурации.** `.env.example` и `docker-compose.yml` — источник правды значений. `infrastructure.md` синхронизируется с ними, не является источником конфигурации.

Это значит: после создания `docker-compose.yml` и `.env.example` — infrastructure.md должен ссылаться на них, а не наоборот.

### testing.md (`/specs/docs/.system/testing.md`)

Уже описывает Docker для тестирования:

- **Integration-тесты:** "поднимает реальные хранилища (PostgreSQL, Redis в Docker), но мокает другие сервисы"
- **E2E-тесты:** "Всё реальное (docker-compose)" — `docker-compose -f docker-compose.test.yml up`
- **Межсервисные тесты:** "запускает все сервисы + хранилища в изолированной сети"
- **conftest.py (e2e):** комментарий `# docker-compose up, HTTP-клиенты, WS-клиент`

**Значение для docker-compose.test.yml:** testing.md подтверждает необходимость отдельного compose-файла для тестов с изолированной сетью.

### standard-development.md (`/.github/.instructions/development/standard-development.md`)

Цикл разработки уже предполагает Docker:

- Шаг 1: `make dev` — запуск окружения
- `make clean` — "Полная очистка (docker down -v). Использовать, если: сервисы не запускаются после `make dev`, зависшие контейнеры после `make stop`, ошибки port already in use или volume not found"
- Troubleshooting: `connection refused / timeout` → "Сервисы не запущены" → `make dev`

### standard-docs.md (`/specs/.instructions/docs/standard-docs.md`)

Секция "Платформа и окружения" (тип документа `infrastructure.md`) описывает 8 секций:
1. Локальная разработка — docker-compose, make-команды
2. Сервисы и порты — таблица с Docker-хостами
3. Хранилища данных
4. Брокер сообщений
5. Service Discovery
6. Окружения
7. Мониторинг
8. Секреты

### tests-and-platform.md (`/.claude/drafts/2026-02-24-tests-and-platform.md`)

Связанный драфт подтверждает:

- `standard-docker.md` — приоритет "Высокий — нужен при первом сервисе"
- Docker для тестов: `docker-compose.test.yml` — пересечение platform/ и tests/
- `platform/.instructions/` пуст — ни одного стандарта
- Все подпапки platform/ содержат только `.gitkeep`

### Dependabot (`/.github/dependabot.yml`)

Уже настроен мониторинг Docker-зависимостей:

```yaml
- package-ecosystem: "docker"
  directory: "/platform/docker/"
  schedule:
    interval: "weekly"
```

Dependabot ожидает Dockerfile в `/platform/docker/` — это подтверждает, что Docker-файлы должны быть именно там.

### standard-release.md (`/.github/.instructions/releases/standard-release.md`)

Релизный процесс предполагает Docker:

- Release workflow: "Build Docker образов" → "Push образов в Registry"
- Деплой: `docker pull {image}:{version} && docker restart`
- Rollback: `docker pull {image}:{prev_version} && docker restart`
- Release assets включают "Docker images (ссылка в body, сам образ в Docker Registry)"

### CODEOWNERS (`/.github/.instructions/codeowners/standard-codeowners.md`)

Стандарт предусматривает:

- `/platform/docker/ @devops` — отдельный owner для Docker-файлов
- `/Dockerfile @devops` — owner для корневого Dockerfile (если будет)

### .gitignore

Уже содержит правила для .env-файлов:

```
.env
.env.local
.env.*.local
```

Нет правил для Docker-артефактов (volumes, build cache). Возможно, стоит добавить.

### initialization.md (`/.structure/initialization.md`)

Текущая инициализация (`make setup`) НЕ включает Docker:
- Только Python, pre-commit, GitHub CLI
- Нет проверки `docker --version` или `docker compose version`
- Нет шага "запустить Docker Desktop"

**Необходимо:** добавить Docker Desktop в таблицу зависимостей и проверку в `make setup`.

### platform/.instructions/README.md

Индекс инструкций для platform/ — полностью пустой:
- Нет стандартов
- Нет воркфлоу
- Нет валидаций
- Нет скриптов
- Нет скиллов

`standard-docker.md` станет первым документом в этом индексе.

### config/README.md

Конфигурации окружений:

- `config/development.yaml`, `staging.yaml`, `production.yaml` (файлы описаны, но не созданы)
- `config/feature-flags/flags.yaml`
- Граница: `.env файлы сервиса → /src/{service}/`
- Секреты: `vault / env vars`

**Связь с Docker:** config/ содержит YAML-конфигурации окружений, Docker использует `.env` файлы. Нужно определить, как они связаны (config/*.yaml генерирует .env? или это разные механизмы?).

---

## Best practices

### 1. Docker Compose для микросервисной разработки

**Один compose-файл для dev, отдельный для тестов:**

```yaml
# docker-compose.yml (dev)
services:
  auth:
    build:
      context: ../../src/auth
      dockerfile: ../../platform/docker/Dockerfile.auth
    ports:
      - "8001:8001"
    environment:
      - POSTGRES_HOST=postgres
      - AUTH_SERVICE_URL=http://auth:8001
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ../../src/auth:/app  # bind mount для hot reload
    networks:
      - dev-network

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: myapp
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U myapp"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - dev-network

volumes:
  pgdata:

networks:
  dev-network:
    driver: bridge
```

**Рекомендация для проекта:** Согласно infrastructure.md, нужны сервисы (auth, task, notification, admin, gateway), хранилища (PostgreSQL, Redis), брокер (RabbitMQ). Compose-файл должен описывать все 8 контейнеров с правильными depends_on и healthcheck.

### 2. Docker Desktop на Windows + WSL2

**Ответ на открытый вопрос:** WSL2 backend ОБЯЗАТЕЛЕН для Docker Desktop на Windows 10/11. Без WSL2 Docker Desktop использует Hyper-V backend, который значительно медленнее и хуже поддерживает bind mounts.

Шаги установки:

1. Включить WSL2: `wsl --install` (PowerShell от администратора)
2. Установить Docker Desktop: https://docs.docker.com/desktop/install/windows-install/
3. В Docker Desktop Settings: General → "Use the WSL 2 based engine" (включено по умолчанию)
4. Resources → WSL Integration → включить для нужных дистрибутивов
5. Проверка: `docker run hello-world`

**Для проекта:** Добавить в `initialization.md` секцию "Docker Desktop" с этими шагами. Добавить проверку `docker compose version` в `make setup`.

### 3. Hot reload с bind mounts

**Ответ на открытый вопрос:** Bind mount + file watcher — правильный подход. Пересборка образа при каждом изменении слишком медленная.

```yaml
services:
  auth:
    volumes:
      - ../../src/auth:/app          # исходный код
      - /app/node_modules            # исключить node_modules из bind mount
      - /app/.venv                   # исключить virtualenv из bind mount
    command: ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]
```

**Ключевые принципы:**
- Bind mount для исходного кода (`/src/{service}` → `/app`)
- Anonymous volume для зависимостей (`/app/node_modules`, `/app/.venv`) — предотвращает перезапись контейнерных зависимостей хостовыми
- Команда запуска с `--reload` (uvicorn, nodemon, air для Go)
- На Windows+WSL2: файлы должны быть в файловой системе WSL для нормальной производительности inotify; если файлы на NTFS — polling fallback (медленнее)

### 4. Multi-stage Dockerfile builds

```dockerfile
# === Stage 1: Builder ===
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .

# === Stage 2: Development ===
FROM python:3.12-slim AS development

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

# Hot reload для dev
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# === Stage 3: Production ===
FROM python:3.12-slim AS production

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

# Без reload, с gunicorn
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

**Для проекта:** Каждый сервис (`Dockerfile.auth`, `Dockerfile.task` и т.д.) должен иметь multi-stage build с targets `development` и `production`. В compose dev-файле: `target: development`. В CI/release: `target: production`.

```yaml
# docker-compose.yml
services:
  auth:
    build:
      context: ../../src/auth
      dockerfile: ../../platform/docker/Dockerfile.auth
      target: development  # <-- dev target с hot reload
```

### 5. Docker networking для микросервисов

```yaml
networks:
  app-network:
    driver: bridge
    name: myapp-dev  # явное имя, чтобы не зависеть от имени папки

services:
  auth:
    networks:
      - app-network
  postgres:
    networks:
      - app-network
```

**Принципы:**
- Одна bridge-сеть для dev-окружения — все сервисы видят друг друга по имени контейнера
- Для тестов — отдельная сеть (`myapp-test`), чтобы не конфликтовать с dev
- Не использовать `network_mode: host` — ломает кроссплатформенность
- Service discovery через DNS (Docker внутренний): `http://auth:8001`, `postgres:5432`
- Это совпадает с тем, что уже описано в infrastructure.md (Service Discovery через env vars с Docker-хостами)

### 6. Health checks в docker-compose

```yaml
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U myapp"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s

  redis:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  rabbitmq:
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "check_running"]
      interval: 10s
      timeout: 10s
      retries: 5
      start_period: 30s

  auth:
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 10s
      timeout: 5s
      retries: 3
```

**Для проекта:** infrastructure.md указывает `GET /health` для каждого сервиса. Порядок запуска: "PostgreSQL и Redis стартуют первыми (healthcheck), затем сервисы. RabbitMQ стартует параллельно — сервисы с retry до подключения." Это нужно отразить в `depends_on` + `condition: service_healthy`.

### 7. .env файлы и secrets management

**Структура .env файлов для проекта:**

```
platform/docker/.env.example    # Шаблон с описанием переменных (коммитится)
platform/docker/.env            # Локальные значения (НЕ коммитится, в .gitignore)
platform/docker/.env.test       # Значения для тестов (коммитится, без секретов)
```

**Формат .env.example:**

```bash
# === PostgreSQL ===
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=myapp
POSTGRES_PASSWORD=changeme           # <-- заменить на свой пароль
AUTH_DB_NAME=myapp_auth
TASK_DB_NAME=myapp_task
NOTIFICATION_DB_NAME=myapp_notification
ADMIN_DB_NAME=myapp_admin

# === Redis ===
REDIS_HOST=redis
REDIS_PORT=6379
NOTIFICATION_REDIS_DB=0
AUTH_REDIS_DB=1

# === RabbitMQ ===
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672

# === Service URLs ===
AUTH_SERVICE_URL=http://auth:8001
TASK_SERVICE_URL=http://task:8002
NOTIFICATION_SERVICE_URL=http://notification:8003
ADMIN_SERVICE_URL=http://admin:8004

# === JWT ===
JWT_SECRET_KEY=dev-secret-key-change-in-prod  # <-- заменить для prod
```

**Ответ на открытый вопрос (порты):** Фиксированные порты — правильный подход для dev. Infrastructure.md уже фиксирует: PostgreSQL=5432, Redis=6379, RabbitMQ=5672/15672, сервисы=8001-8004, gateway=8000. Динамические порты усложняют конфигурацию service discovery.

### 8. Docker для тестирования

**Два подхода:**

**A. docker-compose.test.yml (E2E и inter-service integration):**

```yaml
# docker-compose.test.yml
services:
  postgres-test:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    tmpfs:
      - /var/lib/postgresql/data  # RAM-диск — быстро и ephemeral
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test"]
      interval: 2s
      timeout: 2s
      retries: 10

  redis-test:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 2s
      timeout: 2s
      retries: 10

networks:
  test-network:
    driver: bridge
    name: myapp-test
```

Ключевое: `tmpfs` для тестовой БД — данные в RAM, мгновенная очистка при остановке, быстрая запись.

**B. Testcontainers (per-service integration tests):**

```python
# src/auth/tests/conftest.py
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg.get_connection_url()
```

Testcontainers запускает контейнер программно из теста — не нужен отдельный compose-файл для integration-тестов внутри сервиса. Подходит для `src/{service}/tests/`.

**Ответ на открытый вопрос (тестовая БД):** Оба подхода нужны. `docker-compose.test.yml` — для E2E (`tests/e2e/`), testcontainers — для per-service integration (`src/{service}/tests/`). Ephemeral данные через `tmpfs` — оптимально для обоих.

### 9. Volume management (named vs bind)

| Тип | Когда использовать | Пример |
|-----|--------------------|--------|
| **Named volume** | Персистентные данные (БД, файловое хранилище) | `pgdata:/var/lib/postgresql/data` |
| **Bind mount** | Исходный код для hot reload | `../../src/auth:/app` |
| **Anonymous volume** | Защита контейнерных зависимостей от перезаписи | `/app/node_modules` |
| **tmpfs** | Ephemeral тестовые данные | `tmpfs: /var/lib/postgresql/data` |

**Для проекта:**
- Named volumes: `pgdata` (PostgreSQL), `redis-data` (Redis, если нужна персистентность), `rabbitmq-data` (RabbitMQ)
- Bind mounts: `../../src/{service}:/app` — для каждого сервиса
- `make clean` = `docker-compose down -v` — удаляет named volumes (уже реализовано в Makefile)

### 10. Docker layer caching optimization

**Порядок инструкций в Dockerfile критичен:**

```dockerfile
# ПРАВИЛЬНО: зависимости отдельно от кода
FROM python:3.12-slim

WORKDIR /app

# 1. Сначала файл зависимостей (меняется редко)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Потом исходный код (меняется часто)
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

```dockerfile
# НЕПРАВИЛЬНО: каждое изменение кода инвалидирует кэш зависимостей
FROM python:3.12-slim
WORKDIR /app
COPY . .                    # <-- изменение любого файла
RUN pip install -r requirements.txt  # <-- пересобирается каждый раз
```

**Дополнительные оптимизации:**
- `.dockerignore` — исключить `.git/`, `__pycache__/`, `node_modules/`, `.venv/`, `*.pyc`, тесты (если не нужны в образе)
- `--no-cache-dir` для pip — не хранить кэш внутри образа
- Alpine-образы (`python:3.12-slim` или `python:3.12-alpine`) — меньший размер
- BuildKit: `DOCKER_BUILDKIT=1` — параллельная сборка стейджей, кэширование mount

### 11. Согласование Makefile и docker-compose

**Текущая проблема:** Makefile использует `docker-compose -f docker-compose.dev.yml up`, но файл не существует и планируется в `platform/docker/`.

**Рекомендация:** Обновить Makefile для указания правильного пути:

```makefile
COMPOSE_FILE = platform/docker/docker-compose.yml
COMPOSE_TEST_FILE = platform/docker/docker-compose.test.yml

dev:
	docker compose -f $(COMPOSE_FILE) up

stop:
	docker compose -f $(COMPOSE_FILE) down

build:
	docker compose -f $(COMPOSE_FILE) build

clean:
	docker compose -f $(COMPOSE_FILE) down -v --remove-orphans

test-integration:
	docker compose -f $(COMPOSE_TEST_FILE) up -d
	pytest tests/integration/
	docker compose -f $(COMPOSE_TEST_FILE) down -v

test-e2e:
	docker compose -f $(COMPOSE_TEST_FILE) up -d
	pytest tests/e2e/
	docker compose -f $(COMPOSE_TEST_FILE) down -v
```

**Примечание:** Современный Docker использует `docker compose` (с пробелом), а не `docker-compose` (с дефисом). `docker-compose` — устаревшая отдельная утилита (Compose V1). `docker compose` — встроенная в Docker CLI (Compose V2). Рекомендуется обновить Makefile на `docker compose`.

### 12. Добавление Docker в initialization.md

Текущая инициализация не включает Docker. Нужно добавить:

**В таблицу зависимостей:**

| Инструмент | Назначение | Установка |
|------------|------------|-----------|
| **Docker Desktop** | Контейнеризация сервисов | [docker.com/desktop](https://docs.docker.com/desktop/install/windows-install/) |

**В `make setup`:**

```makefile
setup:
	@echo "4/4 Docker..."
	@docker --version 2>/dev/null || (echo "Docker не найден. Установите Docker Desktop" && exit 1)
	@docker compose version 2>/dev/null || (echo "Docker Compose не найден" && exit 1)
```

### 13. Структура файлов в platform/docker/

Рекомендуемая итоговая структура:

```
platform/docker/
├── docker-compose.yml          # Dev-конфигурация (основная)
├── docker-compose.test.yml     # Тестовая конфигурация
├── Dockerfile.auth             # Образ auth-сервиса
├── Dockerfile.task             # Образ task-сервиса
├── Dockerfile.notification     # Образ notification-сервиса
├── Dockerfile.admin            # Образ admin-сервиса
├── Dockerfile.gateway          # Образ gateway
├── .env.example                # Шаблон переменных окружения
├── .env.test                   # Переменные для тестов (без секретов)
├── .dockerignore               # Исключения для Docker build
├── init-db.sql                 # Скрипт инициализации БД (создание баз)
└── README.md                   # Quick start + обучение Docker
```

### 14. Ответы на открытые вопросы (сводка)

| Вопрос | Ответ | Обоснование |
|--------|-------|-------------|
| WSL2 нужен? | Да, обязателен | WSL2 backend значительно быстрее Hyper-V, лучше поддержка bind mounts |
| Hot reload | Bind mount + `--reload` | Пересборка образа при каждом изменении слишком медленная |
| Порты | Фиксированные | infrastructure.md уже фиксирует порты, динамические усложняют service discovery |
| `make docker-build` | Не нужен отдельно | `make build` = `docker compose build` уже достаточно |
| Тестовая БД | tmpfs + testcontainers | tmpfs для compose-test, testcontainers для per-service integration |
