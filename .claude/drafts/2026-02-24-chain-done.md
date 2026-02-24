# Воркфлоу завершения цепочки — инструкция + скилл

Последовательный bottom-up переход цепочки из REVIEW в DONE с обновлением docs/ на каждом уровне.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G11 из standard-process.md — переход в DONE должен быть отдельным скиллом
**Почему создан:** Определить формат инструкции и скилла `/chain-done` перед реализацией
**Связанные файлы:**
- `specs/.instructions/standard-process.md` — §5 Фаза 5 (Завершение цепочки)
- `specs/.instructions/analysis/standard-analysis.md` — §6.6 REVIEW to DONE, §7.3 Обновление при реализации
- `specs/.instructions/.scripts/chain_status.py` — ChainManager.transition(to="DONE")
- `specs/.instructions/analysis/review/standard-review.md` — вердикт READY

## Содержание

### Проблема

Переход REVIEW → DONE — сложный многошаговый процесс:

1. **Bottom-up каскад:** Plan Dev → Plan Tests → Design → Discussion — каждый документ переводится в DONE последовательно снизу вверх
2. **Обновление docs/:** При Design → DONE: Planned Changes переносятся в AS IS (§7.3)
3. **Сервисные документы:** {svc}.md обновляются — Planned Changes → основной контент, Changelog
4. **Per-tech стандарты:** standard-{tech}.md обновляются если были изменены
5. **review.md:** Должен быть RESOLVED с вердиктом READY

Сейчас это делается вручную: пользователь последовательно вызывает скиллы на модификацию каждого документа.

### Артефакты

По архитектуре проекта: **инструкция (SSOT) → скилл (обёртка)**. Скилл без SSOT-инструкции запрещён.

| # | Артефакт | Путь | Назначение |
|---|---------|------|------------|
| 1 | **Воркфлоу-инструкция** (SSOT) | `specs/.instructions/analysis/create-chain-done.md` | Пошаговый процесс bottom-up DONE перехода — шаги, чек-лист, примеры |
| 2 | **Скилл** (обёртка) | `/.claude/skills/chain-done/SKILL.md` | Ссылка на SSOT, формат вызова `/chain-done` |

Инструкция регистрируется в `specs/.instructions/analysis/README.md` или `specs/.instructions/README.md`.

> **Расположение:** `specs/.instructions/analysis/` — потому что DONE-переход относится к analysis chain, а не к GitHub или structure.

### Порядок создания

1. `/instruction-create create-chain-done --path specs/.instructions/analysis/` — инструкция
2. `/skill-create chain-done` — скилл, SSOT → create-chain-done.md

### Предлагаемая связка

**Инструкция:** `create-chain-done.md` (SSOT — шаги, чек-лист, примеры)
**Скилл:** `/chain-done` (обёртка — ссылка на SSOT, формат вызова)
**Тип:** Оркестратор bottom-up перехода

### Формат вызова

```
/chain-done {NNNN}
```

| Параметр | Описание | Обязательный |
|----------|----------|--------------|
| `NNNN` | Номер analysis chain | Да |

### Шаги инструкции (create-chain-done.md)

```
/chain-done 0001
```

| Шаг | Действие | Детали | Инструмент |
|-----|---------|--------|------------|
| 1 | Проверить prerequisites | Цепочка в REVIEW, review.md RESOLVED с READY | chain_status.py (check_prerequisites) |
| 2 | Подтверждение пользователя | AskUserQuestion: "Цепочка NNNN готова к завершению?" | AskUserQuestion |
| 3 | Plan Dev → DONE | Вызвать `/plan-dev-modify` с переходом в DONE | `/plan-dev-modify`, chain_status.py (T7) |
| 4 | Plan Tests → DONE | Вызвать `/plan-test-modify` с переходом в DONE | `/plan-test-modify`, chain_status.py (T7) |
| 5 | Design → DONE | Вызвать `/design-modify` с переходом в DONE. **Триггер обновления docs/:** Planned Changes → AS IS | `/design-modify`, chain_status.py (T7) |
| 6 | Обновить docs/ | Для каждого SVC-N: {svc}.md Planned Changes → AS IS, Changelog | `/service-modify` per SVC-N |
| 7 | Обновить per-tech | Если standard-{tech}.md были изменены — финализировать | `/technology-modify` (если нужно) |
| 8 | Discussion → DONE | Вызвать `/discussion-modify` с переходом в DONE | `/discussion-modify`, chain_status.py (T7) |
| 9 | Проверить cross-chain | check_cross_chain() — не затронуты ли другие цепочки | chain_status.py |
| 10 | Обновить README | Dashboard в specs/analysis/README.md | chain_status.py (авто) |
| 11 | Отчёт | Что обновлено, какие docs/ затронуты | Вывод |

### Порядок bottom-up

```
Plan Dev (REVIEW → DONE)
    ↓
Plan Tests (REVIEW → DONE)
    ↓
Design (REVIEW → DONE)
    ↓ → docs/ update (Planned Changes → AS IS)
    ↓ → per-tech update
    ↓
Discussion (REVIEW → DONE)
    ↓
cross-chain check
    ↓
Отчёт
```

### Что обновляется в docs/ (Шаг 6)

Из standard-analysis.md §7.3:

| Документ | Что обновляется |
|----------|----------------|
| `{svc}.md` §§ 1-8 | Planned Changes → AS IS (основной контент) |
| `{svc}.md` § 10 Changelog | Новая запись: версия, дата, описание изменений |
| `overview.md` | Обновление если затронута архитектура |
| `conventions.md` | Обновление если затронуты конвенции |
| `infrastructure.md` | Обновление если затронута инфраструктура |
| `testing.md` | Обновление если затронуто тестирование |

### Обработка ошибок

| Ситуация | Реакция |
|----------|---------|
| review.md не RESOLVED | СТОП: "review.md должен быть RESOLVED с вердиктом READY" |
| review.md вердикт CONFLICT | СТОП: "Вердикт CONFLICT — необходим переход в CONFLICT, не DONE" |
| Цепочка не в REVIEW | СТОП: "Цепочка должна быть в статусе REVIEW" |
| cross-chain конфликт | WARN: "Обнаружен конфликт с цепочкой MMMM, необходимо проверить" |
| Ошибка -modify | СТОП на текущем документе, откат невозможен — пользователю решать |

### Идемпотентность

Если документ уже в DONE — пропустить с сообщением. Позволяет перезапуск при частичном выполнении.

## Решения

- **Инструкция → скилл:** create-chain-done.md (SSOT) → /chain-done (обёртка), по архитектуре проекта
- Bottom-up порядок: Plan Dev → Plan Tests → Design → Discussion (от терминального к корню)
- Design → DONE — триггер обновления docs/ (самый тяжёлый шаг)
- Каждый -modify вызов делает свою работу по обновлению документа: скилл только оркестрирует порядок
- chain_status.py обрабатывает T7 переход для каждого документа

## Открытые вопросы

- Нужно ли автоматически предлагать `/milestone-validate` после DONE (следующий шаг — Release)?
- Нужен ли `--dry-run` режим для предварительного просмотра изменений?
- Как обрабатывать ситуацию когда один из -modify шагов не прошёл (частичный DONE)?
