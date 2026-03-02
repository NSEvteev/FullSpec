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
  - [Шаг 5: Перевести цепочку в RUNNING](#шаг-5-перевести-цепочку-в-running)
  - [Шаг 6: Коммит и Push в main](#шаг-6-коммит-и-push-в-main)
  - [Шаг 7: Создать ветку](#шаг-7-создать-ветку)
  - [Шаг 8: Отчёт](#шаг-8-отчёт)
  - [Шаг 9: Предложить начать разработку](#шаг-9-предложить-начать-разработку)
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
- Записать номер Issue inline в поле `Issue` каждой TASK-N (формат: `[#N](url)`)

**Определение TYPE-метки для Issue:**

Если TASK-N содержит поле `Type` → использовать как TYPE-метку.

Если поле `Type` отсутствует (старые plan-dev) → определить автоматически:

| Условие | TYPE-метка |
|---------|------------|
| `TC: INFRA` | `infra` |
| Системные тесты (STS-N, E2E, load, integration) | `test` |
| Бизнес-логика (CRUD, UI, API-эндпоинты) | `feature` |
| Scaffold, middleware, схемы, boilerplate | `task` |

### Шаг 4: Создать/привязать Milestone

1. Проверить: Milestone {vX.Y.Z} существует?
2. Если нет → `/milestone-create`
3. Привязать все Issues к Milestone

### Шаг 5: Перевести цепочку в RUNNING

**Переход WAITING → RUNNING** — через модуль `chain_status.py` (SSOT статусов):

```python
from chain_status import ChainManager
mgr = ChainManager("NNNN")
result = mgr.transition(to="RUNNING")
# Модуль автоматически: tree-level, все 4 документа → RUNNING, README dashboard
```

### Шаг 6: Коммит и Push в main

Шаги 3-5 изменяют файлы в main (plan-dev.md маппинг Issues, frontmatter статусы, README dashboard). Зафиксировать **до** создания ветки:

```bash
git add specs/analysis/NNNN-{topic}/ specs/analysis/README.md
git commit -m "feat(analysis): NNNN-{topic} RUNNING, маппинг Issues"
git push origin main
```

**Логика:** Ветка (шаг 7) отводится от чистого main, содержащего все метаданные цепочки.

### Шаг 7: Создать ветку

```
/branch-create {NNNN}
```

Ветка создаётся от свежего main (после push шага 6).

### Шаг 8: Отчёт

Вывести: Issues (#N), Milestone, Branch, статус цепочки → RUNNING.

### Шаг 9: Предложить начать разработку

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: "Цепочка NNNN-{topic} в RUNNING. Начать разработку?"

| Ответ | Действие |
|-------|----------|
| Да | Запустить разработку по [modify-development.md](./modify-development.md) (dev-agent) |
| Нет | Завершить воркфлоу |

---

## Чек-лист

- [ ] Все 4 документа цепочки существуют и в WAITING
- [ ] Маркеров `[ТРЕБУЕТ УТОЧНЕНИЯ]` = 0
- [ ] Пользователь подтвердил запуск
- [ ] Issues созданы из TASK-N
- [ ] Поле Issue заполнено inline в каждой TASK-N
- [ ] Milestone создан/привязан
- [ ] Цепочка переведена в RUNNING
- [ ] Коммит + Push в main (метаданные цепочки)
- [ ] Ветка создана (от свежего main)
- [ ] README обновлён
- [ ] Отчёт выведен
- [ ] Пользователю предложено начать разработку

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
