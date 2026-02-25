# Post-release Validation — расширение стандарта

Расширение standard-release.md § 11: детализация post-deploy проверок, критерии успеха, таймауты, автоматизация.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** standard-release.md § 11 описывает post-deploy verification в 3 строки (health check, smoke tests, мониторинг). Этого недостаточно для формального процесса.
**Почему создан:** Post-release — критическая фаза. Без детального описания проверки выполняются по ощущениям.
**Связанные файлы:**
- `/.github/.instructions/releases/standard-release.md` — § 11 Публикация на production
- `/.github/.instructions/releases/validation-release.md` — шаги 3-6 (post-release)
- `/.github/.instructions/.scripts/validate-post-release.py` — текущий скрипт (303 строки)
- `.claude/drafts/2026-02-25-smoke-tests.md` — формализация smoke tests
- `.claude/drafts/2026-02-25-deploy-workflow.md` — deploy.yml

## Содержание

### Текущее описание (standard-release.md § 11)

| # | Проверка | Команда | Критерий |
|---|---------|---------|----------|
| 1 | Health check | `curl /health` | `{"status": "ok"}` |
| 2 | Smoke tests | Основные сценарии | Критичные пути работают |
| 3 | Мониторинг | Error rate (15 мин) | Error rate не вырос |

### Что нужно расширить

| Область | Текущее | Нужное |
|---------|---------|--------|
| Health check | Одна строка | Формат эндпоинта, таймауты, retry, per-service checks |
| Smoke tests | "Основные сценарии" | Формальный список сценариев, автоматизация (→ draft smoke-tests) |
| Мониторинг | "15 мин" | Конкретные метрики, пороги, инструменты |
| Rollback trigger | "Если критично → rollback" | Формальные критерии: когда rollback обязателен |
| Таймауты | Не указаны | Сколько ждать каждый шаг, когда считать провалом |
| Ответственность | Не указана | Кто выполняет проверки (автоматически vs человек) |

### Предлагаемая структура § 11 после расширения

```
§ 11. Публикация на production
  11.1 Триггер деплоя (текущее)
  11.2 Health check protocol
    - Формат: GET /health → 200 {"status": "ok", "version": "vX.Y.Z"}
    - Таймаут: 60 секунд, 3 retry с интервалом 10 секунд
    - Per-service: проверка каждого сервиса отдельно
  11.3 Smoke tests (→ SSOT: standard-testing.md или отдельный раздел)
  11.4 Мониторинг
    - Error rate: baseline (pre-release) vs current (post-release)
    - Latency: p50, p95 не выросли более чем на 20%
    - Availability: uptime > 99.9% за первые 30 мин
  11.5 Критерии rollback
    - Health check fail после 3 retry → автоматический rollback
    - Error rate > 5% за 15 мин → ручной rollback
    - Hotfix невозможен за 30 мин → rollback (уже в § 12)
  11.6 Проверка после деплоя — чек-лист
```

### Зависимости

- **deploy.yml** — без деплоя нечего валидировать (→ draft deploy-workflow)
- **smoke tests** — нет формализации (→ draft smoke-tests)
- **мониторинг** — нет инфраструктуры (Prometheus / Grafana / Datadog?)
- **health endpoint** — не определён в сервисах

## Решения

*Нет решений — зависит от инфраструктуры.*

## Открытые вопросы

- Какой мониторинг? (Prometheus + Grafana / Datadog / CloudWatch / ничего на старте?)
- Health check — стандартный формат для всех сервисов или per-service?
- Автоматический rollback в deploy.yml или ручное решение?
- Где описать расширение: в standard-release.md § 11 или в отдельном стандарте standard-post-release.md?
- validate-post-release.py — нужно ли расширять скрипт или он уже достаточен?
