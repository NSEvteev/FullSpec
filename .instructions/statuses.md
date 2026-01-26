---
description: Система статусов инструкций в README.md
standard: .instructions/standard-instruction.md
index: .instructions/README.md
---

# Система статусов

Правила работы со статусами инструкций в README.md.

**Полезные ссылки:**
- [Инструкции для .instructions](./README.md)

## Оглавление

- [Столбцы таблицы](#столбцы-таблицы)
- [Значения статусов](#значения-статусов)
- [Жизненный цикл статусов](#жизненный-цикл-статусов)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Столбцы таблицы

Таблица в /.claude/.instructions/README.md:

| Столбец | Описание |
|---------|----------|
| Файл | Ссылка на инструкцию |
| Описание | Краткое описание |
| Тип | standard / project |
| Создано | Файл создан |
| Заполнено | Содержимое заполнено |

---

## Значения статусов

| Значок | Значение |
|--------|----------|
| tick | Выполнено |
| empty | Не выполнено |

---

## Жизненный цикл статусов

```
empty empty  ->  tick empty  ->  tick tick  ->  empty empty
(план)          (создано)       (заполнено)     (деактивировано)
```

**Правило:** Строки НЕ удаляются из индекса. При деактивации статусы сбрасываются.

---

## Примеры

### Инструкция в плане

```markdown
| [design.md](./src/api/design.md) | Проектирование API | standard | empty | empty |
```

### Инструкция создана

```markdown
| [design.md](./src/api/design.md) | Проектирование API | standard | tick | empty |
```

### Инструкция заполнена

```markdown
| [design.md](./src/api/design.md) | Проектирование API | standard | tick | tick |
```

### Инструкция деактивирована

```markdown
| [design.md](./src/api/design.md) | Проектирование API | standard | empty | empty |
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/instruction-create](/.claude/skills/instruction-create/SKILL.md) | Устанавливает tick/tick |
| [/instruction-deactivate](/.claude/skills/instruction-deactivate/SKILL.md) | Сбрасывает в empty/empty |

**Скрипт:** `instruction-readme-update.py` — автоматическое обновление статусов.

---

## Связанные инструкции

- [workflow.md](./workflow.md) — жизненный цикл инструкций
- [structure.md](./structure.md) — структура папок
