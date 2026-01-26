---
description: Примеры использования скиллов /specs/
standard: .instructions/standard-instruction.md
index: specs/.instructions/README.md
---

# Примеры использования скиллов /specs/

Примеры вызова и результаты для всех скиллов работы со спецификациями.

**Полезные ссылки:**
- [Инструкции для /specs/](./README.md)

## Оглавление

- [spec-create](#spec-create)
- [spec-status](#spec-status)
- [spec-update](#spec-update)
- [specs-health](#specs-health)
- [specs-index](#specs-index)
- [specs-sync](#specs-sync)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## spec-create

### Пример 1: Создание Discussion

**Команда:**
```
/spec-create discussion "Auth Strategy"
```

**Результат:**
```
✅ Discussion создана

Файл: /specs/discussions/001-auth-strategy.md
Статус: DRAFT

Индекс обновлён: /specs/discussions/README.md

Следующий шаг:
- Заполнить секции документа
- Перевести в REVIEW: /spec-status discussions/001 review
```

### Пример 2: Создание Impact

**Команда:**
```
/spec-create impact 001-auth-strategy
```

**Результат:**
```
✅ Impact создан

Файл: /specs/impact/001-auth-strategy.md
Тип: impact
Статус: DRAFT
Родитель: /specs/discussions/001-auth-strategy.md

Индекс обновлён: /specs/impact/README.md
Backlink добавлен: /specs/discussions/001-auth-strategy.md

Следующий шаг:
- Заполнить анализ влияния
- Перевести в REVIEW: /spec-status impact/001 review
```

### Пример 3: Создание ADR для существующего сервиса

**Команда:**
```
/spec-create adr 001-auth-strategy auth
```

**Результат:**
```
✅ ADR создан

Файл: /specs/services/auth/adr/001-jwt-tokens.md
Тип: ADR
Статус: DRAFT
Родитель: /specs/impact/001-auth-strategy.md

Индекс обновлён: /specs/services/auth/adr/README.md
Backlink добавлен: /specs/impact/001-auth-strategy.md

Следующий шаг:
- Заполнить ADR
- Перевести в REVIEW: /spec-status auth/adr/001 review
```

### Пример 4: Создание ADR с новым сервисом

**Команда:**
```
/spec-create adr 001-auth-strategy payments --new
```

**Диалог:**
```
⚠️ Сервис "payments" не существует.

Создать структуру нового сервиса?
- /src/payments/
- /tests/payments/
- /specs/services/payments/
- /doc/src/payments/

[Y/n] Y

✅ Структура сервиса "payments" создана

✅ ADR создан

Файл: /specs/services/payments/adr/001-payment-processing.md
...
```

### Пример 5: Dry-run режим

**Команда:**
```
/spec-create impact 001-auth-strategy --dry-run
```

**Результат:**
```
📋 Предварительный просмотр (--dry-run)

Будет создано:
- /specs/impact/001-auth-strategy.md

Будет обновлено:
- /specs/impact/README.md (добавлена строка)
- /specs/discussions/001-auth-strategy.md (backlink)

ℹ️ Изменения НЕ применены (--dry-run)
```

---

## spec-status

### Пример 1: Перевод Discussion в REVIEW

**Команда:**
```
/spec-status discussions/001 review
```

**Результат:**
```
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

**Команда:**
```
/spec-status auth/plans/jwt-migration done
```

**Результат:**
```
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

**Команда:**
```
/spec-status auth/adr/003 rejected
```

**Результат:**
```
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

---

## spec-update

### Пример 1: Работа с Discussion

**Команда:**
```
/spec-update discussions/001
```

**Результат:**
```
📄 Discussion 001-auth-strategy

Статус: 🔍 REVIEW
Дата создания: 2025-01-20
Последнее изменение: 2025-01-21

Связанные документы:
- Impact: /specs/impact/001-auth-strategy.md (DRAFT)

Чек-лист текущего статуса:
- [x] Заполнена секция "Контекст"
- [x] Описаны варианты решения
- [ ] Выбран вариант решения

Что делаем?
```

**Продолжение диалога:**
```
User: добавь третий вариант — использование OAuth2

Claude: Добавляю вариант 3 в секцию "Варианты решения"...

✅ Добавлен вариант:
### Вариант 3: OAuth2
...

Обновить таблицу сравнения? [Y/n]
```

### Пример 2: Валидация ADR

**Команда:**
```
/spec-update auth/adr/002 --validate
```

**Результат:**
```
📋 Валидация ADR auth/002-jwt-tokens

Структура: ✅ OK
Ссылка на Impact: ✅ /specs/impact/001-auth-strategy.md
Breaking Changes: ⚠️ YES — секция заполнена

Чек-лист бизнес-логики:
| Правило | В Impact? |
|---------|-----------|
| JWT срок жизни 1 час | ✅ да |
| Refresh token 7 дней | ✅ да |
| Ротация при refresh | ❌ НЕТ |

⚠️ Найдена бизнес-логика не описанная в Impact!

Действия:
1. Обновить Impact (добавить правило ротации)
2. Удалить правило из ADR
3. Игнорировать (--force)
```

---

## specs-health

### Пример 1: Базовая проверка (без проблем)

**Команда:**
```
/specs-health
```

**Результат:**
```
📋 Проверка целостности /specs/

Проверено документов: 12
Проверено сервисов: 3

✅ Проблем не обнаружено
```

### Пример 2: Проверка с проблемами

**Команда:**
```
/specs-health
```

**Результат:**
```
📋 Проверка целостности /specs/

Проверено документов: 24
Проверено сервисов: 5

🔴 Критичные проблемы (3):

1. Inconsistent status
   Impact 001-auth-strategy: RUNNING
   Но все ADR в финальном статусе:
   - auth/001: ✅ DONE
   - gateway/001: ✅ DONE
   → Рекомендация: /spec-status impact/001 done

2. Stuck Plan
   Plan auth/jwt-migration: ⏳ RUNNING (14 дней)
   Все GitHub Issues закрыты
   → Рекомендация: /spec-status auth/plans/jwt-migration done

3. Service without specs
   /src/payments/ существует
   /specs/services/payments/ не найден
   → Рекомендация: /spec-create adr для payments

🟡 Предупреждения (2):

1. Orphan Discussion
   Discussion 003-caching: 🆗 APPROVED (10 дней без Impact)
   → Рекомендация: /spec-create impact 003-caching

2. Missing backlink
   ADR auth/002 ссылается на Impact 001
   Impact 001 не содержит ссылку на ADR auth/002
   → Рекомендация: добавить backlink

✅ Без проблем: 19 документов

Исправить проблемы? [все / критичные / выборочно / пропустить]
```

### Пример 3: С автоисправлением

**Команда:**
```
/specs-health --fix
```

**Результат:**
```
📋 Проверка целостности /specs/
...

🔴 Критичные проблемы (1):

1. Inconsistent status
   Impact 001: RUNNING, но все ADR DONE

Исправить? [Y/n] Y

Выполняю: /spec-status impact/001 done

✅ Исправлено: Impact 001 → DONE
```

---

## specs-index

### Пример 1: Обновить все индексы

**Команда:**
```
/specs-index
```

**Результат:**
```
📋 Обновление индексов /specs/

Сканирование...

Найдено README: 5
Найдено документов: 12

Обновляю...

✅ Индексы обновлены

- discussions/README.md: 3 документа
- impact/README.md: 2 документа
- services/auth/adr/README.md: 4 документа
- services/auth/plans/README.md: 2 документа
- services/gateway/adr/README.md: 1 документ
```

### Пример 2: Обновить конкретный индекс

**Команда:**
```
/specs-index /specs/services/auth/adr/
```

**Результат:**
```
✅ Индекс обновлён: /specs/services/auth/adr/README.md

Документов: 4
- 001-initial.md (DONE)
- 002-jwt-tokens.md (RUNNING)
- 003-session-storage.md (APPROVED)
- 004-rate-limiting.md (DRAFT)
```

---

## specs-sync

### Пример 1: Синхронизация с изменениями

**Команда:**
```
/specs-sync
```

**Результат:**
```
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

**Команда:**
```
/specs-sync --dry-run
```

**Результат:**
```
📋 Синхронизация статусов (dry-run)

Будет изменено:
- Impact 001: RUNNING → DONE
- Discussion 001: RUNNING → DONE

ℹ️ Изменения НЕ применены (--dry-run)
```

---

## Скиллы

| Скилл | Секция с примерами |
|-------|-------------------|
| [/spec-create](/.claude/skills/spec-create/SKILL.md) | [#spec-create](#spec-create) |
| [/spec-status](/.claude/skills/spec-status/SKILL.md) | [#spec-status](#spec-status) |
| [/spec-update](/.claude/skills/spec-update/SKILL.md) | [#spec-update](#spec-update) |
| [/specs-health](/.claude/skills/specs-health/SKILL.md) | [#specs-health](#specs-health) |
| [/specs-index](/.claude/skills/specs-index/SKILL.md) | [#specs-index](#specs-index) |
| [/specs-sync](/.claude/skills/specs-sync/SKILL.md) | [#specs-sync](#specs-sync) |

---

## Связанные инструкции

- [rules.md](./rules.md) — общие правила работы с /specs/
- [output.md](./output.md) — форматы вывода результатов
