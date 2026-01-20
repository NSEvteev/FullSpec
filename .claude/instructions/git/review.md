---
type: standard
description: Code review: чек-лист, CODEOWNERS, правила approve
related:
  - git/workflow.md
  - git/commits.md
  - git/ci.md
---

# Code Review

Правила проведения code review: чек-лист проверки, CODEOWNERS, процесс approve.

## Оглавление

- [Правила](#правила)
  - [Процесс review](#процесс-review)
  - [CODEOWNERS](#codeowners)
  - [Чек-лист reviewer](#чек-лист-reviewer)
  - [Чек-лист self-review (для автора)](#чек-лист-self-review-для-автора)
  - [Правила approve](#правила-approve)
  - [Комментарии](#комментарии)
- [Скиллы](#скиллы)
- [Примеры](#примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Процесс review

**Правило:** Каждый PR требует минимум 1 approve перед merge.

| Этап | Действие | Ответственный |
|------|----------|---------------|
| 1. Создание PR | Автор описывает изменения | Автор |
| 2. Автоматические проверки | CI запускает тесты, линтер | CI |
| 3. Назначение reviewer | Автоматически через CODEOWNERS | GitHub |
| 4. Review | Проверка кода по чек-листу | Reviewer |
| 5. Исправление замечаний | Автор вносит изменения | Автор |
| 6. Approve | Reviewer одобряет PR | Reviewer |
| 7. Merge | Автор мержит после approve | Автор |

**Правило:** Review должен быть завершён в течение 1 рабочего дня.

**SLA по приоритету:**

| Приоритет | Время на review | Когда применять |
|-----------|-----------------|-----------------|
| Critical | 4 часа | Hotfix, security fix |
| High | 8 часов | Блокирующие задачи |
| Normal | 1 рабочий день | Обычные PR |
| Low | 2 рабочих дня | Рефакторинг, docs |

### CODEOWNERS

**Правило:** Файл `.github/CODEOWNERS` определяет ответственных за код.

```
# .github/CODEOWNERS

# По умолчанию — вся команда
*                       @org/team

# Сервисы
/src/auth/              @org/auth-team
/src/notification/      @org/notify-team
/src/payment/           @org/payment-team

# Инфраструктура
/platform/              @org/devops
/.github/               @org/devops

# Документация
/doc/                   @org/docs-team
/.claude/               @org/ai-team

# Общий код — требует 2 approve
/shared/                @org/architects
```

**Правило:** Изменения в protected paths требуют approve от CODEOWNERS.

### Чек-лист reviewer

**Правило:** Reviewer проверяет PR по следующим критериям:

**Функциональность:**
- [ ] Код решает заявленную задачу
- [ ] Нет регрессий в существующем функционале
- [ ] Edge cases обработаны

**Качество кода:**
- [ ] Код читаем и понятен
- [ ] Нет дублирования (DRY)
- [ ] Функции/методы имеют одну ответственность
- [ ] Именование понятное и консистентное

**Тесты:**
- [ ] Добавлены тесты для нового кода
- [ ] Тесты покрывают основные сценарии
- [ ] Тесты покрывают edge cases

**Безопасность:**
- [ ] Нет hardcoded секретов
- [ ] Входные данные валидируются
- [ ] SQL/NoSQL инъекции невозможны
- [ ] XSS/CSRF защита (для frontend)

**Производительность:**
- [ ] Нет N+1 запросов к БД
- [ ] Большие операции выполняются асинхронно
- [ ] Используется кэширование где уместно

**Документация:**
- [ ] Публичные API задокументированы
- [ ] Сложная логика прокомментирована
- [ ] README обновлён (если нужно)

### Чек-лист self-review (для автора)

**Правило:** Автор проводит self-review перед запросом review.

- [ ] Код компилируется без ошибок
- [ ] Все тесты проходят локально
- [ ] Нет закомментированного кода
- [ ] Нет console.log / print для отладки
- [ ] PR описание заполнено (Summary, Test plan)
- [ ] Связан с Issue (например, `Closes #42` или `Fixes #15`)
- [ ] Изменения соответствуют scope задачи (не больше)
- [ ] Проверил diff — нет случайных изменений

### Правила approve

**Правило:** Approve означает "код готов к merge".

| Тип изменений | Требуется approve | От кого |
|---------------|-------------------|---------|
| Обычные изменения | 1 | Любой член команды |
| Изменения в shared/ | 2 | CODEOWNERS |
| Изменения в platform/ | 1 | DevOps |
| Breaking changes | 2 | Tech lead + CODEOWNERS |

**Правило:** Stale reviews отклоняются при новых коммитах.

```yaml
# Branch protection rule
dismiss_stale_reviews: true
require_review_from_code_owners: true
required_approving_review_count: 1
```

**Правило:** Автор НЕ может approve свой PR.

### Комментарии

**Правило:** Комментарии должны быть конструктивными и конкретными.

| Префикс | Значение | Действие |
|---------|----------|----------|
| `nit:` | Мелочь, необязательно | Опционально исправить |
| `suggestion:` | Предложение улучшения | Рассмотреть |
| `question:` | Вопрос для понимания | Ответить |
| `blocker:` | Блокирует approve | Обязательно исправить |

**Примеры комментариев:**

```
nit: можно использовать early return для читаемости

suggestion: рассмотри использование map() вместо forEach()

question: почему выбран этот подход вместо X?

blocker: отсутствует валидация входных данных, возможна SQL инъекция
```

**Правило:** Избегать:
- Субъективных замечаний без обоснования
- Токсичных комментариев
- Требований переписать "по-своему" без причины

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/issue-review](/.claude/skills/issue-review/SKILL.md) | Автоматическое ревью решения перед закрытием Issue |

---

## Примеры

### Пример 1: CODEOWNERS для микросервисов

```
# .github/CODEOWNERS

# Глобальные владельцы
*                           @company/backend-team

# Сервисы (каждая команда владеет своим)
/src/auth/                  @company/auth-team @john
/src/notification/          @company/notify-team
/src/payment/               @company/payment-team @jane
/src/users/                 @company/users-team
/src/gateway/               @company/platform-team

# Инфраструктура
/platform/                  @company/devops
/config/                    @company/devops
/.github/workflows/         @company/devops

# Общий код — требует внимания архитекторов
/shared/contracts/          @company/architects
/shared/libs/               @company/architects @company/backend-team

# Документация
/doc/                       @company/tech-writers
/.claude/                   @company/ai-team
/CLAUDE.md                  @company/ai-team

# Конфигурации безопасности
/src/*/security/            @company/security-team
```

### Пример 2: PR template с чек-листом

```markdown
<!-- .github/pull_request_template.md -->

## Описание

<!-- Что изменено и зачем -->

## Тип изменений

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Чек-лист автора

- [ ] Код соответствует code style
- [ ] Добавлены/обновлены тесты
- [ ] Документация обновлена
- [ ] Self-review выполнен

## Связанные Issues

<!-- Используйте ключевые слова GitHub для автоматического закрытия Issue -->
Closes #42 <!-- Добавить валидацию email в форму регистрации -->
Fixes #15 <!-- Исправить ошибку отображения на мобильных устройствах -->

## Screenshots (если UI)

<!-- Добавьте скриншоты -->
```

### Пример 3: Branch protection rules

```yaml
# Концептуальная конфигурация (настраивается в UI GitHub)
main:
  protection:
    required_status_checks:
      strict: true
      contexts:
        - lint
        - test
        - security

    required_pull_request_reviews:
      required_approving_review_count: 1
      dismiss_stale_reviews: true
      require_code_owner_reviews: true

    restrictions:
      users: []
      teams:
        - devops

    enforce_admins: true
    allow_force_pushes: false
    allow_deletions: false
```

### Пример 4: Конструктивные комментарии

**Плохо:**
```
Это неправильно. Перепиши.
```

**Хорошо:**
```
blocker: Эта функция может вернуть null, но вызывающий код не проверяет это.

Предлагаю:
1. Добавить проверку на null в вызывающем коде
2. Или изменить функцию, чтобы она выбрасывала исключение

Что думаешь?
```

**Плохо:**
```
Мне не нравится этот стиль.
```

**Хорошо:**
```
nit: По нашему code style используем camelCase для переменных.
См. docs/code-style.md#naming
```

---

## Связанные инструкции

- [workflow.md](workflow.md) — Git workflow, ветки, PR
- [commits.md](commits.md) — Формат сообщений коммитов
- [ci.md](ci.md) — CI/CD pipeline, автоматические проверки
