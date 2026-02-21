---
description: Стандарт именования и создания веток — имя ветки = имя папки analysis chain, защита main.
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
- [standard-analysis.md](/specs/.instructions/analysis/standard-analysis.md) — analysis chain (NNNN-нумерация, привязка ветки к цепочке)
- [standard-commit.md](../commits/standard-commit.md) — формат коммитов, pre-commit hooks
- [standard-review.md](../review/standard-review.md) — Branch Protection Rules, merge-стратегии
- [standard-issue.md](../issues/standard-issue.md) — связь NNNN ветки с GitHub Issues
- [standard-github-workflow.md](../standard-github-workflow.md) — общий workflow (стадии 3-5)
- [standard-development.md](../development/standard-development.md) — процесс разработки в ветке

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
  ├─ 0001-oauth2-authorization
  ├─ 0002-notification-service
  ├─ 0015-hotfix-payment-crash
  └─ 0042-cache-optimization
```

**Ключевые свойства main:**
- Защищена от прямых push через Branch Protection Rules (→ [standard-review.md](../review/standard-review.md)). Если защита не настроена — см. процесс настройки в [standard-review.md](../review/standard-review.md).
- Всегда стабильна — все изменения прошли review и CI
- Единственный источник для создания feature-веток

**Принципы:**
- Одна ветка соответствует одному analysis chain — одна ветка — один PR. Имя ветки = имя папки `specs/analysis/NNNN-{topic}/` (→ [standard-analysis.md § 9](/specs/.instructions/analysis/standard-analysis.md))
- Feature-ветки удаляются после merge
- Fork-модель не используется — проект работает с одним origin

---

## 2. Naming Convention

### Формат имени

**Имя ветки = имя папки analysis chain.** Ветка называется точно так же, как папка `specs/analysis/{name}/`.

```
specs/analysis/0001-oauth2-authorization/  →  ветка 0001-oauth2-authorization
specs/analysis/0042-cache-optimization/    →  ветка 0042-cache-optimization
```

| Элемент | Правило | Пример |
|---------|---------|--------|
| `{NNNN}` | 4-значный номер анализа | `0001`, `0042` |
| `{topic}` | Topic slug из имени папки analysis. Kebab-case (lowercase, дефисы). Акронимы строчными: `api`, `jwt`, `cors`. | `oauth2-authorization`, `cache-optimization` |

### Связь с analysis chain

Каждая ветка привязана к analysis chain 1:1. Вся работа в проекте организована через цепочку Discussion → Design → Plan Tests → Plan Dev. Имя ветки = имя папки analysis directory в `specs/analysis/`.

### Допустимые и запрещённые форматы

| Формат | Статус | Причина |
|--------|--------|---------|
| `0001-oauth2-authorization` | Допустимо | Совпадает с именем папки analysis |
| `0002-notification-service` | Допустимо | Совпадает с именем папки analysis |
| `0015-hotfix-payment-crash` | Допустимо | Совпадает с именем папки analysis |
| `0001-oauth2-auth` | Запрещено | Не совпадает с именем папки (сокращение) |
| `feature/auth-42` | Запрещено | Старый формат с type-префиксом |
| `add-auth` | Запрещено | Нет NNNN-префикса |
| `0001_auth` | Запрещено | Подчёркивание вместо дефиса |
| `0001-Auth` | Запрещено | Верхний регистр |

**Regex:** `^\d{4}-[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*$`

**Дополнительная проверка:** папка `specs/analysis/{branch-name}/` ДОЛЖНА существовать.

---

## 3. Жизненный цикл ветки

### Создание

1. Синхронизировать main (→ [standard-sync.md § 3](../sync/standard-sync.md#3-процесс-синхронизации))
2. Создать ветку с именем папки analysis: `git checkout -b {NNNN}-{topic}`

**Пример:** `git checkout -b 0001-oauth2-authorization`

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
| Прямые коммиты в main запрещены | Все изменения только через PR с review (→ [standard-github-workflow.md](../standard-github-workflow.md)) |
| Вложенные ветки запрещены (ветка от ветки) | Усложняет merge, создаёт скрытые зависимости |
| Ветка без analysis chain запрещена | Нарушает трассируемость работы |
| Несколько веток для одного analysis запрещено | Один analysis chain = одна ветка = один PR. Если объём слишком велик — разбить Discussion на несколько analysis chains |

**Вложенные ветки — запрещено:**
```
0001-oauth2-authorization
  └─ 0001-oauth2-ui   ← НЕ создавать
```

**Правильно — отдельные analysis chains от main:**
```
main
  ├─ 0001-oauth2-authorization   (analysis chain 0001)
  └─ 0002-oauth2-ui              (отдельный analysis chain 0002)
```

---

## 5. Граничные случаи

### Большой объём работы

Если analysis chain слишком велик для одного PR — **разбить на уровне analysis chain**: создать несколько Discussion с отдельными NNNN. Каждая Discussion → своя ветка → свой PR.

### Зависимые задачи

Если analysis A зависит от analysis B (который ещё не смержен):

Дождаться merge B → создать ветку A от обновлённой main.

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
git checkout 0001-oauth2-authorization
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
- Формат kebab-case, lowercase
- Существование папки `specs/analysis/{branch-name}/`

**Автоматизация:** Добавлен в pre-commit hook (→ [standard-commit.md § 6](../commits/standard-commit.md)).
