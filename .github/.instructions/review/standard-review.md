---
description: Стандарт Code Review и Merge в GitHub
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/review/README.md
---

# Стандарт Review и Merge

Версия стандарта: 1.0

Code Review процесс, merge стратегии, Branch Protection Rules.

**Полезные ссылки:**
- [Инструкции](./README.md)
- [Стандарт PR](../pull-requests/standard-pull-request.md) — создание PR
- [Стандарт Workflow](../standard-github-workflow.md) — полный цикл

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | *Будет создан* |
| Создание | *Не требуется* |
| Модификация | *Не требуется* |

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
/review-branch
```

**Агент проверяет:**
- Соответствие требованиям Issue
- Качество кода (читаемость, принципы)
- Очевидные ошибки (опечатки, debug-код)
- TODO/FIXME без Issue
- Покрытие тестами

**Результат:** Агент выводит замечания локально. Исправить **до** создания PR.

**Цель:** PR создаётся уже проверенным, без тривиальных проблем.

### Этап 2: Комментарии к PR (после создания)

**После создания PR — агент пишет комментарии:**

```bash
# Агент анализирует PR и пишет комментарии в GitHub
/review-pr 123
```

**Что делает агент:**
1. Получает diff PR через `gh pr diff 123`
2. Анализирует изменения
3. Пишет комментарии через `gh pr comment 123 --body "..."`
4. Комментарии сохраняются в истории PR

**Важно:** Агент работает под вашей учёткой GitHub. Формального "Approved by @reviewer" не будет — вы сами делаете approve после проверки комментариев.

### Approve и Merge

После прочтения комментариев агента:

```bash
# Если всё хорошо — мержим
gh pr merge 123 --squash

# Если нужны правки — исправляем, пушим, повторяем ревью
```

### Ревью от других людей (команда > 1)

Если в команде есть другие люди (не только вы + агент):

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

**Если условия не выполнены:** PR остаётся в очереди auto-merge до выполнения всех условий.

**Отмена auto-merge:**
```bash
gh pr merge 123 --disable-auto
```

### Разрешение конфликтов

Если при merge возникают конфликты:

1. **Локально обновить ветку:**
   ```bash
   git checkout feature/auth-42-43-44
   git pull origin main
   # Разрешить конфликты вручную в редакторе
   git add .
   git commit -m "resolve: merge conflicts with main"
   git push
   ```
2. **Повторить попытку merge через PR** (конфликты должны исчезнуть)
3. Если конфликты сложные — попросить автора PR их разрешить

### После merge

- Feature-ветка автоматически удаляется
- Все Issues закрываются (если указаны `Closes #42`, `Closes #43`, `Closes #44`)
- PR переходит в статус "Merged"

---

## 4. Branch Protection Rules

**Назначение:** Защита main от некачественных изменений.

**Рекомендуемые правила для main:**

| Правило | Описание | Рекомендация |
|---------|----------|--------------|
| **Require a pull request before merging** | Запретить прямые коммиты | ✅ Включить |
| **Require approvals** | Минимум N одобрений для merge | 1 для соло, 2 для команды |
| **Require status checks to pass** | CI должен пройти | ✅ Включить |
| **Require branches to be up to date** | Ветка актуальна с main | ✅ Включить |
| **Require conversation resolution** | Все комментарии resolved | По желанию |
| **Require signed commits** | Подписанные коммиты | По желанию |

**Настройка через GitHub UI:**
1. Settings → Branches → Branch protection rules
2. Add rule → Branch name pattern: `main`
3. Выбрать нужные правила
4. Save changes

**Настройка через CLI (gh):**
```bash
# Посмотреть текущие правила
gh api repos/{owner}/{repo}/branches/main/protection

# Настройка через API — см. GitHub REST API docs
```

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

# 2. Создать ветку от main
git checkout -b fix/130-quick-fix

# 3. Внести изменения
git add .
git commit -m "fix: quick fix"
git push -u origin fix/130-quick-fix

# 4. Создать PR
gh pr create --title "fix: quick fix" --body "Closes #130"

# 5. Мержить через PR
gh pr merge 130 --squash
```

---

## 6. Граничные случаи

### Закрытие PR без merge

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
   git branch -D feature/auth-42-43
   git push origin --delete feature/auth-42-43
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

**Сценарий:** PR был смержен, но обнаружена критическая ошибка.

**Процесс:**
1. Создать revert-коммит в main:
   ```bash
   git checkout main
   git pull origin main
   git revert {commit-hash-of-merge}
   git push origin main
   ```
2. Альтернатива через GitHub UI:
   - Открыть PR: `gh pr view {номер} --web`
   - В UI GitHub: нажать "Revert" (создаст новый PR с откатом)
   - Смержить revert-PR: `gh pr merge {revert-PR-number} --squash`
3. Создать новый Issue для исправления проблемы
4. Разработать фикс в новой ветке → создать новый PR

**Важно:** Revert НЕ удаляет историю — он создаёт новый коммит, отменяющий изменения.

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

### Закрытие PR

```bash
# Закрыть без merge
gh pr close 123 --comment "Причина"

# Переоткрыть
gh pr reopen 123
```

---

## Скиллы

*Нет скиллов.*
