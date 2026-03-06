---
description: Воркфлоу поднятия Docker dev-окружения — docker compose up, healthcheck всех сервисов, troubleshooting. SSOT для скилла /docker-up.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу Docker dev-окружения

Рабочая версия стандарта: 1.3

Оркестрация поднятия dev-окружения (шаг 5.1 в chain). Последовательно: проверка предусловий, docker compose up --build, healthcheck всех сервисов, подтверждение готовности портов.

**Полезные ссылки:**
- [Инструкции specs/](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-docker.md](/platform/.instructions/standard-docker.md) — правила Docker в проекте |
| Валидация | *Не требуется* |
| Создание | Этот документ |
| Модификация | *Не требуется* |

**SSOT-зависимости:**
- [standard-docker.md](/platform/.instructions/standard-docker.md) — общий стандарт Docker
- [docker-compose.yml](/platform/docker/docker-compose.yml) — единственный источник сервисов, портов, healthcheck

## Оглавление

- [Принципы](#принципы)
- [Предварительные требования](#предварительные-требования)
- [Шаги](#шаги)
  - [Шаг 1: Проверить предусловия](#шаг-1-проверить-предусловия)
  - [Шаг 2: Запустить окружение](#шаг-2-запустить-окружение)
  - [Шаг 3: Healthcheck](#шаг-3-healthcheck)
- [Runbook](#runbook)
  - [Источник истины](#источник-истины)
  - [Добавление нового сервиса](#добавление-нового-сервиса)
  - [Удаление сервиса](#удаление-сервиса)
  - [Запуск и остановка](#запуск-и-остановка)
  - [Hot-reload](#hot-reload)
  - [Известные грабли](#известные-грабли)
  - [Текущее состояние](#текущее-состояние)
- [Чек-лист](#чек-лист)
- [Скиллы](#скиллы)

---

## Принципы

> **Явный шаг перед тестами.** Docker-окружение — prerequisite для /test и /test-ui. Поднимается один раз явно, не "на лету" внутри других скиллов.

> **СТОП при unhealthy.** Если хотя бы один сервис не прошёл healthcheck — остановиться. Чинить Docker, не переходить к следующему шагу.

> **stop, не down.** После работы — `make stop` (контейнеры сохраняются, перезапуск мгновенный). `down` / `down -v` только при осознанной необходимости (`make clean`).

> **Каждый сервис ДОЛЖЕН иметь healthcheck.** Без healthcheck нельзя надёжно определить готовность сервиса.

---

## Предварительные требования

| Требование | Как проверить | При failure |
|------------|---------------|-------------|
| `.env` файл существует | `test -f platform/docker/.env` | `cp platform/docker/.env.example platform/docker/.env`, заполнить секреты |
| `.dockerignore` существует | `test -f .dockerignore` | СТОП: без него сборка зависнет на Windows/WSL2 |
| Docker Desktop запущен | `docker ps` выполняется без ошибки | Запустить Docker Desktop |
| Нет конфликтующих compose | `docker ps` — нет контейнеров на портах 5432/8001/3000 | `docker ps` → остановить конфликтующий compose |

---

## Шаги

### Шаг 1: Проверить предусловия

```bash
# Docker доступен?
docker ps

# .env существует?
test -f platform/docker/.env && echo "OK" || echo "MISSING"

# Порты свободны?
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

**При failure:** устранить проблему, не переходить к Шагу 2.

### Шаг 2: Запустить окружение

```bash
docker compose -f platform/docker/docker-compose.yml up -d --build
```

**Ожидание:** команда завершается без ошибок. Если сборка зависает >5 мин — проверить `.dockerignore`.

### Шаг 3: Healthcheck

```bash
# Все контейнеры healthy?
docker ps --format "table {{.Names}}\t{{.Status}}"
```

Ожидаемый статус каждого сервиса: `healthy`.

```bash
# Дополнительно — проверить health endpoint backend-сервисов:
curl http://localhost:8001/api/v1/health
```

**Критерий прохождения:** все сервисы `healthy`. Если нет — см. [Известные грабли](#известные-грабли).

---

## Runbook

### Источник истины

- **Compose-файл:** `platform/docker/docker-compose.yml` — единственный источник списка сервисов, портов, зависимостей
- **Env-шаблон:** `platform/docker/.env.example` — все переменные с дефолтами для dev
- **Dockerignore:** `.dockerignore` в корне репо — контроль build context

### Добавление нового сервиса

1. Добавить сервис в `docker-compose.yml` с обязательными полями: `ports`, `healthcheck`, `depends_on`
2. Dockerfile размещать в `src/{service}/Dockerfile` (единый для dev и test), **не** в `platform/docker/`
3. Добавить volume-маппинг исходников для hot-reload: `../../src/{service}:/app/src/{service}`
4. Если сервис зависит от shared-пакета — добавить volume и `PYTHONPATH`
5. Если сервис требует секреты — добавить переменные в `.env.example` с пустыми значениями
6. Обновить `.dockerignore`: добавить `!src/{service}/**` и `!shared/{service}/**` (если есть)

### Удаление сервиса

1. Удалить сервис из `docker-compose.yml`
2. Убрать его переменные из `.env.example` (если не используются другими сервисами)
3. Убрать `!src/{service}/**` из `.dockerignore`

### Запуск и остановка

```bash
# Запуск (из любой директории)
docker compose -f platform/docker/docker-compose.yml up -d --build

# Остановка (контейнеры сохраняются, перезапуск мгновенный)
docker compose -f platform/docker/docker-compose.yml stop
# make stop

# Перезапуск остановленных контейнеров (без пересборки)
docker compose -f platform/docker/docker-compose.yml start

# Полное удаление контейнеров (пересоздание при следующем up)
docker compose -f platform/docker/docker-compose.yml down

# Полное удаление + данные (volumes)
docker compose -f platform/docker/docker-compose.yml down -v
# make clean
```

**Правило:** после Фазы 5 контейнеры **не удаляются автоматически**. Разработчик сам решает: `make stop` (пауза) или `make clean` (полный сброс).

### Hot-reload

Dev compose ДОЛЖЕН монтировать исходники через volumes, чтобы изменения в `src/{service}/` автоматически подхватывались (uvicorn --reload, Vite HMR, etc.).

### Известные грабли

| Симптом | Причина | Решение |
|---------|---------|---------|
| `bind: address already in use` | Запущен другой compose | `docker ps` → остановить конфликтующий compose |
| Сборка зависает (>5 мин) | Нет `.dockerignore` или широкий build context | Проверить `.dockerignore`, Dockerfile из `src/{service}/` |
| Сервис unhealthy — ошибка парсинга `.env` | pydantic_settings парсит `list[str]` как JSON | Значение должно быть `["item1","item2"]`, не `item1,item2` |
| Сервис не видит shared-пакет | Нет volume-маппинга или PYTHONPATH | Добавить volume `../../shared/{pkg}:/app/shared/{pkg}` + `PYTHONPATH` |
| Dockerfile в `platform/docker/` устарел | Исторический артефакт | Использовать `src/{service}/Dockerfile` |

### Текущее состояние

> Заполняется в проекте. Формат:

```
postgres:{PORT} → {svc}:{PORT} → ...
```

| Сервис | Порт | Dockerfile | Healthcheck |
|--------|------|-----------|-------------|
| postgres | `{PORT}` | `postgres:16-alpine` (готовый образ) | `pg_isready` |
| `{svc}` | `{PORT}` | `src/{svc}/Dockerfile` | `/api/v1/health` |

**Паттерн Dockerfile (обязательный):**
- Размещение: `src/{svc}/Dockerfile` (НЕ в `platform/docker/`)
- Multi-stage: `builder` (gcc + pip install) → `runtime` (COPY --from=builder site-packages, без gcc)
- БД: один postgres, per-service базы через `init-db.sql` (НЕ отдельный postgres-инстанс)

Предварительные требования: заполняются в проекте.

---

## Чек-лист

- [ ] `.env` файл существует (`platform/docker/.env`)
- [ ] `.dockerignore` существует в корне репо
- [ ] Docker Desktop запущен (`docker ps` без ошибок)
- [ ] Нет конфликтующих контейнеров на портах сервисов
- [ ] `docker compose up -d --build` завершился без ошибок
- [ ] Все сервисы в статусе `healthy` (`docker ps`)
- [ ] Health endpoint backend-сервисов отвечает 200

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/docker-up](/.claude/skills/docker-up/SKILL.md) | Поднятие Docker dev-окружения | Этот документ |
