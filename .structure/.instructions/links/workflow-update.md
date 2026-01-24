---
type: standard
description: Воркфлоу обновления ссылок при изменении путей
governed-by: .structure/.instructions/links/README.md
related:
  - .structure/.instructions/links/validation.md
  - .structure/.instructions/workflow-update.md
---

# Воркфлоу обновления ссылок

Шаги обновления ссылок при переименовании, перемещении или удалении файлов.

> [Инструкции по работе со ссылками](./README.md)

## Оглавление

- [Когда обновлять](#когда-обновлять)
- [Шаги](#шаги)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Когда обновлять

| Событие | Действие со ссылками |
|---------|---------------------|
| Переименование файла | Обновить все ссылки на файл |
| Перемещение файла | Обновить все ссылки на файл |
| Удаление файла | Пометить битые ссылки |
| Изменение заголовка | Обновить якорные ссылки |
| Переименование папки | Обновить все ссылки на папку и файлы в ней |

---

## Шаги

### При переименовании/перемещении

#### Шаг 1: Найти все ссылки на файл

```bash
# Поиск ссылок на файл
grep -r "old-name.md" --include="*.md" .
```

**Где искать:**
- `**/*.md` — все markdown файлы
- `.yaml` файлы с frontmatter

#### Шаг 2: Выполнить изменение файла

```bash
mv old-path/old-name.md new-path/new-name.md
```

#### Шаг 3: Обновить ссылки

```
/links-update old-path/old-name.md → new-path/new-name.md
```

#### Шаг 4: Проверить

```
/links-validate
```

---

### При удалении

#### Шаг 1: Найти все ссылки на файл

```bash
grep -r "file-to-delete.md" --include="*.md" .
```

#### Шаг 2: Вызвать /links-delete

```
/links-delete path/to/file.md
```

Скилл пометит все ссылки как битые.

#### Шаг 3: Удалить файл

```bash
rm path/to/file.md
```

#### Шаг 4: Исправить или удалить битые ссылки

Вручную или через редактор.

---

### При изменении заголовка

#### Шаг 1: Найти якорные ссылки

```bash
grep -r "#old-heading" --include="*.md" .
```

#### Шаг 2: Изменить заголовок

```markdown
<!-- До -->
## Old Heading

<!-- После -->
## New Heading
```

#### Шаг 3: Обновить якоря

```
/links-update file.md#old-heading → file.md#new-heading
```

---

## Чек-лист

### Переименование/перемещение

- [ ] Найдены все ссылки на файл
- [ ] Файл переименован/перемещён
- [ ] /links-update вызван
- [ ] /links-validate пройдена

### Удаление

- [ ] Найдены все ссылки на файл
- [ ] /links-delete вызван
- [ ] Файл удалён
- [ ] Битые ссылки исправлены или удалены
- [ ] /links-validate пройдена

### Изменение заголовка

- [ ] Найдены якорные ссылки
- [ ] Заголовок изменён
- [ ] Якоря обновлены
- [ ] /links-validate пройдена

---

## Примеры

### Переименование файла

```bash
# 1. Поиск ссылок
grep -r "old-api.md" --include="*.md" .
# Найдено: src/README.md, docs/api.md

# 2. Переименование
mv docs/old-api.md docs/new-api.md

# 3. Обновление ссылок
/links-update docs/old-api.md → docs/new-api.md

# 4. Проверка
/links-validate
```

### Перемещение папки

```bash
# 1. Поиск ссылок
grep -r "/old-folder/" --include="*.md" .

# 2. Перемещение
mv old-folder/ new-location/new-folder/

# 3. Обновление ссылок
/links-update /old-folder/ → /new-location/new-folder/

# 4. Проверка
/links-validate
```

### Удаление файла

```bash
# 1. Поиск ссылок
grep -r "deprecated.md" --include="*.md" .

# 2. Пометка битых ссылок
/links-delete docs/deprecated.md

# 3. Удаление
rm docs/deprecated.md

# 4. Исправление ссылок вручную
# (удалить или заменить)

# 5. Проверка
/links-validate
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/links-update](/.claude/skills/links-update/SKILL.md) | Обновление путей в ссылках |
| [/links-delete](/.claude/skills/links-delete/SKILL.md) | Пометка битых ссылок |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка всех ссылок |

---

## Связанные инструкции

- [validation.md](./validation.md) — правила валидации
- [../workflow-update.md](../workflow-update.md) — обновление папок (включает ссылки)
