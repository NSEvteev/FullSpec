# План валидации инструкций .github/

Последовательная проверка инструкций на соответствие желаемому поведению.

## Оглавление

- [Контекст](#контекст)
- [Анализ SSOT-ссылок](#анализ-ssot-ссылок)
- [Порядок валидации](#порядок-валидации)
- [Волна 1: Базовые стандарты (0 SSOT-ссылок)](#волна-1-базовые-стандарты-0-ssot-ссылок)
- [Волна 2: Минимальные зависимости (1-2 SSOT-ссылки)](#волна-2-минимальные-зависимости-1-2-ssot-ссылки)
- [Волна 3: Средние зависимости (3 SSOT-ссылки)](#волна-3-средние-зависимости-3-ssot-ссылки)
- [Волна 4: Высокие зависимости (4+ SSOT-ссылок)](#волна-4-высокие-зависимости-4-ssot-ссылок)
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

| Файл | SSOT-ссылки | Зависит от |
|------|-------------|------------|
| `standard-codeowners.md` | 0 | — |
| `standard-labels.md` | 0 | — |
| `standard-pr-template.md` | 0 | — |
| `standard-issue-template.md` | 1 | standard-labels.md |
| `standard-release.md` | 2 | standard-milestone.md, standard-pull-request.md |
| `standard-issue.md` | 2 | standard-labels.md, standard-issue-template.md |
| `standard-pull-request.md` | 3 | standard-labels.md, standard-pr-template.md |
| `standard-milestone.md` | 3 | standard-issue.md, standard-release.md |
| `standard-workflow-file.md` | 4 | standard-development-workflow.md, standard-release-workflow.md, standard-release.md |
| `standard-project.md` | 4 | standard-issue.md, standard-pull-request.md, standard-milestone.md, standard-workflow-file.md |
| `standard-development-workflow.md` | 5 | standard-issue.md, standard-pull-request.md, standard-labels.md |
| `standard-release-workflow.md` | 6 | standard-development-workflow.md, standard-release.md, standard-milestone.md, standard-workflow-file.md |
| `standard-github.md` | 11 | Все остальные (навигационный документ) |

---

## Порядок валидации

### Волна 1: Базовые стандарты (0 SSOT-ссылок)

Самодостаточные документы, не зависящие от других стандартов.

| # | Файл | Приоритет | Обоснование |
|---|------|-----------|-------------|
| 1 | `standard-labels.md` | **Высокий** | Фундамент для 5+ других стандартов (issue, pr, issue-template) |
| 2 | `standard-pr-template.md` | Средний | Используется в standard-pull-request.md |
| 3 | `standard-codeowners.md` | Низкий | Изолированный стандарт, не влияет на другие |

---

### Волна 2: Минимальные зависимости (1-2 SSOT-ссылки)

Зависят только от стандартов Волны 1.

| # | Файл | SSOT-ссылки | Приоритет | Обоснование |
|---|------|-------------|-----------|-------------|
| 4 | `standard-issue-template.md` | 1 | **Высокий** | Зависит от standard-labels.md, нужен для standard-issue.md |
| 5 | `standard-issue.md` | 2 | **Высокий** | Основа development workflow, зависит от labels + templates |
| 6 | `standard-release.md` | 2 | Средний | Зависит от milestone + pull-request, но milestone ещё не провалидирован → читаем для понимания |

> **Циклическая зависимость:** `standard-release.md` ↔ `standard-milestone.md`. Читаем release.md в Волне 2 для понимания, milestone.md — в Волне 3.

---

### Волна 3: Средние зависимости (3 SSOT-ссылки)

Зависят от стандартов Волн 1-2.

| # | Файл | SSOT-ссылки | Приоритет | Обоснование |
|---|------|-------------|-----------|-------------|
| 7 | `standard-pull-request.md` | 3 | **Высокий** | Основа development workflow, зависит от labels + pr-template |
| 8 | `standard-milestone.md` | 3 | Средний | Связь с release + issue |

---

### Волна 4: Высокие зависимости (4+ SSOT-ссылок)

Агрегирующие документы, зависящие от многих стандартов.

| # | Файл | SSOT-ссылки | Приоритет | Обоснование |
|---|------|-------------|-----------|-------------|
| 9 | `standard-workflow-file.md` | 4 | Средний | Технический стандарт YAML, ссылки на workflow-ы |
| 10 | `standard-project.md` | 4 | Низкий | GitHub Projects — опционально для команды 2 чел. |
| 11 | `standard-development-workflow.md` | 5 | **Высокий** | Объединяет issue + pr + labels в единый процесс |
| 12 | `standard-release-workflow.md` | 6 | **Высокий** | Объединяет development + release + milestone |
| 13 | `standard-github.md` | 11 | Последний | Навигационный документ — проверяем ссылки после всех |

---

## Чек-лист

### Волна 1

- [ ] **1. standard-labels.md** — система меток
  - [ ] Категории и naming convention корректны
  - [ ] Правила применения однозначны
  - [ ] Примеры достаточны

- [ ] **2. standard-pr-template.md** — шаблон PR
  - [ ] Обязательные секции определены
  - [ ] Placeholder-ы понятны
  - [ ] Примеры полные

- [ ] **3. standard-codeowners.md** — правила CODEOWNERS
  - [ ] Синтаксис описан полно
  - [ ] Паттерны корректны
  - [ ] Примеры для проекта релевантны

### Волна 2

- [ ] **4. standard-issue-template.md** — YAML-шаблоны Issues
  - [ ] Формат YAML корректен
  - [ ] Связь с labels согласована
  - [ ] Примеры рабочие

- [ ] **5. standard-issue.md** — управление Issues
  - [ ] Жизненный цикл полон
  - [ ] Связь с branch/PR корректна
  - [ ] CLI команды актуальны

- [ ] **6. standard-release.md** — версионирование и releases
  - [ ] SemVer описан корректно
  - [ ] Changelog формат понятен
  - [ ] Связь с milestone/PR согласована

### Волна 3

- [ ] **7. standard-pull-request.md** — работа с PR
  - [ ] Жизненный цикл полон
  - [ ] Merge стратегии корректны
  - [ ] Code review процесс понятен

- [ ] **8. standard-milestone.md** — управление milestones
  - [ ] Типы milestones определены
  - [ ] Связь с release согласована
  - [ ] CLI команды актуальны

### Волна 4

- [ ] **9. standard-workflow-file.md** — GitHub Actions YAML
  - [ ] Структура YAML полна
  - [ ] Триггеры описаны корректно
  - [ ] Best practices актуальны

- [ ] **10. standard-project.md** — GitHub Projects
  - [ ] Scope документа корректен
  - [ ] CLI команды рабочие
  - [ ] Связь с issue/pr согласована

- [ ] **11. standard-development-workflow.md** — полный цикл разработки
  - [ ] Все стадии согласованы с зависимыми стандартами
  - [ ] Нет противоречий с issue.md / pr.md
  - [ ] Граничные случаи покрыты

- [ ] **12. standard-release-workflow.md** — процесс релиза
  - [ ] Все стадии согласованы с release.md / milestone.md
  - [ ] Hotfix процесс полон
  - [ ] Rollback описан корректно

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

**Дата завершения:** 2026-02-03
**Итоговый отчёт:** [2026-02-03-github-instructions-validation-results.md](./2026-02-03-github-instructions-validation-results.md)

### Волна 1

| Файл | Статус | Качество | Комментарий |
|------|--------|----------|-------------|
| standard-labels.md | ✅ | 8/10 | Нет критериев приоритетов |
| standard-pr-template.md | ✅ | 8/10 | Нет критериев выбора шаблона |
| standard-codeowners.md | ✅ | 9/10 | Минимальные доработки |

### Волна 2

| Файл | Статус | Качество | Комментарий |
|------|--------|----------|-------------|
| standard-issue-template.md | ✅ | 9/10 | Нет объяснения зачем id |
| standard-issue.md | ✅ | 8/10 | Нет процедуры stale Issues |
| standard-release.md | ✅ | 9/10 | Пересечение с release-workflow |

### Волна 3

| Файл | Статус | Качество | Комментарий |
|------|--------|----------|-------------|
| standard-pull-request.md | ✅ | 8/10 | Нет self-review, эскалации |
| standard-milestone.md | ✅ | 8/10 | Нет автоматизации Sprint |

### Волна 4

| Файл | Статус | Качество | Комментарий |
|------|--------|----------|-------------|
| standard-workflow-file.md | ✅ | 9/10 | Слишком большой документ |
| standard-project.md | ✅ | 8/10 | Сложный item-edit |
| standard-development-workflow.md | ✅ | 9/10 | Дублирование с issue/pr |
| standard-release-workflow.md | ✅ | 8/10 | Нет release freeze |
| standard-github.md | ✅ | 9/10 | Нет порядка изучения |

---

## Созданные драфты рекомендаций

1. [recommendations-standard-labels.md](./2026-02-03-recommendations-standard-labels.md)
2. [recommendations-standard-pr-template.md](./2026-02-03-recommendations-standard-pr-template.md)
3. [recommendations-standard-codeowners.md](./2026-02-03-recommendations-standard-codeowners.md)
4. [recommendations-standard-issue-template.md](./2026-02-03-recommendations-standard-issue-template.md)
5. [recommendations-standard-issue.md](./2026-02-03-recommendations-standard-issue.md)
6. [recommendations-standard-release.md](./2026-02-03-recommendations-standard-release.md)
7. [recommendations-standard-pull-request.md](./2026-02-03-recommendations-standard-pull-request.md)
8. [recommendations-standard-milestone.md](./2026-02-03-recommendations-standard-milestone.md)
9. [recommendations-standard-workflow-file.md](./2026-02-03-recommendations-standard-workflow-file.md)
10. [recommendations-standard-project.md](./2026-02-03-recommendations-standard-project.md)
11. [recommendations-standard-development-workflow.md](./2026-02-03-recommendations-standard-development-workflow.md)
12. [recommendations-standard-release-workflow.md](./2026-02-03-recommendations-standard-release-workflow.md)
13. [recommendations-standard-github.md](./2026-02-03-recommendations-standard-github.md)
