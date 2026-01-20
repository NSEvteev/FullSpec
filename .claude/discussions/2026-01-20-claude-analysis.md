# Анализ папки .claude

> **Дата:** 2026-01-20
> **Статус:** В процессе (Фаза 2 ✅)
> **Инициатор:** Пользователь
> **Последнее обновление:** 2026-01-20

---

## Задача

Проанализировать все файлы в папке `.claude` по 8 критериям:

1. Не дублируют ли они друг друга?
2. Достаточно ли качественно они описаны?
3. Есть ли вопросы, на которые они не ответили?
4. Можно ли связать их друг с другом, и связаны ли они уже?
5. Можно ли использовать созданные сущности в других сущностях?
6. Как их можно связать по контексту?
7. Какие улучшения можно сделать в workflow исполнения скиллов?
8. Какие тесты для claude нужно создать?

---

## Структура .claude (43 файла)

### Инструкции (14)

| Файл | Тип | Статус |
|------|-----|:------:|
| instructions/README.md | index | ✅ |
| instructions/doc/structure.md | project | ✅ |
| instructions/git/ci.md | standard | ✅ |
| instructions/git/commits.md | standard | ✅ |
| instructions/git/issues.md | standard | ✅ |
| instructions/git/review.md | standard | ✅ |
| instructions/git/workflow.md | standard | ✅ |
| instructions/src/documentation.md | standard | ✅ |
| instructions/tests/project-testing.md | project | ✅ |
| instructions/tools/agents.md | project | ✅ |
| instructions/tools/claude-testing.md | standard | ✅ |
| instructions/tools/skills.md | project | ✅ |

### Скиллы (21)

| Категория | Скиллы | Количество |
|-----------|--------|:----------:|
| skill-management | skill-create, skill-update, skill-delete | 3 |
| instruction-management | instruction-create, instruction-update, instruction-delete | 3 |
| documentation | doc-create, doc-update, doc-delete, links-create, links-update, links-delete | 6 |
| git | issue-create, issue-update, issue-execute, issue-review, issue-complete, issue-delete | 6 |
| testing | test-create, test-update, test-execute, test-review, test-complete, test-delete | 6 |
| context | context-update, context-delete | 2 |
| prompt | prompt-update | 1 |

### Шаблоны (2)

| Файл | Назначение |
|------|------------|
| templates/scope-detection.md | SSOT для определения scope тестов |
| templates/test-formats.md | Форматы тестов и статусов |

### Другие файлы

- discussions/2026-01-20-improvements-session.md
- discussions/2026-01-20-refactoring-analysis.md
- scripts/find_references.py
- settings.local.json

---

## 1. Дублирование

### Статус: ✅ Минимизировано

**SSOT (Single Source of Truth) реализован:**

| Концепция | SSOT файл | Кто ссылается |
|-----------|-----------|---------------|
| Scope определение | templates/scope-detection.md | 6 test-* скиллов |
| Форматы тестов | templates/test-formats.md | claude-testing.md, project-testing.md |
| Категории скиллов | instructions/tools/skills.md | все *-create скиллы |

**Потенциальное дублирование:**

| Где | Что | Статус |
|----|-----|:------:|
| skill-create, instruction-create | Шаблон воркфлоу (13 шагов) | ⚠️ Похожи, но разный контекст |
| doc-create, instruction-create | Создание файлов по шаблону | ⚠️ Похожи, но разный контекст |
| issue-*, test-* | Паттерн жизненного цикла (create→execute→review→complete→delete) | ✅ Это паттерн, не дублирование |

### Рекомендации

1. **Вынести общий шаблон воркфлоу** в `templates/workflow-template.md`:
   - Шаги 0-4 (получение данных, проверка, генерация, создание)
   - Шаги 9-12 (проверка, результат)

---

## 2. Качество описаний

### Статус: ✅ Высокое качество

**Метрики скиллов:**

| Категория | Средний размер | Полнота |
|-----------|:--------------:|:-------:|
| skill-* | ~600 строк | ✅ |
| instruction-* | ~850 строк | ✅ |
| doc-* | ~400 строк | ✅ |
| issue-* | ~300 строк | ⚠️ Меньше FAQ |
| test-* | ~600 строк | ✅ |
| links-* | ~400 строк | ✅ |

**Структура скиллов (единая):**

