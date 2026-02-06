---
description: Стандарт именования и создания веток
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/branches/README.md
---

# Стандарт ветвления

Версия стандарта: 1.2

Правила создания, именования и жизненного цикла веток в репозитории.

**Полезные ссылки:**
- [Инструкции branches](./README.md)

**SSOT-зависимости:**
- [standard-issue.md](../issues/standard-issue.md) — номера Issues используются в имени ветки
- [standard-pull-request.md](../pull-requests/standard-pull-request.md) — ветка привязывается к PR
- [standard-labels.md](../labels/standard-labels.md) — TYPE-метка определяет префикс ветки
- [standard-sync.md](../sync/standard-sync.md) — синхронизация main перед созданием ветки

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-branch.md](./validation-branch.md) |
| Создание | [create-branch.md](./create-branch.md) |
| Модификация | *Не требуется* |

## Оглавление

- [1. Модель ветвления](#1-модель-ветвления)
- [2. Naming Convention](#2-naming-convention)
- [3. Жизненный цикл ветки](#3-жизненный-цикл-ветки)
- [4. Запреты и ограничения](#4-запреты-и-ограничения)
- [5. Граничные случаи](#5-граничные-случаи)
- [6. Валидация](#6-валидация)

---

## 1. Модель ветвления

Проект использует GitHub Flow — упрощённую модель с одной защищённой веткой.

```
main (protected, stable)
  ├─ feature/auth-42-43-44
  ├─ fix/upload-errors-50-51
  ├─ docs/deploy-guide-70
  └─ task/deps-update-60
```

**Ключевые свойства main:**
- Защищена от прямых push через Branch Protection Rules (→ [standard-review.md](../review/standard-review.md)). Если защита не настроена — см. процесс настройки в [standard-review.md](../review/standard-review.md).
- Всегда стабильна — все изменения прошли review и CI
- Единственный источник для создания feature-веток

**Принципы:**
- Одна функциональная задача (фича/баг/задача) или группа связанных задач с общей целью — одна ветка — один PR. Критерии объединения: → [standard-issue.md § 8](../issues/standard-issue.md#8-декомпозиция-и-зависимости).
- Feature-ветки удаляются после merge
- Fork-модель не используется — проект работает с одним origin

---

## 2. Naming Convention

### Формат имени

```
{type}/{description}-{issue-numbers}
```

| Элемент | Правило | Пример |
|---------|---------|--------|
| `{type}` | Определяется TYPE-меткой Issue с минимальным номером в группе | `feature`, `fix`, `docs` |
| `{description}` | Kebab-case (lowercase, дефисы), 2-3 слова. Для feature/task — название функции (`auth`, `two-factor`). Для bug — симптом проблемы (`upload-errors`, `null-response`). Акронимы строчными: `api`, `jwt`, `cors`. | `auth`, `upload-errors`, `api-gateway` |
| `{issue-numbers}` | Номера всех Issues группы через дефис в порядке возрастания | `42-43-44` (42 < 43 < 44) |

### Соответствие TYPE-меток и префиксов

| TYPE-метка Issue | Префикс ветки |
|------------------|---------------|
| `feature` | `feature/` |
| `bug` | `fix/` |
| `task` | `task/` |
| `docs` | `docs/` |
| `refactor` | `refactor/` |

### Правила выбора type

Если в группе Issues разные TYPE-метки — использовать тип Issue с минимальным номером.

**Пример:** Issues #45 (bug), #42 (feature), #50 (task) → префикс `feature/` (т.к. #42 — минимальный номер).

### Обязательность Issue

Каждая ветка ОБЯЗАНА ссылаться хотя бы на один Issue. Создание ветки без Issue запрещено. Перед созданием ветки — создать Issue и получить его номер.

### Допустимые и запрещённые форматы

| Формат | Статус | Причина |
|--------|--------|---------|
| `feature/auth-42-43-44` | Допустимо | Полный формат |
| `fix/null-response-50` | Допустимо | Один Issue |
| `docs/deploy-guide-70-71` | Допустимо | Два Issues |
| `add-auth` | Запрещено | Нет типа и номеров |
| `feature/add-auth` | Запрещено | Нет номеров Issues |
| `feature/42_auth` | Запрещено | Подчёркивание вместо дефиса |

---

## 3. Жизненный цикл ветки

### Создание

```bash
# 1. Синхронизировать main (→ standard-sync.md)
git checkout main
git pull origin main

# 2. Создать ветку
git checkout -b {type}/{description}-{issue-numbers}
```

**Пример:** `git checkout -b feature/auth-42-43-44`

Ветка создаётся ТОЛЬКО от актуального main. Перед созданием обязательна синхронизация.

### Работа

Разработка ведётся в feature-ветке. Коммиты оформляются по [standard-commit.md](../commits/standard-commit.md).

При разработке более 2 календарных дней (от создания ветки) — синхронизировать feature-ветку с main (→ [standard-sync.md § 3](../sync/standard-sync.md#3-процесс-синхронизации)).

### Push ветки в remote

После первого коммита запушить ветку в remote:

```bash
git push -u origin {branch-name}
```

Флаг `-u` (upstream) устанавливает связь между локальной и remote-веткой для последующих `git push` без аргументов.

### Завершение

После merge PR в main ветка ДОЛЖНА быть удалена (для поддержания чистоты репозитория):

- **Автоматически** (рекомендуется): Settings → General → "Automatically delete head branches"
- **Вручную** (если автоудаление отключено):
  ```bash
  git branch -d {branch-name}
  git fetch --prune
  ```

---

## 4. Запреты и ограничения

| Правило | Обоснование |
|---------|-------------|
| Прямые коммиты в main запрещены | Все изменения только через PR с review |
| Вложенные ветки запрещены (ветка от ветки) | Усложняет merge, создаёт скрытые зависимости |
| Ветка без Issue запрещена | Нарушает трассируемость работы |
| Ветка без номера Issue в имени запрещена | Невозможно отследить связь с задачей |

**Вложенные ветки — запрещено:**
```
feature/auth-42-43
  └─ feature/auth-ui-44   ← НЕ создавать
```

**Правильно — одна ветка с объединёнными Issues:**
```
main
  └─ feature/auth-42-43-44
```

---

## 5. Граничные случаи

### Issues слишком разные для одной ветки

Разделить на отдельные ветки, если выполнено ЛЮБОЕ из условий:
- Issues затрагивают файлы с менее чем 20% пересечений
- Issues имеют разные TYPE-метки (bug, feature, docs)

Мержить последовательно:

```
main
  ├─ feature/auth-backend-42-43    (merge первым)
  └─ feature/auth-frontend-44-45   (создать от свежего main ПОСЛЕ merge первой)
```

Последовательность:
1. Создать и смержить первую ветку
2. Синхронизировать main (`git checkout main && git pull origin main`)
3. Создать вторую ветку от обновлённого main

### Ветка создана без Issue (ошибка, требует исправления)

**Как возникла ситуация:** Разработчик создал ветку вручную до прочтения стандарта или забыл создать Issue.

**Процесс исправления:**
1. Создать Issue для задачи (→ [create-issue.md](../issues/create-issue.md))
2. Получить номер (например, #123)
3. Переименовать ветку:
   ```bash
   git branch -m old-name feature/auth-123
   ```

### Issue переименован после создания ветки

Имя ветки НЕ меняется при переименовании Issue. Ветка уже запушена в remote — переименование усложнит трассируемость.

Расхождение между `{description}` в имени ветки и title Issue — допустимо. Связь сохраняется через номер Issue в имени ветки.

### Зависимые задачи

Если Issue A зависит от Issue B (который ещё не смержен):

**Вариант 1 (рекомендуется):** Дождаться merge B → создать ветку A от обновлённой main.

**Вариант 2 (если B большой):** Создать draft PR для B → создать ветку A от main → синхронизировать A с веткой B вручную:

```bash
git checkout feature/A-50
git fetch origin feature/B-49
git rebase origin/feature/B-49
```

**ЗАПРЕЩЕНО:** Создание ветки A от ветки B через `git checkout -b` (вложенные ветки).

### Переключение между ветками

При переключении на другую задачу — сохранить незакоммиченные изменения через `git stash`:

```bash
# Сохранить незакоммиченные изменения
git stash save "WIP: описание"

# Переключиться
git checkout main
git pull origin main
git checkout -b fix/urgent-bug-99

# Вернуться и восстановить
git checkout feature/auth-42-43
git stash pop
```

---

## 6. Валидация

### Проверка формата имени ветки

Перед push проверить формат:

```bash
python .github/.instructions/.scripts/validate-branch-name.py $(git branch --show-current)
```

Скрипт проверяет:
- Наличие префикса из таблицы соответствия TYPE-меток
- Формат `{type}/{description}-{issue-numbers}`
- Существование Issues с указанными номерами

*Скрипт будет создан через `/script-create`.*

**Автоматизация:** Добавить в pre-push hook.
