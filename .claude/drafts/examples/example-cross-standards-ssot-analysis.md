# SSOT-рефакторинг стандартов

Инструкция по устранению дублирования между стандартами.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [Статус решений](#статус-решений)
  - [M1: Координация агентов](#m1-координация-агентов)
  - [M2: Frontmatter агентов](#m2-frontmatter-агентов)
  - [M3: Версионирование](#m3-версионирование)
  - [Порядок выполнения](#порядок-выполнения)
  - [Чек-лист](#чек-лист)

---

## Контекст

**Задача:** Устранить дублирование между 11 стандартами в `.instructions/`, `.structure/`, `.claude/`.

**Проблема:** `standard-agent.md` дублирует контент из `standard-state.md` и `standard-frontmatter.md`.

**Файлы для изменения:**
- `/.claude/.instructions/agents/standard-agent.md`
- `/.structure/.instructions/standard-frontmatter.md`

---

## Содержание

### Статус решений

Все решения утверждены (2026-02-03):

| Проблема | Решение |
|----------|---------|
| Координация агентов | Удалить ~80 строк из standard-agent.md, оставить SSOT-ссылку |
| Frontmatter агентов | Разделить: базовые поля в frontmatter, специфичные (name + version) — в agent |
| Версионирование | Добавить clarification standard-version vs version |

---

### M1: Координация агентов

**Файл:** `/.claude/.instructions/agents/standard-agent.md`
**SSOT:** `/.claude/.instructions/state/standard-state.md`

**Удалить строки 490-589** (секция "Координация между агентами") — ~80 строк.

**Заменить на:**

```markdown
### Координация между агентами

> **SSOT:** [standard-state.md](../state/standard-state.md)

Агенты координируются через файлы состояния в `/.claude/state/`. Полное описание форматов и алгоритмов — в SSOT.

#### Автоматизация через хуки

| Хук | Действие |
|-----|----------|
| `SubagentStart` | Регистрирует агента в `agents-status.json` (status: running) |
| `SubagentStop` | Обновляет статус + cleanup блокировок |

**Что остаётся на агенте:**

> **Чек-лист координации:**
> - [ ] Проверять `locks.json` перед записью
> - [ ] Снимать блокировку сразу после операции (даже при ошибке!)
> - [ ] Вести лог в `agent-{name}-operation.json`
>
> Детали и алгоритмы: [standard-state.md](../state/standard-state.md)
```

---

### M2: Frontmatter агентов

#### M2a: standard-frontmatter.md § 3

**Файл:** `/.structure/.instructions/standard-frontmatter.md`

**Заменить § 3 на:**

```markdown
## 3. Дополнительные поля для агентов

> **Базовые поля** (`description`, `standard`, `standard-version`, `index`) — см. [§ 1](#1-обязательные-поля).

Агенты расширяют базовые поля frontmatter специфичными полями.

**SSOT специфичных полей:** [standard-agent.md § 3](/.claude/.instructions/agents/standard-agent.md#3-формат-конфигурации)

**Обязательные специфичные поля агента:**

| Поле | Назначение | Пример |
|------|------------|--------|
| `name` | Уникальное имя агента (kebab-case, латиница) | `code-reviewer` |
| `version` | Версия агента | `v1.0` |

**Опциональные поля:** `model`, `tools`, `hooks` — см. SSOT.
```

#### M2b: standard-agent.md § 3.2

**Файл:** `/.claude/.instructions/agents/standard-agent.md`

**Заменить § 3.2 (Обязательные поля) на:**

```markdown
### Обязательные поля

> **Базовые поля frontmatter:** [standard-frontmatter.md § 1](/.structure/.instructions/standard-frontmatter.md#1-обязательные-поля)

Агенты расширяют базовые поля frontmatter двумя обязательными полями:

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | string | Уникальное имя агента (kebab-case, латиница) |
| `version` | string | Версия агента (формат: `vX.Y`, например `v1.0`) |

Поля `description`, `standard`, `standard-version`, `index` — обязательны, см. SSOT базовых полей.
```

---

### M3: Версионирование

**Файл:** `/.structure/.instructions/standard-frontmatter.md`

**Добавить после § 1 (после описания `standard-version`):**

```markdown
> **Примечание: версия стандарта vs версия объекта**
>
> | Поле | Назначение | Где описано |
> |------|------------|-------------|
> | `standard-version` | Версия стандарта формата | Этот документ |
> | `version` | Версия самого объекта (агент) | standard-agent.md |
>
> Это разные поля с разным назначением. Не путать!
```

---

### Порядок выполнения

1. **M1** — Удалить дублирование координации в standard-agent.md
2. **M2a** — Обновить § 3 в standard-frontmatter.md
3. **M2b** — Обновить § 3.2 в standard-agent.md
4. **M3** — Добавить clarification в standard-frontmatter.md
5. **Валидация** — `/links-validate` для обоих файлов
6. **Миграция** — `/migration-create` для обновлённых стандартов

---

### Чек-лист

- [x] M1: standard-agent.md — координация сокращена (~80 строк удалено)
- [x] M2a: standard-frontmatter.md § 3 — name + version как обязательные
- [x] M2b: standard-agent.md § 3.2 — удалены дубли базовых полей
- [x] M3: standard-frontmatter.md — clarification версий
- [x] `/links-validate` прошёл
- [ ] `/migration-create` выполнен
