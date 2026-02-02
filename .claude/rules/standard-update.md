---
description: Миграция при изменении стандартов
standard: .claude/.instructions/rules/standard-rule.md
standard-version: v1.1
index: .claude/.instructions/rules/README.md
paths:
  - "**/standard-*.md"
---

После изменения стандарта ОБЯЗАТЕЛЬНО выполнить миграцию (запрещено выполнять вручную):
  1. Выполнить миграцию: `/migration-create {путь}`
  2. Проверить: `/migration-validate {путь}`

**SSOT:** [standard-migration.md](/.instructions/migration/standard-migration.md)
