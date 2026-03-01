---
description: Предложение убрать бинарный вердикт ACCEPT/REVISE из ревьюеров — все замечания обязательны к исправлению.
status: active
---

# Убрать ACCEPT/REVISE — все замечания обязательны

## Проблема

Сейчас ревьюеры (service-reviewer, technology-reviewer, system-reviewer) возвращают бинарный вердикт:
- **ACCEPT** — нет расхождений, документ готов
- **REVISE** — есть расхождения, нужны исправления

При этом technology-reviewer дополнительно делит на:
- **MUST FIX** — блокирует (вердикт REVISE)
- **NICE TO HAVE** — не блокирует (вердикт может быть ACCEPT)

### Проблемы текущего подхода

1. **NICE TO HAVE теряются** — если вердикт ACCEPT, оркестратор может пропустить NICE TO HAVE
2. **Мелкие FORMAT-замечания** (stub-подсекции, H3 вместо абзаца) — формально не блокируют, но ухудшают качество
3. **Бинарность** создаёт ложное ощущение "готовности" при ACCEPT — хотя замечания могут быть

## Предложение

### Для service-reviewer и system-reviewer

**Было:** ACCEPT / REVISE
**Стало:** Всегда возвращать список замечаний (может быть пустой). Каждое замечание = обязательное исправление.

Формат вывода:
```markdown
## Ревью {svc}.md — {N} замечаний

| # | Тип | Секция | В источнике | В документе | Исправление |
|---|-----|--------|-------------|-------------|-------------|
| 1 | MISSING | § 7 | ... | — | Добавить ... |
| 2 | FORMAT | § 6 | standard-service.md: ... | ... | Привести к формату ... |

Если таблица пуста — замечаний нет, документ готов.
```

### Для technology-reviewer

**Было:** MUST FIX (блокирует) / NICE TO HAVE (не блокирует) → ACCEPT / REVISE
**Стало:** Единый уровень — все замечания обязательны. Без деления на MUST FIX / NICE TO HAVE.

### Для оркестратора (create-docs-sync.md)

**Было:** Wave 2 → собрать вердикты → если REVISE → Wave 3 (исправления) → повторный ревью
**Стало:** Wave 2 → собрать замечания → если есть хоть одно → Wave 3 (исправления) → повторный ревью

Логика не меняется, меняется только триггер: `verdict == REVISE` → `len(findings) > 0`.

## Затронутые файлы

| Файл | Что изменить |
|------|-------------|
| `.claude/agents/service-reviewer/AGENT.md` | Убрать ACCEPT/REVISE, новый формат вывода |
| `.claude/agents/technology-reviewer/AGENT.md` | Убрать MUST FIX / NICE TO HAVE, единый уровень |
| `.claude/agents/system-reviewer/AGENT.md` | Убрать ACCEPT/REVISE, новый формат вывода |
| `.claude/agents/design-reviewer/AGENT.md` | Аналогично (если есть ACCEPT/REVISE) |
| `.claude/agents/plantest-reviewer/AGENT.md` | Аналогично |
| `.claude/agents/plandev-reviewer/AGENT.md` | Аналогично |
| `.claude/agents/discussion-reviewer/AGENT.md` | Аналогично |
| `specs/.instructions/create-docs-sync.md` | Шаг 5-6: изменить логику с вердикта на кол-во замечаний |

## Не затронуто

- Максимум 3 итерации Wave 3 — остаётся
- Эскалация пользователю после 3-й итерации — остаётся
- Типы расхождений (MISSING/INVENTED/DISTORTED/FORMAT) — остаются (это классификация, не приоритет)