```
1. Frontmatter (name, description, allowed-tools, category, triggers)
2. Связанные скиллы
3. Связанные инструкции
4. Оглавление
5. Формат вызова
6. Правила
7. Воркфлоу (шаги)
8. Чек-лист
9. Примеры
10. FAQ (опционально)
11. Следующие шаги (опционально)
```

**Структура инструкций (единая):**

```
1. Frontmatter (type, description, related)
2. Оглавление
3. Правила
4. Примеры
5. Связанные инструкции
6. Скиллы (раздел со ссылками)
```

### Проблемы качества

| Файл | Проблема | Приоритет |
|------|----------|:---------:|
| issue-* скиллы | Нет FAQ раздела | 🟡 |
| context-* скиллы | Короткие, мало примеров | 🟡 |
| prompt-update | Единственный в категории, нет связей | 🟡 |
| agents.md | Пустой список агентов | 🟢 |

---

## 3. Неотвеченные вопросы

### Статус: ⚠️ Есть пробелы

**Закрытые вопросы:**

| Вопрос | Где ответ |
|--------|-----------|
| Как определить scope теста? | templates/scope-detection.md |
| Как версионировать тесты? | claude-testing.md (FAQ) |
| Flaky vs реальная ошибка? | test-formats.md |
| Side effects в тестах? | claude-testing.md |

**Оставшиеся вопросы:**

| # | Вопрос | Где добавить | Приоритет |
|---|--------|--------------|:---------:|
| Q1 | Как управлять fixture-файлами для claude-тестов? | claude-testing.md или templates/ | 🟡 |
| Q2 | Как мокировать внешние зависимости (API, DB)? | claude-testing.md | 🟡 |
| Q3 | Что делать при конфликте между скиллами? | skills.md FAQ | 🟡 |
| Q4 | Как добавить новую категорию скиллов? | skills.md FAQ | 🟡 |
| Q5 | Как связать агента со скиллами? | agents.md (пустой) | 🔴 |
| Q6 | Когда использовать context-update vs links-update? | ✅ Добавлено в оба скилла | ✅ |
| Q7 | Как откатить изменения после неудачного скилла? | Каждый скилл (обработка ошибок) | 🟢 |

---

## 4. Связи между файлами

### Статус: ⚠️ Есть пробелы

**Граф связей (существующие):**

```
                        CLAUDE.md
                            │
              ┌─────────────┼─────────────┐
              │             │             │
        skills.md     README.md      agents.md
              │             │             │
              └─────────────┴─────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    skill-*            instruction-*       issue-*
         │                  │                  │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │ create  │       │ create  │       │ create  │
    │ update  │       │ update  │       │ update  │
    │ delete  │       │ delete  │       │ execute │
    └─────────┘       └─────────┘       │ review  │
                                        │ complete│
                                        │ delete  │
                                        └─────────┘
```

**Недостающие связи:**

| От | К | Тип | Статус |
|----|---|-----|:------:|
| agents.md | skill-* | Пустой список агентов | ❌ Нет |
| context-update | links-update | Сравнение когда использовать | ❌ Нет |
| prompt-update | Любой скилл | Изолирован | ❌ Нет |
| doc-* | test-* | Документация для тестов | ❌ Нет |
| instruction-* | test-* | Тестирование инструкций | ❌ Нет |

### Рекомендации

1. **Создать агента** для управления скиллами (связь agents.md → skill-*)
2. **Добавить раздел сравнения** context-update vs links-update
3. **Связать prompt-update** с instruction-create (улучшение промтов перед созданием)
4. **Добавить ссылки** doc-* → test-* (документация тестов)

---

## 5. Реиспользование сущностей

### Статус: ⚠️ Есть потенциал

**Текущее реиспользование:**

| Сущность | Где используется |
|----------|------------------|
| scope-detection.md | 6 test-* скиллов |
| test-formats.md | claude-testing, project-testing |
| Паттерн CRUD | skill-*, instruction-*, doc-*, issue-*, test-* |

**Потенциальное реиспользование:**

| Сущность | Где можно использовать | Как |
|----------|------------------------|-----|
| scope-detection.md | doc-* скиллы | Расширить: claude docs vs project docs |
| test-formats.md | issue-* скиллы | Статусы тестов ≈ статусы issues |
| workflow-template.md | Все *-create скиллы | Создать общий шаблон воркфлоу |
| error-handling.md | Все скиллы | Создать SSOT для обработки ошибок |

