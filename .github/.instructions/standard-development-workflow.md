---
description: Полный цикл разработки от Issue до Merge в GitHub
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/README.md
---

# Стандарт Development Workflow

Версия стандарта: 1.0

Полный цикл разработки: Issue → Branch → Development → PR → Review → Merge.

**Полезные ссылки:**
- [Инструкции .github](./README.md)
- [Инициализация проекта](/.structure/initialization.md) — первые шаги после клонирования

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | *Будет создан* |
| Создание | *Будет создан* |
| Модификация | *Будет создан* |

**Зависимые стандарты:**

| Область | Документ | Что регулирует |
|---------|----------|----------------|
| Issues | [standard-issue.md](./issues/standard-issue.md) | Создание и управление задачами |
| Pull Requests | [standard-pull-request.md](./pull-requests/standard-pull-request.md) | Создание, review, merge PR |
| Labels | [standard-labels.md](./labels/standard-labels.md) | Категоризация задач и PR |

## Оглавление

- [1. Полный цикл разработки](#1-полный-цикл-разработки)
- [2. Стадия 1: Создание Issue](#2-стадия-1-создание-issue)
- [3. Стадия 2: Создание ветки](#3-стадия-2-создание-ветки)
- [4. Стадия 3: Разработка](#4-стадия-3-разработка)
- [5. Стадия 4: Commit правила](#5-стадия-4-commit-правила)
- [6. Стадия 5: Создание Pull Request](#6-стадия-5-создание-pull-request)
- [7. Стадия 6: Code Review](#7-стадия-6-code-review)
- [8. Стадия 7: Merge](#8-стадия-7-merge)
- [9. Стадия 8: Синхронизация с main](#9-стадия-8-синхронизация-с-main)
- [10. Ветвление и именование](#10-ветвление-и-именование)
- [11. Merge стратегии](#11-merge-стратегии)
- [12. Блокирующие условия](#12-блокирующие-условия)
- [13. Граничные случаи](#13-граничные-случаи)

---

## 1. Полный цикл разработки

```
┌───────────────────────────────────────────────────────────────┐
│                    FULL DEVELOPMENT CYCLE                       │
└───────────────────────────────────────────────────────────────┘

1. СОЗДАНИЕ ISSUE
   └─ gh issue create --title "..." --label type:* --label priority:*
   └─ Получаем #123

2. СОЗДАНИЕ ВЕТКИ
   └─ git checkout -b {type}/{issue-number}-{description}
   └─ Пример: feature/123-add-auth

3. РАЗРАБОТКА
   └─ make setup   (если первый запуск после клонирования)
   └─ make dev     (запуск сервисов для разработки)
   └─ Написание кода
   └─ Локальные тесты: make test

4. КОММИТЫ
   └─ git add .
   └─ git commit -m "{type}: {description}"
   └─ Pre-commit hooks выполняются автоматически
   └─ Если hooks провалились → исправить → повторить commit

5. СОЗДАНИЕ PR
   └─ git push -u origin feature/123-add-auth
   └─ gh pr create --title "{type}: {description}" --body "..." \
        --label type:* --label priority:* --reviewer @user
   └─ В body обязательно: "Closes #123"

6. CODE REVIEW
   └─ Reviewer: gh pr review 123 --approve | --request-changes
   └─ Если request-changes → внести правки → git push → повтор ревью

7. MERGE
   └─ Все CI checks пройдены
   └─ Получен минимум 1 approval (обязательно для PR с `priority:critical` или breaking changes)
   └─ gh pr merge 123 --squash
   └─ Feature-ветка удаляется автоматически
   └─ Issue #123 закрывается автоматически

8. СИНХРОНИЗАЦИЯ
   └─ git checkout main
   └─ git pull origin main
   └─ Локальная main синхронизирована с remote
```

**Принципы:**
- **Одна задача — один Issue — одна ветка — один PR**
- **Прямые коммиты в main запрещены** (только через PR)
- **Feature-ветки создаются ТОЛЬКО от актуальной main.** Перед созданием ветки: `git checkout main && git pull origin main && git checkout -b {type}/{issue-number}-{description}`
- **Merge в main только после прохождения pre-commit hooks локально**

---

## 2. Стадия 1: Создание Issue

**SSOT:** [standard-issue.md](./issues/standard-issue.md)

### Процесс

```bash
# Создать Issue
gh issue create --title "Добавить авторизацию пользователей" \
  --body "..." \
  --label type:feature \
  --label priority:high \
  --assignee @me
```

### Выход из стадии

Issue создан → получен номер (например, #123) → переход к созданию ветки.

> **Обязательные элементы:** см. [standard-issue.md § 4](./issues/standard-issue.md#4-правила-создания)

---

## 3. Стадия 2: Создание ветки

### Процесс

```bash
# Переключиться на main
git checkout main

# Обновить main
git pull origin main

# Создать ветку от main
git checkout -b {type}/{issue-number}-{description}
```

### Правила именования

**Формат:**
```
{type}/{issue-number}-{description}
```

**Префиксы (соответствуют метке `type:*`):**

| Метка Issue | Префикс ветки | Пример |
|-------------|---------------|--------|
| `type:feature` | `feature/` | `feature/123-add-auth` |
| `type:bug` | `fix/` | `fix/124-null-pointer` |
| `type:task` | `task/` | `task/125-update-deps` |
| `type:docs` | `docs/` | `docs/126-readme-deploy` |
| `type:refactor` | `refactor/` | `refactor/127-error-handling` |

**Description:**
- 2-4 слова из title Issue
- Kebab-case
- Только английские буквы
- Без номера Issue в конце description (номер уже в префиксе)

**Примеры:**

| Title Issue | Ветка |
|-------------|-------|
| Добавить авторизацию пользователей | `feature/123-add-auth` |
| Исправить ошибку загрузки файлов | `fix/124-file-upload` |
| Обновить README с инструкциями деплоя | `docs/125-readme-deploy` |

### Выход из стадии

Ветка создана → локальная среда готова к разработке → переход к разработке.

**Важно:** Создание ветки — триггер для назначения assignee (если не назначен):
```bash
gh issue edit 123 --add-assignee @me
```

---

## 4. Стадия 3: Разработка

### Первый запуск после клонирования

```bash
# Установить pre-commit hooks (ОБЯЗАТЕЛЬНО!)
make setup
```

> **SSOT:** [initialization.md](/.structure/initialization.md)

### Ежедневная разработка

```bash
# Запустить сервисы для разработки
make dev

# Разработка в редакторе (VSCode, etc)

# Локальные тесты
make test

# Остановить сервисы
make stop
```

### Правила

| Правило | Описание |
|---------|----------|
| **Разработка ТОЛЬКО в feature-ветке** | Никогда не коммитить напрямую в main |
| **Pre-commit hooks должны быть установлены** | `make setup` после клонирования |
| **Тестировать локально перед push** | `make test` |
| **Не создавать вложенные ветки** | Feature-ветка всегда от main |

### Выход из стадии

Код написан → тесты пройдены локально → готовность к коммиту.

---

## 5. Стадия 4: Commit правила

### Формат Conventional Commits

```
{type}({scope}): {description}

{body}

{footer}
```

**Обязательные элементы:**
- `{type}` — тип изменения
- `{description}` — краткое описание (до 70 символов, нижний регистр, без точки)

**Опциональные элементы:**
- `{scope}` — область кода (auth, api, frontend)
- `{body}` — детальное описание (через пустую строку после первой)
- `{footer}` — ссылки на Issues, breaking changes

### Типы коммитов

| Тип | Когда использовать | Пример |
|-----|-------------------|--------|
| `feat` | Новая функциональность | `feat(auth): add JWT validation` |
| `fix` | Исправление бага | `fix(api): handle null response` |
| `docs` | Изменения документации | `docs(readme): update install steps` |
| `refactor` | Рефакторинг без изменения функциональности | `refactor(handlers): extract validation logic` |
| `test` | Добавление/изменение тестов | `test(auth): add unit tests for login` |
| `chore` | Технические задачи (зависимости, конфиги) | `chore: update dependencies` |
| `ci` | Изменения CI/CD | `ci: add lint workflow` |
| `perf` | Улучшение производительности | `perf(db): optimize query with index` |

### Процесс коммита

```bash
# Добавить изменения в staging
git add .

# Создать коммит
git commit -m "feat(auth): add user authentication"
```

**Pre-commit hooks выполняются автоматически:**
1. Линтинг
2. Форматирование
3. Валидация (если настроено)

**Если hooks провалились:**
1. Коммит НЕ создан (Git блокирует создание коммита при провале pre-commit)
2. Прочитать вывод ошибок pre-commit в терминале
3. Исправить ошибки в коде, указанные в выводе
4. Повторить `git add .`
5. Повторить команду `git commit -m "тот же message"` (коммит создастся только после прохождения всех hooks)
6. Повторять шаги 2-5 до успешного прохождения

**Важно:** Коммит НЕ создастся, пока все hooks не пройдут успешно. НЕ использовать `git commit --amend` — коммит ещё не существует.

### Правила коммитов

| Правило | Пример ✅ | Пример ❌ |
|---------|----------|----------|
| Нижний регистр | `feat: add login` | `Feat: Add login` |
| Без точки в конце | `fix: resolve error` | `fix: resolve error.` |
| Начинать с глагола | `docs: update readme` | `docs: readme updated` |
| Не более 70 символов в subject | `feat(auth): add JWT` | `feat(auth): add JWT authentication with refresh tokens and role-based access control` |

### Выход из стадии

Коммит создан → изменения зафиксированы → готовность к push и созданию PR.

---

## 6. Стадия 5: Создание Pull Request

**SSOT:** [standard-pull-request.md](./pull-requests/standard-pull-request.md)

### Процесс

```bash
# Push ветки в remote
git push -u origin feature/123-add-auth

# Создать PR
gh pr create \
  --title "feat(auth): add user authentication" \
  --body "$(cat <<'EOF'
## Summary
- Добавлен эндпоинт POST /api/auth/login
- Реализована JWT-авторизация
- Добавлены unit-тесты

## Related Issue
Closes #123

## How to test
1. make dev
2. POST /api/auth/login с credentials
3. Проверить получение JWT токена
EOF
)" \
  --label type:feature \
  --label priority:high \
  --reviewer @user1
```

> **Обязательные элементы:** см. [standard-pull-request.md § 3](./pull-requests/standard-pull-request.md#3-создание-pull-request)

### Автоматические проверки

После создания PR автоматически запускаются:
1. **Pre-commit hooks** (уже выполнены локально перед push)
2. **CI workflows** (если настроены в `.github/workflows/` с триггером `pull_request`)
3. **Branch protection rules** (если настроены в Settings → Branches)

### Выход из стадии

PR создан → автопроверки запущены → готовность к code review.

---

## 7. Стадия 6: Code Review

### Назначение reviewers

**Кто назначается:**
- Минимум 1 reviewer обязателен для PR с меткой `priority:critical` (любой тип) ИЛИ при наличии секции "Breaking changes" в body PR
- Для остальных PR назначение reviewer опционально
- CODEOWNERS (автоматически, если настроено в `.github/CODEOWNERS`)

**Как назначить:**
```bash
# При создании PR
gh pr create --reviewer @user1,@user2

# После создания
gh pr edit 123 --add-reviewer @user
```

### Процесс ревью

**Reviewer проверяет:**
1. Соответствие требованиям Issue
2. Качество кода (читаемость, принципы из [standard-principles.md](/.instructions/standard-principles.md))
3. Покрытие тестами
4. Документация обновлена (если нужно)
5. Нет конфликтов с main

**Типы ревью:**

| Тип | Команда | Когда использовать |
|-----|---------|-------------------|
| **Approve** | `gh pr review 123 --approve` | Изменения готовы к merge |
| **Request changes** | `gh pr review 123 --request-changes --body "..."` | Требуются исправления |
| **Comment** | `gh pr review 123 --comment --body "..."` | Вопрос или некритичное замечание |

### Цикл исправлений

**Если reviewer запросил изменения:**

1. **Внести правки в feature-ветке:**
   ```bash
   # Находимся в feature/123-add-auth
   # Исправляем код

   git add .
   git commit -m "fix: address review comments"
   git push
   ```

2. **GitHub автоматически:**
   - Уведомляет reviewer о новых изменениях
   - Помечает старые комментарии как "Outdated" (если затронутые строки изменились)

3. **Reviewer проводит повторное ревью:**
   ```bash
   gh pr review 123 --approve
   ```

### Выход из стадии

PR одобрен (approve) → все CI checks пройдены → готовность к merge.

---

## 8. Стадия 7: Merge

### Условия для merge

**Обязательные:**
1. Все CI checks пройдены (status: success)
2. Нет merge conflicts с целевой веткой (main)
3. Pre-commit hooks пройдены локально перед созданием PR

**Опциональные (если настроены Branch Protection Rules):**
4. Получен минимум N approvals от reviewers (обычно 1)
5. PR не в статусе Draft

### Процесс merge

**Default стратегия: Squash Merge**

```bash
# Интерактивно (с выбором стратегии)
gh pr merge 123

# Явно squash merge
gh pr merge 123 --squash

# Auto-merge (мержить автоматически, когда условия выполнены)
gh pr merge 123 --auto --squash
```

### После merge

**Автоматически:**
1. Feature-ветка удаляется из remote
2. Issue закрывается (если в PR body было `Closes #123`)
3. PR переходит в статус "Merged"

**Локальная очистка (опционально):**
```bash
# Переключиться на main
git checkout main

# Обновить main
git pull origin main

# Удалить локальную feature-ветку
git branch -d feature/123-add-auth
```

### Выход из стадии

PR смержен → Issue закрыт → код в main → готовность к синхронизации.

---

## 9. Стадия 8: Синхронизация с main

### Процесс

```bash
# Переключиться на main
git checkout main

# Обновить main из remote
git pull origin main

# Проверить статус
git status
# Вывод: On branch main, Your branch is up to date with 'origin/main'
```

### Когда синхронизировать

| Событие | Действие |
|---------|----------|
| После merge своего PR | Обязательно обновить main |
| Перед созданием новой ветки | Обязательно обновить main |
| В конце рабочего дня | Рекомендуется обновить main |
| Другой разработчик смержил PR | Рекомендуется обновить main перед продолжением работы |

### Конфликты при синхронизации

**Если `git pull` завершился с конфликтами:**
- Разрешить конфликты вручную в редакторе
- Выполнить `git add .`
- Выполнить `git commit -m "resolve: merge conflicts with main"`
- **Важно:** Конфликты в main возникают редко, если соблюдать правило "feature-ветки всегда от свежего main"

### Выход из стадии

Main синхронизирован → готовность к новому циклу разработки (создание следующего Issue).

---

## 10. Ветвление и именование

### Структура репозитория

```
main (protected)
  ├─ feature/123-add-auth
  ├─ fix/124-null-pointer
  ├─ docs/125-readme-deploy
  └─ task/126-update-deps
```

**Правила:**
- **main — защищённая ветка.** Прямые коммиты запрещены (только через PR).
- **Feature-ветки создаются от main** (не от других feature-веток).
- **Feature-ветки удаляются после merge** (автоматически или вручную).
- **main всегда стабильна** (все изменения прошли review и CI).

### Branch Naming Convention

**Формат:**
```
{type}/{issue-number}-{description}
```

**Компоненты:**

| Компонент | Правило | Пример |
|-----------|---------|--------|
| `{type}` | Префикс по метке Issue (см. таблицу ниже) | `feature`, `fix`, `docs` |
| `{issue-number}` | Номер Issue в GitHub | `123` |
| `{description}` | 2-4 слова из title Issue в kebab-case | `add-auth`, `null-pointer` |

**Префиксы по типам:**

| Метка Issue | Префикс ветки | Примеры |
|-------------|---------------|---------|
| `type:feature` | `feature/` | `feature/123-add-auth` |
| `type:bug` | `fix/` | `fix/124-handle-timeout` |
| `type:task` | `task/` | `task/125-update-deps` |
| `type:docs` | `docs/` | `docs/126-readme-deploy` |
| `type:refactor` | `refactor/` | `refactor/127-extract-handlers` |

**Запрещённые форматы:**

| Формат ❌ | Причина |
|----------|---------|
| `add-auth` | Нет типа и номера Issue |
| `feature-add-auth` | Нет номера Issue |
| `feature/add-auth` | Нет номера Issue |
| `123-add-auth` | Нет типа |
| `feature/123_add_auth` | Подчёркивания вместо дефисов |

### Вложенные ветки

**ЗАПРЕЩЕНО:**
```
feature/123-parent
  └─ feature/124-child   ❌ НЕ создавать ветки от других feature-веток
```

**Если задача большая:**
1. Разбить Issue на подзадачи (создать отдельные Issues)
2. Создать каждую feature-ветку от main
3. Мержить подзадачи последовательно в main

**Правильно:**
```
main
  ├─ feature/123-add-auth-core     (мержим первым)
  ├─ feature/124-add-auth-ui       (создаём от свежего main после merge 123)
  └─ feature/125-add-auth-tests    (создаём от свежего main после merge 124)
```

---

## 11. Merge стратегии

### Default: Squash Merge

**Используется по умолчанию для всех PR.**

```bash
gh pr merge 123 --squash
```

**Результат:**
- Все коммиты из feature-ветки объединяются в один коммит
- История main линейная и чистая
- Легко откатить изменения целой фичи

**Формат commit message в main:**
```
{type}: {PR title} (#{PR number})
```

Пример:
```
feat: add user authentication (#123)
```

### Альтернативные стратегии

| Стратегия | Команда | Когда использовать |
|-----------|---------|-------------------|
| **Merge commit** | `gh pr merge 123 --merge` | Сохранить полную историю feature-ветки (редко) |
| **Rebase** | `gh pr merge 123 --rebase` | Линейная история без merge-коммитов (не рекомендуется для коллаборативных веток) |

### Рекомендации

**Всегда использовать Squash Merge, кроме:**
- Merge release-веток (если есть release workflow)
- Merge hotfix-веток с критичными исправлениями (если нужна полная история)

---

## 12. Блокирующие условия

### Запрет merge

PR **НЕ МОЖЕТ** быть смержен если:

| Условие | Описание |
|---------|----------|
| **CI checks не пройдены** | Хотя бы одна автоматическая проверка провалилась |
| **Merge conflicts** | Есть конфликты с целевой веткой (main) |
| **Pre-commit hooks провалились** | Локальные проверки не прошли (блокируют commit, а значит и push) |
| **Не получен approval** | Если настроены Branch Protection Rules с требованием N approvals |
| **PR в статусе Draft** | Черновик не может быть смержен до перевода в "Ready" |
| **Requested changes не разрешены** | Reviewer запросил изменения, но approval ещё не дан |

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
gh issue create --title "Quick fix" --label type:bug --label priority:medium

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

## 13. Граничные случаи

### Hotfix в production

**Сценарий:** Критичный баг на production, нужен срочный фикс.

**Процесс:**
1. Создать Issue с `priority:critical`
2. Создать ветку `fix/{issue-number}-{description}` от main
3. Внести исправление + тесты
4. Создать PR с `--label priority:critical`
5. Ускоренное ревью (минимум 1 approval)
6. Merge сразу после approval
7. Deploy в production (через release workflow или вручную)

**Важно:** НЕ пропускать Issue и PR, даже для hotfix.

### Длительная разработка фичи

**Сценарий:** Фича разрабатывается 1+ неделю, main уходит вперёд.

**Процесс:**
1. Регулярно синхронизировать feature-ветку с main:
   ```bash
   git checkout feature/123-long-task
   git pull origin main
   # Разрешить конфликты (если есть)
   git push
   ```
2. При возникновении конфликтов — разрешать сразу, не копить
3. При создании PR — конфликтов не будет

**Рекомендуется:** Синхронизировать feature-ветку с main минимум 1 раз в 2 дня.

### Отмена PR без merge

**Сценарий:** PR больше не актуален, задача отменена.

**Процесс:**
1. Закрыть PR:
   ```bash
   gh pr close 123 --comment "Задача отменена"
   ```
2. Закрыть связанный Issue:
   ```bash
   gh issue close 123 --comment "Отменено (PR #123 закрыт)"
   ```
3. Удалить feature-ветку:
   ```bash
   git branch -D feature/123-cancelled
   git push origin --delete feature/123-cancelled
   ```

### Несколько Issues в одном PR

**Запрещено:** Один PR не должен закрывать несколько независимых Issues.

**Исключение:** Если Issues зависимые (один блокирует другой), можно закрыть несколько:
```markdown
## Related Issue
Closes #123, #124
```

**Рекомендуется:** Один Issue = один PR. Если задача большая — разбить на подзадачи.

### PR без связанного Issue

**Запрещено:** Создавать PR без Issue.

**Исключение:** Минорные правки (опечатки в README, форматирование) — можно без Issue.

**Правильно для минорных правок:**
```bash
# Создать PR без Issue
gh pr create --title "docs: fix typo in README" \
  --body "Fixed typo in installation section" \
  --label type:docs --label priority:low
```

**Важно:** В body НЕ указывать "Closes #...", так как Issue нет.

### Если CI checks провалились

**Сценарий:** PR создан, но автоматические проверки (CI) завершились с ошибкой.

**Процесс:**
1. Открыть PR: `gh pr view {number} --web`
2. Перейти в раздел "Checks" (внизу страницы PR)
3. Найти провалившуюся проверку (красный крестик ❌)
4. Нажать "Details" → прочитать логи ошибки
5. Исправить ошибку локально (в feature-ветке)
6. Закоммитить и запушить:
   ```bash
   git add .
   git commit -m "fix: resolve CI error"
   git push
   ```
7. CI перезапустится автоматически (GitHub повторит проверки для нового коммита)
8. Дождаться успешного прохождения всех checks

### Откат после merge (revert)

**Сценарий:** PR был смержен, но обнаружена критическая ошибка (production сломался, баг высокой критичности).

**Процесс:**
1. Создать revert-коммит в main:
   ```bash
   git checkout main
   git pull origin main
   git revert {commit-hash-of-merge}
   git push origin main
   ```
2. Альтернатива через GitHub UI:
   - Открыть PR: `gh pr view {PR-number} --web`
   - В UI GitHub: нажать "Revert" (создаст новый PR с откатом)
   - Смержить revert-PR: `gh pr merge {revert-PR-number} --squash`
3. Создать новый Issue для исправления проблемы
4. Разработать фикс в новой ветке → создать новый PR

**Важно:** Revert НЕ удаляет историю — он создаёт новый коммит, отменяющий изменения.

### Координация при параллельной разработке

**Сценарий:** Два разработчика работают над зависимыми фичами (например, #123 — backend API, #124 — frontend интеграция).

**Процесс:**
1. **Определить зависимость:** В Issue #124 указать "Зависит от: #123"
2. **Разработчик 1 (backend):**
   - Создаёт PR для #123
   - Помечает PR как Ready (не Draft)
   - Уведомляет Разработчика 2: "PR #X готов к использованию"
3. **Разработчик 2 (frontend):**
   - Начинает работу НЕ дожидаясь merge PR #X (разработка на основе кода из ветки)
   - Локально объединяет ветку Разработчика 1:
     ```bash
     git checkout feature/124-frontend
     git pull origin feature/123-backend
     ```
   - После merge PR #123 в main — синхронизирует свою ветку с main:
     ```bash
     git pull origin main
     ```
4. **Важно:** НЕ мержить зависимый PR (#124) до merge блокирующего PR (#123)

---

## Скиллы

*Будут созданы после семантического анализа.*
