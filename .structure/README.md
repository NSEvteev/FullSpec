# /.structure/ — Структура проекта

> **SSOT** — единый источник правды о структуре папок проекта.

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
- [3. Дерево папок](#3-дерево-папок)

---

## 1. Корневые папки

### 🔗 [.claude/](../.claude/README.md)

**Инструменты Claude Code.**

Инструкции для написания скиллов (`.instructions/skills/`), автономные агенты (`agents/`), черновики и SSOT-документы (`drafts/`), скиллы автоматизации — 14 команд для управления инструкциями, скиллами, ссылками и спецификациями (`skills/`), настройки Claude (`settings.json`).

### 🔗 [.github/](../.github/README.md)

**GitHub платформа.**

Стандарты работы с GitHub (`.instructions/`), шаблоны для создания Issues (`ISSUE_TEMPLATE/`), CI/CD pipelines — автоматизация сборки, тестирования и деплоя (`workflows/`).

### 🔗 [.instructions/](../.instructions/README.md)

**Мета-инструкции.**

Стандарты написания инструкций: структура, типы, валидация, статусы, связи между инструкциями, шаблоны, воркфлоу создания/обновления/деактивации.

### 🔗 .structure/

**SSOT структуры проекта.**

Единый источник истины о структуре папок проекта — этот файл.

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

```
/
├── .gitignore                       # Git ignore
├── CLAUDE.md                        # Точка входа для Claude
├── Makefile                         # Команды (make help)
└── README.md                        # Главный README
```

---

## 3. Дерево папок

```
/
├── .claude/                             # Инструменты Claude
│   ├── .instructions/
│   │   └── skills/                      #   Как писать скиллы
│   ├── agents/                          #   Агенты
│   ├── drafts/                          #   Черновики (в git)
│   ├── skills/                          #   Скиллы (14)
│   └── settings.json                    #   Настройки
│
├── .github/                             # GitHub платформа
│   ├── .instructions/                   #   Стандарты GitHub (TODO)
│   ├── ISSUE_TEMPLATE/                  #   Шаблоны Issues
│   └── workflows/                       #   CI/CD pipelines
│
├── .instructions/                       # Мета: как писать инструкции
│
├── .structure/                          # SSOT структуры проекта
│   └── README.md                        #   Этот файл
│
├── config/                              # Конфигурации окружений
│   ├── .instructions/                   #   Стандарты конфигураций (TODO)
│   ├── *.yaml                           #   development, staging, production
│   └── feature-flags/                   #   Feature flags
│
├── platform/                            # Общая инфраструктура
│   ├── .instructions/                   #   Стандарты инфраструктуры (TODO)
│   ├── docker/                          #   Docker конфигурации
│   ├── gateway/                         #   API Gateway
│   ├── k8s/                             #   Kubernetes манифесты
│   ├── monitoring/                      #   Мониторинг
│   │   ├── grafana/
│   │   ├── loki/
│   │   └── prometheus/
│   ├── runbooks/                        #   Runbooks
│   └── scripts/                         #   Инфраструктурные скрипты
│
├── shared/                              # Общий код между сервисами
│   ├── .instructions/                   #   Стандарты общего кода (TODO)
│   ├── assets/                          #   Статические ресурсы
│   ├── contracts/                       #   API контракты
│   │   ├── openapi/                     #     REST контракты
│   │   └── protobuf/                    #     gRPC контракты
│   ├── events/                          #   Схемы событий
│   ├── i18n/                            #   Локализация
│   └── libs/                            #   Общие библиотеки
│
├── specs/                               # Спецификации проекта
│   ├── .instructions/                   #   Как писать specs
│   ├── discussions/                     #   Дискуссии: DISC-*.md
│   ├── glossary.md                      #   Глоссарий терминов
│   ├── impact/                          #   Импакт-анализ: IMPACT-*.md
│   └── services/                        #   Спецификации сервисов
│       └── {service}/
│           ├── adr/                     #     ADR-*.md
│           └── plans/                   #     PLAN-*.md
│
├── src/                                 # Исходный код сервисов
│   ├── .instructions/                   #   Стандарты разработки (TODO)
│   └── {service}/                       #   Сервисы
│       ├── backend/
│       │   ├── health/
│       │   ├── shared/
│       │   └── v*/
│       ├── database/
│       │   └── migrations/
│       ├── docs/
│       ├── frontend/
│       └── tests/
│           ├── integration/
│           └── unit/
│
└── tests/                               # Системные тесты
    ├── .instructions/                   #   Стандарты тестирования (TODO)
    ├── e2e/                             #   End-to-end сценарии
    ├── fixtures/                        #   Общие тестовые данные
    ├── integration/                     #   Интеграция между сервисами
    ├── load/                            #   Нагрузочные тесты (k6)
    └── smoke/                           #   Smoke тесты
```
