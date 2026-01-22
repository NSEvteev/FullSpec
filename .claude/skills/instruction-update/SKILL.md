---
name: instruction-update
description: Проверка файлов проекта на соответствие изменённой инструкции
allowed-tools: Read, Edit, Glob, Grep
category: instruction-management
triggers:
  commands:
    - /instruction-update
  phrases:
    ru:
      - обнови инструкцию
      - проверь инструкцию
      - валидируй инструкцию
    en:
      - update instruction
      - validate instruction
      - check instruction
---

# Обновление инструкции

Проверка файлов проекта на соответствие правилам инструкции. Находит несоответствия и формирует список TODO.

**Связанные скиллы:**
- [instruction-create](/.claude/skills/instruction-create/SKILL.md) — создание инструкций
- [instruction-deactivate](/.claude/skills/instruction-deactivate/SKILL.md) — деактивация инструкций
- [context-update](/.claude/skills/context-update/SKILL.md) — распространение контекста
- [test-update](/.claude/skills/test-update/SKILL.md) — обновление связанных тестов

---

## Формат вызова

```
/instruction-update <путь>
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь` | Путь к инструкции (относительно `/.claude/instructions/`) | — (обязательный) |

**Примеры:**
- `/instruction-update src/api/design.md`
- `/instruction-update git/commits.md`

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [workflow-update.md](/.claude/instructions/instructions/workflow-update.md) — **детальный воркфлоу UPDATE (12 шагов)**
> 2. [validation.md](/.claude/instructions/instructions/validation.md) — формат файлов
> 3. [patterns.md](/.claude/instructions/instructions/patterns.md) — паттерны поиска
> 4. [relations.md](/.claude/instructions/instructions/relations.md) — проверка связей (governed-by, related)
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Получить путь

### Шаг 2: Определить зону ответственности (согласно workflow-update.md)

### Шаг 3: Найти файлы в зоне

### Шаг 4: Извлечь правила из инструкции

### Шаг 5: Проверить файлы на соответствие

### Шаг 6: Сформировать список несоответствий

### Шаг 7: Внести изменения в инструкцию (добавить TODO или изменить правила)

### Шаг 8: Обновить README папки

### Шаг 9: Обновить контекст скиллов → /context-update

### Шаг 10: Проверить связанные тесты → /test-update

### Шаг 11: Проверка по чек-листу

### Шаг 12: Результат

```
✅ Проверка инструкции завершена

Инструкция: /.claude/instructions/{путь}
Зона ответственности: {зона}

Статистика:
- Проверено файлов: {N}
- Найдено несоответствий: {M}
- Файлов без проблем: {K}

Связанные скиллы обновлены: {P}
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Получил путь к инструкции
- [ ] Определил зону ответственности
- [ ] Нашёл файлы в зоне
- [ ] Извлёк правила из инструкции
- [ ] Проверил файлы на соответствие
- [ ] Сформировал список несоответствий
- [ ] Внёс изменения в инструкцию (если требуется)
- [ ] Обновил README папки
- [ ] Вызвал /context-update
- [ ] Проверил связанные тесты
- [ ] Вывел итоговый отчёт
