---
type: standard
description: Примеры использования скиллов skill-*
governed-by: skills/README.md
related:
  - skills/workflow.md
  - skills/rules.md
---

# Примеры: Скиллы

Примеры использования скиллов для управления скиллами Claude Code.

**Полезные ссылки:**
- [Инструкции для скиллов](./README.md)
- [Claude Code окружение](../README.md)

## Оглавление

- [skill-create](#skill-create)
- [skill-update](#skill-update)
- [skill-delete](#skill-delete)
- [skill-migrate](#skill-migrate)
- [Скиллы](#скиллы)

---

## skill-create

### Пример 1: Базовое создание

**Команда:**
```
/skill-create agent-create
```

**Результат:**
```
✅ Все предварительные проверки пройдены

Название: agent-create
Формат: ✅ {объект}-{действие}

Категория: agent-management
Описание: Создание нового агента по шаблону

Подтвердить? [Y/n]

✅ Скилл создан: /.claude/skills/agent-create/SKILL.md

Индекс обновлён: /.claude/skills/README.md
```

### Пример 2: Обнаружено пересечение

**Команда:**
```
/skill-create file-create
```

**Результат:**
```
⚠️ Обнаружено пересечение функциональности

Существующие скиллы с похожим назначением:
- doc-create — создание документа
- instruction-create — создание инструкции

Варианты:
1. Продолжить (разные области применения)
2. Использовать существующий скилл
3. Изменить название

Выберите [1/2/3]:
```

### Пример 3: Режим --dry-run

**Команда:**
```
/skill-create my-skill --dry-run
```

**Результат:**
```
📋 Предварительный просмотр

Будет создано:
- /.claude/skills/my-skill/SKILL.md

Будет обновлено:
- /.claude/skills/README.md

Будет вызвано:
- /links-update
- /skill-update

ℹ️ Изменения НЕ применены
```

---

## skill-update

### Пример 1: Интеграция нового скилла

**Команда:**
```
/skill-update issue-review
```

**Результат:**
```
📋 Предложения по интеграции скилла issue-review

Проанализировано: 18 скиллов
Применимых: 2

📄 issue-execute — Шаг 5 (Завершение)
   Польза: Ревью перед закрытием Issue

📄 issue-complete — Шаг 1 (Проверка)
   Польза: Убедиться в прохождении ревью

Применить? [Y/n/выборочно]

✅ Обновлено: 2 скилла
```

### Пример 2: Нет применимых

**Команда:**
```
/skill-update prompt-update
```

**Результат:**
```
📋 Анализ интеграции скилла prompt-update

Проанализировано: 18 скиллов
Применимых: 0

ℹ️ Интеграция не требуется
```

### Пример 3: Выборочное применение

**Команда:**
```
/skill-update context-update
```

**Результат:**
```
📋 Предложения по интеграции

📄 skill-create — Шаг 9
[1] Применить  [2] Пропустить
> 1

📄 doc-create — Шаг 5
[1] Применить  [2] Пропустить
> 2

✅ Обновлено: 1
Пропущено: 1
```

---

## skill-delete

### Пример 1: Удаление с несколькими ссылками

**Команда:**
```
/skill-delete links-validate
```

**Результат:**
```
📋 Очистка ссылок на links-validate

Найдено: 5 ссылок в 3 файлах

📄 skill-create/SKILL.md — 2 ссылки
📄 instruction-create/SKILL.md — 2 ссылки
📄 context-update/SKILL.md — 1 ссылка

Удалить ссылки? [Y/n]

✅ Ссылки удалены

Обновлено: 3 файла
```

### Пример 2: Скилл ещё существует

**Команда:**
```
/skill-delete context-sync
```

**Результат:**
```
⚠️ Скилл context-sync ещё существует!

Путь: /.claude/skills/context-sync/SKILL.md

Варианты:
1. Удалить скилл и очистить ссылки
2. Отменить операцию

> 2

Операция отменена.
```

### Пример 3: Удаление из агента

**Команда:**
```
/skill-delete links-validate
```

**Результат:**
```
📄 doc-writer.md (агент)
   skills: [doc-create, links-validate, context-update]
   → skills: [doc-create, context-update]

✅ Обновлено: 1 агент
```

---

## skill-migrate

### Пример 1: Переименование скилла

**Команда:**
```
/skill-migrate my-old-skill my-new-skill
```

**Результат:**
```
⚠️ Миграция скилла

Было: /my-old-skill
Станет: /my-new-skill

Будет изменено: 5 файлов
- /.claude/skills/README.md
- /.claude/skills/other-skill/SKILL.md
- /.claude/.instructions/skills/examples.md
...

Продолжить? [Y/n]

✅ Скилл мигрирован

Было: /my-old-skill
Стало: /my-new-skill

Обновлено: 5 файлов
```

### Пример 2: Изменение категории

**Команда:**
```
/skill-migrate utility-skill --category documentation
```

**Результат:**
```
✅ Категория изменена

Было: utility
Стало: documentation

Обновлено: /.claude/skills/README.md
```

### Пример 3: Предварительный просмотр

**Команда:**
```
/skill-migrate my-skill new-name --dry-run
```

**Результат:**
```
📋 Предварительный просмотр

Будет переименовано:
- /.claude/skills/my-skill/ → /.claude/skills/new-name/

Будет обновлено:
- /.claude/skills/README.md
- /.claude/skills/other-skill/SKILL.md

ℹ️ Изменения НЕ применены
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/skill-create](/.claude/skills/skill-create/SKILL.md) | Создание нового скилла |
| [/skill-update](/.claude/skills/skill-update/SKILL.md) | Интеграция в существующие |
| [/skill-delete](/.claude/skills/skill-delete/SKILL.md) | Удаление и очистка ссылок |
| [/skill-migrate](/.claude/skills/skill-migrate/SKILL.md) | Переименование скилла |
