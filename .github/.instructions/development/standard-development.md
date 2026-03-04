---
description: Стандарт процесса локальной разработки в feature-ветке — этапы, чек-лист, тесты, линтинг, коммиты.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/development/README.md
---

# Стандарт локальной разработки

Версия стандарта: 1.3

Процесс работы в feature-ветке: запуск окружения, написание кода, тестирование, проверки качества перед коммитом.

**Полезные ссылки:**
- [Инструкции development](./README.md)

**SSOT-зависимости:**
- [CLAUDE.md](/CLAUDE.md) — make-команды проекта
- [initialization.md](/.structure/initialization.md) — первый запуск после клонирования
- [standard-issue.md](../issues/standard-issue.md) — задача берётся из Issue перед началом разработки
- [standard-branching.md](../branches/standard-branching.md) — ветка создана перед началом разработки
- [standard-commit.md](../commits/standard-commit.md) — коммит создаётся после завершения разработки
- [standard-principles.md](/.instructions/standard-principles.md) — принципы программирования при написании кода
- [standard-pull-request.md](../pull-requests/standard-pull-request.md) — PR создаётся после завершения разработки
- [standard-analysis.md](/specs/.instructions/analysis/standard-analysis.md) — analysis chain (контекст задач в ветке)
- [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md) — стратегия тестирования (КАК писать тесты)
- [standard-sync.md](../sync/standard-sync.md) — синхронизация main при длительной разработке
- [standard-github-workflow.md](../standard-github-workflow.md) — полный цикл (стадия 4: Development)
- [create-development.md](./create-development.md) — воркфлоу запуска разработки по analysis chain
- [modify-development.md](./modify-development.md) — воркфлоу процесса разработки в feature-ветке

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-development.md](./validation-development.md) |
| Создание | [create-development.md](./create-development.md) |
| Модификация | [modify-development.md](./modify-development.md) |

## Оглавление

