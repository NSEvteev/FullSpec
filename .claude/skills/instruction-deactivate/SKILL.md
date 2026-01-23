---
name: instruction-deactivate
description: Деактивация инструкции (комментирование содержимого)
allowed-tools: Read, Edit, Glob, Grep
category: instruction-management
triggers:
  commands:
    - /instruction-deactivate
  phrases:
    ru:
      - деактивируй инструкцию
      - деактивировать инструкцию
      - отключи инструкцию
    en:
      - deactivate instruction
      - disable instruction
---

# Деактивация инструкции

Деактивация инструкции — комментирование содержимого и обновление статусов в README.md.

**Принцип:** Инструкции НЕ удаляются. Они деактивируются.

**Связанные скиллы:**
- [instruction-create](/.claude/skills/instruction-create/SKILL.md) — создание инструкций
- [instruction-update](/.claude/skills/instruction-update/SKILL.md) — проверка соответствия

## Оглавление

- [Формат вызова](#формат-вызова)
- [Воркфлоу](#воркфлоу)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)

---

## Формат вызова

```
/instruction-deactivate <путь>
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `путь` | Путь к инструкции (относительно `/.claude/.instructions/`) | — (обязательный) |

**Примеры:**
- `/instruction-deactivate shared/i18n.md`
- `/instruction-deactivate config/old-feature.md`

---

## Воркфлоу

> ⚠️ **ШАГ 0: ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ВЫПОЛНЕНИЕМ**
>
> Прочитать инструкции SSOT:
> 1. [workflow-deactivate.md](/.claude/.instructions/.claude/.instructions/workflow-deactivate.md) — **детальный воркфлоу DEACTIVATE (10 шагов)**
> 2. [statuses.md](/.claude/.instructions/.claude/.instructions/statuses.md) — система статусов
> 3. [relations.md](/.claude/.instructions/.claude/.instructions/relations.md) — обновление обратных ссылок в related
>
> **НЕ ПРОДОЛЖАТЬ** пока не прочитаны все файлы.

### Шаг 1: Получить путь

> **SSOT:** [workflow-deactivate.md](/.claude/.instructions/.claude/.instructions/workflow-deactivate.md#шаг-1-получить-путь)

### Шаг 2: Проверить существование

> **SSOT:** [workflow-deactivate.md](/.claude/.instructions/.claude/.instructions/workflow-deactivate.md#шаг-2-проверить-существование)

### Шаг 3: Прочитать содержимое

> **SSOT:** [workflow-deactivate.md](/.claude/.instructions/.claude/.instructions/workflow-deactivate.md#шаг-3-прочитать-содержимое)

### Шаг 4: Добавить предупреждение

> **SSOT:** [workflow-deactivate.md](/.claude/.instructions/.claude/.instructions/workflow-deactivate.md#шаг-4-добавить-предупреждение)

### Шаг 5: Закомментировать содержимое

> **SSOT:** [workflow-deactivate.md](/.claude/.instructions/.claude/.instructions/workflow-deactivate.md#шаг-5-закомментировать-содержимое)

### Шаг 6: Сохранить файл

> **SSOT:** [workflow-deactivate.md](/.claude/.instructions/.claude/.instructions/workflow-deactivate.md#шаг-6-сохранить-файл)

### Шаг 7: Обновить README папки

> **SSOT:** [workflow-deactivate.md](/.claude/.instructions/.claude/.instructions/workflow-deactivate.md#шаг-7-обновить-readme-папки)

### Шаг 8: Сбросить статус в главном README

> **SSOT:** [workflow-deactivate.md](/.claude/.instructions/.claude/.instructions/workflow-deactivate.md#шаг-8-сбросить-статус-в-главном-readme)

### Шаг 9: Проверка по чек-листу

См. [Чек-лист](#чек-лист) ниже.

### Шаг 10: Результат

```
✅ Инструкция деактивирована

Файл: /.claude/.instructions/{путь}
Статус: Не используется

README папки обновлён
Главный README обновлён
```

---

## Чек-лист

- [ ] Прочитал SSOT инструкции (ШАГ 0)
- [ ] Получил путь к инструкции
- [ ] Проверил существование файла
- [ ] Прочитал содержимое
- [ ] Добавил предупреждение
- [ ] Закомментировал содержимое
- [ ] Сохранил файл
- [ ] Обновил README папки
- [ ] Сбросил статус в главном README
- [ ] Вывел итоговый отчёт

---

## Примеры

> **SSOT:** [examples.md](/.claude/.instructions/.claude/.instructions/examples.md#instruction-deactivate)
