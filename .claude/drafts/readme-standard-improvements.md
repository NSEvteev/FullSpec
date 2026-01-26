# Драфт: Доработка standard-readme.md

**Дата:** 2026-01-25
**Статус:** TODO

---

## Контекст

Сделано:
- `.structure/README.md` — SSOT структуры проекта
- `.structure/.instructions/standard-readme.md` — стандарт оформления README (формат + шаблон)

---

## Задачи

### 1. Доработать standard-readme.md ✅

- [x] **Добавить раздел Frontmatter** — правила заполнения frontmatter для README файлов
- [x] **Добавить раздел "Скиллы и скрипты"** — объединённый блок:
  - Скиллы для работы с README
  - Скрипты автоматизации (если есть)
- [x] **Добавить раздел "Связанные инструкции"** — ссылки на:
  - validation.md
  - workflow-create.md
  - workflow-delete.md
  - workflow-update.md

### 2. Переработать validation.md

Сделать validation.md набором правил, которые используются в:
- workflow-create.md (валидация при создании)
- workflow-update.md (валидация при обновлении)

Структура:
- Правила для README папок проекта
- Правила для README папок инструкций
- Чек-листы валидации

### 3. Использовать standard-readme.md как основу для других инструкций

После доработки — применить этот формат к:
- `/.instructions/` — мета-инструкции
- `/specs/.instructions/` — инструкции specs
- `/.claude/.instructions/skills/` — инструкции скиллов

---

## Порядок выполнения

1. Доработать standard-readme.md (задача 1)
2. Переработать validation.md (задача 2)
3. Обновить workflow-create.md и workflow-update.md — добавить ссылки на правила из validation.md
4. Применить формат к другим инструкциям (задача 3)
