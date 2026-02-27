---
description: Воркфлоу отката analysis chain — T9 ROLLING_BACK, откат артефактов top-down, верификация, T10 REJECTED.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу отката analysis chain

Рабочая версия стандарта: 1.3

Процесс отката analysis chain: чтение состояния, T9 → ROLLING_BACK, откат артефактов top-down (Plan Dev → Design → Plan Tests → Discussion), верификация, T10 → REJECTED, отчёт.

**Полезные ссылки:**
- [standard-analysis.md §§ 6.7-6.8](./analysis/standard-analysis.md#67-to-rolling_back) — SSOT правил отката
- [standard-analysis.md § 7.5](./analysis/standard-analysis.md#75-обновление-при-откате-rolling_back-rejected) — обновление docs/ при откате

**SSOT-зависимости:**
- [standard-analysis.md](./analysis/standard-analysis.md) — правила переходов T9/T10, артефакты для отката
- [chain_status.py](./.scripts/chain_status.py) — T9, T10, side_effects, check_cross_chain
- [standard-issue.md](/.github/.instructions/issues/standard-issue.md) — закрытие Issues `--reason "not planned"`

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-analysis.md](./analysis/standard-analysis.md) |
| Валидация | *Не применимо* |
| Создание | Этот документ |
| Модификация | *Не применимо* |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Чтение состояния цепочки](#шаг-1-чтение-состояния-цепочки)
  - [Шаг 2: Переход T9 (ROLLING_BACK)](#шаг-2-переход-t9-rolling_back)
  - [Шаг 3: Откат Plan Dev](#шаг-3-откат-plan-dev)
  - [Шаг 4: Откат Design](#шаг-4-откат-design)
  - [Шаг 5: Откат Plan Tests](#шаг-5-откат-plan-tests)
  - [Шаг 6: Откат Discussion](#шаг-6-откат-discussion)
  - [Шаг 7: Cross-chain проверка](#шаг-7-cross-chain-проверка)
  - [Шаг 8: Верификация и T10 (REJECTED)](#шаг-8-верификация-и-t10-rejected)
  - [Шаг 9: Отчёт](#шаг-9-отчёт)
- [Таблица идемпотентности](#таблица-идемпотентности)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Идемпотентность всех шагов.** Каждый шаг безопасен для повторного выполнения — при частичном откате можно перезапустить агент.

> **Top-down порядок.** Сначала внешние артефакты (Issues, ветка), затем внутренние (docs/).

> **Одно подтверждение до запуска.** Основной LLM подтверждает с пользователем перед запуском rollback-agent. Агент работает автономно.

> **Продолжение при ошибке.** Если шаг завершился ошибкой — записать в отчёт, перейти к следующему шагу.

---

## Шаги

### Шаг 1: Чтение состояния цепочки

**Входные данные:** номер цепочки `{NNNN}`.

```bash
python specs/.instructions/.scripts/chain_status.py status {NNNN}
```

**Результат:** текущие статусы всех 4 документов цепочки.

**Дополнительно прочитать:**
1. `design.md` — определить затронутые сервисы, технологии, метки из SVC-N секций
2. `plan-dev.md` — определить TASK-N и привязанные Issues, имя ветки

**Определить scope:** какие документы не в DONE/REJECTED — они будут откатываться.

### Шаг 2: Переход T9 (ROLLING_BACK)

```bash
python specs/.instructions/.scripts/chain_status.py transition {NNNN} ROLLING_BACK
```

Tree-level: все не-DONE документы → ROLLING_BACK. Возвращает `side_effects` — список действий для отката.

### Шаг 3: Откат Plan Dev

**Артефакты для отката:**

| Артефакт | Команда | Идемпотентность |
|----------|---------|-----------------|
| Issues milestone | `gh issue close {N} --reason "not planned" --comment "Rolled back: chain {NNNN} rejected"` | Уже закрыт → no-op |
| Feature-ветка (remote) | `git push origin --delete {branch}` | Не существует → игнорировать ошибку |
| Feature-ветка (local) | `git branch -D {branch}` | Не существует → игнорировать ошибку |

### Шаг 4: Откат Design

Основной блок — 6 типов артефактов:

| # | Артефакт | Действие | Идемпотентность |
|---|---------|----------|-----------------|
| 1 | Planned Changes в `{svc}.md` § 9 | Удалить всё между `<!-- chain: {NNNN}-{topic} -->` и `<!-- /chain: {NNNN}-{topic} -->` (включая оба тега) | Нет маркера → skip |
| 2 | Inline-правки в `overview.md` | Если `docs-synced: true` в design.md: прочитать Design SVC-N, определить добавленные/изменённые записи (карта сервисов, связи, потоки, домены), удалить их из overview.md | docs-synced отсутствует → skip (overview.md не обновлялся) |
| 3 | Заглушка `{svc}.md` | Удалить файл если `created-by: {NNNN}` и нет других цепочек | Файл не существует → skip |
| 4 | Per-tech: `standard-{tech}.md`, `validation-{tech}.md`, `.claude/rules/{tech}.md`, строка в `.technologies/README.md` | Удалить файлы и строку реестра | Файл не существует → skip |
| 5 | Метка `svc:{svc}` | `gh label delete "svc:{svc}" --yes` | Метка не существует → skip |
| 6 | `docs-synced` в design.md | Удалить поле `docs-synced` из frontmatter design.md | Поле отсутствует → skip |

**Особый случай — Design (DONE) → REJECTED:**

Если Design уже был DONE (AS IS уже обновлён в docs/), откат по SVC-N секциям:
- **ADDED** → удалить из docs/
- **MODIFIED** → вернуть к предыдущему состоянию (из git history)
- **REMOVED** → восстановить (из git history)

Для восстановления из git history:
```bash
git show HEAD~N:specs/docs/{file}
```
Найти версию файла до DONE-каскада.

### Шаг 5: Откат Plan Tests

| Файл docs/ | Действие |
|-----------|----------|
| `.system/testing.md` | Откат изменений (если Plan Tests вносил изменения). Обычно no-op |

### Шаг 6: Откат Discussion

No-op — Discussion не создаёт артефактов в docs/.

### Шаг 7: Cross-chain проверка

```bash
python specs/.instructions/.scripts/chain_status.py check_cross_chain {NNNN}
```

**Реакции (информировать в отчёте):**

| Статус другой цепочки | Реакция |
|-----------------------|---------|
| DRAFT | Перегенерировать затронутые документы |
| WAITING | Дообновить контекст |
| RUNNING | → CONFLICT |
| DONE | Предложить новую Discussion |

### Шаг 8: Верификация и T10 (REJECTED)

**Чек-лист верификации** (каждый пункт — идемпотентная проверка):

| # | Проверка | Команда | Ожидание |
|---|----------|---------|----------|
| 1 | Planned Changes | `grep -r "chain: {NNNN}" specs/docs/` | Пусто |
| 2 | Issues | `gh issue list --milestone {milestone} --state open` | Пусто |
| 3 | Ветка | `git ls-remote --heads origin {branch}` | Пусто |
| 4 | Заглушки | `{svc}.md` с `created-by: {NNNN}` | Не существуют |
| 5 | Per-tech | `standard-{tech}.md` введённые цепочкой | Не существуют |

Если все проверки пройдены:

```bash
python specs/.instructions/.scripts/chain_status.py transition {NNNN} REJECTED
```

Если проверка не пройдена — записать в отчёт, **НЕ** выполнять T10.

### Шаг 9: Отчёт

Вернуть структурированный отчёт:

```
## Отчёт отката цепочки {NNNN}

**Статус:** REJECTED (или ROLLING_BACK при ошибках)

### Per-document:
- **Plan Dev:** Issues ×{N} закрыты, ветка {branch} удалена
- **Design:** Planned Changes удалены из {N} файлов, заглушки удалены: {список}
- **Plan Tests:** {действие или no-op}
- **Discussion:** no-op

### Cross-chain alerts:
- {список или "нет"}

### Ошибки:
- {список или "нет"}
```

---

## Таблица идемпотентности

Сводная таблица всех операций и их поведения при повторном выполнении:

| Операция | При повторе | Безопасность |
|----------|------------|--------------|
| `chain_status.py transition ROLLING_BACK` | Уже ROLLING_BACK → no-op | Безопасно |
| `gh issue close` | Уже закрыт → no-op | Безопасно |
| `git push origin --delete {branch}` | Не существует → ошибка (игнорировать) | Безопасно |
| `git branch -D {branch}` | Не существует → ошибка (игнорировать) | Безопасно |
| Удалить Planned Changes блок | Нет маркера → skip | Безопасно |
| Удалить заглушку | Файл не существует → skip | Безопасно |
| Удалить per-tech файлы | Файл не существует → skip | Безопасно |
| `gh label delete` | Метка не существует → skip | Безопасно |
| `chain_status.py transition REJECTED` | Уже REJECTED → no-op | Безопасно |

---

## Чек-лист

### Подготовка
- [ ] Номер цепочки {NNNN} получен
- [ ] Состояние цепочки прочитано (chain_status.py status)
- [ ] Scope отката определён (какие документы не в DONE/REJECTED)
- [ ] Design прочитан (сервисы, технологии, метки)
- [ ] Plan Dev прочитан (Issues, ветка)

### Выполнение
- [ ] T9 переход выполнен (→ ROLLING_BACK)
- [ ] Plan Dev откачен (Issues закрыты, ветка удалена)
- [ ] Design откачен (Planned Changes, заглушки, per-tech, метки)
- [ ] Plan Tests откачен (testing.md)
- [ ] Discussion откачен (no-op)
- [ ] Cross-chain проверка выполнена

### Верификация
- [ ] Planned Changes отсутствуют в docs/
- [ ] Открытые Issues отсутствуют
- [ ] Feature-ветка удалена
- [ ] Заглушки удалены
- [ ] Per-tech файлы удалены
- [ ] T10 переход выполнен (→ REJECTED)
- [ ] Отчёт сформирован

---

## Примеры

### Откат цепочки с Design в WAITING

```bash
# 1. Состояние
python specs/.instructions/.scripts/chain_status.py status 0042

# 2. T9
python specs/.instructions/.scripts/chain_status.py transition 0042 ROLLING_BACK

# 3. Plan Dev: закрыть Issues
gh issue close 15 --reason "not planned" --comment "Rolled back: chain 0042 rejected"
gh issue close 16 --reason "not planned" --comment "Rolled back: chain 0042 rejected"

# 3. Plan Dev: удалить ветку
git push origin --delete 0042-user-auth
git branch -D 0042-user-auth

# 4. Design: удалить Planned Changes
# (Edit: удалить chain-блоки из {svc}.md, откатить inline-правки в overview.md, удалить docs-synced из design.md)

# 7. Cross-chain
python specs/.instructions/.scripts/chain_status.py check_cross_chain 0042

# 8. Верификация
grep -r "chain: 0042" specs/docs/
gh issue list --milestone "v1.0" --state open
git ls-remote --heads origin 0042-user-auth

# 8. T10
python specs/.instructions/.scripts/chain_status.py transition 0042 REJECTED
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [chain_status.py](./.scripts/chain_status.py) | Переходы T9/T10, side_effects, cross-chain | Этот документ |

---

## Скиллы

*Нет скиллов — откат делегируется rollback-agent через Task tool.*
