---
description: Dev-agent — блочная параллельная модель разработки с CONFLICT-детекцией. Расширение G10 + архитектура /dev как агента.
type: feature
status: draft
created: 2026-02-24
---

# Dev-agent — блочная параллельная модель разработки

Агент разработки с формальной CONFLICT-детекцией, блоками выполнения (BLOCK-N) и параллельным запуском нескольких агентов на независимые блоки.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Архитектура](#1-архитектура)
  - [2. Блоки выполнения (BLOCK-N)](#2-блоки-выполнения-block-n)
  - [3. Параллельная модель (волны)](#3-параллельная-модель-волны)
  - [4. CONFLICT-детекция](#4-conflict-детекция)
  - [5. Протокол агент ↔ main LLM](#5-протокол-агент--main-llm)
  - [6. Изменения в стандартах](#6-изменения-в-стандартах)
  - [7. Dev-agent AGENT.md](#7-dev-agent-agentmd)
  - [8. /dev SKILL.md](#8-dev-skillmd)
- [Решения](#решения)
- [Закрытые вопросы](#закрытые-вопросы)
- [Задачи](#задачи)

---

## Контекст

**Задача:** G10 из standard-process.md + архитектура `/dev` как агента
**Почему создан:** G10 (автоопределение уровня CONFLICT) — анализ показал, что LLM справляется с классификацией; автоматизация не даёт выигрыша. Но при вынесении `/dev` в агент CONFLICT-детекция становится формальной обязанностью агента, а не неявным поведением. Параллельно: потребность в блочной модели выполнения задач.
**Связанные файлы:**
- `specs/.instructions/analysis/standard-analysis.md` — § 6.3 RUNNING to CONFLICT
- `specs/.instructions/analysis/plan-dev/standard-plan-dev.md` — § 4 модель выполнения
- `specs/.instructions/analysis/plan-test/standard-plan-test.md` — TC-N acceptance-сценарии
- `.github/.instructions/development/modify-development.md` — текущий воркфлоу разработки
- `.claude/skills/dev/SKILL.md` — текущий скилл `/dev`
- `specs/.instructions/.scripts/chain_status.py` — classify_feedback(), transition()

**Предшественник:** Этот черновик расширяет исходный анализ G10 (автоопределение уровня CONFLICT). Исходный вывод G10: LLM справляется с классификацией, автоматизация эвристиками — inferior. Этот вывод сохраняется: CONFLICT-детекция остаётся на LLM (dev-agent), но формализуется как обязанность.

---

## Содержание

### 1. Архитектура

**Текущее состояние:**

| Аспект | Сейчас |
|--------|--------|
| `/dev` | Skill — раскрывается в основном LLM-контексте |
| SSOT | `modify-development.md` — воркфлоу с 5 шагами + переходы |
| CONFLICT-детекция | Неявная часть шага 3 ("при обнаружении — перейди") |
| Модель выполнения | Один LLM, последовательно по Issues |

**Целевое состояние:**

| Аспект | Цель |
|--------|------|
| `/dev` | Agent — запускается через Task tool с `subagent_type: "dev-agent"` |
| SSOT | `modify-development.md` переписан под агентную модель |
| CONFLICT-детекция | Формальная обязанность агента с чек-листом |
| Модель выполнения | N агентов параллельно, каждый на свой BLOCK-N |

**Архитектура исполнения:**

```
Пользователь: /dev
       ↓
Main LLM (оркестратор):
  1. Читает plan-dev.md → определяет BLOCK-N
  2. Строит граф зависимостей блоков → формирует волны (waves)
  3. Запускает N dev-agent через Task tool (parallel calls)
  4. Ожидает результаты (TaskOutput)
  5. При CONFLICT от любого агента → TaskStop для остальных
  6. Собирает результаты → информирует пользователя
  7. Следующая волна (или CONFLICT-разрешение)
       ↓
Dev-agent (subprocess, изолированный контекст):
  1. Получает: BLOCK-N (список Issues), контекст (plan-dev, docs/{svc}.md)
  2. Итерирует по Issues блока: код → тест → линт → коммит
  3. НЕПРЕРЫВНО проверяет: не затронуты ли границы автономии → CONFLICT?
  4. По завершении: обновляет plan-dev.md (чекбоксы), plan-test.md
  5. Возвращает результат main LLM
```

**Skill-режим не нужен.** Если пользователь хочет интерактивно работать с кодом — он общается с main LLM напрямую, без `/dev`. Команда `/dev` = "запусти формальный SDD dev-workflow" = всегда агент. Один путь, нет двусмысленности.

---

### 2. Блоки выполнения (BLOCK-N)

**Определение:** BLOCK-N — группа TASK-N (и соответствующих TC-N из plan-test), которые:
- Логически связаны (обычно per-service, но допускается cross-service)
- Выполнимы одним dev-agent без внешней координации
- Не имеют файловых пересечений с другими блоками той же волны

**Кто определяет блоки:** Main LLM при создании plan-dev.md и plan-test.md (скиллы `/plan-dev-create`, `/plan-test-create`). Блоки — часть документа, не генерируются на лету.

**Формат в plan-dev.md:**

Новая секция после "Кросс-сервисные зависимости", перед "Маппинг GitHub Issues":

```markdown
## Блоки выполнения

| BLOCK | Задачи | Сервисы | Зависимости | Wave |
|-------|--------|---------|-------------|------|
| BLOCK-1 | TASK-1, TASK-2, TASK-3 | auth | — | 1 |
| BLOCK-2 | TASK-4, TASK-5 | gateway | — | 1 |
| BLOCK-3 | TASK-6, TASK-7 | users | — | 1 |
| BLOCK-4 | TASK-8, TASK-9 | shared | BLOCK-1, BLOCK-2 | 2 |
```

**Формат в plan-test.md:**

Новая секция после "Матрица покрытия":

```markdown
## Блоки тестирования

| BLOCK | TC | Сервисы | Dev BLOCK |
|-------|----|---------|-----------|
| BLOCK-1 | TC-1..TC-7 | auth | BLOCK-1 |
| BLOCK-2 | TC-8, TC-9 | gateway | BLOCK-2 |
| BLOCK-3 | TC-10, TC-11 | users | BLOCK-3 |
| BLOCK-4 | TC-12..TC-14 | e2e (system) | BLOCK-4 |
```

**Зеркальность test-блоков:** Test-BLOCK-N = зеркало dev-BLOCK-N для per-service TC. Каждый dev-BLOCK имеет соответствующий test-BLOCK с теми же сервисами. Системные TC (e2e/load из секции "Системные тест-сценарии") выделяются в отдельный test-BLOCK в последней волне.

**Двухуровневое тестирование:**

| Уровень | Кто выполняет | Когда | Команда | Тип TC |
|---------|--------------|-------|---------|--------|
| Per-service | Dev-agent | Во время разработки блока | `make test-{svc}` | unit, integration |
| System/e2e | Main LLM (или test-agent) | После завершения волны | `make test-e2e` | e2e, load |

Dev-agent тестирует только свой сервис — это исключает конфликты при параллельном запуске нескольких агентов. Системные/e2e тесты запускаются после волны, когда все per-service блоки завершены и код стабилен.

**Зависимость:** per-service Makefile таргеты (`make test-{svc}`, `make lint-{svc}`) — требуют реализации. См. драфт `tests-and-platform`.

**Правила блоков:**

| Правило | Описание |
|---------|----------|
| **No file overlap** | Блоки одной волны НЕ ДОЛЖНЫ затрагивать одни и те же файлы. Shared-файлы (`shared/`, `config/`, `platform/`) выделяются в отдельный INFRA-блок |
| **INFRA-блок** | Блок с TASK-N типа `TC: INFRA` (настройка окружения, shared-контракты). Помещается в wave 0 или первую волну, выполняется до service-блоков |
| **Покрытие** | Каждый TASK-N принадлежит ровно одному BLOCK-N. Нет TASK-N без блока |
| **Размер** | 2-5 TASK-N на блок (рекомендация). Один TASK-N = блок допустим для критических зависимостей |
| **Зависимости** | Между блоками — через колонку "Зависимости". Блок не запускается, пока все зависимости не завершены |
| **Соответствие TC** | Каждый dev-BLOCK имеет соответствующий test-BLOCK с TC-N для тех же сервисов |
| **Нумерация** | Сквозная по документу: BLOCK-1, BLOCK-2, ... Совпадает между plan-dev и plan-test |

**Как main LLM определяет блоки:**

1. **Per-service группировка** — TASK-N одного сервиса → один блок (default)
2. **Shared → INFRA** — TASK-N с `TC: INFRA` или затрагивающие `shared/` → отдельный блок
3. **Зависимости** — если BLOCK-A зависит от BLOCK-B, они в разных волнах
4. **File overlap check** — если два блока одной волны затрагивают одни файлы → перенести один в следующую волну или объединить

---

### 3. Параллельная модель (волны)

**Волна (wave)** — набор BLOCK-N без взаимных зависимостей. Все блоки волны запускаются параллельно.

```
Wave 0: [BLOCK-INFRA]                ← shared/, config/
           ↓ завершён
Wave 1: [BLOCK-1] [BLOCK-2] [BLOCK-3] ← auth, gateway, users (параллельно)
              ↓        ↓
Wave 2:           [BLOCK-4]           ← e2e/integration (зависит от wave 1)
```

**Формирование волн (main LLM):**

1. Топологическая сортировка графа зависимостей BLOCK-N
2. Блоки без зависимостей → wave 1 (или wave 0, если INFRA)
3. Блоки, зависящие от wave N → wave N+1
4. Циклические зависимости → ошибка при создании plan-dev (валидация)

**Запуск волны (main LLM):**

```
# Одно сообщение с N параллельными Task вызовами:
Task(subagent_type="dev-agent", prompt="BLOCK-1: TASK-1,2,3 (auth) ...")
Task(subagent_type="dev-agent", prompt="BLOCK-2: TASK-4,5 (gateway) ...")
Task(subagent_type="dev-agent", prompt="BLOCK-3: TASK-6,7 (users) ...")
```

**Между волнами (main LLM):**
- Собрать результаты всех агентов
- Проверить: есть ли CONFLICT среди результатов?
- Если нет → запустить следующую волну
- Если да → разрешение CONFLICT (§ 4), затем перезапуск

**Особый случай — одна волна:** Если все блоки независимы (нет кросс-сервисных зависимостей) — одна волна, все блоки параллельно.

**Особый случай — один блок:** Если один сервис — один блок, один агент. Волны не нужны.

---

### 4. CONFLICT-детекция

#### 4.1 Почему на LLM (вывод из G10)

Исходный анализ G10 показал:
- Эвристики по diff (файл → пакет → уровень) дают низкую точность: diff не показывает "почему"
- AST-анализ слишком сложен для мультиязычного проекта
- LLM уже получает обогащённый контекст: `docs/{svc}.md` Code Map + Границы автономии + Design SVC-N
- `standard-analysis.md § 6.3` формализует критерии: "Свободно" / "Флаг" / "CONFLICT"

**Вывод:** CONFLICT-детекция остаётся на LLM (dev-agent). Формализуется как обязанность, не автоматизируется скриптом.

#### 4.2 Обязанность dev-agent

Dev-agent ОБЯЗАН после каждого коммита (= после каждой подзадачи или задачи):

1. **Проверить границы автономии** — сопоставить внесённые изменения с `docs/{svc}.md` → секция "Границы автономии LLM"
2. **Классифицировать** — изменение "Свободно" / "Флаг" / "CONFLICT" по таблице из `standard-analysis.md § 6.3`:

   | Граница в Code Map | Уровень | Действие агента |
   |---|---|---|
   | **Свободно** (внутри пакета) | Спецификации не затронуты | Продолжить работу |
   | **Флаг** (между пакетами) | Plan Dev / Plan Tests | Автономно обновить документы, продолжить. Записать в отчёт |
   | **CONFLICT** (API, data model, архитектура) | Design или выше | **СТОП.** Вернуть результат main LLM с описанием CONFLICT |

3. **При обнаружении CONFLICT** — агент:
   - Завершает текущий коммит (атомарность)
   - Записывает в результат: уровень CONFLICT, затронутый документ, описание проблемы
   - Останавливается (не берёт следующий Issue)

4. **При "Флаг"** — агент автономно:
   - Обновляет plan-dev.md (подзадачи, описания)
   - Записывает в отчёт: что обновлено, почему
   - Продолжает работу

#### 4.3 CONFLICT при параллельных агентах

**Политика: остановить всех.**

Когда dev-agent обнаруживает CONFLICT:
1. Агент возвращает результат с `status: CONFLICT`
2. Main LLM получает результат (foreground task или TaskOutput)
3. Main LLM вызывает `TaskStop` для всех остальных запущенных агентов волны
4. Main LLM собирает частичные результаты остановленных агентов
5. Main LLM запускает CONFLICT-разрешение (standard-analysis.md § 6.4): chain_status.py T4 → top-down → WAITING → RUNNING
6. После разрешения: main LLM перезапускает незавершённые блоки (resume с учётом уже выполненных Issues)

**Почему "остановить всех":**
- CONFLICT меняет спецификации → другие агенты работают по устаревшим specs
- Дешевле перезапустить, чем разбирать конфликты в коде
- Код завершённых Issues сохраняется (коммиты уже сделаны)

#### 4.4 Обнаружение уровня (B.4)

Dev-agent при CONFLICT определяет **самый высокий затронутый документ** — снизу вверх:
- Plan Dev затронут? → содержание TASK-N стало неверным?
- Plan Tests затронут? → TC-N стали неверными?
- Design затронут? → SVC-N/INT-N/STS-N стали неверными?
- Discussion затронут? → REQ-N стали неверными?

СТОП на первом незатронутом. Самый высокий затронутый = точка начала разрешения.

**Примеры (из standard-analysis.md):**

| Тип изменения | Документ затронут? |
|---------------|-------------------|
| Изменён алгоритм (bcrypt → argon2) в SVC-N | Да — Design |
| Изменено имя метода внутри пакета | Нет |
| Изменена схема БД (добавлена колонка) | Да — Design |
| Изменён retry без смены контракта | Нет |

---

### 5. Протокол агент ↔ main LLM

#### 5.1 Запуск агента (main LLM → agent)

Main LLM передаёт в prompt агента:

```
BLOCK: BLOCK-1
ISSUES: #42 (TASK-1), #43 (TASK-2), #44 (TASK-3)
SERVICE: auth
CHAIN: 0001-oauth2-authorization
BRANCH: 0001-oauth2-authorization

Контекст:
- Plan Dev: specs/analysis/0001-oauth2-authorization/plan-dev.md
- Plan Tests: specs/analysis/0001-oauth2-authorization/plan-test.md
- Service doc: docs/auth.md
- Design: specs/analysis/0001-oauth2-authorization/design.md
- Conventions: docs/.system/conventions.md
- Test BLOCK: BLOCK-1 (TC-1..TC-7)
```

**Обязательный контекст для каждого блока:**

| Файл | Зачем агенту |
|------|-------------|
| `plan-dev.md` | TASK-N задачи блока, подзадачи, чекбоксы |
| `plan-test.md` | TC-N acceptance-сценарии для блока |
| `docs/{svc}.md` | API, Code Map, Границы автономии — CONFLICT-детекция |
| `design.md` | SVC-N секции — контекст решений, INT-N контракты |
| `docs/.system/conventions.md` | Shared-интерфейсы, конвенции API, форматы ответов — агент ОБЯЗАН знать контракты shared/ при работе с зависимостями |

**Опциональный контекст (main LLM добавляет при наличии зависимостей от shared/):**

| Файл | Когда добавлять |
|------|----------------|
| `docs/.system/overview.md` | Блок затрагивает архитектурные связи между сервисами |
| `docs/{другой-svc}.md` § 2 | Блок потребляет API другого сервиса (ссылка из "Зависимости") |

#### 5.2 Результат агента (agent → main LLM)

Агент возвращает структурированный результат:

```
STATUS: COMPLETED | CONFLICT | PARTIAL

COMPLETED_ISSUES: [#42, #43]
REMAINING_ISSUES: [#44]  (если PARTIAL/CONFLICT)

CONFLICT_INFO: (если STATUS=CONFLICT)
  level: design
  affected_doc: SVC-1 (auth)
  description: "API контракт POST /auth/token изменился: добавлен grant_type=device_code, не предусмотренный в Design"
  last_commit: abc1234

FLAGS: (если были рабочие правки)
  - "Добавлена подзадача 2.4 в TASK-2: валидация device_code формата"
  - "Обновлён TC-3: добавлен кейс с device_code"

UPDATED_FILES:
  - plan-dev.md: подзадачи [x] для TASK-1, TASK-2
  - plan-test.md: — (без изменений)
```

#### 5.3 Обновление документов агентом

**plan-dev.md** — агент обновляет:
- `- [ ]` → `- [x]` для выполненных подзадач
- Добавляет подзадачи при "Флаг" (рабочие правки)
- НЕ меняет структуру TASK-N, BLOCK-N, зависимости

**plan-test.md** — агент НЕ обновляет напрямую (TC-N — acceptance-сценарии, не исполнение). При обнаружении "Флаг" касательно тестов — записывает в FLAGS отчёта, main LLM решает.

**Issues** — агент закрывает завершённые Issues:
```bash
gh issue close {number} --comment "Реализовано в коммитах {hashes}"
```

#### 5.4 Между волнами (main LLM)

```
1. Собрать результаты всех агентов волны
2. Если любой STATUS=CONFLICT:
   a. TaskStop для запущенных агентов (если foreground — дождаться)
   b. Собрать частичные результаты
   c. AskUserQuestion: "CONFLICT обнаружен: {description}. Разрешить?"
   d. chain_status.py transition(to="CONFLICT")
   e. Top-down разрешение (§ 6.4 standard-analysis.md)
   f. После разрешения: пересобрать блоки (BLOCK-N могли измениться)
   g. Перезапустить незавершённые блоки
3. Если все STATUS=COMPLETED:
   a. Обновить dashboard (chain_status.py)
   b. Запустить следующую волну
4. Если все волны завершены:
   a. Все Issues закрыты → предложить REVIEW
   b. AskUserQuestion: "Все TASK-N выполнены. Перейти в REVIEW?"
```

---

### 6. Изменения в стандартах

#### 6.1 standard-plan-dev.md

| Секция | Изменение |
|--------|-----------|
| § 4 "Переходы статусов" → "Модель выполнения" | Заменить "последовательную модель, один агент-кодер" на "блочную параллельную модель". Описать BLOCK-N, волны, dev-agent |
| § 5 "Разделы документа" | Добавить секцию "Блоки выполнения" (h2) после "Кросс-сервисные зависимости" с таблицей BLOCK-N |
| § 8 "Чек-лист качества" | Добавить проверки: каждый TASK-N в ровно одном BLOCK-N, нет циклических зависимостей между BLOCK-N, INFRA-блоки в первой волне |
| § 7 "Шаблон" | Добавить секцию "Блоки выполнения" в шаблон |

#### 6.2 standard-plan-test.md

| Секция | Изменение |
|--------|-----------|
| § 5 "Разделы документа" | Добавить секцию "Блоки тестирования" (h2) после "Матрица покрытия" |
| § 8 "Чек-лист качества" | Добавить проверки: каждый TC-N в ровно одном BLOCK-N, нумерация блоков совпадает с plan-dev |
| § 7 "Шаблон" | Добавить секцию |

#### 6.3 standard-analysis.md

| Секция | Изменение |
|--------|-----------|
| § 6.3 "RUNNING to CONFLICT" | Добавить подсекцию: "CONFLICT при параллельных агентах" — политика остановки всех, протокол сбора частичных результатов |
| § 6.3 "Обнаружение затронутого уровня" | Уточнить: агент выполняет обнаружение и возвращает в отчёте |

#### 6.4 modify-development.md

| Секция | Изменение |
|--------|-----------|
| Полный rewrite | Переписать под агентную модель: main LLM оркестрирует блоки/волны, dev-agent выполняет |
| Шаг 1 | Определить блоки и волны (из plan-dev.md) вместо "определить следующий Issue" |
| Шаг 2 | Запуск волны (N параллельных Task вызовов) |
| Шаг 3 | Сбор результатов, обработка CONFLICT |
| Шаг 4 | Следующая волна или REVIEW |
| Переходы | Сохранить RUNNING→CONFLICT, RUNNING→REVIEW, но с агентной спецификой |

#### 6.5 /dev SKILL.md → AGENT.md

| Действие | Описание |
|----------|----------|
| Удалить `.claude/skills/dev/SKILL.md` | Skill больше не нужен |
| Создать `.claude/agents/dev-agent/AGENT.md` | Агент разработки (§ 7 этого черновика) |
| Обновить `.claude/settings.local.json` | Добавить `dev-agent` в `subagent_type` |
| Обновить development README.md | Ссылка на агента вместо скилла |

#### 6.6 standard-process.md

| Секция | Изменение |
|--------|-----------|
| § 10 G10 | Закрыть: "Incorporated — CONFLICT-детекция формализована как обязанность dev-agent" |
| § 5 Фаза 3 | Обновить: ссылка на dev-agent вместо скилла |
| § 8 Сводная таблица | Обновить строку "3.1 Dev cycle" |

#### 6.7 Документация по сервисам (specs/.instructions/docs/service/)

Per-service Makefile таргеты (`make test-{svc}`, `make lint-{svc}`) — необходимы для двухуровневого тестирования (R9). Агент запускает `make test-{svc}` внутри блока, main LLM запускает `make test-e2e` после волны. Для этого каждый `docs/{svc}.md` должен документировать доступные Makefile таргеты, а воркфлоу создания/изменения/удаления/валидации должны это учитывать.

**6.7.1 standard-service.md**

| Секция | Изменение |
|--------|-----------|
| § 3 Code Map | Добавить подсекцию **Makefile таргеты** (после "Внутренние зависимости", перед "Как добавить новый функционал"). Обязательные элементы: таблица таргетов (Таргет, Команда, Описание) |
| § 3 Code Map → описание | Добавить п.5 "Подсекция **Makefile таргеты** — per-service таргеты для тестирования, линтинга, сборки" |
| § 5 Шаблон | Добавить подсекцию "Makefile таргеты" в Code Map шаблона |
| § 6 Пример | Добавить Makefile таргеты в пример notification |

Формат подсекции:

```markdown
### Makefile таргеты

| Таргет | Команда | Описание |
|--------|---------|----------|
| test | `make test-{svc}` | Unit + integration тесты сервиса |
| lint | `make lint-{svc}` | Линтинг кода сервиса |
| build | `make build-{svc}` | Сборка Docker-образа (если применимо) |
```

Правила:
- Таргеты `test` и `lint` обязательны для каждого сервиса
- Таргет `build` — если сервис имеет Docker-образ
- Дополнительные таргеты (seed, migrate) — по необходимости
- Имя таргета = `{action}-{svc}` (kebab-case)

**6.7.2 create-service.md**

| Секция | Изменение |
|--------|-----------|
| Шаг 5 "Заполнить секции" → таблица источников | Добавить строку: `Code Map → Makefile таргеты` / Источник: `Makefile (корневой), src/{svc}/Makefile (если есть)` |
| Новый Шаг (между 5 и 6) | **Шаг 5.1: Создать per-service Makefile таргеты.** Добавить в корневой Makefile таргеты `test-{svc}`, `lint-{svc}`. Если таргеты уже существуют — проверить соответствие |
| Чек-лист | Добавить: `- [ ] Per-service Makefile таргеты созданы (make test-{svc}, make lint-{svc})` |
| Чек-лист | Добавить: `- [ ] Code Map содержит подсекцию Makefile таргеты` |

**6.7.3 modify-service.md**

| Секция | Изменение |
|--------|-----------|
| Таблица триггеров | Добавить: `Добавлен/удалён Makefile таргет` → `Code Map → Makefile таргеты` → Новый сценарий 8 |
| Новый Сценарий 8 | **Сценарий 8: Изменены Makefile таргеты.** Шаги: 1) Code Map → Makefile таргеты — обновить таблицу, 2) Валидация |
| Деактивация → Шаг 1 | Расширить: после удаления `{svc}.md` — удалить per-service таргеты из корневого Makefile (`test-{svc}`, `lint-{svc}`, `build-{svc}`) |
| Миграция → новый Шаг | Добавить шаг между "Обновить h1" и "Обновить docs/README.md": **Переименовать Makefile таргеты** — заменить `{old-svc}` → `{new-svc}` в Makefile (`test-{old-svc}` → `test-{new-svc}`, аналогично lint, build) |
| Чек-лист Деактивация | Добавить: `- [ ] Per-service Makefile таргеты удалены` |
| Чек-лист Миграция | Добавить: `- [ ] Makefile таргеты переименованы ({old-svc} → {new-svc})` |

**6.7.4 validation-service.md**

| Секция | Изменение |
|--------|-----------|
| Коды ошибок | Добавить: `SVC011` — Per-service Makefile таргеты отсутствуют в Code Map → Makefile таргеты. Критичность: Предупреждение |
| Шаг 3 "Проверить таблицы" | Добавить в таблицу обязательных колонок: `Code Map → Makefile таргеты` / `Таргет, Команда, Описание` |
| Чек-лист | Добавить: `- [ ] SVC011: Code Map содержит подсекцию Makefile таргеты с обязательными колонками` |

---

### 7. Dev-agent AGENT.md

**Эскиз конфигурации (frontmatter):**

```yaml
---
name: dev-agent
description: Агент разработки — выполнение блока задач (BLOCK-N) из Plan Dev. Код, тесты, коммиты, CONFLICT-детекция.
standard: .claude/.instructions/agents/standard-agent.md
standard-version: v1.2
index: .claude/.instructions/agents/README.md
type: general-purpose
model: sonnet
tools: Read, Bash, Glob, Grep, Write, Edit
disallowedTools: WebSearch, WebFetch
permissionMode: default
max_turns: 80
version: v1.0
---
```

**Эскиз промпта (ключевые секции):**

```markdown
## Роль

Ты — агент-разработчик. Ты получаешь блок задач (BLOCK-N) и выполняешь их:
код → тесты → линт → коммит. После каждого коммита ты проверяешь границы
автономии и при обнаружении CONFLICT — немедленно останавливаешься.

## Задача

### Алгоритм работы

1. Прочитать контекст: plan-dev.md (BLOCK-N задачи), docs/{svc}.md (Code Map,
   Границы автономии), design.md (SVC-N), conventions.md (shared-интерфейсы,
   конвенции API)
2. Для каждого Issue в блоке (по порядку, пропуская заблокированные):
   a. Прочитать Issue (gh issue view)
   b. Написать код (standard-principles.md)
   c. Запустить тесты (make test)
   d. Запустить линтер (make lint)
   e. Коммит (standard-commit.md)
   f. **CONFLICT-CHECK:** сопоставить изменения с границами автономии
   g. Закрыть Issue (gh issue close)
3. Обновить plan-dev.md: отметить [x] выполненные подзадачи
4. Вернуть отчёт

### CONFLICT-CHECK (обязательный)

После каждого коммита:
1. Прочитать docs/{svc}.md → "Границы автономии LLM"
2. Классифицировать каждое изменение: Свободно / Флаг / CONFLICT
3. Свободно → продолжить
4. Флаг → обновить plan-dev.md, записать в отчёт
5. CONFLICT → СТОП. Определить затронутый уровень (снизу вверх).
   Вернуть отчёт со STATUS: CONFLICT

### Формат результата

STATUS: COMPLETED | CONFLICT | PARTIAL
COMPLETED_ISSUES: [список]
REMAINING_ISSUES: [список]
CONFLICT_INFO: {level, affected_doc, description, last_commit}
FLAGS: [список рабочих правок]
UPDATED_FILES: [список обновлённых документов]
```

**Примечание:** Полный промпт создаётся через `/agent-create` при реализации. Эскиз фиксирует ключевые решения.

---

### 8. /dev SKILL.md

**Текущий** `.claude/skills/dev/SKILL.md` — skill, читает modify-development.md в основном контексте.

**Действие:** Удалить SKILL.md. `/dev` больше не является skill — main LLM распознаёт команду и запускает dev-agent через Task tool.

**Альтернатива:** Сохранить SKILL.md как тонкую обёртку, которая инструктирует main LLM запустить dev-agent. Но это лишний слой — main LLM может читать modify-development.md напрямую (через rule `development.md`).

**Решение:** SKILL.md удаляется. `/dev` обрабатывается main LLM по modify-development.md, который описывает запуск dev-agent.

---

## Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| R1 | G10 → Incorporated | CONFLICT-детекция остаётся на LLM, формализована как обязанность dev-agent |
| R2 | `/dev` = всегда agent | Skill тратит контекст main LLM. Агент изолирован. Если нужна интерактивная работа с кодом — main LLM напрямую, без `/dev` |
| R3 | Блоки BLOCK-N в plan-dev и plan-test | Единица работы для агента. Определяются main LLM при создании документов |
| R4 | Волны (waves) для параллелизма | Топологическая сортировка по зависимостям. Блоки одной волны — параллельно |
| R5 | CONFLICT → остановить всех | CONFLICT меняет specs → остальные агенты работают по устаревшим. Дешевле перезапустить |
| R6 | No file overlap (без worktree) | Правила дизайна блоков вместо git worktree. Shared → INFRA-блок в wave 0. Проще, меньше overhead |
| R7 | Агент пишет в plan-dev.md | Чекбоксы `[x]`, добавление подзадач при "Флаг". Main LLM не нужно отслеживать прогресс по Issues |
| R8 | Агент НЕ пишет в plan-test.md | TC-N — acceptance-сценарии, не исполнение. Изменения тестов — через FLAGS в отчёте |
| R9 | Двухуровневое тестирование | Агент: `make test-{svc}` (unit + integration per-service). После волны: main LLM запускает `make test-e2e` (system/e2e). Требует per-service Makefile таргеты → зависимость от `tests-and-platform` драфта |
| R10 | max_turns = 80, блок до 5 TASK | 5 TASK × 13 turns ≈ 65, запас 15 turns. Рекомендация размера блока: 2-5 TASK-N |
| R11 | Main LLM определяет блоки по документу | Не нужен dev-next-block.py. Main LLM парсит таблицу "Блоки выполнения" из plan-dev.md. `dev-next-issue.py` остаётся для использования агентом внутри блока |
| R12 | Отчёт агента обязателен | Закрытые Issues — трекинг на GitHub. Структурированный отчёт (STATUS, FLAGS, CONFLICT_INFO) — протокол коммуникации агент→main LLM |
| R13 | Test-BLOCK-N = зеркало dev-BLOCK-N | Per-service TC (unit/integration) → в том же BLOCK-N. Системные TC (e2e/load) → отдельный BLOCK в последней волне |
| R14 | Partial resume через REMAINING_ISSUES | Main LLM читает `gh issue list --state closed`, передаёт агенту `REMAINING_ISSUES`. Агент пропускает закрытые |

---

## Закрытые вопросы

### Q1. Скрипт dev-next-issue.py — нужен ли dev-next-block.py?

**Ответ: нет.** Блоки — таблица в plan-dev.md. Main LLM парсит секцию "Блоки выполнения" напрямую (парсинг markdown-таблицы — тривиальная задача для LLM). `dev-next-issue.py` остаётся полезен **внутри агента** — для определения следующего незаблокированного Issue в рамках своего блока.

→ R11

### Q2. Резюме агента vs Issues — нужен ли дополнительный отчёт?

**Ответ: отчёт обязателен.** Закрытые Issues — трекинг на уровне GitHub. Но main LLM нужен **структурированный результат** от агента (STATUS, COMPLETED_ISSUES, FLAGS, CONFLICT_INFO), чтобы:
- Решить: запускать следующую волну или разрешать CONFLICT
- Передать FLAGS в следующую волну (рабочие правки могут влиять на другие блоки)
- Информировать пользователя о прогрессе

Формат отчёта — § 5.2 этого черновика.

→ R12

### Q3. Тестирование блоков — параллельные `make test`

**Проблема:** два агента одновременно запускают `make test` → оба пишут в одну БД, оба поднимают docker-compose, port conflicts.

**Ответ: двухуровневое тестирование.**

1. **Агент тестирует только свой сервис** — `make test-{svc}` (unit + integration per-service). Нет конфликтов, т.к. каждый агент работает с изолированным набором файлов
2. **Main LLM запускает системные тесты после волны** — `make test-e2e` (system/e2e). Все per-service блоки завершены, код стабилен

Это маппится на структуру plan-test: per-service TC (unit/integration) → агент, системные TC (e2e/load из "Системные тест-сценарии") → после волны.

**Зависимость:** требуются per-service Makefile таргеты (`make test-{svc}`, `make lint-{svc}`). Записано в [tests-and-platform драфт](./2026-02-24-tests-and-platform.md).

→ R9

### Q4. Plan-test BLOCK-N — нужны ли отдельно от dev-блоков?

**Ответ: test-BLOCK-N = зеркало dev-BLOCK-N для per-service TC.** Каждый dev-BLOCK имеет соответствующий test-BLOCK с теми же сервисами. Системные TC (e2e/load) выделяются в отдельный test-BLOCK в последней волне.

| Тип TC | Кто выполняет | Когда | Test BLOCK |
|--------|--------------|-------|------------|
| unit, integration (per-service) | Dev-agent как часть BLOCK-N | Во время разработки | Совпадает с dev BLOCK-N |
| e2e, load (system) | Main LLM после волны | После завершения волны | Отдельный BLOCK (последняя волна) |

Нумерация BLOCK-N сквозная и совпадает между plan-dev и plan-test. Маппинг — через колонку "Dev BLOCK" в таблице "Блоки тестирования".

→ R13

### Q5. Partial resume — как передать "начни с Issue #44"

**Проблема:** при CONFLICT и перезапуске агент получает BLOCK-N с некоторыми уже закрытыми Issues. Как не переделывать уже выполненную работу?

**Ответ: main LLM передаёт REMAINING_ISSUES.**

При перезапуске блока:
1. Main LLM читает закрытые Issues: `gh issue list --milestone "{milestone}" --state closed`
2. Main LLM передаёт в prompt агента: `REMAINING_ISSUES: [#44]` (только незакрытые Issues блока)
3. Агент начинает с первого незакрытого, пропускает закрытые
4. Агент дополнительно верифицирует через `gh issue list --state closed` при старте

Формат запуска (§ 5.1) расширяется полем `REMAINING_ISSUES`. Если поле отсутствует — агент работает со всеми Issues блока (первый запуск).

→ R14

### Q6. max_turns — 50 достаточно?

**Расчёт:** На один TASK — ~10-13 turns (read issue, read context, write code, make test, fix, make lint, fix, commit, CONFLICT-CHECK, close issue).

| Размер блока | Turns | Вердикт |
|---|---|---|
| 2 TASK | 26 | Ок при 50 |
| 5 TASK | 65 | Нужно ≥ 80 |
| 8 TASK | 104 | Слишком много |

**Ответ: max_turns = 80, размер блока 2-5 TASK-N.** 5 × 13 = 65, запас 15 turns на непредвиденные ситуации (retry тестов, доп. чтение). При превышении 5 TASK — разбить на два блока.

→ R10

---

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Обновить standard-plan-dev.md — BLOCK-N
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 6.1")
    Обновить specs/.instructions/analysis/plan-dev/standard-plan-dev.md:
    - § 4 "Модель выполнения": заменить "последовательную модель, один агент-кодер" на "блочную параллельную модель" (BLOCK-N, волны, dev-agent)
    - § 5 "Разделы документа": добавить h2 "Блоки выполнения" после "Кросс-сервисные зависимости" с таблицей BLOCK-N (BLOCK, Задачи, Сервисы, Зависимости, Wave)
    - § 7 "Шаблон": добавить секцию "Блоки выполнения"
    - § 8 "Чек-лист качества": добавить проверки — каждый TASK-N в ровно одном BLOCK-N, нет циклических зависимостей, INFRA-блоки в первой волне
  activeForm: Обновляю standard-plan-dev.md

TASK 2: Обновить standard-plan-test.md — блоки тестирования
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 6.2")
    Обновить specs/.instructions/analysis/plan-test/standard-plan-test.md:
    - § 5 "Разделы документа": добавить h2 "Блоки тестирования" после "Матрица покрытия" с таблицей (BLOCK, TC, Сервисы, Dev BLOCK)
    - § 7 "Шаблон": добавить секцию "Блоки тестирования"
    - § 8 "Чек-лист качества": добавить проверки — каждый TC-N в ровно одном BLOCK-N, нумерация блоков совпадает с plan-dev
  activeForm: Обновляю standard-plan-test.md

TASK 3: Обновить standard-analysis.md — CONFLICT при параллельных агентах
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 6.3")
    Обновить specs/.instructions/analysis/standard-analysis.md:
    - § 6.3 "RUNNING to CONFLICT": добавить подсекцию "CONFLICT при параллельных агентах" —
      политика остановки всех агентов, протокол сбора частичных результатов
    - § 6.3 "Обнаружение затронутого уровня": уточнить что агент выполняет обнаружение
      и возвращает в отчёте (level, affected_doc, description)
  activeForm: Обновляю standard-analysis.md

TASK 4: Обновить standard-service.md — Makefile таргеты в Code Map
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 6.7.1")
    Обновить specs/.instructions/docs/service/standard-service.md:
    - § 3 Code Map: добавить п.5 подсекция "Makefile таргеты" (после "Внутренние зависимости",
      перед "Как добавить новый функционал"). Обязательные колонки: Таргет, Команда, Описание.
      Обязательные таргеты: test и lint. Формат имени: {action}-{svc} (kebab-case)
    - § 5 Шаблон: добавить подсекцию "Makefile таргеты" в Code Map
    - § 6 Пример: добавить Makefile таргеты в пример notification
      (make test-notification, make lint-notification, make build-notification)
  activeForm: Обновляю standard-service.md

TASK 5: Обновить create-service.md — шаг создания Makefile таргетов
  blockedBy: [4]
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 6.7.2")
    Обновить specs/.instructions/docs/service/create-service.md:
    - Шаг 5 таблица источников: добавить строку Code Map → Makefile таргеты /
      Источник: Makefile (корневой), src/{svc}/Makefile
    - Новый Шаг 5.1: "Создать per-service Makefile таргеты" — добавить в корневой Makefile
      таргеты test-{svc}, lint-{svc}. Если таргеты уже существуют — проверить соответствие
    - Чек-лист: добавить 2 пункта — per-service Makefile таргеты созданы,
      Code Map содержит подсекцию Makefile таргеты
  activeForm: Обновляю create-service.md

TASK 6: Обновить modify-service.md — сценарий Makefile таргетов
  blockedBy: [4]
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 6.7.3")
    Обновить specs/.instructions/docs/service/modify-service.md:
    - Таблица триггеров: добавить "Добавлен/удалён Makefile таргет" → Code Map → Makefile таргеты
    - Новый Сценарий 8: "Изменены Makefile таргеты" — обновить таблицу в Code Map, валидация
    - Деактивация Шаг 1: добавить удаление per-service таргетов из Makefile
    - Миграция: новый шаг между "Обновить h1" и "Обновить README" —
      переименовать Makefile таргеты (test-{old-svc} → test-{new-svc}, аналогично lint, build)
    - Чек-лист Деактивация: + "Per-service Makefile таргеты удалены"
    - Чек-лист Миграция: + "Makefile таргеты переименованы"
  activeForm: Обновляю modify-service.md

TASK 7: Обновить validation-service.md — SVC011
  blockedBy: [4]
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 6.7.4")
    Обновить specs/.instructions/docs/service/validation-service.md:
    - Коды ошибок: добавить SVC011 — "Per-service Makefile таргеты отсутствуют в Code Map",
      критичность: Предупреждение
    - Шаг 3 таблица обязательных колонок: добавить Code Map → Makefile таргеты /
      Таргет, Команда, Описание
    - Чек-лист: добавить "SVC011: Code Map содержит подсекцию Makefile таргеты"
  activeForm: Обновляю validation-service.md

TASK 8: Миграция стандартов
  blockedBy: [1, 2, 3, 4]
  description: >
    /migration-create для каждого изменённого стандарта:
    - standard-plan-dev.md
    - standard-plan-test.md
    - standard-analysis.md
    - standard-service.md
    Синхронизировать все зависимые файлы (валидации, скрипты, воркфлоу).
  activeForm: Мигрирую зависимости стандартов

TASK 9: Валидация миграций
  blockedBy: [8]
  description: >
    /migration-validate для каждого стандарта из TASK 8.
    Убедиться что все зависимые файлы синхронизированы.
  activeForm: Валидирую миграции

TASK 10: Создать dev-agent AGENT.md
  blockedBy: [1, 2, 3]
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 7")
    /agent-create для .claude/agents/dev-agent/AGENT.md.
    Конфигурация: model=sonnet, tools=Read/Bash/Glob/Grep/Write/Edit,
    disallowedTools=WebSearch/WebFetch, max_turns=80.
    Промпт: алгоритм работы (read context → iterate issues → code → test → lint → commit →
    CONFLICT-CHECK → close issue → report).
    CONFLICT-CHECK: обязательный после каждого коммита (docs/{svc}.md → Границы автономии →
    классификация Свободно/Флаг/CONFLICT).
    Формат результата: STATUS, COMPLETED_ISSUES, REMAINING_ISSUES, CONFLICT_INFO, FLAGS, UPDATED_FILES.
  activeForm: Создаю dev-agent

TASK 11: Переписать modify-development.md — агентная модель
  blockedBy: [10]
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 6.4")
    Полный rewrite .github/.instructions/development/modify-development.md:
    - Шаг 1: Определить блоки и волны (из plan-dev.md) вместо "определить следующий Issue"
    - Шаг 2: Запуск волны (N параллельных Task вызовов dev-agent)
    - Шаг 3: Сбор результатов, обработка CONFLICT (TaskStop, partial results)
    - Шаг 4: Следующая волна или REVIEW
    - Переходы: RUNNING→CONFLICT, RUNNING→REVIEW с агентной спецификой
  activeForm: Переписываю modify-development.md

TASK 12: Удалить /dev SKILL.md
  blockedBy: [10]
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 8")
    /skill-modify --deactivate для .claude/skills/dev/SKILL.md.
    /dev больше не является скиллом — main LLM распознаёт команду
    и запускает dev-agent через Task tool по modify-development.md.
  activeForm: Удаляю /dev SKILL.md

TASK 13: Обновить standard-development.md — ссылки на агента
  blockedBy: [10]
  description: >
    Обновить .github/.instructions/development/standard-development.md:
    - Ссылки на dev-agent вместо /dev скилла
    - Описание агентной модели разработки
  activeForm: Обновляю standard-development.md

TASK 14: Обновить development README.md
  blockedBy: [10, 11, 12]
  description: >
    Обновить .github/.instructions/development/README.md:
    - Ссылка на dev-agent вместо скилла /dev
    - Обновить описание воркфлоу разработки
    README обновляется автоматически при создании артефактов, но проверить полноту.
  activeForm: Обновляю development README.md

TASK 15: Обновить standard-process.md §10 G10 + §5 + §8
  blockedBy: [10]
  description: >
    Драфт: .claude/drafts/2026-02-24-conflict-detect.md (секция "§ 6.6")
    Обновить specs/.instructions/standard-process.md:
    - § 10 G10: закрыть — "Incorporated — CONFLICT-детекция формализована как обязанность dev-agent"
    - § 5 Фаза 3: обновить ссылку на dev-agent вместо скилла
    - § 8 Сводная таблица: обновить строку "3.1 Dev cycle" — dev-agent + modify-development.md
  activeForm: Обновляю standard-process.md

TASK 16: Обновить CLAUDE.md
  blockedBy: [15]
  description: >
    В CLAUDE.md отметить conflict-detect (G10) как [x] выполненный.
  activeForm: Обновляю CLAUDE.md
```
