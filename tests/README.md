# Tests (Общие тесты)

E2E и интеграционные тесты для всего проекта.

## Структура

```
tests/
├── e2e/                  # End-to-end тесты
│   ├── auth.spec.ts
│   ├── users.spec.ts
│   └── full-flow.spec.ts
│
├── integration/          # Интеграционные тесты между сервисами
│   ├── auth-users.spec.ts
│   └── api-gateway.spec.ts
│
└── load/                 # Нагрузочное тестирование
    ├── k6/
    └── artillery/
```

## E2E тесты

Полные сценарии использования приложения (Playwright, Cypress).

## Integration тесты

Взаимодействие между сервисами.

## Load тесты

Нагрузочное тестирование (k6, Artillery).
