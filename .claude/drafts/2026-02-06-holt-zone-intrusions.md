# Зональный анализ черновиков Холта

Анализ пересечений зон ответственности в 5 holt-analysis файлах.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Сводная таблица вторжений](#сводная-таблица-вторжений)
  - [Детальный разбор](#детальный-разбор)
  - [Классификация действий](#классификация-действий)
  - [Итого](#итого)

---

## Контекст

**Задача:** Проверить 5 holt-analysis файлов на вторжения в чужие зоны ответственности перед применением рекомендаций.

**Почему:** Рекомендации Холта могут предлагать добавить контент, который принадлежит другому стандарту. Применение таких рекомендаций создаёт дублирование и нарушает SSOT.

**Связанные файлы:**
- [standard-github-workflow.md](/.github/.instructions/standard-github-workflow.md) — оркестратор (источник зон)
- [2026-02-05-standards-validation-plan.md](./2026-02-05-standards-validation-plan.md) — план валидации

---

## Содержание

**Источник зон:** [standard-github-workflow.md](/.github/.instructions/standard-github-workflow.md) — таблицы "Этапы жизненного цикла", "Независимые объекты", "Автоматизация".

**Файлы анализа:**
- ~~`holt-analysis-standard-branching.md`~~ → зона: naming convention, жизненный цикл ветки, запреты, граничные случаи — **УДАЛЁН** (рекомендации применены, v1.2)
- ~~`holt-analysis-standard-development.md`~~ → зона: процесс работы в feature-ветке, make-команды, тестирование, локальные проверки — **УДАЛЁН** (рекомендации применены, v1.1)
- `holt-analysis-standard-commit.md` → зона: Conventional Commits, типы, scope, body/footer, правила, процесс коммита, pre-commit hooks
- `holt-analysis-standard-review.md` → зона: Code Review, Merge стратегии, Branch Protection, блокирующие условия
- `holt-analysis-standard-sync.md` → зона: триггеры синхронизации, процесс, разрешение конфликтов, запреты

---

## Сводная таблица вторжений

| ID | Источник (holt) | Проблема # | Вторгается в зону | Целевой файл | Уже покрыто? | Действие | Статус |
|----|-----------------|------------|-------------------|--------------|:------------:|----------|:------:|
| B1 | branching | 1.7 | Issues (create) | create-issue.md | ДА | Заменить CLI-пример на SSOT-ссылку | ✅ Применено: §5 "Без Issue" → ссылка на create-issue.md |
| B2 | branching | 2.2 | Labels | standard-labels.md | ДА | Заменить на SSOT-ссылку на standard-labels.md | ✅ Пропущено — рекомендация не применялась (зона Issues) |
| B3 | branching | 2.3 | Issues + Labels | standard-issue.md, standard-labels.md | ДА | Заменить алгоритм на SSOT-ссылку | ✅ Пропущено — рекомендация не применялась (зона Issues) |
| B4 | branching | 4.4 | Review (merge) | standard-review.md | ДА (§3) | Добавить SSOT-ссылку, не дублировать описание | ✅ Пропущено — рекомендация не применялась (зона Review) |
| C1 | commit | 2.6 | Branching + Sync | standard-branching.md, standard-sync.md | ЧАСТИЧНО | Оставить кратко (контекст amend), убрать детали push | ⏳ |
| D1 | development | 1.3 | Commits (hooks) | standard-commit.md | ДА (§6) | Убрать дублирование, оставить SSOT-ссылку на standard-commit.md | ✅ development v1.1 |
| D2 | development | 1.5 | Sync | standard-sync.md | ДА | Рекомендация корректна — добавить SSOT-ссылку (не детали) | ✅ development v1.1 |
| D3 | development | 4.4 | Sync | standard-sync.md | ДА | Не добавлять в development — это зона sync | ✅ Пропущено |
| R1 | review | #11 | Branching | standard-branching.md | ДА (§3) | Холт уже указал — заменить на SSOT-ссылку | ⏳ |
| R2 | review | #12 | State | standard-state.md | ДА | Холт уже указал — заменить на SSOT-ссылку | ⏳ |
| R3 | review | #15 | CODEOWNERS | standard-codeowners.md | НЕТ | SSOT-ссылка на standard-codeowners.md (содержимое добавить туда) | ⏳ |
| R4 | review | #18 | Actions | standard-action.md | — | Холт уже указал — отложить | ⏳ |
| S1 | sync | 1.4 | Branching + PR | standard-branching.md, standard-pull-request.md | ЧАСТИЧНО | Уточнить формулировку в sync, добавить ссылку на branching/PR | ⏳ |
| S2 | sync | 4.3 | Branching | standard-branching.md | НЕТ | Добавить в branching (граничные случаи), не в sync | ⏳ |
| S3 | sync | 5.3 | Branching (fork) | standard-branching.md | НЕТ | Отложить — проект не использует fork-модель (P3) | ⏳ |

---

## Детальный разбор

### B1: branching → Issues (create)

**Проблема 1.7** рекомендует добавить в branching CLI-пример `gh issue create --title "..." --body "..." --label type:feature`.

**Целевой файл:** `create-issue.md` — полный воркфлоу создания Issue с примерами CLI.

**Уже покрыто:** ДА. create-issue.md содержит 8 шагов создания Issue, примеры CLI, batch-создание.

**Решение:** В branching edge case "Ветка создана без Issue" заменить CLI-пример на SSOT-ссылку:
> Создать Issue: см. [create-issue.md](../issues/create-issue.md) или `/issue-create`

---

### B2: branching → Labels

**Проблема 2.2** рекомендует добавить в branching: "Перед созданием ветки проверить, что Issue имеет одну из TYPE-меток. Если TYPE-метка отсутствует — добавить через `gh issue edit`".

**Целевой файл:** `standard-labels.md` — правила применения меток. `standard-issue.md` §4 — обязательные метки при создании.

**Уже покрыто:** ДА. standard-issue.md §4 Labels уже требует "Ровно 1 метка типа". validate-issue.py проверяет это (E007).

**Решение:** В branching добавить SSOT-ссылку, не дублировать правила меток:
> Перед созданием ветки: Issue ДОЛЖЕН иметь TYPE-метку (→ [standard-issue.md §4](../issues/standard-issue.md#labels-обязательные-метки)).

---

### B3: branching → Issues + Labels (алгоритм выбора TYPE)

**Проблема 2.3** рекомендует добавить 5-шаговый алгоритм с вызовом `gh issue view --json labels -q '...'`.

**Целевой файл:** standard-issue.md (метки Issue), standard-labels.md (формат меток).

**Уже покрыто:** ДА. Метки используют простые имена (bug, feature), уже задокументировано. validate-issue.py проверяет наличие TYPE-меток.

**Решение:** В branching описать ТОЛЬКО правило выбора prefix (уже есть — таблица соответствия TYPE → prefix). Алгоритм запросов к GitHub API не нужен — это зона Issues.

---

### B4: branching → Review (Squash Merge)

**Проблема 4.4** рекомендует добавить объяснение Squash Merge в branching.

**Целевой файл:** `standard-review.md` §3 — merge стратегии.

**Уже покрыто:** ДА. standard-review.md содержит описание merge стратегий.

**Решение:** В branching добавить SSOT-ссылку:
> Merge стратегия: Squash Merge (→ [standard-review.md §3](../review/standard-review.md))

---

### C1: commit → Branching + Sync (amend и force push)

**Проблема 2.6** рекомендует уточнить правила `--amend`: "Допустимо в feature-ветке, если никто не работает с веткой (после amend потребуется `git push --force-with-lease`)".

**Целевые файлы:** standard-branching.md (личная ветка), standard-sync.md (force push).

**Уже покрыто:** ЧАСТИЧНО. sync упоминает force push после rebase. Branching запрещает вложенные ветки, но не описывает "личную ветку".

**Решение:** Оставить кратко в commit (контекст amend — это зона commit). Force push деталь — ссылка на sync:
> После amend запушенного коммита — `git push --force-with-lease` (→ [standard-sync.md §5](../sync/standard-sync.md#5-запреты-и-ограничения)).

---

### D1: development → Commits (pre-commit hooks)

**Проблема 1.3** рекомендует уточнить `make lint` vs pre-commit hooks.

**Целевой файл:** `standard-commit.md` §6 — процесс коммита, hooks.

**Уже покрыто:** ДА. standard-commit.md §6 описывает hooks при `git commit`. standard-development.md уже содержит SSOT-ссылку на commit §6.

**Решение:** В development НЕ дублировать описание hooks. Рекомендация Холта корректна в части "добавить SSOT-ссылку", но сами правила hooks — зона commit.

---

### D2: development → Sync (длительная разработка)

**Проблема 1.5** рекомендует добавить принцип синхронизации с main при >2 дней.

**Целевой файл:** `standard-sync.md` §2 — триггеры синхронизации.

**Уже покрыто:** ДА. sync содержит триггер "При длительной разработке (>2 дней)".

**Решение:** В development добавить SSOT-ссылку (не детали):
> При разработке >2 дней — синхронизировать с main (→ [standard-sync.md](../sync/standard-sync.md))

---

### D3: development → Sync (граничные случаи)

**Проблема 4.4** рекомендует добавить граничные случаи длительной разработки (частота sync, конфликты, force-push после rebase).

**Целевой файл:** `standard-sync.md` — весь процесс синхронизации.

**Уже покрыто:** ДА. sync описывает процесс, конфликты, force push.

**Решение:** НЕ добавлять в development. Это полностью зона sync.

---

### R1-R4: review — уже идентифицировано Холтом

Холт сам пометил 4 рекомендации как зональные вторжения (зачёркнуты в итоговой таблице):
- **R1** (#11): Удаление ветки → branching §3 (ПОКРЫТО)
- **R2** (#12): State для агентов → standard-state.md (ПОКРЫТО)
- **R3** (#15): CODEOWNERS конфигурация → standard-codeowners.md (НЕ ПОКРЫТО — добавить в codeowners)
- **R4** (#18): Webhook-интеграция → standard-action.md (ОТЛОЖИТЬ)

---

### S1: sync → Branching + PR (force push до/после PR)

**Проблема 1.4** рекомендует уточнить "личная ветка" → "feature-ветка ДО создания PR".

**Целевые файлы:** standard-branching.md (жизненный цикл), standard-pull-request.md (создание PR).

**Уже покрыто:** ЧАСТИЧНО. Branching описывает жизненный цикл, но не привязывает "личную ветку" к PR-статусу.

**Решение:** Уточнение валидно для sync (критерий force push). Добавить ссылки:
> Допустимо ТОЛЬКО для feature-ветки до создания PR (→ [standard-pull-request.md](../pull-requests/standard-pull-request.md))

---

### S2: sync → Branching (несколько feature-веток)

**Проблема 4.3** рекомендует добавить процесс работы с несколькими feature-ветками.

**Целевой файл:** `standard-branching.md` — граничные случаи.

**Уже покрыто:** НЕТ. Branching описывает переключение между ветками (§5), но не покрывает синхронизацию каждой.

**Решение:** Добавить в branching (граничные случаи), с SSOT-ссылкой на sync для процесса:
> При работе с несколькими feature-ветками — синхронизировать каждую с main перед переключением (→ standard-sync.md)

---

### S3: sync → Branching (fork-модель)

**Проблема 5.3** рекомендует добавить синхронизацию при работе с fork'ами.

**Уже покрыто:** НЕТ (нигде).

**Решение:** Отложить (P3). Проект использует централизованную модель (один origin). Fork-модель актуальна для open-source, но не для текущего проекта.

---

## Классификация действий

### Приоритет 1: Заменить вторжения на SSOT-ссылки (при применении рекомендаций)

| ID | При применении рекомендации к файлу | Вместо | Сделать |
|----|--------------------------------------|--------|---------|
| B1 | standard-branching.md | CLI `gh issue create` | SSOT-ссылка → create-issue.md |
| B2 | standard-branching.md | Правила TYPE-меток | SSOT-ссылка → standard-issue.md §4 |
| B3 | standard-branching.md | 5-шаговый алгоритм запросов | Убрать — зона Issues |
| B4 | standard-branching.md | Описание Squash Merge | SSOT-ссылка → standard-review.md §3 |
| D1 | standard-development.md | Описание hooks | SSOT-ссылка → standard-commit.md §6 |
| D2 | standard-development.md | Детали синхронизации | SSOT-ссылка → standard-sync.md |
| D3 | standard-development.md | Граничные случаи sync | НЕ добавлять — зона sync |
| R1 | standard-review.md | Удаление ветки | SSOT-ссылка → standard-branching.md §3 |

### Приоритет 2: Добавить в целевые файлы (если не покрыто)

| ID | Целевой файл | Что добавить |
|----|-------------|--------------|
| R3 | standard-codeowners.md | Автоназначение ревьюеров через CODEOWNERS |
| S2 | standard-branching.md | Граничный случай: работа с несколькими ветками |

### Приоритет 3: Отложить

| ID | Тема | Причина |
|----|------|---------|
| S3 | Fork-модель | Проект не использует fork'и |
| R4 | Webhook-интеграция | Зона actions, не приоритет |

---

## Итого

- **15 вторжений** найдено в 5 черновиках
- **8** — заменить на SSOT-ссылки при применении рекомендаций (P1)
- **2** — добавить контент в целевые файлы (P2)
- **3** — уже идентифицированы Холтом (R1, R2, R4)
- **2** — отложить (P3)

**Прогресс:** 7/15 разрешены ✅ (B1-B4 branching, D1-D3 development), 8/15 ожидают ⏳ (commit, review, sync).

**Вывод:** Большинство вторжений — это рекомендации добавить КОНТЕНТ чужой зоны в анализируемый файл. Правильное действие: при применении рекомендаций заменять контент на SSOT-ссылки на правильный стандарт.
