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
- [standard-analysis.md](/specs/.instructions/analysis/standard-analysis.md) — analysis chain (именование NNNN, жизненный цикл)

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

> **Каждая ветка привязана к analysis chain** (→ [standard-analysis.md](/specs/.instructions/analysis/standard-analysis.md))**.** Нет analysis — нет ветки. Сначала пройти цепочку Discussion → Design → Plan Tests → Plan Dev.

> **Ветка создаётся ТОЛЬКО от актуального main.** Перед созданием обязательна синхронизация.

> **Один analysis chain — одна ветка — один PR.** Если объём слишком велик — разбить Discussion на несколько analysis chains.

---

## Шаги

### Шаг 1: Определить номер анализа

1. Убедиться, что analysis chain существует в `specs/analysis/NNNN-{topic}/` (→ [standard-analysis.md § 9](/specs/.instructions/analysis/standard-analysis.md))

2. Получить 4-значный номер NNNN (например, `0001`, `0042`)

3. Если analysis chain ещё нет — пройти цепочку SDD: начать с `/discussion-create` (→ [standard-discussion.md](/specs/.instructions/analysis/discussion/standard-discussion.md))

### Шаг 2: Определить имя ветки

**Имя ветки = имя папки analysis chain.** Без сокращений, без ручного выбора description.

```
specs/analysis/0001-oauth2-authorization/  →  ветка 0001-oauth2-authorization
```

**Пример:** analysis `0001-oauth2-authorization/` → ветка `0001-oauth2-authorization`

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
git checkout -b 0001-oauth2-authorization
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
- [ ] Имя ветки = имя папки analysis chain
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

# 1. Определить: папка = 0001-oauth2-authorization
# 2. Имя ветки = 0001-oauth2-authorization
# 3. Синхронизировать
git checkout main && git pull origin main

# 4. Создать
git checkout -b 0001-oauth2-authorization

# 5. Валидация
python .github/.instructions/.scripts/validate-branch-name.py
# ✅ Ветка '0001-oauth2-authorization' — валидация пройдена
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
