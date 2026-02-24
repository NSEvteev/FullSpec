---
description: Напоминание использовать chain_status.py для переходов статусов analysis chain. Активируется при работе с specs/analysis/.
standard: .claude/.instructions/rules/standard-rule.md
standard-version: v1.1
index: .claude/.instructions/rules/README.md
paths:
  - "specs/analysis/**"
---

При изменении статуса документа analysis chain (discussion, design, plan-test, plan-dev) ОБЯЗАТЕЛЬНО использовать модуль `chain_status.py` — SSOT для переходов статусов:

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="TARGET_STATUS", document="doc_name")
```

**Запрещено:** Менять `status:` в frontmatter вручную или обновлять README dashboard без `chain_status.py`.

**SSOT:** [chain_status.py](/specs/.instructions/.scripts/chain_status.py) — управление статусами, prerequisites, каскады, README dashboard.

**Связанные скиллы:**
  - `/analysis-status` — просмотр статусов chain
  - `/discussion-create`, `/design-create`, `/plan-test-create`, `/plan-dev-create` — создание документов
  - `/discussion-modify`, `/design-modify`, `/plan-test-modify`, `/plan-dev-modify` — изменение документов
