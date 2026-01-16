---
name: resource
description: Создание ресурса (database, backend, frontend, infra) из одобренного ADR. Ресурсы описывают конкретные технические компоненты системы.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
---

# Управление ресурсами

Скилл для создания ресурсов на основе одобренных ADR (Architecture Decision Records).

## ВАЖНОЕ ПРАВИЛО

**При ЛЮБЫХ действиях с ресурсами — сначала прочитать этот скилл!**

Это включает:
- Создание нового ресурса
- Изменение существующего ресурса
- Работу с индексами в подпапках `05_resources/`

**Почему:** Скрипты автоматически обновляют счётчики и индексы. Ручные операции ломают синхронизацию.

---

## Типы ресурсов

| Тип | Папка | Описание | Область |
|-----|-------|----------|---------|
| `database` | `05_resources/database/` | Схемы БД, индексы, миграции | Database |
| `backend` | `05_resources/backend/` | API, сервисы, бизнес-логика | Backend/API |
| `frontend` | `05_resources/frontend/` | Компоненты, состояние, маршруты | UI/Frontend |
| `infra` | `05_resources/infra/` | Docker, K8s, CI/CD, мониторинг | Infrastructure |

---

## Когда использовать

**Триггеры:**
- Команда `/resource`
- После одобрения ADR (`🟢 approved`)
- Запрос "создать ресурс" или "описать компонент"

**Контекст:**
- ADR находится в статусе `🟢 approved`
- Известно, какие ресурсы нужно создать

---

## Workflow в цепочке зависимостей

```
ADR (approved)
      ↓
/resource (этот скилл!) + /imp-plan
      ↓
Ресурсы (05_resources/) + План (06_imp_plans/)
```

**Ресурсы создаются из ADR, а НЕ из архитектуры напрямую!**

---

## Инструкции

### Шаг 1: Проверить ADR

1. Прочитать ADR и убедиться:
   - Статус `🟢 approved`
   - Секция "Последствия" заполнена (что нужно реализовать)

**Если статус не approved:**
```
ADR должен быть в статусе approved для создания ресурсов.
Текущий статус: [статус]
```

### Шаг 2: Определить необходимые ресурсы

Из секции "Последствия" ADR определить:
- Какие компоненты нужно создать
- Какого типа каждый компонент (database/backend/frontend/infra)

**Спросить пользователя если неясно:**
```
ADR предполагает создание следующих компонентов:
1. [Компонент 1] — какой тип? (database/backend/frontend/infra)
2. [Компонент 2] — какой тип?

Какие ресурсы создать?
```

### Шаг 3: Создать ресурсы через скрипт

**ОБЯЗАТЕЛЬНО использовать скрипт:**

```bash
python scripts/resource_new.py -n "Название" -t backend -a "DEC-001"
```

**Параметры:**
- `-n` — название ресурса
- `-t` — тип (database/backend/frontend/infra)
- `-a` — ID связанного ADR (например: DEC-001)
- `--desc` — краткое описание

**Скрипт автоматически:**
- Генерирует ID (001, 002, ...)
- Создаёт файл в правильной подпапке
- Обновляет индекс `000_{type}.md`
- Обновляет счётчик `.doc_counter`

**ЗАПРЕЩЕНО:** Создавать файлы вручную через Write tool!

### Шаг 4: Заполнить ресурс

После создания файла заполнить секции по типу:

#### Для database:
- Схема данных (таблицы, связи)
- Индексы
- Миграции

#### Для backend:
- API Endpoints
- Бизнес-логика
- Конфигурация

#### Для frontend:
- Компоненты
- Состояние
- Маршруты

#### Для infra:
- Сервисы
- Мониторинг
- Масштабирование

### Шаг 5: Обновить ADR

После создания ресурсов:

1. Обновить секцию "Связанные документы" в ADR:
   ```markdown
   **Связанные документы:**
   - **Архитектура:** [001_*.md](../02_architecture/001_*.md)
   - **Ресурсы:** [001_*.md](../05_resources/backend/001_*.md) ← ДОБАВИТЬ
   - **План реализации:** [создаётся из этого ADR]
   ```

### Шаг 6: Предложить следующий шаг

```
Ресурсы созданы:
- [001] backend/users_api.md
- [002] database/users_schema.md

Следующий шаг: /imp-plan — создать план реализации
```

---

## Команды

### Скрипты

```bash
# Создать ресурс
python scripts/resource_new.py -n "Название" -t backend -a "DEC-001"
python scripts/resource_new.py -i  # интерактивно

# Удалить ресурс
python scripts/resource_delete.py 001 -t backend
python scripts/resource_delete.py 001 -t backend --force
```

### Makefile

```bash
make resource-new                              # интерактивно
make resource-new-backend NAME="Users API" ADR="DEC-001"
make resource-new-frontend NAME="Auth Form" ADR="DEC-001"
make resource-new-database NAME="Users Schema" ADR="DEC-001"
make resource-new-infra NAME="Redis Cache" ADR="DEC-001"
make resource-index                            # показать индекс
make resource-delete ID="001" TYPE="backend"   # удалить
```

---

## Пример использования

**ADR:** DEC-001_auth_jwt.md (статус: approved)

**Последствия из ADR:**
- Нужна таблица users в БД
- Нужен Auth API сервис
- Нужна форма логина на фронте

**Шаг 1:** Создать ресурсы
```bash
python scripts/resource_new.py -n "Users Schema" -t database -a "DEC-001"
python scripts/resource_new.py -n "Auth API" -t backend -a "DEC-001"
python scripts/resource_new.py -n "Login Form" -t frontend -a "DEC-001"
```

**Шаг 2:** Заполнить каждый ресурс

**database/001_users_schema.md:**
```markdown
## Схема данных

| Таблица | Описание | Связи |
|---------|----------|-------|
| users | Пользователи | — |
| sessions | Сессии | FK → users |

## Индексы

| Таблица | Индекс | Поля | Тип |
|---------|--------|------|-----|
| users | idx_email | email | UNIQUE |
```

**backend/002_auth_api.md:**
```markdown
## API Endpoints

| Endpoint | Метод | Описание | Авторизация |
|----------|-------|----------|-------------|
| /api/v1/auth/login | POST | Логин | — |
| /api/v1/auth/refresh | POST | Обновить токен | required |
| /api/v1/auth/logout | POST | Выход | required |
```

**frontend/003_login_form.md:**
```markdown
## Компоненты

| Компонент | Props | Описание |
|-----------|-------|----------|
| LoginForm | onSuccess, onError | Форма логина |
| AuthProvider | children | Контекст авторизации |
```

---

## Связанная документация

| Документ | Назначение |
|----------|------------|
| [general_docs.md](../../../llm_instructions/general_docs.md#ресурсы-resources) | Правила ведения ресурсов |
| [templates/resource.md](../../../llm_instructions/templates/resource.md) | Шаблон ресурса |
| [000_resources.md](../../../general_docs/05_resources/000_resources.md) | Индекс ресурсов |

## Связанные файлы

- `scripts/resource_new.py` — скрипт создания
- `scripts/resource_delete.py` — скрипт удаления
- `general_docs/05_resources/*/000_*.md` — индексы по типам
- `general_docs/.doc_counter` — счётчик ID

## Связанные скиллы

- `/decision` — создание ADR (предыдущий этап)
- `/imp-plan` — создание плана реализации (параллельный этап)
- `/doc-review` — ревью документа
