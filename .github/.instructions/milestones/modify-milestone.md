---
description: Воркфлоу изменения GitHub Milestone — обновление описания, срока, закрытие или удаление.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/milestones/README.md
---

# Воркфлоу изменения Milestone

Рабочая версия стандарта: 1.1

Процессы обновления, закрытия и удаления GitHub Milestone.

**Полезные ссылки:**
- [Инструкции Milestones](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-milestone.md](./standard-milestone.md) |
| Валидация | [validation-milestone.md](./validation-milestone.md) |
| Создание | [create-milestone.md](./create-milestone.md) |
| Модификация | Этот документ |

## Оглавление

- [Типы изменений](#типы-изменений)
- [Обновление](#обновление)
  - [Шаг 1: Найти Milestone](#шаг-1-найти-milestone)
  - [Шаг 2: Внести изменения](#шаг-2-внести-изменения)
  - [Шаг 3: Валидация](#шаг-3-валидация)
- [Закрытие](#закрытие)
  - [Шаг 1: Проверить готовность](#шаг-1-проверить-готовность)
  - [Шаг 2: Обработать незавершённые Issues](#шаг-2-обработать-незавершённые-issues)
  - [Шаг 3: Закрыть Milestone](#шаг-3-закрыть-milestone)
  - [Шаг 4: Создать Release](#шаг-4-создать-release)
- [Удаление](#удаление)
  - [Шаг 1: Проверить зависимости](#шаг-1-проверить-зависимости)
  - [Шаг 2: Перенести Issues](#шаг-2-перенести-issues)
  - [Шаг 3: Удалить Milestone](#шаг-3-удалить-milestone)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Типы изменений

| Тип | Описание | Пример |
|-----|----------|--------|
| Обновление | Изменение title, description, due date | Продлить дедлайн, обновить критерии |
| Закрытие | Завершение Milestone и создание Release | Все Issues закрыты → закрыть → Release |
| Удаление | Удаление ошибочного/неактуального Milestone | Milestone создан по ошибке |

---

## Обновление

### Шаг 1: Найти Milestone

```bash
# По title
gh api repos/{owner}/{repo}/milestones -f state=open \
  -q '.[] | select(.title == "v1.0.0") | {number, title, state}'

# Все открытые
gh api repos/{owner}/{repo}/milestones -f state=open \
  -q '.[] | {number, title, due_on, open_issues, closed_issues}'
```

### Шаг 2: Внести изменения

**Изменение title (переименование версии):**

```bash
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f title="v1.1.0"
```

> **Важно:** При переименовании title — проверить, нет ли уже Milestone с новым именем.

**Изменение description:**

```bash
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f description="## Цель

Обновлённое описание

## Критерии готовности

- [ ] Обновлённый критерий"
```

**Продление due date:**

```bash
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f due_on="2026-04-01T23:59:59Z"
```

### Шаг 3: Валидация

```bash
python .github/.instructions/.scripts/validate-milestone.py --number {number}
```

---

## Закрытие

**SSOT:** [standard-milestone.md § 8](./standard-milestone.md#8-закрытие-milestone)

### Шаг 1: Проверить готовность

```bash
# Получить статус Milestone
gh api repos/{owner}/{repo}/milestones/{number} \
  -q '{title: .title, open: .open_issues, closed: .closed_issues, due_on: .due_on}'
```

**Критерии готовности к закрытию:**
1. `open_issues == 0` — все Issues закрыты
2. Критерии готовности из description выполнены
3. Due date наступил или до него <= 2 дней

### Шаг 2: Обработать незавершённые Issues

**Если `open_issues > 0`:**

1. Получить список открытых Issues:
   ```bash
   gh issue list --milestone "{title}" --state open
   ```

2. Для каждого Issue — оценить критичность (упомянут ли в "Критерии готовности")

3. **Не критичные** — перенести в следующий Milestone:
   ```bash
   gh issue edit {issue_number} --milestone "v1.1.0"
   ```

4. **Критичные** — НЕ закрывать Milestone, продлить due date:
   ```bash
   gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
     -f due_on="2026-04-01T23:59:59Z"
   ```

### Шаг 3: Закрыть Milestone

```bash
# Финальная проверка
OPEN=$(gh api repos/{owner}/{repo}/milestones/{number} -q '.open_issues')
if [ "$OPEN" -eq 0 ]; then
  gh api PATCH /repos/{owner}/{repo}/milestones/{number} -f state=closed
  echo "Milestone закрыт"
else
  echo "ERROR: Есть $OPEN открытых Issues"
fi
```

### Шаг 4: Создать Release

**SSOT:** [standard-release.md § 9–10](../releases/standard-release.md#9-подготовка-релиза)

После закрытия Milestone — создать GitHub Release по процессу из release-workflow.

---

## Удаление

### Шаг 1: Проверить зависимости

```bash
# Проверить наличие Issues
gh api repos/{owner}/{repo}/milestones/{number} \
  -q '{open: .open_issues, closed: .closed_issues}'

# Проверить наличие Release с тегом = title
TITLE=$(gh api repos/{owner}/{repo}/milestones/{number} -q '.title')
gh release view "$TITLE" --json tagName 2>/dev/null && echo "Release существует — удаление запрещено"
```

**Нельзя удалить Milestone если:**
- Связан с GitHub Release (есть Release с тегом = title)
- Содержит Issues (open или closed)

### Шаг 2: Перенести Issues

```bash
# Перенести все Issues в другой Milestone
gh issue list --milestone "{title}" --state all --json number -q '.[].number' | while read NUM; do
  gh issue edit $NUM --milestone ""
done
```

### Шаг 3: Удалить Milestone

```bash
gh api DELETE /repos/{owner}/{repo}/milestones/{number}
```

> **Важно:** Удаление Milestone НЕ удаляет Issues. Issues остаются без Milestone.

---

## Чек-лист

### Обновление
- [ ] Milestone найден по номеру или title
- [ ] Изменения внесены через `gh api PATCH`
- [ ] При переименовании: уникальность title проверена
- [ ] Валидация пройдена (`/milestone-validate`)

### Закрытие
- [ ] Все Issues закрыты (`open_issues == 0`)
- [ ] Незавершённые Issues перенесены в другой Milestone
- [ ] Критерии готовности из description выполнены
- [ ] Milestone закрыт через `gh api PATCH`
- [ ] Release создан по [standard-release.md](../releases/standard-release.md)

### Удаление
- [ ] Нет связанного Release
- [ ] Issues перенесены или отвязаны
- [ ] Milestone удалён через `gh api DELETE`

---

## Примеры

### Продление дедлайна

```bash
# Найти Milestone
gh api repos/{owner}/{repo}/milestones -f state=open \
  -q '.[] | select(.title == "v1.0.0") | .number'
# → 3

# Продлить на месяц
gh api PATCH /repos/{owner}/{repo}/milestones/3 \
  -f due_on="2026-04-15T23:59:59Z"

# Валидация
python .github/.instructions/.scripts/validate-milestone.py --number 3
```

### Закрытие Milestone и подготовка к Release

```bash
# 1. Проверить готовность
gh api repos/{owner}/{repo}/milestones/3 \
  -q '{open: .open_issues, closed: .closed_issues}'
# → {"open": 0, "closed": 8}

# 2. Закрыть
gh api PATCH /repos/{owner}/{repo}/milestones/3 -f state=closed

# 3. Создать Release (см. release-workflow)
gh release create v1.0.0 --title "v1.0.0" --notes "..."
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [close-milestone.py](../.scripts/close-milestone.py) | Закрытие Milestone: проверки, перенос Issues, верификация | Этот документ |
| [validate-milestone.py](../.scripts/validate-milestone.py) | Валидация после изменений | [validation-milestone.md](./validation-milestone.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/milestone-modify](/.claude/skills/milestone-modify/SKILL.md) | Изменение, закрытие и удаление Milestone | Этот документ |
