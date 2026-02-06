---
description: Воркфлоу создания ветки по стандарту ветвления
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/branches/README.md
---

# Воркфлоу создания ветки

Рабочая версия стандарта: 1.2

Пошаговый процесс создания ветки от main с корректным именем.

**Полезные ссылки:**
- [Инструкции branches](./README.md)

**SSOT-зависимости:**
- [standard-branching.md](./standard-branching.md) — стандарт ветвления (SSOT правил)
- [standard-sync.md](../sync/standard-sync.md) — синхронизация main
- [standard-labels.md](../labels/standard-labels.md) — TYPE-метки определяют префикс
- [standard-issue.md](../issues/standard-issue.md) — номера Issues в имени ветки

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-branching.md](./standard-branching.md) |
| Валидация | [validation-branch.md](./validation-branch.md) |
| Создание | Этот документ |
| Модификация | *Не требуется* |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Подготовить Issues](#шаг-1-подготовить-issues)
  - [Шаг 2: Определить префикс](#шаг-2-определить-префикс)
  - [Шаг 3: Сформировать имя ветки](#шаг-3-сформировать-имя-ветки)
  - [Шаг 4: Синхронизировать main](#шаг-4-синхронизировать-main)
  - [Шаг 5: Создать ветку](#шаг-5-создать-ветку)
  - [Шаг 6: Валидация](#шаг-6-валидация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Каждая ветка привязана к Issue.** Нет Issue — нет ветки. Сначала создать Issue (→ [create-issue.md](../issues/create-issue.md)).

> **Ветка создаётся ТОЛЬКО от актуального main.** Перед созданием обязательна синхронизация.

> **Одна задача (или группа связанных) — одна ветка — один PR.**

---

## Шаги

### Шаг 1: Подготовить Issues

1. Убедиться, что Issues созданы и имеют TYPE-метки:
   ```bash
   gh issue view {number} --json labels -q '[.labels[].name]'
   ```

2. Если Issues ещё нет — создать: `/issue-create`

3. Собрать номера Issues для ветки. Критерии группировки (→ [standard-issue.md § 9](../issues/standard-issue.md#8-декомпозиция-и-зависимости)):
   - Issues имеют общую цель
   - Issues затрагивают файлы с > 20% пересечений
   - Желательно одинаковые TYPE-метки

### Шаг 2: Определить префикс

**SSOT:** [standard-branching.md § 2](./standard-branching.md#2-naming-convention)

1. Найти Issue с минимальным номером в группе

2. Получить его TYPE-метку:
   ```bash
   gh issue view {min-number} --json labels -q '[.labels[].name] | map(select(. == "bug" or . == "feature" or . == "task" or . == "docs" or . == "refactor")) | .[0]'
   ```

3. Определить префикс:

| TYPE-метка | Префикс |
|------------|---------|
| `feature` | `feature/` |
| `bug` | `fix/` |
| `task` | `task/` |
| `docs` | `docs/` |
| `refactor` | `refactor/` |

### Шаг 3: Сформировать имя ветки

**Формат:** `{type}/{description}-{issue-numbers}`

1. **Description** — 2-3 слова в kebab-case:
   - Для feature/task — название функции: `auth`, `two-factor`, `api-gateway`
   - Для bug — симптом проблемы: `upload-errors`, `null-response`
   - Акронимы строчными: `api`, `jwt`, `cors`

2. **Issue numbers** — через дефис, в порядке возрастания:
   - Issues #45, #42, #50 → `42-45-50`

3. Собрать: `{prefix}/{description}-{numbers}`

**Пример:** Issues #42 (feature), #43 (feature), #44 (task) → `feature/auth-42-43-44`

### Шаг 4: Синхронизировать main

**SSOT:** [standard-sync.md](../sync/standard-sync.md)

```bash
git checkout main
git pull origin main
```

### Шаг 5: Создать ветку

```bash
git checkout -b {branch-name}
```

**Пример:**
```bash
git checkout -b feature/auth-42-43-44
```

### Шаг 6: Валидация

Проверить формат имени:

```bash
python .github/.instructions/.scripts/validate-branch-name.py
```

**При ошибках:** переименовать ветку:
```bash
git branch -m {old-name} {correct-name}
```

---

## Чек-лист

### Подготовка
- [ ] Issues созданы и имеют TYPE-метки
- [ ] Номера Issues собраны и отсортированы по возрастанию
- [ ] Определён Issue с минимальным номером
- [ ] Определён префикс по TYPE-метке min Issue

### Создание
- [ ] Сформировано имя: `{type}/{description}-{numbers}`
- [ ] Description в kebab-case, 2-3 слова, акронимы строчными
- [ ] main синхронизирован (`git pull origin main`)
- [ ] Ветка создана от main (`git checkout -b`)

### Проверка
- [ ] Валидация имени пройдена (validate-branch-name.py)
- [ ] Ветка создана от актуального main

---

## Примеры

### Одиночный Issue (feature)

```bash
# Issue #42: "Добавить авторизацию", метка: feature

# 1. Определить: TYPE=feature → prefix=feature
# 2. Имя: feature/auth-42
# 3. Синхронизировать
git checkout main && git pull origin main

# 4. Создать
git checkout -b feature/auth-42

# 5. Валидация
python .github/.instructions/.scripts/validate-branch-name.py
# ✅ Ветка 'feature/auth-42' — валидация пройдена
```

### Группа Issues (bug)

```bash
# Issues: #50 (bug: upload fails), #51 (bug: timeout on large files)

# 1. Min issue = #50, TYPE=bug → prefix=fix
# 2. Имя: fix/upload-errors-50-51
# 3. Синхронизировать
git checkout main && git pull origin main

# 4. Создать
git checkout -b fix/upload-errors-50-51
```

### Разные TYPE-метки в группе

```bash
# Issues: #42 (feature), #45 (bug), #50 (task)

# 1. Min issue = #42, TYPE=feature → prefix=feature
# 2. Имя: feature/auth-flow-42-45-50
git checkout main && git pull origin main
git checkout -b feature/auth-flow-42-45-50
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-branch-name.py](../.scripts/validate-branch-name.py) | Валидация имени ветки | [validation-branch.md](./validation-branch.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/branch-create](/.claude/skills/branch-create/SKILL.md) | Создание ветки по стандарту | Этот документ |
