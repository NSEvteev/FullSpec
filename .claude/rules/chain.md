---
description: Глобальный триггер — предложить /chain при запросе на изменение системы
standard: .claude/.instructions/rules/standard-rule.md
standard-version: v1.1
index: .claude/.instructions/rules/README.md
---

При запросе на добавление функциональности, фичи, изменение поведения системы —
предложить `/chain`.

При запросе на исправление бага, хотфикс, production-инцидент —
предложить `/hotfix`.

Не начинать напрямую с `/discussion-create`, `/design-create` и т.д.
`/chain` создаёт TaskList с полным планом и гарантирует правильный порядок.

Исключение: если пользователь явно просит конкретный скилл (например,
"/discussion-create для OAuth2") — выполнить запрос напрямую.
