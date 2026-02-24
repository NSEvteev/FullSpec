---
description: Полный цикл разработки от Issue до Merge — этапы, ответственные, инструменты. Покрывает весь GitHub workflow проекта.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/README.md
---

# Стандарт Development Workflow

Версия стандарта: 1.5

Полный цикл разработки: Подготовка → Issue → Branch → Development → PR → Review → Merge → Release.

**Полезные ссылки:**
- [Инструкции .github](./README.md)
- [Инициализация проекта](/.structure/initialization.md) — первые шаги после клонирования

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | — (SSOT-ссылки проверяются через `/links-validate`) |
| Создание | — (оркестратор, не имеет экземпляров) |
| Модификация | — |

**Зоны ответственности:**

> Этот документ — HIGH-LEVEL оркестратор. Каждый объект GitHub описан в своём стандарте.
> Workflow описывает **последовательность шагов**. Детали объектов — в зависимых стандартах.

**Этапы жизненного цикла** (порядок = стадии workflow):

| Стадия | Документ | Зона ответственности |
|--------|----------|---------------------|
| 1. Issues | [standard-issue.md](./issues/standard-issue.md) | Жизненный цикл, создание, свойства, закрытие Issues |
| 1. Issue Templates | [standard-issue-template.md](./issues/issue-templates/standard-issue-template.md) | YAML-шаблоны для создания Issues |
| 3. Branches | [standard-branching.md](./branches/standard-branching.md) | Модель GitHub Flow, naming convention, жизненный цикл ветки, запреты, граничные случаи |
| 4. Development | [standard-development.md](./development/standard-development.md) | Процесс работы в feature-ветке, make-команды, тестирование, локальные проверки качества |
| 5. Commits | [standard-commit.md](./commits/standard-commit.md) | Conventional Commits, типы, scope, body/footer, правила оформления, процесс коммита, pre-commit hooks |
| 6. Pull Requests | [standard-pull-request.md](./pull-requests/standard-pull-request.md) | Создание PR, title/body/labels, связь с Issues, Draft PR |
| 6. PR Template | [standard-pr-template.md](./pull-requests/pr-template/standard-pr-template.md) | Шаблон body PR (.github/PULL_REQUEST_TEMPLATE.md) |
| 7-8. Review & Merge | [standard-review.md](./review/standard-review.md) | Code Review, Merge стратегии, Branch Protection, блокирующие условия |
| 9. Sync | [standard-sync.md](./sync/standard-sync.md) | Триггеры синхронизации, процесс (main и feature-ветки), разрешение конфликтов, запреты |
| 10. Releases | [standard-release.md](./releases/standard-release.md) | Версионирование, Changelog, процесс релиза, hotfix, rollback |

**Независимые объекты:**

| Объект | Документ | Зона ответственности |
|--------|----------|---------------------|
| Labels | [standard-labels.md](./labels/standard-labels.md) | Naming convention, правила применения, добавление/удаление меток |
| Milestones | [standard-milestone.md](./milestones/standard-milestone.md) | Версионирование (SemVer), жизненный цикл, связь с Issues/Releases |
| CODEOWNERS | [standard-codeowners.md](./codeowners/standard-codeowners.md) | Синтаксис CODEOWNERS, автоназначение ревьюеров |
| Projects | [standard-project.md](./projects/standard-project.md) | Канбан-доски, views, fields, автоматизация *(деактивирован — не используется)* |

**Автоматизация:**

| Объект | Документ | Зона ответственности |
|--------|----------|---------------------|
| Actions | [standard-action.md](./actions/standard-action.md) | Структура YAML, триггеры, jobs/steps, secrets, best practices |
| Security | [standard-security.md](./actions/security/standard-security.md) | Dependabot, CodeQL, Secret Scanning, SECURITY.md |
| Secrets | [standard-secrets.md](./actions/security/standard-secrets.md) | Именование, уровни хранения, ротация, категории секретов |

