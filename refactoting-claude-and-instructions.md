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
| `specs/` | ✅ Готово | ✅ | 16 файлов SSOT, README переформатирован, relations.md добавлен |
| `config/` | ⬜ Не начато | — | |
| `doc/` | ⬜ Не начато | — | |
| `git/` | ⬜ Не начато | — | |
| `platform/` | ⬜ Не начато | — | |
| `shared/` | ⬜ Не начато | — | |
| `src/` | ⬜ Не начато | — | |
| `tests/` | ⬜ Не начато | — | |

### skills/

| Группа скиллов | Статус | Верифицировано | Комментарий |
|----------------|--------|----------------|-------------|
| `instruction-*` | ✅ Готово | ✅ | 84% сокращение, relations.md добавлен в SSOT |
| `links-*` | ✅ Готово | ✅ | 60% сокращение, SSOT в instructions/links/ |
| `skill-*` | ✅ Готово | ✅ | 80% сокращение (612 строк), SSOT в instructions/skills/ |
| `spec-*` | ✅ Готово | ✅ | 54% сокращение (1440→656 строк), SSOT в instructions/specs/ |
| `doc-*` | ⬜ Не начато | — | |
| `test-*` | ⬜ Не начато | — | |
| `issue-*` | ⬜ Не начато | — | |
| `context-*` | ⬜ Не начато | — | |
| `glossary-*` | ⬜ Не начато | — | |
| `health-check` | ⬜ Не начато | — | |
| `prompt-update` | ⬜ Не начато | — | |
| `agent-create` | ⬜ Не начато | — | |
| `environment-check` | ⬜ Не начато | — | |
| `input-validate` | ⬜ Не начато | — | |

---

## Правила рефакторинга

