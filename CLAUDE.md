# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Точка входа для Claude Code. **Справочная информация** о проекте.

---

## Проверка скиллов (ОБЯЗАТЕЛЬНО)

> **КРИТИЧЕСКОЕ ПРАВИЛО:** Перед выполнением ЛЮБОГО запроса пользователя — проверить скиллы!

### Алгоритм (выполнять ВСЕГДА)

```
1. Получил запрос пользователя
2. СТОП — не начинаю выполнение
3. Читаю список скиллов: /.claude/skills/README.md
4. Проверяю: есть ли скилл для этой задачи?
   - Создать инструкцию → /instruction-create
   - Изменить инструкцию → /instruction-modify
   - Проверить инструкцию → /instruction-validate
   - Создать скрипт → /script-create
   - Изменить скрипт → /script-modify
   - Проверить скрипт → /script-validate
   - Создать скилл → /skill-create
   - Изменить скилл → /skill-modify
   - Проверить скилл → /skill-validate
   - Проверить ссылки → /links-validate
   - Создать папку → /structure-create
   - Изменить папку → /structure-modify
   - Проверить структуру → /structure-validate
5. Если скилл ЕСТЬ → использую скилл
6. Если скилла НЕТ → выполняю вручную
```

### Блокирующие пути

| Путь | Скилл | Ручное создание |
|------|-------|-----------------|
| `**/.instructions/**/*.md` | `/instruction-create`, `/instruction-modify` | ЗАПРЕЩЕНО |
| `/.claude/skills/*/SKILL.md` | `/skill-create`, `/skill-modify` | ЗАПРЕЩЕНО |

---

## Блокирующее подтверждение

**СТОП-ПРАВИЛО:** Если в воркфлоу скилла есть шаг с "подтверждение", "[Y/n]", "Применить?" — Claude ОБЯЗАН остановиться и ждать ответа пользователя.

## Формат вопросов

При предложении вариантов выбора **ВСЕГДА** использовать `AskUserQuestion` tool с кликабельными опциями.

---

## Скиллы (13)

| Категория | Скиллы |
|-----------|--------|
| instruction-* | create, modify, validate |
| script-* | create, modify, validate |
| skill-* | create, modify, validate |
| links-* | validate |
| structure-* | create, modify, validate |

Полный список: [/.claude/skills/README.md](/.claude/skills/README.md)

---

## Инструкции

> **Инструкции = ТОЛЬКО стандарты (КАК делать).**
> Они НЕ описывают структуру папок — это делает README.

| Область | Путь |
|---------|------|
| Как писать инструкции | `/.instructions/` |
| Как писать скиллы | `/.claude/.instructions/skills/` |

---

## Структура

```
/.claude/
├── .instructions/skills/    # Как писать скиллы
├── skills/                  # Скиллы (13)
├── agents/                  # Агенты
├── drafts/                  # Черновики (в git)
└── settings.json            # Настройки

/.instructions/              # Как писать инструкции
```

---

## Команды

**Все команды:** [Makefile](Makefile) или `make help`

```bash
make dev           # Запустить для разработки
make test          # Запустить тесты
make lint          # Линтинг
```

---

## Запрет архивирования инструкций

**ПРАВИЛО:** Архивирование инструкций ЗАПРЕЩЕНО.

**Вместо архивирования:**
1. **Деактивировать** — закомментировать содержимое (см. [modify-instruction.md](/.instructions/modify-instruction.md))
2. **Заменить** — создать новую инструкцию, деактивировать старую

---
