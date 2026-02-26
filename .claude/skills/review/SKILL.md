---
name: review
description: Ревью кода — локальное ревью ветки или ревью PR на GitHub. Объединяет оба этапа code review. Используй перед git push или при получении PR на ревью.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.2
index: .claude/skills/README.md
allowed-tools: Read, Write, Bash, Glob, Grep
argument-hint: "[<pr-number>] [--base <branch>]"
---

# Ревью кода

**SSOT:** [validation-review.md](/.github/.instructions/review/validation-review.md)

**SSOT (process):** [standard-review.md](/specs/.instructions/analysis/review/standard-review.md)

**Агент:** [code-reviewer](/.claude/agents/code-reviewer/AGENT.md)

## Формат вызова

```
/review [<pr-number>] [--base <branch>]
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `pr-number` | Номер PR на GitHub (включает Этап 2) | Нет |
| `--base` | Базовая ветка для сравнения (по умолчанию `main`) | Нет |

## Воркфлоу

> Прочитать [validation-review.md](/.github/.instructions/review/validation-review.md)

> Прочитать [standard-review.md](/specs/.instructions/analysis/review/standard-review.md) — стандарт review.md, формат RV-N, P1/P2/P3.

**Основной LLM — оркестратор параллельного ревью:**

1. Определить ветку: аргумент или `git branch --show-current`
2. **Prerequisite check** — прочитать `specs/analysis/{branch}/plan-dev.md`, проверить поле `status:`:
   - `RUNNING` → OK, продолжить
   - `WAITING` → СТОП: "Plan Dev в WAITING — разработка не начата, переведите в RUNNING"
   - `CONFLICT` → СТОП: "Plan Dev в CONFLICT — сначала разрешите конфликт цепочки"
   - `DONE` → AskUserQuestion: продолжить повторное ревью после DONE?
   - Не найден → СТОП: "analysis chain не найдена для ветки {branch}"
3. Прочитать `specs/analysis/{branch}/review.md` → секция `## Контекст ревью`
   - Если review.md не существует → СТОП: "review.md не найден. Запустите `/review-create`."
   - Извлечь список сервисов из блоков `### {svc}`
4. Подготовить общий пакет документов для агентов:
   - Документы цепочки: discussion.md, design.md, plan-test.md, plan-dev.md
   - Системная документация: specs/docs/.system/overview.md, conventions.md, testing.md
   - Принципы: .instructions/standard-principles.md
   - Tech-стандарты: из секции `### Tech-стандарты` в review.md
   - Полный git diff (или `gh pr diff {N}` для PR-режима)
5. Запустить параллельно одним Task tool call (N+1 агентов):
   - `code-reviewer --svc {svc1}` (+ specs/docs/{svc1}.md из Контекст ревью)
   - `code-reviewer --svc {svc2}` (+ specs/docs/{svc2}.md)
   - `code-reviewer --svc integration` (INT-N, shared/)
6. Собрать все выводы агентов
7. Собрать `## Итерация N` (N = следующий номер):
   - Для каждого сервиса — блок `### {svc}` с выводом агента
   - Блок `### Итого` (агрегат по P1/P2/P3 всех сервисов)
   - Определить вердикт: CONFLICT (есть P1 open) / NOT READY (есть P2 open) / READY (нет open P1/P2)
8. Дописать `## Итерация N` в review.md (Write)
9. Обновить `status` в review.md: CONFLICT/NOT READY → `OPEN`; READY → `RESOLVED`
10. Если PR-режим (`/review {N}`): написать `gh pr comment` с кратким резюме (P1/P2/P3, вердикт)

## Чек-лист

→ См. [validation-review.md#чек-лист](/.github/.instructions/review/validation-review.md#чек-лист)

## Примеры

```
/review
/review --base develop
/review 42
/review 123
```
