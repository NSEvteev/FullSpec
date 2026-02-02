---
description: Отчёт о состоянии миграций в проекте
type: research
status: active
created: 2026-02-02
standard: .claude/.instructions/drafts/standard-draft.md
standard-version: v1.1
---

# Состояние миграций в проекте

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Резюме](#резюме)
  - [Расхождения Level 1](#расхождения-level-1)
  - [Расхождения Level 2](#расхождения-level-2-по-стандартам)
  - [Рекомендации](#4-рекомендации)
  - [История изменений](#5-история-изменений)

---

## Контекст

Черновик создан для отслеживания состояния миграций в проекте. Содержит полный список стандартов и зависимых файлов с их текущими версиями.

**Зачем:** Быстрый обзор того, какие инструкции требуют миграции при обновлении стандартов.

---

## Содержание

### Резюме

**Статус:** Обнаружены расхождения Level 1 и Level 2

**Расхождений Level 1:** 13 файлов (validation/create/modify)

**Расхождений Level 2:** 73 файла (экземпляры)

---

### Исправленные скрипты

**check-version-drift.py:**
- Исправлен баг с `lstrip("./")` → `.claude/` больше не превращается в `claude/`
- Добавлена проверка Level 1 ("Рабочая версия стандарта")
- Вывод разделён на Level 1 и Level 2

**bump-standard-version.py:**
- Добавлен флаг `--check` для показа версии без изменения

---

### Расхождения Level 1

| Стандарт | Версия | Файл с расхождением | Текущая |
|----------|--------|---------------------|---------|
| standard-instruction.md | v1.2 | validation-instruction.md | v1.0 |
| standard-instruction.md | v1.2 | create-instruction.md | v1.0 |
| standard-instruction.md | v1.2 | modify-instruction.md | v1.0 |
| standard-script.md | v1.1 | validation-script.md | v1.0 |
| standard-script.md | v1.1 | create-script.md | v1.0 |
| standard-script.md | v1.1 | modify-script.md | v1.0 |
| ~~standard-principles.md~~ | ~~v1.1~~ | ~~validation-principles.md~~ | ✅ v1.1 |
| ~~standard-links.md~~ | ~~v1.1~~ | ~~validation-links.md~~ | ✅ v1.1 |
| ~~standard-readme.md~~ | ~~v1.1~~ | ~~validation-structure.md~~ | ✅ v1.1 |
| ~~standard-readme.md~~ | ~~v1.1~~ | ~~create-structure.md~~ | ✅ v1.1 |
| ~~standard-readme.md~~ | ~~v1.1~~ | ~~modify-structure.md~~ | ✅ v1.1 |
| standard-skill.md | v1.1 | validation-skill.md | v1.0 |
| standard-skill.md | v1.1 | create-skill.md | v1.0 |
| standard-skill.md | v1.1 | modify-skill.md | v1.0 |
| standard-rule.md | v1.1 | validation-rule.md | v1.0 |
| standard-rule.md | v1.1 | create-rule.md | v1.0 |
| standard-rule.md | v1.1 | modify-rule.md | v1.0 |
| standard-agent.md | v1.2 | validation-agent.md | v1.1 |
| standard-agent.md | v1.2 | create-agent.md | v1.1 |
| standard-agent.md | v1.2 | modify-agent.md | v1.1 |
| standard-draft.md | v1.1 | validation-draft.md | v1.0 |

---

### Расхождения Level 2 (по стандартам)

| Стандарт | Версия | Кол-во расхождений |
|----------|--------|-------------------|
| ~~standard-readme.md~~ | ~~v1.1~~ | ~~19 файлов~~ ✅ |
| standard-instruction.md | v1.2 | 43 файла |
| standard-agent.md | v1.2 | 2 файла |
| standard-rule.md | v1.1 | 4 файла |
| standard-skill.md | v1.1 | 23 файла |
| standard-state.md | v1.1 | 1 файл |

**Итого Level 2:** 73 файла (было 92, мигрировано 19)

**Команда для полного списка:**
```bash
python .instructions/.scripts/check-version-drift.py
```

---

## 4. Рекомендации

### 4.1. Выполнить миграцию

**Порядок:**
1. Сначала Level 1 (validation/create/modify) — через `/migration-create`
2. Затем Level 2 (экземпляры)

```bash
# Миграция по стандартам (Level 1 + Level 2)
/migration-create .instructions/standard-instruction.md
/migration-create .instructions/standard-script.md
/migration-create .claude/.instructions/skills/standard-skill.md
/migration-create .claude/.instructions/rules/standard-rule.md
/migration-create .claude/.instructions/agents/standard-agent.md
/migration-create .claude/.instructions/drafts/standard-draft.md
# ✅ /migration-create .structure/.instructions/standard-links.md
# ✅ /migration-create .structure/.instructions/standard-readme.md
```

### 4.2. Мониторинг

```bash
# Проверить Level 1 + Level 2
python .instructions/.scripts/check-version-drift.py

# Проверить конкретный стандарт
python .instructions/.scripts/check-version-drift.py .instructions/standard-instruction.md
```

---

## 5. История изменений

| Дата | Действие |
|------|----------|
| 2026-02-02 | Создан отчёт |
| 2026-02-02 | Исправлен баг lstrip в check-version-drift.py |
| 2026-02-02 | Обнаружено: 18 Level 1 + 92 Level 2 = 110 расхождений |
| 2026-02-02 | check-version-drift.py: добавлена проверка Level 1 |
| 2026-02-02 | bump-standard-version.py: добавлен флаг --check |
| 2026-02-02 | ✅ Миграция standard-principles.md выполнена (17 Level 1 осталось) |
| 2026-02-02 | ✅ Миграция standard-links.md выполнена (Level 1: validation-links.md + 6 новых шагов) |
| 2026-02-02 | ✅ Миграция standard-readme.md выполнена (Level 1: 3 файла, Level 2: 19 README.md) |
