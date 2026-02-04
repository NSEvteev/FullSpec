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
└── check-github-required.py            # Проверка наличия обязательных файлов
```
