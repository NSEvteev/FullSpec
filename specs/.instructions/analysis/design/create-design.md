---
description: Воркфлоу создания документа проектирования SDD — Unified Scan, Clarify, генерация SVC-N/INT-N/STS-N, валидация, перевод DRAFT → WAITING.
standard: .instructions/standard-instruction.md
standard-version: v1.3
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
  - [Шаг 2: Создать файл из шаблона (скрипт)](#шаг-2-создать-файл-из-шаблона-скрипт)
  - [Шаг 3: Делегировать design-agent](#шаг-3-делегировать-design-agent-unified-scan--clarify--генерация)
  - [Шаг 4: Регистрация в README](#шаг-4-регистрация-в-readme)
  - [Шаг 5: Ревью агентом (обязательно)](#шаг-5-ревью-агентом-обязательно)
  - [Шаг 6: Ревью пользователем](#шаг-6-ревью-пользователем)
  - [Шаг 7: Артефакты WAITING](#шаг-7-артефакты-waiting)
  - [Шаг 7.5: Ревью per-tech стандартов](#шаг-75-ревью-per-tech-стандартов)
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

### Шаг 3: Делегировать design-agent (Unified Scan + Clarify + генерация)

**Агент:** [design-agent](/.claude/agents/design-agent/AGENT.md)

**ОБЯЗАТЕЛЬНО** делегировать design-agent через Task tool. Агент выполняет шаги 4-6 из [standard-design.md](./standard-design.md) в изолированном контексте:

1. **Unified Scan** — чтение 5 источников ([standard-design.md § 1](./standard-design.md#1-назначение))
2. **Clarify** — уточнение решений через AskUserQuestion ([standard-design.md § 6](./standard-design.md#6-clarify))
3. **Генерация** — заполнение Резюме, SVC-N (9 подсекций), INT-N, STS-N ([standard-design.md § 5](./standard-design.md#5-разделы-документа))
4. **Разрешение маркеров** — все `[ТРЕБУЕТ УТОЧНЕНИЯ]` → 0
5. **Валидация** — `validate-analysis-design.py`

```
Task tool:
  subagent_type: design-agent
  prompt: >
    Заполнить документ проектирования specs/analysis/NNNN-{topic}/design.md.
    Parent Discussion: specs/analysis/NNNN-{topic}/discussion.md.
    {--auto-clarify если указан}
```

**Почему агент:** Design — самый сложный документ (Unified Scan 5 источников, 9 подсекций на сервис, INT-N контракты, mermaid-диаграммы). Изолированный контекст агента защищает основной контекст от перегрузки.

**Оркестратор НЕ выполняет** Unified Scan, Clarify и генерацию самостоятельно.

### Шаг 4: Регистрация в README

Обновить запись в `specs/analysis/README.md` — колонка Design:

```markdown
| NNNN | {topic} | WAITING | design.md | vX.Y.Z | {Описание} |
```

### Шаг 5: Ревью агентом (обязательно)

**Агент:** [design-reviewer](/.claude/agents/design-reviewer/AGENT.md)

Design-reviewer вызывается **обязательно** после валидации (исключение из общего правила «опционально» в [standard-analysis.md § 2.4](../standard-analysis.md#24-общий-паттерн-объекта)).

1. Запустить агента `design-reviewer` с путём к документу
2. Агент проверяет: распределение ответственностей, полноту 9 подсекций SVC-N, delta-формат, перекрёстные ссылки INT-N ↔ SVC-N § 6
3. Агент записывает рекомендации (PROP-N) в секцию «Резюме» или создаёт отдельный файл
4. Обработать рекомендации: принять или отклонить каждую
5. Перевалидация: `validate-analysis-design.py`

### Шаг 6: Ревью пользователем

**Перед вопросом:** проверить что маркеров = 0 и валидация пройдена. Если нет — вернуться к шагу 3.

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: «Документ проектирования готов. Всё корректно?»

| Ответ | Действие |
|-------|----------|
| Да, всё корректно | Перевести DRAFT → WAITING через `chain_status.py` (см. шаг 7) → шаг 7 |
| Нет, нужны правки | Внести изменения → перевалидация → повторить шаг 6 |

### Шаг 7: Артефакты WAITING

**SSOT:** [standard-design.md § 4](./standard-design.md#4-переходы-статусов)

Артефакты создаются **автоматически** при переводе в WAITING:

| # | Артефакт | Действие |
|---|----------|----------|
| 1 | Planned Changes в `specs/docs/{svc}.md` § 9 | Для каждого SVC-N: записать дельту из §§ 1-8 |
| 2 | Planned Changes в `specs/docs/.system/overview.md` § 8 | Если архитектурные изменения |
| 3 | Planned Changes в `specs/docs/.system/conventions.md` | Если новые конвенции |
| 4 | Planned Changes в `specs/docs/.system/infrastructure.md` | Если инфраструктурные изменения |
| 5 | Заглушка `specs/docs/{svc}.md` | Через `/service-create` (только для новых сервисов) |
| 6 | Per-tech стандарты | Через `/technology-create` (только для новых технологий) |

**Переход DRAFT → WAITING** — через модуль `chain_status.py` (SSOT статусов):

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="WAITING", document="design")
# Модуль автоматически: обновляет frontmatter + README dashboard
```

Выполнить побочные эффекты из `result.side_effects` (Planned Changes, заглушки, per-tech).

### Шаг 7.5: Ревью per-tech стандартов

**Условие:** Шаг 7 создал per-tech стандарты (строка 6 таблицы артефактов). Если per-tech не создавались — пропустить.

**Агент:** [technology-reviewer](/.claude/agents/technology-reviewer/AGENT.md)

1. Запустить **одного** technology-reviewer на **все** созданные стандарты
2. Агент проверяет 7 критериев (R1-R7) + кросс-стандартную согласованность
3. Если вердикт REVISE — исправить стандарты → перевалидация → повторный ревью
4. Если вердикт ACCEPT — продолжить к шагу 8

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

Артефакты:
- Planned Changes: {список specs/docs/}
- Заглушки: {если создавались}
- Per-tech: {если создавались}

Статус: DRAFT → WAITING

Следующий шаг: Создать Plan Tests

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

### Генерация — design-agent (шаг 3)
- [ ] design-agent делегирован через Task tool
- [ ] Unified Scan выполнен (Discussion + specs/docs/)
- [ ] Clarify проведён (или `--auto-clarify`)
- [ ] Сервисы определены (основной/вторичный/новый)
- [ ] Резюме заполнено
- [ ] Все SVC-N: описание + 9 подсекций (§ 1, § 9 — контент)
- [ ] INT-N с метаданными, контрактом и sequence
- [ ] STS-N таблица (или заглушка)
- [ ] Все маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` разрешены (0 неразрешённых)
- [ ] Валидация пройдена внутри агента

### Проверка (шаги 4-9)
- [ ] Запись обновлена в README (шаг 4)
- [ ] Ревью design-reviewer проведено — обязательно (шаг 5)
- [ ] Ревью пользователем пройдено (шаг 6)
- [ ] Артефакты WAITING созданы (шаг 7)
- [ ] Ревью per-tech пройдено — если создавались (шаг 7.5)
- [ ] Статус переведён в WAITING
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
3. design-agent (Task tool):
   → Unified Scan: Discussion + specs/docs/README + overview + auth.md + gateway.md + users.md + .technologies/
   → Clarify: 3 сервиса (auth основной, gateway, users), RS256, /shared/auth/
   → Разделы: SVC-1 auth, SVC-2 gateway, SVC-3 users, INT-1..INT-4, STS-1..STS-3
   → Маркеров: 0 → OK
   → Валидация → OK
4. README обновлён
5. design-reviewer → 2 рекомендации → приняты → перевалидация → OK
6. Ревью: "Да" → DRAFT → WAITING
7. Артефакты: Planned Changes в auth.md, gateway.md, users.md, overview.md
7.5. technology-reviewer → per-tech не создавались → skip
8. Отчёт
9. "Создать Plan Tests?" → Да
```

### Создание с --auto-clarify

```
Пользователь: "Создать Design для 0003-cache-optimization, --auto-clarify"

1. Parent: discussion.md → WAITING ✓
2. Скрипт → design.md создан
3. design-agent (Task tool, --auto-clarify):
   → Unified Scan: Discussion + specs/docs/
   → Clarify пропущен — маркеры на неясности
   → Разделы: SVC-1 catalog + маркеры
   → Разрешение маркеров: AskUserQuestion → 0
   → Валидация → OK
4-5. README + design-reviewer → OK
6. Ревью → WAITING
7. Артефакты
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
| [design-agent](/.claude/agents/design-agent/AGENT.md) | Unified Scan + Clarify + генерация + валидация Design (DRAFT) | Шаг 3 (обязательно) |
| [design-reviewer](/.claude/agents/design-reviewer/AGENT.md) | Ревью на полноту SVC-N, маппинг, delta-формат | Шаг 5 (обязательно) |
| [technology-reviewer](/.claude/agents/technology-reviewer/AGENT.md) | Ревью содержания per-tech стандартов (7 критериев + кросс-согласованность) | Шаг 7.5 (условно) |
