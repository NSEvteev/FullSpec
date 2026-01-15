# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Язык проекта

Используй русский язык для всех коммуникаций и комментариев в коде.

## Обзор проекта

Универсальный шаблон fullstack проекта с микросервисной архитектурой, настроенной системой документации и интеграцией Claude Code.

### Архитектура

**Клиентские приложения (`apps/`):**
- Web UI — веб-фронтенд

**Бэкенд сервисы (`services/`):**
- API Gateway — единая точка входа
- Auth Service — аутентификация и авторизация
- Users Service — управление пользователями

**Общий код (`packages/`):**
- shared, ui, validation, config

**Инфраструктура:**
- Docker Compose для разработки
- Makefile для автоматизации

### Структура проекта

```
project_template/
├── .claude/                      # Конфигурация Claude Code
│   ├── agents/                   # Определения агентов
│   │   └── amy-santiago.md       # Amy Santiago - Documentation Manager
│   ├── skills/                   # Пользовательские скиллы
│   │   ├── commit-push.md
│   │   ├── doc-*.md              # Скиллы документации
│   │   └── glossary-*.md         # Скиллы глоссария
│   └── settings.local.json       # Локальные настройки Claude
│
├── apps/                         # Клиентские приложения
│   └── web/                      # Web UI (фронтенд)
│
├── services/                     # Бэкенд микросервисы
│   ├── api-gateway/              # API Gateway - точка входа
│   ├── auth/                     # Auth Service - аутентификация
│   └── users/                    # Users Service - управление пользователями
│
├── packages/                     # Общий код (монорепозиторий)
│   ├── shared/                   # Общие утилиты и типы
│   ├── ui/                       # UI компоненты
│   ├── validation/               # Схемы валидации
│   └── config/                   # Общая конфигурация
│
├── general_docs/                 # Документация проекта
│   ├── glossary.md               # Глоссарий терминов
│   ├── 01_discuss/               # Дискуссии (идеи → решения)
│   ├── 02_architecture/          # Архитектурные документы
│   ├── 03_diagrams/              # Диаграммы (.drawio, Mermaid)
│   ├── 04_decisions/             # Decision Records (ADR)
│   ├── 05_resources/             # Описания ресурсов
│   │   ├── database/             # Схемы БД
│   │   ├── backend/              # Бэкенд ресурсы
│   │   ├── frontend/             # Фронтенд ресурсы
│   │   └── infra/                # Инфраструктура
│   └── 06_imp_plans/             # Планы реализации
│
├── llm_instructions/             # Инструкции для LLM
│   ├── llm_instructions.md       # Индекс всех инструкций
│   ├── general_docs.md           # Правила ведения документации
│   ├── tasks.md                  # Управление задачами
│   ├── scripts.md                # Служебные скрипты
│   ├── agents.md                 # Описание агентов Claude Code
│   └── skills.md                 # Описание скиллов Claude Code
│
├── llm_tasks/                    # Задачи для LLM
│   ├── current_tasks.md          # Текущие задачи основного LLM
│   ├── future_tasks.md           # Бэклог задач
│   └── agents/                   # Задачи агентов
│       └── amy-santiago/         # Задачи Amy Santiago
│           ├── current_tasks.md  # Текущие задачи агента
│           ├── future_tasks.md   # Бэклог агента
│           ├── completed_tasks.md # Архив завершённых задач
│           └── temp/             # Временные файлы (отчёты, логи)
│
├── scripts/                      # Служебные скрипты
│   ├── check_doc_health.py       # Проверка здоровья документации
│   ├── check_gloss_health.py     # Проверка глоссария
│   ├── task_add.py               # Добавление задачи в current_tasks.md
│   └── backlog_add.py            # Добавление задачи в бэклог
│
├── templates/                    # Шаблоны документов
│   ├── discussion.md             # Шаблон дискуссии
│   ├── architecture.md           # Шаблон архитектуры
│   ├── decision.md               # Шаблон ADR
│   ├── resource.md               # Шаблон ресурса
│   └── plan.md                   # Шаблон плана реализации
│
├── config/                       # Конфигурация проекта
│   └── examples/                 # Примеры .env файлов
│
├── CLAUDE.md                     # Инструкции для Claude Code (этот файл)
├── README.md                     # Главная документация проекта
├── Makefile                      # Команды автоматизации
├── docker-compose.yml            # Docker конфигурация
└── .env.example                  # Пример переменных окружения
```

