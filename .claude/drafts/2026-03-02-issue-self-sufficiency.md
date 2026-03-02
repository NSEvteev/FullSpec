# Issue как самодостаточная задача для разработки

Переработка флоу создания Issues — обогащение body контекстом из Design и Plan Test, чтобы разработчик (LLM или человек) мог работать по Issue без обращения к specs/.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Проблема: Issue #56](#1-проблема-issue-56)
  - [2. Что нужно для разработки](#2-что-нужно-для-разработки)
  - [3. Предлагаемая структура body](#3-предлагаемая-структура-body)
  - [4. Секция "Контекст реализации"](#4-секция-контекст-реализации)
  - [5. Изменения в стандартах Issues](#5-изменения-в-стандартах-issues)
  - [6. Изменения в /dev-create](#6-изменения-в-dev-create)
  - [7. Изменения в Plan Dev](#7-изменения-в-plan-dev)
  - [8. Миграция существующих Issues](#8-миграция-существующих-issues)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)
- [Затронутые файлы](#затронутые-файлы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** Issue #56 (и все остальные #42-#61) содержат минимальный body — указатель на документы, а не самодостаточную задачу.
**Почему создан:** Разработчик не может написать код, читая только Issue. Нужно переработать процесс создания Issues, чтобы body содержал достаточно контекста.
**Связанные файлы:**
- `.github/.instructions/issues/standard-issue.md` — стандарт Issues (§ 4 Body)
- `.github/.instructions/issues/create-issue.md` — воркфлоу создания Issue
- `.github/.instructions/development/create-development.md` — воркфлоу /dev-create
- `specs/.instructions/analysis/plan-dev/standard-plan-dev.md` — стандарт Plan Dev (поле Источник)
- `specs/analysis/0001-task-dashboard/design.md` — Design с API-контрактами
- `specs/analysis/0001-task-dashboard/plan-test.md` — Plan Test с acceptance-критериями

---

## Содержание

### 1. Проблема: Issue #56

[Issue #56](https://github.com/NSEvteev/project_template/issues/56) — "Реализовать аутентификацию LoginPage и authStore (TASK-15)".

Что видит разработчик:

```markdown
## Описание

Zustand authStore (token, user, login, logout), LoginPage с формой email/password,
ProtectedRoute, роутинг /login + / (protected).

**Сложность:** 5/10 | **Wave:** 2 (frontend) | **TC:** TC-28, TC-29, TC-30
**Зависит от:** #55

## Связанная документация

- Plan Dev — specs/analysis/0001-task-dashboard/plan-dev.md (TASK-15)
- Design SVC-3 § 4, § 5, INT-2 — specs/analysis/0001-task-dashboard/design.md

## Критерии готовности

- [ ] 15.1. authStore.ts (Zustand): token, user, login(), logout()
- [ ] 15.2. LoginPage.tsx: форма с email/password, обработка ошибок
- [ ] 15.3. Вызов auth.api.login → сохранение token в localStorage + authStore
- [ ] 15.4. ProtectedRoute: компонент-обёртка, редирект на /login при отсутствии JWT
- [ ] 15.5. App.tsx: роутинг /login (публичный) + / (protected)
```

Формально соответствует standard-issue.md (Описание + Связанная документация + Критерии готовности). Но по нему **невозможно разработать**: описание — одна строка-перечисление, нет API-контрактов, нет технических решений, нет acceptance-критериев.

### 2. Что нужно для разработки

Для написания кода по #56 разработчик ДОЛЖЕН прочитать:
- **Design SVC-3 § 4** (API) — какой эндпоинт вызывать, формат запроса/ответа
- **Design SVC-3 § 5** (Tech Stack) — Zustand? Jotai? Версия React Router?
- **Design INT-2** (Интеграция) — как frontend общается с auth-сервисом
- **Plan Dev TASK-15** — подзадачи (те же, что в Issue)
- **Plan Test TC-28, TC-29, TC-30** — acceptance-критерии

Issue — указатель на документы, а НЕ самодостаточная задача.

Почему это плохо:
1. **Для LLM (dev-agent):** нужно собирать контекст из 3-5 файлов перед началом работы
2. **Для человека:** Issue на GitHub бесполезен без доступа к specs/
3. **Для ревьюера:** не видит ожидания, не может сверить результат
4. **Дублирование навигации:** каждый раз заново искать нужные секции Design

### 3. Предлагаемая структура body

```markdown
## Описание

Реализовать аутентификацию на фронтенде: Zustand-стор для хранения
JWT-токена и данных пользователя, страницу логина с формой email/password,
компонент ProtectedRoute для защиты маршрутов и роутинг приложения.

**Сложность:** 5/10 | **Wave:** 2 (frontend) | **Сервис:** frontend
**Зависит от:** #55 (API-слой и TanStack Query хуки)

## Контекст реализации

### API-контракты (из Design)

POST /api/auth/login
- Request: { email: string, password: string }
- Response 200: { token: string, user: { id, email, name, role } }
- Response 401: { error: "Invalid credentials" }

### Технические решения (из Design)

- State management: Zustand 5.x (authStore)
- Routing: React Router 7 (ProtectedRoute pattern)
- Token storage: localStorage (JWT)
- HTTP client: ky (через api.ts из TASK-14)

### Acceptance-критерии (из Plan Test)

- TC-28: Пользователь вводит корректный email/password → редирект на / → видит дашборд
- TC-29: Пользователь вводит неверный пароль → сообщение об ошибке, остаётся на /login
- TC-30: Неавторизованный пользователь на / → редирект на /login

## Критерии готовности

- [ ] 15.1. authStore.ts (Zustand): token, user, login(), logout()
- [ ] 15.2. LoginPage.tsx: форма с email/password, обработка ошибок
- [ ] 15.3. Вызов auth.api.login → сохранение token в localStorage + authStore
- [ ] 15.4. ProtectedRoute: компонент-обёртка, редирект на /login при отсутствии JWT
- [ ] 15.5. App.tsx: роутинг /login (публичный) + / (protected)

## Связанная документация

- Plan Dev TASK-15 — specs/analysis/0001-task-dashboard/plan-dev.md
- Design SVC-3 § 4, § 5, INT-2 — specs/analysis/0001-task-dashboard/design.md
- Plan Test TC-28..TC-30 — specs/analysis/0001-task-dashboard/plan-test.md
```

### 4. Секция "Контекст реализации"

Ключевое отличие — новая секция между "Описание" и "Критерии готовности":

| Подсекция | Источник | Что содержит |
|-----------|----------|-------------|
| API-контракты | Design SVC-N § 4 | Эндпоинты, request/response, status codes |
| Технические решения | Design SVC-N § 5 | Конкретные библиотеки, паттерны, версии |
| Acceptance-критерии | Plan Test TC-N | Сценарии на естественном языке |

Алгоритм сбора (при `/dev-create`):
1. Из поля `Источник` TASK-N определить SVC-N и секции Design
2. Прочитать Design SVC-N § 4 (API) → извлечь эндпоинты для этой задачи
3. Прочитать Design SVC-N § 5 (Tech Stack) → извлечь ключевые решения
4. Из поля `TC` прочитать Plan Test TC-N → извлечь acceptance-сценарии
5. Собрать секцию "Контекст реализации"

Описание Issue: 2-3 предложения, объясняющие ЧТО и ЗАЧЕМ (не одна строка-перечисление).

### 5. Изменения в стандартах Issues

**standard-issue.md** — § 4 Body:
- Добавить секцию "Контекст реализации" между "Описание" и "Критерии готовности"
- Опциональна для ручных Issues, обязательна при создании из Plan Dev
- Обновить "Полный пример body"
- Bump версии + `/migration-create`

**create-issue.md** — Шаг 4 "Заполнить body":
- Добавить алгоритм сбора контекста из Design и Plan Test (5 шагов из § 4)
- Batch-создание: тот же алгоритм для каждого TASK-N

**validate-issue.py**:
- Warning (не error) при отсутствии "Контекст реализации" для Issues из Plan Dev

### 6. Изменения в /dev-create

**create-development.md** — Шаг 3 "Создать GitHub Issues":
- Вместо краткого body из plan-dev — собирать полный body с "Контекст реализации"
- Алгоритм: для каждого TASK-N → Источник → Design SVC-N §§ → TC-N → body
- Описание: 2-3 предложения (не одна строка-перечисление)

### 7. Изменения в Plan Dev

**standard-plan-dev.md** — поле `Источник`:
- Уже существует, но нужно усилить правило: Источник ДОЛЖЕН быть достаточно точным для навигации по Design (SVC-N § {номер секции})
- Это поле используется при `/dev-create` для сбора контекста в Issue body

### 8. Миграция существующих Issues

Issues #42-#61 — обогатить body контекстом:
1. Для каждого TASK-N прочитать Design SVC-N §§ (из поля Источник)
2. Прочитать Plan Test TC-N (из поля TC)
3. Собрать секцию "Контекст реализации"
4. Расширить описание (2-3 предложения вместо одной строки)
5. Обновить body: `gh issue edit N --body "..."`

Можно автоматизировать: скрипт читает plan-dev.md → design.md → plan-test.md → генерирует body.

---

## Решения

- **Глубина контекста: минимум** — API-контракты + ключевые решения + acceptance. Issue должен быть читаемым, а не копией Design
- **Синхронизация: snapshot** — Issue = snapshot на момент создания. Ссылки на SSOT-документы для актуальной версии сохраняются в "Связанная документация"
- **Коллапсируемые секции** — использовать `<details>` для контекста реализации, если body слишком длинный

---

## Открытые вопросы

1. **Размер Issue** — 20 Issues с полным контекстом → body может быть 50-100 строк. Приемлемо ли это, или использовать `<details>` для свёртки?
2. **Связь с dev-agent** — dev-agent сейчас читает Plan Dev и Design напрямую. Если Issue самодостаточен → dev-agent может работать только по Issue? Или Issue для людей, а dev-agent по-прежнему читает specs/?
3. **INFRA-задачи** — TASK-1 (монорепо) не привязан к SVC-N. Откуда брать контекст реализации? Из Design § Инфраструктура?

---

## Затронутые файлы

| Файл | Изменение |
|------|-----------|
| `.github/.instructions/issues/standard-issue.md` | § 4 Body — секция "Контекст реализации" + миграция |
| `.github/.instructions/issues/create-issue.md` | Шаг 4 — алгоритм обогащения |
| `.github/.instructions/development/create-development.md` | Шаг 3 — сбор контекста |
| `.github/.instructions/issues/issue-templates/` | Обновление шаблонов |
| `specs/.instructions/analysis/plan-dev/standard-plan-dev.md` | Правило для поля Источник |
| `.github/.instructions/.scripts/validate-issue.py` | Warning: проверка "Контекст реализации" |
| Issues #42-#61 | Миграция body |

---

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

TASK 1: Обновить standard-issue.md — секция "Контекст реализации"
  description: >
    Драфт: .claude/drafts/2026-03-02-issue-self-sufficiency.md (секция "5. Изменения в стандартах Issues")
    Обновить `.github/.instructions/issues/standard-issue.md`:
    - § 4 Body — добавить секцию "Контекст реализации" между "Описание" и "Критерии готовности"
    - Определить: опциональна для ручных Issues, обязательна при создании из Plan Dev
    - Три подсекции: API-контракты (Design § 4), Технические решения (Design § 5), Acceptance-критерии (Plan Test TC-N)
    - Обновить "Полный пример body"
    - Bump версии
    Запустить `/migration-create` после изменения.
  activeForm: Обновление standard-issue.md

TASK 2: Обновить create-issue.md — алгоритм обогащения body
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-03-02-issue-self-sufficiency.md (секция "4. Секция Контекст реализации")
    Обновить `.github/.instructions/issues/create-issue.md`:
    - Шаг 4 "Заполнить body" — добавить алгоритм сбора контекста (5 шагов):
      1. Из поля Источник TASK-N определить SVC-N и секции Design
      2. Прочитать Design SVC-N § 4 → извлечь эндпоинты
      3. Прочитать Design SVC-N § 5 → извлечь решения
      4. Из поля TC прочитать Plan Test TC-N → acceptance-сценарии
      5. Собрать секцию "Контекст реализации"
    - Batch-создание: тот же алгоритм для каждого TASK-N
    - Обновить примеры
  activeForm: Обновление create-issue.md

TASK 3: Обновить create-development.md — обогащение body при /dev-create
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-03-02-issue-self-sufficiency.md (секция "6. Изменения в /dev-create")
    Обновить `.github/.instructions/development/create-development.md`:
    - Шаг 3 "Создать GitHub Issues": вместо краткого body
      собирать полный body с "Контекст реализации" из Design + Plan Test.
    - Описание Issue: 2-3 предложения (НЕ одна строка-перечисление).
    - Описать алгоритм: для каждого TASK-N → Источник → SVC-N §§ → TC-N → body.
  activeForm: Обновление create-development.md

TASK 4: Обновить issue-templates — секция "Контекст реализации"
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-03-02-issue-self-sufficiency.md (секция "5. Изменения в стандартах Issues")
    Обновить шаблоны в `.github/.instructions/issues/issue-templates/`:
    - task.yml: добавить опциональную секцию "Контекст реализации" (`required: false`)
    - Обновить standard-issue-template.md
  activeForm: Обновление Issue Templates

TASK 5: Обновить standard-plan-dev.md — правило для поля Источник
  description: >
    Драфт: .claude/drafts/2026-03-02-issue-self-sufficiency.md (секция "7. Изменения в Plan Dev")
    Обновить правило для поля Источник в `standard-plan-dev.md`:
    - Источник ДОЛЖЕН быть достаточно точным: SVC-N § {номер секции}
    - Добавить примеры хороших и плохих значений
    - Указать: поле используется при `/dev-create` для сбора контекста
    Если bump версии — запустить `/migration-create`.
  activeForm: Обновление правила Источник

TASK 6: Обновить validate-issue.py — проверка "Контекст реализации"
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-03-02-issue-self-sufficiency.md (секция "5. Изменения в стандартах Issues")
    Добавить проверку в validate-issue.py:
    - Если Issue создан из Plan Dev (определяется по ссылке на TASK-N в body) →
      проверить наличие секции "## Контекст реализации"
    - Warning (не error) при отсутствии — обратная совместимость
  activeForm: Обновление validate-issue.py

TASK 7: Миграция существующих Issues #42-#61
  blockedBy: [3]
  description: >
    Драфт: .claude/drafts/2026-03-02-issue-self-sufficiency.md (секция "8. Миграция существующих Issues")
    Для каждого из 20 Issues:
    1. Прочитать Design SVC-N §§ (из поля Источник TASK-N)
    2. Прочитать Plan Test TC-N (из поля TC)
    3. Собрать секцию "Контекст реализации"
    4. Расширить описание (2-3 предложения вместо одной строки)
    5. Обновить body: `gh issue edit N --body "..."`
    Можно автоматизировать скриптом.
  activeForm: Миграция body Issues

TASK 8: Валидация
  blockedBy: [1, 2, 3, 4, 5, 6, 7]
  description: >
    Драфт: .claude/drafts/2026-03-02-issue-self-sufficiency.md (весь документ)
    Валидация всех изменений:
    1. `/issue-validate --all` — все Issues
    2. `/migration-validate` — дрифт стандартов
    3. Визуальная проверка: открыть Issue #56 на GitHub → body самодостаточен
  activeForm: Валидация изменений
