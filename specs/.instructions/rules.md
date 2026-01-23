---
type: standard
description: Правила работы с /specs/ — скиллы, шаблоны, запреты
governed-by: specs/README.md
related:
  - specs/statuses.md
  - specs/workflow.md
  - specs/discussions.md
  - specs/impact.md
  - specs/adr.md
  - specs/plans.md
---

# Правила работы с /specs/

Правила автоматизации, скиллы, шаблоны и запреты для работы с документами `/specs/`.

**Индекс:** [/.claude/.instructions/README.md](/.claude/.instructions/README.md) | **Папка:** [specs/README.md](./README.md)

## Оглавление

- [Скиллы автоматизации](#скиллы-автоматизации)
- [Шаблоны](#шаблоны)
- [Запрет миграции](#запрет-миграции)
- [Запрет удаления](#запрет-удаления)
- [Запрет архивирования](#запрет-архивирования)
- [Принятые решения](#принятые-решения)
- [Связанные инструкции](#связанные-инструкции)

---

## Скиллы автоматизации

> **Правило:** Все изменения в `/specs/` выполняются ТОЛЬКО через скиллы.

### Три универсальных скилла

| Скилл | Назначение |
|-------|------------|
| [/spec-create](/.claude/skills/spec-create/SKILL.md) `<type> [parent] [options]` | Создание документов |
| [/spec-status](/.claude/skills/spec-status/SKILL.md) `<path> <status>` | Изменение статуса |
| [/spec-update](/.claude/skills/spec-update/SKILL.md) `<path>` | Работа с документом (редактирование, валидация, переход) |

> **Тип документа определяется автоматически** по пути. Один скилл вместо четырёх.

### /spec-create — создание документов

```
/spec-create discussion "Auth Strategy"
/spec-create impact 001-auth-strategy
/spec-create adr 001-auth-strategy auth
/spec-create plan auth/002-jwt-tokens
```

| Тип | Parent | Результат |
|-----|--------|-----------|
| `discussion` | — | `/specs/discussions/NNN-{topic}.md` |
| `impact` | discussion ID | `/specs/impact/NNN-{topic}.md` |
| `adr` | impact ID + service | `/specs/services/{service}/adr/NNN-{topic}.md` |
| `plan` | adr path | `/specs/services/{service}/plans/{topic}-plan.md` |

### /spec-status — изменение статуса

```
/spec-status discussions/001 review
/spec-status impact/002 approved
/spec-status auth/adr/003 done
/spec-status auth/plans/jwt-migration rejected
```

**Каскадные переходы выполняются автоматически:**

| Переход | Каскад |
|---------|--------|
| Plan → APPROVED | ADR → RUNNING, Impact → RUNNING |
| Plan → RUNNING | Discussion → RUNNING (если первый план) |
| Plan → DONE | ADR → DONE → Impact → DONE → Discussion → DONE |

### /spec-update — работа с документом

> **Основной скилл** для редактирования документов. Вызывает `/spec-status` при переходе по workflow.

**Способы начать работу с документом:**

```
/spec-update discussions/001          # Явный вызов скилла
/spec-update /specs/impact/002.md     # Полный путь
"поработаем с дискуссией 001"         # Естественный язык
"открой ADR auth/003"                 # Естественный язык
```

#### Режим валидации (--validate)

При указании флага `--validate` скилл выполняет ТОЛЬКО проверку документа без интерактивного редактирования:
1. Найти документ
2. Прочитать метаданные
3. Показать результат валидации (см. [output.md#режим-валидации](./output.md#режим-валидации))

**Триггеры перехода:**

| Фраза пользователя | Действие LLM |
|--------------------|--------------|
| "пошли дальше", "готово", "закончили" | Проверить чек-лист → вызвать `-status` |
| "отложим", "потом" | Сохранить прогресс, не менять статус |
| "отклонить", "не нужно" | Предложить перевод в REJECTED |

### Служебные скиллы

| Скилл | Назначение |
|-------|------------|
| [/specs-health](/.claude/skills/specs-health/SKILL.md) | Проверить целостность: статусы, ссылки, "застрявшие" документы |
| [/specs-sync](/.claude/skills/specs-sync/SKILL.md) | Синхронизировать каскадные статусы (пересчитать все зависимости) |
| [/specs-index](/.claude/skills/specs-index/SKILL.md) | Обновить все README.md индексы в /specs/ |

### Проверки /specs-health

| Проблема | Описание | Рекомендация |
|----------|----------|--------------|
| **Orphan Discussion** | Discussion в APPROVED без Impact >7 дней | Создать Impact или перевести в REJECTED |
| **Orphan Impact** | Impact в REVIEW без ADR >7 дней | Создать ADR или перевести в REJECTED |
| **Stuck ADR** | ADR в APPROVED без Plan >14 дней | Создать Plan или объяснить причину |
| **Stuck Plan** | Plan в RUNNING с закрытыми Issues | Перевести в DONE |
| **Inconsistent status** | Дочерние документы завершены, родитель нет | Обновить статус родителя |
| **Broken links** | Ссылки на несуществующие документы | Исправить или удалить ссылки |
| **Missing backlinks** | Родитель не ссылается на дочерний документ | Добавить обратную ссылку |
| **Service without specs** | Сервис в /src/ без папки в /specs/services/ | Создать ADR для "легализации" |

### Workflow через скиллы

```
/spec-create discussion "Auth Strategy"
    ↓
/spec-status discussions/001 review
    ↓
/spec-status discussions/001 approved
    ↓
/spec-create impact 001-auth-strategy
    ↓
/spec-status impact/001 review
    ↓
/spec-create adr 001-auth-strategy auth
    ↓
/spec-status auth/adr/001 review
    ↓
/spec-status auth/adr/001 approved
    ↓  (когда все ADR approved → impact автоматически approved)
/spec-create plan auth/001-jwt-tokens
    ↓
/spec-status auth/plans/jwt-migration approved
    ↓  (ADR/Impact → RUNNING)
/spec-status auth/plans/jwt-migration running
    ↓  (Discussion → RUNNING)
/spec-status auth/plans/jwt-migration done
    ↓  (каскад: ADR → DONE → Impact → DONE → Discussion → DONE)
```

---

## Шаблоны

Шаблоны для создания документов `/spec-create`:

| Шаблон | Файл | Описание |
|--------|------|----------|
| Discussion | [/.claude/templates/specs/discussion.md](/.claude/templates/specs/discussion.md) | Дискуссия/исследование |
| Impact | [/.claude/templates/specs/impact.md](/.claude/templates/specs/impact.md) | Анализ влияния на систему |
| ADR | [/.claude/templates/specs/adr.md](/.claude/templates/specs/adr.md) | Архитектурное решение |
| Plan | [/.claude/templates/specs/plan.md](/.claude/templates/specs/plan.md) | План реализации |
| Architecture | [/.claude/templates/specs/architecture.md](/.claude/templates/specs/architecture.md) | Архитектура сервиса |

> **Правило:** Скилл `/spec-create` использует эти шаблоны для создания документов.

> **Примеры:** Каждый шаблон содержит пример заполнения в конце файла (в HTML-комментарии `<!-- Пример -->`).

---

## Запрет миграции

> **ПРАВИЛО:** Миграция существующих документов в новую структуру ЗАПРЕЩЕНА.

### Обоснование

- Старые документы сохраняются в git history
- Новая структура применяется только для новых документов
- Избегаем сложной логики маппинга старое ↔ новое
- Контекст старых решений остаётся в истории

### Что делать со старыми документами

| Ситуация | Действие |
|----------|----------|
| Нужна информация из старого документа | Найти в git history |
| Старое решение актуально | Создать новый ADR со ссылкой на историю |
| Старое решение устарело | Игнорировать, создать новое |

### Исключения

Если пользователь явно просит миграцию конкретного документа:
1. Создать новый документ по шаблону
2. Перенести релевантный контент вручную
3. Старый документ НЕ удалять (остаётся в истории)

---

## Запрет удаления

> **ПРАВИЛО:** Физическое удаление документов из `/specs/` ЗАПРЕЩЕНО.

### Вместо удаления — статус

| Ситуация | Действие |
|----------|----------|
| Документ неактуален | Перевести в ❌ REJECTED с указанием причины |
| Документ заменён новым | Перевести в 🚫 SUPERSEDED со ссылкой на замену |
| Ошибочно создан | Перевести в ❌ REJECTED с причиной "Создан ошибочно" |

### Обоснование

- Git history сохраняет контекст принятых решений
- Ссылки из других документов остаются рабочими
- Можно понять "почему так решили" даже для отклонённых идей

### Workflow "удаления"

```
Документ нужно "удалить"
    │
    ├── Заменён новым? → /spec-status <id> superseded <new-id>
    │
    └── Просто неактуален? → /spec-status <id> rejected
                              └── Указать причину в документе
```

---

## Запрет архивирования

> **ПРАВИЛО:** Архивирование документов (перенос в `/archive/` и т.п.) ЗАПРЕЩЕНО.

### Обоснование

- Архивирование создаёт "мёртвый код" в документации
- Ломает ссылки между документами
- Усложняет поиск и навигацию
- Git history уже является архивом

### Вместо архивирования

| Ситуация | Действие |
|----------|----------|
| Старый документ | Оставить на месте со статусом DONE/SUPERSEDED |
| Устаревшая информация | Обновить документ или создать новый |
| "Слишком много документов" | Использовать фильтрацию по статусам в README |

### Фильтрация в README индексах

README.md индексы группируют документы по статусам, что позволяет легко найти актуальные:

```markdown
## По статусам

### 🔍 REVIEW (активные)
- [003-new-feature](003-new-feature.md)

### ✅ DONE (завершённые)
- [001-initial](001-initial.md)
- [002-auth](002-auth.md)

### 🚫 SUPERSEDED (заменённые)
- [001-old-approach](001-old-approach.md) → заменён [003-new-feature](003-new-feature.md)
```

---

## Принятые решения

Ключевые решения по организации `/specs/`.

| Вопрос | Решение |
|--------|---------|
| Название папки спецификаций | `/specs` |
| Где хранить глоссарий | `/specs/glossary.md` |
| Где хранить дискуссии | `/specs/discussions/` (только общий уровень) |
| Где хранить импакт-анализ | `/specs/impact/` (только общий уровень) |
| Структура | Двухуровневая: общее + по сервисам |
| ADR и архитектура | Только по сервисам |
| Формат названий | Порядковые номера: `001-topic.md` |
| README.md в папках | Индексные файлы с навигацией и статусами |
| ADR → Impact | Обязательная ссылка на родительский Impact |
| Impact → ADR | Один Impact может создать несколько ADR |

---

## Связанные инструкции

- [statuses.md](./statuses.md) — система статусов документов
- [workflow.md](./workflow.md) — полный workflow от идеи до реализации
- [discussions.md](./discussions.md) — дискуссии
- [impact.md](./impact.md) — импакт-анализ
- [adr.md](./adr.md) — ADR
- [plans.md](./plans.md) — планы реализации

