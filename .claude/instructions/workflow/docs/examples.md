---
type: standard
description: Примеры работы с документацией — создание, обновление, удаление
governed-by: docs/README.md
related:
  - docs/workflow.md
  - docs/structure.md
  - docs/rules.md
---

# Примеры

Практические примеры работы с документацией.

## Оглавление

- [Создание документации](#создание-документации)
- [Обновление документации](#обновление-документации)
- [Удаление документации](#удаление-документации)
- [Переиндексация](#переиндексация)
- [Сложные сценарии](#сложные-сценарии)
- [Связанные инструкции](#связанные-инструкции)

---

## Создание документации

### Пример 1: Документирование backend-файла

**Задача:** Создать документацию для `/src/auth/backend/handlers.ts`.

**Через скилл:**
```
/docs-create /src/auth/backend/handlers.ts
```

**Диалог:**
```
📋 Создание документации

Исходный файл: /src/auth/backend/handlers.ts
Тип файла: TypeScript (backend)
Шаблон: backend-template.md

Анализирую исходный файл...
Найдено: 5 экспортируемых функций

Создать документацию? [Y/n]
> Y

Создаю директорию /doc/src/auth/backend/...
Записываю /doc/src/auth/backend/handlers.md...
Добавляю ссылку в исходный файл...
Обновляю связи...

✅ Документация создана

Файл: /doc/src/auth/backend/handlers.md
Ссылка добавлена в: /src/auth/backend/handlers.ts
```

---

### Пример 2: Dry-run перед созданием

**Задача:** Посмотреть, что будет создано.

```
/docs-create /src/auth/2fa.ts --dry-run
```

**Диалог:**
```
📋 Предварительный просмотр (--dry-run)

Исходный файл: /src/auth/2fa.ts
Документация: /doc/src/auth/2fa.md
Шаблон: backend-template.md

API (будет задокументировано):
- generateTOTP()
- validateTOTP()
- generateBackupCodes()

Будет создано:
───────────────────────────────────────
# Two-Factor Authentication

> Исходный код: [2fa.ts](/src/auth/2fa.ts)

Модуль двухфакторной аутентификации.

## API

### generateTOTP

Генерация TOTP секрета для пользователя.

**Сигнатура:**
```typescript
export function generateTOTP(userId: string): Promise<TOTPSecret>
```

...
───────────────────────────────────────

ℹ️ Изменения НЕ применены (--dry-run)

Для создания: /docs-create /src/auth/2fa.ts
```

---

### Пример 3: Без добавления ссылки

**Задача:** Создать документацию, но не менять исходный файл.

```
/docs-create /src/legacy/old-module.js --no-link
```

**Результат:**
```
✅ Документация создана

Файл: /doc/src/legacy/old-module.md
Ссылка НЕ добавлена (--no-link)
```

---

## Обновление документации

### Пример 4: Обновление после изменения API

**Задача:** Обновить документацию после добавления функции.

```
/docs-update /src/auth/handlers.ts
```

**Диалог:**
```
📋 Обновление документации

Исходный файл: /src/auth/handlers.ts
Документация: /doc/src/auth/handlers.md

Анализирую изменения...

Обнаружены изменения:
+ Добавлена функция: logout()
~ Изменена сигнатура: login() (добавлен параметр rememberMe)

Показать diff? [Y/n/применить]
> Y

@@ -25,6 +25,10 @@ API
 ### login

-**Сигнатура:**
-```typescript
-export function login(credentials: Credentials): Promise<Token>
+**Сигнатура:**
+```typescript
+export function login(credentials: Credentials, rememberMe?: boolean): Promise<Token>

+### logout
+
+Выход из системы с инвалидацией токена.
+
+**Сигнатура:**
+```typescript
+export function logout(token: string): Promise<void>

Применить изменения? [Y/n]
> Y

✅ Документация обновлена

Изменения:
- Обновлена сигнатура login()
- Добавлена функция logout()
```

---

### Пример 5: Автоматическое обновление всех файлов

**Задача:** Обновить документацию для всех изменённых файлов.

```
/docs-update --auto
```

**Диалог:**
```
📋 Автоматическое обновление документации

Поиск изменённых файлов в /src/...

Найдено: 3 файла с изменениями

1. /src/auth/handlers.ts → /doc/src/auth/handlers.md
   + logout()
   ~ login() сигнатура

2. /src/notify/email.ts → /doc/src/notify/email.md
   + sendBulk()

3. /src/users/profile.ts → /doc/src/users/profile.md
   - deleteAvatar() (удалена)

Применяю изменения...

✅ Обновлено: 3 файла

Отчёт:
- /doc/src/auth/handlers.md ✅
- /doc/src/notify/email.md ✅
- /doc/src/users/profile.md ✅
```

---

### Пример 6: Только показать изменения

**Задача:** Посмотреть, что изменилось, без применения.

```
/docs-update /src/auth/handlers.ts --diff
```

**Результат:** Показывает diff без запроса на применение.

---

## Удаление документации

### Пример 7: Стандартное удаление

**Задача:** Обработать удаление файла `/src/auth/old-handlers.ts`.

```
/docs-delete /src/auth/old-handlers.ts
```

**Диалог:**
```
📋 Удаление документации

Удалённый файл: /src/auth/old-handlers.ts
Документация: /doc/src/auth/old-handlers.md

Действия:
1. Добавить пометку о требовании ревью
2. Создать GitHub Issue
3. Обновить ссылки

Выполнить? [Y/n]
> Y

Добавляю пометку в документацию...
Создаю Issue...
Обновляю ссылки...

✅ Документация помечена для ревью

Issue: #145 [DOCS] Ревью документации old-handlers.md
URL: https://github.com/user/repo/issues/145
```

---

### Пример 8: Удаление без Issue

**Задача:** Быстро пометить документацию без создания Issue.

```
/docs-delete /src/auth/temp.ts --no-issue
```

**Результат:**
```
✅ Документация помечена для ревью

Файл: /doc/src/auth/temp.md
Issue: НЕ создан (--no-issue)
```

---

### Пример 9: Полное удаление

**Задача:** Сразу удалить документацию (без пометки).

```
/docs-delete /src/auth/deprecated.ts --remove
```

**Диалог:**
```
⚠️ Внимание: файл будет удалён безвозвратно

Файл: /doc/src/auth/deprecated.md

Удалить? [y/N]
> y

Удаляю файл...
Обновляю ссылки...

✅ Документация удалена

Удалён: /doc/src/auth/deprecated.md
```

---

## Переиндексация

### Пример 10: Проверка синхронизации

**Задача:** Проверить, все ли файлы задокументированы.

```
/docs-reindex --check
```

**Результат:**
```
📋 Проверка документации

Сканирую /src/...
Сканирую /doc/src/...

═══════════════════════════════════════
📊 ОТЧЁТ
═══════════════════════════════════════

✅ Синхронизировано: 42 файла

⚠️ Проблемы: 4

Missing (нет документации):
├── /src/auth/2fa.ts
└── /src/notify/sms.ts

Orphan (нет исходного файла):
├── /doc/src/auth/old-handlers.md
└── /doc/src/pay/deprecated.md

═══════════════════════════════════════

Для исправления: /docs-reindex --fix
```

---

### Пример 11: Автоматическое исправление

**Задача:** Исправить все проблемы синхронизации.

```
/docs-reindex --fix
```

**Диалог:**
```
📋 Исправление документации

Missing (создаю документацию):
├── /src/auth/2fa.ts
│   Создаю /doc/src/auth/2fa.md...
│   ✅ Создано
└── /src/notify/sms.ts
    Создаю /doc/src/notify/sms.md...
    ✅ Создано

Orphan (помечаю для ревью):
├── /doc/src/auth/old-handlers.md
│   Добавляю пометку...
│   Создаю Issue #146...
│   ✅ Помечено
└── /doc/src/pay/deprecated.md
    Добавляю пометку...
    Создаю Issue #147...
    ✅ Помечено

═══════════════════════════════════════
📊 ИТОГ
═══════════════════════════════════════

Создано: 2 файла
Помечено: 2 файла
Issues: #146, #147

✅ Синхронизация завершена
```

---

### Пример 12: JSON вывод

**Задача:** Получить отчёт в машиночитаемом формате.

```
/docs-reindex --check --json
```

**Результат:**
```json
{
  "synced": 42,
  "problems": {
    "missing": [
      "/src/auth/2fa.ts",
      "/src/notify/sms.ts"
    ],
    "orphan": [
      "/doc/src/auth/old-handlers.md",
      "/doc/src/pay/deprecated.md"
    ],
    "outdated": []
  }
}
```

---

## Сложные сценарии

### Пример 13: Документирование нового сервиса

**Задача:** Создать документацию для всех файлов нового сервиса.

```bash
# 1. Проверить структуру
ls /src/newservice/

# 2. Запустить переиндексацию с фиксом
/docs-reindex --fix
```

**Или последовательно:**
```
/docs-create /src/newservice/backend/handlers.ts
/docs-create /src/newservice/backend/services.ts
/docs-create /src/newservice/database/schema.sql
```

---

### Пример 14: Рефакторинг с переносом файлов

**Задача:** Перенести файл `/src/auth/handlers.ts` → `/src/auth/v2/handlers.ts`.

```bash
# 1. Переименовать исходный файл
git mv /src/auth/handlers.ts /src/auth/v2/handlers.ts

# 2. Обработать удаление старого
/docs-delete /src/auth/handlers.ts --no-issue

# 3. Создать документацию для нового
/docs-create /src/auth/v2/handlers.ts

# 4. Удалить старую документацию (после проверки)
rm /doc/src/auth/handlers.md
```

---

### Пример 15: Массовое обновление после крупного рефакторинга

**Задача:** Обновить документацию после большого PR.

```
# 1. Проверить масштаб изменений
/docs-reindex --check

# 2. Автоматически обновить всё
/docs-update --auto

# 3. Проверить результат
/docs-reindex --check
```

---

## Связанные инструкции

- [workflow.md](./workflow.md) — детальные воркфлоу
- [structure.md](./structure.md) — структура /doc/
- [rules.md](./rules.md) — правила документации
- [errors.md](./errors.md) — обработка ошибок

---

> **Путь:** `/.claude/instructions/docs/examples.md`
