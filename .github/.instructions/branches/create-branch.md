---
description: Воркфлоу создания ветки — формирование имени из analysis chain, проверка уникальности.
standard: .instructions/standard-instruction.md
standard-version: v2.0
index: .github/.instructions/branches/README.md
---

# Воркфлоу создания ветки

Рабочая версия стандарта: 2.0

Пошаговый процесс создания ветки от main с корректным именем.

**Полезные ссылки:**
- [Инструкции branches](./README.md)

**SSOT-зависимости:**
- [standard-branching.md](./standard-branching.md) — стандарт ветвления (SSOT правил)
- [standard-sync.md](../sync/standard-sync.md) — синхронизация main

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
  - [Шаг 1: Определить номер анализа](#шаг-1-определить-номер-анализа)
  - [Шаг 2: Сформировать имя ветки](#шаг-2-сформировать-имя-ветки)
  - [Шаг 3: Синхронизировать main](#шаг-3-синхронизировать-main)
  - [Шаг 4: Создать ветку](#шаг-4-создать-ветку)
  - [Шаг 5: Валидация](#шаг-5-валидация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Каждая ветка привязана к analysis chain.** Нет analysis — нет ветки. Сначала пройти цепочку Discussion → Design → Plan Tests → Plan Dev.

> **Ветка создаётся ТОЛЬКО от актуального main.** Перед созданием обязательна синхронизация.

> **Один analysis chain — одна ветка — один PR.** При большом объёме — несколько веток с одним NNNN и разными description.

---

## Шаги

### Шаг 1: Определить номер анализа

1. Убедиться, что analysis chain существует в `specs/analysis/NNNN-{topic}/`

2. Получить 4-значный номер NNNN (например, `0001`, `0042`)

3. Если analysis chain ещё нет — пройти цепочку SDD: начать с `/discussion-create`

### Шаг 2: Сформировать имя ветки

**Формат:** `{NNNN}-{description}`

1. **NNNN** — 4-значный номер анализа

2. **Description** — 1-4 слова в kebab-case:
   - Из topic slug analysis directory: `oauth2-auth`, `notification-service`
   - Или уточнение при нескольких ветках: `oauth2-backend`, `oauth2-frontend`
   - Акронимы строчными: `api`, `jwt`, `cors`

3. Собрать: `{NNNN}-{description}`

**Пример:** analysis `0001-oauth2-authorization/` → ветка `0001-oauth2-auth`

### Шаг 3: Синхронизировать main

**SSOT:** [standard-sync.md](../sync/standard-sync.md)

```bash
git checkout main
git pull origin main
```

### Шаг 4: Создать ветку

```bash
git checkout -b {branch-name}
```

**Пример:**
```bash
git checkout -b 0001-oauth2-auth
```

### Шаг 5: Валидация

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
- [ ] Analysis chain существует (`specs/analysis/NNNN-{topic}/`)
- [ ] Определён 4-значный номер NNNN

### Создание
- [ ] Сформировано имя: `{NNNN}-{description}`
- [ ] Description в kebab-case, 1-4 слова, акронимы строчными
- [ ] main синхронизирован (`git pull origin main`)
- [ ] Ветка создана от main (`git checkout -b`)

### Проверка
- [ ] Валидация имени пройдена (validate-branch-name.py)
- [ ] Ветка создана от актуального main

---

## Примеры

### Стандартная ветка

```bash
# Analysis: specs/analysis/0001-oauth2-authorization/

# 1. Определить: NNNN=0001, topic=oauth2-authorization
# 2. Имя: 0001-oauth2-auth
# 3. Синхронизировать
git checkout main && git pull origin main

# 4. Создать
git checkout -b 0001-oauth2-auth

# 5. Валидация
python .github/.instructions/.scripts/validate-branch-name.py
# ✅ Ветка '0001-oauth2-auth' — валидация пройдена
```

### Несколько веток для одного analysis

```bash
# Analysis: specs/analysis/0001-oauth2-authorization/
# Объём большой — делим на backend и frontend

# Ветка 1:
git checkout main && git pull origin main
git checkout -b 0001-oauth2-backend

# ... merge первой ветки ...

# Ветка 2:
git checkout main && git pull origin main
git checkout -b 0001-oauth2-frontend
```

### Срочный баг

```bash
# Даже hotfix проходит через analysis chain
# Analysis: specs/analysis/0015-payment-crash/

git checkout main && git pull origin main
git checkout -b 0015-hotfix-payment-crash
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
