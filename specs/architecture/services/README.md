---
description: Per-service архитектура — спецификации отдельных сервисов, API, зависимости. Индекс сервисных документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: specs/architecture/services/README.md
---

# /specs/architecture/services/ — Per-service архитектура

Архитектурные документы отдельных сервисов: Code Map, Tech Stack, Planned Changes, Boundaries.

**Полезные ссылки:**
- [architecture/](../README.md)
- [Спецификации проекта](../../README.md)
- [Структура проекта](/.structure/README.md)

## Оглавление

- [1. Файлы](#1-файлы)
- [2. Дерево](#2-дерево)

---

## 1. Сервисы

| Сервис | Описание | Ключевые API | Технологии | Последний ADR |
|--------|----------|-------------|-----------|---------------|
| `notification` | Уведомления в реальном времени через WebSocket и REST API | — | — | — |
| `frontend` | Клиентское приложение — UI компоненты уведомлений | — | — | — |
| `gateway` | API Gateway — WebSocket proxy и rate limiting | — | — | — |
| `auth` | Аутентификация — генерация и валидация JWT | — | — | — |

---

## 2. Дерево

```
/specs/architecture/services/
├── README.md                # Этот файл
├── notification.md          # Сервис уведомлений (заглушка)
├── frontend.md              # Клиентское приложение (заглушка)
├── gateway.md               # API Gateway (заглушка)
└── auth.md                  # Аутентификация (заглушка)
```
