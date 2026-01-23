---
type: instruction
status: active
priority: required
description: Команды gh CLI для работы с GitHub Issues
related:
  - issues/workflow.md
  - issues/labels.md
---

# Команды gh CLI

Справочник команд GitHub CLI для работы с Issues.

## Оглавление

- [Создание](#создание)
- [Просмотр](#просмотр)
- [Редактирование](#редактирование)
- [Закрытие](#закрытие)
- [Комментарии](#комментарии)
- [Фильтрация](#фильтрация)
- [Связанные инструкции](#связанные-инструкции)

---

## Создание

### Базовое создание

```bash
gh issue create --title "[AUTH] Добавить OAuth" --label "service:auth"
```

### С телом

```bash
gh issue create \
  --title "[AUTH] Добавить OAuth авторизацию" \
  --label "service:auth,feature" \
  --body "## Описание

Реализовать OAuth авторизацию.

## Критерии готовности

- [ ] OAuth через Google
- [ ] OAuth через GitHub"
```

### С назначением

```bash
gh issue create \
  --title "[AUTH] Добавить OAuth" \
  --label "service:auth" \
  --assignee @me
```

### Интерактивное создание

```bash
gh issue create  # Откроет редактор
```

---

## Просмотр

### Список открытых

```bash
gh issue list --state open
```

### Детали Issue

```bash
gh issue view 123
```

### JSON формат

```bash
gh issue view 123 --json number,title,state,labels,assignees,body
```

### С комментариями

```bash
gh issue view 123 --comments
```

### В браузере

```bash
gh issue view 123 --web
```

---

## Редактирование

### Изменить заголовок

```bash
gh issue edit 123 --title "[AUTH] Новый заголовок"
```

### Добавить метку

```bash
gh issue edit 123 --add-label "in-progress"
```

### Удалить метку

```bash
gh issue edit 123 --remove-label "in-progress"
```

### Изменить тело

```bash
gh issue edit 123 --body "Новое описание"
```

### Назначить исполнителя

```bash
gh issue edit 123 --add-assignee @me
gh issue edit 123 --add-assignee username
```

### Снять назначение

```bash
gh issue edit 123 --remove-assignee @me
```

### Множественные изменения

```bash
gh issue edit 123 \
  --add-label "priority:high" \
  --add-label "in-progress" \
  --add-assignee @me
```

---

## Закрытие

### Закрыть как выполненный

```bash
gh issue close 123 --reason completed
```

### Закрыть как неактуальный

```bash
gh issue close 123 --reason "not planned"
```

### Закрыть с комментарием

```bash
gh issue close 123 --comment "Выполнено в PR #456"
```

### Переоткрыть

```bash
gh issue reopen 123
```

---

## Комментарии

### Добавить комментарий

```bash
gh issue comment 123 --body "Начал работу над задачей"
```

### Многострочный комментарий

```bash
gh issue comment 123 --body "$(cat <<'EOF'
## Статус

Выполнено:
- [x] Пункт 1
- [x] Пункт 2

Осталось:
- [ ] Пункт 3
EOF
)"
```

### Через редактор

```bash
gh issue comment 123 --editor
```

---

## Фильтрация

### По сервису

```bash
gh issue list --label "service:auth"
```

### По приоритету

```bash
gh issue list --label "priority:high"
```

### По исполнителю

```bash
gh issue list --assignee @me
gh issue list --assignee username
```

### По состоянию

```bash
gh issue list --state open
gh issue list --state closed
gh issue list --state all
```

### Комбинированный фильтр

```bash
gh issue list \
  --label "service:auth" \
  --label "bug" \
  --state open \
  --assignee @me
```

### Поиск

```bash
gh issue list --search "OAuth in:title"
gh issue list --search "is:open label:bug"
```

### Лимит результатов

```bash
gh issue list --limit 10
gh issue list --limit 100
```

### JSON вывод

```bash
gh issue list --json number,title,labels --jq '.[] | "\(.number): \(.title)"'
```

---

## Полезные алиасы

### Мои задачи в работе

```bash
gh issue list --assignee @me --label "in-progress"
```

### Срочные баги

```bash
gh issue list --label "bug" --label "priority:high" --state open
```

### Заблокированные

```bash
gh issue list --label "blocked" --state open
```

### Связанные PR

```bash
gh pr list --search "closes #123 OR fixes #123"
```

### Проверить CI статус PR

```bash
gh pr checks 456
```

---

## Массовые операции

### Закрыть несколько Issue

```bash
for i in 123 124 125; do
  gh issue close $i --reason "not planned" --comment "Неактуально"
done
```

### Добавить метку к нескольким

```bash
gh issue list --label "bug" --json number -q '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "priority:high"
```

### Назначить себя на все Issue сервиса

```bash
gh issue list --label "service:auth" --state open --json number -q '.[].number' | \
  xargs -I {} gh issue edit {} --add-assignee @me
```

---

## Связанные инструкции

- [workflow.md](./workflow.md) — жизненный цикл Issue
- [labels.md](./labels.md) — система меток
- [errors.md](./errors.md) — обработка ошибок

---

> **Путь:** `/.claude/.instructions/issues/commands.md`
