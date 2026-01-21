---
name: specs-health
description: Проверка целостности /specs/ — статусы, ссылки, застрявшие документы
allowed-tools: Read, Glob, Grep, Bash
category: specs
triggers:
  commands:
    - /specs-health
  phrases:
    ru:
      - проверь спецификации
      - здоровье specs
      - найди проблемы в specs
    en:
      - check specs
      - specs health
      - find specs issues
---

# Проверка целостности /specs/

Диагностика проблем в документах спецификаций: статусы, ссылки, застрявшие документы.

**Связанные скиллы:**
- [spec-status](/.claude/skills/spec-status/SKILL.md) — исправление статусов
- [specs-sync](/.claude/skills/specs-sync/SKILL.md) — синхронизация статусов
- [specs-index](/.claude/skills/specs-index/SKILL.md) — обновление индексов

**Связанные инструкции:**
- [specs/statuses.md](/.claude/instructions/specs/statuses.md) — система статусов
- [specs/rules.md](/.claude/instructions/specs/rules.md) — правила работы

## Оглавление

- [Формат вызова](#формат-вызова)
- [Проверки](#проверки)
- [Воркфлоу](#воркфлоу)
- [Формат отчёта](#формат-отчёта)
- [Примеры использования](#примеры-использования)

---

## Формат вызова

```
/specs-health [--fix] [--verbose]
```

| Параметр | Описание |
|----------|----------|
| `--fix` | Предложить исправления для найденных проблем |
| `--verbose` | Подробный вывод всех проверок |

---

## Проверки

| Проблема | Описание | Рекомендация |
|----------|----------|--------------|
| **Orphan Discussion** | Discussion в APPROVED без Impact >7 дней | Создать Impact или REJECTED |
| **Orphan Impact** | Impact в REVIEW без ADR >7 дней | Создать ADR или REJECTED |
| **Stuck ADR** | ADR в APPROVED без Plan >14 дней | Создать Plan |
| **Stuck Plan** | Plan в RUNNING с закрытыми Issues | Перевести в DONE |
| **Inconsistent status** | Дочерние завершены, родитель нет | Обновить родителя |
| **Broken links** | Ссылки на несуществующие документы | Исправить ссылки |
| **Missing backlinks** | Родитель не ссылается на дочерний | Добавить backlink |
| **Service without specs** | Сервис в /src/ без /specs/services/ | Создать ADR |

---

## Воркфлоу

### Шаг 1: Собрать все документы

```bash
find /specs -name "*.md" -not -name "README.md"
```

### Шаг 2: Проверить каждый документ

Для каждого документа:
1. Прочитать статус
2. Проверить ссылки
3. Проверить даты
4. Проверить связи с дочерними/родительскими

### Шаг 3: Проверить консистентность статусов

Для каждой цепочки Discussion → Impact → ADR → Plan:
- Все дочерние в финальном статусе → родитель тоже должен быть
- Родитель в RUNNING → хотя бы один дочерний в RUNNING

### Шаг 4: Проверить сервисы

Сравнить `/src/` с `/specs/services/`:
- Каждый сервис должен иметь папку в specs

### Шаг 5: Сформировать отчёт

---

## Формат отчёта

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

---

## Примеры использования

### Пример 1: Базовая проверка

```
/specs-health

📋 Проверка целостности /specs/

Проверено документов: 12
Проверено сервисов: 3

✅ Проблем не обнаружено
```

### Пример 2: С исправлениями

```
/specs-health --fix

📋 Проверка целостности /specs/
...

🔴 Критичные проблемы (1):

1. Inconsistent status
   Impact 001: RUNNING, но все ADR DONE

Исправить? [Y/n] Y

Выполняю: /spec-status impact/001 done

✅ Исправлено: Impact 001 → DONE
```
