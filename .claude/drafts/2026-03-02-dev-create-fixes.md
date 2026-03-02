---
description: Исправления процесса /dev-create — порядок ветки, SVC-метки, inline маппинг, src/ папки.
status: active
---

# Исправления /dev-create 0001

Обнаружены проблемы при первом прогоне `/dev-create 0001`. Ниже — список исправлений с приоритетами.

## FIX-0: Порядок ветки (коммит до ветки)

**Проблема:** Изменения analysis chain (WAITING → RUNNING, маппинг Issues) сделаны на ветке `0001-task-dashboard` вместо main. По логике: specs/analysis/ — это метаданные проекта, они должны быть в main.

**Исправление:**
1. Удалить ветку `0001-task-dashboard` (локально)
2. Вернуться на main
3. Закоммитить изменения (RUNNING + маппинг) в main
4. Запушить main
5. Пересоздать ветку `0001-task-dashboard` от обновлённого main

**Затрагивает:** `create-development.md` — добавить явный шаг "Закоммитить и запушить в main ПЕРЕД созданием ветки". Текущий порядок шагов (3: Issues → 4: Milestone → 5: Branch → 6: RUNNING) не упоминает коммит между шагами 5 и 6.

**Предложение для стандарта:** Переупорядочить шаги:
- Шаг 3: Создать Issues
- Шаг 4: Milestone
- Шаг 5: Перевести в RUNNING (frontmatter changes)
- Шаг 6: Коммит + Push в main
- Шаг 7: Создать ветку (от свежего main)

## FIX-1: Inline маппинг Issue в TASK-N

**Проблема:** Номера GitHub Issues находятся в отдельной таблице "Маппинг GitHub Issues" внизу plan-dev.md. Неудобно — нужно скроллить, чтобы понять какой Issue к какому TASK-N.

**Исправление:** Добавить поле `Issue:` к каждому TASK-N заголовку или метаданным.

**Формат (выбран вариант A — поле в метаданных, полная ссылка):**
```markdown
#### TASK-2: Scaffold task-сервиса и Prisma-схема
- **Сложность:** 5/10
- **Приоритет:** high
- **Зависимости:** TASK-1
- **TC:** TC-1
- **Источник:** SVC-1 § 3, SVC-1 § 5
- **Issue:** [#43](https://github.com/NSEvteev/project_template/issues/43)
```

**Затрагивает:**
- `standard-plan-dev.md` — добавить поле Issue к формату TASK-N
- `plan-dev.md` (0001) — переписать все TASK-N с inline Issue
- Таблица "Маппинг GitHub Issues" — удалить или оставить как сводку

## FIX-2: Папки src/ и SVC-метки → часть /docs-sync

**Проблема:** Папки `src/task/`, `src/auth/`, `src/frontend/` не созданы. Метки `svc:task`, `svc:auth`, `svc:frontend` не существуют. Оба артефакта привязаны к сервису и должны создаваться вместе с `specs/docs/{svc}.md`.

**Решение:** `/docs-sync` создаёт **всё для сервиса**:
- `specs/docs/{svc}.md` — документация (уже есть)
- `src/{svc}/` — папка кода (добавить)
- `svc:{name}` — GitHub label (добавить)

**Точные правки `create-docs-sync.md`:**
- Шаг 2 "Определить scope": после извлечения списка сервисов из Design добавить подшаг:
  - Для каждого нового сервиса: `mkdir -p src/{svc}` (если не существует)
  - Для каждого нового сервиса: создать label `svc:{svc}` через `gh label create` (если не существует)
  - Добавить `svc:{svc}` в `labels.yml` секцию SVC (через `/labels-modify` или напрямую)
- Шаг 8 "Отчёт": добавить в вывод — созданные папки src/, созданные SVC-метки

**Точные правки `labels.yml`:**
- Добавить категорию SVC (если отсутствует):
```yaml
SVC:
  color: "1d76db"
  description_prefix: "🔷"
  labels: []  # Заполняется динамически при /docs-sync
```

**Затрагивает:**
- `create-docs-sync.md` — шаг 2 + шаг 8
- `labels.yml` — секция SVC
- Артефакты draft — добавить src/ папки и svc-метки

## FIX-3: SVC-метки на Issues (следствие FIX-2)

**Проблема:** SVC-метки не были созданы при /docs-sync (FIX-2). Как следствие — 20 Issues без SVC-меток.

**Исправление (ретроактивное для 0001):**
1. Создать метки `svc:task`, `svc:auth`, `svc:frontend` через `/labels-modify`
2. Добавить метки на Issues:
   - `svc:task`: #43, #44, #45, #46, #47, #48
   - `svc:auth`: #49, #50, #51, #52, #53
   - `svc:frontend`: #54, #55, #56, #57, #58, #59
   - Без SVC: #42 (INFRA)
   - Все три: #60, #61 (system tests — затрагивают все сервисы)

**После исправления FIX-2 в стандарте** — этот шаг будет не нужен, т.к. /docs-sync создаст метки заранее, а /dev-create при создании Issues уже сможет их использовать.

## FIX-4: Автономность создания Issues

**Проблема:** Каждый `gh issue create` требовал подтверждения пользователя в UI (Bash permission).

**Статус:** Это не проблема процесса, а настройка permissions. SSOT `create-issue.md` уже говорит "НЕ спрашивать подтверждения". Пользователь может настроить auto-allow для `gh issue create` в permissions.

---

## Порядок исправлений

### Сейчас (ретроактивно для 0001):
1. **FIX-3** — Создать SVC-метки, добавить на Issues
2. **FIX-0** — Удалить ветку, вернуться на main, закоммитить, запушить
3. **FIX-1** — Inline маппинг (изменить стандарт + plan-dev.md) — в том же коммите
4. **FIX-0 финал** — Пересоздать ветку от обновлённого main

