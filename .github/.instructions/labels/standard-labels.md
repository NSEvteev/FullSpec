---
description: Стандарт управления метками GitHub
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/labels/README.md
---

# Стандарт управления метками

Версия стандарта: 1.0

Правила создания, применения и управления метками (Labels) для Issues и Pull Requests.

**Полезные ссылки:**
- [Справочник меток](../../labels/labels.md) — SSOT категорий и меток
- [Инструкции](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Справочник | [labels.md](../../labels/labels.md) — категории и метки |
| Валидация | *Будет создан* |
| Создание | *Будет создан* |
| Модификация | *Будет создан* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Naming Convention](#2-naming-convention)
- [3. Правила применения](#3-правила-применения)
- [4. Разрешение конфликтов](#4-разрешение-конфликтов)
- [5. Добавление категории](#5-добавление-категории)
- [6. Добавление метки](#6-добавление-метки)
- [7. Удаление метки](#7-удаление-метки)
- [8. Переименование метки](#8-переименование-метки)
- [9. Синхронизация с GitHub](#9-синхронизация-с-github)
- [10. Автоматизация](#10-автоматизация)

---

## 1. Назначение

Система меток для категоризации Issues и Pull Requests.

**Применяется к:**
- GitHub Issues
- GitHub Pull Requests

**Цель:**
- Классификация задач по типу, приоритету, статусу, области кода
- Быстрый поиск и фильтрация
- Визуальная идентификация (через цветовое кодирование)
- Автоматизация в GitHub Projects и Actions

**Принципы:**
- Каждая метка принадлежит категории (префикс)
- Одна задача может иметь несколько меток из разных категорий
- Цвет одинаков в рамках категории (кроме priority — градиент)
- Справочник меток хранится в [labels.md](../../labels/labels.md)

---

## 2. Naming Convention

**Формат метки:**
```
{category}:{value}
```

| Элемент | Правило | Пример |
|---------|---------|--------|
| `{category}` | Название категории (lowercase) | `type`, `priority`, `status` |
| `:` | Разделитель (ОБЯЗАТЕЛЬНО) | `:` |
| `{value}` | Значение в kebab-case (lowercase) | `bug`, `in-review`, `high` |

**Правила:**
- Только латиница
- Нижний регистр (lowercase)
- Дефис `-` для разделения слов (kebab-case)
- Без пробелов, подчёркиваний, camelCase

**Примеры:**

| Формат | Корректно | Причина |
|--------|-----------|---------|
| `type:bug` | ✅ | — |
| `priority:high` | ✅ | — |
| `status:in-review` | ✅ | kebab-case для значения |
| `Type:Bug` | ❌ | Верхний регистр |
| `priority_high` | ❌ | Подчёркивание вместо двоеточия |
| `bugfix` | ❌ | Нет категории |
| `type: bug` | ❌ | Пробел после двоеточия |

---

## 3. Правила применения

### Обязательные метки

Каждая задача (Issue) ДОЛЖНА иметь:
- **Ровно одну** метку `type:*` — тип задачи
- **Ровно одну** метку `priority:*` — приоритет

### Опциональные метки

Добавлять метку, если задача затрагивает соответствующую область:

| Категория | Когда добавлять |
|-----------|-----------------|
| `status:*` | Задача заблокирована, на ревью, или готова к работе |
| `area:*` | Задача затрагивает конкретную область кода (макс. 3) |
| `effort:*` | Для планирования спринтов |
| `env:*` | ТОЛЬКО для `type:bug` — где проявляется баг |

### Примеры применения

**Баг на production:**
```
type:bug
priority:critical
area:backend
area:api
env:production
effort:s
```

**Новая фича:**
```
type:feature
priority:medium
area:frontend
effort:m
```

**Документация:**
```
type:docs
priority:low
area:docs
effort:xs
```

---

## 4. Разрешение конфликтов

| Конфликт | Правило |
|----------|---------|
| Несколько меток `type:*` | Удалить все, кроме одной основной. Если неясно — спросить автора Issue. |
| Несколько меток `priority:*` | Удалить все, кроме одной. Приоритет выбирается автором или maintainer. |
| `env:*` на не-баге | **Удалить** метку `env:*`. Метки окружения только для `type:bug`. |
| Более 3 меток `area:*` | Оставить 3 основные. Если больше — разбить задачу на подзадачи. |

**Валидация:** Если на задаче есть `env:*`, проверить наличие `type:bug`. Если `type:bug` отсутствует — удалить метку `env:*`.

---

## 5. Добавление категории

Новая категория добавляется редко (раз в полгода-год).

**Когда добавлять:**
- Появилась новая ось классификации, которую нельзя выразить существующими категориями
- Категория будет использоваться регулярно (>10% задач)

**Процесс:**

1. **Обоснование:** Описать в Issue/PR, зачем нужна категория
2. **Naming:** Выбрать префикс (lowercase, короткий)
3. **Цвет:** Выбрать уникальный HEX, не пересекающийся с существующими
4. **Метки:** Определить начальный набор меток категории
5. **Обновить labels.md:**
   - Добавить строку в таблицу "Категории"
   - Добавить секцию с метками
   - Добавить в `labels.yml`
6. **Синхронизация:** Выполнить `gh label create` для новых меток
7. **Документация:** Обновить README области

**Пример:**
```bash
# Добавить категорию "scope" с метками
gh label create "scope:mvp" --description "MVP релиз" --color "22D3EE"
gh label create "scope:v2" --description "Версия 2.0" --color "22D3EE"
```

---

## 6. Добавление метки

Новая метка в существующей категории.

**Когда добавлять:**
- Появилось новое значение, которое используется регулярно
- Нельзя выразить существующими метками

**Процесс:**

1. **Проверить:** Метка не дублирует существующую
2. **Naming:** `{category}:{value}` в kebab-case
3. **Цвет:** Использовать цвет категории (из [labels.md](../../labels/labels.md))
4. **Обновить labels.md:**
   - Добавить строку в таблицу категории
   - Добавить в `labels.yml`
5. **Синхронизация:**
   ```bash
   gh label create "{category}:{value}" --description "{описание}" --color "{HEX}"
   ```

**Пример:**
```bash
# Добавить метку area:mobile
gh label create "area:mobile" --description "Мобильное приложение" --color "10B981"
```

---

## 7. Удаление метки

**Когда удалять:**
- Метка не используется >6 месяцев
- Метка дублирует другую
- Область кода удалена из проекта

**Процесс:**

1. **Проверить использование:**
   ```bash
   gh issue list --label "{метка}" --state all --limit 100
   gh pr list --label "{метка}" --state all --limit 100
   ```
2. **Мигрировать:** Если есть Issues/PR с меткой — заменить на альтернативную или удалить
3. **Удалить из GitHub:**
   ```bash
   gh label delete "{метка}" --yes
   ```
4. **Обновить labels.md:**
   - Удалить строку из таблицы
   - Удалить из `labels.yml`

**Важно:** НЕ удалять метки категорий `type:*` и `priority:*` без согласования.

---

## 8. Переименование метки

**Когда переименовывать:**
- Название неточно отражает назначение
- Изменилась терминология проекта

**Процесс:**

1. **Найти все Issues/PR с меткой:**
   ```bash
   gh issue list --label "{старое_имя}" --state all --json number -q '.[].number'
   ```
2. **Создать новую метку:**
   ```bash
   gh label create "{новое_имя}" --description "{описание}" --color "{HEX}"
   ```
3. **Заменить на всех Issues/PR:**
   ```bash
   # Для каждого номера:
   gh issue edit {number} --remove-label "{старое_имя}" --add-label "{новое_имя}"
   ```
4. **Удалить старую метку:**
   ```bash
   gh label delete "{старое_имя}" --yes
   ```
5. **Обновить labels.md**

**Пример: переименование `area:infra` → `area:platform`:**
```bash
gh label create "area:platform" --description "Инфраструктура" --color "10B981"
for num in $(gh issue list --label "area:infra" --state all --json number -q '.[].number'); do
  gh issue edit $num --remove-label "area:infra" --add-label "area:platform"
done
gh label delete "area:infra" --yes
```

---

## 9. Синхронизация с GitHub

Метки хранятся в [labels.md](../../labels/labels.md) в секции `labels.yml`.

**Ручная синхронизация:**
```bash
# Создать метку
gh label create "{name}" --description "{desc}" --color "{hex}"

# Обновить описание/цвет
gh label edit "{name}" --description "{new_desc}" --color "{new_hex}"

# Удалить метку
gh label delete "{name}" --yes

# Список всех меток
gh label list
```

**Автоматическая синхронизация:**

Скрипт `setup-labels.py` (будет создан) синхронизирует `labels.yml` с GitHub:
```bash
python .github/.instructions/.scripts/setup-labels.py
```

---

## 10. Автоматизация

### Через Issue Templates

Issue Templates могут содержать предустановленные метки:

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
labels:
  - type:bug
  - priority:medium
```

### Через GitHub Actions

Автоматическое добавление меток на основе содержимого:

```yaml
# .github/workflows/auto-label.yml
name: Auto Label
on:
  issues:
    types: [opened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            const body = context.payload.issue.body || '';
            const labels = [];

            if (body.includes('backend')) labels.push('area:backend');
            if (body.includes('frontend')) labels.push('area:frontend');

            if (labels.length > 0) {
              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue.number,
                labels: labels
              });
            }
```

### Интеграция с GitHub Projects

Метки используются для автоматической организации в Project Board:

| Метка | Действие |
|-------|----------|
| `status:ready` | Переместить в колонку "Ready" |
| `status:wip` | Переместить в колонку "In Progress" |
| `status:in-review` | Переместить в колонку "Review" |
| `status:blocked` | Переместить в колонку "Blocked" |

---

## Скиллы

*Нет скиллов.*
