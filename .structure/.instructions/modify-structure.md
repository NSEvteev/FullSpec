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
| Стандарт | [standard-readme.md](./standard-readme.md), [standard-links.md](./standard-links.md) |
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

```bash
python .structure/.instructions/.scripts/ssot.py rename {старое_имя} {новое_имя} --description "Описание"
```

Скрипт автоматически обновляет в `/.structure/README.md`:
- Секцию папки (название и ссылка)
- Оглавление
- Дерево папок

### Шаг 4: Обновить README папки

Обновить заголовок `# /path/new-name/ — ...`

### Шаг 5: Обновить ссылки вручную

Найти и заменить все вхождения `old-name/` на `new-name/` в markdown-файлах.

### Шаг 6: Валидация структуры

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

### Шаг 7: Валидация ссылок

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

В `/.structure/README.md`:
1. **Секция старого родителя** — удалить упоминание
2. **Секция нового родителя** — добавить упоминание
3. **Дерево папок** — переместить ветку

### Шаг 4: Обновить README папки

Обновить:
- Заголовок с новым путём
- Блок "Полезные ссылки" (цепочка родителей изменилась)

### Шаг 5: Обновить README дочерних папок

Если есть подпапки — их "Полезные ссылки" тоже изменились.

### Шаг 6: Обновить ссылки вручную

Найти и заменить все вхождения `src/utils/` на `shared/utils/` в markdown-файлах.

### Шаг 7: Валидация структуры

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

### Шаг 8: Валидация ссылок

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

```bash
python .structure/.instructions/.scripts/ssot.py delete {папка}
```

Скрипт автоматически удаляет из `/.structure/README.md`:
- Секцию папки
- Ссылку из оглавления
- Запись из дерева

### Шаг 3: Обновить связанные документы

- `CLAUDE.md` — удалить упоминания
- Другие README — обновить или пометить битые ссылки

### Шаг 4: Пометить битые ссылки

Добавить комментарий `<!-- BROKEN: папка удалена -->` к ссылкам на удаляемую папку.

### Шаг 5: Удалить папку

**Только после обновления документов:**

```bash
rm -rf {папка}/
```

### Шаг 6: Валидация структуры

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

### Шаг 7: Валидация ссылок

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

#### Шаг 4: Проверить

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
- [ ] Ссылки обновлены вручную
- [ ] Валидация структуры пройдена
- [ ] Валидация ссылок пройдена

### Перемещение

- [ ] Найдены все ссылки
- [ ] Папка перемещена
- [ ] SSOT обновлён (оба родителя, дерево)
- [ ] README папки обновлён (путь, "Полезные ссылки")
- [ ] README дочерних папок обновлены
- [ ] Ссылки обновлены вручную
- [ ] Валидация структуры пройдена
- [ ] Валидация ссылок пройдена

### Удаление

- [ ] Найдены все зависимости
- [ ] Секция удалена из SSOT
- [ ] Связанные документы обновлены
- [ ] Битые ссылки помечены
- [ ] Папка удалена из файловой системы
- [ ] Валидация структуры пройдена
- [ ] Валидация ссылок пройдена

### Обновление ссылок (файлы)

- [ ] Найдены все ссылки на файл
- [ ] Файл переименован/перемещён/удалён
- [ ] Ссылки обновлены или помечены
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

# Шаг 5: Обновить ссылки вручную
# Заменить shared/utils/ на shared/helpers/

# Шаг 6-7: Валидация
python .structure/.instructions/.scripts/validate-structure.py
/links-validate
```

### Перемещение: src/common/ → shared/libs/

**Шаг 2:** Перемещение
```bash
mv src/common/ shared/libs/
```

**Шаг 4:** Обновление README
```markdown
# /shared/libs/ — Общие библиотеки

**Полезные ссылки:**
- [shared/](../README.md)
- [Структура проекта](/.structure/README.md)
```

**Шаг 6:** Обновление ссылок вручную — найти и заменить `src/common/` на `shared/libs/`.

### Удаление: legacy/

```bash
# Шаг 1: Поиск зависимостей
python .structure/.instructions/.scripts/find-references.py "legacy/"

# Шаг 2: Удалить из SSOT
python .structure/.instructions/.scripts/ssot.py delete legacy

# Шаг 3-4: Обновить документы, пометить битые ссылки
# <!-- BROKEN: папка удалена -->

# Шаг 5: Удалить папку
rm -rf legacy/

# Шаг 6-7: Валидация
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
python .structure/.instructions/.scripts/ssot.py rename <старое> <новое> --description "Описание"
python .structure/.instructions/.scripts/ssot.py delete <папка>
python .structure/.instructions/.scripts/validate-structure.py
```

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Валидация ссылок | [validation-links.md](./validation-links.md) |
