---
description: Воркфлоу создания новой папки в структуре проекта — README, .instructions/, синхронизация SSOT и дерева.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .structure/.instructions/README.md
---

# Воркфлоу создания

Рабочая версия стандарта: 1.1

Создание новой папки с README в структуре проекта.

**Полезные ссылки:**
- [Инструкции для .structure](./README.md)
- [SSOT структуры проекта](../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-readme.md](./standard-readme.md) |
| Валидация | [validation-structure.md](./validation-structure.md) |
| Создание | Этот документ |
| Модификация | [modify-structure.md](./modify-structure.md) |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **README.md создаётся ВМЕСТЕ с папкой.** Папка без README не существует.

> **Папка в SSOT → зеркало в `.instructions`.** Если папка добавлена в SSOT, для неё создаётся зеркало инструкций.

> **Инструкции подпапок — вложенные области.** Если родитель уже имеет `.instructions/`, инструкции подпапки создаются в `{родитель}/.instructions/{подпапка}/`, а НЕ в `{родитель}/{подпапка}/.instructions/`. Пример: `.claude/drafts/` → `.claude/.instructions/drafts/`.

> **Шаблоны — из примеров SSOT.** При создании файлов использовать шаблоны из секции "Примеры". Запрещено придумывать свой формат.

Структура документируется в момент создания, не после.

---

## Шаги

### Шаг 1: Создать папку и сгенерировать шаблон README

```bash
python .structure/.instructions/.scripts/generate-readme.py {путь} --create
```

Флаг `--create` автоматически создаёт папку. Скрипт выводит шаблон в stdout.

### Шаг 2: Заполнить плейсхолдеры и записать README

Заменить `{PLACEHOLDER}` на реальные значения:

| Плейсхолдер | Что заполнить |
|-------------|---------------|
| `{DESCRIPTION}` | Краткое описание папки |
| `{FOLDER_PURPOSE}` | Назначение (для заголовка) |
| `{EXTENDED_DESCRIPTION}` | Расширенное описание |
| `{FOLDERS_CONTENT}` | Секции подпапок (или *Нет подпапок.*) |
| `{FILES_CONTENT}` | Секции файлов (или *Нет файлов.*) |
| `{TREE_CONTENT}` | ASCII-дерево (удалить строку если пусто) |

Записать:
```
Write → {путь}/README.md
```

### Шаг 3: README родительской папки (автоматически)

> **Автоматизировано в `ssot.py add`** — выполняется автоматически при добавлении подпапки.

При добавлении подпапки (`ssot.py add parent/child`) скрипт автоматически обновляет `parent/README.md`:
- **Секция "Папки"** — добавляет описание новой подпапки
- **Дерево** — добавляет ветку новой подпапки

> Для корневых папок — пропускается (родитель = корневой README).

### Шаг 4: Добавить в SSOT

> **ПРАВИЛО:** ВСЕ папки добавляются в SSOT, включая подпапки.

```bash
# С автозаменой {EXTENDED_DESCRIPTION}
python .structure/.instructions/.scripts/ssot.py add {путь} -d "Описание" -e "Расширенное описание"

# Подпапка (родитель должен быть в SSOT)
python .structure/.instructions/.scripts/ssot.py add {родитель}/{папка} -d "Описание" -e "Расширенное описание"
```

Флаг `-e` / `--extended` автоматически заменяет `{EXTENDED_DESCRIPTION}` в SSOT.

Скрипт добавляет в `/.structure/README.md`:
- Секцию папки (алфавитный порядок)
- Оглавление (с отступом для подпапок)
- Дерево (внутри родительской папки)

### Шаг 5: Создать зеркало `.instructions`

> **ПРАВИЛО:** Папка в SSOT → зеркало в `.instructions`.

> **ВАЖНО:** Для подпапок инструкции создаются как вложенная область родительского `.instructions/`, а НЕ как отдельный `.instructions/` внутри подпапки.

```bash
python .structure/.instructions/.scripts/mirror-instructions.py create {путь}
```

**Что создаёт скрипт:**

