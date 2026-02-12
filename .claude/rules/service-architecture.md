---
description: Правила работы с сервисной архитектурой — создание и изменение services/{svc}.md по событиям SDD-lifecycle.
standard: .claude/.instructions/rules/standard-rule.md
standard-version: v1.1
index: .claude/.instructions/rules/README.md
paths:
  - "specs/architecture/services/**"
  - "specs/.instructions/living-docs/service/**"
---
При работе с сервисной документацией ОБЯЗАТЕЛЬНО использовать скиллы:
  - `/service-create` - создание сервисного документа (stub при Design → WAITING)
  - `/service-modify` - изменение по SDD-lifecycle (ADR → DONE, Design → DONE и т.д.)

SSOT стандарт: [standard-service.md](/specs/.instructions/living-docs/service/standard-service.md)

Сервисный документ `services/{svc}.md` создаётся в два этапа:
  1. **Stub** при Design → WAITING (только Резюме + Planned Changes)
  2. **Full** при ADR → DONE (заполнение секций 1-6 из дельты)

Детекция режима: отсутствие `created-by` в frontmatter = stub.
