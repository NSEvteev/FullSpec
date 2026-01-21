---
name: spec-status
description: Изменение статуса документа /specs/ с каскадными проверками
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
category: specs
triggers:
  commands:
    - /spec-status
  phrases:
    ru:
      - статус спецификации
      - измени статус
      - переведи в review
      - одобри adr
    en:
      - spec status
      - change status
      - move to review
      - approve adr
---

# Изменение статуса документа /specs/

Изменение статуса документа спецификации с автоматическими каскадными проверками и переходами.

**Связанные скиллы:**
- [spec-create](/.claude/skills/spec-create/SKILL.md) — создание документов
- [spec-update](/.claude/skills/spec-update/SKILL.md) — работа с документом
- [specs-sync](/.claude/skills/specs-sync/SKILL.md) — синхронизация всех статусов
- [specs-health](/.claude/skills/specs-health/SKILL.md) — проверка целостности

**Связанные инструкции:**
- [specs/statuses.md](/.claude/instructions/specs/statuses.md) — система статусов
- [specs/workflow.md](/.claude/instructions/specs/workflow.md) — полный workflow
- [specs/discussions.md](/.claude/instructions/specs/discussions.md) — чек-листы Discussion
- [specs/impact.md](/.claude/instructions/specs/impact.md) — чек-листы Impact
- [specs/adr.md](/.claude/instructions/specs/adr.md) — чек-листы ADR
- [specs/plans.md](/.claude/instructions/specs/plans.md) — чек-листы Plan

## Оглавление

