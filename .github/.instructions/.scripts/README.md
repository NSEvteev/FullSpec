---
description: Скрипты автоматизации GitHub — валидация labels, issues, branches. Индекс Python-скриптов для CI/CD.
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
| [collect-pr-issues.py](./collect-pr-issues.py) | Сбор Issues из plan-dev.md для создания PR | [create-pull-request.md](../pull-requests/create-pull-request.md) |
| [validate-labels.py](./validate-labels.py) | Валидация labels.yml и меток на Issues/PR | [validation-labels.md](../labels/validation-labels.md) |
| [sync-labels.py](./sync-labels.py) | Синхронизация labels.yml с GitHub | [modify-labels.md](../labels/modify-labels.md) |
| [migrate-label.py](./migrate-label.py) | Миграция меток на Issues/PR | [modify-labels.md](../labels/modify-labels.md) |
| [validate-pr-template.py](./validate-pr-template.py) | Валидация структуры PR template | [validation-pr-template.md](../pull-requests/pr-template/validation-pr-template.md) |
| [validate-codeowners.py](./validate-codeowners.py) | Валидация синтаксиса CODEOWNERS | [validation-codeowners.md](../codeowners/validation-codeowners.md) |
| [validate-type-templates.py](./validate-type-templates.py) | Валидация соответствия меток типа и Issue Templates | [validation-type-templates.md](../issues/issue-templates/validation-type-templates.md) |
| [validate-milestone.py](./validate-milestone.py) | Валидация Milestone: title, description, due date, Issues, Release | [validation-milestone.md](../milestones/validation-milestone.md) |
| [create-milestone.py](./create-milestone.py) | Создание Milestone: версия, уникальность, API | [create-milestone.md](../milestones/create-milestone.md) |
| [close-milestone.py](./close-milestone.py) | Закрытие Milestone: проверки, перенос Issues | [modify-milestone.md](../milestones/modify-milestone.md) |
| [validate-action.py](./validate-action.py) | Валидация GitHub Actions workflow файлов (A001-A007) | [validation-action.md](../actions/validation-action.md) |
| [validate-deploy.py](./validate-deploy.py) | Валидация deploy.yml (D001-D008) | [validation-deploy.md](../actions/deploy/validation-deploy.md) |
| [validate-security.py](./validate-security.py) | Валидация файлов безопасности (SEC001-SEC010) | [validation-security.md](../actions/security/validation-security.md) |
| [validate-issue.py](./validate-issue.py) | Валидация Issue: title, body, labels, assignees, milestone, закрытие | [validation-issue.md](../issues/validation-issue.md) |
| [rotate-secret.py](./rotate-secret.py) | Ротация секретов GitHub | [standard-secrets.md](../actions/security/standard-secrets.md) |
| [validate-branch-name.py](./validate-branch-name.py) | Валидация имени ветки: формат, Issues, TYPE-метки (BR001-BR011) | [validation-branch.md](../branches/validation-branch.md) |
| [validate-pre-release.py](./validate-pre-release.py) | Валидация пре-релизных условий | [validation-release.md](../releases/validation-release.md) |
| [validate-post-release.py](./validate-post-release.py) | Валидация пост-релизных артефактов | [validation-release.md](../releases/validation-release.md) |
| [validate-review.py](./validate-review.py) | Pre-commit хук: проверка завершённости ревью кода (review.md, RESOLVED, READY) | [standard-review.md](../review/standard-review.md) |
| [check-github-required.py](./check-github-required.py) | Проверка наличия обязательных файлов GitHub | — |
| [check-chain-readiness.py](./check-chain-readiness.py) | Проверка готовности analysis chain (4/4 WAITING, 0 маркеров). Делегирует утилиты `chain_status.py` | [create-development.md](../development/create-development.md) |
| [dev-next-issue.py](./dev-next-issue.py) | Определение следующего незаблокированного Issue. Делегирует утилиты `chain_status.py` | [modify-development.md](../development/modify-development.md) |

---

## Дерево

```
/.github/.instructions/.scripts/
├── README.md                           # Этот файл
├── collect-pr-issues.py               # Сбор Issues для PR
├── validate-labels.py                  # Валидация labels.yml и меток
├── sync-labels.py                      # Синхронизация с GitHub
├── migrate-label.py                    # Миграция меток на Issues/PR
├── validate-codeowners.py              # Валидация синтаксиса CODEOWNERS
├── validate-pr-template.py             # Валидация структуры PR template
├── validate-type-templates.py          # Валидация меток типа ↔ Issue Templates
├── validate-milestone.py              # Валидация Milestone по стандарту
├── create-milestone.py                # Создание Milestone по стандарту
├── close-milestone.py                 # Закрытие Milestone с проверками
├── validate-action.py                  # Валидация GitHub Actions workflows
├── validate-deploy.py                  # Валидация deploy.yml (D001-D008)
├── validate-security.py                # Валидация файлов безопасности
├── validate-issue.py                   # Валидация Issue по стандарту
├── validate-branch-name.py             # Валидация имени ветки
├── validate-pre-release.py             # Валидация пре-релизных условий
├── validate-post-release.py            # Валидация пост-релизных артефактов
├── rotate-secret.py                    # Ротация секретов GitHub
├── validate-review.py                  # Pre-commit: проверка завершённости ревью
├── check-github-required.py            # Проверка наличия обязательных файлов
├── check-chain-readiness.py            # Проверка готовности analysis chain
└── dev-next-issue.py                   # Определение следующего Issue
```
