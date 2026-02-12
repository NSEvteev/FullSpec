---
description: Стандарт фиксированных файлов архитектуры — существование, структура, обязательные секции, frontmatter, шаблоны.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/.instructions/living-docs/architecture/README.md
---

# Стандарт фиксированных файлов архитектуры

Версия стандарта: 1.0

Правила существования и структуры фиксированных файлов `specs/architecture/` (system/ и domains/). Файлы создаются при инициализации проекта и содержат системный контекст.

**Полезные ссылки:**
- [Стандарт сервисной документации](../service/standard-service.md) — обновление файлов (триггеры, Planned Changes, AS IS)
- [Инструкции living-docs](../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Обновление | [standard-service.md](../service/standard-service.md) § 4, § 6 |
| Валидация | [validation-architecture.md](./validation-architecture.md) |

**Разделение ответственности:**

| Аспект | Кто отвечает |
|--------|-------------|
| Когда обновлять (триггеры, Planned Changes, AS IS) | [standard-service.md](../service/standard-service.md) § 4, § 6 |
| Что должно быть (структура, секции, шаблоны) | Этот документ |
| Валидация структуры, pre-commit хук | [validation-architecture.md](./validation-architecture.md) + скрипт |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Расположение и именование](#2-расположение-и-именование)
- [3. Frontmatter](#3-frontmatter)
- [4. Обязательные секции](#4-обязательные-секции)
  - [4.1 system/overview.md](#41-systemoverviewmd)
  - [4.2 system/data-flows.md](#42-systemdata-flowsmd)
  - [4.3 system/infrastructure.md](#43-systeminfrastructuremd)
  - [4.4 domains/context-map.md](#44-domainscontext-mapmd)
- [5. Шаблоны](#5-шаблоны)
  - [5.1 Шаблон system/overview.md](#51-шаблон-systemoverviewmd)
  - [5.2 Шаблон system/data-flows.md](#52-шаблон-systemdata-flowsmd)
  - [5.3 Шаблон system/infrastructure.md](#53-шаблон-systeminfrastructuremd)
  - [5.4 Шаблон domains/context-map.md](#54-шаблон-domainscontext-mapmd)
- [6. Чек-лист качества](#6-чек-лист-качества)

---

## 1. Назначение

В `specs/architecture/` есть 4 фиксированных файла, которые создаются при инициализации проекта и содержат системный контекст:

| # | Файл | Назначение |
|---|------|-----------|
| 1 | `system/overview.md` | Обзор системной архитектуры — сервисы, потоки, инфраструктура |
| 2 | `system/data-flows.md` | Потоки данных между сервисами — контракты, паттерны, протоколы |
| 3 | `system/infrastructure.md` | Deployment, networking, мониторинг, алерты |
| 4 | `domains/context-map.md` | Карта доменов, bounded contexts и их связей |

**Этот стандарт управляет:**
- Обязательным существованием 4 файлов
- Структурой frontmatter
- Обязательными секциями в каждом файле
- Шаблонами для инициализации

**Этот стандарт НЕ управляет:**
- Когда и как обновлять файлы — это [standard-service.md](../service/standard-service.md) § 4 (триггеры), § 6 (описания секций)
- Per-service документами `services/{svc}.md` — это [standard-service.md](../service/standard-service.md) § 5
- Per-domain файлами `domains/{domain}.md` — это [standard-service.md](../service/standard-service.md) § 6.4

---

## 2. Расположение и именование

**Расположение:** `specs/architecture/`

```
specs/architecture/
├── system/
│   ├── overview.md           # Обзор системной архитектуры
│   ├── data-flows.md         # Потоки данных между сервисами
│   └── infrastructure.md     # Deployment, networking, мониторинг
├── domains/
│   └── context-map.md        # Карта доменов и их связей
└── ...
```

**Именование:** Фиксированные имена. Переименование запрещено.

| Файл | Имя | Изменяемое |
|------|-----|-----------|
| Обзор архитектуры | `system/overview.md` | Нет |
| Потоки данных | `system/data-flows.md` | Нет |
| Инфраструктура | `system/infrastructure.md` | Нет |
| Карта контекстов | `domains/context-map.md` | Нет |

---

## 3. Frontmatter

**SSOT frontmatter:** [standard-frontmatter.md](/.structure/.instructions/standard-frontmatter.md)

Все 4 фиксированных файла используют стандартный frontmatter с одним обязательным полем:

| Поле | Обязательное | Описание |
|------|-------------|----------|
| `description` | Да | Краткое описание файла (до 1024 символов) |

```yaml
---
description: Обзор системной архитектуры — сервисы, потоки данных, инфраструктура.
---
```

---

## 4. Обязательные секции

Каждый фиксированный файл содержит набор обязательных секций (заголовки `##`). Секции `## Planned Changes` и `## Changelog` обязательны во всех 4 файлах.

### 4.1 [system/overview.md](/specs/architecture/system/overview.md)

Высокоуровневый обзор системы: какие сервисы существуют, как взаимодействуют, какая инфраструктура.

| # | Секция | Назначение |
|---|--------|-----------|
| 1 | `## Домены и сервисы` | Таблица сервисов по доменам: Сервис, Назначение, Ключевые API |
| 2 | `## Потоки данных` | Высокоуровневая карта взаимодействий |
| 3 | `## Инфраструктура` | Компоненты инфраструктуры |
| 4 | `## Planned Changes` | Запланированные изменения (ссылки на Design) |
| 5 | `## Changelog` | История применённых Design-цепочек |

**Пример заполненного файла:**

```markdown
# Обзор системной архитектуры

## Домены и сервисы

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

## Planned Changes

*Нет запланированных изменений.*

## Changelog

*Нет записей.*
```

**Допустимые дополнительные секции:** архитектурные принципы, критический путь, домены и сервисы (группировка по доменам). Обязательные секции не удаляются.

### 4.2 [system/data-flows.md](/specs/architecture/system/data-flows.md)

Детальные потоки данных между сервисами. Каждый поток описывается блоком с таблицей.

| # | Секция | Назначение |
|---|--------|-----------|
| 1 | Блоки потоков `## {от} → {к}: {назначение}` | Таблица: Участники, Контракт, Паттерн, Протокол |
| 2 | `## Planned Changes` | Запланированные изменения |
| 3 | `## Changelog` | История применённых Design-цепочек |

**Формат блока потока:**

```markdown
## auth → notifications: UserRegistered

| Поле | Значение |
|------|----------|
| Участники | auth (publisher) → notifications (consumer) |
| Контракт | UserRegisteredEvent {user_id, email, name, registered_at} |
| Паттерн | async/events (RabbitMQ) |
| Протокол | AMQP, JSON-схема |
```

**Пример заполненного файла:**

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

## Planned Changes

*Нет запланированных изменений.*

## Changelog

*Нет записей.*
```

**Допустимые дополнительные секции:** принципы взаимодействия, группировка по темам (нумерованные разделы). Блоки могут быть вложены в тематические секции.

### 4.3 [system/infrastructure.md](/specs/architecture/system/infrastructure.md)

Deployment topology, networking, мониторинг, алерты.

| # | Секция | Назначение |
|---|--------|-----------|
| 1 | `## Deployment` | Таблица окружений: Окружение, Технология, Конфигурация |
| 2 | `## Networking` | Путь запроса, DNS, Network Policies |
| 3 | `## Мониторинг` | Метрики, логи, трейсинг, алерты |
| 4 | `## Planned Changes` | Запланированные изменения |
| 5 | `## Changelog` | История применённых Design-цепочек |

**Пример заполненного файла:**

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

## Planned Changes

*Нет запланированных изменений.*

## Changelog

*Нет записей.*
```

**Допустимые дополнительные секции:** принципы, секреты, стратегии деплоя, ресурсы.

### 4.4 [domains/context-map.md](/specs/architecture/domains/context-map.md)

Карта доменов и их связей. Единственный **фиксированный** файл в `domains/` (per-domain файлы `{domain}.md` создаются динамически — см. [standard-service.md § 6](../service/standard-service.md#per-domain-файлы-domainsdomainmd)).

| # | Секция | Назначение |
|---|--------|-----------|
| 1 | `## Домены` | Описание каждого домена: ответственность, сервисы, инварианты |
| 2 | `## Связи между контекстами` | Таблица: Upstream, Downstream, Паттерн, Описание |
| 3 | `## Planned Changes` | Запланированные изменения |
| 4 | `## Changelog` | История применённых Design-цепочек |

**Формат таблицы связей:**

```markdown
| Upstream | Downstream | Паттерн | Описание |
|----------|-----------|---------|----------|
| Identity | Commerce | Customer/Supplier | Commerce использует данные пользователей |
```

**Пример заполненного файла:**

```markdown
# Context Map

## Домены

### Identity — управление пользователями и авторизацией

**Ответственность:** аутентификация, авторизация, управление ролями

**Сервисы:** `auth`, `users`

**Ключевые инварианты:**
- Один пользователь — один email
- Минимум одна роль у пользователя

## Связи между контекстами

| Upstream | Downstream | Паттерн | Описание |
|----------|-----------|---------|----------|
| Identity | Billing | Customer/Supplier | Billing получает информацию о пользователях |
| Identity | Notification | Published Language | Стандартные события UserCreated, RoleAssigned |
| Gateway | Identity | Conformist | Gateway конформен к API Identity |

## Planned Changes

*Нет запланированных изменений.*

## Changelog

*Нет записей.*
```

**Допустимые дополнительные секции:** визуализация (ASCII-диаграмма), Anti-Corruption Layers.

---

## 5. Шаблоны

Шаблоны используются при инициализации проекта. Пустой шаблон содержит структуру секций с placeholder-ами.

### 5.1 Шаблон system/overview.md

`````markdown
---
description: Обзор системной архитектуры — сервисы, потоки данных, инфраструктура.
---

# Обзор системной архитектуры

## Домены и сервисы

| Сервис | Назначение | Ключевые API |
|--------|-----------|-------------|
| {service} | {назначение} | {endpoints} |

## Потоки данных

{Высокоуровневая карта: кто с кем общается, через что}

## Инфраструктура

{Deployment, networking, мониторинг — краткая сводка}

## Planned Changes

*Нет запланированных изменений.*

## Changelog

*Нет записей.*
`````

### 5.2 Шаблон system/data-flows.md

`````markdown
---
description: Потоки данных между сервисами — участники, контракты, паттерны взаимодействия.
---

# Потоки данных

## {от} → {к}: {назначение}

| Поле | Значение |
|------|----------|
| Участники | {от} ({роль}) → {к} ({роль}) |
| Контракт | {контракт} |
| Паттерн | {sync/gRPC | async/events} |
| Протокол | {протокол} |

## Planned Changes

*Нет запланированных изменений.*

## Changelog

*Нет записей.*
`````

### 5.3 Шаблон system/infrastructure.md

`````markdown
---
description: Инфраструктура проекта — deployment, networking, мониторинг.
---

# Инфраструктура

## Deployment

| Окружение | Технология | Конфигурация |
|-----------|-----------|-------------|
| dev | {технология} | config/dev/ |
| staging | {технология} | config/staging/ |
| prod | {технология} | config/prod/ |

## Networking

{Путь запроса, DNS, Network Policies}

## Мониторинг

{Метрики, логи, трейсинг, алерты}

## Planned Changes

*Нет запланированных изменений.*

## Changelog

*Нет записей.*
`````

### 5.4 Шаблон domains/context-map.md

`````markdown
---
description: Карта взаимодействия между bounded contexts — домены, ответственности, паттерны связей.
---

# Context Map

## Домены

### {Domain Name} — {краткое описание}

**Ответственность:** {что делает домен}

**Сервисы:** `{service1}`, `{service2}`

**Ключевые инварианты:**
- {инвариант 1}

## Связи между контекстами

| Upstream | Downstream | Паттерн | Описание |
|----------|-----------|---------|----------|
| {Domain1} | {Domain2} | {паттерн} | {описание} |

## Planned Changes

*Нет запланированных изменений.*

## Changelog

*Нет записей.*
`````

---

## 6. Чек-лист качества

### Существование
- [ ] `system/overview.md` существует
- [ ] `system/data-flows.md` существует
- [ ] `system/infrastructure.md` существует
- [ ] `domains/context-map.md` существует

### Frontmatter
- [ ] Каждый файл содержит frontmatter (`---`)
- [ ] Поле `description` присутствует и непустое

### Обязательные секции

**overview.md:**
- [ ] `## Домены и сервисы` присутствует
- [ ] `## Потоки данных` присутствует
- [ ] `## Инфраструктура` присутствует
- [ ] `## Planned Changes` присутствует
- [ ] `## Changelog` присутствует

**data-flows.md:**
- [ ] `## Planned Changes` присутствует
- [ ] `## Changelog` присутствует

**infrastructure.md:**
- [ ] `## Deployment` присутствует
- [ ] `## Networking` присутствует
- [ ] `## Мониторинг` присутствует
- [ ] `## Planned Changes` присутствует
- [ ] `## Changelog` присутствует

**context-map.md:**
- [ ] `## Домены` присутствует
- [ ] `## Связи между контекстами` присутствует
- [ ] `## Planned Changes` присутствует
- [ ] `## Changelog` присутствует

### Согласованность
- [ ] При добавлении нового сервиса в `specs/services/` — файлы architecture/ обновлены
