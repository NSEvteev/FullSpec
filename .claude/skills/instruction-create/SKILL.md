---
name: instruction-create
description: Создание новой инструкции по шаблону
allowed-tools: Write, Read, Edit, Glob, Grep
category: instruction-management
triggers:
  commands:
    - /instruction-create
  phrases:
    ru:
      - создай инструкцию
      - новая инструкция
      - добавь инструкцию
    en:
      - create instruction
      - new instruction
      - add instruction
---

# Создание инструкции

Создание новой инструкции в `/.claude/instructions/`.

**Связанные скиллы:**
- [instruction-update](/.claude/skills/instruction-update/SKILL.md) — проверка соответствия
- [instruction-deactivate](/.claude/skills/instruction-deactivate/SKILL.md) — деактивация

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/instruction-create <путь> [--dry-run] [--auto]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь` | Путь к инструкции (относительно `/.claude/instructions/`) | — (обязательный) |
| `--dry-run` | Показать план без создания | false |
| `--auto` | Автоматический режим (без подтверждений) | false |

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [structure.md](/.claude/instructions/meta/instructions/structure.md) — расположение и допустимые папки
> 2. [types.md](/.claude/instructions/meta/instructions/types.md) — типы (standard/project)
> 3. [validation.md](/.claude/instructions/meta/instructions/validation.md) — формат названия и секций
> 4. [relations.md](/.claude/instructions/meta/instructions/relations.md) — заполнение governed-by и related
> 5. [workflow-create.md](/.claude/instructions/meta/instructions/workflow-create.md) — **детальный воркфлоу CREATE (15 шагов)**
> 6. [statuses.md](/.claude/instructions/meta/instructions/statuses.md) — статусы в README.md
>
> **Шаблоны:**
> - [instruction.md](/.claude/templates/meta/instructions/instruction.md) — шаблон инструкции
> - [readme.md](/.claude/templates/meta/instructions/readme.md) — шаблон README папки
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Получить путь

> **SSOT:** [workflow-create.md](/.claude/instructions/meta/instructions/workflow-create.md#шаг-1-получить-путь)

### Шаг 2: Fail-fast проверки (согласно validation.md)

> **SSOT:** [workflow-create.md](/.claude/instructions/meta/instructions/workflow-create.md#шаг-2-fail-fast-проверки)

### Шаг 3: Проверить существование

> **SSOT:** [workflow-create.md](/.claude/instructions/meta/instructions/workflow-create.md#шаг-3-проверить-существование)

### Шаг 4: Сгенерировать содержимое (согласно types.md)

> **SSOT:** [workflow-create.md](/.claude/instructions/meta/instructions/workflow-create.md#шаг-4-сгенерировать-содержимое)

### Шаг 5: Создать файл инструкции

> **SSOT:** [workflow-create.md](/.claude/instructions/meta/instructions/workflow-create.md#шаг-5-создать-файл-инструкции)

### Шаг 6: Создать/обновить README папки

> **SSOT:** [workflow-create.md](/.claude/instructions/meta/instructions/workflow-create.md#шаг-6-создатьобновить-readme-папки)

### Шаг 7: Обновить главный README (согласно statuses.md)

> **SSOT:** [workflow-create.md](/.claude/instructions/meta/instructions/workflow-create.md#шаг-7-обновить-главный-readme)

### Шаг 8: Ревью

> **SSOT:** [workflow-create.md](/.claude/instructions/meta/instructions/workflow-create.md#шаг-8-ревью)

### Шаг 9: Синхронизировать ссылки → /links-update

> **SSOT:** [SKILL.md](/.claude/skills/links-update/SKILL.md)

### Шаг 10: Обновить контекст → /context-update

> **SSOT:** [SKILL.md](/.claude/skills/context-update/SKILL.md)

### Шаг 11: Проверить соответствие проекта → /instruction-update

> **SSOT:** [SKILL.md](/.claude/skills/instruction-update/SKILL.md)

### Шаг 12: Обновить связанные скиллы (ОБЯЗАТЕЛЬНО)

> **SSOT:** [workflow-create.md](/.claude/instructions/meta/instructions/workflow-create.md#шаг-12-обновить-связанные-скиллы)

### Шаг 13: Анализ и предложение новых скиллов → /skill-create

> **SSOT:** [SKILL.md](/.claude/skills/skill-create/SKILL.md)

### Шаг 14: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 15: Результат

```
✅ Инструкция создана

Файл: /.claude/instructions/{путь}
Описание: {краткое описание}
Тип: {standard | project}

Статусы обновлены: /.claude/instructions/README.md
Ссылки: {N} документов через /links-update
Контекст: {M} документов через /context-update
Скиллы обновлены: {P}
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Получил путь
- [ ] Прошёл fail-fast проверки
- [ ] Проверил существование
- [ ] Сгенерировал содержимое
- [ ] Создал файл инструкции
- [ ] Создал/обновил README папки
- [ ] Обновил главный README
- [ ] Провёл ревью
- [ ] Вызвал /links-update
- [ ] Вызвал /context-update
- [ ] Вызвал /instruction-update
- [ ] Обновил связанные скиллы
- [ ] Проанализировал и предложил новые скиллы
- [ ] Вывел итоговый отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/instructions/meta/instructions/examples.md#instruction-create)
