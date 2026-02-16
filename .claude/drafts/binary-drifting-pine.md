# План: Обогащение заглушек сервисных документов данными из Impact/Design

## Контекст

Сейчас при Design → WAITING создаётся заглушка `services/{svc}.md` с секциями 2-6 как `*Заполняется при ADR → DONE.*`. Это слишком мало — Impact и Design уже содержат данные об API, Data Model, зависимостях. Решение: заполнять секции 2 (API контракты), 3 (Data Model), 5 (Внешние зависимости) предварительными данными с маркером `*Предварительно (Design → WAITING). Финализируется при ADR → DONE.*`. Секции 4 (Code Map) и 6 (Границы автономии LLM) остаются placeholder.

Также нужна явная связь в `create-design.md` шаг 9 — маппинг данных из Design SVC-N в `/service-create`.

## Файлы и изменения

### 1. `specs/.instructions/living-docs/service/standard-service.md`

- **§ 5 таблица секций:** колонка "Обновляется при" для секций 2, 3, 5 → добавить `Design → WAITING (предварительно)`
- **§ 9.1 шаблон заглушки:** заменить placeholder секций 2, 3, 5 на таблицы с маркером Planned
- **§ 10 чек-лист:** обновить "Режим заглушки" — секции 2, 3, 5 содержат предварительные данные ИЛИ placeholder
- **§ 11.1 пример auth:** обновить фазу 1 (заглушка) — показать предварительные таблицы

### 2. `specs/.instructions/living-docs/service/create-service.md`

- **Шаг 1:** расширить — извлечь API-N, DATA-N из Impact SVC-N + INT-N/Dependencies из Design
- **Шаг 3:** заполнять секции 2, 3, 5 предварительными данными (маппинг: Impact API-N → API контракты, Impact DATA-N → Data Model, Design Dependencies/INT-N → Внешние зависимости)
- **Чек-лист:** обновить пункт о секциях 2-6

### 3. `specs/.instructions/design/create-design.md`

- **Шаг 9, артефакт 3:** добавить явный маппинг параметров для `/service-create`:
  - `svc` = имя из SVC-N
  - `description` = описание из SVC-N
  - `api` = API-N из parent Impact
  - `data` = DATA-N из parent Impact
  - `dependencies` = Dependencies из Design SVC-N + INT-N

### 4. `specs/.instructions/living-docs/service/validation-service.md`

- Обновить правила режима заглушки: секции 2, 3, 5 могут содержать предварительные таблицы с маркером Planned (не только placeholder)

### 5. `specs/.instructions/.scripts/validate-service.py` (если существует)

- Добавить `PLANNED_MARKER` для валидации
- Режим заглушки: секции 2, 3, 5 → или placeholder или таблица с Planned маркером

### 6. `.claude/skills/service-create/SKILL.md`

- Добавить параметры `--design`, `--impact` для передачи источников данных

### 7. `specs/.instructions/living-docs/service/modify-service.md`

- Добавить сценарий: при ADR → DONE секции с Planned маркером → финальные данные (убрать маркер)

## Маппинг данных

```
Impact SVC-N → API-N        →  Service § 2 API контракты (предварительно)
Impact SVC-N → DATA-N       →  Service § 3 Data Model (предварительно)
Design SVC-N → Dependencies →  Service § 5 Внешние зависимости (предварительно)
Design INT-N → Contract     →  Service § 5 (дополнительно)
```

## Маркер

```markdown
*Предварительно (Design → WAITING). Финализируется при ADR → DONE.*
```

## Верификация

1. Обновить standard-service.md → `/migration-create` + `/migration-validate`
2. Проверить validate-service.py на новый формат заглушки
3. Убедиться что пример § 11.1 соответствует новому шаблону
