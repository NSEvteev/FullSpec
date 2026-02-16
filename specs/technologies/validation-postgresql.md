---
description: Валидация кода на PostgreSQL — коды ошибок, чек-лист проверки.
standard: .instructions/standard-instruction.md
standard-version: v1.0
index: specs/technologies/README.md
technology: postgresql
---

# Валидация PostgreSQL

Рабочая версия стандарта: 1.0

Проверка соответствия кода стандарту [standard-postgresql.md](./standard-postgresql.md).

**Полезные ссылки:**
- [Технологический реестр](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-postgresql.md](./standard-postgresql.md) |
| Валидация | Этот документ |

## Оглавление

- [1. Когда валидировать](#1-когда-валидировать)
- [2. Коды ошибок](#2-коды-ошибок)
- [3. Чек-лист](#3-чек-лист)
- [4. Скрипты](#4-скрипты)

---

## 1. Когда валидировать

- После написания SQL-запросов или миграций
- При code review
- Перед коммитом (автоматически через rule)

---

## 2. Коды ошибок

| Код | Описание | Severity |
|-----|----------|----------|
| PG001 | Таблица не в snake_case или не во множественном числе | error |
| PG002 | Колонка не в snake_case | error |
| PG003 | Foreign key без индекса | error |
| PG004 | TIMESTAMP вместо TIMESTAMPTZ | error |
| PG005 | SELECT * в production-коде | warning |
| PG006 | N+1 запросы (цикл SELECT вместо JOIN) | error |
| PG007 | Миграция не соответствует формату `{NNN}_{description}.sql` | error |
| PG008 | Отсутствует `created_at` / `updated_at` в таблице | warning |
| PG009 | SQL ключевые слова не в UPPER CASE | warning |
| PG010 | Offset-based пагинация без обоснования (вместо cursor-based) | warning |

---

## 3. Чек-лист

- [ ] Таблицы в snake_case, множественное число
- [ ] Колонки в snake_case, единственное число
- [ ] FK именованы как `{referenced_table_singular}_id`
- [ ] Индексы на все FK (`idx_{table}_{columns}`)
- [ ] Все timestamp-колонки используют TIMESTAMPTZ
- [ ] `created_at` и `updated_at` присутствуют с DEFAULT NOW()
- [ ] Нет SELECT * в production-запросах
- [ ] Нет N+1 запросов (используются JOIN / подзапросы)
- [ ] SQL ключевые слова в UPPER CASE
- [ ] Миграции нумерованы: `{NNN}_{description}.sql`
- [ ] Порядок в миграции: TYPE → TABLE → INDEX → FUNCTION/TRIGGER
- [ ] Нет типичных ошибок из § 5 стандарта

---

## 4. Скрипты

| Скрипт | Назначение |
|--------|------------|
| [validate-postgresql-code.py](/specs/.instructions/.scripts/validate-postgresql-code.py) | Автоматическая проверка PG001-PG005, PG007, PG009 |
