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
> 1. [structure.md](/.claude/instructions/instructions/structure.md) — расположение и допустимые папки
> 2. [types.md](/.claude/instructions/instructions/types.md) — типы (standard/project)
> 3. [validation.md](/.claude/instructions/instructions/validation.md) — формат названия и секций
> 4. [workflow-create.md](/.claude/instructions/instructions/workflow-create.md) — **детальный воркфлоу CREATE (15 шагов)**
> 5. [statuses.md](/.claude/instructions/instructions/statuses.md) — статусы в README.md
>
> **Шаблоны:**
> - [instruction.md](/.claude/templates/instructions/instruction.md) — шаблон инструкции
> - [readme.md](/.claude/templates/instructions/readme.md) — шаблон README папки
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Получить путь

### Шаг 2: Fail-fast проверки (согласно validation.md)

### Шаг 3: Проверить существование

### Шаг 4: Сгенерировать содержимое (согласно types.md)

### Шаг 5: Создать файл инструкции

### Шаг 6: Создать/обновить README папки

### Шаг 7: Обновить главный README (согласно statuses.md)

### Шаг 8: Ревью

### Шаг 9: Синхронизировать ссылки → /links-update

### Шаг 10: Обновить контекст → /context-update

### Шаг 11: Проверить соответствие проекта → /instruction-update

### Шаг 12: Обновить связанные скиллы (ОБЯЗАТЕЛЬНО)

### Шаг 13: Анализ и предложение новых скиллов → /skill-create

### Шаг 14: Проверка по чек-листу

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
