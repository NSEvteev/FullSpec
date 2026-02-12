---
description: Стандарт живых документов архитектуры — сущность сервиса, триггеры создания/обновления, секции документа, Code Map, системная/доменная архитектура, shared-код, Quick Scan, шаблоны, чек-лист.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/.instructions/living-docs/service/README.md
---

# Стандарт сервисной документации

Версия стандарта: 2.0

Правила создания и обновления живых документов архитектуры (`specs/architecture/`). Сервис-центричный подход: `services/{svc}.md` — главная сущность, `system/` и `domains/` — контекст.

**Полезные ссылки:**
- [Стандарт SDD](../../standard-specs.md) — статусы, каскады, живые документы (таблица), полный воркфлоу
- [Инструкции specs/](../../README.md)
- [standard-impact.md](../../impact/standard-impact.md)
- [standard-design.md](../../design/standard-design.md)
- [standard-adr.md](../../adr/standard-adr.md)

**Файлы architecture/ (регулируемые этим стандартом):**
- [architecture/services/](/specs/architecture/services/) — per-service документы
- [architecture/system/](/specs/architecture/system/) — системная архитектура (overview, data-flows, infrastructure)
- [architecture/domains/](/specs/architecture/domains/) — доменная архитектура (bounded contexts, context map)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт SDD | [standard-specs.md](../../standard-specs.md) |
| Валидация | `validation-service.md` *(будет создан)* |
| Создание | `create-service.md` *(будет создан)* |
| Модификация | `modify-service.md` *(будет создан)* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Расположение и именование](#2-расположение-и-именование)
- [3. Frontmatter](#3-frontmatter)
- [4. Триггеры создания и обновления](#4-триггеры-создания-и-обновления)
  - [Таблица триггеров](#таблица-триггеров)
  - [Дельта-блоки ADR](#дельта-блоки-adr)
  - [Паттерн AS IS / TO BE](#паттерн-as-is--to-be)
- [5. Секции документа сервиса](#5-секции-документа-сервиса)
  - [5.1 Резюме](#51-резюме)
  - [5.2 API контракты](#52-api-контракты)
  - [5.3 Data Model](#53-data-model)
  - [5.4 Code Map](#54-code-map)
  - [5.5 Внешние зависимости](#55-внешние-зависимости)
  - [5.6 Границы автономии LLM](#56-границы-автономии-llm)
  - [5.7 Planned Changes](#57-planned-changes)
- [6. Системная и доменная архитектура](#6-системная-и-доменная-архитектура)
  - [6.1 system/overview.md](#61-systemoverviewmd)
  - [6.2 system/data-flows.md](#62-systemdata-flowsmd)
  - [6.3 system/infrastructure.md](#63-systeminfrastructuremd)
  - [6.4 domains/{domain}.md](#64-domainsdomainmd)
  - [6.5 domains/context-map.md](#65-domainscontext-mapmd)
- [7. Shared-код (/shared/)](#7-shared-код-shared)
- [8. Quick Scan для Impact](#8-quick-scan-для-impact)
- [9. Шаблоны](#9-шаблоны)
  - [9.1 Шаблон services/{svc}.md](#91-шаблон-servicessvcmd)
  - [9.2 Шаблон system/overview.md](#92-шаблон-systemoverviewmd)
  - [9.3 Шаблон domains/{domain}.md](#93-шаблон-domainsdomainmd)
- [10. Чек-лист качества](#10-чек-лист-качества)
- [11. Примеры](#11-примеры)
  - [11.1 Создание первого сервиса (auth)](#111-создание-первого-сервиса-auth)
  - [11.2 Обновление сервиса при ADR → DONE](#112-обновление-сервиса-при-adr--done)
  - [11.3 Пустой проект](#113-пустой-проект)

---

## 1. Назначение

Стандарт регулирует создание и обновление файлов в `specs/architecture/` — живых документов, отражающих текущее состояние архитектуры системы.

**Сервис-центричный подход:** Сервис — главная сущность. Документ `services/{svc}.md` — единица описания: содержит резюме, API, data model, Code Map, внешние зависимости, границы автономии и Planned Changes. Файлы `system/` и `domains/` — контекст, связывающий сервисы.

**Сервис в SDD** — логическая единица, объединяющая:

- **Код:** `src/{service}/` — реализация (backend, database, tests)
- **Архитектурный документ:** `architecture/services/{service}.md` — полное описание сервиса

Минимальное определение сервиса:

| Поле | Описание | Пример |
|------|----------|--------|
| Имя | kebab-case идентификатор | `auth`, `user-profile`, `notification` |
| Назначение | Одно предложение | "Аутентификация и авторизация пользователей" |
| Ключевые API | Основные endpoints/contracts | `/auth/token`, `/auth/refresh` |
| Технологии | Языки, фреймворки, хранилища | Python, FastAPI, PostgreSQL |

**Регулирует:**
- Структуру и формат `services/{svc}.md` (§ 5)
- Структуру `system/` и `domains/` (§ 6)
- Правила документирования `shared/` кода (§ 7)
- Порядок чтения для Impact Analysis (§ 8)

**НЕ регулирует:**
- Технологические стандарты — [standard-technology.md](/specs/.instructions/technologies/standard-technology.md)
- Code review, тестирование — стандарты разработки
- Содержимое спецификаций (Discussion, Impact, Design, ADR) — их собственные стандарты

**Граничные случаи:**
- **Пустой проект** — файлы `system/` и `domains/` существуют как пустые шаблоны, `services/` пуст. Impact опирается на Discussion + Clarify, предлагает все сервисы как "Новый (план создания)" с уверенностью "Предположительно" ([§ 11.3](#113-пустой-проект))
- **shared/** — не сервис, документируется через сервисы-владельцы ([§ 7](#7-shared-код-shared))
- **Монолит** — один `services/monolith.md`, system/ содержит только infrastructure.md

**Жизненный цикл сервисной документации:**

```
1. Инициализация проекта: system/ и domains/ файлы создаются как пустые шаблоны
2. Discussion → Impact: "Нужен сервис X" (предложение)
   - Если architecture/services/X.md существует → читать Резюме + Planned Changes
   - Если не существует → Impact предлагает "Новый (план создания)"
3. Impact → Design: Design РЕШАЕТ создание/использование
4. Design → WAITING: Planned Changes добавляются в system/, domains/, services/{svc}.md
5. Design → ADR: ADR для сервиса X
6. ADR → DONE: Создаётся/обновляется architecture/services/X.md
7. Design → DONE: Planned Changes в system/ и domains/ становятся актуальным AS IS
8. services/README.md обновляется (новая строка в таблице сервисов)
```

**Ключевые правила:**
- Файлы `system/` и `domains/` (фиксированные: overview.md, data-flows.md, infrastructure.md, context-map.md) **создаются при инициализации проекта** как пустые шаблоны. Design → WAITING заполняет их Planned Changes, Design → DONE превращает планируемое в AS IS
- Файлы `domains/{domain}.md` (per-domain) **создаются при первом Design → WAITING**, который идентифицирует этот домен
- Архитектурный документ `services/{svc}.md` **создаётся** при первом ADR → DONE для этого сервиса. До этого момента сервис существует только как предложение в Impact/Design
- При создании папки `specs/services/{svc}/` **ОБЯЗАТЕЛЬНО** создать метку `svc:{svc}` в `labels.yml`

---

## 2. Расположение и именование

**Расположение:** `specs/architecture/`

```
specs/architecture/
├── system/                        # Системная архитектура
│   ├── overview.md                #   Сервисы, потоки, высокоуровневая карта
│   ├── data-flows.md             #   Потоки данных между сервисами
│   └── infrastructure.md         #   Deployment, networking, monitoring
├── services/                      # Per-service архитектура
│   └── {service}.md               #   Резюме, API, data model, Code Map, зависимости
├── domains/                       # Доменная архитектура (DDD)
│   ├── {domain}.md                #   Один файл на bounded context
│   └── context-map.md             #   Карта взаимодействия контекстов
└── README.md
```

| Папка | Что хранит | Создаётся | Обновляется при |
|-------|-----------|-----------|-----------------|
| `system/` | Системная архитектура: overview, data-flows, infrastructure | Инициализация проекта (пустые шаблоны) | Planned Changes при Design → WAITING, AS IS при Design → DONE |
| `services/{svc}.md` | Архитектура сервиса: резюме, API, data model, **Code Map**, **Planned Changes** | Первый ADR → DONE | Planned Changes при Design → WAITING, AS IS при ADR → DONE |
| `domains/` | Bounded contexts, агрегаты, события, context map | Инициализация проекта (пустые шаблоны); per-domain при первом Design → WAITING | Planned Changes при Design → WAITING, AS IS при Design → DONE |

**Именование файлов:**

| Файл | Конвенция | Пример |
|------|-----------|--------|
| Сервис | `services/{service}.md`, kebab-case, совпадает с `src/{service}/` | `services/auth.md`, `services/user-profile.md` |
| Домен | `domains/{domain}.md`, kebab-case | `domains/identity.md`, `domains/billing.md` |
| Context map | `domains/context-map.md` (единственный) | — |
| System | Фиксированные имена | `overview.md`, `data-flows.md`, `infrastructure.md` |

**Формат README-таблицы** (`specs/architecture/services/README.md`):

| Сервис | Описание | Ключевые API | Технологии | Последний ADR |
|--------|----------|-------------|-----------|---------------|
| `auth` | Аутентификация и авторизация | `/auth/token`, `/auth/refresh` | Python, FastAPI, PostgreSQL | adr-0001 |

---

## 3. Frontmatter

**SSOT frontmatter:** [standard-frontmatter.md](/.structure/.instructions/standard-frontmatter.md) ([§ 1 — базовые поля](/.structure/.instructions/standard-frontmatter.md#1-обязательные-поля))

Файлы `services/{svc}.md` используют специализированный frontmatter:

| Поле | Обязательное | Описание |
|------|-------------|----------|
| `description` | Да | "Архитектура сервиса {service} — {назначение}" (до 1024 символов) |
| `service` | Да | kebab-case имя сервиса (совпадает с `src/{service}/`) |
| `created-by` | Да | ID ADR, при котором документ создан (`adr-NNNN`) |
| `last-updated-by` | Да | ID последнего ADR, обновившего документ (`adr-NNNN`) |

```yaml
---
description: Архитектура сервиса auth — аутентификация и авторизация пользователей.
service: auth
created-by: adr-0001
last-updated-by: adr-0003
---
```

**Для system/ и domains/ файлов:** Стандартный frontmatter проекта без специализированных полей:

```yaml
---
description: Обзор системной архитектуры — сервисы, потоки данных, инфраструктура.
---
```

---

## 4. Триггеры создания и обновления

### Таблица триггеров

| Событие | Действие | Файлы |
|---------|----------|-------|
| Инициализация проекта | **Создать** пустые шаблоны | `system/overview.md`, `system/data-flows.md`, `system/infrastructure.md`, `domains/context-map.md` |
| Design → WAITING | Добавить **Planned Changes** | `system/`, `domains/`, `services/{svc}.md` для затронутых сервисов |
| Design → WAITING (первый для домена) | **Создать** + Planned Changes | `domains/{domain}.md` |
| Design → DONE | **Обновить** AS IS (Planned Changes → актуальное) | `system/`, `domains/` файлы |
| ADR → WAITING | Добавить ссылку на ADR в Planned Changes | `services/{svc}.md` |
| ADR → DONE (первый для сервиса) | **Создать** | `services/{svc}.md`, строка в `services/README.md` |
| ADR → DONE (последующий) | **Обновить** | `services/{svc}.md` (дельта-блоки), `services/README.md` |
| Создание папки `specs/services/{svc}/` | **Создать** метку `svc:{svc}` в labels.yml | `labels.yml`, GitHub (через `/labels-modify`) |
| Удаление папки `specs/services/{svc}/` | **Удалить** метку `svc:{svc}` из labels.yml | `labels.yml`, GitHub (через `/labels-modify`, с миграцией Issues) |
| Design/ADR → REJECTED | Убрать Planned Changes | Затронутые `system/`, `domains/`, `services/{svc}.md` |

**Валидация svc-меток:**
```bash
python specs/.instructions/.scripts/validate-service-labels.py
```
Pre-commit хук `service-labels-validate` запускается автоматически при изменении `labels.yml` или `specs/services/`.

**Создание файлов:**
- **system/ и domains/ (фиксированные):** Создаются при инициализации проекта как пустые шаблоны. Первый Design → WAITING заполняет их Planned Changes
- **domains/{domain}.md (per-domain):** Создаётся при первом Design → WAITING, который идентифицирует этот домен
- **services/{svc}.md:** Создаётся при первом ADR → DONE для этого сервиса

### Дельта-блоки ADR

Каждый ADR содержит формализованную секцию изменений (ADDED/MODIFIED/REMOVED), которая напрямую указывает что обновить в живом документе:

```markdown
## Дельта

### ADDED
- Пакет `auth.tokens` — управление JWT-токенами
- Endpoint `POST /api/v1/tokens/refresh`
- Таблица `refresh_tokens` в PostgreSQL

### MODIFIED
- Middleware `auth.middleware` — добавлена JWT-валидация (ранее: API-key)
- Endpoint `POST /api/v1/login` — возвращает access + refresh token (ранее: только session)

### REMOVED
- Endpoint `POST /api/v1/session` — заменён на token-based auth
- Middleware `session_middleware` — больше не используется
```

**Применение при ADR → DONE:** Блоки ADDED добавляются в `services/{svc}.md`, MODIFIED обновляются, REMOVED удаляются. LLM не "угадывает" — список изменений формализован в ADR.

**Связь с ADR:** Полный формат дельта-блоков определяется в стандарте ADR ([standard-adr.md](../../adr/standard-adr.md)). В стандарте SDD — [§ 6 "Связи между уровнями"](../../standard-specs.md#6-связи-между-уровнями).

### Паттерн AS IS / TO BE

LLM читает живые документы (включая Planned Changes) **перед** проектированием. Изменения фиксируются в объектах (TO BE), а при завершении — переносятся в живые документы (новый AS IS).

```
1. LLM читает architecture/services/auth.md (AS IS)
2. ADR описывает дельту: что добавить/изменить/удалить (TO BE)
3. ADR → DONE: дельта применяется, auth.md обновляется (новый AS IS)
```

---

## 5. Секции документа сервиса

Документ `services/{svc}.md` содержит **7 секций** в фиксированном порядке. Все секции обязательны.

| Секция | Назначение | Обновляется при |
|--------|-----------|-----------------|
| **Резюме** | Назначение сервиса, ключевые характеристики | ADR → DONE |
| **API контракты** | Публичные endpoints, события, CLI | ADR → DONE |
| **Data Model** | Основные сущности и хранилища | ADR → DONE |
| **Code Map** | Tech Stack, пакеты, точки входа, внутренние зависимости | ADR → DONE |
| **Внешние зависимости** | Зависимости от shared/ и других сервисов | ADR → DONE |
| **Границы автономии LLM** | Три уровня: Свободно, Флаг, CONFLICT | ADR → DONE |
| **Planned Changes** | Запланированные изменения (навигационные ссылки) | Design → WAITING / ADR → DONE |

### 5.1 Резюме

Назначение сервиса, ключевые характеристики. 1-3 предложения. Impact читает эту секцию при Quick Scan ([§ 8](#8-quick-scan-для-impact)).

```markdown
## Резюме

Сервис аутентификации и авторизации. Управляет JWT-токенами (access + refresh),
ротацией ключей и RBAC. Обслуживает все сервисы проекта через middleware-валидацию.
```

### 5.2 API контракты

Таблица публичных API: REST endpoints, events, CLI commands. Полный контракт (формат данных, протокол) описан в Design — здесь только навигационная таблица.

```markdown
## API контракты

| Тип | Endpoint/Event | Метод | Описание |
|-----|---------------|-------|----------|
| REST | /api/v1/auth/token | POST | Создание access + refresh token |
| REST | /api/v1/auth/token | PUT | Обновление token по refresh_token |
| REST | /api/v1/auth/token | DELETE | Отзыв refresh_token |
| Event | UserCreatedEvent | publish | Уведомление о регистрации нового пользователя |
| CLI | auth migrate | — | Миграция схемы БД |
```

### 5.3 Data Model

Основные сущности и хранилища. Таблица навигационная — полная схема в ADR.

```markdown
## Data Model

| Сущность | Хранилище | Назначение |
|----------|-----------|-----------|
| User | PostgreSQL: users | Профиль пользователя (id, email, password_hash) |
| RefreshToken | Redis: tokens:{user_id} | Токены обновления (token, expires_at) |
| Role | PostgreSQL: roles | Роли для RBAC (id, name, permissions) |
```

### 5.4 Code Map

Навигационная карта кода сервиса. Описывает внутреннюю структуру на уровне **пакетов/модулей** (не файлов).

**Почему пакеты, а не файлы:**

| Проблема per-file спеков | Как Code Map её избегает |
|--------------------------|------------------------|
| **Синхронизация** — 200 файлов = 200 точек рассинхронизации | Описание на уровне пакетов (5-15 на сервис), обновляется при ADR → DONE |
| **Дублирование** — спек повторяет docstrings и type hints | Code Map описывает навигацию и границы, не реализацию |
| **Масштаб** — невозможно поддерживать вручную | Пакеты меняются редко, файлы — постоянно |
| **Мультиязычность** — docstring формат зависит от языка | Пакет/модуль — универсальная абстракция |

```markdown
## Code Map

### Tech Stack

| Технология | Назначение |
|-----------|-----------|
| Python 3.12 | Бэкенд |
| PostgreSQL 16 | Хранение пользователей и ролей |
| Redis 7 | Хранение refresh-токенов |
| FastAPI | API-фреймворк |

### Пакеты

| Пакет | Назначение | Ключевые модули |
|-------|-----------|----------------|
| `auth.tokens` | Управление JWT-токенами | `generator.py`, `validator.py` |
| `auth.keys` | Ротация и хранение ключей | `rotation.py`, `store.py` |
| `auth.middleware` | Аутентификация запросов | `jwt_middleware.py` |
| `auth.rbac` | Role-based access control | `permissions.py`, `decorators.py` |

### Точки входа

- API: `auth/api/routes.py`
- Events: `auth/events/handlers.py`
- CLI: `auth/cli/commands.py`

### Внутренние зависимости

auth.middleware → auth.tokens → auth.keys
auth.rbac → auth.tokens
```

**Tech Stack и технологические стандарты:** При наличии `standard-{tech}.md` в `specs/.instructions/technologies/` — таблица Tech Stack дополняется ссылками на стандарт и валидацию. Технологические стандарты регулируются [standard-technology.md](/specs/.instructions/technologies/standard-technology.md).

### 5.5 Внешние зависимости

Зависимости от `shared/` и других сервисов. Показывает, что данный сервис использует извне и что предоставляет.

```markdown
## Внешние зависимости

| Тип | Путь/Сервис | Что используем | Роль |
|-----|------------|---------------|------|
| shared | shared/events/user_created.py | UserCreatedEvent | publisher |
| shared | shared/contracts/auth.proto | protobuf-схемы авторизации | provider |
| service | notification | UserCreatedEvent | consumer потребляет наше событие |
| service | gateway | /api/v1/auth/* | provider вызывает наши endpoints |
```

**Роли:**
- **provider** — сервис предоставляет API/событие/контракт
- **consumer** — сервис потребляет API/событие/контракт
- **publisher** — сервис публикует событие в shared/
- **subscriber** — сервис подписывается на событие из shared/

### 5.6 Границы автономии LLM

Ключевая секция. Явно говорит LLM при выполнении задачи, что можно менять самостоятельно:

```markdown
## Границы автономии LLM

- **Свободно:** реализация внутри пакета (алгоритмы, рефакторинг, оптимизация)
- **Флаг:** изменение контрактов между пакетами (может затронуть План тестов)
- **CONFLICT:** изменение API сервиса, data model, добавление/удаление пакетов (затрагивает ADR)
```

| Уровень | Что можно менять | Действие LLM |
|---------|-----------------|--------------|
| **Свободно** | Реализация внутри пакета: алгоритмы, рефакторинг, оптимизация | Нет обратной связи |
| **Флаг** | Контракты между пакетами сервиса | Автономно обновляет План тестов/План разработки, информирует в чат |
| **CONFLICT** | API сервиса, data model, добавление/удаление пакетов | Вся цепочка → CONFLICT ([§ 8.3 SDD](../../standard-specs.md#83-running-to-conflict)) |

Три уровня напрямую связаны с механизмом обратной связи Code → Specs ([Стандарт SDD § 8.3](../../standard-specs.md#83-running-to-conflict)).

**Когда обновляется:** При ADR → DONE — как часть обычного каскада обновления `services/{svc}.md`.

### 5.7 Planned Changes

Секция Planned Changes — навигационный указатель на запланированные, но ещё не применённые изменения.

```markdown
## Planned Changes

- **[Discussion 001: OAuth2 авторизация](../../discussion/disc-0001-oauth2-authorization.md)**
  Статус: RUNNING | Затрагивает: API endpoints, data model
  Design: [design-0001-oauth2-service-design.md](../../design/design-0001-oauth2-service-design.md)
  ADR: [adr-0001-jwt-to-oauth2.md](../services/auth/adr/adr-0001-jwt-to-oauth2.md)
```

**Правила:**
1. **Добавляется** когда Design переходит в WAITING
2. LLM при чтении AS IS **обязан** учитывать Planned Changes
3. При необходимости LLM переходит по ссылке на Design и читает дочерние ADR для получения дельт
4. **Не дублирует контент** — навигационный указатель на цепочку, не копия дельт. Дельты могут измениться при CONFLICT, дублирование нарушает SSOT
5. **Удаляется** при обновлении живого документа (ADR → DONE — дельта применяется) или при REJECTED (дельта отклоняется)

**Подробнее:** [Стандарт SDD § 9.1](../../standard-specs.md#91-обновление-при-планировании-to-waiting)

---

## 6. Системная и доменная архитектура

Файлы `system/` и `domains/` — контекст, связывающий сервисы.

**Жизненный цикл:**
1. **Инициализация проекта** — фиксированные файлы создаются как пустые шаблоны: `system/overview.md`, `system/data-flows.md`, `system/infrastructure.md`, `domains/context-map.md`
2. **Design → WAITING** — LLM добавляет Planned Changes (ссылки на Design с описанием планируемых изменений). Per-domain файлы `domains/{domain}.md` создаются при первом обращении
3. **Design → DONE** — Planned Changes превращаются в актуальный AS IS (контент обновляется, секция Planned Changes очищается)

### 6.1 system/overview.md

Высокоуровневый обзор системы: какие сервисы существуют, как взаимодействуют.

```markdown
# Обзор системной архитектуры

## Сервисы

| Сервис | Назначение | Ключевые API |
|--------|-----------|-------------|
| auth | Аутентификация и авторизация | /auth/token, /auth/refresh |
| gateway | API Gateway, маршрутизация, rate limiting | /api/v1/* |
| users | Управление профилями пользователей | /users/{id} |

## Потоки данных

auth → gateway: JWT-валидация через middleware
users → auth: проверка permissions через gRPC
auth → notification: UserCreatedEvent (async, RabbitMQ)

## Инфраструктура

Deployment: Docker Compose (dev), Kubernetes (staging/prod)
Networking: внутренняя сеть сервисов, gateway — единственная точка входа
Мониторинг: Prometheus + Grafana
```

### 6.2 system/data-flows.md

Детальные потоки данных между сервисами. Формат соответствует блокам взаимодействия из Design:

```markdown
# Потоки данных

## auth → notification: UserCreatedEvent

| Поле | Значение |
|------|----------|
| Участники | auth (publisher) → notification (consumer) |
| Контракт | UserCreatedEvent {user_id, email, created_at} |
| Паттерн | async/events (RabbitMQ) |
| Протокол | AMQP, JSON-схема |

## gateway → auth: JWT-валидация

| Поле | Значение |
|------|----------|
| Участники | gateway (consumer) → auth (provider) |
| Контракт | ValidateToken(token) → {valid, user_id, roles} |
| Паттерн | sync/gRPC |
| Протокол | gRPC, protobuf |
```

### 6.3 system/infrastructure.md

Deployment topology, networking, monitoring. Обновляется при Design → DONE, если Design затрагивает инфраструктуру.

```markdown
# Инфраструктура

## Deployment

| Окружение | Технология | Конфигурация |
|-----------|-----------|-------------|
| dev | Docker Compose | config/dev/ |
| staging | Kubernetes | config/staging/ |
| prod | Kubernetes | config/prod/ |

## Networking

- Внутренняя сеть: {network-name}
- Gateway: единственная точка входа
- Service mesh: нет (прямые вызовы)

## Мониторинг

- Метрики: Prometheus
- Дашборды: Grafana
- Логи: ELK Stack
- Алерты: Alertmanager
```

### 6.4 domains/{domain}.md

Bounded context: агрегаты, события, команды, инварианты. Один файл на домен.

```markdown
# Домен: Identity

## Агрегаты

| Агрегат | Описание | Сервис |
|---------|----------|--------|
| User | Профиль, credentials, роли | auth, users |
| Session | Текущая сессия (refresh tokens) | auth |

## Доменные события

| Событие | Издатель | Потребители |
|---------|----------|------------|
| UserCreated | auth | notification, billing |
| RoleAssigned | auth | gateway |

## Инварианты

- Один пользователь — один email (уникальность)
- Refresh token привязан к одному пользователю
- Минимум одна роль у каждого пользователя
```

### 6.5 domains/context-map.md

Карта взаимодействия между bounded contexts. Единственный файл.

```markdown
# Context Map

## Связи между контекстами

| Upstream | Downstream | Паттерн | Описание |
|----------|-----------|---------|----------|
| Identity | Billing | Customer/Supplier | Billing получает информацию о пользователях |
| Identity | Notification | Published Language | Стандартные события UserCreated, RoleAssigned |
| Gateway | Identity | Conformist | Gateway конформен к API Identity |
```

---

## 7. Shared-код (/shared/)

**Принцип:** `shared/` — **НЕ сервис**. Папка `architecture/services/shared/` **НЕ создаётся**. Контент `shared/` описывается через существующие механизмы SDD: блоки взаимодействия в Design определяют контракты, ADR сервисов описывают создание и использование.

**Владение:**

| Содержимое shared/ | Владелец | Где описано |
|---|---|---|
| Контракты API (protobuf, OpenAPI) | Сервис-провайдер (кто предоставляет API) | Design → блоки взаимодействия |
| Схемы событий (UserCreatedEvent) | Сервис-издатель (кто публикует событие) | Design → блоки взаимодействия |
| Общие библиотеки (валидация, логирование) | Сервис-инициатор | ADR сервиса |

**Правила:**

1. **Владение изменением:** ADR сервиса-провайдера включает дельту `ADDED`/`MODIFIED` для файлов в `shared/`. ADR сервисов-потребителей указывают **внешнюю зависимость** от `shared/`, но не включают дельту для `shared/`
2. **Code Map:** Каждый сервис указывает зависимости от `shared/` в секции "Внешние зависимости" ([§ 5.5](#55-внешние-зависимости))
3. **Зависимости задач:** Задача "создать в shared/" (из Plan провайдера) блокирует задачи "реализовать обработчик" (из Plan потребителей)
4. **Обратная связь:** Изменение контракта в shared/ — изменение блока взаимодействия → CONFLICT уровня Design, каскад на все ADR сервисов-участников
5. **Что НЕ попадает:** Код, используемый только одним сервисом. Выносится в `shared/` только при появлении второго потребителя

**Подробнее:** [Стандарт SDD § 6 "Shared код"](../../standard-specs.md#shared-код-shared)

---

## 8. Quick Scan для Impact

Impact Analysis ([standard-impact.md](../../impact/standard-impact.md)) обязан прочитать архитектурные документы **до** фазы Clarify. Порядок чтения:

| # | Что читать | Зачем |
|---|-----------|-------|
| 1 | **`architecture/services/README.md`** — таблица сервисов | Список существующих сервисов, технологии, API |
| 2 | **`architecture/system/overview.md`** (если существует) | Общая картина, потоки между сервисами |
| 3 | **`architecture/services/{svc}.md`** — Резюме + Planned Changes | Детали по затронутым сервисам |

**Impact НЕ читает** детально Code Map, Tech Stack, границы автономии — это уровень ADR/Design.

**Пустой проект:** Если `architecture/` содержит только пустые шаблоны (system/, domains/) и `services/` пуст — Impact опирается только на Discussion + Clarify. Предлагает все сервисы как "Новый (план создания)" с уверенностью "Предположительно".

---

## 9. Шаблоны

### 9.1 Шаблон services/{svc}.md

`````markdown
---
description: Архитектура сервиса {service} — {назначение}.
service: {service-name}
created-by: adr-NNNN
last-updated-by: adr-NNNN
---

# {service-name}

## Резюме

{1-3 предложения: назначение, ключевые характеристики, роль в системе}

## API контракты

| Тип | Endpoint/Event | Метод | Описание |
|-----|---------------|-------|----------|
| {REST/Event/CLI} | {endpoint} | {метод} | {описание} |

## Data Model

| Сущность | Хранилище | Назначение |
|----------|-----------|-----------|
| {Entity} | {Storage: table/key} | {описание} |

## Code Map

### Tech Stack

| Технология | Назначение |
|-----------|-----------|
| {tech} | {назначение} |

### Пакеты

| Пакет | Назначение | Ключевые модули |
|-------|-----------|----------------|
| `{package}` | {назначение} | `{module1}`, `{module2}` |

### Точки входа

- API: `{service}/api/routes.py`
- Events: `{service}/events/handlers.py`
- CLI: `{service}/cli/commands.py`

### Внутренние зависимости

{package.a} → {package.b} → {package.c}

## Внешние зависимости

| Тип | Путь/Сервис | Что используем | Роль |
|-----|------------|---------------|------|
| {shared/service} | {путь} | {что} | {provider/consumer/publisher/subscriber} |

## Границы автономии LLM

- **Свободно:** {что можно менять без согласования}
- **Флаг:** {что можно менять, но информировать}
- **CONFLICT:** {что нельзя менять — ADR-уровень}

## Planned Changes

*Нет запланированных изменений.*
`````

### 9.2 Шаблон system/overview.md

`````markdown
---
description: Обзор системной архитектуры — сервисы, потоки данных, инфраструктура.
---

# Обзор системной архитектуры

## Сервисы

| Сервис | Назначение | Ключевые API |
|--------|-----------|-------------|
| {service} | {назначение} | {endpoints} |

## Потоки данных

{Высокоуровневая карта: кто с кем общается, через что}

## Инфраструктура

{Deployment, networking, мониторинг}

## Planned Changes

*Нет запланированных изменений.*
`````

### 9.3 Шаблон domains/{domain}.md

`````markdown
---
description: Домен {domain} — {описание bounded context}.
---

# Домен: {Domain Name}

## Агрегаты

| Агрегат | Описание | Сервис |
|---------|----------|--------|
| {Aggregate} | {описание} | {service} |

## Доменные события

| Событие | Издатель | Потребители |
|---------|----------|------------|
| {Event} | {publisher} | {consumers} |

## Инварианты

- {инвариант 1}
- {инвариант 2}

## Planned Changes

*Нет запланированных изменений.*
`````

---

## 10. Чек-лист качества

### Frontmatter (services/{svc}.md)
- [ ] `description` — до 1024 символов, формат "Архитектура сервиса X — назначение"
- [ ] `service` — kebab-case, совпадает с `src/{service}/`
- [ ] `created-by` — ID ADR (`adr-NNNN`)
- [ ] `last-updated-by` — ID последнего ADR

### Содержание
- [ ] Все 7 секций присутствуют (Резюме, API, Data Model, Code Map, Внешние зависимости, Границы, Planned Changes)
- [ ] Порядок секций соответствует стандарту
- [ ] Резюме — 1-3 предложения, без технических деталей реализации
- [ ] API контракты — таблица с колонками Тип, Endpoint/Event, Метод, Описание
- [ ] Data Model — таблица с колонками Сущность, Хранилище, Назначение

### Code Map
- [ ] Tech Stack — таблица технологий с назначением
- [ ] Пакеты — таблица с Пакет, Назначение, Ключевые модули
- [ ] Точки входа указаны (API, Events, CLI)
- [ ] Внутренние зависимости описаны
- [ ] Уровень описания — пакеты/модули, не файлы

### Внешние зависимости
- [ ] Таблица с колонками Тип, Путь/Сервис, Что используем, Роль
- [ ] Все зависимости от `shared/` указаны
- [ ] Роли корректны (provider/consumer/publisher/subscriber)

### Границы автономии LLM
- [ ] Три уровня указаны (Свободно, Флаг, CONFLICT)
- [ ] Конкретные примеры для каждого уровня
- [ ] Соответствует текущему Code Map (пакеты, API)

### Planned Changes
- [ ] Формат: ссылка на Discussion + Design + ADR
- [ ] Не содержит дублирования дельт из ADR
- [ ] Ссылки валидны (документы существуют)

### System/ и Domains/
- [ ] Фиксированные файлы существуют: `system/overview.md`, `system/data-flows.md`, `system/infrastructure.md`, `domains/context-map.md`
- [ ] Секция Planned Changes присутствует в каждом файле system/ и domains/
- [ ] При Design → WAITING — Planned Changes заполнены ссылками на Design
- [ ] При Design → DONE — контент актуален (AS IS), Planned Changes очищены

### Метки
- [ ] Метка `svc:{svc}` существует в `labels.yml`

### README
- [ ] Строка в `services/README.md` актуальна (Сервис, Описание, API, Технологии, Последний ADR)

---

## 11. Примеры

### 11.1 Создание первого сервиса (auth)

Greenfield: первый ADR → DONE создаёт `services/auth.md`.

**Контекст:**
- Discussion: "OAuth2 авторизация"
- Design решил: auth отвечает за токены
- ADR auth: "JWT с ES256, ротация ключей, refresh-токены"
- ADR → DONE (первый для auth)

**Результат — `architecture/services/auth.md`:**

```markdown
---
description: Архитектура сервиса auth — аутентификация и авторизация пользователей.
service: auth
created-by: adr-0001
last-updated-by: adr-0001
---

# auth

## Резюме

Сервис аутентификации и авторизации. Управляет JWT-токенами (access + refresh),
ротацией ключей ES256 и RBAC.

## API контракты

| Тип | Endpoint/Event | Метод | Описание |
|-----|---------------|-------|----------|
| REST | /api/v1/auth/token | POST | Создание access + refresh token |
| REST | /api/v1/auth/token | PUT | Обновление token по refresh_token |
| REST | /api/v1/auth/token | DELETE | Отзыв refresh_token |
| Event | UserCreatedEvent | publish | Уведомление о регистрации |

## Data Model

| Сущность | Хранилище | Назначение |
|----------|-----------|-----------|
| User | PostgreSQL: users | Профиль (id, email, password_hash) |
| RefreshToken | Redis: tokens:{user_id} | Токены обновления |
| Role | PostgreSQL: roles | Роли RBAC |

## Code Map

### Tech Stack

| Технология | Назначение |
|-----------|-----------|
| Python 3.12 | Бэкенд |
| PostgreSQL 16 | Хранение пользователей и ролей |
| Redis 7 | Хранение refresh-токенов |
| FastAPI | API-фреймворк |

### Пакеты

| Пакет | Назначение | Ключевые модули |
|-------|-----------|----------------|
| `auth.tokens` | Управление JWT-токенами | `generator.py`, `validator.py` |
| `auth.keys` | Ротация и хранение ключей | `rotation.py`, `store.py` |
| `auth.middleware` | Аутентификация запросов | `jwt_middleware.py` |

### Точки входа

- API: `auth/api/routes.py`
- Events: `auth/events/handlers.py`
- CLI: `auth/cli/commands.py`

### Внутренние зависимости

auth.middleware → auth.tokens → auth.keys

## Внешние зависимости

| Тип | Путь/Сервис | Что используем | Роль |
|-----|------------|---------------|------|
| shared | shared/events/user_created.py | UserCreatedEvent | publisher |

## Границы автономии LLM

- **Свободно:** реализация внутри пакета (алгоритмы, рефакторинг, оптимизация)
- **Флаг:** изменение контрактов между пакетами (может затронуть План тестов)
- **CONFLICT:** изменение API (/auth/*), data model (users, tokens), добавление/удаление пакетов

## Planned Changes

*Нет запланированных изменений.*
```

**Одновременно обновляется `services/README.md`:**

| Сервис | Описание | Ключевые API | Технологии | Последний ADR |
|--------|----------|-------------|-----------|---------------|
| `auth` | Аутентификация и авторизация | /auth/token | Python, FastAPI, PostgreSQL | adr-0001 |

### 11.2 Обновление сервиса при ADR → DONE

Существующий сервис auth, второй ADR добавляет OAuth2 client credentials.

**ADR adr-0002 содержит дельту:**

```markdown
## Дельта

### ADDED
- Пакет `auth.oauth2` — OAuth2 client credentials flow
- Endpoint `POST /api/v1/auth/clients` — регистрация OAuth2-клиента
- Таблица `oauth2_clients` в PostgreSQL

### MODIFIED
- Endpoint `POST /api/v1/auth/token` — поддерживает grant_type=client_credentials

### REMOVED
- (нет)
```

**Результат — в `auth.md` обновляются:**

1. **API контракты** — добавляется строка `POST /api/v1/auth/clients`, обновляется описание `POST /token`
2. **Data Model** — добавляется `OAuth2Client | PostgreSQL: oauth2_clients`
3. **Code Map → Пакеты** — добавляется `auth.oauth2`
4. **Code Map → Внутренние зависимости** — обновляется граф
5. **Frontmatter** — `last-updated-by: adr-0002`
6. **services/README.md** — обновляются колонки "Ключевые API" и "Последний ADR"

### 11.3 Пустой проект

Impact Analysis когда `architecture/` содержит пустые шаблоны:

```
1. Impact читает architecture/services/README.md → таблица пуста
2. Impact читает architecture/system/overview.md → файл существует, но пуст (шаблон)
3. Impact опирается только на Discussion + Clarify
4. Все предложенные сервисы получают:
   - Статус: "Новый (план создания)"
   - Уверенность: "Предположительно"
5. Design принимает решение о создании сервисов
6. Design → WAITING: system/overview.md, domains/ заполняются Planned Changes
7. Design → DONE: Planned Changes → актуальный AS IS
8. Первые ADR → DONE создают services/{svc}.md для каждого сервиса
```