**Ключевые папки:**
- **`.claude/`** - конфигурация Claude Code (агенты, скиллы, настройки)
- **`llm_instructions/`** - инструкции для работы LLM с проектом
- **`llm_tasks/`** - управление задачами (текущие, бэклог, агенты)
- **`general_docs/`** - документация проекта (дискуссии, архитектура, планы)
- **`scripts/`** - служебные скрипты (проверки, автоматизация задач)
- **`templates/`** - шаблоны для создания документов

---

## Правила для Claude

### Структура инструкций

| Файл | Назначение |
|------|------------|
| **CLAUDE.md** | Быстрый справочник (этот файл) |
| [llm_instructions.md](llm_instructions/llm_instructions.md) | Полный индекс инструкций и структура проекта |

**Важно:** CLAUDE.md содержит краткую информацию для быстрого старта. Для полного понимания контекста проекта — см. [llm_instructions.md](llm_instructions/llm_instructions.md).

### Синхронизация инструкций

При изменении любого файла в `llm_instructions/` — обновить CLAUDE.md релевантной информацией.

**Автоматизация:** Используй скилл `/doc-claude` для автоматического обновления CLAUDE.md и llm_instructions.md при важных изменениях.

### Управление задачами (обязательно!)

**КРИТИЧЕСКИ ВАЖНО:** При каждой новой сессии:

1. **Прочитать** [tasks.md](llm_instructions/tasks.md) — полные правила работы с задачами
2. **Проверить** [current_tasks.md](llm_tasks/current_tasks.md) — текущие задачи сессии
3. **Предложить** пользователю варианты:
   - Продолжить текущие задачи
   - Начать новые задачи
   - Просмотреть бэклог ([future_tasks.md](llm_tasks/future_tasks.md))

**Запрещено:** Использовать временные файлы (PROJECT_IMPROVEMENTS.md и подобные) — только `llm_tasks/`.

### Сохранение новых правил

При введении пользователем новых правил или инструкций для Claude — предложить:
1. Сохранить правила в `llm_instructions/` (новый файл или существующий)
2. Обновить [llm_instructions.md](llm_instructions/llm_instructions.md) — добавить в индекс
3. Обновить CLAUDE.md — добавить краткую информацию

---

## Быстрый старт LLM

1. **Контекст проекта:** Ознакомиться с [llm_instructions.md](llm_instructions/llm_instructions.md)
2. **Новая сессия:** **ОБЯЗАТЕЛЬНО** проверить [current_tasks.md](llm_tasks/current_tasks.md)
   - Если есть текущие задачи → предложить пользователю:
     - Продолжить работу над текущими задачами
     - Работать с новыми задачами
     - Посмотреть бэклог ([future_tasks.md](llm_tasks/future_tasks.md))
3. **Задачи:** Следовать [tasks.md](llm_instructions/tasks.md)
4. **Документация:** Следовать [general_docs.md](llm_instructions/general_docs.md)
5. **Термины:** Добавлять в [glossary.md](general_docs/glossary.md)
6. **Скрипты:** См. [scripts.md](llm_instructions/scripts.md)

---

## Инструкции для LLM

