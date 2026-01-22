# /doc/ — Документация проекта

| IN | OUT |
|----|-----|
| README, guides, runbooks | Спецификации (→ `/specs/`) |

## Структура

```
doc/
├── runbooks/      # Общие runbooks (system)
├── src/           # Документация сервисов
│   └── {service}/
│       └── runbooks/  # Runbooks сервиса
├── shared/        # Документация общего кода
└── platform/      # Документация инфраструктуры
    └── runbooks/  # Runbooks инфраструктуры
```
