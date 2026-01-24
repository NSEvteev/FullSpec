---
type: standard
description: Связи между документами /specs/ и разделение с /doc/
governed-by: specs/README.md
related:
  - specs/workflow.md
  - specs/statuses.md
---

# Связи между документами /specs/

Граф зависимостей документов, обязательные ссылки, backlinks, и разделение ответственности между `/specs/` и `/doc/`.

> [Инструкции по работе со спецификациями](./README.md)

## Оглавление

- [Цепочка документов](#цепочка-документов)
- [Граф зависимостей](#граф-зависимостей)
- [Обязательные ссылки](#обязательные-ссылки)
- [Обратные ссылки (Backlinks)](#обратные-ссылки-backlinks)
- [Связь /specs/ ↔ /doc/](#связь-specs--doc)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Цепочка документов

```
Discussion → Impact → ADR → Plan → Implementation
```

| Этап | Документ | Назначение |
|------|----------|------------|
| 1 | Discussion | Исследование проблемы |
| 2 | Impact | Анализ затронутых сервисов |
| 3 | ADR | Архитектурное решение |
| 4 | Plan | Декомпозиция на задачи |
| 5 | Implementation | Код + документация |

---

## Граф зависимостей

```
┌─────────────────┐
│   Discussion    │
│ 001-auth-flow   │
│ status: APPROVED│
└────────┬────────┘
         │ создаёт
         ▼
┌─────────────────┐
│     Impact      │
│ 001-auth-flow   │
│ status: APPROVED│
└────────┬────────┘
         │ создаёт несколько ADR
         ├──────────────────────────────┐
         ▼                              ▼
┌─────────────────────┐    ┌─────────────────────┐
│ ADR: auth/001-jwt   │    │ ADR: gateway/001-.. │
│ impact: 001-auth    │    │ impact: 001-auth    │
│ status: APPROVED    │    │ status: APPROVED    │
└─────────┬───────────┘    └─────────┬───────────┘
          │ создаёт                   │ создаёт
          ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐
│ Plan: jwt-migration │    │ Plan: auth-gateway  │
│ adr: auth/001       │    │ adr: gateway/001    │
│ status: RUNNING     │    │ status: DRAFT       │
└─────────────────────┘    └─────────────────────┘
```

---

## Обязательные ссылки

Каждый документ **обязан** ссылаться на родителя.

| Документ | Обязательно ссылается на | Поле в метаданных |
|----------|--------------------------|-------------------|
| Impact | Discussion (родительская) | `discussion:` |
| ADR | Impact (родительский) | `impact:` |
| Plan | ADR (родительский) | `adr:` |
| Architecture раздел | ADR (который его ввёл) | Ссылка в тексте |

### Проверка ссылок

Скилл `/specs-health` проверяет:
- Все обязательные ссылки существуют
- Ссылки ведут на существующие документы
- Ссылки взаимны (backlinks)

---

## Обратные ссылки (Backlinks)

При создании дочернего документа **родительский документ автоматически обновляется**.

| Действие | Родитель | Что обновляется |
|----------|----------|-----------------|
| `/spec-create impact <discussion>` | Discussion | Секция "Связанные документы" |
| `/spec-create adr <impact> <service>` | Impact | Таблица "Затронутые сервисы" |
| `/spec-create plan <adr>` | ADR | Секция "План реализации" |

### Формат backlink в Discussion

```markdown
## Связанные документы

- Impact: [001-auth-strategy](/specs/impact/001-auth-strategy.md)
```

### Формат backlink в Impact

```markdown
## Затронутые сервисы

| Сервис | ADR | Статус |
|--------|-----|--------|
| auth | [001-jwt-tokens](/specs/services/auth/adr/001-jwt-tokens.md) | 📝 DRAFT |
| gateway | [001-auth-middleware](/specs/services/gateway/adr/001-auth-middleware.md) | 📝 DRAFT |
```

### Формат backlink в ADR

```markdown
## План реализации

- [jwt-migration-plan](/specs/services/auth/plans/jwt-migration-plan.md) — 📝 DRAFT
```

---

## Связь /specs/ ↔ /doc/

### Назначение папок

| Папка | Назначение | Что хранит | Когда обновляется |
|-------|------------|------------|-------------------|
| `/specs/` | **Проектная документация** | Решения, планы, архитектура | При принятии решений |
| `/doc/` | **Документация кода** | API, компоненты, runbooks | При изменении кода |

### Принцип разделения

```
/specs/ — "ПОЧЕМУ и ЧТО решили делать"
  └── Discussion → Impact → ADR → Plan

/doc/ — "КАК это сделано сейчас"
  └── API docs, компоненты, runbooks
```

### Структура /doc/

```
/doc/
├── README.md                         # ИНДЕКС: точка входа
├── src/                              # Зеркало /src/
│   └── {service}/
│       ├── README.md                 # ИНДЕКС: ссылки на specs
│       ├── api.md
│       └── runbooks/
├── shared/
├── platform/
└── runbooks/
```

### Синхронизация

| Событие | /specs/ | /doc/ |
|---------|---------|-------|
| ADR → DONE | architecture.md обновлён | README/api.md обновлены |
| Рефакторинг кода | Не меняется | Обновляется |
| Новое ADR | Новый документ | Не меняется (пока ADR не DONE) |

### Ссылки между папками

**В `/doc/src/{service}/README.md`:**
```markdown
## Архитектура

См. [/specs/services/{service}/architecture.md](/specs/services/{service}/architecture.md)

## Архитектурные решения

См. [/specs/services/{service}/adr/](/specs/services/{service}/adr/)
```

**В `/specs/services/{service}/architecture.md`:**
```markdown
## Документация API

См. [/doc/src/{service}/api.md](/doc/src/{service}/api.md)
```

---

## Скиллы

| Скилл | Использует |
|-------|------------|
| [/spec-create](/.claude/skills/spec-create/SKILL.md) | Создание связей, backlinks |
| [/specs-health](/.claude/skills/specs-health/SKILL.md) | Проверка связей |

---

## Связанные инструкции

- [workflow.md](./workflow.md) — полный workflow от идеи до реализации
- [statuses.md](./statuses.md) — каскадные переходы статусов
