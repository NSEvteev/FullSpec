# Инструкции для LLM

## Назначение

Папка `llm_instructions/` содержит все инструкции для работы LLM с проектом.

**Связанные ресурсы:**
- [CLAUDE.md](../CLAUDE.md) — краткие инструкции для Claude Code
- [llm_tasks/](../llm_tasks/) — управление задачами сессии
- [general_docs/](../general_docs/) — общая документация проекта

---

## Инструкции

| Файл | Назначение |
|------|------------|
| [general_docs.md](general_docs.md) | Правила ведения документации: структура `general_docs/`, [📖 workflow статусов](../general_docs/glossary.md#workflow-статусов), правила [📖 feedback](../general_docs/glossary.md#feedback), шаблоны |
| [tasks.md](tasks.md) | **Управление задачами через `llm_tasks/`** (current_tasks.md, future_tasks.md) |
| [scripts.md](scripts.md) | Служебные скрипты для поддержания порядка в проекте |
| [agents.md](agents.md) | Конфигурация AI-[📖 агентов](../general_docs/glossary.md#агент) Claude Code (`.claude/agents/`) — включая **Amy Santiago** (Documentation Manager) |
| [skills.md](skills.md) | Конфигурация [📖 скиллов](../general_docs/glossary.md#скилл) Claude Code (`.claude/skills/`) |
| [workflow_test_doc.md](workflow_test_doc.md) | **Тест workflow документации** — полный цикл от дискуссии до задач |

---

## Шаблоны документов

Папка `templates/` содержит шаблоны для создания документов в `general_docs/`:

| Шаблон | Назначение | Расположение документов |
|--------|------------|-------------------------|
| [discuss.md](templates/discuss.md) | [📖 Дискуссии](../general_docs/glossary.md#дискуссия) (идея → решение) | `general_docs/01_discuss/` |
| [architecture.md](templates/architecture.md) | Архитектурные документы | `general_docs/02_architecture/` |
| [decision_adr.md](templates/decision_adr.md) | [📖 Decision (ADR)](../general_docs/glossary.md#decision-adr) — архитектурные решения | `general_docs/04_decisions/` |
| [imp_plan.md](templates/imp_plan.md) | [📖 Планы реализации](../general_docs/glossary.md#план-реализации) | `general_docs/06_imp_plans/` |
| [resource.md](templates/resource.md) | Описания ресурсов | `general_docs/05_resources/` |
| [folder_doc.md](templates/folder_doc.md) | [📖 Документация папок](../general_docs/glossary.md#документация-папок) кода | `src/*/[название]_doc.md` |
| [000_index.md](templates/000_index.md) | Индексные файлы (000_*.md) | Индексы в папках `general_docs/` |
| [general_docs_README.md](templates/general_docs_README.md) | README для основных папок документации | `general_docs/*/README.md` |
| [resources_README.md](templates/resources_README.md) | README для папок ресурсов | `general_docs/05_resources/*/README.md` |

**Примечание:** Шаблоны — рекомендуемая структура. Адаптируйте под конкретную задачу.

---

### Ключевые особенности структуры

**Микросервисная архитектура:**
- `apps/web/` — клиентское веб-приложение
- `services/api-gateway/` — единая точка входа, маршрутизация запросов
- `services/auth/` — аутентификация, авторизация, JWT, OAuth
- `services/users/` — управление пользователями, RBAC, профили

**Переиспользуемый код:**
- `packages/shared/` — общие утилиты и типы
- `packages/ui/` — библиотека UI компонентов
- `packages/validation/` — схемы валидации
- `packages/config/` — конфигурации линтеров и форматтеров

**Инфраструктура:**
- Docker Compose для локальной разработки
- Makefile с 40+ командами автоматизации
- Kubernetes манифесты для продакшена
- Terraform для IaC

**Базы данных:**
- PostgreSQL 15 (отдельные БД для auth и users)
- Redis 7 (кеширование, сессии)

**Инструменты разработки:**
- MailHog — тестирование email (http://localhost:8025)
- PgAdmin — управление БД (http://localhost:5050)
- Redis Commander — просмотр Redis (http://localhost:8081)

**Проверка документации:**
- `check_doc_health.py` — ссылки, структура, статусы, метаданные
- `check_gloss_health.py` — проверка глоссария
- Скилл `/doc-health` для Claude Code

**IDE:**
- VS Code настройки (.vscode/)
- Рекомендуемые расширения
- Задачи и отладка

---

## Быстрый старт LLM

См. раздел «Быстрый старт LLM» в [CLAUDE.md](../CLAUDE.md#быстрый-старт-llm)


## Структура проекта

Проект использует микросервисную архитектуру с разделением на клиентские приложения (`apps/`), бэкенд-сервисы (`services/`), общий код (`packages/`) и инфраструктуру (`infrastructure/`).

```
project_template/
│
├── .editorconfig                      # Настройки редактора
├── .env.example                       # Шаблон переменных окружения
├── .gitignore                         # Игнорируемые файлы Git
├── docker-compose.yml                 # Docker Compose для локальной разработки
├── Makefile                           # Команды для управления проектом (40+ команд)
├── CLAUDE.md                          # Быстрый справочник Claude
├── CHANGELOG.md                       # Журнал изменений (Keep a Changelog)
├── CONTRIBUTING.md                    # Руководство для контрибьюторов
├── LICENSE                            # Лицензия проекта
├── PROJECT_IMPROVEMENTS.md            # План улучшений (Фаза 1,2,4,5 ✅)
├── README.md                          # Описание проекта
│
├── apps/                              # Клиентские приложения
│   └── web/                           # Веб-фронтенд
│       ├── public/                    # Статические файлы
│       ├── src/                       # Исходный код фронтенда
│       ├── tests/                     # Тесты фронтенда
│       ├── Dockerfile                 # Docker образ
│       ├── .env.example               # Переменные окружения
│       └── README.md                  # Документация (стек, API integration)
│
├── services/                          # Бэкенд микросервисы
│   ├── api-gateway/                   # API Gateway (единая точка входа)
│   │   ├── src/                       # Исходный код
│   │   ├── tests/                     # Тесты
│   │   ├── Dockerfile                 # Docker образ
│   │   ├── .env.example               # Переменные окружения
│   │   └── README.md                  # Документация (middleware, routing)
│   │
│   ├── auth/                          # Сервис авторизации
│   │   ├── src/                       # Исходный код
│   │   ├── tests/                     # Тесты
│   │   ├── static/                    # Email шаблоны
│   │   ├── Dockerfile                 # Docker образ
│   │   ├── .env.example               # Переменные окружения
│   │   └── README.md                  # Документация (JWT, OAuth, API)
│   │
│   └── users/                         # Сервис управления пользователями
│       ├── src/                       # Исходный код
│       ├── tests/                     # Тесты
│       ├── static/                    # Статические файлы
│       ├── Dockerfile                 # Docker образ
│       ├── .env.example               # Переменные окружения
│       └── README.md                  # Документация (RBAC, profiles, API)
│
├── packages/                          # Общий переиспользуемый код
│   ├── shared/                        # Утилиты, типы, константы
│   │   └── src/
│   ├── ui/                            # UI библиотека компонентов
│   │   └── components/
│   ├── validation/                    # Схемы валидации (Zod/Joi)
│   │   └── src/
│   ├── config/                        # Конфигурации (ESLint, TS, Prettier)
│   │   ├── eslint/
│   │   ├── typescript/
│   │   └── prettier/
│   └── README.md                      # Документация пакетов
│
├── infrastructure/                    # Инфраструктурный код
│   ├── docker/                        # Docker конфигурации
│   │   ├── postgres/                  # Скрипты инициализации БД
│   │   └── nginx/                     # Конфигурация веб-сервера
│   ├── kubernetes/                    # K8s манифесты
│   │   ├── deployments/
│   │   ├── services/
│   │   └── ingress/
│   ├── terraform/                     # IaC (Infrastructure as Code)
│   │   ├── modules/
│   │   └── environments/
│   └── README.md                      # Документация инфраструктуры
│
├── tests/                             # Общие тесты
│   ├── e2e/                           # End-to-end тесты
│   ├── integration/                   # Интеграционные тесты
│   ├── load/                          # Нагрузочное тестирование
│   └── README.md                      # Документация тестирования
│
├── config/                            # Конфигурационные файлы
│   └── examples/                      # Примеры конфигураций
│       ├── .env.development.example   # Dev окружение
│       ├── .env.production.example    # Production окружение
│       ├── .env.test.example          # Test окружение
│       ├── database.config.example.json
│       ├── logging.config.example.yaml
│       └── README.md
│
├── .claude/                           # Конфигурация Claude Code
│   ├── settings.local.json
│   ├── agents/                        # AI-агенты
│   │   ├── amy-santiago.md            # Documentation Manager
│   │   └── README.md
│   └── skills/                        # Скиллы
│       ├── architect/                 # Создание архитектуры из дискуссии
│       ├── commit-push/               # Коммит и пуш с форматированием
│       ├── decision/                  # Создание ADR из архитектуры
│       ├── discussion/                # Управление дискуссиями
│       ├── discussion-review/         # Ревью решения дискуссии
│       ├── doc-claude/                # Обновление CLAUDE.md и llm_instructions.md
│       ├── doc-delete/                # Безопасное удаление документа
│       ├── doc-health/                # Проверка документации
│       ├── doc-health-deep/           # Глубокий аудит документации
│       ├── doc-project-structure/     # Генерация структуры проекта
│       ├── doc-review/                # Глубокое ревью документа
│       ├── feedback/                  # Отслеживание изменений по цепочке
│       ├── glossary-candidates/       # Поиск терминов для глоссария
│       ├── glossary-link/             # Добавление ссылок на глоссарий
│       ├── glossary-review/           # Интерактивная обработка кандидатов
│       ├── imp-plan/                  # Создание плана реализации
│       ├── resource/                  # Создание ресурса из ADR
│       ├── summary/                   # Обновление SUMMARY файлов
│       └── task-documentation/        # Документирование задач
│
├── .vscode/                           # Настройки VS Code
│   ├── settings.json                  # Настройки редактора
│   ├── extensions.json                # Рекомендуемые расширения
│   ├── tasks.json                     # Задачи автоматизации
│   └── launch.json                    # Конфигурация отладки
│
├── general_docs/                      # Общая документация
│   ├── glossary.md                    # Глоссарий терминов
│   ├── 01_discuss/                    # Дискуссии (идея → решение)
│   ├── 02_architecture/               # Архитектурные документы
│   ├── 03_diagrams/                   # Диаграммы (.drawio, Mermaid)
│   ├── 04_decisions/                  # Decision (ADR) — архитектурные решения
│   │   ├── 000_decisions.md           # Индекс решений
│   │   └── archive/                   # Устаревшие/отклонённые решения
│   ├── 05_resources/                  # Описания ресурсов
│   │   ├── api/                       # API документация
│   │   ├── backend/                   # Бэкенд ресурсы
│   │   ├── database/                  # Схемы БД
│   │   ├── frontend/                  # Фронтенд ресурсы
│   │   └── infra/                     # Инфраструктурные ресурсы
│   └── 06_imp_plans/                  # Планы реализации
│
├── llm_instructions/                  # Инструкции для LLM
│   ├── llm_instructions.md            # Индекс (этот файл)
│   ├── agents.md         # Инструкции для AI-агентов
│   ├── general_docs.md   # Правила ведения документации
│   ├── instructions_scripts.md        # Служебные скрипты
│   ├── skills.md         # Конфигурация скиллов
│   └── templates/                     # Шаблоны документов
│       ├── discuss.md
│       ├── architecture.md
│       ├── decision_adr.md
│       ├── imp_plan.md
│       ├── resource.md
│       ├── folder_doc.md
│       ├── 000_index.md
│       ├── general_docs_README.md
│       └── resources_README.md
│
├── llm_tasks/                         # Управление задачами LLM
│   ├── .task_counter                  # Счётчики ID для каждой категории
│   ├── current/                       # Текущие задачи (все исполнители)
│   │   ├── 0_task_index.md            # Индекс с группировкой
│   │   └── FEAT-00001.md              # Файлы задач
│   ├── future/                        # Бэклог задач
│   │   └── 0_task_index.md
│   ├── completed/                     # Архив завершённых задач
│   │   └── YYYY-MM/{assignee}/        # По месяцам и исполнителям
│   └── temp/                          # Временные файлы
│       └── amy-santiago/              # Временные файлы Amy
│
└── scripts/                           # Служебные скрипты
    ├── check_doc_health.py            # Комплексная проверка документации
    ├── check_gloss_health.py          # Проверка глоссария
    ├── check_doc_links.py             # [УСТАРЕЛ] Заменён на check_doc_health.py
    │
    ├── task_new.py                    # Создание задачи с автоинкрементом ID
    ├── task_complete.py               # Завершение задачи
    ├── task_move.py                   # Перемещение задачи между current/future
    │
    ├── discuss_new.py                 # Создание дискуссии
    ├── discuss_delete.py              # Удаление дискуссии
    │
    ├── architecture_new.py            # Создание архитектуры из дискуссии
    │
    ├── decision_new.py                # Создание ADR (DEC-XXX)
    ├── decision_delete.py             # Удаление ADR
    │
    ├── resource_new.py                # Создание ресурса (по типам)
    ├── resource_delete.py             # Удаление ресурса
    │
    ├── imp_plan_new.py                # Создание плана реализации
    └── imp_plan_delete.py             # Удаление плана
```
