---
description: Триггер — предложить /hotfix при запросе на исправление бага или production-инцидент
standard: .claude/.instructions/rules/standard-rule.md
index: .claude/.instructions/rules/README.md
---

При запросе на хотфикс, исправление бага, production-инцидент,
группу мелких фиксов — предложить `/hotfix`.

Не использовать `/chain` для багов.
`/hotfix` создаёт специализированный TaskList для диагностики и исправления.

SSOT: [standard-hotfix.md](/specs/.instructions/hotfixes/standard-hotfix.md)
