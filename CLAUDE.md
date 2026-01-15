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

### Ключевые папки

- **`.claude/`** - конфигурация Claude Code (агенты, скиллы, настройки)
- **`llm_instructions/`** - инструкции для работы LLM с проектом
- **`llm_tasks/`** - управление задачами (текущие, бэклог, агенты)
- **`general_docs/`** - документация проекта (дискуссии, архитектура, планы)
- **`scripts/`** - служебные скрипты (проверки, автоматизация задач)
- **`templates/`** - шаблоны для создания документов

**Полная структура:** См. [llm_instructions.md](llm_instructions/llm_instructions.md)

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
2. **Проверить** индекс текущих задач [0_task_index.md](llm_tasks/current/0_task_index.md)
3. **Предложить** пользователю варианты:
   - Продолжить текущие задачи из `current/`
   - Начать новые задачи (создать через `task_new.py`)
   - Просмотреть бэклог ([0_task_index.md](llm_tasks/future/0_task_index.md))
   - Переместить задачи из `future/` в `current/`

**Запрещено:** Использовать временные файлы (PROJECT_IMPROVEMENTS.md и подобные) — только `llm_tasks/` с уникальными ID.

### Сохранение новых правил

При введении пользователем новых правил или инструкций для Claude — предложить:
1. Сохранить правила в `llm_instructions/` (новый файл или существующий)
2. Обновить [llm_instructions.md](llm_instructions/llm_instructions.md) — добавить в индекс
3. Обновить CLAUDE.md — добавить краткую информацию

---

## Быстрый старт LLM

1. **Контекст проекта:** Ознакомиться с [llm_instructions.md](llm_instructions/llm_instructions.md)
2. **Новая сессия:** **ОБЯЗАТЕЛЬНО** проверить индекс текущих задач [0_task_index.md](llm_tasks/current/0_task_index.md)
   - Если есть текущие задачи → предложить пользователю:
     - Продолжить работу над текущими задачами из `current/`
     - Работать с новыми задачами (создать через скрипты)
     - Просмотреть бэклог ([0_task_index.md](llm_tasks/future/0_task_index.md))
     - Переместить задачи из бэклога в текущие
3. **Задачи:** Следовать [tasks.md](llm_instructions/tasks.md) — полная документация системы с ID
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
- doc-health, doc-claude, doc-project-structure, doc-review
- glossary-candidates, glossary-link, glossary-review
- task-documentation (автоматическое документирование завершённых задач)

**Использование скиллов:**

Amy **автоматически** использует скиллы в правильной последовательности:

- **Аудит:** /doc-health → /doc-claude → /glossary-candidates → /glossary-link → /doc-review
- **Создание документа:** /glossary-candidates → /glossary-review → /glossary-link → /doc-health → /doc-review
- **Изменение структуры:** /doc-project-structure → /doc-claude → /doc-health

**Скилл doc-review (ревью документа):**

Также доступен напрямую (без агента) по команде `/doc-review` или по ключевым словам:
- "уделить внимание [документу]"
- "подумать над [документом]"
- "сделать ревью"
- "ультрасинк" / "ультрасинг"

Автоматически применяется при завершении работы над .md файлами в:
- `general_docs/`
- `.claude/agents/`, `.claude/skills/`
- `llm_instructions/`

