---
description: Валидация соответствия меток типа (type:*) и Issue Templates — наличие шаблонов, формат полей.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/issues/issue-templates/README.md
---

# Валидация соответствия меток типа и Issue Templates

Рабочая версия стандарта: 1.2

Проверка что для каждой метки типа (bug, task, docs, refactor, feature, infra, test) в `labels.yml` существует Issue Template, и наоборот.

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
  - [Шаг 0: Автоматическая валидация](#шаг-0-автоматическая-валидация)
  - [Шаг 1: Исправить ошибки](#шаг-1-исправить-ошибки)
- [Чек-лист](#чек-лист)
- [Типичные ошибки](#типичные-ошибки)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Когда валидировать

**После изменения меток типа:**
- Добавление метки типа в `labels.yml`
- Удаление метки типа из `labels.yml`

**После изменения Issue Templates:**
- Создание нового шаблона
- Удаление шаблона
- Изменение `labels:` в шаблоне

**Автоматически:**
- Pre-commit hook при изменении `labels.yml` или `.github/ISSUE_TEMPLATE/*.yml`

---

## Шаги

### Шаг 0: Автоматическая валидация

```bash
python .github/.instructions/.scripts/validate-type-templates.py
```

Скрипт проверяет все правила TT001-TT007. Если валидация пройдена — **готово**, шаг 1 не нужен.

**Если скрипт недоступен** — выполнить шаг 1 вручную.

### Шаг 1: Исправить ошибки

| Ошибка | Действие |
|--------|----------|
| TT001: Метка без шаблона | Создать Issue Template (см. [standard-issue-template.md](./standard-issue-template.md)) |
| TT002: Шаблон без метки типа | Добавить метку типа в `labels:` шаблона |
| TT003: Неизвестная метка | Добавить метку в `labels.yml` или исправить опечатку |
| TT006: Нет поля documents | Добавить `id: documents` с `required: true` (см. [standard-issue-template.md § body](./standard-issue-template.md#body-обязательно)) |
| TT007: Нет поля assignment | Добавить `id: assignment` с `required: true` (см. [standard-issue-template.md § body](./standard-issue-template.md#body-обязательно)) |
| TT008: Нет поля practical-context | Добавить `id: practical-context` с `required: true` (см. [standard-issue-template.md § body](./standard-issue-template.md#body-обязательно)) |
| TT009: Нет поля task-description | Добавить `id: task-description` с `required: true` (см. [standard-issue-template.md § body](./standard-issue-template.md#body-обязательно)) |

---

## Чек-лист

- [ ] Для каждой метки типа есть шаблон
- [ ] Каждый шаблон содержит метку типа в `labels:`
- [ ] Каждый шаблон содержит поле `id: task-description` с `required: true`
- [ ] Каждый шаблон содержит поле `id: documents` с `required: true`
- [ ] Каждый шаблон содержит поле `id: assignment` с `required: true`
- [ ] Каждый шаблон содержит поле `id: acceptance-criteria` с `required: true`
- [ ] Каждый шаблон содержит поле `id: practical-context` с `required: true`
- [ ] Метки в шаблонах существуют в `labels.yml`
- [ ] Валидация проходит без ошибок

---

## Типичные ошибки

| Ошибка | Код | Причина | Решение |
|--------|-----|---------|---------|
| Метка без шаблона | TT001 | Добавили метку типа в labels.yml без создания шаблона | Создать Issue Template |
| Шаблон без метки типа | TT002 | Шаблон не содержит метку типа в `labels:` | Добавить метку в `labels:` |
| Неизвестная метка | TT003 | Опечатка в шаблоне или метка удалена | Исправить имя или добавить в labels.yml |
| labels.yml не найден | TT004 | Файл отсутствует | Создать `.github/labels.yml` |
| Папка не найдена | TT005 | Нет `.github/ISSUE_TEMPLATE/` | Создать папку и шаблоны |
| Нет поля documents | TT006 | Шаблон не содержит `id: documents` или `required: true` | Добавить обязательное поле documents |
| Нет поля assignment | TT007 | Шаблон не содержит `id: assignment` или `required: true` | Добавить обязательное поле assignment |
| Нет поля practical-context | TT008 | Шаблон не содержит `id: practical-context` или `required: true` | Добавить обязательное поле practical-context |
| Нет поля task-description | TT009 | Шаблон не содержит `id: task-description` или `required: true` | Добавить обязательное поле task-description |

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-type-templates.py](../../.scripts/validate-type-templates.py) | Валидация соответствия меток типа и шаблонов | Этот документ |

---

## Скиллы

*Нет скиллов.*
