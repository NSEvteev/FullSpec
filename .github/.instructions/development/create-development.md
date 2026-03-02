---
description: Воркфлоу запуска разработки по analysis chain — prerequisite check, создание Issues/Milestone/Branch, переход WAITING → RUNNING.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/development/README.md
---

# Воркфлоу запуска разработки

Рабочая версия стандарта: 1.4

Пошаговый процесс перехода analysis chain из WAITING в RUNNING.

**Полезные ссылки:**
- [Инструкции development](./README.md)
- [Стандарт локальной разработки § 0](./standard-development.md#0-запуск-разработки) — полный воркфлоу
- [Стандарт analysis chain § 6.2](/specs/.instructions/analysis/standard-analysis.md#62-waiting-to-running)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-development.md](./standard-development.md) |
| Валидация | [validation-development.md](./validation-development.md) |
| Создание | Этот документ |
| Модификация | [modify-development.md](./modify-development.md) |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить готовность цепочки](#шаг-1-проверить-готовность-цепочки)
  - [Шаг 2: Подтверждение пользователя](#шаг-2-подтверждение-пользователя)
  - [Шаг 3: Создать GitHub Issues](#шаг-3-создать-github-issues)
  - [Шаг 4: Создать/привязать Milestone](#шаг-4-создатьпривязать-milestone)
  - [Шаг 5: Перевести цепочку в RUNNING](#шаг-5-перевести-цепочку-в-running)
  - [Шаг 6: Коммит и Push в main](#шаг-6-коммит-и-push-в-main)
  - [Шаг 7: Создать ветку](#шаг-7-создать-ветку)
  - [Шаг 8: Отчёт](#шаг-8-отчёт)
  - [Шаг 9: Предложить начать разработку](#шаг-9-предложить-начать-разработку)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **SSOT — standard-development.md § 0.** Эта инструкция описывает шаги запуска. Детали каждого шага — в [§ 0 стандарта](./standard-development.md#0-запуск-разработки).

> **Все 4 документа — одновременно.** Переход в RUNNING выполняется tree-level: все документы цепочки меняют статус одновременно.

> **Пользователь подтверждает запуск.** Автоматический переход WAITING → RUNNING запрещён.

---

## Шаги

> Эта секция применяется при работе с analysis chain (specs/analysis/).
> Если Issues созданы вручную — перейти к [§ 1 Взятие задачи](./standard-development.md#1-взятие-задачи).

### Шаг 1: Проверить готовность цепочки

```bash
python .github/.instructions/.scripts/check-chain-readiness.py {NNNN}
```

Скрипт проверяет все 4 документа: status=WAITING и 0 маркеров. Если скрипт недоступен — проверить вручную:

Прочитать frontmatter всех 4 документов цепочки NNNN-{topic}:

| Документ | Требование |
|----------|------------|
| Discussion | `status: WAITING` |
| Design | `status: WAITING` |
| Plan Tests | `status: WAITING` |
| Plan Dev | `status: WAITING` |

Дополнительно: маркеров `[ТРЕБУЕТ УТОЧНЕНИЯ]` = 0 во всех документах.

Если не все в WAITING → **СТОП:** "Цепочка не готова. {документ} в статусе {status}."

### Шаг 2: Подтверждение пользователя

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: "Цепочка NNNN-{topic} готова к разработке. {N} TASK-N, Milestone {vX.Y.Z}. Начать?"

| Ответ | Действие |
|-------|----------|
| Да | Продолжить |
| Нет | **СТОП** |

### Шаг 3: Создать GitHub Issues

Для каждого TASK-N из Plan Dev → `/issue-create`:
- Sub-issues для подзадач (N.M)
- Записать номер Issue inline в поле `Issue` каждой TASK-N (формат: `[#N](url)`)

**Определение TYPE-метки для Issue:**

Если TASK-N содержит поле `Type` → использовать как TYPE-метку.

Если поле `Type` отсутствует (старые plan-dev) → определить автоматически:

| Условие | TYPE-метка |
|---------|------------|
| `TC: INFRA` | `infra` |
| Системные тесты (STS-N, E2E, load, integration) | `test` |
| Бизнес-логика (CRUD, UI, API-эндпоинты) | `feature` |
| Scaffold, middleware, схемы, boilerplate | `task` |

**Генерация body — Issue как полный промт для dev-agent:**

**SSOT:** [standard-issue.md § 4 Body](../issues/standard-issue.md#body-структура-описания)

Каждый Issue содержит **5 обязательных секций** — полный промт для изолированного агента. Агент получает Issue и работает автономно, без доступа к контексту основной сессии.

**Алгоритм сбора контекста (для каждого TASK-N):**

```
--- Подготовка ---
1. Прочитать TASK-N: Источник (SVC-N §§), TC (TC-N), Зависимости, подзадачи
2. Определить сервис: SVC-N → {svc} → specs/docs/{svc}.md
3. Определить тип сервиса: {svc}.md → Tech Stack → frontend/backend/infra
4. Определить наличие тестов: есть ли поле TC: в TASK-N?

--- Секция "Описание задачи" ---
5. 2-3 предложения ЧТО и ЗАЧЕМ (заголовок TASK-N + контекст Design)
   + сложность, сервис, волна, зависимости (Issues + что от них нужно)

--- Секция "Документы для изучения" ---
6. .system/ файлы: отфильтровать по типу сервиса (таблица ниже)
   Если есть TC → ОБЯЗАТЕЛЬНО включить testing.md
7. Design: из Источника → Design SVC-N § K с описанием "что искать"
8. Сервисная документация: specs/docs/{svc}.md — "Code Map, структура, точки входа"
9. Per-tech стандарты: {svc}.md → Tech Stack → standard-{tech}.md (отфильтрованные)
   В колонке "Что искать": "ОБЯЗАТЕЛЬНО следуй при написании кода"
10. Plan Test: TC-N — "сценарии тестов: входные данные, шаги, ожидаемый результат.
    Напиши тесты по ним"

--- Секция "Задание" ---
11. Вступление: "В соответствии с описанием {сервис}-сервиса в specs/docs/{svc}.md,
    на основании проектирования в Design SVC-N (...) и критериев приёмки из
    Plan Test TC-N..TC-M (...), реализуй {описание задачи}:"
    + подзадачи → развёрнутые инструкции с ссылками на Design/TC/conventions
12. Если есть TC → последний пункт: "Напиши тесты для TC-N..TC-M"
    со ссылкой на Plan Test и testing.md

--- Секция "Критерии готовности" ---
13. Ссылка на Plan Test + список TC-N + подзадачи как чек-лист
    + подзадача "Тесты: TC-N, TC-M" (если есть TC)

--- Секция "Практический контекст" ---
14. Существующий код: ls src/{svc}/ → snapshot структуры
15. Зависимости: для каждого Issue-зависимости → файл + экспорт + сигнатура
16. Как запустить: из Makefile / {svc}.md § Dev

17. Собрать body: 5 секций → `/issue-create`
```

**Фильтрация .system/ файлов по типу сервиса:**

Определение типа: из `Источник: SVC-N` → `specs/docs/{svc}.md` → Tech Stack. React/Vue → frontend. Express/Fastify/NestJS → backend. Нет SVC → infra.

| Тип задачи | overview.md | conventions.md | infrastructure.md | testing.md |
|------------|:-----------:|:--------------:|:-----------------:|:----------:|
| frontend | + | + (JWT, ошибки) | — | + (если есть TC) |
| backend | + | + | + (порты, БД) | + (если есть TC) |
| infra (без SVC) | + | — | + (PRIMARY) | + (если есть TC) |
| test | + | + | + | + (PRIMARY) |

**Дополнительный фильтр по подзадачам:**
- Подзадача содержит "тест" / "test" → добавить testing.md
- Подзадача содержит "порт" / "Docker" / "env" → добавить infrastructure.md
- Подзадача содержит "API" / "endpoint" / "ошибк" → добавить conventions.md

**Per-tech стандарты:** Из `specs/docs/{svc}.md` → § Tech Stack → для каждой технологии проверить `specs/docs/.technologies/standard-{tech}.md`. Включить только те, для которых файл существует. Из 9+ per-tech стандартов для frontend-задачи нужны только React + TypeScript.

**Принцип: навигация, а не копирование.** Issue содержит ПУТИ к документам + "Что искать". Агент читает через Read tool. Документы — SSOT, Issue — маршрут.

**Пример сгенерированного body (TASK-15, frontend):**

```markdown
## Описание задачи

Реализовать аутентификацию на фронтенде: Zustand-стор для хранения JWT-токена
и данных пользователя, страницу логина с формой email/password, компонент
ProtectedRoute для защиты маршрутов и роутинг приложения.

Это часть frontend-сервиса, который общается с auth-сервисом через REST API.
После реализации пользователь сможет войти в систему и получить доступ к дашборду.

**Сложность:** 5/10 | **Сервис:** frontend | **Wave:** 2
**Зависит от:** #55 (API-слой и TanStack Query хуки) — ДОЛЖЕН быть готов.

## Документы для изучения

Перед началом работы ОБЯЗАТЕЛЬНО прочитай документы из таблицы ниже.
Каждый документ содержит информацию, критичную для реализации задачи.

| # | Документ | Путь | Что искать |
|---|----------|------|-----------|
| 1 | Архитектура системы | specs/docs/.system/overview.md | Карта сервисов, как frontend связан с auth |
| 2 | Конвенции API | specs/docs/.system/conventions.md | Формат ответов, формат ошибок, JWT claims, Bearer |
| 3 | Design SVC-3 § 4 | specs/analysis/0001-task-dashboard/design.md | Контракт POST /api/v1/auth/login — request/response |
| 4 | Design SVC-3 § 5 | (тот же файл) | Zustand 5.x, React Router 7, JWT в localStorage |
| 5 | Design INT-2 | (тот же файл) | Flow frontend ↔ auth: вызов API, хранение токена |
| 6 | Сервисная документация | specs/docs/frontend.md | Code Map (§ 5), структура проекта, точки входа |
| 7 | React стандарт | specs/docs/.technologies/standard-react.md | Структура компонентов, хуки — ОБЯЗАТЕЛЬНО следуй |
| 8 | TypeScript стандарт | specs/docs/.technologies/standard-typescript.md | Типизация, именование — ОБЯЗАТЕЛЬНО следуй |
| 9 | Тестирование | specs/docs/.system/testing.md | Стратегия тестов, мокирование, структура тест-файлов |
| 10 | Plan Test | specs/analysis/0001-task-dashboard/plan-test.md | TC-28, TC-29, TC-30 — сценарии, входные данные, результат |

## Задание

В соответствии с описанием frontend-сервиса в specs/docs/frontend.md,
на основании проектирования в Design SVC-3 (specs/analysis/0001-task-dashboard/design.md)
и критериев приёмки из Plan Test TC-28..TC-30 (specs/analysis/0001-task-dashboard/plan-test.md),
реализуй аутентификацию frontend-приложения:

1. **Создай `src/frontend/stores/authStore.ts`** — Zustand стор.
   Поля: `token` (string | null), `user` (User | null).
   Методы: `login(email, password)` — вызывает POST /api/v1/auth/login
   через API-слой из #55. `logout()` — очищает token и user.
   Формат API-ответа: см. Design SVC-3 § 4. Формат ошибок: см. conventions.md.

2. **Создай `src/frontend/pages/LoginPage.tsx`** — страница логина.
   Форма с полями email и password. При submit → `authStore.login()`.
   При ошибке 401 → "Неверный email или пароль" (TC-29).
   Следуй паттернам из standard-react.md.

3. **Создай `src/frontend/components/ProtectedRoute.tsx`** — обёртка маршрута.
   Если `authStore.token` === null → Navigate to /login (TC-30).

4. **Обнови `src/frontend/App.tsx`** — добавь роутинг:
   - /login — LoginPage, / — ProtectedRoute(Dashboard) (TC-28).

5. **Напиши тесты** для TC-28, TC-29, TC-30.
   Прочитай каждый TC полностью. Структура тестов: см. testing.md.

## Критерии готовности

Тест-кейсы приёмки: specs/analysis/0001-task-dashboard/plan-test.md
TC-28, TC-29, TC-30 — прочитай ПОЛНОСТЬЮ перед началом работы.

- [ ] 15.1. authStore.ts: token, user, login(), logout()
- [ ] 15.2. LoginPage.tsx: форма + обработка ошибок
- [ ] 15.3. Интеграция с API-слоем → localStorage + authStore
- [ ] 15.4. ProtectedRoute: редирект при отсутствии JWT
- [ ] 15.5. App.tsx: роутинг /login + / (protected)
- [ ] 15.6. Тесты: TC-28, TC-29, TC-30

## Практический контекст

**Существующий код:**
src/frontend/ содержит: App.tsx, main.tsx, api/ (из #55), components/, pages/.
Точка входа: src/frontend/main.tsx → App.tsx.

**Зависимость #55 экспортирует:**
`src/frontend/api/auth.ts` → `authApi.login(email, password): Promise<LoginResponse>`

**Как запустить:** `make dev` → http://localhost:3000
**Как проверить:** `cd src/frontend && npm test`
```

### Шаг 4: Создать/привязать Milestone

1. Проверить: Milestone {vX.Y.Z} существует?
2. Если нет → `/milestone-create`
3. Привязать все Issues к Milestone

### Шаг 5: Перевести цепочку в RUNNING

**Переход WAITING → RUNNING** — через модуль `chain_status.py` (SSOT статусов):

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="RUNNING")
# Модуль автоматически: tree-level, все 4 документа → RUNNING, README dashboard
```

### Шаг 6: Коммит и Push в main

Шаги 3-5 изменяют файлы в main (plan-dev.md маппинг Issues, frontmatter статусы, README dashboard). Зафиксировать **до** создания ветки:

```bash
git add specs/analysis/NNNN-{topic}/ specs/analysis/README.md
git commit -m "feat(analysis): NNNN-{topic} RUNNING, маппинг Issues"
git push origin main
```

**Логика:** Ветка (шаг 7) отводится от чистого main, содержащего все метаданные цепочки.

### Шаг 7: Создать ветку

```
/branch-create {NNNN}
```

Ветка создаётся от свежего main (после push шага 6).

### Шаг 8: Отчёт

Вывести: Issues (#N), Milestone, Branch, статус цепочки → RUNNING.

### Шаг 9: Предложить начать разработку

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: "Цепочка NNNN-{topic} в RUNNING. Начать разработку?"

| Ответ | Действие |
|-------|----------|
| Да | Запустить разработку по [modify-development.md](./modify-development.md) (dev-agent) |
| Нет | Завершить воркфлоу |

---

## Чек-лист

- [ ] Все 4 документа цепочки существуют и в WAITING
- [ ] Маркеров `[ТРЕБУЕТ УТОЧНЕНИЯ]` = 0
- [ ] Пользователь подтвердил запуск
- [ ] Issues созданы из TASK-N с полным body (5 секций: Описание задачи, Документы для изучения, Задание, Критерии готовности, Практический контекст)
- [ ] Body содержит отфильтрованные .system/ файлы, Design §§, per-tech стандарты, Plan Test TC-N
- [ ] Поле Issue заполнено inline в каждой TASK-N
- [ ] Milestone создан/привязан
- [ ] Цепочка переведена в RUNNING
- [ ] Коммит + Push в main (метаданные цепочки)
- [ ] Ветка создана (от свежего main)
- [ ] README обновлён
- [ ] Отчёт выведен
- [ ] Пользователю предложено начать разработку

---

## Примеры

### Запуск разработки цепочки 0001

```
/dev-create 0001
```

### Возобновление после CONFLICT → WAITING

```
/dev-create 0001 --resume
```

Issues уже существуют — `/dev-create --resume` обнаружит и пропустит создание.

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [check-chain-readiness.py](../.scripts/check-chain-readiness.py) | Проверка готовности цепочки (4/4 WAITING, 0 маркеров) | Этот документ |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/dev-create](/.claude/skills/dev-create/SKILL.md) | Запуск разработки по analysis chain | Этот документ |
