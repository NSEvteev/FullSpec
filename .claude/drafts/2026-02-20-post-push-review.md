# Чек-лист ревью после пушей f26c67e, 4b48e15

Коммиты: `f26c67e` (196 файлов), `4b48e15` (96 файлов) — оба в main.

Семь блоков изменений: стандарт веток v2.0, analysis-контур (фазы 6-9 SDD v2), очистка, багфикс, review-инфраструктура, review.md (сессия 2026-02-22), REVIEW статус + /dev (сессия 2026-02-24).

---

## 1. Стандарт ветвления v2.0 (сделано в этой сессии)

Замена `{type}/{description}-{issue-numbers}` на `{NNNN}-{description}`.

### Core — полностью переписаны

- [ ] `.github/.instructions/branches/standard-branching.md` — новый формат, убраны TYPE-таблица и Issue-обязательность
- [ ] `.github/.instructions/branches/create-branch.md` — шаги через analysis chain вместо Issues
- [ ] `.github/.instructions/branches/validation-branch.md` — новые BR001-BR006, убраны шаги 2-3 (Issues, TYPE-метки)
- [ ] `.github/.instructions/.scripts/validate-branch-name.py` — новый regex, убраны validate_issues/validate_labels
- [ ] `.claude/skills/branch-create/SKILL.md` — обновлены description, argument-hint, примеры

### Ссылки — точечные правки примеров

- [ ] `.github/.instructions/development/standard-development.md` — 3 правки
- [ ] `.github/.instructions/development/validation-development.md` — 1 правка
- [ ] `.github/.instructions/review/standard-review.md` — 3 правки
- [ ] `.github/.instructions/sync/standard-sync.md` — 2 правки
- [ ] `.github/.instructions/releases/standard-release.md` — 3 правки
- [ ] `.github/.instructions/issues/standard-issue.md` — 4 правки (lifecycle, assignees, связь с branch)
- [ ] `.github/.instructions/standard-github-workflow.md` — 2 правки
- [ ] `.github/.instructions/pull-requests/standard-pull-request.md` — 3 правки
- [ ] `CLAUDE.md` — убрана задача "пересмотреть стандарт веток"

---

## 2. Analysis-контур (фазы 6-9 SDD v2, сделано в предыдущих сессиях)

### Новые стандарты analysis/

- [ ] `specs/.instructions/analysis/standard-analysis.md` — мета-стандарт 4-уровневой цепочки
- [ ] `specs/.instructions/analysis/design/standard-design.md` — стандарт design.md
- [ ] `specs/.instructions/analysis/design/validation-design.md`
- [ ] `specs/.instructions/analysis/design/create-design.md`
- [ ] `specs/.instructions/analysis/design/modify-design.md`
- [ ] `specs/.instructions/analysis/discussion/standard-discussion.md` — обновлённый стандарт discussion.md
- [ ] `specs/.instructions/analysis/discussion/validation-discussion.md`
- [ ] `specs/.instructions/analysis/discussion/create-discussion.md`
- [ ] `specs/.instructions/analysis/discussion/modify-discussion.md`
- [ ] `specs/.instructions/analysis/plan-test/standard-plan-test.md` — стандарт plan-test.md
- [ ] `specs/.instructions/analysis/plan-test/validation-plan-test.md`
- [ ] `specs/.instructions/analysis/plan-test/create-plan-test.md`
- [ ] `specs/.instructions/analysis/plan-test/modify-plan-test.md`
- [ ] `specs/.instructions/analysis/plan-dev/standard-plan-dev.md` — стандарт plan-dev.md
- [ ] `specs/.instructions/analysis/plan-dev/validation-plan-dev.md`
- [ ] `specs/.instructions/analysis/plan-dev/create-plan-dev.md`
- [ ] `specs/.instructions/analysis/plan-dev/modify-plan-dev.md`

### Новые стандарты docs/

