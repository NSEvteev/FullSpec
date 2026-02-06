---
description: Воркфлоу создания GitHub Issue
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/issues/README.md
---

# Воркфлоу создания Issue

Рабочая версия стандарта: 1.4

Пошаговый процесс создания нового GitHub Issue.

**Полезные ссылки:**
- [Инструкции Issues](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-issue.md](./standard-issue.md) |
| Валидация | [validation-issue.md](./validation-issue.md) |
| Создание | Этот документ |
| Модификация | [modify-issue.md](./modify-issue.md) |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить дубликаты](#шаг-1-проверить-дубликаты)
  - [Шаг 2: Подготовить title](#шаг-2-подготовить-title)
  - [Шаг 3: Выбрать шаблон](#шаг-3-выбрать-шаблон)
  - [Шаг 4: Заполнить body](#шаг-4-заполнить-body)
  - [Шаг 5: Определить labels](#шаг-5-определить-labels)
  - [Шаг 6: Назначить milestone](#шаг-6-назначить-milestone)
  - [Шаг 7: Создать Issue](#шаг-7-создать-issue)
  - [Шаг 8: Валидация](#шаг-8-валидация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Каждая задача — отдельный Issue.** Не группировать несвязанные задачи в один Issue.

> **ВСЕГДА использовать шаблон.** Шаблоны обеспечивают структуру body. SSOT: [standard-issue-template.md](./issue-templates/standard-issue-template.md).

> **Связанная документация обязательна.** Создатель Issue ДОЛЖЕН указать файлы проекта для контекста или явно написать "Связанной документации нет".

> **Issue = задача с PR.** Issue завершается только через merge PR с `Fixes #N`. Нет PR — нет завершения.

> **Milestone обязателен.** Каждый Issue ДОЛЖЕН быть привязан к Milestone.

---

## Шаги

### Шаг 1: Проверить дубликаты

**SSOT:** [standard-issue.md § 6](./standard-issue.md#6-закрытие-issue)

```bash
gh issue list --search "ключевое слово" --state all
```

**Если найден дубликат:**
- Не создавать новый Issue
- При необходимости — добавить комментарий к существующему

### Шаг 2: Подготовить title

**SSOT:** [standard-issue.md § 4 Title](./standard-issue.md#title-правила-именования)

**Правила:**
- Начинать с глагола в инфинитиве с заглавной буквы
- Длина: 50-70 символов
- Без префиксов типа (тип — в labels)
- Без номера Issue

| Корректно | Некорректно |
|-----------|-------------|
| `Добавить авторизацию пользователей` | `добавить авторизацию` |
| `Исправить ошибку загрузки файлов` | `Bug: ошибка загрузки` |

### Шаг 3: Выбрать шаблон

**SSOT:** [standard-issue-template.md](./issue-templates/standard-issue-template.md)

```bash
# Список доступных шаблонов
ls .github/ISSUE_TEMPLATE/*.yml
```

| Тип задачи | Шаблон |
|------------|--------|
| Баг | `bug-report.yml` |
| Фича | `feature-request.yml` |
| Техническая задача | `task.yml` |
| Документация | `docs.yml` |
| Рефакторинг | `refactor.yml` |
| Вопрос | `question.yml` |

### Шаг 4: Заполнить body

**SSOT:** [standard-issue.md § 4 Body](./standard-issue.md#body-структура-описания)

**Обязательные секции:**

| Секция | Содержание |
|--------|------------|
| `## Описание` | Что нужно сделать и зачем |
| `## Связанная документация` | Список файлов или "Связанной документации нет" |
| `## Критерии готовности` | Чек-лист `- [ ]` |

**Формат связанной документации:** `{описание} — {путь к файлу}`

**Если есть зависимости:** добавить `**Зависит от:** #N, #M` после секции "Описание".

**Минимальная структура:**

```markdown
## Описание

{Что нужно сделать и зачем}

## Связанная документация

- {Описание} — {путь}

## Критерии готовности

- [ ] {Пункт 1}
- [ ] {Пункт 2}
```

### Шаг 5: Определить labels

**SSOT:** [standard-issue.md § 4 Labels](./standard-issue.md#labels-обязательные-метки), [standard-labels.md](../labels/standard-labels.md)

**Обязательные:**
- Ровно 1 метка `type:*` (определяется шаблоном)
- Ровно 1 метка `priority:*`

**Проверить существование меток:**

```bash
gh label list --search "type:feature"
gh label list --search "priority:high"
```

| Приоритет | Когда |
|-----------|-------|
| `priority:critical` | Блокирует релиз, нужно немедленно |
| `priority:high` | Важно для текущего milestone |
| `priority:medium` | Стандартная задача |
| `priority:low` | Можно отложить |

### Шаг 6: Назначить milestone

**SSOT:** [standard-issue.md § 9](./standard-issue.md#9-связь-с-milestones)

```bash
# Список открытых milestones
gh api repos/{owner}/{repo}/milestones --method GET -q '.[].title'
```

Выбрать milestone, в рамках которого Issue должен быть завершён.

**Если нет подходящего milestone:**
- Создать через `/milestone-create` (см. [create-milestone.md](../milestones/create-milestone.md))

### Шаг 7: Создать Issue

**SSOT:** [standard-issue.md § 7](./standard-issue.md#7-cli-команды)

**Через шаблон (РЕКОМЕНДУЕТСЯ):**

```bash
gh issue create --template bug-report.yml
```

**С параметрами:**

```bash
gh issue create \
  --title "Добавить авторизацию пользователей" \
  --body "## Описание

Добавить JWT-авторизацию для API.

## Связанная документация

- Архитектура API — specs/services/api/architecture.md
- Спецификация эндпоинтов — specs/services/api/api-spec.md

## Критерии готовности

- [ ] Эндпоинт POST /auth/login
- [ ] Middleware проверки токена
- [ ] Тесты" \
  --label type:feature --label priority:high \
  --milestone "v1.0.0"
```

**Запомнить номер созданного Issue** — он нужен для валидации.

### Шаг 8: Валидация

**ОБЯЗАТЕЛЬНО** после создания — запустить валидацию:

```bash
# Один Issue
python .github/.instructions/.scripts/validate-issue.py {number}

# Все открытые Issues
python .github/.instructions/.scripts/validate-issue.py --all
```

Или через скилл: `/issue-validate {number}`

**Критерии прохождения:** все проверки без ошибок (E001-E015).

---

## Чек-лист

### Подготовка
- [ ] Проверены дубликаты
- [ ] Title начинается с глагола, 50-70 символов
- [ ] Выбран шаблон
- [ ] Заполнен body с обязательными секциями

### Метаданные
- [ ] Ровно 1 метка `type:*`
- [ ] Ровно 1 метка `priority:*`
- [ ] Milestone назначен

### Body
- [ ] Секция "Описание" заполнена
- [ ] Секция "Связанная документация" заполнена (файлы или "Связанной документации нет")
- [ ] Секция "Критерии готовности" содержит чек-лист
- [ ] Зависимости указаны (если есть)

### Проверка
- [ ] Issue создан
- [ ] Валидация пройдена (`validate-issue.py` или `/issue-validate`)
- [ ] Номер Issue получен

---

## Примеры

### Создание баг-репорта

```bash
# 1. Проверить дубликаты
gh issue list --search "ошибка загрузки файлов" --state all

# 2. Создать через шаблон
gh issue create --template bug-report.yml

# 3. Или с параметрами
gh issue create \
  --title "Исправить ошибку загрузки файлов более 10 МБ" \
  --body "## Описание

При загрузке файлов более 10 МБ возникает ошибка 413.

## Связанная документация

- Конфигурация Nginx — platform/gateway/nginx.conf
- Спецификация upload API — specs/services/api/upload-spec.md

## Критерии готовности

- [ ] Лимит увеличен до 50 МБ
- [ ] Тест на загрузку большого файла" \
  --label type:bug --label priority:high \
  --milestone "v1.0.0"

# 4. Валидация
python .github/.instructions/.scripts/validate-issue.py 42
```

### Создание технической задачи (без документации)

```bash
gh issue create \
  --title "Настроить CI/CD pipeline для staging окружения" \
  --body "## Описание

Настроить автоматический деплой на staging при мерже в main.

## Связанная документация

Связанной документации нет

## Критерии готовности

- [ ] GitHub Action для деплоя
- [ ] Переменные окружения настроены
- [ ] Smoke-тест после деплоя" \
  --label type:task --label priority:medium \
  --milestone "v0.1.0"
```

### Массовая валидация

```bash
# Проверить все открытые Issues
python .github/.instructions/.scripts/validate-issue.py --all

# Проверить Issues конкретного milestone
python .github/.instructions/.scripts/validate-issue.py --milestone "v1.0.0"
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-issue.py](../.scripts/validate-issue.py) | Валидация Issue: один, все, по milestone | [validation-issue.md](./validation-issue.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/issue-create](/.claude/skills/issue-create/SKILL.md) | Создание Issue по стандарту | Этот документ |
| [/issue-validate](/.claude/skills/issue-validate/SKILL.md) | Валидация Issue | [validation-issue.md](./validation-issue.md) |