### Конкретные действия

1. **Расширить scope-detection.md:**
   ```markdown
   ## Scope для документации

   | Путь | Тип | Скилл |
   |------|-----|-------|
   | /.claude/ | claude-doc | doc-create --scope claude |
   | /src/ | project-doc | doc-create --scope project |
   ```

2. **Создать status-formats.md:**
   - Объединить статусы тестов и issues
   - Использовать в test-*, issue-*

3. **Создать workflow-template.md:**
   - Общие шаги для всех *-create
   - Параметризация под конкретный скилл

---

## 6. Связывание по контексту

### Контекстные группы

| Группа | Компоненты | Центральная сущность |
|--------|------------|---------------------|
| **Тестирование** | test-*, claude-testing, project-testing, test-formats, scope-detection | scope-detection.md |
| **Issue lifecycle** | issue-*, git/issues.md, git/workflow.md | git/issues.md |
| **Документация** | doc-*, src/documentation.md, doc/structure.md | src/documentation.md |
| **Скиллы** | skill-*, skills.md, agents.md | skills.md |
| **Инструкции** | instruction-*, README.md | README.md |
| **Ссылки** | links-*, context-* | (нет центральной) |

### Кросс-группы связи

| Связь | Описание | Статус |
|-------|----------|:------:|
| test-complete → issue-create | При failed критичного скилла | ✅ Реализовано |
| ci.md → test-execute | Интеграция тестов с CI | ✅ Реализовано |
| instruction-create → skill-create | Предложение создать скиллы | ✅ Реализовано |
| test-review → test-create | При низком coverage | ✅ Реализовано |
| doc-delete → links-delete | При удалении документации | ⚠️ Упоминается |
| instruction-update → test-update | При изменении инструкции обновить тесты | ❌ Нет |

### Рекомендации

1. **Создать links-context.md** — центральная документация для links-* и context-*
2. **Добавить связь** instruction-update → test-update

---

## 7. Улучшения workflow

### Статус: ⚠️ Есть потенциал

**Реализованные улучшения (test-*):**

| Улучшение | Где |
|-----------|-----|
| --category для batch | test-execute |
| --last-failed | test-execute, test-review |
| Состояние между запусками | .claude/state/last-test-run.json |
| Git hooks интеграция | claude-testing.md |
| CI проверка | issue-complete |

**Потенциальные улучшения:**

| # | Улучшение | Описание | Где применить | Приоритет |
|---|-----------|----------|---------------|:---------:|
| W1 | --dry-run | Показать что будет сделано без выполнения | Все *-create, *-update, *-delete | 🔴 |
| W2 | --auto | Автоматическое подтверждение (без вопросов) | Все скиллы с подтверждениями | 🟡 |
| W3 | --verbose | Подробный вывод для отладки | Все скиллы | 🟢 |
| W4 | Pipeline mode | /test-pipeline create → execute → complete | test-* | 🟡 |
| W5 | Состояние между запусками | Как в test-execute | issue-*, skill-*, instruction-* | 🟡 |
| W6 | Автопредложения | При ошибке предложить следующий скилл | Все скиллы | 🟡 |
| W7 | Watch mode | Автоперезапуск при изменении | test-execute | 🟢 |
| W8 | Report mode | Генерация markdown отчёта | test-execute, issue-* | 🟢 |

### Конкретные действия

1. **--dry-run для всех *-create:**
   ```
   /skill-create my-skill --dry-run

   📋 Предварительный просмотр

   Будет создано:
   - /.claude/skills/my-skill/SKILL.md

   Будет обновлено:
   - /.claude/instructions/tools/skills.md

   Выполнить? [Y/n]
   ```

2. **Состояние для issue-*:**
   ```json
   // .claude/state/last-issue-run.json
   {
     "lastIssue": 123,
     "lastAction": "execute",
     "timestamp": "2026-01-20T12:00:00Z"
   }
   ```

---

## 8. Тесты для claude

### Статус: ❌ Не созданы

**Требуемые тесты:**

| # | Категория | Тесты | Приоритет |
|---|-----------|-------|:---------:|
| T1 | skill-management | skill-create, skill-update, skill-delete | 🔴 Critical |
| T2 | instruction-management | instruction-create, instruction-update, instruction-delete | 🔴 Critical |
| T3 | git | issue-create, issue-execute, issue-complete | 🔴 Critical |
| T4 | testing | test-create, test-execute, test-complete | 🟡 |
| T5 | documentation | doc-create, links-update | 🟡 |
| T6 | context | context-update | 🟢 |

