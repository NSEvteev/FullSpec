---
description: Воркфлоу создания сервисного документа services/{svc}.md — от Design → WAITING до создания заглушки с Резюме и Planned Changes, обновления README и labels.
standard: .instructions/standard-instruction.md
standard-version: v2.2
index: specs/.instructions/living-docs/service/README.md
---

# Воркфлоу создания сервисной документации

Рабочая версия стандарта: 2.2

Пошаговый процесс создания `specs/architecture/services/{svc}.md` при первом Design → WAITING для сервиса. Создаётся заглушка с Резюме и Planned Changes. Полное содержание заполняется позже при ADR → DONE (→ [modify-service.md](./modify-service.md)).

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
  - [Шаг 1: Прочитать Design и Impact](#шаг-1-прочитать-design-и-impact)
  - [Шаг 2: Создать services/{svc}.md (заглушка)](#шаг-2-создать-servicessvcmd-заглушка)
  - [Шаг 3: Заполнить секции](#шаг-3-заполнить-секции)
  - [Шаг 4: Обновить services/README.md](#шаг-4-обновить-servicesreadmemd)
  - [Шаг 5: Создать метку svc:{svc}](#шаг-5-создать-метку-svcsvc)
  - [Шаг 6: Валидация](#шаг-6-валидация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Триггер создания — Design → WAITING (первый для сервиса).** Заглушка создаётся когда Design определил новый сервис. До ADR → DONE секции 2-6 остаются как placeholder.

> **Шаблон — из стандарта.** Использовать шаблон заглушки из [standard-service.md § 9.1](./standard-service.md#шаблон-заглушки-design-waiting). Запрещено придумывать свой формат.

> **Заглушка — минимальная операция.** Создаётся только `services/{svc}.md` (заглушка), строка в README и метка. Архитектурные файлы (system/, domains/) обновляются своим воркфлоу при Design → WAITING (Planned Changes).

---

## Когда создавать

| Событие | Действие |
|---------|----------|
| Design → WAITING (первый для сервиса) | Создать `services/{svc}.md` (заглушка) + README + метка |
| Design → WAITING (первый для домена) | Создать `domains/{domain}.md` (отдельный триггер) |

**НЕ создавать когда:**
- Design ещё в DRAFT
- Сервис уже существует (→ modify-service.md)
- Изменение shared/ кода (shared/ — не сервис, [§ 7](./standard-service.md#7-shared-код-shared))

---

## Шаги

### Шаг 1: Прочитать Design и Impact

Прочитать Design, который переходит в WAITING, и parent Impact:

1. Найти **секцию сервиса** (`## SVC-N: {name}`) — Design содержит секции по сервисам
2. Извлечь **имя сервиса** (kebab-case, совпадает с `src/{service}/`)
3. Извлечь **назначение** (ответственность сервиса — 1-3 предложения для Planned Changes → ADDED → Резюме)
4. Из **parent Impact** (SVC-N для этого сервиса):
   - **API-N** — endpoints/события для Planned Changes → ADDED → API контракты
   - **DATA-N** — сущности/хранилища для Planned Changes → ADDED → Data Model
5. Из **Design** (SVC-N + INT-N):
   - **Dependencies** из SVC-N → для Planned Changes → ADDED → Внешние зависимости
   - **INT-N → Contract** — дополнительные зависимости из контрактов взаимодействия

### Шаг 2: Создать services/{svc}.md (заглушка)

```bash
python specs/.instructions/.scripts/create-service-file.py --svc {service} --design specs/design/design-NNNN-topic.md [--description "назначение"]
```

Скрипт создаёт `specs/architecture/services/{service}.md` по шаблону заглушки из [standard-service.md § 9.1](./standard-service.md#шаблон-заглушки-design-waiting). Проверяет status Design = WAITING, извлекает ссылки на Discussion/Design для Planned Changes.

**Вручную (если скрипт недоступен):**

**Путь:** `specs/architecture/services/{service}.md`

**Frontmatter (без `created-by`/`last-updated-by` — ADR ещё не существует):**

```yaml
---
description: Архитектура сервиса {service} — {назначение из Design}.
service: {service}
---
```

**SSOT frontmatter:** [standard-frontmatter.md § 5](/.structure/.instructions/standard-frontmatter.md#5-дополнительные-поля-для-живых-документов-архитектуры)

### Шаг 3: Заполнить секции (двухслойная модель)

**AS IS секции (1–6)** — пусты. Сервис ещё не реализован, данные НЕ копируются из Impact/Design.

| Секция | Содержание |
|--------|-----------|
| Резюме | `*Сервис ещё не реализован.*` |
| API контракты | `*Нет.*` |
| Data Model | `*Нет.*` |
| Code Map | `*Нет.*` |
| Внешние зависимости | `*Нет.*` |
| Границы автономии LLM | `*Нет.*` |

**Planned Changes** — один блок для Design с дельтами ADDED/MODIFIED/REMOVED:

| Подсекция | Содержание | Источник |
|-----------|-----------|----------|
| ADDED → Резюме | Назначение сервиса (1-3 предложения) | Design SVC-N |
| ADDED → API контракты | Таблица endpoints/событий | Impact SVC-N → API-N, Design INT-N |
| ADDED → Data Model | Таблица сущностей/хранилищ | Impact SVC-N → DATA-N |
| ADDED → Внешние зависимости | Таблица зависимостей | Design SVC-N → Dependencies + INT-N |
| MODIFIED | `*Нет (новый сервис).*` | — |
| REMOVED | `*Нет.*` | — |

**Changelog:** `*Нет записей.*`

**Формат Planned Changes блока:**

```markdown
## Planned Changes

### design-NNNN: {topic}

> [Discussion NNNN]({путь к Discussion}) →
> [Design NNNN]({путь к Design}) |
> Статус: WAITING

#### ADDED

**Резюме:** {назначение из Design SVC-N — 1-3 предложения}

**API контракты:**

| Тип | Endpoint/Event | Метод | Описание |
|-----|---------------|-------|----------|
| ... | ... | ... | ... |

**Data Model:**

| Сущность | Хранилище | Назначение |
|----------|-----------|-----------|
| ... | ... | ... |

**Внешние зависимости:**

| Тип | Путь/Сервис | Что используем | Роль |
|-----|------------|---------------|------|
| ... | ... | ... | ... |

#### MODIFIED

*Нет (новый сервис).*

#### REMOVED

*Нет.*
```

**Правила:** [standard-service.md § 5.7](./standard-service.md#57-planned-changes)

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
# Валидация сервисного документа (режим заглушки)
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
- [ ] `services/{svc}.md` создан по шаблону заглушки
- [ ] Frontmatter заполнен (description, service). БЕЗ `created-by`/`last-updated-by`
- [ ] Оглавление присутствует
- [ ] AS IS секции (1–6) содержат `*Нет.*` или `*Сервис ещё не реализован.*`
- [ ] Planned Changes содержит блок Design с ADDED/MODIFIED/REMOVED
- [ ] Данные из Impact/Design размещены в Planned Changes → ADDED (не в AS IS)
- [ ] Changelog содержит `*Нет записей.*`

### Каскадные обновления
- [ ] `services/README.md` — строка добавлена (минимально)
- [ ] `labels.yml` — метка `svc:{service}` создана

### Валидация
- [ ] `validate-service.py` — пройден (режим заглушки)
- [ ] `validate-architecture.py --check-services` — пройден

---

## Примеры

### Создание первого сервиса (auth) — заглушка

Полный пример двухфазного создания — [standard-service.md § 11.1](./standard-service.md#111-создание-первого-сервиса-auth).

```bash
# 1. Design design-0001 → WAITING (auth: аутентификация и авторизация)

# 2. Создать заглушку
# specs/architecture/services/auth.md — по шаблону заглушки § 9.1

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
| `create-service-file.py` | Создание файла-заглушки из шаблона (шаг 2) | [specs/.instructions/.scripts/create-service-file.py](../../.scripts/create-service-file.py) |
| `validate-service.py` | Валидация `services/{svc}.md` (шаг 6) | [specs/.instructions/.scripts/validate-service.py](../../.scripts/validate-service.py) |
| `validate-architecture.py` | Валидация фиксированных файлов (шаг 6) | [specs/.instructions/.scripts/validate-architecture.py](../../.scripts/validate-architecture.py) |

---

## Скиллы

| Скилл | Назначение | Путь |
|-------|------------|------|
| `/service-create` | Создание `services/{svc}.md` (заглушка) | [.claude/skills/service-create/SKILL.md](/.claude/skills/service-create/SKILL.md) |
