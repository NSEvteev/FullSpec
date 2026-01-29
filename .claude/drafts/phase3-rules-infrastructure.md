# Фаза 3: Rules инфраструктура

Создание системы rules с автоматической загрузкой контекста.

---

## Статус: Готова к выполнению

**Дата:** 2026-01-29
**Зависит от:** Фаза 2 ✅

---

## Цель

Создать инфраструктуру для rules:
1. Инструкции (standard → validation → create → modify)
2. Скрипты (validate-rule.py, list-rules.py)
3. Скиллы (rule-create, rule-modify, rule-validate)
4. Базовый rule для rules

---

## Контекст выполнения

### Используемые скиллы

| Скилл | Когда использовать |
|-------|-------------------|
| `/instruction-create` | Создание инструкций standard, validation, create, modify |
| `/script-create` | Создание скриптов validate-rule.py, list-rules.py |
| `/skill-create` | Создание скиллов rule-* |
| `/instruction-validate` | Валидация созданных инструкций |
| `/script-validate` | Валидация скриптов |
| `/skill-validate` | Валидация скиллов |
| `/links-validate` | Проверка ссылок |

### Порядок создания (БЛОКИРУЮЩИЙ)

> **SSOT:** [standard-instruction.md § 10](/.instructions/standard-instruction.md#10-правила-для-createmodify-инструкций)

```
standard-rule.md     ← Сначала (нечего валидировать без стандарта)
     ↓
validation-rule.md   ← Потом (нечем проверять без валидации)
     ↓
create-rule.md       ← Потом (нечего модифицировать без создания)
     ↓
modify-rule.md       ← Последний
```

---

## ⚠️ Критическое правило: Рестарт сессии

> **Rules загружаются ТОЛЬКО при старте сессии Claude Code.**

| Событие | Rules применяются? |
|---------|:------------------:|
| Старт сессии | ✅ Все rules загружаются |
| Создание нового rule-файла | ❌ НЕ применяется до рестарта |
| Изменение существующего rule | ❌ НЕ применяется до рестарта |

**Правило для отчётов:**
- После создания/изменения rule — ВСЕГДА сообщать пользователю о необходимости НОВОЙ сессии
- Это ОБЯЗАТЕЛЬНАЯ часть отчёта, не опциональная

---

## Формат rule (СПРАВКА)

> **Frontmatter для rules отличается от инструкций!**

### Официальные поля Claude Code

Claude Code поддерживает **только `paths`** — остальные поля игнорируются.

### Наше расширение

Согласовано со стандартом frontmatter: [standard-frontmatter.md](/.structure/.instructions/standard-frontmatter.md)

```yaml
---
description: Краткое описание rule
standard: .claude/.instructions/rules/standard-rule.md
index: .claude/.instructions/rules/README.md
paths:
  - "паттерн/**"
---

# Название

Содержимое rule.
```

### Поля frontmatter

| Поле | Обязательное | Использует Claude Code | Описание |
|------|:------------:|:----------------------:|----------|
| `description` | ✅ | ❌ | Краткое описание rule |
| `standard` | ✅ | ❌ | Ссылка на стандарт: `standard-rule.md` |
| `index` | ✅ | ❌ | Ссылка на README области rules |
| `paths` | ❌ | ✅ | Glob-паттерны для условного применения |

### Типы применения

| Тип | Frontmatter | Когда загружается |
|-----|-------------|-------------------|
| Глобальный | Без `paths` | Всегда (при старте сессии) |
| Условный | С `paths` | При работе с файлами по паттерну |

### Стандартные paths по областям

| Область | Paths |
|---------|-------|
| Структура проекта | `.structure/**` |
| Скиллы | `.claude/skills/**` |
| Инструкции | `**/.instructions/**` |
| Скрипты | `**/.scripts/**` |
| Rules | `.claude/rules/**` |
| Глобальный | ❌ нет (без paths) |

---

## Структура результата

### Инструкции
```
/.claude/.instructions/rules/
├── README.md              # Индекс
├── standard-rule.md       # Стандарт формата rule
├── validation-rule.md     # Валидация rules
├── create-rule.md         # Создание rule
├── modify-rule.md         # Изменение rule
└── .scripts/
    ├── validate-rule.py   # Валидация формата
    └── list-rules.py      # Список всех rules
```

### Скиллы
```
/.claude/skills/
├── rule-create/SKILL.md   # → create-rule.md
├── rule-modify/SKILL.md   # → modify-rule.md
└── rule-validate/SKILL.md # → validation-rule.md
```

### Rules
```
/.claude/rules/
├── rules.md               # Условный: для работы с rules
└── ssot.md                # Глобальный: чтение SSOT-файлов
```

---

## Порядок выполнения

```
[ ] 3.1. standard-rule.md
[ ] 3.2. validation-rule.md + validate-rule.py + /rule-validate
[ ] 3.3. create-rule.md + list-rules.py + /rule-create
[ ] 3.4. modify-rule.md + /rule-modify
[ ] 3.5. README.md (индекс области)
[ ] 3.6. Базовый rule (rules.md)
[ ] 3.7. Обновить CLAUDE.md и /.claude/skills/README.md
[ ] 3.8. Финальная валидация
```

---

## 3.1. standard-rule.md

**Действие:** `/instruction-create standard-rule --area .claude/.instructions/rules`

**Секции для заполнения:**

| № | Секция | Содержание |
|---|--------|------------|
| 1 | Назначение | Что такое rule, когда создавать, когда НЕ создавать |
| 2 | Расположение | `/.claude/rules/{name}.md`, правила именования |
| 3 | Frontmatter | `description`, `standard`, `index`, `paths` (опционально) |
| 4 | Структура | Заголовок H1 + содержимое |
| 5 | Типы применения | Глобальный (без paths) vs Условный (с paths) |
| 6 | Содержимое | Ограничения и best practices |
| 7 | Конфликты paths | Поведение при пересечении |
| 8 | Примеры | 2-3 примера rules |

### Содержимое rule (для секции 6)

| Аспект | Значение |
|--------|----------|
| Максимальный размер | 50 строк (загружается в контекст каждой сессии) |
| Формат ссылок на скиллы | `→ /skill-name` |
| Структура | H1 заголовок → краткое описание → ссылки на скиллы |
| Best practice | Не дублировать инструкции, только триггеры |

### Конфликты paths (для секции 7)

- Claude Code применяет **все совпавшие rules** — это фича, не баг
- Если rules противоречат друг другу — ошибка проектирования, исправить содержимое
- `list-rules.py` выводит warning при пересечении paths

### Подпапки

> **Решение:** Подпапки в `/.claude/rules/` НЕ поддерживаются.

- Плоская структура `/.claude/rules/*.md`
- Rules мало (5-15), подпапки избыточны
- При необходимости группировки — через naming: `frontend-components.md`

**Финальная валидация:**
```bash
python .instructions/.scripts/validate-instruction.py .claude/.instructions/rules/standard-rule.md
```

---

## 3.2. validation-rule.md + validate-rule.py + /rule-validate

### 3.2.1. Инструкция validation-rule.md

**Действие:** `/instruction-create validation-rule --area .claude/.instructions/rules`

**Секции для заполнения:**

| Секция | Содержание |
|--------|------------|
| Когда валидировать | После создания/изменения rule |
| Шаги | Автоматически: `validate-rule.py`, вручную: чек-лист |
| Чек-лист | Файл, frontmatter, структура, ссылки |
| Тестирование после рестарта | Проверка работоспособности rule |
| Типичные ошибки | Таблица кодов R0xx |
| Скрипты | validate-rule.py |
| Скиллы | /rule-validate |

### Тестирование rule после рестарта (для секции "Тестирование после рестарта")

| Метод | Как проверить |
|-------|---------------|
| `/memory` | Показывает загруженные rules — проверить наличие созданного rule |
| Триггер | Открыть файл по paths → убедиться, что Claude следует rule |

**Чек-лист тестирования:**
1. Начать новую сессию Claude Code
2. Выполнить `/memory` — rule должен быть в списке
3. Открыть файл, соответствующий paths rule
4. Убедиться, что Claude применяет правила из rule

**Коды ошибок R0xx:**

| Код | Описание |
|-----|----------|
| R001 | Неверное расположение (не в `/.claude/rules/`) |
| R002 | Неверное расширение (не `.md`) |
| R010 | Невалидный frontmatter |
| R011 | Отсутствует `description` |
| R012 | Отсутствует `standard` |
| R013 | Отсутствует `index` |
| R014 | `paths` не массив строк |
| R015 | Невалидный glob-паттерн в `paths` |
| R020 | Нет заголовка H1 |
| R021 | Несколько заголовков H1 |

### 3.2.2. Скрипт validate-rule.py

**Действие:** `/script-create validate-rule --area .claude/.instructions/rules`

**Назначение:** Валидация формата rule

**Проверки:**
- Файл в `/.claude/rules/`
- Расширение `.md`
- Frontmatter валиден:
  - `description` — присутствует, не пустое
  - `standard` — присутствует, указывает на standard-rule.md
  - `index` — присутствует, указывает на README области
  - `paths` (если есть) — массив строк с валидными glob-паттернами
- Есть единственный заголовок H1

**Обязательно:** `ERROR_CODES` с кодами R0xx

### 3.2.3. Скилл /rule-validate

**Действие:** `/skill-create rule-validate`

**SSOT:** `/.claude/.instructions/rules/validation-rule.md`

**Триггеры:**
- Команда: `/rule-validate`
- Фразы ru: "проверь rule", "валидация rule"
- Фразы en: "validate rule"

---

## 3.3. create-rule.md + list-rules.py + /rule-create

### 3.3.1. Инструкция create-rule.md

**Действие:** `/instruction-create create-rule --area .claude/.instructions/rules`

**Секции для заполнения:**

| Секция | Содержание |
|--------|------------|
| Принципы | Rule = триггер контекста, не дублировать существующие |
| Шаги | См. ниже |
| Чек-лист | Подготовка, создание, проверка |
| Примеры | Глобальный rule, условный rule |
| Скрипты | list-rules.py |
| Скиллы | /rule-create |

**Шаги:**

```
### Шаг 1: Проверить существующие rules

> **ОБЯЗАТЕЛЬНО** — DRY

```bash
python .claude/.instructions/rules/.scripts/list-rules.py
```

LLM анализирует: есть ли rule с похожим функционалом?

Если найден похожий — AskUserQuestion:
1. Расширить существующий → `/rule-modify`
2. Создать новый

### Шаг 2: Определить область применения (paths)

> **LLM автоматически анализирует** и предлагает paths.

**Алгоритм LLM:**

1. Понять, для какой области создаётся rule
2. Определить paths по таблице:

   | Область | Paths |
   |---------|-------|
   | Структура проекта | `.structure/**` |
   | Скиллы | `.claude/skills/**` |
   | Инструкции | `**/.instructions/**` |
   | Скрипты | `**/.scripts/**` |
   | Rules | `.claude/rules/**` |
   | Общие правила | ❌ нет (глобальный) |

3. Сформировать предложение:

```
**Предлагаемая область:**
- Тип: {Глобальный/Условный}
- Paths: {список паттернов или "нет — глобальный"}

Причина: {почему выбрана эта область}
```

**AskUserQuestion:**

1. Подтвердить предложенную область
2. Изменить тип (глобальный ↔ условный)
3. Изменить paths
4. Другое — ввести вручную

### Шаг 3: Определить имя

Имя: kebab-case, описательное

**Формат:** `{область}-{назначение}.md` или `{назначение}.md`

Примеры:
- `ssot.md` — глобальное правило про SSOT
- `skills.md` — правила для скиллов
- `instructions.md` — правила для инструкций

### Шаг 4: Создать файл

```bash
# Создать файл по шаблону из standard-rule.md
```

**Шаблон:**
```yaml
---
description: {описание}
standard: .claude/.instructions/rules/standard-rule.md
index: .claude/.instructions/rules/README.md
paths:          # Только для условных rules
  - "{паттерн}"
---

# {Заголовок}

{Содержимое}
```

### Шаг 5: Валидация

```bash
python .claude/.instructions/rules/.scripts/validate-rule.py {name}
```

### Шаг 6: Отчёт

```
## Отчёт о создании rule

**Создан rule:** `{name}.md`

**Тип:** {Глобальный/Условный}

**Paths:** {список или "нет (глобальный)"}

**Валидация:** пройдена ✅

---

⚠️ **ТРЕБУЕТСЯ НОВАЯ СЕССИЯ**

Для применения rule необходимо:
1. Завершить текущую сессию
2. Начать НОВУЮ сессию Claude Code

Rules загружаются при старте сессии. Без рестарта rule НЕ будет работать.
```
```

### 3.3.2. Скрипт list-rules.py

**Действие:** `/script-create list-rules --area .claude/.instructions/rules`

**Назначение:** Список всех rules с описаниями

**Функционал:**
- Сканирует `/.claude/rules/*.md` (плоская структура, без подпапок)
- Извлекает из frontmatter: `description`, `paths`
- Определяет тип: глобальный (без paths) / условный (с paths)
- Выводит таблицу для анализа LLM
- **Выводит warning при пересечении paths** между rules

**Формат вывода:**
```
| Rule | Type | Paths | Description |
|------|------|-------|-------------|
| rules.md | conditional | .claude/rules/** | Правила работы с rules |
| ssot.md | global | — | Обязательное чтение SSOT-файлов |

⚠️ WARNING: Пересечение paths между rules.md и instructions.md
```

### 3.3.3. Скилл /rule-create

**Действие:** `/skill-create rule-create`

**SSOT:** `/.claude/.instructions/rules/create-rule.md`

**Триггеры:**
- Команда: `/rule-create`
- Фразы ru: "создай rule", "добавь rule"
- Фразы en: "create rule"

---

## 3.4. modify-rule.md + /rule-modify

### 3.4.1. Инструкция modify-rule.md

**Действие:** `/instruction-create modify-rule --area .claude/.instructions/rules`

**Секции для заполнения:**

| Секция | Содержание |
|--------|------------|
| Типы изменений | Обновление, деактивация, миграция |
| Обновление | Шаги обновления содержимого/paths |
| Деактивация | Шаги деактивации (переименование в `_old`) |
| Миграция | Шаги переименования |
| Обновление ссылок | Где искать ссылки на rule |
| Чек-лист | По типам изменений |
| Примеры | Обновление, деактивация, миграция |
| Скрипты | find-rule-references.py (опционально) |
| Скиллы | /rule-modify |

**Обязательно в отчёте:**
```
⚠️ **ТРЕБУЕТСЯ НОВАЯ СЕССИЯ**

Изменения в rule вступят в силу только после:
1. Завершения текущей сессии
2. Начала НОВОЙ сессии Claude Code
```

### 3.4.2. Скилл /rule-modify

**Действие:** `/skill-create rule-modify`

**SSOT:** `/.claude/.instructions/rules/modify-rule.md`

**Триггеры:**
- Команда: `/rule-modify`
- Фразы ru: "измени rule", "обнови rule"
- Фразы en: "modify rule", "update rule"

---

## 3.5. README.md (индекс области)

**Формат:** стандартный README для папки инструкций

**SSOT:** [standard-readme.md § 3](/.structure/.instructions/standard-readme.md#3-readme-папок-инструкций)

**Содержит:**

```markdown
# Rules — инструкции

Инструкции для создания и управления rules.

## Инструкции

| Инструкция | Тип | Описание |
|------------|-----|----------|
| [standard-rule.md](./standard-rule.md) | standard | Стандарт формата rule |
| [validation-rule.md](./validation-rule.md) | validation | Валидация rules |
| [create-rule.md](./create-rule.md) | create | Создание rule |
| [modify-rule.md](./modify-rule.md) | modify | Изменение rule |

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-rule.py](./.scripts/validate-rule.py) | Валидация формата rule | validation-rule.md |
| [list-rules.py](./.scripts/list-rules.py) | Список всех rules | create-rule.md |
```

---

## 3.6. Базовые rules

### 3.6.1. rules.md (условный)

**Файл:** `/.claude/rules/rules.md`

**Действие:** Создать вручную (первый rule в системе)

```markdown
---
description: Правила работы с rules
standard: .claude/.instructions/rules/standard-rule.md
index: .claude/.instructions/rules/README.md
paths:
  - ".claude/rules/**"
---

# Rules

При создании rule:
→ `/rule-create`

При изменении rule:
→ `/rule-modify`

При валидации rule:
→ `/rule-validate`
```

### 3.6.2. ssot.md (глобальный)

**Файл:** `/.claude/rules/ssot.md`

**Действие:** Создать вручную (глобальное правило)

```markdown
---
description: Обязательное чтение SSOT-файлов
standard: .claude/.instructions/rules/standard-rule.md
index: .claude/.instructions/rules/README.md
---

# SSOT (Single Source of Truth)

> **КРИТИЧЕСКОЕ ПРАВИЛО:** Если в документе есть ссылка вида `**SSOT:** [файл](путь)` —
> Claude **ОБЯЗАН** прочитать этот файл перед выполнением.

## Правило

1. При обнаружении `**SSOT:**` — немедленно прочитать указанный файл
2. Нельзя выполнять действие по памяти или предположениям
3. SSOT-файл содержит актуальные шаги и правила

## Где встречается

- Скиллы: `**SSOT:** [инструкция.md](путь)`
- Инструкции: поле `standard:` в frontmatter
- Документация: ссылки на первоисточники
```

### Валидация базовых rules

```bash
python .claude/.instructions/rules/.scripts/validate-rule.py rules
python .claude/.instructions/rules/.scripts/validate-rule.py ssot
```

### ⚠️ ВАЖНО: Рестарт сессии

> **ОБЯЗАТЕЛЬНО** после создания базовых rules — начать НОВУЮ сессию Claude Code.

**Почему:**
- Rules загружаются при **старте сессии**
- Новые rule-файлы НЕ применяются в текущей сессии
- Без рестарта rules не будут работать

**Сообщить пользователю:**
```
⚠️ ТРЕБУЕТСЯ НОВАЯ СЕССИЯ

Созданы базовые rules:
- rules.md
- ssot.md

Для применения правил необходимо:
1. Завершить текущую сессию
2. Начать НОВУЮ сессию Claude Code

После рестарта rules будут автоматически загружены и применены.
```

---

## 3.7. Обновить документацию

### CLAUDE.md

**Обновить таблицу скиллов:**

```markdown
| rule-* | create, modify, validate |
```

Обновить счётчик: `13` → `16`

**Добавить в блокирующие пути:**

```markdown
| `/.claude/rules/**` | `/rule-create`, `/rule-modify` | ЗАПРЕЩЕНО |
```

> Ручное создание rules ЗАПРЕЩЕНО — использовать только скиллы.

### /.claude/skills/README.md

Добавить категорию:

```markdown
## rule-*

| Скилл | Описание | SSOT |
|-------|----------|------|
| [/rule-create](./rule-create/SKILL.md) | Создание rule | create-rule.md |
| [/rule-modify](./rule-modify/SKILL.md) | Изменение rule | modify-rule.md |
| [/rule-validate](./rule-validate/SKILL.md) | Валидация rule | validation-rule.md |
```

---

## 3.8. Финальная валидация

### Инструкции

```bash
python .instructions/.scripts/validate-instruction.py .claude/.instructions/rules/standard-rule.md
python .instructions/.scripts/validate-instruction.py .claude/.instructions/rules/validation-rule.md
python .instructions/.scripts/validate-instruction.py .claude/.instructions/rules/create-rule.md
python .instructions/.scripts/validate-instruction.py .claude/.instructions/rules/modify-rule.md
```

### Скрипты

```bash
python .instructions/.scripts/validate-script.py .claude/.instructions/rules/.scripts/validate-rule.py
python .instructions/.scripts/validate-script.py .claude/.instructions/rules/.scripts/list-rules.py
```

### Скиллы

```bash
python .claude/.instructions/skills/.scripts/validate-skill.py rule-create
python .claude/.instructions/skills/.scripts/validate-skill.py rule-modify
python .claude/.instructions/skills/.scripts/validate-skill.py rule-validate
```

### Rules

```bash
python .claude/.instructions/rules/.scripts/validate-rule.py rules
python .claude/.instructions/rules/.scripts/validate-rule.py ssot
```

### Ссылки

```
/links-validate .claude/.instructions/rules/
/links-validate .claude/skills/rule-create/
/links-validate .claude/skills/rule-modify/
/links-validate .claude/skills/rule-validate/
```

---

## Чек-лист Фазы 3

### Инструкции
- [ ] standard-rule.md создан и валиден
- [ ] validation-rule.md создан и валиден
- [ ] create-rule.md создан и валиден
- [ ] modify-rule.md создан и валиден
- [ ] README.md создан

### Скрипты
- [ ] validate-rule.py создан и работает
- [ ] list-rules.py создан и работает
- [ ] ERROR_CODES присутствует в validate-rule.py

### Скиллы
- [ ] /rule-create создан и валиден
- [ ] /rule-modify создан и валиден
- [ ] /rule-validate создан и валиден

### Rules
- [ ] rules.md создан и валиден (условный)
- [ ] ssot.md создан и валиден (глобальный)

### Документация
- [ ] CLAUDE.md обновлён (16 скиллов)
- [ ] /.claude/skills/README.md обновлён

### Валидация
- [ ] Все инструкции проходят validate-instruction.py
- [ ] Все скрипты проходят validate-script.py
- [ ] Все скиллы проходят validate-skill.py
- [ ] rules.md проходит validate-rule.py
- [ ] ssot.md проходит validate-rule.py
- [ ] Все ссылки валидны

### Рестарт
- [ ] Пользователю сообщено о необходимости НОВОЙ сессии
- [ ] Новая сессия начата
- [ ] Rules загружены и работают

---

## Результат Фазы 3

**Создано:**
- 5 инструкций (standard, validation, create, modify, README)
- 2 скрипта (validate-rule.py, list-rules.py)
- 3 скилла (rule-create, rule-modify, rule-validate)
- 2 rules (rules.md, ssot.md)

**Обновлено:**
- CLAUDE.md
- /.claude/skills/README.md

---

## После Фазы 3

> **Rules для областей создаются вручную** после завершения Фазы 3.

Примеры rules для областей (создать через `/rule-create`):

| Rule | Paths | Назначение |
|------|-------|------------|
| `instructions.md` | `**/.instructions/**` | → `/instruction-*` |
| `scripts.md` | `**/.scripts/**` | → `/script-*` |
| `skills.md` | `.claude/skills/**` | → `/skill-*` |
| `structure.md` | `.structure/**` | → `/structure-*` |

**Порядок:** Создавать по мере необходимости, используя `/rule-create`.
