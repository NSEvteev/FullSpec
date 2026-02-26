---
description: Валидация deploy.yml на соответствие стандарту — триггер, discover, matrix, environments, rollback, permissions.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/actions/deploy/README.md
---

# Валидация Deploy Workflow

Рабочая версия стандарта: 1.0

Проверка `deploy.yml` на соответствие [standard-deploy.md](./standard-deploy.md).

**Полезные ссылки:**
- [Инструкции deploy](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-deploy.md](./standard-deploy.md) |
| Валидация | Этот документ |
| Создание | *Не требуется — deploy.yml создаётся при /init-project* |
| Модификация | *Не требуется — deploy.yml не меняется вручную* |

## Оглавление

- [Когда валидировать](#когда-валидировать)
- [Проверки](#проверки)
- [Шаги](#шаги)
- [Чек-лист](#чек-лист)
- [Скрипты](#скрипты)

---

## Когда валидировать

**Автоматически (pre-commit хук):**
- При коммите `.github/workflows/deploy.yml`

**Вручную:**
- После создания deploy.yml при `/init-project`
- При code review PR с изменениями в deploy.yml

---

## Проверки

| Код | Проверка | Уровень |
|-----|---------|---------|
| D001 | deploy.yml существует | Критичный |
| D002 | Триггер `release: types: [published]` | Критичный |
| D003 | Discover job с `outputs.services` (dynamic service discovery) | Критичный |
| D004 | Matrix strategy с `fromJson()` из discover outputs | Критичный |
| D005 | Environment `staging` присутствует | Критичный |
| D006 | Environment `production` присутствует | Критичный |
| D007 | Rollback job с `if: failure()` | Критичный |
| D008 | Permissions `packages: write` | Критичный |

---

## Шаги

### Шаг 1: Автоматическая проверка

**Скрипт:**

```bash
python .github/.instructions/.scripts/validate-deploy.py
python .github/.instructions/.scripts/validate-deploy.py --json
```

**Ожидаемый результат:**

```
✅ deploy.yml — валидация пройдена
```

### Шаг 2: Ручная проверка (при review)

Дополнительно к автоматическим проверкам:

1. Pre-release guard: `if: "!github.event.release.prerelease"` на discover job
2. `timeout-minutes` на всех deploy jobs
3. PLACEHOLDER-комментарии на deploy commands (до /init-project)
4. Health check endpoints (`/health`) в smoke test steps

---

## Чек-лист

- [ ] D001: deploy.yml существует в `.github/workflows/`
- [ ] D002: Триггер `on: release: types: [published]`
- [ ] D003: Job discover с `outputs.services`
- [ ] D004: Matrix `service: ${{ fromJson(...) }}`
- [ ] D005: Environment `staging`
- [ ] D006: Environment `production`
- [ ] D007: Rollback job с `if: failure()`
- [ ] D008: `permissions: packages: write`

---

## Скрипты

| Скрипт | Назначение |
|--------|-----------|
| [validate-deploy.py](../../.scripts/validate-deploy.py) | Автоматическая валидация deploy.yml (D001-D008) |
