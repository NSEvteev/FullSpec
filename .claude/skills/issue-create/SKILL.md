---
name: issue-create
description: Создание GitHub Issue с правильным форматом
allowed-tools: Read, Bash, Glob
category: git
triggers:
  commands:
    - /issue-create
  phrases:
    ru:
      - создай задачу
      - создай issue
      - новая задача
    en:
      - create issue
      - new issue
      - create task
---

# Создание Issue

Команда для создания GitHub Issue с правильным форматом: префикс, метки, шаблон описания.

**Связанная инструкция:** [/.claude/instructions/git/issues.md](/.claude/instructions/git/issues.md)

**Связанные скиллы:**
- [issue-update](/.claude/skills/issue-update/SKILL.md) — обновление Issue
- [issue-delete](/.claude/skills/issue-delete/SKILL.md) — закрытие Issue
- [issue-execute](/.claude/skills/issue-execute/SKILL.md) — взятие Issue в работу

## Оглавление

- [Формат вызова](#формат-вызова)
- [Префиксы сервисов](#префиксы-сервисов)
- [Воркфлоу](#воркфлоу)
- [Шаблон Issue](#шаблон-issue)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/issue-create [--service <сервис>] [--type <тип>] [--priority <приоритет>] "<заголовок>"
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--service` | Сервис (auth, notify, pay, users, gw, infra, docs) | Определяется из контекста |
| `--type` | Тип (feature, bug, enhancement) | feature |
| `--priority` | Приоритет (high, medium, low) | — |
| `заголовок` | Описание задачи | — (обязательный) |

**Примеры:**
- `/issue-create --service auth "Добавить OAuth авторизацию"`
- `/issue-create --service notify --type bug "Email не отправляется"`
- `/issue-create --service infra --priority high "Настроить CI"`

---

## Префиксы сервисов

| Сервис | Префикс | Label |
|--------|---------|-------|
| auth | AUTH | service:auth |
| notify | NOTIFY | service:notify |
| pay | PAY | service:payment |
| users | USERS | service:users |
| gw | GW | service:gateway |
| infra | INFRA | infra |
| docs | DOCS | docs |

---

## Воркфлоу

### Шаг 1: Определить сервис

1. Из параметра `--service`
2. Или из текущего контекста (открытый файл)
3. Или спросить у пользователя

### Шаг 2: Сформировать заголовок

```
[{PREFIX}] {заголовок}
```

Пример: `[AUTH] Добавить OAuth авторизацию`

### Шаг 3: Определить метки

1. Метка сервиса: `service:auth`
2. Метка типа: `feature`, `bug`, `enhancement`
3. Метка приоритета (если указан): `priority:high`

### Шаг 4: Сформировать тело Issue

Использовать шаблон с разделами:
- Описание
- Критерии готовности
- Связанные файлы

### Шаг 5: Показать предпросмотр

```
📋 Создание Issue

Заголовок: [AUTH] Добавить OAuth авторизацию
Метки: service:auth, feature

Тело:
---
## Описание

{описание}

## Критерии готовности

- [ ] {критерий}

## Связанные файлы

- {файлы}
---

Создать? [Y/n/редактировать]
```

### Шаг 6: Создать Issue

```bash
gh issue create \
  --label "service:auth,feature" \
  --title "[AUTH] Добавить OAuth авторизацию" \
  --body "..."
```

### Шаг 7: Результат

```
✅ Issue создан

Номер: #123
URL: https://github.com/user/repo/issues/123
Заголовок: [AUTH] Добавить OAuth авторизацию
Метки: service:auth, feature
```

---

## Шаблон Issue

```markdown
## Описание

{Что нужно сделать}

## Критерии готовности

- [ ] {Чек-лист выполнения}

## Связанные файлы

- {Ссылки на код/документацию}
```

---

## Чек-лист

- [ ] **Шаг 1:** Определил сервис
- [ ] **Шаг 2:** Сформировал заголовок с префиксом
- [ ] **Шаг 3:** Определил метки
- [ ] **Шаг 4:** Сформировал тело по шаблону
- [ ] **Шаг 5:** Показал предпросмотр
- [ ] **Шаг 6:** Создал Issue через `gh issue create`
- [ ] **Шаг 7:** Вывел результат с URL

---

## Примеры

### Пример 1: Фича для сервиса auth

**Вызов:**
```
/issue-create --service auth "Добавить двухфакторную аутентификацию"
```

**Результат:**
```
✅ Issue создан

Номер: #45
URL: https://github.com/user/repo/issues/45
Заголовок: [AUTH] Добавить двухфакторную аутентификацию
Метки: service:auth, feature
```

### Пример 2: Баг с высоким приоритетом

**Вызов:**
```
/issue-create --service notify --type bug --priority high "Email не отправляется при регистрации"
```

**Результат:**
```
✅ Issue создан

Номер: #46
Заголовок: [NOTIFY] Email не отправляется при регистрации
Метки: service:notify, bug, priority:high
```

### Пример 3: Задача на документацию

**Вызов:**
```
/issue-create --service docs "Обновить README после рефакторинга"
```

**Результат:**
```
✅ Issue создан

Номер: #47
Заголовок: [DOCS] Обновить README после рефакторинга
Метки: docs
```

### Пример 4: Интерактивный режим

**Вызов:**
```
/issue-create "Настроить кэширование"
```

**Вывод:**
```
📋 Создание Issue

Заголовок: Настроить кэширование

Для какого сервиса?
[1] auth
[2] notify
[3] pay
[4] users
[5] gw
[6] infra
[7] docs

> 6

✅ Issue создан

Номер: #48
Заголовок: [INFRA] Настроить кэширование
Метки: infra, feature
```
