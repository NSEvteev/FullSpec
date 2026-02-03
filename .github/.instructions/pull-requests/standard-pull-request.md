---
description: Стандарт работы с Pull Requests в GitHub
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/pull-requests/README.md
---

# Стандарт Pull Request

Версия стандарта: 1.0

Процесс работы с Pull Requests: создание, review, merge.

**Полезные ссылки:**
- [Инструкции](./README.md)
- [Стандарт меток](../labels/standard-labels.md) — категоризация PR

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Шаблон PR | [standard-pr-template.md](../pr-template/standard-pr-template.md) |
| Валидация | *Будет создан* |
| Создание | *Будет создан* |
| Модификация | *Будет создан* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Жизненный цикл PR](#2-жизненный-цикл-pr)
- [3. Создание Pull Request](#3-создание-pull-request)
- [4. Именование title](#4-именование-title)
- [5. Структура body](#5-структура-body)
- [6. Связь с Issue](#6-связь-с-issue)
- [7. Применение меток](#7-применение-меток)
- [8. Code Review процесс](#8-code-review-процесс)
- [9. Merge стратегии](#9-merge-стратегии)
- [10. CLI команды](#10-cli-команды)

---

## 1. Назначение

Pull Request (PR) — запрос на слияние изменений из одной ветки в другую.

**Применяется для:**
- Code review перед мержем в main
- Документирования изменений
- Запуска автоматических проверок (CI/CD)
- Обсуждения реализации
- Связывания кода с задачами (Issues)

**Принципы:**
- Каждая фича/баг/задача → отдельный PR
- PR создаётся ИЗ feature-ветки В main
- Merge в main происходит только через PR
- PR закрывает связанный Issue автоматически

**Роли:**
- **Author** — создатель PR
- **Reviewer** — ревьюер кода
- **Assignee** — ответственный за PR (обычно совпадает с author)

---

## 2. Жизненный цикл PR

```
1. СОЗДАНИЕ
   └─ Автор создаёт PR из feature-ветки
   └─ Заполняет title, body, reviewers, labels
   └─ PR в статусе Open (или Draft)

2. АВТОПРОВЕРКИ
   └─ Pre-commit хуки выполнены локально
   └─ CI workflows (если есть в .github/workflows/ с триггером pull_request)
   └─ Branch protection rules (если настроены)

3. CODE REVIEW
   └─ Reviewer просматривает изменения
   └─ Approve / Request changes / Comment
   └─ При Request changes → автор исправляет и пушит

4. MERGE
   └─ Все автоматические проверки пройдены (pre-commit, CI)
   └─ Получен минимум 1 approval от reviewer
   └─ Нет merge conflicts
   └─ Squash merge в main
   └─ Feature-ветка удаляется

5. АВТОЗАКРЫТИЕ ISSUE
   └─ Если в body есть "Closes #123"
   └─ Issue закрывается автоматически после merge
```

### Draft PR (черновик)

**Когда использовать:**
- Фича большая, хочется показать направление разработки до завершения
- Нужен early feedback от команды
- PR в процессе разработки, но хочется сохранить прогресс

**Ограничения:**
- Draft PR **нельзя** мержить до перевода в статус "Ready"
- Reviewers могут оставлять комментарии, но approval не требуется

**Перевод в Ready:**
```bash
gh pr ready 123
```

### Статусы PR

| Статус | Описание |
|--------|----------|
| `Draft` | Черновик, не готов к ревью, нельзя мержить |
| `Open` | Готов к ревью |
| `Changes requested` | Требуются правки после ревью |
| `Approved` | Одобрен ревьюером |
| `Merged` | Слит в целевую ветку |
| `Closed` | Закрыт без мержа |

---

## 3. Создание Pull Request

### Обязательные поля

| Поле | Правило | Пример |
|------|---------|--------|
| `title` | Короткий заголовок (до 70 символов) | `feat: add user authentication` |
| `body` | Описание изменений | См. [5. Структура body](#5-структура-body) |
| `head` | Исходная ветка (автоматически) | `feature/123-auth` |
| `base` | Целевая ветка | `main` |

### Опциональные поля

| Поле | Когда добавлять | Пример |
|------|-----------------|--------|
| `reviewers` | Минимум 1 для критичных изменений (type:bug с priority:critical, breaking changes) | `@username1,@username2` |
| `assignees` | Если автор ≠ исполнитель | `@me` |
| `labels` | Всегда | `type:feature`, `priority:high` |
| `milestone` | Если привязано к спринту/релизу | `Sprint 1`, `v1.0` |
| `project` | Если используется kanban | `Roadmap` |
| `draft` | Если не готов к ревью | `--draft` |

---

## 4. Именование title

**Формат:**
```
{type}: {краткое описание}
```

**Правила:**
- Начинается с типа изменения (без префикса category)
- Нижний регистр
- Без точки в конце
- До 70 символов

**Типы изменений:**

| Тип | Когда использовать | Метка |
|-----|-------------------|-------|
| `feat` | Новая функциональность | `type:feature` |
| `fix` | Исправление бага | `type:bug` |
| `docs` | Изменения в документации | `type:docs` |
| `refactor` | Рефакторинг кода | `type:refactor` |
| `test` | Добавление/изменение тестов | `type:task` |
| `chore` | Технические задачи (зависимости, конфиги) | `type:task` |
| `perf` | Улучшение производительности | `type:refactor` |
| `ci` | Изменения CI/CD | `type:task` |

**Важно:** Префикс title (`feat`, `fix`) **не преобразуется** автоматически в метку. Метки добавляются вручную через флаг `--label` при создании PR.

**Примеры:**

| Формат | Корректно | Причина |
|--------|-----------|---------|
| `feat: add login endpoint` | ✅ | — |
| `fix: resolve null pointer in auth` | ✅ | — |
| `docs: update API documentation` | ✅ | — |
| `Feature: Add login` | ❌ | Верхний регистр, не тот префикс |
| `add login endpoint` | ❌ | Нет типа |
| `feat: Add login endpoint.` | ❌ | Точка в конце |

**Область (scope) — опциональна:**
```
{type}({scope}): {описание}
```

Примеры:
- `feat(auth): add OAuth support`
- `fix(api): handle timeout errors`
- `docs(readme): update installation steps`

---

## 5. Структура body

**Обязательные секции:**

```markdown
## Summary
{Что сделано — 1-3 пункта}

## Related Issue
Closes #{номер}

## How to test
{Как проверить изменения}
```

**Опциональные секции:**

```markdown
## Breaking changes
{Только если изменения нарушают обратную совместимость API/контрактов}

## Screenshots
{Если есть UI изменения}

## Notes
{Дополнительные комментарии}
```

**Важно:** Секция "Breaking changes" добавляется ТОЛЬКО если изменения нарушают обратную совместимость. Если breaking changes отсутствуют — секция не добавляется.

**Пример полного body:**

```markdown
## Summary
- Добавлен эндпоинт POST /api/auth/login
- Реализована JWT-авторизация
- Добавлены unit-тесты для auth-модуля

## Related Issue
Closes #123

## How to test
1. Запустить проект: `make dev`
2. Отправить POST /api/auth/login с credentials
3. Проверить получение JWT токена

## Breaking changes
Изменён формат ответа /api/user — добавлено поле `role`
```

---

## 6. Связь с Issue

**Автоматическое закрытие Issue:**

Использовать ключевые слова в body PR:

| Ключевое слово | Действие |
|----------------|----------|
| `Closes #123` | Закрыть Issue при merge |
| `Fixes #123` | То же |
| `Resolves #123` | То же |

**Правила:**
- Писать на отдельной строке в секции "Related Issue"
- Можно закрыть несколько Issues: `Closes #123, #124`
- Issue закрывается автоматически ПОСЛЕ успешного merge PR в целевую ветку (когда PR переходит в статус "Merged")

**Ссылка без закрытия:**
```markdown
Related to #123
See #124
```

---

## 7. Применение меток

**SSOT:** [standard-labels.md](../labels/standard-labels.md)

**Обязательно при создании PR:**
- Ровно 1 метка `type:*`
- Ровно 1 метка `priority:*`

Правила применения — см. SSOT.

---

## 8. Code Review процесс

### Запрос ревью

**Как назначить reviewers:**

```bash
# При создании PR
gh pr create --reviewer @username1,@username2

# Для существующего PR
gh pr edit 123 --add-reviewer @username
```

**Кто назначается:**
- CODEOWNERS (автоматически, если настроено)
- Эксперты области кода
- Минимум 1 reviewer для критичных изменений (`type:bug` с `priority:critical`, breaking changes)

### Проведение ревью

**Reviewer проверяет:**
1. Соответствие требованиям Issue
2. Качество кода (читаемость, принципы)
3. Покрытие тестами
4. Документация обновлена (если нужно)
5. Нет конфликтов с main

**Комментарии:**
- Оставлять комментарии к конкретным строкам
- Объяснять причину замечания
- Предлагать альтернативы

### Типы ревью

| Тип | Команда | Когда использовать |
|-----|---------|-------------------|
| **Approve** | `gh pr review {PR} --approve` | Изменения готовы к merge |
| **Request changes** | `gh pr review {PR} --request-changes --body "..."` | Требуются исправления |
| **Comment** | `gh pr review {PR} --comment --body "..."` | Вопрос или некритичное замечание |

### После Request changes

Если reviewer запросил изменения:

1. **Внести правки** в локальную ветку
2. **Закоммитить и запушить:**
   ```bash
   git add .
   git commit -m "fix: address review comments"
   git push
   ```
3. **Reviewer получит уведомление** о новых изменениях
4. GitHub автоматически помечает старые комментарии как "Outdated" если затронутые строки изменились

**Примеры:**

```bash
# Одобрить PR
gh pr review 123 --approve

# Запросить изменения
gh pr review 123 --request-changes --body "Нужно добавить проверку на null в строке 42"

# Комментарий без блокировки
gh pr review 123 --comment --body "Отличная реализация!"
```

---

## 9. Merge стратегии

**Default стратегия: Squash Merge**

```bash
gh pr merge 123 --squash
```

**Причины:**
- Чистая история main (один коммит на фичу)
- Легко откатить изменения
- Удобно для changelog

**Альтернативные стратегии:**

| Стратегия | Команда | Когда использовать |
|-----------|---------|-------------------|
| **Squash merge** | `--squash` | По умолчанию для фич |
| **Merge commit** | `--merge` | Сохранить полную историю ветки |
| **Rebase** | `--rebase` | Линейная история без merge-коммитов |

### Auto-merge

```bash
# Мержить автоматически, когда все условия выполнены
gh pr merge 123 --auto --squash
```

**Условия срабатывания auto-merge:**
1. Все CI workflows завершились успешно (status: success)
2. Получены необходимые approvals (если настроены Branch Protection Rules)
3. Нет merge conflicts

**Если условия не выполнены:** PR остаётся в очереди auto-merge до выполнения всех условий.

**Отмена auto-merge:**
```bash
gh pr merge 123 --disable-auto
```

### Разрешение конфликтов

Если при merge возникают конфликты:

1. **Локально обновить ветку:**
   ```bash
   git checkout feature-branch
   git pull origin main
   # Разрешить конфликты вручную в редакторе
   git add .
   git commit -m "resolve: merge conflicts with main"
   git push
   ```
2. **Повторить попытку merge через PR** (конфликты должны исчезнуть)
3. Если конфликты сложные — попросить автора PR их разрешить

### Закрытие без merge

PR закрывается без merge в случаях:
- Изменения больше не актуальны (задача отменена)
- Дубликат другого PR
- Автор отказался от изменений

```bash
gh pr close 123 --comment "Дубликат #456"
```

### После merge

- Feature-ветка автоматически удаляется
- Issue закрывается (если указан `Closes #123`)
- PR переходит в статус "Merged"

---

## 10. CLI команды

### Создание PR

```bash
# Базовое создание
gh pr create --title "feat: add login" --body "Summary..."

# Заполнить из коммитов
gh pr create --fill

# С reviewers и labels
gh pr create --title "fix: null pointer" \
  --reviewer @user1,@user2 \
  --label type:bug,priority:high

# Черновик
gh pr create --draft

# В другую ветку (не main)
gh pr create --base develop
```

### Просмотр PR

```bash
# Список PR
gh pr list
gh pr list --state all
gh pr list --label type:bug
gh pr list --assignee @me

# Детали PR
gh pr view 123
gh pr view 123 --comments
gh pr view 123 --web

# Diff
gh pr diff 123

# Проверки CI
gh pr checks 123
```

### Ревью PR

```bash
# Одобрить
gh pr review 123 --approve

# Запросить изменения
gh pr review 123 --request-changes --body "Комментарий"

# Комментарий
gh pr review 123 --comment --body "Вопрос: почему используется X?"
```

### Merge PR

```bash
# Интерактивно (с выбором стратегии)
gh pr merge 123

# Squash merge
gh pr merge 123 --squash

# Merge commit
gh pr merge 123 --merge

# Rebase
gh pr merge 123 --rebase

# Auto-merge при прохождении CI
gh pr merge 123 --auto --squash

# Удалить ветку после merge
gh pr merge 123 --squash --delete-branch
```

### Редактирование PR

```bash
# Изменить title
gh pr edit 123 --title "New title"

# Добавить reviewer
gh pr edit 123 --add-reviewer @user

# Добавить label
gh pr edit 123 --add-label priority:critical

# Снять draft
gh pr ready 123

# Закрыть без merge
gh pr close 123 --comment "Причина"

# Переоткрыть
gh pr reopen 123
```

---

## Скиллы

*Нет скиллов.*
