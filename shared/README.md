# /shared/ — Общий код между сервисами

| IN | OUT |
|----|-----|
| contracts, events, libs, assets, i18n | Код сервисов (→ `/src/`) |

## Структура

```
shared/
├── contracts/     # API контракты
│   ├── openapi/   # REST (*.yaml)
│   └── protobuf/  # gRPC (*.proto)
├── events/        # Схемы событий
├── libs/          # Общие библиотеки
├── assets/        # Статические ресурсы
└── i18n/          # Локализация
```
