# Расширение TYPE-меток GitHub

Добавление `feature`, `infra`, `test` к существующим TYPE-меткам и интеграция определения типа в процесс создания задач (Plan Dev → Issues).

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Проблема](#1-проблема)
  - [2. Предлагаемые TYPE-метки](#2-предлагаемые-type-метки)
  - [3. Изменения в labels](#3-изменения-в-labels)
  - [4. Изменения в Issues](#4-изменения-в-issues)
  - [5. Изменения в Plan Dev](#5-изменения-в-plan-dev)
  - [6. Изменения в /dev-create](#6-изменения-в-dev-create)
  - [7. Issue Templates](#7-issue-templates)
  - [8. Миграция существующих Issues](#8-миграция-существующих-issues)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [Затронутые файлы](#затронутые-файлы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** При `/dev-create 0001` все 20 TASK-N получили метку `task` — метка теряет смысл как фильтр.
**Почему создан:** Нужно расширить набор TYPE-меток и встроить определение типа в процесс создания задач.
**Связанные файлы:**
- `.github/labels.yml` — справочник меток
- `.github/.instructions/labels/standard-labels.md` — стандарт меток
- `.github/.instructions/issues/standard-issue.md` — стандарт Issues
- `.github/.instructions/issues/create-issue.md` — воркфлоу создания Issue
- `specs/.instructions/analysis/plan-dev/standard-plan-dev.md` — стандарт Plan Dev
- `.github/.instructions/development/create-development.md` — воркфлоу /dev-create

---

## Содержание

### 1. Проблема

Сейчас в labels.yml 4 TYPE-метки: `bug`, `task`, `docs`, `refactor`.

При создании Issues из Plan Dev (`/dev-create`) ВСЕ 20 задач получили `task`:
- TASK-1 (монорепо, docker-compose) — `task`
- TASK-5 (CRUD-эндпоинты) — `task`
- TASK-16 (канбан-доска с drag-and-drop) — `task`
- TASK-19 (E2E тесты) — `task`
- TASK-20 (нагрузочные тесты) — `task`

Scaffold сервиса, бизнес-логика, UI-компонент, системные тесты, инфраструктура — всё `task`. Фильтрация по типу бесполезна.

### 2. Предлагаемые TYPE-метки

| Метка | Описание | Когда | Примеры (0001) |
|-------|----------|-------|----------------|
| `feature` | Новая функциональность | Новый эндпоинт, UI-компонент, бизнес-логика | TASK-5 CRUD, TASK-16 канбан, TASK-10 Login |
| `infra` | Инфраструктура | Docker, CI/CD, монорепо, конфиги | TASK-1 монорепо |
| `test` | Тесты | E2E, integration, load, smoke | TASK-19 E2E, TASK-20 нагрузка |
| `task` | Техническая задача | Scaffold, middleware, схемы, boilerplate | TASK-2 scaffold, TASK-4 JWT-middleware |
| `bug` | Баг | Как есть | — |
| `docs` | Документация | Как есть | — |
| `refactor` | Рефакторинг | Как есть | — |

Итого: 7 TYPE-меток (было 4, добавляются 3).

### 3. Изменения в labels

**labels.yml** — добавить 3 метки в секцию TYPE:
```yaml
- name: "feature"
  description: "✨ Новая функциональность"
  color: "..."  # подобрать

- name: "infra"
  description: "🏗️ Инфраструктура"
  color: "..."

- name: "test"
  description: "🧪 Тесты"
  color: "..."
```

**standard-labels.md** — обновить:
- § 3 "Правила применения" — таблица критериев выбора TYPE (7 строк)
- Примеры применения — добавить для feature, infra, test
- Bump версии + `/migration-create`

### 4. Изменения в Issues

**standard-issue.md** — § 4 Labels:
- Расширить: "Ровно 1 метка типа (bug, task, docs, refactor)" → "(bug, task, docs, refactor, feature, infra, test)"
- Обновить примеры

**create-issue.md** — Шаг 3 "Определить шаблон":
- Таблица контекст → шаблон → метка TYPE (7 строк вместо 4)
- Шаг 5 "Определить labels" — обновить

**validate-issue.py** — обновить список допустимых TYPE-меток.

### 5. Изменения в Plan Dev

**standard-plan-dev.md** — добавить поле `Type` в формат TASK-N:

```markdown
#### TASK-N: {title}
- **Сложность:** N/10
- **Приоритет:** high/medium/low
- **Зависимости:** TASK-M / —
- **TC:** TC-N / INFRA
- **Источник:** SVC-N § M
- **Issue:** — (заполняется при /dev-create)
- **Type:** feature / task / infra / test
```

Type — 8-е поле, опциональное при DRAFT/WAITING (как Issue). При создании Plan Dev LLM определяет тип из контекста задачи.

Критерии выбора:
- INFRA-блок (TC: INFRA) → `infra`
- Acceptance TC-N с бизнес-логикой (CRUD, UI, API) → `feature`
- Системные тесты (TC: STS-N или E2E/load/integration) → `test`
- Scaffold, middleware, схемы, boilerplate → `task`

### 6. Изменения в /dev-create

**create-development.md** — Шаг 3 "Создать GitHub Issues":
- Если TASK-N имеет поле Type → использовать как TYPE-метку
- Если поле Type отсутствует (старые plan-dev) → определить автоматически по критериям из § 5

### 7. Issue Templates

Рекомендация: один шаблон `task.yml` для всех типов. TYPE определяется меткой, а не шаблоном — секции body одинаковые для feature/task/infra/test.

Альтернатива: отдельные шаблоны (feature.yml, infra.yml, test.yml) — если в будущем секции body будут отличаться.

### 8. Миграция существующих Issues

Issues #42-#61 — пересмотреть метку `task` на правильный TYPE:

| Issues | Текущий TYPE | Новый TYPE | Причина |
|--------|-------------|-----------|---------|
| #42 | task | infra | Монорепо, docker-compose, shared |
| #43, #49, #54 | task | task | Scaffold сервисов |
| #44, #50 | task | task | Zod-схемы (boilerplate) |
| #45 | task | task | JWT-middleware |
| #46, #47, #48 | task | feature | CRUD, фильтрация, история |
| #51, #52, #53 | task | feature | Login, Validate, Users эндпоинты |
| #55 | task | task | API-слой (инфраструктурный) |
| #56-#59 | task | feature | UI-компоненты (LoginPage, канбан, формы) |
| #60 | task | test | E2E и integration тесты |
| #61 | task | test | Нагрузочные тесты |

---

## Решения

- **Явное поле Type в TASK-N** (не автоопределение) — надёжнее, прозрачнее, воспроизводимо
- **Один шаблон task.yml** для всех типов — проще поддерживать, TYPE через метку

---

## Открытые вопросы

1. **Цвета для новых меток** — подобрать из палитры, не конфликтуя с существующими
2. **Маппинг TASK-N → TYPE для пограничных случаев** — например, TASK-4 (JWT-middleware): это `task` или `feature`? Middleware — инфраструктурный boilerplate, но с бизнес-логикой авторизации
3. **Обратная совместимость** — старые plan-dev без поля Type: `/dev-create` должен уметь определять тип автоматически

---

## Затронутые файлы

| Файл | Изменение |
|------|-----------|
| `.github/labels.yml` | +3 метки (feature, infra, test) |
| `.github/.instructions/labels/standard-labels.md` | § 3, примеры, bump + миграция |
| `.github/.instructions/issues/standard-issue.md` | § 4 Labels |
| `.github/.instructions/issues/create-issue.md` | Шаг 3, 5 |
| `.github/.instructions/issues/issue-templates/` | Опционально: обновить task.yml |
| `specs/.instructions/analysis/plan-dev/standard-plan-dev.md` | Поле Type в TASK-N + миграция |
| `.github/.instructions/development/create-development.md` | Шаг 3 — TYPE логика |
| `.github/.instructions/.scripts/validate-issue.py` | Список TYPE |
| Issues #42-#61 | Миграция меток |

---

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

TASK 1: Добавить TYPE-метки в labels.yml и GitHub
  description: >
    Драфт: .claude/drafts/2026-03-02-expand-type-labels.md (секция "3. Изменения в labels")
    Добавить `feature`, `infra`, `test` в секцию TYPE файла `.github/labels.yml`.
    Подобрать цвета (не конфликтующие с существующими).
    Синхронизировать с GitHub: `gh label create` для каждой новой метки.
    Валидация: `python .github/.instructions/.scripts/validate-labels.py --file`.
  activeForm: Добавление TYPE-меток

TASK 2: Обновить standard-labels.md
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-03-02-expand-type-labels.md (секция "3. Изменения в labels")
    Обновить `.github/.instructions/labels/standard-labels.md`:
    - § 3 "Правила применения" — таблица критериев выбора TYPE (7 строк вместо 4)
    - Примеры применения — добавить для feature, infra, test
    - Bump версии стандарта
    Запустить `/migration-create` после изменения стандарта.
  activeForm: Обновление standard-labels.md

TASK 3: Обновить standard-issue.md и create-issue.md
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-03-02-expand-type-labels.md (секция "4. Изменения в Issues")
    standard-issue.md:
    - § 4 Labels — расширить список TYPE-меток до 7
    - Обновить примеры
    create-issue.md:
    - Шаг 3 "Определить шаблон" — таблица контекст → шаблон → метка TYPE (7 строк)
    - Шаг 5 "Определить labels" — обновить
    - Чек-лист — обновить список TYPE
    Запустить `/migration-create` для standard-issue.md.
  activeForm: Обновление стандартов Issues

TASK 4: Обновить issue-templates
  blockedBy: [3]
  description: >
    Драфт: .claude/drafts/2026-03-02-expand-type-labels.md (секция "7. Issue Templates")
    Решение из драфта: один шаблон task.yml + метка (секции одинаковые).
    Обновить task.yml description если нужно.
    Обновить standard-issue-template.md — список TYPE-меток.
  activeForm: Обновление Issue Templates

TASK 5: Обновить standard-plan-dev.md — поле Type в TASK-N
  description: >
    Драфт: .claude/drafts/2026-03-02-expand-type-labels.md (секция "5. Изменения в Plan Dev")
    Добавить поле `Type` (8-е поле, опциональное) в формат TASK-N:
    - Таблица "Формат задачи" — новая строка
    - Правила — критерии выбора TYPE для TASK-N (4 правила)
    - Шаблоны (§ 5, § 7) — добавить `- **Type:** —`
    - Чек-лист (§ 8) — добавить проверку
    - Примеры (§ 9) — добавить в 3 примера
    Bump версии. Запустить `/migration-create`.
  activeForm: Добавление поля Type в TASK-N

TASK 6: Обновить create-development.md — TYPE-логика при создании Issues
  blockedBy: [3, 5]
  description: >
    Драфт: .claude/drafts/2026-03-02-expand-type-labels.md (секция "6. Изменения в /dev-create")
    Шаг 3 "Создать GitHub Issues":
    - Если TASK-N имеет поле Type → использовать как TYPE-метку
    - Если поле Type отсутствует (старые plan-dev) → определить автоматически
    - Таблица маппинга: INFRA → infra, бизнес-логика → feature, тесты → test, boilerplate → task
  activeForm: Обновление create-development.md

TASK 7: Обновить validate-issue.py
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-03-02-expand-type-labels.md (секция "4. Изменения в Issues")
    Обновить список допустимых TYPE-меток в скрипте validate-issue.py:
    - Было: bug, task, docs, refactor
    - Стало: bug, task, docs, refactor, feature, infra, test
  activeForm: Обновление validate-issue.py

TASK 8: Миграция существующих Issues #42-#61
  blockedBy: [1, 7]
  description: >
    Драфт: .claude/drafts/2026-03-02-expand-type-labels.md (секция "8. Миграция существующих Issues")
    Для каждого из 20 Issues определить правильный TYPE по таблице из драфта.
    Обновить метки: `gh issue edit N --remove-label task --add-label {type}`.
    Не трогать Issues #35-#39 (уже docs).
  activeForm: Миграция TYPE-меток на Issues

TASK 9: Валидация
  blockedBy: [2, 3, 4, 5, 6, 7, 8]
  description: >
    Драфт: .claude/drafts/2026-03-02-expand-type-labels.md (весь документ)
    Валидация всех изменений:
    1. `/labels-validate` — labels.yml + GitHub sync
    2. `/issue-validate --all` — все Issues
    3. `/migration-validate` — дрифт стандартов
    4. `/plan-dev-validate` — plan-dev.md 0001
  activeForm: Валидация изменений
