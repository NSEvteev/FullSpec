---
name: resource
description: Создание ресурса (database, backend, frontend, infra) из одобренного ADR. Ресурсы организованы по IT-сервисам и описывают конкретные технические компоненты системы.
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

## Ключевая концепция: Структура по сервисам

```
05_resources/
├── backend/
│   └── [service-name]/           # Папка сервиса
│       ├── 000_SUMMARY.md        # Агрегация бэкенд-компонентов
│       ├── notification.service.md  # Имя = имя файла в src/
│       └── email.worker.md
│
├── database/
│   └── [service-name]/
│       ├── 000_SUMMARY.md
│       └── email_queue.md        # Имя = имя таблицы
│
├── frontend/
│   └── [feature-name]/
│       ├── 000_SUMMARY.md
│       └── NotificationSettingsPage.md
│
└── infra/
    └── [service-name]/
        ├── 000_SUMMARY.md
        └── redis_queue.md
```

**Принцип именования файлов:** Имя файла ресурса = имя файла в `src/` (без расширения `.ts/.tsx` + `.md`)

**Связь с IT-сервисами:**
```
00_services/notification-service/
        ↓
05_resources/backend/notification-service/
05_resources/database/notification-service/
05_resources/frontend/notification-settings/
05_resources/infra/notification-service/
```

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

### Шаг 2: Определить IT-сервис и ресурсы

#### 2.1 Определить IT-сервис

Из ADR определить к какому IT-сервису относятся ресурсы:
1. Проверить секцию "Связанные документы" — указан ли сервис
2. Проверить `00_services/` — существует ли сервис
3. Если сервис новый — он должен быть создан через `/summary-doc`

**Спросить пользователя если неясно:**
```
К какому IT-сервису относятся ресурсы из ADR [ID]?
1. [Существующие сервисы из 00_services/]
2. Другой: [название]
```

#### 2.2 Определить необходимые ресурсы

Из секции "Последствия" ADR определить:
- Какие компоненты нужно создать
- Какого типа каждый компонент (database/backend/frontend/infra)
- Как будет называться файл в `src/`

**Пример:**
```
ADR: DEC-001_email_queue_system.md
IT-сервис: notification-service

Ресурсы:
1. notification.service.ts (backend) → backend/notification-service/notification.service.md
2. email.worker.ts (backend) → backend/notification-service/email.worker.md
3. таблица email_queue (database) → database/notification-service/email_queue.md
4. Redis Queue (infra) → infra/notification-service/redis_queue.md
```

**Спросить пользователя если неясно:**
```
ADR предполагает создание следующих компонентов:
1. [Компонент 1] — какой тип? (database/backend/frontend/infra), как будет называться файл в src/?
2. [Компонент 2] — какой тип?, имя файла?

Какие ресурсы создать?
```

### Шаг 3: Подготовить структуру папок

#### 3.1 Проверить/создать папку сервиса

```bash
# Проверить существование
ls general_docs/05_resources/backend/[service-name]/ 2>/dev/null

# Создать если нет
mkdir -p general_docs/05_resources/backend/[service-name]/
mkdir -p general_docs/05_resources/database/[service-name]/
mkdir -p general_docs/05_resources/frontend/[feature-name]/
mkdir -p general_docs/05_resources/infra/[service-name]/
```

#### 3.2 Создать 000_SUMMARY.md для папки сервиса (если нет)

**Шаблон:**
```markdown
# [Service Name]: [Type] компоненты

**IT-сервис:** [service-name] ([00_services/[service-name]/](../../../00_services/[service-name]/))

**ADR:** [DEC-XXX](../../../04_decisions/DEC-XXX.md)

---

## Компоненты

| Файл | Назначение | Статус |
|------|------------|--------|
| — | — | — |

---

## Связи

| Компонент | Зависит от | Используется в |
|-----------|-----------|----------------|
| — | — | — |

---

**Последнее обновление:** [YYYY-MM-DD]
```

### Шаг 4: Создать ресурсы

#### Вариант А: Через скрипт (если доступен)

```bash
python scripts/resource_new.py -n "notification.service" -t backend -s "notification-service" -a "DEC-001"
```

**Параметры:**
- `-n` — имя файла (как в src/, без расширения)
- `-t` — тип (database/backend/frontend/infra)
- `-s` — имя сервиса (папка)
- `-a` — ID связанного ADR (например: DEC-001)
- `--desc` — краткое описание

#### Вариант Б: Вручную (если скрипт недоступен)

1. **Создать файл:**
   ```
   general_docs/05_resources/[type]/[service-name]/[filename].md
   ```

2. **Использовать шаблон** из `llm_instructions/templates/resource.md`

3. **Обновить 000_SUMMARY.md** в папке сервиса

4. **Обновить индекс** `000_[type].md`

### Шаг 5: Заполнить ресурс

После создания файла заполнить секции по типу:

#### Для database:
- Схема данных (таблицы, связи)
- Индексы
- Миграции
- SQL-код (CREATE TABLE, индексы)

#### Для backend:
- API Endpoints (если есть)
- Интерфейсы (TypeScript)
- Бизнес-логика (методы, функции)
- Зависимости

#### Для frontend:
- Props интерфейс
- Состояние компонента
- Хуки (если есть)
- Стили (если специфичные)

#### Для infra:
- Конфигурация
- Переменные окружения
- Мониторинг
- Масштабирование

### Шаг 6: Обновить связанные документы

#### 6.1 Обновить 000_SUMMARY.md папки сервиса

Добавить строку в таблицу "Компоненты":
```markdown
| [filename].md | [Назначение] | 🟡 draft |
```

#### 6.2 Обновить индекс типа (000_[type].md)

Добавить запись о новом ресурсе.

#### 6.3 Обновить ADR

Добавить ссылки на ресурсы в секцию "Связанные документы":
```markdown
**Связанные документы:**
- **Архитектура:** [001_*.md](../02_architecture/001_*.md)
- **Ресурсы:**
  - [backend/notification-service/](../05_resources/backend/notification-service/)
  - [database/notification-service/](../05_resources/database/notification-service/)
- **План реализации:** [создаётся из этого ADR]
```

#### 6.4 Обновить IT-сервис

Добавить ссылки на ресурсы в `00_services/[service-name]/README.md`.

### Шаг 7: Предложить следующий шаг

```
Ресурсы созданы для сервиса [service-name]:

📁 backend/[service-name]/
- notification.service.md
- email.worker.md

📁 database/[service-name]/
- email_queue.md
- email_templates.md

📁 infra/[service-name]/
- redis_queue.md

Обновлены:
- 000_SUMMARY.md в каждой папке
- ADR: DEC-XXX
- IT-сервис: 00_services/[service-name]/

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

**ADR:** DEC-001_email_queue_system.md (статус: approved)
**IT-сервис:** notification-service

**Последствия из ADR:**
- Notification Service API (бэкенд)
- Email Worker (бэкенд)
- Таблицы email_queue, email_templates, email_logs (БД)
- Redis Queue (инфра)
- Страница настроек (фронтенд)

### Шаг 1: Создать структуру папок

```bash
mkdir -p general_docs/05_resources/backend/notification-service/
mkdir -p general_docs/05_resources/database/notification-service/
mkdir -p general_docs/05_resources/frontend/notification-settings/
mkdir -p general_docs/05_resources/infra/notification-service/
```

### Шаг 2: Создать 000_SUMMARY.md в каждой папке

**backend/notification-service/000_SUMMARY.md:**
```markdown
# Notification Service: Backend компоненты

**IT-сервис:** notification-service ([00_services/notification-service/](../../../00_services/notification-service/))

**ADR:** [DEC-001](../../../04_decisions/DEC-001_email_queue_system.md)

## Компоненты

| Файл | Назначение | Статус |
|------|------------|--------|
| notification.service.md | API для отправки уведомлений | 🟡 draft |
| email.worker.md | Обработчик очереди | 🟡 draft |
```

### Шаг 3: Создать файлы ресурсов

**backend/notification-service/notification.service.md:**
```markdown
# notification.service.ts

**IT-сервис:** notification-service
**ADR:** DEC-001

## Назначение

API для приёма запросов на отправку уведомлений и добавления их в очередь.

## Интерфейс

\`\`\`typescript
interface NotificationService {
  sendEmail(to: string, template: string, data: object): Promise<void>;
  sendBulk(notifications: Notification[]): Promise<void>;
  getStatus(jobId: string): Promise<JobStatus>;
}
\`\`\`

## API Endpoints

| Endpoint | Метод | Описание |
|----------|-------|----------|
| /api/v1/notifications/send | POST | Отправить уведомление |
| /api/v1/notifications/status/:id | GET | Статус отправки |

## Зависимости

- BullMQ (очередь)
- Redis (хранение очереди)
```

**database/notification-service/email_queue.md:**
```markdown
# email_queue

**IT-сервис:** notification-service
**ADR:** DEC-001

## Назначение

Таблица для хранения очереди email-сообщений.

## Схема

| Поле | Тип | Описание |
|------|-----|----------|
| id | UUID | PK |
| to_email | VARCHAR(255) | Получатель |
| template_id | UUID | FK → email_templates |
| status | ENUM | pending/sent/failed |
| created_at | TIMESTAMP | Время создания |

## Индексы

| Индекс | Поля | Тип |
|--------|------|-----|
| idx_status | status | BTREE |
| idx_created | created_at | BTREE |

## SQL

\`\`\`sql
CREATE TABLE email_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  to_email VARCHAR(255) NOT NULL,
  template_id UUID REFERENCES email_templates(id),
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW()
);
\`\`\`
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
