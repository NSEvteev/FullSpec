---
type: standard
description: Паттерны поиска ссылок на инструкции
governed-by: instructions/README.md
related:
  - instructions/workflow.md
  - instructions/statuses.md
---

# Паттерны поиска ссылок

Паттерны для поиска ссылок на инструкции при обновлении и деактивации.

**Индекс:** [/.claude/.instructions/README.md](/.claude/.instructions/README.md) | **Папка:** [instructions/README.md](./README.md)

## Оглавление

- [Где искать](#где-искать)
- [Типы ссылок](#типы-ссылок)
- [Действия при обнаружении](#действия-при-обнаружении)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Где искать

| Место | Glob-паттерн |
|-------|--------------|
| Инструкции | /.claude/.instructions/**/*.md |
| Скиллы | /.claude/skills/*/SKILL.md |
| Индекс | /.claude/.instructions/README.md |
| Агенты | /.claude/agents/*.md |

---

## Типы ссылок

### Markdown-ссылка

**Паттерн:**
```
[текст](путь/к/инструкции.md)
```

**Regex:**
```
\[.*\]\(.*{путь}.*\)
```

### Frontmatter related

**Паттерн:**
```yaml
related:
  - путь/к/инструкции.md
```

**Regex:**
```
related:[\s\S]*?{путь}
```

### Строка таблицы в README.md

**Паттерн:**
```
| [имя.md](./путь/имя.md) | описание | тип | tick | tick |
```

**Regex:**
```
\| \[{имя}\]\(.*\) \|.*\| tick \| tick \|
```

---

## Действия при обнаружении

| Тип ссылки | При деактивации |
|------------|-----------------|
| Markdown-ссылка | Удалить строку или пометить |
| related в frontmatter | Удалить элемент из массива |
| Строка таблицы | Заменить tick на empty |
| Ссылка в скилле | Добавить пометку или удалить |

---

## Примеры

### Поиск ссылок в инструкциях

```bash
grep -r "design.md" .claude/.instructions/
```

### Поиск в скиллах

```bash
grep -r "instructions/src/api" .claude/skills/
```

### Поиск в frontmatter

```bash
grep -A 5 "related:" .claude/.instructions/**/*.md | grep "design.md"
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/instruction-deactivate](/.claude/skills/instruction-deactivate/SKILL.md) | Использует паттерны при деактивации |
| [/links-update](/.claude/skills/links-update/SKILL.md) | Обновляет ссылки при переименовании |

---

## Связанные инструкции

- [workflow.md](./workflow.md) — жизненный цикл
- [statuses.md](./statuses.md) — статусы в README.md
