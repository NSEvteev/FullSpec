# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Язык проекта

Используй русский язык для всех коммуникаций и комментариев в коде.

## Обзор проекта

Платформа для разработки, бэктестинга и исполнения торговых стратегий.

---

## Правила для Claude

### Структура инструкций

| Файл | Назначение |
|------|------------|
| **CLAUDE.md** | Быстрый справочник (этот файл) |
| [llm_instructions.md](llm_instructions/llm_instructions.md) | Полный индекс инструкций и структура проекта |

**Важно:** CLAUDE.md содержит краткую информацию для быстрого старта. Для полного понимания контекста проекта — см. [llm_instructions.md](llm_instructions/llm_instructions.md).

### Синхронизация инструкций

При изменении любого файла в `llm_instructions/` — обновить CLAUDE.md релевантной информацией.

### Сохранение новых правил

При введении пользователем новых правил или инструкций для Claude — предложить:
1. Сохранить правила в `llm_instructions/` (новый файл или существующий)
2. Обновить [llm_instructions.md](llm_instructions/llm_instructions.md) — добавить в индекс
3. Обновить CLAUDE.md — добавить краткую информацию

---

## Быстрый старт LLM

1. **Контекст проекта:** Ознакомиться с [llm_instructions.md](llm_instructions/llm_instructions.md)
2. **Новая сессия:** Проверить [current_tasks.md](llm_tasks/current_tasks.md)
3. **Документация:** Следовать [instructions_general_docs.md](llm_instructions/instructions_general_docs.md)
4. **Термины:** Добавлять в [glossary.md](general_docs/glossary.md)
5. **Скрипты:** См. [instructions_scripts.md](llm_instructions/instructions_scripts.md)

---

## Инструкции для LLM

| Инструкция | Назначение |
|------------|------------|
| [instructions_general_docs.md](llm_instructions/instructions_general_docs.md) | Правила ведения документации |
| [instructions_scripts.md](llm_instructions/instructions_scripts.md) | Служебные скрипты |
| [instructions_agents.md](llm_instructions/instructions_agents.md) | AI-агенты Claude Code |
| [instructions_skills.md](llm_instructions/instructions_skills.md) | Скиллы Claude Code |

## Управление задачами

| Файл | Назначение |
|------|------------|
| [current_tasks.md](llm_tasks/current_tasks.md) | Текущие задачи сессии |
| [future_tasks.md](llm_tasks/future_tasks.md) | Бэклог задач |

---

## Команды

<!-- TODO: Заполнить после выбора стека -->

## Переменные окружения (.env)

<!-- TODO: Заполнить после настройки проекта -->

## Архитектура

<!-- TODO: Заполнить после создания архитектурных документов -->

## Заглушки (Mocks)

<!-- TODO: Заполнить при необходимости -->

---

## Документация

Проект использует структурированную систему документации.

### Структура документации

```
general_docs/
├── glossary.md             # Глоссарий терминов проекта
├── discuss/                # Дискуссии (идея → решение)
├── architecture/           # Архитектурные документы
├── diagrams/               # Диаграммы (.drawio, Mermaid)
├── imp_plans/              # Планы реализации
└── resources/              # Описания ресурсов
    ├── database/
    ├── backend/
    ├── frontend/
    └── infra/
```

### Цепочка зависимостей документов

**Прямая:** Дискуссия → Архитектура → Ресурсы → План реализации → Документация папок

**При изменениях:**
- Изменение архитектуры → обновить связанные дискуссии
- Изменение ресурса → обновить архитектуру и документацию папок
- Изменение кода → обновить документацию папки, при существенных изменениях — ресурс

### Документация папок

Размещается в корне значимых папок как `[название_папки]_doc.md` (например: `src/auth/auth_doc.md`).

### Глоссарий

Все новые термины добавлять в [glossary.md](general_docs/glossary.md).
**Формат ссылок на глоссарий:** `[📖 Термин](путь/к/glossary.md#термин)`

Эмодзи `📖` визуально отличает ссылки на глоссарий от обычных ссылок.
**Правило для LLM:** При встрече незнакомого термина из проекта — проверить [glossary.md](general_docs/glossary.md). Если термин есть в глоссарии, ознакомиться с его определением перед продолжением работы.

---

## MCP серверы

<!-- TODO: Добавить MCP серверы при необходимости -->
