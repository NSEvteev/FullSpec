# /tests/ — Системные тесты

## Зона ответственности

Тесты всей системы: e2e, интеграция между сервисами, нагрузка.

**IN:** e2e/, integration/, load/, smoke/, fixtures/, conftest.py

**Границы:**
- системные тесты → здесь
- unit тесты сервиса → /src/{service}/tests/
- integration тесты внутри сервиса → /src/{service}/tests/integration/

**Полезные ссылки:**
- [Структура проекта](/.structure/README.md)

---

## Структура

```
tests/
├── e2e/              # End-to-end сценарии
├── integration/      # Тесты между сервисами
├── load/             # Нагрузочные тесты (k6)
├── smoke/            # Smoke тесты
└── fixtures/         # Общие тестовые данные
```

---

## Связи

- **Инструкции:** [/.claude/.instructions/tests/](/.claude/.instructions/tests/)
