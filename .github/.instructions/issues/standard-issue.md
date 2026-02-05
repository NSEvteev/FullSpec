---
description: Процесс работы с GitHub Issues
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/issues/README.md
---

# Стандарт управления GitHub Issues

Версия стандарта: 1.1

Правила жизненного цикла, создания и управления задачами (Issues) в репозитории.

**Полезные ссылки:**
- [Инструкции Issues](./README.md)

**SSOT-зависимости:**
- [standard-labels.md](../labels/standard-labels.md) — метки Issues
- [standard-milestone.md](../milestones/standard-milestone.md) — milestones
- [standard-project.md](../projects/standard-project.md) — GitHub Projects
- [standard-issue-template.md](./issue-templates/standard-issue-template.md) — шаблоны Issues
- [standard-pull-request.md](../pull-requests/standard-pull-request.md) — связь с PR

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
- [8. Связь с шаблонами Issue](#8-связь-с-шаблонами-issue)
- [9. Зависимости между Issues](#9-зависимости-между-issues)
- [10. Связь с Milestones](#10-связь-с-milestones)

---

## 1. Назначение

GitHub Issues — система управления задачами, багами, фичами и вопросами проекта.

**Применяется к:**
- Задачи разработки (фичи, рефакторинг, документация)
- Баги и проблемы
- Технические задачи
- Вопросы и обсуждения

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

**Метаданные (опционально):**

| Свойство | Тип | Обязательно | SSOT |
|----------|-----|-------------|------|
| `labels` | label[] | да | [standard-labels.md](../labels/standard-labels.md) |
| `assignees` | user[] | опционально | См. [§4 Assignees](#assignees-назначение) |
| `milestone` | milestone | опционально | [standard-milestone.md](../milestones/standard-milestone.md) |
| `project` | project | опционально | [standard-project.md](../projects/standard-project.md) |

**Как установить:** `--label`, `--assignee`, `--milestone`, `--project` (см. [§7 CLI команды](#7-cli-команды))

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
       ├─ Создание ветки: git checkout -b feature/123-description
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
3. **В РАБОТЕ** — Разработка ведётся локально. **Триггер:** создана ветка `{type}/{issue-number}-*` через `git checkout -b`. Опционально: добавить метку `status:wip`.
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

**Минимальная структура (если без шаблона):**

```markdown
## Описание

{Что нужно сделать и зачем}

## Критерии готовности

- [ ] {Пункт 1}
- [ ] {Пункт 2}
```

**Для багов, фич, задач:** Использовать соответствующий шаблон из `.github/ISSUE_TEMPLATE/` — см. [примеры шаблонов](./issue-templates/standard-issue-template.md#11-примеры-шаблонов).

### Labels — обязательные метки

**SSOT:** [standard-labels.md](../labels/standard-labels.md)

**Обязательно при создании Issue:**
- Ровно 1 метка `type:*`
- Ровно 1 метка `priority:*`

**Опционально:** `status:*`, `area:*`, `effort:*`, `env:*`

Правила применения и разрешение конфликтов — см. [standard-labels.md § 3, 5](../labels/standard-labels.md#3-правила-применения).

### Assignees — назначение

**Когда назначать:**
- Issue создан И известен исполнитель → назначить через `--assignee {username}`
- Issue создан И исполнитель неизвестен → оставить без assignee
- Создана ветка `{type}/{issue-number}-*` → назначить себя через `gh issue edit {number} --add-assignee @me`

**Как назначить:**

```bash
# При создании
gh issue create --assignee @me

# После создания
gh issue edit 123 --add-assignee user1,user2
```

**Правила:**
- Максимум 3 assignee на Issue
- Если требуется более 3 исполнителей → разбить задачу на подзадачи (создать связанные Issues)
- Самоназначение: `@me` — можно использовать в CLI

---

## 5. Связь с Branch и PR

**SSOT-зависимости:**
- Именование веток — [standard-github-workflow.md](../standard-github-workflow.md)
- Формат PR и ключевые слова — [standard-pull-request.md](../pull-requests/standard-pull-request.md)

**Процесс:**

1. **Issue создан** — получает номер (например, #123)
2. **Создание ветки** — формат: `{type}/{issue-number}-{краткое-описание}`
   ```bash
   # Примеры:
   git checkout -b fix/123-auth-error
   git checkout -b feature/123-add-auth
   git checkout -b docs/123-update-readme
   ```
3. **Создание PR** — связать с Issue через ключевое слово в body PR:
   ```markdown
   Fixes #123
   ```
4. **Мерж PR** — Issue автоматически закроется

**Ключевые слова для автозакрытия:** `Fixes`, `Closes`, `Resolves` — подробнее см. [standard-pull-request.md](../pull-requests/standard-pull-request.md#6-связь-с-issues).

---

## 6. Закрытие Issue

### Автоматическое закрытие

Через мерж PR с ключевым словом (см. [§ 5](#5-связь-с-branch-и-pr)).

### Ручное закрытие

```bash
# Закрыть Issue
gh issue close 123

# Закрыть с комментарием
gh issue close 123 --comment "Исправлено в PR #456"

# Переоткрыть Issue
gh issue reopen 123
```

**Когда закрывать вручную:**
- Issue решён другим способом (не через PR)
- Issue дублирует другой Issue
- Issue больше не актуален

**Правила:**
- При ручном закрытии — ОБЯЗАТЕЛЬНО добавить комментарий с причиной
- Не закрывать Issue без выполнения задачи (кроме дубликатов/неактуальных)

---

## 7. CLI команды

### Создание

```bash
# Базовое создание (интерактивно)
gh issue create

# С параметрами
gh issue create --title "Добавить авторизацию" --body "Описание..." --label type:feature --label priority:high --assignee @me

# Из шаблона
gh issue create --template bug.yml
```

### Просмотр

```bash
# Список Issues
gh issue list                           # Открытые
gh issue list --state all               # Все (открытые + закрытые)
gh issue list --label type:bug          # Только баги
gh issue list --assignee @me            # Назначенные мне
gh issue list --milestone "Sprint 1"    # По milestone

# Детали Issue
gh issue view 123                       # Краткая информация
gh issue view 123 --comments            # С комментариями
gh issue view 123 --web                 # Открыть в браузере
```

### Редактирование

```bash
# Изменить title
gh issue edit 123 --title "Новый заголовок"

# Добавить/удалить метки
gh issue edit 123 --add-label priority:critical
gh issue edit 123 --remove-label priority:medium

# Добавить/удалить assignees
gh issue edit 123 --add-assignee user1,user2
gh issue edit 123 --remove-assignee user1

# Установить milestone
gh issue edit 123 --milestone "Sprint 2"

# Добавить в project
gh issue edit 123 --add-project "Roadmap"
```

### Статус

```bash
# Закрыть
gh issue close 123
gh issue close 123 --comment "Причина закрытия"

# Переоткрыть
gh issue reopen 123

# Закрепить (pin)
gh issue pin 123

# Заблокировать комментарии
gh issue lock 123
```

### Поиск

```bash
# По метке
gh issue list --label type:bug

# По assignee
gh issue list --assignee username

# По milestone
gh issue list --milestone "v1.0"

# По состоянию
gh issue list --state closed

# Комбинация фильтров
gh issue list --label type:bug --label priority:critical --state open
```

---

## 8. Связь с шаблонами Issue

Issue могут создаваться через шаблоны из `.github/ISSUE_TEMPLATE/`.

**При создании Issue через CLI:**
```bash
# Интерактивный выбор шаблона
gh issue create

# Явный выбор шаблона
gh issue create --template bug.yml

# Без шаблона (НЕ РЕКОМЕНДУЕТСЯ)
gh issue create --title "..." --body "..." --label type:task --label priority:medium
```

**Правило:** ВСЕГДА использовать шаблон при создании Issue через CLI (кроме технических задач без структуры).

**Подробнее:**
- Структура шаблонов — [standard-issue-template.md](./issue-templates/standard-issue-template.md)
- Валидация шаблонов — [validation-type-templates.md](./issue-templates/validation-type-templates.md)

---

## 9. Зависимости между Issues

### Указание зависимости

В body Issue добавить:
```markdown
**Зависит от:** #123, #124
```

### Проверка перед закрытием

Перед закрытием Issue проверить:
```bash
# Вручную проверить статус зависимых Issues
gh issue view 123
gh issue view 124

# Если хотя бы один Issue открыт → НЕ закрывать текущий Issue
```

**Правило:** Не закрывать Issue если зависимые Issues ещё открыты.

---

## 10. Связь с Milestones

Issue может быть добавлен в Milestone для группировки по целевой версии релиза.

**SSOT (Milestones):** [standard-milestone.md](../milestones/standard-milestone.md)

### Добавление Issue в Milestone

**При создании Issue:**

1. Проверить существование Milestone:
   ```bash
   gh api repos/{owner}/{repo}/milestones -q '.[] | select(.title == "v1.0.0") | .number'
   # Если пусто → Milestone не существует, создать или выбрать другой
   ```
2. Создать Issue с Milestone:
   ```bash
   gh issue create \
     --title "Добавить OAuth2" \
     --body "..." \
     --label type:feature \
     --label priority:high \
     --milestone "v1.0.0"
   ```

**Для существующего Issue:**

```bash
gh issue edit 123 --milestone "v1.0.0"
```

**Удаление Issue из Milestone:**

```bash
gh issue edit 123 --milestone ""
```

### Правила группировки Issues

**Принцип:**
- Issue принадлежит Milestone, если он запланирован на выполнение в рамках этого Milestone
- Один Issue — один Milestone (нельзя добавить в несколько Milestones)
- Issue ДОЛЖЕН быть завершён для релиза этой версии

**Ограничения:**
- Не перегружать Milestone (макс. 15-20 Issues)
- Если Issues > 20 → разбить на подзадачи или вынести часть в следующий Milestone

### Просмотр Issues в Milestone

```bash
# Список Issues
gh issue list --milestone "v1.0.0"

# Открытые Issues
gh issue list --milestone "v1.0.0" --state open

# Закрытые Issues
gh issue list --milestone "v1.0.0" --state closed
```
