---
type: standard
description: Работа со связями между инструкциями (governed-by, related)
governed-by: instructions/README.md
related:
  - instructions/validation.md
  - instructions/workflow.md
  - instructions/structure.md
---

# Связи между инструкциями

Правила работы с полями `governed-by` и `related` в frontmatter инструкций.

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [instructions/README.md](./README.md)

## Оглавление

- [governed-by](#governed-by)
- [related](#related)
- [Правила обновления](#правила-обновления)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## governed-by

Поле `governed-by` указывает на мета-инструкцию, которая управляет данной инструкцией.

### Назначение

- **Иерархия:** определяет родительскую инструкцию
- **Контекст:** помогает LLM найти связанные правила
- **Навигация:** упрощает поиск инструкций по области

### Формат

```yaml
governed-by: {путь-к-мета-инструкции}
```

### Правила

1. **Путь относительный** — относительно `/.claude/instructions/`
2. **Файл должен существовать** — ссылка на несуществующий файл = ошибка
3. **Обычно README.md** — указывает на README папки

### Маппинг governed-by

| Расположение инструкции | governed-by |
|-------------------------|-------------|
| `src/api/*.md` | `src/api/README.md` |
| `git/*.md` | `git/README.md` |
| `instructions/*.md` | `instructions/README.md` |
| `{folder}/*.md` | `{folder}/README.md` |
| `{folder}/README.md` | `{parent}/README.md` или `README.md` |

### Пример

```yaml
# Для файла: /.claude/instructions/src/api/design.md
governed-by: src/api/README.md

# Для файла: /.claude/instructions/git/commits.md
governed-by: git/README.md

# Для файла: /.claude/instructions/src/api/README.md
governed-by: src/README.md
```

---

## related

Поле `related` содержит список связанных инструкций.

### Назначение

- **Контекст:** помогает LLM найти дополнительные правила
- **Навигация:** связывает инструкции по смыслу
- **Обновление:** при изменении инструкции проверять related

### Формат

```yaml
related:
  - {путь/к/инструкции1.md}
  - {путь/к/инструкции2.md}
```

### Правила

1. **Пути относительные** — относительно `/.claude/instructions/`
2. **Файлы должны существовать** — ссылка на несуществующий файл = ошибка
3. **Без циклов** — избегать A→B→C→A (хотя технически допустимо)
4. **Симметричность** — если A ссылается на B, то B должен ссылаться на A

### Когда добавлять в related

| Ситуация | Добавлять в related |
|----------|---------------------|
| Инструкция расширяет другую | ✅ Да |
| Инструкция ссылается на правила | ✅ Да |
| Инструкция в той же папке | ⚠️ Обычно не нужно (есть governed-by) |
| Инструкция в другой области | ✅ Если есть смысловая связь |

### Пример

```yaml
# Для файла: /.claude/instructions/src/api/design.md
related:
  - src/api/versioning.md      # Версионирование API
  - src/data/errors.md         # Формат ошибок
  - shared/contracts.md        # Контракты

# Для файла: /.claude/instructions/git/commits.md
related:
  - git/workflow.md            # Общий workflow
  - git/review.md              # Code review
```

---

## Правила обновления

### При создании инструкции (CREATE)

1. **governed-by:** указать README папки
2. **related:** добавить связанные инструкции
3. **Обратные ссылки:** добавить текущую инструкцию в related связанных

### При обновлении инструкции (UPDATE)

1. **Проверить governed-by:** если инструкция перемещена, обновить
2. **Проверить related:** добавить новые связи, удалить неактуальные
3. **Обратные ссылки:** обновить related в связанных инструкциях

### При деактивации инструкции (DEACTIVATE)

1. **Не изменять frontmatter** деактивированной инструкции
2. **Обратные ссылки:** удалить из related всех связанных инструкций

### Автоматизация

Скиллы автоматически обновляют связи:

| Действие | Скилл |
|----------|-------|
| Обновление ссылок в тексте | `/links-update` |
| Распространение контекста | `/context-update` |

---

## Примеры

### Правильно

```yaml
---
type: standard
description: Дизайн REST API
governed-by: src/api/README.md
related:
  - src/api/versioning.md
  - src/data/errors.md
---
```

### Неправильно

```yaml
---
type: standard
description: Дизайн REST API
# ❌ governed-by отсутствует
related:
  - /.claude/instructions/src/api/versioning.md  # ❌ Абсолютный путь
  - versioning.md                                 # ❌ Относительно текущего файла
---
```

### Исправление

```yaml
---
type: standard
description: Дизайн REST API
governed-by: src/api/README.md                   # ✅ Добавлено
related:
  - src/api/versioning.md                        # ✅ Относительно /.claude/instructions/
---
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/instruction-create](/.claude/skills/instruction-create/SKILL.md) | Создаёт инструкцию с правильными связями |
| [/instruction-update](/.claude/skills/instruction-update/SKILL.md) | Проверяет и обновляет связи |
| [/links-update](/.claude/skills/links-update/SKILL.md) | Обновляет ссылки в тексте |
| [/context-update](/.claude/skills/context-update/SKILL.md) | Распространяет контекст по графу |

---

## Связанные инструкции

- [validation.md](./validation.md) — валидация frontmatter (включая governed-by, related)
- [workflow.md](./workflow.md) — жизненный цикл инструкций
- [structure.md](./structure.md) — структура папок (влияет на governed-by)
