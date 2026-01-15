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
- ✅ Создание нового документа (дискуссия, архитектура, план, ресурс)
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
- Поддерживает цепочку зависимостей (Дискуссия → Архитектура → Ресурсы → План)
- Запускает процесс обратной связи (feedback)
- Валидирует структуру, ссылки, метаданные

**Скиллы:**
- doc-health, doc-claude, doc-project-structure
- glossary-candidates, glossary-link, glossary-review

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
├── glossary.md             # Глоссарий терминов проекта
├── discuss/                # [📖 Дискуссии](general_docs/glossary.md#дискуссия) (идея → решение)
├── architecture/           # Архитектурные документы
├── diagrams/               # Диаграммы (.drawio, Mermaid)
├── imp_plans/              # [📖 Планы реализации](general_docs/glossary.md#план-реализации)
└── resources/              # Описания ресурсов
    ├── database/
    ├── backend/
    ├── frontend/
    └── infra/
```

### [📖 Цепочка зависимостей](general_docs/glossary.md#цепочка-зависимостей) документов

**Прямая:** [📖 Дискуссия](general_docs/glossary.md#дискуссия) → Архитектура → [📖 Ресурсы](general_docs/glossary.md#ресурс) → [📖 План реализации](general_docs/glossary.md#план-реализации) → [📖 Документация папок](general_docs/glossary.md#документация-папок)

**При изменениях:**
- Изменение архитектуры → обновить связанные дискуссии
- Изменение [📖 ресурса](general_docs/glossary.md#ресурс) → обновить архитектуру и [📖 документацию папок](general_docs/glossary.md#документация-папок)
- Изменение кода → обновить документацию папки, при существенных изменениях — ресурс

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