| Тип папки | Что создаётся | НЕ создаётся |
|-----------|---------------|--------------|
| Корневая (`docs/`) | `docs/.instructions/README.md` | — |
| Подпапка (`docs/api/`) | `docs/.instructions/api/README.md` | ~~`docs/api/.instructions/`~~ |

README для `.instructions` содержит индекс инструкций папки.

**Если добавляется подпапка в существующую `.instructions/`:**

Скрипт автоматически обновляет родительский README:
- Добавляет секцию "Вложенные области" (если не было)
- Добавляет строку в таблицу вложенных областей
- Обновляет оглавление и дерево

### Шаг 6: Валидация

```bash
python .structure/.instructions/.scripts/validate.py --path {путь}
```

Единый скрипт запускает проверки:
- Структура SSOT
- Ссылки в markdown
- Наличие зеркала `.instructions`

---

## Чек-лист

- [ ] Папка создана (generate-readme.py --create)
- [ ] README.md заполнен и записан
- [ ] SSOT обновлён (ssot.py add -d -e) — автоматически обновляет README родителя
- [ ] Зеркало `.instructions` создано (mirror-instructions.py create)
- [ ] Валидация пройдена (validate.py)

---

## Примеры

### Создание корневой папки docs/

```bash
# Шаг 1: Создать папку и сгенерировать шаблон
python .structure/.instructions/.scripts/generate-readme.py docs --create

# Шаг 2: Заполнить плейсхолдеры, записать README (Write tool)

# Шаг 3: Пропускаем (корневая папка)

# Шаг 4: Обновить SSOT
python .structure/.instructions/.scripts/ssot.py add docs -d "Документация проекта" -e "Проектная документация и руководства."

# Шаг 5: Создать зеркало .instructions
python .structure/.instructions/.scripts/mirror-instructions.py create docs
# Создаст: docs/.instructions/README.md

# Шаг 6: Валидация
python .structure/.instructions/.scripts/validate.py --path docs
```

### Создание подпапки docs/api/

```bash
# Шаг 1: Создать папку и сгенерировать шаблон
python .structure/.instructions/.scripts/generate-readme.py docs/api --create

# Шаг 2: Заполнить плейсхолдеры, записать README (Write tool)

# Шаг 3: Обновить SSOT (родитель docs/ должен быть в SSOT)
# Автоматически обновит docs/README.md (секция "Папки", дерево)
python .structure/.instructions/.scripts/ssot.py add docs/api -d "API документация" -e "Документация API."

# Шаг 4: Создать зеркало .instructions
python .structure/.instructions/.scripts/mirror-instructions.py create docs/api
# Создаст: docs/.instructions/api/README.md

# Шаг 5: Валидация
python .structure/.instructions/.scripts/validate.py --path docs
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [generate-readme.py](./.scripts/generate-readme.py) | Генерация шаблона README | Этот документ |
| [ssot.py](./.scripts/ssot.py) | Управление SSOT (add/rename/delete) | Этот документ, [modify-structure.md](./modify-structure.md) |
| [mirror-instructions.py](./.scripts/mirror-instructions.py) | Зеркалирование `.instructions` | Этот документ, [modify-structure.md](./modify-structure.md) |
| [validate.py](./.scripts/validate.py) | Единая валидация | [validation-structure.md](./validation-structure.md), [validation-links.md](./validation-links.md) |

**Использование:**
```bash
# Генерация README с автосозданием папки
python .structure/.instructions/.scripts/generate-readme.py <путь> --create

# Добавление в SSOT с расширенным описанием
python .structure/.instructions/.scripts/ssot.py add <путь> -d "Описание" -e "Расширенное описание"

# Создание зеркала .instructions
python .structure/.instructions/.scripts/mirror-instructions.py create <путь>

# Валидация (все проверки)
python .structure/.instructions/.scripts/validate.py
python .structure/.instructions/.scripts/validate.py --path <папка>
```

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/structure-create](/.claude/skills/structure-create/SKILL.md) | Создание папки | Этот документ |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Валидация ссылок | [validation-links.md](./validation-links.md) |
