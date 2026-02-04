# План валидации инструкций .github/

Последовательная проверка инструкций на соответствие желаемому поведению.

## Оглавление

- [Контекст](#контекст)
- [Анализ SSOT-ссылок](#анализ-ssot-ссылок)
- [Порядок валидации](#порядок-валидации)
- [Волна 1: Базовые стандарты](#волна-1-базовые-стандарты-0-1-ssot-ссылки)
- [Волна 2: PR, Milestone, Release](#волна-2-pr-milestone-release)
- [Волна 3: Issue и Project](#волна-3-issue-и-project)
- [Волна 4: Workflow-документы](#волна-4-workflow-документы)
- [Волна 5: Навигация](#волна-5-навигация)
- [Чек-лист](#чек-лист)

---

## Контекст

**Задача:** Провалидировать все инструкции в `.github/.instructions/`, чтобы они соответствовали желаемому поведению.

**Принцип сортировки:**
1. Минимальное количество SSOT-ссылок = читать первыми (самодостаточные документы)
2. При равном количестве ссылок — анализировать "важность" для зависимых файлов

**Что проверяем:**
- Корректность описанных процессов
- Согласованность с реальным workflow
- Отсутствие противоречий между стандартами  
- Полнота информации

---

## Анализ SSOT-ссылок

| Файл | SSOT-ссылки | Зависит от | Статус |
|------|-------------|------------|--------|
| `standard-codeowners.md` | 0 | — | ✅ |
| `standard-labels.md` | 0 | — | ✅ |
| `standard-pr-template.md` | 0 | — | ✅ |
| `standard-issue-template.md` | 1 | standard-labels.md | ✅ |
| `standard-pull-request.md` | 2 | standard-labels.md, standard-pr-template.md | ⏳ |
| `standard-milestone.md` | 2 | standard-issue.md↔, standard-release.md↔ | ⏳ |
| `standard-issue.md` | 5 | labels, issue-template, **pull-request**, **milestone**, project | ⏳ |
| `standard-release.md` | 2 | standard-milestone.md, standard-pull-request.md | ⏳ |
| `standard-workflow-file.md` | 4 | standard-development-workflow.md, standard-release-workflow.md, standard-release.md | ⏳ |
| `standard-project.md` | 4 | standard-issue.md, standard-pull-request.md, standard-milestone.md, standard-workflow-file.md | ⏳ |
| `standard-development-workflow.md` | 5 | standard-issue.md, standard-pull-request.md, standard-labels.md | ⏳ |
| `standard-release-workflow.md` | 6 | standard-development-workflow.md, standard-release.md, standard-milestone.md, standard-workflow-file.md | ⏳ |
| `standard-github.md` | 11 | Все остальные (навигационный документ) | ⏳ |

> **↔ = циклическая зависимость** — milestone ↔ issue, milestone ↔ release. Решение: валидировать milestone раньше, но помнить о взаимосвязи. 

---

## Порядок валидации

> **Принцип:** Валидировать документ ПОСЛЕ его зависимостей. Issue зависит от PR и Milestone — поэтому Issue идёт после них.

| # | Файл | Волна | Статус |
|---|------|-------|--------|
| 1 | `standard-labels.md` | 1 | ✅ |
| 2 | `standard-pr-template.md` | 1 | ✅ |
| 3 | `standard-codeowners.md` | 1 | ✅ |
| 4 | `standard-issue-template.md` | 1 | ✅ |
| 5 | `standard-pull-request.md` | 2 | ⏳ |
| 6 | `standard-milestone.md` | 2 | ⏳ |
| 7 | `standard-release.md` | 2 | ⏳ |
| 8 | `standard-issue.md` | 3 | ⏳ |
| 9 | `standard-project.md` | 3 | ⏳ |
| 10 | `standard-development-workflow.md` | 4 | ⏳ |
| 11 | `standard-release-workflow.md` | 4 | ⏳ |
| 12 | `standard-workflow-file.md` | 4 | ⏳ |
| 13 | `standard-github.md` | 5 | ⏳ |

---

### Волна 1: Базовые стандарты (0-1 SSOT-ссылки)

Самодостаточные документы — "строительные блоки".

| # | Файл | Приоритет | Обоснование |
|---|------|-----------|-------------|
| 1 | `standard-labels.md` | **Высокий** | Фундамент для всех остальных (issue, pr, templates) |
| 2 | `standard-pr-template.md` | Средний | Используется в standard-pull-request.md |
| 3 | `standard-codeowners.md` | Низкий | Изолированный стандарт |
| 4 | `standard-issue-template.md` | Средний | Зависит только от labels.md |

---

### Волна 2: PR, Milestone, Release

Сущности, от которых зависит Issue.

| # | Файл | Зависит от | Приоритет | Обоснование |
|---|------|------------|-----------|-------------|
| 5 | `standard-pull-request.md` | labels, pr-template | **Высокий** | Issue закрывается через PR |
| 6 | `standard-milestone.md` | ↔issue, ↔release | **Высокий** | Issue привязывается к Milestone |
| 7 | `standard-release.md` | milestone, pull-request | Средний | Release создаётся из Milestone |

> **Циклическая зависимость:** milestone ↔ issue, milestone ↔ release. Валидируем milestone раньше, затем проверим согласованность в issue/release.

---

### Волна 3: Issue и Project

Issue зависит от PR и Milestone (workflow: создать Issue → привязать к Milestone → создать PR → закрыть Issue).

| # | Файл | Зависит от | Приоритет | Обоснование |
|---|------|------------|-----------|-------------|
| 8 | `standard-issue.md` | labels, templates, **PR**, **milestone**, project | **Высокий** | Центральная сущность workflow |
| 9 | `standard-project.md` | issue, pr, milestone | Низкий | GitHub Projects — опционально |

---

### Волна 4: Workflow-документы

Агрегирующие документы, объединяющие сущности в процессы.

| # | Файл | Зависит от | Приоритет | Обоснование |
|---|------|------------|-----------|-------------|
| 10 | `standard-development-workflow.md` | issue, pr, labels | **Высокий** | Полный цикл разработки |
| 11 | `standard-release-workflow.md` | development, release, milestone | **Высокий** | Процесс релиза |
| 12 | `standard-workflow-file.md` | development, release-workflow | Средний | YAML-файлы GitHub Actions |

---

### Волна 5: Навигация

| # | Файл | Зависит от | Приоритет | Обоснование |
|---|------|------------|-----------|-------------|
| 13 | `standard-github.md` | Все остальные | Последний | Навигационный документ |

---

## Чек-лист

### Волна 1: Базовые стандарты

- [x] **1. standard-labels.md** — система меток
  - [x] Категории и naming convention корректны
  - [x] Правила применения однозначны
  - [x] Примеры достаточны

- [x] **2. standard-pr-template.md** — шаблон PR
  - [x] Обязательные секции определены
  - [x] Placeholder-ы понятны
  - [x] Примеры полные

- [x] **3. standard-codeowners.md** — правила CODEOWNERS
  - [x] Синтаксис описан полно
  - [x] Паттерны корректны
  - [x] Примеры для проекта релевантны

- [x] **4. standard-issue-template.md** — YAML-шаблоны Issues
  - [x] Формат YAML корректен
  - [x] Связь с labels согласована
  - [x] Примеры рабочие

### Волна 2: PR, Milestone, Release

- [ ] **5. standard-pull-request.md** — работа с PR
  - [ ] Жизненный цикл полон
  - [ ] Merge стратегии корректны
  - [ ] Code review процесс понятен
  - [ ] Связь с Issue (закрытие) описана

- [ ] **6. standard-milestone.md** — управление milestones
  - [ ] Типы milestones определены
  - [ ] Связь с release согласована
  - [ ] CLI команды актуальны

- [ ] **7. standard-release.md** — версионирование и releases
  - [ ] SemVer описан корректно
  - [ ] Changelog формат понятен
  - [ ] Связь с milestone/PR согласована

### Волна 3: Issue и Project

- [ ] **8. standard-issue.md** — управление Issues
  - [ ] Жизненный цикл полон
  - [ ] Связь с PR (закрытие) корректна
  - [ ] Связь с Milestone корректна
  - [ ] CLI команды актуальны

- [ ] **9. standard-project.md** — GitHub Projects
  - [ ] Scope документа корректен
  - [ ] CLI команды рабочие
  - [ ] Связь с issue/pr согласована

### Волна 4: Workflow-документы

- [ ] **10. standard-development-workflow.md** — полный цикл разработки
  - [ ] Все стадии согласованы с зависимыми стандартами
  - [ ] Нет противоречий с issue.md / pr.md
  - [ ] Граничные случаи покрыты

- [ ] **11. standard-release-workflow.md** — процесс релиза
  - [ ] Все стадии согласованы с release.md / milestone.md
  - [ ] Hotfix процесс полон
  - [ ] Rollback описан корректно

- [ ] **12. standard-workflow-file.md** — GitHub Actions YAML
  - [ ] Структура YAML полна
  - [ ] Триггеры описаны корректно
  - [ ] Best practices актуальны

### Волна 5: Навигация

- [ ] **13. standard-github.md** — навигационный индекс
  - [ ] Все SSOT-ссылки работают
  - [ ] Принципы не противоречат стандартам
  - [ ] Нет устаревшей информации

---

## Инструкции по валидации

Для каждого файла:

1. **Прочитать файл полностью**
2. **Проверить:**
   - Содержимое соответствует желаемому поведению?
   - Есть ли неясности или двусмысленности?
   - Все ли аспекты покрыты?
3. **Отметить проблемы:**
   - Что нужно изменить?
   - Что нужно добавить?
   - Что нужно удалить?
4. **Принять решение:**
   - ✅ Одобрено — без изменений
   - ⚠️ Требуются правки — указать что именно
5. **Отметить в чек-листе**

---

## Результаты валидации

*Заполняется в процессе работы.*

### Волна 1: Базовые стандарты

| Файл | Статус | Комментарий |
|------|--------|-------------|
| standard-labels.md | ✅ | Инструкции созданы, метки без префиксов |
| standard-pr-template.md | ✅ | validation + скрипт + pre-commit хук |
| standard-codeowners.md | ✅ | validation + скрипт + pre-commit хук + CODEOWNERS файл |
| standard-issue-template.md | ✅ | v1.2: связь с labels, Issue Templates созданы (6 шт.) |

### Волна 2: PR, Milestone, Release

| Файл | Статус | Комментарий |
|------|--------|-------------|
| standard-pull-request.md | ⏳ | — |
| standard-milestone.md | ⏳ | — |
| standard-release.md | ⏳ | — |

### Волна 3: Issue и Project

| Файл | Статус | Комментарий |
|------|--------|-------------|
| standard-issue.md | ⏳ | — |
| standard-project.md | ⏳ | — |

### Волна 4: Workflow-документы

| Файл | Статус | Комментарий |
|------|--------|-------------|
| standard-development-workflow.md | ⏳ | — |
| standard-release-workflow.md | ⏳ | — |
| standard-workflow-file.md | ⏳ | — |

### Волна 5: Навигация

| Файл | Статус | Комментарий |
|------|--------|-------------|
| standard-github.md | ⏳ | — |

---

## Созданные драфты рекомендаций

*Заполняется по мере завершения валидации.*

| Стандарт | Драфт рекомендаций |
|----------|-------------------|
| standard-labels.md | *Инструкции созданы, рекомендации не требуются* |
| standard-pr-template.md | *Инструкции созданы, рекомендации не требуются* |
| standard-codeowners.md | *Инструкции созданы, рекомендации не требуются* |
| standard-issue-template.md | *Инструкции созданы, рекомендации не требуются* |
| standard-issue.md | [recommendations-standard-issue.md](./2026-02-03-recommendations-standard-issue.md) |
| standard-release.md | [recommendations-standard-release.md](./2026-02-03-recommendations-standard-release.md) |
| standard-pull-request.md | [recommendations-standard-pull-request.md](./2026-02-03-recommendations-standard-pull-request.md) |
| standard-milestone.md | [recommendations-standard-milestone.md](./2026-02-03-recommendations-standard-milestone.md) |
| standard-workflow-file.md | [recommendations-standard-workflow-file.md](./2026-02-03-recommendations-standard-workflow-file.md) |
| standard-project.md | [recommendations-standard-project.md](./2026-02-03-recommendations-standard-project.md) |
| standard-development-workflow.md | [recommendations-standard-development-workflow.md](./2026-02-03-recommendations-standard-development-workflow.md) |
| standard-release-workflow.md | [recommendations-standard-release-workflow.md](./2026-02-03-recommendations-standard-release-workflow.md) |
| standard-github.md | [recommendations-standard-github.md](./2026-02-03-recommendations-standard-github.md) |
