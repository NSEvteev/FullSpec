---
description: Инструкции для работы с GitHub — issues, branches, commits, PRs, review, releases, actions, security. Индекс всех подпапок.
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
├── actions/                            # Инструкции для GitHub Actions
│   └── security/                       # Безопасность (Dependabot, CodeQL)
├── branches/                           # Инструкции для ветвления
├── codeowners/                         # Инструкции для CODEOWNERS
├── commits/                            # Инструкции для коммитов
├── development/                        # Инструкции для локальной разработки
├── issues/                             # Инструкции для GitHub Issues
│   └── issue-templates/                # Инструкции для ISSUE_TEMPLATE/
├── labels/                             # Инструкции для labels/
├── milestones/                         # Инструкции для milestones/
├── projects/                           # Инструкции для GitHub Projects
├── pull-requests/                      # Инструкции для GitHub PR
│   └── pr-template/                    # Инструкции для PR template
├── releases/                           # Инструкции для releases/
├── review/                             # Инструкции для Code Review и Merge
├── sync/                               # Инструкции для синхронизации
├── README.md                           # Этот файл (индекс)
└── standard-github-workflow.md         # Полный цикл разработки
```

---

## Вложенные области

Инструкции разделены на подобласти:

| Область | Описание | Индекс |
|---------|----------|--------|
| [.scripts/](./.scripts/) | Скрипты автоматизации | [README](./.scripts/README.md) |
| [actions/](./actions/) | Инструкции для GitHub Actions | [README](./actions/README.md) |
| [branches/](./branches/) | Инструкции для ветвления | [README](./branches/README.md) |
| [codeowners/](./codeowners/) | Инструкции для CODEOWNERS | [README](./codeowners/README.md) |
| [commits/](./commits/) | Инструкции для коммитов | [README](./commits/README.md) |
| [development/](./development/) | Инструкции для локальной разработки | [README](./development/README.md) |
| [issues/](./issues/) | Инструкции для GitHub Issues | [README](./issues/README.md) |
| [labels/](./labels/) | Инструкции для labels/ | [README](./labels/README.md) |
| [milestones/](./milestones/) | Инструкции для milestones/ | [README](./milestones/README.md) |
| [projects/](./projects/) | Инструкции для GitHub Projects | [README](./projects/README.md) |
| [pull-requests/](./pull-requests/) | Инструкции для GitHub PR | [README](./pull-requests/README.md) |
| [releases/](./releases/) | Инструкции для releases/ | [README](./releases/README.md) |
| [review/](./review/) | Инструкции для Code Review и Merge | [README](./review/README.md) |
| [sync/](./sync/) | Инструкции для синхронизации | [README](./sync/README.md) |

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

## 1.2. Стандарт GitHub Workflow

Полный цикл разработки: Подготовка → Issue → Branch → Development → PR → Review → Merge → Release.

**Оглавление:**
- [Полный цикл разработки](./standard-github-workflow.md#1-полный-цикл-разработки)
- [Фаза 0: Подготовка инфраструктуры](./standard-github-workflow.md#2-фаза-0-подготовка-инфраструктуры)
- [Стадия 1: Планирование и создание Issues](./standard-github-workflow.md#3-стадия-1-планирование-и-создание-issues)
- [Стадия 2: Группировка Issues](./standard-github-workflow.md#4-стадия-2-группировка-issues)
- [Стадия 3: Создание ветки](./standard-github-workflow.md#5-стадия-3-создание-ветки)
- [Стадия 4: Разработка](./standard-github-workflow.md#6-стадия-4-разработка)
- [Стадия 5: Commit правила](./standard-github-workflow.md#7-стадия-5-commit-правила)
- [Стадия 6: Создание Pull Request](./standard-github-workflow.md#8-стадия-6-создание-pull-request)
- [Стадия 7: Code Review](./standard-github-workflow.md#9-стадия-7-code-review)
- [Стадия 8: Merge](./standard-github-workflow.md#10-стадия-8-merge)
- [Стадия 9: Синхронизация](./standard-github-workflow.md#11-стадия-9-синхронизация-с-main)
- [Стадия 10: Релиз](./standard-github-workflow.md#12-стадия-10-релиз)
- [Блокирующие условия](./standard-github-workflow.md#13-блокирующие-условия)
- [Граничные случаи](./standard-github-workflow.md#14-граничные-случаи)

**Инструкция:** [standard-github-workflow.md](./standard-github-workflow.md)

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
