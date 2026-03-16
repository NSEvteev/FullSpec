---
description: Воркфлоу создания документа плана разработки SDD — скрипт файла, Clarify, агенты (plandev-agent + plandev-reviewer), валидация, синхронизация plan-test.md.
standard: .instructions/standard-instruction.md
standard-version: v1.7
index: specs/.instructions/README.md
---

# Воркфлоу создания плана разработки

Рабочая версия стандарта: 1.7

Пошаговый процесс создания нового документа плана разработки (`specs/analysis/NNNN-{topic}/plan-dev.md`).

**Полезные ссылки:**
- [Стандарт плана разработки](./standard-plan-dev.md)
- [Стандарт аналитического контура](../standard-analysis.md) — статусы, Clarify, маркеры, общий паттерн объекта
- [Инструкции specs/](../../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-plan-dev.md](./standard-plan-dev.md) |
| Валидация | [validation-plan-dev.md](./validation-plan-dev.md) |
| Создание | Этот документ |
| Модификация | [modify-plan-dev.md](./modify-plan-dev.md) |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить parent Plan Tests](#шаг-1-проверить-parent-plan-tests)
  - [Шаг 2: Создать файл скриптом](#шаг-2-создать-файл-скриптом)
  - [Шаг 3: Определить scope](#шаг-3-определить-scope)
  - [Шаг 4: Clarify](#шаг-4-clarify)
  - [Шаг 5: Волна 1 — plandev-agent](#шаг-5-волна-1-plandev-agent)
  - [Шаг 6: Волна 2 — plandev-reviewer](#шаг-6-волна-2-plandev-reviewer)
  - [Шаг 7: Волна 3 — исправления](#шаг-7-волна-3-исправления)
  - [Шаг 8: Синхронизация plan-test.md](#шаг-8-синхронизация-plan-testmd)
  - [Шаг 9: README + Валидация](#шаг-9-readme-валидация)
  - [Шаг 10: Ревью пользователем](#шаг-10-ревью-пользователем)
  - [Шаг 11: Создание review.md и WAITING](#шаг-11-создание-reviewmd-и-waiting)
  - [Шаг 12: Отчёт о выполнении](#шаг-12-отчёт-о-выполнении)
  - [Шаг 13: Предложить запуск разработки](#шаг-13-предложить-запуск-разработки)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Plan Dev — после Plan Tests.** Plan Dev создаётся только после одобрения Plan Tests (статус WAITING). Без Plan Tests — нет Plan Dev.

> **Зона: WHAT TASKS.** Plan Dev определяет задачи реализации. Тестовые сценарии — Plan Tests, архитектура — Design, бизнес-требования — Discussion.

> **Файл создаётся скриптом.** Скрипт `create-analysis-plan-dev-file.py` создаёт файл с заполненным frontmatter и пустыми per-service секциями из SVC-N в Design. Это обеспечивает resumability и единообразие.

> **Агенты генерируют, оркестратор координирует.** plandev-agent генерирует TASK-N (3 вызова: INFRA + per-service + system), plandev-reviewer проверяет покрытие и записывает PROP-N. Оркестратор управляет: Clarify, review, статусы.

> **Терминальный объект.** Plan Dev — конец цепочки. Поле `children` в frontmatter запрещено.

---

## Шаги

### Шаг 1: Проверить parent Plan Tests

**SSOT:** [standard-plan-dev.md § 1](./standard-plan-dev.md#1-назначение)

1. Проверить, что Plan Tests существует в `specs/analysis/NNNN-{topic}/plan-test.md`
2. Проверить, что `status: WAITING` в frontmatter Plan Tests
3. Если Plan Tests не в WAITING — **СТОП**: «Plan Dev может быть создан только после одобрения Plan Tests»

### Шаг 2: Создать файл скриптом

```bash
python specs/.instructions/.scripts/create-analysis-plan-dev-file.py {branch}
```

Скрипт автоматически:
- Читает frontmatter plan-test.md (проверяет статус WAITING)
- Извлекает milestone из discussion.md
- Извлекает SVC-N заголовки из design.md
- Создаёт `plan-dev.md` с заполненным frontmatter и пустыми per-service секциями

**После создания:** обновить `children` в parent Plan Tests — добавить путь к plan-dev.md.

### Шаг 3: Определить scope

Прочитать 4 источника и определить scope работ:

| # | Источник | Что извлечь |
|---|---------|-------------|
| 1 | **Plan Tests** | TC-N сценарии — определить задачи по реализации тестов и кода |
| 2 | **Design SVC-N** | Подсекции §§ 1-8 (delta) + § 9 решения — определить что менять в коде |
| 3 | **Discussion REQ-N** | Приоритеты требований — расставить приоритеты задач |
| 4 | **`specs/docs/{svc}.md`** | Текущий AS IS (Code Map, зависимости) — контекст объёма работ |

**Результат:** список SVC-N с описанием scope, список TC-N, список STS-N, список REQ-N — для передачи в промпт агентов.

### Шаг 4: Clarify

**SSOT:** [standard-plan-dev.md § 6](./standard-plan-dev.md#6-clarify), [Стандарт analysis/ § 8](../standard-analysis.md#8-clarify-и-блокирующие-правила)

**Если `--auto-clarify` НЕ указан:**

LLM **сам предлагает** и уточняет через AskUserQuestion:

| Что предлагает LLM | Пример |
|---------------------|--------|
| Приоритеты задач | «Реализация auth важнее gateway? Порядок?» |
| Порядок реализации | «Начать с shared-схем или с бизнес-логики?» |
| Детализация подзадач | «Достаточно ли разбить на 3 подзадачи или детализировать?» |
| Ресурсы | «Есть ли ограничения по времени на конкретные задачи?» |

**Если `--auto-clarify` указан:**

LLM пропускает Clarify, генерирует документ на основе источников и ставит маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` на все неясности.

### Шаг 5: Волна 1 — plandev-agent

**Агент:** [plandev-agent](/.claude/agents/plandev-agent/AGENT.md)

Запустить **последовательно** через Task tool три вызова plandev-agent с разными `mode`:

**5.1. mode=INFRA** (первый — wave 0):

```
Промпт оркестратора → plandev-agent:
- mode: INFRA
- plan-dev.md: specs/analysis/NNNN-{topic}/plan-dev.md
- design.md: specs/analysis/NNNN-{topic}/design.md
- plan-test.md: specs/analysis/NNNN-{topic}/plan-test.md
- discussion.md: specs/analysis/NNNN-{topic}/discussion.md
- Ответы Clarify: {ответы из шага 4}
- Текущий max TASK-N: 0
```

**5.2. mode=per-service** (для каждого SVC-N — последовательно):

```
Промпт оркестратора → plandev-agent:
- mode: per-service
- SVC-N: SVC-1: {name}
- plan-dev.md: ...
- Текущий max TASK-N: {max из предыдущего вызова}
```

Повторить для каждого SVC-N.

**5.3. mode=system** (последний — системные тесты, кросс-зависимости, BLOCK-N; тестовые TC: 1 TC = 1 BLOCK по умолчанию):

```
Промпт оркестратора → plandev-agent:
- mode: system
- plan-dev.md: ...
- Текущий max TASK-N: {max из предыдущего вызова}
```

**После всех вызовов:** оркестратор проверяет сквозную нумерацию TASK-N (без дублей, без пропусков).

### Шаг 6: Волна 2 — plandev-reviewer

**Агент:** [plandev-reviewer](/.claude/agents/plandev-reviewer/AGENT.md)

Запустить через Task tool:

```
Промпт оркестратора → plandev-reviewer:
- plan-dev.md: specs/analysis/NNNN-{topic}/plan-dev.md
- design.md: specs/analysis/NNNN-{topic}/design.md
- plan-test.md: specs/analysis/NNNN-{topic}/plan-test.md
- discussion.md: specs/analysis/NNNN-{topic}/discussion.md
```

**Результат:** вердикт ACCEPT или REVISE + PROP-N записи в секции "Предложения".

| Вердикт | Действие |
|---------|----------|
| ACCEPT | → обработать PROP-N пользователем (см. ниже) → продолжить с шага 8 |
| REVISE | → перейти к шагу 7 |

**При ACCEPT:** обработать PROP-N (оркестратор, НЕ агент):
   - PROP-N обрабатываются пачками по 4 через AskUserQuestion (лимит инструмента — 4 вопроса)
   - Каждый AskUserQuestion содержит до 4 PROP с вариантами (принять / отклонить)
   - Если PROP больше 4 — следующая пачка после ответа на предыдущую
   - **ВАЖНО: обрабатывать PROP по одному через Edit, НЕ заменять секцию «Предложения» целиком.**
     Для каждого PROP после получения ответа:
     - Принятый PROP:
       (a) применить основную правку к содержимому документа
       (b) Grep по документу на все связанные термины/секции из правки
       (c) распространить изменение на все затронутые места (TASK-N, подзадачи, зависимости, BLOCK-N, маппинг Issues)
       (d) удалить строку PROP из секции «Предложения»
     - Отклонённый PROP: (a) удалить строку PROP из секции «Предложения», (b) добавить в секцию «Отвергнутые предложения» (с указанием причины)
   - После обработки всех PROP: оставить секцию с текстом `_Все предложения обработаны._`. Секция «Отвергнутые предложения» сохраняется.

### Шаг 7: Волна 3 — исправления

**При REVISE:** перезапустить plandev-agent с mode=system (исправления по PROP-N):

```
Промпт оркестратора → plandev-agent:
- mode: system
- Контекст: PROP-N записи из "Предложения" (P1, P2)
- Действие: исправить расхождения, перенести принятые PROP-N в "Отвергнутые предложения" или удалить из "Предложения"
```

После исправлений → перезапустить plandev-reviewer (шаг 6).

**Максимум 3 итерации** (шаги 6-7). При 3+ REVISE — эскалация пользователю:

AskUserQuestion: «plandev-reviewer отклонил 3 раза. Варианты:»
1. Принять текущую версию (ACCEPT с замечаниями)
2. Просмотреть PROP-N и решить вручную
3. Откатить план разработки

### Шаг 8: Синхронизация plan-test.md

Обновить таблицу "Блоки тестирования" в plan-test.md: синхронизировать колонку "Dev BLOCK" с BLOCK-N из plan-dev.md.

1. Прочитать таблицу BLOCK-N из plan-dev.md
2. Для каждого BLOCK-N определить маппинг TC-N → Dev BLOCK
3. Обновить колонку "Dev BLOCK" в таблице "Блоки тестирования" plan-test.md через Edit

**Маркеры:** Если сложность соответствия высока — ставить `[ТРЕБУЕТ УТОЧНЕНИЯ]` и уточнять.

### Шаг 9: README + Валидация

**9.1. Регистрация в README:**

Обновить запись в `specs/analysis/README.md` — колонка Plan Dev.

**9.2. Валидация:**

```bash
python specs/.instructions/.scripts/validate-analysis-plan-dev.py specs/analysis/NNNN-{topic}/plan-dev.md
```

**Если скрипт недоступен:** пройти чек-лист из [validation-plan-dev.md](./validation-plan-dev.md).

Исправить ошибки до продолжения.

**9.3. Разрешение маркеров:**

1. Проверить документ на наличие `[ТРЕБУЕТ УТОЧНЕНИЯ]` маркеров
2. Если маркеры есть — для каждого маркера уточнить через AskUserQuestion
3. Заменить маркеры на ответы пользователя
4. Повторять пока маркеров = 0

### Шаг 10: Ревью пользователем

**Перед вопросом:** проверить что маркеров = 0 и валидация пройдена. Если нет — вернуться к шагу 9.

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: «План разработки готов. Всё корректно?»

| Ответ | Действие |
|-------|----------|
| Да, всё корректно | → продолжить с шага 11 |
| Нет, нужны правки | Внести изменения → продолжить с шага 9 |

### Шаг 11: Создание review.md и WAITING

1. Вызвать `/review-create` — создаёт `review.md` с секцией "Контекст ревью" на основе цепочки документов.

   `/review-create` вызывается **после** одобрения пользователем, **перед** переходом статуса. Это гарантирует, что review.md создаётся только для одобренных Plan Dev.

2. **Переход DRAFT → WAITING** — через модуль `chain_status.py` (SSOT статусов):

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="WAITING", document="plan-dev")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

- `result.side_effects` — включает "Создать review.md" (уже выполнено выше)
- `result.auto_propose` — предложение следующего шага (`/dev-create NNNN`)

### Шаг 12: Отчёт о выполнении

Вывести отчёт:

```
## Отчёт о создании плана разработки

Создан план разработки: `specs/analysis/NNNN-{topic}/plan-dev.md`

Описание: {description}

Milestone: {vX.Y.Z}

Сервисы:
- {Сервис 1}: {N} TASK-N (средняя сложность: {S}/10)
- ...

Всего TASK-N: {итого}
Средняя сложность: {S}/10

Кросс-сервисные зависимости: {N}

Покрытие:
- TC-N: {X}/{Y} покрыты TASK-N

Агенты:
- plandev-agent: {N} вызовов (INFRA + {N} per-service + system)
- plandev-reviewer: {вердикт} ({N} итераций)

Статус: DRAFT → WAITING

Валидация: пройдена
```

### Шаг 13: Предложить запуск разработки

Проверить: все ли 4 документа цепочки в WAITING.

| Все в WAITING? | Действие |
|----------------|----------|
| Да | AskUserQuestion: "Все спецификации готовы. Начать разработку через `/dev-create {NNNN}`?" |
| Нет | Вывести: "Plan Dev → WAITING. Ожидают: {список документов не в WAITING}" |

При подтверждении → выполнить `/dev-create {NNNN}`.

---

## Чек-лист

### Подготовка
- [ ] Parent Plan Tests в статусе WAITING
- [ ] Файл создан скриптом (create-analysis-plan-dev-file.py)
- [ ] `children` в parent Plan Tests обновлён

### Источники и Clarify
- [ ] Plan Tests прочитан целиком (TC-N)
- [ ] Design прочитан (SVC-N, INT-N, STS-N)
- [ ] Discussion прочитана (REQ-N, приоритеты)
- [ ] specs/docs/{svc}.md прочитаны (AS IS)
- [ ] Clarify проведён (или `--auto-clarify`)

### Волна 1: plandev-agent
- [ ] mode=INFRA: INFRA-задачи сгенерированы (wave 0)
- [ ] mode=per-service: для каждого SVC-N TASK-N сгенерированы
- [ ] mode=system: системные задачи, кросс-зависимости, BLOCK-N (тестовые TC: 1 TC = 1 BLOCK) сгенерированы
- [ ] Нумерация TASK-N сквозная (без дублей)

### Волна 2: plandev-reviewer
- [ ] Вердикт ACCEPT или REVISE
- [ ] PROP-N записаны в секцию "Предложения"

### Волна 3: исправления (при REVISE)
- [ ] Исправления внесены (макс 3 итерации)
- [ ] ACCEPT получен или эскалация пользователю

### Синхронизация
- [ ] plan-test.md: колонка "Dev BLOCK" обновлена

### Проверка
- [ ] Все маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` разрешены (0 неразрешённых)
- [ ] Валидация пройдена (скрипт или чек-лист)
- [ ] Запись обновлена в README
- [ ] Ревью пользователем пройдено
- [ ] `/review-create` выполнен — review.md создан
- [ ] Статус переведён в WAITING
- [ ] README обновлён (статус WAITING)
- [ ] Отчёт выведен
- [ ] Предложен запуск разработки (если все 4 в WAITING)

---

## Примеры

### Создание Plan Dev для OAuth2

```
Пользователь: "Создать Plan Dev для OAuth2 авторизации"

1. Parent: specs/analysis/0001-oauth2-authorization/plan-test.md → WAITING ✓
2. Скрипт: python create-analysis-plan-dev-file.py 0001-oauth2-authorization → plan-dev.md
3. Scope: 3 SVC-N (auth, gateway, users), 14 TC-N, 5 REQ-N
4. Clarify: порядок — сначала auth, затем gateway, приоритет — high для core auth
5. Волна 1 — plandev-agent:
   5.1. mode=INFRA: TASK-1 (docker-compose), TASK-2 (shared config)
   5.2. mode=per-service (auth): TASK-3..6, (gateway): TASK-7..8, (users): TASK-9..11
   5.3. mode=system: кросс-зависимости, BLOCK-N (тестовые TC: 1 TC = 1 BLOCK, 7 блоков, 3 волны)
6. Волна 2 — plandev-reviewer: ACCEPT (0 P1, 1 P3)
7. (пропущен — ACCEPT)
8. plan-test.md: Dev BLOCK синхронизированы
9. README + Валидация → OK
10. Ревью: "Да"
11. /review-create → review.md → DRAFT → WAITING
12. Отчёт: 3 сервиса, 11 TASK-N, средняя сложность 5.2/10
13. "Все спецификации готовы. Начать через /dev-create 0001?" → Да
```

### Создание с --auto-clarify и REVISE

```
Пользователь: "Создать Plan Dev для 0003-cache-optimization, --auto-clarify"

1. Parent: plan-test.md → WAITING ✓
2. Скрипт → plan-dev.md
3. Scope: 1 SVC-N (catalog), 4 TC-N
4. Clarify пропущен — маркеры на неясности
5. Волна 1 — plandev-agent: INFRA (1 TASK) + per-service (3 TASK) + system
6. Волна 2 — plandev-reviewer: REVISE (1 P1: TC-3 не покрыт)
7. Волна 3: plandev-agent mode=system → исправлен → plandev-reviewer: ACCEPT
8. plan-test.md: Dev BLOCK синхронизированы
9. README + Валидация → Разрешение маркеров через AskUserQuestion → OK
10. Ревью → "Да"
11. /review-create → WAITING
12. Отчёт
13. Предложен /dev-create
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [create-analysis-plan-dev-file.py](../../.scripts/create-analysis-plan-dev-file.py) | Создание файла plan-dev.md по шаблону (шаг 2) | Этот документ |
| [validate-analysis-plan-dev.py](../../.scripts/validate-analysis-plan-dev.py) | Валидация созданного документа (шаг 9) | [validation-plan-dev.md](./validation-plan-dev.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/plan-dev-create](/.claude/skills/plan-dev-create/SKILL.md) | Создание документа плана разработки | Этот документ |
