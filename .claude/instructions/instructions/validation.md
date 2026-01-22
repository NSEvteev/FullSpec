---
type: standard
description: Валидация путей и формата файлов инструкций
governed-by: instructions/README.md
related:
  - instructions/structure.md
  - instructions/types.md
---

# Валидация инструкций

Правила валидации путей, имён и формата файлов инструкций.

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [instructions/README.md](./README.md)

## Оглавление

- [Формат названия](#формат-названия)
- [Обязательные секции](#обязательные-секции)
- [Навигационные ссылки](#навигационные-ссылки)
- [Frontmatter](#frontmatter)
- [governed-by](#governed-by)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Формат названия

**Правила:**
- Только латиница (a-z)
- Цифры (0-9)
- Дефис (-)
- Расширение .md

**Примеры:**

| Правильно | Неправильно |
|-----------|-------------|
| design.md | Design.md |
| error-handling.md | error_handling.md |
| api-v2.md | api v2.md |

---

## Обязательные секции

Каждая инструкция ДОЛЖНА содержать:

1. **Frontmatter** — YAML в начале файла
2. **Заголовок** — # Название
3. **Навигационные ссылки** — после описания
4. **Оглавление** — ## Оглавление
5. **Правила** — ## Правила (или тематические секции)
6. **Примеры** — ## Примеры
7. **Скиллы** — ## Скиллы
8. **Связанные инструкции** — ## Связанные инструкции

---

## Навигационные ссылки

После описания (перед оглавлением) каждая инструкция содержит ссылки:

```markdown
**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [{папка}/README.md](./README.md)
```

**Назначение:**
- **Индекс** — ссылка на главный индекс всех инструкций
- **Папка** — ссылка на README папки, в которой расположена инструкция

---

## Frontmatter

**Обязательные поля:**

| Поле | Обязательно | Описание |
|------|-------------|----------|
| type | Да | standard или project |
| description | Да | Краткое описание |
| governed-by | Да | Ссылка на мета-инструкцию |
| related | Нет | Список связанных инструкций |

**Пример:**

```yaml
---
type: standard
description: Правила проектирования REST API
governed-by: instructions/README.md
related:
  - src/api/versioning.md
  - src/data/errors.md
---
```

---

## governed-by

**Назначение:** Связь инструкции с мета-инструкцией, которая определяет правила работы с инструкциями.

**Значение:** Всегда `instructions/README.md` (путь относительно `/.claude/instructions/`).

**Зачем нужно:**
- Единый источник правил для всех инструкций
- Возможность найти все инструкции, подчинённые определённым правилам
- Валидация соответствия формату

---

## Примеры

### Пример навигационных ссылок

Для `src/api/design.md`:

```markdown
**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [src/api/README.md](./README.md)
```

### Пример frontmatter

```yaml
---
type: standard
description: Правила проектирования REST API
governed-by: instructions/README.md
related:
  - src/api/versioning.md
---
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/instruction-create](/.claude/skills/instruction-create/SKILL.md) | Создаёт инструкцию по шаблону |

**Скрипт:** `instruction-validate.py` — автоматическая валидация пути и формата.

---

## Связанные инструкции

- [structure.md](./structure.md) — допустимые папки
- [types.md](./types.md) — типы инструкций
