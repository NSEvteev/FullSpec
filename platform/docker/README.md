# /platform/docker/ — Docker конфигурации

| IN | OUT |
|----|-----|
| docker-compose.yml, Dockerfile.* | Конфиги сервиса (→ `/src/{service}/`) |

**Стандарт:** [standard-docker.md](/platform/.instructions/standard-docker.md)

---

## Quick Start

```bash
# 1. Скопировать переменные окружения
cp platform/docker/.env.example platform/docker/.env

# 2. Запустить инфраструктуру (PostgreSQL, Redis, RabbitMQ)
make dev

# 3. Проверить что всё работает
docker compose -f platform/docker/docker-compose.yml ps

# 4. Остановить
make stop

# 5. Остановить и удалить данные
make clean
```

---

## Что такое Docker

**Контейнер** — изолированный процесс с собственной файловой системой, сетью и зависимостями. В отличие от виртуальной машины, контейнер использует ядро хоста — запускается за секунды, не минуты.

**Образ (image)** — шаблон для создания контейнера. Содержит код, зависимости, конфигурацию. Собирается из `Dockerfile`.

**Docker Compose** — оркестратор нескольких контейнеров. Описывает все сервисы в одном YAML-файле, запускает их одной командой.

---

## Установка

### Windows

1. **WSL2** (обязательно):
   ```powershell
   wsl --install
   ```
   Перезагрузить компьютер после установки.

2. **Docker Desktop:**
   - Скачать: https://www.docker.com/products/docker-desktop/
   - При установке выбрать "Use WSL 2 based engine"
   - После установки: Settings → Resources → WSL Integration → включить для дистрибутива

3. **Проверить:**
   ```bash
   docker compose version
   # Docker Compose version v2.x.x
   ```

### macOS / Linux

1. Установить Docker Desktop (macOS) или Docker Engine (Linux)
2. Проверить: `docker compose version`

---

## Основные команды

| Команда | Описание |
|---------|----------|
| `make dev` | Запустить все сервисы |
| `make stop` | Остановить сервисы (данные сохраняются) |
| `make clean` | Остановить + удалить volumes (полная очистка) |
| `make build` | Пересобрать образы |
| `make test` | Запустить тесты (поднимает тестовую инфраструктуру) |

### Docker Compose напрямую

```bash
# Логи конкретного сервиса
docker compose -f platform/docker/docker-compose.yml logs -f postgres

# Статус сервисов
docker compose -f platform/docker/docker-compose.yml ps

# Подключиться к PostgreSQL
docker compose -f platform/docker/docker-compose.yml exec postgres psql -U myapp

# Подключиться к Redis
docker compose -f platform/docker/docker-compose.yml exec redis redis-cli
```

---

## Структура файлов

```
platform/docker/
├── docker-compose.yml       # Dev-окружение (основной)
├── docker-compose.test.yml  # Тестовое окружение (tmpfs, изолированная сеть)
├── .env.example             # Шаблон переменных (коммитится)
├── .env                     # Локальные значения (НЕ коммитится)
├── .env.test                # Тестовые значения (коммитится)
├── .dockerignore            # Исключения для Docker build
├── init-db.sql              # Создание per-service баз данных
└── README.md                # Этот файл
```

---

## Troubleshooting

### Порт занят

```
Error: Bind for 0.0.0.0:5432 failed: port is already allocated
```

Другой процесс использует порт. Найти и остановить:
```bash
# Linux/macOS
lsof -i :5432
# Windows (PowerShell)
netstat -ano | findstr :5432
```

### Hot reload не работает (Windows)

Bind mounts из Windows-файловой системы (`/mnt/c/`) не поддерживают inotify. Перенести проект в файловую систему WSL2: `/home/user/projects/`.

### Контейнер перезапускается в цикле

```bash
# Посмотреть логи
docker compose -f platform/docker/docker-compose.yml logs postgres
```

Частые причины: неправильные переменные окружения, нехватка памяти Docker Desktop (Settings → Resources → Memory).

### Пересборка образа

```bash
# Пересобрать конкретный сервис без кэша
docker compose -f platform/docker/docker-compose.yml build --no-cache auth
```
