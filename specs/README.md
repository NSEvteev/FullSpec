# /specs/ — Спецификации проекта

## Зона ответственности

Спецификации, архитектурные решения, планы развития проекта.

**IN:** discussions/, impact/, services/, glossary.md

**Границы:**
- архитектура, планы, решения → здесь
- документация кода → */docs/
- README файлы → в соответствующих папках
- инструкции для LLM → /.claude/.instructions/

> **Все зоны:** [/.structure/responsibilities.md](/.structure/responsibilities.md)

---

## Структура

```
specs/
├── discussions/          # Обсуждения фич (DISC-*.md)
├── impact/               # Импакт-анализ (IMPACT-*.md)
├── services/             # Спецификации по сервисам
│   └── {service}/
│       ├── adr/          # Архитектурные решения (ADR-*.md)
│       └── plans/        # Планы реализации (PLAN-*.md)
└── glossary.md           # Глоссарий терминов
```

---

## Workflow

```
Discussion → Impact → ADR → Plan → Implementation
```

---

## Связи

- **Инструкции:** [/.claude/.instructions/specs/](/.claude/.instructions/specs/)
