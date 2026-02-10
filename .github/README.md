---
description: GitHub конфигурация — шаблоны Issues/PR, workflows, labels, инструкции. Индекс .github/ директории.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/README.md
---

# /.github/ — GitHub конфигурация

Конфигурация GitHub: шаблоны Issues/PR, workflows, labels, инструкции.

**Полезные ссылки:**
- [Структура проекта](/.structure/README.md)

## Оглавление

- [1. Папки](#1-папки)
- [2. Файлы](#2-файлы)
- [3. Дерево](#3-дерево)

---

## 1. Папки

### 🔗 [.instructions/](./.instructions/README.md)

**Инструкции для работы с GitHub.**

Инструкции для работы с GitHub: Issues, Pull Requests, Releases, Labels, Workflows и другие объекты. Оркестратор workflow, 13 тематических подпапок.

### 🔗 [ISSUE_TEMPLATE/](./ISSUE_TEMPLATE/README.md)

**Шаблоны Issues.**

### 🔗 [workflows/](./workflows/README.md)

**GitHub Actions workflows.**

---

## 2. Файлы

| Файл | Описание |
|------|----------|
| [CODEOWNERS](./CODEOWNERS) | Владельцы кода — автоматическое назначение ревьюеров |
| [dependabot.yml](./dependabot.yml) | Конфигурация Dependabot (обновления зависимостей) |
| [labels.yml](./labels.yml) | Справочник меток проекта (SSOT) |
| [PULL_REQUEST_TEMPLATE.md](./PULL_REQUEST_TEMPLATE.md) | Шаблон Pull Request |
| [SECURITY.md](./SECURITY.md) | Политика безопасности (confidential disclosure) |

---

## 3. Дерево

```
/.github/
├── .instructions/                      # Инструкции для работы с GitHub
├── ISSUE_TEMPLATE/                     # Шаблоны Issues
├── workflows/                          # GitHub Actions workflows
├── CODEOWNERS                          # Владельцы кода
├── dependabot.yml                      # Конфигурация Dependabot
├── labels.yml                          # Справочник меток проекта
├── PULL_REQUEST_TEMPLATE.md            # Шаблон Pull Request
├── README.md                           # Этот файл
└── SECURITY.md                         # Политика безопасности
```
