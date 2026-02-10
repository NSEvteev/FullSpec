---
description: Правила миграции standard-файлов — обязательное использование скиллов. Активируется при изменении standard-*.md.
standard: .claude/.instructions/rules/standard-rule.md
standard-version: v1.1
index: .claude/.instructions/rules/README.md
paths:
  - "**/standard-*.md"
---

При работе с миграцией standard-*.md` файлов ОБЯЗАТЕЛЬНО использовать скиллы (запрещено делать вручную):
  1. Выполнить миграцию: `/migration-create {путь}`
  2. Проверить: `/migration-validate {путь}`

После изменения ЛЮБОГО /standard-*.md ОБЯЗАТЕЛЬНО выполнить миграцию