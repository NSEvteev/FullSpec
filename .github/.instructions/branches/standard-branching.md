---
description: Стандарт именования и создания веток — паттерн NNNN-description, привязка к analysis chain, защита main.
standard: .instructions/standard-instruction.md
standard-version: v2.0
index: .github/.instructions/branches/README.md
---

# Стандарт ветвления

Версия стандарта: 2.0

Правила создания, именования и жизненного цикла веток в репозитории.

**Полезные ссылки:**
- [Инструкции branches](./README.md)

**SSOT-зависимости:**
- [standard-pull-request.md](../pull-requests/standard-pull-request.md) — ветка привязывается к PR
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
  ├─ 0001-oauth2-auth
  ├─ 0002-notification-service
  ├─ 0015-hotfix-payment-crash
  └─ 0042-cache-optimization
```

**Ключевые свойства main:**
- Защищена от прямых push через Branch Protection Rules (→ [standard-review.md](../review/standard-review.md)). Если защита не настроена — см. процесс настройки в [standard-review.md](../review/standard-review.md).
- Всегда стабильна — все изменения прошли review и CI
- Единственный источник для создания feature-веток

**Принципы:**
- Одна ветка соответствует одному analysis chain (`specs/analysis/NNNN-{topic}/`) — одна ветка — один PR
- Feature-ветки удаляются после merge
- Fork-модель не используется — проект работает с одним origin

---

## 2. Naming Convention

### Формат имени

```
{NNNN}-{description}
```

| Элемент | Правило | Пример |
|---------|---------|--------|
| `{NNNN}` | 4-значный номер анализа из `specs/analysis/NNNN-{topic}/` | `0001`, `0042` |
| `{description}` | Kebab-case (lowercase, дефисы), 1-4 слова. Из topic slug или уточнение. Акронимы строчными: `api`, `jwt`, `cors`. | `oauth2-auth`, `cache-optimization` |

### Связь с analysis chain

Каждая ветка привязана к analysis chain через номер NNNN. Вся работа в проекте организована через цепочку Discussion → Design → Plan Tests → Plan Dev. Номер NNNN — это номер analysis directory в `specs/analysis/`.

### Допустимые и запрещённые форматы

| Формат | Статус | Причина |
|--------|--------|---------|
| `0001-oauth2-auth` | Допустимо | Полный формат |
| `0002-notification-service` | Допустимо | Полный формат |
| `0015-hotfix-payment-crash` | Допустимо | Срочный баг — но через analysis chain |
| `feature/auth-42` | Запрещено | Старый формат с type-префиксом |
| `add-auth` | Запрещено | Нет NNNN-префикса |
| `0001_auth` | Запрещено | Подчёркивание вместо дефиса |
| `0001-Auth` | Запрещено | Верхний регистр |

**Regex:** `^\d{4}-[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*$`

---

## 3. Жизненный цикл ветки

### Создание

```bash
# 1. Синхронизировать main (→ standard-sync.md)
git checkout main
git pull origin main

# 2. Создать ветку
git checkout -b {NNNN}-{description}
```

**Пример:** `git checkout -b 0001-oauth2-auth`

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
| Ветка без analysis chain запрещена | Нарушает трассируемость работы |

**Вложенные ветки — запрещено:**
```
0001-oauth2-auth
  └─ 0001-oauth2-ui   ← НЕ создавать
```

**Правильно — отдельные ветки от main:**
```
main
  ├─ 0001-oauth2-auth
  └─ 0001-oauth2-ui       (создать от main ПОСЛЕ merge первой)
```

---

## 5. Граничные случаи

### Несколько веток для одного analysis chain

Если объём работы по одному analysis chain слишком велик для одной ветки — разделить на этапы. Каждая ветка использует тот же NNNN с уточнением в description:

```
main
  ├─ 0001-oauth2-backend    (merge первым)
  └─ 0001-oauth2-frontend   (создать от свежего main ПОСЛЕ merge первой)
```

Последовательность:
1. Создать и смержить первую ветку
2. Синхронизировать main (`git checkout main && git pull origin main`)
3. Создать вторую ветку от обновлённого main

### Зависимые задачи

Если analysis A зависит от analysis B (который ещё не смержен):

**Вариант 1 (рекомендуется):** Дождаться merge B → создать ветку A от обновлённой main.

**Вариант 2 (если B большой):** Создать draft PR для B → создать ветку A от main → синхронизировать A с веткой B вручную:

```bash
git checkout 0002-notification-service
git fetch origin 0001-oauth2-auth
git rebase origin/0001-oauth2-auth
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
git checkout -b 0015-hotfix-payment-crash

# Вернуться и восстановить
git checkout 0001-oauth2-auth
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
- Наличие 4-значного NNNN-префикса
- Формат `{NNNN}-{description}`
- Description в kebab-case, lowercase

**Автоматизация:** Добавлен в pre-commit hook.
