---
type: standard
description: Форматы ссылок в markdown-документах
governed-by: links/README.md
related:
  - links/patterns.md
  - links/workflow.md
---

# Форматы ссылок

Форматы ссылок: стандартные, на папки, помеченные (marked).

**Индекс:** [/.claude/.instructions/README.md](/.claude/.instructions/README.md) | **Папка:** [links/README.md](./README.md)

## Оглавление

- [Стандартная ссылка](#стандартная-ссылка)
- [Ссылка на папку](#ссылка-на-папку)
- [Помеченная ссылка](#помеченная-ссылка)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Стандартная ссылка

Формат markdown-ссылки на файл:

```markdown
[имя-файла](полный-путь)
```

**Правила:**
- Текст ссылки — имя файла (без пути)
- Путь — абсолютный от корня репозитория
- Начинается с `/`

| Упоминание | Результат |
|------------|-----------|
| `skills.md` | `[skills.md](/.claude/skills/README.md)` |
| `/.claude/agents/amy.md` | `[amy.md](/.claude/agents/amy.md)` |
| `package.json` | `[package.json](/package.json)` |
| `.gitignore` | `[.gitignore](/.gitignore)` |

---

## Ссылка на папку

Формат ссылки на папку (директорию):

```markdown
[имя-папки/](полный-путь/)
```

**Правила:**
- Текст заканчивается на `/`
- Путь заканчивается на `/`
- Указывает на директорию, не на файл

| Упоминание | Результат |
|------------|-----------|
| `/.claude/scripts/` | `[scripts/](/.claude/scripts/)` |
| `/config/` | `[config/](/config/)` |
| `/.claude/skills/` | `[skills/](/.claude/skills/)` |

---

## Помеченная ссылка

Формат помеченной (удалённой) ссылки:

```
{текст} *(ссылка удалена: {путь})*
```

**Когда используется:**
- Файл/папка был(а) удален(а)
- Ссылка станет битой
- Нужно сохранить контекст для восстановления

**Принцип:** НЕ удаляем контент, а помечаем для возможного восстановления.

**Regex для поиска:**
```regex
(\S+)\s*\*\(ссылка удалена:\s*([^)]+)\)\*
```

**Восстановление:** через `/links-update` с флагом `--old-name`

---

## Примеры

### Преобразование упоминания в ссылку

**До:**
```markdown
Настройки в /.claude/settings.json
```

**После:**
```markdown
Настройки в [settings.json](/.claude/settings.json)
```

### Преобразование ссылки в пометку

**До:**
```markdown
[config.yaml](/config/config.yaml)
```

**После:**
```markdown
config.yaml *(ссылка удалена: /config/config.yaml)*
```

### Восстановление пометки

**До:**
```markdown
config.yaml *(ссылка удалена: /config/config.yaml)*
```

**После:**
```markdown
[config.yaml](/config/settings.yaml)
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/links-create](/.claude/skills/links-create/SKILL.md) | Создаёт ссылки из упоминаний |
| [/links-delete](/.claude/skills/links-delete/SKILL.md) | Помечает ссылки при удалении файлов |
| [/links-update](/.claude/skills/links-update/SKILL.md) | Восстанавливает помеченные ссылки |

---

## Связанные инструкции

- [patterns.md](./patterns.md) — паттерны поиска ссылок
- [workflow.md](./workflow.md) — жизненный цикл ссылок
