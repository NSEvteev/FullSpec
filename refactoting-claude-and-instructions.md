# Рефакторинг .claude/ и instructions/

Трекер прогресса рефакторинга папок проекта.

---

## Папки .claude/

| Папка | Статус | Верифицировано | Комментарий |
|-------|--------|----------------|-------------|
| `agents/` | ⬜ Не начато | — | |
| `discussions/` | ⬜ Не начато | — | |
| `instructions/` | 🔄 В процессе | ⬜ | instructions/instructions/ готово, links/ готово |
| `scripts/` | ⬜ Не начато | — | |
| `skills/` | 🔄 В процессе | ⬜ | instruction-*, links-* готовы |
| `state/` | ⬜ Не начато | — | |
| `templates/` | ⬜ Не начато | — | |

---

## Детали по папкам

### instructions/

| Подпапка | Статус | Верифицировано | Комментарий |
|----------|--------|----------------|-------------|
| `instructions/` | ✅ Готово | ✅ | SSOT для инструкций, workflow-*.md, relations.md |
| `links/` | ✅ Готово | ✅ | Вынесено из links-* скиллов, governed-by исправлен |
| `config/` | ⬜ Не начато | — | |
| `doc/` | ⬜ Не начато | — | |
| `git/` | ⬜ Не начато | — | |
| `platform/` | ⬜ Не начато | — | |
| `shared/` | ⬜ Не начато | — | |
| `specs/` | ⬜ Не начато | — | |
| `src/` | ⬜ Не начато | — | |
| `tests/` | ⬜ Не начато | — | |

### skills/

| Группа скиллов | Статус | Верифицировано | Комментарий |
|----------------|--------|----------------|-------------|
| `instruction-*` | ✅ Готово | ✅ | 84% сокращение, relations.md добавлен в SSOT |
| `links-*` | ✅ Готово | ✅ | 60% сокращение, SSOT в instructions/links/ |
| `skill-*` | ⬜ Не начато | — | |
| `doc-*` | ⬜ Не начато | — | |
| `test-*` | ⬜ Не начато | — | |
| `issue-*` | ⬜ Не начато | — | |
| `context-*` | ⬜ Не начато | — | |
| `spec-*` | ⬜ Не начато | — | |
| `glossary-*` | ⬜ Не начато | — | |
| `health-check` | ⬜ Не начато | — | |
| `prompt-update` | ⬜ Не начато | — | |
| `agent-create` | ⬜ Не начато | — | |
| `environment-check` | ⬜ Не начато | — | |
| `input-validate` | ⬜ Не начато | — | |

---


## После каждой переработки:

**Запрос:**

Мы переработали .claude\instructions\folder

Проанализируй, что сейчас из себя представляет работа с инструкциями в проекте? Есть ли щаблоны? есть ли скиллы управления? Есть ли индексы? Верные ли индексы? Исполняют ли инструкции правила для для инструкций, регламентированные в .claude\instructions\instructions? Дай ПОЛНУЮ сводку.

Подумай, какие еще улучшения мы можем сделать. Нужны ли нам эти изменения? Помогут ли они в реальных проектах или только увеличат контекст?

---

### Сводка: instructions/instructions/ (2025-01-22)

#### 1. Компоненты системы

| Компонент | Количество | Статус |
|-----------|------------|--------|
| **Мета-инструкции** (`instructions/instructions/`) | 11 файлов | ✅ Полные |
| **Шаблоны** (`templates/instructions/`) | 2 файла | ✅ Есть |
| **Скиллы** (`skills/instruction-*`) | 3 скилла (6 файлов) | ✅ Есть |
| **Скрипты** (`scripts/instruction-*`) | 2 скрипта | ✅ Есть |
| **Инструкции проекта** | 104 файла | ✅ 100% созданы |

#### 2. Мета-инструкции (SSOT)

```
/.claude/instructions/instructions/
├── README.md               # Индекс (194 строки)
├── structure.md            # Где хранить
├── types.md                # standard vs project
├── validation.md           # Формат и frontmatter
├── statuses.md             # Система ✅/пусто
├── workflow.md             # Обзор жизненного цикла
├── workflow-create.md      # 15 шагов CREATE
├── workflow-update.md      # 12 шагов UPDATE
├── workflow-deactivate.md  # 10 шагов DEACTIVATE
├── relations.md            # governed-by, related
└── patterns.md             # Паттерны поиска ссылок
```

#### 3. Скиллы управления

