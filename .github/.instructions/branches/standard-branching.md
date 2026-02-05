---
description: Стандарт именования и создания веток
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/branches/README.md
---

# Стандарт ветвления

Версия стандарта: 1.1

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
| Валидация | *Будет создан* |
| Создание | *Будет создан* |
| Модификация | *Будет создан* |

## Оглавление

- [1. Модель ветвления](#1-модель-ветвления)
- [2. Naming Convention](#2-naming-convention)
- [3. Жизненный цикл ветки](#3-жизненный-цикл-ветки)
- [4. Запреты и ограничения](#4-запреты-и-ограничения)
- [5. Граничные случаи](#5-граничные-случаи)

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
- Защищена от прямых push (Branch Protection Rules — см. [standard-review.md](../review/standard-review.md))
- Всегда стабильна — все изменения прошли review и CI
- Единственный источник для создания feature-веток

**Принципы:**
- Одна фича/область — группа Issues — одна ветка — один PR
- Feature-ветки удаляются после merge

---

## 2. Naming Convention

### Формат имени

```
{type}/{description}-{issue-numbers}
```

| Элемент | Правило | Пример |
|---------|---------|--------|
| `{type}` | Определяется TYPE-меткой первого Issue в группе | `feature`, `fix`, `docs` |
| `{description}` | Kebab-case, 2-3 слова, описание фичи/области | `auth`, `upload-errors` |
| `{issue-numbers}` | Номера всех Issues группы через дефис | `42-43-44` |

### Соответствие TYPE-меток и префиксов

| TYPE-метка Issue | Префикс ветки |
|------------------|---------------|
| `feature` | `feature/` |
| `bug` | `fix/` |
| `task` | `task/` |
| `docs` | `docs/` |
| `refactor` | `refactor/` |

### Правила выбора type

Если в группе Issues разные TYPE-метки — использовать тип первого Issue по номеру.

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

При длительной разработке (>2 дней) — синхронизировать feature-ветку с main (→ [standard-sync.md § 3](../sync/standard-sync.md#3-процесс-синхронизации)).

### Завершение

После merge PR в main ветка удаляется:
- **Автоматически:** если включено "Automatically delete head branches" в Settings → General
- **Вручную:**
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

Если Issues из группы затрагивают разные области кода без пересечений или имеют разные TYPE-метки — разделить на отдельные ветки и мержить последовательно:

```
main
  ├─ feature/auth-backend-42-43    (merge первым)
  └─ feature/auth-frontend-44-45   (создать от свежего main ПОСЛЕ merge первой)
```

Последовательность:
1. Создать и смержить первую ветку
2. Синхронизировать main (`git checkout main && git pull origin main`)
3. Создать вторую ветку от обновлённого main

### Ветка создана без Issue (ошибка)

1. Создать Issue: `gh issue create`
2. Получить номер (например, #123)
3. Переименовать ветку:
   ```bash
   git branch -m old-name feature/auth-123
   ```

### Переключение между ветками

При переключении на другую задачу — сохранить текущий прогресс:

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
