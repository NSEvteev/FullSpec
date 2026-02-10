---
description: Стандарт GitHub Projects — канбан-доски, views, поля, автоматизация, интеграция с Issues и Milestones.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/README.md
---

> **ВАЖНО:** Эта инструкция не используется в проекте.
>
> Причина: команда из 2 человек — Projects не нужны (Issues + Labels + Milestones достаточно).
> Содержимое закомментировано. Для реактивации — раскомментировать.

<!--
# Стандарт GitHub Projects

Версия стандарта: 1.0

Формат и правила работы с GitHub Projects (Project v2) — канбан-доски для визуализации работы.

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [GitHub Projects documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub CLI Manual — gh project](https://cli.github.com/manual/gh_project)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-project.md](./validation-project.md) |
| Создание | [create-project.md](./create-project.md) |
| Модификация | [modify-project.md](./modify-project.md) |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Область ответственности](#2-область-ответственности)
- [3. Свойства Project](#3-свойства-project)
- [4. Views (представления)](#4-views-представления)
- [5. Fields (поля)](#5-fields-поля)
- [6. Items (элементы доски)](#6-items-элементы-доски)
- [7. Автоматизация](#7-автоматизация)
- [8. CLI команды](#8-cli-команды)
- [9. Связь с другими объектами GitHub](#9-связь-с-другими-объектами-github)
- [10. Когда использовать Projects](#10-когда-использовать-projects)
- [11. Последовательность создания проекта](#11-последовательность-создания-проекта)
- [12. Типичные ошибки CLI](#12-типичные-ошибки-cli)
- [13. Переиспользование полей](#13-переиспользование-полей)
- [14. Лимиты GitHub Projects](#14-лимиты-github-projects)
- [15. Автоматизация через GitHub Actions](#15-автоматизация-через-github-actions)

---

## 1. Назначение

**GitHub Projects (v2)** — визуализация работы в формате канбан-доски с гибкими представлениями (Board, Table) и настраиваемыми полями.

**Используется для:**
- Визуализация workflow (Backlog → In Progress → Done)
- Приоритизация задач
- Планирование спринтов
- Отслеживание прогресса команды

**НЕ используется для:**
- Основное хранилище задач (задачи живут в Issues, Project — визуализация)
- Замена Milestones (для группировки используются Milestones)
- Подробное описание задач (описание в Issue, не в Project)

---

## 2. Область ответственности

**Project покрывает:**
- Канбан-доски (Board view)
- Табличные представления (Table view)
- Кастомные поля (Priority, Status, Sprint и т.д.)
- Автоматизацию перемещения карточек
- Связь Issues/PR с досками

**Project НЕ покрывает:**
- Issues — см. [standard-issue.md](../issues/standard-issue.md)
- Pull Requests — см. [standard-pull-request.md](../pull-requests/standard-pull-request.md)
- Milestones — см. [standard-milestone.md](../milestones/standard-milestone.md)

---

## 3. Свойства Project

| Свойство | Тип | Описание | Изменяемость |
|----------|-----|----------|--------------|
| `title` | string | Название проекта | ✅ |
| `description` | string | Описание проекта | ✅ |
| `fields` | field[] | Список полей (Status, Priority, etc.) | ✅ |
| `items` | item[] | Issues/PR добавленные в проект | ✅ |
| `views` | view[] | Представления (Board, Table) | ✅ |
| `workflows` | workflow[] | Автоматизация. Поле всегда существует, может быть пустым массивом. Настройка автоматизации опциональна. | ✅ |
| `owner` | user/org | Владелец проекта (user или organization) | ❌ (при создании) |
| `visibility` | enum | public/private | ✅ |
| `closed` | bool | Архивирован ли проект | ✅ |
| `id` | int | Уникальный ID (авто) | ❌ |
| `created_at` | datetime | Дата создания (авто) | ❌ |
| `updated_at` | datetime | Дата изменения (авто) | ❌ |

---

## 4. Views (представления)

**View** — способ отображения данных проекта.

### Типы Views

| Тип | Назначение | Когда использовать |
|-----|------------|--------------------|
| **Board** | Канбан-доска с колонками | Визуализация workflow (Backlog → Done) |
| **Table** | Табличное представление | Детальный просмотр всех полей |
| **Roadmap** | Временная шкала (timeline) | Планирование на месяцы. Требует кастомное поле типа Date (например "Due Date"). Без поля Date view создаётся, но элементы не отображаются на timeline. |

### Свойства View

| Свойство | Тип | Описание |
|----------|-----|----------|
| `name` | string | Название view (например: "Current Sprint") |
| `layout` | enum | board / table / roadmap |
| `fields` | field[] | Какие поля показывать |
| `filter` | filter | Фильтр (например: `status:open`) |
| `sort` | sort | Сортировка (например: по Priority) |
| `group_by` | field | Группировка (для Board — по Status). **Важно:** поле Status ДОЛЖНО существовать ДО создания Board view с группировкой. |

### Примеры Views

| View | Layout | Group By | Filter |
|------|--------|----------|--------|
| Current Sprint | Board | Status | milestone:"Sprint 1" |
| Backlog | Table | — | status:open NOT milestone:* |
| Roadmap | Roadmap | — | — |

### Roadmap View: создание поля Date

Roadmap view требует кастомное поле типа Date. Без него элементы не отображаются на timeline.

```bash
# Создать поле Due Date
gh project field-create 1 --owner @me --name "Due Date" --data-type "DATE"
```

После создания поля — задать дату для items, и они появятся на Roadmap timeline.

---

## 5. Fields (поля)

**Field** — атрибут элемента доски (Issue/PR/Draft).

### Встроенные поля

GitHub Projects автоматически создаёт поля для Issues/PR:

| Поле | Тип | Описание | Источник |
|------|-----|----------|----------|
| `Title` | text | Заголовок | Issue/PR |
| `Assignees` | user[] | Исполнители | Issue/PR |
| `Labels` | label[] | Метки | Issue/PR |
| `Milestone` | milestone | Веха | Issue/PR |
| `Repository` | repo | Репозиторий (если проект org-level) | Issue/PR |
| `Status` | single_select | Статус (кастомное поле) | Project |

### Кастомные поля

Помимо встроенных полей, GitHub Projects позволяет создавать кастомные поля. Как минимум два кастомных поля (Status и Priority) ДОЛЖНЫ быть созданы — см. раздел "Обязательные поля".

| Тип поля | Описание | Пример |
|----------|----------|--------|
| **Text** | Одна строка текста | Notes |
| **Number** | Число | Story Points |
| **Date** | Дата | Due Date |
| **Single Select** | Выбор одного значения | Priority (High/Medium/Low) |
| **Iteration** | Спринт/итерация | Sprint 1, Sprint 2 |

### Обязательные кастомные поля (создать сразу после проекта)

Эти поля НЕ создаются автоматически. Их необходимо создать вручную через `gh project field-create` перед добавлением Items в проект.

| Поле | Тип | Значения | Назначение |
|------|-----|----------|------------|
| **Status** | Single Select | Backlog, Todo, In Progress, In Review, Done | Workflow |
| **Priority** | Single Select | Critical, High, Medium, Low | Приоритизация |

**Опциональные поля:**

| Поле | Тип | Когда добавлять |
|------|-----|-----------------|
| Sprint | Iteration | Если используются спринты |
| Story Points | Number | Если оценивается сложность |
| Due Date | Date | Если есть жёсткие дедлайны |

---

## 6. Items (элементы доски)

**Item** — элемент проекта (Issue или PR).

### Типы Items

| Тип | Описание | Когда использовать |
|-----|----------|--------------------|
| **Issue** | GitHub Issue | Основной тип — задачи, баги, фичи |
| **Pull Request** | GitHub PR | Добавляется вручную или через автоматизацию (см. "Project → Pull Requests") |

### Добавление Items

**CLI:**
```bash
gh project item-add <project-number> --owner <owner> --url <issue-url>
```

**Автоматически (требует настройки):**
- Issue может автоматически добавляться через workflow (Settings → Workflows → "Item added")
- PR автоматически НЕ добавляется по умолчанию — требуется настройка (см. раздел "Project → Pull Requests")

### Удаление Items

**Важно:** Удаление Item из проекта НЕ удаляет Issue/PR — только убирает из доски.

---

## 7. Автоматизация

**Workflows** — автоматическое изменение полей при событиях.

### Встроенная автоматизация

| Событие | Действие | Пример |
|---------|----------|--------|
| Issue opened | Установить Status = "Todo" | Новая задача → автоматически в колонку Todo |
| Issue closed | Установить Status = "Done" | Закрытая задача → автоматически в Done |
| PR merged | Установить Status = "Done" | Смёрженный PR → в Done |

### Настройка автоматизации

**Через Web UI:**
1. Открыть Project → Settings → Workflows
2. Выбрать триггер (например: "Item opened")
3. Указать действие (например: "Set Status = Todo")

**Через CLI:** В текущей версии `gh` API — автоматизация настраивается только через Web UI.

### Настройка через Web UI

**Открыть проект в браузере:**
```bash
gh project view 1 --owner @me --web
```

**Настройка автоматизации:**
1. Открыть проект → верхнее меню "..." → Settings
2. Вкладка "Workflows"
3. Выбрать триггер (например "Item opened")
4. Указать действие (например "Set Status to: Todo")
5. Сохранить

**Создание views:**
1. Открыть проект → вкладка views (иконка рядом с названием проекта)
2. "+" → New view → выбрать тип (Board/Table/Roadmap)
3. Настроить фильтры, группировку, сортировку
4. Сохранить

---

## 8. CLI команды

**SSOT:** [GitHub CLI Manual — projects](https://cli.github.com/manual/gh_project)

### Авторизация

```bash
# GitHub Projects требует scope "project"
# Выполнить один раз перед первым использованием gh project
# Если получена ошибка "insufficient OAuth scopes" — повторить команду
gh auth refresh -s project
```

### Основные команды

| Команда | Назначение |
|---------|------------|
| `gh project list` | Список проектов |
| `gh project view <number>` | Просмотр проекта |
| `gh project create` | Создание проекта |
| `gh project edit <number>` | Редактирование проекта |
| `gh project close <number>` | Архивирование проекта |
| `gh project delete <number>` | Удаление проекта (необратимо) |
| `gh project item-add` | Добавление Issue/PR в проект |
| `gh project item-list` | Список элементов проекта |
| `gh project item-edit` | Изменение полей item (Status, Priority, etc.) |
| `gh project field-list` | Список полей проекта |
| `gh project field-create` | Создание кастомного поля |

### Примеры

**Создание проекта:**
```bash
gh project create --owner @me --title "Roadmap 2026"
```

**Добавление Issue в проект:**
```bash
gh project item-add 1 --owner @me --url https://github.com/owner/repo/issues/123
```

**Просмотр полей:**
```bash
gh project field-list 1 --owner @me
```

**Создание кастомного поля Priority:**
```bash
gh project field-create 1 --owner @me --name "Priority" --data-type "SINGLE_SELECT" --single-select-options "Critical,High,Medium,Low"
```

**Открыть проект в браузере:**
```bash
gh project view 1 --owner @me --web
```

**Удаление проекта:**
```bash
gh project delete 1 --owner @me
```

**Редактирование полей item (полный скрипт):**
```bash
# Установить Status = "In Progress" для Issue #123
PROJECT=1
OWNER="@me"
ISSUE=123

ITEM_ID=$(gh project item-list $PROJECT --owner $OWNER --format json | jq -r ".items[] | select(.content.number==$ISSUE) | .id")
FIELD_ID=$(gh project field-list $PROJECT --owner $OWNER --format json | jq -r '.fields[] | select(.name=="Status") | .id')
OPTION_ID=$(gh project field-list $PROJECT --owner $OWNER --format json | jq -r '.fields[] | select(.name=="Status") | .options[] | select(.name=="In Progress") | .id')

gh project item-edit --project-id $PROJECT --id $ITEM_ID --field-id $FIELD_ID --single-select-option-id $OPTION_ID
```

**Фильтрация items:**
```bash
# Все items
gh project item-list 1 --owner @me

# Фильтрация через jq (Status="In Progress")
gh project item-list 1 --owner @me --format json | jq '.items[] | select(.fieldValues[] | select(.field.name=="Status" and .name=="In Progress"))'

# Фильтрация через jq (Priority="High")
gh project item-list 1 --owner @me --format json | jq '.items[] | select(.fieldValues[] | select(.field.name=="Priority" and .name=="High"))'
```

---

## 9. Связь с другими объектами GitHub

### Project → Issues

- **Связь:** Project содержит Issues как Items
- **Направление:** один проект → много Issues
- **Добавление:** `gh project item-add` или автоматически при создании Issue с полем `project`

### Project → Pull Requests

- **Связь:** PR может быть добавлен в проект
- **Направление:** один проект → много PR
- **Автоматика:** По умолчанию PR НЕ добавляется автоматически. Необходимо настроить workflow автоматизации в проекте (Settings → Workflows → "When pull request is linked to an issue"). Если workflow настроен — PR автоматически добавляется при связывании с Issue через `Fixes #123`.

### Project → Milestones

- **Связь:** Items (Issues) имеют поле Milestone
- **Направление:** Project фильтрует по Milestone
- **Использование:** View "Current Sprint" фильтрует `milestone:"Sprint 1"`

### Project → Labels

- **Связь:** Items (Issues) имеют поле Labels
- **Направление:** Project фильтрует/группирует по Labels
- **Использование:** Группировка по `area:*` или фильтр `high`

---

## 10. Когда использовать Projects

### Сценарии использования

| Сценарий | Использовать Project | Альтернатива |
|----------|----------------------|--------------|
| **Команда из 2 человек** | Нет | Issues + Milestones достаточно |
| **Команда 5+ человек** | Да (критично для координации) | При 5+ участниках Issues + Labels недостаточно для визуализации work-in-progress и приоритетов |
| **Спринты/итерации** | Да | Можно через Milestones, но Project удобнее |
| **Визуализация workflow** | Да | — |
| **Приоритизация backlog** | Да | Можно через Labels, но менее наглядно |
| **Roadmap на месяцы** | Да (Roadmap view) | — |

### Монорепо

Проект использует монорепо — **один Project на весь репозиторий**. При масштабировании до нескольких команд — один Project на команду.

### Текущий проект (2 человека)

**Решение:** Projects — **НЕ создавать сейчас**. Использовать Issues + Labels + Milestones.

**Причины:**
- Небольшая команда (2 человека)
- Issues + Labels + Milestones покрывают базовые потребности
- Визуализация не критична (можно просматривать Issues списком)

**Когда добавить:**
- Команда выросла до 5+ человек
- Требуется визуализация для стейкхолдеров
- Используются спринты с детальным трекингом

### Масштабирование до 10 человек

При росте команды:

1. Создать Project "Roadmap" с views:
   - Current Sprint (Board)
   - Backlog (Table)
   - Roadmap (Roadmap)

2. Добавить поля:
   - Status (Backlog, Todo, In Progress, In Review, Done)
   - Priority (Critical, High, Medium, Low)
   - Sprint (Iteration)

3. Настроить автоматизацию:
   - Issue opened → Status = "Todo"
   - Issue closed → Status = "Done"

---

## 11. Последовательность создания проекта

**Шаги создания проекта (обязательный порядок):**

1. **Авторизация с scope project:**
   ```bash
   gh auth refresh -s project
   ```

2. **Создать проект:**
   ```bash
   gh project create --owner @me --title "Roadmap"
   ```

3. **Создать кастомные поля:**
   ```bash
   # Status (обязательно)
   gh project field-create 1 --owner @me --name "Status" --data-type "SINGLE_SELECT" \
     --single-select-options "Backlog,Todo,In Progress,In Review,Done"

   # Priority (обязательно)
   gh project field-create 1 --owner @me --name "Priority" --data-type "SINGLE_SELECT" \
     --single-select-options "Critical,High,Medium,Low"
   ```

4. **Настроить views через Web UI** (CLI не поддерживает создание views):
   - Открыть проект: `gh project view 1 --owner @me --web`
   - Создать Board view с группировкой по Status
   - Создать Table view

5. **Добавить items:**
   ```bash
   gh project item-add 1 --owner @me --url https://github.com/owner/repo/issues/123
   ```

6. **Настроить автоматизацию** (опционально, через Web UI):
   - Project → Settings → Workflows

---

## 12. Типичные ошибки CLI

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `insufficient OAuth scopes` | Scope "project" не активирован | Выполнить `gh auth refresh -s project` |
| `project not found` | Неверный номер проекта или owner | Проверить номер через `gh project list` |
| `field already exists` | Поле с таким именем уже создано | Использовать существующее поле |
| `item already in project` | Item уже добавлен в проект | Проверить через `gh project item-list` |
| `could not resolve to a Project` | Проект принадлежит другому owner | Указать правильный `--owner` |

---

## 13. Переиспользование полей

**Важно:** Кастомные поля создаются ДЛЯ КОНКРЕТНОГО ПРОЕКТА. При создании второго проекта поля Status/Priority нужно создавать заново.

**Решение для нескольких проектов:**
1. Создать первый проект с полями Status/Priority
2. Использовать его как шаблон
3. GitHub Projects НЕ поддерживает копирование проектов через CLI (только через Web UI: "..." → Copy project)

**Альтернатива:** Создать скрипт для автоматического создания проекта с набором стандартных полей.

---

## 14. Лимиты GitHub Projects

| Лимит | Free | Pro/Team | Enterprise |
|-------|------|----------|------------|
| Проектов на пользователя | 100 | 100 | 1000 |
| Items в проекте | 1200 | 1200 | 5000 |
| Кастомных полей | 50 | 50 | 50 |
| Views на проект | 20 | 20 | 20 |

**Что делать при превышении лимита items:**
- Разделить проект на несколько (например, по Milestones)
- Архивировать старые items (закрытые Issues)
- Использовать фильтры views вместо добавления всех items

**SSOT:** [GitHub Projects documentation — Limits](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects#project-limits)

---

## 15. Автоматизация через GitHub Actions

Для автоматического добавления Issues в Project через GitHub Actions — см. [standard-action.md](../actions/standard-action.md).

**Альтернатива:** Встроенная автоматизация Projects (§ 7) — настраивается через Web UI без `.yml` файлов.

---
-->