| Скилл | Воркфлоу | Вызывает |
|-------|----------|----------|
| `/instruction-create` | 15 шагов | `/links-update`, `/context-update`, `/instruction-update` |
| `/instruction-update` | 12 шагов | `/context-update`, `/test-update` |
| `/instruction-deactivate` | 10 шагов | Только внутренние операции |

#### 4. Шаблоны

| Шаблон | Назначение |
|--------|------------|
| `instruction.md` | Полный шаблон инструкции (frontmatter, структура, секции) |
| `readme.md` | Шаблон README для папки инструкций |

#### 5. Индексы

| Индекс | Соответствие реальности |
|--------|------------------------|
| `/.claude/instructions/README.md` | ✅ 100% (104 инструкции) |
| `/.claude/instructions/instructions/README.md` | ✅ 100% (11 файлов) |
| Таблицы статусов | ✅ Все ✅✅ (заполнены) |

#### 6. Скрипты автоматизации

| Скрипт | Назначение |
|--------|------------|
| `instruction-validate.py` | Валидация пути и формата |
| `instruction-readme-update.py` | Обновление README папки |

#### 7. Итоговая рекомендация

**Система ЗАВЕРШЕНА.** Дополнительные улучшения увеличат контекст без реальной пользы.

Единственное возможное изменение: объединить `workflow-*.md` в один файл (сэкономит ~3 файла).

---

### Сводка: instructions/links/ (2025-01-22)

#### 1. Компоненты системы

| Компонент | Количество | Статус |
|-----------|------------|--------|
| **Инструкции** (`instructions/links/`) | 6 файлов | ✅ Полные |
| **Шаблоны** (`templates/links/`) | 0 | ✅ Не нужны |
| **Скиллы** (`skills/links-*`) | 4 скилла (8 файлов) | ✅ Есть |
| **Скрипты** (`scripts/*link*`) | 2 скрипта | ✅ Есть |

#### 2. Инструкции (SSOT для ссылок)

```
/.claude/instructions/links/
├── README.md           # Индекс (136 строк)
├── format.md           # Форматы: standard, folder, marked
├── patterns.md         # Regex-паттерны поиска
├── workflow.md         # CREATE → UPDATE → DELETE → VALIDATE
├── validation.md       # Правила проверки
└── edge-cases.md       # Граничные случаи
```

#### 3. Скиллы

| Скилл | Фаза | Ссылается на SSOT |
|-------|------|-------------------|
| `/links-create` | CREATE | format.md, patterns.md, workflow.md |
| `/links-update` | UPDATE | format.md, patterns.md, workflow.md, edge-cases.md |
| `/links-delete` | DELETE | format.md, workflow.md |
| `/links-validate` | VALIDATE | validation.md, patterns.md |

#### 4. Соответствие правилам instructions/instructions/

| Правило | Все 5 файлов |
|---------|:------------:|
| Frontmatter (type, description, governed-by, related) | ✅ |
| Заголовок (# Название) | ✅ |
| Навигационные ссылки | ✅ |
| Оглавление (## Оглавление) | ✅ |
| Скиллы (## Скиллы) | ✅ |
| Связанные инструкции | ✅ |
| governed-by: links/README.md | ✅ (исправлено) |

#### 5. Индексы

| Индекс | Соответствие |
|--------|--------------|
| `links/README.md` | ✅ 6 файлов |
| Главный `instructions/README.md` | ✅ links/ зарегистрирована |
| Таблицы статусов | ✅ Все ✅✅ |

#### 6. Скрипты

| Скрипт | Назначение |
|--------|------------|
| `find_references.py` | Поиск ссылок на файл |
| `update_links.py` | Массовая замена ссылок |

#### 7. Итоговая рекомендация

**Система ЗАВЕРШЕНА.** Полный жизненный цикл: CREATE → UPDATE → DELETE → VALIDATE.

---

## Связанные файлы

- [workflow-refactoring.md](./workflow-refactoring.md) — воркфлоу рефакторинга (5 фаз)

---

## История изменений

- **2025-01-22**: Дополнен workflow-refactoring.md (governed-by, верификация, ссылка на трекер)
- **2025-01-22**: Верификация links/, исправлен governed-by на links/README.md, добавлена сводка
- **2025-01-22**: Удалён instruction-stats.py (не используется), добавлена сводка по instructions/
- **2025-01-22**: Рефакторинг instruction-* скиллов, создание workflow-*.md
- **2025-01-22**: Рефакторинг links-* скиллов, вынос в instructions/links/
- **2025-01-22**: Создание relations.md, добавлен столбец "Верифицировано", валидация instruction-* скиллов
