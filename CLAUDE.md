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
- **`llm_instructions/templates/`** - шаблоны для создания документов

**Полная структура:** См. [llm_instructions.md](llm_instructions/llm_instructions.md)

---

## Правила для Claude

Нужно продолжить работу с документом refactoring.md

### Структура инструкций

| Файл | Назначение |
|------|------------|
| **CLAUDE.md** | Быстрый справочник (этот файл) |
| [llm_instructions.md](llm_instructions/llm_instructions.md) | Полный индекс инструкций и структура проекта |

**Важно:** CLAUDE.md содержит краткую информацию для быстрого старта. Для полного понимания контекста проекта — см. [llm_instructions.md](llm_instructions/llm_instructions.md).

### Синхронизация инструкций

При изменении любого файла в `llm_instructions/` — обновить CLAUDE.md релевантной информацией.

**Автоматизация:** Используй скилл `/doc-claude` для автоматического обновления CLAUDE.md и llm_instructions.md при важных изменениях.

### Сохранение новых правил

При введении пользователем новых правил или инструкций для Claude — предложить:
1. Сохранить правила в `llm_instructions/` (новый файл или существующий)
2. Обновить [llm_instructions.md](llm_instructions/llm_instructions.md) — добавить в индекс
3. Обновить CLAUDE.md — добавить краткую информацию

---

## Быстрый старт LLM

1. **Контекст:** Ознакомиться с [llm_instructions.md](llm_instructions/llm_instructions.md)
2. **Задачи:** Проверить [текущие задачи](llm_tasks/current/0_task_index.md), предложить: продолжить / создать новые / [бэклог](llm_tasks/future/0_task_index.md)
3. **Документация:** Следовать [general_docs.md](llm_instructions/general_docs.md)
4. **Термины:** Проверять/добавлять в [glossary.md](general_docs/glossary.md)

---

## Инструкции для LLM

| Инструкция | Назначение |
|------------|------------|
| [general_docs.md](llm_instructions/general_docs.md) | Правила ведения документации (дискуссии, архитектура, планы, README.md) |
| [tasks.md](llm_instructions/tasks.md) | **Управление задачами через llm_tasks/** |
| [scripts.md](llm_instructions/scripts.md) | Служебные скрипты (check_doc_health.py, check_gloss_health.py) |
| [agents.md](llm_instructions/agents.md) | AI-[📖 агенты](general_docs/glossary.md#агент) Claude Code |
| [skills.md](llm_instructions/skills.md) | [📖 Скиллы](general_docs/glossary.md#скилл) Claude Code |
| [workflow_test_doc.md](llm_instructions/workflow_test_doc.md) | Тест workflow документации (полный цикл) |

---

## Документация

Проект использует структурированную систему документации в `general_docs/`.

**Подробнее:** См. [general_docs.md](llm_instructions/general_docs.md) — полные правила ведения документации.

### Ключевые принципы

- **`000_*.md`** — индексы (ЧТО есть в папке, автообновляемые)
- **`README.md`** — правила (КАК работать с документами)
- **[📖 IT-сервис](general_docs/glossary.md#it-сервис)** — бизнес-сущность в `00_services/`, стоит НАД цепочкой зависимостей
- **[📖 Цепочка зависимостей](general_docs/glossary.md#цепочка-зависимостей):** Дискуссия → Архитектура → Decision (ADR) → Ресурсы → План → Документация папок

### IT-сервисы

**Папка:** `general_docs/00_services/`

IT-сервис объединяет все документы, относящиеся к одной бизнес-функции:

```
00_services/notification-service/  ← Бизнес-ценность
        ↓
01_discuss/ → 02_architecture/ → 04_decisions/ → 05_resources/ → 06_imp_plans/
                                                        ↓
                                            backend/notification-service/
                                            database/notification-service/
```

**Создание:** Автоматически через `/summary-doc` при одобрении дискуссии

### Глоссарий

Все термины проекта — в [glossary.md](general_docs/glossary.md).

**Формат ссылок:** `[📖 Термин](путь/к/glossary.md#термин)`

**Правило:** При встрече незнакомого термина — проверить глоссарий перед продолжением работы.

### Диаграммы

**Формат:** Mermaid (текстовый, в Markdown)

**Папка:** `general_docs/03_diagrams/`

**Просмотр:** GitHub/GitLab рендерит автоматически, VS Code — расширение "Markdown Preview Mermaid Support"

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
- discussion-review, architect-review (ревью дискуссий и архитектуры)
- doc-health, doc-claude, doc-project-structure, doc-review
- glossary-candidates, glossary-link, glossary-review
- summary-doc, summary-arch (обновление SUMMARY файлов)
- task-documentation (автоматическое документирование завершённых задач)

**Использование скиллов:**

Amy **автоматически** использует скиллы в правильной последовательности:

- **Создание документа:** /doc-review → /doc-health → /doc-claude → /glossary-candidates → /glossary-review → /glossary-link
- **Аудит:** /doc-review → /doc-health → /doc-claude → /glossary-candidates → /glossary-link
- **Изменение структуры:** /doc-project-structure → /doc-health → /doc-claude

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

## Скиллы Claude Code

Список скиллов: [skills.md](llm_instructions/skills.md#скиллы-проекта)

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

### Запуск отдельного теста

```bash
# Пример для сервиса auth:
cd services/auth && npm test -- --grep "test name"
```

### Разработка и отладка

```bash
make restart           # Перезапуск всех сервисов
make logs-web          # Логи фронтенда
make logs-auth         # Логи auth сервиса
make db-migrate        # Запустить миграции
make db-reset          # Сбросить и пересоздать БД
```

### Shell-доступ к контейнерам

```bash
make shell-web         # Shell в web контейнере
make shell-auth        # Shell в auth контейнере
make shell-users       # Shell в users контейнере
make shell-db          # psql в PostgreSQL
make shell-redis       # redis-cli
```

### Утилиты

```bash
make ps                # Показать запущенные контейнеры
make clean             # Очистить node_modules, dist, build
make clean-all         # Полная очистка (+ Docker volumes)
```

### Проверка документации

```bash
make docs-health       # Проверка документации (ссылки, структура, статусы)
make gloss-health      # Проверка глоссария
make docs-check        # Полная проверка (документация + глоссарий)
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
Web UI (apps/web)
    ↓
API Gateway (services/api-gateway)
    ↓
    ├─→ Auth Service → PostgreSQL (auth_db)
    └─→ Users Service → PostgreSQL (users_db)
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
