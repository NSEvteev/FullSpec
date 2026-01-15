# Project Template

Шаблон проекта с настроенной системой документации и интеграцией Claude Code.

## Документация

| Документ | Назначение |
|----------|------------|
| [CLAUDE.md](CLAUDE.md) | Инструкции для Claude Code |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Руководство для контрибьюторов |
| [CHANGELOG.md](CHANGELOG.md) | Журнал изменений |
| [llm_instructions/](llm_instructions/llm_instructions.md) | Полные инструкции для LLM |
| [general_docs/](general_docs/) | Общая документация проекта |

## Глоссарий

Терминология проекта доступна в [глоссарии](general_docs/glossary.md). Все специфичные термины и понятия, используемые в проекте, описаны там с соответствующими определениями.

---

## Архитектура

Проект использует микросервисную архитектуру с разделением на фронтенд и бэкенд-сервисы.

### Компоненты

- **Web UI** — клиентское веб-приложение
- **API Gateway** — единая точка входа для всех запросов
- **Auth Service** — аутентификация и авторизация
- **Users Service** — управление профилями пользователей
- **Shared Packages** — переиспользуемый код

## Структура проекта

```
project_template/
│
├── .editorconfig                  # Настройки редактора
├── .env.example                   # Шаблон переменных окружения
├── .gitignore                     # Игнорируемые файлы Git
├── docker-compose.yml             # Docker Compose для локальной разработки
├── Makefile                       # Команды для управления проектом
├── CLAUDE.md                      # Инструкции для Claude Code
├── LICENSE                        # Лицензия проекта
├── PROJECT_IMPROVEMENTS.md        # План улучшений структуры
├── README.md                      # Описание проекта (этот файл)
│
├── apps/                          # Клиентские приложения
│   └── web/                       # Веб-фронтенд
│       ├── public/                # Статические файлы
│       ├── src/                   # Исходный код фронтенда
│       ├── tests/                 # Тесты фронтенда
│       └── README.md              # Документация фронтенда
│
├── services/                      # Бэкенд микросервисы
│   ├── api-gateway/               # API Gateway
│   │   ├── src/                   # Исходный код
│   │   ├── tests/                 # Тесты
│   │   └── README.md              # Документация
│   │
│   ├── auth/                      # Сервис авторизации
│   │   ├── src/                   # Исходный код
│   │   ├── tests/                 # Тесты
│   │   ├── static/                # Статические файлы (email шаблоны)
│   │   └── README.md              # Документация
│   │
│   └── users/                     # Сервис управления пользователями
│       ├── src/                   # Исходный код
│       ├── tests/                 # Тесты
│       ├── static/                # Статические файлы
│       └── README.md              # Документация
│
├── packages/                      # Общий переиспользуемый код
│   ├── shared/                    # Общие утилиты и типы
│   ├── ui/                        # UI библиотека компонентов
│   ├── validation/                # Схемы валидации
│   ├── config/                    # Общие конфигурации (ESLint, TS, Prettier)
│   └── README.md
│
├── infrastructure/                # Инфраструктурный код
│   ├── docker/                    # Docker конфигурации
│   ├── kubernetes/                # K8s манифесты
│   ├── terraform/                 # IaC (Infrastructure as Code)
│   └── README.md
│
├── tests/                         # Общие тесты
│   ├── e2e/                       # End-to-end тесты
│   ├── integration/               # Интеграционные тесты
│   ├── load/                      # Нагрузочное тестирование
│   └── README.md
│
├── config/                        # Конфигурационные файлы
│   └── examples/                  # Примеры конфигураций
│       ├── .env.development.example
│       ├── .env.production.example
│       ├── .env.test.example
│       ├── database.config.example.json
│       ├── logging.config.example.yaml
│       └── README.md
│
├── .claude/                       # Конфигурация Claude Code
│   ├── settings.local.json
│   ├── agents/                    # AI-агенты
│   └── skills/                    # Скиллы
│
├── general_docs/                  # Общая документация
│   ├── glossary.md                # Глоссарий терминов
│   ├── 02_architecture/              # Архитектурные документы
│   ├── 03_diagrams/                  # Диаграммы
│   ├── 01_discuss/                   # Дискуссии
│   ├── 06_imp_plans/                 # Планы реализации
│   └── 05_resources/                 # Описания ресурсов
│
├── llm_instructions/              # Инструкции для LLM
│   ├── llm_instructions.md
│   ├── instructions_*.md
│   └── templates/
│
├── llm_tasks/                     # Управление задачами LLM
│   ├── current_tasks.md
│   └── future_tasks.md
│
└── scripts/                       # Служебные скрипты
    └── check_doc_links.py
```

---

## Стек

**Frontend:**
- TODO: Выбрать (React/Vue/Angular + TypeScript + Vite)

**Backend Services:**
- TODO: Выбрать для каждого сервиса (Node.js/Python/Go)

**Базы данных:**
- PostgreSQL 15
- Redis 7

**Инфраструктура:**
- Docker & Docker Compose
- Makefile для автоматизации

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Make (опционально, но рекомендуется)
- Git

### 1. Клонирование и инициализация

```bash
# Клонировать репозиторий
git clone <repository-url>
cd project_template

# Инициализация проекта (создание .env файлов)
make init

# Или вручную:
cp .env.example .env
```

### 2. Запуск всех сервисов

```bash
# Запустить все сервисы в Docker
make dev

# Или напрямую через docker-compose:
docker-compose up -d
```

Доступные сервисы после запуска:
- **Web UI:** http://localhost:3000
- **API Gateway:** http://localhost:8000
- **Auth Service:** http://localhost:8001
- **Users Service:** http://localhost:8002

Dev tools:
- **MailHog:** http://localhost:8025 (тестирование email)
- **PgAdmin:** http://localhost:5050 (управление БД)
- **Redis Commander:** http://localhost:8081 (просмотр Redis)

### 3. Остановка сервисов

```bash
make stop

# Или:
docker-compose down
```

## Полезные команды

```bash
# Показать все доступные команды
make help

# Просмотр логов
make logs                # Все сервисы
make logs-web            # Только фронтенд
make logs-auth           # Только auth сервис

# Тестирование
make test                # Все тесты
make test-unit           # Unit тесты
make test-e2e            # E2E тесты

# База данных
make db-migrate          # Запустить миграции
make db-seed             # Заполнить тестовыми данными
make db-reset            # Сбросить и пересоздать БД

# Проверки кода
make lint                # Линтинг
make format              # Форматирование
make check               # Lint + Tests

# Проверка документации
make docs-health         # Проверка документации (ссылки, структура, статусы)
make docs-links          # Только проверка ссылок
make gloss-health        # Проверка глоссария
make docs-check          # Полная проверка (документация + глоссарий)

# Сборка
make build               # Собрать для production
make build-docker        # Собрать Docker образы
```

---

## Настройки IDE

Проект включает настройки для VS Code в директории `.vscode/`:
- `settings.json` — настройки редактора
- `extensions.json` — рекомендуемые расширения
- `tasks.json` — задачи для автоматизации
- `launch.json` — конфигурация отладки

VS Code автоматически предложит установить рекомендуемые расширения при открытии проекта.

---

## Статус разработки

<!-- TODO: Заполнить -->

## Лицензия

Проприетарный проект.
