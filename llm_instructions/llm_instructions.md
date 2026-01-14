# Инструкции для LLM

## Назначение

Папка `llm_instructions/` содержит все инструкции для работы LLM с проектом.

**Связанные ресурсы:**
- [CLAUDE.md](../CLAUDE.md) — краткие инструкции для Claude Code
- [llm_tasks/](../llm_tasks/) — управление задачами сессии
- [general_docs/](../general_docs/) — общая документация проекта

---

## Инструкции

| Файл | Назначение |
|------|------------|
| [instructions_general_docs.md](instructions_general_docs.md) | Правила ведения документации: структура `general_docs/`, workflow статусов, правила feedback |
| [instructions_scripts.md](instructions_scripts.md) | Служебные скрипты для поддержания порядка в проекте |
| [instructions_agents.md](instructions_agents.md) | Конфигурация AI-агентов Claude Code (`.claude/agents/`) |
| [instructions_skills.md](instructions_skills.md) | Конфигурация скиллов Claude Code (`.claude/skills/`) |

---

## Шаблоны документов

Папка `templates/` содержит шаблоны для создания документов в `general_docs/`:

| Шаблон | Назначение | Расположение документов |
|--------|------------|-------------------------|
| [template_discuss.md](templates/template_discuss.md) | Дискуссии (идея → решение) | `general_docs/discuss/` |
| [template_architecture.md](templates/template_architecture.md) | Архитектурные документы | `general_docs/architecture/` |
| [template_imp_plan.md](templates/template_imp_plan.md) | Планы реализации | `general_docs/imp_plans/` |
| [template_resource.md](templates/template_resource.md) | Описания ресурсов | `general_docs/resources/` |
| [template_folder_doc.md](templates/template_folder_doc.md) | Документация папок кода | `src/*/[название]_doc.md` |

**Примечание:** Шаблоны — рекомендуемая структура. Адаптируйте под конкретную задачу.

---

## Структура проекта

```
trading_platform/
├── .claude/                           # Конфигурация Claude Code
│   ├── settings.local.json            # Локальные настройки
│   └── skills/                        # Скиллы
│       ├── commit-push/               # Скилл коммита и пуша
│       │   └── SKILL.md
│       └── doc-structure-project/     # Скилл структуры проекта
│           └── SKILL.md
├── general_docs/                      # Общая документация
│   ├── architecture/                  # Архитектурные документы
│   ├── diagrams/                      # Диаграммы
│   ├── discuss/                       # Дискуссии
│   ├── imp_plans/                     # Планы реализации
│   ├── resources/                     # Описания ресурсов
│   │   ├── backend/
│   │   ├── database/
│   │   ├── frontend/
│   │   └── infra/
│   └── glossary.md                    # Глоссарий терминов
├── llm_instructions/                  # Инструкции для LLM
│   ├── templates/                     # Шаблоны документов
│   │   ├── template_architecture.md
│   │   ├── template_discuss.md
│   │   ├── template_folder_doc.md
│   │   ├── template_imp_plan.md
│   │   └── template_resource.md
│   ├── instructions_agents.md         # Инструкции по агентам
│   ├── instructions_general_docs.md   # Правила документации
│   ├── instructions_scripts.md        # Служебные скрипты
│   ├── instructions_skills.md         # Инструкции по скиллам
│   └── llm_instructions.md            # Индекс инструкций (этот файл)
├── llm_tasks/                         # Управление задачами
│   ├── current_tasks.md               # Текущие задачи сессии
│   └── future_tasks.md                # Бэклог задач
├── scripts/                           # Служебные скрипты
│   └── check_doc_links.py             # Проверка ссылок в документации
├── .gitignore
├── CLAUDE.md                          # Быстрый справочник Claude
└── README.md                          # Описание проекта
```

---

## Быстрый старт LLM

См. раздел «Быстрый старт LLM» в [CLAUDE.md](../CLAUDE.md#быстрый-старт-llm)
