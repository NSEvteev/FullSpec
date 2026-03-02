---
description: YAML-шаблоны для создания GitHub Issues — config.yml, типы задач. Индекс шаблонов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/ISSUE_TEMPLATE/README.md
---

# /.github/ISSUE_TEMPLATE/ — Шаблоны Issues

YAML-шаблоны для создания Issues в GitHub.

**Полезные ссылки:**
- [GitHub конфигурация](../README.md)
- [Структура проекта](/.structure/README.md)

**Инструкции:** [.instructions/issues/issue-templates/](../.instructions/issues/issue-templates/README.md)

## Оглавление

- [1. Папки](#1-папки)
- [2. Файлы](#2-файлы)
- [3. Дерево](#3-дерево)

---

## 1. Папки

*Нет подпапок.*

---

## 2. Файлы

| Файл | Описание |
|------|----------|
| [bug-report.yml](./bug-report.yml) | Баг-репорт — сообщить о баге или неожиданном поведении |
| [config.yml](./config.yml) | Конфигурация Issue chooser (blank issues отключены) |
| [docs.yml](./docs.yml) | Документация — проблема или улучшение документации |
| [feature.yml](./feature.yml) | Функциональность — новая бизнес-логика, CRUD, UI |
| [infra.yml](./infra.yml) | Инфраструктура — Docker, CI/CD, конфиги окружений |
| [refactor.yml](./refactor.yml) | Рефакторинг — без изменения функциональности |
| [task.yml](./task.yml) | Задача — техническая задача или улучшение |
| [test.yml](./test.yml) | Тесты — E2E, integration, load, smoke тесты |

---

## 3. Дерево

```
/.github/ISSUE_TEMPLATE/
├── bug-report.yml                      # Баг-репорт
├── config.yml                          # Конфигурация Issue chooser
├── docs.yml                            # Документация
├── feature.yml                         # Функциональность
├── infra.yml                           # Инфраструктура
├── refactor.yml                        # Рефакторинг
├── task.yml                            # Задача
├── test.yml                            # Тесты
└── README.md                           # Этот файл
```