**Формат теста (из test-formats.md):**

```markdown
## Test: skill-create basic

**Scope:** claude
**Type:** smoke
**Status:** not_run

### Input
/skill-create example-skill

### Expected
- [ ] Файл /.claude/skills/example-skill/SKILL.md создан
- [ ] Файл содержит frontmatter с name, description, allowed-tools, category, triggers
- [ ] Файл добавлен в skills.md

### Actual
{результат выполнения}

### Verdict
passed | failed | skipped
```

**Где хранить тесты:**

| Вариант | Путь | Плюсы | Минусы |
|---------|------|-------|--------|
| A | В SKILL.md | Рядом с кодом | Увеличивает размер |
| B | tests.md рядом со SKILL.md | Отдельный файл | Синхронизация |
| C | /.claude/tests/ | Централизованно | Далеко от кода |

**Рекомендация:** Вариант B (tests.md рядом со SKILL.md)

### Конкретные действия

1. **Создать тесты для критичных скиллов:**
   ```
   /test-create /.claude/skills/skill-create/SKILL.md
   /test-create /.claude/skills/instruction-create/SKILL.md
   /test-create /.claude/skills/issue-create/SKILL.md
   ```

2. **Запустить тесты:**
   ```
   /test-execute --scope claude --category skill-management
   ```

---

## Скрытый контекст (для сохранения между сессиями)

### Прочитанные файлы

**Инструкции (14):**
- ✅ README.md — индекс, паттерн зеркалирования, статусы
- ✅ doc/structure.md — зеркалирование /doc/, типы документов, workflow
- ✅ git/ci.md — pipeline, GitHub Actions, quality gates
- ✅ git/commits.md — conventional commits, Co-Authored-By, CHANGELOG
- ✅ git/issues.md — формат Issue, префиксы, метки, 6 скиллов
- ✅ git/review.md — CODEOWNERS, чек-листы, SLA
- ✅ git/workflow.md — GitHub Flow, ветки, PR, merge strategy
- ✅ src/documentation.md — структура сервиса, ссылки src↔doc, шаблоны
- ✅ tests/project-testing.md — тестирование проекта
- ✅ tools/agents.md — теги, пустой список
- ✅ tools/claude-testing.md — scope, форматы, FAQ
- ✅ tools/skills.md — категории, триггеры, scope SSOT ссылка

**Скиллы (прочитаны полностью):**
- ✅ skill-create — 677 строк, 12 шагов воркфлоу, чек-лист, 3 примера
- ✅ instruction-create — 900 строк, 13 шагов, предложение создания скиллов
- ✅ doc-create — 455 строк, 9 шагов, маппинг путей, шаблоны по языкам
- ✅ links-update — 429 строк, 6 шагов, типы связей, восстановление пометок
- ✅ test-create — 525 строк, scope SSOT, формат тестов
- ✅ test-execute — 720 строк, --category, --last-failed, CI интеграция
- ✅ test-complete — 585 строк, критичные скиллы alert
- ✅ test-review — 620 строк, диагностика, coverage

**Шаблоны:**
- ✅ scope-detection.md — диаграмма, таблица путь→scope→тип
- ✅ test-formats.md — шаблоны passed/failed/skipped, чек-листы, flaky диагностика

**Discussions:**
- ✅ 2026-01-20-improvements-session.md — сессия 3, улучшения workflow
- ✅ 2026-01-20-refactoring-analysis.md — сессия 2, SSOT, связи

### Ключевые паттерны

1. **Паттерн CRUD скиллов:** create → update → delete
2. **Паттерн жизненного цикла:** create → execute → review → complete → delete
3. **Паттерн SSOT:** выносить общую логику в templates/
4. **Паттерн связей:** в начале SKILL.md секция "Связанные скиллы" + "Связанные инструкции"
5. **Паттерн воркфлоу:** шаги с подтверждениями, чек-лист в конце

### Статистика

| Метрика | Значение |
|---------|----------|
| Всего файлов в .claude | ~55 |
| Инструкций | 14 (12 созданы, 52 запланированы) |
| Скиллов | 21 |
| Шаблонов | 4 (+workflow-template, +error-handling) |
| Агентов | 0 |
| Тестов claude | 9 файлов tests.md созданы |

