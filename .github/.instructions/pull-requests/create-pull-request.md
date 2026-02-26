---
description: Воркфлоу создания PR — сбор Issues из chain, формирование title/body/labels, push, preview, gh pr create.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/pull-requests/README.md
---

# Воркфлоу создания PR

Рабочая версия стандарта: 1.3

Процесс создания Pull Request: определение chain, сбор данных скриптом, формирование title/body/labels, push, preview, создание PR через `gh pr create`.

**Полезные ссылки:**
- [Инструкции pull-requests](./README.md)
- [Стандарт PR](./standard-pull-request.md) — SSOT правил

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-pull-request.md](./standard-pull-request.md) |
| Валидация | *Покрыта скриптом [validate-pr-template.py](../.scripts/validate-pr-template.py)* |
| Создание | Этот документ |
| Модификация | *Будет создан* |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Определение chain](#шаг-1-определение-chain)
  - [Шаг 2: Prerequisites](#шаг-2-prerequisites)
  - [Шаг 3: Сбор данных](#шаг-3-сбор-данных)
  - [Шаг 4: Формирование title](#шаг-4-формирование-title)
  - [Шаг 5: Формирование body](#шаг-5-формирование-body)
  - [Шаг 6: Определение labels](#шаг-6-определение-labels)
  - [Шаг 7: Push ветки](#шаг-7-push-ветки)
  - [Шаг 8: Preview и подтверждение](#шаг-8-preview-и-подтверждение)
  - [Шаг 9: Создание PR](#шаг-9-создание-pr)
  - [Шаг 10: Отчёт](#шаг-10-отчёт)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Данные — из скрипта.** `collect-pr-issues.py` парсит chain без LLM. Агент подставляет данные в шаблон.

> **Preview обязателен.** Создание PR — публичное действие. Всегда показать preview через AskUserQuestion.

> **Правила — из стандарта.** Все правила PR — в [standard-pull-request.md](./standard-pull-request.md). Эта инструкция описывает процесс, не правила.

> **Один chain = один PR.** Все Issues chain'а группируются в один PR с `Closes #N`.

---

## Шаги

### Шаг 1: Определение chain

1. Определить текущую ветку:
   ```bash
   git branch --show-current
   ```

2. Парсинг NNNN из имени ветки (формат `{NNNN}-{topic}` из [standard-branching.md](../branches/standard-branching.md))

3. Если ветка = `main` — ошибка: "Нельзя создать PR из main"

4. Если имя не содержит `{NNNN}-` — fallback: ручной режим без chain (см. [Fallback](#fallback-без-chain))

### Шаг 2: Prerequisites

| # | Проверка | Команда | Блокирующая |
|---|---------|---------|:-----------:|
| 1 | Ветка не main | `git branch --show-current` | Да |
| 2 | Есть коммиты для push | `git log origin/{branch}..HEAD --oneline` | Да |
| 3 | Chain в RUNNING | `python specs/.instructions/.scripts/chain_status.py --chain {NNNN} --status` | Рекомендуемая |
| 4 | Нет существующего PR | Поле `existing_pr` из скрипта | Да |

Если remote branch не существует — все коммиты считаются новыми (prerequisite 2 пройден).

### Шаг 3: Сбор данных

```bash
python .github/.instructions/.scripts/collect-pr-issues.py {NNNN}
```

Парсить JSON-ответ. Если `errors` не пуст — обработать:

| Ошибка | Действие |
|--------|----------|
| `no_chain` | Fallback: ручной режим |
| `no_plan_dev` | Сообщить: "plan-dev.md не найден для chain {NNNN}". Предложить ручной режим |
| `no_issues` | Сообщить: "Таблица маппинга пуста — Issues не созданы" |
| `all_closed` | Сообщить: "Все Issues закрыты — PR не нужен" |
| `pr_exists` | Сообщить: "PR #{N} уже существует для этой ветки" |

### Шаг 4: Формирование title

Формат: `{type}: {description}` (SSOT: [standard-pull-request.md § 4](./standard-pull-request.md#4-именование-title))

- `type` — из `suggested_type` скрипта (TYPE-метка из Issues)
- `description` — из `description` скрипта (discussion.md frontmatter), нижний регистр, без точки
- Общая длина — до 70 символов

**Допустимые типы:** `bug`, `task`, `docs`, `refactor` (SSOT: labels.yml). **НЕТ `feature`**.

### Шаг 5: Формирование body

По шаблону [PULL_REQUEST_TEMPLATE.md](../../PULL_REQUEST_TEMPLATE.md):

```markdown
## Summary
{description из discussion.md — 2-5 предложений}

## Changes
- {TASK-1 title} (#{issue_number})
- {TASK-2 title} (#{issue_number})
- {TASK-3 title} (#{issue_number})

## Test plan
- [ ] Локально протестировано (`make dev`)
- [ ] Pre-commit проверки пройдены
- [ ] Unit-тесты пройдены
- [ ] Интеграционные тесты пройдены (если применимо)
- [ ] Документация обновлена (если нужно)

## Related issues
Closes #{issue_1}
Closes #{issue_2}
Closes #{issue_3}
```

- Секцию **Breaking changes** включить только если есть (иначе удалить)
- Секцию **Notes** включить только если есть (иначе удалить)
- `Closes #N` — каждый Issue на отдельной строке

### Шаг 6: Определение labels

- TYPE: из `suggested_type` (ровно 1)
- PRIORITY: из `suggested_priority` (ровно 1)
- Формат: `--label {type} --label {priority}`

### Шаг 7: Push ветки

```bash
git push -u origin {branch}
```

Если remote branch уже существует и up-to-date — skip.

### Шаг 8: Preview и подтверждение

Показать пользователю через AskUserQuestion:

```
PR для ветки {branch}:

Title: {title}
Labels: {type}, {priority}
Milestone: {milestone}
Issues: Closes #{...}, #{...}

Body:
{полный текст body}
```

Опции:
1. Создать PR
2. Создать как Draft
3. Отменить

Если `--dry-run` — показать preview и остановиться.

### Шаг 9: Создание PR

```bash
gh pr create --title "{title}" --body "$(cat <<'EOF'
{body}
EOF
)" --label {type} --label {priority}
```

Дополнительные флаги:
- `--draft` если пользователь выбрал "Создать как Draft"
- `--milestone "{milestone}"` если milestone определён

Обработка ошибок:

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `HTTP 403` | Нет прав | Проверить `gh auth status` |
| `already exists` | PR уже создан | Показать `gh pr view` |
| `no commits` | Нечего пушить | Сделать commit перед PR |

### Шаг 10: Отчёт

Вывести:
- PR URL
- PR номер
- Привязанные Issues (количество и номера)
- Labels
- Milestone
- Следующий шаг: "Запустите `/review {PR-N}` для code review"

---

### Fallback без chain

Если ветка не содержит `{NNNN}-{topic}`:

1. Type определяется из diff (`git diff --stat` — только `.md` файлы → `docs`)
2. Issues не привязываются (или пользователь указывает вручную)
3. Summary формируется из коммитов (`git log --oneline`)
4. Preview и подтверждение — как обычно

---

## Чек-лист

### Подготовка
- [ ] Chain определён из имени ветки
- [ ] Prerequisites проверены (не main, есть коммиты, нет дубликата PR)
- [ ] Данные собраны скриптом (или fallback)

### Формирование
- [ ] Title сформирован (type: description, до 70 символов)
- [ ] Body заполнен по шаблону
- [ ] Labels определены (TYPE + PRIORITY)
- [ ] Milestone привязан (если есть)

### Создание
- [ ] Ветка запушена (`git push -u`)
- [ ] Preview показан и подтверждён
- [ ] PR создан (`gh pr create`)
- [ ] Отчёт выведен

---

## Примеры

### PR из chain

```bash
# Ветка: 0042-oauth2-authorization
# 1. Сбор данных
python .github/.instructions/.scripts/collect-pr-issues.py 0042
# → JSON с issues, milestone, suggested_type

# 2. Создание PR
gh pr create \
  --title "task: add OAuth2 authorization" \
  --body "$(cat <<'EOF'
## Summary
OAuth2 авторизация для микросервисов — JWT токены, middleware, refresh.

## Changes
- Добавить JWT токены (#42)
- Middleware авторизации (#43)
- Refresh токены (#44)

## Test plan
- [ ] Локально протестировано (`make dev`)
- [ ] Pre-commit проверки пройдены
- [ ] Unit-тесты пройдены

## Related issues
Closes #42
Closes #43
Closes #44
EOF
)" \
  --label task --label high \
  --milestone "v1.2.0"
```

### PR без chain (doc-only)

```bash
# Ветка: fix-typos
# Нет chain → fallback
gh pr create \
  --title "docs: fix typos in README" \
  --body "$(cat <<'EOF'
## Summary
Исправлены опечатки в README файлах.

## Changes
- Исправлены опечатки в 3 файлах

## Test plan
- [ ] Pre-commit проверки пройдены

## Related issues
N/A
EOF
)" \
  --label docs --label low
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [collect-pr-issues.py](../.scripts/collect-pr-issues.py) | Сбор Issues из chain для PR | Этот документ |

---

## Скиллы

*Нет скиллов.*
