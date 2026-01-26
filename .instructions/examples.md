---
type: standard
description: Примеры использования скиллов instruction-*
governed-by: instructions/README.md
related:
  - instructions/workflow.md
  - instructions/validation.md
---

# Примеры: Инструкции

Примеры использования скиллов для управления инструкциями проекта.

**Полезные ссылки:**
- [Инструкции для .instructions](./README.md)

## Оглавление

- [instruction-create](#instruction-create)
- [instruction-update](#instruction-update)
- [instruction-deactivate](#instruction-deactivate)
- [Правила examples.md](#правила-examplesmd)
- [Скиллы](#скиллы)

---

## instruction-create

### Пример 1: Создание новой инструкции

**Команда:**
```
/instruction-create .claude/.instructions/git/review.md
```

**Результат:**
```
📋 Создание инструкции

Путь: /.claude/.instructions/git/review.md
Папка: git/ (существует)
Тип: standard

Описание: Правила проведения code review
governed-by: git/README.md

Подтвердить? [Y/n]

✅ Инструкция создана

Файл: /.claude/.instructions/git/review.md
Тип: standard
Статус: добавлена в README.md
```

### Пример 2: Путь не существует

**Команда:**
```
/instruction-create .claude/.instructions/new-area/rules.md
```

**Результат:**
```
⚠️ Папка new-area/ не существует

Варианты:
1. Создать папку new-area/ и инструкцию
2. Выбрать существующую папку
3. Отменить

> 1

✅ Создано:
- /.claude/.instructions/new-area/README.md
- /.claude/.instructions/new-area/rules.md
```

### Пример 3: Режим --dry-run

**Команда:**
```
/instruction-create .claude/.instructions/config/env.md --dry-run
```

**Результат:**
```
📋 Предварительный просмотр

Будет создано:
- /.claude/.instructions/config/env.md

Будет обновлено:
- /.claude/.instructions/config/README.md (статус)
- /.claude/.instructions/README.md (счётчик)

ℹ️ Изменения НЕ применены
```

---

## instruction-update

### Пример 1: Проверка соответствия

**Команда:**
```
/instruction-update .claude/.instructions/git/commits.md
```

**Результат:**
```
🔍 Проверка соответствия проекта инструкции

Инструкция: git/commits.md
Тип: standard

Проверено: 12 файлов
✅ Соответствует: 10
⚠️ Требует внимания: 2

📄 src/services/auth/handler.py
   Строка 45: commit message не соответствует формату

📄 scripts/deploy.sh
   Строка 12: отсутствует type в commit

Исправить? [Y/n/выборочно]
```

### Пример 2: Всё соответствует

**Команда:**
```
/instruction-update .claude/.instructions/src/api/versioning.md
```

**Результат:**
```
🔍 Проверка соответствия

Инструкция: src/api/versioning.md
Проверено: 8 файлов

✅ Все файлы соответствуют инструкции
```

### Пример 3: После изменения инструкции

**Команда:**
```
/instruction-update .claude/.instructions/tests/unit.md --changed
```

**Результат:**
```
🔍 Проверка после изменения инструкции

Изменено: секция "Naming convention"

Затронутые файлы: 24
Требуют обновления: 5

📄 tests/auth/test_login.py — имя файла
📄 tests/auth/test_logout.py — имя файла
...

Обновить? [Y/n]
```

---

## instruction-deactivate

### Пример 1: Деактивация инструкции

**Команда:**
```
/instruction-deactivate .claude/.instructions/deprecated/old-api.md
```

**Результат:**
```
⚠️ Деактивация инструкции

Файл: deprecated/old-api.md

Ссылки на инструкцию: 3
- skills/api-create/SKILL.md
- instructions/src/api/README.md
- doc/migration.md

Варианты:
1. Деактивировать и обновить ссылки
2. Отменить

> 1

✅ Инструкция деактивирована

Помечено: 3 ссылки
Статус: ⬜ в README.md
```

### Пример 2: Нет ссылок

**Команда:**
```
/instruction-deactivate .claude/.instructions/tests/deprecated-format.md
```

**Результат:**
```
✅ Деактивация инструкции

Файл: tests/deprecated-format.md
Ссылок: 0

Статус обновлён: ⬜ в README.md
```

### Пример 3: Режим --dry-run

**Команда:**
```
/instruction-deactivate .claude/.instructions/platform/old-deploy.md --dry-run
```

**Результат:**
```
📋 Предварительный просмотр

Будет деактивировано:
- /.claude/.instructions/platform/old-deploy.md

Будет помечено:
- 2 ссылки в 2 файлах

ℹ️ Изменения НЕ применены
```

---

## Правила examples.md

Каждая папка инструкций должна иметь файл `examples.md`:

| Условие | Содержимое examples.md |
|---------|------------------------|
| Есть скиллы для папки | Примеры использования скиллов |
| Нет скиллов для папки | Заглушка с пояснением |

### Структура файла

```markdown
---
type: standard
description: Примеры использования скиллов {область}
governed-by: {область}/README.md
---

# Примеры: {Область}

## {skill-name}

### Пример 1: {Сценарий}
...
```

### Заглушка (нет скиллов)

```markdown
# Примеры: {Область}

**Скиллы для этой области отсутствуют.**

Примеры будут добавлены после создания скиллов.
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/instruction-create](/.claude/skills/instruction-create/SKILL.md) | Создание инструкции |
| [/instruction-update](/.claude/skills/instruction-update/SKILL.md) | Проверка соответствия проекта |
| [/instruction-deactivate](/.claude/skills/instruction-deactivate/SKILL.md) | Деактивация инструкции |