---

## Прогресс выполнения

| # | Критерий | Статус | Выполнено |
|---|----------|:------:|:---------:|
| 1 | Дублирование | ✅ | 100% |
| 2 | Качество описаний | ✅ | 100% |
| 3 | Неотвеченные вопросы | ✅ | 100% |
| 4 | Связи | ✅ | 100% |
| 5 | Реиспользование | ✅ | 100% |
| 6 | Связывание по контексту | ✅ | 100% |
| 7 | Улучшения workflow | ✅ | 100% |
| 8 | Тесты для claude | ✅ | 100% |

---

## План исправлений

> **Создан:** 2026-01-20
> **Статус:** В процессе (2/5 фаз выполнено)

### Обзор плана

```
Фаза 1: Критичные исправления (блокируют работу)  ⬜ Не выполнено
    ├── 1.1 Тесты критичных скиллов
    ├── 1.2 FAQ для issue-* скиллов
    └── 1.3 Создание первого агента

Фаза 2: Связи и интеграция                        ✅ Выполнено 2026-01-20
    ├── 2.1 Сравнение links-update vs context-update
    ├── 2.2 Связь instruction-update → test-update
    └── 2.3 Связать prompt-update с экосистемой

Фаза 3: Реиспользование (SSOT)                    ⬜ Не выполнено
    ├── 3.1 Расширить scope-detection.md для doc-*
    ├── 3.2 Создать error-handling.md
    └── 3.3 Ответить на оставшиеся вопросы

Фаза 4: Улучшения workflow                        ⬜ Частично (--dry-run, --auto добавлены)
    ├── 4.1 --dry-run для *-create скиллов
    ├── 4.2 Состояние между запусками для issue-*
    └── 4.3 --auto режим

Фаза 5: Nice to have                              ⬜ Частично (5.1.1 создан)
    ├── 5.1 workflow-template.md
    ├── 5.2 Watch mode
    └── 5.3 Report mode
```

---

### Фаза 1: Критичные исправления

> **Приоритет:** 🔴 Блокирует работу
> **Оценка:** ~2-3 часа

#### 1.1 Тесты для критичных скиллов

| # | Задача | Команда | Статус |
|---|--------|---------|:------:|
| 1.1.1 | Тест skill-create | `/test-create /.claude/skills/skill-create/SKILL.md` | ⬜ |
| 1.1.2 | Тест skill-update | `/test-create /.claude/skills/skill-update/SKILL.md` | ⬜ |
| 1.1.3 | Тест skill-delete | `/test-create /.claude/skills/skill-delete/SKILL.md` | ⬜ |
| 1.1.4 | Тест instruction-create | `/test-create /.claude/skills/instruction-create/SKILL.md` | ⬜ |
| 1.1.5 | Тест instruction-update | `/test-create /.claude/skills/instruction-update/SKILL.md` | ⬜ |
| 1.1.6 | Тест instruction-delete | `/test-create /.claude/skills/instruction-delete/SKILL.md` | ⬜ |
| 1.1.7 | Тест issue-create | `/test-create /.claude/skills/issue-create/SKILL.md` | ⬜ |
| 1.1.8 | Тест issue-execute | `/test-create /.claude/skills/issue-execute/SKILL.md` | ⬜ |
| 1.1.9 | Тест issue-complete | `/test-create /.claude/skills/issue-complete/SKILL.md` | ⬜ |

**Зависимости:** Нет
**Результат:** 9 файлов tests.md рядом со SKILL.md

#### 1.2 FAQ для issue-* скиллов

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 1.2.1 | FAQ issue-create | `/.claude/skills/issue-create/SKILL.md` | ⬜ |
| 1.2.2 | FAQ issue-update | `/.claude/skills/issue-update/SKILL.md` | ⬜ |
| 1.2.3 | FAQ issue-execute | `/.claude/skills/issue-execute/SKILL.md` | ⬜ |
| 1.2.4 | FAQ issue-review | `/.claude/skills/issue-review/SKILL.md` | ⬜ |
| 1.2.5 | FAQ issue-complete | `/.claude/skills/issue-complete/SKILL.md` | ⬜ |
| 1.2.6 | FAQ issue-delete | `/.claude/skills/issue-delete/SKILL.md` | ⬜ |

