---
description: Воркфлоу запуска разработки по analysis chain — prerequisite check, создание Issues/Milestone/Branch, переход WAITING → RUNNING.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/development/README.md
---

# Воркфлоу запуска разработки

Пошаговый процесс перехода analysis chain из WAITING в RUNNING.

**Полезные ссылки:**
- [Стандарт локальной разработки](./standard-development.md) — § 0 содержит полный воркфлоу
- [Стандарт analysis chain](/specs/.instructions/analysis/standard-analysis.md) — § 6.2

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-development.md](./standard-development.md) |
| Валидация | [validation-development.md](./validation-development.md) |
| Создание | Этот документ |
| Модификация | — |

## Воркфлоу

**SSOT:** [standard-development.md § 0](./standard-development.md#0-запуск-разработки)

→ Выполнить шаги из § 0 стандарта.

## Чек-лист

- [ ] Все 4 документа цепочки существуют и в WAITING
- [ ] Маркеров = 0
- [ ] Пользователь подтвердил запуск
- [ ] Issues созданы из TASK-N
- [ ] Milestone создан/привязан
- [ ] Ветка создана
- [ ] Цепочка переведена в RUNNING
- [ ] README обновлён
- [ ] Отчёт выведен

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/dev](/.claude/skills/dev/SKILL.md) | Запуск разработки по analysis chain | Этот документ |
