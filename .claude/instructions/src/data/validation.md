---
type: standard
description: Валидация входных данных — правила, форматы ошибок, JSON Schema
related:
  - src/data/errors.md
  - src/data/pagination.md
  - src/api/design.md
---

# Валидация данных

Стандарт валидации входных данных для API и внутренних сервисов.

## Принципы

1. **Fail fast** — валидация на входе, до бизнес-логики
2. **Полная информация** — все ошибки за один запрос, не по одной
3. **Машиночитаемость** — структурированные ошибки для UI
4. **Безопасность** — защита от инъекций и переполнений

## Формат ошибок валидации

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Ошибка валидации входных данных",
    "details": {
      "fields": {
        "email": {
          "code": "INVALID_FORMAT",
          "message": "Некорректный формат email"
        },
        "password": {
          "code": "TOO_SHORT",
          "message": "Минимальная длина — 8 символов",
          "params": {
            "min": 8,
            "actual": 5
          }
        },
        "age": {
          "code": "OUT_OF_RANGE",
          "message": "Значение должно быть от 18 до 120",
          "params": {
            "min": 18,
            "max": 120,
            "actual": 15
          }
        }
      }
    },
    "request_id": "req_abc123def456"
  }
}
```

## Коды ошибок полей

| Код | Описание | Параметры |
|-----|----------|-----------|
| `REQUIRED` | Поле обязательно | — |
| `INVALID_TYPE` | Неверный тип данных | `expected`, `actual` |
| `INVALID_FORMAT` | Неверный формат | `format` |
| `TOO_SHORT` | Слишком короткое значение | `min`, `actual` |
| `TOO_LONG` | Слишком длинное значение | `max`, `actual` |
| `OUT_OF_RANGE` | Значение вне диапазона | `min`, `max`, `actual` |
| `INVALID_ENUM` | Недопустимое значение | `allowed` |
| `PATTERN_MISMATCH` | Не соответствует паттерну | `pattern` |
| `ALREADY_EXISTS` | Значение уже существует | — |
| `NOT_FOUND` | Связанный ресурс не найден | `resource` |

## JSON Schema

### Определение схемы

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "email": {
      "type": "string",
      "format": "email",
      "maxLength": 255
    },
    "password": {
      "type": "string",
      "minLength": 8,
      "maxLength": 128
    },
    "age": {
      "type": "integer",
      "minimum": 18,
      "maximum": 120
    },
    "role": {
      "type": "string",
      "enum": ["admin", "user", "guest"]
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "maxItems": 10,
      "uniqueItems": true
    }
  },
  "required": ["email", "password"],
  "additionalProperties": false
}
```

### Вложенные объекты

```json
{
  "type": "object",
  "properties": {
    "address": {
      "type": "object",
      "properties": {
        "city": { "type": "string", "minLength": 1 },
        "street": { "type": "string", "minLength": 1 },
        "zip": { "type": "string", "pattern": "^\\d{6}$" }
      },
      "required": ["city", "street"]
    }
  }
}
```

