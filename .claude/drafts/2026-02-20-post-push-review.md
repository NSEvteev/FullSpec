# Чек-лист ревью после пушей f26c67e, 4b48e15

Коммиты: `f26c67e` (196 файлов), `4b48e15` (96 файлов) — оба в main.

Пять блоков изменений: стандарт веток v2.0, analysis-контур (фазы 6-9 SDD v2), очистка, багфикс, review-инфраструктура.

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

## Как ревьюить

1. **Приоритет 1:** Блок 1 (ветвление) — полностью новый контент
2. **Приоритет 2:** Блок 5 (code-reviewer + unified /review) — новые артефакты
3. **Приоритет 3:** Блок 2 standard-*.md — ключевые стандарты, определяющие формат документов
4. **Приоритет 4:** Блок 2 скрипты — автоматическая валидация
5. **Приоритет 5:** Блок 5 SSOT-ссылки — массовые исправления ссылок в analysis chain
6. **Приоритет 6:** Блок 3 — убедиться что ничего нужного не удалено
