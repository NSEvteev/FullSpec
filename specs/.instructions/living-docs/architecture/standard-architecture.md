---
description: Стандарт живых документов архитектуры — Code Map, Tech Stack, границы автономии LLM, технологические стандарты, Planned Changes.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/.instructions/living-docs/architecture/README.md
---

# Стандарт живых документов архитектуры

Версия стандарта: 1.0

Правила создания и обновления живых документов архитектуры (`specs/architecture/`). Code Map, Tech Stack, границы автономии LLM, технологические стандарты, Planned Changes.

**Полезные ссылки:**
- [Справочник SDD](../../standard-specs-reference.md) — статусы, каскады, живые документы (таблица)
- [Навигатор SDD](../../standard-specs-workflow.md) — полный воркфлоу
- [Инструкции specs/](../../README.md)
- [Архитектура specs/ (черновик)](/.claude/drafts/examples/2026-02-08-specs-architecture.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Справочник | [standard-specs-reference.md](../../standard-specs-reference.md) |
| Навигатор | [standard-specs-workflow.md](../../standard-specs-workflow.md) |
| ADR | [standard-adr.md](../../adr/standard-adr.md) *(будет создан)* |
| Design | [standard-design.md](../../design/standard-design.md) *(будет создан)* |
| Валидация | — |
| Создание | — |
| Модификация | — |

## Оглавление

- [1. Структура architecture/](#1-структура-architecture)
- [2. Code Map](#2-code-map)
  - [Проблема](#проблема)
  - [Решение](#решение)
  - [Содержимое Code Map](#содержимое-code-map)
  - [Границы автономии LLM](#границы-автономии-llm)
- [3. Технологические стандарты](#3-технологические-стандарты)
  - [Расположение и формат](#расположение-и-формат)
  - [Автозагрузка через rules](#автозагрузка-через-rules)
  - [Триггер создания — ADR](#триггер-создания--adr)
  - [Связь Code Map ↔ Tech Stack ↔ Rules](#связь-code-map--tech-stack--rules)
- [4. Planned Changes](#4-planned-changes)

---

## 1. Структура architecture/

```
specs/architecture/
├── system/                        # Системная архитектура
│   ├── overview.md                #   Сервисы, потоки, высокоуровневая карта
│   ├── data-flows.md             #   Потоки данных между сервисами
│   └── infrastructure.md         #   Deployment, networking, monitoring
├── services/                      # Per-service архитектура
│   └── {service}.md               #   Компоненты, tech stack, API, data model, Code Map
├── domains/                       # Доменная архитектура (DDD)
│   ├── {domain}.md                #   Один файл на bounded context
│   └── context-map.md             #   Карта взаимодействия контекстов
└── README.md
```

| Папка | Что хранит | Обновляется при |
|-------|-----------|-----------------|
| `system/` | Системная архитектура: overview, data-flows, infrastructure | Design → DONE |
| `services/{svc}.md` | Архитектура сервиса: компоненты, API, data model, **Code Map**, **Planned Changes** | ADR → DONE (+ Planned Changes при Design → WAITING) |
| `domains/` | Bounded contexts, агрегаты, события, context map | Design → DONE |

**Создание vs обновление:** При первом обращении файл **создаётся** (первый Design → DONE создаёт `system/`, `domains/`; первый ADR → DONE создаёт `services/{svc}.md`). При последующих — **обновляется** (AS IS → TO BE).

**Паттерн AS IS / TO BE:** LLM читает живые документы (включая Planned Changes) перед проектированием. Изменения фиксируются в объектах (TO BE), а при завершении — переносятся в живые документы (новый AS IS).

---

## 2. Code Map

### Проблема

Между `architecture/services/{svc}.md` (высокоуровневое описание сервиса) и реальным кодом в `src/{svc}/` существует навигационный разрыв. Когда LLM берёт задачу из GitHub Issue, он знает ЧТО делать (План разработки), КАК проверить (План тестов), КАКОЕ решение принято (ADR) — но не знает КУДА СМОТРЕТЬ в коде и ЧТО МОЖНО МЕНЯТЬ самостоятельно.

```
Issue → План разработки → План тестов → ADR → architecture/services/{svc}.md
                                          ↓
                                     Code Map     ← мост между спеками и кодом
                                          ↓
                                  src/{svc}/ (реальный код)
```

### Решение

Code Map — секция внутри `architecture/services/{svc}.md`. Описывает внутреннюю структуру сервиса на уровне **пакетов/модулей** (не файлов).

**Почему не per-file спецификации:**

| Проблема per-file спеков | Как Code Map её избегает |
|--------------------------|------------------------|
| **Синхронизация** — 200 файлов = 200 точек рассинхронизации | Описание на уровне пакетов (5-15 на сервис), обновляется при ADR → DONE |
| **Дублирование** — спек повторяет docstrings и type hints | Code Map описывает навигацию и границы, не реализацию |
| **Масштаб** — невозможно поддерживать вручную | Пакеты меняются редко, файлы — постоянно |
| **Мультиязычность** — docstring формат зависит от языка | Пакет/модуль — универсальная абстракция (Python package, TS module, Go package) |

### Содержимое Code Map

```markdown
## Code Map

### Tech Stack

| Технология | Стандарт | Валидация | Назначение |
|-----------|---------|-----------|-----------|
| Python 3.12 | [standard-python.md] | [validation-python.md] | Бэкенд |
| PostgreSQL 16 | [standard-postgresql.md] | [validation-postgresql.md] | Хранение |
| FastAPI | [standard-fastapi.md] | [validation-fastapi.md] | API-фреймворк |

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

### Внешние зависимости

- `shared/events/` — UserCreatedEvent (publisher)
- `shared/contracts/` — protobuf-схемы для gateway

### Границы автономии LLM

- **Свободно:** реализация внутри пакета (алгоритмы, рефакторинг, оптимизация)
- **Флаг:** изменение контрактов между пакетами (может затронуть План тестов)
- **CONFLICT:** изменение API сервиса, data model, добавление/удаление пакетов (затрагивает ADR)
```

### Границы автономии LLM

Ключевая секция Code Map. Явно говорит LLM при выполнении задачи:

- **Свободно** — можно менять без согласования. Реализация, рефакторинг, оптимизация внутри пакета.
- **Флаг** — можно менять, но нужно сообщить. Изменение может затронуть тестовые сценарии (План тестов). LLM информирует, но не блокируется.
- **CONFLICT** — нельзя менять самостоятельно. Изменение затрагивает архитектурные решения (ADR). Требуется обратная связь Code → Specs.

Эти три уровня напрямую связаны с механизмом обратной связи Code → Specs ([§ 4 Справочника](../../standard-specs-reference.md#4-обратная-связь-code-specs)): "свободно" = нет обратной связи, "флаг" = рабочие правки, "CONFLICT" = уровень ADR и выше.

**Когда обновляется:** При ADR → DONE — как часть обычного каскада обновления `architecture/services/{svc}.md`. Не требует отдельного процесса.

---

## 3. Технологические стандарты

### Расположение и формат

Code Map говорит LLM КУДА смотреть и ЧТО можно менять. Но не говорит КАК писать код — какие конвенции приняты в проекте для конкретных языков, фреймворков и технологий.

Технологические стандарты — пара `standard-{tech}.md` + `validation-{tech}.md` в `.instructions/technologies/`. Тот же паттерн, что и для остальных инструкций проекта.

```
.instructions/
├── technologies/
│   ├── standard-python.md
│   ├── validation-python.md
│   ├── standard-typescript.md
│   ├── validation-typescript.md
│   ├── standard-tailwind.md
│   ├── validation-tailwind.md
│   ├── standard-postgresql.md
│   ├── validation-postgresql.md
│   └── README.md
```

**Почему `.instructions/technologies/`, а не `specs/.instructions/`:** Стандарты применяются к **коду**, не к спецификациям. Загружаются при работе с файлами кода. Проектный уровень.

**Содержимое standard-{tech}.md** — конкретные правила с примерами, не абстрактные принципы:

```markdown
# standard-python.md

## Module docstring (обязательно)
"""
Модуль: {package}.{module}
Назначение: {что делает}
Зависимости: {от кого зависит}
Контракт: {публичные функции → типы}
"""

## Imports (порядок)
1. stdlib
2. third-party
3. project shared/
4. local package

## Error handling
- Кастомные исключения наследуют ServiceError
- Никогда bare except
```

### Автозагрузка через rules

Каждый стандарт подключается как rule, активируемый при работе с соответствующими файлами:

```markdown
# .claude/rules/python.md
При работе с Python-файлами (*.py) ОБЯЗАТЕЛЬНО следовать:
- [standard-python.md](/.instructions/technologies/standard-python.md)
- [validation-python.md](/.instructions/technologies/validation-python.md)
```

LLM автоматически получает стандарт при работе с файлами соответствующего типа.

### Триггер создания — ADR

Когда ADR вводит новую технологию ("используем Tailwind для стилизации"):

1. Проверить: существует ли `standard-tailwind.md`?
2. Если нет → создать `standard-tailwind.md` + `validation-tailwind.md` + rule в `.claude/rules/`
3. Если да → ADR ссылается на существующий стандарт

Это часть каскада ADR → DONE: технология введена → стандарт создан → rule активирован → Code Map в `architecture/services/{svc}.md` ссылается на стандарт в секции Tech Stack.

### Связь Code Map ↔ Tech Stack ↔ Rules

```
ADR вводит технологию
  → standard-{tech}.md + validation-{tech}.md в .instructions/technologies/
  → rule в .claude/rules/ (автозагрузка по типу файла)
  → Code Map → Tech Stack (ссылки на стандарт и валидацию)

LLM берёт задачу из Issue
  → Plan → ADR → Code Map → Tech Stack (какие стандарты)
  → rule автоматически загружает стандарт при работе с файлами
  → LLM пишет код по стандарту
  → validation проверяет соответствие
```

---

## 4. Planned Changes

Формат секции Planned Changes в файлах `architecture/`:

```markdown
## Planned Changes

- **[Discussion 001: OAuth2 авторизация](../discussion/disc-0001-oauth2-authorization.md)**
  Статус: RUNNING | Затрагивает: API endpoints, data model
  Design: [design-0001-oauth2-service-design.md](../design/design-0001-oauth2-service-design.md)
```

**Правила:**
- Добавляется когда Design переходит в WAITING
- LLM при чтении AS IS **обязан** учитывать Planned Changes
- При необходимости LLM переходит по ссылке на Design и читает дочерние ADR (через frontmatter `children`) для получения конкретных дельт
- Planned Changes — навигационный указатель на цепочку спецификаций, не дублирование контента. Обогащение дельтами из ADR не производится: дельты могут измениться при CONFLICT, а дублирование нарушает SSOT
- Секция применяется при обновлении живого документа (ADR → DONE): запланированные изменения переносятся в основной контент, секция убирается. При любом переходе связанного документа в REJECTED (включая сам Design) — секция убирается без применения
