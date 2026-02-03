---
description: Инструкции для работы с GitHub
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/README.md
---

# Инструкции /.github/.instructions/

Инструкции для работы с GitHub: Issues, Pull Requests, Releases, Labels, Workflows и другие объекты.

**Полезные ссылки:**
- [.github](../README.md)

**Содержание:** GitHub объекты, шаблоны, workflows, labels.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [Вложенные области](#вложенные-области) | — | Подобласти инструкций |
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для этой области |

```
/.github/.instructions/
├── .scripts/                           # Скрипты автоматизации
├── codeowners/                         # Инструкции для CODEOWNERS
├── issue-templates/                    # Инструкции для ISSUE_TEMPLATE/
├── issues/                             # Инструкции для GitHub Issues
├── labels/                             # Инструкции для labels/
├── milestones/                         # Инструкции для milestones/
├── pr-template/                        # Инструкции для PR template
├── projects/                           # Инструкции для GitHub Projects
├── pull-requests/                      # Инструкции для GitHub PR
├── releases/                           # Инструкции для releases/
├── workflows-files/                    # Инструкции для workflows/
├── README.md                           # Этот файл (индекс)
├── standard-development-workflow.md    # TODO: добавить описание
├── standard-github.md                  # TODO: добавить описание
└── standard-release-workflow.md        # TODO: добавить описание
```

---

## Вложенные области

Инструкции разделены на подобласти:

| Область | Описание | Индекс |
|---------|----------|--------|
| [.scripts/](./.scripts/) | Скрипты автоматизации | [README](./.scripts/README.md) |
| [codeowners/](./codeowners/) | Инструкции для CODEOWNERS | [README](./codeowners/README.md) |
| [issue-templates/](./issue-templates/) | Инструкции для ISSUE_TEMPLATE/ | [README](./issue-templates/README.md) |
| [issues/](./issues/) | Инструкции для GitHub Issues | [README](./issues/README.md) |
| [labels/](./labels/) | Инструкции для labels/ | [README](./labels/README.md) |
| [milestones/](./milestones/) | Инструкции для milestones/ | [README](./milestones/README.md) |
| [pr-template/](./pr-template/) | Инструкции для PR template | [README](./pr-template/README.md) |
| [projects/](./projects/) | Инструкции для GitHub Projects | [README](./projects/README.md) |
| [pull-requests/](./pull-requests/) | Инструкции для GitHub PR | [README](./pull-requests/README.md) |
| [releases/](./releases/) | Инструкции для releases/ | [README](./releases/README.md) |
| [workflows-files/](./workflows-files/) | Инструкции для workflows/ | [README](./workflows-files/README.md) |

---

# 1. Стандарты

## 1.1. Стандарт CODEOWNERS

Синтаксис, правила и паттерны для файла `.github/CODEOWNERS`.

**Оглавление:**
- [Назначение](./codeowners/standard-codeowners.md#1-назначение)
- [Расположение](./codeowners/standard-codeowners.md#2-расположение)
- [Синтаксис](./codeowners/standard-codeowners.md#3-синтаксис)
- [Правила приоритета](./codeowners/standard-codeowners.md#4-правила-приоритета)
- [Типичные паттерны](./codeowners/standard-codeowners.md#5-типичные-паттерны)

**Инструкция:** [codeowners/standard-codeowners.md](./codeowners/standard-codeowners.md)

---

## 1.2. Стандарт Development Workflow

Полный цикл разработки: Issue → Branch → Development → PR → Review → Merge.

**Оглавление:**
- [Полный цикл разработки](./standard-development-workflow.md#1-полный-цикл-разработки)
- [Создание Issue](./standard-development-workflow.md#2-стадия-1-создание-issue)
- [Создание ветки](./standard-development-workflow.md#3-стадия-2-создание-ветки)
- [Разработка](./standard-development-workflow.md#4-стадия-3-разработка)
- [Commit правила](./standard-development-workflow.md#5-стадия-4-commit-правила)
- [Создание PR](./standard-development-workflow.md#6-стадия-5-создание-pull-request)
- [Code Review](./standard-development-workflow.md#7-стадия-6-code-review)
- [Merge](./standard-development-workflow.md#8-стадия-7-merge)

**Инструкция:** [standard-development-workflow.md](./standard-development-workflow.md)

---

## 1.3. Стандарт Release Workflow

Процесс релиза: подготовка → создание → публикация → hotfix → rollback.

**Оглавление:**
- [Зона ответственности](./standard-release-workflow.md#1-зона-ответственности)
- [Полный цикл релиза](./standard-release-workflow.md#2-полный-цикл-релиза)
- [Подготовка релиза](./standard-release-workflow.md#3-подготовка-релиза)
- [Создание релиза](./standard-release-workflow.md#4-создание-релиза)
- [Публикация на production](./standard-release-workflow.md#5-публикация-на-production)
- [Hotfix-релиз](./standard-release-workflow.md#6-hotfix-релиз)
- [Rollback процесс](./standard-release-workflow.md#7-rollback-процесс)
- [Связь с Development Workflow](./standard-release-workflow.md#8-связь-с-development-workflow)

**Инструкция:** [standard-release-workflow.md](./standard-release-workflow.md)

---

# 2. Воркфлоу

*Нет воркфлоу.*

<!-- Шаблон для добавления воркфлоу:
## 2.1. Создание {объекта}

{Описание — одно предложение.}

**Оглавление:**
- [{Раздел}](./create-{object}.md#раздел)

**Инструкция:** [create-{object}.md](./create-{object}.md)
-->

---

# 3. Валидация

*Нет валидаций.*

<!-- Шаблон для добавления валидации:
## 3.1. Валидация {объекта}

{Описание — одно предложение.}

**Оглавление:**
- [{Раздел}](./validation-{object}.md#раздел)

**Инструкция:** [validation-{object}.md](./validation-{object}.md)
-->

---

# 4. Скрипты

*Нет скриптов.*

<!-- Шаблон для добавления скриптов:
| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [{script}.py](./.scripts/{script}.py) | {описание} | [{инструкция}.md](./{инструкция}.md) |
-->

---

# 5. Скиллы

*Нет скиллов.*

<!-- Шаблон для добавления скиллов:
| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/{skill}](/.claude/skills/{skill}/SKILL.md) | {описание} | [{инструкция}.md](./{инструкция}.md) |
-->
