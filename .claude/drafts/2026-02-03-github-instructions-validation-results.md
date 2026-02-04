# Итоги смысловой валидации GitHub-инструкций

**Дата:** 2026-02-03
**Обновлено:** 2026-02-04
**Статус:** draft
**Валидировано документов:** 13

> **Примечание (2026-02-04):** После реструктуризации:
> - `standard-development-workflow.md` → `standard-github-workflow.md`
> - `standard-github.md` → **УДАЛЁН**
> - `standard-release-workflow.md` → `releases/standard-release-workflow.md`
> - Создан `review/standard-review.md` (Code Review и Merge)

---

## Сводная таблица результатов

| # | Стандарт | Качество | Полнота | Основные проблемы |
|---|----------|----------|---------|-------------------|
| 1 | standard-labels.md | 8/10 | 7/10 | Нет критериев приоритетов, нет валидации |
| 2 | standard-pr-template.md | 8/10 | 7/10 | Нет критериев выбора шаблона |
| 3 | standard-codeowners.md | 9/10 | 8/10 | Нет процедуры добавления/удаления владельца |
| 4 | standard-issue-template.md | 9/10 | 8/10 | Нет объяснения зачем нужен id |
| 5 | standard-issue.md | 8/10 | 7/10 | Нет процедуры для stale Issues |
| 6 | standard-release.md | 9/10 | 9/10 | Пересечение с release-workflow |
| 7 | standard-pull-request.md | 8/10 | 7/10 | Нет self-review, эскалации |
| 8 | standard-milestone.md | 8/10 | 7/10 | Нет автоматизации Sprint |
| 9 | standard-workflow-file.md | 9/10 | 9/10 | Слишком большой (~1300 строк) |
| 10 | standard-project.md | 8/10 | 7/10 | Сложный item-edit без скрипта |
| 11 | standard-github-workflow.md | 9/10 | 8/10 | Дублирование с issue/pr |
| 12 | releases/standard-release-workflow.md | 8/10 | 8/10 | Нет release freeze процедуры |
| 13 | ~~standard-github.md~~ | — | — | **УДАЛЁН** |
| 14 | review/standard-review.md | — | — | *Новый документ (2026-02-04)* |

---

## Общие паттерны проблем

### 1. Дублирование между документами

**Где:** standard-github-workflow.md ↔ standard-issue.md ↔ standard-pull-request.md

**Проблема:** Контент про создание Issue и PR повторяется в нескольких местах.

**Рекомендация:** Заменить дублирование на SSOT-ссылки. Development-workflow должен описывать только ПРОЦЕСС (последовательность), а детали — в специализированных стандартах.

### 2. Пересечение standard-release.md и standard-release-workflow.md

**Проблема:** Оба документа описывают создание Release. Границы размыты.

**Рекомендация:** Чётко разделить:
- **standard-release.md:** ЧТО (свойства, формат, версионирование)
- **standard-release-workflow.md:** КОГДА и КАК (процесс, проверки)

### 3. Отсутствие процедур для edge cases

**Примеры:**
- Что делать с "зависшими" Issues (stale)
- Что делать при срыве сроков Milestone
- Как эскалировать затянувшийся review

**Рекомендация:** Добавить секции "Граничные случаи" или "Troubleshooting" в каждый стандарт.

### 4. Нет автоматизации для рутинных операций

**Примеры:**
- Создание Sprint Milestone каждую неделю
- Валидация обязательных меток на Issues
- Определение версии по conventional commits

**Рекомендация:** Добавить примеры скриптов или GitHub Actions для автоматизации.

---

## Приоритизация доработок

### Критичные (влияют на workflow)

1. **Убрать дублирование** в standard-github-workflow.md
2. **Разделить** standard-release.md и standard-release-workflow.md
3. **Добавить критерии приоритетов** в standard-labels.md

### Важные (улучшают понимание)

