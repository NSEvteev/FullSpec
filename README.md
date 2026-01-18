# Project Template

Шаблон fullstack проекта с микросервисной архитектурой.

## Документация

| Документ | Назначение |
|----------|------------|
| [CLAUDE.md](CLAUDE.md) | Точка входа для LLM |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Руководство для контрибьюторов |
| [SECURITY.md](SECURITY.md) | Политика безопасности |

## Структура проекта

```
/
├── .claude/                    # Инструменты Claude (инструкции, агенты, скиллы)
├── /src/                       # Код сервисов
├── /doc/                       # Документация (зеркало src, shared, platform)
├── /shared/                    # Общий код (контракты, библиотеки)
├── /config/                    # Конфигурации окружений
├── /platform/                  # Инфраструктура (Docker, мониторинг)
├── /tests/                     # Системные тесты (e2e, нагрузочные)
├── /.github/                   # CI/CD workflows
│
├── CLAUDE.md                   # Точка входа для LLM
├── README.md                   # Руководство по началу работы (этот файл)
├── docker-compose.yml          # Конфигурация запуска сервисов
├── Makefile                    # Интерфейс команд проекта
└── ...
```

## Быстрый старт

### Требования

- Docker и Docker Compose
- Make
- Git

### Запуск

```bash
# Клонировать репозиторий
git clone <repository-url>
cd project_template

# Инициализация проекта
make init

# Запуск всех сервисов
make dev

# Остановка
make stop
```

### Основные команды

```bash
make help          # Показать все команды
make dev           # Запустить для разработки
make stop          # Остановить сервисы
make test          # Запустить тесты
make build         # Собрать для production
```

## Статус

Проект в процессе рефакторинга. См. [refactoring.md](refactoring.md).

## Лицензия

Проприетарный проект.