### Ошибки вложенных объектов

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Ошибка валидации входных данных",
    "details": {
      "fields": {
        "address.city": {
          "code": "REQUIRED",
          "message": "Поле обязательно"
        },
        "address.zip": {
          "code": "PATTERN_MISMATCH",
          "message": "Почтовый индекс должен содержать 6 цифр",
          "params": {
            "pattern": "^\\d{6}$"
          }
        }
      }
    },
    "request_id": "req_7f3a9b2c"
  }
}
```

## Типы валидации

### Строки

| Правило | JSON Schema | Описание |
|---------|-------------|----------|
| Обязательность | `required` | Поле обязательно |
| Минимум | `minLength` | Минимальная длина |
| Максимум | `maxLength` | Максимальная длина |
| Паттерн | `pattern` | Регулярное выражение |
| Формат | `format` | email, uri, date, uuid |

### Числа

| Правило | JSON Schema | Описание |
|---------|-------------|----------|
| Минимум | `minimum` | Минимальное значение |
| Максимум | `maximum` | Максимальное значение |
| Эксклюзивный | `exclusiveMinimum` | Строго больше |
| Кратность | `multipleOf` | Кратно значению |

### Массивы

| Правило | JSON Schema | Описание |
|---------|-------------|----------|
| Мин. элементов | `minItems` | Минимум элементов |
| Макс. элементов | `maxItems` | Максимум элементов |
| Уникальность | `uniqueItems` | Уникальные элементы |
| Тип элементов | `items` | Схема элементов |

## Примеры валидации

### Регистрация пользователя

**Запрос:**
```json
{
  "email": "invalid-email",
  "password": "123",
  "username": "",
  "age": 15
}
```

**Ответ (400 Bad Request):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Ошибка валидации входных данных",
    "details": {
      "fields": {
        "email": {
          "code": "INVALID_FORMAT",
          "message": "Некорректный формат email"
        },
        "password": {
          "code": "TOO_SHORT",
          "message": "Минимальная длина — 8 символов",
          "params": { "min": 8, "actual": 3 }
        },
        "username": {
          "code": "TOO_SHORT",
          "message": "Поле не может быть пустым",
          "params": { "min": 1, "actual": 0 }
        },
        "age": {
          "code": "OUT_OF_RANGE",
          "message": "Возраст должен быть от 18 до 120",
          "params": { "min": 18, "max": 120, "actual": 15 }
        }
      }
    },
    "request_id": "req_8d4e1f6a"
  }
}
```

### Создание заказа

**Запрос:**
```json
{
  "items": [],
  "delivery": {
    "address": {
      "city": "Москва"
    }
  }
}
```

**Ответ (400 Bad Request):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Ошибка валидации входных данных",
    "details": {
      "fields": {
        "items": {
          "code": "TOO_SHORT",
          "message": "Заказ должен содержать хотя бы один товар",
          "params": { "min": 1, "actual": 0 }
        },
        "delivery.address.street": {
          "code": "REQUIRED",
          "message": "Укажите улицу доставки"
        }
      }
    },
    "request_id": "req_2c5b8a3d"
  }
}
```

## Уровни валидации

### 1. Синтаксическая (JSON Schema)

- Типы данных
- Форматы (email, uuid)
- Ограничения длины
- Обязательные поля

### 2. Семантическая (бизнес-логика)

- Существование связанных сущностей
- Уникальность значений
- Бизнес-правила

### 3. Контекстная (состояние)

- Права доступа
- Статус ресурса
- Временные ограничения

## Безопасность

### Санитизация

```python
# ❌ Опасно
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# ✅ Безопасно — параметризованный запрос
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, [user_input])
```

### Лимиты

| Параметр | Лимит | Причина |
|----------|-------|---------|
| Строка | 10 KB | Защита от DoS |
| Массив | 1000 элементов | Защита от DoS |
| Вложенность | 5 уровней | Защита от stack overflow |
| Размер JSON | 1 MB | Защита от DoS |

### Запрещённые символы

```json
{
  "patterns": {
    "no_html": "^[^<>]*$",
    "no_script": "^(?!.*<script).*$",
    "safe_path": "^[a-zA-Z0-9/_-]+$"
  }
}
```

## Антипаттерны

```json
// ❌ Неправильно: одна ошибка за раз
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некорректный email"
  }
}
// Пользователь исправит email, а потом узнает про password

// ✅ Правильно: все ошибки сразу
{
  "error": {
    "code": "VALIDATION_ERROR",
    "details": {
      "fields": {
        "email": { "code": "INVALID_FORMAT" },
        "password": { "code": "TOO_SHORT" }
      }
    }
  }
}

// ❌ Неправильно: плоский список ошибок
{
  "errors": ["email invalid", "password too short"]
}

// ❌ Неправильно: технические детали
{
  "error": {
    "message": "jsonschema.ValidationError: 'email' does not match"
  }
}
```

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование правил валидации |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление при изменении схем |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |

---

## Связанные инструкции

- [errors.md](errors.md) — Общий формат ошибок API
- [pagination.md](pagination.md) — Валидация параметров пагинации
- [src/api/design.md](../api/design.md) — Дизайн API
