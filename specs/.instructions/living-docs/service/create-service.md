---
description: Воркфлоу создания сервисного документа services/{svc}.md — от Design → WAITING до создания stub с Резюме и Planned Changes, обновления README и labels.
standard: .instructions/standard-instruction.md
standard-version: v2.0
index: specs/.instructions/living-docs/service/README.md
---

# Воркфлоу создания сервисной документации

Рабочая версия стандарта: 2.0

Пошаговый процесс создания `specs/architecture/services/{svc}.md` при первом Design → WAITING для сервиса. Создаётся stub — файл-заглушка с Резюме и Planned Changes. Полное содержание заполняется позже при ADR → DONE (→ [modify-service.md](./modify-service.md)).

**Полезные ссылки:**
- [Стандарт сервисной документации](./standard-service.md)
- [Инструкции living-docs](../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-service.md](./standard-service.md) |
| Валидация | [validation-service.md](./validation-service.md) |
| Создание | Этот документ |
| Модификация | [modify-service.md](./modify-service.md) |

## Оглавление

- [Принципы](#принципы)
- [Когда создавать](#когда-создавать)
- [Шаги](#шаги)
  - [Шаг 1: Прочитать Design](#шаг-1-прочитать-design)
  - [Шаг 2: Создать services/{svc}.md (stub)](#шаг-2-создать-servicessvcmd-stub)
  - [Шаг 3: Заполнить Резюме и Planned Changes](#шаг-3-заполнить-резюме-и-planned-changes)
  - [Шаг 4: Обновить services/README.md](#шаг-4-обновить-servicesreadmemd)
  - [Шаг 5: Создать метку svc:{svc}](#шаг-5-создать-метку-svcsvc)
  - [Шаг 6: Валидация](#шаг-6-валидация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Триггер создания — Design → WAITING (первый для сервиса).** Файл-заглушка создаётся когда Design определил новый сервис. До ADR → DONE секции 2-6 остаются как placeholder.

> **Шаблон — из стандарта.** Использовать шаблон stub из [standard-service.md § 9.1](./standard-service.md#шаблон-stub-design--waiting). Запрещено придумывать свой формат.

> **Stub — минимальная операция.** Создаётся только `services/{svc}.md` (stub), строка в README и метка. Архитектурные файлы (system/, domains/) обновляются своим воркфлоу при Design → WAITING (Planned Changes).

---

## Когда создавать

| Событие | Действие |
|---------|----------|
| Design → WAITING (первый для сервиса) | Создать `services/{svc}.md` (stub) + README + метка |
| Design → WAITING (первый для домена) | Создать `domains/{domain}.md` (отдельный триггер) |

**НЕ создавать когда:**
- Design ещё в DRAFT
- Сервис уже существует (→ modify-service.md)
- Изменение shared/ кода (shared/ — не сервис, [§ 7](./standard-service.md#7-shared-код-shared))

---

## Шаги

### Шаг 1: Прочитать Design

Прочитать Design, который переходит в WAITING:

1. Найти **секцию сервиса** (`## Сервис {name}`) — Design содержит секции по сервисам
2. Извлечь **имя сервиса** (kebab-case, совпадает с `src/{service}/`)
3. Извлечь **назначение** (ответственность сервиса — 1-3 предложения для Резюме)
4. Извлечь **области влияния** (для поля "Затрагивает" в Planned Changes)

### Шаг 2: Создать services/{svc}.md (stub)

Создать файл по шаблону stub из [standard-service.md § 9.1](./standard-service.md#шаблон-stub-design--waiting).

**Путь:** `specs/architecture/services/{service}.md`

**Frontmatter (без `created-by`/`last-updated-by` — ADR ещё не существует):**

```yaml
---
description: Архитектура сервиса {service} — {назначение из Design}.
service: {service}
---
```

**SSOT frontmatter:** [standard-frontmatter.md § 5](/.structure/.instructions/standard-frontmatter.md#5-дополнительные-поля-для-живых-документов-архитектуры)

### Шаг 3: Заполнить Резюме и Planned Changes

Заполнить **2 секции**, остальные — placeholder:

| Секция | Содержание |
|--------|-----------|
| Резюме | Назначение из секции сервиса в Design (1-3 предложения) |
| API контракты | `*Заполняется при ADR → DONE.*` |
| Data Model | `*Заполняется при ADR → DONE.*` |
| Code Map | `*Заполняется при ADR → DONE.*` |
| Внешние зависимости | `*Заполняется при ADR → DONE.*` |
| Границы автономии LLM | `*Заполняется при ADR → DONE.*` |
| Planned Changes | Ссылка на Discussion + Design |
| Changelog | `*Нет записей.*` |

**Формат Planned Changes:**

```markdown
## Planned Changes

- **[Discussion N: {topic}]({путь к Discussion})**
  Статус: WAITING | Затрагивает: {области из Design}
  Design: [{design-id}]({путь к Design})
```

**Правила заполнения:** [standard-service.md § 5.7](./standard-service.md#57-planned-changes)

### Шаг 4: Обновить services/README.md

Добавить строку в таблицу `specs/architecture/services/README.md`:

```markdown
| `{service}` | {описание} | — | — | — |
```

**Примечание:** Колонки "Ключевые API", "Технологии" и "Последний ADR" заполняются при ADR → DONE.

**Формат таблицы:** [standard-service.md § 2](./standard-service.md#2-расположение-и-именование)

### Шаг 5: Создать метку svc:{svc}

```bash
# Через скилл
/labels-modify --add "svc:{service}" --color "C5DEF5" --description "Сервис {service}"
```

Или вручную: добавить в `.github/labels.yml` и синхронизировать.

### Шаг 6: Валидация

```bash
# Валидация сервисного документа (stub-режим)
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/{svc}.md --verbose

# Валидация архитектурных документов
python specs/.instructions/.scripts/validate-architecture.py --check-services --verbose
```

---

## Чек-лист

### Подготовка
- [ ] Design перешёл в WAITING (первый для сервиса)
- [ ] Имя сервиса определено (kebab-case, совпадает с `src/{service}/`)
- [ ] Секция сервиса в Design прочитана (назначение, области влияния)

### Создание файла
- [ ] `services/{svc}.md` создан по шаблону stub
- [ ] Frontmatter заполнен (description, service). БЕЗ `created-by`/`last-updated-by`
- [ ] Резюме заполнено (1-3 предложения из Design)
- [ ] Секции 2-6 содержат `*Заполняется при ADR → DONE.*`
- [ ] Planned Changes заполнены (ссылка на Discussion + Design)
- [ ] Changelog содержит `*Нет записей.*`

### Каскадные обновления
- [ ] `services/README.md` — строка добавлена (минимально)
- [ ] `labels.yml` — метка `svc:{service}` создана

### Валидация
- [ ] `validate-service.py` — пройден (stub-режим)
- [ ] `validate-architecture.py --check-services` — пройден

---

## Примеры

### Создание первого сервиса (auth) — stub

Полный пример двухфазного создания — [standard-service.md § 11.1](./standard-service.md#111-создание-первого-сервиса-auth).

```bash
# 1. Design design-0001 → WAITING (auth: аутентификация и авторизация)

# 2. Создать файл-заглушку
# specs/architecture/services/auth.md — по шаблону stub § 9.1

# 3. Заполнить Резюме + Planned Changes

# 4. Обновить services/README.md
# | `auth` | Аутентификация и авторизация | — | — | — |

# 5. Создать метку
# /labels-modify --add "svc:auth"

# 6. Валидация
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/auth.md --verbose
python specs/.instructions/.scripts/validate-architecture.py --check-services --verbose
```

---

## Скрипты

| Скрипт | Назначение | Путь |
|--------|------------|------|
| `validate-service.py` | Валидация `services/{svc}.md` (шаг 6) | [specs/.instructions/.scripts/validate-service.py](../../.scripts/validate-service.py) |
| `validate-architecture.py` | Валидация фиксированных файлов (шаг 6) | [specs/.instructions/.scripts/validate-architecture.py](../../.scripts/validate-architecture.py) |

---

## Скиллы

| Скилл | Назначение | Путь |
|-------|------------|------|
| `/service-create` | Создание `services/{svc}.md` (stub) | [.claude/skills/service-create/SKILL.md](/.claude/skills/service-create/SKILL.md) |
