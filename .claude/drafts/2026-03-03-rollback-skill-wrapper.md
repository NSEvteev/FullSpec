# Скилл-обёртка для rollback-agent

Создание `/rollback-chain` скилла, который оркестрирует rollback-agent с правильными переходами статусов, валидацией артефактов и обновлением README.

## Оглавление

- [Контекст](#контекст)
- [Проблема](#проблема)
- [Решение](#решение)
- [Содержание](#содержание)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** Обернуть rollback-agent в скилл с оркестрацией — статусы, валидация, README
**Почему создан:** При тестовом прогоне chain 0001 rollback-agent: (1) сразу поставил REJECTED минуя ROLLING_BACK, (2) не откатил platform/docker файлы, (3) не обновил specs/analysis/README.md
**Связанные файлы:**
- `specs/.instructions/create-rollback.md` — SSOT инструкции rollback-agent
- `.claude/agents/rollback-agent/AGENT.md` — конфигурация агента
- `.claude/skills/` — папка скиллов

---

## Проблема

Текущий флоу:

```
пользователь → /rollback → rollback-agent (делает всё сам)
```

Баги, обнаруженные при прогоне 0001:

1. **Преждевременный REJECTED** — агент ставил REJECTED не дождавшись завершения всех шагов. Должно быть: RUNNING → ROLLING_BACK (сразу) → REJECTED (после валидации).
2. **Пропущены docker-артефакты** — `platform/docker/` не был откатен (docker-compose.yml, init-db.sql, .env.example, .env.test).
3. **specs/analysis/README.md не обновлён** — статус цепочки в README не синхронизируется.
4. **Нет валидации** — после агента никто не проверяет что все артефакты действительно удалены.

---

## Решение

Новый флоу:

```
пользователь → /rollback-chain скилл →
  1. Основной LLM: RUNNING → ROLLING_BACK (в frontmatter + chain_status.py)
  2. rollback-agent (откат артефактов)
  3. Основной LLM: валидация + отчёт (изменённые/удалённые файлы)
  4. Основной LLM: AskUserQuestion "Подтверждаете переход цепочки NNNN в REJECTED?"
  5. Основной LLM: ROLLING_BACK → REJECTED + обновить specs/analysis/README.md
```

Ключевой принцип: **статусные переходы делает основной LLM**, агент только откатывает артефакты.

---

## Содержание

### Шаг 1 — Переход RUNNING → ROLLING_BACK (основной LLM)

До вызова агента основной LLM:

1. Читает все 4 frontmatter (discussion/design/plan-test/plan-dev)
2. Меняет `status: RUNNING` → `status: ROLLING_BACK` в каждом
3. Запускает `chain_status.py transition {NNNN} ROLLING_BACK`

### Шаг 2 — rollback-agent

Вызывается с полным контекстом: номер цепочки, список сервисов, список per-tech технологий, флаг `docs-synced`.

Агент работает по `create-rollback.md` — откатывает артефакты согласно чек-листу (Issues, ветка, заглушки, per-tech, docker, labels).

### Шаг 3 — Валидация (основной LLM)

После завершения агента основной LLM проходит по чек-листу `create-rollback.md § Верификация`:

| # | Проверка | Команда |
|---|---------|---------|
| 1 | Issues закрыты | `gh issue list --milestone {M} --state open` |
| 2 | Ветка удалена | `git branch --list {NNNN}-*` |
| 3 | Заглушки удалены | `ls specs/docs/{svc}.md` для каждого сервиса |
| 4 | Per-tech удалены | `ls specs/docs/.technologies/standard-{tech}.md` |
| 5 | Docker откатен | проверить compose/init-db/.env на наличие svc-блоков |
| 6 | Labels удалены | `gh label list` |
| 7 | docs-synced сброшен | читать frontmatter design.md |

Если какая-то проверка не прошла — основной LLM исправляет сам (не перезапускает агента).

После прохождения всех проверок — сформировать **отчёт об откате**:

```
## Отчёт отката цепочки NNNN

### Изменённые файлы
| Файл | Что изменено |
|------|-------------|
| specs/analysis/NNNN-.../design.md | status: RUNNING → ROLLING_BACK |
| platform/docker/docker-compose.yml | Удалены блоки сервисов {svc} |
| platform/docker/init-db.sql | Удалены CREATE DATABASE myapp_{svc} |
| ... | ... |

### Удалённые файлы
| Файл | Причина |
|------|---------|
| specs/docs/{svc}.md | Сервис создан chain NNNN (created-by: NNNN) |
| specs/docs/.technologies/standard-{tech}.md | Технология введена chain NNNN |
| .claude/rules/{tech}.md | Rule введён chain NNNN |
| ... | ... |

### Issues закрыты: #N, #N+1, ...
### Ветка удалена: NNNN-{name}
### Метки удалены: svc:{svc}, ...
```

### Шаг 4 — Подтверждение (AskUserQuestion)

Основной LLM вызывает `AskUserQuestion`:

> «Отчёт об откате выше. Подтверждаете перевод цепочки {NNNN} в статус REJECTED?»

Опции: «Да, перевести в REJECTED» / «Нет, остановиться».

Если пользователь отказался — цепочка остаётся в `ROLLING_BACK`, работа останавливается.

### Шаг 5 — Финализация (основной LLM)

1. `chain_status.py transition {NNNN} REJECTED`
2. Меняет `status: ROLLING_BACK` → `status: REJECTED` в frontmatter всех 4 документов
3. Обновляет `specs/analysis/README.md` — строка цепочки меняет статус на REJECTED

### Скилл SKILL.md

```
/rollback-chain <NNNN>
```

SSOT: `specs/.instructions/create-rollback.md` (расширить новым воркфлоу).

Скилл не вызывает агента напрямую — он даёт основному LLM инструкцию пройти все 5 фаз последовательно.

### Изменения в create-rollback.md

Добавить новую секцию **§ Оркестрация** перед текущим § Шаги:

```markdown
## Оркестрация

Rollback выполняется в 5 фаз. Фазы 1, 3, 4, 5 — основной LLM. Фаза 2 — rollback-agent.

| Фаза | Исполнитель | Действие |
|------|------------|---------|
| 1 | Основной LLM | RUNNING → ROLLING_BACK |
| 2 | rollback-agent | Откат артефактов |
| 3 | Основной LLM | Валидация + отчёт (изменённые/удалённые файлы) |
| 4 | Основной LLM | AskUserQuestion — подтверждение REJECTED |
| 5 | Основной LLM | ROLLING_BACK → REJECTED + README |
```

### Изменения в rollback-agent/AGENT.md

Убрать из scope агента:
- Переход статусов (это делает основной LLM)
- Обновление specs/analysis/README.md

Добавить в scope агента:
- Явный список docker-артефактов для отката (Dockerfile.{svc}, compose блок, init-db, .env)

---

## Tasklist

TASK 1: Обновить `specs/.instructions/create-rollback.md` — добавить § Оркестрация (5 фаз), шаблон отчёта, AskUserQuestion перед REJECTED
Секция: [Шаг 1](#шаг-1--переход-running--rolling_back-основной-llm), [Шаг 3](#шаг-3--валидация-основной-llm), [Шаг 4](#шаг-4--подтверждение-askuserquestion), [Шаг 5](#шаг-5--финализация-основной-llm)
activeForm: Обновляя create-rollback.md

TASK 2: Обновить `.claude/agents/rollback-agent/AGENT.md` — убрать статусные переходы и README из scope, добавить явный список docker-артефактов
Секция: [Шаг 2](#шаг-2--rollback-agent), [Изменения в rollback-agent](#изменения-в-rollback-agentmd)
activeForm: Обновляя rollback-agent/AGENT.md
blockedBy: TASK 1

TASK 3: Создать `/rollback-chain` скилл (`skills/rollback-chain/SKILL.md`) с SSOT-ссылкой на обновлённый create-rollback.md
Секция: [Скилл SKILL.md](#скилл-skillmd)
activeForm: Создавая /rollback-chain скилл
blockedBy: TASK 1

TASK 4: Протестировать на chain 0001 — вручную пройти новый воркфлоу
activeForm: Тестируя воркфлоу
blockedBy: TASK 3
