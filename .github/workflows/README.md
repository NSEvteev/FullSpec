---
description: GitHub Actions workflows — CI/CD пайплайны, автоматические проверки. Индекс YAML-файлов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/workflows/README.md
---

# /.github/workflows/ — GitHub Actions

YAML-файлы GitHub Actions для CI/CD.

**Полезные ссылки:**
- [GitHub конфигурация](../README.md)
- [Структура проекта](/.structure/README.md)

**Инструкции:** [.instructions/actions/](../.instructions/actions/README.md)

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
| [ci.yml](./ci.yml) | CI — pre-commit, тесты, линтинг, dependency review при push/PR |
| [pre-release.yml](./pre-release.yml) | Pre-release — полная валидация перед релизом (workflow_dispatch) |
| [deploy.yml](./deploy.yml) | Deploy — build & deploy сервисов при Release published ([standard-deploy.md](../.instructions/actions/deploy/standard-deploy.md)) |

---

## 3. Дерево

```
/.github/workflows/
├── ci.yml                   # CI — pre-commit, тесты, линтинг, dependency review
├── deploy.yml               # Deploy — build & deploy при Release published
├── pre-release.yml          # Pre-release — полная валидация перед релизом
└── README.md                # Этот файл
```
