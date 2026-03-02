# Project Template

Шаблон fullstack проекта с микросервисной архитектурой.

## Оглавление

- [Быстрый старт](#быстрый-старт)
- [Структура проекта](#структура-проекта)
- [Процесс разработки](#процесс-разработки)
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

## Процесс разработки

Любое изменение системы проходит полный цикл от идеи до релиза. Точка входа — `/chain`.

```
Фаза 1 — Аналитика (DRAFT → WAITING):
  1. Discussion        — зачем? требования, критерии успеха
  2. Design            — как? сервисы, API, data model, технологии
  3. Plan Tests        — как проверяем? acceptance-сценарии
  4. Plan Dev          — какие задачи? TASK-N, блоки, зависимости

Фаза 2 — Docs Sync:
  5. /docs-sync        — параллельные агенты обновляют specs/docs/
                         (per-service docs + per-tech стандарты + overview.md)

Фаза 3 — Запуск:
  6. /dev-create       — Issues + Milestone + Branch → RUNNING

Фаза 4 — Реализация:
  7. dev-agent         — код + тесты + коммиты (по TASK-N)

Фаза 5 — Финальная валидация:
  8. /test             — sync main, тесты, lint, build, отчёт READY/NOT READY

Фаза 6 — Доставка:
  9. /review           — ревью ветки
 10. /pr-create        — Push + Pull Request
 11. /review {PR}      — ревью PR
 12. /merge            — Squash merge + sync main

Фаза 7 — Завершение:
 13. /chain-done       — DONE + обновление docs/ (Planned Changes → AS IS)

Фаза 8 — Поставка:
 14. /release-create   — GitHub Release (опционально)
```

Подробнее: [standard-process.md](/specs/.instructions/standard-process.md)

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

