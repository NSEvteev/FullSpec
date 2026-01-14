# Trading Platform

Платформа для разработки, [📖 бэктестинга](general_docs/glossary.md#бэктестинг) и исполнения [📖 торговых стратегий](general_docs/glossary.md#торговая-стратегия).

## Документация

| Документ | Назначение |
|----------|------------|
| [CLAUDE.md](CLAUDE.md) | Инструкции для Claude Code |
| [llm_instructions/](llm_instructions/llm_instructions.md) | Полные инструкции для LLM |
| [general_docs/](general_docs/) | Общая документация проекта |

---

## Структура проекта

```
trading_platform/
│
├── CLAUDE.md                      # Инструкции для Claude Code
├── README.md                      # Описание проекта (этот файл)
│
├── llm_instructions/              # Инструкции для LLM
│   ├── llm_instructions.md        # Индекс инструкций
│   ├── instructions_general_docs.md  # Правила документации
│   ├── instructions_scripts.md    # Служебные скрипты
│   ├── instructions_agents.md     # AI-агенты Claude
│   ├── instructions_skills.md     # [📖 Скиллы](general_docs/glossary.md#скилл) Claude
│   └── templates/                 # Шаблоны документов
│
├── llm_tasks/                     # Управление задачами LLM
│   ├── current_tasks.md           # Текущие задачи сессии
│   └── future_tasks.md            # [📖 Бэклог](general_docs/glossary.md#бэклог) задач
│
├── general_docs/                  # [📖 Общая документация](general_docs/glossary.md#общая-документация)
│   ├── glossary.md                # Глоссарий терминов
│   ├── discuss/                   # [📖 Дискуссии](general_docs/glossary.md#дискуссия) (идея → решение)
│   ├── architecture/              # Архитектурные документы
│   ├── diagrams/                  # Диаграммы (.drawio, Mermaid)
│   ├── imp_plans/                 # [📖 Планы реализации](general_docs/glossary.md#план-реализации)
│   └── resources/                 # Описания ресурсов
│       ├── database/
│       ├── backend/
│       ├── frontend/
│       └── infra/
│
├── scripts/                       # Служебные скрипты
│   └── check_doc_links.py         # Проверка ссылок в документации
│
└── .claude/                       # Конфигурация Claude Code
    ├── agents/                    # AI-агенты
    └── skills/                    # Скиллы
```

---

## Стек

<!-- TODO: Заполнить после выбора стека -->

## Установка

<!-- TODO: Заполнить после настройки проекта -->

## Запуск

<!-- TODO: Заполнить после настройки проекта -->

## Тесты

<!-- TODO: Заполнить после настройки проекта -->

---

## Статус разработки

<!-- TODO: Заполнить -->

## Лицензия

Проприетарный проект.
