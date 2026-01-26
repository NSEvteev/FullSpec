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

## Оглавление

- [Принцип](#принцип)
- [Шаги](#шаги)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

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

Обновить `/.structure/README.md`:

1. **Секция папки** — добавить в "Корневые папки" (алфавитный порядок)
2. **Оглавление** — добавить ссылку `- [{папка}/](#-{папка})`
3. **Дерево** — добавить в ASCII-дерево с комментарием

### Шаг 6: Обновить связанные документы

| Документ | Когда обновлять |
|----------|-----------------|
| `CLAUDE.md` | Если папка важна для Claude Code |
| `/.instructions/coverage.md` | Если планируются инструкции |

### Шаг 7: Валидация

```bash
python .structure/.instructions/.scripts/validate-structure.py
```

---

## Чек-лист

- [ ] Папка создана
- [ ] README.md сгенерирован и заполнен
- [ ] Секция добавлена в SSOT
- [ ] Оглавление обновлено
- [ ] Дерево обновлено
- [ ] Связанные документы обновлены
- [ ] Валидация пройдена

---

## Примеры

### Создание папки docs/

**Шаг 1-2:** Создать и сгенерировать
```bash
mkdir docs
python .structure/.instructions/.scripts/generate-readme.py docs
```

**Шаг 5:** Добавить в SSOT

```markdown
<!-- Секция в "Корневые папки" -->
### 🔗 [docs/](../docs/README.md)

**Документация проекта.**

Архитектурные схемы (`architecture/`), руководства (`guides/`), API (`api/`).

<!-- Оглавление -->
- [docs/](#-docs)

<!-- Дерево -->
├── docs/                    # Документация проекта
```

---

## Скрипты

| Скрипт | Назначение | Использование |
|--------|------------|---------------|
| [generate-readme.py](./.scripts/generate-readme.py) | Генерация шаблона README | `python .structure/.instructions/.scripts/generate-readme.py <путь>` |
| [validate-structure.py](./.scripts/validate-structure.py) | Валидация структуры | `python .structure/.instructions/.scripts/validate-structure.py` |

**Воркфлоу LLM:**
1. Вызвать generate-readme.py → получить шаблон
2. Заполнить `{PLACEHOLDER}` значениями
3. Записать через Write tool
4. Вызвать validate-structure.py → проверить

---

## Скиллы

**Скиллы для этой области отсутствуют.**

---

## Связанные инструкции

- [standard-readme.md](./standard-readme.md) — стандарт README
- [workflow-modify.md](./workflow-modify.md) — изменение папки
- [validation-structure.md](./validation-structure.md) — валидация структуры
