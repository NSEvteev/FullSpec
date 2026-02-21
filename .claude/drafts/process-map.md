ВАЖНЕЙШЕЕ ЗАМЕЧАНИЕ:
Нужно создать отдельный драфт с полной картой процесса "от идеи до деплоя". Предварительный анализ выявил 17 шагов.

Покрытие процесса (~85%):
| Шаг | Этап | Скилл | Агент | Pre-commit | Rule |
|-----|------|-------|-------|-----------|------|
| 1 | Discussion | /discussion-create | discussion-reviewer (опц) | ❌ нет хука | core, specs-analysis |
| 2 | Design | /design-create | design-agent (обяз), design-reviewer (опц) | design-validate | core, specs-analysis |
| 3 | Plan Tests | /plan-test-create | ❌ нет | plan-test-validate | core, specs-analysis |
| 4 | Plan Dev | /plan-dev-create | ❌ нет | plan-dev-validate | core, specs-analysis |
| 5 | WAITING→RUNNING | ❌ нет скилла | ❌ нет | ❌ нет | specs-analysis |
| 6 | Issues+Milestone | /issue-create, /milestone-create | ❌ нет | type-templates-validate | development, core |
| 7 | Branch | /branch-create | ❌ нет | branch-validate | development, core |
| 8 | Development | /principles-validate | ❌ нет | (make test/lint) | development, code |
| 9 | Commits | ❌ нет скилла | ❌ нет | 24 хука | development, core |
| 10 | Branch Review | /review | code-reviewer | ❌ нет | development |
| 11 | PR Create | ❌ нет скилла | ❌ нет | pr-template-validate | development, core |
| 12 | PR Review | /review {N} | code-reviewer | ❌ нет | development, code |
| 13 | Merge | ❌ нет скилла | ❌ нет | ❌ нет | development |
| 14 | DONE + docs/ update | ❌ нет скилла | ❌ нет | service-validate, docs-validate | specs-analysis |
| 15 | Sync main | ❌ нет скилла | ❌ нет | ❌ нет | development |
| 16 | Release+Deploy | /milestone-validate | ❌ нет | actions-validate | development, core |
| 17 | Hotfix/Rollback | ❌ нет скилла | ❌ нет | ❌ нет | development |

Ключевые пробелы:
- Скиллы: нет /analysis-run (WAITING→RUNNING), /analysis-complete (каскад DONE), /release-create
- Агенты: нет developer-agent (реализация Tasks). code-reviewer создан
- Pre-commit: нет discussion-validate хука (скрипт есть, хук не добавлен в конфиг)