### Потом (изменение стандартов для будущих цепочек):
5. **FIX-2** — Обновить `create-docs-sync.md`: добавить создание `src/{svc}/` и `svc:` меток
6. **FIX-0** — Обновить `create-development.md`: порядок шагов (RUNNING → коммит → ветка)

FIX-4 не требует изменений в коде (настройка permissions).

---

## Точные правки create-development.md (FIX-0 стандарт)

**Текущий порядок шагов:**
1. Проверить готовность цепочки
2. Подтверждение пользователя
3. Создать GitHub Issues
4. Создать/привязать Milestone
5. Создать ветку
6. Перевести цепочку в RUNNING
7. Отчёт
8. Предложить начать разработку

**Новый порядок шагов:**
1. Проверить готовность цепочки
2. Подтверждение пользователя
3. Создать GitHub Issues
4. Создать/привязать Milestone
5. Перевести цепочку в RUNNING (frontmatter → RUNNING, README dashboard)
6. **Коммит + Push в main** (новый шаг)
7. Создать ветку (от свежего main)
8. Отчёт
9. Предложить начать разработку

**Логика:** Шаги 3-5 меняют файлы в main (plan-dev.md маппинг, frontmatter status, README). Шаг 6 фиксирует. Шаг 7 создаёт ветку от чистого main.

---

## Решённые вопросы

**OQ-1:** FIX-1 → **Вариант A** (поле `- **Issue:** [#N](url)` в метаданных, полная ссылка). Единообразно с другими полями, кликабельно в любом контексте.

---

## Tasklist

TASK 1: Создать SVC-метки на GitHub
  description: >
    Драфт: FIX-3.
    Создать метки `svc:task`, `svc:auth`, `svc:frontend` через `/labels-modify`.
    Добавить секцию SVC в labels.yml.
    Проверить: `gh label list | grep svc:`.
  activeForm: Создаю SVC-метки

TASK 2: Добавить SVC-метки на существующие Issues
  description: >
    Драфт: FIX-3.
    `gh issue edit` для всех 20 Issues:
    svc:task → #43-#48, svc:auth → #49-#53, svc:frontend → #54-#59.
    #60, #61 (system) → все три метки.
    #42 (INFRA) → без SVC.
    Проверить: `/issue-validate --milestone v0.1.0`.
  activeForm: Добавляю SVC-метки на Issues

TASK 3: Вернуться на main (удалить ветку)
  description: >
    Драфт: FIX-0.
    `git checkout main && git branch -D 0001-task-dashboard`.
    Все незакоммиченные изменения переносятся на main (modified files).
  activeForm: Переключаюсь на main

TASK 4: Обновить standard-plan-dev.md — добавить поле Issue
  description: >
    Драфт: FIX-1.
    Изменить `standard-plan-dev.md`:
    - § "Формат задачи (TASK-N)": добавить поле Issue (опц., заполняется при /dev-create)
    - § "Маппинг GitHub Issues": обновить описание — номера теперь inline в TASK-N
    - Шаблон: добавить `- **Issue:** —` (заполнится позже)
    - Чек-лист: обновить
    Запустить `/migration-create` после.
  activeForm: Обновляю standard-plan-dev.md

TASK 5: Обновить plan-dev.md 0001 — inline Issue + удалить таблицу
  description: >
    Драфт: FIX-1.
    Добавить `- **Issue:** #N` к каждому TASK-1..TASK-20.
    Удалить отдельную таблицу "Маппинг GitHub Issues" (номера теперь inline).
    Оставить секцию с описанием процесса маппинга (без конкретных номеров — они в TASK-N).
  activeForm: Обновляю plan-dev.md 0001

TASK 6: Обновить create-development.md — порядок шагов
  description: >
    Драфт: FIX-0 стандарт.
    Переупорядочить шаги: RUNNING (шаг 5) → Коммит+Push (шаг 6) → Ветка (шаг 7).
    Добавить новый Шаг 6 "Коммит и Push в main" с описанием и командами.
    Обновить нумерацию шагов 5-8 → 5-9.
  activeForm: Обновляю create-development.md

TASK 7: Обновить create-docs-sync.md — src/ папки + svc-метки
  description: >
    Драфт: FIX-2.
    Шаг 2 "Определить scope": добавить подшаги mkdir + gh label create.
    Шаг 8 "Отчёт": добавить вывод созданных src/ и svc-меток.
  activeForm: Обновляю create-docs-sync.md

TASK 8: Коммит + Push в main
  description: >
    Драфт: FIX-0.
    Закоммитить все изменения:
    - specs/analysis/0001-task-dashboard/ (RUNNING + inline Issues)
    - specs/analysis/README.md (dashboard)
    - standard-plan-dev.md + миграция
    - create-development.md
    - create-docs-sync.md
    - labels.yml
    - drafts/
    Push в main.
  activeForm: Коммичу в main

TASK 9: Пересоздать ветку 0001-task-dashboard
  description: >
    Драфт: FIX-0 финал.
    `git checkout -b 0001-task-dashboard` от свежего main.
    `python validate-branch-name.py` — валидация.
  activeForm: Пересоздаю ветку

TASK 10: Валидация
  description: >
    Проверить:
    - `gh label list | grep svc:` — 3 метки
    - `/issue-validate --milestone v0.1.0` — все Issues валидны
    - `git branch --show-current` = 0001-task-dashboard
    - `git log main --oneline -3` — коммит виден в main
    - plan-dev.md: inline Issue, нет отдельной таблицы
    - Обновить artifacts draft
  activeForm: Валидация
