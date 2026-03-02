---
description: Стандарт управления метками GitHub — категории, именование, цвета, синхронизация labels.yml с репозиторием.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/labels/README.md
---

# Стандарт управления метками

Версия стандарта: 1.3

Правила создания, применения и управления метками (Labels) для Issues и Pull Requests.

**Полезные ссылки:**
- [Справочник меток](../labels.yml) — SSOT категорий и меток
- [Инструкции](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Справочник | [labels.yml](../labels.yml) — категории и метки |
| Валидация | [validation-labels.md](./validation-labels.md) |
| Создание | *Не требуется (labels.yml создаётся разово)* |
| Модификация | [modify-labels.md](./modify-labels.md) |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Naming Convention](#2-naming-convention)
- [3. Правила применения](#3-правила-применения)
- [4. Связь TYPE-меток с Issue Templates](#4-связь-type-меток-с-issue-templates)
- [5. Разрешение конфликтов](#5-разрешение-конфликтов)
- [6. Добавление категории](#6-добавление-категории)
- [7. Добавление метки](#7-добавление-метки)
- [8. Удаление метки](#8-удаление-метки)
- [9. Переименование метки](#9-переименование-метки)
- [10. Переименование категории](#10-переименование-категории)
- [11. Синхронизация с GitHub](#11-синхронизация-с-github)
- [12. Автоматизация](#12-автоматизация)

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
- Справочник меток хранится в [labels.yml](../labels.yml)

---

## 2. Naming Convention

**Формат метки:**
```
{value}
```

Метки называются по значению без категорийного префикса. Категория определяется по секции в [labels.yml](../../labels.yml).

**Правила для имени метки:**
- Только латиница
- Нижний регистр (lowercase)
- Дефис `-` для разделения слов (kebab-case)
- Без пробелов, подчёркиваний, camelCase

**Правила для description:**
- Начинать с emoji, отражающего суть метки
- Краткое описание на русском или английском
- Максимум 50 символов

**Примеры:**

| Формат | Корректно | Причина |
|--------|-----------|---------|
| `bug` | ✅ | — |
| `high` | ✅ | — |
| `in-review` | ✅ | kebab-case для многословных |
| `Bug` | ❌ | Верхний регистр |
| `in_review` | ❌ | Подчёркивание вместо дефиса |
| `inReview` | ❌ | camelCase |

**Исключение — категория SVC:**

Категория SVC использует префикс `svc:` для отличия от AREA-меток. Имя после префикса — kebab-case, совпадает с `src/{service}/`.

| Формат | Корректно | Причина |
|--------|-----------|---------|
| `svc:auth` | ✅ | Префикс svc: + имя сервиса |
| `svc:user-profile` | ✅ | kebab-case для многословных |
| `svc:Auth` | ❌ | Верхний регистр |
| `auth` | ❌ | Без префикса svc: (это AREA-метка) |

---

## 3. Правила применения

### Обязательные метки

Каждая задача (Issue) ДОЛЖНА иметь:
- **Ровно одну** метку `TYPE-метку` — тип задачи
- **Ровно одну** метку `PRIORITY-метку` — приоритет

> **Для LLM:** Перед созданием Issue/PR проверить наличие обязательных меток `TYPE-метку` и `PRIORITY-метку`. Если метки не указаны — запросить у пользователя.

### Критерии выбора типа

| Тип | Критерий | Примеры |
|-----|----------|---------|
| `bug` | Нечто работает не так, как ожидалось | 🐛 Падение сервиса, неверный ответ API, UI-баг |
| `feature` | Новая функциональность (CRUD, UI, бизнес-логика) | ✨ Новый эндпоинт, UI-компонент, канбан-доска |
| `task` | Техническая задача (scaffold, middleware, boilerplate) | 🔧 Scaffold сервиса, Zod-схемы, JWT-middleware |
| `infra` | Инфраструктура (Docker, CI/CD, конфиги) | 🏗️ docker-compose, монорепо, shared config |
| `test` | Тесты (E2E, integration, load, smoke) | 🧪 E2E тесты, нагрузочные тесты |
| `docs` | Документация | 📚 README, спецификации, API docs |
| `refactor` | Рефакторинг без изменения функциональности | ♻️ Переименование, вынос утилит |

### Критерии выбора приоритета

| Приоритет | Критерий | Примеры |
|-----------|----------|---------|
| `critical` | Блокирует production | 🔴 Падение сервиса, потеря данных, security breach |
| `high` | Блокирует разработку | 🟠 Критичный для спринта, deadline |
| `medium` | Обычная задача | 🟡 Фича без deadline, плановые улучшения |
| `low` | Можно отложить | 🟢 Nice-to-have, косметические улучшения |

### Опциональные метки

Добавлять метку, если задача затрагивает соответствующую область:

| Категория | Когда добавлять |
|-----------|-----------------|
| `STATUS-метку` | Задача заблокирована, на ревью, или готова к работе. `blocked` — при незакрытых зависимостях (см. [standard-issue.md § 8](../issues/standard-issue.md#8-декомпозиция-и-зависимости)) |
| `AREA-метку` | Задача затрагивает конкретную область кода (макс. 3) |
| `EFFORT-метку` | Для планирования спринтов |
| `ENV-метку` | ТОЛЬКО для `bug` — где проявляется баг |
| `SVC-метку` | Задача затрагивает конкретный сервис (макс. 3). SSOT: `specs/services/` |

### Примеры применения

**Баг на production:**
```
bug
critical
backend
api
production
s
```

**Новая задача:**
```
task
medium
frontend
m
```

**Документация:**
```
docs
low
specs
xs
```

**Инфраструктура:**
```
infra
high
platform
m
```

**Тесты:**
```
test
medium
tests
s
```

**Задача на конкретный сервис:**
```
svc:auth
feature
high
backend
m
```

---

## 4. Связь TYPE-меток с Issue Templates

**SSOT шаблонов:** [standard-issue-template.md](../issues/issue-templates/standard-issue-template.md)

Категория `TYPE-метку` имеет особую роль — каждая метка типа **ДОЛЖНА** иметь соответствующий Issue Template в `.github/ISSUE_TEMPLATE/`.

**Правило соответствия:**
- Для каждой метки типа в [labels.yml](../../labels.yml) должен существовать шаблон
- Шаблон должен содержать метку типа в `labels:`
- Именование шаблона — см. [standard-issue-template.md](../issues/issue-templates/standard-issue-template.md)

**При добавлении метки `TYPE-метку`:** создать Issue Template (→ [standard-issue-template.md § 7](../issues/issue-templates/standard-issue-template.md#7-предустановленные-метки)).

**При удалении метки `TYPE-метку`:** удалить соответствующий Issue Template.

**Валидация:**
```bash
python .github/.instructions/.scripts/validate-type-templates.py
```

> **Для LLM:** При модификации меток `TYPE-метку` — проверить соответствие с Issue Templates.

---

## 5. Разрешение конфликтов

| Конфликт | Правило |
|----------|---------|
| Несколько меток `TYPE-метку` | Удалить все, кроме одной основной. Если неясно — спросить автора Issue. |
| Несколько меток `PRIORITY-метку` | Удалить все, кроме одной. Приоритет выбирается автором или maintainer. |
| `ENV-метку` на не-баге | **Удалить** метку `ENV-метку`. Метки окружения только для `bug`. |
| Более 3 меток `AREA-метку` | Оставить 3 основные. Если больше — разбить задачу на подзадачи. |

**Валидация:** Если на задаче есть `ENV-метку`, проверить наличие `bug`. Если `bug` отсутствует — удалить метку `ENV-метку`.

---

## 6. Добавление категории

Новая категория добавляется редко (раз в полгода-год).

**Когда добавлять:**
- Появилась новая ось классификации, которую нельзя выразить существующими категориями
- Категория будет использоваться регулярно (>10% задач)

**Процесс:**

1. **Обоснование:** Описать в Issue/PR, зачем нужна категория
2. **Naming:** Выбрать префикс (lowercase, короткий)
3. **Цвет:** Выбрать уникальный HEX, не пересекающийся с существующими
4. **Метки:** Определить начальный набор меток категории
5. **Обновить labels.yml:**
   - Добавить строку в таблицу "Категории"
   - Добавить секцию с метками
   - Добавить в `labels.yml`
6. **Синхронизация:** Выполнить `gh label create` для новых меток
7. **Документация:** Обновить README области

**Пример:**
```bash
# Добавить категорию "scope" с метками
gh label create "mvp" --description "🎯 MVP релиз" --color "22D3EE"
gh label create "v2" --description "🚀 Версия 2.0" --color "22D3EE"
```

---

## 7. Добавление метки

Новая метка в существующей категории.

**Когда добавлять:**
- Появилось новое значение, которое используется регулярно
- Нельзя выразить существующими метками

**Процесс:**

1. **Проверить:** Метка не дублирует существующую
2. **Naming:** `{name}` в kebab-case
3. **Цвет:** Использовать цвет категории (из [labels.yml](../labels.yml))
4. **Обновить labels.yml:**
   - Добавить строку в таблицу категории
   - Добавить в `labels.yml`
5. **Синхронизация:**
   ```bash
   gh label create "{name}" --description "{описание}" --color "{HEX}"
   ```

**Пример:**
```bash
# Добавить метку mobile
gh label create "mobile" --description "📱 Мобильное приложение" --color "10B981"
```

---

## 8. Удаление метки

> **Важно:** Метка не может быть "деактивирована" или "архивирована" — только **удалена**. Перед удалением ВСЕ Issues/PR с этой меткой ДОЛЖНЫ быть мигрированы.

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
2. **Мигрировать (ОБЯЗАТЕЛЬНО):** Все Issues/PR с меткой должны быть перенесены:
   - Определить альтернативную метку для замены
   - Заменить метку на всех Issues/PR:
     ```bash
     for num in $(gh issue list --label "{старая_метка}" --state all --json number -q '.[].number'); do
       gh issue edit $num --remove-label "{старая_метка}" --add-label "{новая_метка}"
     done
     for num in $(gh pr list --label "{старая_метка}" --state all --json number -q '.[].number'); do
       gh pr edit $num --remove-label "{старая_метка}" --add-label "{новая_метка}"
     done
     ```
   - Если альтернативы нет — удалить метку с Issues/PR (не рекомендуется)
3. **Проверить:** Убедиться, что метка не используется:
   ```bash
   gh issue list --label "{метка}" --state all --limit 1
   gh pr list --label "{метка}" --state all --limit 1
   ```
4. **Удалить из GitHub:**
   ```bash
   gh label delete "{метка}" --yes
   ```
5. **Обновить labels.yml:**
   - Удалить строку из таблицы
   - Удалить из `labels.yml`

**Важно:** НЕ удалять метки категорий `TYPE-метку` и `PRIORITY-метку` без согласования.

---

## 9. Переименование метки

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
5. **Обновить labels.yml**

**Пример: переименование `infra` → `platform`:**
```bash
gh label create "platform" --description "🔧 Инфраструктура и платформа" --color "10B981"
for num in $(gh issue list --label "infra" --state all --json number -q '.[].number'); do
  gh issue edit $num --remove-label "infra" --add-label "platform"
done
gh label delete "infra" --yes
```

---

## 10. Переименование категории

Массовое переименование всех меток категории (например, `AREA-метку` → `scope:*`).

**Когда применять:**
- Изменилась терминология проекта
- Категория переименовывается в рамках рефакторинга

**Процесс:**

1. **Собрать список меток категории:**
   ```bash
   gh label list --json name -q '.[] | select(.name | startswith("{old_category}:")) | .name'
   ```

2. **Для каждой метки выполнить переименование (§8):**
   ```bash
   OLD_CAT="area"
   NEW_CAT="scope"
   COLOR="10B981"

   for label in $(gh label list --json name,description -q ".[] | select(.name | startswith(\"${OLD_CAT}:\"))"); do
     old_name=$(echo $label | jq -r '.name')
     desc=$(echo $label | jq -r '.description')
     value=${old_name#*:}
     new_name="${NEW_CAT}:${value}"

     # Создать новую метку
     gh label create "$new_name" --description "$desc" --color "$COLOR"

     # Мигрировать Issues
     for num in $(gh issue list --label "$old_name" --state all --json number -q '.[].number'); do
       gh issue edit $num --remove-label "$old_name" --add-label "$new_name"
     done

     # Мигрировать PR
     for num in $(gh pr list --label "$old_name" --state all --json number -q '.[].number'); do
       gh pr edit $num --remove-label "$old_name" --add-label "$new_name"
     done

     # Удалить старую метку
     gh label delete "$old_name" --yes
   done
   ```

3. **Обновить labels.yml:**
   - Переименовать категорию в таблице "Категории"
   - Обновить все метки в секции категории
   - Обновить `labels.yml`

4. **Чек-лист проверки:**
   - [ ] Все Issues мигрированы (проверить `gh issue list --label "{old_cat}:*"`)
   - [ ] Все PR мигрированы
   - [ ] Старые метки удалены
   - [ ] labels.yml обновлён
   - [ ] labels.yml обновлён

---

## 11. Синхронизация с GitHub

Метки хранятся в [labels.yml](../labels.yml) — единый SSOT справочник меток.

**Автоматическая синхронизация:**

Скрипт [sync-labels.py](../.instructions/.scripts/sync-labels.py) синхронизирует `labels.yml` с GitHub:
```bash
# Показать план изменений
python .github/.instructions/.scripts/sync-labels.py

# Применить изменения
python .github/.instructions/.scripts/sync-labels.py --apply
```

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

Автоматическая синхронизация имеет приоритет над ручной синхронизацией.

---

## 12. Автоматизация

### Через Issue Templates

Issue Templates могут содержать предустановленные метки:

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
labels:
  - bug
  - medium
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

            if (body.includes('backend')) labels.push('backend');
            if (body.includes('frontend')) labels.push('frontend');

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
| `ready` | Переместить в колонку "Ready" |
| `wip` | Переместить в колонку "In Progress" |
| `in-review` | Переместить в колонку "Review" |
| `blocked` | Переместить в колонку "Blocked" |

---

## Скиллы

*Нет скиллов.*
