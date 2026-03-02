---
description: Стандарт Code Review и Merge — критерии одобрения, типы комментариев, squash merge, автоматизация.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/review/README.md
---

# Стандарт Review и Merge

Версия стандарта: 1.1

Code Review процесс, merge стратегии, Branch Protection Rules.

**Полезные ссылки:**
- [Инструкции](./README.md)
- [Стандарт PR](../pull-requests/standard-pull-request.md) — создание PR
- [Стандарт Workflow](../standard-github-workflow.md) — полный цикл

**SSOT-зависимости:**
- [standard-pull-request.md](../pull-requests/standard-pull-request.md) — PR создаётся перед ревью
- [standard-branching.md](../branches/standard-branching.md) — жизненный цикл ветки после merge
- [standard-commit.md](../commits/standard-commit.md) — формат коммитов при исправлении замечаний
- [validation-development.md](../development/validation-development.md) — обязательный шаг перед созданием PR
- [standard-development.md](../development/standard-development.md) — контекст: review после development
- [standard-sync.md](../sync/standard-sync.md) — синхронизация main после merge
- [standard-github-workflow.md](../standard-github-workflow.md) — полный цикл (стадии 7-8: Review, Merge)
- [standard-release.md](../releases/standard-release.md) — revert, hotfix, Release Freeze
- [code-reviewer AGENT.md](/.claude/agents/code-reviewer/AGENT.md) — агент ревью кода
- [specs/.instructions/analysis/review/standard-review.md](/.specs/.instructions/analysis/review/standard-review.md) — **процесс ревью кода** (что проверять, RV-N, P1/P2/P3, review.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-review.md](./validation-review.md) |
| Создание | [create-merge.md](./create-merge.md) |
| Модификация | *Не требуется (процесс)* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Code Review процесс](#2-code-review-процесс)
- [3. Merge стратегии](#3-merge-стратегии)
- [4. Branch Protection Rules](#4-branch-protection-rules)
- [5. Блокирующие условия](#5-блокирующие-условия)
- [6. Граничные случаи](#6-граничные-случаи)
- [7. CLI команды](#7-cli-команды)

---

## 1. Назначение

Review и Merge — финальные этапы жизненного цикла PR:
1. PR прошёл все автопроверки (CI)
2. Code review выполнен
3. PR готов к слиянию в main

**Предшествующий этап:** Создание PR → [standard-pull-request.md](../pull-requests/standard-pull-request.md)

---

## 2. Code Review процесс

Ревью состоит из двух этапов: локальное ревью агентом **до** создания PR и комментарии к PR **после** создания.

### Этап 1: Локальное ревью (до создания PR)

**Перед созданием PR — запустить агента-ревьюера локально:**

```bash
# Агент анализирует diff между текущей веткой и main
/review
```

**Агент проверяет:**
- Соответствие требованиям Issue
- Качество кода (читаемость, принципы)
- Очевидные ошибки (опечатки, debug-код)
- TODO/FIXME без Issue
- Покрытие тестами (содержательные критерии — в [code-reviewer AGENT.md](/.claude/agents/code-reviewer/AGENT.md), Проходы 4-5)

> **Процесс ревью кода** (что проверять, RV-N, P1/P2/P3, review.md):
> [specs/.instructions/analysis/review/standard-review.md](/.specs/.instructions/analysis/review/standard-review.md)
> Этот раздел описывает только GitHub-механику. Содержательный процесс ревью — в specs SSOT выше.

**Управление статусами:** [`chain_status.py`](/specs/.instructions/.scripts/chain_status.py) — SSOT-модуль для переходов статусов analysis chain.

**Результат:** Агент выводит замечания локально.

**Процесс исправления:**
1. Прочитать замечания агента
2. Внести исправления в код
3. Закоммитить изменения (→ [standard-commit.md](../commits/standard-commit.md))
4. Повторить `/review` (опционально, если исправления значительные)
5. Только после устранения всех замечаний — создавать PR

**Цель:** PR создаётся уже проверенным, без тривиальных проблем.

### Этап 2: Комментарии к PR (после создания)

**После создания PR — агент пишет комментарии:**

```bash
# Агент анализирует PR и пишет комментарии в GitHub
/review 123
```

**Что делает агент:**
1. Получает diff PR через `gh pr diff 123`
2. Анализирует изменения
3. Пишет комментарии через `gh pr comment 123 --body "..."`
4. Комментарии сохраняются в истории PR

**Важно:** Агент работает под учёткой пользователя GitHub. Формального "Approved by @reviewer" не будет. После проверки комментариев агента пользователь ДОЛЖЕН вручную выполнить approve. Агент НЕ выполняет approve автоматически — он только пишет комментарии.

### Approve и Merge

После прочтения комментариев агента:

```bash
# Шаг 1: Approve (ОБЯЗАТЕЛЬНО перед merge)
gh pr review 123 --approve

# Шаг 2: Merge (выполняется ПОСЛЕ approve)
gh pr merge 123 --squash

# Если комментарии требуют исправлений — внести правки, запушить, повторить ревью
```

### Ревью от других людей (команда > 1)

Если в команде есть другие люди (не только автор + агент):

**Как назначить reviewers:**
```bash
gh pr create --reviewer @username1,@username2
gh pr edit 123 --add-reviewer @username
```

**Типы ревью:**

| Тип | Команда | Когда использовать |
|-----|---------|-------------------|
| **Approve** | `gh pr review {PR} --approve` | Изменения готовы к merge |
| **Request changes** | `gh pr review {PR} --request-changes --body "..."` | Требуются исправления |
| **Comment** | `gh pr review {PR} --comment --body "..."` | Вопрос или некритичное замечание |

### Ревью Draft PR

Draft PR можно ревьюить до перевода в Ready:
- Комментарии разрешены: `gh pr review {номер} --comment --body "..."`
- Approve и Request changes НЕ требуются (PR в статусе черновика)
- После перевода в Ready (`gh pr ready {номер}`) — полноценное ревью с approve

**SSOT Draft PR:** [standard-pull-request.md § 2](../pull-requests/standard-pull-request.md#2-жизненный-цикл-pr)

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

---

## 3. Merge стратегии

**Default стратегия: Squash Merge**

```bash
gh pr merge 123 --squash
```

**Что такое Squash Merge:**
Все коммиты из PR объединяются в **один** коммит при слиянии в main. Например:
- Было: 5 коммитов ("начал", "исправил опечатку", "добавил тест", "ой забыл", "финал")
- Стало: 1 коммит `feature: add login endpoint (#123)`

**Причины использования:**
- Чистая история main (один коммит на фичу)
- Легко откатить изменения целиком
- Удобно для автоматического changelog

**Формат итогового commit message:**

```
{type}: {краткое описание} (#{PR номер})

{Опционально: детали из body PR}

Closes #{issue номера}
```

Примеры:
```
# Минимальный (GitHub генерирует автоматически из title):
feature: add user authentication (#10)

# С деталями и несколькими Issues:
feature: add user authentication (#10)

- Добавлена форма логина (#42)
- Реализована валидация (#43)
- Создан API эндпоинт (#44)

Closes #42, #43, #44
```

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
3. Нет активных "Requested changes" от reviewers
4. Нет merge conflicts

**Когда использовать auto-merge:**
- CI workflows запущены, но ещё не завершены (ожидание 5+ минут)
- Нужно мержить вне рабочего времени (например, настроить auto-merge перед уходом)
- PR требует approval от других ревьюеров, которые ещё не ответили

**Когда НЕ использовать:**
- Все условия уже выполнены (CI пройден, approvals получены) → мержить вручную сразу
- Срочный hotfix → мержить вручную

**Если условия не выполнены:** PR остаётся в очереди auto-merge до выполнения всех условий.

**Граничные случаи auto-merge:**

| Ситуация | Поведение |
|----------|-----------|
| CI перезапустился после включения auto-merge | Ожидание завершения нового CI |
| Reviewer отозвал approval | Merge блокируется до получения нового approval |
| В PR добавлены новые коммиты | Auto-merge отключается, нужно включить заново |
| Появились merge conflicts | Auto-merge блокируется до разрешения конфликтов |

**Отмена auto-merge:**
```bash
gh pr merge 123 --disable-auto
```

### Разрешение конфликтов

Если при merge возникают конфликты:

1. **Локально обновить ветку:**
   ```bash
   git checkout 0001-oauth2-authorization
   git pull origin main
   # Разрешить конфликты вручную в редакторе
   git add .
   git commit -m "resolve: merge conflicts with main"
   git push
   ```
2. **Повторить попытку merge через PR** (конфликты должны исчезнуть)
3. Если конфликты затрагивают более 3 файлов ИЛИ более 50 строк ИЛИ автоматическое слияние невозможно — сообщить пользователю: "Конфликты требуют ручного разрешения"

### После merge

**Автоматически (на GitHub):**
- Remote feature-ветка удаляется
- Все Issues закрываются (если указаны `Closes #42`, `Closes #43`, `Closes #44`)
- PR переходит в статус "Merged"

**Локальная очистка:** → [standard-branching.md § 3](../branches/standard-branching.md#3-жизненный-цикл-ветки) (SSOT жизненного цикла ветки)

**Синхронизация main:** → [standard-sync.md](../sync/standard-sync.md) (обновить локальный main после merge)

---

## 4. Branch Protection Rules

**Назначение:** Защита main от некачественных изменений.

**Рекомендуемые правила для main:**

| Правило | Описание | Рекомендация |
|---------|----------|--------------|
| **Require a pull request before merging** | Запретить прямые коммиты | Включить всегда |
| **Require approvals** | Минимум N одобрений для merge | 1 для соло, 2 для команды |
| **Require status checks to pass** | CI должен пройти | Включить всегда |
| **Require branches to be up to date** | Ветка актуальна с main | Включить всегда |
| **Require conversation resolution** | Все комментарии resolved | Для команд 2+ человек |
| **Require signed commits** | Подписанные коммиты | Для публичных проектов |

**Настройка:** → [initialization.md § 7](/.structure/initialization.md#7-настройка-branch-protection-rules) (одноразовая настройка нового репозитория)

---

## 5. Блокирующие условия

### Запрет merge

PR **не может** быть смержен, если:

| Условие | Описание |
|---------|----------|
| **CI fails** | Хотя бы одна автоматическая проверка провалилась |
| **Requested changes** | Хотя бы один reviewer запросил изменения (и не снял блокировку) |
| **Merge conflicts** | Есть конфликты с целевой веткой |
| **Draft status** | PR в статусе Draft |
| **Branch protection** | Не выполнены правила защиты ветки |

### Запрет push в main

> **SSOT:** Полный workflow → [standard-github-workflow.md](../standard-github-workflow.md)

**Прямые коммиты в main запрещены.**

```bash
# ❌ Запрещено
git checkout main
git commit -m "fix: quick fix"
git push origin main
```

**Правильно:**
```bash
# 1. Создать Issue
gh issue create --title "Quick fix" --label bug --label medium

# 2. Создать ветку от main (NNNN — номер analysis chain)
git checkout -b 0042-quick-fix

# 3. Внести изменения
git add .
git commit -m "fix: quick fix"
git push -u origin 0042-quick-fix

# 4. Создать PR
gh pr create --title "fix: quick fix" --body "Closes #130"

# 5. Мержить через PR
gh pr merge --squash
```

---

## 6. Граничные случаи

### Закрытие PR без merge

> **SSOT:** Управление жизненным циклом PR → [standard-pull-request.md](../pull-requests/standard-pull-request.md)

**Сценарий:** PR больше не актуален, задача отменена.

**Процесс:**
1. Закрыть PR:
   ```bash
   gh pr close {номер-PR} --comment "Задача отменена"
   ```
2. Закрыть связанные Issues:
   ```bash
   gh issue close 42 --comment "Отменено"
   gh issue close 43 --comment "Отменено"
   ```
3. Удалить feature-ветку:
   ```bash
   git branch -D 0001-oauth2-authorization
   git push origin --delete 0001-oauth2-authorization
   ```

### Провал CI checks

**Сценарий:** PR создан, но автоматические проверки (CI) завершились с ошибкой.

**Процесс:**
1. Открыть PR: `gh pr view {номер} --web`
2. Перейти в раздел "Checks" (внизу страницы PR)
3. Найти провалившуюся проверку (красный крестик)
4. Нажать "Details" → прочитать логи ошибки
5. Исправить ошибку локально (в feature-ветке)
6. Закоммитить и запушить:
   ```bash
   git add .
   git commit -m "fix: resolve CI error"
   git push
   ```
7. CI перезапустится автоматически
8. Дождаться успешного прохождения всех checks

### Откат после merge (revert)

> **См. также:** Hotfix-релиз → [standard-release.md](../releases/standard-release.md), тип коммита "revert" → [standard-commit.md § 7](../commits/standard-commit.md)

**Сценарий:** PR был смержен, но обнаружена критическая ошибка.

**Вариант 1: Через PR (рекомендуется):**
1. Открыть PR: `gh pr view {номер} --web`
2. В UI GitHub: нажать "Revert" (создаст новый PR с откатом)
3. Смержить revert-PR: `gh pr merge {revert-PR-number} --squash`

**Вариант 2: Через CLI (для срочных hotfix):**
```bash
git checkout main
git pull origin main
git revert {commit-hash-of-merge}
git push origin main
# ⚠️ ИСКЛЮЧЕНИЕ: Это единственный случай прямого коммита в main.
# Использовать ТОЛЬКО для критичных откатов production.
# В остальных случаях — создавать revert-PR (Вариант 1).
```

**После revert:**
1. Создать новый Issue для исправления проблемы
2. Разработать фикс в новой ветке → создать новый PR

**Важно:** Revert НЕ удаляет историю — он создаёт новый коммит, отменяющий изменения.

### Граничные случаи Review и Merge

**SSOT:** [standard-review.md § 6](#6-граничные-случаи) — этот раздел.

---

## 7. CLI команды

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
# Squash merge (по умолчанию)
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

### Закрытие PR

```bash
# Закрыть без merge
gh pr close 123 --comment "Причина"

# Переоткрыть
gh pr reopen 123
```

### Обработка ошибок

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `HTTP 403: Resource not accessible` | Нет прав на репозиторий | Проверить `gh auth status`, выполнить `gh auth login` |
| `pull request is in clean status` | PR уже смержен или закрыт | Проверить статус: `gh pr view {номер}` |
| `merge conflict` | Конфликты с целевой веткой | См. [§ 3. Разрешение конфликтов](#разрешение-конфликтов) |
| `required status checks must pass` | CI не пройден | Дождаться успешного CI или исправить ошибки |
| `review is required` | Нет approve | Выполнить `gh pr review {номер} --approve` |

---

## Скиллы

*Нет скиллов.*
