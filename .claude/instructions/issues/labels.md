---
type: instruction
status: active
priority: required
description: Система меток (labels) для GitHub Issues
related:
  - issues/format.md
  - issues/workflow.md
---

# Метки Issues

Система меток для категоризации и фильтрации GitHub Issues.

## Оглавление

- [Принцип](#принцип)
- [Метки по сервису](#метки-по-сервису)
- [Метки по типу](#метки-по-типу)
- [Метки по приоритету](#метки-по-приоритету)
- [Метки по статусу](#метки-по-статусу)
- [Комбинации меток](#комбинации-меток)
- [Управление метками](#управление-метками)
- [Связанные инструкции](#связанные-инструкции)

---

## Принцип

**Правило:** Каждый Issue должен иметь метки минимум из двух категорий:
1. **Сервис** или **Категория** (service:*, infra, docs)
2. **Тип** (feature, bug, enhancement)

Остальные метки (приоритет, статус) добавляются по необходимости.

---

## Метки по сервису

| Метка | Описание | Пример задачи |
|-------|----------|---------------|
| `service:auth` | Сервис аутентификации | OAuth, JWT, 2FA |
| `service:notify` | Сервис уведомлений | Email, SMS, push |
| `service:payment` | Сервис платежей | Stripe, PayPal, подписки |
| `service:users` | Сервис пользователей | Профили, настройки |
| `service:gateway` | API gateway | Rate limiting, routing |

### Категории (не сервисы)

| Метка | Описание | Пример задачи |
|-------|----------|---------------|
| `infra` | Инфраструктура | CI/CD, Docker, K8s |
| `docs` | Документация | README, API docs |

---

## Метки по типу

| Метка | Описание | Когда использовать |
|-------|----------|-------------------|
| `feature` | Новая функциональность | Добавление нового функционала |
| `bug` | Ошибка | Исправление дефекта |
| `enhancement` | Улучшение | Оптимизация существующего |
| `refactor` | Рефакторинг | Улучшение кода без изменения поведения |
| `security` | Безопасность | Уязвимости, аудит |

### Выбор типа

```
Новый функционал?           → feature
Что-то сломано?             → bug
Работает, но можно лучше?   → enhancement
Код нужно переписать?       → refactor
Связано с безопасностью?    → security
```

---

## Метки по приоритету

| Метка | Описание | SLA | Когда использовать |
|-------|----------|-----|-------------------|
| `priority:critical` | Критический | Немедленно | Продакшн падает |
| `priority:high` | Высокий | 1-2 дня | Блокирует релиз |
| `priority:medium` | Средний | 1 неделя | Важно, но не срочно |
| `priority:low` | Низкий | Бэклог | Nice-to-have |

### Правила приоритизации

| Ситуация | Приоритет |
|----------|-----------|
| Баг в продакшене | `priority:critical` или `priority:high` |
| Регрессия после деплоя | `priority:high` |
| Новая фича для релиза | `priority:medium` |
| Технический долг | `priority:low` |
| Улучшение UX | `priority:medium` или `priority:low` |

---

## Метки по статусу

| Метка | Описание | Кто ставит |
|-------|----------|-----------|
| `in-progress` | В работе | `/issue-execute` |
| `blocked` | Заблокировано | Вручную |
| `needs-review` | Требует ревью | `/issue-review` |
| `ready-for-release` | Готово к релизу | После мержа PR |

### Жизненный цикл статусов

```
[создан] → in-progress → needs-review → [закрыт]
              ↓
           blocked
              ↓
          in-progress
```

### Правила статусов

| Правило | Описание |
|---------|----------|
| Один статус одновременно | Нельзя `in-progress` + `blocked` |
| `in-progress` снимается автоматически | При закрытии Issue |
| `blocked` требует комментарий | Указать, чем заблокировано |

---

## Комбинации меток

### Обязательные комбинации

| Сценарий | Метки |
|----------|-------|
| Баг в auth | `service:auth`, `bug` |
| Фича в payment | `service:payment`, `feature` |
| Срочный баг | `service:*`, `bug`, `priority:high` |
| Задача в работе | `service:*`, `type`, `in-progress` |

### Типичные комбинации

```bash
# Срочный баг в авторизации
service:auth, bug, priority:high, in-progress

# Новая фича в уведомлениях
service:notify, feature, priority:medium

# Документация на ревью
docs, needs-review

# Заблокированная задача
service:payment, feature, blocked
```

### Несовместимые комбинации

| Комбинация | Почему нельзя |
|------------|---------------|
| `bug` + `feature` | Задача или исправляет, или добавляет |
| `in-progress` + `blocked` | Если заблокировано — не в работе |
| Два `service:*` | Разбить на отдельные Issues |

---

## Управление метками

### Добавление метки

```bash
# Через gh CLI
gh issue edit 123 --add-label "in-progress"

# Через скилл
/issue-update 123 --add-label "in-progress"
```

### Удаление метки

```bash
# Через gh CLI
gh issue edit 123 --remove-label "in-progress"

# Через скилл
/issue-update 123 --remove-label "in-progress"
```

### Создание новой метки

```bash
# Создать метку с цветом
gh label create "service:newservice" --color "0E8A16" --description "Новый сервис"
```

### Цвета меток (convention)

| Категория | Цвет | Hex |
|-----------|------|-----|
| service:* | Зелёный | `0E8A16` |
| bug | Красный | `D73A4A` |
| feature | Синий | `0075CA` |
| enhancement | Голубой | `A2EEEF` |
| priority:high | Оранжевый | `FF7619` |
| priority:low | Серый | `C5DEF5` |
| in-progress | Жёлтый | `FEF2C0` |
| blocked | Красный | `B60205` |

---

## Фильтрация по меткам

### Примеры запросов

```bash
# Все открытые по сервису
gh issue list --label "service:auth" --state open

# Срочные баги
gh issue list --label "bug" --label "priority:high"

# В работе у меня
gh issue list --label "in-progress" --assignee @me

# Заблокированные
gh issue list --label "blocked"
```

### Веб-интерфейс

```
# URL фильтры
is:open label:service:auth label:bug
is:open label:priority:high
is:open assignee:@me label:in-progress
```

---

## Связанные инструкции

- [format.md](./format.md) — формат Issue
- [workflow.md](./workflow.md) — жизненный цикл
- [commands.md](./commands.md) — команды gh

---

> **Путь:** `/.claude/instructions/issues/labels.md`
