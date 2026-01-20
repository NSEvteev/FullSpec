---
type: standard
description: Dockerfile best practices, docker-compose, образы, multi-stage builds
related:
  - platform/deployment.md
  - platform/security.md
  - platform/observability/overview.md
  - git/ci.md
---

# Docker

Правила работы с Docker: написание Dockerfile, docker-compose, управление образами.

## Оглавление

- [Правила](#правила)
  - [Dockerfile best practices](#dockerfile-best-practices)
  - [Multi-stage builds](#multi-stage-builds)
  - [Базовые образы](#базовые-образы)
  - [Docker Compose](#docker-compose)
  - [Теги и версионирование](#теги-и-версионирование)
  - [Безопасность образов](#безопасность-образов)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Dockerfile best practices

**Правило:** Один контейнер = один процесс.

| Практика | Правильно | Неправильно |
|----------|-----------|-------------|
| Процессы | Один main процесс | Несколько сервисов |
| Init система | `--init` или tini | Без init |
| PID 1 | Приложение | Shell wrapper |

**Правило:** Минимизировать количество слоёв, группируя команды.

```dockerfile
# Правильно: один слой
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Неправильно: много слоёв
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y ca-certificates
```

**Правило:** Использовать `.dockerignore` для исключения ненужных файлов.

```dockerignore
# .dockerignore
.git
.gitignore
*.md
!README.md
node_modules
__pycache__
.env*
.vscode
.idea
coverage
dist
```

**Правило:** Порядок инструкций — от редко меняющихся к часто меняющимся.

```dockerfile
# 1. Базовый образ (редко меняется)
FROM node:20-alpine

# 2. Системные зависимости (редко меняются)
RUN apk add --no-cache dumb-init

# 3. Рабочая директория
WORKDIR /app

# 4. Зависимости приложения (меняются при обновлении)
COPY package*.json ./
RUN npm ci --only=production

# 5. Код приложения (меняется часто)
COPY . .

# 6. Настройки запуска
USER node
EXPOSE 3000
CMD ["dumb-init", "node", "server.js"]
```

### Multi-stage builds

**Правило:** Использовать multi-stage для уменьшения размера финального образа.

```dockerfile
# Стадия сборки
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Финальная стадия
FROM node:20-alpine AS production
WORKDIR /app
RUN apk add --no-cache dumb-init
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["dumb-init", "node", "dist/server.js"]
```

**Правило:** Именовать стадии для ясности и повторного использования.

| Стадия | Назначение |
|--------|------------|
| `base` | Общие зависимости |
| `builder` | Компиляция, сборка |
| `test` | Запуск тестов |
| `production` | Финальный образ |

### Базовые образы

**Правило:** Использовать официальные образы с тегом версии.

| Тип | Рекомендуемый образ | Размер |
|----|---------------------|--------|
| Node.js | `node:20-alpine` | ~180MB |
| Python | `python:3.12-slim` | ~150MB |
| Go | `golang:1.22-alpine` (build), `scratch` (run) | ~10MB |
| Java | `eclipse-temurin:21-jre-alpine` | ~200MB |

**Правило:** Для production использовать `-alpine` или `-slim` варианты.

**Правило:** Никогда не использовать `latest` — всегда указывать версию.

```dockerfile
# Правильно
FROM node:20.11-alpine

# Неправильно
FROM node:latest
FROM node
```

### Docker Compose

**Правило:** Использовать версию 3.8+ для docker-compose.yml.

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  postgres_data:
  redis_data:
```

**Правило:** Использовать `depends_on` с условиями для порядка запуска.

**Правило:** Конфигурировать healthcheck для всех сервисов.

### Теги и версионирование

**Правило:** Использовать семантическое версионирование для образов.

| Тег | Назначение | Пример |
|-----|------------|--------|
| `v{semver}` | Релизные версии | `app:v1.2.3` |
| `{git-sha}` | CI/CD билды | `app:a1b2c3d` |
| `latest` | Последний стабильный | `app:latest` |
| `{branch}-{sha}` | Feature branches | `app:feature-abc-a1b2c3d` |

**Правило:** В production использовать только immutable теги (semver или sha).

```bash
# Сборка с тегами
docker build -t myapp:v1.2.3 -t myapp:latest .

# В CI/CD
docker build -t myapp:${GITHUB_SHA} .
```

### Безопасность образов

**Правило:** Не запускать контейнер от root.

```dockerfile
# Создать пользователя
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -D appuser

# Переключиться на пользователя
USER appuser
```

**Правило:** Не хранить секреты в образе.

```dockerfile
# Неправильно
ENV API_KEY=secret123
COPY .env /app/.env

# Правильно — передавать при запуске
# docker run -e API_KEY=$API_KEY myapp
```

**Правило:** Сканировать образы на уязвимости.

```bash
# Trivy
trivy image myapp:latest

# Docker Scout
docker scout cves myapp:latest
```

---

## Примеры

### Пример 1: Node.js приложение

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS base
WORKDIR /app
RUN apk add --no-cache dumb-init

FROM base AS deps
COPY package*.json ./
RUN npm ci --only=production

FROM base AS builder
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM base AS production
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["dumb-init", "node", "dist/server.js"]
```

### Пример 2: Python приложение

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

FROM base AS builder
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM base AS production
COPY --from=builder /app/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN adduser --disabled-password --gecos '' appuser
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

### Пример 3: Go приложение (scratch)

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app
RUN apk add --no-cache ca-certificates tzdata
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server ./cmd/server

FROM scratch AS production
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /app/server /server
USER 65534:65534
EXPOSE 8080
ENTRYPOINT ["/server"]
```

### Пример 4: docker-compose для разработки

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build:
      context: .
      target: base
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port
    environment:
      - NODE_ENV=development
    command: npm run dev

  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: app_dev
    volumes:
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| — | Пока нет специализированных скиллов |

---

## FAQ / Troubleshooting

### Образ слишком большой — как уменьшить?

1. **Использовать multi-stage builds:**
   - Отделить build-зависимости от runtime

2. **Выбрать минимальный базовый образ:**
   | Образ | Размер |
   |-------|--------|
   | `ubuntu:22.04` | ~77MB |
   | `debian:slim` | ~80MB |
   | `alpine:3.19` | ~7MB |
   | `scratch` | 0MB |

3. **Очистить кэш пакетных менеджеров:**
   ```dockerfile
   RUN apt-get update && apt-get install -y \
       package1 \
       && rm -rf /var/lib/apt/lists/*
   ```

4. **Проанализировать слои:**
   ```bash
   docker history myapp:latest
   dive myapp:latest  # интерактивный анализ
   ```

### Контейнер падает при запуске — как отладить?

1. **Посмотреть логи:**
   ```bash
   docker logs <container_id>
   docker logs -f <container_id>  # follow
   ```

2. **Запустить интерактивно:**
   ```bash
   docker run -it myapp:latest /bin/sh
   ```

3. **Проверить entrypoint:**
   ```bash
   docker inspect myapp:latest | jq '.[0].Config.Entrypoint'
   docker inspect myapp:latest | jq '.[0].Config.Cmd'
   ```

4. **Проверить права доступа:**
   ```bash
   docker run -it myapp:latest ls -la /app
   ```

### Как передать секреты при сборке?

**Использовать BuildKit secrets:**

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm install
```

```bash
DOCKER_BUILDKIT=1 docker build --secret id=npmrc,src=.npmrc .
```

**Не использовать ARG для секретов** — они видны в истории образа.

### Как ускорить сборку?

1. **Использовать кэш зависимостей:**
   ```dockerfile
   COPY package*.json ./
   RUN npm ci
   COPY . .
   ```

2. **Использовать BuildKit:**
   ```bash
   DOCKER_BUILDKIT=1 docker build .
   ```

3. **Использовать cache mounts:**
   ```dockerfile
   RUN --mount=type=cache,target=/root/.npm \
       npm ci
   ```

4. **Параллельные стадии в multi-stage:**
   ```dockerfile
   FROM base AS deps
   ...

   FROM base AS assets
   ...

   FROM base AS final
   COPY --from=deps ...
   COPY --from=assets ...
   ```

### Как работать с приватными репозиториями?

**Для npm:**
```dockerfile
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci
```

**Для Go:**
```dockerfile
ARG GOPRIVATE=github.com/myorg/*
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    go mod download
```

**Для pip:**
```dockerfile
RUN --mount=type=secret,id=pip,target=/root/.pip/pip.conf \
    pip install -r requirements.txt
```

---

## Связанные инструкции

- [deployment.md](deployment.md) — Стратегии деплоя
- [security.md](security.md) — Безопасность инфраструктуры
- [observability/overview.md](observability/overview.md) — Наблюдаемость
- [ci.md](../git/ci.md) — CI/CD pipeline
