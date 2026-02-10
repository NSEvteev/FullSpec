---
description: Валидация GitHub Actions workflow на соответствие стандарту — структура, именование, секреты, permissions.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/actions/README.md
---

# Валидация GitHub Actions

Рабочая версия стандарта: 1.0

Проверка workflow файлов (`.github/workflows/*.yml`) на соответствие [standard-action.md](./standard-action.md).

**Полезные ссылки:**
- [Инструкции actions](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-action.md](./standard-action.md) |
| Валидация | Этот документ |
| Создание | *Не планируется* |
| Модификация | *Не планируется* |

## Оглавление

- [Когда валидировать](#когда-валидировать)
- [Шаги](#шаги)
  - [Шаг 1: Автоматическая проверка](#шаг-1-автоматическая-проверка)
  - [Шаг 2: Ручная проверка (при review)](#шаг-2-ручная-проверка-при-review)
- [Чек-лист](#чек-лист)
- [Типичные ошибки](#типичные-ошибки)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Когда валидировать

**Автоматически (pre-commit хук):**
- При коммите файлов `.github/workflows/*.yml`

**Вручную:**
- При code review PR с изменениями в workflows
- После создания нового workflow

---

## Шаги

### Шаг 1: Автоматическая проверка

**Скрипт:**

```bash
python .github/.instructions/.scripts/validate-action.py .github/workflows/ci.yml
python .github/.instructions/.scripts/validate-action.py --all
python .github/.instructions/.scripts/validate-action.py --all --json
```

**Что проверяет:**

| Код | Правило | Ссылка на стандарт |
|-----|---------|-------------------|
| A001 | `name:` указан на уровне workflow | [§ 12.1](./standard-action.md#121-именование) |
| A002 | `permissions:` явно указаны | [§ 12.3](./standard-action.md#123-минимизация-прав-permissions) |
| A003 | `timeout-minutes:` указан для каждого job | [§ 12.6](./standard-action.md#126-timeout-для-jobs) |
| A004 | Actions используют версию (`@v4`), а не ветку (`@main`) | [§ 12.2](./standard-action.md#122-версионирование-actions) |
| A005 | Secrets не используются напрямую в `run:` | [§ 12.8](./standard-action.md#128-secrets-в-переменных-окружения) |
| A006 | Каждый job имеет `runs-on:` | [§ 6](./standard-action.md#6-jobs-и-steps) |
| A007 | Файл расположен в `.github/workflows/` | [§ 2](./standard-action.md#2-расположение-и-именование) |

### Шаг 2: Ручная проверка (при review)

Скрипт проверяет формат, но не логику. При review дополнительно проверить:

| Проверка | Описание |
|----------|----------|
| Триггеры | Корректные ветки (`main`), нет лишних триггеров |
| Разделение CI/CD | Тесты и деплой не смешаны в одном workflow |
| Concurrency | Для deploy-workflows указан `concurrency:` |
| Environment | Для production указан `environment:` с Protection Rules |

---

## Чек-лист

### Автоматические проверки (скрипт)
- [ ] A001: `name:` указан
- [ ] A002: `permissions:` указаны
- [ ] A003: `timeout-minutes:` на каждом job
- [ ] A004: Actions версионированы (`@vN`)
- [ ] A005: Secrets через `env:`, не в `run:` напрямую
- [ ] A006: `runs-on:` на каждом job
- [ ] A007: Файл в `.github/workflows/`

### Ручные проверки (review)
- [ ] Триггеры корректны
- [ ] CI и CD разделены
- [ ] Concurrency для deploy
- [ ] Environment для production

---

## Типичные ошибки

| Ошибка | Код | Причина | Решение |
|--------|-----|---------|---------|
| Нет `permissions` | A002 | Забыли добавить | Добавить `permissions: contents: read` (минимум) |
| Нет `timeout-minutes` | A003 | Дефолт 360 мин — слишком много | Добавить `timeout-minutes: 15` (для CI) |
| `uses: actions/checkout@main` | A004 | Нестабильная ветка | Заменить на `@v4` |
| `${{ secrets.TOKEN }}` в `run:` | A005 | Секрет в command-line | Вынести в `env:` блок job/step |

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-action.py](../.scripts/validate-action.py) | Валидация workflow файлов (A001-A007) | Этот документ |

---

## Скиллы

*Нет скиллов.*
