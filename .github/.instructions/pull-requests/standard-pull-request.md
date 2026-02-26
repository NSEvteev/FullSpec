---
description: Стандарт работы с Pull Requests — формат заголовка, описание, reviewers, метки, чек-лист готовности.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/pull-requests/README.md
---

# Стандарт Pull Request

Версия стандарта: 1.0

Процесс работы с Pull Requests: создание, review, merge.

**Полезные ссылки:**
- [Инструкции](./README.md)
- [standard-pr-template.md](./pr-template/standard-pr-template.md) — Шаблон PR

**SSOT-зависимости:**
- [standard-branching.md](../branches/standard-branching.md) — PR создаётся из feature-ветки
- [standard-labels.md](../labels/standard-labels.md) — категоризация PR
- [standard-review.md](../review/standard-review.md) — процесс review после создания PR
- [standard-issue.md](../issues/standard-issue.md) — Closes #N, связь PR → Issues
- [standard-development.md](../development/standard-development.md) — проверки до создания PR
- [standard-sync.md](../sync/standard-sync.md) — синхронизация при длительной разработке
- [standard-github-workflow.md](../standard-github-workflow.md) — полный цикл (стадия 5: PR)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | *Будет создан* |
| Создание | [create-pull-request.md](./create-pull-request.md) |
| Модификация | *Будет создан* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Жизненный цикл PR](#2-жизненный-цикл-pr)
- [3. Создание Pull Request](#3-создание-pull-request)
- [4. Именование title](#4-именование-title)
- [5. Структура body](#5-структура-body)
- [6. Связь с Issues](#6-связь-с-issues)
- [7. Применение меток](#7-применение-меток)
- [8. Review и Merge](#8-review-и-merge)
- [9. CLI команды](#9-cli-команды)
- [10. Граничные случаи](#10-граничные-случаи)

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
- Каждая фича/область → группа Issues → один PR
- PR создаётся ИЗ feature-ветки В main
- Merge в main происходит только через PR
- PR закрывает все связанные Issues автоматически (через `Closes #42, #43, #44`)

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
   └─ Нет активных "Requested changes" от reviewers
   └─ Нет merge conflicts
   └─ Squash merge в main
   └─ Feature-ветка удаляется

5. АВТОЗАКРЫТИЕ ISSUES
   └─ Если в body есть "Closes #42", "Closes #43", "Closes #44"
   └─ Все указанные Issues закрываются автоматически после merge
```

### Draft PR (черновик)

**Когда использовать:**
- Фича большая, хочется показать направление разработки до завершения
- Нужен early feedback от команды
- PR в процессе разработки, но хочется сохранить прогресс

**Ограничения:**

| Аспект | Ограничение |
|--------|-------------|
| Merge | Запрещён до перевода в Ready |
| Approval | Не требуется (reviewers могут комментировать) |
| CI checks | Выполняются, но не блокируют |

**Заполнение секций в Draft PR:**

| Секция | Требование |
|--------|------------|
| Summary | ОБЯЗАТЕЛЬНО, добавить `[WIP]` или `[Draft]` в начало |
| Changes | Можно заполнить частично или оставить placeholder |
| Test plan | Можно не отмечать чекбоксы |
| Related issues | ОБЯЗАТЕЛЬНО указать (для трекинга) |

**Перевод в Ready:**

1. Убрать `[WIP]`/`[Draft]` из Summary
2. Заполнить все обязательные секции
3. Отметить выполненные пункты в Test plan
4. Убедиться что CI проходит

```bash
gh pr ready 123
```

> **Возврат в Draft** — только через GitHub UI (CLI не поддерживает).

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
| `title` | Короткий заголовок (до 70 символов) | `feature: add user authentication` |
| `body` | Описание изменений | См. [5. Структура body](#5-структура-body) |
| `head` | Исходная ветка (автоматически) | `0001-oauth2-authorization` |
| `base` | Целевая ветка | `main` |

### Опциональные поля

| Поле | Когда добавлять | Пример |
|------|-----------------|--------|
| `reviewers` | Минимум 1 для критичных изменений (bug с critical, breaking changes) | `@username1,@username2` |
| `assignees` | Если автор ≠ исполнитель | `@me` |
| `labels` | Всегда | `feature`, `high` |
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

**Допустимые типы:**

Тип в title **должен совпадать** с одной из меток категории TYPE из [labels.yml](/.github/labels.yml).

**SSOT типов:** [labels.yml](/.github/labels.yml) — секция "TYPE"

**Примеры:**
```
feature: add login endpoint      → метка: feature
bug: fix null pointer in auth    → метка: bug
docs: update API documentation   → метка: docs
```

**Важно:**
- При изменении меток в labels.yml — типы в title меняются автоматически
- Метки добавляются вручную через флаг `--label` при создании PR

**Примеры:**

| Формат | Корректно | Причина |
|--------|-----------|---------|
| `feature: add login endpoint` | ✅ | — |
| `bug: resolve null pointer in auth` | ✅ | — |
| `docs: update API documentation` | ✅ | — |
| `Feature: Add login` | ❌ | Верхний регистр |
| `add login endpoint` | ❌ | Нет типа |
| `feature: Add login endpoint.` | ❌ | Точка в конце |
| `feat: add login` | ❌ | Устаревший тип (используйте `feature`) |

**Область (scope) — опциональна:**
```
{type}({scope}): {описание}
```

Примеры:
- `feature(auth): add OAuth support`
- `bug(api): handle timeout errors`
- `docs(readme): update installation steps`

---

## 5. Структура body

**SSOT:** [standard-pr-template.md](./pr-template/standard-pr-template.md)

Body PR заполняется по шаблону `.github/PULL_REQUEST_TEMPLATE.md`.

Структура секций, правила заполнения и примеры — см. SSOT.

---

## 6. Связь с Issues

### Группировка Issues

**Принцип:** Одна фича/область → группа связанных Issues → один PR.

**Критерии группировки:**

| Критерий | Пример |
|----------|--------|
| Одна фича | Все Issues про авторизацию (#42, #43, #44) → один PR |
| Одна область кода | Все Issues про API /users (#50, #51) → один PR |
| Логическая связь | Issues, которые нельзя сделать по отдельности |

**Когда разделять на несколько PR:**
- Issues из разных фич/областей
- Issues не зависят друг от друга
- PR получается слишком большим (>500 строк изменений)

### Автоматическое закрытие Issues

**Ключевые слова:**

| Слово | Действие |
|-------|----------|
| `Closes #номер` | Закрыть Issue при merge |
| `Fixes #номер` | Закрыть Issue при merge |
| `Resolves #номер` | Закрыть Issue при merge |
| `Related to #номер` | Связать без закрытия |

**Формат (каждый Issue на отдельной строке):**
```markdown
## Related Issues
Closes #42
Closes #43
Closes #44
```

**Важно:** Issues закрываются автоматически ТОЛЬКО после успешного merge PR в целевую ветку.

**Формат синтаксиса:** см. [standard-pr-template.md](./pr-template/standard-pr-template.md)

---

## 7. Применение меток

**SSOT:** [standard-labels.md](../labels/standard-labels.md)

**Обязательно при создании PR:**
- Ровно 1 метка типа (категория TYPE из labels.yml)
- Ровно 1 метка приоритета (категория PRIORITY из labels.yml)

**SSOT меток:** [labels.yml](/.github/labels.yml)

---

## 8. Review и Merge

**SSOT:** [standard-review.md](../review/standard-review.md)

После создания PR начинается процесс ревью и merge. Все детали (Code Review процесс, merge стратегии, Branch Protection Rules, блокирующие условия) — см. SSOT.

---

## 9. CLI команды

### Создание PR

```bash
# Базовое создание
gh pr create --title "feature: add login" --body "Summary..."

# Заполнить из коммитов
gh pr create --fill

# С reviewers и labels
gh pr create --title "bug: null pointer" \
  --reviewer @user1,@user2 \
  --label bug,high

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
gh pr list --label bug
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
gh pr edit 123 --add-label critical

# Снять draft
gh pr ready 123

# Закрыть без merge
gh pr close 123 --comment "Причина"

# Переоткрыть
gh pr reopen 123
```

---

## 10. Граничные случаи

### PR без связанного Issue

**Запрещено:** Создавать PR без Issue.

**Исключение:** Минорные правки (опечатки в README, форматирование) — можно без Issue.

**Правильно для минорных правок:**
```bash
gh pr create --title "docs: fix typo in README" \
  --body "Fixed typo in installation section" \
  --label docs --label low
```

**Важно:** В body НЕ указывать "Closes #...", так как Issue нет.

### Hotfix в production

**Сценарий:** Критичный баг на production, нужен срочный фикс.

**Процесс:**
1. Создать Issue с меткой `critical`
2. Создать ветку `{NNNN}-hotfix-{description}` от main
3. Внести исправление + тесты
4. Создать PR с `--label critical`
5. Ускоренное ревью (минимум 1 approval)
6. Merge сразу после approval
7. Deploy в production

**Важно:** НЕ пропускать Issue и PR, даже для hotfix.

### Длительная разработка (синхронизация с main)

**Сценарий:** Фича разрабатывается 1+ неделю, main уходит вперёд.

**Процесс:**
1. Регулярно синхронизировать feature-ветку с main:
   ```bash
   git checkout 0001-oauth2-authorization
   git pull origin main
   # Разрешить конфликты (если есть)
   git push
   ```
2. При возникновении конфликтов — разрешать сразу, не копить
3. При создании PR — конфликтов не будет

**Рекомендуется:** Синхронизировать feature-ветку с main минимум 1 раз в 2 дня.

### Координация зависимых PR

**Сценарий:** Работа над зависимыми фичами (например, backend API и frontend интеграция).

**Рекомендация:** Один analysis chain = одна ветка = один PR. Если объём слишком велик — разбить на уровне Discussion (создать отдельные analysis chains).

**Если разделение необходимо:**
1. Создать отдельные analysis chains (Discussion → Design → Plan Tests → Plan Dev)
2. Первая цепочка (например, backend API) мержится первой
3. Вторая цепочка (например, frontend) создаётся от свежего main после merge первой

```
main
  ├─ 0042-user-api               (мержим первым)
  └─ 0043-user-ui                (создаём после merge первой)
```

### Один Issue = один PR

**ЗАПРЕЩЕНО** создавать отдельный PR на каждый Issue.

**Правило:** Группа связанных Issues → одна ветка → один PR.

**Исключение:** Минорные изолированные правки (опечатки, форматирование) — допустим один Issue = один PR.

### Граничные случаи Review и Merge

**SSOT:** [standard-review.md § 6](../review/standard-review.md#6-граничные-случаи)

Граничные случаи, связанные с ревью и merge (закрытие без merge, провал CI, revert после merge) — см. SSOT.

---

## Скиллы

*Нет скиллов.*
