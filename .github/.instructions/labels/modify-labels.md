---
description: Воркфлоу модификации меток GitHub — добавление, удаление, переименование с синхронизацией labels.yml.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/labels/README.md
---

# Воркфлоу изменения

Рабочая версия стандарта: 1.3

Модификация меток GitHub (добавление, удаление, переименование)

**Полезные ссылки:**
- [Инструкции](./README.md)
- [labels.yml](../../labels.yml)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-labels.md](./standard-labels.md) |

| Валидация | [validation-labels.md](./validation-labels.md) |
| Создание | *Не требуется (labels.yml создаётся разово)* |
| Модификация | Этот документ |

## Оглавление

- [Типы изменений](#типы-изменений)
- [Добавление категории](#добавление-категории)
- [Добавление метки](#добавление-метки)
- [Обновление метки](#обновление-метки)
- [Переименование метки](#переименование-метки)
- [Переименование категории](#переименование-категории)
- [Удаление метки](#удаление-метки)
- [Обновление ссылок](#обновление-ссылок)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Типы изменений

| Тип | Описание | Пример |
|-----|----------|--------|
| Добавление категории | Добавить новую категорию меток | Добавить категорию `scope:*` для релизов |
| Добавление метки | Добавить метку в существующую категорию | Добавить метку `area:mobile` |
| Обновление метки | Изменить description/color метки | Уточнить описание метки `area:api` |
| Переименование метки | Изменить имя метки | `area:infra` → `area:platform` |
| Переименование категории | Переименовать все метки категории | `area:*` → `scope:*` |
| Удаление метки | Удалить метку и мигрировать Issues/PR | Удалить устаревшую метку `area:legacy` |

---

## Добавление категории

> **SSOT:** [standard-labels.md § 6](./standard-labels.md#6-добавление-категории)

Новая категория добавляется редко (раз в полгода-год). Категория — это префикс для группы меток.

### Шаг 1: Обосновать необходимость

**Когда добавлять:**
- Появилась новая ось классификации, которую нельзя выразить существующими категориями
- Категория будет использоваться регулярно (>10% задач)

Если не уверены — спросить команду через Issue.

### Шаг 2: Выбрать имя и цвет

**Naming:**
- Префикс: lowercase, короткий (1 слово)
- Примеры: `type`, `priority`, `area`, `scope`

**Цвет:**
- Выбрать уникальный HEX (6 символов, без `#`)
- Не пересекаться с существующими категориями
- Исключение: `priority` использует градиент

### Шаг 3: Определить начальный набор меток

Создать список меток для новой категории:
- Минимум 2 метки
- Формат: `{category}:{value}`
- Каждая метка: имя, описание с emoji, цвет

**Пример:**
```yaml
- name: scope:mvp
  description: 🎯 MVP релиз
  color: 22D3EE
- name: scope:v2
  description: 🚀 Версия 2.0
  color: 22D3EE
```

### Шаг 4: Обновить labels.yml

Добавить категорию и метки в `labels.yml`:

1. Открыть `.github/labels.yml`
2. Добавить строку в таблицу "Категории"
3. Добавить секцию с метками категории
4. Сохранить файл

### Шаг 5: Синхронизация с GitHub

Создать метки в GitHub:

```bash
# Для каждой метки категории:
gh label create "{category}:{value}" --description "{описание}" --color "{HEX}"
```

**Пример:**
```bash
gh label create "scope:mvp" --description "🎯 MVP релиз" --color "22D3EE"
gh label create "scope:v2" --description "🚀 Версия 2.0" --color "22D3EE"
```

### Шаг 6: Валидация

```bash
python .github/.instructions/.scripts/validate-labels.py --file
python .github/.instructions/.scripts/validate-labels.py --sync
```

### Шаг 7: Документация

Обновить:
- `standard-labels.md` — добавить категорию в описание

---

## Добавление метки

> **SSOT:** [standard-labels.md § 7](./standard-labels.md#7-добавление-метки)

Новая метка в существующей категории.

### Шаг 1: Проверить дублирование

Убедиться, что метка не дублирует существующую:

```bash
gh label list | grep "{category}:"
```

Или посмотреть в `labels.yml`.

### Шаг 2: Выбрать имя

Формат: `{category}:{value}`

Правила:
- `{value}` — kebab-case, lowercase
- Описательное (отражает суть)
- Краткое (1-2 слова)

### Шаг 3: Написать description

- Начать с emoji, отражающего суть
- Краткое описание на русском или английском
- Максимум 50 символов

**Примеры:**
- `📱 Мобильное приложение`
- `🔒 Безопасность и аутентификация`
- `⚡ Критичный для production`

### Шаг 4: Определить цвет

Использовать цвет категории из `labels.yml`.

**Исключение:** категория `priority` использует градиент (каждая метка имеет свой цвет).

### Шаг 5: Добавить в labels.yml

1. Открыть `.github/labels.yml`
2. Найти секцию категории
3. Добавить строку:
   ```yaml
   - name: {category}:{value}
     description: {emoji} {описание}
     color: {HEX}
   ```
4. Сохранить файл

### Шаг 6: Создать метку в GitHub

```bash
gh label create "{category}:{value}" --description "{описание}" --color "{HEX}"
```

**Пример:**
```bash
gh label create "area:mobile" --description "📱 Мобильное приложение" --color "10B981"
```

### Шаг 7: Валидация

```bash
python .github/.instructions/.scripts/validate-labels.py --file
python .github/.instructions/.scripts/validate-labels.py --sync
```

---

## Обновление метки

Изменение description или color метки.

### Шаг 1: Обновить labels.yml

1. Открыть `.github/labels.yml`
2. Найти метку
3. Изменить `description` или `color`
4. Сохранить файл

### Шаг 2: Обновить метку в GitHub

```bash
gh label edit "{name}" --description "{new_desc}" --color "{new_hex}"
```

**Пример:**
```bash
gh label edit "area:api" --description "🔌 REST API и GraphQL" --color "10B981"
```

### Шаг 3: Валидация

```bash
python .github/.instructions/.scripts/validate-labels.py --sync
```

---

## Переименование метки

> **SSOT:** [standard-labels.md § 9](./standard-labels.md#9-переименование-метки)

Изменение имени метки (value в `{category}:{value}`).

### Шаг 1: Найти все Issues/PR с меткой

```bash
gh issue list --label "{старое_имя}" --state all --json number -q '.[].number'
gh pr list --label "{старое_имя}" --state all --json number -q '.[].number'
```

### Шаг 2: Создать новую метку

```bash
gh label create "{новое_имя}" --description "{описание}" --color "{HEX}"
```

### Шаг 3: Заменить метку на всех Issues/PR

**Автоматически:**
```bash
python .github/.instructions/.scripts/migrate-label.py "{старое_имя}" "{новое_имя}" --apply
```

**Вручную (если скрипт недоступен):**
```bash
# Для каждого Issue:
for num in $(gh issue list --label "{старое_имя}" --state all --json number -q '.[].number'); do
  gh issue edit $num --remove-label "{старое_имя}" --add-label "{новое_имя}"
done

# Для каждого PR:
for num in $(gh pr list --label "{старое_имя}" --state all --json number -q '.[].number'); do
  gh pr edit $num --remove-label "{старое_имя}" --add-label "{новое_имя}"
done
```

### Шаг 4: Удалить старую метку

```bash
gh label delete "{старое_имя}" --yes
```

### Шаг 5: Обновить labels.yml

1. Открыть `.github/labels.yml`
2. Найти старую метку
3. Изменить `name` на новое имя
4. Сохранить файл

### Шаг 6: Валидация

```bash
python .github/.instructions/.scripts/validate-labels.py --file
python .github/.instructions/.scripts/validate-labels.py --sync
python .github/.instructions/.scripts/validate-labels.py --all
```

---

## Переименование категории

> **SSOT:** [standard-labels.md § 10](./standard-labels.md#10-переименование-категории)

Массовое переименование всех меток категории (например, `area:*` → `scope:*`).

### Шаг 1: Собрать список меток категории

```bash
gh label list --json name -q '.[] | select(.name | startswith("{old_category}:")) | .name'
```

### Шаг 2: Переименовать каждую метку

Для каждой метки выполнить [Переименование метки](#переименование-метки):

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

### Шаг 3: Обновить labels.yml

1. Открыть `.github/labels.yml`
2. Переименовать категорию в таблице "Категории"
3. Обновить все метки в секции категории (изменить `name`)
4. Сохранить файл

### Шаг 4: Валидация

```bash
python .github/.instructions/.scripts/validate-labels.py --file
python .github/.instructions/.scripts/validate-labels.py --sync
python .github/.instructions/.scripts/validate-labels.py --all
```

### Шаг 5: Чек-лист проверки

- [ ] Все Issues мигрированы (проверить `gh issue list --label "{old_cat}:*"`)
- [ ] Все PR мигрированы
- [ ] Старые метки удалены
- [ ] labels.yml обновлён

---

## Удаление метки

> **SSOT:** [standard-labels.md § 8](./standard-labels.md#8-удаление-метки)

> **Важно:** Метка не может быть "деактивирована" или "архивирована" — только **удалена**. Перед удалением ВСЕ Issues/PR с этой меткой ДОЛЖНЫ быть мигрированы.

### Шаг 1: Проверить использование

```bash
gh issue list --label "{метка}" --state all --limit 100
gh pr list --label "{метка}" --state all --limit 100
```

### Шаг 2: Мигрировать Issues/PR (ОБЯЗАТЕЛЬНО)

**Определить альтернативную метку:**
- Если есть похожая метка → заменить
- Если альтернативы нет → удалить метку с Issues/PR (не рекомендуется)

**Автоматически:**
```bash
# Заменить на другую метку
python .github/.instructions/.scripts/migrate-label.py "{старая_метка}" "{новая_метка}" --apply

# Или удалить без замены
python .github/.instructions/.scripts/migrate-label.py "{старая_метка}" --delete --apply
```

**Вручную (если скрипт недоступен):**
```bash
# Для каждого Issue:
for num in $(gh issue list --label "{старая_метка}" --state all --json number -q '.[].number'); do
  gh issue edit $num --remove-label "{старая_метка}" --add-label "{новая_метка}"
done

# Для каждого PR:
for num in $(gh pr list --label "{старая_метка}" --state all --json number -q '.[].number'); do
  gh pr edit $num --remove-label "{старая_метка}" --add-label "{новая_метка}"
done
```

### Шаг 3: Проверить отсутствие использования

```bash
gh issue list --label "{метка}" --state all --limit 1
gh pr list --label "{метка}" --state all --limit 1
```

Должно вернуть пустой результат.

### Шаг 4: Удалить из GitHub

```bash
gh label delete "{метка}" --yes
```

### Шаг 5: Удалить из labels.yml

1. Открыть `.github/labels.yml`
2. Найти метку
3. Удалить строку
4. Сохранить файл

### Шаг 6: Валидация

```bash
python .github/.instructions/.scripts/validate-labels.py --file
python .github/.instructions/.scripts/validate-labels.py --sync
```

**Важно:** НЕ удалять метки типа (bug, task, docs, refactor) и приоритета (critical, high, medium, low) без согласования с командой.

---

## Обновление ссылок

При переименовании или удалении метки НЕ требуется обновлять ссылки в документации — метки не используются в ссылках.

**Исключение:** Если в документации есть примеры с конкретными метками (например, в README или стандартах):
1. Найти упоминания через grep:
   ```bash
   grep -r "{старое_имя}" .github/
   ```
2. Обновить вручную

---

## Чек-лист

### Добавление категории

- [ ] Обоснование создано (Issue или обсуждение)
- [ ] Выбран префикс (lowercase, короткий)
- [ ] Выбран уникальный HEX цвет
- [ ] Определён начальный набор меток (минимум 2)
- [ ] labels.yml обновлён
- [ ] Метки созданы в GitHub
- [ ] Валидация пройдена
- [ ] Документация обновлена

### Добавление метки

- [ ] Проверено дублирование (метка не существует)
- [ ] Имя выбрано (`{category}:{value}`, kebab-case)
- [ ] Description написан (emoji + текст, макс. 50 символов)
- [ ] Цвет определён (из категории)
- [ ] labels.yml обновлён
- [ ] Метка создана в GitHub
- [ ] Валидация пройдена

### Обновление метки

- [ ] labels.yml обновлён
- [ ] Метка обновлена в GitHub
- [ ] Валидация пройдена

### Переименование метки

- [ ] Найдены все Issues/PR с меткой
- [ ] Создана новая метка в GitHub
- [ ] Метка заменена на всех Issues/PR
- [ ] Старая метка удалена из GitHub
- [ ] labels.yml обновлён
- [ ] Валидация пройдена

### Переименование категории

- [ ] Собран список всех меток категории
- [ ] Каждая метка переименована (см. чек-лист "Переименование метки")
- [ ] labels.yml обновлён
- [ ] Валидация пройдена
- [ ] Все Issues мигрированы
- [ ] Все PR мигрированы
- [ ] Старые метки удалены

### Удаление метки

- [ ] Проверено использование (Issues/PR)
- [ ] Определена альтернативная метка
- [ ] Issues/PR мигрированы
- [ ] Проверено отсутствие использования
- [ ] Метка удалена из GitHub
- [ ] labels.yml обновлён
- [ ] Валидация пройдена

---

## Примеры

### Добавление метки area:mobile

```bash
# 1. Проверить дублирование
gh label list | grep "area:"

# 2. Добавить в labels.yml
# (открыть файл, добавить строку в секцию "area")

# 3. Создать метку в GitHub
gh label create "area:mobile" --description "📱 Мобильное приложение" --color "10B981"

# 4. Валидация
python .github/.instructions/.scripts/validate-labels.py --file
python .github/.instructions/.scripts/validate-labels.py --sync
```

### Переименование метки: area:infra → area:platform

```bash
# 1. Найти Issues/PR
gh issue list --label "area:infra" --state all --json number -q '.[].number'

# 2. Создать новую метку
gh label create "area:platform" --description "🔧 Инфраструктура и платформа" --color "10B981"

# 3. Мигрировать Issues
for num in $(gh issue list --label "area:infra" --state all --json number -q '.[].number'); do
  gh issue edit $num --remove-label "area:infra" --add-label "area:platform"
done

# 4. Мигрировать PR
for num in $(gh pr list --label "area:infra" --state all --json number -q '.[].number'); do
  gh pr edit $num --remove-label "area:infra" --add-label "area:platform"
done

# 5. Удалить старую метку
gh label delete "area:infra" --yes

# 6. Обновить labels.yml
# (открыть файл, изменить name с "area:infra" на "area:platform")

# 7. Валидация
python .github/.instructions/.scripts/validate-labels.py --file
python .github/.instructions/.scripts/validate-labels.py --sync
```

### Удаление метки area:legacy

```bash
# 1. Проверить использование
gh issue list --label "area:legacy" --state all --limit 100
gh pr list --label "area:legacy" --state all --limit 100

# 2. Мигрировать Issues (заменить на area:backend)
for num in $(gh issue list --label "area:legacy" --state all --json number -q '.[].number'); do
  gh issue edit $num --remove-label "area:legacy" --add-label "area:backend"
done

# 3. Мигрировать PR
for num in $(gh pr list --label "area:legacy" --state all --json number -q '.[].number'); do
  gh pr edit $num --remove-label "area:legacy" --add-label "area:backend"
done

# 4. Проверить отсутствие использования
gh issue list --label "area:legacy" --state all --limit 1

# 5. Удалить из GitHub
gh label delete "area:legacy" --yes

# 6. Удалить из labels.yml
# (открыть файл, удалить строку)

# 7. Валидация
python .github/.instructions/.scripts/validate-labels.py --file
python .github/.instructions/.scripts/validate-labels.py --sync
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [sync-labels.py](../.scripts/sync-labels.py) | Синхронизация labels.yml с GitHub (создание, удаление, обновление) | Этот документ |
| [migrate-label.py](../.scripts/migrate-label.py) | Миграция меток на Issues/PR (замена, удаление) | Этот документ |
| [validate-labels.py](../.scripts/validate-labels.py) | Валидация labels.yml и меток | [validation-labels.md](./validation-labels.md) |

### Использование sync-labels.py

```bash
# Показать план изменений (dry-run)
python .github/.instructions/.scripts/sync-labels.py

# Применить изменения (с подтверждением)
python .github/.instructions/.scripts/sync-labels.py --apply

# Применить без подтверждения
python .github/.instructions/.scripts/sync-labels.py --apply --force
```

### Использование migrate-label.py

```bash
# Показать план миграции (dry-run)
python .github/.instructions/.scripts/migrate-label.py area:infra area:platform

# Применить миграцию (с подтверждением)
python .github/.instructions/.scripts/migrate-label.py area:infra area:platform --apply

# Удалить метку с Issues/PR (без замены)
python .github/.instructions/.scripts/migrate-label.py area:legacy --delete --apply
```

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/labels-modify](/.claude/skills/labels-modify/SKILL.md) | Изменение меток | Этот документ |
