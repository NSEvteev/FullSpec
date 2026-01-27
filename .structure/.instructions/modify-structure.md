---
description: Воркфлоу изменения папки — переименование, перемещение, удаление
standard: .instructions/standard-instruction.md
index: .structure/.instructions/README.md
---

# Воркфлоу изменения

Изменение существующей папки в структуре проекта: переименование, перемещение, удаление.

**Полезные ссылки:**
- [Инструкции для .structure](./README.md)
- [SSOT структуры проекта](../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-readme.md](./standard-readme.md), [standard-links.md](./standard-links.md), [standard-frontmatter.md](./standard-frontmatter.md) |
| Валидация | [validation-structure.md](./validation-structure.md), [validation-links.md](./validation-links.md) |
| Создание | [create-structure.md](./create-structure.md) |
| Модификация | Этот документ |

## Оглавление

- [Типы изменений](#типы-изменений)
- [Переименование](#переименование)
- [Перемещение](#перемещение)
- [Удаление](#удаление)
- [Обновление ссылок](#обновление-ссылок)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Типы изменений

| Тип | Описание | Пример |
|-----|----------|--------|
| Переименование | Изменение имени папки | `utils/` → `helpers/` |
| Перемещение | Изменение родителя | `src/utils/` → `shared/utils/` |
| Комбинированный | Переименование + перемещение | `src/utils/` → `shared/helpers/` |
| Удаление | Полное удаление папки | `legacy/` → ∅ |

---

## Переименование

### Шаг 1: Найти все ссылки

```bash
python .structure/.instructions/.scripts/find-references.py {old-name}/
```

Скрипт найдёт все ссылки в markdown-файлах и покажет файл, строку и контекст.

**Где искать (автоматически):**
- `/.structure/README.md` — SSOT структуры
- `CLAUDE.md` — точка входа
- `**/README.md` — README папок
- `.instructions/**` — инструкции
- `specs/**` — спецификации

### Шаг 2: Переименовать папку

```bash
mv old-name/ new-name/
```

### Шаг 3: Обновить SSOT

> **ПРАВИЛО:** ВСЕ папки должны быть в SSOT, включая подпапки. Используйте полный путь.

```bash
# Корневая папка
python .structure/.instructions/.scripts/ssot.py rename {старое_имя} {новое_имя} --description "Описание"

# Подпапка
python .structure/.instructions/.scripts/ssot.py rename {родитель}/{старое} {родитель}/{новое} --description "Описание"
```

Скрипт автоматически обновляет в `/.structure/README.md`:
- Секцию папки (название и ссылка)
- Оглавление (с учётом вложенности)
- Дерево папок (внутри родителя)

### Шаг 4: Обновить README папки

Обновить заголовок `# /path/new-name/ — ...`

### Шаг 5: Обновить README родительской папки

> **SSOT:** [standard-readme.md#52-обновление-readme-родительской-папки](./standard-readme.md#52-обновление-readme-родительской-папки)

В README родительской папки обновить:
- **Секция "Папки"** — название и ссылку на подпапку
- **Дерево** — название подпапки

### Шаг 6: Обновить ссылки вручную

Найти и заменить все вхождения `old-name/` на `new-name/` в markdown-файлах.

### Шаг 7: Валидация структуры

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

### Шаг 8: Валидация ссылок

```
/links-validate
```

---

## Перемещение

### Шаг 1: Найти все ссылки

Аналогично переименованию.

### Шаг 2: Переместить папку

```bash
mv src/utils/ shared/utils/
```

### Шаг 3: Обновить SSOT

> **ПРАВИЛО:** ВСЕ папки должны быть в SSOT, включая подпапки. Используйте полный путь.

```bash
# Удалить старый путь
python .structure/.instructions/.scripts/ssot.py delete {старый_путь}

# Добавить новый путь
python .structure/.instructions/.scripts/ssot.py add {новый_путь} --description "Описание"
```

> **После:** Замените `{EXTENDED_DESCRIPTION}` в новой секции.

### Шаг 4: Обновить README папки

Обновить:
- Заголовок с новым путём
- Блок "Полезные ссылки" (цепочка родителей изменилась)

### Шаг 5: Обновить frontmatter

> **SSOT:** [standard-frontmatter.md](./standard-frontmatter.md)

При перемещении относительные пути в frontmatter могут стать невалидными:

```yaml
---
standard: ../../.instructions/standard.md  # ← путь изменился
index: ../README.md                         # ← путь изменился
---
```

Проверить и обновить поля `standard` и `index` во всех `.md` файлах перемещённой папки.

### Шаг 6: Обновить README родительских папок

> **SSOT:** [standard-readme.md#52-обновление-readme-родительской-папки](./standard-readme.md#52-обновление-readme-родительской-папки)

**README старого родителя:**
- **Секция "Папки"** — удалить описание подпапки
- **Дерево** — удалить ветку подпапки

**README нового родителя:**
- **Секция "Папки"** — добавить описание подпапки
- **Дерево** — добавить ветку подпапки

### Шаг 7: Обновить README дочерних папок

Если есть подпапки — их "Полезные ссылки" тоже изменились.

### Шаг 8: Обновить ссылки вручную

Найти и заменить все вхождения `src/utils/` на `shared/utils/` в markdown-файлах.

### Шаг 9: Валидация структуры

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

### Шаг 10: Валидация ссылок

```
/links-validate
```

---

## Удаление

### Шаг 1: Проверить зависимости

Найти все ссылки на удаляемую папку:
- `/.structure/README.md` — SSOT
- `CLAUDE.md` — точка входа
- `**/README.md` — другие README
- `.instructions/**` — инструкции

### Шаг 2: Удалить из SSOT

> **ПРАВИЛО:** ВСЕ папки должны быть в SSOT, включая подпапки. Используйте полный путь.

```bash
# Корневая папка
python .structure/.instructions/.scripts/ssot.py delete {папка}

# Подпапка
python .structure/.instructions/.scripts/ssot.py delete {родитель}/{папка}
```

Скрипт автоматически удаляет из `/.structure/README.md`:
- Секцию папки
- Ссылку из оглавления
- Запись из дерева (с учётом вложенности)

### Шаг 3: Обновить README родительской папки

> **SSOT:** [standard-readme.md#52-обновление-readme-родительской-папки](./standard-readme.md#52-обновление-readme-родительской-папки)

В README родительской папки удалить:
- **Секция "Папки"** — описание удаляемой подпапки
- **Дерево** — ветку удаляемой подпапки

### Шаг 4: Обновить связанные документы

- `CLAUDE.md` — удалить упоминания
- Другие README — обновить или пометить битые ссылки

### Шаг 5: Пометить битые ссылки

Добавить комментарий `<!-- BROKEN: папка удалена -->` к ссылкам на удаляемую папку.

### Шаг 6: Удалить папку

**Только после обновления документов:**

```bash
rm -rf {папка}/
```

### Шаг 7: Валидация структуры

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

### Шаг 8: Валидация ссылок

```
/links-validate
```

---

## Обновление ссылок

Детальный воркфлоу обновления ссылок при изменении путей.

### При переименовании/перемещении файла

#### Шаг 1: Найти все ссылки на файл

```bash
grep -r "old-name.md" --include="*.md" .
```

**Где искать:**
- `**/*.md` — все markdown файлы
- `.yaml` файлы с frontmatter

#### Шаг 2: Выполнить изменение

```bash
mv old-path/old-name.md new-path/new-name.md
```

#### Шаг 3: Обновить ссылки вручную

Найти и заменить все вхождения пути в markdown-файлах.

#### Шаг 4: Обновить frontmatter

> **SSOT:** [standard-frontmatter.md](./standard-frontmatter.md)

Если файл перемещён — проверить и обновить относительные пути в полях `standard` и `index`.

#### Шаг 5: Проверить

```bash
grep -r "old-path/old-name.md" --include="*.md" .
```

### При удалении файла

#### Шаг 1: Найти все ссылки

```bash
grep -r "file-to-delete.md" --include="*.md" .
```

#### Шаг 2: Пометить битые ссылки

Добавить комментарий `<!-- BROKEN: файл удалён -->` к найденным ссылкам.

#### Шаг 3: Удалить файл

```bash
rm path/to/file.md
```

#### Шаг 4: Исправить битые ссылки

Вручную удалить или заменить помеченные ссылки.

### При изменении заголовка

#### Шаг 1: Найти якорные ссылки

```bash
grep -r "#old-heading" --include="*.md" .
```

#### Шаг 2: Изменить заголовок

```markdown
## Old Heading  →  ## New Heading
```

#### Шаг 3: Обновить якоря вручную

Найти и заменить все вхождения `#old-heading` на `#new-heading` в markdown-файлах.

---

## Чек-лист

### Переименование

- [ ] Найдены все ссылки
- [ ] Папка переименована
- [ ] SSOT обновлён (секция, оглавление, дерево)
- [ ] README папки обновлён
- [ ] README родительской папки обновлён
- [ ] Ссылки обновлены вручную
- [ ] Валидация структуры пройдена
- [ ] Валидация ссылок пройдена

### Перемещение

- [ ] Найдены все ссылки
- [ ] Папка перемещена
- [ ] SSOT обновлён (оба родителя, дерево)
- [ ] README папки обновлён (путь, "Полезные ссылки")
- [ ] Frontmatter обновлён (поля `standard`, `index`)
- [ ] README родительских папок обновлены (старый и новый)
- [ ] README дочерних папок обновлены
- [ ] Ссылки обновлены вручную
- [ ] Валидация структуры пройдена
- [ ] Валидация ссылок пройдена

### Удаление

- [ ] Найдены все зависимости
- [ ] Секция удалена из SSOT
- [ ] README родительской папки обновлён
- [ ] Связанные документы обновлены
- [ ] Битые ссылки помечены
- [ ] Папка удалена из файловой системы
- [ ] Валидация структуры пройдена
- [ ] Валидация ссылок пройдена

### Обновление ссылок (файлы)

- [ ] Найдены все ссылки на файл
- [ ] Файл переименован/перемещён/удалён
- [ ] Ссылки обновлены или помечены
- [ ] Frontmatter обновлён (при перемещении)
- [ ] Проверка пройдена
- [ ] Битые ссылки исправлены (при удалении)

### Изменение заголовка

- [ ] Найдены якорные ссылки
- [ ] Заголовок изменён
- [ ] Якоря обновлены
- [ ] Проверка пройдена

---

## Примеры

### Переименование: utils/ → helpers/

```bash
# Шаг 1: Найти ссылки
python .structure/.instructions/.scripts/find-references.py "utils/"

# Шаг 2: Переименовать папку
mv shared/utils/ shared/helpers/

# Шаг 3: Обновить SSOT
python .structure/.instructions/.scripts/ssot.py rename utils helpers --description "Хелперы"

# Шаг 4: Обновить README папки (заголовок)

# Шаг 5: Обновить README родительской папки (секция "Папки", дерево)

# Шаг 6: Обновить ссылки вручную
# Заменить shared/utils/ на shared/helpers/

# Шаг 7-8: Валидация
python .structure/.instructions/.scripts/validate-structure.py
/links-validate
```

### Перемещение: src/common/ → shared/libs/

**Шаг 2:** Перемещение
```bash
mv src/common/ shared/libs/
```

**Шаг 4:** Обновление README папки
```markdown
# /shared/libs/ — Общие библиотеки

**Полезные ссылки:**
- [shared/](../README.md)
- [Структура проекта](/.structure/README.md)
```

**Шаг 6:** Обновление README родительских папок:
- `src/README.md` — удалить описание `common/` из секции "Папки" и дерева
- `shared/README.md` — добавить описание `libs/` в секцию "Папки" и дерево

**Шаг 8:** Обновление ссылок вручную — найти и заменить `src/common/` на `shared/libs/`.

### Удаление: legacy/

```bash
# Шаг 1: Поиск зависимостей
python .structure/.instructions/.scripts/find-references.py "legacy/"

# Шаг 2: Удалить из SSOT
python .structure/.instructions/.scripts/ssot.py delete legacy

# Шаг 3: Обновить README родительской папки (секция "Папки", дерево)

# Шаг 4-5: Обновить документы, пометить битые ссылки
# <!-- BROKEN: папка удалена -->

# Шаг 6: Удалить папку
rm -rf legacy/

# Шаг 7-8: Валидация
python .structure/.instructions/.scripts/validate-structure.py
/links-validate
```

### Переименование файла: old-api.md → new-api.md

```bash
# 1. Поиск ссылок
grep -r "old-api.md" --include="*.md" .

# 2. Переименование
mv docs/old-api.md docs/new-api.md

# 3. Обновление ссылок вручную
# Заменить old-api.md на new-api.md во всех найденных файлах

# 4. Проверка
grep -r "old-api.md" --include="*.md" .
```

### Изменение заголовка

```bash
# 1. Поиск якорных ссылок
grep -r "#old-heading" --include="*.md" .

# 2. Изменение заголовка в файле
# ## Old Heading → ## New Heading

# 3. Обновление якорей вручную
# Заменить #old-heading на #new-heading во всех найденных файлах

# 4. Проверка
grep -r "#old-heading" --include="*.md" .
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [find-references.py](./.scripts/find-references.py) | Поиск ссылок на папку/файл | Этот документ |
| [ssot.py](./.scripts/ssot.py) | Управление SSOT (add/rename/delete) | [create-structure.md](./create-structure.md), Этот документ |
| [validate-structure.py](./.scripts/validate-structure.py) | Валидация структуры | [validation-structure.md](./validation-structure.md) |

**Использование:**
```bash
python .structure/.instructions/.scripts/find-references.py <паттерн>
python .structure/.instructions/.scripts/ssot.py rename <старый_путь> <новый_путь> --description "Описание"
python .structure/.instructions/.scripts/ssot.py delete <путь>
python .structure/.instructions/.scripts/validate-structure.py
```

**Примеры с вложенными путями:**
```bash
python .structure/.instructions/.scripts/ssot.py rename test/old test/new --description "Новое имя"
python .structure/.instructions/.scripts/ssot.py delete test/subtest
```

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/structure-modify](/.claude/skills/structure-modify/SKILL.md) | Изменение папки | Этот документ |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Валидация ссылок | [validation-links.md](./validation-links.md) |
