# Реструктуризация GitHub-документации

Перераспределение контента между стандартами: workflow, issues, pull-requests, review, releases, actions.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Статус выполнения](#статус-выполнения)
- [Принятые решения](#принятые-решения)

---

## Контекст

**Задача:** Реструктуризация документации `.github/.instructions/`
**Почему создан:** Текущее распределение контента не соответствует логике разделения ответственности
**Статус:** ВЫПОЛНЕНО (2026-02-04)

**Выполненные изменения:**
- `.github/.instructions/standard-development-workflow.md` → переименован в `standard-github-workflow.md`
- `.github/.instructions/standard-github.md` → удалён (дублировал workflow)
- `.github/.instructions/issue-templates/` → перенесён в `issues/issue-templates/`
- `.github/.instructions/pr-template/` → перенесён в `pull-requests/pr-template/`
- `.github/.instructions/standard-release-workflow.md` → перенесён в `releases/`
- `.github/.instructions/review/` → создан с `standard-review.md`
- `.github/.instructions/releases/` → создан (README.md)
- `.github/.instructions/actions/` → создан с `security/`
- `.github/.instructions/projects/` → создан (README.md)
- `pull-requests/pr-template/standard-draft-pr.md` → создан

---

## Содержание

### Финальная архитектура

```
.github/.instructions/
│
├── standard-github-workflow.md        ← HIGH-LEVEL воркфлоу: ссылки на этапы
│
├── [НЕЗАВИСИМЫЕ]
│   ├── codeowners/
│   │   ├── README.md
│   │   ├── standard-codeowners.md
│   │   └── validation-codeowners.md
│   ├── labels/
│   │   ├── README.md
│   │   ├── standard-labels.md
│   │   ├── modify-labels.md
│   │   └── validation-labels.md
│   └── milestones/
│       ├── README.md
│       └── standard-milestone.md
│
├── [ЭТАПЫ ЖИЗНЕННОГО ЦИКЛА]
│   │
│   ├── issues/                        ← этап 1: создание задач
│   │   ├── README.md
│   │   ├── standard-issue.md
│   │   └── issue-templates/           ← ПЕРЕНЕСЕНО из корня
│   │       ├── README.md
│   │       ├── standard-issue-template.md
│   │       └── validation-type-templates.md
│   │
│   ├── pull-requests/                 ← этап 2: создание и работа с PR
│   │   ├── README.md
│   │   ├── standard-pull-request.md   ← ОБНОВЛЕНО (ссылка на review/)
│   │   └── pr-template/               ← ПЕРЕНЕСЕНО из корня
│   │       ├── README.md
│   │       ├── standard-pr-template.md
│   │       ├── standard-draft-pr.md   ← СОЗДАН
│   │       └── validation-pr-template.md
│   │
│   ├── review/                        ← этап 3: ревью и merge (СОЗДАН)
│   │   ├── README.md
│   │   └── standard-review.md         ← СОЗДАН
│   │
│   └── releases/                      ← этап 4: релиз (СОЗДАН)
│       ├── README.md
│       ├── standard-release.md        ← существовал
│       └── standard-release-workflow.md ← ПЕРЕНЕСЕНО из корня
│
├── [АВТОМАТИЗАЦИЯ]
│   ├── actions/                       ← СОЗДАН
│   │   ├── README.md
│   │   └── security/                  ← СОЗДАН
│   │       └── README.md
│   └── workflows-files/
│       ├── README.md
│       └── standard-workflow-file.md
│
├── [ДОПОЛНИТЕЛЬНО]
│   └── projects/                      ← СОЗДАН
│       ├── README.md
│       └── standard-project.md        ← существовал
│
└── [СЛУЖЕБНЫЕ]
    └── .scripts/
        └── *.py
```

### Ответственности документов

| Документ | Отвечает за |
|----------|-------------|
| **standard-github-workflow.md** | HIGH-LEVEL: последовательность этапов + ссылки |
| **issues/** | Создание и управление задачами |
| **issues/issue-templates/** | YAML-шаблоны Issues |
| **pull-requests/** | Issues → ветка → разработка → PR → "Ready for review" |
| **pull-requests/pr-template/** | PR template и Draft PR |
| **review/** | Code Review → Merge в main + Branch Protection |
| **releases/** | Release Workflow + Версионирование |
| **actions/** | GitHub Actions |
| **actions/security/** | Dependabot, CodeQL, Secret Scanning |
| **projects/** | GitHub Projects |

### Что НЕ включено

| Функция | Причина |
|---------|---------|
| Discussions | Не нужно для соло + агенты |
| Wiki | Не используется |
| Packages | Отложено |

---

## Статус выполнения

### Выполненные операции

| # | Операция | Статус |
|---|----------|--------|
| 1 | Переименовать `standard-development-workflow.md` → `standard-github-workflow.md` | ✅ |
| 2 | Удалить `standard-github.md` (дубликат) | ✅ |
| 3 | Создать `review/` с README.md и standard-review.md | ✅ |
| 4 | Создать `releases/` с README.md | ✅ |
| 5 | Создать `actions/` с README.md | ✅ |
| 6 | Создать `actions/security/` с README.md | ✅ |
| 7 | Создать `projects/` с README.md | ✅ |
| 8 | Перенести `issue-templates/` → `issues/issue-templates/` | ✅ |
| 9 | Перенести `pr-template/` → `pull-requests/pr-template/` | ✅ |
| 10 | Перенести `standard-release-workflow.md` → `releases/` | ✅ |
| 11 | Создать `standard-draft-pr.md` в `pr-template/` | ✅ |
| 12 | Обновить `standard-pull-request.md` (убрать review/merge, добавить ссылку) | ✅ |
| 13 | Обновить `standard-github-workflow.md` (ссылки на review/) | ✅ |
| 14 | Обновить все внутренние ссылки | ✅ |
| 15 | Обновить README.md затронутых папок | ✅ |

### Результаты валидации

**Команда:** `/links-validate --path .github/.instructions/`

**Ошибки (ожидаемые — файлы запланированы к созданию):**
- `validation-*.md`, `create-*.md`, `modify-*.md` — воркфлоу-файлы (TODO)
- `standard-security.md` — TODO
- `standard-project.md` якоря — TODO (файл существует, но якоря не совпадают)

**Исправленные ошибки:**
- Все ссылки на `standard-development-workflow.md` обновлены
- Все ссылки на перенесённые папки обновлены
- Все ссылки на `standard-release-workflow.md` обновлены
- Якоря в `standard-github-workflow.md` обновлены на review/

---

### Граничные случаи — распределение

| Кейс | Куда |
|------|------|
| PR без связанного Issue | pull-requests/ |
| Hotfix в production | pull-requests/ |
| Длительная разработка (синхронизация) | pull-requests/ |
| Координация зависимых PR | pull-requests/ |
| Один Issue = один PR (запрещено) | pull-requests/ |
| Закрытие PR без merge | review/ |
| Провал CI checks | review/ |
| Откат после merge (revert) | review/ |
| Branch Protection Rules | review/ |

---

### CLI команды — распределение

| Команда | Куда |
|---------|------|
| `gh pr create` | pull-requests/ |
| `gh pr edit` | pull-requests/ |
| `gh pr ready` | pull-requests/ |
| `gh pr view`, `gh pr list`, `gh pr diff` | pull-requests/ |
| `gh pr review` | review/ |
| `gh pr merge` | review/ |
| `gh pr close` | review/ |
| `gh release create` | releases/ |

---

## Принятые решения

| Вопрос | Решение |
|--------|---------|
| **projects/** | ✅ Создать `projects/standard-project.md` |
| **Жизненный цикл PR** | ✅ Разделить: до "Ready" → PR, после → review/ |
| **Draft PR** | ✅ В `pr-template/standard-draft-pr.md` |
| **actions/security/** | ✅ Создать сейчас |
| **issue-templates/** | ✅ Перенести в `issues/issue-templates/` |
| **pr-template/** | ✅ Перенести в `pull-requests/pr-template/` |
| **standard-release-workflow.md** | ✅ Перенести в `releases/` |
| **standard-github.md** | ✅ Удалить (дублирует workflow) |

---

## TODO (следующие шаги)

| Задача | Приоритет |
|--------|-----------|
| Создать `actions/security/standard-security.md` | Низкий |
| Исправить якоря в `projects/README.md` | Низкий |
| Удалить временный файл `123.md` | Низкий |
