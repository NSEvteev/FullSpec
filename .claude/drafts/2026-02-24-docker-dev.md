---
description: Docker dev-среда — standard-docker.md + docker-compose конфиги + обновление Makefile и initialization.md
type: feature
status: ready
created: 2026-02-24
---

# Docker dev-среда — стандарт + инфраструктура

Стандарт Docker конфигураций для platform/, docker-compose для dev и тестов, обучение пользователя.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** `platform/docker/` пуст, `make dev` ссылается на docker-compose, но конфигурации нет. Пользователь не использовал Docker — нужно обучение.
**Почему создан:** Микросервисная архитектура требует Docker для локальной разработки и тестирования. Без docker-compose невозможно запустить ни один `make` таргет (dev, test, build, clean).
**Связанные файлы:**
- `platform/docker/` — пусто (.gitkeep + README)
- `platform/.instructions/` — пусто (нет стандартов)
- `Makefile` — `make dev/stop/build/clean` ссылаются на docker-compose (файл не существует)
- `specs/docs/.system/infrastructure.md` — спецификация сервисов, портов, зависимостей
- `specs/docs/.system/testing.md` — упоминает docker-compose.test.yml
- `.structure/initialization.md` — Docker Desktop не в списке зависимостей
- `.github/dependabot.yml` — уже мониторит `/platform/docker/` для Docker-зависимостей

**Из tests-and-platform (Часть B):** Стандарты platform/ перенесены сюда. `standard-docker.md` — первый и единственный высокоприоритетный стандарт platform/. Остальные (k8s, monitoring, gateway, runbooks, scripts) — отложены до реального использования.

## Содержание

### Артефакт 1: Стандарт `standard-docker.md`

**Путь:** `platform/.instructions/standard-docker.md`
**Действие:** Создать через `/instruction-create`.

Стандарт Docker конфигураций для проекта. Секции:

| # | Секция | Содержание |
|---|--------|-----------|
| 1 | Dockerfile формат | Multi-stage builds (dev/prod targets), non-root user, .dockerignore, layer caching (зависимости перед кодом) |
| 2 | Compose конвенции | Именование сервисов (kebab-case), depends_on + condition: service_healthy, profiles |
| 3 | Сети | Одна bridge-сеть per environment (`myapp-dev`, `myapp-test`), явное имя (не зависит от имени папки) |
| 4 | Volumes | Named volumes для данных (pgdata), bind mounts для кода (hot reload), anonymous для зависимостей (/app/node_modules) |
| 5 | Порты | Фиксированные (из infrastructure.md): PG=5432, Redis=6379, RabbitMQ=5672/15672, сервисы=8001-8004, gateway=8000 |
| 6 | Health checks | Обязательны для инфраструктуры (pg_isready, redis-cli ping, rabbitmq-diagnostics), рекомендованы для сервисов (/health) |
| 7 | Environment | .env.example (коммитится, шаблон), .env (не коммитится, локальные значения), .env.test (коммитится, без секретов) |
| 8 | Тестовое окружение | docker-compose.test.yml — изолированная сеть, tmpfs для БД (RAM-диск), ephemeral данные |
| 9 | Hot reload | Bind mount + `--reload` (uvicorn/nodemon/air). Anonymous volume для зависимостей. Windows+WSL2: файлы в файловой системе WSL для inotify |

### Артефакт 2: `docker-compose.yml` (dev)

**Путь:** `platform/docker/docker-compose.yml`

Основная dev-конфигурация. Инфраструктурные сервисы (из infrastructure.md):

| Сервис | Образ | Порт | Health check |
|--------|-------|------|-------------|
| postgres | postgres:16-alpine | 5432 | pg_isready |
| redis | redis:7-alpine | 6379 | redis-cli ping |
| rabbitmq | rabbitmq:3-management-alpine | 5672, 15672 | rabbitmq-diagnostics |

Сервисы приложения — stub-секции с комментариями (реальные Dockerfiles появятся при создании сервисов через analysis chain):

```yaml
# Раскомментировать при создании сервиса:
# auth:
#   build:
#     context: ../../src/auth
#     dockerfile: ../../platform/docker/Dockerfile.auth
#     target: development
#   ports: ["8001:8001"]
#   depends_on:
#     postgres: { condition: service_healthy }
#     redis: { condition: service_healthy }
#   volumes: ["../../src/auth:/app"]
#   env_file: [.env]
#   networks: [app-network]
```

Named volumes: `pgdata`, `redis-data`, `rabbitmq-data`.
Сеть: `app-network` (bridge, name: `myapp-dev`).

