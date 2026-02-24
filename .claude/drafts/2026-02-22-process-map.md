# Карта процесса «от идеи до деплоя»

Справочная карта покрытия процесса инструментами проекта.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Пробелы](#пробелы)

---

## Контекст

**Задача:** Зафиксировать, какие шаги процесса разработки покрыты скиллами, агентами, хуками и правилами.

**Покрытие:** ~85% шагов имеют хотя бы один инструмент.

**Связанные файлы:** `.claude/skills/README.md`, `.claude/agents/`, `.pre-commit-config.yaml`, `.claude/rules/`

---

## Содержание

### Карта процесса (18 шагов)

| Шаг | Этап | Скилл | Агент | Pre-commit | Rule |
|-----|------|-------|-------|-----------|------|
| 1 | Discussion | /discussion-create | discussion-reviewer (опц) | discussion-validate | core, specs-analysis |
| 2 | Design | /design-create | design-agent (обяз), design-reviewer (опц) | design-validate | core, specs-analysis |
| 3 | Plan Tests | /plan-test-create | ❌ нет | plan-test-validate | core, specs-analysis |
| 4 | Plan Dev | /plan-dev-create | ❌ нет | plan-dev-validate | core, specs-analysis |
| 5 | WAITING→RUNNING | ❌ нет скилла | ❌ нет | ❌ нет | specs-analysis |
| 6 | Issues+Milestone | /issue-create, /milestone-create | ❌ нет | type-templates-validate | development, core |
| 7 | Branch | /branch-create | ❌ нет | branch-validate | development, core |
| 8 | Development | /principles-validate | ❌ нет | (make test/lint) | development, code |
| 9 | Review Create (Plan Dev → WAITING) | /review-create | ❌ нет | ❌ нет | development |
| 10 | Branch Review | /review (N+1 агентов → ## Итерация 1 в review.md) | code-reviewer (per-svc) | review-validate | development |
| 11 | Commits | ❌ нет скилла | ❌ нет | 24 хука | development, core |
| 12 | PR Create | ❌ нет скилла | ❌ нет | pr-template-validate | development, core |
| 13 | PR Review | /review {N} (N+1 агентов → ## Итерация 2 + gh pr comment) | code-reviewer (per-svc) | ❌ нет | development |
| 14 | Merge | ❌ нет скилла | ❌ нет | ❌ нет | development |
| 15 | DONE + docs/ update | ❌ нет скилла | ❌ нет | service-validate, docs-validate | specs-analysis |
| 16 | Sync main | ❌ нет скилла | ❌ нет | ❌ нет | development |
| 17 | Release+Deploy | /milestone-validate | ❌ нет | actions-validate | development, core |
| 18 | Hotfix/Rollback | ❌ нет скилла | ❌ нет | ❌ нет | development |

---

## Пробелы

Скиллы с наибольшим приоритетом для создания:

| Пробел | Приоритет | Что нужно |
|--------|-----------|-----------|
| Шаг 5: WAITING→RUNNING | Высокий | /analysis-run — переводит plan-dev.md в RUNNING, фиксирует дату старта |
| Шаг 15: DONE + docs/ update | Высокий | /analysis-complete — каскад DONE, обновление docs/ по Planned Changes |
| Шаг 17: Release | Средний | /release-create — по standard-release.md |
| Агенты: разработка | Низкий | developer-agent — реализация TASK-N (автономная разработка) |
