# Карта процесса «от идеи до деплоя»

Справочная карта покрытия процесса инструментами проекта.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Закрытые пробелы](#закрытые-пробелы-сессия-2026-02-24)
- [Оставшиеся пробелы](#оставшиеся-пробелы)

---

## Контекст

**Задача:** Зафиксировать, какие шаги процесса разработки покрыты скиллами, агентами, хуками и правилами.

**Покрытие:** ~94% шагов имеют хотя бы один инструмент (15 из 16).

**Связанные файлы:** `.claude/skills/README.md`, `.claude/agents/`, `.pre-commit-config.yaml`, `.claude/rules/`

---

## Содержание

### Карта процесса (16 шагов)

| Шаг | Этап | Скилл | Агент | Pre-commit | Rule | chain_status.py |
|-----|------|-------|-------|-----------|------|-----------------|
| 1 | Discussion | /discussion-create, /discussion-modify | discussion-reviewer (опц) | discussion-validate | core, analysis-status-transition | T1 (DRAFT→WAITING) |
| 2 | Design | /design-create, /design-modify | design-agent (обяз), design-reviewer (опц) | design-validate | core, analysis-status-transition | T1 |
| 3 | Plan Tests | /plan-test-create, /plan-test-modify | ❌ нет | plan-test-validate | core, analysis-status-transition | T1 |
| 4 | Plan Dev + Review Create | /plan-dev-create, /review-create | ❌ нет | plan-dev-validate, review-validate | core, analysis-status-transition | T1 |
| 5 | WAITING→RUNNING (Issues+Milestone+Branch) | /dev-create | ❌ нет | branch-validate, type-templates-validate | development, analysis-status-transition | T3 |
| 6 | Development | /dev, /principles-validate | ❌ нет | (make test/lint) | development, code | classify_feedback() |
| 7 | Branch Review | /review | code-reviewer (per-svc) | review-validate | development | — |
| 8 | Commits | ❌ нет скилла | ❌ нет | 24 хука | development, core | — |
| 9 | PR Create | ❌ нет скилла | ❌ нет | pr-template-validate | development, core | — |
| 10 | PR Review | /review {N} | code-reviewer (per-svc) | ❌ нет | development | — |
| 11 | Merge | ❌ нет скилла | ❌ нет | ❌ нет | development | — |
| 12 | RUNNING→REVIEW→DONE + docs/ update | /analysis-status | ❌ нет | service-validate, docs-validate | analysis-status-transition | T6, T7, check_cross_chain() |
| 13 | Sync main | ❌ нет скилла | ❌ нет | ❌ нет | development | — |
| 14 | Release+Deploy | /milestone-validate | ❌ нет | actions-validate | development, core | — |
| 15 | CONFLICT resolution | /discussion-modify → /plan-dev-modify | ❌ нет | *-validate | analysis-status-transition | T4/T8, T5 |
| 16 | Rollback/Reject | ❌ нет скилла | ❌ нет | ❌ нет | analysis-status-transition | T9, T10 |

---

## Закрытые пробелы (сессия 2026-02-24)

| Пробел | Решение |
|--------|---------|
| ~~WAITING→RUNNING~~ | `/dev-create` — Issues, Milestone, Branch, `ChainManager.transition(to="RUNNING")` |
| ~~DONE + docs/ update~~ | `ChainManager.transition(to="DONE")` — T7 bottom-up каскад, `side_effects` для обновления docs/ |
| ~~Нет модуля статусов~~ | `chain_status.py` — SSOT для T1-T10, prerequisites, каскады, cross-chain |
| ~~Нет /dev скилла~~ | `/dev-create` + `/dev` — запуск и процесс разработки |

## Оставшиеся пробелы

| Пробел | Приоритет | Что нужно |
|--------|-----------|-----------|
| Шаг 11: Merge | Низкий | Нет скилла — ручной процесс, покрыт стандартом |
| Шаг 14: Release | Средний | /release-create — по standard-release.md |
| Шаг 16: Rollback | Низкий | Нет скилла — chain_status.py T9/T10 управляет статусами, но откат артефактов ручной по modify-* инструкциям |
| Агенты: разработка | Низкий (Q11) | developer-agent — реализация TASK-N. Отложено до первого реального прогона цепочки |