### Артефакт 3: `docker-compose.test.yml`

**Путь:** `platform/docker/docker-compose.test.yml`

Тестовая конфигурация — изолированные зависимости для integration/e2e тестов:

| Отличие от dev | Зачем |
|----------------|-------|
| `tmpfs` для PostgreSQL | RAM-диск — мгновенная очистка, быстрая запись |
| Отдельная сеть (`myapp-test`) | Не конфликтует с dev |
| Нет bind mounts | Тестам не нужен hot reload |
| Нет сервисов приложения | Поднимаются тестовым фреймворком или docker-compose отдельно |

### Артефакт 4: `.env.example` + `.env.test`

**Путь:** `platform/docker/.env.example`, `platform/docker/.env.test`

`.env.example` — шаблон с описанием всех переменных (из infrastructure.md):
- PostgreSQL: host, port, user, password, per-service DB names
- Redis: host, port, per-service DB numbers
- RabbitMQ: URL
- Service URLs: http://{service}:{port}
- JWT: secret key

`.env.test` — значения для тестов (без секретов, коммитится).

### Артефакт 5: `.dockerignore`

**Путь:** `platform/docker/.dockerignore`

Исключения: `.git/`, `__pycache__/`, `node_modules/`, `.venv/`, `*.pyc`, `tests/` (если не нужны в образе), `.env`.

### Артефакт 6: `init-db.sql`

**Путь:** `platform/docker/init-db.sql`

Скрипт инициализации PostgreSQL — создание per-service баз данных (из infrastructure.md):
```sql
CREATE DATABASE myapp_auth;
CREATE DATABASE myapp_task;
CREATE DATABASE myapp_notification;
CREATE DATABASE myapp_admin;
```

Монтируется в `docker-entrypoint-initdb.d/` PostgreSQL-контейнера.

### Обновления существующих файлов

#### Makefile

Текущая проблема: `make dev` ссылается на `docker-compose.dev.yml` (не существует) и использует устаревший `docker-compose` (V1).

Обновить:
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

test:
	docker compose -f $(COMPOSE_TEST_FILE) up -d --wait
	pytest src/ tests/integration/
	docker compose -f $(COMPOSE_TEST_FILE) down -v

test-e2e:
	docker compose -f $(COMPOSE_TEST_FILE) up -d --wait
	pytest tests/e2e/
	docker compose -f $(COMPOSE_TEST_FILE) down -v
