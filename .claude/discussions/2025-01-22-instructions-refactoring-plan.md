# Рефакторинг инструкций: создание /.claude/instructions/instructions/

**Дата:** 2025-01-22
**Статус:** В процессе

---

## Цель

Создать папку `/.claude/instructions/instructions/` для регламентирования работы с инструкциями:
- Вынести общие концепции из трёх скиллов instruction-*
- Устранить дублирование
- Создать единый источник правды (SSOT)
- Создать шаблоны в `/.claude/templates/instructions/`

---

## Выполненные изменения

### Этап 1: Создание инструкций (7 файлов)

Создана папка `/.claude/instructions/instructions/` со следующими файлами:

| Файл | Описание |
|------|----------|
| README.md | Индекс папки с навигацией |
| structure.md | Расположение и допустимые папки |
| types.md | Типы инструкций (standard/project) |
| validation.md | Валидация путей и формата |
| statuses.md | Система статусов в README.md |
| workflow.md | Жизненный цикл (CREATE, UPDATE, DEACTIVATE) |
| patterns.md | Паттерны поиска ссылок |

### Этап 2: Создание шаблонов (2 файла)

Создана папка `/.claude/templates/instructions/`:

| Шаблон | Описание |
|--------|----------|
| instruction.md | Шаблон инструкции |
| readme.md | Шаблон README для папки инструкций |

### Этап 3: Форматирование по шаблонам

Все файлы приведены к единому формату:

**Структура инструкции:**
1. Frontmatter (type, description, governed-by, related)
2. Заголовок
3. Описание
4. Навигационные ссылки (Индекс | Папка)
5. Оглавление
6. Тематические секции
7. Примеры
8. Скиллы
9. Связанные инструкции

**Структура README папки:**
1. Заголовок и описание
2. Содержание
3. Оглавление (таблица)
4. Дерево файлов
5. Секции с оглавлением каждой инструкции
6. Шаблоны
7. Скиллы
8. Скрипты

---

## Ключевые решения

### 1. Навигационные ссылки

Каждая инструкция содержит ссылки после описания:

```markdown
**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [{папка}/README.md](./README.md)
```

**Зачем:** Быстрая навигация вверх по иерархии.

### 2. Синхронизация README

При любой операции с инструкцией (CREATE, UPDATE, DEACTIVATE) обновляются:
1. Инструкция — целевой файл
2. README папки — `/.claude/instructions/{папка}/README.md`
3. Главный README — `/.claude/instructions/README.md`

**Зачем:** Консистентность индексов.

### 3. Обязательные разделы в README

Каждый README папки инструкций содержит:
- Шаблоны (или "отсутствуют")
- Скиллы (или "отсутствуют")
- Скрипты (или "отсутствуют")

**Зачем:** Единообразие, легко найти связанные ресурсы.

### 4. governed-by

Каждая инструкция содержит в frontmatter:

```yaml
governed-by: instructions/README.md
```

**Зачем:** Связь с мета-инструкцией, валидация соответствия формату.

### 5. Философия распределена по инструкциям

Вместо отдельной секции "Философия" в README:
- "Инструкции НЕ удаляются" → workflow.md (DEACTIVATE)
- "governed-by" → validation.md (Frontmatter)

**Зачем:** Информация там, где она нужна.

### 6. Переименование скилла

`/instruction-delete` → `/instruction-deactivate`

**Зачем:** Название отражает действие (деактивация, а не удаление).

---

## Созданные файлы

```
/.claude/instructions/instructions/
├── README.md
├── structure.md
├── types.md
├── validation.md
├── statuses.md
├── workflow.md
└── patterns.md

/.claude/templates/instructions/
├── instruction.md
└── readme.md
```

---

## Следующие шаги (PHASE 3+)

### PHASE 3: Обновить скиллы instruction-*
- [ ] instruction-create/SKILL.md — добавить ссылки на инструкции
- [ ] instruction-update/SKILL.md — добавить ссылки на инструкции
- [ ] instruction-deactivate/SKILL.md — переименовать из instruction-delete

### PHASE 4: Обновить индексы
- [ ] /.claude/instructions/README.md — добавить секцию /instructions/
- [ ] /CLAUDE.md — обновить дерево

### PHASE 5: governed-by для существующих инструкций
- [ ] Добавить `governed-by: instructions/README.md` в ~75 инструкций
- [ ] Добавить навигационные ссылки

---

## Связанные файлы

- [2025-01-22-instructions-collected.md](./2025-01-22-instructions-collected.md) — сбор информации из скиллов
- [План](~/.claude/plans/jiggly-wishing-donut.md) — исходный план

---

## Итоги

**Создано:** 9 файлов (7 инструкций + 2 шаблона)
**Обновлено:** 7 файлов (приведены к формату шаблонов)
**Статус:** Этапы 1-3 выполнены, переход к PHASE 3
