---
description: Стандарт работы с GitHub Issues — формат заголовка, метки, milestone, описание, жизненный цикл и связи.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/issues/README.md
---

# Стандарт управления GitHub Issues

Версия стандарта: 1.4

Правила жизненного цикла, создания и управления задачами (Issues) в репозитории.

**Полезные ссылки:**
- [Инструкции Issues](./README.md)

**SSOT-зависимости:**
- [standard-labels.md](../labels/standard-labels.md) — метки Issues
- [standard-milestone.md](../milestones/standard-milestone.md) — milestones
- [standard-issue-template.md](./issue-templates/standard-issue-template.md) — шаблоны Issues
- [standard-pull-request.md](../pull-requests/standard-pull-request.md) — связь с PR
- [standard-development.md](../development/standard-development.md) — рабочий процесс (§1 взятие задачи, §6 завершение)
- [standard-branching.md](../branches/standard-branching.md) — связь NNNN ветки с Issues
- [standard-github-workflow.md](../standard-github-workflow.md) — полный цикл (стадия 1: Issue)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-issue.md](./validation-issue.md) |
| Создание | [create-issue.md](./create-issue.md) |
| Модификация | [modify-issue.md](./modify-issue.md) |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Свойства Issue](#2-свойства-issue)
- [3. Жизненный цикл](#3-жизненный-цикл)
- [4. Правила создания](#4-правила-создания)
  - [Title — правила именования](#title-правила-именования)
  - [Body — структура описания](#body-структура-описания)
  - [Labels — обязательные метки](#labels-обязательные-метки)
  - [Assignees — назначение](#assignees-назначение)
- [5. Связь с Branch и PR](#5-связь-с-branch-и-pr)
- [6. Закрытие Issue](#6-закрытие-issue)
- [7. CLI команды](#7-cli-команды)
- [8. Декомпозиция и зависимости](#8-декомпозиция-и-зависимости)
- [9. Связь с Milestones](#9-связь-с-milestones)

---

## 1. Назначение

GitHub Issues — система управления задачами, багами и техническими работами проекта.

**Применяется к:**
- Задачи разработки (рефакторинг, документация)
- Баги и проблемы
- Технические задачи

**Цель:**
- Организация работы команды
- Прозрачность планирования
- Связь задач с кодом (через PR)
- Отслеживание прогресса

**Принципы:**
- Каждая задача — отдельный Issue
- Каждый Issue имеет чёткое описание и критерии готовности
- Issue связан с Branch и PR
- Issue закрывается автоматически при мерже PR

---

## 2. Свойства Issue

**Базовые свойства:**

| Свойство | Тип | Обязательно | Описание | Как установить |
|----------|-----|-------------|----------|----------------|
| `number` | int | авто | Уникальный номер (генерируется автоматически) | — |
| `title` | string | да | Заголовок задачи | `--title` |
| `body` | markdown | да | Описание задачи | `--body` |
| `state` | enum | авто | `open` / `closed` | `gh issue close/reopen` |
| `author` | user | авто | Создатель | — |
| `created_at` | datetime | авто | Дата создания | — |

**Метаданные:**

| Свойство | Тип | Обязательно | SSOT |
|----------|-----|-------------|------|
| `labels` | label[] | да | [standard-labels.md](../labels/standard-labels.md) |
| `assignees` | user[] | опционально | См. [§4 Assignees](#assignees-назначение) |
| `milestone` | milestone | да | [standard-milestone.md](../milestones/standard-milestone.md) |

**Как установить:** `--label`, `--assignee`, `--milestone` (см. [§7 CLI команды](#7-cli-команды))

---

## 3. Жизненный цикл

```
┌─────────────┐
│   СОЗДАНИЕ  │  gh issue create
└──────┬──────┘
       │
       ├─ Заполнение: title, body, labels, assignees
       │
       v
┌─────────────┐
│  ОТКРЫТ     │  state: open
│  (READY)    │
└──────┬──────┘
       │
       ├─ Создание ветки: git checkout -b 0001-auth
       │
       v
┌─────────────┐
│  В РАБОТЕ   │  label: status:wip (опционально)
└──────┬──────┘
       │
       ├─ Разработка локально (make dev)
       │
       v
┌─────────────┐
│  PR СОЗДАН  │  gh pr create (связан через "Fixes #123")
└──────┬──────┘
       │
       ├─ Code review
       │
       v
┌─────────────┐
│  REVIEW     │  label: status:in-review (опционально)
└──────┬──────┘
       │
       ├─ Мерж PR
       │
       v
┌─────────────┐
│  ЗАКРЫТ     │  state: closed (автоматически)
└─────────────┘
```

**Ключевые этапы:**
1. **СОЗДАНИЕ** — Issue создаётся в GitHub
2. **ОТКРЫТ** — Ожидает начала работы
3. **В РАБОТЕ** — Разработка ведётся локально. **Триггер:** создана ветка `{NNNN}-{topic}` через `git checkout -b` (имя ветки = имя папки analysis chain). Метка `status:wip` опциональна — для команды ≤3 человек прозрачность обеспечивается малым размером команды.
4. **PR СОЗДАН** — Код отправлен на ревью
5. **REVIEW** — Проходит code review
6. **ЗАКРЫТ** — PR смержен, Issue автоматически закрывается

**Переходы:**
- `open` → `closed` — автоматически при мерже PR (если в PR есть `Fixes #123`)
- `closed` → `open` — вручную через `gh issue reopen` (если нужно переоткрыть)

---

## 4. Правила создания

### Title — правила именования

**Формат:**
```
{Краткое описание действия}
```

**Правила:**
- Начинать с глагола в инфинитиве (добавить, исправить, обновить)
- Длина: 50-70 символов
- Без префиксов типа (они в labels)
- Без номера Issue в title

**Примеры:**

| Корректно | Некорректно | Причина |
|-----------|-------------|---------|
| Добавить авторизацию пользователей | добавить авторизацию | Заглавная буква |
| Исправить ошибку загрузки файлов | Bug: ошибка загрузки | Префикс в title (должен быть в labels) |
| Обновить README с инструкциями по деплою | #123 Обновить README | Номер Issue не нужен в title |
| Рефакторинг модуля обработки ошибок | Рефакторинг | Неинформативно |

### Body — структура описания

**SSOT:** [standard-issue-template.md](./issue-templates/standard-issue-template.md) — структура body определяется шаблоном Issue.

**Правило:** ВСЕГДА использовать шаблон при создании Issue (кроме технических задач без структуры). Примеры шаблонов — [standard-issue-template.md § 11](./issue-templates/standard-issue-template.md#11-примеры-шаблонов).

**Минимальная структура (если без шаблона):**

```markdown
## Описание

{Что нужно сделать и зачем}

## Связанная документация

{Список файлов проекта, помогающих понять контекст задачи, ИЛИ "Связанной документации нет"}

## Критерии готовности

- [ ] {Пункт 1}
- [ ] {Пункт 2}
```

**Секция "Связанная документация" (ОБЯЗАТЕЛЬНА):**

Создатель Issue (LLM или человек) ДОЛЖЕН указать файлы проекта, которые помогут исполнителю быстро понять контекст задачи. Если релевантных документов нет — указать "Связанной документации нет".

Формат: `{описание} — {путь к файлу}`

```markdown
## Связанная документация

- Стандарт меток — `.github/.instructions/labels/standard-labels.md`
- Справочник меток — `.github/labels.yml`
```

**Опциональная строка "Сервис":**

Если Issue привязан к одному сервису — добавить строку "Сервис" со ссылкой на архитектурный документ. Если задача cross-service — не добавлять (информация в метках `svc:*`).

```markdown
**Сервис:** [auth](specs/architecture/services/auth.md)
```

**Полный пример body (с зависимостями, документацией и чек-листом):**

```markdown
## Описание

Добавить возможность экспорта данных в CSV формат для эндпоинта API.

**Зависит от:** #120 (API авторизация)

## Связанная документация

- Спецификация API — `specs/services/api/api-spec.md`
- Архитектура сервиса — `specs/services/api/architecture.md`

## Критерии готовности

- [ ] Эндпоинт GET /api/export/csv
- [ ] Тесты покрывают happy path и edge cases
- [ ] Документация API обновлена
```

### Labels — обязательные метки

**SSOT:** [standard-labels.md](../labels/standard-labels.md)

**Обязательно при создании Issue:**
- Ровно 1 метка типа (bug, task, docs, refactor)
- Ровно 1 метка приоритета (critical, high, medium, low)

**Опционально:** status (ready, wip, in-review, blocked), area, effort, env, svc

Правила применения и разрешение конфликтов — см. [standard-labels.md § 3, 5](../labels/standard-labels.md#3-правила-применения).

### Assignees — назначение

**Когда назначать:**
- Issue создан И известен исполнитель → назначить через `--assignee {username}`
- Issue создан И исполнитель неизвестен → оставить без assignee
- Создана ветка `{NNNN}-{topic}` → назначить себя через `gh issue edit {number} --add-assignee @me`

**Правила:**
- Максимум 3 assignee на Issue
- Если требуется более 3 исполнителей → разбить задачу на подзадачи (создать связанные Issues)
- Самоназначение: `@me` — можно использовать в CLI

CLI команды назначения — см. [§7 CLI команды](#7-cli-команды).

---

## 5. Связь с Branch и PR

**SSOT:**
- Именование веток — [standard-branching.md](../branches/standard-branching.md#2-naming-convention)
- Формат PR и ключевые слова — [standard-pull-request.md](../pull-requests/standard-pull-request.md)

**Процесс:** Issue → ветка `{NNNN}-{topic}` (имя папки analysis chain) → PR с `Fixes #N` → мерж → Issue закрывается автоматически.

Детали процесса — см. [§3 Жизненный цикл](#3-жизненный-цикл). Ключевые слова автозакрытия: `Fixes`, `Closes`, `Resolves` — см. [standard-pull-request.md](../pull-requests/standard-pull-request.md#6-связь-с-issues).

---

## 6. Закрытие Issue

**Основной способ:** Автоматически через мерж PR с ключевым словом `Fixes #N` (см. [§ 5](#5-связь-с-branch-и-pr)).

**Запрет:** Ручное закрытие с reason `completed` **ЗАПРЕЩЕНО**. Если задача выполнена — должен быть PR.

### Ручное закрытие (только `not planned`)

Допускается **только** с `--reason "not planned"` в следующих случаях:

| Причина | Действие |
|---------|----------|
| Дубликат | Закрыть с комментарием-ссылкой на оригинал |
| Больше не актуален | Закрыть с указанием причины |
| Создан по ошибке | Закрыть с пояснением |

**Правила:**
- Комментарий с причиной **ОБЯЗАТЕЛЕН**
- CLI — см. [§7](#7-cli-команды)

### Обработка дубликатов

**Перед созданием Issue:**
```bash
gh issue list --search "ключевое слово" --state all
```

**При обнаружении дубликата:**
- Закрывать **более новый** Issue (с большим номером)
- Если новый содержит полезную информацию — перенести в комментарий оригинала

---

## 7. CLI команды

### Создание

```bash
# Из шаблона (РЕКОМЕНДУЕТСЯ)
gh issue create --template bug.yml

# С параметрами
gh issue create --title "Добавить авторизацию" --body "Описание..." \
  --label feature --label high --assignee @me --milestone "v1.0.0"
```

### Просмотр

```bash
# Список Issues
gh issue list                           # Открытые
gh issue list --state all               # Все
gh issue list --label bug          # По метке
gh issue list --assignee @me            # Назначенные мне
gh issue list --milestone "v1.0.0"      # По milestone

# Детали Issue
gh issue view 123                       # Краткая информация
gh issue view 123 --comments            # С комментариями
```

### Редактирование

```bash
# Title
gh issue edit 123 --title "Новый заголовок"

# Метки
gh issue edit 123 --add-label critical
gh issue edit 123 --remove-label medium

# Assignees
gh issue edit 123 --add-assignee user1,user2
gh issue edit 123 --remove-assignee user1

# Milestone
gh issue edit 123 --milestone "v1.0.0"
gh issue edit 123 --milestone ""        # Убрать из milestone
```

### Закрытие и статус

```bash
# Закрыть (только not planned — см. §6)
gh issue close 123 --reason "not planned" --comment "Причина закрытия"

# Переоткрыть
gh issue reopen 123

# Закрепить (pin)
gh issue pin 123
```

### Поиск

```bash
# Комбинация фильтров
gh issue list --label bug --label critical --state open

# По milestone
gh issue list --milestone "v1.0.0" --state open
```

---

## 8. Декомпозиция и зависимости

GitHub Issues не имеет нативного поля "depends on". Для управления связями используются два дополняющих механизма:

| Тип связи | Механизм | Когда |
|-----------|----------|-------|
| Вертикальная (parent → child) | Sub-issues | Крупная задача → подзадачи |
| Горизонтальная (A → B) | Body text | Issue B зависит от результата Issue A |

### Sub-issues (декомпозиция)

Sub-issues — нативная иерархия GitHub: parent Issue содержит child Issues с прогресс-баром.

**Когда создавать sub-issues:**
- Задача требует 3+ отдельных PR
- Разные исполнители для разных частей
- Нужен визуальный прогресс на parent Issue

**Когда НЕ создавать:**
- Задача выполнима в 1 PR
- Подзадачи не требуют отдельного отслеживания → использовать чек-лист в body (см. ниже)

**Создание:**
```bash
# UI: на parent Issue → "Create sub-issue"
# CLI: создать Issue, затем привязать
gh issue create --title "Подзадача" --label task
# Привязать к parent через UI или API
```

**Пример:**
```
#100 "Настроить CI/CD pipeline" (parent)
  ├── #101 "Настроить linting"          ✅
  ├── #102 "Настроить тесты"            ✅
  ├── #103 "Настроить деплой staging"    🔄
  └── #104 "Настроить деплой prod"       ⏳ Зависит от #103
```

**Порядок sub-issues = порядок выполнения.** Parent Issue показывает прогресс (2/4 done).

### Зависимости между Issues

Горизонтальная зависимость: Issue B не может быть выполнен без результата Issue A.

**Формат:** В body Issue, сразу после секции "Описание":
```markdown
## Описание

{Что нужно сделать}

**Зависит от:** #123, #124
```

**Правила:**
- Формат строго: `**Зависит от:** #номер, #номер`
- Размещение: сразу после "## Описание" или первого абзаца body
- Проверка: ручная, перед закрытием Issue
- Если зависимость появилась после создания Issue → добавить в body через `gh issue edit`

**Проверка перед закрытием:**
```bash
# Проверить статус зависимых Issues
gh issue view 123 --json state --jq '.state'
gh issue view 124 --json state --jq '.state'

# Если хотя бы один OPEN → НЕ закрывать текущий Issue
```

### Подзадачи внутри Issue (чек-лист)

Для мелких подзадач, не требующих отдельного Issue:
```markdown
## Критерии готовности

- [ ] Эндпоинт GET /api/export
- [ ] Тесты покрывают happy path
- [ ] Документация обновлена
```

GitHub показывает прогресс (2/3 tasks) прямо в списке Issues.

**Когда выносить в отдельный Issue:**
- Подзадача требует отдельного PR
- Подзадача назначается другому исполнителю
- Подзадача имеет собственные зависимости

---

## 9. Связь с Milestones

Issue **ДОЛЖЕН** быть добавлен в Milestone для группировки по целевой версии релиза.

**SSOT (Milestones):** [standard-milestone.md](../milestones/standard-milestone.md)

### Правила группировки Issues

**Принцип:**
- Issue принадлежит Milestone, если он запланирован на выполнение в рамках этого Milestone
- Один Issue — один Milestone (нельзя добавить в несколько Milestones)
- Issue ДОЛЖЕН быть завершён для релиза этой версии

**Ограничения:**
- Не перегружать Milestone (макс. 15-20 Issues)
- Если Issues > 20 → разбить на подзадачи или вынести часть в следующий Milestone

CLI команды для работы с milestones — см. [§7 CLI команды](#7-cli-команды).