```

#### `.structure/initialization.md`

Добавить Docker Desktop в таблицу зависимостей + шаги установки WSL2. Добавить проверку `docker compose version` в `make setup`.

#### `platform/docker/README.md`

Заменить .gitkeep-заглушку на quick start + обучение Docker:
- Что такое Docker (контейнер vs VM, образ vs контейнер)
- Установка Docker Desktop + WSL2
- Основные команды (docker compose up/down/logs)
- Как это работает в проекте (make dev/stop/clean)
- Troubleshooting (порты, память, пересборка)

#### `platform/.instructions/README.md`

Зарегистрировать `standard-docker.md` (первый стандарт platform/).

#### `standard-process.md`

**Фаза 0 (шаг 0.3):** Добавить Docker Desktop в `make setup`. Ссылка на `standard-docker.md`.
**§ 8:** Добавить `standard-docker.md` в строку Фаза 0.

### Порядок создания

| # | Артефакт | Инструмент | Зависимости |
|---|---------|------------|-------------|
| 1 | `standard-docker.md` | `/instruction-create` | — |
| 2 | `docker-compose.yml` | Write | ← 1 (следует стандарту) |
| 3 | `docker-compose.test.yml` | Write | ← 1 |
| 4 | `.env.example` + `.env.test` | Write | ← 2 |
| 5 | `.dockerignore` + `init-db.sql` | Write | ← 2 |
| 6 | `platform/docker/README.md` | Write | ← 2 |
| 7 | Makefile | Edit | ← 2, 3 |
| 8 | `initialization.md` | Edit | ← 7 |
| 9 | `platform/.instructions/README.md` | Автоматически (шаг 1) | ← 1 |
| 10 | `standard-process.md` §0/§8 | Edit | ← 1 |

## Решения

- **Docker обязателен** — микросервисная архитектура без него не работает локально
- **WSL2 обязателен** на Windows — значительно быстрее Hyper-V, лучше bind mounts
- **Фиксированные порты** — из infrastructure.md, динамические усложняют service discovery
- **`docker compose` (V2)** — не `docker-compose` (V1, устаревший)
- **Multi-stage builds** — dev target с hot reload, prod target с gunicorn. В compose: `target: development`
- **Hot reload через bind mount** — `--reload` (uvicorn/nodemon/air), не пересборка образа
- **tmpfs для тестовой БД** — RAM-диск, мгновенная очистка, быстрая запись
- **Два compose-файла** — dev (docker-compose.yml) и test (docker-compose.test.yml), не override
- **Stub-секции для сервисов** — Dockerfiles появятся при создании реальных сервисов через analysis chain
- **`standard-docker.md` — первый стандарт platform/** — остальные (k8s, monitoring, gateway) отложены до реального использования
- **Обучение пользователя** — в platform/docker/README.md (quick start + Docker basics)
- **Testcontainers для per-service integration** — описать в standard-docker.md как рекомендуемый подход для `src/{svc}/tests/`
- **`make docker-build` отдельно не нужен** — `make build` = `docker compose build` достаточно

## Открытые вопросы

*Нет открытых вопросов.*

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Создать standard-docker.md
  description: >
    Драфт: .claude/drafts/2026-02-24-docker-dev.md (секция "Артефакт 1")
    /instruction-create для platform/.instructions/standard-docker.md.
    9 секций: Dockerfile формат, Compose конвенции, Сети, Volumes, Порты,
    Health checks, Environment, Тестовое окружение, Hot reload.
    Включить: multi-stage builds, layer caching, tmpfs, testcontainers, WSL2.
  activeForm: Создаю standard-docker.md

TASK 2: Создать docker-compose.yml (dev)
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-docker-dev.md (секция "Артефакт 2")
    Создать platform/docker/docker-compose.yml.
    Инфраструктура: postgres:16-alpine, redis:7-alpine, rabbitmq:3-management-alpine.
    Health checks, named volumes, bridge network (myapp-dev).
    Stub-секции для сервисов (закомментированы).
    Порты из infrastructure.md.
  activeForm: Создаю docker-compose.yml

TASK 3: Создать docker-compose.test.yml + .env файлы + .dockerignore + init-db.sql
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-docker-dev.md (секции "Артефакт 3-6")
    Создать 5 файлов в platform/docker/:
    - docker-compose.test.yml (tmpfs, изолированная сеть myapp-test)
    - .env.example (шаблон переменных из infrastructure.md)
    - .env.test (тестовые значения, без секретов)
    - .dockerignore (исключения для Docker build)
    - init-db.sql (CREATE DATABASE per service)
  activeForm: Создаю тестовую конфигурацию Docker

TASK 4: Обновить platform/docker/README.md
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-24-docker-dev.md (секция "Обновления", README)
    Заменить .gitkeep-заглушку на quick start + обучение Docker.
    Что такое Docker, установка Docker Desktop + WSL2, основные команды,
    как работает в проекте (make dev/stop/clean), troubleshooting.
  activeForm: Обновляю Docker README

TASK 5: Обновить Makefile
  blockedBy: [2, 3]
  description: >
    Драфт: .claude/drafts/2026-02-24-docker-dev.md (секция "Обновления", Makefile)
    Заменить пути docker-compose.dev.yml → platform/docker/docker-compose.yml.
    docker-compose → docker compose (V2).
    Добавить COMPOSE_FILE и COMPOSE_TEST_FILE переменные.
    Обновить test/test-e2e таргеты для использования docker-compose.test.yml.
  activeForm: Обновляю Makefile

TASK 6: Обновить initialization.md + make setup
  blockedBy: [5]
  description: >
    Драфт: .claude/drafts/2026-02-24-docker-dev.md (секция "Обновления", initialization)
    Добавить Docker Desktop в таблицу зависимостей initialization.md.
    Шаги: WSL2, Docker Desktop, проверка docker compose version.
    Добавить проверку Docker в make setup.
  activeForm: Обновляю initialization.md

TASK 7: Обновить platform/.instructions/README.md
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-docker-dev.md (секция "Порядок создания", шаг 9)
    Зарегистрировать standard-docker.md в platform/.instructions/README.md.
    Первый стандарт platform/ — обновить секцию "Стандарты".
  activeForm: Обновляю platform README

TASK 8: Обновить standard-process.md
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-docker-dev.md (секция "Обновления", standard-process)
    Фаза 0 (шаг 0.3): добавить Docker Desktop в make setup, ссылка на standard-docker.md.
    §8: добавить standard-docker.md в строку Фаза 0.
  activeForm: Обновляю standard-process.md
```
