---
description: Валидация GitHub Milestone по стандарту — формат версии, описание, привязка Issue, статус.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/milestones/README.md
---

# Валидация Milestone

Рабочая версия стандарта: 1.1

Проверка соответствия GitHub Milestone стандарту: title, description, due date, связь с Issues и Release.

**Полезные ссылки:**
- [Инструкции Milestones](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-milestone.md](./standard-milestone.md) |
| Валидация | Этот документ |
| Создание | [create-milestone.md](./create-milestone.md) |
| Модификация | [modify-milestone.md](./modify-milestone.md) |

## Оглавление

- [Когда валидировать](#когда-валидировать)
- [Шаги](#шаги)
  - [Шаг 1: Проверить title (SemVer)](#шаг-1-проверить-title-semver)
  - [Шаг 2: Проверить description](#шаг-2-проверить-description)
  - [Шаг 3: Проверить due date](#шаг-3-проверить-due-date)
  - [Шаг 4: Проверить Issues](#шаг-4-проверить-issues)
  - [Шаг 5: Проверить связь с Release (для закрытых)](#шаг-5-проверить-связь-с-release-для-закрытых)
- [Чек-лист](#чек-лист)
- [Типичные ошибки](#типичные-ошибки)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Когда валидировать

Запускать валидацию:

1. **После создания Milestone** — проверить title, description, due date
2. **Перед закрытием Milestone** — проверить что все Issues закрыты, критерии готовности выполнены
3. **Перед созданием Release** — проверить что Milestone закрыт, связь корректна
4. **Периодически** — аудит открытых Milestones (просроченные, перегруженные)

---

## Шаги

### Шаг 1: Проверить title (SemVer)

**SSOT:** [standard-milestone.md § 4](./standard-milestone.md#4-версионирование-semver)

**Вручную:**

1. Получить title Milestone:
   ```bash
   gh api repos/{owner}/{repo}/milestones/{number} -q '.title'
   ```

2. Проверить формат:

| Правило | Корректно | Некорректно |
|---------|-----------|-------------|
| Префикс `v` | `v1.0.0` | `1.0.0` |
| SemVer формат | `v1.2.3` | `v1.2` |
| Pre-release допустим | `v1.0.0-beta.1` | `v1.0.0_beta` |
| Без пробелов | `v1.0.0` | `v 1.0.0` |

**Критерии прохождения:**
- Title соответствует формату `vMAJOR.MINOR.PATCH[-PRERELEASE]`
- Title уникален среди всех Milestones

---

### Шаг 2: Проверить description

**SSOT:** [standard-milestone.md § 5 Description](./standard-milestone.md#description)

**Вручную:**

1. Получить description Milestone:
   ```bash
   gh api repos/{owner}/{repo}/milestones/{number} -q '.description'
   ```

2. Проверить обязательные секции:

| Секция | Обязательна | Проверка |
|--------|:-----------:|----------|
| `## Цель` | да | Описывает зачем создаётся Milestone |
| `## Критерии готовности` | да | Содержит чек-лист `- [ ]` |
| `## Фокус` | нет | Направления работы |

**Критерии прохождения:**
- Присутствует секция "Цель" с описанием
- Присутствует секция "Критерии готовности" с хотя бы одним пунктом `- [ ]`

---

### Шаг 3: Проверить due date

**SSOT:** [standard-milestone.md § 5 Due Date](./standard-milestone.md#due-date)

**Вручную:**

1. Получить due date:
   ```bash
   gh api repos/{owner}/{repo}/milestones/{number} -q '.due_on'
   ```

2. Проверить:

| Правило | Проверка |
|---------|----------|
| Due date установлен | `due_on != null` |
| Формат ISO 8601 | `YYYY-MM-DDTHH:MM:SSZ` |
| Не в прошлом (для open) | `due_on >= now()` |

**Критерии прохождения:**
- Due date установлен
- Для открытых Milestones — due date не просрочен (или просрочен менее чем на 7 дней)

---

### Шаг 4: Проверить Issues

**SSOT:** [standard-issue.md § 9](../issues/standard-issue.md#9-связь-с-milestones)

**Вручную:**

1. Получить статистику:
   ```bash
   gh api repos/{owner}/{repo}/milestones/{number} \
     -q '{open: .open_issues, closed: .closed_issues}'
   ```

2. Проверить:

| Правило | Проверка |
|---------|----------|
| Не перегружен | `open + closed <= 20` |
| Есть Issues | `open + closed > 0` |
| Для закрытия: все закрыты | `open == 0` |

3. Список открытых Issues (если есть):
   ```bash
   gh issue list --milestone "{title}" --state open
   ```

**Критерии прохождения:**
- Milestone содержит от 1 до 20 Issues
- Для закрытого Milestone — `open_issues == 0`

---

### Шаг 5: Проверить связь с Release (для закрытых)

**SSOT:** [standard-release.md § 9–10](../releases/standard-release.md#9-подготовка-релиза)

**Вручную:**

1. Проверить наличие Release с тегом, совпадающим с title Milestone:
   ```bash
   gh release view "{title}" --json tagName,name 2>/dev/null
   ```

2. Если Milestone закрыт:

| Правило | Проверка |
|---------|----------|
| Release существует | Команда выше вернула результат |
| Release Notes содержит ссылку на Milestone | `## Milestone` в body Release |

**Критерии прохождения:**
- Для закрытого Milestone — существует GitHub Release с соответствующим тегом
- Release Notes содержит ссылку на Milestone

---

## Чек-лист

### Title
- [ ] Формат `vMAJOR.MINOR.PATCH[-PRERELEASE]`
- [ ] Уникален среди всех Milestones
- [ ] Длина до 50 символов

### Description
- [ ] Присутствует секция "Цель"
- [ ] Присутствует секция "Критерии готовности" с чек-листом
- [ ] Description не пустой

### Due Date
- [ ] Due date установлен
- [ ] Формат ISO 8601
- [ ] Не просрочен (для открытых)

### Issues
- [ ] Milestone содержит Issues (не пустой)
- [ ] Не перегружен (макс. 20 Issues)
- [ ] Для закрытия: все Issues закрыты (`open_issues == 0`)

### Release (для закрытых Milestones)
- [ ] Существует GitHub Release с тегом = title Milestone
- [ ] Release Notes содержит ссылку на Milestone

---

## Типичные ошибки

| Ошибка | Код | Причина | Решение |
|--------|-----|---------|---------|
| Title не SemVer | E001 | Название не соответствует `vX.Y.Z` | Переименовать: `gh api PATCH .../milestones/{n} -f title="vX.Y.Z"` |
| Title без префикса `v` | E002 | Пропущен префикс | Добавить `v` к title |
| Дубликат title | E003 | Milestone с таким title уже существует | Выбрать другую версию или удалить дубликат |
| Description пустой | E004 | Не заполнено описание | Добавить секции "Цель" и "Критерии готовности" |
| Нет "Критериев готовности" | E005 | Отсутствует чек-лист в description | Добавить секцию `## Критерии готовности` |
| Due date не установлен | E006 | Пропущен при создании | Установить: `gh api PATCH .../milestones/{n} -f due_on="..."` |
| Due date просрочен | E007 | Milestone не закрыт вовремя | Продлить due date или закрыть Milestone |
| Milestone перегружен | E008 | Более 20 Issues | Перенести часть Issues в следующий Milestone |
| Milestone пустой | E009 | Нет Issues | Добавить Issues или удалить Milestone |
| Закрыт с открытыми Issues | E010 | Issues не завершены | Переоткрыть Milestone или перенести Issues |
| Нет Release для закрытого | E011 | Release не создан после закрытия | Создать Release по процессу из release-workflow |
| Нет ссылки на Milestone в Release | E012 | Пропущена секция "Milestone" в Release Notes | Добавить секцию `## Milestone` в Release Notes |

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-milestone.py](../.scripts/validate-milestone.py) | Валидация Milestone: title, description, due date, Issues, Release | Этот документ |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/milestone-validate](/.claude/skills/milestone-validate/SKILL.md) | Валидация Milestone по стандарту | Этот документ |
