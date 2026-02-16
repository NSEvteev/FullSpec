---
description: Воркфлоу изменения per-tech стандарта — обновление сервисов, версии, конвенций, деактивация.
standard: .instructions/standard-instruction.md
standard-version: v1.1
index: specs/.instructions/technologies/README.md
---

# Воркфлоу изменения per-tech стандарта

Рабочая версия стандарта: 1.1

Процесс обновления, отката и деактивации `standard-{tech}.md` + `validation-{tech}.md` + rule + реестра.

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
- [Сценарий B: Заполнение заглушки (ADR → DONE)](#сценарий-b-заполнение-заглушки-adr-done)
- [Сценарий C: Обновление конвенций](#сценарий-c-обновление-конвенций)
- [Сценарий D: Откат (ROLLING_BACK)](#сценарий-d-откат-rolling_back)
- [Сценарий E: Деактивация](#сценарий-e-деактивация)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Типы изменений

| Тип | Триггер | Описание |
|-----|---------|----------|
| Новый сервис | Design → WAITING (существующая технология) | Добавить сервис в колонку "Сервисы" реестра |
| Заполнение заглушки | ADR → DONE | Заменить placeholder конвенциями (→ Фаза 2 из [create-technology.md](./create-technology.md)) |
| Обновление конвенций | Ручное/ADR | Обновить правила в standard-{tech}.md |
| Откат Design | Design → ROLLING_BACK | Удалить заглушки, rule, строку реестра |
| Откат ADR | ADR → ROLLING_BACK | Вернуть к состоянию заглушки |
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

## Сценарий B: Заполнение заглушки (ADR → DONE)

**Триггер:** ADR → DONE, `standard-{tech}.md` содержит placeholder.

Выполнить Фазу 2 из [create-technology.md](./create-technology.md#фаза-2-заполнение-adr-done): шаги 7-10.

---

## Сценарий C: Обновление конвенций

**Триггер:** Изменение правил кодирования (новый ADR, ручное обновление).

### Шаг C1: Обновить standard-{tech}.md

Внести изменения в соответствующие секции (§ 2-6).

### Шаг C2: Обновить validation-{tech}.md

Обновить коды ошибок и чек-лист при изменении правил.

### Шаг C3: Валидация

```bash
python specs/.instructions/.scripts/validate-technology.py specs/.instructions/technologies/standard-{tech}.md --verbose
```

---

## Сценарий D: Откат (ROLLING_BACK)

### D1: Откат Design → ROLLING_BACK

**Условие:** Технология введена этим Design (не существовала ранее).

1. Удалить `standard-{tech}.md`
2. Удалить `validation-{tech}.md`
3. Удалить `.claude/rules/{tech}.md`
4. Удалить строку из `specs/technologies/README.md`
5. Обновить `specs/.instructions/technologies/README.md` (если обновлялся)

### D2: Откат ADR → ROLLING_BACK

**Условие:** ADR заполнил заглушку конвенциями.

1. Заменить содержание § 2-6 в `standard-{tech}.md` обратно на `*Заполняется при ADR → DONE.*`
2. Заменить содержание `validation-{tech}.md` обратно на placeholder
3. Убрать ссылку на стандарт из Code Map `architecture/services/{svc}.md`

---

## Сценарий E: Деактивация

**Триггер:** Технология выведена из проекта (все сервисы мигрировали).

### Шаг E1: Проверить использование

Проверить колонку "Сервисы" в реестре — должна быть пустой.

### Шаг E2: Удалить файлы

1. Удалить `standard-{tech}.md`
2. Удалить `validation-{tech}.md`
3. Удалить `.claude/rules/{tech}.md`
4. Удалить строку из `specs/technologies/README.md`
5. Обновить `specs/.instructions/technologies/README.md`

### Шаг E3: Обновить Code Map

Убрать строку из Tech Stack всех `architecture/services/{svc}.md`.

---

## Чек-лист

### Новый сервис (A)
- [ ] Колонка "Сервисы" в реестре обновлена
- [ ] "Последний Design" обновлён

### Заполнение заглушки (B)
- [ ] → Чек-лист Фазы 2 из [create-technology.md](./create-technology.md#чек-лист)

### Обновление конвенций (C)
- [ ] Изменения внесены в standard-{tech}.md
- [ ] validation-{tech}.md обновлён (если нужно)
- [ ] Валидация пройдена

### Откат Design (D1)
- [ ] standard-{tech}.md удалён
- [ ] validation-{tech}.md удалён
- [ ] Rule удалён
- [ ] Строка реестра удалена

### Откат ADR (D2)
- [ ] § 2-6 возвращены к placeholder
- [ ] validation-{tech}.md возвращён к placeholder
- [ ] Ссылка убрана из Code Map

### Деактивация (E)
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
# 1. Удалить specs/.instructions/technologies/standard-python.md
# 2. Удалить specs/.instructions/technologies/validation-python.md
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
