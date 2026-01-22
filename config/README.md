# /config/ — Конфигурации окружений

| IN | OUT |
|----|-----|
| environments, feature-flags | .env сервисов (→ `/src/{service}/`) |

## Структура

```
config/
├── development.yaml    # Окружение разработки
├── staging.yaml        # Staging окружение
├── production.yaml     # Production окружение
└── feature-flags/      # Feature flags
```
