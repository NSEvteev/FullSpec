# Project Template

Шаблон fullstack проекта с микросервисной архитектурой.

## Оглавление

- [Быстрый старт](#быстрый-старт)
- [Структура проекта](#структура-проекта)
- [Документация](#документация)

---

## Быстрый старт

### Требования

- Docker и Docker Compose
- Python 3.10+ (для pre-commit)
- Git

### Запуск

```bash
# Клонировать репозиторий
git clone <repository-url>
cd project_template

# Установить pre-commit хуки (обязательно!)
make setup

# Запуск всех сервисов
make dev

# Остановка
make stop
```

### Основные команды

```bash
make help      # Показать все команды
make dev       # Запустить для разработки
make stop      # Остановить сервисы
make test      # Запустить тесты
make lint      # Линтинг
make build     # Собрать для production
```

---

## Структура проекта

**SSOT структуры:** [.structure/README.md](/.structure/README.md)

| Папка | Назначение |
|-------|------------|
| `/.claude/` | Инструменты Claude Code — скиллы, rules, агенты, черновики |
| `/.github/` | GitHub платформа — шаблоны Issues, CI/CD workflows |
| `/.instructions/` | Мета-инструкции — стандарты написания инструкций |
| `/.structure/` | SSOT структуры проекта |
| `/config/` | Конфигурации окружений (dev/staging/prod) |
| `/platform/` | Инфраструктура — Docker, Gateway, K8s, мониторинг |
| `/shared/` | Общий код — контракты API, события, библиотеки |
| `/specs/` | Спецификации — ADR, планы, глоссарий |
| `/src/` | Исходный код сервисов |
| `/tests/` | Системные тесты (e2e, integration, load) |

### Принцип инструкций

Каждая папка содержит `.instructions/` с правилами работы:

```
/src/
├── .instructions/          # Как писать код в /src/
│   ├── standard-*.md       # Стандарты
│   └── README.md           # Индекс инструкций
├── {service}/              # Сервисы
└── README.md               # Описание папки
```

---

## Документация

| Документ | Назначение |
|----------|------------|
| [CLAUDE.md](CLAUDE.md) | Точка входа для Claude Code |
| [.structure/README.md](/.structure/README.md) | SSOT структуры проекта |
| [.structure/quick-start.md](/.structure/quick-start.md) | Quick Start для LLM |
| [specs/glossary.md](/specs/glossary.md) | Глоссарий терминов |

---

## Лицензия

Проприетарный проект.
