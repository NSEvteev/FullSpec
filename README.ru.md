🌐 [English](README.md) | [Русский](README.ru.md)

# FullSpec

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/NSEvteev/fullspec/actions/workflows/ci.yml/badge.svg)](https://github.com/NSEvteev/fullspec/actions/workflows/ci.yml)

Фреймворк spec-driven разработки для [Claude Code](https://claude.ai/code). Структурированный процесс от требований до production — сначала спецификации, потом код.

FullSpec организует цикл разработки в цепочку формальных документов (Discussion → Design → Plan Tests → Plan Dev), где каждый шаг валидируется перед следующим. Результат: прослеживаемые решения, консистентная архитектура, автоматизированная доставка.

> Внутренняя документация проекта (инструкции, стандарты, спецификации) написана на русском языке. Claude Code понимает русский нативно — форкните, настройте со своим Claude, и всё работает как есть.

---

## Как это работает

```
/chain "Добавить аутентификацию с OAuth2"

Фаза 1 — Аналитика
  ✓ Discussion     — требования и критерии успеха
  ✓ Design         — сервисы, контракты API, модель данных
  ✓ Plan Tests     — acceptance-сценарии (пишутся до кода)
  ✓ Plan Dev       — задачи с зависимостями и блоками выполнения

Фаза 2 — Docs Sync
  ✓ Per-service документация и стандарты кодирования сгенерированы

Фазы 3–4 — Реализация
  ✓ GitHub Issues + Milestone + Branch созданы
  ✓ Код пишется задача за задачей, с валидацией по спецификациям

Фазы 5–8 — Доставка
  ✓ Тесты, lint, build → Code review → PR → Merge → Release
```

Одна команда запускает процесс. У каждой фазы — свои скиллы и агенты. Решения прослеживаются от требований через проектирование до кода.

---

## Быстрый старт

```bash
# 1. GitHub: "Use this template" → "Create a new repository"

# 2. Клонировать и настроить
git clone https://github.com/{owner}/{repo}.git
cd {repo}
make setup

# 3. Начать строить
/chain
```

<details>
<summary><b>Требования</b></summary>

| Инструмент | Назначение |
|------------|------------|
| [Claude Code](https://claude.ai/code) | AI-ассистент разработки |
| Docker + Docker Compose | Контейнеризация сервисов |
| Python 3.8+ | Скрипты валидации, pre-commit хуки |
| Git + GitHub CLI (`gh`) | Контроль версий, Issues, PR |

Подробная настройка: [initialization.md](.structure/initialization.md)

</details>

---

## Что это даёт

| Аспект | Без спецификаций | С FullSpec |
|--------|-----------------|------------|
| Требования | Разбросаны по истории чата | Формальный документ с критериями успеха |
| Архитектура | Решается на ходу при написании кода | Design с контрактами и моделями данных |
| Тестирование | Пишется после реализации | План тестов определяется до кода |
| Планирование задач | Размыто, без порядка | Задачи с зависимостями и блоками выполнения |
| Стандарты кодирования | Различаются от разработчика к разработчику | Per-tech стандарты генерируются из Design |
| Документация | Устаревает | Живые документы синхронизируются из спецификаций |
| Релиз | Ручной, с риском ошибок | Автоматический: валидация → PR → release |

---

## Что внутри

| Компонент | Количество | Назначение |
|-----------|-----------|------------|
| Скиллы | 70 | Slash-команды для каждого шага: `/chain`, `/commit`, `/review`, `/release-create` |
| Агенты | 23 | Параллельные воркеры для анализа, code review, синхронизации документации |
| Скрипты валидации | 80+ | Pre-commit хуки и CI проверки |
| Контекстные правила | 16 | Автозагрузка стандартов при редактировании файлов определённых типов |
| Per-tech стандарты | 9 | TypeScript, React, FastAPI, PostgreSQL, Protobuf, OpenAPI, AsyncAPI, Tailwind CSS |

---

## Структура проекта

Каждая папка содержит `.instructions/` — Claude читает их автоматически и применяет соответствующие стандарты.

```
src/           → Исходный код сервисов (backend, database, tests)
shared/        → Контракты API, события, общие библиотеки
platform/      → Docker, Gateway, Kubernetes, мониторинг
config/        → Конфигурации окружений (dev / staging / prod)
tests/         → Системные тесты (e2e, integration, load, smoke)
specs/         → Спецификации и analysis chains
.claude/       → Скиллы, агенты, контекстные правила
.github/       → CI/CD workflows, шаблоны Issues, метки
.instructions/ → Стандарты написания инструкций
```

Полное дерево: [.structure/README.md](.structure/README.md)

---

## Команды

```bash
make setup      # Установить pre-commit хуки (обязательно после клонирования)
make help       # Список всех доступных команд
make dev        # Запустить сервисы (docker-compose)
make stop       # Остановить сервисы
make test       # Unit & integration тесты
make test-e2e   # End-to-end тесты
make lint       # Линтинг
make build      # Сборка для production
make clean      # Полная очистка (docker down -v)
```

---

## Документация

| Документ | Содержание |
|----------|-----------|
| [Инициализация](.structure/initialization.md) | Гайд по настройке для Windows, macOS, Linux |
| [Структура проекта](.structure/README.md) | Дерево папок с описаниями |
| [Процесс поставки](specs/.instructions/standard-process.md) | 8 фаз, статусы, скиллы, агенты |
| [CLAUDE.md](CLAUDE.md) | Точка входа для Claude Code |
| [Глоссарий](specs/glossary.md) | Терминология проекта |

---

## Контакт

Вопросы, обратная связь, сотрудничество: [n.s.evteev@ya.ru](mailto:n.s.evteev@ya.ru)

---

## Лицензия

[MIT](LICENSE)
