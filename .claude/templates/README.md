# Шаблоны (SSOT)

Single Source of Truth шаблоны, используемые скиллами и инструкциями.

## Назначение

Шаблоны — это SSOT документы, на которые ссылаются скиллы. Изменение шаблона автоматически влияет на все скиллы, которые его используют.

## Шаблоны

| Шаблон | Описание | Используется в |
|--------|----------|----------------|
| [output-formats.md](./output-formats.md) | Форматы вывода (✅❌⚠️📋) | Все 37 скиллов |
| [error-handling.md](./error-handling.md) | Обработка ошибок, откат, retry | Все 37 скиллов |
| [scope-detection.md](./scope-detection.md) | Определение scope (claude/project) | test-*, doc-* |
| [test-formats.md](./test-formats.md) | Форматы тестов (smoke, functional) | test-* |
| [workflow-template.md](./workflow-template.md) | Шаблон структуры воркфлоу | skill-create, instruction-create |
| [doc-rules.md](./doc-rules.md) | Правила документирования | doc-* |

## Структура шаблона

```markdown
# Название шаблона

{Описание назначения}

## Использование

{Как ссылаться на шаблон из скилла}

## Правила

{Правила, которые описывает шаблон}

## Примеры

{Примеры использования}
```

## Ссылка из скилла

```markdown
> **SSOT:** [output-formats.md](/.claude/templates/output-formats.md)
```

---

## Связанные инструкции

- [/.claude/README.md](/.claude/README.md) — хаб навигации
- [/.claude/skills/README.md](/.claude/skills/README.md) — индекс скиллов
- [/.claude/instructions/doc/structure.md](/.claude/instructions/doc/structure.md) — структура документации /doc/
