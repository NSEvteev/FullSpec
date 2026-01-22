---
type: standard
description: Feature flags: когда использовать, YAML vs Unleash
related:
  - config/environments.md
  - platform/deployment.md
---

# Feature Flags

Правила использования флагов функций (feature flags) для управления релизами.

## Оглавление

- [Когда использовать](#когда-использовать)
- [Варианты реализации](#варианты-реализации)
- [Структура](#структура)
- [Правила](#правила)
- [Жизненный цикл](#жизненный-цикл)
- [Примеры](#примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## Когда использовать

### Рекомендуется

| Сценарий | Описание |
|----------|----------|
| **Trunk-based development** | Код в main, но функция ещё не готова |
| **A/B тестирование** | Разные версии для разных пользователей |
| **Постепенный rollout** | 1% → 10% → 50% → 100% пользователей |
| **Kill switch** | Быстрое отключение проблемной функции |
| **Beta-тестирование** | Доступ только для определённых пользователей |

### Не рекомендуется

| Сценарий | Почему | Альтернатива |
|----------|--------|--------------|
| Конфигурация | Усложняет код | Файлы в `/config/` |
| Постоянные различия | Technical debt | Разные эндпоинты |
| Секреты | Небезопасно | Secrets manager |

---

## Варианты реализации

### Вариант 1: YAML файл (простой)

**Когда:** До 10 флагов, нет A/B тестов, нет динамического изменения.

```
/config/features/
  features.yaml
```

**Плюсы:**
- Просто
- Версионируется в git
- Нет внешних зависимостей

**Минусы:**
- Требует редеплой для изменения
- Нет UI для управления
- Нет аналитики

### Вариант 2: Unleash (продвинутый)

**Когда:** Много флагов, A/B тесты, динамическое управление.

```
/src/feature-flags/     ← сервис Unleash
```

**Плюсы:**
- UI для управления
- Аналитика использования
- Динамическое изменение без редеплоя
- A/B тестирование
- Градиент rollout

**Минусы:**
- Дополнительный сервис
- Сложнее в настройке

### Матрица выбора

| Критерий | YAML | Unleash |
|----------|:----:|:-------:|
| Количество флагов | < 10 | > 10 |
| A/B тестирование | ❌ | ✅ |
| Динамическое изменение | ❌ | ✅ |
| Простота | ✅ | ❌ |
| Аналитика | ❌ | ✅ |

---

## Структура

### YAML вариант

```yaml
# /config/features/features.yaml

flags:
  new_checkout_flow:
    enabled: false
    description: "Новый процесс оформления заказа"
    owner: "@team-checkout"
    created: "2024-01-15"
    expires: "2024-04-15"  # обязательно!

  dark_mode:
    enabled: true
    description: "Тёмная тема интерфейса"
    owner: "@team-ui"
    created: "2024-01-10"

  beta_api_v2:
    enabled: false
    description: "Бета версия API v2"
    owner: "@team-api"
    created: "2024-01-20"
    users:  # whitelist пользователей
      - "user-123"
      - "user-456"
```

### Unleash вариант

Конфигурация через UI или API Unleash. Схема хранится в БД сервиса.

---

## Правила

### 1. Обязательные поля

Каждый флаг **должен** иметь:

| Поле | Описание |
|------|----------|
| `enabled` | Текущее состояние |
| `description` | Что делает флаг |
| `owner` | Кто отвечает (команда/человек) |
| `created` | Дата создания |
| `expires` | Дата удаления (для временных) |

### 2. Временность флагов

**Флаги — временные!** Каждый флаг должен быть удалён после:
- Полного rollout (100% пользователей)
- Отмены функции
- Истечения срока эксперимента

**Срок жизни:** максимум 3 месяца.

### 3. Именование

| Формат | Пример |
|--------|--------|
| `snake_case` | `new_checkout_flow` |
| Описательное | `beta_api_v2`, `dark_mode` |
| Без `flag_` префикса | ~~`flag_dark_mode`~~ → `dark_mode` |

### 4. Код с флагами

```python
# Хорошо — чистый код с fallback
if feature_flags.is_enabled("new_checkout_flow"):
    return new_checkout()
else:
    return old_checkout()

# Плохо — вложенные условия
if feature_flags.is_enabled("flag_a"):
    if feature_flags.is_enabled("flag_b"):
        # ...
```

### 5. Тестирование

Тесты **обязаны** проверять оба состояния флага:
- `enabled: true`
- `enabled: false`

---

## Жизненный цикл

```
┌─────────────┐
│  CREATED    │ ← Флаг создан, enabled: false
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ROLLOUT    │ ← Постепенное включение (1% → 100%)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  STABLE     │ ← Флаг enabled: true для всех
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  CLEANUP    │ ← Удаление флага из кода
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  REMOVED    │ ← Флаг удалён из конфига
└─────────────┘
```

### Чек-лист удаления флага

- [ ] Флаг `enabled: true` для всех пользователей минимум 2 недели
- [ ] Нет ошибок, связанных с функцией
- [ ] Код без флага протестирован
- [ ] PR с удалением флага из кода
- [ ] Флаг удалён из конфига

---

## Примеры

### Пример 1: Простой флаг

```yaml
flags:
  new_payment_provider:
    enabled: false
    description: "Интеграция с новым платёжным провайдером"
    owner: "@team-payments"
    created: "2024-02-01"
    expires: "2024-05-01"
```

```python
# В коде
def process_payment(order):
    if feature_flags.is_enabled("new_payment_provider"):
        return new_provider.charge(order)
    return old_provider.charge(order)
```

### Пример 2: Флаг с whitelist

```yaml
flags:
  admin_dashboard_v2:
    enabled: false
    description: "Новый дизайн админ-панели"
    owner: "@team-admin"
    created: "2024-02-10"
    expires: "2024-04-10"
    users:
      - "admin-1"
      - "admin-2"
```

```python
def get_dashboard(user_id):
    if feature_flags.is_enabled_for_user("admin_dashboard_v2", user_id):
        return dashboard_v2()
    return dashboard_v1()
```

### Пример 3: Градиентный rollout (Unleash)

```
Unleash UI:
- Flag: new_search_algorithm
- Strategy: gradual rollout
- Percentage: 10%
- Increment: +10% каждые 2 дня
```

---

## Скиллы

> Специфичные скиллы для фича-флагов отсутствуют.
> Используйте [/environment-check](/.claude/skills/environment-check/SKILL.md) для проверки окружения.

---

## Связанные инструкции

- [environments.md](./environments.md) — конфигурации окружений
- [platform/deployment.md](../platform/deployment.md) — стратегии деплоя (canary)