**Подробнее:** См. [agents.md](llm_instructions/agents.md#amy-santiago-documentation-manager)

---

## Управление задачами

**ВАЖНО:** Все задачи проекта ведутся через `llm_tasks/` с уникальными ID, а не через временные файлы.

### Структура задач

```
llm_tasks/
├── .task_counter          # Счётчики ID для каждой категории
├── current/               # Текущие задачи (все исполнители)
│   ├── 0_task_index.md    # Индекс с группировкой по исполнителям
│   ├── FEAT-00001.md      # assignee: llm-main
│   └── AMY-00002.md       # assignee: amy-santiago
├── future/                # Бэклог задач (все исполнители)
│   ├── 0_task_index.md    # Индекс с группировкой по исполнителям
│   └── FIX-00004.md
├── completed/             # Архив завершённых задач
│   └── YYYY-MM/           # Месяц завершения
│       └── {assignee}/    # Исполнитель
│           └── 0_task_index.md
└── temp/                  # Временные файлы агентов
```

### Формат ID задач

Задачи имеют уникальные ID формата: `CATEGORY-NNNNN`

**Категории:**
- `FEAT-00001` — новая функциональность
- `FIX-00001` — исправление бага
- `REFACTOR-00001` — рефакторинг кода
- `DOCS-00001` — документация
- `TEST-00001` — тесты
- `INFRA-00001` — инфраструктура
- `ID-00001` — общие задачи (без категории)
- `AMY-00001` — задачи для Amy Santiago

**Счётчики:** Каждая категория имеет отдельный счётчик в `.task_counter`

### Работа с задачами через скрипты

```bash
# Создание новых задач
python scripts/task_new.py -i                    # Интерактивно
python scripts/task_new.py -t "Название" -c feat # С параметрами

# Завершение задачи (автоматически вызывает Amy Santiago)
python scripts/task_complete.py FEAT-00001

# Перемещение между current и future
python scripts/task_move.py FEAT-00001 current   # future → current
python scripts/task_move.py FEAT-00002 future    # current → future
```

### Makefile команды

```bash
# Создание задач
make task-new              # Интерактивное создание
make task-new-feat TITLE="..." PRIORITY="high"
make task-new-fix TITLE="..." PRIORITY="medium"

# Управление задачами
make task-complete ID=FEAT-00001
make task-move-current ID=FEAT-00001
make task-move-future ID=FEAT-00001

# Просмотр
make tasks-current         # Показать текущие задачи
make tasks-future          # Показать бэклог
make tasks-completed       # Показать архив
```

### Автоматическое документирование

При завершении задачи (`task_complete.py`) автоматически вызывается **Amy Santiago** со скиллом `task-documentation` для обновления связанной документации:

- Обновляет дискуссии (добавляет ссылку на задачу)
- Обновляет архитектуру (добавляет в историю изменений)
- Обновляет планы реализации (отмечает выполненные подзадачи)
- Обновляет индексы документации (000_*_index.md в general_docs/)
- **Обновляет индекс завершённых задач** `completed/YYYY-MM/{assignee}/0_task_index.md`

**Колонка "Документация обновлена":**
- `Success: [Doc1](путь), [Doc2](путь)` — все связанные документы обновлены
- `Need` — требуется обновление (Amy не смогла автоматически обновить)
- `N/A` — нет связанных документов

**Индексы с группировкой:**

Current/future индексы (`0_task_index.md`) группируются по исполнителям:
- Навигация: [LLM-main](#llm-main) | [Amy Santiago](#amy-santiago) | [Другие](#другие)
- Секции с таблицами задач для каждого исполнителя
- Единая точка входа для всех задач

**Подробнее:** См. [tasks.md](llm_instructions/tasks.md) — полная документация системы управления задачами

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

# Запуск отдельного теста (пример для сервиса auth):
cd services/auth && npm test -- --grep "test name"
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
# Создание задач в текущие (current/)
make task-new              # Интерактивно
make task-new-feat TITLE="..." PRIORITY="high"    # FEAT задача
make task-new-fix TITLE="..." PRIORITY="medium"   # FIX задача
make task-new-docs TITLE="..." PRIORITY="low"     # DOCS задача

# Создание задач в бэклог (future/)
make backlog-new           # Интерактивно
make backlog-new-feat TITLE="..." PRIORITY="medium"
make backlog-new-fix TITLE="..." PRIORITY="low"
make backlog-new-docs TITLE="..." PRIORITY="low"

# Управление задачами
make task-complete ID=FEAT-00001           # Завершить задачу (вызывает Amy)
make task-move-current ID=FEAT-00001       # Переместить из future в current
make task-move-future ID=FEAT-00001        # Переместить из current в future

# Просмотр индексов
make tasks-current         # Показать текущие задачи
make tasks-future          # Показать бэклог
make tasks-completed       # Показать архив (последний месяц)

# Альтернатива: Python скрипты напрямую
python scripts/task_new.py -i                        # Интерактивно
python scripts/task_new.py -t "Название" -c feat -f future  # В бэклог
python scripts/task_complete.py FEAT-00001
python scripts/task_move.py FEAT-00001 current
```

**Примеры:**
```bash
# Создание текущей задачи
make task-new
make task-new-feat TITLE="Добавить OAuth" PRIORITY="high"

# Создание задачи в бэклог
make backlog-new
make backlog-new-feat TITLE="Будущая фича" PRIORITY="medium"

# Перенос из бэклога в текущие
make task-move-current ID=FEAT-00100

# Завершение задачи (автоматически документируется Amy)
make task-complete ID=FEAT-00001
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