- [ ] `specs/.instructions/docs/testing/standard-testing.md` — стандарт testing.md
- [ ] `specs/.instructions/docs/testing/validation-testing.md`
- [ ] `specs/.instructions/docs/testing/modify-testing.md`
- [ ] `specs/.instructions/docs/service/standard-service.md` — стандарт {svc}.md
- [ ] `specs/.instructions/docs/service/validation-service.md`
- [ ] `specs/.instructions/docs/service/create-service.md`
- [ ] `specs/.instructions/docs/service/modify-service.md`
- [ ] `specs/.instructions/docs/technology/standard-technology.md` — стандарт standard-{tech}.md
- [ ] `specs/.instructions/docs/technology/validation-technology.md`
- [ ] `specs/.instructions/docs/technology/create-technology.md`
- [ ] `specs/.instructions/docs/technology/modify-technology.md`

### Новые скрипты валидации

- [ ] `specs/.instructions/.scripts/validate-analysis-design.py`
- [ ] `specs/.instructions/.scripts/validate-analysis-discussion.py`
- [ ] `specs/.instructions/.scripts/validate-analysis-plan-dev.py`
- [ ] `specs/.instructions/.scripts/validate-analysis-plan-test.py`
- [ ] `specs/.instructions/.scripts/validate-docs-service.py`
- [ ] `specs/.instructions/.scripts/validate-docs-technology.py`
- [ ] `specs/.instructions/.scripts/validate-docs-testing.py`
- [ ] `specs/.instructions/.scripts/validate-docs-readme-services.py`

### Новые скиллы

- [ ] `.claude/skills/plan-dev-create/SKILL.md`
- [ ] `.claude/skills/plan-dev-modify/SKILL.md`
- [ ] `.claude/skills/plan-dev-validate/SKILL.md`
- [ ] `.claude/skills/plan-test-create/SKILL.md`
- [ ] `.claude/skills/plan-test-modify/SKILL.md`
- [ ] `.claude/skills/plan-test-validate/SKILL.md`
- [ ] `.claude/skills/service-validate/SKILL.md`

### Обновлённые docs/ документы

- [ ] `specs/docs/.system/testing.md` — заполнен по новому стандарту
- [ ] `specs/docs/.system/conventions.md` — обновлён
- [ ] `specs/docs/.system/overview.md` — обновлён
- [ ] `specs/docs/.technologies/standard-example.md` — обновлён
- [ ] `specs/docs/example.md` — обновлён
- [ ] `specs/docs/README.md` — обновлён

### Обновлённые агенты

- [ ] `.claude/agents/design-agent/AGENT.md` — обновлён
- [ ] `.claude/agents/design-reviewer/AGENT.md` — обновлён

### Pre-commit hooks

