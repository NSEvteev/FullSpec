---
description: Воркфлоу изменения GitHub Issue — обновление описания, меток, milestone, статуса, закрытие и переоткрытие.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/issues/README.md
---

# Воркфлоу изменения Issue

Рабочая версия стандарта: 1.7

Процессы обновления, закрытия и переоткрытия GitHub Issue.

**Полезные ссылки:**
- [Инструкции Issues](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-issue.md](./standard-issue.md) |
| Валидация | [validation-issue.md](./validation-issue.md) |
| Создание | [create-issue.md](./create-issue.md) |
| Модификация | Этот документ |

## Оглавление

- [Типы изменений](#типы-изменений)
- [Обновление](#обновление)
  - [Шаг 1: Найти Issue](#шаг-1-найти-issue)
  - [Шаг 2: Внести изменения](#шаг-2-внести-изменения)
  - [Шаг 3: Валидация](#шаг-3-валидация)
- [Закрытие](#закрытие)
  - [Шаг 1: Определить тип закрытия](#шаг-1-определить-тип-закрытия)
  - [Шаг 2: Закрыть через PR (completed)](#шаг-2-закрыть-через-pr-completed)
  - [Шаг 3: Закрыть вручную (not planned)](#шаг-3-закрыть-вручную-not-planned)
- [Переоткрытие](#переоткрытие)
  - [Шаг 1: Проверить причину переоткрытия](#шаг-1-проверить-причину-переоткрытия)
  - [Шаг 2: Переоткрыть Issue](#шаг-2-переоткрыть-issue)
  - [Шаг 3: Обновить метаданные](#шаг-3-обновить-метаданные)
- [Обновление ссылок](#обновление-ссылок)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Типы изменений

| Тип | Описание | Пример |
|-----|----------|--------|
| Обновление | Изменение title, body, labels, assignees, milestone | Уточнить title, добавить метку, назначить milestone |
| Закрытие | Завершение Issue через PR или вручную | PR смержен → auto-close, дубликат → not planned |
| Переоткрытие | Возврат закрытого Issue в работу | Закрыт по ошибке, задача не выполнена |

---

## Обновление

### Шаг 1: Найти Issue

```bash
# По номеру
gh issue view 123

# По ключевому слову
gh issue list --search "авторизация" --state open

# По milestone
gh issue list --milestone "v1.0.0" --state open
```

### Шаг 2: Внести изменения

**Изменение title:**

**SSOT:** [standard-issue.md § 4 Title](./standard-issue.md#title-правила-именования)

```bash
gh issue edit 123 --title "Новый заголовок задачи с глаголом в инфинитиве"
```

> **Важно:** Новый title должен соответствовать правилам: глагол в инфинитиве, заглавная буква, 50-70 символов, без префиксов типа.

**Изменение body:**

**SSOT:** [standard-issue.md § 4 Body](./standard-issue.md#body-структура-описания)

```bash
gh issue edit 123 --body "## Описание задачи

Обновлённое описание задачи. 2-3 предложения ЧТО и ЗАЧЕМ.

**Сервис:** api-gateway

## Документы для изучения

| # | Документ | Путь | Описание | Что искать |
|---|----------|------|----------|-----------|
| 1 | Конвенции API | specs/docs/.system/conventions.md | Конвенции API и shared-интерфейсов | Формат ошибок |
| 2 | Сервисная документация | specs/docs/api-gateway.md | Per-service документация api-gateway | Code Map |

## Задание

1. **Обнови** обработчик в src/.../routes.ts — описание.
2. **Напиши тест** — покрыть сценарий.

## Критерии готовности

- [ ] Обновлённый критерий 1
- [ ] Обновлённый критерий 2

## Практический контекст

**Как запустить:** make dev
**Как проверить:** cd src/api-gateway && npm test"
```

> **Важно:** При изменении body сохранять все 5 обязательных секций: "Описание задачи", "Документы для изучения", "Задание", "Критерии готовности", "Практический контекст".

**Добавление зависимостей:**

```bash
# Получить текущий body
gh issue view 123 --json body -q '.body'

# Добавить зависимость в body (после секции "Описание")
# Формат: **Зависит от:** #N, #M
```

**Изменение labels:**

**SSOT:** [standard-issue.md § 4 Labels](./standard-issue.md#labels-обязательные-метки)

```bash
# Добавить метку
gh issue edit 123 --add-label critical

# Удалить метку
gh issue edit 123 --remove-label medium

# Заменить приоритет (удалить старый, добавить новый)
gh issue edit 123 --remove-label medium --add-label high
```

> **Важно:** После изменения labels должны оставаться: ровно 1 метка типа и ровно 1 метка приоритета.

**Изменение assignees:**

**SSOT:** [standard-issue.md § 4 Assignees](./standard-issue.md#assignees-назначение)

```bash
# Добавить assignee
gh issue edit 123 --add-assignee user1

# Самоназначение
gh issue edit 123 --add-assignee @me

# Удалить assignee
gh issue edit 123 --remove-assignee user1
```

> **Важно:** Максимум 3 assignees. Если больше — декомпозировать задачу.

**Изменение milestone:**

**SSOT:** [standard-issue.md § 9](./standard-issue.md#9-связь-с-milestones)

```bash
# Назначить milestone
gh issue edit 123 --milestone "v1.0.0"

# Перенести в другой milestone
gh issue edit 123 --milestone "v1.1.0"

# Убрать из milestone (НЕ РЕКОМЕНДУЕТСЯ — milestone обязателен)
gh issue edit 123 --milestone ""
```

> **Важно:** Issue ДОЛЖЕН быть привязан к Milestone. Убирать milestone допустимо только при переносе — сразу назначить новый.

### Шаг 3: Валидация

**ОБЯЗАТЕЛЬНО** после любого изменения:

```bash
python .github/.instructions/.scripts/validate-issue.py 123
```

Или через скилл: `/issue-validate 123`

---

## Закрытие

**SSOT:** [standard-issue.md § 6](./standard-issue.md#6-закрытие-issue)

### Шаг 1: Определить тип закрытия

| Тип | Когда | Как |
|-----|-------|-----|
| Через PR (completed) | Задача выполнена, есть PR | Автоматически при мерже PR с `Fixes #N` |
| Вручную (not planned) | Дубликат, не актуален, ошибка | `gh issue close` с `--reason "not planned"` |

> **ЗАПРЕТ:** Ручное закрытие с reason `completed` **ЗАПРЕЩЕНО**. Если задача выполнена — должен быть PR.

### Шаг 2: Закрыть через PR (completed)

**SSOT:** [standard-pull-request.md](../pull-requests/standard-pull-request.md)

1. Создать PR с ключевым словом в body:
   ```
   Fixes #123
   ```

2. После ревью и мержа PR — Issue закроется автоматически с reason `completed`.

3. Проверить закрытие:
   ```bash
   gh issue view 123 --json state,stateReason -q '{state: .state, reason: .stateReason}'
   ```

### Шаг 3: Закрыть вручную (not planned)

**Только для следующих случаев:**

| Причина | Комментарий |
|---------|-------------|
| Дубликат | Ссылка на оригинальный Issue |
| Больше не актуален | Объяснение почему |
| Создан по ошибке | Пояснение |

```bash
# Закрыть с комментарием (ОБЯЗАТЕЛЬНО)
gh issue close 123 --reason "not planned" --comment "Дубликат #100"
```

> **Важно:** Комментарий с причиной **ОБЯЗАТЕЛЕН** при закрытии `not planned`.

---

## Переоткрытие

### Шаг 1: Проверить причину переоткрытия

**Когда переоткрывать:**

| Причина | Пример |
|---------|--------|
| Закрыт по ошибке | Issue закрыт случайно без PR |
| Задача не выполнена | PR смержен, но критерии готовности не выполнены |
| Регрессия | Баг вернулся после фикса |

**Когда НЕ переоткрывать:**

| Ситуация | Действие |
|----------|----------|
| Новые требования | Создать новый Issue |
| Связанная, но другая задача | Создать новый Issue с ссылкой |

### Шаг 2: Переоткрыть Issue

```bash
gh issue reopen 123
```

### Шаг 3: Обновить метаданные

После переоткрытия — проверить и обновить:

```bash
# Добавить комментарий с причиной переоткрытия
gh issue comment 123 --body "Переоткрыт: критерий готовности 'тесты покрывают edge cases' не выполнен"

# Проверить milestone (может быть закрыт)
gh issue view 123 --json milestone -q '.milestone.title'

# При необходимости — перенести в актуальный milestone
gh issue edit 123 --milestone "v1.1.0"

# Валидация
python .github/.instructions/.scripts/validate-issue.py 123
```

---

## Обновление ссылок

GitHub Issues — remote-объекты, не файлы. Ссылки на Issues имеют формат `#N` и не требуют обновления при изменении Issue.

**Что может потребовать обновления:**

| Ситуация | Действие |
|----------|----------|
| Issue закрыт как дубликат | Обновить ссылки в зависимых Issues: `**Зависит от:** #100` → `**Зависит от:** #50` |
| Milestone перенесён | Issues автоматически остаются в milestone — обновление не требуется |
| Title изменён | Ссылки `#N` не зависят от title — обновление не требуется |

---

## Чек-лист

### Обновление
- [ ] Issue найден по номеру или поиску
- [ ] Изменения соответствуют стандарту (title, body, labels, assignees, milestone)
- [ ] При изменении labels: ровно 1 метка типа и 1 метка приоритета
- [ ] При изменении body: все 5 обязательных секций сохранены (Описание задачи, Документы для изучения, Задание, Критерии готовности, Практический контекст)
- [ ] При изменении milestone: Issue привязан к Milestone
- [ ] Валидация пройдена (`/issue-validate`)

### Закрытие
- [ ] Тип закрытия определён (completed/not planned)
- [ ] `completed` — только через PR с `Fixes #N`
- [ ] `not planned` — с комментарием-причиной
- [ ] Ручное закрытие с `completed` не используется
- [ ] Зависимости проверены (все `**Зависит от:**` закрыты)

### Переоткрытие
- [ ] Причина переоткрытия обоснована
- [ ] Комментарий с причиной добавлен
- [ ] Milestone актуален (не закрыт)
- [ ] Метаданные обновлены при необходимости
- [ ] Валидация пройдена (`/issue-validate`)

---

## Примеры

### Обновление title и приоритета

```bash
# Найти Issue
gh issue view 42

# Изменить title
gh issue edit 42 --title "Исправить ошибку загрузки файлов более 10 МБ"

# Повысить приоритет
gh issue edit 42 --remove-label medium --add-label critical

# Валидация
python .github/.instructions/.scripts/validate-issue.py 42
```

### Закрытие дубликата

```bash
# Закрыть как дубликат с комментарием
gh issue close 55 --reason "not planned" --comment "Дубликат #42. Задача уже описана в оригинальном Issue."

# Проверить
gh issue view 55 --json state,stateReason
```

### Перенос Issue в другой milestone

```bash
# Перенести в следующий milestone
gh issue edit 42 --milestone "v1.1.0"

# Добавить комментарий с причиной
gh issue comment 42 --body "Перенесён в v1.1.0: не успеваем в v1.0.0"

# Валидация
python .github/.instructions/.scripts/validate-issue.py 42
```

### Переоткрытие после неверного закрытия

```bash
# Переоткрыть
gh issue reopen 42

# Добавить комментарий
gh issue comment 42 --body "Переоткрыт: задача закрыта по ошибке, PR #88 не решает проблему полностью"

# Проверить milestone
gh issue view 42 --json milestone -q '.milestone'

# Валидация
python .github/.instructions/.scripts/validate-issue.py 42
```

### Массовое обновление приоритета Issues milestone

```bash
# Список Issues milestone
gh issue list --milestone "v1.0.0" --state open --json number -q '.[].number'

# Обновить приоритет для конкретного Issue
gh issue edit 42 --remove-label low --add-label high

# Массовая валидация
python .github/.instructions/.scripts/validate-issue.py --milestone "v1.0.0"
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-issue.py](../.scripts/validate-issue.py) | Валидация Issue после изменений | [validation-issue.md](./validation-issue.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/issue-modify](/.claude/skills/issue-modify/SKILL.md) | Изменение Issue по стандарту | Этот документ |
| [/issue-validate](/.claude/skills/issue-validate/SKILL.md) | Валидация Issue по стандарту | [validation-issue.md](./validation-issue.md) |
