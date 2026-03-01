---
description: Воркфлоу создания review.md с секцией Контекст ревью — вызывается при Plan Dev → WAITING.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу создания ревью

Рабочая версия стандарта: 1.2

Пошаговый процесс создания документа `review.md` при переходе Plan Dev → WAITING.

**Полезные ссылки:**
- [Стандарт ревью](./standard-review.md)
- [Валидация ревью](./validation-review.md)
- [Инструкции specs/](../../README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-review.md](./standard-review.md) |
| Валидация | [validation-review.md](./validation-review.md) |
| Создание | Этот документ |
| Модификация | *Не требуется* |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить условия запуска](#шаг-1-проверить-условия-запуска)
  - [Шаг 2: Идемпотентность](#шаг-2-идемпотентность)
  - [Шаг 3: Создать файл из шаблона](#шаг-3-создать-файл-из-шаблона)
  - [Шаг 4: Заполнить frontmatter](#шаг-4-заполнить-frontmatter)
  - [Шаг 5: Извлечь контекст сервисов](#шаг-5-извлечь-контекст-сервисов)
  - [Шаг 6: Заполнить Контекст ревью](#шаг-6-заполнить-контекст-ревью)
  - [Шаг 7: Валидация](#шаг-7-валидация)
  - [Шаг 8: Обновить индекс](#шаг-8-обновить-индекс)
  - [Шаг 9: Отчёт](#шаг-9-отчёт)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Создаётся при WAITING.** `review.md` создаётся в момент Plan Dev → WAITING — до начала разработки. Разработчик видит что будет проверяться ещё до написания кода. Итерации заполняются позже — при статусе цепочки REVIEW (через `/review`).

> **Без Clarify.** Создание review.md полностью автоматизировано: LLM читает цепочку документов и заполняет Контекст ревью без интерактивных вопросов.

> **Один review.md на ветку.** Файл — общий для всех сервисов изменения. Мультисервисность фиксируется через подразделы `### {svc}`.

> **Контекст ревью — неизменяем после создания.** Секция `## Контекст ревью` заполняется однократно при создании и не правится вручную. Изменения постановки (CONFLICT цепочки) — через новую итерацию `/review`.

> **OPEN сразу.** review.md не проходит фазу DRAFT — создаётся со `status: OPEN`.

---

## Шаги

### Шаг 1: Проверить условия запуска

**SSOT:** [standard-review.md § 1](./standard-review.md#1-назначение)

1. Определить ветку: `git branch --show-current` → `NNNN-{topic}`
2. Проверить, что папка `specs/analysis/NNNN-{topic}/` существует
3. Проверить, что `plan-dev.md` существует в папке
4. Проверить статус `plan-dev.md` — убедиться, что `status: WAITING`. Для проверки можно использовать `chain_status.py` (SSOT статусов):
   ```python
   from chain_status import ChainManager
   mgr = ChainManager("NNNN")
   statuses = mgr.status()  # → {"plan-dev": "WAITING", ...}
   ```

**Если `status` ≠ `WAITING`:** остановиться. `/review-create` вызывается только при WAITING.

### Шаг 2: Идемпотентность

Проверить, существует ли `specs/analysis/NNNN-{topic}/review.md`.

**Если файл существует:**
- Сообщить пользователю: "`review.md` уже создан для этой ветки."
- Предложить запустить `/review` для добавления новой итерации.
- Завершить воркфлоу.

### Шаг 3: Создать файл из шаблона

```bash
python specs/.instructions/.scripts/create-review-file.py NNNN-{topic}
```

Скрипт создаёт `specs/analysis/NNNN-{topic}/review.md` из шаблона [standard-review.md § 7](./standard-review.md#7-шаблон) со всеми плейсхолдерами.

**Если скрипт недоступен:** создать файл вручную по шаблону из [standard-review.md § 7](./standard-review.md#7-шаблон).

### Шаг 4: Заполнить frontmatter

**SSOT:** [standard-review.md § 3](./standard-review.md#3-frontmatter)

Прочитать `discussion.md` — взять `milestone`.

| Поле | Значение |
|------|----------|
| `description` | `Ревью кода для {NNNN}-{topic}.` |
| `standard` | `specs/.instructions/analysis/review/standard-review.md` |
| `standard-version` | `v1.2` |
| `parent` | `specs/analysis/{NNNN}-{topic}/plan-dev.md` |
| `index` | `specs/analysis/README.md` |
| `milestone` | Из `discussion.md` frontmatter |
| `status` | `OPEN` |

Также заполнить заголовок документа и мета-строки:
- `# review: NNNN {Тема}` — тема из имени папки (kebab-case → Title Case)
- `**Ветка:** NNNN-{topic}`
- `**Base:** main`

### Шаг 5: Извлечь контекст сервисов

```bash
python specs/.instructions/.scripts/extract-svc-context.py specs/analysis/NNNN-{topic}/design.md
```

Скрипт парсит SVC-N из `design.md` и выводит JSON:

```json
{
  "services": [
    {
      "name": "{svc}",
      "critical_level": "critical-{level}",
      "sections": [
        {"id": "§ 2", "title": "API контракты", "changes": "ADDED: ..."},
        {"id": "§ 9", "title": "Planned Changes", "changes": "эталон P1-сверки"}
      ]
    }
  ],
  "technologies": ["{tech1}", "{tech2}"]
}
```

**Если скрипт недоступен:** прочитать `design.md` вручную — найти все секции `## SVC-N` и извлечь:
- Имя сервиса из заголовка SVC-N
- Criticality level из `specs/docs/{svc}.md § 1` (или из SVC-N если указан)
- Список §§ с изменениями (только те, где есть Planned Changes)
- Список технологий из `specs/docs/{svc}.md § Tech Stack`

### Шаг 6: Заполнить Контекст ревью

**SSOT:** [standard-review.md § 5.1](./standard-review.md#51-контекст-ревью-заполняется-при-review-create)

Используя данные из шага 5, заполнить секцию `## Контекст ревью`:

#### 6.1 Постановка

Таблица с путями к 4 документам цепочки:

| Документ | Путь |
|----------|------|
| Discussion | `specs/analysis/{branch}/discussion.md` |
| Design | `specs/analysis/{branch}/design.md` |
| Plan Tests | `specs/analysis/{branch}/plan-test.md` |
| Plan Dev | `specs/analysis/{branch}/plan-dev.md` |

#### 6.2 Блоки сервисов

Для каждого сервиса из JSON (шаг 5) создать блок `### {svc} (critical-{level})`:

```markdown
### {svc} (critical-{level})

| Секция | Путь | Что проверяем |
|--------|------|----------------|
| § 2 API контракты | `specs/docs/{svc}.md#api-контракты` | {changes из § 2} |
| § 9 Planned Changes | `specs/docs/{svc}.md#planned-changes` | **Эталон для P1-сверки** |
```

- Включать только §§ с реальными изменениями (есть в SVC-N design.md)
- `§ 9 Planned Changes` включается всегда — это эталон P1-сверки
- `§ 8 Автономия` включается если у сервиса есть автономные решения
- Колонка "Что проверяем" — кратко из Planned Changes (ADDED/MODIFIED/REMOVED)

#### 6.3 Системная документация

```markdown
### Системная документация

- `specs/docs/.system/overview.md`
- `specs/docs/.system/conventions.md`
- `specs/docs/.system/testing.md`
- `specs/docs/.system/infrastructure.md` *(при изменениях в platform/)*
```

`infrastructure.md` включается только если затронуты `platform/` изменения (есть INFRA TASK-N в plan-dev.md).

#### 6.4 Tech-стандарты

Из JSON (шаг 5) — таблица технологий:

```markdown
### Tech-стандарты

| Технология | Стандарт |
|------------|----------|
| {tech} | `specs/docs/.technologies/standard-{tech}.md` |
```

Только технологии, для которых существует `specs/docs/.technologies/standard-{tech}.md`.

#### 6.5 Процесс разработки

```markdown
### Процесс разработки

- [validation-development.md](/.github/.instructions/development/validation-development.md)
```

Включается всегда — чек-лист процесса разработки (тесты, линт, сборка, зависимости, полнота реализации).

### Шаг 7: Валидация

```bash
python specs/.instructions/.scripts/validate-analysis-review.py specs/analysis/NNNN-{topic}/review.md
```

**Если скрипт недоступен:** пройти чек-лист из [validation-review.md](./validation-review.md).

На этом этапе ожидаемо отсутствие итераций (`status: OPEN`, `## Итерация N` не должно быть).

### Шаг 8: Обновить индекс

Обновить `specs/analysis/README.md`:

**8.1. Dashboard статусов** — только через скрипт:

```bash
python specs/.instructions/.scripts/analysis-status.py --update
```

**ЗАПРЕЩЕНО** редактировать блок `<!-- BEGIN:analysis-status -->...<!-- END:analysis-status -->` вручную.

### Шаг 9: Отчёт

```
Создан review.md: specs/analysis/NNNN-{topic}/review.md

Статус: OPEN

Контекст ревью:
- Постановка: 4 документа
- Сервисы: {N} блоков ({список сервисов})
- Технологии: {список технологий}

Следующий шаг: разработчик изучает Контекст ревью, затем запускает /review по завершении задач.
```

---

## Чек-лист

### Подготовка
- [ ] Ветка определена (`git branch --show-current`)
- [ ] `plan-dev.md` существует и `status: WAITING`
- [ ] `review.md` не существует (идемпотентность)

### Создание файла
- [ ] Файл создан из шаблона (`create-review-file.py` или вручную)
- [ ] Frontmatter заполнен (все 7 полей)
- [ ] Заголовок и мета-строки заполнены

### Контекст ревью
- [ ] `extract-svc-context.py` выполнен (или ручной парсинг)
- [ ] `### Постановка` заполнена (4 строки)
- [ ] Блоки `### {svc} (critical-{level})` созданы для всех сервисов
- [ ] Только §§ с изменениями (+ § 9 всегда)
- [ ] `### Системная документация` заполнена
- [ ] `### Процесс разработки` заполнена
- [ ] `### Tech-стандарты` заполнена (только существующие стандарты)

### Индекс
- [ ] Dashboard обновлён (`analysis-status.py --update`)

### Проверка
- [ ] Валидация пройдена
- [ ] Отчёт выведен

---

## Примеры

### Создание review.md для одного сервиса

```
Ветка: 0001-oauth2-authorization
plan-dev.md: status=WAITING

1. extract-svc-context.py → {services: [{name: "auth", critical_level: "critical-high",
   sections: [{id: "§ 2", changes: "ADDED: POST /auth/token, POST /auth/refresh"},
              {id: "§ 3", changes: "ADDED: таблица refresh_tokens"},
              {id: "§ 9", changes: "эталон P1-сверки"}]}],
   technologies: ["Python", "PostgreSQL"]}

2. Создан review.md:
   - Frontmatter: status=OPEN, parent=plan-dev.md, milestone=v1.0
   - ### Постановка — 4 документа
   - ### auth (critical-high) — § 2, § 3, § 9
   - ### Системная документация
   - ### Tech-стандарты: Python, PostgreSQL

3. Валидация: OK

4. README обновлён: dashboard (Review = OP)
```

### Создание review.md для двух сервисов

```
Ветка: 0002-payment-integration
plan-dev.md: status=WAITING

1. extract-svc-context.py → {services: [
     {name: "payment", critical_level: "critical-high", sections: [§ 2, § 3, § 9]},
     {name: "gateway", critical_level: "critical-medium", sections: [§ 2, § 9]}
   ], technologies: ["Python", "Stripe SDK"]}

2. Создан review.md:
   - ### payment (critical-high) — § 2, § 3, § 9
   - ### gateway (critical-medium) — § 2, § 9

3. Валидация: OK

4. README обновлён: dashboard (Review = OP)
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [create-review-file.py](../../.scripts/create-review-file.py) | Создание файла review.md из шаблона | Этот документ |
| [extract-svc-context.py](../../.scripts/extract-svc-context.py) | Извлечение сервисного контекста из design.md | Этот документ |
| [validate-analysis-review.py](../../.scripts/validate-analysis-review.py) | Валидация созданного документа (шаг 7) | [validation-review.md](./validation-review.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/review-create](/.claude/skills/review-create/SKILL.md) | Создание review.md | Этот документ |
