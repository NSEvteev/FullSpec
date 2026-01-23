---
type: project
description: Локальная разработка: make dev, hot reload, debug порты, IDE
related:
  - /.claude/.instructions/src/dev/testing.md
  - /.claude/.instructions/src/dev/performance.md
  - /.claude/.instructions/platform/docker.md
  - /.claude/.instructions/config/environments.md
---

# Локальная разработка

Правила и инструменты для локальной разработки сервисов.

## Оглавление

- [Запуск проекта](#запуск-проекта)
- [Hot reload](#hot-reload)
- [Debug режим](#debug-режим)
- [IDE настройки](#ide-настройки)
- [Работа с сервисами](#работа-с-сервисами)
- [Переменные окружения](#переменные-окружения)
- [Troubleshooting](#troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Запуск проекта

### Быстрый старт

```bash
# Поднять все сервисы
make dev

# Остановить
make stop

# Полная очистка (volumes, images)
make clean
```

### Команды Makefile

| Команда | Описание |
|---------|----------|
| `make dev` | Запуск всех сервисов в dev-режиме |
| `make dev-{service}` | Запуск конкретного сервиса (например `make dev-auth`) |
| `make stop` | Остановка всех сервисов |
| `make restart` | Перезапуск всех сервисов |
| `make logs` | Просмотр логов всех сервисов |
| `make logs-{service}` | Логи конкретного сервиса |
| `make clean` | Очистка volumes и остановка |

### Docker Compose файлы

```
/docker-compose.yml           ← базовая конфигурация
/docker-compose.dev.yml       ← переопределения для dev (volumes, ports)
/docker-compose.test.yml      ← конфигурация для тестов
```

**Правило:** `make dev` использует `docker-compose.dev.yml` поверх базового.

---

## Hot reload

### Принцип работы

Код монтируется в контейнер через volume. При изменении файлов — автоматическая перезагрузка.

### Настройка по языкам

| Язык | Инструмент | Конфигурация |
|------|------------|--------------|
| Node.js | nodemon | `nodemon.json` в сервисе |
| Python | uvicorn --reload | Флаг в docker-compose |
| Go | air | `.air.toml` в сервисе |

### Пример volume mount

```yaml
# docker-compose.dev.yml
services:
  auth:
    volumes:
      - ./src/auth/backend:/app    # монтирование кода
      - /app/node_modules          # исключение node_modules
```

### Исключения из hot reload

- `/node_modules/`, `/vendor/`, `/.venv/`
- Конфигурационные файлы (требуют перезапуска)
- Миграции БД

---

## Debug режим

### Debug порты

| Сервис | Язык | Debug порт | Протокол |
|--------|------|------------|----------|
| auth | Node.js | 9229 | Chrome DevTools |
| users | Node.js | 9230 | Chrome DevTools |
| notification | Python | 5678 | debugpy |
| payment | Go | 2345 | Delve |

### Включение debug

```yaml
# docker-compose.dev.yml
services:
  auth:
    command: node --inspect=0.0.0.0:9229 src/index.js
    ports:
      - "9229:9229"
```

### Node.js (Chrome DevTools)

1. Запустить сервис: `make dev-auth`
2. Открыть Chrome → `chrome://inspect`
3. Нажать "Configure" → добавить `localhost:9229`
4. Кликнуть "inspect" на появившемся target

### Python (debugpy)

```python
# Добавить в код для breakpoint
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()  # опционально — ждать подключения
```

### VS Code attach

```json
// .vscode/launch.json
{
  "configurations": [
    {
      "name": "Attach to Auth",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "restart": true,
      "localRoot": "${workspaceFolder}/src/auth",
      "remoteRoot": "/app"
    }
  ]
}
```

---

## IDE настройки

### VS Code

**Рекомендуемые расширения:**

```json
// .vscode/extensions.json
{
  "recommendations": [
    "ms-azuretools.vscode-docker",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-python.python",
    "golang.go",
    "eamodio.gitlens"
  ]
}
```

**Настройки workspace:**

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  },
  "files.exclude": {
    "**/node_modules": true,
    "**/.venv": true
  }
}
```

### JetBrains (WebStorm, PyCharm, GoLand)

1. **Docker integration:** Settings → Build → Docker → добавить connection
2. **Remote interpreter:** Settings → Languages → выбрать Docker
3. **Run configurations:** создать Docker Compose конфигурацию

### EditorConfig

```ini
# .editorconfig (в корне проекта)
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[Makefile]
indent_style = tab
```

---

## Работа с сервисами

### Выполнение команд внутри контейнера

```bash
# Войти в контейнер
docker exec -it auth sh

# Выполнить одну команду
docker exec auth npm test

# Через Makefile
make exec-auth CMD="npm test"
```

### Просмотр логов

```bash
# Все сервисы
make logs

# Конкретный сервис
make logs-auth

# Follow mode (как tail -f)
docker-compose logs -f auth

# Последние 100 строк
docker-compose logs --tail=100 auth
```

### Перезапуск сервиса

```bash
# Перезапуск одного сервиса
docker-compose restart auth

# Пересборка и запуск
docker-compose up -d --build auth
```

### Доступ к базам данных

| Сервис | БД | Порт | Credentials |
|--------|------|------|-------------|
| auth | PostgreSQL | 5432 | см. .env |
| cache | Redis | 6379 | без пароля (dev) |

```bash
# PostgreSQL CLI
docker exec -it postgres psql -U user -d auth_db

# Redis CLI
docker exec -it redis redis-cli
```

---

## Переменные окружения

### Файлы окружения

```
/.env.example                 ← шаблон (в git)
/.env                         ← локальные значения (НЕ в git)
/src/auth/.env.example        ← шаблон для сервиса
/src/auth/.env                ← значения сервиса
```

### Настройка

```bash
# Скопировать шаблон
cp .env.example .env

# Заполнить значения
nano .env
```

### Приоритет переменных

1. Переменные в docker-compose.yml
2. Файл .env в корне
3. Системные переменные окружения

### Пример .env

```bash
# Database
POSTGRES_USER=developer
POSTGRES_PASSWORD=devpassword
POSTGRES_DB=app_dev

# Services
AUTH_SERVICE_URL=http://auth:8080
USERS_SERVICE_URL=http://users:8080

# Debug
DEBUG=true
LOG_LEVEL=debug
```

---

## Troubleshooting

### Проблема: Порт занят

```bash
# Найти процесс
lsof -i :8080

# Или использовать другой порт в .env
AUTH_PORT=8081
```

### Проблема: Hot reload не работает

1. Проверить volume mounts в docker-compose.dev.yml
2. Проверить nodemon.json / uvicorn --reload
3. На Windows: включить WSL2 для Docker Desktop

### Проблема: Нет доступа к БД

```bash
# Проверить статус контейнера
docker-compose ps postgres

# Проверить логи
docker-compose logs postgres

# Проверить сеть
docker network ls
docker network inspect project_default
```

### Проблема: Изменения в package.json не применяются

```bash
# Пересобрать образ
docker-compose build auth

# Или с очисткой кэша
docker-compose build --no-cache auth
```

### Проблема: "Permission denied" в volumes

```bash
# Linux: проверить права
ls -la src/auth/

# Установить права
chmod -R 755 src/auth/
```

---

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование процесса разработки |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление при изменении конфигурации |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |
| [/environment-check](/.claude/skills/environment-check/SKILL.md) | Проверка окружения разработки |

---

## Связанные инструкции

- [testing.md](./testing.md) — тестирование сервисов
- [performance.md](./performance.md) — профилирование и бенчмарки
- [docker.md](/.claude/.instructions/platform/docker.md) — Docker best practices
- [environments.md](/.claude/.instructions/config/environments.md) — конфигурации окружений