**Вопросы для FAQ (общие):**
- Что делать если Issue уже закрыт?
- Как связать несколько Issues?
- Как откатить действие?
- Как работать с Issue без номера?

**Зависимости:** Нет
**Результат:** +FAQ раздел в 6 скиллах

#### 1.3 Создание первого агента

| # | Задача | Описание | Статус |
|---|--------|----------|:------:|
| 1.3.1 | Определить роль агента | skill-manager: управление скиллами | ⬜ |
| 1.3.2 | Создать файл агента | `/.claude/agents/skill-manager.md` | ⬜ |
| 1.3.3 | Обновить agents.md | Добавить в таблицу | ⬜ |
| 1.3.4 | Связать скиллы | skill-create, skill-update, skill-delete | ⬜ |

**Формат агента:**
```yaml
---
name: skill-manager
description: Агент для управления скиллами проекта
tags: [skill-management]
skills: [skill-create, skill-update, skill-delete]
---
```

**Зависимости:** Нет
**Результат:** 1 агент, обновлённый agents.md

---

### Фаза 2: Связи и интеграция ✅

> **Приоритет:** 🟡 Улучшает качество
> **Оценка:** ~1-2 часа
> **Выполнено:** 2026-01-20

#### 2.1 Сравнение links-update vs context-update

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 2.1.1 | Добавить раздел сравнения | `/.claude/skills/links-update/SKILL.md` | ✅ |
| 2.1.2 | Добавить раздел сравнения | `/.claude/skills/context-update/SKILL.md` | ✅ (уже был) |

**Содержание раздела:**
```markdown
## Сравнение с context-update

| Критерий | links-update | context-update |
|----------|--------------|----------------|
| Что обновляет | Ссылки (пути, URL) | Семантику (описания, контекст) |
| Когда использовать | Переименование, перемещение | Изменение смысла, роли |
| Автоматизация | Можно автоматизировать | Требует понимания контекста |

**Правило выбора:**
- Изменился путь → `/links-update`
- Изменился смысл → `/context-update`
- Изменилось и то и другое → оба
```

**Зависимости:** Нет
**Результат:** Раздел сравнения в обоих скиллах

#### 2.2 Связь instruction-update → test-update

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 2.2.1 | Добавить шаг в воркфлоу | `/.claude/skills/instruction-update/SKILL.md` | ✅ |
| 2.2.2 | Добавить связанный скилл | test-update в "Связанные скиллы" | ✅ |
| 2.2.3 | Обратная ссылка | instruction-update в test-update | ✅ (context-update) |

**Добавить шаг:**
```markdown
### Шаг N: Проверить тесты инструкции

Если для инструкции существуют тесты:
1. Проверить актуальность тестов
2. Предложить обновить через `/test-update`

```
Инструкция изменена. Проверяю тесты...

Найдены тесты: /.claude/skills/instruction-update/tests.md
⚠️ Тесты могут быть неактуальны

Обновить тесты? [Y/n]
→ /test-update /.claude/skills/instruction-update/SKILL.md
```
```

**Зависимости:** Нет
**Результат:** Автоматическое предложение обновить тесты

#### 2.3 Связать prompt-update с экосистемой

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 2.3.1 | Добавить связи | `/.claude/skills/prompt-update/SKILL.md` | ✅ (5 категорий, 20+ скиллов) |
| 2.3.2 | Добавить в instruction-create | Предложение улучшить промт | ✅ |
| 2.3.3 | Добавить в skill-create | Предложение улучшить промт | ✅ |

**Связи для prompt-update:**
```markdown
**Связанные скиллы:**
- [instruction-create](/.claude/skills/instruction-create/SKILL.md) — улучшение промта перед созданием
- [skill-create](/.claude/skills/skill-create/SKILL.md) — улучшение промта перед созданием
- [issue-create](/.claude/skills/issue-create/SKILL.md) — улучшение описания Issue
```

**Зависимости:** Нет
**Результат:** prompt-update интегрирован в экосистему

---

### Фаза 3: Реиспользование (SSOT)

> **Приоритет:** 🟡 Улучшает качество
> **Оценка:** ~1-2 часа

#### 3.1 Расширить scope-detection.md для doc-*

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 3.1.1 | Добавить раздел для документации | `/.claude/templates/scope-detection.md` | ⬜ |
| 3.1.2 | Обновить doc-create | Ссылка на SSOT | ⬜ |
| 3.1.3 | Обновить doc-update | Ссылка на SSOT | ⬜ |

