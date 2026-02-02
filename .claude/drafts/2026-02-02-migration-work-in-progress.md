---
description: Рабочий драфт миграции — текущее состояние работы
type: work-in-progress
status: active
created: 2026-02-02
standard: .claude/.instructions/drafts/standard-draft.md
standard-version: v1.1
---

# Миграция стандартов — рабочий драфт

## Контекст

Выполняется последовательная миграция стандартов с полной проверкой:
- Level 1 документов (содержание, не только версия)
- Скриптов (реализация проверок)
- Скиллов (соответствие SSOT)

**SSOT миграции:** [create-migration.md](/.instructions/migration/create-migration.md)

**Правило добавлено в:** `.claude/rules/core.md` — обязательные 9 шагов миграции

---

## Завершённые миграции

### ✅ standard-principles.md v1.1

| Элемент | Статус | Изменения |
|---------|--------|-----------|
| validation-principles.md | ✅ v1.1 | Шаги 1-8 покрывают §1-§8 |
| validate-principles.py | ✅ Обновлён | Добавлены P002 (DRY), P003 (YAGNI), рефакторинг `parse_functions()` |
| validate-script.py | ✅ Обновлён | Импортирует `check_principles()` из validate-principles.py (DRY) |
| /principles-validate | ✅ Соответствует | — |

**Проверка:** `python .instructions/.scripts/check-version-drift.py .instructions/standard-principles.md` → 0 расхождений

---

## В процессе

### 🔄 standard-links.md v1.1

**Статус:** Читаю скрипты

**Стандарт содержит:** 13 секций (§1-§13)

**validation-links.md:** Уже обновлён до v1.1, содержит шаги 1-14

| Шаг | Секция стандарта | Коды ошибок |
|-----|------------------|-------------|
| 1-8 | §1-§7 (базовые) | E001-E013, W001-W005 |
| 9 | §8 Ссылки на строки кода | E014, E015, W006 |
| 10 | §9 Ссылки в блоках кода | — (пропуск) |
| 11 | §10 Ссылки между репозиториями | W007 |
| 12 | §11 Lifecycle ссылок | W008 |
| 13 | §12 Автогенерируемые файлы | — |
| 14 | §13 Граф зависимостей | E016, W009 |

**Что проверить:**

| Элемент | Путь | Что проверить |
|---------|------|---------------|
| validate-links.py | .structure/.instructions/.scripts/validate-links.py | Реализованы ли E001-E016, W001-W009? |
| update-skill-refs.py | .structure/.instructions/.scripts/update-skill-refs.py | Соответствует §11 Lifecycle? |
| /links-validate | .claude/skills/links-validate/SKILL.md | Соответствует validation-links.md? |

---

### ⏳ standard-readme.md v1.1

**Статус:** Ожидает

**Level 1 документы:**
- validation-structure.md
- create-structure.md
- modify-structure.md

**Скрипты (8 штук):**
- validate-structure.py
- validate.py
- generate-readme.py
- ssot.py
- mirror-instructions.py
- find-references.py
- mark-deleted.py
- update-skill-refs.py

**Скиллы (3 штуки):**
- /structure-create
- /structure-modify
- /structure-validate

---

## Оставшиеся миграции (из 2026-02-02-migration-status.md)

| Стандарт | Level 1 | Level 2 |
|----------|---------|---------|
| standard-instruction.md v1.2 | 3 файла | 43 файла |
| standard-script.md v1.1 | 3 файла | — |
| standard-skill.md v1.1 | 3 файла | 23 файла |
| standard-rule.md v1.1 | 3 файла | 4 файла |
| standard-agent.md v1.2 | 3 файла | 2 файла |
| standard-draft.md v1.1 | 1 файл | — |

---

## Команды проверки

```bash
# Проверить конкретный стандарт
python .instructions/.scripts/check-version-drift.py <путь-к-стандарту>

# Проверить все
python .instructions/.scripts/check-version-drift.py
```

---

## История

| Время | Действие |
|-------|----------|
| — | Добавлено правило миграции в core.md |
| — | ✅ Миграция standard-principles.md завершена |
| — | 🔄 Начата миграция standard-links.md |
