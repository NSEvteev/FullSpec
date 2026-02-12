---
description: Воркфлоу изменения сервисного документа services/{svc}.md — обновление при ADR/Design событиях, деактивация и миграция сервиса.
standard: .instructions/standard-instruction.md
standard-version: v2.0
index: specs/.instructions/living-docs/service/README.md
---

# Воркфлоу изменения сервисной документации

Рабочая версия стандарта: 2.0

Процессы изменения `specs/architecture/services/{svc}.md` в ответ на события SDD-lifecycle: заполнение содержания при ADR → DONE, перемещение Planned Changes → Changelog при Design → DONE, деактивация и миграция сервиса.

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
  - [Сценарий C: ADR DONE, stub to full](#сценарий-c-adr-done-stub-to-full)
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

#### Шаг A2: Добавить Planned Changes

Добавить запись в секцию `## Planned Changes` файла `services/{svc}.md`:

```markdown
- **[Discussion N: {topic}]({путь к Discussion})**
  Статус: WAITING | Затрагивает: {области из Design}
  Design: [{design-id}]({путь к Design})
```

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

Добавить строку `ADR:` к существующей записи:

```markdown
- **[Discussion N: {topic}]({путь})**
  Статус: WAITING | Затрагивает: {области}
  Design: [{design-id}]({путь})
  ADR: [{adr-id}]({путь к ADR})
```

При нескольких ADR в одном Design — добавляются все:
```markdown
  ADR: [{adr-1}]({путь}), [{adr-2}]({путь})
```

---

### Сценарий C: ADR DONE, stub to full

**Триггер:** ADR → DONE, файл `services/{svc}.md` является **stub** (нет `created-by` в frontmatter).

**Это ключевой сценарий:** stub заполняется полным содержанием из дельты ADR.

**Шаги:**

#### Шаг C1: Прочитать ADR

1. Найти дельта-блоки ADR (ADDED/MODIFIED/REMOVED)
2. Извлечь данные для секций 1-6

#### Шаг C2: Обновить frontmatter

Добавить поля, отсутствующие в stub:

```yaml
---
description: Архитектура сервиса {service} — {назначение}.
service: {service}
created-by: {adr-id}
last-updated-by: {adr-id}
---
```

**SSOT frontmatter:** [standard-frontmatter.md § 5](/.structure/.instructions/standard-frontmatter.md#5-дополнительные-поля-для-живых-документов-архитектуры)

#### Шаг C3: Заполнить секции 1-6

Заменить placeholder `*Заполняется при ADR → DONE.*` на реальное содержание из дельты ADR:

| Секция | Источник |
|--------|----------|
| Резюме | Обновить (расширить из Design) |
| API контракты | Дельта ADR — ADDED endpoints |
| Data Model | Дельта ADR — ADDED entities |
| Code Map | Дельта ADR — Tech Stack, пакеты, точки входа |
| Внешние зависимости | Дельта ADR — зависимости от shared/ и других сервисов |
| Границы автономии LLM | Дельта ADR — три уровня |

**Формат секций:** [standard-service.md § 5](./standard-service.md#5-секции-документа-сервиса)

#### Шаг C4: Обновить Planned Changes

Убрать ссылку на ADR из записи Planned Changes (дельта применена в AS IS):

```markdown
- **[Discussion N: {topic}]({путь})**
  Статус: RUNNING | Затрагивает: {области}
  Design: [{design-id}]({путь})
```

Если все ADR в цепочке DONE — запись готова к перемещению в Changelog при Design → DONE.

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

Обновить затронутые секции `services/{svc}.md`:

| Дельта | Действие |
|--------|----------|
| ADDED | Добавить новые элементы в таблицы/списки |
| MODIFIED | Обновить существующие записи |
| REMOVED | Удалить элементы |

**Не менять секции, не затронутые дельтой.**

#### Шаг D3: Обновить frontmatter

```yaml
last-updated-by: {adr-id}
```

#### Шаг D4: Обновить Planned Changes

Убрать ссылку на этот ADR из записи Planned Changes (дельта применена).

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

#### Шаг E2: Переместить в Changelog

**Удалить** запись из `## Planned Changes` и **добавить** в начало `## Changelog`:

```markdown
## Changelog

- **[disc-NNNN: {topic}]({путь})** | DONE {дата}
  Design: [{design-id}]({путь}) | ADR: [{adr-1}]({путь}), [{adr-2}]({путь})
  Затрагивало: {области из Design}
```

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

#### Шаг F1: Переместить в Changelog с маркером REJECTED

**Удалить** запись из `## Planned Changes` и **добавить** в начало `## Changelog`:

```markdown
- **[disc-NNNN: {topic}]({путь})** | REJECTED {дата}
  Design: [{design-id}]({путь}) | ADR: [{adr-1}]({путь})
  Затрагивало: {области}
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
- [ ] Запись Planned Changes добавлена (формат § 5.7)
- [ ] Валидация пройдена

### Обновление — Сценарий B (ADR → WAITING)
- [ ] ADR в статусе WAITING
- [ ] Запись Planned Changes для этого Design найдена в `services/{svc}.md`
- [ ] Строка `ADR:` добавлена к записи (ссылка на ADR)
- [ ] Валидация пройдена

### Обновление — Сценарий C (ADR → DONE, stub → full)
- [ ] ADR в статусе DONE
- [ ] Файл — stub (нет `created-by`)
- [ ] Frontmatter: добавлены `created-by`, `last-updated-by`
- [ ] Все секции 1-6 заполнены (нет placeholder)
- [ ] Planned Changes: ссылка на ADR убрана
- [ ] `services/README.md`: колонки заполнены
- [ ] Валидация в full-режиме пройдена

### Обновление — Сценарий D (ADR → DONE, последующий)
- [ ] ADR в статусе DONE
- [ ] Файл — full (есть `created-by`)
- [ ] Дельта применена к затронутым секциям
- [ ] `last-updated-by` обновлён
- [ ] Planned Changes: ссылка на ADR убрана
- [ ] `services/README.md` обновлён
- [ ] Валидация пройдена

### Обновление — Сценарий E (Design → DONE)
- [ ] Все ADR цепочки в DONE
- [ ] Запись перемещена из Planned Changes в Changelog
- [ ] Формат Changelog: маркер DONE + дата
- [ ] system/ и domains/ обновлены аналогично
- [ ] Валидация пройдена

### Обновление — Сценарий F (REJECTED)
- [ ] Запись перемещена из Planned Changes в Changelog с маркером REJECTED
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

### ADR → DONE (stub → full) — сервис auth

```bash
# 1. ADR adr-0001 → DONE для auth (stub → full)

# 2. Обновить frontmatter — добавить created-by, last-updated-by
# specs/architecture/services/auth.md

# 3. Заполнить секции 1-6 из дельты ADR

# 4. Обновить Planned Changes — убрать ссылку на adr-0001

# 5. Обновить services/README.md — заполнить колонки

# 6. Валидация
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/auth.md --verbose
```

### Design → DONE — перемещение в Changelog

```bash
# 1. Design design-0001 → DONE (все ADR завершены)

# 2. Переместить запись из Planned Changes в Changelog:
#    - **[disc-0001: OAuth2 авторизация](...) ** | DONE 2026-02-15
#      Design: [design-0001](...) | ADR: [adr-0001](...), [adr-0002](...)
#      Затрагивало: Создание сервиса

# 3. Проверить полноту — все ADR DONE, AS IS секции содержат изменения

# 4. Обновить system/ и domains/ аналогично

# 5. Валидация
python specs/.instructions/.scripts/validate-service.py specs/architecture/services/auth.md --verbose
python specs/.instructions/.scripts/validate-architecture.py --check-services --verbose
```

---

## Скрипты

| Скрипт | Назначение | Путь |
|--------|------------|------|
| `validate-service.py` | Валидация `services/{svc}.md` (full/stub) | [specs/.instructions/.scripts/validate-service.py](../../.scripts/validate-service.py) |
| `validate-architecture.py` | Валидация фиксированных файлов | [specs/.instructions/.scripts/validate-architecture.py](../../.scripts/validate-architecture.py) |

---

## Скиллы

| Скилл | Назначение | Путь |
|-------|------------|------|
| `/service-modify` | Изменение `services/{svc}.md` по событию SDD | [.claude/skills/service-modify/SKILL.md](/.claude/skills/service-modify/SKILL.md) |
