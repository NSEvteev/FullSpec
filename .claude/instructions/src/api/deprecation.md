---
type: standard
description: Вывод API: Sunset header, Deprecation header, сроки, migration guide
related:
  - src/api/versioning.md
  - src/api/design.md
  - src/api/swagger.md
---

# API Deprecation

Правила вывода API из эксплуатации: заголовки, сроки, миграция.

## Оглавление

- [Правила](#правила)
  - [HTTP заголовки](#http-заголовки)
  - [Сроки deprecation](#сроки-deprecation)
  - [Коммуникация](#коммуникация)
  - [Migration Guide](#migration-guide)
- [Примеры](#примеры)
- [Чек-лист deprecation](#чек-лист-deprecation)
- [FAQ](#faq)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### HTTP заголовки

**Правило:** Использовать стандартные заголовки deprecation (RFC 8594).

| Заголовок | Назначение | Формат |
|-----------|------------|--------|
| `Deprecation` | Дата начала deprecation | HTTP-date или `true` |
| `Sunset` | Дата отключения | HTTP-date |
| `Link` | Ссылка на документацию/новую версию | URL |

**Правило:** Заголовок `Deprecation` обязателен для deprecated endpoints.

```http
HTTP/1.1 200 OK
Deprecation: Sat, 01 Jun 2024 00:00:00 GMT
Sunset: Sat, 01 Dec 2024 00:00:00 GMT
Link: </api/v2/users>; rel="successor-version"
Link: <https://docs.example.com/migration/v1-to-v2>; rel="deprecation"
```

**Правило:** Заголовок `Sunset` — дата полного отключения.

```http
Sunset: Sat, 01 Dec 2024 00:00:00 GMT
```

После этой даты endpoint возвращает:
```http
HTTP/1.1 410 Gone
{"error": {"code": "API_SUNSET", "message": "This API version has been retired. Please use /api/v2/"}}
```

**Правило:** Заголовок `Link` указывает на новую версию и документацию миграции.

```http
Link: </api/v2/users>; rel="successor-version"
Link: <https://docs.example.com/api/migration>; rel="deprecation"
```

### Сроки deprecation

**Правило:** Минимальный срок между deprecation и sunset — 6 месяцев.

```
Deprecation announcement: 01.06.2024
Sunset date:              01.12.2024 (+ 6 месяцев)
```

**Правило:** Для критичных API (платежи, авторизация) — минимум 12 месяцев.

| Тип API | Минимальный срок | Причина |
|---------|------------------|---------|
| Внутренний | 3 месяца | Контролируем клиентов |
| Публичный | 6 месяцев | Внешние интеграторы |
| Критичный (платежи) | 12 месяцев | Регуляторные требования |

**Жизненный цикл deprecation:**

```
[Active] -> [Deprecated] -> [Sunset Warning] -> [Gone]
    |            |                 |               |
    |            |                 |               +-- 410 Gone
    |            |                 +-- За 30 дней: email, warnings
    |            +-- Deprecation header, работает
    +-- Без заголовков, полная поддержка
```

### Коммуникация

**Правило:** Уведомлять о deprecation через несколько каналов.

| Канал | Когда | Что включить |
|-------|-------|--------------|
| HTTP заголовки | Каждый ответ | Deprecation, Sunset, Link |
| Email | При объявлении + за 30 дней до sunset | Migration guide |
| Документация | При объявлении | Changelog, migration guide |
| API response warning | Опционально | Поле `_warning` |

**Правило:** Дополнительное предупреждение в теле ответа (опционально).

```json
{
  "data": [...],
  "_meta": {
    "deprecation": {
      "message": "This API version is deprecated and will be removed on 2024-12-01",
      "migration_guide": "https://docs.example.com/migration/v1-to-v2",
      "successor": "/api/v2/users"
    }
  }
}
```

**Правило:** За 30 дней до sunset — усиленное уведомление.

```http
HTTP/1.1 200 OK
Deprecation: Sat, 01 Jun 2024 00:00:00 GMT
Sunset: Sat, 01 Dec 2024 00:00:00 GMT
Warning: 299 - "API sunset in 30 days. Migrate to /api/v2/"
```

### Migration Guide

**Правило:** Migration guide обязателен для каждого deprecated endpoint/версии.

**Структура migration guide:**

```markdown
# Migration Guide: v1 -> v2

## Обзор изменений
- Краткое описание что изменилось

## Breaking Changes
- Список несовместимых изменений

## Шаги миграции
1. Шаг 1
2. Шаг 2

## Маппинг endpoints
| v1 | v2 |
|----|----|

## Маппинг полей
| v1 field | v2 field | Изменения |
|----------|----------|-----------|

## Примеры кода
- До (v1)
- После (v2)

## FAQ / Troubleshooting

## Поддержка
- Контакты для вопросов по миграции
```

**Правило:** Migration guide должен быть доступен по URL из заголовка `Link`.

---

## Примеры

### Пример 1: Deprecated endpoint response

```http
GET /api/v1/users/123

HTTP/1.1 200 OK
Content-Type: application/json
Deprecation: Sat, 01 Jun 2024 00:00:00 GMT
Sunset: Sat, 01 Dec 2024 00:00:00 GMT
Link: </api/v2/users/123>; rel="successor-version"
Link: <https://docs.example.com/api/migration/v1-v2>; rel="deprecation"

{
  "id": 123,
  "name": "John Doe",
  "_meta": {
    "deprecation_warning": "This API version is deprecated. Please migrate to /api/v2/"
  }
}
```

### Пример 2: Sunset response (после отключения)

```http
GET /api/v1/users/123

HTTP/1.1 410 Gone
Content-Type: application/json

{
  "error": {
    "code": "API_SUNSET",
    "message": "API v1 has been retired on 2024-12-01",
    "details": {
      "successor": "/api/v2/users/123",
      "migration_guide": "https://docs.example.com/api/migration/v1-v2"
    }
  }
}
```

### Пример 3: Deprecation конкретного поля

```http
GET /api/v2/users/123

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "123",
  "name": "John Doe",
  "fullName": "John Doe",  // Новое поле
  "_meta": {
    "deprecated_fields": {
      "name": {
        "replacement": "fullName",
        "sunset": "2025-01-01",
        "message": "Use 'fullName' instead of 'name'"
      }
    }
  }
}
```

### Пример 4: Migration guide пример

```markdown
# Migration Guide: Users API v1 -> v2

## Обзор изменений

API v2 добавляет пагинацию, изменяет формат ID и расширяет модель User.

## Breaking Changes

1. **ID теперь string** (был int64)
2. **Ответ обёрнут в `data`** (был голый массив)
3. **Удалено поле `middleName`**
4. **Поле `name` переименовано в `fullName`**

## Маппинг endpoints

| v1 | v2 | Изменения |
|----|----|----|
| GET /api/v1/users | GET /api/v2/users | Пагинация |
| GET /api/v1/users/:id | GET /api/v2/users/:id | Формат ответа |
| POST /api/v1/users | POST /api/v2/users | Поля |

## Маппинг полей

| v1 | v2 | Тип изменения |
|----|----|----|
| `id` (int) | `id` (string) | Тип |
| `name` | `fullName` | Переименование |
| `middleName` | - | Удалено |
| - | `email` | Добавлено |
| - | `profile` | Добавлено |

## Примеры кода

**До (v1):**
```python
response = requests.get("/api/v1/users")
users = response.json()  # Прямой список
for user in users:
    print(user["id"])  # int
```

**После (v2):**
```python
response = requests.get("/api/v2/users")
data = response.json()
users = data["data"]  # Обёрнуто в data
pagination = data["pagination"]
for user in users:
    print(user["id"])  # string
```
```

---

## Чек-лист deprecation

### При объявлении deprecation

- [ ] Добавлен заголовок `Deprecation` в ответы
- [ ] Добавлен заголовок `Sunset` с датой отключения
- [ ] Добавлен заголовок `Link` на новую версию
- [ ] Добавлен заголовок `Link` на migration guide
- [ ] Создан migration guide
- [ ] Обновлена документация (changelog)
- [ ] Отправлено уведомление (email/slack)

### За 30 дней до sunset

- [ ] Отправлено напоминание
- [ ] Добавлен заголовок `Warning`
- [ ] Проверен список активных клиентов

### В день sunset

- [ ] Endpoint возвращает `410 Gone`
- [ ] Тело ответа содержит ссылку на migration guide
- [ ] Логирование обращений для анализа
- [ ] Уведомление о завершении deprecation

### После sunset

- [ ] Мониторинг 410 ответов
- [ ] Через 30 дней — полное удаление кода (опционально)

---

## FAQ

### Можно ли отложить sunset?

**Ответ:** Да, но только продлить. Объявленную дату можно отодвинуть, но нельзя приблизить. Новая дата должна быть объявлена за 30+ дней.

### Что если клиент не мигрировал?

**Ответ:** После sunset — `410 Gone`. Если критичный клиент — индивидуальная работа до sunset. После sunset — только новая версия.

### Как deprecate отдельное поле без новой версии?

**Ответ:**
1. Добавить новое поле с правильным именем
2. Старое поле продолжает работать
3. Документировать в `_meta.deprecated_fields`
4. Через N месяцев — удалить старое поле в следующей мажорной версии

### Нужно ли deprecation для internal API?

**Ответ:** Да, но сроки короче (3 месяца). Контролируем всех клиентов, можем координировать миграцию.

---

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Создание Migration Guide |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление документации при deprecation |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |
| [/issue-create](/.claude/skills/issue-create/SKILL.md) | Создание задачи на миграцию клиентов |

---

## Связанные инструкции

- [src/api/versioning.md](versioning.md) — версионирование API
- [src/api/design.md](design.md) — общие правила дизайна API
- [src/api/swagger.md](swagger.md) — документация API