- [Формат вызова](#формат-вызова)
- [Статусы](#статусы)
- [Воркфлоу](#воркфлоу)
- [Каскадные переходы](#каскадные-переходы)
- [Чек-листы переходов](#чек-листы-переходов)
- [Обработка ошибок](#обработка-ошибок)
- [Примеры использования](#примеры-использования)

---

## Формат вызова

```
/spec-status <path> <status> [--force]
```

| Параметр | Описание | Пример |
|----------|----------|--------|
| `path` | Путь к документу (сокращённый) | `discussions/001`, `auth/adr/002` |
| `status` | Целевой статус | `review`, `approved`, `done`, `rejected` |
| `--force` | Пропустить проверку чек-листа | — |

**Сокращённые пути:**
- `discussions/001` → `/specs/discussions/001-*.md`
- `impact/001` → `/specs/impact/001-*.md`
- `auth/adr/001` → `/specs/services/auth/adr/001-*.md`
- `auth/plans/jwt` → `/specs/services/auth/plans/*jwt*.md`

---

## Статусы

| Статус | Команда | Описание |
|--------|---------|----------|
| DRAFT | — | Начальный статус |
| REVIEW | `review` | На рассмотрении |
| APPROVED | `approved` | Одобрен |
| RUNNING | `running` | В реализации |
| DONE | `done` | Завершён |
| REJECTED | `rejected` | Отклонён |
| SUPERSEDED | `superseded <new-id>` | Заменён |

---

## Воркфлоу

### Шаг 1: Найти документ

По сокращённому пути найти полный путь к документу:

```bash
# Пример для discussions/001
ls /specs/discussions/001-*.md
```

### Шаг 2: Прочитать текущий статус

Из метаданных документа или из README.md индекса.

### Шаг 3: Проверить допустимость перехода

Согласно [statuses.md](/.claude/instructions/specs/statuses.md):

```
DRAFT → REVIEW → APPROVED → RUNNING → DONE
                    ↓
                REJECTED
```

Недопустимые переходы:
- `DONE → *` (кроме SUPERSEDED)
- `REJECTED → *` (кроме переоткрытия)
- Пропуск статусов (DRAFT → APPROVED)

### Шаг 4: Проверить чек-лист

Для каждого перехода есть чек-лист в соответствующей инструкции:
- Discussion: [discussions.md](/.claude/instructions/specs/discussions.md)
- Impact: [impact.md](/.claude/instructions/specs/impact.md)
- ADR: [adr.md](/.claude/instructions/specs/adr.md)
- Plan: [plans.md](/.claude/instructions/specs/plans.md)

**Формат проверки:**
```
📋 Чек-лист перехода {type} {id}: {current} → {target}

- [x] Заполнена секция "Контекст"
- [x] Описаны варианты решения
- [ ] Указаны критерии оценки

❌ Чек-лист не пройден. Заполните недостающие пункты.
```

Если `--force` — пропустить и предупредить.

### Шаг 5: Обновить статус в документе

```markdown
| **Статус** | REVIEW |
```

### Шаг 6: Обновить README.md индекс

```markdown
| [001](001-auth.md) | Auth | 🔍 REVIEW | 2025-01-21 |
```

### Шаг 7: Выполнить каскадные действия

См. [Каскадные переходы](#каскадные-переходы).

### Шаг 8: Результат

```
✅ Статус изменён

Документ: /specs/discussions/001-auth-strategy.md
Переход: DRAFT → REVIEW

Каскадные действия: нет

Следующий шаг:
- Получить одобрение
- /spec-status discussions/001 approved
```

---

## Каскадные переходы

| Переход | Каскадное действие |
|---------|-------------------|
| Plan → APPROVED | Если ВСЕ планы Impact APPROVED → ADR → RUNNING, Impact → RUNNING |
| Plan → RUNNING | Если первый план → Discussion → RUNNING |
| Plan → DONE | Предложить `/spec-status {service}/adr/{id} done` |
| ADR → APPROVED | Если ВСЕ ADR Impact APPROVED → Impact → APPROVED |
| ADR → DONE | Если ВСЕ ADR Impact в финальном статусе → Impact → DONE → Discussion → DONE |

**Автоматическое выполнение:**

```
/spec-status auth/plans/jwt-migration done

✅ Статус изменён: Plan → DONE

📋 Каскадные действия:

1. Проверка: все планы ADR auth/002 завершены? ✅
   → Предлагаю: /spec-status auth/adr/002 done

Выполнить? [Y/n]
```

---

## Чек-листы переходов

### Discussion: DRAFT → REVIEW

- [ ] Заполнена секция "Контекст"
- [ ] Описаны минимум 2 варианта решения
- [ ] Указаны критерии оценки
- [ ] Заполнена таблица сравнения

### Discussion: REVIEW → APPROVED

- [ ] Выбран вариант решения
- [ ] Заполнена секция "Решение"
- [ ] Заполнена секция "Ревью решения"
- [ ] Отвечены вопросы

### ADR: REVIEW → APPROVED

- [ ] ВСЯ бизнес-логика описана в Impact (все ✅ в таблице)
- [ ] Секция "Влияние на архитектуру" заполнена

### Plan: REVIEW → APPROVED

- [ ] Пользователь просмотрел план
- [ ] Пользователь подтвердил согласие

### ADR: RUNNING → DONE

- [ ] Plan в статусе DONE
- [ ] Обновлён architecture.md
- [ ] Добавлена запись в "История изменений"

---

## Обработка ошибок

| Ошибка | Действие |
|--------|----------|
| Документ не найден | Показать существующие документы |
| Недопустимый переход | Показать допустимые переходы |
| Чек-лист не пройден | Показать невыполненные пункты |
| Конфликт статусов | Предложить `/specs-sync` |

---

## Примеры использования

### Пример 1: Перевод Discussion в REVIEW

```
/spec-status discussions/001 review

📋 Чек-лист перехода Discussion 001: DRAFT → REVIEW

- [x] Заполнена секция "Контекст"
- [x] Описаны минимум 2 варианта решения
- [x] Указаны критерии оценки
- [x] Заполнена таблица сравнения

✅ Статус изменён: DRAFT → REVIEW

Документ: /specs/discussions/001-auth-strategy.md
Индекс обновлён: /specs/discussions/README.md
```

### Пример 2: Каскадный переход при DONE плана

```
/spec-status auth/plans/jwt-migration done

📋 Чек-лист перехода Plan: RUNNING → DONE

- [x] ВСЕ GitHub Issues закрыты
- [x] Все задачи отмечены выполненными

✅ Статус изменён: RUNNING → DONE

📋 Каскадные действия:

Проверка ADR auth/002-jwt-tokens:
- Plan jwt-migration: ✅ DONE
- Других планов нет

→ ADR готов к завершению.

Выполнить /spec-status auth/adr/002 done? [Y/n]
```

### Пример 3: Отклонение ADR

```
/spec-status auth/adr/003 rejected

⚠️ Для REJECTED необходимо указать причину.

Причина отклонения:
> Выбран альтернативный подход с Redis

✅ Статус изменён: REVIEW → REJECTED

Документ обновлён: добавлена причина отклонения
Impact остаётся в REVIEW

Варианты:
1. /spec-create adr 001-auth-strategy auth — создать новый ADR
2. /spec-status impact/001 rejected — отклонить Impact
```
