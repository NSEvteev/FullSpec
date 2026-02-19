---
description: Технологический реестр проекта — какие технологии используются, версии, сервисы, ссылки на стандарты.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: specs/technologies/README.md
---

# /specs/technologies/ — Технологический реестр

Какие технологии используются в проекте — версии, сервисы, ссылки на стандарты.

**Полезные ссылки:**
- [Спецификации проекта](../README.md)
- [Инструкции](/specs/.instructions/technologies/README.md)

## Оглавление

- [1. Папки](#1-папки)
- [2. Файлы](#2-файлы)
- [3. Реестр технологий](#3-реестр-технологий)
- [4. Дерево](#4-дерево)

---

## 1. Папки

*Нет подпапок.*

---

## 2. Файлы

| Файл | Описание |
|------|----------|
| [README.md](./README.md) | Этот файл (реестр технологий) |
| [standard-postgresql.md](./standard-postgresql.md) | Стандарт PostgreSQL |
| [validation-postgresql.md](./validation-postgresql.md) | Валидация PostgreSQL |
| [standard-redis.md](./standard-redis.md) | Стандарт Redis |
| [validation-redis.md](./validation-redis.md) | Валидация Redis |

---

## 3. Реестр технологий

| Технология | Версия | Сервисы | Стандарт | Последний Design |
|-----------|--------|---------|---------|-----------------|
| PostgreSQL | 16 | notification | [standard-postgresql.md](/specs/technologies/standard-postgresql.md) | design-0001 |
| Redis | 7 | notification | [standard-redis.md](/specs/technologies/standard-redis.md) | design-0001 |

---

## 4. Дерево

```
/specs/technologies/
├── standard-postgresql.md   # Стандарт PostgreSQL
├── validation-postgresql.md # Валидация PostgreSQL
├── standard-redis.md        # Стандарт Redis
├── validation-redis.md      # Валидация Redis
└── README.md                # Этот файл (реестр технологий)
```