> **SSOT:** [workflow-refactoring.md](./workflow-refactoring.md#правила-рефакторинга-обязательно)

---

## Важные шаги рефакторинга instructions/skills/

Выполненные шаги при рефакторинге skill-* (2025-01-22):

1. **Таблицы сравнения** — создали 8 таблиц сравнения инструкций и скиллов
2. **Выбор источника правды** — для каждого противоречия определили SSOT
3. **Обновление rules.md** — добавлено уточнение о вызове других скиллов
4. **Создание validation.md** — fail-fast, ревью, чек-листы
5. **Создание integration.md** — матрица применимости, типы ссылок
6. **Рефакторинг скиллов** — удаление дублирования, добавление ШАГ 0
7. **Обновление шаблона** — запрет комментариев к шагам, ссылки на SSOT
8. **Удаление skill-report** — дублировал README.md

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

### Сводка: skill-* (2025-01-22)

#### 1. Изменения

| Компонент | Было | Стало | Изменение |
|-----------|------|-------|-----------|
| skill-create | 841 строк | 180 строк | −79% |
| skill-update | 555 строк | 148 строк | −73% |
| skill-delete | 720 строк | 150 строк | −79% |
| skill-migrate | 210 строк | 134 строки | −36% |
| skill-report | 765 строк | **Удалён** | −100% |
| **Скиллы итого** | **3091 строк** | **612 строк** | **−80%** |

#### 2. Новые инструкции

| Файл | Строк | Описание |
|------|-------|----------|
| validation.md | 295 | Fail-fast, ревью, чек-листы |
| integration.md | 290 | Матрица применимости, типы ссылок |
| **Итого** | **585** | |

#### 3. Баланс

- **Было:** 3091 строк (5 скиллов)
- **Стало:** 612 строк (4 скилла) + 585 строк (2 инструкции) = 1197 строк
- **Чистое сокращение:** 1894 строки (−61%)

#### 4. Структурные изменения

- Добавлен **ШАГ 0** с блокирующим чтением SSOT во все skill-* скиллы
- Удалён **skill-report** (дублировал /.claude/skills/README.md)
- Обновлён **rules.md** — добавлено уточнение о вызове других скиллов
- Обновлён **skills/README.md** — добавлены validation.md, integration.md

#### 5. SSOT-ссылки в скиллах

| Скилл | Ссылается на |
|-------|--------------|
| skill-create | rules.md, workflow.md, validation.md, parameters.md, integration.md |
| skill-update | integration.md, workflow.md, errors.md |
| skill-delete | integration.md, errors.md |
| skill-migrate | rules.md, integration.md, errors.md |

#### 6. Итоговая рекомендация

**Система ЗАВЕРШЕНА.** Все skill-* скиллы рефакторены по паттерну SSOT.

---

### Сводка: spec-* (2025-01-22)

#### 1. Изменения скиллов

| Скилл | Было | Стало | Изменение |
|-------|------|-------|-----------|
| spec-create | 408 строк | 125 строк | −69% |
| spec-status | 304 строки | 119 строк | −61% |
| spec-update | 229 строк | 109 строк | −52% |
| specs-health | 181 строка | 109 строк | −40% |
| specs-sync | 154 строки | 102 строки | −34% |
| specs-index | 164 строки | 92 строки | −44% |
| **Скиллы итого** | **1440 строк** | **656 строк** | **−54%** |

#### 2. Инструкции (SSOT)

```
/.claude/instructions/specs/
├── README.md           # Индекс (переформатирован по шаблону)
├── statuses.md         # Статусы, переходы, каскадные проверки
├── workflow.md         # Discussion → Impact → ADR → Plan
├── discussions.md      # Формат, чек-листы
├── impact.md           # Формат, связь с ADR
├── adr.md              # Формат, проверка бизнес-логики
├── plans.md            # Формат, GitHub Issues
├── architecture.md     # Живой документ
├── glossary.md         # Глоссарий терминов
├── rules.md            # Скиллы, запреты, принятые решения
├── naming.md           # Нумерация, сокращённые пути
├── indexes.md          # Форматы README-таблиц
├── errors.md           # Обработка ошибок (дополнен specs-sync, specs-index)
├── output.md           # Форматы вывода
├── examples.md         # Примеры
└── relations.md        # Граф зависимостей (создан из README)
```

**Всего:** 16 файлов SSOT.

#### 3. Структурные изменения

- **README.md** полностью переформатирован по шаблону `templates/instructions/readme.md`
- **relations.md** — вынесен из README (секции "Связи документов", "Связь /specs/ ↔ /doc/")
- **rules.md** — добавлена секция "Принятые решения" (из README)
- **errors.md** — добавлены секции specs-sync, specs-index
- **ШАГ 0** добавлен во все spec-* скиллы с блокирующим чтением SSOT

#### 4. SSOT-ссылки в скиллах

| Скилл | Ссылается на |
|-------|--------------|
| spec-create | README.md, naming.md, relations.md, errors.md, rules.md, output.md, examples.md |
| spec-status | statuses.md, workflow.md, naming.md, errors.md, indexes.md, output.md, examples.md |
| spec-update | README.md, workflow.md, rules.md, errors.md, naming.md, output.md, examples.md |
| specs-health | statuses.md, rules.md, relations.md, errors.md, README.md, output.md, examples.md |
| specs-sync | statuses.md, workflow.md, relations.md, errors.md, output.md, examples.md |
| specs-index | indexes.md, statuses.md, errors.md, output.md, examples.md |

#### 5. Итоговая рекомендация

**Система ЗАВЕРШЕНА.** Все spec-* скиллы рефакторены по паттерну SSOT.

---

## Связанные файлы

- [workflow-refactoring.md](./workflow-refactoring.md) — воркфлоу рефакторинга (5 фаз)

---

## История изменений

- **2025-01-22**: Рефакторинг spec-* скиллов (6 скиллов, −54%), переформатирован README.md по шаблону, создан relations.md
- **2025-01-22**: Добавлен формат SSOT для шагов с вызовом скиллов (`→ /{skill}` → `SKILL.md`), исправлены instruction-create и instruction-update
- **2025-01-22**: Добавлены SSOT-ссылки ко всем шагам в links-* и instruction-* скиллах (skill-* уже имели)
- **2025-01-22**: Добавлена валидация скиллов по шаблону в workflow-refactoring.md (PHASE 5, шаг 7)
- **2025-01-22**: Исправлен шаблон skill.md и 11 скиллов — добавлены ## Оглавление, ## Чек-лист, ссылки на внутренний чек-лист
- **2025-01-22**: Исправлен skills/README.md по шаблону, правила рефакторинга перенесены в workflow-refactoring.md
- **2025-01-22**: Добавлены examples.md в instructions/instructions, links, skills — примеры вынесены из скиллов в SSOT
- **2025-01-22**: Финальная чистка skill-* — удалены детали из шагов, только SSOT-ссылки (80% сокращение)
- **2025-01-22**: Обновлён шаблон скилла — запрет комментариев в шагах, обязательные ссылки на SSOT
- **2025-01-22**: Добавлены правила рефакторинга и важные шаги в трекер
- **2025-01-22**: Рефакторинг skill-* скиллов, удалён skill-report, добавлены validation.md и integration.md
- **2025-01-22**: Дополнен workflow-refactoring.md (governed-by, верификация, ссылка на трекер)
- **2025-01-22**: Верификация links/, исправлен governed-by на links/README.md, добавлена сводка
- **2025-01-22**: Удалён instruction-stats.py (не используется), добавлена сводка по instructions/
- **2025-01-22**: Рефакторинг instruction-* скиллов, создание workflow-*.md
- **2025-01-22**: Рефакторинг links-* скиллов, вынос в instructions/links/
- **2025-01-22**: Создание relations.md, добавлен столбец "Верифицировано", валидация instruction-* скиллов
