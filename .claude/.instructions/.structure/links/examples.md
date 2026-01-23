---
type: standard
description: Примеры использования скиллов links-*
governed-by: links/README.md
related:
  - links/workflow.md
  - links/format.md
---

# Примеры: Ссылки

Примеры использования скиллов для работы со ссылками в документах.

**Индекс:** [/.claude/.instructions/README.md](/.claude/.instructions/README.md) | **Папка:** [links/README.md](./README.md)

## Оглавление

- [links-create](#links-create)
- [links-update](#links-update)
- [links-delete](#links-delete)
- [links-validate](#links-validate)
- [Скиллы](#скиллы)

---

## links-create

### Пример 1: Оформление упоминаний в документе

**Команда:**
```
/links-create doc/architecture.md
```

**До:**
```markdown
Код хранится в src/services/auth/.
Конфигурация в config/auth.yaml.
```

**После:**
```markdown
Код хранится в [src/services/auth/](../../src/services/auth/).
Конфигурация в [config/auth.yaml](../../config/auth.yaml).
```

**Результат:**
```
✅ Ссылки созданы в doc/architecture.md

Оформлено: 2
Не найдено: 0
Пропущено (код): 0
```

### Пример 2: Пропуск блоков кода

**Команда:**
```
/links-create README.md
```

**Результат:**
```
✅ Ссылки созданы в README.md

Оформлено: 5
Не найдено: 1 (old_config.yaml)
Пропущено (код): 3
```

---

## links-update

### Пример 1: После создания файла

**Команда:**
```
/links-update .claude/.instructions/skills/examples.md
```

**Результат:**
```
✅ Ссылки обновлены для examples.md

Обновлено: 3
- skills/README.md — добавлена ссылка
- skill-create/SKILL.md — добавлена ссылка
- skill-update/SKILL.md — добавлена ссылка

Без изменений: 12
```

### Пример 2: После переименования

**Команда:**
```
/links-update .claude/skills/test-run --old-name test-execute
```

**Результат:**
```
✅ Ссылки обновлены для test-run

Обновлено: 8
- skills/README.md — test-execute → test-run
- test-create/SKILL.md — test-execute → test-run
- issue-complete/SKILL.md — test-execute → test-run
...

Восстановлено помеченных: 2
```

### Пример 3: Предварительный просмотр

**Команда:**
```
/links-update doc/api/ --dry-run
```

**Результат:**
```
📋 Предварительный просмотр

Будет обновлено: 5 файлов
- doc/README.md (строка 45)
- .claude/.instructions/src/api/README.md (строка 12)
...

ℹ️ Изменения НЕ применены
```

---

## links-delete

### Пример 1: Пометка после удаления файла

**Команда:**
```
/links-delete .claude/skills/old-skill
```

**Результат:**
```
✅ Ссылки помечены для old-skill

Найдено: 4 ссылки в 3 файлах

Помечено:
- skills/README.md:45 — [old-skill] → ~~[old-skill]~~ <!-- DELETED -->
- doc-create/SKILL.md:28 — [old-skill] → ~~[old-skill]~~ <!-- DELETED -->
```

### Пример 2: Подтверждение удаления

**Команда:**
```
/links-delete src/deprecated/
```

**Результат:**
```
⚠️ Найдено 12 ссылок на src/deprecated/

📄 doc/architecture.md — 3 ссылки
📄 CLAUDE.md — 1 ссылка
📄 README.md — 2 ссылки

Пометить как удалённые? [Y/n]
```

---

## links-validate

### Пример 1: Проверка всего проекта

**Команда:**
```
/links-validate
```

**Результат:**
```
🔍 Валидация ссылок проекта

Проверено: 245 файлов, 1,847 ссылок

❌ Битые ссылки: 3
- doc/api.md:45 → src/old-service/ (не существует)
- README.md:12 → doc/deprecated.md (не существует)
- .claude/skills/test/SKILL.md:8 → /missing.md (не существует)

⚠️ Помеченные: 2
- skills/README.md:67 — ~~[old-skill]~~ <!-- DELETED -->

✅ Валидные: 1,842
```

### Пример 2: Проверка с автоисправлением

**Команда:**
```
/links-validate --fix
```

**Результат:**
```
🔍 Валидация ссылок (режим --fix)

Проверено: 245 файлов

❌ Битые: 3 → Помечены как <!-- DELETED -->
⚠️ Помеченные: 2 → Без изменений
✅ Валидные: 1,842

Исправлено: 3 ссылки
```

### Пример 3: Проверка папки

**Команда:**
```
/links-validate .claude/skills/
```

**Результат:**
```
🔍 Валидация ссылок в .claude/skills/

Проверено: 32 файла, 156 ссылок

✅ Все ссылки валидны
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/links-create](/.claude/skills/links-create/SKILL.md) | Создание ссылок в документе |
| [/links-update](/.claude/skills/links-update/SKILL.md) | Обновление при переименовании |
| [/links-delete](/.claude/skills/links-delete/SKILL.md) | Пометка битых ссылок |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Валидация ссылок проекта |
