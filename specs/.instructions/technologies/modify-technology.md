---
description: Воркфлоу изменения per-tech стандарта — обновление сервисов, конвенций, откат, деактивация.
standard: .instructions/standard-instruction.md
standard-version: v1.1
index: specs/.instructions/technologies/README.md
---

# Воркфлоу изменения per-tech стандарта

Рабочая версия стандарта: 1.1

Процесс обновления, отката и деактивации `standard-{tech}.md` + `validation-{tech}.md` + rule + реестра. Стандарт создаётся полностью при Design → WAITING, поэтому "заполнение заглушки" не требуется.

**Полезные ссылки:**
- [Инструкции технологий](./README.md)
- [Стандарт технологий](./standard-technology.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-technology.md](./standard-technology.md) |
| Валидация | [validation-technology.md](./validation-technology.md) |
| Создание | [create-technology.md](./create-technology.md) |
| Модификация | Этот документ |

## Оглавление

- [Типы изменений](#типы-изменений)
- [Сценарий A: Новый сервис использует технологию](#сценарий-a-новый-сервис-использует-технологию)
- [Сценарий B: Обновление конвенций](#сценарий-b-обновление-конвенций)
- [Сценарий C: Откат (ROLLING_BACK)](#сценарий-c-откат-rolling_back)
- [Сценарий D: Деактивация](#сценарий-d-деактивация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Типы изменений

| Тип | Триггер | Описание |
|-----|---------|----------|
| Новый сервис | Design → WAITING (существующая технология) | Добавить сервис в колонку "Сервисы" реестра |
| Обновление конвенций | Ручное/ADR | Обновить правила в standard-{tech}.md |
| Откат Design | Design → ROLLING_BACK | Удалить standard, validation, rule, строку реестра |
| Деактивация | Технология выведена из проекта | Удалить standard + validation + rule + реестр |

---

## Сценарий A: Новый сервис использует технологию

**Триггер:** Design → WAITING, технология уже существует в реестре.

### Шаг A1: Обновить реестр

В `specs/technologies/README.md` обновить колонку "Сервисы" — добавить новый сервис:

```markdown
| Python | 3.12 | auth, billing, **notifications** | ... | design-0002 |
```

### Шаг A2: Обновить колонку "Последний Design"

Обновить на ID нового Design.

---

## Сценарий B: Обновление конвенций

**Триггер:** Изменение правил кодирования (новый ADR, ручное обновление).

### Шаг B1: Обновить standard-{tech}.md

Внести изменения в соответствующие секции (§ 2-6).

### Шаг B2: Обновить validation-{tech}.md

Обновить коды ошибок и чек-лист при изменении правил.

### Шаг B3: Валидация

```bash
python specs/.instructions/.scripts/validate-technology.py specs/technologies/standard-{tech}.md --verbose
```

---

## Сценарий C: Откат (ROLLING_BACK)

**Условие:** Технология введена этим Design (не существовала ранее). Design → ROLLING_BACK.

1. Удалить `standard-{tech}.md`
2. Удалить `validation-{tech}.md`
3. Удалить `.claude/rules/{tech}.md`
4. Удалить строку из `specs/technologies/README.md`
5. Обновить `specs/.instructions/technologies/README.md` (если обновлялся)

---

## Сценарий D: Деактивация

**Триггер:** Технология выведена из проекта (все сервисы мигрировали).

### Шаг D1: Проверить использование

Проверить колонку "Сервисы" в реестре — должна быть пустой.

### Шаг D2: Удалить файлы

1. Удалить `standard-{tech}.md`
2. Удалить `validation-{tech}.md`
3. Удалить `.claude/rules/{tech}.md`
4. Удалить строку из `specs/technologies/README.md`
5. Обновить `specs/.instructions/technologies/README.md`

### Шаг D3: Обновить Code Map

Убрать строку из Tech Stack всех `architecture/services/{svc}.md`.

---

## Чек-лист

### Новый сервис (A)
- [ ] Колонка "Сервисы" в реестре обновлена
- [ ] "Последний Design" обновлён

### Обновление конвенций (B)
- [ ] Изменения внесены в standard-{tech}.md
- [ ] validation-{tech}.md обновлён (если нужно)
- [ ] Валидация пройдена

### Откат Design (C)
- [ ] standard-{tech}.md удалён
- [ ] validation-{tech}.md удалён
- [ ] Rule удалён
- [ ] Строка реестра удалена

### Деактивация (D)
- [ ] Нет сервисов, использующих технологию
- [ ] Все файлы удалены
- [ ] Реестр обновлён
- [ ] Code Map очищен

---

## Примеры

### Новый сервис использует Python

```bash
# Design design-0002 → WAITING (notifications: Python 3.12 — уже в реестре)
# Обновить реестр: добавить notifications в колонку "Сервисы"
# | Python | 3.12 | auth, notifications | ... | design-0002 |
```

### Откат Design (Python — новая технология)

```bash
# Design design-0001 → ROLLING_BACK
# 1. Удалить specs/technologies/standard-python.md
# 2. Удалить specs/technologies/validation-python.md
# 3. Удалить .claude/rules/python.md
# 4. Удалить строку Python из specs/technologies/README.md
```

---

## Скрипты

| Скрипт | Назначение | Путь |
|--------|------------|------|
| `validate-technology.py` | Валидация per-tech стандарта | [specs/.instructions/.scripts/validate-technology.py](../.scripts/validate-technology.py) |

---

## Скиллы

| Скилл | Назначение | Путь |
|-------|------------|------|
| `/technology-modify` | Изменение per-tech стандарта | [.claude/skills/technology-modify/SKILL.md](/.claude/skills/technology-modify/SKILL.md) |
