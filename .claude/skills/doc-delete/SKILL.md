---
name: doc-delete
description: Пометка документации при удалении файла из /src/
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
category: documentation
triggers:
  commands:
    - /doc-delete
  phrases:
    ru:
      - удали документацию
      - пометь документацию
      - документация устарела
    en:
      - delete documentation
      - mark documentation
      - docs outdated
---

# Удаление документации

Команда для пометки документации при удалении файла из `/src/`. Создаёт GitHub Issue для отслеживания.

**Связанные инструкции:**
- [/.claude/instructions/src/documentation.md](/.claude/instructions/src/documentation.md)
- [/.claude/instructions/git/issues.md](/.claude/instructions/git/issues.md)

**Связанные скиллы:**
- [doc-create](/.claude/skills/doc-create/SKILL.md) — создание документации
- [doc-update](/.claude/skills/doc-update/SKILL.md) — обновление документации
- [issue-create](/.claude/skills/issue-create/SKILL.md) — создание GitHub Issue

## Оглавление

- [Формат вызова](#формат-вызова)
- [Когда использовать](#когда-использовать)
- [Воркфлоу](#воркфлоу)
- [Формат пометки](#формат-пометки)
- [GitHub Issue](#github-issue)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/doc-delete <путь-к-удалённому-файлу> [--no-issue] [--dry-run]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь` | Удалённый файл из /src/ | — (обязательный) |
| `--no-issue` | Не создавать GitHub Issue | false |
| `--dry-run` | Показать изменения без применения | false |

**Примеры:**
- `/doc-delete /src/auth/backend/old-handlers.ts`
- `/doc-delete /src/legacy/module.py --no-issue`

---

## Когда использовать

| Событие | Действие |
|---------|----------|
| Удалён файл из `/src/` | Пометить документацию, создать Issue |
| Удалена папка из `/src/` | Пометить все документы в папке |
| Рефакторинг (файл перемещён) | `/doc-delete` + `/doc-create` |

---

## Воркфлоу

### Шаг 1: Получить путь

1. Из аргумента: `/doc-delete /src/auth/backend/old-handlers.ts`
2. Определить путь документации: `/doc/src/auth/backend/old-handlers.md`

### Шаг 2: Проверить документацию

1. Если документация не существует:
   ```
   ℹ️ Документация не найдена: /doc/src/auth/backend/old-handlers.md

   Файл уже удалён или не был задокументирован.
   Создание Issue не требуется.
   ```

### Шаг 3: Пометить документацию

Добавить в начало файла документации:

```markdown
> ⚠️ **ТРЕБУЕТ РЕВЬЮ:** Исходный файл `/src/auth/backend/old-handlers.ts` был удалён.
>
> - [ ] Удалить этот файл документации
> - [ ] Или обновить ссылку на новый файл
>
> См. Issue: #{issue-number}
```

### Шаг 4: Найти ссылки на документацию

Найти все ссылки на помечаемую документацию:

```
📋 Ссылки на /doc/src/auth/backend/old-handlers.md

Найдено: 3

1. /doc/src/auth/README.md:45
2. /.claude/instructions/src/README.md:23
3. /doc/src/auth/backend/api.md:12
```

### Шаг 5: Создать GitHub Issue

**Если не указан `--no-issue`:**

```bash
gh issue create \
  --label "docs" \
  --title "[DOCS] Ревью документации после удаления old-handlers.ts" \
  --body "## Описание

Файл \`/src/auth/backend/old-handlers.ts\` был удалён.
Документация \`/doc/src/auth/backend/old-handlers.md\` требует ревью.

## Действия

- [ ] Удалить или обновить документацию
- [ ] Обновить ссылки в связанных документах:
  - /doc/src/auth/README.md:45
  - /.claude/instructions/src/README.md:23
  - /doc/src/auth/backend/api.md:12

## Связанные файлы

- Удалённый файл: \`/src/auth/backend/old-handlers.ts\`
- Документация: \`/doc/src/auth/backend/old-handlers.md\`"
```

### Шаг 6: Вызвать links-delete

Пометить ссылки на удалённый исходный файл:

```
/links-delete /src/auth/backend/old-handlers.ts
```

### Шаг 7: Проверка по чек-листу

```
✅ Шаг 1: Получил путь
✅ Шаг 2: Проверил документацию
✅ Шаг 3: Пометил документацию
✅ Шаг 4: Нашёл ссылки
✅ Шаг 5: Создал GitHub Issue
✅ Шаг 6: Вызвал links-delete
```

### Шаг 8: Результат

```
✅ Документация помечена для ревью

Удалённый файл: /src/auth/backend/old-handlers.ts
Документация: /doc/src/auth/backend/old-handlers.md

Выполнено:
- Добавлена пометка в документацию
- Создан GitHub Issue #123
- Помечено ссылок: 3

GitHub Issue: https://github.com/user/repo/issues/123

Следующие шаги:
- Решить судьбу документации (удалить или обновить)
- Обновить или удалить ссылки
```

---

## Формат пометки

### Стандартная пометка

```markdown
> ⚠️ **ТРЕБУЕТ РЕВЬЮ:** Исходный файл `{путь}` был удалён.
>
> - [ ] Удалить этот файл документации
> - [ ] Или обновить ссылку на новый файл
>
> См. Issue: #{issue-number}
```

### Пометка без Issue

```markdown
> ⚠️ **ТРЕБУЕТ РЕВЬЮ:** Исходный файл `{путь}` был удалён.
>
> - [ ] Удалить этот файл документации
> - [ ] Или обновить ссылку на новый файл
```

---

## GitHub Issue

### Формат заголовка

```
[DOCS] Ревью документации после удаления {filename}
```

### Метки

- `docs` — документация

### Тело Issue

```markdown
## Описание

Файл `{исходный-путь}` был удалён.
Документация `{путь-документации}` требует ревью.

## Действия

- [ ] Удалить или обновить документацию
- [ ] Обновить ссылки в связанных документах:
  {список-ссылок}

## Связанные файлы

- Удалённый файл: `{исходный-путь}`
- Документация: `{путь-документации}`
```

---

## Чек-лист

- [ ] **Шаг 1:** Получил путь к удалённому файлу
- [ ] **Шаг 2:** Проверил существование документации
- [ ] **Шаг 3:** Добавил пометку в документацию
- [ ] **Шаг 4:** Нашёл все ссылки на документацию
- [ ] **Шаг 5:** Создал GitHub Issue (если не `--no-issue`)
- [ ] **Шаг 6:** Вызвал `/links-delete` для исходного файла
- [ ] **Шаг 7:** Проверил выполнение всех пунктов
- [ ] **Шаг 8:** Вывел результат

---

## Примеры

### Пример 1: Стандартное удаление

**Контекст:** Удалён файл `/src/auth/backend/old-handlers.ts`.

**Вызов:**
```
/doc-delete /src/auth/backend/old-handlers.ts
```

**Вывод:**
```
📋 Пометка документации

Удалённый файл: /src/auth/backend/old-handlers.ts
Документация: /doc/src/auth/backend/old-handlers.md

Найдено ссылок на документацию: 2

Создать GitHub Issue? [Y/n]
> Y

✅ Документация помечена для ревью

- Добавлена пометка в документацию
- Создан GitHub Issue #45
- Вызван /links-delete

Issue: https://github.com/user/repo/issues/45
```

### Пример 2: Без создания Issue

**Вызов:**
```
/doc-delete /src/legacy/old-module.py --no-issue
```

**Вывод:**
```
✅ Документация помечена для ревью

Удалённый файл: /src/legacy/old-module.py
Документация: /doc/src/legacy/old-module.md

- Добавлена пометка (без Issue)
- Вызван /links-delete
```

### Пример 3: Документация не существует

**Вызов:**
```
/doc-delete /src/auth/backend/undocumented.ts
```

**Вывод:**
```
ℹ️ Документация не найдена

Файл /doc/src/auth/backend/undocumented.md не существует.
Файл не был задокументирован — пометка не требуется.

Вызов /links-delete для исходного файла...
```

### Пример 4: Предпросмотр (--dry-run)

**Вызов:**
```
/doc-delete /src/auth/backend/handlers.ts --dry-run
```

**Вывод:**
```
📋 Предпросмотр пометки (--dry-run)

Документация: /doc/src/auth/backend/handlers.md

Будет добавлено:
```markdown
> ⚠️ **ТРЕБУЕТ РЕВЬЮ:** Исходный файл `/src/auth/backend/handlers.ts` был удалён.
```

Будет создан Issue:
- Заголовок: [DOCS] Ревью документации после удаления handlers.ts
- Метки: docs

Ссылки для пометки: 3

Изменения НЕ применены (--dry-run)
```

### Пример 5: Удаление папки

**Вызов:**
```
/doc-delete /src/legacy/
```

**Вывод:**
```
📋 Пометка документации для папки

Удалённая папка: /src/legacy/
Документация: /doc/src/legacy/

Найдено файлов документации: 5
- /doc/src/legacy/README.md
- /doc/src/legacy/old-api.md
- /doc/src/legacy/helpers.md
- /doc/src/legacy/utils.md
- /doc/src/legacy/constants.md

Пометить все? [Y/n]
> Y

✅ Помечено файлов: 5
Создан GitHub Issue #67
```
