---
description: Воркфлоу отката analysis chain — T9 ROLLING_BACK, откат артефактов top-down, верификация, T10 REJECTED.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу отката analysis chain

Рабочая версия стандарта: 1.3

Процесс отката analysis chain: 5 фаз оркестрации — основной LLM ставит ROLLING_BACK, rollback-agent откатывает артефакты, основной LLM валидирует + формирует отчёт, запрашивает подтверждение у пользователя, переводит в REJECTED и обновляет README.

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
- [Оркестрация](#оркестрация)
- [Шаги](#шаги)
  - [Шаг 1: Чтение состояния цепочки](#шаг-1-чтение-состояния-цепочки)
  - [Шаг 2: Переход T9 (ROLLING_BACK)](#шаг-2-переход-t9-rolling_back)
  - [Шаг 3: Откат Plan Dev (IF статус ≥ RUNNING)](#шаг-3-откат-plan-dev-if-статус--running)
  - [Шаг 4: Откат docs-sync артефактов (IF docs-synced: true)](#шаг-4-откат-docs-sync-артефактов-if-docs-synced-true)
  - [Шаг 5: Откат Plan Tests](#шаг-5-откат-plan-tests)
  - [Шаг 6: Откат Discussion](#шаг-6-откат-discussion)
  - [Шаг 7: Cross-chain проверка](#шаг-7-cross-chain-проверка)
  - [Шаг 8: Верификация и отчёт](#шаг-8-верификация-и-отчёт)
  - [Шаг 9: Подтверждение пользователя](#шаг-9-подтверждение-пользователя)
  - [Шаг 10: T10 (REJECTED) + README](#шаг-10-t10-rejected--readme)
- [Таблица идемпотентности](#таблица-идемпотентности)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Идемпотентность всех шагов.** Каждый шаг безопасен для повторного выполнения — при частичном откате можно перезапустить агент.

> **Top-down порядок.** Сначала внешние артефакты (Issues, ветка), затем внутренние (docs/).

> **Два подтверждения.** Первое — основной LLM запрашивает разрешение перед запуском rollback-agent. Второе — после отката основной LLM показывает отчёт и запрашивает подтверждение перехода в REJECTED через AskUserQuestion.

> **Продолжение при ошибке.** Если шаг завершился ошибкой — записать в отчёт, перейти к следующему шагу.

---

## Оркестрация

Rollback выполняется в 5 фаз. **Статусные переходы делает основной LLM** — агент только откатывает артефакты.

| Фаза | Исполнитель | Шаги | Действие |
|------|------------|------|---------|
| 1 | Основной LLM | 1–2 | Читает состояние → RUNNING → ROLLING_BACK |
| 2 | rollback-agent | 3–7 | Откат артефактов (Issues, ветка, docs-sync, cross-chain) |
| 3 | Основной LLM | 8 | Верификация + отчёт (изменённые/удалённые файлы) |
| 4 | Основной LLM | 9 | AskUserQuestion — подтверждение перехода в REJECTED |
| 5 | Основной LLM | 10 | ROLLING_BACK → REJECTED + обновить specs/analysis/README.md |

**Вызов rollback-agent** (Фаза 2) — с контекстом: номер цепочки, список сервисов, per-tech технологии, флаг `docs-synced`.

**Если пользователь отказался** на Фазе 4 — цепочка остаётся в `ROLLING_BACK`, работа останавливается.

---

## Шаги

### Шаг 1: Чтение состояния цепочки *(основной LLM)*

**Входные данные:** номер цепочки `{NNNN}`.

```bash
python specs/.instructions/.scripts/chain_status.py status {NNNN}
```

**Результат:** текущие статусы всех 4 документов цепочки.

**Дополнительно прочитать:**
1. `design.md` — определить затронутые сервисы, технологии, метки из SVC-N секций
2. `plan-dev.md` — определить TASK-N и привязанные Issues, имя ветки

**Определить scope:** какие документы не в DONE/REJECTED — они будут откатываться.

**Определить docs-synced:** прочитать frontmatter `design.md` — поле `docs-synced`.
- `docs-synced: true` → /docs-sync выполнялся, docs-sync артефакты существуют → откатывать (Шаг 4).
- `docs-synced` отсутствует или false → /docs-sync НЕ выполнялся → Шаг 4 skip.

**Определить статус цепочки:** если хотя бы один документ был в RUNNING или REVIEW → /dev-create выполнялся → откатывать dev-create артефакты (Шаг 3). Иначе Шаг 3 skip.

### Шаг 2: Переход T9 (ROLLING_BACK) *(основной LLM)*

```bash
python specs/.instructions/.scripts/chain_status.py transition {NNNN} ROLLING_BACK
```

Tree-level: все не-DONE документы → ROLLING_BACK. Возвращает `side_effects` — список действий для отката.

### Шаг 3: Откат Plan Dev (IF статус ≥ RUNNING) *(rollback-agent)*

**Артефакты для отката:**

| Артефакт | Команда | Идемпотентность |
|----------|---------|-----------------|
| Issues milestone | `gh issue close {N} --reason "not planned" --comment "Rolled back: chain {NNNN} rejected"` | Уже закрыт → no-op |
| Feature-ветка (remote) | `git push origin --delete {branch}` | Не существует → игнорировать ошибку |
| Feature-ветка (local) | `git branch -D {branch}` | Не существует → игнорировать ошибку |
| Milestone | Если Milestone содержит ТОЛЬКО Issues этой цепочки → `gh api -X DELETE repos/{owner}/{repo}/milestones/{number}`. Если есть Issues других цепочек → оставить. | Уже удалён → skip |
| review.md | Оставить as-is — review.md живёт в папке цепочки `specs/analysis/{NNNN}-{topic}/`, не управляется T9/T10 | No-op |

### Шаг 4: Откат docs-sync артефактов (IF docs-synced: true) *(rollback-agent)*

**Условие:** выполняется ТОЛЬКО если `docs-synced: true` в design.md. Если отсутствует/false → skip весь шаг.

| # | Артефакт | Действие | Идемпотентность |
|---|---------|----------|-----------------|
| 1 | Planned Changes в `{svc}.md` § 9 | Удалить всё между `<!-- chain: {NNNN}-{topic} -->` и `<!-- /chain: {NNNN}-{topic} -->` (включая оба тега) | Нет маркера → skip |
| 2 | Inline-правки в `overview.md` | Если `docs-synced: true` в design.md: прочитать Design SVC-N, определить добавленные/изменённые записи (карта сервисов, связи, потоки, домены), удалить их из overview.md | docs-synced отсутствует → skip (overview.md не обновлялся) |
| 3 | Заглушка `{svc}.md` | Удалить файл если `created-by: {NNNN}` и нет других цепочек | Файл не существует → skip |
| 4 | Per-tech: `standard-{tech}.md`, `security-{tech}.md` (если есть), `.claude/rules/{tech}.md`, строка в `.technologies/README.md` | Удалить файлы и строку реестра | Файл не существует → skip |
| 5 | Метка `svc:{svc}` | `gh label delete "svc:{svc}" --yes` | Метка не существует → skip |
| 6 | Docker `Dockerfile.{svc}` | Удалить `platform/docker/Dockerfile.{svc}` | Файл не существует → skip |
| 7 | Docker compose блок | Удалить блок сервиса из `platform/docker/docker-compose.yml` | Блок не найден → skip |
| 8 | Docker `init-db.sql` | Удалить `CREATE DATABASE myapp_{svc}` из `platform/docker/init-db.sql` | Строка не найдена → skip |
| 9 | Docker `.env` | Удалить per-service переменные из `.env.example` и `.env.test` | Переменные не найдены → skip |
| 10 | Docker `.dockerignore` | Удалить `src/{svc}/.dockerignore` | Файл не существует → skip |
| 11 | `specs/docs/README.md` | Удалить строки новых сервисов (если `created-by: {NNNN}`) | Строки отсутствуют → skip |
| 12 | `.github/labels.yml` | Удалить строки `svc:{svc}` из секции SVC (для сервисов с `created-by: {NNNN}`) | Строки отсутствуют → skip |
| 13 | `src/{svc}/` (папка кода) | **No-op** — папка может содержать код из параллельных цепочек | — |
| 14 | `docs-synced` в design.md | Удалить поле `docs-synced` из frontmatter design.md | Поле отсутствует → skip |

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

### Шаг 5: Откат Plan Tests *(rollback-agent)*

| Файл docs/ | Действие |
|-----------|----------|
| `.system/testing.md` | Откат изменений (если Plan Tests вносил изменения). Обычно no-op |

### Шаг 6: Откат Discussion *(rollback-agent)*

No-op — Discussion не создаёт артефактов в docs/.

### Шаг 7: Cross-chain проверка *(rollback-agent)*

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

### Шаг 8: Верификация и отчёт *(основной LLM)*

**Чек-лист верификации** (каждый пункт — идемпотентная проверка):

| # | Проверка | Команда | Ожидание |
|---|----------|---------|----------|
| 1 | Planned Changes | `grep -r "chain: {NNNN}" specs/docs/` | Пусто |
| 2 | Issues | `gh issue list --milestone {milestone} --state open` | Пусто |
| 3 | Ветка | `git ls-remote --heads origin {branch}` | Пусто |
| 4 | Заглушки | `{svc}.md` с `created-by: {NNNN}` | Не существуют |
| 5 | Per-tech | `standard-{tech}.md` введённые цепочкой | Не существуют |
| 6 | Docker | `Dockerfile.{svc}`, compose блок, init-db запись, .env переменные, .dockerignore | Удалены/отсутствуют |
| 7 | security-{tech}.md | `specs/docs/.technologies/security-{tech}.md` введённые цепочкой | Не существуют |
| 8 | labels.yml | `.github/labels.yml` секция SVC: строки `svc:{svc}` | Удалены/отсутствуют |
| 9 | docs/README.md | `specs/docs/README.md` строки новых сервисов | Удалены/отсутствуют |
| 10 | Milestone | `gh api repos/{owner}/{repo}/milestones` | Удалён/не содержит Issues цепочки |

Если проверка не пройдена — основной LLM исправляет сам (не перезапускает агента), затем переходит к следующей.

После прохождения всех проверок сформировать отчёт:

```
## Отчёт отката цепочки {NNNN}

### Изменённые файлы
| Файл | Что изменено |
|------|-------------|
| specs/analysis/{NNNN}-.../discussion.md | status: RUNNING → ROLLING_BACK |
| specs/analysis/{NNNN}-.../design.md | status: RUNNING → ROLLING_BACK, удалено docs-synced |
| platform/docker/docker-compose.yml | Удалены блоки сервисов: {svc1}, {svc2} |
| platform/docker/init-db.sql | Удалены: CREATE DATABASE myapp_{svc} |
| platform/docker/.env.example | Удалены переменные: {SVC}_DB_NAME, {SVC}_SERVICE_URL, ... |
| ... | ... |

### Удалённые файлы
| Файл | Причина |
|------|---------|
| specs/docs/{svc}.md | Сервис создан chain {NNNN} (created-by: {NNNN}) |
| specs/docs/.technologies/standard-{tech}.md | Технология введена chain {NNNN} |
| .claude/rules/{tech}.md | Rule введён chain {NNNN} |
| ... | ... |

### Итог
- Issues закрыты: #{N}, #{N+1}, ...
- Ветка удалена: {NNNN}-{name}
- Метки удалены: svc:{svc}, ...
- Cross-chain alerts: {список или "нет"}
- Ошибки: {список или "нет"}
```

### Шаг 9: Подтверждение пользователя *(основной LLM)*

Вызвать `AskUserQuestion`:

> «Отчёт отката цепочки {NNNN} выше. Подтверждаете перевод в статус REJECTED?»

Опции: «Да, перевести в REJECTED» / «Нет, остановиться».

Если пользователь отказался — цепочка остаётся в `ROLLING_BACK`, работа останавливается.

### Шаг 10: T10 (REJECTED) + README *(основной LLM)*

1. Выполнить:
```bash
python specs/.instructions/.scripts/chain_status.py transition {NNNN} REJECTED
```

2. Обновить frontmatter всех 4 документов: `status: ROLLING_BACK` → `status: REJECTED`

3. Обновить `specs/analysis/README.md` — строка цепочки {NNNN}: статус → REJECTED

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
| Удалить Docker Dockerfile | Файл не существует → skip | Безопасно |
| Удалить Docker compose блок | Блок не найден → skip | Безопасно |
| Удалить Docker init-db запись | Строка не найдена → skip | Безопасно |
| Удалить Docker .env переменные | Переменные не найдены → skip | Безопасно |
| Удалить Docker .dockerignore | Файл не существует → skip | Безопасно |
| Удалить строки docs/README.md | Строки отсутствуют → skip | Безопасно |
| Удалить строки labels.yml | Строки отсутствуют → skip | Безопасно |
| Удалить security-{tech}.md | Файл не существует → skip | Безопасно |
| Удалить/закрыть Milestone | Уже удалён/закрыт → skip | Безопасно |
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
- [ ] Design откачен (Planned Changes, заглушки, per-tech, метки, Docker scaffolding)
- [ ] Plan Tests откачен (testing.md)
- [ ] Discussion откачен (no-op)
- [ ] Cross-chain проверка выполнена

### Верификация и финализация
- [ ] Planned Changes отсутствуют в docs/
- [ ] Открытые Issues отсутствуют
- [ ] Feature-ветка удалена
- [ ] Заглушки удалены
- [ ] Per-tech файлы удалены
- [ ] Docker артефакты откатены
- [ ] Отчёт сформирован (изменённые + удалённые файлы)
- [ ] Пользователь подтвердил REJECTED (AskUserQuestion)
- [ ] T10 переход выполнен (→ REJECTED)
- [ ] specs/analysis/README.md обновлён

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

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/rollback-chain](/.claude/skills/rollback-chain/SKILL.md) | Оркестрация отката цепочки (5 фаз) | Этот документ |
