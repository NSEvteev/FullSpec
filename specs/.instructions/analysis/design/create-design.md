---
description: Воркфлоу создания документа проектирования SDD — Unified Scan, Clarify, генерация SVC-N/INT-N/STS-N, валидация, перевод DRAFT → WAITING.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу создания проектирования

Рабочая версия стандарта: 2.2

Пошаговый процесс создания нового документа проектирования (`specs/analysis/NNNN-{topic}/design.md`).

**Полезные ссылки:**
- [Стандарт проектирования](./standard-design.md)
- [Стандарт аналитического контура](../standard-analysis.md) — статусы, Clarify, маркеры, общий паттерн объекта
- [Инструкции specs/](../../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-design.md](./standard-design.md) |
| Валидация | [validation-design.md](./validation-design.md) |
| Создание | Этот документ |
| Модификация | [modify-design.md](./modify-design.md) |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить parent Discussion](#шаг-1-проверить-parent-discussion)
  - [Шаг 2: Создать файл из шаблона (скрипт)](#шаг-2-создать-файл-из-шаблона-скрипт)
  - [Шаг 3a: Делегировать design-agent-first](#шаг-3a-делегировать-design-agent-first-unified-scan--clarify--технологии)
  - [Шаг 3b: Подтверждение сервисов и технологий](#шаг-3b-подтверждение-сервисов-и-технологий)
  - [Шаг 3c: Делегировать design-agent-second](#шаг-3c-делегировать-design-agent-second-svc-n--int-n--sts-n)
  - [Шаг 4: Регистрация в README](#шаг-4-регистрация-в-readme)
  - [Шаг 5: Ревью агентом (обязательно)](#шаг-5-ревью-агентом-обязательно)
  - [Шаг 6: Ревью пользователем](#шаг-6-ревью-пользователем)
  - [Шаг 7: DRAFT → WAITING](#шаг-7-draft--waiting)
  - [Шаг 8: Отчёт о выполнении](#шаг-8-отчёт-о-выполнении)
  - [Шаг 9: Авто-предложение следующего этапа](#шаг-9-авто-предложение-следующего-этапа)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)
- [Агенты](#агенты)

---

## Принципы

> **Design — после Discussion.** Design создаётся только после одобрения Discussion (статус WAITING). Без Discussion — нет Design.

> **Зона: AFFECTED + HOW + DETAILS.** Design распределяет ответственности между сервисами и определяет контракты. Бизнес-требования — Discussion, тесты — Plan Tests, задачи — Plan Dev.

> **Файл до Scan.** Сначала создать файл из шаблона и заполнить frontmatter — затем выполнять Unified Scan. Это обеспечивает resumability при прерывании.

> **Unified Scan до Clarify.** LLM читает 5 источников, составляет предложение по сервисам — затем уточняет у пользователя.

> **LLM предлагает, пользователь подтверждает.** LLM сам анализирует и предлагает распределение. НЕ спрашивает «как распределить?»

> **9 подсекций SVC-N.** §§ 1-8 зеркалят {svc}.md, § 9 — Design-only WHY.

> **AGENT REVIEW обязателен.** design-reviewer вызывается всегда из-за сложности документа.

---

## Шаги

### Шаг 1: Проверить parent Discussion

**SSOT:** [standard-design.md § 1](./standard-design.md#1-назначение)

1. Проверить, что Discussion существует в `specs/analysis/NNNN-{topic}/discussion.md`
2. Проверить, что `status: WAITING` в frontmatter Discussion
3. Если Discussion не в WAITING — **СТОП**: «Design может быть создан только после одобрения Discussion»

### Шаг 2: Создать файл из шаблона (скрипт)

**Скрипт:** [create-analysis-design-file.py](../../.scripts/create-analysis-design-file.py)

Скрипт автоматически:
- Проверяет наличие discussion.md и статус WAITING
- Копирует milestone из parent Discussion
- Заполняет frontmatter по [standard-design.md § 3](./standard-design.md#3-frontmatter)
- Создаёт файл из шаблона [standard-design.md § 7](./standard-design.md#7-шаблон)

```bash
python specs/.instructions/.scripts/create-analysis-design-file.py NNNN-{topic}
```

### Шаг 3a: Делегировать design-agent-first (Unified Scan + Clarify + технологии)

**Агент:** [design-agent-first](/.claude/agents/design-agent-first/AGENT.md)

**ОБЯЗАТЕЛЬНО** делегировать design-agent-first через Task tool. Агент выполняет первую фазу:

1. **Unified Scan** — чтение 5 источников ([standard-design.md § 1](./standard-design.md#1-назначение))
2. **Clarify** — уточнение сервисов и технологий через AskUserQuestion ([standard-design.md § 6](./standard-design.md#6-clarify))
3. **Генерация** — заполнение Резюме + секция "Выбор технологий" (7 критериев, AskUserQuestion пачками по 4, **инкрементальная запись** после каждой пачки ответов) + заголовки SVC-N (h2, с кратким описанием + стек, без подсекций)
4. **Разрешение маркеров** — все `[ТРЕБУЕТ УТОЧНЕНИЯ]` → 0 (кроме `--auto-clarify`)
5. **Частичная валидация** — Резюме + Выбор технологий + заголовки
6. **Сохранение шаблона** — placeholder-секции (### 1-9, INT-N, STS-N) НЕ удаляются

```
Task tool:
  subagent_type: design-agent-first
  prompt: >
    Заполнить первую часть документа проектирования specs/analysis/NNNN-{topic}/design.md.
    Parent Discussion: specs/analysis/NNNN-{topic}/discussion.md.
    {--auto-clarify если указан}
```

**Результат:** partial design.md (Резюме + Выбор технологий с "Выбрано" + заголовки SVC-N с описанием). Placeholder-секции из шаблона (### 1-9, INT-N, STS-N) сохранены для design-agent-second.

### Шаг 3b: Подтверждение сервисов и технологий

**БЛОКИРУЮЩЕЕ.** Оркестратор проверяет результат design-agent-first и подтверждает с пользователем.

**При `--auto-clarify`:** разрешить маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` в "Выбрано" через AskUserQuestion перед запуском design-agent-second.

**AskUserQuestion:** «Сервисы и технологии определены (Резюме + Выбор технологий). Подтверждаете?»

| Ответ | Действие |
|-------|----------|
| Да, подтверждаю | Перейти к шагу 3c |
| Нет, нужны изменения | Указать правки → Edit design.md → повторить шаг 3b |
| Вернуться к шагу 3a | Перезапустить design-agent-first |

### Шаг 3c: Делегировать design-agent-second (SVC-N + INT-N + STS-N)

**Агент:** [design-agent-second](/.claude/agents/design-agent-second/AGENT.md)

**ОБЯЗАТЕЛЬНО** делегировать design-agent-second через Task tool. Агент выполняет вторую фазу:

1. **Чтение контекста** — partial design.md + Discussion + overview.md + {svc}.md + per-tech стандарты (naming conventions)
2. **Генерация** — заполнение подсекций SVC-N (9 шт.), INT-N, STS-N на основе выбранного стека. **При генерации § 5 Code Map** — пути по конвенции монорепо (см. [standard-design.md § 5, Правила путей](./standard-design.md#5-разделы-документа)): `src/{svc}/components/`, без вложенного `src/` внутри сервиса
3. **Разрешение маркеров** — все `[ТРЕБУЕТ УТОЧНЕНИЯ]` → 0
4. **Полная валидация** — `validate-analysis-design.py`

```
Task tool:
  subagent_type: design-agent-second
  prompt: >
    Заполнить вторую часть документа проектирования specs/analysis/NNNN-{topic}/design.md.
    Parent Discussion: specs/analysis/NNNN-{topic}/discussion.md.
```

**Результат:** полный design.md (Резюме + Выбор технологий + SVC-N с подсекциями + INT-N + STS-N).

**Почему два агента:** Design — самый сложный документ. Разделение на две фазы позволяет: (1) пользователю подтвердить технологии ДО генерации контрактов и моделей, (2) каждому агенту работать с меньшим контекстом, (3) design-agent-second опираться на уже выбранный стек.

**Оркестратор НЕ выполняет** Unified Scan, Clarify и генерацию самостоятельно.

### Шаг 4: Регистрация в README

Обновить таблицу Цепочки (колонка Design) и dashboard статусов:

1. В таблице **Цепочки** — вручную добавить `design.md` в колонку Design
2. В таблице **Статусы цепочек** — **только через скрипт:**

```bash
python specs/.instructions/.scripts/analysis-status.py --update
```

**ЗАПРЕЩЕНО** редактировать блок `<!-- BEGIN:analysis-status -->...<!-- END:analysis-status -->` вручную.

### Шаг 5: Ревью агентом (обязательно)

**Агент:** [design-reviewer](/.claude/agents/design-reviewer/AGENT.md)

Design-reviewer вызывается **обязательно** после валидации (исключение из общего правила «опционально» в [standard-analysis.md § 2.4](../standard-analysis.md#24-общий-паттерн-объекта)).

1. Запустить агента `design-reviewer` с путём к документу
2. Агент проверяет: распределение ответственностей, полноту 9 подсекций SVC-N, delta-формат, перекрёстные ссылки INT-N ↔ SVC-N § 6, честность оценок технологий, feasibility check
3. Агент записывает рекомендации (PROP-N) в секцию «Предложения» (после STS-N)
4. **Классификация предложений** (перед обработкой):
   Для каждого PROP определить тип:
   | Тип | Критерий | Действие |
   |-----|----------|----------|
   | **Формальный** | Очевидное уточнение, идемпотентность, safety, единственный разумный вариант | Принять автоматически |
   | **Решение** | Есть несколько разумных вариантов, требуется выбор пользователя | AskUserQuestion с рекомендацией |
   - Формальные PROP: применить все, показать пользователю список "Автоматически приняты: PROP-X, PROP-Y, PROP-Z"
   - Решения: обрабатывать пачками по 4 через AskUserQuestion, рекомендованный вариант первым + "(рекомендуется)"
5. Обработка предложений (оркестратор, НЕ агент):
   - PROP-N типа "Решение" обрабатываются пачками по 4 через AskUserQuestion (лимит инструмента — 4 вопроса)
   - Каждый AskUserQuestion содержит до 4 PROP с вариантами (принять / отклонить), рекомендованный вариант первым + "(рекомендуется)"
   - Если PROP больше 4 — следующая пачка после ответа на предыдущую
   - **ВАЖНО: обрабатывать PROP по одному через Edit, НЕ заменять секцию «Предложения» целиком.**
     Для каждого PROP после получения ответа:
     - Принятый PROP:
       (a) применить основную правку к содержимому документа
       (b) Grep по документу на все связанные термины/поля/endpoints из правки
       (c) распространить изменение на все затронутые места (§2 API, §3 Data Model, §4 Потоки, §5 Code Map, INT-N контракты и sequences, STS-N сценарии, §9 Решения)
       (d) удалить строку PROP из секции «Предложения»
     - Отклонённый PROP: (a) удалить строку PROP из секции «Предложения», (b) добавить в секцию «Отвергнутые предложения» (создать секцию, если не существует)
   - **Upward feedback PROP (↑ Discussion):** принятый upward PROP обновляет parent Discussion (REQ-N / F-N) → обязательно провалидировать discussion.md после изменения
   - После обработки всех PROP: если секция «Предложения» пуста — оставить секцию с текстом `_Все предложения обработаны._`. Секция «Отвергнутые предложения» сохраняется.
5. Перевалидация: `validate-analysis-design.py`

### Шаг 6: Ревью пользователем

**Перед вопросом:** проверить что маркеров = 0 и валидация пройдена. Если нет — вернуться к шагу 3.

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: «Документ проектирования готов. Выберите действие:»

| Ответ | Действие |
|-------|----------|
| Повторный ревью (Recommended) | Повторить шаг 5 (design-reviewer) |
| Да, всё корректно | Перевести DRAFT → WAITING через `chain_status.py` (см. шаг 7) → шаг 7 |
| Нет, нужны правки | Внести изменения → перевалидация → повторить шаг 6 |

### Шаг 7: DRAFT → WAITING

**SSOT:** [standard-design.md § 4](./standard-design.md#4-переходы-статусов)

**Переход DRAFT → WAITING** — через модуль `chain_status.py` (SSOT статусов):

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="WAITING", document="design")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

> **Артефакты specs/docs/ (per-service, per-tech, overview.md) НЕ создаются при Design → WAITING.** Они создаются на отдельном шаге `/docs-sync` после завершения аналитической цепочки (все 4 документа в WAITING). См. [create-docs-sync.md](../../create-docs-sync.md).

### Шаг 8: Отчёт о выполнении

Вывести отчёт:

```
## Отчёт о создании проектирования

Создано проектирование: `specs/analysis/NNNN-{topic}/design.md`

Описание: {description}

Milestone: {vX.Y.Z}

Сервисы:
- SVC-1: {имя} ({основной/вторичный/новый})
- ...

Взаимодействия: {N} INT-N блоков
Системные тесты: {N} STS-N сценариев

Статус: DRAFT → WAITING

Следующий шаг: Создать Plan Tests (артефакты specs/docs/ — через /docs-sync после аналитической цепочки)

Валидация: пройдена
```

### Шаг 9: Авто-предложение следующего этапа

AskUserQuestion: «Перейти к созданию Plan Tests?»

| Ответ | Действие |
|-------|----------|
| Да | Вызвать воркфлоу создания Plan Tests с путём к текущему Design |
| Нет | Завершить воркфлоу |

---

## Чек-лист

### Подготовка (шаги 1-2)
- [ ] Parent Discussion в статусе WAITING
- [ ] Файл создан скриптом `create-analysis-design-file.py`
- [ ] Frontmatter заполнен (базовые поля, milestone из Discussion)

### Генерация — фаза 1: design-agent-first (шаг 3a)
- [ ] design-agent-first делегирован через Task tool
- [ ] Unified Scan выполнен (Discussion + specs/docs/)
- [ ] Clarify проведён (или `--auto-clarify`)
- [ ] Сервисы определены (основной/вторичный/новый)
- [ ] Резюме заполнено
- [ ] Секция "Выбор технологий" заполнена с "Выбрано" (инкрементально после каждой пачки)
- [ ] Заголовки SVC-N добавлены (h2, с описанием + стек, без подсекций)
- [ ] Placeholder-секции шаблона сохранены (### 1-9, INT-N, STS-N)
- [ ] Частичная валидация пройдена

### Подтверждение (шаг 3b)
- [ ] Пользователь подтвердил сервисы и технологии
- [ ] При `--auto-clarify`: маркеры в "Выбрано" разрешены

### Генерация — фаза 2: design-agent-second (шаг 3c)
- [ ] design-agent-second делегирован через Task tool
- [ ] Per-tech стандарты прочитаны (naming conventions для API/событий)
- [ ] conventions.md прочитан (формат ответов/ошибок для § 2 и INT-N)
- [ ] testing.md прочитан (стратегия тестирования для STS-N)
- [ ] Все SVC-N: описание + 9 подсекций (§ 1, § 9 — контент)
- [ ] SVC-N § 5 Code Map: пути по конвенции монорепо (`src/{svc}/`, без вложенного `src/`)
- [ ] INT-N с метаданными, контрактом и sequence
- [ ] STS-N таблица (или заглушка)
- [ ] Все маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` разрешены (0 неразрешённых)
- [ ] Полная валидация пройдена

### Проверка (шаги 4-9)
- [ ] Запись обновлена в README (шаг 4)
- [ ] Ревью design-reviewer проведено — обязательно (шаг 5)
- [ ] Ревью пользователем пройдено (шаг 6)
- [ ] Статус переведён в WAITING (шаг 7)
- [ ] README обновлён (статус WAITING)
- [ ] Отчёт выведен (шаг 8)
- [ ] Авто-предложение следующего этапа — Plan Tests (шаг 9)

---

## Примеры

### Создание Design для OAuth2

```
Пользователь: "Создать Design для OAuth2 авторизации"

1. Parent: specs/analysis/0001-oauth2-authorization/discussion.md → WAITING ✓
2. Скрипт: create-analysis-design-file.py 0001-oauth2-authorization → design.md создан
3a. design-agent-first (Task tool):
    → Unified Scan: Discussion + specs/docs/README + overview + auth.md + gateway.md + users.md + .technologies/
    → Clarify: 3 сервиса (auth основной, gateway, users), технологии
    → Резюме + Выбор технологий (4 категории) + заголовки SVC-1..SVC-3
    → Частичная валидация → OK
3b. Подтверждение: "Сервисы: auth, gateway, users. Стек: Node.js, Express, PostgreSQL. Подтверждаете?" → Да
3c. design-agent-second (Task tool):
    → Чтение: partial design.md + Discussion + overview + auth.md + gateway.md + users.md
    → SVC-1 auth (9 подсекций), SVC-2 gateway, SVC-3 users
    → INT-1..INT-4, STS-1..STS-3
    → Маркеров: 0 → OK
    → Полная валидация → OK
4. README обновлён
5. design-reviewer → 2 рекомендации → приняты → перевалидация → OK
6. Ревью: "Да" → DRAFT → WAITING
7. DRAFT → WAITING (chain_status.py)
8. Отчёт
9. "Создать Plan Tests?" → Да
```

### Создание с --auto-clarify

```
Пользователь: "Создать Design для 0003-cache-optimization, --auto-clarify"

1. Parent: discussion.md → WAITING ✓
2. Скрипт → design.md создан
3a. design-agent-first (Task tool, --auto-clarify):
    → Unified Scan: Discussion + specs/docs/
    → Clarify пропущен — маркеры на неясности
    → Резюме + Выбор технологий (маркеры в "Выбрано") + заголовки SVC-N
3b. Подтверждение: разрешение маркеров "Выбрано" через AskUserQuestion → подтверждено
3c. design-agent-second (Task tool):
    → Чтение: partial design.md + Discussion
    → SVC-1 catalog (9 подсекций) + маркеры
    → Разрешение маркеров: AskUserQuestion → 0
    → Полная валидация → OK
4-5. README + design-reviewer → OK
6. Ревью → WAITING
7. DRAFT → WAITING (chain_status.py)
8. Отчёт
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [create-analysis-design-file.py](../../.scripts/create-analysis-design-file.py) | Создание файла design.md из шаблона (шаг 2) | Этот документ |
| [validate-analysis-design.py](../../.scripts/validate-analysis-design.py) | Валидация созданного документа (шаг 3, внутри агента) | [validation-design.md](./validation-design.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/design-create](/.claude/skills/design-create/SKILL.md) | Создание документа проектирования | Этот документ |

---

## Агенты

| Агент | Назначение | Шаг |
|-------|------------|-----|
| [design-agent-first](/.claude/agents/design-agent-first/AGENT.md) | Unified Scan + Clarify + Резюме + Выбор технологий + заголовки SVC-N | Шаг 3a (обязательно) |
| [design-agent-second](/.claude/agents/design-agent-second/AGENT.md) | Генерация подсекций SVC-N + INT-N + STS-N | Шаг 3c (обязательно) |
| [design-reviewer](/.claude/agents/design-reviewer/AGENT.md) | Ревью на полноту SVC-N, маппинг, delta-формат | Шаг 5 (обязательно) |
