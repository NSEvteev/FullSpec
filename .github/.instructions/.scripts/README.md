---
description: Скрипты автоматизации GitHub
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/.scripts/README.md
---

# /.github/.instructions/.scripts/ — Скрипты

Скрипты автоматизации для работы с GitHub: синхронизация labels, валидация шаблонов.

**Полезные ссылки:**
- [Инструкции .github](../README.md)
- [.github](../../README.md)

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-labels.py](./validate-labels.py) | Валидация labels.yml и меток на Issues/PR | [validation-labels.md](../labels/validation-labels.md) |
| [sync-labels.py](./sync-labels.py) | Синхронизация labels.yml с GitHub | [modify-labels.md](../labels/modify-labels.md) |
| [migrate-label.py](./migrate-label.py) | Миграция меток на Issues/PR | [modify-labels.md](../labels/modify-labels.md) |
| [validate-pr-template.py](./validate-pr-template.py) | Валидация структуры PR template | [validation-pr-template.md](../pull-requests/pr-template/validation-pr-template.md) |
| [validate-codeowners.py](./validate-codeowners.py) | Валидация синтаксиса CODEOWNERS | [validation-codeowners.md](../codeowners/validation-codeowners.md) |
| [validate-type-templates.py](./validate-type-templates.py) | Валидация соответствия type:* и Issue Templates | [validation-type-templates.md](../issues/issue-templates/validation-type-templates.md) |
| [validate-milestone.py](./validate-milestone.py) | Валидация Milestone: title, description, due date, Issues, Release | [validation-milestone.md](../milestones/validation-milestone.md) |
| [create-milestone.py](./create-milestone.py) | Создание Milestone: версия, уникальность, API | [create-milestone.md](../milestones/create-milestone.md) |
| [close-milestone.py](./close-milestone.py) | Закрытие Milestone: проверки, перенос Issues | [modify-milestone.md](../milestones/modify-milestone.md) |
| [validate-action.py](./validate-action.py) | Валидация GitHub Actions workflow файлов (A001-A007) | [validation-action.md](../actions/validation-action.md) |
| [validate-security.py](./validate-security.py) | Валидация файлов безопасности (SEC001-SEC010) | [validation-security.md](../actions/security/validation-security.md) |
| [validate-issue.py](./validate-issue.py) | Валидация Issue: title, body, labels, assignees, milestone, закрытие | [validation-issue.md](../issues/validation-issue.md) |
| [rotate-secret.py](./rotate-secret.py) | Ротация секретов GitHub | [standard-secrets.md](../actions/security/standard-secrets.md) |
| [check-github-required.py](./check-github-required.py) | Проверка наличия обязательных файлов GitHub | — |

---

## Дерево

```
/.github/.instructions/.scripts/
├── README.md                           # Этот файл
├── validate-labels.py                  # Валидация labels.yml и меток
├── sync-labels.py                      # Синхронизация с GitHub
├── migrate-label.py                    # Миграция меток на Issues/PR
├── validate-codeowners.py              # Валидация синтаксиса CODEOWNERS
├── validate-pr-template.py             # Валидация структуры PR template
├── validate-type-templates.py          # Валидация type:* ↔ Issue Templates
├── validate-milestone.py              # Валидация Milestone по стандарту
├── create-milestone.py                # Создание Milestone по стандарту
├── close-milestone.py                 # Закрытие Milestone с проверками
├── validate-action.py                  # Валидация GitHub Actions workflows
├── validate-security.py                # Валидация файлов безопасности
├── validate-issue.py                   # Валидация Issue по стандарту
├── rotate-secret.py                    # Ротация секретов GitHub
└── check-github-required.py            # Проверка наличия обязательных файлов
```
