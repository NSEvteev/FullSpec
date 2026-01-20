# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Точка входа для Claude Code. **Справочная информация** о проекте.

> 📖 **CLAUDE.md** — справочник со ссылками и статусами.
> 📋 **/.claude/instructions/** — инструкции для LLM (правила работы).

---

## ⚠️ ШАГ 0: Проверка скиллов (ОБЯЗАТЕЛЬНО)

> **КРИТИЧЕСКОЕ ПРАВИЛО:** Перед выполнением ЛЮБОГО запроса пользователя — проверить скиллы!

### Алгоритм (выполнять ВСЕГДА)

```
1. Получил запрос пользователя
2. СТОП — не начинаю выполнение
3. Читаю список скиллов: /.claude/instructions/tools/skills.md
4. Проверяю: есть ли скилл для этой задачи?
   - Создать инструкцию → /instruction-create
   - Создать скилл → /skill-create
   - Создать документ → /doc-create
   - Создать issue → /issue-create
   - Обновить ссылки → /links-update
   - И т.д.
5. Если скилл ЕСТЬ → использую скилл
6. Если скилла НЕТ → выполняю вручную
```

### Самопроверка перед действием

Перед использованием `Write`, `Edit`, `mkdir` для файлов в `/.claude/`:

```
⚠️ ПРОВЕРКА: {путь к файлу}
Тип: {skill | instruction | agent | doc | other}
Скилл существует: {да → название | нет}
→ Использую: {/skill-name | ручное создание}
```

**Если скилл существует, но я собираюсь делать вручную → СТОП → использовать скилл.**

### Блокирующие пути

| Путь | Скилл | Ручное создание |
|------|-------|-----------------|
| `/.claude/skills/*/SKILL.md` | `/skill-create` | ❌ ЗАПРЕЩЕНО |
| `/.claude/instructions/**/*.md` | `/instruction-create` | ❌ ЗАПРЕЩЕНО |
| `/.claude/agents/*.md` | спросить пользователя | ⚠️ уточнить |

---

## Язык

Используй русский язык для коммуникаций и комментариев в коде.

## Блокирующее подтверждение

**СТОП-ПРАВИЛО:** Если в воркфлоу скилла есть шаг с:
- "подтверждение"
- "спросить пользователя"
- "[Y/n]"
- "Применить?"

То Claude ОБЯЗАН:
1. Вывести информацию
2. Задать вопрос
3. **ОСТАНОВИТЬСЯ И ЖДАТЬ ОТВЕТА**
4. НЕ продолжать выполнение до ответа пользователя

Нарушение этого правила = критическая ошибка.

## Использование скиллов

**КРИТИЧНО:** При любом запросе пользователя проверять, можно ли использовать пользовательские скиллы из [/.claude/skills/](/.claude/skills/).

Список скиллов: [/.claude/instructions/tools/skills.md](/.claude/instructions/tools/skills.md)

Приоритет: пользовательские скиллы > ручное выполнение.

## Статус проекта

Проект в процессе рефакторинга. Целевая структура описана в [refactoring.md](refactoring.md).

**Временные папки (для примеров):**
- `.claude_old/` — старая структура Claude
- `llm_instructions_old/` — старые инструкции

## Инициализация проекта

> **Блокирующее требование:** Все инструкции из [/.claude/instructions/README.md](/.claude/instructions/README.md) должны быть созданы и заполнены перед началом работы с проектом.

Для создания инструкции используйте `/instruction-create <путь>`.

### Типы инструкций

| Тип | Назначение | При инициализации |
|-----|------------|-------------------|
| `standard` | Стандарты качества (КАК делать) | Использовать as-is |
| `project` | Специфика проекта (ЧТО есть) | Заполнить под проект |

## Структура проекта

```
/.claude/                   # Инструменты Claude
  /instructions/            # Инструкции для LLM
  /agents/                  # Агенты
  /skills/                  # Скиллы
  /scripts/                 # Скрипты Python
  /templates/               # Шаблоны
  /discussions/             # Дискуссии

/src/                       # Код сервисов
/doc/                       # Документация
/shared/                    # Общий код
/config/                    # Конфигурации окружений
/platform/                  # Инфраструктура
/tests/                     # Системные тесты
```

## Инструкции

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md)

**Правило:** При работе с папкой `/X/` — читать `/.claude/instructions/X/README.md`.

## Ключевые файлы

| Файл | Назначение |
|------|------------|
| `/doc/glossary.md` | Глоссарий терминов |
| `/.claude/discussions/` | Активные дискуссии |
| `/doc/src/{service}/specs/adr/` | ADR сервиса |

## Задачи

Задачи ведутся через GitHub Issues с префиксами:
- `[AUTH]`, `[NOTIFY]`, `[PAY]` — по сервисам
- `[INFRA]` — инфраструктура
- `[DOCS]` — документация

```bash
gh issue list --state open
gh issue create --label "service:auth" --title "[AUTH] Описание"
```

## Команды

**Все команды:** [Makefile](Makefile) или `make help`

```bash
make dev           # Запустить для разработки
make test          # Запустить тесты
make lint          # Линтинг
```

## Подробнее

Полное описание структуры и правил: [refactoring.md](refactoring.md)

---

## 📌 При следующем запуске

> **Дата:** 2026-01-20
> **Статус:** Рефакторинг в процессе

---

### ✅ ВЫПОЛНЕНО В ЭТОЙ СЕССИИ

| Задача | Статус |
|--------|--------|
| Блок 1: skill-update проверен | ✅ Файл в порядке |
| Блок 1: Циклические зависимости | ✅ Ложная проблема — циклов нет |
| instruction-update: добавлен Шаг 8 (context-update) | ✅ |
| git/ci.md: + Скиллы, + rollback, + alerting | ✅ |
| git/review.md: + SLA, + self-review чек-лист | ✅ |
| git/workflow.md: + Скиллы, + related | ✅ |
| issue-review: + ссылка на self-review чек-лист | ✅ |

---

### ✅ ВЫПОЛНЕНО В ЭТОЙ СЕССИИ (продолжение)

| Задача | Статус |
|--------|--------|
| Блок A.1: testing.md → claude-testing.md | ✅ |
| Блок A.2: tools/skills.md (+ related, + стандарт параметров) | ✅ |
| Блок B.1: tests/README.md создан | ✅ |
| Блок B.2: /tests/ обновлён в refactoring.md | ✅ |

---

### ✅ БЛОК C ВЫПОЛНЕН

Созданы 6 test-* скиллов с автоопределением scope:
- [test-create](/.claude/skills/test-create/SKILL.md) ✅
- [test-update](/.claude/skills/test-update/SKILL.md) ✅
- [test-review](/.claude/skills/test-review/SKILL.md) ✅
- [test-execute](/.claude/skills/test-execute/SKILL.md) ✅
- [test-complete](/.claude/skills/test-complete/SKILL.md) ✅
- [test-delete](/.claude/skills/test-delete/SKILL.md) ✅

---

### 🟡 ТЕКУЩИЙ ПЛАН

#### Задача: Переименовать tests/README.md → project-testing.md

По аналогии с `claude-testing.md`:
- `tools/claude-testing.md` — тесты Claude Code
- `tools/project-testing.md` — тесты проекта (бывший tests/README.md)

#### Блок D: Создать критические инструкции

| # | Инструкция | Тип | Почему критично |
|---|------------|-----|-----------------|
| D.1 | src/dev/local.md | project | Как запустить проект локально |
| D.2 | config/environments.md | project | Какие окружения есть |

---

### 📊 ГРАФ СВЯЗЕЙ СКИЛЛОВ (обновлённый)

```
ТРИАДЫ СКИЛЛОВ:

skill-*:       create ←→ update ←→ delete
instruction-*: create ←→ update ←→ delete
doc-*:         create ←→ update ←→ delete
links-*:       create ←→ update ←→ delete
context-*:     update ←→ delete
test-*:        create ←→ update ←→ review ←→ execute ←→ complete ←→ delete  # НОВОЕ

issue-*:       create → update → execute → review → complete
                                                 ↘ delete

ЦЕПОЧКИ ВЫЗОВОВ:

instruction-create:
  └→ links-update (Шаг 7)
  └→ context-update (Шаг 8)
  └→ instruction-update (Шаг 9)
  └→ skill-update (Шаг 10)
  └→ skill-create (Шаг 11, если пользователь согласен)

instruction-update:
  └→ context-update (Шаг 8)  # ДОБАВЛЕНО

skill-create:
  └→ links-update (Шаг 9)
  └→ skill-update (Шаг 10)
```

---

### 📋 ПОРЯДОК ВЫПОЛНЕНИЯ

```
1. Блок A — завершить инструкции
2. Коммит + пуш

3. Блок B — создать структуру тестов
4. Коммит + пуш

5. Блок C — создать скиллы test-*
6. Коммит + пуш

7. Блок D — создать критические инструкции
8. Коммит + пуш

9. Удалить этот раздел из CLAUDE.md
```

---

### 📈 МЕТРИКИ ДЛЯ ОТСЛЕЖИВАНИЯ

После завершения проверить:

- [ ] Все инструкции имеют раздел "Скиллы"
- [ ] Все frontmatter имеют полные related
- [ ] `testing.md` переименован в `claude-testing.md`
- [ ] Создана структура `/.claude/instructions/tests/`
- [ ] Создано 6 скиллов test-*
- [ ] Обновлён `/tests/` в refactoring.md (добавлен smoke/)
