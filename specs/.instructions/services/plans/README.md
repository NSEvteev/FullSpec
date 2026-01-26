---
description: Планы реализации — декомпозиция ADR на задачи с GitHub Issues
standard: .instructions/standard-instruction.md
index: specs/.instructions/services/plans/README.md
---

# Планы /specs/services/{service}/plans/

План — декомпозиция ADR на конкретные задачи. Создаётся после APPROVED ADR, требует согласования с пользователем.

**Полезные ссылки:**
- [Инструкции для /specs/](../../README.md)

## Оглавление

- [Расположение](#расположение)
- [Формат документа](#формат-документа)
- [Статусы Plan](#статусы-plan)
- [Согласование с пользователем](#согласование-с-пользователем)
- [Автоматическое создание GitHub Issues](#автоматическое-создание-github-issues)
- [Версионирование планов](#версионирование-планов)
- [Критерий готовности](#критерий-готовности)
- [Чек-листы переходов](#чек-листы-переходов)
- [Связанные инструкции](#связанные-инструкции)

---

## Расположение

```
/specs/services/{service}/plans/
├── README.md              # ИНДЕКС: список планов, статусы
└── {topic}-plan.md        # Формат: jwt-migration-plan.md
```

---

## Формат документа

> **Шаблон:** [/.claude/templates/specs/plan.md](/.claude/templates/specs/plan.md)

Шаблон и пример заполнения находятся в файле шаблона.

### Формат README.md

```markdown
# Планы — {Service}

## Все планы

| План | ADR | Статус | Дата |
|------|-----|--------|------|
| [jwt-migration](jwt-migration-plan.md) | [002-jwt-tokens](../adr/002-jwt-tokens.md) | 🆗 APPROVED | 2025-01-21 |
| [redis-cache](redis-cache-plan.md) | [003-redis-cache](../adr/003-redis-cache.md) | 📝 DRAFT | 2025-01-22 |

## По статусам

### 📝 DRAFT
- [redis-cache](redis-cache-plan.md) — ждёт согласования

### 🆗 APPROVED
- [jwt-migration](jwt-migration-plan.md) — готов к выполнению
```

---

## Статусы Plan

| Статус | Значение |
|--------|----------|
| 📝 `DRAFT` | Черновик плана |
| 🔍 `REVIEW` | На согласовании с пользователем |
| 🆗 `APPROVED` | Согласован, готов к выполнению |
| ⏳ `RUNNING` | В работе |
| ✅ `DONE` | Выполнен |
| ❌ `REJECTED` | План отклонён |
| 🚫 `SUPERSEDED` | Заменён новым планом |

---

## Согласование с пользователем

**ВАЖНО:** План должен быть согласован с пользователем перед началом реализации.

### Workflow согласования

```
Plan создан (DRAFT)
    │
    ▼
Claude: "План готов к согласованию. Хотите внести изменения?"
    │
    ├── Пользователь: "Да, добавь..." → Обновить план → DRAFT
    │
    └── Пользователь: "Нет, всё ок" → Plan → APPROVED
                                      │
                                      ▼
                                ADR → RUNNING
                                Impact → RUNNING
```

---

## Автоматическое создание GitHub Issues

### Правило

При переходе Plan → RUNNING скилл `/spec-status {service}/plans/ <id> running` **автоматически создаёт GitHub Issues** для всех задач плана.

### Workflow

```
/spec-status {service}/plans/ jwt-migration running
    │
    ▼
Скилл читает секцию "Задачи" из плана
    │
    ▼
Для каждой задачи создаёт GitHub Issue:
  - Title: [SERVICE] Задача из плана
  - Body: Ссылка на план, описание задачи
  - Labels: service:{service}, plan:{plan-name}
    │
    ▼
Обновляет секцию "GitHub Issues" в плане
    │
    ▼
Plan → ⏳ RUNNING
```

### Формат создаваемых Issues

```markdown
## [AUTH] Создать миграцию для таблицы refresh_tokens

**План:** [jwt-migration-plan](/specs/services/auth/plans/jwt-migration-plan.md)
**ADR:** [002-jwt-tokens](/specs/services/auth/adr/002-jwt-tokens.md)
**Фаза:** 1. База данных

### Описание задачи

Создать миграцию для таблицы `refresh_tokens`

### Критерии готовности

- [ ] Миграция создана
- [ ] Миграция применена на dev
- [ ] Тесты проходят
```

### Связь Issue ↔ Plan

| В Plan | В Issue |
|--------|---------|
| Ссылка на Issue | Ссылка на Plan |
| Статус Issue | Labels: plan:{name} |
| Фаза задачи | Указана в body |

### Закрытие Issues

При закрытии всех Issues плана:
- Скилл `/spec-status {service}/plans/ <id> done` проверяет, что все Issues закрыты
- Если да → Plan → DONE
- Если нет → ошибка с указанием открытых Issues

---

## Версионирование планов

### Правило

При отклонении плана (Plan → REJECTED) и создании нового плана для того же ADR используется суффикс версии.

### Формат имени

```
{topic}-plan.md      # Первая версия
{topic}-plan-v2.md   # После отклонения первой
{topic}-plan-v3.md   # После отклонения второй
```

### Пример

```
jwt-migration-plan.md      # ❌ REJECTED — слишком сложный
jwt-migration-plan-v2.md   # 🆗 APPROVED — упрощённый вариант
```

### Workflow

```
Plan "jwt-migration-plan.md" (🔍 REVIEW)
    │
    ▼
Пользователь: "Слишком сложно, нужен другой подход"
    │
    ▼
/spec-status {service}/plans/ jwt-migration rejected
    │
    └── Plan → ❌ REJECTED
        ADR остаётся в 🆗 APPROVED
    │
    ▼
/spec-create plan auth/002-jwt-tokens
    │
    └── Создаёт "jwt-migration-plan-v2.md" (📝 DRAFT)
```

### Связь версий

В новом плане указать ссылку на предыдущую версию:

```markdown
## Метаданные

| Поле | Значение |
|------|----------|
| **Статус** | 📝 DRAFT |
| **ADR** | [002-jwt-tokens](../adr/002-jwt-tokens.md) |
| **Предыдущий план** | [jwt-migration-plan](jwt-migration-plan.md) ❌ REJECTED |
```

### Правило: один активный Plan на ADR

**Один ADR = один активный Plan.** Не может быть двух планов в статусах DRAFT/REVIEW/APPROVED/RUNNING для одного ADR одновременно.

Если ADR расширяется (появляются новые требования):
1. Текущий Plan → SUPERSEDED
2. Создаётся Plan v2 с учётом изменений

```
ADR 002-jwt-tokens (⏳ RUNNING)
    │
    ├── jwt-migration-plan.md (❌ REJECTED) — отклонён
    └── jwt-migration-plan-v2.md (⏳ RUNNING) — активный
```

> **Ошибка:** Нельзя создать jwt-migration-plan-v3.md, пока v2 не завершён или не отклонён.

---

## Критерий готовности

**Правило:** План переходит в статус ✅ DONE, когда все связанные GitHub Issues закрыты.

```
Plan (⏳ RUNNING)
    │
    ▼
Проверка: Все GitHub Issues закрыты?
    │
    ├── ДА → Plan → ✅ DONE
    │         ADR → ✅ DONE (если все планы DONE)
    │
    └── НЕТ → Остаётся ⏳ RUNNING
```

---

## Чек-листы переходов

> **Правило:** Все изменения статусов выполняются ТОЛЬКО через скиллы.

### 📝 DRAFT → 🔍 REVIEW

| | |
|---|---|
| **Скилл** | `/spec-status {service}/plans/ <id> review` |
| **Когда** | План готов к согласованию |

**Чек-лист (проверяется скиллом):**
- [ ] Указана ссылка на родительский ADR
- [ ] Задачи разбиты по фазам
- [ ] Указаны зависимости между задачами
- [ ] Указана оценка сложности

**Каскадные действия:** нет

---

### 🔍 REVIEW → 🆗 APPROVED

| | |
|---|---|
| **Скилл** | `/spec-status {service}/plans/ <id> approved` |
| **Когда** | Пользователь согласовал план |

**Чек-лист (проверяется скиллом):**
- [ ] Пользователь просмотрел план
- [ ] Пользователь подтвердил согласие (явно)
- [ ] Все вопросы по плану разрешены

**Каскадные действия:**
- Проверяет: все ли планы Impact в APPROVED?
- Если да → ADR → RUNNING, Impact → RUNNING

---

### 🆗 APPROVED → ⏳ RUNNING

| | |
|---|---|
| **Скилл** | `/spec-status {service}/plans/ <id> running` |
| **Когда** | Началась реализация задач |

**Чек-лист (проверяется скиллом):**
- [ ] Создан первый GitHub Issue для задач плана
- [ ] Начата работа над первой задачей

**Каскадные действия:**
- Добавляет ссылки на GitHub Issues в секцию документа
- **Если это первый RUNNING план:** Discussion → RUNNING

---

### ⏳ RUNNING → ✅ DONE

| | |
|---|---|
| **Скилл** | `/spec-status {service}/plans/ <id> done` |
| **Когда** | Все задачи выполнены |

**Чек-лист (проверяется скиллом):**
- [ ] ВСЕ GitHub Issues из секции "GitHub Issues" закрыты
- [ ] Все задачи в документе отмечены как выполненные

**Каскадные действия:**
- Предлагает выполнить `/spec-status {service}/adr/ <adr-id> done`

---

### 🔍 REVIEW → ❌ REJECTED

| | |
|---|---|
| **Скилл** | `/spec-status {service}/plans/ <id> rejected` |
| **Когда** | План не согласован, нужен другой подход |

**Чек-лист (проверяется скиллом):**
- [ ] Указана причина отклонения

**Каскадные действия:**
- ADR → APPROVED (если был в RUNNING)
- Скилл предлагает `/spec-create plan <adr-id>` — создать новый план

---

## Связанные инструкции

- [statuses.md](./statuses.md) — система статусов документов
- [workflow.md](./workflow.md) — полный workflow от идеи до реализации
- [adr.md](./adr.md) — ADR (предыдущий шаг)
- [architecture.md](./architecture.md) — обновление архитектуры при завершении

