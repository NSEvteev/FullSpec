# /shared/ — Общий код между сервисами

## Зона ответственности

Код, используемый несколькими сервисами: контракты, библиотеки, ресурсы.

**IN:** contracts/, events/, libs/, assets/, i18n/, docs/

**Границы:**
- код для нескольких сервисов → здесь
- код конкретного сервиса → /src/{service}/
- реализация handlers → /src/

> [Разделение ответственности всех папок проекта](/.structure/README.md)

---

## Структура

```
shared/
├── contracts/        # API контракты
│   ├── openapi/      # REST (*.yaml)
│   └── protobuf/     # gRPC (*.proto)
├── events/           # Схемы событий
├── libs/             # Общие библиотеки
│   ├── errors/
│   ├── logging/
│   └── validation/
├── assets/           # Статические ресурсы
├── i18n/             # Локализация
└── docs/             # Документация shared
```

---

## Связи

- **Инструкции:** [/.claude/.instructions/shared/](/.claude/.instructions/shared/)
