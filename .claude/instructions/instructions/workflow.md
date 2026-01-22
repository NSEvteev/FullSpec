---
type: standard
description: Жизненный цикл инструкций: CREATE, UPDATE, DEACTIVATE
governed-by: instructions/README.md
related:
  - instructions/statuses.md
  - instructions/patterns.md
---

# Жизненный цикл инструкций

Фазы работы с инструкциями: создание, обновление, деактивация.

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [instructions/README.md](./README.md)

## Оглавление

- [Диаграмма](#диаграмма)
- [Синхронизация README](#синхронизация-readme)
- [Фаза CREATE](#фаза-create)
- [Фаза UPDATE](#фаза-update)
- [Фаза DEACTIVATE](#фаза-deactivate)
- [Граф зависимостей](#граф-зависимостей)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Диаграмма

```
СОЗДАНИЕ -> АКТИВНАЯ -> (опционально) НЕАКТИВНАЯ
                              |
                    НЕ УДАЛЯЕТСЯ, а помечается
```

---

## Синхронизация README

**Правило:** Все операции с инструкциями синхронизируют README-файлы.

При любой операции (CREATE, UPDATE, DEACTIVATE) обновляются:
1. **Инструкция** — целевой файл
2. **README папки** — `/.claude/instructions/{папка}/README.md`
3. **Главный README** — `/.claude/instructions/README.md`

| Операция | Инструкция | README папки | Главный README |
|----------|------------|--------------|----------------|
| CREATE | Создать | Создать или обновить | Обновить статус |
| UPDATE | Изменить | Обновить | — |
| DEACTIVATE | Пометить | Обновить | Сбросить статус |

**Важно:** Если README папки не существует, он создаётся автоматически при создании первой инструкции в папке.

---

## Фаза CREATE

**Скилл:** /instruction-create

**Шаги:**
1. Получить путь
2. Fail-fast проверки
3. Проверить существование
4. Сгенерировать содержимое
5. Создать файл инструкции
6. **Создать/обновить README папки**
7. **Обновить главный README**
8. Ревью
9. Синхронизировать ссылки
10. Обновить контекст
11. Проверить соответствие проекта
12. Обновить связанные скиллы
13. Результат

**Подробности:** [instruction-create/SKILL.md](/.claude/skills/instruction-create/SKILL.md)

---

## Фаза UPDATE

**Скилл:** /instruction-update

**Шаги:**
1. Получить путь
2. Определить зону ответственности
3. Найти файлы в зоне
4. Извлечь правила
5. Проверить файлы
6. Сформировать список несоответствий
7. Внести изменения в инструкцию
8. **Обновить README папки**
9. Обновить контекст скиллов
10. Проверить тесты
11. Результат

**Подробности:** [instruction-update/SKILL.md](/.claude/skills/instruction-update/SKILL.md)

---

## Фаза DEACTIVATE

**Скилл:** /instruction-deactivate

**Когда использовать:** Инструкция не используется в проекте.

**Принцип:** Инструкции НЕ удаляются. Они деактивируются.

**Шаги:**
1. Получить путь
2. Проверить существование
3. Прочитать содержимое
4. Добавить предупреждение
5. Закомментировать содержимое
6. Сохранить файл
7. **Обновить README папки**
8. **Сбросить статус в главном README**
9. Результат

**Что происходит при деактивации:**
- Файл остаётся (не удаляется)
- Frontmatter сохраняется
- Содержимое комментируется: `<!-- ... -->`
- Добавляется предупреждение: `> **ВАЖНО:** В проекте не используется...`

**Пример:** [shared/i18n.md](../shared/i18n.md)

---

## Граф зависимостей

```
instruction-create
    |-> README папки (создать/обновить)
    |-> Главный README (обновить статус)
    |-> links-update
    |-> context-update
    |-> instruction-update
    |-> skill-create (опционально)

instruction-update
    |-> README папки (обновить)
    |-> context-update
    |-> test-update

instruction-deactivate
    |-> README папки (обновить)
    |-> Главный README (сбросить статус)
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/instruction-create](/.claude/skills/instruction-create/SKILL.md) | Фаза CREATE |
| [/instruction-update](/.claude/skills/instruction-update/SKILL.md) | Фаза UPDATE |
| [/instruction-deactivate](/.claude/skills/instruction-deactivate/SKILL.md) | Фаза DEACTIVATE |

---

## Связанные инструкции

- [statuses.md](./statuses.md) — система статусов
- [patterns.md](./patterns.md) — паттерны поиска ссылок
