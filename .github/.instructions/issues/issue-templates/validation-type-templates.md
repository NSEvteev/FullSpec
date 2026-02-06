---
description: Валидация соответствия type:* меток и Issue Templates
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/issues/issue-templates/README.md
---

# Валидация соответствия type:* и Issue Templates

Рабочая версия стандарта: 1.2

Проверка что для каждой метки `type:*` в `labels.yml` существует Issue Template, и наоборот.

**Полезные ссылки:**
- [Инструкции Issue Templates](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт Labels | [standard-labels.md](../../labels/standard-labels.md) |
| Стандарт Templates | [standard-issue-template.md](./standard-issue-template.md) |
| Валидация | Этот документ |
| Создание | *Не требуется (кросс-валидация)* |
| Модификация | *Не требуется (кросс-валидация)* |

## Оглавление

- [Когда валидировать](#когда-валидировать)
- [Шаги](#шаги)
- [Чек-лист](#чек-лист)
- [Типичные ошибки](#типичные-ошибки)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Когда валидировать

**После изменения меток `type:*`:**
- Добавление метки `type:*` в `labels.yml`
- Удаление метки `type:*` из `labels.yml`

**После изменения Issue Templates:**
- Создание нового шаблона
- Удаление шаблона
- Изменение `labels:` в шаблоне

**Автоматически:**
- Pre-commit hook при изменении `labels.yml` или `.github/ISSUE_TEMPLATE/*.yml`

---

## Шаги

### Шаг 1: Запустить валидацию

**Автоматически:**
```bash
python .github/.instructions/.scripts/validate-type-templates.py
```

**С подробным выводом:**
```bash
python .github/.instructions/.scripts/validate-type-templates.py --verbose
```

### Шаг 2: Исправить ошибки

| Ошибка | Действие |
|--------|----------|
| TT001: Метка без шаблона | Создать Issue Template (см. [standard-issue-template.md](./standard-issue-template.md)) |
| TT002: Шаблон без type:* | Добавить `labels: [type:{value}]` в шаблон |
| TT003: Неизвестная метка | Добавить метку в `labels.yml` или исправить опечатку |
| TT006: Нет поля dependencies | Добавить `id: dependencies` с `required: true` (см. [standard-issue-template.md § body](./standard-issue-template.md#body-обязательно)) |
| TT007: Нет поля related-docs | Добавить `id: related-docs` с `required: true` (см. [standard-issue-template.md § body](./standard-issue-template.md#body-обязательно)) |

### Шаг 3: Повторить валидацию

После исправления повторить Шаг 1.

---

## Чек-лист

- [ ] Для каждой метки `type:*` есть шаблон
- [ ] Каждый шаблон содержит `labels: [type:{value}]`
- [ ] Каждый шаблон содержит поле `id: related-docs` с `required: true`
- [ ] Каждый шаблон содержит поле `id: dependencies` с `required: true`
- [ ] Метки в шаблонах существуют в `labels.yml`
- [ ] Валидация проходит без ошибок

---

## Типичные ошибки

| Ошибка | Код | Причина | Решение |
|--------|-----|---------|---------|
| Метка без шаблона | TT001 | Добавили `type:*` в labels.yml без создания шаблона | Создать Issue Template |
| Шаблон без type:* | TT002 | Шаблон не содержит `labels: [type:{value}]` | Добавить метку в `labels:` |
| Неизвестная метка | TT003 | Опечатка в шаблоне или метка удалена | Исправить имя или добавить в labels.yml |
| labels.yml не найден | TT004 | Файл отсутствует | Создать `.github/labels.yml` |
| Папка не найдена | TT005 | Нет `.github/ISSUE_TEMPLATE/` | Создать папку и шаблоны |
| Нет поля dependencies | TT006 | Шаблон не содержит `id: dependencies` или `required: true` | Добавить обязательное поле dependencies |
| Нет поля related-docs | TT007 | Шаблон не содержит `id: related-docs` или `required: true` | Добавить обязательное поле related-docs |

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-type-templates.py](../../.scripts/validate-type-templates.py) | Валидация соответствия type:* и шаблонов | Этот документ |

---

## Скиллы

*Нет скиллов.*
