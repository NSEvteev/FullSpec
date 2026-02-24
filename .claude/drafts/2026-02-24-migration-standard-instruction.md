# Миграция standard-instruction.md v1.2 → v1.3

Синхронизация 37 зависимых файлов после обновления standard-instruction.md до v1.3.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Следующие шаги](#следующие-шаги)

---

## Контекст

**Задача:** `/migration-create .instructions/standard-instruction.md` — обновить 37 файлов с v1.2 до v1.3
**Почему создан:** `check-version-drift.py` показывает 37 расхождений (3 Workflow + 34 экземпляра). Миграция не была выполнена после bump версии в коммите `cb94381` (2026-02-11).
**Связанные файлы:** `.instructions/standard-instruction.md`

## Содержание

### Что изменилось в v1.3

Коммит `cb94381` — "docs: реструктуризация validation-инструкций — паттерн Шаг 0".

Добавлены два паттерна в § 5 (Инструкции типа validation):
- **Паттерн А:** есть комплексный скрипт (один скрипт покрывает все проверки) — Шаг 0 запускает скрипт, далее ручные шаги только при его отсутствии
- **Паттерн Б:** нет комплексного скрипта (разные инструменты, LLM-анализ) — все шаги выполняются последовательно

### Затронутые файлы

#### Workflows (3 файла)

| Файл | Текущая версия | Нужна версия |
|------|---------------|--------------|
| `.instructions/validation-instruction.md` | v1.2 | v1.3 |
| `.instructions/create-instruction.md` | v1.2 | v1.3 |
| `.instructions/modify-instruction.md` | v1.2 | v1.3 |

#### Экземпляры (34 файла)

| Файл | Текущая версия |
|------|---------------|
| `.claude/.instructions/agents/create-agent.md` | v1.2 |
| `.claude/.instructions/agents/modify-agent.md` | v1.2 |
| `.claude/.instructions/agents/standard-agent.md` | v1.2 |
| `.claude/.instructions/agents/validation-agent.md` | v1.2 |
| `.claude/.instructions/drafts/standard-draft.md` | v1.2 |
| `.claude/.instructions/rules/create-rule.md` | v1.2 |
| `.claude/.instructions/rules/modify-rule.md` | v1.2 |
| `.claude/.instructions/rules/standard-rule.md` | v1.2 |
| `.claude/.instructions/skills/create-skill.md` | v1.2 |
| `.claude/.instructions/skills/modify-skill.md` | v1.2 |
| `.claude/.instructions/skills/standard-skill.md` | v1.2 |
| `.claude/.instructions/skills/validation-skill.md` | v1.2 |
| `.instructions/create-script.md` | v1.2 |
| `.instructions/modify-script.md` | v1.2 |
| `.instructions/standard-instruction.md` | v1.2 |
| `.instructions/standard-principles.md` | v1.2 |
| `.instructions/standard-script.md` | v1.2 |
| `.instructions/validation-principles.md` | v1.2 |
| `.instructions/migration/create-migration.md` | v1.2 |
| `.instructions/migration/standard-migration.md` | v1.2 |
| `.instructions/migration/validation-migration.md` | v1.2 |
| `.structure/.instructions/create-structure.md` | v1.2 |
| `.structure/.instructions/modify-structure.md` | v1.2 |
| `.structure/.instructions/standard-frontmatter.md` | v1.2 |
| `.structure/.instructions/standard-links.md` | v1.2 |
| `.structure/.instructions/standard-readme.md` | v1.2 |
| `.structure/.instructions/standard-search.md` | v1.2 |
| `specs/.instructions/analysis/design/create-design.md` | v1.2 |
| `specs/.instructions/analysis/design/modify-design.md` | v1.2 |
| `specs/.instructions/analysis/design/validation-design.md` | v1.2 |
| `specs/.instructions/analysis/review/create-review.md` | v1.2 |
| `specs/.instructions/analysis/review/standard-review.md` | v1.2 |
| `specs/.instructions/analysis/review/validation-review.md` | v1.2 |
| `specs/.instructions/docs/standard-docs.md` | v1.0 |

### Ожидаемый объём работ

1. **Bump frontmatter** standard-instruction.md: `standard-version: v1.2` → `v1.3`
2. **Bump standard-version** в 37 файлах: `v1.2` → `v1.3` (и `v1.0` → `v1.3` для standard-docs.md)
3. **Проверка содержания Workflows:** validation-instruction.md, create-instruction.md, modify-instruction.md — реализуют ли паттерны А/Б из § 5?
4. **Проверка содержания экземпляров типа validation:** validation-*.md файлы — соответствуют ли паттерну А или Б?

### Оценка сложности

- Bump версий — механическая работа (37 замен)
- Проверка содержания — нужно прочитать каждый validation-*.md и сверить с паттернами А/Б
- Потенциальные правки содержания — если validation-файлы не реализуют паттерны

---

## Следующие шаги

1. Выполнить `/migration-create .instructions/standard-instruction.md`
2. Проверить `/migration-validate .instructions/standard-instruction.md`
