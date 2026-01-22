---
type: standard
description: Жизненный цикл ссылок: CREATE, UPDATE, DELETE, VALIDATE
governed-by: instructions/README.md
related:
  - links/format.md
  - links/edge-cases.md
---

# Жизненный цикл ссылок

Фазы работы со ссылками: создание, обновление, удаление, валидация.

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [links/README.md](./README.md)

## Оглавление

- [Диаграмма](#диаграмма)
- [Фаза CREATE](#фаза-create)
- [Фаза UPDATE](#фаза-update)
- [Фаза DELETE](#фаза-delete)
- [Фаза VALIDATE](#фаза-validate)
- [Отличие от context-update](#отличие-от-context-update)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Диаграмма

```
Упоминание → CREATE → Ссылка → UPDATE → Ссылка (новый путь)
                                 ↓
                              DELETE → Пометка → UPDATE → Восстановлено
                                                    ↓
                                            (или удалить вручную)
```

| Фаза | Скилл | Триггер | Результат |
|------|-------|---------|-----------|
| CREATE | links-create | Новый документ | `text` → `[text](path)` |
| UPDATE | links-update | Переименование файла | Путь обновлён |
| DELETE | links-delete | Удаление файла | `[text](path)` → `text *(удалена)*` |
| VALIDATE | links-validate | Аудит | Отчёт о битых ссылках |

---

## Фаза CREATE

**Скилл:** /links-create

**Когда:** В документе есть упоминания файлов, которые не оформлены как ссылки.

**Шаги:**
1. Найти упоминания файлов/папок
2. Исключить: блоки кода, bash-команды, URL
3. Проверить существование каждого файла
4. Оформить как ссылку: `[имя](путь)`

**Пример:**
```diff
- Настройки в /.claude/settings.json
+ Настройки в [settings.json](/.claude/settings.json)
```

**Подробности:** [links-create/SKILL.md](/.claude/skills/links-create/SKILL.md)

---

## Фаза UPDATE

**Скилл:** /links-update

**Когда:** Файл/папка переименован(а) или перемещён(а).

**Шаги:**
1. Найти все ссылки на старый путь
2. Найти помеченные ссылки (если есть)
3. Обновить путь в ссылках
4. Восстановить помеченные (опционально)

**Вызов:**
```
/links-update /new/path.md --old-name /old/path.md
```

**Восстановление помеченных:**
```diff
- config.yaml *(ссылка удалена: /config/old.yaml)*
+ [config.yaml](/config/new.yaml)
```

**Подробности:** [links-update/SKILL.md](/.claude/skills/links-update/SKILL.md)

---

## Фаза DELETE

**Скилл:** /links-delete

**Когда:** Файл/папка удалён(а).

**Принцип:** НЕ удаляем контент. Помечаем для возможного восстановления.

**Шаги:**
1. Найти все ссылки на удалённый путь
2. Показать diff для подтверждения
3. Заменить ссылки на пометки

**Пример:**
```diff
- [config.yaml](/config/config.yaml)
+ config.yaml *(ссылка удалена: /config/config.yaml)*
```

**Режим --scan-all:** Аудит всех битых ссылок в проекте.

**Подробности:** [links-delete/SKILL.md](/.claude/skills/links-delete/SKILL.md)

---

## Фаза VALIDATE

**Скилл:** /links-validate

**Когда:** Проверка целостности документации.

**Шаги:**
1. Найти все markdown-файлы
2. Извлечь все ссылки
3. Проверить существование целей
4. Сформировать отчёт

**Режим --fix:** Автоматические предложения по исправлению (fuzzy match).

**Подробности:** [links-validate/SKILL.md](/.claude/skills/links-validate/SKILL.md)

---

## Отличие от context-update

| Аспект | links-update | context-update |
|--------|--------------|----------------|
| **Цель** | Обновить синтаксис `[text](path)` | Обновить семантику |
| **Что меняет** | Пути в ссылках | Описания, связи |
| **Глубина** | Прямые ссылки | Транзитивные (A→B→C) |
| **Когда** | Путь изменился | Смысл изменился |

**Правило выбора:**
- Изменился только путь → `/links-update`
- Изменился смысл/роль → `/context-update`
- Изменилось и то и другое → оба скилла

---

## Скиллы

| Скилл | Фаза |
|-------|------|
| [/links-create](/.claude/skills/links-create/SKILL.md) | CREATE |
| [/links-update](/.claude/skills/links-update/SKILL.md) | UPDATE |
| [/links-delete](/.claude/skills/links-delete/SKILL.md) | DELETE |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | VALIDATE |

---

## Связанные инструкции

- [format.md](./format.md) — форматы ссылок
- [edge-cases.md](./edge-cases.md) — граничные случаи
