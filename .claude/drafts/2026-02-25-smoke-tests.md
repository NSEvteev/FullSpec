# Smoke Tests — формализация pre/post-release тестирования

Определение стандарта smoke-тестов: что тестировать, как запускать, критерии pass/fail, интеграция с Release workflow.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** standard-release.md § 11 упоминает smoke tests ("основные сценарии"), но нет формального описания: что считать smoke test, как запускать, как автоматизировать.
**Почему создан:** Без формализации smoke tests — ручная проверка без критериев. Post-release validation неполная.
**Связанные файлы:**
- `/.github/.instructions/releases/standard-release.md` — § 11 Post-deploy verification
- `/tests/` — системные тесты (пусто)
- `.claude/drafts/2026-02-24-tests-and-platform.md` — аудит тестового покрытия
- `specs/docs/.system/testing.md` — стратегия тестирования (если существует)

## Содержание

### Что нужно

1. **Стандарт smoke tests** — что входит, критерии, формат
2. **Интеграция с Release** — pre-release и post-release фазы
3. **Автоматизация** — `make test-smoke` или отдельный скрипт
4. **Связь с `/tests/`** — где живут smoke tests в структуре проекта

### Типы тестов по фазам Release

| Фаза | Тип | Что проверяет | Как запускать |
|------|-----|---------------|--------------|
| Pre-release | Unit + Integration | Код работает | `make test` (уже в validate-pre-release.py) |
| Pre-release | E2E | Критичные user flows | `make test-e2e` (не реализовано) |
| Post-release | Health check | Сервисы доступны | `curl /health` |
| Post-release | Smoke | Критичные пути работают | `make test-smoke` (не существует) |
| Post-release | Мониторинг | Error rate не вырос | Observability (не настроена) |

### Связь с drafts

- `tests-and-platform.md` — описывает что `/tests/` пуст, CI не тестирует код
- `deploy-workflow.md` — smoke tests запускаются после деплоя

## Решения

*Нет решений — зависит от инфраструктуры и тестового фреймворка.*

## Открытые вопросы

- Какой тестовый фреймворк для smoke tests? (pytest + requests / Playwright / curl-скрипты)
- Какие сценарии считать "smoke"? (регистрация, логин, основной CRUD?)
- Smoke tests запускаются автоматически в deploy.yml или вручную после деплоя?
- Нужен ли отдельный стандарт (standard-testing.md) или раздел в standard-release.md?
- Как smoke tests соотносятся с тестовыми сценариями из analysis chain (plan-test.md)?
