# Версионирование стандартов и интеграция Holt

**Статус:** Драфт
**Дата:** 2026-02-02
**Цель:** Автоматическая синхронизация документов при изменении стандартов

---

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Версионирование стандартов](#1-версионирование-стандартов)
  - [2. Процесс обновления версии](#2-процесс-обновления-версии)
  - [3. Каскадное обновление зависимых документов](#3-каскадное-обновление-зависимых-документов)
  - [4. Интеграция Captain Holt](#4-интеграция-captain-holt)
  - [5. Обновление standard-frontmatter.md](#5-обновление-standard-frontmattermd)
  - [6. Полный воркфлоу](#6-полный-воркфлоу)
  - [7. Изменения в существующих файлах](#7-изменения-в-существующих-файлах)
  - [8. Новые скрипты](#8-новые-скрипты)
  - [9. Чек-лист реализации](#9-чек-лист-реализации)
  - [10. Открытые вопросы](#10-открытые-вопросы)
- [Следующие шаги](#следующие-шаги)

---

## Контекст

Сейчас при изменении `standard-*.md` все зависимые документы (validation-*, create-*, modify-*) мгновенно устаревают. Нет механизма:
- Отслеживания версий стандартов
- Автоматического обновления зависимых документов
- Валидации на двойственность (Holt)

---

## Содержание

### 1. Версионирование стандартов

#### 1.1. Формат версии в стандарте

**Файл:** `.instructions/standard-instruction.md` (и другие standard-*.md)

```markdown
---
description: Стандарт формата инструкций
...
---

# Стандарт инструкций

Версия стандарта: 1.1

...
```

**Правила:**
- Версия в теле документа (не frontmatter) — для читаемости
- Формат: `X.Y` (major.minor)
- Увеличивается при любом изменении логики стандарта

#### 1.2. Рабочая версия в зависимых документах

**Файлы:** `validation-*.md`, `create-*.md`, `modify-*.md`

```markdown
---
description: Воркфлоу создания инструкции
standard: .instructions/standard-instruction.md
standard-version: v1.0
...
---

# Воркфлоу создания

Рабочая версия стандарта: 1.0

...
```

**Правила:**
- `standard-version` во frontmatter — для автоматизации
- "Рабочая версия стандарта: X.Y" в теле — для читаемости
- Должна совпадать с версией стандарта после синхронизации

---

### 2. Процесс обновления версии

#### 2.1. Триггеры увеличения версии

| Триггер | Действие |
|---------|----------|
| Изменение логики в standard-*.md | Minor: 1.0 → 1.1 |
| Breaking change (структура, обязательные поля) | Major: 1.x → 2.0 |
| Исправление опечаток, форматирование | Без изменения версии |

#### 2.2. Границы версии — git commit

**Правило:** Версия увеличивается один раз за коммит.

```
Сценарий:
1. Изменил standard-instruction.md (версия 1.0 → 1.1)
2. Ещё раз изменил standard-instruction.md (версия остаётся 1.1)
3. git commit → версия 1.1 зафиксирована
4. Новые изменения → версия 1.1 → 1.2
```

**Реализация:**
- Перед увеличением версии проверить: `git diff --cached standard-*.md`
- Если файл уже изменён в staging — не увеличивать версию повторно
- Если файл не в staging — увеличить версию

---

### 3. Каскадное обновление зависимых документов

#### 3.1. Алгоритм синхронизации

```
1. Обнаружить изменение standard-*.md
2. Получить новую версию стандарта (из тела документа)
3. Найти все файлы с:
   - standard: {путь к изменённому стандарту}
   - standard-version: {отличается от новой версии}
4. Для каждого файла:
   a. Вызвать /modify-{type} (instruction, skill, rule, etc.)
   b. Обновить standard-version во frontmatter
   c. Обновить "Рабочая версия стандарта" в теле
5. Валидировать через Holt (если включено)
```

#### 3.2. Поиск зависимых файлов

```bash
# Найти все файлы, зависящие от standard-instruction.md
grep -r "standard: .instructions/standard-instruction.md" --include="*.md" -l
```

#### 3.3. Скрипт автоматизации

**Файл:** `.instructions/.scripts/sync-standard-version.py`

```python
"""
sync-standard-version.py — Синхронизация версий стандартов

Использование:
    python sync-standard-version.py <standard-file>
    python sync-standard-version.py .instructions/standard-instruction.md

Действия:
    1. Читает версию из стандарта
    2. Находит зависимые файлы
    3. Сравнивает версии
    4. Выводит список файлов для обновления
"""
```

---

### 4. Интеграция Captain Holt

#### 4.1. Когда запускать Holt

| Событие | Запуск Holt |
|---------|-------------|
| Создание standard-*.md | Обязательно |
| Изменение standard-*.md | Обязательно |
| Создание validation/create/modify-*.md | Опционально |
| Перед коммитом standard-*.md | Рекомендуется |

#### 4.2. Интеграция в воркфлоу

**Шаг в create-instruction.md:**

```markdown
### Шаг N: Валидация Holt (для standard-*.md)

Если создаётся файл с префиксом `standard-`:

1. Запустить агента Captain Holt:
   - Анализ на двойственность
   - Анализ на риски интерпретации

2. При обнаружении P1 проблем:
   - Исправить перед продолжением
   - Повторить валидацию

3. При обнаружении P2-P3:
   - Показать пользователю
   - Спросить: исправить сейчас или оставить?
```

#### 4.3. Автоматическое исправление

**Режим работы Holt:**

| Режим | Действие |
|-------|----------|
| `analyze` | Только анализ, вывод отчёта |
| `fix` | Анализ + автоматическое исправление P1 |
| `interactive` | Анализ + вопросы по каждой проблеме |

**Вызов:**
```
captain-holt analyze .instructions/standard-instruction.md
captain-holt fix .instructions/standard-instruction.md
```

---

### 5. Обновление standard-frontmatter.md

#### 5.1. Таблица актуальных версий

**Добавить в `.structure/.instructions/standard-frontmatter.md`:**

```markdown
## Актуальные версии стандартов

| Стандарт | Текущая версия | Путь |
|----------|----------------|------|
| Инструкции | 1.1 | .instructions/standard-instruction.md |
| Скиллы | 1.0 | .claude/.instructions/skills/standard-skill.md |
| Агенты | 1.1 | .claude/.instructions/agents/standard-agent.md |
| Правила | 1.0 | .claude/.instructions/rules/standard-rule.md |
| README | 1.0 | .structure/.instructions/standard-readme.md |
| Скрипты | 1.0 | .instructions/standard-script.md |
```

**Обновление:**
- При изменении версии стандарта — обновить таблицу
- Автоматизировать через скрипт или хук

---

### 6. Полный воркфлоу

```
┌─────────────────────────────────────────────────────────────┐
│                    ИЗМЕНЕНИЕ СТАНДАРТА                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Редактирование standard-*.md                             │
│    - Внести изменения                                       │
│    - Увеличить версию (если не в staging)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Валидация Holt                                           │
│    - captain-holt analyze <file>                            │
│    - Исправить P1 проблемы                                  │
│    - Решить по P2-P3                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Каскадное обновление                                     │
│    - python sync-standard-version.py <standard-file>        │
│    - Получить список зависимых файлов                       │
│    - Для каждого: /modify-{type}                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Обновление индексов                                      │
│    - standard-frontmatter.md (таблица версий)               │
│    - README.md (если нужно)                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Коммит                                                   │
│    - git add <все изменённые файлы>                         │
│    - git commit -m "feat: обновление standard-X до vY.Z"    │
└─────────────────────────────────────────────────────────────┘
```

---

### 7. Изменения в существующих файлах

#### 7.1. standard-instruction.md

**Добавить после заголовка:**
```markdown
Версия стандарта: 1.1
```

#### 7.2. validation-instruction.md, create-instruction.md, modify-instruction.md

**Добавить после заголовка:**
```markdown
Рабочая версия стандарта: 1.0
```

**Обновить frontmatter:**
```yaml
standard-version: v1.0
```

#### 7.3. standard-frontmatter.md

**Добавить секцию:**
- Таблица актуальных версий стандартов
- Описание поля `standard-version`

#### 7.4. core.md (rules)

**Добавить правило:**
```markdown
**Синхронизация версий:** При изменении standard-*.md проверить зависимые файлы. Если standard-version отличается — вызвать /modify-{type}.
```

---

### 8. Новые скрипты

| Скрипт | Назначение |
|--------|------------|
| `sync-standard-version.py` | Поиск и обновление зависимых файлов |
| `check-version-drift.py` | Проверка расхождения версий (для CI) |
| `bump-standard-version.py` | Увеличение версии стандарта |

---

### 9. Чек-лист реализации

- [ ] Добавить "Версия стандарта: 1.1" в standard-instruction.md
- [ ] Добавить "Рабочая версия стандарта: 1.0" в validation/create/modify-instruction.md
- [ ] Добавить standard-version во frontmatter всех инструкций
- [ ] Создать скрипт sync-standard-version.py
- [ ] Обновить standard-frontmatter.md (таблица версий)
- [ ] Обновить core.md (правило синхронизации)
- [ ] Интегрировать Holt в create-instruction.md
- [ ] Провалидировать standard-instruction.md через Holt
- [ ] Обновить все зависимые документы до версии 1.1

---

### 10. Решения по открытым вопросам

| Вопрос | Решение |
|--------|---------|
| Автоматизация vs ручной контроль | **Автоматически** — сразу обновлять без подтверждения |
| Глубина каскада | **Только прямые** — validation/create/modify для этого стандарта |
| Версионирование объектов | **Да, увеличивать** — v1.0 → v1.1 при синхронизации |
| Holt триггер | **Всегда автоматически** — при любом изменении standard-*.md |

---

## Подробный план выполнения

### Инвентаризация

**Стандарты (11 файлов):**

| Стандарт | Зависимых файлов | Путь |
|----------|------------------|------|
| instruction | 53 | .instructions/standard-instruction.md |
| skill | 22 | .claude/.instructions/skills/standard-skill.md |
| readme | 19 | .structure/.instructions/standard-readme.md |
| rule | 12 | .claude/.instructions/rules/standard-rule.md |
| agent | 10 | .claude/.instructions/agents/standard-agent.md |
| draft | ? | .claude/.instructions/drafts/standard-draft.md |
| state | 1 | .claude/.instructions/state/standard-state.md |
| principles | ? | .instructions/standard-principles.md |
| script | ? | .instructions/standard-script.md |
| frontmatter | ? | .structure/.instructions/standard-frontmatter.md |
| links | ? | .structure/.instructions/standard-links.md |

**Прямые зависимости (21 файл validation/create/modify):**

| Тип | Файлы |
|-----|-------|
| instruction | validation-instruction.md, create-instruction.md, modify-instruction.md |
| script | validation-script.md, create-script.md, modify-script.md |
| principles | validation-principles.md |
| agent | validation-agent.md, create-agent.md, modify-agent.md |
| skill | validation-skill.md, create-skill.md, modify-skill.md |
| rule | validation-rule.md, create-rule.md, modify-rule.md |
| draft | validation-draft.md |
| structure | validation-structure.md, create-structure.md, modify-structure.md |
| links | validation-links.md |

---

### Фаза 1: Версионирование стандартов (11 файлов)

**Задача:** Добавить "Версия стандарта: 1.0" после заголовка в каждый standard-*.md

| # | Файл | Действие |
|---|------|----------|
| 1.1 | .instructions/standard-instruction.md | Добавить "Версия стандарта: 1.0" |
| 1.2 | .instructions/standard-script.md | Добавить "Версия стандарта: 1.0" |
| 1.3 | .instructions/standard-principles.md | Добавить "Версия стандарта: 1.0" |
| 1.4 | .claude/.instructions/agents/standard-agent.md | Добавить "Версия стандарта: 1.1" (уже обновлён) |
| 1.5 | .claude/.instructions/skills/standard-skill.md | Добавить "Версия стандарта: 1.0" |
| 1.6 | .claude/.instructions/rules/standard-rule.md | Добавить "Версия стандарта: 1.0" |
| 1.7 | .claude/.instructions/drafts/standard-draft.md | Добавить "Версия стандарта: 1.0" |
| 1.8 | .claude/.instructions/state/standard-state.md | Добавить "Версия стандарта: 1.0" |
| 1.9 | .structure/.instructions/standard-frontmatter.md | Добавить "Версия стандарта: 1.0" |
| 1.10 | .structure/.instructions/standard-readme.md | Добавить "Версия стандарта: 1.0" |
| 1.11 | .structure/.instructions/standard-links.md | Добавить "Версия стандарта: 1.0" |

---

### Фаза 2: Рабочая версия в зависимых (21 файл)

**Задача:** Добавить "Рабочая версия стандарта: 1.0" после заголовка

| # | Файл | standard-version |
|---|------|------------------|
| 2.1 | validation-instruction.md | v1.0 |
| 2.2 | create-instruction.md | v1.0 |
| 2.3 | modify-instruction.md | v1.0 |
| 2.4 | validation-script.md | v1.0 |
| 2.5 | create-script.md | v1.0 |
| 2.6 | modify-script.md | v1.0 |
| 2.7 | validation-principles.md | v1.0 |
| 2.8 | validation-agent.md | v1.1 |
| 2.9 | create-agent.md | v1.1 |
| 2.10 | modify-agent.md | v1.1 |
| 2.11 | validation-skill.md | v1.0 |
| 2.12 | create-skill.md | v1.0 |
| 2.13 | modify-skill.md | v1.0 |
| 2.14 | validation-rule.md | v1.0 |
| 2.15 | create-rule.md | v1.0 |
| 2.16 | modify-rule.md | v1.0 |
| 2.17 | validation-draft.md | v1.0 |
| 2.18 | validation-structure.md | v1.0 |
| 2.19 | create-structure.md | v1.0 |
| 2.20 | modify-structure.md | v1.0 |
| 2.21 | validation-links.md | v1.0 |

---

### Фаза 3: Скрипты автоматизации

| # | Скрипт | Назначение | Путь |
|---|--------|------------|------|
| 3.1 | sync-standard-version.py | Найти устаревшие файлы, обновить standard-version | .instructions/.scripts/ |
| 3.2 | bump-standard-version.py | Увеличить версию стандарта | .instructions/.scripts/ |
| 3.3 | check-version-drift.py | Проверить расхождения (для CI) | .instructions/.scripts/ |

**Логика sync-standard-version.py:**
```
1. Принять путь к standard-*.md
2. Прочитать версию из "Версия стандарта: X.Y"
3. Найти все файлы с standard: {путь}
4. Для каждого файла:
   a. Прочитать standard-version из frontmatter
   b. Если отличается:
      - Обновить standard-version
      - Обновить "Рабочая версия стандарта: X.Y"
      - Увеличить version файла (v1.0 → v1.1)
      - Добавить запись в CHANGELOG (если есть)
5. Вывести отчёт
```

---

### Фаза 4: Интеграция Holt

| # | Задача | Файл |
|---|--------|------|
| 4.1 | Добавить режим fix в AGENT.md | .claude/agents/captain-holt/AGENT.md |
| 4.2 | Добавить шаг Holt в create-instruction.md | .instructions/create-instruction.md |
| 4.3 | Добавить шаг Holt в modify-instruction.md | .instructions/modify-instruction.md |
| 4.4 | Создать скилл /holt-validate | .claude/skills/holt-validate/SKILL.md |

**Шаг в create-instruction.md (после создания standard-*.md):**
```markdown
### Шаг N: Валидация Holt (для standard-*.md)

> **Только для файлов с префиксом `standard-`**

1. Запустить Captain Holt: анализ на двойственность
2. При P1 проблемах — исправить, повторить
3. При P2-P3 — показать, спросить
```

---

### Фаза 5: Обновление документации

| # | Задача | Файл |
|---|--------|------|
| 5.1 | Добавить таблицу версий стандартов | .structure/.instructions/standard-frontmatter.md |
| 5.2 | Добавить правило синхронизации | .claude/rules/core.md |
| 5.3 | Обновить README агентов | .claude/.instructions/agents/README.md |

---

### Фаза 6: Валидация Holt всех стандартов

| # | Файл | Статус |
|---|------|--------|
| 6.1 | standard-instruction.md | Ожидает |
| 6.2 | standard-script.md | Ожидает |
| 6.3 | standard-principles.md | Ожидает |
| 6.4 | standard-agent.md | ✅ Проанализирован (37 проблем) |
| 6.5 | standard-skill.md | Ожидает |
| 6.6 | standard-rule.md | Ожидает |
| 6.7 | standard-draft.md | Ожидает |
| 6.8 | standard-state.md | Ожидает |
| 6.9 | standard-frontmatter.md | Ожидает |
| 6.10 | standard-readme.md | Ожидает |
| 6.11 | standard-links.md | Ожидает |

---

### Фаза 7: Тестирование и коммит

| # | Задача |
|---|--------|
| 7.1 | Протестировать sync-standard-version.py на standard-agent.md |
| 7.2 | Проверить каскадное обновление |
| 7.3 | git add + commit + push |

---

## Порядок выполнения

```
Фаза 1 (версии стандартов)
    ↓
Фаза 2 (рабочие версии)
    ↓
Фаза 3 (скрипты) ←── можно параллельно с Фазой 4
    ↓
Фаза 4 (интеграция Holt)
    ↓
Фаза 5 (документация)
    ↓
Фаза 6 (валидация Holt)
    ↓
Фаза 7 (тест + коммит)
```

**Оценка объёма:**
- Фаза 1-2: 32 файла (механические правки)
- Фаза 3: 3 скрипта (~300 строк кода)
- Фаза 4: 3 файла
- Фаза 5: 3 файла
- Фаза 6: 10 анализов Holt
- Фаза 7: тестирование

---

## Следующие шаги

1. ✅ Решены открытые вопросы
2. ✅ Составлен подробный план
3. → Утвердить план
4. → Выполнить по фазам
