---
description: Воркфлоу изменения сервисного документа services/{svc}.md — обновление при ADR/Design событиях, деактивация и миграция сервиса.
standard: .instructions/standard-instruction.md
standard-version: v2.2
index: specs/.instructions/living-docs/service/README.md
---

# Воркфлоу изменения сервисной документации

Рабочая версия стандарта: 2.2

Процессы изменения `specs/architecture/services/{svc}.md` в ответ на события SDD-lifecycle. Двухслойная модель: AS IS (факт) + Planned Changes (дельты ADDED/MODIFIED/REMOVED по каждому Design). ADR → DONE = миграция из Planned Changes в AS IS. Design → DONE = удаление блока Planned Changes + запись в Changelog.

**Полезные ссылки:**
- [Стандарт сервисной документации](./standard-service.md)
- [Инструкции living-docs](../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-service.md](./standard-service.md) |
| Валидация | [validation-service.md](./validation-service.md) |
| Создание | [create-service.md](./create-service.md) |
| Модификация | Этот документ |

## Оглавление

- [Типы изменений](#типы-изменений)
- [Обновление](#обновление)
  - [Сценарий A: повторный Design WAITING](#сценарий-a-повторный-design-waiting)
  - [Сценарий B: ADR WAITING](#сценарий-b-adr-waiting)
  - [Сценарий C: ADR DONE, заглушка → полный](#сценарий-c-adr-done-заглушка-полный)
  - [Сценарий D: ADR DONE, последующий](#сценарий-d-adr-done-последующий)
  - [Сценарий E: Design DONE](#сценарий-e-design-done)
  - [Сценарий F: REJECTED](#сценарий-f-rejected)
- [Деактивация](#деактивация)
- [Миграция](#миграция)
- [Обновление ссылок](#обновление-ссылок)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Типы изменений

| Тип | Описание | Пример |
|-----|----------|--------|
| Обновление | Изменение содержания по событию SDD-lifecycle | ADR → DONE: дельта → AS IS секции |
| Деактивация | Сервис удалён или не актуален | Удаление `src/{svc}/`, архивация документа |
| Миграция | Переименование сервиса | `auth` → `identity`, обновление всех ссылок |

**Триггеры обновления** — 6 сценариев (A–F). Полная таблица триггеров: [standard-service.md § 4](./standard-service.md#4-триггеры-создания-и-обновления).

---

## Обновление

### Сценарий A: повторный Design WAITING

**Триггер:** Design переходит в WAITING для **существующего** сервиса (файл `services/{svc}.md` уже есть).

**Шаги:**

#### Шаг A1: Прочитать Design

1. Найти секцию сервиса в Design
2. Извлечь **области влияния** (для поля "Затрагивает" в Planned Changes)

#### Шаг A2: Добавить блок Planned Changes

Добавить **новый блок** в секцию `## Planned Changes` файла `services/{svc}.md`:

```markdown
### {design-id}: {topic}

> [Discussion NNNN]({путь к Discussion}) →
> [Design NNNN]({путь к Design}) |
> Статус: WAITING

#### ADDED

{данные из Design — что этот Design добавляет в сервис}
{формат повторяет структуру AS IS секций: Резюме, API контракты, Data Model, Внешние зависимости}

#### MODIFIED

{что этот Design изменяет в существующем AS IS}
{таблица: Элемент | Изменение}

#### REMOVED

{что удаляется}
```

**Если AS IS секции пусты** (новый сервис) — все данные в ADDED, секции MODIFIED и REMOVED содержат `*Нет (новый сервис).*` или `*Нет.*`.

**Правила:** [standard-service.md § 5.7](./standard-service.md#57-planned-changes)

#### Шаг A3: Валидация

```bash
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/{svc}.md --verbose
```

---

### Сценарий B: ADR WAITING

**Триггер:** ADR переходит в WAITING — расширяем Planned Changes ссылкой на ADR.

**Шаги:**

#### Шаг B1: Найти запись Planned Changes

Найти в `services/{svc}.md` запись Planned Changes для соответствующего Discussion/Design.

#### Шаг B2: Добавить ссылку на ADR

Добавить строку `ADR:` в навигационный блок blockquote:

```markdown
### {design-id}: {topic}

> [Discussion NNNN]({путь}) →
> [Design NNNN]({путь}) |
> ADR: [{adr-id}]({путь к ADR}) |
> Статус: WAITING

#### ADDED
...
```

При нескольких ADR в одном Design — перечисляются все:
```markdown
> ADR: [{adr-1}]({путь}), [{adr-2}]({путь}) |
```

---

### Сценарий C: ADR DONE, заглушка → полный

**Триггер:** ADR → DONE, файл `services/{svc}.md` является **заглушкой** (нет `created-by` в frontmatter).

**Это ключевой сценарий:** данные из Planned Changes → ADDED мигрируют в AS IS секции (ранее пустые).

**Шаги:**

#### Шаг C1: Прочитать ADR и Planned Changes

1. Найти дельта-блоки ADR (ADDED/MODIFIED/REMOVED) — финальные данные
2. Найти блок Planned Changes для этого Design в `services/{svc}.md` — предварительные дельты
3. ADR = источник правды. Planned Changes = ориентир, ADR может добавить/изменить/удалить записи

#### Шаг C2: Обновить frontmatter

Добавить поля, отсутствующие в заглушке:

```yaml
---
description: Архитектура сервиса {service} — {назначение}.
service: {service}
created-by: {adr-id}
last-updated-by: {adr-id}
---
```

**SSOT frontmatter:** [standard-frontmatter.md § 5](/.structure/.instructions/standard-frontmatter.md#5-дополнительные-поля-для-живых-документов-архитектуры)

#### Шаг C3: Заполнить AS IS секции 1-6

AS IS секции заглушки содержат `*Нет.*` / `*Сервис ещё не реализован.*`. Заменить пустые маркеры финальным содержанием из дельты ADR:

| Секция | Источник | Примечание |
|--------|----------|-----------|
| Резюме | Дельта ADR — Резюме | 1-3 предложения |
| API контракты | Дельта ADR — ADDED endpoints | Таблица: Тип, Endpoint/Event, Метод, Описание |
| Data Model | Дельта ADR — ADDED entities | Таблица: Сущность, Хранилище, Назначение |
| Code Map | Дельта ADR — Tech Stack, пакеты, точки входа | 4 подсекции |
| Внешние зависимости | Дельта ADR — зависимости | Таблица: Тип, Путь/Сервис, Что используем, Роль |
| Границы автономии LLM | Дельта ADR — три уровня | Свободно, Флаг, CONFLICT |

**Источник данных:** ADR = финальный источник правды. Planned Changes → ADDED = ориентир, ADR может отличаться.

**Формат секций:** [standard-service.md § 5](./standard-service.md#5-секции-документа-сервиса)

#### Шаг C4: Удалить блок Planned Changes

Удалить весь блок Planned Changes для этого Design (от `### {design-id}:` до следующего `###` или `## Changelog`). Дельта применена в AS IS секциях.

Если других активных Design нет — секция Planned Changes содержит `*Нет активных Design.*`

Если Design → DONE одновременно — добавить запись в Changelog (см. Сценарий E).

#### Шаг C5: Обновить services/README.md

Заполнить колонки таблицы (ранее были прочерки):

```markdown
| `{service}` | {описание} | {ключевые API} | {технологии} | {adr-id} |
```

#### Шаг C6: Валидация

```bash
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/{svc}.md --verbose
```

Теперь скрипт работает в **full-режиме** (обнаруживает `created-by`).

---

### Сценарий D: ADR DONE, последующий

**Триггер:** ADR → DONE для сервиса с **полным** документом (есть `created-by`).

**Шаги:**

#### Шаг D1: Прочитать ADR

Извлечь дельта-блоки (ADDED/MODIFIED/REMOVED).

#### Шаг D2: Применить дельту к AS IS секциям

Применить изменения из дельты ADR к AS IS секциям `services/{svc}.md`. Блок Planned Changes для этого Design содержит предварительные ADDED/MODIFIED/REMOVED — ADR = финальный источник правды.

| Дельта | Действие в AS IS |
|--------|----------|
| ADDED | Добавить новые элементы в таблицы/списки |
| MODIFIED | Обновить существующие записи |
| REMOVED | Удалить элементы |

**Не менять секции, не затронутые дельтой.**

#### Шаг D3: Обновить frontmatter

```yaml
last-updated-by: {adr-id}
```

#### Шаг D4: Удалить блок Planned Changes

Удалить весь блок Planned Changes для этого Design (от `### {design-id}:` до следующего `###` или `## Changelog`). Дельта применена в AS IS.

Если других активных Design нет — `*Нет активных Design.*`

#### Шаг D5: Обновить services/README.md

Обновить колонки "Ключевые API", "Технологии", "Последний ADR" если изменились.

#### Шаг D6: Валидация

```bash
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/{svc}.md --verbose
```

---

### Сценарий E: Design DONE

**Триггер:** Design переходит в DONE — все ADR цепочки завершены.

**Действие:** Переместить запись из Planned Changes в Changelog.

**Шаги:**

#### Шаг E1: Найти запись в Planned Changes

Найти запись для завершённого Design в `services/{svc}.md`.

#### Шаг E2: Удалить блок Planned Changes и добавить в Changelog

**Удалить** весь блок для этого Design из `## Planned Changes` (от `### {design-id}:` до следующего `###` или `## Changelog`).

**Добавить** запись в начало `## Changelog`:

```markdown
## Changelog

- **{design-id}** ({дата}): {topic} — {краткое описание изменений: ADDED: ..., MODIFIED: ..., REMOVED: ...}
  [Discussion NNNN]({путь}) → [Design NNNN]({путь}) | ADR: [{adr-1}]({путь}) | DONE
```

Если блоков Planned Changes не осталось — `*Нет активных Design.*`

**Правила Changelog:** [standard-service.md § 5.8](./standard-service.md#58-changelog)

#### Шаг E3: Проверить полноту

- Все ссылки на ADR должны вести к ADR в статусе DONE
- В Planned Changes не осталось записей для этого Design
- AS IS секции содержат все изменения из ADR-цепочки

#### Шаг E4: Обновить system/ и domains/

> **Примечание:** system/ и domains/ файлы обновляются аналогично — Planned Changes → Changelog. Формат: [standard-architecture.md](../architecture/standard-architecture.md).

#### Шаг E5: Валидация

```bash
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/{svc}.md --verbose
python specs/.instructions/.scripts/validate-architecture.py --check-services --verbose
```

---

### Сценарий F: REJECTED

**Триггер:** Design или ADR отклонён (→ REJECTED).

**Шаги:**

#### Шаг F1: Удалить блок Planned Changes и добавить в Changelog

**Удалить** весь блок для этого Design из `## Planned Changes`.

**Добавить** в начало `## Changelog`:

```markdown
- **{design-id}** ({дата}): {topic} — REJECTED
  [Discussion NNNN]({путь}) → [Design NNNN]({путь}) | ADR: [{adr-1}]({путь}) | REJECTED
```

#### Шаг F2: Откатить частичные изменения (если нужно)

Если ADR → DONE уже применил дельту, а Design → REJECTED:
1. Создать **новый ADR** с обратной дельтой (откат)
2. Применить откат через сценарий D
3. Запись в Changelog помечается `REJECTED` + ссылка на ADR-откат

#### Шаг F3: Обновить system/ и domains/

Аналогично — PC → Changelog с маркером REJECTED.

---

## Деактивация

Когда сервис удаляется из проекта (`src/{svc}/` удалён).

### Шаг 1: Удалить файл сервиса

```bash
rm specs/architecture/services/{svc}.md
```

### Шаг 2: Удалить строку из README

Удалить строку сервиса из `specs/architecture/services/README.md`.

### Шаг 3: Удалить метку

```bash
/labels-modify --remove "svc:{svc}"
```

### Шаг 4: Обновить архитектурные документы

Убрать упоминания сервиса из `system/` и `domains/` файлов.

### Шаг 5: Проверить ссылки

```bash
/links-validate --path specs/architecture/
```

---

## Миграция

Когда сервис переименовывается (например, `auth` → `identity`).

### Шаг 1: Переименовать файл

```bash
git mv specs/architecture/services/{old}.md specs/architecture/services/{new}.md
```

### Шаг 2: Обновить frontmatter

```yaml
description: Архитектура сервиса {new} — {назначение}.
service: {new}
```

### Шаг 3: Обновить services/README.md

Заменить `{old}` на `{new}` в таблице.

### Шаг 4: Обновить метку

```bash
/labels-modify --rename "svc:{old}" "svc:{new}"
```

### Шаг 5: Обновить ссылки

Найти и обновить все ссылки на старый файл:

```bash
/links-validate --path specs/
```

### Шаг 6: Обновить архитектурные документы

Обновить упоминания сервиса в `system/` и `domains/` файлах.

---

## Обновление ссылок

### При переименовании файла

Найти и заменить все ссылки на старый файл:

```bash
# 1. Найти все ссылки
/links-validate --path specs/architecture/

# 2. Или вручную через Grep
# Grep: паттерн "{old}.md" в specs/ и .instructions/
```

### При изменении заголовков

Если заголовки (якоря) в `services/{svc}.md` изменились — проверить внешние ссылки:

```bash
/links-validate --path specs/
```

---

## Чек-лист

### Обновление — Сценарий A (Design → WAITING)
- [ ] Design в статусе WAITING (не DRAFT)
- [ ] Файл `services/{svc}.md` существует
- [ ] Блок Planned Changes добавлен: `### {design-id}: {topic}` + ADDED/MODIFIED/REMOVED
- [ ] AS IS секции не изменялись
- [ ] Валидация пройдена

### Обновление — Сценарий B (ADR → WAITING)
- [ ] ADR в статусе WAITING
- [ ] Блок Planned Changes для этого Design найден в `services/{svc}.md`
- [ ] Строка `ADR:` добавлена в навигационный blockquote блока
- [ ] Валидация пройдена

### Обновление — Сценарий C (ADR → DONE, заглушка → полный)
- [ ] ADR в статусе DONE
- [ ] Файл — заглушка (нет `created-by`)
- [ ] Frontmatter: добавлены `created-by`, `last-updated-by`
- [ ] AS IS секции 1-6 заполнены из дельты ADR (маркеры `*Нет.*` заменены)
- [ ] Блок Planned Changes для этого Design удалён
- [ ] `services/README.md`: колонки заполнены
- [ ] Валидация в full-режиме пройдена

### Обновление — Сценарий D (ADR → DONE, последующий)
- [ ] ADR в статусе DONE
- [ ] Файл — full (есть `created-by`)
- [ ] Дельта из ADR применена к AS IS секциям (ADDED/MODIFIED/REMOVED)
- [ ] `last-updated-by` обновлён
- [ ] Блок Planned Changes для этого Design удалён
- [ ] `services/README.md` обновлён
- [ ] Валидация пройдена

### Обновление — Сценарий E (Design → DONE)
- [ ] Все ADR цепочки в DONE
- [ ] Блок Planned Changes для этого Design удалён
- [ ] Запись добавлена в Changelog: маркер DONE + дата + краткое описание
- [ ] system/ и domains/ обновлены аналогично
- [ ] Валидация пройдена

### Обновление — Сценарий F (REJECTED)
- [ ] Блок Planned Changes для этого Design удалён
- [ ] Запись добавлена в Changelog с маркером REJECTED
- [ ] Частичные изменения откачены (если были)
- [ ] system/ и domains/ обновлены

### Деактивация
- [ ] Файл `services/{svc}.md` удалён
- [ ] Строка из `services/README.md` удалена
- [ ] Метка `svc:{svc}` удалена
- [ ] Архитектурные документы обновлены
- [ ] Ссылки проверены

### Миграция
- [ ] Файл переименован (`git mv`)
- [ ] Frontmatter обновлён (`service`, `description`)
- [ ] `services/README.md` обновлён
- [ ] Метка переименована
- [ ] Все ссылки обновлены
- [ ] Архитектурные документы обновлены

---

## Примеры

### ADR → DONE (заглушка → полный) — сервис auth

```bash
# 1. ADR adr-0001 → DONE для auth (заглушка → полный)

# 2. Обновить frontmatter — добавить created-by, last-updated-by
# specs/architecture/services/auth.md

# 3. Заполнить AS IS секции 1-6 из дельты ADR (заменить *Нет.* на данные)

# 4. Удалить блок Planned Changes для design-0001 (дельта применена в AS IS)
#    Если Planned Changes пуст — *Нет активных Design.*

# 5. Обновить services/README.md — заполнить колонки

# 6. Валидация
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/auth.md --verbose
```

### Design → WAITING для существующего сервиса

```bash
# 1. Design design-0002 → WAITING, затрагивает notification (уже существует, full)

# 2. Добавить новый блок в Planned Changes:
#    ### design-0002: notification preferences
#    > [Discussion 0002](...) → [Design 0002](...) | Статус: WAITING
#    #### ADDED
#    ...новые endpoint'ы и сущности...
#    #### MODIFIED
#    ...что изменяется в существующем AS IS...
#    #### REMOVED
#    *Нет.*

# 3. AS IS секции НЕ менять

# 4. Валидация
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/notification.md --verbose
```

### Design → DONE — перемещение в Changelog

```bash
# 1. Design design-0001 → DONE (все ADR завершены)

# 2. Удалить блок Planned Changes для design-0001

# 3. Добавить запись в Changelog:
#    - **design-0001** (2026-02-20): realtime notifications — ADDED: Notification service,
#      REST API, WebSocket, PostgreSQL + Redis.
#      [Discussion 0001](...) → [Design 0001](...) | ADR: [adr-0001](...) | DONE

# 4. Проверить полноту — все ADR DONE, AS IS секции содержат изменения

# 5. Обновить system/ и domains/ аналогично

# 6. Валидация
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/auth.md --verbose
python specs/.instructions/.scripts/validate-architecture.py --check-services --verbose
```

---

## Скрипты

| Скрипт | Назначение | Путь |
|--------|------------|------|
| `validate-service.py` | Валидация `services/{svc}.md` (полный/заглушка) | [specs/.instructions/.scripts/validate-service.py](../../.scripts/validate-service.py) |
| `validate-architecture.py` | Валидация фиксированных файлов | [specs/.instructions/.scripts/validate-architecture.py](../../.scripts/validate-architecture.py) |

---

## Скиллы

| Скилл | Назначение | Путь |
|-------|------------|------|
| `/service-modify` | Изменение `services/{svc}.md` по событию SDD | [.claude/skills/service-modify/SKILL.md](/.claude/skills/service-modify/SKILL.md) |
