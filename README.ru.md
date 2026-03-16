🌐 [English](README.md) | [Русский](README.ru.md)

# Project Template

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/NSEvteev/project_template/actions/workflows/ci.yml/badge.svg)](https://github.com/NSEvteev/project_template/actions/workflows/ci.yml)

**AI-ассистенты пишут код быстро — но без структуры каждый проект изобретает велосипед.** Требования остаются в истории чата, решения не документируются, а "просто напиши" ведёт к переделкам.

Project Template добавляет структурированный процесс разработки: вы с AI **договариваетесь, что строить, до написания кода** — а затем автоматизируете весь путь от идеи до production-релиза.

> **Примечание:** Внутренняя документация проекта (инструкции, стандарты, спецификации) написана на русском языке. Claude Code понимает русский нативно — форкните, настройте со своим Claude, и всё работает.

---

## Как это работает

Одна команда. Полный цикл.

```
Вы: /chain
    "Добавить аутентификацию с OAuth2"

Claude создаёт план и ведёт по всем этапам:

  ✓ Discussion     — уточнить требования, определить критерии успеха
  ✓ Design         — выбрать сервисы, контракты API, модель данных
  ✓ Plan Tests     — написать acceptance-сценарии до кода
  ✓ Plan Dev       — разбить на задачи с зависимостями
  ✓ Docs Sync      — сгенерировать per-service документы и стандарты кодирования
  ✓ Dev Launch     — создать GitHub Issues, Milestone, ветку
  ✓ Implementation — писать код задача за задачей, с валидацией
  ✓ Review & PR    — автоматическое code review и pull request
  ✓ Release        — GitHub Release с changelog

Каждое решение прослеживается. Каждый шаг валидируется. Ничего не теряется.
```

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
| Python 3.8+ | Скрипты валидации, pre-commit |
| Git + GitHub CLI (`gh`) | Контроль версий, Issues, PR |

Подробная настройка: [initialization.md](.structure/initialization.md)

</details>

---

## Зачем этот шаблон?

### Проблема

AI-ассистенты генерируют код быстро — но **какой** код? Без общего понимания требований, архитектуры и критериев успеха получается:
- Фичи, которых никто не просил
- Конфликтующие реализации между сервисами
- Отсутствие тестов на граничные случаи
- Релизы "на авось"

### Как мы это решаем

| Без структуры | С Project Template |
|---|---|
| Требования в истории чата | Формальный документ Discussion с критериями успеха |
| Архитектурные решения ad-hoc | Design с контрактами сервисов и моделями данных |
| Тесты — в последнюю очередь | Plan Tests пишется до кода |
| Задачи расплывчатые | Plan Dev с зависимостями и блоками |
| Стандарты у каждого свои | Per-tech стандарты кодирования генерируются автоматически |
| Документация всегда устарела | Живые документы синхронизируются из спецификаций |
| Релиз — ручной и страшный | Автоматическая валидация → PR → Release пайплайн |

### Что внутри

- **70 скиллов** — slash-команды для каждого шага (`/chain`, `/commit`, `/review`, `/release-create`)
- **23 агента** — параллельные воркеры для анализа, code review, синхронизации документации
- **80+ скриптов валидации** — pre-commit хуки + CI гарантируют целостность
- **16 контекстных правил** — Claude автоматически загружает нужные стандарты при работе с файлами
- **9 per-tech стандартов** — TypeScript, React, FastAPI, PostgreSQL, Protobuf, OpenAPI, AsyncAPI, Tailwind CSS

---

## 8 фаз процесса

```
Фаза 1 — Аналитика        Discussion → Design → Plan Tests → Plan Dev
Фаза 2 — Docs Sync        Per-service документы, per-tech стандарты, overview
Фаза 3 — Запуск           GitHub Issues + Milestone + Branch
Фаза 4 — Реализация       Код по задачам, с детекцией конфликтов
Фаза 5 — Валидация        Тесты, lint, build, e2e → READY / NOT READY
Фаза 6 — Доставка         Code review → PR → Merge
Фаза 7 — Завершение       Обновление живых документов, закрытие цепочки
Фаза 8 — Релиз            GitHub Release + деплой
```

У каждой фазы — свои скиллы и агенты. Фазы идут по порядку, но внутри каждой параллельные агенты ускоряют работу.

Полный процесс: [standard-process.md](specs/.instructions/standard-process.md)

---

## Структура проекта

Каждая папка содержит `.instructions/` — Claude читает их автоматически.

```
src/           → Исходный код сервисов (backend, database, tests)
shared/        → Контракты API, события, общие библиотеки
platform/      → Docker, Gateway, Kubernetes, мониторинг
config/        → Конфигурации окружений (dev / staging / prod)
tests/         → Системные тесты (e2e, integration, load, smoke)
specs/         → Спецификации и analysis chains
.claude/       → Скиллы (70), агенты (23), правила (16)
.github/       → CI/CD workflows, шаблоны Issues, метки
.instructions/ → Мета-инструкции для написания инструкций
```

Полное дерево: [.structure/README.md](.structure/README.md)

---

## Команды

```bash
make setup      # Установить pre-commit хуки (обязательно после клонирования!)
make help       # Показать все команды
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

| Документ | Что найдёте |
|----------|------------|
| [Инициализация](.structure/initialization.md) | Гайд по настройке для 3 платформ (Windows, macOS, Linux) |
| [Структура проекта](.structure/README.md) | Полное дерево папок с описаниями |
| [Процесс поставки](specs/.instructions/standard-process.md) | 8 фаз, статусы, скиллы, агенты |
| [CLAUDE.md](CLAUDE.md) | Точка входа для Claude Code |
| [Глоссарий](specs/glossary.md) | Терминология проекта |

---

## Лицензия

[MIT](LICENSE) — используйте, модифицируйте, распространяйте.
