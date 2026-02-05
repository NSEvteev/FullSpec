---
description: SSOT структуры проекта — единый источник правды о папках и файлах
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
---

# /.structure/ — Структура проекта

> **SSOT** — единый источник правды о структуре папок проекта.

Корневые папки: инструменты Claude (`.claude/`), GitHub платформа (`.github/`), мета-инструкции (`.instructions/`), структура проекта (`.structure/`), конфигурации (`config/`), инфраструктура (`platform/`), общий код (`shared/`), спецификации (`specs/`), исходный код (`src/`), тесты (`tests/`). Корневые файлы: `.gitignore`, `CLAUDE.md`, `Makefile`, `README.md`.

**Полезные ссылки:**
- [Точка входа Claude](../CLAUDE.md)
- [Главный README](../README.md)

---

## Оглавление

- [1. Корневые папки](#1-корневые-папки)
  - [.claude/](#-claude)
  - [.github/](#-github)
  - [.instructions/](#-instructions)
  - [.structure/](#-structure)
  - [config/](#-config)
  - [platform/](#-platform)
  - [shared/](#-shared)
  - [specs/](#-specs)
  - [src/](#-src)
  - [tests/](#-tests)
- [2. Корневые файлы](#2-корневые-файлы)
  - [.gitignore](#-gitignore)
  - [CLAUDE.md](#-claudemd)
  - [Makefile](#-makefile)
  - [README.md](#-readmemd)
- [3. Дерево](#3-дерево)
- [4. Диаграмма](#4-диаграмма)

---

## 1. Корневые папки

### 🔗 [.claude/](../.claude/README.md)

**Инструменты Claude Code.**

Инструкции для написания скиллов и rules (`.instructions/skills/`, `.instructions/rules/`), скиллы автоматизации — 16 команд для управления инструкциями, скриптами, скиллами, rules, ссылками и структурой (`skills/`), контекстные правила для автозагрузки (`rules/`), автономные агенты (`agents/`), черновики и SSOT-документы (`drafts/`), настройки Claude (`settings.json`).

### 🔗 [.github/](../.github/README.md)

**GitHub платформа.**

Стандарты работы с GitHub (`.instructions/`), шаблоны для создания Issues (`ISSUE_TEMPLATE/`), CI/CD pipelines — автоматизация сборки, тестирования и деплоя (`workflows/`).

### 🔗 [.instructions/](../.instructions/README.md)

**Мета-инструкции.**

Стандарты написания инструкций: структура, типы, валидация, статусы, связи между инструкциями, шаблоны, воркфлоу создания/обновления/деактивации.

### 🔗 .structure/ (этот файл)

**SSOT структуры проекта.**

Инструкции по работе со структурой (`.instructions/`), единый источник истины о структуре папок проекта (этот файл).

### 🔗 [config/](../config/README.md)

**Конфигурации окружений.**

Стандарты конфигураций (`.instructions/`), YAML-файлы окружений — development, staging, production, feature flags для управления функциональностью (`feature-flags/`).

### 🔗 [platform/](../platform/README.md)

**Общая инфраструктура.**

Стандарты инфраструктуры (`.instructions/`), Docker-конфигурации (`docker/`), API Gateway — Traefik/Nginx (`gateway/`), Kubernetes манифесты (`k8s/`), мониторинг — Grafana дашборды, Loki логи, Prometheus метрики (`monitoring/`), операционные runbooks (`runbooks/`), инфраструктурные скрипты деплоя и бэкапа (`scripts/`).

### 🔗 [shared/](../shared/README.md)

**Общий код между сервисами.**

Стандарты общего кода (`.instructions/`), статические ресурсы — иконки, шрифты (`assets/`), API контракты — OpenAPI для REST, Protobuf для gRPC (`contracts/`), схемы событий для межсервисного взаимодействия (`events/`), локализация — переводы интерфейса (`i18n/`), общие библиотеки — errors, logging, validation (`libs/`).

### 🔗 [specs/](../specs/README.md)

**Спецификации проекта.**

Инструкции по написанию specs (`.instructions/`), дискуссии по архитектурным решениям (`discussions/`), глоссарий терминов проекта (`glossary.md`), импакт-анализ изменений (`impact/`), спецификации сервисов — ADR (архитектурные решения) и планы реализации (`services/{service}/adr/`, `services/{service}/plans/`).

### 🔗 [src/](../src/README.md)

**Исходный код сервисов.**

Стандарты разработки (`.instructions/`), сервисы проекта (`{service}/`) — каждый содержит: версионированный backend API с handlers, routes, services (`backend/v*/`), общий код между версиями (`backend/shared/`), health endpoints (`backend/health/`), схему БД и миграции (`database/`), документацию сервиса (`docs/`), клиентский код (`frontend/`), unit и integration тесты сервиса (`tests/`).

### 🔗 [tests/](../tests/README.md)

**Системные тесты.**

Стандарты тестирования (`.instructions/`), end-to-end сценарии — полные пользовательские флоу (`e2e/`), общие тестовые данные (`fixtures/`), интеграционные тесты между сервисами (`integration/`), нагрузочные тесты на k6 (`load/`), smoke тесты — быстрая проверка работоспособности (`smoke/`).

---

## 2. Корневые файлы

### 🔗 [.gitignore](../.gitignore)

**Git ignore.**

Файлы и папки, исключённые из системы контроля версий — временные файлы, зависимости, секреты, артефакты сборки.

### 🔗 [CLAUDE.md](../CLAUDE.md)

**Точка входа для Claude.**

Справочная информация о проекте для Claude Code — проверка скиллов, блокирующие пути, структура папок, доступные команды.

### 🔗 [Makefile](../Makefile)

**Команды проекта.**

Унифицированный интерфейс для разработки — `make help` (список команд), `make dev` (запуск), `make test` (тесты), `make lint` (линтинг).

### 🔗 [README.md](../README.md)

**Главный README.**

Описание проекта, быстрый старт для новых разработчиков, ссылки на документацию.

---

## 3. Дерево

```
/
├── .claude/                             # Инструменты Claude Code
│   ├── .instructions/
│   │   ├── agents/                      #   Как писать агентов
│   │   ├── drafts/                      #   Как работать с черновиками
│   │   ├── rules/                       #   Как писать rules
│   │   ├── skills/                      #   Как писать скиллы
│   │   └── state/                       #   Как работать с state
│   ├── agents/                          #   Конфигурации агентов
│   ├── drafts/                          #   Черновики (в git)
│   │   └── examples/                    #     Эталонные примеры черновиков для будущих запросов к LLM
│   ├── hooks/                           #   Claude Code hooks
│   ├── rules/                           #   Rules для автозагрузки контекста
│   ├── skills/                          #   Скиллы (16)
│   ├── state/                           #   Состояние между вызовами
│   ├── CHANGELOG.md                     #   История изменений
│   ├── onboarding.md                    #   Руководство для новых участников
│   ├── README.md                        #   Описание .claude/
│   └── settings.json                    #   Настройки
│
├── .github/                             # GitHub платформа
│   ├── .instructions/                   #   Инструкции для работы с GitHub
│   │   ├── branches/                    #     Стандарт именования и создания веток
│   │   ├── commits/                     #     Стандарт оформления коммитов
│   │   ├── development/                 #     Инструкции для процесса локальной разработки
│   │   └── sync/                        #     Стандарт синхронизации с main
│   ├── ISSUE_TEMPLATE/                  #   Шаблоны Issues
│   ├── labels/                          #   Справочник меток проекта
│   ├── milestones/                      #   Справочник milestones проекта
│   ├── releases/                        #   История релизов проекта
│   ├── workflows/                       #   CI/CD pipelines
│   └── README.md                        #   Описание .github/
│
├── .instructions/                       # Мета-инструкции
│   ├── .scripts/                        #   Скрипты автоматизации
│   ├── migration/                       #   Инструкции для миграции стандартов
│   └── README.md                        #   Индекс инструкций
│
├── .structure/                          # SSOT структуры проекта
│   ├── .instructions/                   #   Как работать со структурой
│   ├── artifacts.md                     #   Типы артефактов системы
│   ├── initialization.md                #   Инициализация проекта
│   ├── pre-commit.md                    #   Pre-commit хуки
│   ├── quick-start.md                   #   Быстрый старт для LLM
│   ├── ssot.md                          #   Паттерн SSOT
│   └── README.md                        #   Этот файл (SSOT структуры)
│
├── config/                              # Конфигурации окружений
│   ├── .instructions/                   #   Стандарты конфигураций
│   ├── feature-flags/                   #   Feature flags
│   └── README.md                        #   Описание config/
│
├── platform/                            # Общая инфраструктура
│   ├── .instructions/                   #   Стандарты инфраструктуры
│   ├── docker/                          #   Docker конфигурации
│   ├── gateway/                         #   API Gateway
│   ├── k8s/                             #   Kubernetes манифесты
│   ├── monitoring/                      #   Мониторинг
│   │   ├── grafana/
│   │   ├── loki/
│   │   └── prometheus/
│   ├── scripts/                         #   Инфраструктурные скрипты
│   └── README.md                        #   Описание platform/
│
├── shared/                              # Общий код между сервисами
│   ├── .instructions/                   #   Стандарты общего кода
│   ├── assets/                          #   Статические ресурсы
│   ├── contracts/                       #   API контракты
│   │   ├── openapi/                     #     REST контракты
│   │   └── protobuf/                    #     gRPC контракты
│   ├── events/                          #   Схемы событий
│   ├── i18n/                            #   Локализация
│   ├── libs/                            #   Общие библиотеки
│   └── README.md                        #   Описание shared/
│
├── specs/                               # Спецификации проекта
│   ├── .instructions/                   #   Как писать specs
│   ├── discussions/                     #   Дискуссии: DISC-*.md
│   ├── impact/                          #   Импакт-анализ: IMPACT-*.md
│   ├── services/                        #   Спецификации сервисов
│   ├── glossary.md                      #   Глоссарий терминов
│   └── README.md                        #   Описание specs/
│
├── src/                                 # Исходный код сервисов
│   ├── .instructions/                   #   Стандарты разработки
│   └── README.md                        #   Описание src/
│
├── tests/                               # Системные тесты
│   ├── .instructions/                   #   Стандарты тестирования
│   ├── e2e/                             #   End-to-end сценарии
│   ├── fixtures/                        #   Общие тестовые данные
│   ├── integration/                     #   Интеграция между сервисами
│   ├── load/                            #   Нагрузочные тесты (k6)
│   ├── smoke/                           #   Smoke тесты
│   └── README.md                        #   Описание tests/
│
├── .gitignore                           # Git ignore
├── .pre-commit-config.yaml              # Pre-commit hooks
├── CLAUDE.md                            # Точка входа для Claude
├── Makefile                             # Команды (make help)
└── README.md                            # Главный README
```

---

## 4. Диаграмма

```mermaid
graph TD
    subgraph "Инфраструктура"
        CLAUDE[.claude/]
        GITHUB[.github/]
        INSTRUCTIONS[.instructions/]
        STRUCTURE[.structure/]
    end

    subgraph "Конфигурация"
        CONFIG[config/]
        PLATFORM[platform/]
    end

    subgraph "Код"
        SRC[src/]
        SHARED[shared/]
        TESTS[tests/]
    end

    subgraph "Документация"
        SPECS[specs/]
    end

    CLAUDE --> |скиллы| SRC
    CLAUDE --> |скиллы| SPECS
    SHARED --> |контракты| SRC
    SPECS --> |планы| SRC
    CONFIG --> |переменные| PLATFORM
    PLATFORM --> |деплой| SRC
    SRC --> |код| TESTS
```

---

## Концептуальные документы

- [Инициализация](./initialization.md) — установка зависимостей после клонирования
- [SSOT](./ssot.md) — паттерн единого источника истины
- [Артефакты системы](./artifacts.md) — типы артефактов и их стандарты
- [Quick Start](./quick-start.md) — быстрое введение для LLM
- [Pre-commit](./pre-commit.md) — автоматическая валидация перед коммитом
