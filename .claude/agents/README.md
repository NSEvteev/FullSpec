---
description: Конфигурации агентов
standard: .structure/.instructions/standard-readme.md
index: .claude/agents/README.md
---

# /.claude/agents/ — Конфигурации агентов

Настройки и конфигурации для Claude агентов.

**Полезные ссылки:**
- [.claude/](../README.md)
- [Структура проекта](/.structure/README.md)

## Оглавление

- [1. Агенты](#1-агенты)
- [2. Формат](#2-формат)

---

## 1. Агенты

| Агент | Описание | Тип | Модель |
|-------|----------|-----|--------|
| [amy-santiago](./amy-santiago/AGENT.md) | Помощник по созданию инструкций (Эми Сантьяго) | general-purpose | sonnet |

---

## 2. Формат

Каждый агент — это папка с файлом `AGENT.md`:

```
/.claude/agents/{agent-name}/
└── AGENT.md          # Конфигурация агента
```

**SSOT:** [standard-agent.md](/.claude/.instructions/agents/standard-agent.md)
