---
name: specs-sync
description: Синхронизация каскадных статусов документов /specs/
allowed-tools: Read, Write, Edit, Glob, Grep
category: specs
triggers:
  commands:
    - /specs-sync
  phrases:
    ru:
      - синхронизируй статусы
      - пересчитай статусы
      - обнови статусы specs
    en:
      - sync statuses
      - recalculate statuses
      - update specs statuses
---

# Синхронизация статусов /specs/

Пересчёт каскадных статусов для всех документов. Приводит статусы родительских документов в соответствие с дочерними.

**Связанные скиллы:**
- [spec-status](/.claude/skills/spec-status/SKILL.md) — изменение отдельного статуса
- [specs-health](/.claude/skills/specs-health/SKILL.md) — диагностика проблем

**Связанные инструкции:**
- [specs/statuses.md](/.claude/instructions/specs/statuses.md) — правила статусов
- [specs/workflow.md](/.claude/instructions/specs/workflow.md) — каскадные переходы

## Оглавление

- [Формат вызова](#формат-вызова)
- [Правила синхронизации](#правила-синхронизации)
- [Воркфлоу](#воркфлоу)
- [Примеры использования](#примеры-использования)

---

## Формат вызова

```
/specs-sync [--dry-run]
```

| Параметр | Описание |
|----------|----------|
| `--dry-run` | Показать план без применения |

---

## Правила синхронизации

### Снизу вверх

```
Plan изменился
    ↓
Проверить ADR (все планы в финальном?)
    ↓
Проверить Impact (все ADR в финальном?)
    ↓
Проверить Discussion (Impact в финальном?)
```

### Правила переходов

| Условие | Действие |
|---------|----------|
| ВСЕ ADR Impact в APPROVED | Impact → APPROVED |
| ВСЕ планы Impact в APPROVED | ADR → RUNNING, Impact → RUNNING |
| Первый Plan → RUNNING | Discussion → RUNNING |
| ВСЕ ADR в финальном + минимум 1 DONE | Impact → DONE |
| Impact → DONE | Discussion → DONE |

### Финальные статусы

Документ в **финальном статусе** если:
- DONE
- REJECTED
- SUPERSEDED

---

## Воркфлоу

### Шаг 1: Собрать все цепочки

Построить граф: Discussion → Impact → ADR → Plan

### Шаг 2: Для каждой цепочки (снизу вверх)

1. Собрать статусы всех Plans
2. Определить ожидаемый статус ADR
3. Собрать статусы всех ADR
4. Определить ожидаемый статус Impact
5. Определить ожидаемый статус Discussion

### Шаг 3: Найти расхождения

Сравнить текущие статусы с ожидаемыми.

### Шаг 4: Применить изменения

Для каждого расхождения — вызвать `/spec-status`.

---

## Примеры использования

### Пример 1: Синхронизация

```
/specs-sync

📋 Синхронизация статусов /specs/

Проверено цепочек: 3
Найдено расхождений: 2

Изменения:

1. Impact 001-auth-strategy
   Текущий: ⏳ RUNNING
   Ожидаемый: ✅ DONE
   Причина: Все ADR в финальном статусе (auth/001 DONE, gateway/001 DONE)

2. Discussion 001-auth-strategy
   Текущий: ⏳ RUNNING
   Ожидаемый: ✅ DONE
   Причина: Impact 001 → DONE

Применить? [Y/n] Y

✅ Синхронизация завершена
- Impact 001: RUNNING → DONE
- Discussion 001: RUNNING → DONE
```

### Пример 2: Dry-run

```
/specs-sync --dry-run

📋 Синхронизация статусов (dry-run)

Будет изменено:
- Impact 001: RUNNING → DONE
- Discussion 001: RUNNING → DONE

ℹ️ Изменения НЕ применены (--dry-run)
```
