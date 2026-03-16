🌐 [English](README.md) | [Русский](README.ru.md)

# Project Template

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/NSEvteev/project_template/actions/workflows/ci.yml/badge.svg)](https://github.com/NSEvteev/project_template/actions/workflows/ci.yml)

Шаблон fullstack проекта с микросервисной архитектурой и AI-powered процессом разработки через [Claude Code](https://claude.ai/code).

Полный цикл от идеи до релиза: дискуссия, проектирование, планирование тестов, план разработки, реализация, ревью, деплой — автоматизирован через **70 скиллов**, **23 агента** и **80+ скриптов валидации**.

> **Примечание:** Внутренняя документация проекта (инструкции, стандарты, спецификации) написана на русском языке. Claude Code понимает русский нативно — просто форкните, настройте под себя и позвольте вашему Claude работать с документацией как есть.

## Оглавление

- [Возможности](#возможности)
- [Быстрый старт](#быстрый-старт)
- [Структура проекта](#структура-проекта)
- [Процесс разработки](#процесс-разработки)
- [Команды](#команды)
- [Документация](#документация)
- [Лицензия](#лицензия)

---

## Возможности

**Процесс поставки ценности** — 8 фаз от идеи до production, каждая автоматизирована скиллами Claude Code. Одна команда `/chain` создаёт полный план и ведёт по всем этапам.

**Analysis chain** — формальная цепочка документов (Discussion → Design → Plan Tests → Plan Dev) с трассируемостью требований, системой статусов и каскадным обнаружением конфликтов.

**Инструкции в каждой папке** — `.instructions/` с правилами, стандартами и скриптами валидации. Claude Code автоматически подхватывает контекст через rules.

**Per-tech стандарты кодирования** — стандарты для TypeScript, React, FastAPI, PostgreSQL, Protobuf и других технологий генерируются из Design и привязываются к конкретным сервисам.

**Pre-commit хуки** — валидация структуры README, rules, скриптов и скиллов при каждом коммите. CI дублирует проверки на GitHub Actions.

**GitHub-интеграция** — скиллы для Issues, Milestones, Labels, PR, Releases. Стандартизированные шаблоны и метки.

---

## Быстрый старт

### Новый проект из template

```bash
# 1. GitHub: "Use this template" → "Create a new repository"
# 2. Клонировать
git clone https://github.com/{owner}/{repo}.git
cd {repo}

# 3. Установить хуки
make setup

# 4. Полная настройка через Claude Code
/init-project
```

Подробная инструкция: [initialization.md](.structure/initialization.md)

### Существующий проект

```bash
git clone https://github.com/NSEvteev/project_template.git
cd project_template

# Установить pre-commit хуки (обязательно!)
make setup

# Запуск сервисов
make dev

# Остановка
make stop
```

### Требования

| Инструмент | Назначение |
|------------|------------|
| Docker + Docker Compose | Контейнеризация сервисов |
| Python 3.8+ | Скрипты валидации, pre-commit |
| Git | Контроль версий |
| GitHub CLI (`gh`) | Работа с Issues, PR, Releases |

---

## Структура проекта

**SSOT структуры:** [.structure/README.md](.structure/README.md)

| Папка | Назначение |
|-------|------------|
| `src/` | Исходный код сервисов |
| `shared/` | Контракты API, события, общие библиотеки |
| `platform/` | Docker, Gateway, Kubernetes, мониторинг |
| `config/` | Конфигурации окружений (dev/staging/prod) |
| `tests/` | Системные тесты (e2e, integration, load) |
| `specs/` | Спецификации, analysis chains, глоссарий |
| `.claude/` | Скиллы, rules, агенты Claude Code |
| `.github/` | Шаблоны Issues, CI/CD workflows |
| `.instructions/` | Мета-инструкции — стандарты написания инструкций |
| `.structure/` | SSOT структуры, инициализация |

Каждая папка содержит `.instructions/` с правилами работы:

```
src/
├── .instructions/          # Стандарты разработки сервисов
│   ├── standard-*.md       # Стандарты
│   └── README.md           # Индекс
├── {service}/              # Сервисы
└── README.md
```

---

## Процесс разработки

Любое изменение системы начинается с `/chain`. Одна команда создаёт TaskList с полной последовательностью от идеи до релиза.

```
Фаза 1 — Аналитика (DRAFT → WAITING):
  1. Discussion        — зачем? требования, критерии успеха
  2. Design            — как? сервисы, API, data model, технологии
  3. Plan Tests        — как проверяем? acceptance-сценарии
  4. Plan Dev          — какие задачи? TASK-N, блоки, зависимости

Фаза 2 — Docs Sync:
  5. /docs-sync        — параллельные агенты: per-service docs,
                         per-tech стандарты, overview.md

Фаза 3 — Запуск:
  6. /dev-create       — Issues + Milestone + Branch → RUNNING

Фаза 4 — Реализация:
  7. dev-agent         — код + тесты + коммиты (по TASK-N)

Фаза 5 — Финальная валидация:
  8. /test             — sync main, тесты, lint, build → READY/NOT READY

Фаза 6 — Доставка:
  9. /review           — ревью ветки
 10. /pr-create        — Pull Request
 11. /merge            — Squash merge + sync main

Фаза 7 — Завершение:
 12. /chain-done       — DONE + обновление docs/

Фаза 8 — Поставка:
 13. /release-create   — GitHub Release
```

Подробнее: [standard-process.md](specs/.instructions/standard-process.md)

---

## Команды

```bash
make setup      # Установить pre-commit хуки (обязательно после клонирования!)
make help       # Показать все команды
make dev        # Запустить для разработки (docker-compose)
make stop       # Остановить сервисы
make test       # Unit/integration тесты
make test-e2e   # E2E тесты
make lint       # Линтинг
make build      # Собрать для production
make clean      # Очистка (docker down -v)
```

---

## Документация

| Документ | Назначение |
|----------|------------|
| [CLAUDE.md](CLAUDE.md) | Точка входа для Claude Code |
| [Инициализация](.structure/initialization.md) | Установка, настройка GitHub, template workflow |
| [Структура проекта](.structure/README.md) | SSOT структуры — дерево папок, описание |
| [Quick Start](.structure/quick-start.md) | Quick Start для LLM |
| [Процесс поставки](specs/.instructions/standard-process.md) | Полный стандарт — 8 фаз, статусы, скиллы |
| [Глоссарий](specs/glossary.md) | Термины проекта |
| [Pre-commit хуки](.structure/pre-commit.md) | Настройка и решение проблем |

---

## Лицензия

Проект распространяется под [лицензией MIT](LICENSE).
