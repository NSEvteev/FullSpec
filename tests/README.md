# /tests/ — Системные тесты

| IN | OUT |
|----|-----|
| e2e, integration, load, smoke, fixtures | Unit тесты (→ `/src/{service}/tests/`) |

## Структура

```
tests/
├── e2e/           # End-to-end сценарии
├── integration/   # Тесты между сервисами
├── load/          # Нагрузочные тесты (k6)
├── smoke/         # Smoke тесты
└── fixtures/      # Общие тестовые данные
```
