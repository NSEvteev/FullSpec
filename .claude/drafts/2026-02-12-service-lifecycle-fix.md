# Исправление lifecycle services/{svc}.md

Исправление противоречий в триггерах создания/обновления сервисного документа + добавление секции Changelog.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Проблема](#проблема)
  - [Решение](#решение)
  - [Затронутые файлы](#затронутые-файлы)
- [Открытые вопросы](#открытые-вопросы)
- [Решения](#решения)

---

## Контекст

**Задача:** Исправить противоречия в таблице триггеров `standard-service.md § 4` и `standard-specs.md § 5, 6, 8.5, 9` — файл `services/{svc}.md` используется для записи Planned Changes до того, как он создан.

**Почему создан:** При анализе `create-service.md` обнаружено, что триггер "ADR → DONE (первый для сервиса) → Создать" противоречит двум более ранним триггерам, которые пишут в тот же файл (Design → WAITING, ADR → WAITING).

**Связанные файлы:**
- [standard-service.md](/specs/.instructions/living-docs/service/standard-service.md) — § 1, § 4, § 5.7, § 9, § 10
- [standard-specs.md](/specs/.instructions/standard-specs.md) — § 5, § 6, § 8.5, § 9.1, § 9.3
- [standard-frontmatter.md](/.structure/.instructions/standard-frontmatter.md) — § 5 (новый)
- [standard-architecture.md](/specs/.instructions/living-docs/architecture/standard-architecture.md) — § 4, § 5
- [create-service.md](/specs/.instructions/living-docs/service/create-service.md)
- [validation-service.md](/specs/.instructions/living-docs/service/validation-service.md)
- [validate-service.py](/specs/.instructions/.scripts/validate-service.py)
- [search-docs.py](/.instructions/.scripts/search-docs.py)

---

## Содержание

### Проблема

#### Противоречия в standard-service.md § 4

Текущая таблица триггеров:

| Событие | Действие | Файлы |
|---------|----------|-------|
| Design → WAITING | Добавить **Planned Changes** | `services/{svc}.md` для затронутых сервисов |
| ADR → WAITING | Добавить ссылку на ADR в Planned Changes | `services/{svc}.md` |
| **ADR → DONE (первый для сервиса)** | **Создать** | `services/{svc}.md` |

На шагах Design → WAITING и ADR → WAITING мы **записываем** в `services/{svc}.md`, но файл **создаётся** только при ADR → DONE. Для **нового** сервиса файла не существует.

Для `domains/` проблема решена — есть явная строка:
```
Design → WAITING (первый для домена) | Создать + Planned Changes | domains/{domain}.md
```

Для `services/` аналогичной строки **нет**.

#### Противоречия в standard-specs.md

1. **§ 5** (строка 405): `Design → WAITING → Planned Changes добавляются в architecture/` — подразумевает, что `services/{svc}.md` уже существует.
2. **§ 6** (строка 501): `Greenfield: ADR создаёт начальную архитектуру` — говорит, что файл создаётся при ADR.
3. **§ 8.5** (строка 900): `ADR → DONE | обновление architecture/services/{svc}.md` — слово "обновление" подразумевает, что файл уже существует.

#### Противоречие в lifecycle § 1

```
4. Design → WAITING: Planned Changes добавляются в services/{svc}.md  ← ПИШЕМ
6. ADR → DONE: Создаётся/обновляется architecture/services/X.md      ← СОЗДАЁМ
```

Шаг 4 пишет в файл, шаг 6 создаёт его.

### Решение

#### 1. Двухфазное создание

Файл `services/{svc}.md` создаётся в **два этапа** (по аналогии с `domains/{domain}.md`):

**Фаза 1 — Design → WAITING (первый для сервиса):** Создать файл-заглушку:
- Frontmatter: `description`, `service` (без `created-by`/`last-updated-by` — ADR ещё не существует)
- Резюме: назначение из секции сервиса в Design (1-3 предложения)
- Секции 2-6: `*Заполняется при ADR → DONE.*`
- Planned Changes: заполнены (ссылка на Discussion + Design)

**Фаза 2 — ADR → DONE (первый для сервиса):** Заполнить полное содержание:
- Frontmatter: добавить `created-by` и `last-updated-by`
- Все 7 секций заполнены из дельты ADR
- Planned Changes: ADR-часть "применена" (перенесена в AS IS)

#### 2. Обратная симметрия DONE

Полный lifecycle с обратной симметрией (top-down при планировании, bottom-up при реализации):

```
ПЛАНИРОВАНИЕ (top-down, от общего к частному):
  Design → WAITING  → создаёт stub + Planned Changes (высокоуровневый)
  ADR → WAITING     → расширяет Planned Changes (детальный, со ссылкой на ADR)

РЕАЛИЗАЦИЯ (bottom-up, от частного к общему):
  ADR → DONE        → применяет дельту: Planned Changes → AS IS секции
  Design → DONE     → проверяет полноту, Planned Changes → Changelog
```

**При нескольких ADR в одном Design:**

```
Design → WAITING:   stub + PC(Design)
ADR-1 → WAITING:   PC расширен ссылкой на ADR-1
ADR-2 → WAITING:   PC расширен ссылкой на ADR-2
ADR-1 → DONE:      дельта ADR-1 применена → AS IS, ссылка ADR-1 убрана из PC
ADR-2 → DONE:      дельта ADR-2 применена → AS IS, ссылка ADR-2 убрана из PC
Design → DONE:      всё применено, PC(Design) → Changelog
```

#### 3. Секция Changelog

8-я секция в `services/{svc}.md` — после Planned Changes.

**Назначение:** История изменений сервисного документа. Когда Design → DONE перемещает запись из Planned Changes, она не удаляется, а переносится в Changelog.

**Формат:**

```markdown
## Changelog

- **[disc-0002: Pricing Service](...)** | DONE 2026-03-15
  Design: [design-0002](...) | ADR: [adr-0003](...)
  Затрагивало: API endpoints, data model

- **[disc-0001: OAuth2 авторизация](...)** | DONE 2026-02-10
  Design: [design-0001](...) | ADR: [adr-0001](...), [adr-0002](...)
  Затрагивало: Создание сервиса
```

**Правила:**
1. Записи добавляются в обратном хронологическом порядке (новые сверху)
2. Каждая запись — навигационный указатель (не копия дельт)
3. Маркер `DONE` — финальный статус цепочки
4. При REJECTED — запись тоже переносится, но с маркером `REJECTED`
5. При CONFLICT-резолюции — запись обновляется (дополнительная пометка)

**Рост файла:** Changelog растёт линейно с количеством Design-цепочек, затронувших сервис. Для типичного сервиса — 5-20 записей за всю жизнь. Не проблема.

#### Обновлённая таблица триггеров (standard-service.md § 4)

| Событие | Действие | Файлы |
|---------|----------|-------|
| Design → WAITING (первый для сервиса) | **Создать** (stub + Planned Changes) | `services/{svc}.md` |
| Design → WAITING | Добавить **Planned Changes** | `system/`, `domains/`, `services/{svc}.md` для затронутых сервисов |
| Design → WAITING (первый для домена) | **Создать** + Planned Changes | `domains/{domain}.md` |
| ADR → WAITING | Расширить Planned Changes (ссылка на ADR) | `services/{svc}.md` |
| ADR → DONE (первый для сервиса) | **Заполнить** полное содержание (дельта → AS IS) | `services/{svc}.md`, строка в `services/README.md` |
| ADR → DONE (последующий) | **Обновить** (дельта → AS IS) | `services/{svc}.md`, `services/README.md` |
| Design → DONE | Проверить полноту, **Planned Changes → Changelog** | `system/`, `domains/`, `services/{svc}.md` |
| Создание папки `specs/services/{svc}/` | **Создать** метку `svc:{svc}` | `labels.yml`, GitHub |
| Удаление папки `specs/services/{svc}/` | **Удалить** метку `svc:{svc}` | `labels.yml`, GitHub |
| Design/ADR → REJECTED | Убрать Planned Changes, **→ Changelog** (с маркером REJECTED) | затронутые файлы |

#### Обновлённый lifecycle (standard-service.md § 1)

```
1. Инициализация проекта: system/ и domains/ файлы создаются как пустые шаблоны
2. Discussion → Impact: "Нужен сервис X" (предложение)
   - Если architecture/services/X.md существует → читать Резюме + Planned Changes
   - Если не существует → Impact предлагает "Новый (план создания)"
3. Impact → Design: Design РЕШАЕТ создание/использование
4. Design → WAITING: services/{svc}.md создаётся (stub + Planned Changes)
   system/, domains/ получают Planned Changes
5. Design → ADR: ADR для сервиса X
6. ADR → WAITING: services/{svc}.md — Planned Changes расширены (ссылка на ADR)
7. ADR → DONE: services/{svc}.md — дельта применена (Planned Changes → AS IS)
   services/README.md обновляется (новая строка в таблице)
8. Design → DONE: Planned Changes → Changelog в services/{svc}.md, system/, domains/
```

#### Шаблон stub (services/{svc}.md при Design → WAITING)

```markdown
---
description: Архитектура сервиса {service} — {назначение из Design}.
service: {service}
---

# {service-name}

## Резюме

{назначение из секции сервиса в Design — 1-3 предложения}

## API контракты

*Заполняется при ADR → DONE.*

## Data Model

*Заполняется при ADR → DONE.*

## Code Map

*Заполняется при ADR → DONE.*

## Внешние зависимости

*Заполняется при ADR → DONE.*

## Границы автономии LLM

*Заполняется при ADR → DONE.*

## Planned Changes

- **[Discussion N: {topic}]({путь})**
  Статус: WAITING | Затрагивает: {области}
  Design: [{design-id}]({путь})

## Changelog

*Нет записей.*
```

### Затронутые файлы

#### standard-service.md

| Секция | Что менять |
|--------|-----------|
| § 1 Назначение | Обновить lifecycle (8 шагов вместо 8, но с новыми формулировками) |
| § 2 Расположение | Обновить таблицу "Создаётся" для services/ — `Design → WAITING (stub)` вместо `Первый ADR → DONE` |
| § 3 Frontmatter | Заменить контент на SSOT-ссылку: `**SSOT:** [standard-frontmatter.md § 5](...)`. Убрать таблицу полей и пример — они переезжают в standard-frontmatter.md |
| § 4 Триггеры | Обновить таблицу триггеров (см. выше). Добавить описание Design → DONE |
| § 5 Секции | Добавить § 5.8 Changelog. Обновить таблицу: 8 секций вместо 7 |
| § 5.7 Planned Changes | Обновить правила: ADR → DONE частично "применяет" PC, Design → DONE перемещает в Changelog |
| § 9.1 Шаблон | Добавить секцию Changelog. Добавить шаблон stub |
| § 9.2 Каскадные документы | Обновить таблицу: stub при Design → WAITING, заполнение при ADR → DONE |
| § 10 Чек-лист | Добавить проверки Changelog |
| § 11 Примеры | Обновить пример 11.1 — двухфазное создание |

#### standard-specs.md

| Место | Что менять |
|-------|-----------|
| § 2 mermaid-диаграмма | `LIVE` блок — добавить "Planned Changes при → WAITING" |
| § 5 Прямой поток | Шаг 3: "Design → WAITING → Planned Changes добавляются, **services/{svc}.md создаётся**" |
| § 6 Greenfield | Убрать "ADR создаёт начальную архитектуру". Вместо: "stub создаётся при Design → WAITING, заполняется при ADR → DONE" |
| § 8.5 ADR → DONE | Уточнить: "обновление" (не "создание") `architecture/services/{svc}.md` — файл уже существует как stub |
| § 9.1 | Добавить упоминание создания stub для новых сервисов |
| § 9.3 | Добавить строку Design → DONE: "Planned Changes → Changelog в services/{svc}.md, system/, domains/" |

#### create-service.md

Полная переработка — триггер меняется с "ADR → DONE" на "Design → WAITING", шаги другие:

| Шаг | Старый | Новый |
|-----|--------|-------|
| Триггер | ADR → DONE (первый для сервиса) | Design → WAITING (первый для сервиса) |
| 1 | Прочитать ADR | Прочитать Design (секция сервиса) |
| 2 | Создать services/{svc}.md (полный) | Создать services/{svc}.md (stub) |
| 3 | Заполнить 7 секций | Заполнить Резюме + Planned Changes |
| 4 | Обновить services/README.md | Обновить services/README.md (минимально) |
| 5 | Обновить архитектурные документы | — (system/, domains/ обновляются своим воркфлоу) |
| 6 | Создать метку svc:{svc} | Создать метку svc:{svc} |
| 7 | Валидация | Валидация (stub-режим) |

**Замечание:** Шаги "заполнить полное содержание при ADR → DONE" и "переместить PC → Changelog при Design → DONE" — это территория `modify-service.md`, а не `create-service.md`.

#### validation-service.md

| Что менять |
|-----------|
| Добавить проверку Changelog (SVC014) |
| Правила для stub: секции 2-6 могут быть `*Заполняется при ADR → DONE.*` |
| Frontmatter: `created-by`/`last-updated-by` — опциональны для stub, обязательны для полного документа |

#### validate-service.py

| Что менять |
|-----------|
| Добавить проверку Changelog (SVC014) |
| Добавить режим `--stub` для валидации файла-заглушки |
| В обычном режиме: 8 секций вместо 7 |

#### standard-frontmatter.md (SSOT frontmatter)

| Что менять |
|-----------|
| Добавить **§ 5** "Дополнительные поля для живых документов архитектуры" |
| Перенести контент из standard-service.md § 3 (таблица полей, пример, правила) |
| Добавить: `created-by`/`last-updated-by` — опциональны для stub, обязательны для полного документа |
| Добавить: логика stub-детекции (Q4) — отсутствие `created-by` + проверка содержимого |
| Добавить пример frontmatter для stub и для полного документа |

#### standard-architecture.md

| Что менять |
|-----------|
| Добавить секцию Changelog в шаблоны фиксированных файлов (§ 5) |
| Добавить Changelog в обязательные секции (§ 4) |

#### search-docs.py

Скрипт собирает 6 типов: instruction, skill, agent, rule, readme, script. **Не собирает:**
- `specs/architecture/services/*.md` — сервисные документы
- `specs/architecture/system/*.md` — системные файлы
- `specs/architecture/domains/*.md` — доменные файлы

| Что менять |
|-----------|
| Новый тип `--type service` для `specs/architecture/services/*.md` |
| Показывать статус: stub (нет `created-by`) / full |
| Читать frontmatter: `service`, `created-by`, `last-updated-by` |
| Обновить `VALID_TYPES` — добавить `"service"` |
| Новая функция `collect_services()` |

---

## Решения

| # | Вопрос | Решение |
|---|--------|---------|
| 1 | Когда создаётся `services/{svc}.md` | **Design → WAITING** (stub + Planned Changes), по аналогии с `domains/{domain}.md` |
| 2 | Когда заполняется полное содержание | **ADR → DONE** (дельта → AS IS) |
| 3 | Что происходит при Design → DONE | Planned Changes → **Changelog** (не удаляются) |
| 4 | Обратная симметрия | **Top-down при WAITING, bottom-up при DONE** |
| 5 | Количество секций | **8** (+ Changelog после Planned Changes) |
| Q1 | CONFLICT-записи в Changelog | **C** — только если CONFLICT изменил AS IS секции (не Planned Changes). Маркер `CONFLICT-RESOLVED` |
| Q2 | REJECTED-записи в Changelog | **A** — да, с маркером `REJECTED`. Полная история, REJECTED редки |
| Q3 | Changelog в system/domains | **A** — во всех живых документах. Единообразие, рост управляем (одна запись на Design-цепочку) |
| Q4 | Формат frontmatter для stub | **D** (комбинация A+C) — отсутствие `created-by` = основной признак + проверка содержимого секций. Двойная валидация: frontmatter и контент согласованы |
| 6 | SSOT frontmatter архитектуры | **standard-frontmatter.md § 5** — SSOT. Контент переносится из standard-service.md § 3. В § 3 остаётся ссылка |
| 7 | search-docs.py | **В основной план.** Новый тип `--type service` |

### Детали решения Q4

Логика валидации stub vs full:

```
если нет created-by:
  → stub-режим
  → секции 2-6 ДОЛЖНЫ быть "*Заполняется при ADR → DONE.*"
  → если секции заполнены → ошибка SVC004 "created-by обязателен для заполненного документа"

если есть created-by:
  → полный режим
  → все секции ДОЛЖНЫ быть заполнены
  → если есть "*Заполняется при ADR → DONE.*" → ошибка "stub-placeholder в полном документе"
```

### Полный список затронутых файлов (9)

| # | Файл | Объём изменений |
|---|------|----------------|
| 1 | `standard-service.md` | Крупный — § 1, 2, 3, 4, 5, 9, 10, 11 |
| 2 | `standard-specs.md` | Средний — § 2, 5, 6, 8.5, 9.1, 9.3 |
| 3 | `standard-frontmatter.md` | Средний — новый § 5 (перенос из standard-service.md § 3) |
| 4 | `standard-architecture.md` | Малый — Changelog в шаблонах (Q3) |
| 5 | `create-service.md` | Крупный — полная переработка |
| 6 | `validation-service.md` | Средний — Changelog, stub-режим |
| 7 | `validate-service.py` | Средний — Changelog, stub-режим |
| 8 | `search-docs.py` | Малый — новый тип `service` |
| 9 | `specs/.instructions/living-docs/service/README.md` | Малый — обновить дерево |