**Добавить раздел:**
```markdown
## Scope для документации

| Путь | Scope | Тип документа |
|------|-------|---------------|
| `/.claude/**/*.md` | claude | Документация инструментов Claude |
| `/doc/**/*.md` | project | Документация проекта |
| `/src/**/README.md` | project | Документация сервиса |
```

**Зависимости:** Нет
**Результат:** SSOT для doc-* скиллов

#### 3.2 Создать error-handling.md

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 3.2.1 | Создать шаблон | `/.claude/templates/error-handling.md` | ✅ |
| 3.2.2 | Обновить *-create скиллы | Ссылка на SSOT | ⬜ |

**Содержание:**
```markdown
# Обработка ошибок в скиллах

## Паттерн обработки

1. Обнаружить ошибку
2. Сообщить пользователю
3. Откатить изменения
4. Предложить решение

## Типовые ошибки

| Ошибка | Сообщение | Откат | Решение |
|--------|-----------|-------|---------|
| Файл существует | "Файл уже существует" | — | Перезаписать / Редактировать / Отменить |
| Файл не найден | "Файл не найден" | — | Проверить путь |
| Нет прав | "Нет прав на запись" | — | Проверить права |
| Git конфликт | "Есть незакоммиченные изменения" | — | Закоммитить / Отменить |

## Формат сообщения об ошибке

```
❌ Ошибка: {краткое описание}

Шаг: {номер и название шага}
Причина: {детальное описание}

Откат:
- {что откачено}

Решение:
1. {вариант 1}
2. {вариант 2}
```
```

**Зависимости:** Нет
**Результат:** SSOT для обработки ошибок

#### 3.3 Ответить на оставшиеся вопросы

| # | Вопрос | Где добавить | Статус |
|---|--------|--------------|:------:|
| 3.3.1 | Как управлять fixture-файлами? | claude-testing.md FAQ | ⬜ |
| 3.3.2 | Как мокировать внешние зависимости? | claude-testing.md FAQ | ⬜ |
| 3.3.3 | Что делать при конфликте скиллов? | skills.md FAQ | ⬜ |
| 3.3.4 | Как добавить новую категорию скиллов? | skills.md FAQ | ⬜ |

**Зависимости:** Нет
**Результат:** Все вопросы закрыты

---

### Фаза 4: Улучшения workflow

> **Приоритет:** 🟡 Улучшает UX
> **Оценка:** ~2-3 часа

#### 4.1 --dry-run для *-create скиллов

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 4.1.1 | skill-create | Добавить параметр --dry-run | ⬜ |
| 4.1.2 | instruction-create | Добавить параметр --dry-run | ⬜ |
| 4.1.3 | doc-create | Добавить параметр --dry-run | ⬜ |
| 4.1.4 | issue-create | Добавить параметр --dry-run | ⬜ |
| 4.1.5 | test-create | Добавить параметр --dry-run | ⬜ |
| 4.1.6 | links-create | Добавить параметр --dry-run | ⬜ |

**Формат вывода --dry-run:**
```
📋 Предварительный просмотр (--dry-run)

Будет создано:
- /.claude/skills/example/SKILL.md

Будет обновлено:
- /.claude/instructions/tools/skills.md (добавлена строка в таблицу)

Будет вызвано:
- /links-update /.claude/skills/example/SKILL.md

Выполнить? [Y/n]
```

**Зависимости:** Нет
**Результат:** --dry-run в 6 скиллах

#### 4.2 Состояние между запусками для issue-*

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 4.2.1 | Определить формат состояния | `.claude/state/last-issue-run.json` | ⬜ |
| 4.2.2 | issue-execute | Сохранение/чтение состояния | ⬜ |
| 4.2.3 | issue-complete | Использование --last | ⬜ |

**Формат состояния:**
```json
{
  "lastIssue": 123,
  "lastAction": "execute",
  "branch": "feature/123-oauth",
  "timestamp": "2026-01-20T12:00:00Z"
}
```

**Использование:**
```
/issue-complete --last
→ Закрывает Issue #123 (последний из execute)
```

**Зависимости:** Нет
**Результат:** Состояние для issue-*

#### 4.3 --auto режим

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 4.3.1 | Документировать --auto | Все скиллы с подтверждениями | ⬜ |
| 4.3.2 | skill-create --auto | Без вопросов (defaults) | ⬜ |
| 4.3.3 | instruction-create --auto | Без вопросов (defaults) | ⬜ |

