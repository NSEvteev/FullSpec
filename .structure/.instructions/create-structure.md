---
description: Воркфлоу создания новой папки и README
standard: .instructions/standard-instruction.md
index: .structure/.instructions/README.md
---

# Воркфлоу создания

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

- [Принцип](#принцип)
- [Шаги](#шаги)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принцип

> **README.md создаётся ВМЕСТЕ с папкой.** Папка без README не существует.

Структура документируется в момент создания, не после.

---

## Шаги

### Шаг 1: Создать папку

```bash
mkdir {путь_к_папке}
```

### Шаг 2: Сгенерировать шаблон README

```bash
python .structure/.instructions/.scripts/generate-readme.py {путь}
```

Скрипт определит тип папки и создаст шаблон с плейсхолдерами.

### Шаг 3: Заполнить плейсхолдеры

Заменить `{PLACEHOLDER}` на реальные значения:

| Плейсхолдер | Что заполнить |
|-------------|---------------|
| `{DESCRIPTION}` | Краткое описание папки |
| `{FOLDER_PURPOSE}` | Назначение (для заголовка) |
| `{EXTENDED_DESCRIPTION}` | Расширенное описание |
| `{FOLDERS_CONTENT}` | Секции подпапок |
| `{FILES_CONTENT}` | Секции файлов |
| `{TREE_CONTENT}` | ASCII-дерево |

### Шаг 4: Записать README

```
Write → {путь}/README.md
```

### Шаг 5: Добавить в SSOT

```bash
python .structure/.instructions/.scripts/ssot.py add {папка} --description "Описание"
```

Скрипт автоматически добавляет в `/.structure/README.md`:
- Секцию папки (алфавитный порядок)
- Оглавление
- Дерево

> **После:** Замените `{EXTENDED_DESCRIPTION}` в секции папки.

### Шаг 6: Валидация структуры

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

### Шаг 7: Валидация ссылок

```
/links-validate
```

---

## Чек-лист

- [ ] Папка создана
- [ ] README.md сгенерирован и заполнен
- [ ] SSOT обновлён (update-ssot.py)
- [ ] {EXTENDED_DESCRIPTION} заполнен
- [ ] Валидация структуры пройдена
- [ ] Валидация ссылок пройдена

---

## Примеры

### Создание папки docs/

```bash
# Шаг 1-2: Создать папку и сгенерировать шаблон
mkdir docs
python .structure/.instructions/.scripts/generate-readme.py docs

# Шаг 3-4: Заполнить плейсхолдеры, записать README

# Шаг 5: Обновить SSOT
python .structure/.instructions/.scripts/ssot.py add docs --description "Документация проекта"

# Шаг 6-7: Валидация
python .structure/.instructions/.scripts/validate-structure.py
/links-validate
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [generate-readme.py](./.scripts/generate-readme.py) | Генерация шаблона README | Этот документ |
| [ssot.py](./.scripts/ssot.py) | Управление SSOT (add/rename/delete) | Этот документ, [modify-structure.md](./modify-structure.md) |
| [validate-structure.py](./.scripts/validate-structure.py) | Валидация структуры | [validation-structure.md](./validation-structure.md) |

**Использование:**
```bash
python .structure/.instructions/.scripts/generate-readme.py <путь>
python .structure/.instructions/.scripts/ssot.py add <папка> --description "Описание"
python .structure/.instructions/.scripts/validate-structure.py
```

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Валидация ссылок | [validation-links.md](./validation-links.md) |
