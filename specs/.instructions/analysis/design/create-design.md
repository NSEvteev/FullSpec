---
description: Воркфлоу создания документа проектирования SDD — Unified Scan, Clarify, генерация SVC-N/INT-N/STS-N, валидация, перевод DRAFT → WAITING.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: specs/.instructions/README.md
---

# Воркфлоу создания проектирования

Рабочая версия стандарта: 2.1

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
  - [Шаг 2: Создать файл из шаблона](#шаг-2-создать-файл-из-шаблона)
  - [Шаг 3: Заполнить frontmatter](#шаг-3-заполнить-frontmatter)
  - [Шаг 4: Unified Scan](#шаг-4-unified-scan)
  - [Шаг 5: Clarify](#шаг-5-clarify)
  - [Шаг 6: Заполнить разделы](#шаг-6-заполнить-разделы)
  - [Шаг 7: Регистрация в README](#шаг-7-регистрация-в-readme)
  - [Шаг 8: Валидация](#шаг-8-валидация)
  - [Шаг 8.5: Ревью агентом (обязательно)](#шаг-85-ревью-агентом-обязательно)
  - [Шаг 9: Ревью пользователем](#шаг-9-ревью-пользователем)
  - [Шаг 10: Артефакты WAITING](#шаг-10-артефакты-waiting)
  - [Шаг 11: Отчёт о выполнении](#шаг-11-отчёт-о-выполнении)
  - [Шаг 12: Авто-предложение следующего этапа](#шаг-12-авто-предложение-следующего-этапа)
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

### Шаг 2: Создать файл из шаблона

**SSOT:** [standard-design.md § 7](./standard-design.md#7-шаблон)

1. Скопировать шаблон из [standard-design.md § 7](./standard-design.md#7-шаблон)
2. Создать файл `specs/analysis/NNNN-{topic}/design.md`

### Шаг 3: Заполнить frontmatter

**SSOT:** [standard-design.md § 3](./standard-design.md#3-frontmatter)

Заполнить поля, известные до Unified Scan:

| Поле | Значение |
|------|----------|
| `description` | Краткое описание (до 1024 символов) |
| `standard` | `specs/.instructions/analysis/design/standard-design.md` |
| `standard-version` | `v2.1` |
| `index` | `specs/analysis/README.md` |
| `parent` | `discussion.md` |
| `children` | `[]` (Plan Tests ещё не создан) |
| `status` | `DRAFT` |
| `milestone` | Скопировать из parent Discussion |

### Шаг 4: Unified Scan

**SSOT:** [standard-design.md § 1 → Unified Scan](./standard-design.md#1-назначение)

Последовательно прочитать 5 источников:

| # | Источник | Что извлечь |
|---|---------|-------------|
| 1 | Parent Discussion (целиком) | Требования, user stories, критерии успеха |
| 2 | `docs/README.md` | Таблица всех сервисов, технологии — обзор ландшафта |
| 3 | `docs/.system/overview.md` | Архитектура, data flows, Planned Changes |
| 4 | `docs/{svc}.md` для кандидатов | API, Data Model, Потоки, Code Map, зависимости |
| 5 | `docs/.technologies/` | Технологические конвенции |

**Алгоритм выбора кандидатов (шаг 4):** После шагов 2-3 составить список:
- (a) сервисы, **явно упомянутые** в Discussion
- (b) сервисы из overview.md, **связанные** с затронутыми по data flow
- (c) сервисы из Planned Changes overview.md, **пересекающиеся** по домену

**При отсутствии `docs/`:** шаги 2-5 пропускаются, LLM фиксирует «docs/ не найден — проект новый», Clarify расширяется.

**Агентный режим:** Unified Scan выполняется **design-agent** — агент читает все 5 источников в изолированном контексте. Структура секций `docs/{svc}.md` определена в [standard-service.md § 3](/specs/.instructions/docs/service/standard-service.md) — design-agent использует её для 8:8 маппинга подсекций SVC-N.

### Шаг 5: Clarify

**SSOT:** [standard-design.md § 6](./standard-design.md#6-clarify), [Стандарт analysis/ § 8](../standard-analysis.md#8-clarify-и-блокирующие-правила)

**Если `--auto-clarify` НЕ указан:**

LLM **сам предлагает** и уточняет через AskUserQuestion:

| Что предлагает LLM | Пример |
|---------------------|--------|
| Затронутые сервисы | «Unified Scan: auth (основной), gateway, users. Согласны?» |
| Shared-компоненты | «Token Validator → /shared/auth/. Или внутри auth?» |
| Новый сервис | «Предлагаю notification-service. Или отдельная Discussion?» |
| Контракты | «gateway → auth: REST /api/v1/auth/token. Или gRPC?» |
| Алгоритмы | «JWT: RS256 (asymmetric). Альтернатива: HS256. Выбор?» |
| Системные тесты | «INT-1: 3 сценария (happy, expired, rate limit). Достаточно?» |

**Если `--auto-clarify` указан:**

LLM пропускает Clarify, генерирует документ на основе Unified Scan и ставит маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` на все неясности.

### Шаг 6: Заполнить разделы

**SSOT:** [standard-design.md § 5](./standard-design.md#5-разделы-документа)

На основе результатов Unified Scan (шаг 4) и Clarify (шаг 5) заполнить **все разделы**:

1. **Резюме** — scope, ключевые решения, кол-во INT-N и STS-N, cross-cutting WHY
2. **SVC-N для каждого сервиса** — описание + 9 подсекций (§§ 1-9):
   - § 1 Назначение (контент обязателен)
   - §§ 2-7 Delta с маркерами ADDED/MODIFIED/REMOVED (или заглушка)
   - § 8 Границы автономии LLM (таблица уровней или заглушка)
   - § 9 Решения по реализации (контент обязателен, минимум 1 WHY)
3. **INT-N для каждого взаимодействия** — метаданные + Контракт + Sequence (mermaid)
4. **Системные тест-сценарии** — таблица STS-N (или заглушка)

**Порядок SVC:** Основной → Вторичный → Новый (определения в [standard-design.md § 5](./standard-design.md#5-разделы-документа)).

**Маркеры:** Если информации недостаточно — ставить `[ТРЕБУЕТ УТОЧНЕНИЯ: вопрос]`.

**Dependency Barrier:** Если генерация следующей секции зависит от неразрешённого маркера — остановить генерацию ([Стандарт analysis/ § 8.3](../standard-analysis.md#83-dependency-barrier)).

**Разрешение маркеров (обязательно перед продолжением):**

После заполнения всех разделов:
1. Проверить документ на наличие `[ТРЕБУЕТ УТОЧНЕНИЯ]` маркеров
2. Если маркеры есть — для каждого маркера уточнить через AskUserQuestion
3. Заменить маркеры на ответы пользователя
4. Если был Dependency Barrier — продолжить генерацию оставшихся секций
5. Повторять пока маркеров = 0

### Шаг 7: Регистрация в README

Обновить запись в `specs/analysis/README.md` — колонка Design:

```markdown
| NNNN | {topic} | WAITING | design.md | vX.Y.Z | {Описание} |
```

### Шаг 8: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-design.py specs/analysis/NNNN-{topic}/design.md
```

**Если скрипт недоступен:** пройти чек-лист из [validation-design.md](./validation-design.md).

Исправить ошибки до продолжения.

### Шаг 8.5: Ревью агентом (обязательно)

**Агент:** [design-reviewer](/.claude/agents/design-reviewer/AGENT.md)

Design-reviewer вызывается **обязательно** после валидации (исключение из общего правила «опционально» в [standard-analysis.md § 2.4](../standard-analysis.md#24-общий-паттерн-объекта)).

1. Запустить агента `design-reviewer` с путём к документу
2. Агент проверяет: распределение ответственностей, полноту 9 подсекций SVC-N, delta-формат, перекрёстные ссылки INT-N ↔ SVC-N § 6
3. Агент записывает рекомендации (PROP-N) в секцию «Резюме» или создаёт отдельный файл
4. Обработать рекомендации: принять или отклонить каждую
5. Вернуться к шагу 8 (перевалидация)

### Шаг 9: Ревью пользователем

**Перед вопросом:** проверить что маркеров = 0 и валидация пройдена. Если нет — вернуться к шагу 6.

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: «Документ проектирования готов. Всё корректно?»

| Ответ | Действие |
|-------|----------|
| Да, всё корректно | Перевести DRAFT → WAITING → шаг 10 |
| Нет, нужны правки | Внести изменения → продолжить с шага 8 |

### Шаг 10: Артефакты WAITING

**SSOT:** [standard-design.md § 4](./standard-design.md#4-переходы-статусов)

Артефакты создаются **автоматически** при переводе в WAITING:

| # | Артефакт | Действие |
|---|----------|----------|
| 1 | Planned Changes в `docs/{svc}.md` § 9 | Для каждого SVC-N: записать дельту из §§ 1-8 |
| 2 | Planned Changes в `docs/.system/overview.md` § 8 | Если архитектурные изменения |
| 3 | Planned Changes в `docs/.system/conventions.md` | Если новые конвенции |
| 4 | Planned Changes в `docs/.system/infrastructure.md` | Если инфраструктурные изменения |
| 5 | Заглушка `docs/{svc}.md` | Через `/service-create` (только для новых сервисов) |
| 6 | Per-tech стандарты | Через `/technology-create` (только для новых технологий) |

Обновить frontmatter: `status: WAITING`. Обновить README.

### Шаг 11: Отчёт о выполнении

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

Артефакты:
- Planned Changes: {список docs/}
- Заглушки: {если создавались}
- Per-tech: {если создавались}

Статус: DRAFT → WAITING

Следующий шаг: Создать Plan Tests

Валидация: пройдена
```

### Шаг 12: Авто-предложение следующего этапа

AskUserQuestion: «Перейти к созданию Plan Tests?»

| Ответ | Действие |
|-------|----------|
| Да | Вызвать воркфлоу создания Plan Tests с путём к текущему Design |
| Нет | Завершить воркфлоу |

---

## Чек-лист

### Подготовка
- [ ] Parent Discussion в статусе WAITING
- [ ] Файл создан из шаблона
- [ ] Frontmatter заполнен (базовые поля, milestone из Discussion)

### Unified Scan
- [ ] Discussion прочитана целиком
- [ ] docs/README.md прочитан
- [ ] overview.md прочитан
- [ ] {svc}.md для кандидатов прочитаны
- [ ] .technologies/ прочитаны

### Clarify
- [ ] Clarify проведён (или `--auto-clarify`)
- [ ] Сервисы определены (основной/вторичный/новый)
- [ ] Контракты согласованы
- [ ] Shared-компоненты определены

### Содержание
- [ ] Резюме заполнено
- [ ] Все SVC-N: описание + 9 подсекций
- [ ] § 1, § 9 — контент (не заглушка)
- [ ] Delta-формат в §§ 2-7
- [ ] INT-N с метаданными, контрактом и sequence
- [ ] STS-N таблица (или заглушка)
- [ ] Все маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` разрешены (0 неразрешённых)

### Проверка
- [ ] Валидация пройдена (скрипт или чек-лист)
- [ ] Ревью design-reviewer проведено (обязательно)
- [ ] Запись обновлена в README
- [ ] Ревью пользователем пройдено
- [ ] Артефакты WAITING созданы
- [ ] Статус переведён в WAITING
- [ ] README обновлён (статус WAITING)
- [ ] Отчёт выведен
- [ ] Авто-предложение следующего этапа (Plan Tests)

---

## Примеры

### Создание Design для OAuth2

```
Пользователь: "Создать Design для OAuth2 авторизации"

1. Parent: specs/analysis/0001-oauth2-authorization/discussion.md → WAITING ✓
2. Файл создан из шаблона → design.md
3. Frontmatter: status=DRAFT, parent=discussion.md, milestone=v1.2.0
4. Unified Scan: Discussion + docs/README + overview + auth.md + gateway.md + users.md + .technologies/
5. Clarify: 3 сервиса (auth основной, gateway, users), RS256, /shared/auth/
6. Разделы: SVC-1 auth, SVC-2 gateway, SVC-3 users, INT-1..INT-4, STS-1..STS-3
   → Маркеров: 0 → OK
7. README обновлён
8. Валидация → OK
8.5. design-reviewer → 2 рекомендации → приняты → перевалидация → OK
9. Ревью: "Да" → DRAFT → WAITING
10. Артефакты: Planned Changes в auth.md, gateway.md, users.md, overview.md
11. Отчёт
12. "Создать Plan Tests?" → Да
```

### Создание с --auto-clarify

```
Пользователь: "Создать Design для 0003-cache-optimization, --auto-clarify"

1. Parent: discussion.md → WAITING ✓
2-3. Файл + frontmatter
4. Unified Scan: Discussion + docs/
5. Clarify пропущен — маркеры на неясности
6. Разделы: SVC-1 catalog + маркеры [ТРЕБУЕТ УТОЧНЕНИЯ]
   → Разрешение маркеров: AskUserQuestion → замена → 0 маркеров
7-8. README + Валидация
8.5. design-reviewer → OK
9. Ревью → WAITING
10. Артефакты
11. Отчёт
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-analysis-design.py](../../.scripts/validate-analysis-design.py) | Валидация созданного документа (шаг 8) | [validation-design.md](./validation-design.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/design-create](/.claude/skills/design-create/SKILL.md) | Создание документа проектирования | Этот документ |

---

## Агенты

| Агент | Назначение | Шаг |
|-------|------------|-----|
| [design-agent](/.claude/agents/design-agent/AGENT.md) | Unified Scan + генерация Design (DRAFT) | Шаг 4-6 (агентный режим) |
| [design-reviewer](/.claude/agents/design-reviewer/AGENT.md) | Ревью на полноту SVC-N, маппинг, delta-формат | Шаг 8.5 |
