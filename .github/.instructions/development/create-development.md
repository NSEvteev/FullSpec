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

Оркестрация через issue-agent + issue-reviewer (2 волны):

**Шаг 3.0: Определить блоки**
Парсить plan-dev.md → определить ## секции (блоки).
Каждый блок = один issue-agent. Примеры блоков: `## INFRA`, `## SVC-1: auth`, `## Системные тесты`.

**Шаг 3.1: Pre-parsing контекста**
Перед запуском issue-agent оркестратор извлекает контекст для каждого блока:

1. Из plan-dev.md: список TASK-N блока, их Источники (SVC-N §§), TC-N
2. Из design.md: извлечь текст секций SVC-N §§ для TASK-N данного блока
3. Из plan-test.md: извлечь текст TC-N для TASK-N данного блока
4. Из specs/docs/{svc}.md: извлечь Code Map и Tech Stack
5. Собрать описания документов (frontmatter description):
   ```bash
   python -c "
   import yaml, pathlib, sys
   for p in sys.argv[1:]:
       fp = pathlib.Path(p)
       if fp.exists():
           text = fp.read_text(encoding='utf-8')
           if text.startswith('---'):
               end = text.index('---', 3)
               fm = yaml.safe_load(text[3:end])
               print(f'{p} | {fm.get(\"description\",\"—\")}')
   " specs/docs/.system/overview.md specs/docs/.system/conventions.md \
     specs/docs/.system/infrastructure.md specs/docs/.system/testing.md \
     specs/docs/.technologies/standard-*.md specs/docs/{svc}.md
   ```

**Шаг 3.2: Волна 1 — issue-agent × K параллельно**
Для каждого блока запустить issue-agent (Agent tool, subagent_type=issue-agent):
- block-section: заголовок блока
- plan-dev-path: путь к plan-dev.md
- milestone, chain-id
- design-context: извлечённые секции SVC-N (текст, не путь)
- test-context: извлечённые TC-N (текст, не путь)
- svc-doc-context: Code Map + Tech Stack (текст, не путь)
- doc-descriptions: таблица путь|описание (для "Документы для изучения")
Агент создаёт Issues используя pre-parsed контекст — НЕ читает полные файлы.
Возвращает: список {TASK-N: Issue #N, URL}.

**Шаг 3.3: Записать маппинг Issue**
Оркестратор обновляет plan-dev.md: `Issue: —` → `Issue: [#N](url)` для каждого TASK-N.

**Шаг 3.4: Волна 2 — issue-reviewer × K параллельно**
Для каждого блока запустить issue-reviewer (Agent tool, subagent_type=issue-reviewer):
- block-section, issue-numbers (список от Волны 1)
- plan-dev-path
Reviewer "вживается в роль разработчика": читает Issue, формулирует
конкретные вопросы, ищет ответы в документах из таблицы Issue.
Если ответ не найден — дописывает в Issue. Не перечитывает все источники.

**Шаг 3.5: Отчёт + возможность повторного запуска**
Оркестратор выводит отчёт (кол-во правок per-Issue).
Пользователь может запустить issue-reviewer повторно на любой блок
(или все блоки) — каждый запуск проходит 3 фазы заново.

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

**Алгоритм сбора контекста:**

Оркестратор выполняет pre-parsing контекста (шаг 3.1), затем передаёт
извлечённый контент в prompt issue-agent. Агент НЕ читает полные файлы
design.md, plan-test.md, discussion.md, specs/docs/{svc}.md, .system/,
per-tech стандарты. См. шаг 3.1 и issue-agent AGENT.md § Алгоритм.

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

**Принцип: навигация, а не копирование.** Issue содержит ПУТИ, ОПИСАНИЯ (из frontmatter) и "Что искать". Описания позволяют исполнителю определить, содержит ли документ ответ на конкретный вопрос, без чтения полного файла. Документы — SSOT, Issue — маршрут.

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

| # | Документ | Путь | Описание | Что искать |
|---|----------|------|----------|-----------|
| 1 | Архитектура системы | specs/docs/.system/overview.md | Архитектура системы — карта сервисов, связи, потоки, домены | Как frontend связан с auth |
| 2 | Конвенции API | specs/docs/.system/conventions.md | Конвенции API и shared-интерфейсов — кросс-сервисные соглашения | Формат ответов, ошибок, JWT claims |
| 3 | Design SVC-3 § 4 | specs/analysis/0001-task-dashboard/design.md | Проектирование — SVC-N секции, INT-N контракты | Контракт POST /api/v1/auth/login |
| 4 | Design SVC-3 § 5 | (тот же файл) | (тот же файл) | Zustand 5.x, React Router 7, JWT в localStorage |
| 5 | Design INT-2 | (тот же файл) | (тот же файл) | Flow frontend ↔ auth: вызов API, хранение токена |
| 6 | Сервисная документация | specs/docs/frontend.md | Per-service документация frontend — API, Data Model, Code Map | Code Map (§ 5), структура проекта, точки входа |
| 7 | React стандарт | specs/docs/.technologies/standard-react.md | Стандарт кодирования React — компоненты, хуки, структура | ОБЯЗАТЕЛЬНО следуй при написании кода |
| 8 | TypeScript стандарт | specs/docs/.technologies/standard-typescript.md | Стандарт кодирования TypeScript — типизация, именование | ОБЯЗАТЕЛЬНО следуй при написании кода |
| 9 | Тестирование | specs/docs/.system/testing.md | Стратегия тестирования — типы, мокирование, размещение | Стратегия тестов, структура тест-файлов |
| 10 | Plan Test | specs/analysis/0001-task-dashboard/plan-test.md | План тестирования — TC-N acceptance-сценарии | TC-28, TC-29, TC-30 — сценарии, входные данные, результат |

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

**Зависимость #55 создала:**
`src/frontend/api/auth.ts` — API-клиент для auth-сервиса (login, logout)

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
- [ ] Issues созданы через issue-agent (по блокам, параллельно)
- [ ] Issues проверены issue-reviewer (по блокам, параллельно)
- [ ] Body содержит 5 секций с описаниями документов и отфильтрованными .system/ файлами
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
