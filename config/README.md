# /config/ — Конфигурации окружений

## Зона ответственности

Общие конфигурации окружений и feature flags.

**IN:** *.yaml (development, staging, production), feature-flags/

**Границы:**
- общие конфигурации окружений → здесь
- .env файлы сервиса → /src/{service}/
- секреты → vault / env vars

> **Все зоны:** [/.structure/responsibilities.md](/.structure/responsibilities.md)

---

## Структура

```
config/
├── development.yaml    # Окружение разработки
├── staging.yaml        # Staging окружение
├── production.yaml     # Production окружение
└── feature-flags/      # Feature flags
    └── flags.yaml
```

---

## Связи

- **Инструкции:** [/.claude/.instructions/config/](/.claude/.instructions/config/)
