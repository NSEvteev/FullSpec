---
description: Воркфлоу создания GitHub Milestone — версия, описание, срок, привязка Issue. Включает валидацию.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/milestones/README.md
---

# Воркфлоу создания Milestone

Рабочая версия стандарта: 1.1

Пошаговый процесс создания нового GitHub Milestone.

**Полезные ссылки:**
- [Инструкции Milestones](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-milestone.md](./standard-milestone.md) |
| Валидация | [validation-milestone.md](./validation-milestone.md) |
| Создание | Этот документ |
| Модификация | [modify-milestone.md](./modify-milestone.md) |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Определить версию](#шаг-1-определить-версию)
  - [Шаг 2: Проверить уникальность](#шаг-2-проверить-уникальность)
  - [Шаг 3: Подготовить description](#шаг-3-подготовить-description)
  - [Шаг 4: Установить due date](#шаг-4-установить-due-date)
  - [Шаг 5: Создать Milestone через API](#шаг-5-создать-milestone-через-api)
  - [Шаг 6: Валидация](#шаг-6-валидация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Один Milestone = одна версия продукта (vX.Y.Z).** Milestone напрямую связан с GitHub Release.

> **SemVer — единственный формат title.** Формат: `vMAJOR.MINOR.PATCH[-PRERELEASE]`. SSOT: [standard-milestone.md § 4](./standard-milestone.md#4-версионирование-semver).

> **Description обязателен.** Секции "Цель" и "Критерии готовности" — обязательны.

> **Версия определяется по conventional commits.** `feat:` → MINOR, `fix:` → PATCH, `BREAKING CHANGE:` → MAJOR.

---

## Шаги

### Шаг 1: Определить версию

**SSOT:** [standard-milestone.md § 4](./standard-milestone.md#4-версионирование-semver)

1. Получить последнюю версию:
   ```bash
   gh api repos/{owner}/{repo}/milestones -f state=all -f sort=due_on -f direction=desc \
     -q '.[0].title'
   ```

2. Определить тип инкремента по планируемым изменениям:

   | Изменения | Инкремент | Пример |
   |-----------|-----------|--------|
   | Breaking changes | MAJOR | `v1.0.0` → `v2.0.0` |
   | Новая функциональность | MINOR | `v1.0.0` → `v1.1.0` |
   | Исправления багов | PATCH | `v1.0.0` → `v1.0.1` |
   | Первый Milestone | — | `v0.1.0` |

3. Сформировать title: `v{MAJOR}.{MINOR}.{PATCH}`

### Шаг 2: Проверить уникальность

```bash
# Проверить что Milestone с таким title не существует
EXISTING=$(gh api repos/{owner}/{repo}/milestones -f state=all \
  -q '.[] | select(.title == "v1.0.0") | .number')

if [ -n "$EXISTING" ]; then
  echo "ERROR: Milestone v1.0.0 уже существует (number: $EXISTING)"
  exit 1
fi
```

**Если существует:**
- Выбрать другую версию (следующий инкремент)
- Или использовать pre-release: `v1.0.0-beta.1`

### Шаг 3: Подготовить description

**SSOT:** [standard-milestone.md § 5 Description](./standard-milestone.md#description)

**Обязательная структура:**

```markdown
## Цель

{Зачем создаётся этот Milestone, какая проблема решается}

## Критерии готовности

- [ ] {Критерий 1}
- [ ] {Критерий 2}
```

**Опционально:**

```markdown
## Фокус

{Основные направления работы}
```

**Правила:**
- Секция "Цель" — обязательна, описывает зачем создаётся Milestone
- Секция "Критерии готовности" — обязательна, содержит чек-лист `- [ ]`
- Минимум 1 критерий готовности

### Шаг 4: Установить due date

**SSOT:** [standard-milestone.md § 5 Due Date](./standard-milestone.md#due-date)

**Формат:** ISO 8601 — `YYYY-MM-DDTHH:MM:SSZ`

**Рекомендация:** использовать `23:59:59Z` (конец дня).

```bash
# Пример: дедлайн 15 марта 2025
DUE_DATE="2025-03-15T23:59:59Z"
```

### Шаг 5: Создать Milestone через API

```bash
gh api POST /repos/{owner}/{repo}/milestones \
  -f title="v1.0.0" \
  -f description="## Цель

Первый стабильный релиз

## Критерии готовности

- [ ] MVP реализован
- [ ] Тесты покрывают основную функциональность" \
  -f due_on="2025-03-15T23:59:59Z"
```

**Ответ (успех):**

```json
{
  "number": 3,
  "title": "v1.0.0",
  "state": "open",
  "due_on": "2025-03-15T23:59:59Z",
  "html_url": "https://github.com/owner/repo/milestone/3"
}
```

**Обработка ошибок:**

| Код ошибки | Причина | Решение |
|------------|---------|---------|
| `422` | Title уже существует | Выбрать другую версию |
| `400` | Невалидный формат `due_on` | Использовать ISO 8601 |
| `403` | Нет прав | Проверить доступ к репозиторию |

### Шаг 6: Валидация

Запустить валидацию созданного Milestone:

```bash
python .github/.instructions/.scripts/validate-milestone.py --title "v1.0.0"
```

Или через скилл: `/milestone-validate --title "v1.0.0"`

**Критерии прохождения:** все проверки без ошибок (E001-E009).

---

## Чек-лист

### Подготовка
- [ ] Определена версия (SemVer)
- [ ] Проверена уникальность title
- [ ] Подготовлен description с секциями "Цель" и "Критерии готовности"
- [ ] Установлен due date (ISO 8601)

### Создание
- [ ] Milestone создан через `gh api POST`
- [ ] Получен номер Milestone (number)
- [ ] Ответ API не содержит ошибок

### Проверка
- [ ] Валидация пройдена (`/milestone-validate`)
- [ ] Title — SemVer формат (`vX.Y.Z`)
- [ ] Description содержит "Цель" и "Критерии готовности"
- [ ] Due date установлен и не в прошлом

---

## Примеры

### Создание первого Milestone (v0.1.0)

```bash
# 1. Проверить уникальность
gh api repos/{owner}/{repo}/milestones -f state=all -q '.[].title'
# Пусто → можно создавать v0.1.0

# 2. Создать
gh api POST /repos/{owner}/{repo}/milestones \
  -f title="v0.1.0" \
  -f description="## Цель

Первая рабочая версия проекта (MVP).

## Критерии готовности

- [ ] Базовая структура проекта
- [ ] GitHub инструкции настроены
- [ ] CI/CD pipeline работает" \
  -f due_on="2026-03-01T23:59:59Z"

# 3. Валидация
python .github/.instructions/.scripts/validate-milestone.py --title "v0.1.0"
```

### Создание pre-release Milestone

```bash
gh api POST /repos/{owner}/{repo}/milestones \
  -f title="v1.0.0-beta.1" \
  -f description="## Цель

Beta-версия для публичного тестирования.

## Критерии готовности

- [ ] Все фичи MVP реализованы
- [ ] Критических багов нет
- [ ] Документация обновлена" \
  -f due_on="2026-02-28T23:59:59Z"
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [create-milestone.py](../.scripts/create-milestone.py) | Создание Milestone: версия, уникальность, API | Этот документ |
| [validate-milestone.py](../.scripts/validate-milestone.py) | Валидация созданного Milestone | [validation-milestone.md](./validation-milestone.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/milestone-create](/.claude/skills/milestone-create/SKILL.md) | Создание Milestone | Этот документ |
