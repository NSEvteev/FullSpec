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

---

## Дерево

```
/.github/.instructions/.scripts/
├── README.md                           # Этот файл
├── validate-labels.py                  # Валидация labels.yml и меток
├── sync-labels.py                      # Синхронизация с GitHub
└── migrate-label.py                    # Миграция меток на Issues/PR
```
