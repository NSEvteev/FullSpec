---
name: doc-create
description: Создание документации для нового файла в /src/
allowed-tools: Read, Write, Edit, Glob, Grep
category: documentation
triggers:
  commands:
    - /doc-create
  phrases:
    ru:
      - создай документацию
      - добавь документацию
      - задокументируй
    en:
      - create documentation
      - add documentation
      - document this
---

# Создание документации

Команда для автоматического создания документации при добавлении нового файла в `/src/`.

**Связанная инструкция:** [/.claude/instructions/src/documentation.md](/.claude/instructions/src/documentation.md)

**Связанные скиллы:**
- [doc-update](/.claude/skills/doc-update/SKILL.md) — обновление документации
- [doc-delete](/.claude/skills/doc-delete/SKILL.md) — пометка документации при удалении

## Оглавление

- [Формат вызова](#формат-вызова)
- [Что создаётся](#что-создаётся)
- [Воркфлоу](#воркфлоу)
- [Шаблон документации](#шаблон-документации)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/doc-create <путь-к-файлу-в-src>
```

**Примеры:**
- `/doc-create /src/auth/backend/handlers.ts`
- `/doc-create /src/notification/services/email.py`

---

## Что создаётся

| Действие | Результат |
|----------|-----------|
| Файл документации | `/doc/src/{service}/{path}.md` |
| Ссылка в исходном файле | Добавляется в начало файла |

**Маппинг путей:**

| Исходный файл | Документация |
|---------------|--------------|
| `/src/auth/backend/handlers.ts` | `/doc/src/auth/backend/handlers.md` |
| `/src/notification/services/email.py` | `/doc/src/notification/services/email.md` |

---

## Воркфлоу

### Шаг 1: Получить путь к файлу

1. Из аргумента: `/doc-create /src/auth/backend/handlers.ts`
2. Проверить, что файл существует
3. Проверить, что файл в `/src/`

### Шаг 2: Определить путь документации

Преобразовать путь:
```
/src/{service}/{path}.{ext} → /doc/src/{service}/{path}.md
```

### Шаг 3: Проверить существование

1. Если документация уже существует — спросить:
   ```
   ⚠️ Документация уже существует: /doc/src/auth/backend/handlers.md

   Варианты:
   1. Перезаписать
   2. Открыть для редактирования
   3. Отменить
   ```

### Шаг 4: Прочитать исходный файл

1. Определить язык по расширению
2. Извлечь:
   - Название модуля (из имени файла или первого класса/функции)
   - Публичные функции/классы
   - Импорты (зависимости)

### Шаг 5: Создать документацию

1. Создать папку если не существует
2. Создать файл по шаблону
3. Заполнить:
   - Название модуля
   - Ссылку на исходный код
   - Список API (функции/классы)

### Шаг 6: Добавить ссылку в исходный файл

Добавить в начало исходного файла ссылку на документацию:

**Python:**
```python
"""
{Описание модуля}

Документация: /doc/src/{service}/{path}.md
"""
```

**TypeScript/JavaScript:**
```typescript
/**
 * {Описание модуля}
 *
 * Документация: /doc/src/{service}/{path}.md
 */
```

### Шаг 7: Проверка по чек-листу

```
✅ Шаг 1: Получил путь к файлу
✅ Шаг 2: Определил путь документации
✅ Шаг 3: Проверил существование
✅ Шаг 4: Прочитал исходный файл
✅ Шаг 5: Создал документацию
✅ Шаг 6: Добавил ссылку в исходный файл
```

### Шаг 8: Результат

```
✅ Документация создана

Исходный файл: /src/auth/backend/handlers.ts
Документация: /doc/src/auth/backend/handlers.md

Добавлено:
- Файл документации с описанием API
- Ссылка на документацию в исходном файле

Следующие шаги:
- Заполнить описания функций в документации
- Добавить примеры использования
```

---

## Шаблон документации

```markdown
# {Название модуля}

> Исходный код: [{filename}](/{path-to-source})

{Краткое описание — заполнить вручную}

## API

### {FunctionName}

{Описание — заполнить вручную}

**Сигнатура:**
\`\`\`{language}
{signature}
\`\`\`

---

## Зависимости

- [{dependency}](/{path}) — {description}
```

---

## Чек-лист

- [ ] **Шаг 1:** Получил путь к файлу, проверил существование
- [ ] **Шаг 2:** Определил путь документации (`/doc/src/...`)
- [ ] **Шаг 3:** Проверил, что документация не существует (или получил подтверждение)
- [ ] **Шаг 4:** Прочитал исходный файл, извлёк API
- [ ] **Шаг 5:** Создал файл документации по шаблону
- [ ] **Шаг 6:** Добавил ссылку на документацию в исходный файл
- [ ] **Шаг 7:** Проверил выполнение всех пунктов
- [ ] **Шаг 8:** Вывел результат

---

## Примеры

### Пример 1: TypeScript файл

**Вызов:**
```
/doc-create /src/auth/backend/handlers.ts
```

**Создаётся `/doc/src/auth/backend/handlers.md`:**
```markdown
# Auth Handlers

> Исходный код: [handlers.ts](/src/auth/backend/handlers.ts)

Обработчики аутентификации.

## API

### login

Аутентификация пользователя.

**Сигнатура:**
\`\`\`typescript
async function login(request: LoginRequest): Promise<AuthResponse>
\`\`\`

### logout

Завершение сессии.

**Сигнатура:**
\`\`\`typescript
async function logout(token: string): Promise<void>
\`\`\`

---

## Зависимости

- [jwt.ts](/src/auth/utils/jwt.ts) — работа с JWT токенами
```

**Добавляется в `/src/auth/backend/handlers.ts`:**
```typescript
/**
 * Auth Handlers
 *
 * Документация: /doc/src/auth/backend/handlers.md
 */
```

### Пример 2: Python файл

**Вызов:**
```
/doc-create /src/notification/services/email.py
```

**Создаётся `/doc/src/notification/services/email.md`:**
```markdown
# Email Service

> Исходный код: [email.py](/src/notification/services/email.py)

Сервис отправки email уведомлений.

## API

### send_email

Отправка email.

**Сигнатура:**
\`\`\`python
def send_email(to: str, subject: str, body: str) -> bool
\`\`\`

---

## Зависимости

- [templates.py](/src/notification/templates/templates.py) — шаблоны писем
```

### Пример 3: Документация уже существует

**Вызов:**
```
/doc-create /src/auth/backend/handlers.ts
```

**Вывод:**
```
⚠️ Документация уже существует: /doc/src/auth/backend/handlers.md

Варианты:
[1] Перезаписать
[2] Открыть для редактирования
[3] Отменить

> 3

Операция отменена.
```
