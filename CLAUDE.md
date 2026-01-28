# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Точка входа для Claude Code. **Справочная информация** о проекте.

---

## TODO (29.01.2026)

- [ ] **Продолжить:** `.claude/drafts/scripts-for-instructions.md`
  - [ ] `create-script-file.py` — создание скрипта по шаблону
  - [ ] Обновить инструкции со ссылками на новые скрипты
- [ ] Исправить битые ссылки (414 ошибок) — отдельная сессия

### Выполнено (28.01.2026)
- [x] Скрипты и инструкции v2 — полная переработка `.instructions/`
- [x] 7 новых скриптов, 2 новые инструкции (principles)

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
   - Создать скилл → /skill-create
   - Создать спецификацию → /spec-create
   - Изменить статус спецификации → /spec-status
   - Работать со спецификацией → /spec-update
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
| `/.claude/skills/*/SKILL.md` | `/skill-create` | ЗАПРЕЩЕНО |
| `/specs/**` | `/spec-create`, `/spec-update`, `/spec-status` | ЗАПРЕЩЕНО |

---

## Блокирующее подтверждение

**СТОП-ПРАВИЛО:** Если в воркфлоу скилла есть шаг с "подтверждение", "[Y/n]", "Применить?" — Claude ОБЯЗАН остановиться и ждать ответа пользователя.

## Формат вопросов

При предложении вариантов выбора **ВСЕГДА** использовать `AskUserQuestion` tool с кликабельными опциями.

---

## Скиллы (13)

| Категория | Скиллы |
|-----------|--------|
| instruction-* | create, modify |
| skill-* | create, delete, migrate, update |
| spec-* | create, status, update |
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
| Как писать specs | `/specs/.instructions/` |

---

## Структура

```
/.claude/
├── .instructions/skills/    # Как писать скиллы
├── skills/                  # Скиллы (14)
├── agents/                  # Агенты
├── drafts/                  # Черновики (в git)
└── settings.json            # Настройки

/.instructions/              # Как писать инструкции
/specs/.instructions/        # Как писать specs
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
