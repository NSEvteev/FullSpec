---
description: Воркфлоу завершения analysis chain — pre-flight проверки, T7 DONE каскад, перенос Planned Changes в AS IS, cross-chain, отчёт.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу завершения analysis chain

Рабочая версия стандарта: 1.3

Процесс завершения analysis chain: pre-flight проверки, T7 → DONE (bottom-up каскад), перенос Planned Changes → AS IS в specs/docs/, обновление Changelog, cross-chain проверка, отчёт.

**Полезные ссылки:**
- [standard-analysis.md § 6.6](./analysis/standard-analysis.md#66-review-to-done) — SSOT правил каскада DONE
- [standard-analysis.md § 7.3](./analysis/standard-analysis.md#73-обновление-при-реализации-to-done) — обновление specs/docs/ при DONE

**SSOT-зависимости:**
- [standard-analysis.md](./analysis/standard-analysis.md) — правила перехода T7, DONE_CASCADE_ORDER, обновление docs/
- [chain_status.py](./.scripts/chain_status.py) — T7, bottom-up каскад, side_effects, dry_run, check_cross_chain
- [standard-service.md](./docs/service/standard-service.md) — формат docs/{svc}.md (§§ 1-8 маппинг)

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
  - [Шаг 1: Pre-flight проверки](#шаг-1-pre-flight-проверки)
  - [Шаг 2: Переход T7 (DONE каскад)](#шаг-2-переход-t7-done-каскад)
  - [Шаг 3: Обновление docs/ (Design DONE)](#шаг-3-обновление-docs-design-done)
  - [Шаг 3.5: Обновление .system/ (system-agent mode=done)](#шаг-35-обновление-system-system-agent-modedone)
  - [Шаг 4: Cross-chain проверка](#шаг-4-cross-chain-проверка)
  - [Шаг 5: Отчёт](#шаг-5-отчёт)
- [Маппинг SVC-N на docs/](#маппинг-svc-n-на-docs)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Fail Fast.** Все проверки — до любых мутаций. Если pre-flight не пройден — СТОП.

> **Bottom-up каскад.** Plan Dev → Plan Tests → Design → Discussion. Порядок закодирован в `chain_status.py DONE_CASCADE_ORDER`.

> **Planned Changes → AS IS.** Дельты из design SVC-N переносятся в docs/{svc}.md: ADDED — добавить, MODIFIED — заменить, REMOVED — удалить.

> **Идемпотентность через chain-маркер.** Проверить наличие `<!-- chain: NNNN-{topic} -->` в Planned Changes. Нет маркера — docs/ уже обновлены, skip.

> **DONE — финальный.** Откат DONE невозможен. Cross-chain alerts возвращаются в отчёте, но НЕ прерывают процесс.

> **review.md остаётся RESOLVED.** При DONE review.md не меняет статус — остаётся в RESOLVED. Это документированное поведение.

---

## Шаги

### Шаг 1: Pre-flight проверки

**Входные данные:** номер цепочки `{NNNN}`.

Все проверки выполняются **до** любых мутаций:

| # | Проверка | Команда | Ожидание |
|---|----------|---------|----------|
| 1 | Статусы документов | `python specs/.instructions/.scripts/chain_status.py status {NNNN}` | Все 4 документа в REVIEW |
| 2 | review.md существует | `Read specs/analysis/{NNNN}-{topic}/review.md` | Файл существует, `status: RESOLVED` |
| 3 | Вердикт review | Прочитать последнюю итерацию review.md | Вердикт = `READY` |
| 4 | SVC-N в design.md | `Read specs/analysis/{NNNN}-{topic}/design.md` | Хотя бы один SVC-N |
| 5 | docs/ файлы | Проверить что все `docs/{svc}.md` из SVC-N существуют | Файлы доступны |
| 6 | Planned Changes | Проверить что docs/{svc}.md содержат блоки `<!-- chain: {NNNN}-{topic} -->` | Маркеры присутствуют |

Если **любая** проверка не прошла — **СТОП** с описанием причины. Не выполнять T7.

### Шаг 2: Переход T7 (DONE каскад)

```bash
python specs/.instructions/.scripts/chain_status.py transition {NNNN} DONE
```

Bottom-up каскад: Plan Dev → Plan Tests → Design → Discussion. `chain_status.py` итерирует `DONE_CASCADE_ORDER`, пропускает уже DONE. Возвращает `side_effects` — список действий для обновления docs/.

**Dry-run (опционально):**

```bash
python specs/.instructions/.scripts/chain_status.py transition {NNNN} DONE --dry-run
```

Возвращает preview без мутаций.

### Шаг 3: Обновление docs/ (Design DONE)

Основной блок — перенос Planned Changes → AS IS:

| Файл docs/ | Действие |
|-----------|----------|
| `{svc}.md` §§ 1-8 | Контент из Planned Changes → основные секции (ADDED — добавить, MODIFIED — заменить, REMOVED — удалить) |
| `{svc}.md` § 9 Planned Changes | Удалить всё между `<!-- chain: {NNNN}-{topic} -->` и `<!-- /chain: {NNNN}-{topic} -->` (включая оба тега) |
| `{svc}.md` § 10 Changelog | Новая запись: номер цепочки, дата, описание изменений |

> **Обновление .system/ файлов** (overview, conventions, infrastructure, testing) — см. Шаг 3.5 (system-agent mode=done).

**Как определить что менять:**

Прочитать design.md — SVC-N секции (§§ 1-8 маппятся 1:1 на docs/{svc}.md §§ 1-8). Каждая подсекция SVC-N содержит дельты ADDED/MODIFIED/REMOVED — применить их к соответствующим секциям docs/.

**Идемпотентность:** Проверить наличие chain-маркера `<!-- chain: {NNNN}-{topic} -->` в Planned Changes § 9. Если маркера нет — docs/ уже обновлены, skip.

**Per-tech стандарты (`specs/docs/.technologies/standard-{tech}.md`, `.claude/rules/{tech}.md`):**
Не требуют обновления при DONE — создаются и ревьюятся при Design → WAITING (technology-agent + technology-reviewer). При DONE остаются как есть.

**При ошибке в одном сервисе:** записать ошибку, продолжить с остальными сервисами. Отразить в отчёте.

### Шаг 3.5: Обновление .system/ (system-agent mode=done)

Полноценное обновление всех 4 файлов specs/docs/.system/ из Design + Plan Tests + реального кода.

**Запуск system-agent mode=done:**

```bash
# Task tool с subagent_type=system-agent
# Входные данные:
#   design-path: specs/analysis/{NNNN}-{topic}/design.md
#   plan-test-path: specs/analysis/{NNNN}-{topic}/plan-test.md
#   src-path: src/
#   mode: done
```

| Файл .system/ | Источники данных | Действие |
|------|--------|----------|
| `overview.md` | Design SVC-N, INT-N + реальный код | Финализация: подтвердить/уточнить данные из /docs-sync (mode=sync) |
| `conventions.md` | Design + реальные паттерны из кода | Обновить API конвенции, форматы ответов/ошибок |
| `infrastructure.md` | Реальный код: docker-compose.yml, .env.example | Обновить Docker Compose, переменные окружения, порты |
| `testing.md` | Plan Tests TC-N + реальные тест-файлы | Обновить стратегию, системные сценарии, покрытие |

**Запуск system-reviewer mode=done:**

После system-agent — сверка всех 4 файлов с источниками. Вердикт: ACCEPT / REVISE.

При REVISE: перезапуск system-agent mode=done с REVISE-таблицей в prompt. Макс. 3 итерации, потом — в отчёт как warning.

**При ошибке:** записать ошибку, продолжить с Шагом 4. Отразить в отчёте.

### Шаг 4: Cross-chain проверка

```bash
python specs/.instructions/.scripts/chain_status.py check_cross_chain {NNNN}
```

Вызывается **после** обновления docs/ и **до** финального отчёта.

**Реакции (информировать в отчёте):**

| Статус другой цепочки | Реакция | Severity |
|-----------------------|---------|----------|
| DRAFT | Перегенерировать затронутые документы | info |
| WAITING | Дообновить контекст | warning |
| RUNNING | → CONFLICT | critical |
| DONE | Предложить новую Discussion | info |

При critical alert — **предупредить в отчёте**, но НЕ прерывать (DONE — финальный, откат невозможен).

### Шаг 5: Отчёт

Вернуть структурированный отчёт:

```
## Отчёт завершения цепочки {NNNN}

**Статус:** DONE

### Каскад:
  plan-dev.md:    REVIEW → DONE
  plan-test.md:   REVIEW → DONE
  design.md:      REVIEW → DONE (+ docs/ updated)
  discussion.md:  REVIEW → DONE

### docs/ обновлено:
  - {svc}.md: §§ {список} updated, Changelog added
  - overview.md: AS IS updated (если затронуто)

### Cross-chain alerts:
  - {список или "нет"}

### Ошибки:
  - {список или "нет"}

### Next:
  - /milestone-validate (если все цепочки milestone завершены)
```

---

## Маппинг SVC-N на docs/

Design SVC-N §§ 1-8 маппятся 1:1 на docs/{svc}.md §§ 1-8:

| SVC-N подсекция | docs/{svc}.md секция |
|-----------------|---------------------|
| § 1 Purpose | § 1 Purpose |
| § 2 API | § 2 API |
| § 3 Data Model | § 3 Data Model |
| § 4 Dependencies | § 4 Dependencies |
| § 5 Events | § 5 Events |
| § 6 Error Handling | § 6 Error Handling |
| § 7 Tech Stack | § 7 Tech Stack |
| § 8 Configuration | § 8 Configuration |

Каждая подсекция SVC-N содержит дельты:
- **ADDED** — новый контент, добавить в соответствующую секцию docs/
- **MODIFIED** — заменить существующий контент
- **REMOVED** — удалить из docs/

---

## Чек-лист

### Pre-flight
- [ ] Номер цепочки {NNNN} получен
- [ ] Все 4 документа в REVIEW
- [ ] review.md существует, status: RESOLVED, вердикт READY
- [ ] Design содержит SVC-N
- [ ] Все docs/{svc}.md существуют
- [ ] Planned Changes содержат chain-маркер

### Выполнение
- [ ] T7 каскад выполнен (bottom-up)
- [ ] docs/{svc}.md §§ 1-8 обновлены (Planned Changes → AS IS)
- [ ] docs/{svc}.md § 9 Planned Changes: chain-блок удалён
- [ ] docs/{svc}.md § 10 Changelog: запись добавлена
- [ ] system-agent mode=done запущен (все 4 .system/ файла)
- [ ] system-reviewer mode=done: ACCEPT (или warnings в отчёте)
- [ ] Cross-chain проверка выполнена

### Отчёт
- [ ] Структурированный отчёт сформирован
- [ ] Cross-chain alerts включены
- [ ] Ошибки (если есть) описаны
- [ ] Next steps указаны

---

## Примеры

### Завершение цепочки с двумя сервисами

```bash
# 1. Pre-flight
python specs/.instructions/.scripts/chain_status.py status 0042
# → Все 4 документа: REVIEW
# Проверить review.md → RESOLVED, READY

# 2. T7 каскад
python specs/.instructions/.scripts/chain_status.py transition 0042 DONE
# → plan-dev → plan-test → design → discussion: DONE

# 3. Обновить docs/ (по SVC-N из design.md)
# auth.md: §§ 1,2,3,5 — применить ADDED/MODIFIED/REMOVED
# gateway.md: §§ 2,4 — применить дельты
# Удалить Planned Changes блоки <!-- chain: 0042-user-auth -->
# Добавить Changelog записи

# 3.5. Обновить .system/ через system-agent mode=done + system-reviewer mode=done

# 4. Cross-chain
python specs/.instructions/.scripts/chain_status.py check_cross_chain 0042
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [chain_status.py](./.scripts/chain_status.py) | T7 каскад, side_effects, dry_run, cross-chain | Этот документ |

---

## Скиллы

| Скилл | Назначение | SSOT |
|-------|------------|------|
| `/chain-done` | Завершение analysis chain (RUNNING → REVIEW → DONE) | Этот документ |