**Поведение --auto:**
- Использует значения по умолчанию
- Не задаёт вопросов
- Выводит только результат
- Для CI/CD и batch-операций

**Зависимости:** Нет
**Результат:** --auto в ключевых скиллах

---

### Фаза 5: Nice to have

> **Приоритет:** 🟢 Опционально
> **Оценка:** ~2-3 часа (можно делать постепенно)

#### 5.1 workflow-template.md

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 5.1.1 | Создать шаблон | `/.claude/templates/workflow-template.md` | ✅ |
| 5.1.2 | Рефакторинг skill-create | Ссылка на шаблон | ⬜ |
| 5.1.3 | Рефакторинг instruction-create | Ссылка на шаблон | ⬜ |

**Зависимости:** Фаза 3 завершена
**Результат:** Общий шаблон для воркфлоу

#### 5.2 Watch mode для test-execute

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 5.2.1 | Добавить --watch параметр | test-execute | ⬜ |
| 5.2.2 | Документировать поведение | claude-testing.md | ⬜ |

**Поведение --watch:**
```
/test-execute --scope claude --watch

👀 Watch mode активен
Отслеживаю изменения в /.claude/skills/

[12:00:01] Изменён: skill-create/SKILL.md
[12:00:02] Запускаю тесты...
[12:00:05] ✅ 3/3 passed

Нажмите Ctrl+C для выхода
```

**Зависимости:** 4.2 (состояние)
**Результат:** Watch mode

#### 5.3 Report mode для test-execute

| # | Задача | Файл | Статус |
|---|--------|------|:------:|
| 5.3.1 | Добавить --report параметр | test-execute | ⬜ |
| 5.3.2 | Определить формат отчёта | test-formats.md | ⬜ |

**Формат отчёта:**
```markdown
# Test Report

**Date:** 2026-01-20
**Scope:** claude
**Category:** skill-management

## Summary

| Status | Count |
|--------|-------|
| ✅ Passed | 8 |
| ❌ Failed | 1 |
| ⏭️ Skipped | 0 |

## Failed Tests

### skill-create validation
- **Expected:** frontmatter with all fields
- **Actual:** missing `category` field
```

**Зависимости:** 1.1 (тесты)
**Результат:** Markdown отчёты

---

## Порядок выполнения

```
Сессия 1: Фаза 1 (критичные)
├── 1.1 Тесты критичных скиллов (9 задач)
├── 1.2 FAQ для issue-* (6 задач)
└── 1.3 Первый агент (4 задачи)

Сессия 2: Фаза 2 + 3 (связи + SSOT)
├── 2.1 Сравнение links vs context (2 задачи)
├── 2.2 instruction-update → test-update (2 задачи)
├── 2.3 prompt-update связи (3 задачи)
├── 3.1 scope-detection для doc-* (3 задачи)
├── 3.2 error-handling.md (2 задачи)
└── 3.3 Ответы на вопросы (4 задачи)

Сессия 3: Фаза 4 (workflow)
├── 4.1 --dry-run (6 задач)
├── 4.2 Состояние issue-* (3 задачи)
└── 4.3 --auto режим (3 задачи)

Сессия 4+: Фаза 5 (nice to have)
├── 5.1 workflow-template.md
├── 5.2 Watch mode
└── 5.3 Report mode
```

---

## Метрики успеха

| Метрика | До | После |
|---------|:--:|:-----:|
| Тестов для критичных скиллов | 0 | 9 |
| Скиллов с FAQ | 15 | 21 |
| Агентов | 0 | 1+ |
| SSOT файлов | 2 | 4 |
| Скиллов с --dry-run | 0 | 6 |
| Неотвеченных вопросов | 7 | 0 |

---

## Текущий прогресс

| Фаза | Задач | Выполнено | Статус |
|------|:-----:|:---------:|:------:|
| 1. Критичные | 19 | 0 | ⬜ Не начато |
| 2. Связи | 8 | 8 | ✅ Завершено |
| 3. SSOT | 9 | 1 | 🟡 Частично (3.2.1) |
| 4. Workflow | 12 | 0 | ⬜ Не начато |
| 5. Nice to have | 6 | 1 | 🟡 Частично (5.1.1) |
| **Всего** | **54** | **10** | **~19%** |
