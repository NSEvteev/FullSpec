---
description: Воркфлоу изменения структуры папок — переименование, перемещение, удаление с обновлением ссылок и SSOT.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .structure/.instructions/README.md
---

# Воркфлоу изменения

Рабочая версия стандарта: 1.1

Изменение существующей папки в структуре проекта: обновление, деактивация, миграция.

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
- [Обновление](#обновление)
- [Миграция](#миграция)
  - [Переименование](#переименование)
  - [Перемещение](#перемещение)
- [Деактивация](#деактивация)
- [Обновление ссылок](#обновление-ссылок)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Шаблоны — из примеров SSOT.** При изменении файлов использовать шаблоны из секции "Примеры". Запрещено придумывать свой формат.

---

## Типы изменений

| Тип | Описание | Пример |
|-----|----------|--------|
| Обновление | Изменение README/содержимого | Добавить описание файла |
| Миграция | Переименование или перемещение | `utils/` → `helpers/`, `src/utils/` → `shared/utils/` |
| Деактивация | Удаление папки из структуры | `legacy/` → ∅ |

---

## Обновление

Изменение содержимого папки или её README без изменения пути.

### Шаг 1: Определить что обновляется

| Изменение | Что обновить |
|-----------|--------------|
| Добавление файла | README папки (секция "Файлы", дерево) |
| Удаление файла | README папки (секция "Файлы", дерево) |
| Добавление подпапки | README папки (секция "Папки", дерево) + SSOT |
| Изменение описания | README папки, SSOT (комментарий в дереве) |

### Шаг 2: Обновить README папки

> **SSOT:** [standard-readme.md](./standard-readme.md)

Обновить соответствующие секции README:
- **Секция "Папки"** или **"Файлы"** — добавить/удалить/обновить описание
- **Дерево** — добавить/удалить/обновить запись

### Шаг 3: Обновить SSOT (при необходимости)

Если изменилось описание папки:
```bash
# Обновить комментарий в дереве SSOT
# Вручную редактировать /.structure/README.md
```

### Шаг 4: Валидация

```bash
python .structure/.instructions/.scripts/validate.py --path {путь}
```

---

## Миграция

Переименование или перемещение папки. Включает два сценария: переименование и перемещение.

### Переименование

#### Шаг 1: Найти все ссылки

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

#### Шаг 2: Переименовать папку

```bash
mv old-name/ new-name/
```

#### Шаг 3: Обновить SSOT

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

#### Шаг 4: Обновить README папки

Обновить заголовок `# /path/new-name/ — ...`

#### Шаг 5: Обновить README родительской папки

> **SSOT:** [standard-readme.md#52-обновление-readme-родительской-папки](./standard-readme.md#52-обновление-readme-родительской-папки)

В README родительской папки обновить:
- **Секция "Папки"** — название и ссылку на подпапку
- **Дерево** — название подпапки

#### Шаг 6: Обновить ссылки вручную

Найти и заменить все вхождения `old-name/` на `new-name/` в markdown-файлах.

#### Шаг 7: Переименовать зеркало `.instructions`

> **ПРАВИЛО:** При переименовании папки — переименовать зеркало в `.instructions`.

```bash
python .structure/.instructions/.scripts/mirror-instructions.py rename {старый_путь} {новый_путь}
```

Скрипт автоматически:
- Переименовывает папку в `.instructions`
- Обновляет README внутри

#### Шаг 7.1: Обновить родительский README `.instructions`

> **Если переименованная папка является подпапкой `.instructions/`:**

В README родительской папки инструкций обновить:
- **Секция "Вложенные области"** — название и ссылку на подпапку

#### Шаг 8: Обновить ссылки в скиллах

> **ПРАВИЛО:** Скиллы ссылаются на инструкции через `SSOT:`. При переименовании инструкции — обновить ссылки в скиллах.

```bash
python .structure/.instructions/.scripts/update-skill-refs.py {старый_путь} {новый_путь}
```

Скрипт автоматически:
- Находит все скиллы с `SSOT:` ссылкой на старый путь
- Обновляет путь на новый

**Вручную (если нужно):**
1. Найти скиллы: `grep -r "старый_путь" .claude/skills/`
2. Обновить поле `SSOT:` в SKILL.md

#### Шаг 9: Валидация структуры

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

#### Шаг 10: Валидация ссылок

```
/links-validate
```

---

### Перемещение

#### Шаг 1: Найти все ссылки

Аналогично переименованию.

#### Шаг 2: Переместить папку

```bash
mv src/utils/ shared/utils/
```

#### Шаг 3: Обновить SSOT

> **ПРАВИЛО:** ВСЕ папки должны быть в SSOT, включая подпапки. Используйте полный путь.

```bash
# Удалить старый путь
python .structure/.instructions/.scripts/ssot.py delete {старый_путь}

# Добавить новый путь
python .structure/.instructions/.scripts/ssot.py add {новый_путь} --description "Описание"
```

> **После:** Замените `{EXTENDED_DESCRIPTION}` в новой секции.

#### Шаг 4: Обновить README папки

Обновить:
- Заголовок с новым путём
- Блок "Полезные ссылки" (цепочка родителей изменилась)

#### Шаг 5: Обновить frontmatter

> **SSOT:** [standard-frontmatter.md](./standard-frontmatter.md)

При перемещении относительные пути в frontmatter могут стать невалидными:

```yaml
---
standard: ../../.instructions/standard.md  # ← путь изменился
index: ../README.md                         # ← путь изменился
---
```

Проверить и обновить поля `standard` и `index` во всех `.md` файлах перемещённой папки.

#### Шаг 6: Обновить README родительских папок

> **SSOT:** [standard-readme.md#52-обновление-readme-родительской-папки](./standard-readme.md#52-обновление-readme-родительской-папки)

**README старого родителя:**
- **Секция "Папки"** — удалить описание подпапки
- **Дерево** — удалить ветку подпапки

**README нового родителя:**
- **Секция "Папки"** — добавить описание подпапки
- **Дерево** — добавить ветку подпапки

#### Шаг 7: Обновить README дочерних папок

Если есть подпапки — их "Полезные ссылки" тоже изменились.

#### Шаг 8: Обновить ссылки вручную

Найти и заменить все вхождения `src/utils/` на `shared/utils/` в markdown-файлах.

#### Шаг 9: Переместить зеркало `.instructions`

> **ПРАВИЛО:** При перемещении папки — переместить зеркало в `.instructions`.

```bash
python .structure/.instructions/.scripts/mirror-instructions.py move {старый_путь} {новый_путь}
```

Скрипт автоматически:
- Перемещает папку из `{старый_корень}/.instructions/` в `{новый_корень}/.instructions/`
- Обновляет ссылки в README

#### Шаг 10: Обновить ссылки в скиллах

> **ПРАВИЛО:** Скиллы ссылаются на инструкции через `SSOT:`. При перемещении инструкции — обновить ссылки в скиллах.

```bash
python .structure/.instructions/.scripts/update-skill-refs.py {старый_путь} {новый_путь}
```

См. [Шаг 8 в Переименовании](#шаг-8-обновить-ссылки-в-скиллах).

#### Шаг 11: Валидация структуры

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

#### Шаг 12: Валидация ссылок

```
/links-validate
```

---

## Деактивация

> **ВАЖНО:** Папка инструкций НЕ УДАЛЯЕТСЯ, а помечается префиксом `DELETE_`. Инструкции содержат знания, которые могут понадобиться позже.

### Шаг 1: Проверить зависимости

Найти все ссылки на удаляемую папку:
- `/.structure/README.md` — SSOT
- `CLAUDE.md` — точка входа
- `**/README.md` — другие README
- `.instructions/**` — инструкции

### Шаг 2: Пометить зеркало `.instructions` как удалённое

> **ПРАВИЛО:** Инструкции НЕ удаляются, а помечаются `DELETE_`.

```bash
python .structure/.instructions/.scripts/mark-deleted.py {путь}
```

Скрипт автоматически:
1. Переименовывает папку: `{корень}/.instructions/{папка}/` → `{корень}/.instructions/DELETE_{папка}/`
2. Переименовывает файлы внутри: `*.md` → `DELETE_*.md`
3. Находит связанные скиллы и переименовывает: `/.claude/skills/{skill}/` → `/.claude/skills/DELETE_{skill}/`

**Пример:**
```
docs/.instructions/api/           → docs/.instructions/DELETE_api/
docs/.instructions/api/README.md  → docs/.instructions/DELETE_api/DELETE_README.md
.claude/skills/docs-api-create/   → .claude/skills/DELETE_docs-api-create/
```

### Шаг 2.1: Обновить родительский README `.instructions`

> **Если удаляемая папка является подпапкой `.instructions/`:**

В README родительской папки инструкций:
- **Секция "Вложенные области"** — удалить строку из таблицы
- Если это была последняя подпапка — удалить секцию "Вложенные области"

### Шаг 3: Удалить из SSOT

```bash
python .structure/.instructions/.scripts/ssot.py delete {путь}
```

Скрипт автоматически удаляет из `/.structure/README.md`:
- Секцию папки
- Ссылку из оглавления
- Запись из дерева

### Шаг 4: Обновить README родительской папки

> **SSOT:** [standard-readme.md#52-обновление-readme-родительской-папки](./standard-readme.md#52-обновление-readme-родительской-папки)

В README родительской папки удалить:
- **Секция "Папки"** — описание удаляемой подпапки
- **Дерево** — ветку удаляемой подпапки

### Шаг 5: Обновить связанные документы

- `CLAUDE.md` — удалить упоминания
- Другие README — обновить или пометить битые ссылки

### Шаг 6: Пометить битые ссылки

Добавить комментарий `<!-- BROKEN: папка удалена -->` к ссылкам на удаляемую папку.

### Шаг 7: Удалить папку

**Только после пометки инструкций и обновления документов:**

```bash
rm -rf {папка}/
```

### Шаг 8: Валидация структуры

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

### Шаг 9: Валидация ссылок

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
- [ ] Зеркало `.instructions` переименовано (mirror-instructions.py rename)
- [ ] Родительский README `.instructions` обновлён (секция "Вложенные области")
- [ ] Ссылки в скиллах обновлены (update-skill-refs.py)
- [ ] Валидация пройдена

### Перемещение

- [ ] Найдены все ссылки
- [ ] Папка перемещена
- [ ] SSOT обновлён (оба родителя, дерево)
- [ ] README папки обновлён (путь, "Полезные ссылки")
- [ ] Frontmatter обновлён (поля `standard`, `index`)
- [ ] README родительских папок обновлены (старый и новый)
- [ ] README дочерних папок обновлены
- [ ] Ссылки обновлены вручную
- [ ] Зеркало `.instructions` перемещено (mirror-instructions.py move)
- [ ] Ссылки в скиллах обновлены (update-skill-refs.py)
- [ ] Валидация пройдена

### Удаление

- [ ] Найдены все зависимости
- [ ] Зеркало `.instructions` помечено DELETE_ (mark-deleted.py)
- [ ] Родительский README `.instructions` обновлён (секция "Вложенные области")
- [ ] Связанные скиллы помечены DELETE_
- [ ] Секция удалена из SSOT
- [ ] README родительской папки обновлён
- [ ] Связанные документы обновлены
- [ ] Битые ссылки помечены
- [ ] Папка удалена из файловой системы
- [ ] Валидация пройдена

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

### Переименование: shared/utils/ → shared/helpers/

```bash
# Шаг 1: Найти ссылки
python .structure/.instructions/.scripts/find-references.py "shared/utils/"

# Шаг 2: Переименовать папку
mv shared/utils/ shared/helpers/

# Шаг 3: Обновить SSOT
python .structure/.instructions/.scripts/ssot.py rename shared/utils shared/helpers --description "Хелперы"

# Шаг 4: Обновить README папки (заголовок)

# Шаг 5: Обновить README родительской папки (секция "Папки", дерево)

# Шаг 6: Обновить ссылки вручную
# Заменить shared/utils/ на shared/helpers/

# Шаг 7: Переименовать зеркало .instructions
python .structure/.instructions/.scripts/mirror-instructions.py rename shared/utils shared/helpers

# Шаг 8: Обновить ссылки в скиллах
python .structure/.instructions/.scripts/update-skill-refs.py shared/utils shared/helpers

# Шаг 9-10: Валидация
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

**Шаг 9:** Перемещение зеркала `.instructions`:
```bash
python .structure/.instructions/.scripts/mirror-instructions.py move src/common shared/libs
# Переместит: src/.instructions/common/ → shared/.instructions/libs/
```

**Шаг 10:** Обновление ссылок в скиллах:
```bash
python .structure/.instructions/.scripts/update-skill-refs.py src/common shared/libs
```

### Удаление: docs/api/

```bash
# Шаг 1: Поиск зависимостей
python .structure/.instructions/.scripts/find-references.py "docs/api/"

# Шаг 2: Пометить инструкции и скиллы как DELETE_
python .structure/.instructions/.scripts/mark-deleted.py docs/api
# Результат:
#   docs/.instructions/api/           → docs/.instructions/DELETE_api/
#   docs/.instructions/api/README.md  → docs/.instructions/DELETE_api/DELETE_README.md
#   .claude/skills/docs-api-*/        → .claude/skills/DELETE_docs-api-*/

# Шаг 3: Удалить из SSOT
python .structure/.instructions/.scripts/ssot.py delete docs/api

# Шаг 4: Обновить README родительской папки (секция "Папки", дерево)

# Шаг 5-6: Обновить документы, пометить битые ссылки
# <!-- BROKEN: папка удалена -->

# Шаг 7: Удалить папку
rm -rf docs/api/

# Шаг 8-9: Валидация
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
| [mirror-instructions.py](./.scripts/mirror-instructions.py) | Зеркалирование `.instructions` | [create-structure.md](./create-structure.md), Этот документ |
| [mark-deleted.py](./.scripts/mark-deleted.py) | Пометка DELETE_ при удалении | Этот документ |
| [update-skill-refs.py](./.scripts/update-skill-refs.py) | Обновление ссылок в скиллах | Этот документ |
| [validate-structure.py](./.scripts/validate-structure.py) | Валидация структуры | [validation-structure.md](./validation-structure.md) |
| [validate-links.py](./.scripts/validate-links.py) | Валидация ссылок | [validation-links.md](./validation-links.md) |

**Использование:**
```bash
# Поиск ссылок
python .structure/.instructions/.scripts/find-references.py <паттерн>

# SSOT
python .structure/.instructions/.scripts/ssot.py rename <старый_путь> <новый_путь> --description "Описание"
python .structure/.instructions/.scripts/ssot.py delete <путь>

# Зеркалирование .instructions
python .structure/.instructions/.scripts/mirror-instructions.py rename <старый_путь> <новый_путь>
python .structure/.instructions/.scripts/mirror-instructions.py move <старый_путь> <новый_путь>

# Пометка DELETE_ при удалении
python .structure/.instructions/.scripts/mark-deleted.py <путь>

# Обновление ссылок в скиллах
python .structure/.instructions/.scripts/update-skill-refs.py <старый_путь> <новый_путь>

# Валидация
python .structure/.instructions/.scripts/validate-structure.py
```

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/structure-modify](/.claude/skills/structure-modify/SKILL.md) | Изменение папки | Этот документ |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Валидация ссылок | [validation-links.md](./validation-links.md) |