## Оглавление

- [1. Полный цикл разработки](#1-полный-цикл-разработки)
- [2. Фаза 0: Подготовка инфраструктуры](#2-фаза-0-подготовка-инфраструктуры)
- [3. Стадия 1: Планирование и создание Issues](#3-стадия-1-планирование-и-создание-issues)
- [4. Стадия 2: Группировка Issues](#4-стадия-2-группировка-issues)
- [5. Стадия 3: Создание ветки](#5-стадия-3-создание-ветки)
- [6. Стадия 4: Разработка](#6-стадия-4-разработка)
- [7. Стадия 5: Commit правила](#7-стадия-5-commit-правила)
- [8. Стадия 6: Создание Pull Request](#8-стадия-6-создание-pull-request)
- [9. Стадия 7: Code Review](#9-стадия-7-code-review)
- [10. Стадия 8: Merge](#10-стадия-8-merge)
- [11. Стадия 9: Синхронизация с main](#11-стадия-9-синхронизация-с-main)
- [12. Стадия 10: Релиз](#12-стадия-10-релиз)
- [13. Блокирующие условия](#13-блокирующие-условия)
- [14. Граничные случаи](#14-граничные-случаи)

---

## 1. Полный цикл разработки

### Фаза 0: Подготовка инфраструктуры (однократно)

Выполняется **один раз** перед началом работы — см. [§ 2](#2-фаза-0-подготовка-инфраструктуры).

### Фаза 1: Цикл разработки (повторяется)

```
┌───────────────────────────────────────────────────────────────┐
│                    ЦИКЛ РАЗРАБОТКИ (ПОВТОРЯЕТСЯ)               │
└───────────────────────────────────────────────────────────────┘

0. ЗАПУСК РАЗРАБОТКИ (из analysis chain)
   └─ /dev-create {NNNN} → Issues + Milestone + Branch → RUNNING
   └─ → standard-development.md § 0

1. ПЛАНИРОВАНИЕ
   └─ Создать Issues для фичи/области (#42, #43, #44)
   └─ → standard-issue.md

2. ГРУППИРОВКА
   └─ Сгруппировать Issues (одна фича = один PR)
   └─ Назначить группу в Milestone
   └─ → standard-pull-request.md § 6, standard-milestone.md

3. СОЗДАНИЕ ВЕТКИ
   └─ git checkout main && git pull origin main
   └─ git checkout -b {NNNN}-{topic}
   └─ → standard-branching.md

4. РАЗРАБОТКА
   └─ make dev (запуск сервисов)
   └─ Написание кода + локальные тесты: make test
   └─ standard-development.md

5. КОММИТЫ
   └─ git add . && git commit -m "{type}({scope}): {description}"
   └─ Pre-commit hooks выполняются автоматически
   └─ → standard-commit.md

6. СОЗДАНИЕ PR
   └─ /review (локальное ревью до создания PR)
   └─ git push -u origin {branch}
   └─ gh pr create --title "..." --body "Closes #42, #43, #44"
   └─ → standard-pull-request.md

7. CODE REVIEW
   └─ /review {номер} (агент пишет комментарии)
   └─ Исправить замечания → push → повтор
   └─ → standard-review.md § 2

8. MERGE
   └─ gh pr merge {номер} --squash
   └─ Feature-ветка удаляется, Issues закрываются
   └─ → standard-review.md § 3

9. СИНХРОНИЗАЦИЯ
   └─ git checkout main && git pull origin main
   └─ → standard-sync.md

10. РЕЛИЗ (по решению)
    └─ gh release create v1.0.0 --generate-notes
    └─ → standard-release.md
```

### Принципы

- **Одна фича/область — группа Issues — одна ветка — один PR**
- **Прямые коммиты в main запрещены** (только через PR)
- **Feature-ветки создаются ТОЛЬКО от актуальной main** — см. [standard-branching.md](./branches/standard-branching.md)
- **Merge в main только после прохождения pre-commit hooks локально**
- **Все Issues группы закрываются одним PR** (через "Closes #42, #43, #44")
- **Merge в main ≠ деплой.** Код на production попадает ТОЛЬКО через Release — см. [standard-release.md](./releases/standard-release.md)

---

## 2. Фаза 0: Подготовка инфраструктуры

Выполняется **один раз** перед началом работы. Каждый пункт — ссылка на стандарт объекта.

```
┌───────────────────────────────────────────────────────────────┐
│                    ПОДГОТОВКА (ОДНОКРАТНО)                      │
└───────────────────────────────────────────────────────────────┘

1. LABELS
   └─ Создать метки в GitHub по labels.yml
   └─ → standard-labels.md

2. CODEOWNERS
   └─ Настроить .github/CODEOWNERS (зоны ответственности)
   └─ → standard-codeowners.md

3. ISSUE TEMPLATES
   └─ Создать YAML-шаблоны в .github/ISSUE_TEMPLATE/
   └─ → standard-issue-template.md

4. PR TEMPLATE
   └─ Создать .github/PULL_REQUEST_TEMPLATE.md
   └─ → standard-pr-template.md

5. MILESTONES
   └─ Создать первый Milestone (vX.Y.Z)
   └─ → standard-milestone.md

6. GITHUB PROJECTS (опционально)
   └─ Создать канбан-доску (для команд 5+ человек)
   └─ → standard-project.md

7. GITHUB ACTIONS
   └─ Настроить CI workflow (.github/workflows/ci.yml)
   └─ → standard-action.md

8. SECURITY
   └─ Настроить Dependabot, CodeQL, Secret Scanning, SECURITY.md
   └─ → standard-security.md

9. PRE-COMMIT HOOKS
   └─ make setup (обязательно после клонирования)
   └─ → initialization.md
```

---

## 3. Стадия 1: Планирование и создание Issues

**SSOT:** [standard-issue.md](./issues/standard-issue.md)

### Процесс

> **Из analysis chain:** Issues создаются автоматически через `/dev-create` — см. [standard-development.md § 0](./development/standard-development.md#0-запуск-разработки).

Декомпозиция фичи/области на отдельные Issues:
- #42: Добавить форму логина
- #43: Добавить валидацию полей
- #44: Создать эндпоинт POST /auth/login

> **Создание Issue:** см. [standard-issue.md](./issues/standard-issue.md)

### Выход из стадии

Issues созданы → переход к группировке.

---

## 4. Стадия 2: Группировка Issues

**SSOT:** [standard-pull-request.md § 6](./pull-requests/standard-pull-request.md#6-связь-с-issues), [standard-milestone.md](./milestones/standard-milestone.md)

Issues группируются по фиче/области. Одна группа = одна ветка = один PR. Группа назначается в Milestone.

> **Milestones = релизные версии (vX.Y.Z), не спринты.** При разработке с LLM каждый Milestone → GitHub Release. Работа ведётся до достижения результата, а не до окончания временного окна. Подробнее — [standard-milestone.md § 1](./milestones/standard-milestone.md#1-назначение).

> **Критерии группировки, связь с PR:** см. SSOT

### Выход из стадии

Группа сформирована (например, #42, #43, #44) → назначена в Milestone → переход к созданию ветки.

---

## 5. Стадия 3: Создание ветки

**SSOT:** [standard-branching.md](./branches/standard-branching.md)

Создать ветку от актуальной main для группы Issues.

> **Naming convention, процесс, вложенные ветки:** см. SSOT

### Выход из стадии

Ветка создана → локальная среда готова к разработке → переход к разработке.

---

## 6. Стадия 4: Разработка

**SSOT:** [standard-development.md](./development/standard-development.md)

Разработка ведётся в feature-ветке. Процесс, make-команды, тестирование — см. SSOT.

> **Первый запуск после клонирования:** `make setup` — см. [initialization.md](/.structure/initialization.md)

### Выход из стадии

Код написан → тесты пройдены локально (`make test`) → готовность к коммиту.

---

## 7. Стадия 5: Commit правила

**SSOT:** [standard-commit.md](./commits/standard-commit.md)

Формат Conventional Commits: `{type}({scope}): {description}`

> **Типы коммитов, процесс, pre-commit hooks, правила:** см. SSOT

### Выход из стадии

Коммит создан → изменения зафиксированы → готовность к push и созданию PR.

---

## 8. Стадия 6: Создание Pull Request

**SSOT:** [standard-pull-request.md](./pull-requests/standard-pull-request.md)

### Процесс

1. **Локальное ревью** — `/review` (исправить замечания до создания PR)
2. **Push ветки** — `git push -u origin 0001-oauth2-authorization`
3. **Создать PR** — `gh pr create --title "..." --body "..." --label ...`

> **Формат title, body, labels, CLI команды:** см. [standard-pull-request.md](./pull-requests/standard-pull-request.md)

### Выход из стадии

PR создан → автопроверки запущены → готовность к code review.

---

## 9. Стадия 7: Code Review

**SSOT:** [standard-review.md § 2](./review/standard-review.md#2-code-review-процесс)

### Процесс

1. **Ревью агентом** — `/review {номер-PR}`
2. **Цикл исправлений** — правки → push → повторное ревью
3. **Ревью от людей** (если команда > 1) — `gh pr edit {номер} --add-reviewer @user`

> **Этапы ревью, типы, цикл исправлений:** см. SSOT

### Выход из стадии

Ревью пройдено → все CI checks пройдены → готовность к merge.

---

## 10. Стадия 8: Merge

**SSOT:** [standard-review.md](./review/standard-review.md) — merge стратегии (§ 3), блокирующие условия (§ 5), граничные случаи (§ 6).

**Default:** Squash Merge — `gh pr merge {номер} --squash`

> **Стратегии merge, условия, auto-merge, разрешение конфликтов:** см. SSOT.

### После merge

**Автоматически:** Feature-ветка удаляется, Issues закрываются, PR → "Merged".

**Локальная очистка:** см. [standard-branching.md § 3](./branches/standard-branching.md#3-жизненный-цикл-ветки).

> Синхронизация main с remote — см. [§ 11](#11-стадия-9-синхронизация-с-main).

### Выход из стадии

PR смержен → Issues закрыты → код в main → готовность к синхронизации.

---

## 11. Стадия 9: Синхронизация с main

**SSOT:** [standard-sync.md](./sync/standard-sync.md)

Синхронизация локальной main с remote после merge.

> **Процесс, когда синхронизировать, конфликты:** см. SSOT

### Выход из стадии

Main синхронизирован → готовность к релизу или новому циклу разработки.

---

## 12. Стадия 10: Релиз

**SSOT:** [standard-release.md](./releases/standard-release.md)

Создание релиза после накопления изменений в main.

> **Процесс релиза, версионирование, hotfix, rollback, changelog:** см. SSOT

### Выход из стадии

Релиз создан → цикл завершён → переход к новому циклу.

---

## 13. Блокирующие условия

> **Условия merge PR:** см. [standard-review.md § 5](./review/standard-review.md#5-блокирующие-условия)

**Прямые коммиты в main запрещены** — любое изменение проходит полный цикл: Issue → Branch → PR → Review → Merge (см. [§ 1](#1-полный-цикл-разработки)).

---

## 14. Граничные случаи

**SSOT:**
- PR: [standard-pull-request.md § 10](./pull-requests/standard-pull-request.md#10-граничные-случаи) — hotfix, длительная разработка, координация PR
- Review: [standard-review.md § 6](./review/standard-review.md#6-граничные-случаи) — revert, провал CI, закрытие без merge

---

## Скиллы

— (оркестратор не имеет собственных скиллов; скиллы определены в зависимых стандартах)