- [ ] `.pre-commit-config.yaml` — 12 новых хуков (#12-#24)
- [ ] `.structure/pre-commit.md` — обновлён

---

## 3. Очистка

### Удалено (просто убедиться, что ничего нужного не пропало)

- [ ] `specs/_old/` — весь каталог (SDD v1 артефакты)
- [ ] `.claude/agents/impact-reviewer/` — агент (impact упразднён)
- [ ] `.claude/skills/impact-create/`, `impact-modify/`, `impact-validate/` — скиллы
- [ ] 13 черновиков + `maybe-archive/` — применённые драфты
- [ ] `.github/labels.yml` — убраны 15 строк (какие именно?)

---

## 4. Багфикс

- [ ] `specs/.instructions/.scripts/validate-docs-readme.py` — исключить EXCLUDED_FILES из table_files (RDM004)

---

## 5. Коммит 4b48e15 — review-инфраструктура и SSOT-ссылки

### Объединение review-скиллов

- [ ] `.claude/skills/review/SKILL.md` — **новый** единый скилл `/review` (заменил `/review-branch` + `/review-pr`)
- [ ] `.claude/skills/review-branch/SKILL.md` — **удалён**
- [ ] `.claude/skills/review-pr/SKILL.md` — **удалён**
- [ ] `.claude/skills/README.md` — убраны review-branch/review-pr, добавлен review

### Новый агент code-reviewer

- [ ] `.claude/agents/code-reviewer/AGENT.md` — **новый** агент (v1.0, type: general-purpose, model: sonnet, tools: Read/Grep/Glob/Bash)
- [ ] `.claude/agents/code-reviewer/CHANGELOG.md` — **новый**
- [ ] `.claude/.instructions/agents/README.md` — добавлен code-reviewer в реестр

### Обновления review-стандартов

- [ ] `.github/.instructions/review/standard-review.md` — добавлена ссылка на code-reviewer агента, уточнены 2 этапа (ветка vs PR)
- [ ] `.github/.instructions/review/validation-review.md` — добавлена ссылка на code-reviewer агента в секции "Скиллы"
- [ ] `.github/.instructions/review/README.md` — добавлен агент в описание

### Исправления SSOT-ссылок в analysis chain

- [ ] `specs/.instructions/analysis/standard-analysis.md` — исправлены внутренние ссылки на подстандарты
- [ ] `specs/.instructions/analysis/design/standard-design.md` — исправлены SSOT-ссылки (parent на standard-analysis)
- [ ] `specs/.instructions/analysis/design/create-design.md` — исправлена SSOT-ссылка
- [ ] `specs/.instructions/analysis/design/modify-design.md` — исправлена SSOT-ссылка
- [ ] `specs/.instructions/analysis/discussion/standard-discussion.md` — исправлены SSOT-ссылки
- [ ] `specs/.instructions/analysis/discussion/create-discussion.md` — исправлена SSOT-ссылка
- [ ] `specs/.instructions/analysis/discussion/validation-discussion.md` — исправлена SSOT-ссылка
- [ ] `specs/.instructions/analysis/plan-test/standard-plan-test.md` — исправлены SSOT-ссылки
- [ ] `specs/.instructions/analysis/plan-test/modify-plan-test.md` — исправлена SSOT-ссылка
- [ ] `specs/.instructions/analysis/plan-dev/standard-plan-dev.md` — исправлены SSOT-ссылки
- [ ] `specs/.instructions/analysis/plan-dev/modify-plan-dev.md` — исправлена SSOT-ссылка
- [ ] `specs/.instructions/analysis/plan-dev/validation-plan-dev.md` — исправлена SSOT-ссылка

### Исправления docs-стандартов

- [ ] `specs/.instructions/docs/service/standard-service.md` — исправлены ссылки
- [ ] `specs/.instructions/docs/technology/standard-technology.md` — исправлены ссылки
- [ ] `specs/.instructions/docs/testing/standard-testing.md` — исправлены ссылки

### Исправления скриптов валидации

- [ ] `specs/.instructions/.scripts/validate-analysis-discussion.py` — мелкое исправление
- [ ] `specs/.instructions/.scripts/validate-docs-overview.py` — убраны лишние проверки
- [ ] `specs/.instructions/.scripts/validate-docs-readme.py` — исправлена логика

---

## 6. Сессия 2026-02-22 — review.md инфраструктура

Создание review.md как артефакта SDD analysis chain. Черновик: `.claude/drafts/2026-02-22-review-document-design.md`

### Новые инструкции (specs/.instructions/analysis/review/)

- [ ] `specs/.instructions/analysis/review/standard-review.md` — **создан** — стандарт документа review.md (lifecycle, frontmatter, секции, шаблон)
- [ ] `specs/.instructions/analysis/review/validation-review.md` — **создан** — правила валидации RV001-RV015, чек-лист
- [ ] `specs/.instructions/analysis/review/create-review.md` — **создан** — воркфлоу создания review.md при Plan Dev → WAITING (8 шагов)

### Новые скиллы

- [ ] `.claude/skills/review-create/SKILL.md` — **создан** — `/review-create [ветка]`
- [ ] `.claude/skills/review-validate/SKILL.md` — **создан** — `/review-validate [путь] [--all]`

### Обновлённые скиллы

- [ ] `.claude/skills/review/SKILL.md` — **обновлён** — добавлен `Write` в allowed-tools, воркфлоу N+1 параллельных агентов, SSOT на standard-review.md
- [ ] `.claude/skills/README.md` — **обновлён** — добавлены review-create, review-validate в секцию specs

### Обновлённые агенты

- [ ] `.claude/agents/code-reviewer/AGENT.md` — **обновлён** v1.0→v2.0 — P1/P2/P3 вместо critical/warning/info, режим одного сервиса (--svc), RV-N формат вывода, Planned Changes (§ 9) + границы автономии (§ 8) в анализе
- [ ] `.claude/agents/code-reviewer/CHANGELOG.md` — **обновлён** — запись v2.0

### Prerequisite-проверка /review (задача #16)

- [ ] `.claude/skills/review/SKILL.md` — добавлен шаг 2 Prerequisite check: проверка plan-dev.md status перед запуском ревью (RUNNING → OK, WAITING/CONFLICT → СТОП, DONE → AskUserQuestion)

> Примечание: GitHub Issue-статусы (TASK-N → `gh issue view {N}`) — future design. Требуется скрипт check-issues-status.py и добавление предупреждающего шага 2.1 в /review (не блокирующего, P3 уровень).

### Обновлённые инструкции (.github/.instructions/review/)

- [ ] `.github/.instructions/review/standard-review.md` — **обновлён** — добавлена SSOT-ссылка на specs process, примечание в § 2 Этап 1
- [ ] `.github/.instructions/review/validation-review.md` — **обновлён** — severity `critical/warning/info` → P1/P2/P3, чтение review.md в Шаг 1, формат RV-N в Шаг 3, CONFLICT в вердикте
- [ ] `.github/.instructions/review/README.md` — **обновлён** — добавлен /review-create в Скиллы

### Новые скрипты

- [ ] `specs/.instructions/.scripts/validate-analysis-review.py` — **создан** — валидация review.md (RV001-RV015)
- [ ] `.github/.instructions/.scripts/validate-review.py` — **создан** — pre-commit хук (наличие, RESOLVED, итерации, READY)

### Хуки pre-commit

- [ ] `.pre-commit-config.yaml` — добавлен хук #26 `review-validate` (always_run)
- [ ] `.structure/pre-commit.md` — добавлена строка в таблицу активных хуков

### Реестр скриптов

- [ ] `specs/.instructions/README.md` — добавлены `validate-analysis-review.py`, `create-review-file.py`, `extract-svc-context.py` в дерево и таблицу
- [ ] `specs/.instructions/.scripts/create-review-file.py` — **создан** — генерация пустого review.md по шаблону (frontmatter + Контекст ревью)
- [ ] `specs/.instructions/.scripts/extract-svc-context.py` — **создан** — парсинг SVC-N из design.md: список сервисов, затронутые §§, технологии

### Обновлённый standard-analysis.md

- [ ] `specs/.instructions/analysis/standard-analysis.md` — **обновлён** — 6 изменений: review.md в § 2.2 (таблица), § 2.5 (расширяемость), § 6.3 (источники CONFLICT), § 9 (дерево), § 11 (стандарты), § 12 (решения 38-39)

### Обновлённая документация

- [ ] `specs/.instructions/README.md` — **обновлён** — добавлен validate-analysis-review.py в таблицу скриптов
- [ ] `specs/analysis/README.md` — **создан** — индекс цепочек NNNN-{topic} с review.md
- [ ] `specs/README.md` — **обновлён** — review.md как артефакт в таблице analysis chain, tree

---

## 7. Сессия 2026-02-24 — REVIEW статус + /dev скилл

Два драфта: `2026-02-24-review-status-integration.md` (Phase 1) и `2026-02-24-dev-skill.md` (Phase 2).

### Phase 1: REVIEW как 8-й статус (review-status-integration)

#### Центральный стандарт

- [ ] `specs/.instructions/analysis/standard-analysis.md` — 8 статусов, новый § 6.5 RUNNING→REVIEW, перенумерация §§ 6.6-6.8, обновление § 4.1 шаг 5 (/dev), § 6.2 (/dev воркфлоу)

#### Per-object standard-*.md (4 файла)

- [ ] `specs/.instructions/analysis/discussion/standard-discussion.md` — split RUNNING→DONE на RUNNING→REVIEW + REVIEW→DONE
- [ ] `specs/.instructions/analysis/design/standard-design.md` — аналогично
- [ ] `specs/.instructions/analysis/plan-test/standard-plan-test.md` — аналогично
- [ ] `specs/.instructions/analysis/plan-dev/standard-plan-dev.md` — 8 статусов, split переходов, «Следующий шаг после WAITING», /review-create

#### Per-object modify-*.md (4 файла)

- [ ] `specs/.instructions/analysis/discussion/modify-discussion.md` — TOC, таблица, RUNNING→REVIEW + REVIEW→DONE, §§ 6.x
- [ ] `specs/.instructions/analysis/design/modify-design.md` — аналогично
- [ ] `specs/.instructions/analysis/plan-test/modify-plan-test.md` — аналогично
- [ ] `specs/.instructions/analysis/plan-dev/modify-plan-dev.md` — аналогично + AskUserQuestion /dev при DRAFT→WAITING и CONFLICT→WAITING

#### Per-object validation-*.md (4 файла)

- [ ] `specs/.instructions/analysis/discussion/validation-discussion.md` — REVIEW в статусах (2 места)
- [ ] `specs/.instructions/analysis/design/validation-design.md` — аналогично
- [ ] `specs/.instructions/analysis/plan-test/validation-plan-test.md` — аналогично
- [ ] `specs/.instructions/analysis/plan-dev/validation-plan-dev.md` — аналогично

#### create-plan-dev.md

- [ ] `specs/.instructions/analysis/plan-dev/create-plan-dev.md` — шаг 10 /review-create, шаг 12 AskUserQuestion /dev, перенумерация

#### review/ (3 файла)

- [ ] `specs/.instructions/analysis/review/standard-review.md` — lifecycle (REVIEW tree-level), § 3 frontmatter (REVIEW в chain status), § 5.2 (итерации при REVIEW)
- [ ] `specs/.instructions/analysis/review/create-review.md` — пояснение: итерации при REVIEW
- [ ] `specs/.instructions/analysis/review/validation-review.md` — без изменений (подтверждено)

### Phase 2: /dev скилл + /analysis-status (dev-skill)

#### Изменённые файлы

- [ ] `.github/.instructions/development/standard-development.md` — новая § 0 «Запуск разработки», SSOT-зависимость create-dev.md, предусловие в § 2
- [ ] `specs/.instructions/analysis/plan-dev/create-plan-dev.md` — шаг 12 AskUserQuestion /dev (дополнение к Phase 1)
- [ ] `specs/.instructions/analysis/plan-dev/modify-plan-dev.md` — AskUserQuestion /dev при DRAFT→WAITING и CONFLICT→WAITING (дополнение к Phase 1)
- [ ] `specs/.instructions/analysis/plan-dev/standard-plan-dev.md` — § 4 «Следующий шаг после WAITING», § 1 маппинг Issues (дополнение к Phase 1)
- [ ] `specs/.instructions/analysis/standard-analysis.md` — § 4.1 шаг 5 /dev, § 6.2 /dev (дополнение к Phase 1)
- [ ] `.github/.instructions/standard-github-workflow.md` — стадия 0, blockquote в § 3

#### Новые файлы

- [ ] `.github/.instructions/development/create-dev.md` — **создан** — воркфлоу /dev (делегат к § 0). **⚠️ Не прошёл валидацию (I022, I027) → драфт 2026-02-24-create-dev-rework.md**
- [ ] `.claude/skills/dev/SKILL.md` — **создан** — скилл /dev (исправлен: добавлен frontmatter, Чек-лист, Примеры)
- [ ] `specs/.instructions/.scripts/analysis-status.py` — **создан** — скрипт статусов цепочек (✅ валидация пройдена)
- [ ] `.claude/skills/analysis-status/SKILL.md` — **создан** — скилл /analysis-status (исправлен: добавлен frontmatter, Чек-лист, Примеры)

#### README регистрация

- [ ] `.github/.instructions/development/README.md` — добавлен create-dev.md
- [ ] `.claude/skills/README.md` — добавлены /dev и /analysis-status
- [ ] `specs/.instructions/README.md` — добавлен analysis-status.py
- [ ] `specs/analysis/README.md` — dashboard статусов (маркеры BEGIN/END)

---

## Как ревьюить

1. **Приоритет 1:** Блок 1 (ветвление) — полностью новый контент
2. **Приоритет 2:** Блок 5 (code-reviewer + unified /review) — новые артефакты
3. **Приоритет 3:** Блок 2 standard-*.md — ключевые стандарты, определяющие формат документов
4. **Приоритет 4:** Блок 2 скрипты — автоматическая валидация
5. **Приоритет 5:** Блок 5 SSOT-ссылки — массовые исправления ссылок в analysis chain
6. **Приоритет 6:** Блок 3 — убедиться что ничего нужного не удалено