4. ~~**Добавить порядок изучения** в standard-github.md~~ **НЕАКТУАЛЬНО** (файл удалён)
5. **Добавить checklist** перед созданием PR
6. **Добавить процедуру stale Issues** в standard-issue.md
7. **Добавить release freeze** в releases/standard-release-workflow.md

### Желательные (полировка)

8. Quick Reference для standard-workflow-file.md
9. Скрипт item-edit для standard-project.md
10. ~~Глоссарий терминов в standard-github.md~~ → рассмотреть отдельный документ

---

## Проверка согласованности SSOT

### Корректные ссылки

- standard-issue.md → standard-labels.md ✅
- standard-issue.md → standard-issue-template.md ✅
- standard-pull-request.md → standard-pr-template.md ✅
- standard-pull-request.md → standard-labels.md ✅
- standard-milestone.md → standard-release.md ✅
- standard-release.md → standard-milestone.md ✅
- ~~standard-github.md → все остальные~~ **УДАЛЁН**

### Циклические зависимости

- standard-milestone.md ↔ standard-release.md — **допустимо**, но требует ясного указания направления

### Отсутствующие ссылки

- standard-project.md → standard-milestone.md — добавить интеграцию Views с Milestones
- standard-github-workflow.md → standard-project.md — добавить ссылку если используется Projects

---

## Рекомендации по дополнению других SSOT

При доработке GitHub-стандартов могут появиться требования, специфичные для других областей:

| Рекомендация | Целевой SSOT |
|--------------|--------------|
| Описание pre-commit hooks для валидации меток | .structure/pre-commit.md |
| Автоматизация через скрипты | .instructions/standard-script.md |
| Интеграция с CI/CD деплоем | platform/.instructions/ |

---

## Следующие шаги

1. [ ] Приоритизировать доработки с владельцем проекта
2. [ ] Создать Issues для каждой доработки
3. [ ] Выполнить доработки в порядке приоритета
4. [ ] Повторить валидацию после доработок

---

## Файлы рекомендаций

| Стандарт | Файл рекомендаций |
|----------|-------------------|
| standard-labels.md | [2026-02-03-recommendations-standard-labels.md](./2026-02-03-recommendations-standard-labels.md) |
| standard-pr-template.md | [2026-02-03-recommendations-standard-pr-template.md](./2026-02-03-recommendations-standard-pr-template.md) |
| standard-codeowners.md | [2026-02-03-recommendations-standard-codeowners.md](./2026-02-03-recommendations-standard-codeowners.md) |
| standard-issue-template.md | [2026-02-03-recommendations-standard-issue-template.md](./2026-02-03-recommendations-standard-issue-template.md) |
| standard-issue.md | [2026-02-03-recommendations-standard-issue.md](./2026-02-03-recommendations-standard-issue.md) |
| standard-release.md | [2026-02-03-recommendations-standard-release.md](./2026-02-03-recommendations-standard-release.md) |
| standard-pull-request.md | [2026-02-03-recommendations-standard-pull-request.md](./2026-02-03-recommendations-standard-pull-request.md) |
| standard-milestone.md | [2026-02-03-recommendations-standard-milestone.md](./2026-02-03-recommendations-standard-milestone.md) |
| standard-workflow-file.md | [2026-02-03-recommendations-standard-workflow-file.md](./2026-02-03-recommendations-standard-workflow-file.md) |
| standard-project.md | [2026-02-03-recommendations-standard-project.md](./2026-02-03-recommendations-standard-project.md) |
| standard-github-workflow.md | [2026-02-03-recommendations-standard-development-workflow.md](./2026-02-03-recommendations-standard-development-workflow.md) |
| releases/standard-release-workflow.md | [2026-02-03-recommendations-standard-release-workflow.md](./2026-02-03-recommendations-standard-release-workflow.md) |
| ~~standard-github.md~~ | [2026-02-03-recommendations-standard-github.md](./2026-02-03-recommendations-standard-github.md) (**УСТАРЕЛ**) |