| Инструкция | Назначение |
|------------|------------|
| [general_docs.md](llm_instructions/general_docs.md) | Правила ведения документации (дискуссии, архитектура, планы, README.md) |
| [tasks.md](llm_instructions/tasks.md) | **Управление задачами через llm_tasks/** |
| [scripts.md](llm_instructions/scripts.md) | Служебные скрипты (check_doc_health.py, check_gloss_health.py) |
| [agents.md](llm_instructions/agents.md) | AI-[📖 агенты](general_docs/glossary.md#агент) Claude Code |
| [skills.md](llm_instructions/skills.md) | [📖 Скиллы](general_docs/glossary.md#скилл) Claude Code |

---

## Агенты Claude Code

**Amy Santiago (Documentation Manager)** — специализированный агент для управления документацией.

**Когда использовать:**
- ✅ Создание нового документа (дискуссия, архитектура, decision (ADR), план, ресурс)
- ✅ Изменение документа, влияющее на другие
- ✅ Проверка документации на соответствие стандартам
- ✅ Массовое обновление индексов (000_*.md)

**Вызов агента:**
```
Используй агента amy-santiago для создания дискуссии об аутентификации
```

**Возможности:**
- Создаёт документы по шаблонам с правильными метаданными
- Автоматически обновляет индексы (000_*.md)
- Поддерживает цепочку зависимостей (Дискуссия → Архитектура → Decision (ADR) → Ресурсы → План)
- Запускает процесс обратной связи (feedback)
- Валидирует структуру, ссылки, метаданные

**Скиллы:**
- doc-health, doc-claude, doc-project-structure
- glossary-candidates, glossary-link, glossary-review

**Использование скиллов:**

Amy **автоматически** использует скиллы в правильной последовательности:

- **Аудит:** /doc-health → /doc-claude → /glossary-candidates → /glossary-link
- **Создание документа:** /glossary-candidates → /glossary-review → /glossary-link → /doc-health
- **Изменение структуры:** /doc-project-structure → /doc-claude → /doc-health

**Подробнее:** См. [agents.md](llm_instructions/agents.md#amy-santiago-documentation-manager)

---

## Управление задачами

**ВАЖНО:** Все задачи проекта ведутся через `llm_tasks/`, а не через временные файлы.

### Основной LLM

| Файл | Назначение |
|------|------------|
| [current_tasks.md](llm_tasks/current_tasks.md) | Текущие задачи сессии (проверять при каждом запуске!) |
| [future_tasks.md](llm_tasks/future_tasks.md) | [📖 Бэклог](general_docs/glossary.md#бэклог) задач |
| [tasks.md](llm_instructions/tasks.md) | Правила работы с задачами |

### Агенты

Каждый агент имеет собственную папку задач в `llm_tasks/agents/[имя-агента]/`:

```
llm_tasks/agents/amy-santiago/
├── current_tasks.md      # Текущие задачи
├── future_tasks.md       # Бэклог
├── completed_tasks.md    # Архив завершённых задач
└── temp/                 # Временные файлы
```

| Файл | Назначение |
|------|------------|
| [current_tasks.md](llm_tasks/agents/amy-santiago/current_tasks.md) | Текущие задачи Amy (с секцией "Что было сделано") |
| [future_tasks.md](llm_tasks/agents/amy-santiago/future_tasks.md) | Бэклог задач Amy |
| [completed_tasks.md](llm_tasks/agents/amy-santiago/completed_tasks.md) | Архив завершённых задач (обратная хронология) |
| temp/ | Временные файлы (отчёты, логи, промежуточные результаты) |

**Правила для агентов:**
1. При запуске — показать "Что было сделано в прошлый раз"
2. При начале новой задачи — очистить `temp/`
3. Во время работы — сохранять временные файлы в `temp/`
4. При завершении — переместить задачу в `completed_tasks.md` (вверх файла)

### Правила работы с задачами

1. **Начало сессии:** Обязательно прочитать `current_tasks.md`
2. **Планирование:** Переносить задачи из `future_tasks.md` в `current_tasks.md`
3. **Выполнение:** Обновлять статусы подзадач в реальном времени
4. **Завершение:** Синхронизировать `current_tasks.md` с выполненной работой

---

## Команды

### Основные команды Makefile

```bash
make help              # Показать все доступные команды
make init              # Инициализация проекта (первый запуск)
make dev               # Запустить все сервисы для разработки
make stop              # Остановить все сервисы
make logs              # Показать логи всех сервисов
make test              # Запустить все тесты
make build             # Собрать для production
```

### Запуск и остановка

```bash
make dev               # Запуск: Web (3000), API Gateway (8000), Auth (8001), Users (8002)
make stop              # Остановка всех сервисов
make restart           # Перезапуск
```

### Разработка

```bash
make logs-web          # Логи фронтенда
make logs-auth         # Логи auth сервиса
make logs-users        # Логи users сервиса
make shell-web         # Открыть shell в web контейнере
make shell-db          # Открыть psql в PostgreSQL
```

### База данных

```bash
make db-migrate        # Запустить миграции
make db-seed           # Заполнить тестовыми данными
make db-reset          # Сбросить и пересоздать БД
```

### Проверка документации

```bash
make docs-health       # Полная проверка документации (ссылки, структура, статусы)
make docs-links        # Только проверка ссылок
make gloss-health      # Проверка глоссария
make docs-check        # Документация + глоссарий
```

### Управление задачами

```bash
# Добавление задач (интерактивно)
make task-add          # Добавить задачу в current_tasks.md
make backlog-add       # Добавить задачу в бэклог (future_tasks.md)

# Добавление задач (через параметры)
make task TITLE="Название задачи" PRIORITY="средний"
make backlog TITLE="Название" PRIORITY="P2" CATEGORY="docs"

# Просмотр задач
make tasks-view        # Просмотреть текущие задачи
make backlog-view      # Просмотреть бэклог

# Альтернатива: Python скрипты напрямую
python scripts/task_add.py -i
python scripts/backlog_add.py -i
```

**Примеры:**
```bash
# Интерактивный режим (рекомендуется)
make task-add

# Быстрое добавление
make task TITLE="Исправить баг в auth" PRIORITY="высокий"
make backlog TITLE="Добавить тесты" PRIORITY="P2" CATEGORY="feat"
```

## Переменные окружения (.env)

### Файлы конфигураций

- **`.env.example`** — базовый шаблон в корне
- **`config/examples/`** — примеры для разных окружений:
  - `.env.development.example` — для разработки
  - `.env.production.example` — для продакшена
  - `.env.test.example` — для тестов

### Инициализация

```bash
# Автоматическая инициализация
make init

# Или вручную
cp .env.example .env
cp apps/web/.env.example apps/web/.env
cp services/auth/.env.example services/auth/.env
cp services/users/.env.example services/users/.env
```

## Архитектура сервисов

### Взаимодействие компонентов

```
Client (Browser)
    ↓
Web UI (apps/web) :3000
    ↓
API Gateway (services/api-gateway) :8000
    ↓
    ├─→ Auth Service :8001 → PostgreSQL (auth_db)
    └─→ Users Service :8002 → PostgreSQL (users_db)
           ↓
        Redis (кэш, сессии)
```

### Ответственность сервисов

**Auth Service:**
- Регистрация/логин
- JWT токены
- OAuth интеграция
- Восстановление пароля

**Users Service:**
- Профили пользователей
- Роли и права (RBAC)
- Загрузка аватаров
- История активности

**API Gateway:**
- Маршрутизация запросов
- Rate limiting
- Валидация JWT
- CORS обработка

---

## Документация

Проект использует структурированную систему документации.

### Структура документации

```
general_docs/
├── README.md                    # Обзор системы документации (для разработчиков)
├── glossary.md                  # Глоссарий терминов (14 терминов, 3 категории)
│
├── 01_discuss/                  # Дискуссии (идеи → решения)
│   ├── 000_discuss.md           # ЧТО: Индекс всех дискуссий (автообновляемый)
│   └── README.md                # КАК: Правила создания дискуссий
│
├── 02_architecture/             # Архитектурные документы
│   ├── 000_architecture.md      # ЧТО: Индекс архитектуры (автообновляемый)
│   └── README.md                # КАК: Правила работы с архитектурой
│
├── 03_diagrams/                 # Диаграммы (.drawio, Mermaid)
│   ├── 000_diagrams.md          # ЧТО: Индекс диаграмм
│   └── README.md                # КАК: Правила создания диаграмм
│
├── 04_decisions/                # Decision Records (ADR)
│   ├── 000_decisions.md         # ЧТО: Индекс решений (автообновляемый)
│   ├── README.md                # КАК: Правила фиксации решений
│   └── archive/                 # Устаревшие решения
│
├── 05_resources/                # Описания ресурсов
│   ├── 000_resources.md         # ЧТО: Индекс всех ресурсов
│   ├── database/                # Схемы БД и миграции
│   │   ├── 000_database.md      # Индекс БД ресурсов
│   │   └── README.md            # Правила работы с БД
│   ├── backend/                 # Backend ресурсы (API, сервисы)
│   │   ├── 000_backend.md
│   │   └── README.md
│   ├── frontend/                # Frontend ресурсы (UI, компоненты)
│   │   ├── 000_frontend.md
│   │   └── README.md
│   └── infra/                   # Инфраструктура (Docker, CI/CD)
│       ├── 000_infra.md
│       └── README.md
│
└── 06_imp_plans/                # Планы реализации
    ├── 000_imp_plans.md         # ЧТО: Индекс планов (автообновляемый)
    └── README.md                # КАК: Правила создания планов
```

**Ключевые принципы:**

**Разделение ЧТО vs КАК:**
- `000_*.md` — **ЧТО** есть в папке (динамический индекс, автообновляемый)
- `README.md` — **КАК** работать с документами (статичные правила)

**Категории глоссария:**
- Документация (9 терминов) — дискуссия, архитектура, план, ресурс, etc.
- Claude Code (3 термина) — агент, скилл, команда
- Управление задачами (2 термина) — бэклог, LLM-сессия

### [📖 Цепочка зависимостей](general_docs/glossary.md#цепочка-зависимостей) документов

**Прямая:** [📖 Дискуссия](general_docs/glossary.md#дискуссия) → Архитектура → [📖 Decision (ADR)](general_docs/glossary.md#decision-adr) → [📖 Ресурсы](general_docs/glossary.md#ресурс) → [📖 План реализации](general_docs/glossary.md#план-реализации) → [📖 Документация папок](general_docs/glossary.md#документация-папок)

**При изменениях:**
- Изменение [📖 Decision (ADR)](general_docs/glossary.md#decision-adr) → обновить связанные дискуссии и архитектуру
- Изменение [📖 ресурса](general_docs/glossary.md#ресурс) → обновить Decision (ADR) и [📖 документацию папок](general_docs/glossary.md#документация-папок)
- Изменение кода → обновить документацию папки, при существенных изменениях — ресурс и Decision (ADR)

### [📖 Документация папок](general_docs/glossary.md#документация-папок)

Размещается в корне значимых папок как `README.md` (например: `services/auth/README.md`, `packages/shared/README.md`).

### Глоссарий

Все новые термины добавлять в [glossary.md](general_docs/glossary.md).
**Формат ссылок на глоссарий:** `[📖 Термин](путь/к/glossary.md#термин)`

Эмодзи `📖` визуально отличает ссылки на глоссарий от обычных ссылок.
**Правило для LLM:** При встрече незнакомого термина из проекта — проверить [glossary.md](general_docs/glossary.md). Если термин есть в глоссарии, ознакомиться с его определением перед продолжением работы.

---

## MCP серверы

<!-- TODO: Добавить MCP серверы при необходимости -->
