---
description: Валидация безопасности GitHub — Dependabot, Secret Scanning, security policies. Чек-лист и коды ошибок.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/actions/security/README.md
---

# Валидация безопасности GitHub

Рабочая версия стандарта: 1.0

Проверка файлов безопасности (`dependabot.yml`, `SECURITY.md`, `codeql.yml`) на соответствие [standard-security.md](./standard-security.md).

**Полезные ссылки:**
- [Инструкции security](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-security.md](./standard-security.md) |
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
- При коммите файлов `dependabot.yml`, `SECURITY.md`, `codeql.yml`

**Вручную:**
- При code review PR с изменениями в файлах безопасности
- После создания нового репозитория из шаблона

---

## Шаги

### Шаг 1: Автоматическая проверка

**Скрипт:**

```bash
python .github/.instructions/.scripts/validate-security.py
python .github/.instructions/.scripts/validate-security.py --json
```

**Что проверяет:**

| Код | Правило | Ссылка на стандарт |
|-----|---------|-------------------|
| SEC001 | `dependabot.yml` существует | [§ 2](./standard-security.md#2-файлы-и-расположение) |
| SEC002 | `dependabot.yml` содержит `version: 2` | [§ 3](./standard-security.md#3-dependabot) |
| SEC003 | `dependabot.yml` содержит `updates` | [§ 3](./standard-security.md#3-dependabot) |
| SEC004 | Каждый ecosystem имеет обязательные поля | [§ 3](./standard-security.md#3-dependabot) |
| SEC005 | `SECURITY.md` существует | [§ 6](./standard-security.md#6-securitymd) |
| SEC006 | `SECURITY.md` имеет секцию Reporting | [§ 6](./standard-security.md#6-securitymd) |
| SEC007 | `SECURITY.md` имеет секцию Response timeline | [§ 6](./standard-security.md#6-securitymd) |
| SEC008 | `codeql.yml` существует | [§ 4](./standard-security.md#4-code-scanning-codeql) |
| SEC009 | `codeql.yml` использует Advanced Setup (matrix.language) | [§ 4](./standard-security.md#4-code-scanning-codeql) |
| SEC010 | `codeql.yml` имеет `permissions` | [§ 4](./standard-security.md#4-code-scanning-codeql) |

### Шаг 2: Ручная проверка (при review)

Скрипт проверяет формат, но не Settings. При review дополнительно проверить:

| Проверка | Описание |
|----------|----------|
| Settings: Dependabot | Dependabot Alerts и Security Updates включены |
| Settings: Secret Scanning | Secret Scanning и Push Protection включены |
| Settings: Code Scanning | Default Setup НЕ включён (конфликт с codeql.yml) |
| dependabot.yml: директории | Все сервисы монорепо перечислены |
| codeql.yml: языки | Все используемые языки в `matrix.language` |
| SECURITY.md: контакт | Email актуален |

---

## Чек-лист

### Автоматические проверки (скрипт)
- [ ] SEC001-SEC004: dependabot.yml корректен
- [ ] SEC005-SEC007: SECURITY.md корректен
- [ ] SEC008-SEC010: codeql.yml корректен (Advanced Setup)

### Ручные проверки (review)
- [ ] Dependabot Alerts включены в Settings
- [ ] Secret Scanning + Push Protection включены
- [ ] Default Setup НЕ включён
- [ ] Все сервисы перечислены в dependabot.yml
- [ ] Все языки перечислены в codeql.yml

---

## Типичные ошибки

| Ошибка | Код | Причина | Решение |
|--------|-----|---------|---------|
| Нет `dependabot.yml` | SEC001 | Файл не создан | Скопировать из стандарта [§ 3](./standard-security.md#3-dependabot) |
| Нет `version: 2` | SEC002 | Старый формат | Добавить `version: 2` в начало файла |
| Нет `SECURITY.md` | SEC005 | Файл не создан | Скопировать из стандарта [§ 6](./standard-security.md#6-securitymd) |
| Нет `matrix.language` | SEC009 | Используется Default Setup | Переключиться на Advanced Setup [§ 4](./standard-security.md#4-code-scanning-codeql) |

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-security.py](../../.scripts/validate-security.py) | Валидация файлов безопасности (SEC001-SEC010) | Этот документ |

---

## Скиллы

*Нет скиллов.*