- [0. Запуск разработки](#0-запуск-разработки)
- [1. Взятие задачи](#1-взятие-задачи)
- [2. Процесс разработки](#2-процесс-разработки)
- [3. Make-команды](#3-make-команды)
- [4. Тестирование](#4-тестирование)
- [5. Проверки качества](#5-проверки-качества)
- [6. Работа с зависимостями](#6-работа-с-зависимостями)
- [7. Завершение работы над Issue](#7-завершение-работы-над-issue)
- [8. Запреты и ограничения](#8-запреты-и-ограничения)
- [9. Требования по уровням критичности сервисов](#9-требования-по-уровням-критичности-сервисов)

---

## 0. Запуск разработки

> **Скилл:** `/dev-create`

> Эта секция применяется при работе с analysis chain (specs/analysis/).
> Если Issues созданы вручную — перейти к [§ 1 Взятие задачи](#1-взятие-задачи).

**Управление статусами:** [`chain_status.py`](/specs/.instructions/.scripts/chain_status.py) — SSOT-модуль для переходов статусов analysis chain. Вызовы `ChainManager.transition()` — в `create-development.md` и `modify-development.md`.

### Предусловия

- Все 4 документа цепочки (Discussion, Design, Plan Tests, Plan Dev) существуют
- Все 4 документа в статусе `WAITING`
- Маркеров `[ТРЕБУЕТ УТОЧНЕНИЯ]` = 0 во всех документах

### Воркфлоу запуска

1. **Проверить готовность цепочки**
   - Прочитать frontmatter всех 4 документов → `status: WAITING`
   - Если не все в WAITING → СТОП: "Цепочка не готова. {документ} в статусе {status}"

2. **Подтверждение пользователя**
   - AskUserQuestion: "Цепочка NNNN-{topic} готова к разработке.
     {N} TASK-N, Milestone {vX.Y.Z}. Начать?"
   - Если "Нет" → СТОП

3. **Создать GitHub Issues**
   - Волна 1: issue-agent × K параллельно (K = кол-во блоков в plan-dev.md)
   - Волна 2: issue-reviewer × K параллельно (дополняет + 7 критериев проверки)
   - Повторный запуск reviewer — по запросу пользователя
   - Оркестратор обновляет маппинг Issues в plan-dev.md

4. **Создать/привязать Milestone**
   - Проверить: Milestone {vX.Y.Z} существует?
   - Если нет → `/milestone-create`
   - Привязать все Issues к Milestone

5. **Создать ветку**
   - `/branch-create {NNNN}`

6. **Перевести цепочку в RUNNING**
   - Обновить `status: WAITING` → `status: RUNNING` во всех 4 документах
   - Обновить `specs/analysis/README.md`

7. **Отчёт**
   - Вывести: Issues (#N), Milestone, Branch, статус цепочки → RUNNING

### Выход из секции

Issues созданы → Milestone назначен → ветка создана → цепочка в RUNNING →
переход к [§ 1 Взятие задачи](#1-взятие-задачи).

---

## 1. Взятие задачи

Перед началом разработки — выбрать Issue и проверить готовность к работе.

### Шаг 1: Прочитать Issue

```bash
gh issue view {number}
```

Перед началом работы изучить:
1. **Description** — что делать, критерии готовности
2. **Полезные ссылки** — связанные файлы и документы
3. **Dependencies** — зависимости от других Issues
4. **Sub-issues** — декомпозиция (если parent)
5. **Labels** — тип задачи и приоритет

Структура Issue: → [standard-issue.md](../issues/standard-issue.md)

### Шаг 2: Проверить зависимости

Проверить поле **Dependencies** в Issue. Если есть ссылки на другие Issues:

```bash
# Проверить статус каждой зависимости
gh issue view {dep-number} --json state --jq '.state'
```

| Статус зависимости | Действие |
|-------------------|----------|
| Все `closed` | Продолжить — зависимости выполнены |
| Есть `open` | **СТОП** — сначала выполнить открытую зависимость |
| Зависимость чужая (другой assignee) | Добавить `blocked` на текущий Issue, уведомить пользователя |

### Шаг 3: Назначить себя и начать

```bash
# Назначить себя
gh issue edit {number} --add-assignee @me
```

Создать ветку: → [create-branch.md](../branches/create-branch.md)

---

## 2. Процесс разработки

> **Агент:** [dev-agent](/.claude/agents/dev-agent/AGENT.md) — выполняет BLOCK-N из Plan Dev. Оркестрация волн — [modify-development.md](./modify-development.md).

### Предусловия

- Разработка запущена: `/dev-create {NNNN}` выполнен (→ [§ 0](#0-запуск-разработки))
- Задача взята: Issue прочитан, зависимости проверены (→ [§1](#1-взятие-задачи))
- Feature-ветка создана от актуальной main (→ [standard-branching.md § 3](../branches/standard-branching.md#3-жизненный-цикл-ветки))
- Окружение инициализировано: `make setup` выполнен после клонирования (→ [initialization.md](/.structure/initialization.md))

### Цикл работы в feature-ветке

```
┌─────────────────────────────────────────────────┐
│           ЦИКЛ РАЗРАБОТКИ В ВЕТКЕ               │
└─────────────────────────────────────────────────┘

1. ЗАПУСК ОКРУЖЕНИЯ
   └─ make dev

2. НАПИСАНИЕ КОДА
   └─ Реализация задач из analysis chain (→ standard-analysis.md)
   └─ Ветка привязана к NNNN (→ standard-branching.md § 2)
   └─ Следовать принципам программирования (→ standard-principles.md)

3. ЛОКАЛЬНОЕ ТЕСТИРОВАНИЕ
   └─ make test
   └─ Все тесты должны пройти. При failing тестах:
      - Упали тесты текущих изменений → исправить код, повторить шаг 2-3
      - Упали существующие тесты → проверить актуальность main, исправить breaking changes
      БЛОКИРОВКА: Переход к шагу 4 запрещён при failing тестах

4. ПРОВЕРКИ КАЧЕСТВА
   └─ make lint
   └─ Исправить все ERRORS. Warnings: исправить в изменённых файлах,
      существующие warnings в неизменённом коде — допустимы
   └─ БЛОКИРОВКА: Переход к шагу 5 запрещён при наличии ERRORS

5. КОММИТ
   └─ → standard-commit.md
```

### Принципы

- **Итеративность** — повторять шаги 2-4 до достижения результата
- **Малые изменения** — один логический блок работы = один коммит
- **Тесты рядом с кодом** — unit-тесты создаются вместе с реализацией
- **Синхронизация с main** — при разработке >2 дней синхронизировать feature-ветку с main (→ [standard-sync.md](../sync/standard-sync.md))

---

## 3. Make-команды

Полный список make-команд определён в [CLAUDE.md](/CLAUDE.md). Здесь описан контекст использования.

### Команды разработки

| Команда | Когда использовать |
|---------|-------------------|
| `make setup` | Один раз после клонирования — устанавливает pre-commit hooks |
| `make dev` | Запуск сервисов для локальной разработки |
| `make stop` | Остановка сервисов после завершения работы |
| `make clean` | Полная очистка (docker down -v). Использовать, если: сервисы не запускаются после `make dev`, зависшие контейнеры после `make stop`, ошибки "port already in use" или "volume not found" |

### Команды проверки

| Команда | Когда использовать |
|---------|-------------------|
| `make test` | После реализации функциональности перед коммитом |
| `make lint` | Опционально вручную перед коммитом. Автоматически запускается через pre-commit hooks при `git commit` (→ [standard-commit.md § 6](../commits/standard-commit.md#6-процесс-коммита)) |
| `make build` | Перед push — проверка, что проект собирается (exit code 0, нет ошибок компиляции) |

### Команды тестирования

| Команда | Когда использовать |
|---------|-------------------|
| `make test` | Unit и integration тесты |
| `make test-e2e` | E2E тесты — перед созданием PR |

---

## 4. Тестирование

> **Стратегия тестирования** (КАК писать тесты) определена в [standard-testing.md](/specs/.instructions/docs/testing/standard-testing.md). Здесь описано КОГДА запускать тесты.

### Требования перед коммитом

- `make test` проходит без ошибок
- Новый код покрыт unit-тестами

### Требования перед созданием PR

- `make test` проходит без ошибок
- `make test-e2e` проходит без ошибок. Обязательно при изменениях: API endpoints, database schema, inter-service communication, gateway routes. Опционально: изменения только внутри одного сервиса без внешних зависимостей
- `make build` завершается успешно (exit code 0, нет ошибок компиляции)

### Расположение тестов

| Тип тестов | Расположение | Когда запускать |
|------------|-------------|-----------------|
| Unit-тесты сервиса | `/src/{service}/tests/` | `make test` — при каждом изменении |
| Системные тесты | `/tests/` | `make test-e2e` — перед PR |

### Отладка failing тестов

При провале тестов:

1. Прочитать вывод `make test` — найти имя failing теста и сообщение об ошибке
2. Запустить отдельный тест для локализации проблемы (команда зависит от фреймворка)
3. Проверить: failing тест связан с текущими изменениями или с устаревшей main

| Симптом | Вероятная причина | Решение |
|---------|------------------|---------|
| Тест упал в изменённом файле | Ошибка в текущем коде | Исправить код, повторить тест |
| Тест упал в неизменённом файле | Устаревшая main | Синхронизировать main (→ [standard-sync.md](../sync/standard-sync.md)) |
| "connection refused", "timeout" | Сервисы не запущены | `make dev`, подождать инициализацию |
| "port already in use" | Зависшие контейнеры | `make clean && make dev` |

---

## 5. Проверки качества

### Обязательные проверки перед коммитом

1. **Тесты:** `make test` — все тесты проходят
2. **Линтинг:** Автоматически через pre-commit hooks (→ [standard-commit.md § 6](../commits/standard-commit.md#6-процесс-коммита)). Вручную: `make lint` (если нужна проверка до коммита)

### Pre-commit hooks

Запускаются автоматически при `git commit` (→ [standard-commit.md § 6](../commits/standard-commit.md#6-процесс-коммита)). Если hooks не установлены — выполнить `make setup`.

### Checklist перед push

ОБЯЗАТЕЛЬНО провести провеку по чек-листу:

- [ ] Код реализует ВСЕ задачи из analysis chain, указанного в имени ветки (→ [standard-branching.md § 2](../branches/standard-branching.md#2-naming-convention))
- [ ] Unit-тесты написаны и проходят (`make test`)
- [ ] Линтер проходит (`make lint`)
- [ ] Проект собирается (`make build` — exit code 0, нет ошибок компиляции)
- [ ] E2E тесты проходят (`make test-e2e`) — обязательно при изменениях API, database, inter-service communication
- [ ] Код соответствует принципам программирования (→ [standard-principles.md](/.instructions/standard-principles.md))
- [ ] Валидация процесса пройдена (→ [validation-development.md](./validation-development.md))

---

## 6. Работа с зависимостями

### Добавление зависимости

1. Установить пакет через менеджер зависимостей сервиса
2. Убедиться, что lockfile обновлён (package-lock.json, Pipfile.lock, go.sum и т.д.)
3. Проверить: `make dev` запускается, `make test` проходит
4. Закоммитить lockfile ВМЕСТЕ с кодом, использующим зависимость

### Обновление зависимости

1. Обновить пакет через менеджер зависимостей
2. Проверить: `make test` и `make build` проходят
3. Закоммитить обновлённый lockfile

### Правила

| Правило | Обоснование |
|---------|-------------|
| Lockfile ВСЕГДА коммитится | Гарантирует одинаковые версии у всех разработчиков |
| После добавления/обновления — `make test` | Новая зависимость может сломать существующий код |
| Один коммит = код + lockfile | Атомарность — зависимость и её использование неразделимы |

---

## 7. Завершение работы над Issue

После последнего коммита — завершить работу над задачей и обновить связанные Issues.

### Шаг 1: Создать PR

```bash
gh pr create --title "..." --body "Fixes #{number}"
```

Ключевое слово `Fixes #N` автоматически закроет Issue при мерже (→ [standard-pull-request.md](../pull-requests/standard-pull-request.md)).

### Шаг 2: Проверить зависимые Issues

Кто ждёт завершения текущей задачи?

```bash
# Поиск Issues, которые зависят от текущего
gh issue list --state open --search "#{number}" --limit 50
```

Для каждого найденного Issue с `**Зависит от:** #{number}` в body:

| Ситуация | Действие |
|----------|----------|
| Текущий Issue был единственной зависимостью | Убрать `blocked`: `gh issue edit {dep} --remove-label blocked` |
| Есть другие открытые зависимости | Оставить `blocked`, добавить комментарий: "Зависимость #{number} выполнена" |

### Шаг 3: Обновить связанные Issues

Если в ходе работы были созданы артефакты (документы, стандарты, скрипты), на которые опираются связанные Issues:

```bash
# Добавить комментарий с ссылками на созданные артефакты
gh issue comment {related} --body "Создано в #{number}: [описание артефакта](путь)"
```

### Шаг 4: Проверить sub-issues (если parent)

Если текущий Issue — parent с sub-issues:

```bash
gh issue view {number}
# Проверить: все sub-issues закрыты? Если нет — parent НЕ закрывать.
```

---

## 8. Запреты и ограничения

| Правило | Обоснование |
|---------|-------------|
| Не коммитить секреты (.env, credentials) | Только `.env.example` — см. [CLAUDE.md](/CLAUDE.md) |
| Не пропускать failing тесты | Сломанные тесты блокируют CI и merge |
| Не пропускать `make setup` после клонирования | Pre-commit hooks не будут работать |
| Не разрабатывать в main | Все изменения только в feature-ветке (→ [standard-branching.md § 4](../branches/standard-branching.md#4-запреты-и-ограничения)) |

---

## 9. Требования по уровням критичности сервисов

Требования к процессу разработки зависят от уровня критичности сервиса. Уровень определяется в `{svc}.md` (поле `criticality`). Допустимые значения: `critical-high`, `critical-medium`, `critical-low`.

| Критерий | critical-high | critical-medium | critical-low |
|----------|--------------|-----------------|--------------|
| Reviewers для PR | ≥2, включая senior/lead | ≥1 | ≥1 (self-merge допустим) |
| Branch protection | Strict (no force push, required reviews) | Standard (required reviews) | Basic |
| Feature flags | Обязательны для крупных изменений | Рекомендуются | Не требуются |
| Документация API | Обязательна (OpenAPI/AsyncAPI) | Обязательна | Рекомендуется |
