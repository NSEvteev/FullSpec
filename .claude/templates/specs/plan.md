# План: {TITLE}

## Метаданные

| Поле | Значение |
|------|----------|
| **Статус** | 📝 DRAFT |
| **ADR** | [{ADR_NUMBER}-{ADR_SLUG}](/specs/services/{SERVICE}/adr/{ADR_NUMBER}-{ADR_SLUG}.md) |
| **Сервис** | {SERVICE} |
| **Дата** | {DATE} |

## Задачи

### Фаза 1: {PHASE_1_NAME}
- [ ] {TASK_1_1}
- [ ] {TASK_1_2}

### Фаза 2: {PHASE_2_NAME}
- [ ] {TASK_2_1}
- [ ] {TASK_2_2}
- [ ] {TASK_2_3}

### Фаза 3: Тесты
- [ ] Unit-тесты для {COMPONENT}
- [ ] Integration-тесты для endpoints

### Фаза 4: Документация
- [ ] Обновить `architecture.md`
- [ ] Обновить API docs

## Зависимости

| Задача | Зависит от |
|--------|------------|
| {PHASE_2_NAME} | {PHASE_1_NAME} |
| Тесты | {PHASE_2_NAME} |
| Документация | — |

## Оценка

| Фаза | Сложность |
|------|-----------|
| {PHASE_1_NAME} | Low |
| {PHASE_2_NAME} | Medium |
| Тесты | Medium |
| Документация | Low |

## GitHub Issues

| Issue | Фаза | Статус |
|-------|------|--------|
| _(создаются после APPROVED)_ | — | — |

## Критерий готовности

> Условия для перевода в DONE

- [ ] Все задачи выполнены
- [ ] Тесты пройдены
- [ ] Code review пройден
- [ ] Документация обновлена
- [ ] `architecture.md` обновлён

## Связанные документы

- ADR: [{ADR_NUMBER}-{ADR_SLUG}](/specs/services/{SERVICE}/adr/{ADR_NUMBER}-{ADR_SLUG}.md)
- Impact: _(через ADR)_

## История

| Дата | Событие |
|------|---------|
| {DATE} | Создан план |

---

<!--
## Пример заполнения

# План: JWT Migration

## Метаданные

| Поле | Значение |
|------|----------|
| **Статус** | 🔍 REVIEW |
| **ADR** | [001-jwt-tokens](/specs/services/auth/adr/001-jwt-tokens.md) |
| **Сервис** | auth |
| **Дата** | 2025-01-21 |

## Задачи

### Фаза 1: База данных
- [ ] Создать миграцию для таблицы `refresh_tokens`
- [ ] Добавить индексы

### Фаза 2: Backend
- [ ] Обновить `TokenService`
- [ ] Добавить endpoint `POST /auth/refresh`
- [ ] Добавить endpoint `DELETE /auth/sessions`

### Фаза 3: Тесты
- [ ] Unit-тесты для `TokenService`
- [ ] Integration-тесты для endpoints

### Фаза 4: Документация
- [ ] Обновить `architecture.md`
- [ ] Обновить API docs

## Зависимости

| Задача | Зависит от |
|--------|------------|
| Backend | База данных |
| Тесты | Backend |
| Документация | — |

## Оценка

| Фаза | Сложность |
|------|-----------|
| База данных | Low |
| Backend | Medium |
| Тесты | Medium |
| Документация | Low |

## GitHub Issues

| Issue | Фаза | Статус |
|-------|------|--------|
| [#123](link) | База данных | Open |
| [#124](link) | Backend | Open |
| [#125](link) | Тесты | Open |

## Критерий готовности

- [x] Все задачи выполнены
- [x] Тесты пройдены
- [x] Code review пройден
- [x] Документация обновлена
- [x] `architecture.md` обновлён

## Связанные документы

- ADR: [001-jwt-tokens](/specs/services/auth/adr/001-jwt-tokens.md)
- Impact: [001-auth-flow](/specs/impact/001-auth-flow.md)

## История

| Дата | Событие |
|------|---------|
| 2025-01-21 | Создан план |
| 2025-01-25 | APPROVED → RUNNING |
| 2025-01-30 | RUNNING → DONE |
-->
