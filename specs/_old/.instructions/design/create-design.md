---
description: Воркфлоу создания документа проектирования SDD — multi-agent оркестрация (design-agent + design-reviewer), Deep Scan, артефакты, перевод DRAFT → WAITING.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/design/README.md
---

# Воркфлоу создания проектирования

Рабочая версия стандарта: 1.0

Пошаговый процесс создания нового документа проектирования (`specs/design/design-*.md`). Оркестратор (основной LLM) делегирует тяжёлую работу агентам, сохраняя контекст чистым.

**Полезные ссылки:**
- [Стандарт проектирования](./standard-design.md)
- [Стандарт SDD](../standard-specs.md) — статусы, Clarify, маркеры, общий паттерн объекта
- [Инструкции design/](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-design.md](./standard-design.md) |
| Валидация | [validation-design.md](./validation-design.md) |
| Создание | Этот документ |
| Модификация | [modify-design.md](./modify-design.md) |

## Оглавление

- [Принципы](#принципы)
- [Архитектура процесса](#архитектура-процесса)
- [Шаги](#шаги)
  - [Шаг 1: Проверить parent Impact (оркестратор)](#шаг-1-проверить-parent-impact-оркестратор)
  - [Шаг 2: Создать файл из шаблона (оркестратор)](#шаг-2-создать-файл-из-шаблона-оркестратор)
  - [Шаг 3: Заполнить frontmatter (оркестратор)](#шаг-3-заполнить-frontmatter-оркестратор)
  - [Шаг 4: Запустить design-agent (CLARIFY, GENERATE, VALIDATE)](#шаг-4-запустить-design-agent-clarify-generate-validate)
  - [Шаг 5: Обработать результат design-agent (оркестратор)](#шаг-5-обработать-результат-design-agent-оркестратор)
  - [Шаг 6: Запустить design-reviewer (AGENT REVIEW)](#шаг-6-запустить-design-reviewer-agent-review)
  - [Шаг 7: Обработать PROP-N (оркестратор)](#шаг-7-обработать-prop-n-оркестратор)
  - [Шаг 8: Ревью пользователем (USER REVIEW)](#шаг-8-ревью-пользователем-user-review)
  - [Шаг 9: Артефакты при переходе в WAITING](#шаг-9-артефакты-при-переходе-в-waiting)
  - [Шаг 10: Отчёт о выполнении](#шаг-10-отчёт-о-выполнении)
  - [Шаг 11: Авто-предложение следующего этапа](#шаг-11-авто-предложение-следующего-этапа)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)
- [Агенты](#агенты)

---

## Принципы

> **Multi-agent архитектура.** Скилл `/design-create` — оркестратор. Тяжёлую работу (Deep Scan + CLARIFY + GENERATE + VALIDATE) выполняет **design-agent** в изолированном контексте. Оркестратор НЕ читает `specs/architecture/` напрямую — это делает агент ([standard-design.md § 1](./standard-design.md#1-назначение)).

> **design-reviewer — обязателен.** После design-agent оркестратор запускает **design-reviewer** для ревью распределения ответственностей. Это не опциональный шаг — это часть процесса ([Стандарт SDD § 2.3, шаг 5](../standard-specs.md#23-общий-паттерн-объекта)).

> **USER REVIEW — блокирующий.** Пользователь финально ревьюит результат обоих агентов и одобряет → WAITING. Без одобрения пользователя перевод в WAITING невозможен.

> **Design создаётся только после Impact в WAITING.** Parent Impact обязателен. Без одобренного Impact — нет Design.

> **Роль — РЕШАТЕЛЬ.** Design **критически оценивает** предложения Impact и **РЕШАЕТ** распределение ответственностей. Impact ПРЕДЛАГАЕТ — Design РЕШАЕТ.

> **Артефакты при WAITING.** При переводе Design → WAITING создаются 5 типов артефактов: Planned Changes, заглушки новых сервисов, per-tech стандарты для новых технологий, ADR-документы. Без артефактов перевод в WAITING неполный.

> **Документ без маркеров.** Воркфлоу завершается переводом в WAITING. Все маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` должны быть разрешены до USER REVIEW.

---

## Архитектура процесса

**SSOT:** [standard-design.md § 1 — Агентный режим](./standard-design.md#1-назначение), [Стандарт SDD § 2.3 — Общий паттерн объекта](../standard-specs.md#23-общий-паттерн-объекта)

| Фаза (§ 2.3) | Исполнитель | Шаги | Что делает |
|---------------|-------------|------|------------|
| **PREPARE** (шаг 1) | Оркестратор | 1–3 | Проверка parent Impact, создание файла, frontmatter |
| **CLARIFY → GENERATE → VALIDATE** (шаги 2–4) | **design-agent** | 4 | Deep Scan (6 источников), Clarify, генерация секций SVC/INT/STS, валидация |
| Post-agent | Оркестратор | 5 | Проверка результата, README, parent Impact |
| **AGENT REVIEW** (шаг 5) | **design-reviewer** | 6–7 | Ревью распределения, PROP-N, обработка предложений |
| **USER REVIEW** (шаг 6) | Пользователь | 8 | Финальное одобрение → WAITING |
| **REPORT** (шаг 7) | Оркестратор | 9–11 | Артефакты, отчёт, предложение ADR |

**Зачем multi-agent:** design-agent читает `specs/architecture/` в деталях (per-service документы, overview, services/README) — это большой объём текста, который засоряет контекст оркестратора. Агент работает в изолированном контексте и возвращает только заполненный Design-документ.

---

## Шаги

### Шаг 1: Проверить parent Impact (оркестратор)

**SSOT:** [standard-design.md § 1](./standard-design.md#1-назначение)

1. Определить parent Impact (из запроса пользователя или контекста)
2. Прочитать **frontmatter** parent Impact (не весь документ — полное чтение делает design-agent)
3. Проверить `status` в frontmatter:
   - `WAITING` → продолжить
   - Любой другой → **СТОП**: "Impact должен быть в статусе WAITING для создания Design"
4. Извлечь `milestone` из parent Impact (наследуется от parent Discussion)
5. Извлечь `parent` из parent Impact — путь к parent Discussion

### Шаг 2: Создать файл из шаблона (оркестратор)

**SSOT:** [standard-design.md § 2](./standard-design.md#2-расположение-и-именование), [§ 7](./standard-design.md#7-шаблон)

```bash
python specs/.instructions/.scripts/create-design-file.py --parent specs/impact/impact-NNNN-topic.md [topic]
```

Скрипт извлекает NNNN из parent Impact и создаёт `specs/design/design-NNNN-topic.md` из шаблона. Topic извлекается из parent filename если не указан явно.

**Если `specs/design/` не существует:** вызвать `/structure-create specs/design`.

**Вручную (если скрипт недоступен):**
1. Номер = NNNN из parent Discussion (disc-0002 → design-0002)
2. Сформировать имя: `design-NNNN-topic.md` (topic — kebab-case, латиница)
3. Скопировать шаблон из [standard-design.md § 7](./standard-design.md#7-шаблон)

### Шаг 3: Заполнить frontmatter (оркестратор)

**SSOT:** [standard-design.md § 3](./standard-design.md#3-frontmatter)

| Поле | Значение |
|------|----------|
| `description` | Краткое описание проектирования (до 1024 символов) |
| `standard` | `specs/.instructions/design/standard-design.md` |
| `standard-version` | `v1.1` |
| `index` | `specs/design/README.md` |
| `parent` | Путь к Impact-документу (из шага 1) |
| `children` | `[]` (ADR ещё не созданы) |
| `status` | `DRAFT` |
| `milestone` | Значение из parent Discussion (через Impact — скопировать, не спрашивать) |

### Шаг 4: Запустить design-agent (CLARIFY, GENERATE, VALIDATE)

**SSOT:** [standard-design.md § 1 — Агентный режим](./standard-design.md#1-назначение)

**Агент:** [design-agent](/.claude/agents/design-agent/AGENT.md)

Оркестратор запускает design-agent через Task tool. Агент выполняет шаги 2–4 из [Общего паттерна объекта (§ 2.3)](../standard-specs.md#23-общий-паттерн-объекта) в изолированном контексте.

**Запуск:**

```
Task tool:
  subagent_type: design-agent
  prompt: |
    Заполни документ проектирования: specs/design/design-NNNN-topic.md
    Parent Impact: specs/impact/impact-NNNN-topic.md
    Parent Discussion: specs/discussion/disc-NNNN-topic.md
    [--auto-clarify] (если пользователь указал)
```

**Что делает design-agent:**

| Подшаг | Фаза § 2.3 | Действие |
|--------|------------|----------|
| 4.1 | CLARIFY | **Deep Scan** — читает 6 источников ([standard-design.md § 1](./standard-design.md#1-назначение)): parent Impact, parent Discussion, `services/README.md`, `system/overview.md`, per-service `{svc}.md`, `specs/technologies/README.md` + per-tech стандарты |
| 4.2 | CLARIFY | **Clarify** — предлагает проектные решения пользователю через AskUserQuestion (или ставит маркеры при `--auto-clarify`) |
| 4.3 | GENERATE | **Генерация** — заполняет разделы: Резюме, секции SVC-N (3 подсекции каждая), блоки INT-N (Контракт + Sequence), STS-N |
| 4.4 | GENERATE | **Разрешение маркеров** — итеративно разрешает `[ТРЕБУЕТ УТОЧНЕНИЯ]` через AskUserQuestion (пока маркеров = 0) |
| 4.5 | GENERATE | **Upward feedback** — если обнаружена информация для Impact/Discussion → приостановка, обновление parent, AskUserQuestion, возобновление |
| 4.6 | VALIDATE | **Валидация** — запускает `validate-design.py`, исправляет ошибки |

**Правила генерации** (design-agent следует [standard-design.md § 5](./standard-design.md#5-разделы-документа)):
- Порядок SVC: Основной → Вторичный → Новый
- Отклонённые сервисы — только в Резюме с обоснованием
- Косвенные сервисы — без секции SVC
- Нумерация SVC-N, CMP-N, INT-N, STS-N — сквозная
- Зона ответственности: нет деталей реализации (→ ADR), нет бизнес-обоснований (→ Discussion)

**Результат:** design-agent возвращает заполненный документ (все разделы, 0 маркеров, валидация пройдена).

**Обработка ошибок:**

| Ситуация | Действие |
|----------|----------|
| Агент не смог завершить (max_turns) | Оркестратор читает текущее состояние файла, предлагает пользователю: дозаполнить вручную или перезапустить агента |
| Остались маркеры | Оркестратор разрешает маркеры через AskUserQuestion |
| Валидация не пройдена | Оркестратор исправляет ошибки вручную |

### Шаг 5: Обработать результат design-agent (оркестратор)

После завершения design-agent оркестратор:

1. **Прочитать файл** `specs/design/design-NNNN-topic.md` — убедиться, что заполнен
2. **Проверить маркеры:** если остались `[ТРЕБУЕТ УТОЧНЕНИЯ]` — разрешить через AskUserQuestion
3. **Регистрация в README:** добавить запись в `specs/design/README.md`:
   ```markdown
   | NNNN | design-NNNN-topic.md | DRAFT | impact-NNNN | — | vX.Y.Z | {Описание} |
   ```
4. **Обновить parent Impact:** добавить Design в `children` frontmatter parent Impact:
   ```yaml
   children:
     - design/design-NNNN-topic.md
   ```
5. **Обновить Impact README:** колонка Design: `—` → `design-NNNN`

### Шаг 6: Запустить design-reviewer (AGENT REVIEW)

**SSOT:** [Стандарт SDD § 2.3, шаг 5](../standard-specs.md#23-общий-паттерн-объекта)

**Агент:** [design-reviewer](/.claude/agents/design-reviewer/AGENT.md)

> **ОБЯЗАТЕЛЬНЫЙ шаг.** Design-reviewer проверяет распределение ответственностей, покрытие Impact, зону ответственности.

**Запуск:**

```
Task tool:
  subagent_type: design-reviewer
  prompt: "Проанализируй документ: specs/design/design-NNNN-topic.md"
```

**Что делает design-reviewer:**
- Читает Design-документ и parent Impact
- Проверяет покрытие всех SVC из Impact
- Анализирует распределение ответственностей
- Проверяет зону ответственности (нет деталей реализации → ADR)
- Записывает PROP-N в секцию "Предложения"

### Шаг 7: Обработать PROP-N (оркестратор)

После возврата design-reviewer — обработать каждый PROP-N:

1. Для каждого PROP-N — AskUserQuestion: принять, отклонить или изменить
2. **Обычные PROP** (без `↑`): если принят — применить к Design, если отклонён — удалить
3. **Upward feedback PROP** (с `↑ Impact:` или `↑ Discussion:`): если принят — обновить parent документ ([standard-specs.md § 3.6](../standard-specs.md#36-upward-feedback)):
   - Приостановить работу с Design
   - Внести изменения в Impact (и Discussion, если затронута)
   - AskUserQuestion: подтвердить изменения
   - Статус parent документов остаётся WAITING
   - Возобновить работу с Design
4. После обработки всех PROP — перезапустить валидацию:
   ```bash
   python specs/.instructions/.scripts/validate-design.py specs/design/design-NNNN-topic.md
   ```

### Шаг 8: Ревью пользователем (USER REVIEW)

**SSOT:** [Стандарт SDD § 2.3, шаг 6](../standard-specs.md#23-общий-паттерн-объекта)

**Перед вопросом:** проверить что маркеров = 0 и валидация пройдена.

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: "Документ проектирования готов. Всё корректно?"

| Ответ | Действие |
|-------|----------|
| Да, всё корректно | Перевести DRAFT → WAITING: обновить frontmatter (`status: WAITING`), обновить README → шаг 9 |
| Нет, нужны правки | Внести изменения → вернуться к шагу 6 (перезапуск design-reviewer) или к шагу 4 (перезапуск design-agent, если правки масштабные) |

### Шаг 9: Артефакты при переходе в WAITING

**SSOT:** [standard-design.md § 4](./standard-design.md#4-переходы-статусов)

При переводе Design в WAITING — создать 5 типов артефактов:

| # | Артефакт | Действие |
|---|----------|----------|
| 1 | **Planned Changes** в `services/{svc}.md` | Для каждого SVC-N: добавить запись в секцию Planned Changes сервисного документа. Вызвать `/service-modify` или добавить вручную |
| 2 | **Planned Changes** в `system/overview.md`, `system/data-flows.md` (если есть INT-N), `system/infrastructure.md` (если затрагивает инфраструктуру), `domains/context-map.md`, `domains/{domain}.md` (если новый домен) | Добавить Planned Changes в файлы системной/доменной архитектуры |
| 3 | **Заглушка сервиса** (только для новых) | Для сервисов с решением "Подтверждён (новый)" или "Добавлен Design": вызвать `/service-create {svc} --design {design-path} --impact {impact-path}` — создаст файл-заглушку с Резюме, предварительными данными (API, Data Model, Внешние зависимости) и Planned Changes. Маппинг: `svc` = имя из SVC-N, `description` = описание из SVC-N, `api` = API-N из parent Impact, `data` = DATA-N из parent Impact, `dependencies` = Dependencies из Design SVC-N + INT-N |
| 4 | **Per-tech стандарты** (только для новых технологий) | Для каждой технологии из Tech Stack Design, у которой нет per-tech стандарта: вызвать `/technology-create {tech}:{version} --design {design-path} --mode stub`. Запускает N technology-agent параллельно (по одному на технологию). Создаёт заглушку `specs/technologies/standard-{tech}.md` с § 1 заполненным и § 2-6 placeholder |
| 5 | **ADR-документы** (1:N) | Для каждого SVC-N: вызвать `/adr-create` — создаст ADR-документ. Обновить `children` в frontmatter Design |

**Порядок:** артефакты 1-4 создаются перед ADR (артефакт 5), т.к. ADR может ссылаться на Planned Changes и per-tech стандарты.

**Если скиллы `/service-create`, `/service-modify`, `/adr-create` недоступны:** создать артефакты вручную по стандартам:
- Planned Changes: [standard-service.md § 5.7](../living-docs/service/standard-service.md#57-planned-changes)
- Заглушки: [standard-service.md § 9.1](../living-docs/service/standard-service.md#шаблон-заглушки-design-waiting)

### Шаг 10: Отчёт о выполнении

```
## 📋 Отчёт о создании проектирования

✅ **Создан документ проектирования:** `specs/design/design-NNNN-topic.md`
📄 **Parent Impact:** `impact-NNNN-topic.md`
📄 **Parent Discussion:** `disc-NNNN-topic.md`

📝 **Описание:** {description}

🏷️ **Milestone:** {vX.Y.Z}

🏗️ **Сервисы:** {количество SVC} (подтверждённых: N, изменённых: N, добавленных: N, отклонённых: N)

🔗 **Блоки взаимодействия:** {количество INT}

🧪 **Системные тесты:** {количество STS}

📦 **Артефакты:**
- Planned Changes: {количество} сервисных документов обновлено
- Заглушки: {количество} новых сервисов
- ADR: {количество} документов создано

🤖 **Агенты:**
- design-agent: выполнен (Deep Scan + CLARIFY + GENERATE + VALIDATE)
- design-reviewer: выполнен ({количество} PROP-N, принято: N, отклонено: N)

🔄 **Статус:** DRAFT → WAITING

⏭️ **Следующий шаг:** Заполнить ADR для каждого сервиса

✅ **Валидация:** пройдена
```

### Шаг 11: Авто-предложение следующего этапа

AskUserQuestion: "Перейти к заполнению ADR?"

| Ответ | Действие |
|-------|----------|
| Да | Предложить первый ADR из `children` для заполнения |
| Нет | Завершить воркфлоу |

---

## Чек-лист

### PREPARE (оркестратор, шаги 1–3)
- [ ] Parent Impact в статусе WAITING
- [ ] Milestone извлечён из parent Discussion (через Impact)
- [ ] Файл создан из шаблона (design-NNNN-topic.md)
- [ ] Frontmatter заполнен (description, standard, parent, children=[], status=DRAFT, milestone)

### CLARIFY → GENERATE → VALIDATE (design-agent, шаг 4)
- [ ] design-agent запущен с правильными параметрами
- [ ] Deep Scan выполнен (6 источников)
- [ ] Clarify проведён (или `--auto-clarify`)
- [ ] Секция "📋 Резюме" заполнена контентом
- [ ] Минимум 1 секция SVC-N с 3 подсекциями (Ответственность, Компоненты, Зависимости)
- [ ] Минимум 1 блок INT-N с 2 подсекциями (Контракт, Sequence) — если > 1 сервиса
- [ ] Секция "🧪 Системные тест-сценарии" присутствует
- [ ] Все маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` разрешены (0 маркеров)
- [ ] Нумерация SVC-N, CMP-N, INT-N, STS-N сквозная, без дублей
- [ ] Валидация пройдена (validate-design.py)

### Post-agent (оркестратор, шаг 5)
- [ ] Файл прочитан и проверен оркестратором
- [ ] Оставшиеся маркеры разрешены (если были)
- [ ] Запись добавлена в `specs/design/README.md`
- [ ] `children` обновлён в parent Impact
- [ ] Колонка Design обновлена в Impact README

### AGENT REVIEW (design-reviewer, шаги 6–7)
- [ ] design-reviewer запущен (обязательный шаг)
- [ ] PROP-N обработаны: для каждого — принять/отклонить
- [ ] Upward feedback PROP обработаны (если были)
- [ ] Валидация перезапущена после применения PROP

### USER REVIEW (шаг 8)
- [ ] Маркеров = 0
- [ ] Валидация пройдена
- [ ] Пользователь одобрил документ
- [ ] Статус обновлён: DRAFT → WAITING
- [ ] README обновлён: DRAFT → WAITING

### Артефакты (шаг 9)
- [ ] Planned Changes добавлены в `services/{svc}.md` для каждого SVC
- [ ] Planned Changes добавлены в `system/overview.md`
- [ ] Planned Changes добавлены в `system/data-flows.md` (если есть INT-N)
- [ ] Planned Changes добавлены в `system/infrastructure.md` (если затрагивает инфраструктуру)
- [ ] Planned Changes добавлены в `domains/context-map.md`
- [ ] Per-domain файлы `domains/{domain}.md` созданы (если новые домены)
- [ ] Заглушки созданы для новых сервисов
- [ ] Per-tech стандарты созданы для новых технологий (`/technology-create`)
- [ ] ADR-документы созданы (1:N по сервисам)
- [ ] `children` в frontmatter Design обновлён (пути к ADR)

### Завершение (шаги 10–11)
- [ ] Отчёт выведен
- [ ] Авто-предложение ADR

---

## Примеры

### Создание проектирования для новой функциональности

```
Пользователь: "Создай Design для impact-0001-oauth2-authorization.md"

PREPARE (оркестратор):
1. Parent Impact: impact-0001, status=WAITING, milestone=v1.2.0
2. Файл создан: design-0001-oauth2-authorization.md
3. Frontmatter: parent=impact-0001, milestone=v1.2.0, status=DRAFT

CLARIFY → GENERATE → VALIDATE (design-agent):
4. Запуск design-agent:
   - Deep Scan: Impact (SVC-1..SVC-3), Discussion (требования),
     services/README, overview.md, auth.md, gateway.md, users.md
   - Clarify: "auth подтверждаю как основной: JWT lifecycle. Согласны?"
     → Пользователь: "Да"
   - Генерация: Резюме, SVC-1..SVC-3, INT-1..INT-4, STS-1..STS-3
   - Маркеров: 0
   - Валидация: ОК

Post-agent (оркестратор):
5. Файл проверен, README обновлён, parent Impact → children обновлён

AGENT REVIEW (design-reviewer):
6. design-reviewer → 2 PROP-N:
   - PROP-1 (P2): "CMP-3 Token Validator — уточнить: /shared/auth/ или /shared/jwt/"
   - PROP-2 (P3): "STS-4 — добавить сценарий revoke token"
7. Обработка: PROP-1 принят → /shared/auth/, PROP-2 принят → добавлен STS-4

USER REVIEW:
8. "Да, всё корректно" → DRAFT → WAITING

Артефакты:
9. Planned Changes (3 сервиса), заглушки (0), ADR (3 документа)

10. Отчёт
11. "Перейти к ADR?" → Да
```

### Создание с --auto-clarify

```
Пользователь: "Создай Design для impact-0005-cache-optimization.md --auto-clarify"

PREPARE: шаги 1-3 (стандартные)

design-agent:
4. Clarify пропущен — маркеры на неясности
   → Генерация с маркерами
   → Разрешение маркеров через AskUserQuestion
   → Валидация ОК

Post-agent → design-reviewer → PROP-N → USER REVIEW → WAITING → Артефакты
```

### Создание с upward feedback

```
Пользователь: "Создай Design для impact-0010-payment-integration.md"

design-agent:
4. Deep Scan → при чтении services/billing.md обнаружена зависимость
   от external payment gateway (не учтена в Impact)
   → Upward feedback: приостановка Design
   → Дополнить Impact: DEP-N (billing → payment-gateway)
   → Проверить Discussion: добавить зависимость в scope
   → AskUserQuestion: подтвердить
   → Возобновить генерацию Design

Далее стандартный поток: post-agent → reviewer → user review → artifacts
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [create-design-file.py](../.scripts/create-design-file.py) | Создание файла проектирования из шаблона (шаг 2) | Этот документ |
| [validate-design.py](../.scripts/validate-design.py) | Валидация созданного документа (шаг 4.6, шаг 7) | [validation-design.md](./validation-design.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/design-create](/.claude/skills/design-create/SKILL.md) | Создание документа проектирования (оркестратор) | Этот документ |

---

## Агенты

| Агент | Роль | Шаг | Обязательность |
|-------|------|-----|----------------|
| [design-agent](/.claude/agents/design-agent/AGENT.md) | Deep Scan + CLARIFY + GENERATE + VALIDATE | 4 | Обязателен |
| [design-reviewer](/.claude/agents/design-reviewer/AGENT.md) | Ревью распределения ответственностей, PROP-N | 6 | Обязателен |
