---
description: Воркфлоу запуска разработки по analysis chain — prerequisite check, создание Issues/Milestone/Branch, переход WAITING → RUNNING.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/development/README.md
---

# Воркфлоу запуска разработки

Рабочая версия стандарта: 1.3

Пошаговый процесс перехода analysis chain из WAITING в RUNNING.

**Полезные ссылки:**
- [Инструкции development](./README.md)
- [Стандарт локальной разработки § 0](./standard-development.md#0-запуск-разработки) — полный воркфлоу
- [Стандарт analysis chain § 6.2](/specs/.instructions/analysis/standard-analysis.md#62-waiting-to-running)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-development.md](./standard-development.md) |
| Валидация | [validation-development.md](./validation-development.md) |
| Создание | Этот документ |
| Модификация | [modify-development.md](./modify-development.md) |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить готовность цепочки](#шаг-1-проверить-готовность-цепочки)
  - [Шаг 2: Подтверждение пользователя](#шаг-2-подтверждение-пользователя)
  - [Шаг 3: Создать GitHub Issues](#шаг-3-создать-github-issues)
  - [Шаг 4: Создать/привязать Milestone](#шаг-4-создатьпривязать-milestone)
  - [Шаг 5: Создать ветку](#шаг-5-создать-ветку)
  - [Шаг 6: Перевести цепочку в RUNNING](#шаг-6-перевести-цепочку-в-running)
  - [Шаг 7: Отчёт](#шаг-7-отчёт)
  - [Шаг 8: Предложить начать разработку](#шаг-8-предложить-начать-разработку)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **SSOT — standard-development.md § 0.** Эта инструкция описывает шаги запуска. Детали каждого шага — в [§ 0 стандарта](./standard-development.md#0-запуск-разработки).

> **Все 4 документа — одновременно.** Переход в RUNNING выполняется tree-level: все документы цепочки меняют статус одновременно.

> **Пользователь подтверждает запуск.** Автоматический переход WAITING → RUNNING запрещён.

---

## Шаги

> Эта секция применяется при работе с analysis chain (specs/analysis/).
> Если Issues созданы вручную — перейти к [§ 1 Взятие задачи](./standard-development.md#1-взятие-задачи).

### Шаг 1: Проверить готовность цепочки

```bash
python .github/.instructions/.scripts/check-chain-readiness.py {NNNN}
```

Скрипт проверяет все 4 документа: status=WAITING и 0 маркеров. Если скрипт недоступен — проверить вручную:

Прочитать frontmatter всех 4 документов цепочки NNNN-{topic}:

| Документ | Требование |
|----------|------------|
| Discussion | `status: WAITING` |
| Design | `status: WAITING` |
| Plan Tests | `status: WAITING` |
| Plan Dev | `status: WAITING` |

Дополнительно: маркеров `[ТРЕБУЕТ УТОЧНЕНИЯ]` = 0 во всех документах.

Если не все в WAITING → **СТОП:** "Цепочка не готова. {документ} в статусе {status}."

### Шаг 2: Подтверждение пользователя

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: "Цепочка NNNN-{topic} готова к разработке. {N} TASK-N, Milestone {vX.Y.Z}. Начать?"

| Ответ | Действие |
|-------|----------|
| Да | Продолжить |
| Нет | **СТОП** |

### Шаг 3: Создать GitHub Issues

Для каждого TASK-N из Plan Dev → `/issue-create`:
- Sub-issues для подзадач (N.M)
- Обновить таблицу маппинга TASK-N → Issue в plan-dev.md

### Шаг 4: Создать/привязать Milestone

1. Проверить: Milestone {vX.Y.Z} существует?
2. Если нет → `/milestone-create`
3. Привязать все Issues к Milestone

### Шаг 5: Создать ветку

```
/branch-create {NNNN}
```

### Шаг 6: Перевести цепочку в RUNNING

1. Обновить `status: WAITING` → `status: RUNNING` во всех 4 документах
2. Обновить `specs/analysis/README.md`

### Шаг 7: Отчёт

Вывести: Issues (#N), Milestone, Branch, статус цепочки → RUNNING.

### Шаг 8: Предложить начать разработку

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: "Цепочка NNNN-{topic} в RUNNING. Начать разработку (`/dev`)?"

| Ответ | Действие |
|-------|----------|
| Да | Запустить `/dev` (→ [modify-development.md](./modify-development.md)) |
| Нет | Завершить воркфлоу |

---

## Чек-лист

- [ ] Все 4 документа цепочки существуют и в WAITING
- [ ] Маркеров `[ТРЕБУЕТ УТОЧНЕНИЯ]` = 0
- [ ] Пользователь подтвердил запуск
- [ ] Issues созданы из TASK-N
- [ ] Таблица маппинга в plan-dev.md обновлена
- [ ] Milestone создан/привязан
- [ ] Ветка создана
- [ ] Цепочка переведена в RUNNING
- [ ] README обновлён
- [ ] Отчёт выведен
- [ ] Пользователю предложено запустить `/dev`

---

## Примеры

### Запуск разработки цепочки 0001

```
/dev-create 0001
```

### Возобновление после CONFLICT → WAITING

```
/dev-create 0001 --resume
```

Issues уже существуют — `/dev-create --resume` обнаружит и пропустит создание.

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [check-chain-readiness.py](../.scripts/check-chain-readiness.py) | Проверка готовности цепочки (4/4 WAITING, 0 маркеров) | Этот документ |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/dev-create](/.claude/skills/dev-create/SKILL.md) | Запуск разработки по analysis chain | Этот документ |
