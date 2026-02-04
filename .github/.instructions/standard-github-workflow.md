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

**Принцип SSOT:**

> Этот документ описывает **последовательность шагов** воркфлоу.
> Детали каждого шага (форматы, правила, примеры) — в зависимых стандартах.
>
> **Запрещено:** дублировать правила из зависимых стандартов.
> **Обязательно:** ссылаться на SSOT для деталей.

## Оглавление

- [1. Полный цикл разработки](#1-полный-цикл-разработки)
- [2. Стадия 1: Планирование и создание Issues](#2-стадия-1-планирование-и-создание-issues)
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

1. ПЛАНИРОВАНИЕ
   └─ Создать Issues для фичи/области (#42, #43, #44)
   └─ Сгруппировать связанные Issues (одна фича = один PR)

2. СОЗДАНИЕ ВЕТКИ
   └─ git checkout -b {type}/{description}-{issue-numbers}
   └─ Пример: feature/auth-42-43-44

3. РАЗРАБОТКА
   └─ make setup   (если первый запуск после клонирования)
   └─ make dev     (запуск сервисов для разработки)
   └─ Написание кода (все Issues из группы)
   └─ Локальные тесты: make test

4. КОММИТЫ
   └─ git add .
   └─ git commit -m "{type}: {description}"
   └─ Pre-commit hooks выполняются автоматически
   └─ Если hooks провалились → исправить → повторить commit

5. ЛОКАЛЬНОЕ РЕВЬЮ
   └─ /review-branch (агент проверяет код до создания PR)
   └─ Исправить замечания → повторить коммит

6. СОЗДАНИЕ PR
   └─ git push -u origin feature/auth-42-43-44
   └─ gh pr create --title "{type}: {description}" --body "..."
   └─ В body: "Closes #42, #43, #44"

7. CODE REVIEW
   └─ /review-pr {номер} (агент пишет комментарии к PR)
   └─ Если есть замечания → исправить → git push → повтор

8. MERGE
   └─ Все CI checks пройдены
   └─ gh pr merge {номер} --squash
   └─ Feature-ветка удаляется автоматически
   └─ Все Issues (#42, #43, #44) закрываются автоматически

9. СИНХРОНИЗАЦИЯ
   └─ git checkout main
   └─ git pull origin main
   └─ Локальная main синхронизирована с remote
```

**Принципы:**
- **Одна фича/область — группа Issues — одна ветка — один PR**
- **Прямые коммиты в main запрещены** (только через PR)
- **Feature-ветки создаются ТОЛЬКО от актуальной main.** Перед созданием ветки: `git checkout main && git pull origin main && git checkout -b {type}/{description}-{issue-numbers}`
- **Merge в main только после прохождения pre-commit hooks локально**
- **Все Issues группы закрываются одним PR** (через "Closes #42, #43, #44")

---

## 2. Стадия 1: Планирование и создание Issues

**SSOT:** [standard-issue.md](./issues/standard-issue.md)

### Процесс

**1. Декомпозиция фичи на Issues:**

Разбить фичу/область на отдельные задачи. Пример:
- #42: Добавить форму логина
- #43: Добавить валидацию полей
- #44: Создать эндпоинт POST /auth/login

**2. Группировка Issues:**

Issues группируются по фиче/области. Одна группа = один PR.

**SSOT группировки:** [standard-pull-request.md § 6](./pull-requests/standard-pull-request.md#6-связь-с-issues)

### Выход из стадии

Issues созданы → группа сформирована (например, #42, #43, #44) → переход к созданию ветки.

> **Создание Issue:** см. [standard-issue.md](./issues/standard-issue.md)

---

## 3. Стадия 2: Создание ветки

### Процесс

```bash
# Переключиться на main и обновить
git checkout main
git pull origin main

# Создать ветку от main (для группы Issues)
git checkout -b {type}/{description}-{issue-numbers}
```

**Пример:** `git checkout -b feature/auth-42-43-44`

> **Формат, префиксы, примеры:** см. [§ 10. Ветвление и именование](#10-ветвление-и-именование)

### Выход из стадии

Ветка создана → локальная среда готова к разработке → переход к разработке.

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

1. **Локальное ревью** — `/review-branch` (исправить замечания до создания PR)
2. **Push ветки** — `git push -u origin feature/auth-42-43-44`
3. **Создать PR** — `gh pr create --title "..." --body "..." --label ...`

> **Формат title, body, labels, CLI команды:** см. [standard-pull-request.md](./pull-requests/standard-pull-request.md)

### Выход из стадии

PR создан → автопроверки запущены → готовность к code review.

---

## 7. Стадия 6: Code Review

**SSOT:** [standard-review.md § 2](./review/standard-review.md#2-code-review-процесс)

### Процесс

1. **Ревью агентом** — `/review-pr {номер-PR}`
2. **Цикл исправлений** — правки → push → повторное ревью
3. **Ревью от людей** (если команда > 1) — `gh pr edit {номер} --add-reviewer @user`

> **Этапы ревью, типы, цикл исправлений:** см. SSOT

### Выход из стадии

Ревью пройдено → все CI checks пройдены → готовность к merge.

---

## 8. Стадия 7: Merge

**SSOT:** [standard-review.md § 3](./review/standard-review.md#3-merge-стратегии)

### Процесс

```bash
# Squash merge (default)
gh pr merge {номер} --squash
```

> **Условия merge, стратегии, auto-merge:** см. SSOT

### После merge

**Автоматически:** Feature-ветка удаляется, Issues закрываются, PR → "Merged".

**Локальная очистка:**
```bash
git checkout main
git pull origin main
git branch -d feature/auth-42-43-44
```

### Выход из стадии

PR смержен → Issues закрыты → код в main → готовность к синхронизации.

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
  ├─ feature/auth-42-43-44        (группа Issues)
  ├─ fix/upload-errors-50-51      (группа Issues)
  ├─ docs/deploy-guide-70         (один Issue)
  └─ task/deps-update-60          (один Issue)
```

**Правила:**
- **main — защищённая ветка.** Прямые коммиты запрещены (только через PR).
- **Feature-ветки создаются от main** (не от других feature-веток).
- **Feature-ветки удаляются после merge** (автоматически или вручную).
- **main всегда стабильна** (все изменения прошли review и CI).
- **Одна ветка = одна фича/область = группа Issues**

### Branch Naming Convention

**Формат:**
```
{type}/{description}-{issue-numbers}
```

**Компоненты:**

| Компонент | Правило | Пример |
|-----------|---------|--------|
| `{type}` | Префикс по основному типу группы | `feature`, `fix`, `docs` |
| `{description}` | 2-3 слова, описывающие фичу/область | `auth`, `upload-errors` |
| `{issue-numbers}` | Номера Issues через дефис | `42-43-44`, `50-51`, `70` |

**Префиксы по типам:**

| Метка Issues | Префикс ветки | Примеры |
|--------------|---------------|---------|
| `feature` | `feature/` | `feature/auth-42-43-44` |
| `bug` | `fix/` | `fix/upload-errors-50-51` |
| `task` | `task/` | `task/deps-update-60` |
| `docs` | `docs/` | `docs/deploy-guide-70-71` |
| `refactor` | `refactor/` | `refactor/handlers-80-81-82` |

**Запрещённые форматы:**

| Формат ❌ | Причина |
|----------|---------|
| `add-auth` | Нет типа и номеров Issues |
| `feature-add-auth` | Нет номеров Issues |
| `feature/add-auth` | Нет номеров Issues |
| `feature/42_43_auth` | Подчёркивания вместо дефисов |

### Вложенные ветки

**ЗАПРЕЩЕНО:**
```
feature/auth-42-43
  └─ feature/auth-ui-44   ❌ НЕ создавать ветки от других feature-веток
```

**Правильно — объединить в одну ветку:**
```
main
  └─ feature/auth-42-43-44   ✅ Все связанные Issues в одной ветке
```

**Если Issues слишком разные для одного PR:**
1. Сгруппировать по логике (разные фичи = разные ветки)
2. Мержить последовательно в main

```
main
  ├─ feature/auth-backend-42-43    (мержим первым)
  └─ feature/auth-frontend-44-45   (создаём от свежего main после merge)
```

---

## 11. Merge стратегии

**SSOT:** [standard-review.md § 3](./review/standard-review.md#3-merge-стратегии)

**Default:** Squash Merge (`gh pr merge {номер} --squash`)

Детали (что такое Squash Merge, альтернативные стратегии, формат commit message) — см. SSOT.

---

## 12. Блокирующие условия

### Запрет merge

**SSOT:** [standard-review.md § 5](./review/standard-review.md#5-блокирующие-условия) — условия merge, auto-merge, разрешение конфликтов.

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

**SSOT:**
- PR: [standard-pull-request.md § 10](./pull-requests/standard-pull-request.md#10-граничные-случаи) — hotfix, длительная разработка, координация PR
- Review: [standard-review.md § 6](./review/standard-review.md#6-граничные-случаи) — revert, провал CI, закрытие без merge

---

## Скиллы

*Будут созданы после семантического анализа.*
