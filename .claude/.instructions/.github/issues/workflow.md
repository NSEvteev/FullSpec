---
type: instruction
status: active
priority: required
description: Жизненный цикл GitHub Issue — состояния, переходы, скиллы
related:
  - issues/format.md
  - issues/labels.md
  - git/workflow.md
---

# Workflow Issues

Жизненный цикл Issue и управление состояниями.

## Оглавление

- [Состояния Issue](#состояния-issue)
- [Переходы между состояниями](#переходы-между-состояниями)
- [Цепочки скиллов](#цепочки-скиллов)
- [State-файл](#state-файл)
- [Ветки и PR](#ветки-и-pr)
- [Блокировки](#блокировки)
- [Workflow скиллов](#lifecycle)
  - [issue-create](#issue-create)
  - [issue-execute](#issue-execute)
  - [issue-review](#issue-review)
  - [issue-complete](#issue-complete)
  - [issue-delete](#issue-delete)
  - [issue-reopen](#issue-reopen)
  - [issue-update](#issue-update)
- [Связанные инструкции](#связанные-инструкции)

---

## Состояния Issue

### Основные состояния

| Состояние | GitHub State | Метка | Описание |
|-----------|--------------|-------|----------|
| Создан | OPEN | — | Новый Issue |
| В работе | OPEN | `in-progress` | Взят в работу |
| На ревью | OPEN | `needs-review` | Решение готово |
| Заблокирован | OPEN | `blocked` | Ожидает внешних факторов |
| Выполнен | CLOSED | — | `reason: completed` |
| Отменён | CLOSED | — | `reason: not_planned` |

### Диаграмма состояний

```
                    ┌──────────────┐
                    │   Создан     │
                    └──────┬───────┘
                           │ /issue-execute
                           ▼
┌──────────────┐    ┌──────────────┐
│ Заблокирован │◄───│  В работе    │
└──────┬───────┘    └──────┬───────┘
       │                   │ /issue-review
       │ разблокировка     ▼
       │            ┌──────────────┐
       └───────────►│  На ревью    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │ Выполнен │ │ Доработка│ │ Отменён  │
       └──────────┘ └────┬─────┘ └──────────┘
                         │
                         └──► В работе
```

---

## Переходы между состояниями

### Матрица переходов

| Из / В | В работе | На ревью | Заблокирован | Выполнен | Отменён |
|--------|----------|----------|--------------|----------|---------|
| **Создан** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **В работе** | — | ✅ | ✅ | ❌ | ✅ |
| **На ревью** | ✅ | — | ❌ | ✅ | ✅ |
| **Заблокирован** | ✅ | ❌ | — | ❌ | ✅ |
| **Выполнен** | ❌ | ❌ | ❌ | — | ❌ |
| **Отменён** | ❌ | ❌ | ❌ | ❌ | — |

### Переоткрытие закрытого Issue

```
Выполнен/Отменён → /issue-reopen → Создан → ...
```

---

## Цепочки скиллов

### Основная цепочка (happy path)

```
/issue-create
    │
    ▼
/issue-execute
    │
    ├─► [Выполнение задачи: код, тесты, документация]
    │
    ▼
/issue-review (автовызов)
    │
    ├─► Ревью пройдено?
    │       │
    │       ├─► Да → /issue-complete (автовызов)
    │       │
    │       └─► Нет → Доработка → /issue-review
    │
    ▼
[Issue закрыт]
```

### Цепочка с отменой

```
/issue-create
    │
    ▼
/issue-delete
    │
    ▼
[Issue закрыт как not_planned]
```

### Цепочка с переоткрытием

```
[Issue закрыт]
    │
    ▼
/issue-reopen
    │
    ▼
/issue-execute
    │
    ▼
...
```

---

## Скиллы и их действия

| Скилл | Переход состояния | Действия |
|-------|-------------------|----------|
| `/issue-create` | — → Создан | Создать Issue с префиксом и метками |
| `/issue-execute` | Создан → В работе | Назначить, ветка, метка `in-progress` |
| `/issue-review` | В работе → На ревью | 4-аспектное ревью, метка `needs-review` |
| `/issue-complete` | На ревью → Выполнен | Проверить PR, закрыть как `completed` |
| `/issue-delete` | * → Отменён | Закрыть как `not_planned` |
| `/issue-reopen` | Закрыт → Создан | Переоткрыть с комментарием |
| `/issue-update` | — | Изменить заголовок/метки/тело |

---

## State-файл

### Назначение

Файл `.claude/state/last-issue-run.json` хранит контекст последнего выполняемого Issue.

### Формат

```json
{
  "issue": 123,
  "title": "[AUTH] Добавить OAuth авторизацию",
  "branch": "feature/123-oauth-auth",
  "started_at": "2026-01-22T10:30:00Z",
  "status": "in_progress"
}
```

### Использование

```bash
# Флаг --last в скиллах
/issue-complete --last    # Закроет Issue из state-файла
/issue-review --last      # Проревьюит Issue из state-файла
```

### Когда обновляется

| Событие | Изменение |
|---------|-----------|
| `/issue-execute #123` | Записывает новый Issue |
| `/issue-complete #123` | Очищает state-файл |
| `/issue-delete #123` | Очищает state-файл |

---

## Ветки и PR

### Создание ветки

**Правило:** `/issue-execute` автоматически создаёт ветку.

```
/issue-execute #123
↓
git checkout -b feature/123-oauth-auth
```

### Формат имени ветки

```
feature/{issue-number}-{short-name}
```

| Issue | Заголовок | Ветка |
|-------|-----------|-------|
| #123 | [AUTH] Добавить OAuth | `feature/123-oauth-auth` |
| #45 | [NOTIFY] Исправить email | `feature/45-fix-email` |
| #200 | [PAY] Stripe интеграция | `feature/200-stripe-integration` |

### Связь Issue и PR

**Правило:** PR должен ссылаться на Issue.

```markdown
# В описании PR
Closes #123
```

**Или:**
```markdown
Fixes #123
Resolves #123
```

### Автозакрытие

При мерже PR с `Closes #123` — Issue закрывается автоматически.

---

## Блокировки

### Когда Issue заблокирован

| Причина | Действие |
|---------|----------|
| Ожидание внешнего API | Добавить `blocked`, комментарий с причиной |
| Зависит от другого Issue | Добавить `blocked`, указать `Blocked by #X` |
| Ожидание ревью | Добавить `needs-review` (не `blocked`) |

### Как пометить заблокированным

```
/issue-update #123 --add-label "blocked" --comment "Blocked by #200 (ожидаем API)"
```

### Как разблокировать

```
/issue-update #123 --remove-label "blocked" --comment "Разблокировано: API готово"
/issue-execute #123  # Продолжить работу
```

---

## Проверка статуса

### Через gh CLI

```bash
# Детали Issue
gh issue view 123 --json state,labels,assignees

# Связанные PR
gh pr list --search "closes #123"

# История событий
gh issue view 123 --comments
```

### Через скилл

```
/issue-update 123  # Покажет текущее состояние
```

---

## lifecycle

**Жизненный цикл Issue:** см. [Состояния Issue](#состояния-issue) и [Диаграмма состояний](#диаграмма-состояний).

---

## issue-create

**Детальный workflow создания Issue.**

```
Шаг 0: /environment-check github --fix
Шаг 1: Определить сервис (из параметра или контекста)
Шаг 2: Сформировать заголовок [PREFIX] {описание}
Шаг 3: Определить метки (service:*, type, priority)
Шаг 4: Сформировать тело по шаблону (Описание, Критерии готовности, Связанные файлы)
Шаг 5: Показать предпросмотр (или --auto)
Шаг 6: gh issue create --title "..." --label "..." --body "..."
Шаг 7: Вывести результат с URL
```

**Формат:** см. [format.md](./format.md)
**Метки:** см. [labels.md](./labels.md)

---

## issue-execute

**Детальный workflow взятия Issue в работу.**

```
Шаг 0: /environment-check github --fix
Шаг 1: Получить номер Issue, проверить существование
Шаг 2: Показать Issue (gh issue view), запросить подтверждение
Шаг 3: gh issue edit --add-assignee @me
Шаг 4: gh issue edit --add-label "in-progress"
Шаг 5: git checkout -b {type}/{num}-{slug}
Шаг 6: gh issue comment --body "🚀 Начал работу..."
Шаг 6.5: Сохранить состояние в .claude/state/last-issue-run.json
Шаг 7: [Выполнить задачу]
Шаг 8: Вызвать /issue-review
```

**Формат ветки:** `feature/123-oauth-auth`, `fix/45-email-bug`

---

## issue-review

**Детальный workflow ревью решения.**

```
Шаг 1: Получить контекст (gh issue view, git diff)
Шаг 2: Проверить качество кода (npm run lint, tsc --noEmit)
Шаг 3: Оценить реализацию, собрать ВСЕ предложения
Шаг 4: Проверить тесты (npm test)
Шаг 5: Проверить критерии готовности из body Issue
Шаг 6: Сформировать отчёт
Шаг 7: Применить согласованные исправления (цикл к Шагу 2)
Шаг 8: Принять решение — вызвать /issue-complete или reject
```

**Критерии ревью:**
| Аспект | Блокирует |
|--------|:---------:|
| Линтинг, типизация | ✅ |
| Оптимальность | ⚠️ |
| Тесты | ✅ |
| Критерии готовности | ✅ |

---

## issue-complete

**Детальный workflow закрытия Issue как выполненного.**

```
Шаг 1: Получить номер Issue (или --last)
Шаг 2: Проверить статус (open, in-progress)
Шаг 3: Проверить критерии готовности (все [x])
Шаг 4: Найти связанный PR, проверить CI статус
Шаг 5: gh issue comment --body "✅ Выполнено в PR #..."
Шаг 6: gh issue edit --remove-label "in-progress"
Шаг 6: gh issue close --reason completed
Шаг 7: Вызвать /docs-update
Шаг 8: Вывести результат
```

---

## issue-delete

**Детальный workflow закрытия Issue как неактуального.**

```
Шаг 0: /environment-check github --fix
Шаг 1: Получить номер Issue
Шаг 2: Показать текущее состояние (gh issue view)
Шаг 3: Определить причину (not_planned / duplicate)
Шаг 4: gh issue comment --body "Причина: ..."
Шаг 5: gh issue close --reason "not planned"
Шаг 6: Вывести результат
```

**Причины закрытия:**
- `not_planned` — неактуально, отменено
- `duplicate` — дубликат (комментарий "Дубликат #X")

---

## issue-reopen

**Детальный workflow переоткрытия закрытого Issue.**

```
Шаг 0: /environment-check github --fix, /input-validate
Шаг 1: gh issue view --json state,title,closedAt,stateReason
Шаг 2: Проверить статус (должен быть CLOSED)
Шаг 3: Показать информацию, запросить подтверждение
Шаг 4: gh issue reopen
Шаг 5: gh issue comment --body "🔄 Issue переоткрыт: {причина}"
Шаг 6: (если --assign) gh issue edit --add-assignee @me
Шаг 7: Вывести результат
```

**Когда использовать:**
- Закрыто преждевременно
- Новые требования
- Баг вернулся (регрессия)
- Решение неполное

---

## issue-update

**Детальный workflow обновления Issue.**

```
Шаг 0: /environment-check github --fix
Шаг 1: Получить номер Issue
Шаг 2: Показать текущее состояние (gh issue view)
Шаг 3: Определить изменения (из параметров или интерактивно)
Шаг 4: Применить изменения:
       - gh issue edit --title "..."
       - gh issue edit --add-label "..."
       - gh issue edit --remove-label "..."
       - gh issue edit --body "..."
       - gh issue comment --body "..."
Шаг 5: Вывести результат
```

---

## Связанные инструкции

- [format.md](./format.md) — формат Issue
- [labels.md](./labels.md) — система меток
- [commands.md](./commands.md) — команды gh
- [../git/workflow.md](../git/workflow.md) — ветки и PR

---

> **Путь:** `/.claude/.instructions/issues/workflow.md`
