# Миграционная стратегия стандартов

Стандарт миграции при обновлении стандартов проекта.

## Оглавление

- [Контекст](#контекст)
- [Архитектура решения](#архитектура-решения)
- [Стандарт миграции](#стандарт-миграции)
  - [standard-migration.md](#standard-migrationmd)
  - [validation-migration.md](#validation-migrationmd)
  - [create-migration.md](#create-migrationmd)
- [Скиллы и правила](#скиллы-и-правила)
- [Pre-commit хук](#pre-commit-хук)
- [Текущие инструменты](#текущие-инструменты)
- [Специфика по типам объектов](#специфика-по-типам-объектов)
- [План реализации](#план-реализации)
- [Решения](#решения)

---

## Контекст

**Задача:** Создать стандарт миграции для обновления зависимых файлов при изменении стандартов.

**Проблема:**

При изменении `standard-*.md` возникает каскад:

```
standard-{object}.md (vX.Y → vX.Z)
         │
         ▼ Уровень 1: Связанные документы (инструкции для объекта)
┌────────┴────────────────────────────┐
│ validation-{object}.md             │
│ create-{object}.md                 │  ← должны обрабатывать новую версию
│ modify-{object}.md                 │
└────────┬────────────────────────────┘
         │
         ▼ Уровень 2: Экземпляры (созданные по стандарту)
┌────────┴────────────────────────────┐
│ Все файлы с:                       │
│ standard: <путь к стандарту>       │  ← должны соответствовать новой версии
└─────────────────────────────────────┘
```

**Текущее состояние:**
- Нет формального процесса миграции
- Скрипты обновляют только метаданные (версию), но не содержимое
- Нет проверки при коммите

---

## Архитектура решения

```
┌─────────────────────────────────────────────────────────────────┐
│                         СТАНДАРТ                                │
│  .instructions/standard-migration.md                            │
│  - Что такое миграция                                          │
│  - Два уровня обновления                                        │
│  - Формат отчёта о миграции                                     │
└─────────────────────────────────────────────────────────────────┘
         │
         ├──────────────────────┬──────────────────────┐
         ▼                      ▼                      ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐
│   ВАЛИДАЦИЯ     │  │    СОЗДАНИЕ     │  │    PRE-COMMIT       │
│                 │  │                 │  │                     │
│ validation-     │  │ create-         │  │ Хук проверяет:      │
│ migration.md    │  │ migration.md    │  │ - Изменился стандарт│
│                 │  │                 │  │ - Обновлены ли      │
│ Проверяет:      │  │ Шаги:           │  │   зависимые файлы?  │
│ - standard-ver  │  │ 1. Найти зав.   │  │ - Если нет → драфт  │
│   совпадает?    │  │ 2. Обновить L1  │  │                     │
│ - Экземпляры    │  │ 3. Обновить L2  │  │                     │
│   актуальны?    │  │ 4. Отчёт        │  │                     │
└────────┬────────┘  └────────┬────────┘  └──────────┬──────────┘
         │                    │                      │
         ▼                    ▼                      │
┌─────────────────┐  ┌─────────────────┐             │
│     СКИЛЛ       │  │     СКИЛЛ       │             │
│ /migration-     │  │ /migration-     │             │
│ validate        │  │ create          │             │
└────────┬────────┘  └────────┬────────┘             │
         │                    │                      │
         └────────────────────┴──────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │      RULE       │
                    │ standard-*.md   │
                    │ Напоминает о    │
                    │ миграции        │
                    └─────────────────┘
```

---

## Стандарт миграции

### standard-migration.md

**Расположение:** `.instructions/migration/standard-migration.md`

**Тип:** Стандарт процесса (без экземпляров)

**Содержание:**

```markdown
# Стандарт миграции

Версия стандарта: 1.0

Процесс обновления зависимых файлов при изменении стандартов.

## 1. Что такое миграция

Миграция — процесс приведения зависимых файлов в соответствие
с новой версией стандарта.

**Когда нужна миграция:**
- Изменился standard-*.md (увеличилась версия)
- Зависимые файлы ссылаются на старую версию

## 2. Два уровня обновления

### Уровень 1: Связанные документы

Файлы, которые РЕГЛАМЕНТИРУЮТ работу с объектом:
- validation-{object}.md
- create-{object}.md
- modify-{object}.md

**Что обновлять:** Шаги, чек-листы, примеры — чтобы соответствовали новой версии стандарта.

**Как обновлять:** `/modify-instruction`

### Уровень 2: Экземпляры

Файлы, СОЗДАННЫЕ по стандарту (имеют `standard: <путь>` в frontmatter).

**Что обновлять:** Структура, секции, формат — согласно новым требованиям.

**Как обновлять:** `/modify-{type}` (instruction, skill, agent, rule...)

## 3. Порядок миграции

1. Сначала Уровень 1 (связанные документы)
2. Затем Уровень 2 (экземпляры)

**Почему:** Нельзя обновлять экземпляры через modify-инструкцию,
которая сама устарела.

## 4. Формат отчёта о миграции

После миграции создаётся отчёт:

    ## Отчёт о миграции

    **Стандарт:** {путь} (v{старая} → v{новая})
    **Дата:** {дата}

    ### Уровень 1
    - ✅ validation-{object}.md
    - ✅ create-{object}.md
    - ✅ modify-{object}.md

    ### Уровень 2
    - ✅ {N} файлов обновлено
    - ⏭️ {M} файлов отложено (причина)

    ### Валидация
    - ✅ check-version-drift.py: 0 расхождений
```

---

### validation-migration.md

**Расположение:** `.instructions/migration/validation-migration.md`

**Содержание:**

```markdown
# Валидация миграции

Рабочая версия стандарта: 1.0

Проверка корректности миграции после обновления стандарта.

## Когда валидировать

- После изменения standard-*.md
- После выполнения /migration-create
- Перед коммитом (автоматически через хук)

## Шаги

### Шаг 1: Проверка версий стандарта

```bash
python .instructions/.scripts/check-version-drift.py <стандарт>
```

**Что проверяет:**
- Все файлы с `standard: <путь>` имеют актуальный `standard-version`

### Шаг 2: Проверка Уровня 1

Связанные документы (validation, create, modify) должны:
- Иметь `standard-version` = версии стандарта
- Содержать шаги, соответствующие новой версии

**Как проверить:**
```bash
python .instructions/.scripts/validate-instruction.py validation-{object}.md
python .instructions/.scripts/validate-instruction.py create-{object}.md
python .instructions/.scripts/validate-instruction.py modify-{object}.md
```

### Шаг 3: Проверка Уровня 2

Все экземпляры должны:
- Иметь `standard-version` = версии стандарта
- Соответствовать новым требованиям формата

**Как проверить:**
```bash
python .instructions/.scripts/check-version-drift.py <стандарт>
```

Для каждого файла с расхождением — `/validate-{type}`

## Чек-лист

- [ ] check-version-drift.py: 0 расхождений
- [ ] validation-{object}.md: валидация пройдена
- [ ] create-{object}.md: валидация пройдена
- [ ] modify-{object}.md: валидация пройдена
- [ ] Все экземпляры: standard-version актуален

## Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| standard-version устарел | Файл не обновлён после миграции | /modify-{type} |
| Структура не соответствует | Новые секции не добавлены | /modify-{type} |
| Уровень 1 не обновлён | Сначала обновить инструкции | /modify-instruction |
```

---

### create-migration.md

**Расположение:** `.instructions/migration/create-migration.md`

**Содержание:**

```markdown
# Воркфлоу миграции

Рабочая версия стандарта: 1.0

Процесс выполнения миграции при обновлении стандарта.

## Принципы

> **Миграция выполняется СРАЗУ после изменения стандарта.**

> **Порядок: сначала Уровень 1, затем Уровень 2.**

## Шаги

### Шаг 1: Определить изменённый стандарт

Какой standard-*.md был изменён?

```bash
# Показать изменения
git diff --name-only HEAD~1 | grep "standard-"
```

### Шаг 2: Проверить версию

Убедиться, что версия стандарта увеличена:

```bash
python .instructions/.scripts/bump-standard-version.py --check <стандарт>
```

Если версия не увеличена — увеличить.

### Шаг 3: Найти зависимые файлы

```bash
python .instructions/.scripts/check-version-drift.py <стандарт>
```

Вывод покажет:
- Уровень 1: связанные документы (validation, create, modify)
- Уровень 2: экземпляры

### Шаг 4: Обновить Уровень 1

Для каждого связанного документа:

```
/modify-instruction validation-{object}.md
/modify-instruction create-{object}.md
/modify-instruction modify-{object}.md
```

**Что обновлять:**
- standard-version в frontmatter
- Шаги, чек-листы — согласно изменениям в стандарте

### Шаг 5: Обновить Уровень 2

Для каждого экземпляра:

```
/modify-{type} <файл>
```

Где {type} определяется по стандарту:
- standard-instruction.md → /modify-instruction
- standard-skill.md → /modify-skill
- standard-agent.md → /modify-agent
- и т.д.

### Шаг 6: Валидация

```bash
python .instructions/.scripts/check-version-drift.py <стандарт>
```

Должно показать: 0 расхождений.

### Шаг 7: Отчёт

Вывести отчёт по шаблону из стандарта.

## Чек-лист

- [ ] Версия стандарта увеличена
- [ ] Уровень 1: все 3 файла обновлены
- [ ] Уровень 2: все экземпляры обновлены
- [ ] check-version-drift.py: 0 расхождений
- [ ] Отчёт сформирован

## Примеры

### Миграция standard-instruction.md

```bash
# 1. Проверить расхождения
python .instructions/.scripts/check-version-drift.py .instructions/standard-instruction.md

# 2. Обновить Уровень 1
/modify-instruction .instructions/validation-instruction.md
/modify-instruction .instructions/create-instruction.md
/modify-instruction .instructions/modify-instruction.md

# 3. Обновить Уровень 2 (все инструкции в проекте)
# Для каждого файла из списка расхождений:
/modify-instruction <файл>

# 4. Проверить
python .instructions/.scripts/check-version-drift.py .instructions/standard-instruction.md
```

---

## Скиллы и правила

### Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| `/migration-validate` | Проверить состояние миграции | validation-migration.md |
| `/migration-create` | Выполнить миграцию | create-migration.md |

**Файлы:**
- `.claude/skills/migration-validate/SKILL.md`
- `.claude/skills/migration-create/SKILL.md`

### Правило

**Файл:** `.claude/rules/standard-update.md`

```markdown
---
description: Напоминание о миграции при изменении стандарта
globs:
  - "**/standard-*.md"
---

# При изменении стандарта

> **После изменения этого файла требуется миграция.**

## Команды

    # Проверить состояние
    /migration-validate <стандарт>

    # Выполнить миграцию
    /migration-create <стандарт>

## Шаги

1. Убедиться, что версия увеличена
2. Обновить Уровень 1 (validation, create, modify)
3. Обновить Уровень 2 (экземпляры)
4. Проверить: `/migration-validate`
```

---

## Pre-commit хук

**Механизм:** Git pre-commit хук проверяет, нужна ли миграция.

**Файл:** `.git/hooks/pre-commit` (или через `.claude/settings.json`)

**Логика:**

```
1. Получить список изменённых файлов в коммите
2. Найти изменённые standard-*.md
3. Для каждого:
   a. Проверить: обновлены ли связанные документы (Уровень 1)?
   b. Проверить: обновлены ли экземпляры (Уровень 2)?
4. Если есть необновлённые файлы:
   a. Создать драфт .claude/drafts/YYYY-MM-DD-migration-pending.md
   b. Вывести предупреждение
   c. (Опционально) Заблокировать коммит
```

**Скрипт:** `.instructions/.scripts/pre-commit-migration-check.py`

```python
#!/usr/bin/env python3
"""
pre-commit-migration-check.py — Проверка миграции перед коммитом.

Проверяет, обновлены ли зависимые файлы при изменении стандартов.
Если нет — создаёт драфт с неучтёнными файлами.
"""

import subprocess
import sys
from pathlib import Path
from datetime import date

def get_staged_files():
    """Получить список файлов в staging."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True
    )
    return result.stdout.strip().split("\n")

def find_changed_standards(files):
    """Найти изменённые standard-*.md."""
    return [f for f in files if "standard-" in f and f.endswith(".md")]

def check_dependencies(standard_path):
    """Проверить, обновлены ли зависимые файлы."""
    result = subprocess.run(
        ["python", ".instructions/.scripts/check-version-drift.py",
         standard_path, "--check"],
        capture_output=True, text=True
    )
    return result.returncode == 0, result.stdout

def create_pending_draft(standards, pending_files):
    """Создать драфт с неучтёнными файлами."""
    today = date.today().isoformat()
    draft_path = Path(f".claude/drafts/{today}-migration-pending.md")

    content = f"""# Ожидающая миграция

**Дата:** {today}
**Статус:** Требуется миграция

## Изменённые стандарты

{chr(10).join(f"- {s}" for s in standards)}

## Неучтённые файлы

{chr(10).join(f"- {f}" for f in pending_files)}

## Что делать

Для каждого стандарта выполнить:

    /migration-create <стандарт>

Или вручную обновить файлы и выполнить:

    /migration-validate <стандарт>
"""

    draft_path.write_text(content, encoding="utf-8")
    return draft_path

def main():
    staged = get_staged_files()
    standards = find_changed_standards(staged)

    if not standards:
        sys.exit(0)  # Нет изменённых стандартов

    all_pending = []

    for standard in standards:
        ok, output = check_dependencies(standard)
        if not ok:
            # Парсим вывод, собираем неучтённые файлы
            all_pending.extend(parse_pending(output))

    if all_pending:
        draft = create_pending_draft(standards, all_pending)
        print(f"""
⚠️  МИГРАЦИЯ НЕ ЗАВЕРШЕНА

Изменены стандарты:
{chr(10).join(f"  • {s}" for s in standards)}

Не обновлены файлы: {len(all_pending)}

Создан драфт: {draft}

Для завершения миграции:
  /migration-create <стандарт>
""")
        # sys.exit(1)  # Раскомментировать для блокировки коммита

    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Интеграция с Claude Code:**

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python .instructions/.scripts/pre-commit-migration-check.py"
          }
        ]
      }
    ]
  }
}
```

**Или через git hooks:**

```bash
# .git/hooks/pre-commit
#!/bin/sh
python .instructions/.scripts/pre-commit-migration-check.py
```

---

## Текущие инструменты

| Скрипт | Назначение | Используется в |
|--------|------------|----------------|
| `check-version-drift.py` | Показать файлы с устаревшей версией | validation-migration, create-migration |
| `sync-standard-version.py` | Обновить standard-version в frontmatter | create-migration (опционально) |
| `bump-standard-version.py` | Увеличить версию стандарта | create-migration |
| `pre-commit-migration-check.py` | Проверка перед коммитом | pre-commit хук |

---

## Специфика по типам объектов

| Стандарт | Уровень 1 | Уровень 2 | Скилл для L2 |
|----------|-----------|-----------|--------------|
| standard-instruction.md | validation/create/modify-instruction | Все инструкции (~50) | /modify-instruction |
| standard-skill.md | validation/create/modify-skill | Все скиллы (~25) | /modify-skill |
| standard-agent.md | validation/create/modify-agent | Все агенты (~5) | /modify-agent |
| standard-rule.md | validation/create/modify-rule | Все rules (~10) | /modify-rule |
| standard-readme.md | — | Все README (~30) | Вручную |
| standard-draft.md | validation-draft | Все drafts | Вручную |

---

## План реализации

| # | Задача | Скилл | Статус |
|---|--------|-------|--------|
| 0 | Создать папку `.instructions/migration/` | `/structure-create` | ✅ |
| 1 | Создать `standard-migration.md` | `/instruction-create` | ✅ |
| 2 | Создать `validation-migration.md` | `/instruction-create` | ✅ |
| 3 | Создать `create-migration.md` | `/instruction-create` | ✅ |
| 4 | Создать скилл `/migration-validate` | `/skill-create` | ✅ |
| 5 | Создать скилл `/migration-create` | `/skill-create` | ✅ |
| 6 | Создать rule `standard-update.md` | `/rule-create` | ✅ |
| 7 | Создать `check-version-drift.py` | `/script-create` | ❌ |
| 8 | Создать `pre-commit-migration-check.py` | `/script-create` | ❌ |
| 9 | Интегрировать git pre-commit hook | Bash | ❌ |

**Зависимости:**
- 0 → 1, 2, 3 (папка сначала)
- 1 → 2, 3 (стандарт сначала)
- 2 → 4 (инструкция → скилл)
- 3 → 5 (инструкция → скилл)
- 1, 2, 3 → 6 (rule после инструкций)
- 7 → 8 (скрипт drift → pre-commit)

---

## Решения

| # | Вопрос | Решение |
|---|--------|---------|
| 1 | Pre-commit: блокировать коммит? | ✅ Только предупреждение (создаёт драфт) |
| 2 | Драфт: автоудаление после миграции? | ✅ Вручную (пользователь удаляет) |
| 3 | Уровень 2: массово или по одному? | ✅ Выбор пользователя (скилл спрашивает) |
| 4 | Где modify-migration.md? | ✅ Не нужен (миграция одноразовая) |
| 5 | Расположение файлов? | ✅ `.instructions/migration/` |
| 6 | check-version-drift.py? | ✅ Создать новый |
| 7 | Pre-commit механизм? | ✅ Git hook (.git/hooks/pre-commit) |
| 8 | standard-migration.md? | ✅ Стандарт процесса (без экземпляров) |
| 9 | validation/create-migration.md? | ✅ Инструкции по standard-instruction.md |
| 10 | Скрипты куда? | ✅ `.instructions/.scripts/` |
| 11 | Формат check-version-drift? | ✅ JSON |
