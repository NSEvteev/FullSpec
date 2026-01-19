---
type: standard
description: Документирование кода: ссылки на /doc/, комментарии, README
related:
  - doc/structure.md
---

# Документирование кода

Правила документирования исходного кода в `/src/`. Обеспечивает связь между кодом и документацией.

## Оглавление

- [Правила](#правила)
- [Примеры](#примеры)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Ссылка на инструкцию

**Правило:** При генерации любого файла в `/src/` добавлять ссылку на данную инструкцию:

```
Инструкция: /.claude/instructions/src/documentation.md
```

Это обеспечивает связь кода с правилами документирования.

### Связь src ↔ doc

**Правило:** При создании файла в `/src/{service}/{path}` — создать `/doc/src/{service}/{path}.md` и добавить ссылку в начало файла.

| Файл в /src/ | Документация в /doc/ |
|--------------|---------------------|
| `/src/auth/` | `/doc/src/auth/` |
| `/src/auth/backend/handlers.ts` | `/doc/src/auth/backend/handlers.md` |
| `/src/notification/database/schema.sql` | `/doc/src/notification/database/schema.md` |

### README.md сервиса

Каждый сервис содержит `README.md` со ссылкой на документацию:

```markdown
# {Service} Service

Документация: [/doc/src/{service}/](/doc/src/{service}/)
```

### Ссылки в коде

Файлы кода содержат ссылку на документацию в начале:

**Python:**
```python
"""
Auth handlers.

Документация: /doc/src/auth/backend/handlers.md
"""
```

**TypeScript/JavaScript:**
```typescript
/**
 * Auth handlers.
 *
 * Документация: /doc/src/auth/backend/handlers.md
 */
```

### Комментарии

- Комментировать **"почему"**, а не **"что"**
- Код должен быть самодокументируемым
- Сложная логика требует пояснения
- Использовать JSDoc/docstrings для публичных API

---

## Примеры

### Пример 1: README.md сервиса auth

**Файл:** `/src/auth/README.md`

```markdown
# Auth Service

Документация: [/doc/src/auth/](/doc/src/auth/)

## Быстрый старт

См. документацию для настройки и запуска.
```

### Пример 2: Файл с обработчиками

**Файл:** `/src/auth/backend/handlers.py`

```python
"""
Обработчики аутентификации.

Документация: /doc/src/auth/backend/handlers.md
"""

def login(request):
    """
    Аутентификация пользователя.

    Args:
        request: HTTP запрос с credentials

    Returns:
        JWT токен при успехе
    """
    # Проверяем rate limit перед валидацией
    # (защита от brute-force атак)
    check_rate_limit(request.ip)
    ...
```

### Пример 3: Комментарии — хорошо vs плохо

```python
# ❌ Плохо — описывает "что"
# Увеличиваем счётчик на 1
counter += 1

# ✅ Хорошо — объясняет "почему"
# Пропускаем первую строку CSV (заголовки)
counter += 1
```

---

## Связанные инструкции

- [doc/structure.md](../doc/structure.md) — структура документации, зеркалирование
